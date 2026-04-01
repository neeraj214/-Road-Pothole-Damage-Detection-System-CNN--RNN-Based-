import os
from pathlib import Path

# Base Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
TRAIN_DIR = os.path.join(RAW_DATA_DIR, "train")
VAL_DIR = os.path.join(RAW_DATA_DIR, "val")
MASK_DIR = os.path.join(DATA_DIR, "processed", "masks")
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Model Configuration
MODEL_NAME = "pothole_detector_mobilenetv2_v4"
MODEL_FILENAME = "best_model_dual_v4.keras"
INPUT_SHAPE = (160, 160, 3) # Reduced from 256 for RTX 2050 4GB OOM fix
BATCH_SIZE = 8 # Reduced from 16 to fit in memory
ACCUMULATION_STEPS = 2 # Simulate effective batch size of 16
EPOCHS = 30
LEARNING_RATE = 0.001

# Training Parameters
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42

# Classification Classes (Image-level)
CLASSES = ["normal", "crack", "pothole"]
NUM_CLASSES = len(CLASSES)

# Class Weights (Handled dynamically in train.py, but defined here for reference)
# Usually Pothole and Crack are minority classes
CLASS_WEIGHTS = {0: 1.0, 1: 2.0, 2: 3.0} 

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
    for path in [DATA_DIR, RAW_DATA_DIR, TRAIN_DIR, VAL_DIR, MASK_DIR, MODELS_DIR, RESULTS_DIR]:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

if __name__ == "__main__":
    create_dirs()
    print("Project directories verified.")
