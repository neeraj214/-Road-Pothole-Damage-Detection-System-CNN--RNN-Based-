import os
import shutil
from pathlib import Path

# Paths
RGB_DIR = Path(r"c:\Users\neera\OneDrive\Documents\Road porthole detection\temp_dataset\pothole600\training\rgb")
LABEL_DIR = Path(r"c:\Users\neera\OneDrive\Documents\Road porthole detection\temp_dataset\pothole600\training\label")
DEST_IMG_DIR = Path(r"c:\Users\neera\OneDrive\Documents\Road porthole detection\data\raw\train\pothole")
DEST_MASK_DIR = Path(r"c:\Users\neera\OneDrive\Documents\Road porthole detection\data\processed\masks")

# Create dirs if they don't exist
DEST_IMG_DIR.mkdir(parents=True, exist_ok=True)
DEST_MASK_DIR.mkdir(parents=True, exist_ok=True)

print("Moving images...")
for img_path in RGB_DIR.glob("*.png"):
    shutil.copy(img_path, DEST_IMG_DIR / img_path.name)

print("Moving and renaming masks...")
for mask_path in LABEL_DIR.glob("*.png"):
    new_mask_name = f"{mask_path.stem}_mask.png"
    shutil.copy(mask_path, DEST_MASK_DIR / new_mask_name)

print("Done! Pothole-600 dataset is now ready for training.")
