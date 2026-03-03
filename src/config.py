import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"

# Model Configuration
MODEL_NAME = "pothole_detector_mobilenetv2"
INPUT_SHAPE = (224, 224, 3)
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.0001

# Training Parameters
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42

# Classes
CLASSES = ["pothole", "crack", "normal"]
NUM_CLASSES = len(CLASSES)

# Augmentation Config
AUGMENTATION_PARAMS = {
    "rotation_range": 20,
    "width_shift_range": 0.2,
    "height_shift_range": 0.2,
    "shear_range": 0.2,
    "zoom_range": 0.2,
    "horizontal_flip": True,
    "fill_mode": "nearest"
}

def create_dirs():
    """Ensure all required directories exist."""
    for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR]:
        path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    create_dirs()
    print("Project directories verified.")
