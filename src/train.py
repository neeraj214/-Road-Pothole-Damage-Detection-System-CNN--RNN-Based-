import os
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard, LambdaCallback
from tensorflow.keras.losses import categorical_crossentropy
import matplotlib.pyplot as plt
import logging
from src.model import build_dual_head_model, unfreeze_top_layers
from src.data_loader import build_generators
from src.utils import bce_dice_loss
from src import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = "data/raw/train" # Adjusted to find normal/crack/pothole subdirs
MASK_DIR = "data/processed/masks"
MODELS_DIR = "models"
LOGS_DIR = "logs"
RESULTS_DIR = "results"

def plot_training_history(history, save_path, stage_name):
    """
    Creates a 2x2 matplotlib figure for monitoring training.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    keys = history.history.keys()
    # Find matching keys in history
    loss_key = [k for k in keys if 'loss' in k and 'val' not in k and '_' not in k][0]
    cls_acc_key = [k for k in keys if 'cls_output_accuracy' in k and 'val' not in k][0]
    seg_acc_key = [k for k in keys if 'seg_output_accuracy' in k and 'val' not in k][0]
    lr_key = [k for k in keys if 'lr' in k][0] if any('lr' in k for k in keys) else None

    epochs = range(1, len(history.history[loss_key]) + 1)
    
    plt.figure(figsize=(15, 12))
    plt.suptitle(f"Training History - {stage_name}", fontsize=16)
    
    # Subplot 1: Total Loss
    plt.subplot(2, 2, 1)
    plt.plot(epochs, history.history[loss_key], 'b-', label='Train Loss')
    plt.plot(epochs, history.history[f'val_{loss_key}'], 'r-', label='Val Loss')
    plt.title('Total Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    # Subplot 2: Classification Accuracy
    plt.subplot(2, 2, 2)
    plt.plot(epochs, history.history[cls_acc_key], 'b-', label='Train Cls Acc')
    plt.plot(epochs, history.history[f'val_{cls_acc_key}'], 'r-', label='Val Cls Acc')
    plt.title('Classification Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # Subplot 3: Segmentation Accuracy
    plt.subplot(2, 2, 3)
    plt.plot(epochs, history.history[seg_acc_key], 'b-', label='Train Seg Acc')
    plt.plot(epochs, history.history[f'val_{seg_acc_key}'], 'r-', label='Val Seg Acc')
    plt.title('Segmentation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # Subplot 4: Learning Rate
    plt.subplot(2, 2, 4)
    if lr_key:
        plt.plot(epochs, history.history[lr_key], 'g-', label='Learning Rate')
        plt.title('Learning Rate')
        plt.xlabel('Epochs')
        plt.ylabel('LR')
        plt.yscale('log')
        plt.legend()
        plt.grid(True)
    else:
        plt.text(0.5, 0.5, 'LR info not available', ha='center')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(save_path)
    plt.close()
    logger.info(f"History plot saved to {save_path}")

def get_epoch_logger():
    """Returns a LambdaCallback for custom epoch printing."""
    return LambdaCallback(
        on_epoch_end=lambda epoch, logs: print(
            f"Epoch {epoch+1} | "
            f"cls_acc: {logs.get('cls_output_accuracy', 0):.3f} | "
            f"seg_acc: {logs.get('seg_output_accuracy', 0):.3f} | "
            f"val_loss: {logs.get('val_loss', 0):.3f} | "
            f"LR: {logs.get('lr', 0):.7f}"
        )
    )

def stage1_train(epochs=15):
    """
    STAGE 1: Training heads only with a frozen MobileNetV2 backbone.
    """
    logger.info("Starting STAGE 1: Head training...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(os.path.join(LOGS_DIR, "stage1"), exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    train_gen, val_gen = build_generators(DATA_DIR, MASK_DIR, batch_size=2)
    
    # Build model (frozen base)
    model = build_dual_head_model(freeze_base=True)
    
    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss={
            "cls_output": "categorical_crossentropy",
            "seg_output": bce_dice_loss
        },
        loss_weights={"cls_output": 1.0, "seg_output": 2.0},
        metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
    )
    
    callbacks = [
        ModelCheckpoint(os.path.join(MODELS_DIR, "stage1.keras"), monitor="val_cls_output_accuracy", save_best_only=True, verbose=1, mode='max'),
        EarlyStopping(patience=5, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=3, verbose=1),
        TensorBoard(log_dir=os.path.join(LOGS_DIR, "stage1")),
        get_epoch_logger()
    ]
    
    history = model.fit(train_gen, validation_data=val_gen, epochs=epochs, callbacks=callbacks)
    
    plot_training_history(history, os.path.join(RESULTS_DIR, "stage1_history.png"), "Stage 1")
    return os.path.join(MODELS_DIR, "stage1.keras")

def stage2_finetune(stage1_model_path, epochs=20):
    """
    STAGE 2: Fine-tuning top layers of MobileNetV2.
    """
    logger.info("Starting STAGE 2: Fine-tuning backbone...")
    os.makedirs(os.path.join(LOGS_DIR, "stage2"), exist_ok=True)
    
    # Load Stage 1 model
    model = tf.keras.models.load_model(stage1_model_path, custom_objects={"bce_dice_loss": bce_dice_loss})
    
    # Unfreeze top layers
    model = unfreeze_top_layers(model, num_layers=30)
    
    train_gen, val_gen = build_generators(DATA_DIR, MASK_DIR, batch_size=2)
    
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss={
            "cls_output": "categorical_crossentropy",
            "seg_output": bce_dice_loss
        },
        loss_weights={"cls_output": 1.0, "seg_output": 2.0},
        metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
    )
    
    callbacks = [
        ModelCheckpoint(os.path.join(MODELS_DIR, config.MODEL_FILENAME), monitor="val_loss", save_best_only=True, verbose=1),
        EarlyStopping(patience=7, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=3, verbose=1),
        TensorBoard(log_dir=os.path.join(LOGS_DIR, "stage2")),
        get_epoch_logger()
    ]
    
    history = model.fit(train_gen, validation_data=val_gen, epochs=epochs, callbacks=callbacks, workers=0, use_multiprocessing=False)
    
    plot_training_history(history, os.path.join(RESULTS_DIR, "stage2_history.png"), "Stage 2")
    logger.info(f"Final model saved: {os.path.join(MODELS_DIR, config.MODEL_FILENAME)}")

if __name__ == "__main__":
    try:
        stage1_path = stage1_train(epochs=15)
        stage2_finetune(stage1_path, epochs=20)
    except Exception as e:
        logger.error(f"Training failed: {e}")
        import traceback
        traceback.print_exc()
