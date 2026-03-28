import os
import tensorflow as tf
import numpy as np
import logging
from src.model import build_dual_head_model
from src.data_loader import build_generators
from src import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sanity_check():
    logger.info("Starting Sanity Check...")
    
    # 1. Build Model
    img_size = config.INPUT_SHAPE[0]
    model = build_dual_head_model(img_size=img_size, freeze_base=True)
    
    # Verify layers
    layer_names = [l.name for l in model.layers]
    if "cls_output" in layer_names and "seg_output" in layer_names:
        logger.info("✅ Model layers 'cls_output' and 'seg_output' exist.")
    else:
        logger.error(f"❌ Missing layers! Found: {layer_names}")
    
    # 2. Test Generator
    data_dir = os.path.join(config.BASE_DIR, "data")
    mask_dir = config.MASK_DIR
    train_ds, _ = build_generators(data_dir, mask_dir, batch_size=2, img_size=img_size)
    
    # Get one batch
    for x, y in train_ds.take(1):
        # Image stats
        img_min = np.min(x)
        img_max = np.max(x)
        logger.info(f"📊 Input Image - Min: {img_min:.4f}, Max: {img_max:.4f}")
        if -1.1 <= img_min <= 0.1 and 0.0 <= img_max <= 1.1:
             logger.info("✅ Image normalization (preprocess_input) looks correct (approx -1 to 1).")
        else:
             logger.warning(f"⚠️ Image range unexpected: {img_min} to {img_max}")

        # Mask stats
        mask_batch = y['seg_output']
        # mask_batch is one-hot encoded (B, H, W, 4)
        mask_indices = np.argmax(mask_batch, axis=-1)
        unique_vals = np.unique(mask_indices)
        logger.info(f"📊 Mask Unique Indices: {unique_vals}")
        if np.all(unique_vals <= 3):
            logger.info("✅ Mask indices are within range [0, 3].")
        else:
            logger.error(f"❌ Mask indices out of range! Found: {unique_vals}")

if __name__ == "__main__":
    sanity_check()
