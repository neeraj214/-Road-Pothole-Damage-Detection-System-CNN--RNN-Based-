import tensorflow as tf
from tensorflow.keras import layers, models, Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_model(config):
    """
    Builds and compiles a Dual-head model (Classification + Segmentation) 
    using Transfer Learning with MobileNetV2 as shared encoder.

    Args:
        config: Configuration module or object containing hyperparameters.

    Returns:
        tf.keras.Model: Compiled Keras model.
    """
    
    logger.info(f"Building dual-head model with input shape: {config.INPUT_SHAPE}")

    # 1. Base Model: MobileNetV2 (Shared Encoder)
    base_model = MobileNetV2(
        include_top=False,
        weights="imagenet",
        input_shape=config.INPUT_SHAPE
    )

    # 2. Select layers for skip connections and classification
    # These names are specific to MobileNetV2
    layer_names = [
        "block_1_expand_relu",   # 112x112
        "block_3_expand_relu",   # 56x56
        "block_6_expand_relu",   # 28x28
        "block_13_expand_relu",  # 14x14
        "out_relu"               # 7x7
    ]
    layers_outputs = [base_model.get_layer(name).output for name in layer_names]

    # Create the feature extraction model
    encoder = Model(inputs=base_model.input, outputs=layers_outputs, name="encoder")
    encoder.trainable = False  # Initially frozen
    
    inputs = layers.Input(shape=config.INPUT_SHAPE)
    skips = encoder(inputs)
    
    # 3. Classification Head
    # Use the last layer from encoder for classification
    bottleneck = skips[-1]
    x = layers.GlobalAveragePooling2D()(bottleneck)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.5)(x)
    num_classes = len(config.CLASSES)
    cls_output = layers.Dense(num_classes, activation="softmax", name="classification_output")(x)

    # 4. Segmentation Decoder (UNet-like)
    def upsample_block(x, skip, filters, name):
        x = layers.Conv2DTranspose(filters, (3, 3), strides=(2, 2), padding="same")(x)
        x = layers.Concatenate()([x, skip])
        x = layers.Conv2D(filters, (3, 3), padding="same", activation="relu")(x)
        x = layers.Conv2D(filters, (3, 3), padding="same", activation="relu")(x)
        return x

    # Upsampling
    u1 = upsample_block(bottleneck, skips[3], 256, "up1")  # 7x7 -> 14x14
    u2 = upsample_block(u1, skips[2], 128, "up2")         # 14x14 -> 28x28
    u3 = upsample_block(u2, skips[1], 64, "up3")          # 28x28 -> 56x56
    u4 = upsample_block(u3, skips[0], 32, "up4")          # 56x56 -> 112x112
    
    # Final upsampling to original size (224, 224)
    u5 = layers.Conv2DTranspose(16, (3, 3), strides=(2, 2), padding="same")(u4)
    # Output 4 channels for pixel-level severity (background, hairline, alligator, deep)
    seg_output = layers.Conv2D(config.NUM_SEG_CLASSES, (1, 1), activation="softmax", name="segmentation_output")(u5)

    # 5. Construct Final Model
    model = Model(inputs=inputs, outputs=[cls_output, seg_output], name="Road_Pothole_DualHead_Model")

    # 6. Compile Model
    logger.info(f"Compiling model with Adam optimizer (learning rate={config.LEARNING_RATE})...")
    optimizer = Adam(learning_rate=config.LEARNING_RATE)
    
    model.compile(
        optimizer=optimizer,
        loss={
            "classification_output": "categorical_crossentropy",
            "segmentation_output": "categorical_crossentropy" # One-hot masks
        },
        loss_weights={
            "classification_output": 1.0,
            "segmentation_output": 2.0  # Slightly more weight on segmentation
        },
        metrics={
            "classification_output": "accuracy",
            "segmentation_output": ["accuracy", tf.keras.metrics.MeanIoU(num_classes=config.NUM_SEG_CLASSES)]
        }
    )

    model.summary()
    return model

if __name__ == "__main__":
    # Quick test if run directly
    try:
        from src import config
        model = build_model(config)
        logger.info("Successfully built and compiled the model.")
    except Exception as e:
        logger.error(f"Model building failed: {e}")
