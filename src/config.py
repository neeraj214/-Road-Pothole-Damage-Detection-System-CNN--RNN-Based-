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
MODEL_FILENAME = "best_model_dual.keras"
INPUT_SHAPE = (224, 224, 3)
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.0001

# Training Parameters
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42

# Classification Classes (Image-level)
CLASSES = ["pothole", "normal"]
NUM_CLASSES = len(CLASSES)

# Segmentation Classes (Pixel-level)
# 0: Background, 1: Hairline Crack, 2: Alligator Crack, 3: Deep Pothole
SEG_CLASSES = ["background", "hairline_crack", "alligator_crack", "deep_pothole"]
NUM_SEG_CLASSES = len(SEG_CLASSES)

# Repair Priority Score (RPS) Weights
# Assign higher weight to more severe damages
RPS_WEIGHTS = {
    "background": 0.0,
    "hairline_crack": 1.0,
    "alligator_crack": 2.5,
    "deep_pothole": 5.0
}

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
