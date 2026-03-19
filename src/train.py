import os
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import logging
from src.config import create_dirs, MODELS_DIR, EPOCHS
from src.data_loader import get_data_generators
from src.model import build_model
from src import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Main training script for the Road Pothole & Damage Detection System.
    """
    # 1. Ensure models/ directory exists
    create_dirs()
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)

    # 2. Load Data Generators
    logger.info("Loading data generators...")
    try:
        train_generator, val_generator, test_generator = get_data_generators(config)
    except Exception as e:
        logger.error(f"Failed to load data generators: {e}")
        return

    # 3. Build the Model
    logger.info("Building model using build_model(config)...")
    model = build_model(config)

    # 4. Define Callbacks
    # EarlyStopping: monitor="val_loss", patience=5, restore_best_weights=True
    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )

    # ModelCheckpoint: filepath="models/best_model.h5", monitor="val_loss", save_best_only=True
    best_model_path = os.path.join(MODELS_DIR, "best_model.h5")
    model_checkpoint = ModelCheckpoint(
        filepath=best_model_path,
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    )

    # ReduceLROnPlateau: monitor="val_loss", factor=0.2, patience=3
    reduce_lr = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=3,
        verbose=1
    )

    # 5. Train the Model
    logger.info(f"Starting joint training for {EPOCHS} epochs...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=[early_stopping, model_checkpoint, reduce_lr],
        verbose=1
    )

    # 6. Save final trained model to models/final_model.h5
    final_model_path = os.path.join(MODELS_DIR, "final_model.h5")
    model.save(final_model_path)

    # 7. Print results
    logger.info("-------------------------------------------------")
    logger.info("Training completed successfully!")
    
    # Extract best validation metrics from history
    best_val_cls_acc = max(history.history['val_classification_output_accuracy'])
    best_val_seg_acc = max(history.history['val_segmentation_output_accuracy'])
    
    logger.info(f"Best Validation Classification Accuracy: {best_val_cls_acc:.4f}")
    logger.info(f"Best Validation Segmentation Accuracy: {best_val_seg_acc:.4f}")
    logger.info(f"Best model saved to: {best_model_path}")
    logger.info(f"Final model saved to: {final_model_path}")
    logger.info("-------------------------------------------------")

if __name__ == "__main__":
    main()
