import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard, LambdaCallback
)
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras import layers
import albumentations as A
import src.data_loader as dl
from src.data_loader import build_generators
from src.utils import bce_dice_loss
from src import config

# --- STEP 2: STRONGER AUGMENTATION ---
def get_strong_augmentations(img_size=160):
    return A.Compose([
        A.Resize(img_size, img_size),
        A.RandomBrightnessContrast(
            brightness_limit=0.35, contrast_limit=0.35, p=0.7),
        A.MotionBlur(blur_limit=7, p=0.4),
        A.GaussNoise(var_limit=(10.0, 80.0), p=0.4),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.2),
        A.ShiftScaleRotate(
            shift_limit=0.1, scale_limit=0.15, rotate_limit=20, p=0.6),
        A.OneOf([
            A.RandomShadow(p=0.3),
            A.RandomFog(fog_coef_lower=0.1, fog_coef_upper=0.3, p=0.2),
            A.RandomRain(p=0.2),
        ], p=0.4),
        A.CoarseDropout(
            max_holes=8, max_height=20, max_width=20, p=0.3),
        A.GridDistortion(p=0.2),
    ], additional_targets={'mask': 'mask'}, is_check_shapes=False)

# Monkey-patch the augmentation function in data_loader
dl.get_augmentations = get_strong_augmentations

# --- STEP 5: WEIGHTED LOSS ---
def weighted_categorical_crossentropy(class_weights):
    weights_tensor = tf.constant(
        [class_weights[i] for i in sorted(class_weights.keys())], 
        dtype=tf.float32
    )
    def loss_fn(y_true, y_pred):
        cce = CategoricalCrossentropy(label_smoothing=0.1, reduction='none')
        per_sample_loss = cce(y_true, y_pred)
        # Compute per-sample weight from the true class
        sample_weights = tf.reduce_sum(
            tf.cast(y_true, tf.float32) * weights_tensor, axis=-1
        )
        return tf.reduce_mean(per_sample_loss * sample_weights)
    return loss_fn

