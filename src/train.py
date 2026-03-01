import os
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import logging
from src import config, data_loader, model, utils

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train():
    """
    Main training script for the Road Pothole & Damage Detection System.
    """
    
    # 1. Load Data Generators
    logger.info("Loading data generators...")
    try:
        train_gen, val_gen, test_gen = data_loader.get_data_generators(config)
        logger.info(f"Loaded generators for classes: {config.CLASSES}")
    except Exception as e:
        logger.error(f"Failed to load data generators: {e}")
        return

    # 2. Build the Model
    logger.info("Building model architecture...")
    cnn_model = model.build_model(config)

    # 3. Define Callbacks
    # - EarlyStopping: Stop training if validation loss doesn't improve for 5 epochs
    # - ModelCheckpoint: Save the best model version based on validation accuracy
    # - ReduceLROnPlateau: Reduce learning rate when validation loss plateaus
    
    checkpoint_path = os.path.join(config.MODELS_DIR, f"{config.MODEL_NAME}_best.keras")
    
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            filepath=checkpoint_path,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]

    # 4. Train the Model
    logger.info(f"Starting training for {config.EPOCHS} epochs...")
    try:
        history = cnn_model.fit(
            train_gen,
            epochs=config.EPOCHS,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1
        )
        logger.info("Training completed successfully.")
    except Exception as e:
        logger.error(f"Training failed: {e}")
        return

    # 5. Evaluate on Test Set
    logger.info("Evaluating model on test set...")
    test_loss, test_acc = cnn_model.evaluate(test_gen, verbose=1)
    logger.info(f"Test Accuracy: {test_acc:.4f}, Test Loss: {test_loss:.4f}")

    # 6. Post-Training: Save Plots and Summaries
    logger.info("Saving training results...")
    
    # Plot training history (Accuracy/Loss)
    utils.plot_training_history(history, config.MODELS_DIR)
    
    # Save model summary to file
    utils.save_model_summary(cnn_model, config.MODELS_DIR)
    
    # Save the final model (in case the checkpoint didn't save it)
    final_model_path = os.path.join(config.MODELS_DIR, f"{config.MODEL_NAME}_final.keras")
    cnn_model.save(final_model_path)
    logger.info(f"Final model saved to: {final_model_path}")

if __name__ == "__main__":
    # Ensure project directories exist before training
    config.create_dirs()
    
    # Start the training process
    train()
