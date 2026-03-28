import os
import shutil
import tensorflow as tf
import numpy as np
from tensorflow.keras import mixed_precision

# --- MIXED PRECISION & GPU CONFIGURATION ---
# Use mixed precision for RTX 2050 (Ampere architecture supports it well)
try:
    mixed_precision.set_global_policy('mixed_float16')
    print("✅ Mixed precision (mixed_float16) enabled.")
except Exception as e:
    print(f"⚠️ Mixed precision not supported: {e}")

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
from tensorflow.keras.losses import CategoricalCrossentropy
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
DATA_DIR = os.path.join(config.BASE_DIR, "data") 
MASK_DIR = config.MASK_DIR
MODELS_DIR = config.MODELS_DIR
LOGS_DIR = "logs"
RESULTS_DIR = "results"

def cleanup_model_path(path):
    """
    Safely removes a file or directory at the given path to avoid HDF5/dataset conflicts.
    """
    if os.path.exists(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            logger.info(f"🧹 Cleaned up existing model path: {path}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to cleanup {path}: {e}")

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

class GradientAccumulationModel(tf.keras.Model):
    """
    Custom model wrapper to implement gradient accumulation in model.fit()
    """
    def __init__(self, n_gradients, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_gradients = tf.constant(n_gradients, dtype=tf.int32)
        self.n_steps = tf.Variable(0, trainable=False, dtype=tf.int32)
        self.gradient_accumulation = None

    def train_step(self, data):
        # Initialize accumulation variables lazily on first step
        if self.gradient_accumulation is None:
            self.gradient_accumulation = [tf.Variable(tf.zeros_like(v), trainable=False) for v in self.trainable_variables]

        x, y = data
        self.n_steps.assign_add(1)

        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)
            loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

        gradients = tape.gradient(loss, self.trainable_variables)
        
        for i in range(len(gradients)):
            self.gradient_accumulation[i].assign_add(gradients[i])

        def apply_grads():
            avg_gradients = [g / tf.cast(self.n_gradients, tf.float32) for g in self.gradient_accumulation]
            self.optimizer.apply_gradients(zip(avg_gradients, self.trainable_variables))
            
            for i in range(len(self.gradient_accumulation)):
                self.gradient_accumulation[i].assign(tf.zeros_like(self.gradient_accumulation[i]))
            
            self.n_steps.assign(0)
            return tf.constant(0)

        def do_nothing():
            return tf.constant(0)

        tf.cond(
            tf.equal(self.n_steps % self.n_gradients, 0),
            apply_grads,
            do_nothing
        )

        self.compiled_metrics.update_state(y, y_pred)
        return {m.name: m.result() for m in self.metrics}

def stage1_train(epochs=15, batch_size=config.BATCH_SIZE):
    """STAGE 1: Training improved heads with frozen backbone."""
    tf.keras.backend.clear_session()
    logger.info(f"Starting STAGE 1 (Batch Size: {batch_size})...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    img_size = config.INPUT_SHAPE[0]
    checkpoint_path = os.path.join(MODELS_DIR, "stage1_v6_tf")
    cleanup_model_path(checkpoint_path)
    
    try:
        train_ds, val_ds = build_generators(
            DATA_DIR, MASK_DIR, 
            batch_size=batch_size,
            img_size=img_size
        )
        
        base_model = build_dual_head_model(img_size=img_size, freeze_base=True)
        model = GradientAccumulationModel(n_gradients=config.ACCUMULATION_STEPS, inputs=base_model.inputs, outputs=base_model.outputs)
        
        model.compile(
            optimizer=Adam(learning_rate=1e-3),
            loss={
                "cls_output": CategoricalCrossentropy(label_smoothing=0.1),
                "seg_output": bce_dice_loss
            },
            loss_weights={"cls_output": 5.0, "seg_output": 1.0},
            metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
        )
        
        callbacks = [
            ModelCheckpoint(
                filepath=checkpoint_path, 
                monitor="val_cls_output_accuracy", 
                save_best_only=True, 
                mode='max',
                save_format="tf",
                verbose=1
            ),
            EarlyStopping(monitor="val_cls_output_accuracy", patience=8, restore_best_weights=True, verbose=1),
            ReduceLROnPlateau(monitor="val_cls_output_loss", factor=0.3, patience=2, min_lr=1e-6, verbose=1),
            TensorBoard(log_dir=os.path.join(LOGS_DIR, "stage1_v6")),
            get_epoch_logger()
        ]
        
        history = model.fit(
            train_ds, 
            validation_data=val_ds, 
            epochs=epochs, 
            callbacks=callbacks
        )
        plot_training_history(history, os.path.join(RESULTS_DIR, "stage1_v6_history.png"), "Stage 1 V6")
        return checkpoint_path

    except tf.errors.ResourceExhaustedError:
        logger.warning(f"OOM with batch size {batch_size}. Retrying with {batch_size // 2}...")
        if batch_size > 1:
            return stage1_train(epochs, batch_size // 2)
        else:
            raise

def stage2_finetune(stage1_model_path, epochs=25, batch_size=config.BATCH_SIZE):
    """STAGE 2: Optimized Fine-tuning."""
    tf.keras.backend.clear_session()
    logger.info(f"Starting STAGE 2 (Batch Size: {batch_size})...")
    
    img_size = config.INPUT_SHAPE[0]
    final_checkpoint_path = os.path.join(MODELS_DIR, "best_model_dual_v6_tf")
    cleanup_model_path(final_checkpoint_path)
    
    try:
        loaded_model = tf.keras.models.load_model(stage1_model_path, custom_objects={"bce_dice_loss": bce_dice_loss})
        loaded_model = unfreeze_top_layers(loaded_model, num_layers=80)
        
        model = GradientAccumulationModel(n_gradients=config.ACCUMULATION_STEPS, inputs=loaded_model.inputs, outputs=loaded_model.outputs)
        
        train_ds, val_ds = build_generators(
            DATA_DIR, MASK_DIR, 
            batch_size=batch_size,
            img_size=img_size
        )
        
        model.compile(
            optimizer=Adam(learning_rate=3e-5), 
            loss={
                "cls_output": CategoricalCrossentropy(label_smoothing=0.1),
                "seg_output": bce_dice_loss
            },
            loss_weights={"cls_output": 5.0, "seg_output": 1.0},
            metrics={"cls_output": "accuracy", "seg_output": "accuracy"}
        )
        
        callbacks = [
            ModelCheckpoint(
                filepath=final_checkpoint_path, 
                monitor="val_cls_output_accuracy", 
                save_best_only=True, 
                mode='max',
                save_format="tf",
                verbose=1
            ),
            EarlyStopping(monitor="val_cls_output_accuracy", patience=10, restore_best_weights=True, verbose=1),
            ReduceLROnPlateau(monitor="val_cls_output_loss", factor=0.3, patience=2, min_lr=1e-6, verbose=1),
            TensorBoard(log_dir=os.path.join(LOGS_DIR, "stage2_v6")),
            get_epoch_logger()
        ]
        
        history = model.fit(
            train_ds, 
            validation_data=val_ds, 
            epochs=epochs, 
            callbacks=callbacks
        )
        plot_training_history(history, os.path.join(RESULTS_DIR, "stage2_v6_history.png"), "Stage 2 V6")
        logger.info(f"🏆 Final optimized model saved to {final_checkpoint_path}")

    except tf.errors.ResourceExhaustedError:
        logger.warning(f"OOM with batch size {batch_size}. Retrying with {batch_size // 2}...")
        if batch_size > 1:
            return stage2_finetune(stage1_model_path, epochs, batch_size // 2)
        else:
            raise

if __name__ == "__main__":
    try:
        stage1_path = os.path.join(MODELS_DIR, "stage1_v6_tf")
        if not os.path.exists(stage1_path):
            stage1_path = stage1_train(epochs=15)
        
        stage2_finetune(stage1_path, epochs=25)
    except Exception as e:
        logger.error(f"Training failed: {e}")
        import traceback
        traceback.print_exc()

