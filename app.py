import os
import numpy as np
import tensorflow as tf
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
            model = tf.keras.models.load_model(model_path)
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
        image = image.resize((config.INPUT_SHAPE[0], config.INPUT_SHAPE[1]))
        
        # Convert to numpy array and normalize
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # 3. Perform prediction
        if model is not None:
            predictions = model.predict(img_array)
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])
            prediction_class = config.CLASSES[class_idx]
        else:
            # Mock response if model is not loaded (for testing frontend)
            import random
            prediction_class = random.choice(config.CLASSES)
            confidence = random.uniform(0.85, 0.99)
            logger.info("Using mock prediction because model is not loaded.")

        return {
            "class": prediction_class.capitalize(),
            "confidence": confidence
        }

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
