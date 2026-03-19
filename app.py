import os
import numpy as np
import base64
try:
    import tensorflow as tf
except ImportError:
    tf = None
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import logging
from src import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Road Pothole Detection API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable for the model
model = None

def load_trained_model():
    global model
    model_path = os.path.join(config.MODELS_DIR, "best_model.h5")
    
    if os.path.exists(model_path):
        try:
            # Load model with custom metrics if necessary, but compile=False is safer for loading weights
            model = tf.keras.models.load_model(model_path, compile=False)
            logger.info(f"Successfully loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    else:
        logger.warning(f"Model file not found at {model_path}. Predictions will use mock data until a model is trained.")

# Load model on startup
@app.on_event("startup")
async def startup_event():
    load_trained_model()

@app.get("/")
async def root():
    return {"message": "Road Pothole Detection API is running"}

def calculate_rps_score(mask):
    """Calculates Road Pothole Severity (RPS) score based on weighted mask density."""
    # mask: (H, W) with values 0, 1, 2, 3
    rps_score = 0
    total_pixels = mask.size
    
    for class_idx, weight in enumerate(config.RPS_WEIGHTS.values()):
        if weight == 0: continue
        pixels_count = np.sum(mask == class_idx)
        rps_score += (pixels_count / total_pixels) * weight * 100
        
    return round(float(rps_score), 2)

def mask_to_base64(mask):
    """Converts a multi-class mask (0-3) to a base64 encoded PNG image."""
    # mask: (H, W) with values 0, 1, 2, 3
    # Multiply by 64 to make it visible (0, 64, 128, 192) or just keep as indices
    # We'll keep as raw indices 0-3 for the frontend to map
    mask_img = mask.astype(np.uint8)
    if mask_img.ndim == 3 and mask_img.shape[-1] == 1:
        mask_img = np.squeeze(mask_img, axis=-1)
    
    img = Image.fromarray(mask_img, mode='L')
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model
    
    # 1. Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # 2. Read and preprocess image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Resize to match model input shape (224, 224)
        image_resized = image.resize((config.INPUT_SHAPE[0], config.INPUT_SHAPE[1]))
        
        # Convert to numpy array and normalize
        img_array = np.array(image_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # 3. Perform prediction
        if model is not None:
            predictions = model.predict(img_array)
            # Dual-head model returns [cls_output, seg_output]
            cls_pred = predictions[0][0]
            seg_pred = predictions[1][0] # (H, W, 4)
            
            class_idx = np.argmax(cls_pred)
            confidence = float(cls_pred[class_idx])
            prediction_class = config.CLASSES[class_idx]
            
            # Post-process mask: Argmax over channels to get (H, W) with 0-3
            mask = np.argmax(seg_pred, axis=-1)
            rps_score = calculate_rps_score(mask)
            mask_base64 = mask_to_base64(mask)
            
        else:
            # Mock response if model is not loaded (for testing frontend)
            import random
            prediction_class = random.choice(config.CLASSES)
            confidence = random.uniform(0.85, 0.99)
            
            # Create a mock multi-class mask
            mock_mask = np.zeros((config.INPUT_SHAPE[0], config.INPUT_SHAPE[1]), dtype=np.uint8)
            if prediction_class != "normal":
                yy, xx = np.mgrid[:224, :224]
                # Different circles for different severity
                if prediction_class == "pothole":
                    # Deep pothole (index 3)
                    circle = (xx - 112)**2 + (yy - 112)**2 < 50**2
                    mock_mask[circle] = 3
                else:
                    # Cracks (index 1 or 2)
                    circle1 = (xx - 80)**2 + (yy - 80)**2 < 30**2
                    mock_mask[circle1] = 1
                    circle2 = (xx - 150)**2 + (yy - 150)**2 < 40**2
                    mock_mask[circle2] = 2
            
            rps_score = calculate_rps_score(mock_mask)
            mask_base64 = mask_to_base64(mock_mask)
            
            logger.info("Using mock multi-class prediction and mask.")

        return {
            "class": prediction_class.capitalize(),
            "confidence": confidence,
            "rps_score": rps_score,
            "mask": mask_base64,
            "seg_classes": config.SEG_CLASSES
        }

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
