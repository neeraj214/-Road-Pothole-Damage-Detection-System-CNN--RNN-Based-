import tensorflow as tf
from tensorflow.keras import layers, models, Model
from tensorflow.keras.applications import MobileNetV2
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
NUM_SEG_CLASSES = 4   # background + 3 damage types (hairline crack, alligator crack, pothole)
NUM_CLS_CLASSES = 3   # normal / crack / pothole

def decoder_block(x, skip, filters, name):
    """
    U-Net Decoder Block: UpSampling2D -> Concatenate -> Conv2D -> BN -> ReLU -> Conv2D -> BN -> ReLU
    """
    x = layers.UpSampling2D(size=(2, 2), interpolation="bilinear", name=f"{name}_upsample")(x)
    x = layers.Concatenate(name=f"{name}_concat")([x, skip])
    
    # Conv Block 1
    x = layers.Conv2D(filters, (3, 3), padding="same", name=f"{name}_conv1")(x)
    x = layers.BatchNormalization(name=f"{name}_bn1")(x)
    x = layers.Activation("relu", name=f"{name}_relu1")(x)
    
    # Conv Block 2
    x = layers.Conv2D(filters, (3, 3), padding="same", name=f"{name}_conv2")(x)
    x = layers.BatchNormalization(name=f"{name}_bn2")(x)
    x = layers.Activation("relu", name=f"{name}_relu2")(x)
    
    return x

def build_dual_head_model(img_size=224, freeze_base=True):
    """
    Builds a dual-head model (Classification + Segmentation) using MobileNetV2 as shared backbone.
    """
    logger.info(f"Building Dual-Head Model with input size: ({img_size}, {img_size}, 3)")
    
    inputs = layers.Input(shape=(img_size, img_size, 3), name="input_image")
    
    # 1. SHARED BACKBONE: MobileNetV2
    base_model = MobileNetV2(
        include_top=False,
        weights="imagenet",
        input_tensor=inputs
    )
    
    if freeze_base:
        base_model.trainable = False
        logger.info("MobileNetV2 backbone frozen for Stage 1 training.")
    else:
        base_model.trainable = True
        logger.info("MobileNetV2 backbone unfrozen for Stage 2 joint fine-tuning.")

    # Extract skip connections
    # Layer names are confirmed for MobileNetV2 (224x224 input)
    skip_layers = [
        "block_1_expand_relu",   # 112x112
        "block_3_expand_relu",   # 56x56
        "block_6_expand_relu",   # 28x28
        "block_13_expand_relu",  # 14x14
        "out_relu"               # 7x7 (bottleneck)
    ]
    
    skips = [base_model.get_layer(name).output for name in skip_layers]
    bottleneck = skips[-1]
    
    # 2. CLASSIFICATION HEAD
    cls_x = layers.GlobalAveragePooling2D(name="cls_gap")(bottleneck)
    cls_x = layers.Dense(256, activation="relu", name="cls_dense")(cls_x)
    cls_x = layers.Dropout(0.4, name="cls_dropout")(cls_x)
    cls_output = layers.Dense(NUM_CLS_CLASSES, activation="softmax", name="cls_output")(cls_x)
    
    # 3. U-NET DECODER HEAD
    # d1: bottleneck (7x7) + skip_14x14 (14x14) -> 256 filters
    d1 = decoder_block(bottleneck, skips[3], 256, name="dec1")
    
    # d2: d1 (14x14) + skip_28x28 (28x28) -> 128 filters
    d2 = decoder_block(d1, skips[2], 128, name="dec2")
    
    # d3: d2 (28x28) + skip_56x56 (56x56) -> 64 filters
    d3 = decoder_block(d2, skips[1], 64, name="dec3")
    
    # d4: d3 (56x56) + skip_112x112 (112x112) -> 32 filters
    d4 = decoder_block(d3, skips[0], 32, name="dec4")
    
    # Final UpSampling to original 224x224
    seg_x = layers.UpSampling2D(size=(2, 2), interpolation="bilinear", name="seg_final_upsample")(d4)
    seg_output = layers.Conv2D(NUM_SEG_CLASSES, (1, 1), activation="softmax", name="seg_output")(seg_x)
    
    # Construct Model
    model = Model(inputs=inputs, outputs=[cls_output, seg_output], name="Pothole_DualHead_CNN_UNet")
    
    return model

def unfreeze_top_layers(model, num_layers=30):
    """
    Unfreezes the top N layers of the model for fine-tuning.
    """
    # Find the backbone (MobileNetV2 part)
    # Since we used the functional API, the base_model layers are part of the main model
    model.trainable = True
    
    # We want to keep the bottom layers frozen and only unfreeze the top ones
    # MobileNetV2 has ~154 layers. 
    # Let's freeze all layers first, then unfreeze the last 'num_layers'
    for layer in model.layers[:-num_layers]:
        layer.trainable = False
    for layer in model.layers[-num_layers:]:
        layer.trainable = True
        
    logger.info(f"Unfrozen the top {num_layers} layers for fine-tuning.")
    return model

if __name__ == "__main__":
    # Quick architecture test
    try:
        # 1. Build the model with freeze_base=True
        model = build_dual_head_model(img_size=224, freeze_base=True)
        
        # 2. Print model summary
        model.summary()
        logger.info("Successfully built dual-head model.")
        
        # 3. Create a random input tensor np.random.rand(1, 224, 224, 3)
        dummy_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
        
        # 4. Run a forward pass
        cls_output, seg_output = model.predict(dummy_input)
        
        # 5. Verify and print both output shapes
        logger.info(f"Classification Output Shape: {cls_output.shape}")
        logger.info(f"Segmentation Output Shape: {seg_output.shape}")
        
        # 6. Assert both shapes are correct
        expected_cls_shape = (1, 3)
        expected_seg_shape = (1, 224, 224, 4)
        
        assert cls_output.shape == expected_cls_shape, \
            f"Incorrect cls_output shape! Expected {expected_cls_shape}, got {cls_output.shape}"
        assert seg_output.shape == expected_seg_shape, \
            f"Incorrect seg_output shape! Expected {expected_seg_shape}, got {seg_output.shape}"
            
        logger.info("Architecture verification passed! Output shapes are correct.")
        
        # Optional: Test unfreezing
        model = unfreeze_top_layers(model, num_layers=30)
        logger.info("Successfully unfrozen top layers for fine-tuning test.")
        
    except Exception as e:
        logger.error(f"Model architecture test failed: {e}")
        import traceback
        traceback.print_exc()
