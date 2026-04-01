import tensorflow as tf
import numpy as np
import cv2
import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from src.utils import bce_dice_loss
from src import config

# GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(f"GPU config error: {e}")

# Allow MODEL_PATH override via environment variable (useful for Render deployment)
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    os.path.join(config.MODELS_DIR, "best_model_dual_v6_deeper_tf")
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None

import glob

def find_model_path(base_dir):
    matches = glob.glob(
        os.path.join(base_dir, "**", "saved_model.pb"),
        recursive=True
    )
    if matches:
        return os.path.dirname(matches[0])
    return None

def load_model():
    """Download (if needed) then load the Keras model. Sets model=None on any failure."""
    global model

    # Attempt to download model from HF Model Hub if not present locally
    try:
        from download_model import download_model
        download_model()
    except ImportError:
        # download_model.py not present (local dev without hf_space/ in path)
        pass
    except Exception as e:
        logger.warning(f"download_model failed (non-fatal): {e}")

    actual_path = find_model_path(config.MODELS_DIR)
    if not actual_path:
        logger.warning("=" * 60)
        logger.warning(f"Model not found in {config.MODELS_DIR}")
        logger.warning("API will start but /predict will return 503.")
        logger.warning("Set MODEL_URL env var to auto-download from HF Model Hub.")
        logger.warning("=" * 60)
        model = None
        return

    try:
        model = tf.keras.models.load_model(
            actual_path,
            custom_objects={"bce_dice_loss": bce_dice_loss},
            compile=False
        )
        logger.info(f"Model loaded successfully from {actual_path}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model = None

load_model()

app = FastAPI(
    title="Road Pothole Detection API",
    description="Detects potholes, cracks, and normal road surfaces",
    version="2.0"
)

# ALLOWED_ORIGINS env var lets you restrict CORS in production.
# Example: ALLOWED_ORIGINS=https://my-app.vercel.app,https://my-other-domain.com
# Default is "*" (allow all) for local dev / initial deployment.
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_image(image_bytes: bytes, img_size: int = 160):
    """
    Preprocesses image bytes for MobileNetV2 inference.
    Must match training preprocessing exactly.
    """
    # Decode image bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image")
    
    # Convert BGR to RGB (cv2 loads as BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize to model input size
    img = cv2.resize(img, (img_size, img_size))
    
    # Apply MobileNetV2 preprocessing — scales to [-1, 1]
    # DO NOT use img / 255.0 — this is wrong for MobileNetV2
    img = preprocess_input(img.astype(np.float32))
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    return img

CLASS_NAMES = ["Normal", "Crack", "Pothole"]
SEG_CLASS_NAMES = ["Background", "Hairline Crack", "Alligator Crack", "Deep Pothole"]

# Repair Priority Score weights (from config)
RPS_WEIGHTS = [0.0, 1.0, 2.5, 5.0]

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Accepts an image file and returns:
    - Predicted road condition class
    - Confidence scores for all 3 classes
    - Dominant segmentation class
    - Repair Priority Score (RPS)
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"File must be an image. Got: {file.content_type}"
        )
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Preprocess
        img_size = config.INPUT_SHAPE[0]
        processed_img = preprocess_image(image_bytes, img_size)
        
        # Run inference
        predictions = model(processed_img, training=False)
        cls_pred = predictions[0].numpy()[0]   # shape: (3,)
        seg_pred = predictions[1].numpy()[0]   # shape: (H, W, 4)
        
        # Classification result
        predicted_class_idx = int(np.argmax(cls_pred))
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = float(cls_pred[predicted_class_idx])
        
        # All class confidences
        class_confidences = {
            CLASS_NAMES[i]: round(float(cls_pred[i]), 4)
            for i in range(len(CLASS_NAMES))
        }
        
        # Segmentation result — find dominant damage class
        seg_class_map = np.argmax(seg_pred, axis=-1)  # shape: (H, W)
        seg_pixel_counts = np.bincount(
            seg_class_map.flatten(), minlength=4
        )
        total_pixels = seg_class_map.size
        
        # Calculate damage coverage percentages
        seg_coverage = {
            SEG_CLASS_NAMES[i]: round(
                float(seg_pixel_counts[i]) / total_pixels * 100, 2
            )
            for i in range(4)
        }
        
        # Repair Priority Score
        damage_pixels = total_pixels - seg_pixel_counts[0]  # exclude background
        rps = float(np.sum([
            seg_pixel_counts[i] * RPS_WEIGHTS[i]
            for i in range(4)
        ]) / total_pixels)
        rps = round(rps, 4)
        
        # Severity label based on RPS
        # Thresholds: > 0.6 = High, 0.3–0.6 = Medium, < 0.3 = Low
        if rps > 0.6:
            severity = "High"
        elif rps >= 0.3:
            severity = "Medium"
        else:
            severity = "Low"
        
        return JSONResponse(content={
            "status": "success",
            "prediction": {
                "class": predicted_class,
                "confidence": round(confidence, 4),
                "all_confidences": class_confidences,
            },
            "segmentation": {
                "coverage_percent": seg_coverage,
                "dominant_damage": SEG_CLASS_NAMES[
                    int(np.argmax(seg_pixel_counts[1:])) + 1
                ] if damage_pixels > 0 else "None",
            },
            "repair_priority": {
                "score": rps,
                "severity": severity,
                "recommendation": (
                    "No action needed" if predicted_class == "Normal"
                    else f"Schedule {severity.lower()} priority repair"
                )
            }
        })
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "classes": CLASS_NAMES
    }

@app.get("/")
async def root():
    return {"message": "Road Pothole Detection API is running. POST to /predict"}

@app.on_event("startup")
async def startup_event():
    logger.info("Road Pothole Detection API starting up...")
    logger.info(f"Running in {'GPU' if gpus else 'CPU'} mode")
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Model loaded: {model is not None}")
    logger.info(f"Input shape: {config.INPUT_SHAPE}")
    logger.info(f"Classes: {CLASS_NAMES}")
    logger.info(f"Allowed origins: {ALLOWED_ORIGINS}")
    logger.info("API ready to accept requests.")

if __name__ == "__main__":
    import uvicorn
    # HF Spaces uses 7860; local dev fallback is 8000
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
