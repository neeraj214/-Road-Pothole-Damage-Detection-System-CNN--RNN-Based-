import os
import tensorflow as tf
import numpy as np

# --- GPU CONFIGURATION ---
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU detected: {gpus[0].name}. Memory growth enabled.")
    except RuntimeError as e:
        print(f"❌ GPU config error: {e}")

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
DATA_DIR = os.path.join(config.BASE_DIR, "data") # Broad scan of entire data folder
MASK_DIR = config.MASK_DIR
MODELS_DIR = config.MODELS_DIR
LOGS_DIR = "logs"
RESULTS_DIR = "results"

def plot_training_history(history, save_path, stage_name):
    """
    Creates a detailed matplotlib figure for monitoring training.
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
    plt.suptitle(f"Training Performance - {stage_name}", fontsize=16)
    
    # Total Loss
    plt.subplot(2, 2, 1)
    plt.plot(epochs, history.history[loss_key], 'b-', label='Train Loss')
    plt.plot(epochs, history.history[f'val_{loss_key}'], 'r-', label='Val Loss')
    plt.title('Loss Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    # Accuracy
    plt.subplot(2, 2, 2)
    plt.plot(epochs, history.history[cls_acc_key], 'b-', label='Train Cls Acc')
    plt.plot(epochs, history.history[f'val_{cls_acc_key}'], 'r-', label='Val Cls Acc')
    plt.title('Classification Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # Segmentation Accuracy
    plt.subplot(2, 2, 3)
    plt.plot(epochs, history.history[seg_acc_key], 'b-', label='Train Seg Acc')
    plt.plot(epochs, history.history[f'val_{seg_acc_key}'], 'r-', label='Val Seg Acc')
    plt.title('Segmentation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # Learning Rate
    plt.subplot(2, 2, 4)
    if lr_key:
        plt.plot(epochs, history.history[lr_key], 'g-', label='Learning Rate')
        plt.title('Learning Rate Decay')
        plt.xlabel('Epochs')
        plt.ylabel('LR')
        plt.yscale('log')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(save_path)
    plt.close()
    logger.info(f"📊 History plot saved to {save_path}")

def get_epoch_logger():
    """Returns a LambdaCallback for clean custom epoch logging."""
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
    """STAGE 1: Training improved heads with frozen backbone."""
    logger.info("Starting STAGE 1: Improved Head training...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Compute Class Weights automatically from training labels
    # We will pass these to the generator to create sample_weights
    from sklearn.utils import class_weight
    all_img_paths = []
    all_cls_labels = []
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.lower().endswith(valid_extensions):
                path_lower = os.path.join(root, file).lower()
                if "pothole" in path_lower: label_idx = 2
                elif "crack" in path_lower or "damage" in path_lower: label_idx = 1
                else: label_idx = 0
                all_cls_labels.append(label_idx)
    
    weights = class_weight.compute_class_weight('balanced', classes=np.unique(all_cls_labels), y=all_cls_labels)
    class_weights_dict = dict(enumerate(weights))
    logger.info(f"⚖️ Computed Class Weights: {class_weights_dict}")

    # Load Data with 224x224 resolution and sample weights
    train_gen, val_gen = build_generators(
        DATA_DIR, MASK_DIR, 
        batch_size=config.BATCH_SIZE,
        img_size=224,
        class_weights=class_weights_dict
    )
    
    model = build_dual_head_model(img_size=224, freeze_base=True)
    
    # Use higher weight for classification (4.0) to reach 80-90% target
    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss={
            "cls_output": "categorical_crossentropy",
            "seg_output": bce_dice_loss
        },
        loss_weights={"cls_output": 4.0, "seg_output": 1.0},
        metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
    )
    
    callbacks = [
        ModelCheckpoint(
            os.path.join(MODELS_DIR, "stage1_v4.keras"), 
            monitor="val_cls_output_accuracy", 
            save_best_only=True, 
            mode='max',
            verbose=1
        ),
        EarlyStopping(monitor="val_cls_output_accuracy", patience=8, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_cls_output_accuracy", factor=0.5, patience=4, min_lr=1e-6, verbose=1),
        TensorBoard(log_dir=os.path.join(LOGS_DIR, "stage1_v4")),
        get_epoch_logger()
    ]
    
    # NOTE: class_weight removed for multi-output compatibility. 
    # Weights are now handled via sample_weights in the generator.
    history = model.fit(
        train_gen, 
        validation_data=val_gen, 
        epochs=epochs, 
        callbacks=callbacks
    )
    plot_training_history(history, os.path.join(RESULTS_DIR, "stage1_v4_history.png"), "Stage 1 V4")
    return os.path.join(MODELS_DIR, "stage1_v4.keras")

def stage2_finetune(stage1_model_path, epochs=20):
    """STAGE 2: Optimized Fine-tuning for 90% accuracy."""
    logger.info("Starting STAGE 2: Optimized Fine-tuning...")
    
    model = tf.keras.models.load_model(stage1_model_path, custom_objects={"bce_dice_loss": bce_dice_loss})
    
    # Gradual unfreezing: Top 15 layers, keeping BN frozen for stability
    model = unfreeze_top_layers(model, num_layers=15)
    
    # Load Data with 224x224 resolution and sample weights
    train_gen, val_gen = build_generators(
        DATA_DIR, MASK_DIR, 
        batch_size=config.BATCH_SIZE,
        img_size=224,
        class_weights=class_weights_dict
    )
    
    # Optimized LR for fine-tuning
    model.compile(
        optimizer=Adam(learning_rate=3e-5), 
        loss={"cls_output": "categorical_crossentropy", "seg_output": bce_dice_loss},
        loss_weights={"cls_output": 4.0, "seg_output": 1.0}, # Keep classification focus
        metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
    )
    
    callbacks = [
        ModelCheckpoint(
            os.path.join(MODELS_DIR, "best_model_dual_v4.keras"), 
            monitor="val_cls_output_accuracy", 
            save_best_only=True, 
            mode='max',
            verbose=1
        ),
        EarlyStopping(monitor="val_cls_output_accuracy", patience=10, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_cls_output_accuracy", factor=0.2, patience=5, min_lr=1e-7, verbose=1),
        TensorBoard(log_dir=os.path.join(LOGS_DIR, "stage2_v4")),
        get_epoch_logger()
    ]
    
    # NOTE: class_weight removed for multi-output compatibility.
    history = model.fit(
        train_gen, 
        validation_data=val_gen, 
        epochs=epochs, 
        callbacks=callbacks
    )
    plot_training_history(history, os.path.join(RESULTS_DIR, "stage2_v4_history.png"), "Stage 2 V4")
    logger.info(f"🏆 Final optimized model saved to models/best_model_dual_v4.keras")

if __name__ == "__main__":
    try:
        # Check if Stage 1 model exists, else train it
        stage1_path = os.path.join(MODELS_DIR, "stage1.keras")
        if not os.path.exists(stage1_path):
            stage1_path = stage1_train(epochs=15)
        
        # Run Improved Fine-tuning
        stage2_finetune(stage1_path, epochs=10)
    except Exception as e:
        logger.error(f"Training failed: {e}")
        import traceback
        traceback.print_exc()