def run_stage3():
    # Setup GPU memory growth
    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

    DATA_DIR = os.path.join(config.BASE_DIR, "data")
    MASK_DIR = config.MASK_DIR
    img_size = config.INPUT_SHAPE[0]

    # Build generators with monkey-patched strong augmentation
    train_ds, val_ds = build_generators(
        DATA_DIR, MASK_DIR, 
        batch_size=config.BATCH_SIZE, 
        img_size=img_size
    )

    # --- STEP 3: STRONGER CLASSIFICATION HEAD ---
    MODEL_PATH = os.path.join(config.MODELS_DIR, "best_model_dual_v6_deeper_tf")
    print(f"Loading model from {MODEL_PATH}...")
    
    loaded = tf.keras.models.load_model(
        MODEL_PATH, 
        custom_objects={"bce_dice_loss": bce_dice_loss},
        compile=False
    )

    # Extract the backbone output (bottleneck layer)
    bottleneck = loaded.get_layer("out_relu").output

    # Build new stronger head with more regularization
    gap = layers.GlobalAveragePooling2D(name="s3_gap")(bottleneck)
    gmp = layers.GlobalMaxPooling2D(name="s3_gmp")(bottleneck)
    x = layers.Concatenate(name="s3_concat")([gap, gmp])

    x = layers.Dense(
        512, activation="relu", name="s3_dense_1", 
        kernel_regularizer=tf.keras.regularizers.l2(1e-3)
    )(x)
    x = layers.BatchNormalization(name="s3_bn_1")(x)
    x = layers.Dropout(0.55, name="s3_drop_1")(x)

    x = layers.Dense(
        256, activation="relu", name="s3_dense_2", 
        kernel_regularizer=tf.keras.regularizers.l2(1e-3)
    )(x)
    x = layers.BatchNormalization(name="s3_bn_2")(x)
    x = layers.Dropout(0.4, name="s3_drop_2")(x)

    x = layers.Dense(
        128, activation="relu", name="s3_dense_3", 
        kernel_regularizer=tf.keras.regularizers.l2(5e-4)
    )(x)
    x = layers.BatchNormalization(name="s3_bn_3")(x)
    x = layers.Dropout(0.3, name="s3_drop_3")(x)

    new_cls_output = layers.Dense(
        3, activation="softmax", dtype="float32", name="cls_output"
    )(x)

    # Keep the existing seg_output unchanged
    seg_output = loaded.get_layer("seg_output").output

    # Build new model with replaced head
    new_model = tf.keras.Model(
        inputs=loaded.input,
        outputs=[new_cls_output, seg_output],
        name="Pothole_Stage3"
    )

    # --- STEP 4 & 6: TWO-PHASE TRAINING ---
    
    # Freeze all layers first
    new_model.trainable = False

    # Unfreeze new classification head layers
    head_layer_names = [
        "s3_gap", "s3_gmp", "s3_concat", 
        "s3_dense_1", "s3_bn_1", "s3_drop_1", 
        "s3_dense_2", "s3_bn_2", "s3_drop_2", 
        "s3_dense_3", "s3_bn_3", "s3_drop_3", 
        "cls_output"
    ]
    for name in head_layer_names:
        try:
            new_model.get_layer(name).trainable = True
        except ValueError:
            pass

    # Find backbone for unfreezing later
    backbone = None
    for layer in new_model.layers:
        if "mobilenetv2" in layer.name.lower():
            backbone = layer
            break

    # Phase A — head warmup (5 epochs, only new head trains, LR=1e-3)
    print("Starting Phase A: Head Warmup (5 epochs)...")
    if backbone:
        backbone.trainable = False

    new_model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss={
            "cls_output": weighted_categorical_crossentropy(config.CLASS_WEIGHTS),
            "seg_output": bce_dice_loss
        },
        loss_weights={"cls_output": 3.0, "seg_output": 1.0},
        metrics={
            "cls_output": ["accuracy"],
            "seg_output": [tf.keras.metrics.MeanIoU(num_classes=4, name="seg_iou")]
        }
    )

    history_a = new_model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=5,
        callbacks=[
            LambdaCallback(
                on_epoch_end=lambda epoch, logs: print(
                    f"PhaseA Epoch {epoch+1} | "
                    f"cls_acc: {logs.get('cls_output_accuracy', 0):.3f} | "
                    f"val_cls_acc: {logs.get('val_cls_output_accuracy', 0):.3f}"
                )
            )
        ]
    )

    # Phase B — full fine-tune (20 epochs, top backbone + head, LR=5e-5)
    print("Starting Phase B: Joint Fine-tuning (20 epochs)...")
    if backbone:
        backbone.trainable = True
        freeze_until = max(0, len(backbone.layers) - 40)
        for i, layer in enumerate(backbone.layers):
            if i < freeze_until:
                layer.trainable = False
            else:
                # Always keep BN frozen for stability
                if isinstance(layer, layers.BatchNormalization):
                    layer.trainable = False
                else:
                    layer.trainable = True

    STAGE3_PATH = os.path.join(config.MODELS_DIR, "best_model_stage3_tf")
    if os.path.exists(STAGE3_PATH):
        import shutil
        shutil.rmtree(STAGE3_PATH)

    new_model.compile(
        optimizer=Adam(learning_rate=5e-5),
        loss={
            "cls_output": weighted_categorical_crossentropy(config.CLASS_WEIGHTS),
            "seg_output": bce_dice_loss
        },
        loss_weights={"cls_output": 3.0, "seg_output": 1.0},
        metrics={
            "cls_output": ["accuracy"],
            "seg_output": [tf.keras.metrics.MeanIoU(num_classes=4, name="seg_iou")]
        }
    )

    callbacks_b = [
        ModelCheckpoint(
            filepath=STAGE3_PATH,
            monitor="val_cls_output_accuracy",
            save_best_only=True,
            mode="max",
            save_format="tf",
            verbose=1
        ),
        EarlyStopping(
            monitor="val_cls_output_accuracy",
            patience=7,
            restore_best_weights=True,
            min_delta=0.003,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.4,
            patience=3,
            min_lr=1e-7,
            verbose=1
        ),
        TensorBoard(log_dir="logs/stage3"),
        LambdaCallback(
            on_epoch_end=lambda epoch, logs: print(
                f"PhaseB Epoch {epoch+1} | "
                f"cls_acc: {logs.get('cls_output_accuracy', 0):.3f} | "
                f"val_cls_acc: {logs.get('val_cls_output_accuracy', 0):.3f} | "
                f"val_loss: {logs.get('val_loss', 0):.4f} | "
                f"LR: {logs.get('lr', 0):.7f}"
            )
        )
    ]

    history_b = new_model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20,
        callbacks=callbacks_b
    )

    print("Stage 3 complete. Best model saved to:", STAGE3_PATH)

if __name__ == "__main__":
    run_stage3()
