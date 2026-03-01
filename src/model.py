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
    Builds and compiles a CNN model using Transfer Learning with MobileNetV2.

    Args:
        config: Configuration module or object containing hyperparameters.

    Returns:
        tf.keras.Model: Compiled Keras model.
    """
    
    logger.info(f"Building model with input shape: {config.INPUT_SHAPE}")

    # 1. Base Model: MobileNetV2 (Transfer Learning)
    base_model = MobileNetV2(
        include_top=False,
        weights="imagenet",
        input_shape=config.INPUT_SHAPE
    )

    # 2. Freeze base model layers initially
    base_model.trainable = False
    logger.info("Base model (MobileNetV2) layers frozen.")

    # 3. Custom Classification Head
    inputs = tf.keras.Input(shape=config.INPUT_SHAPE)
    
    # Preprocessing for MobileNetV2 (if needed, but usually rescaling 1./255 is done in data_loader)
    # x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base_model(inputs, training=False)
    
    # Add GlobalAveragePooling2D
    x = layers.GlobalAveragePooling2D()(x)
    
    # Add Dense(128, activation="relu")
    x = layers.Dense(128, activation="relu")(x)
    
    # Add Dropout(0.5)
    x = layers.Dropout(0.5)(x)
    
    # Output layer: Dense(num_classes, activation="softmax")
    num_classes = len(config.CLASSES)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    # Construct the final model
    model = Model(inputs=inputs, outputs=outputs, name="Road_Pothole_Detection_Model")

    # 4. Compile Model
    logger.info(f"Compiling model with Adam optimizer (learning rate={config.LEARNING_RATE})...")
    optimizer = Adam(learning_rate=config.LEARNING_RATE)
    
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # 5. Print Model Summary
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
