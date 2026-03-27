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

def build_dual_head_model(img_size=256, freeze_base=True):
    """
    Builds an improved dual-head model (Classification + Segmentation) using MobileNetV2.
    """
    logger.info(f"Building Improved Dual-Head Model with input size: ({img_size}, {img_size}, 3)")
    
    inputs = layers.Input(shape=(img_size, img_size, 3), name="input_image")
    
    # 1. SHARED BACKBONE: MobileNetV2
    base_model = MobileNetV2(
        include_top=False,
        weights="imagenet",
        input_tensor=inputs,
        alpha=1.0 # Standard width
    )
    
    if freeze_base:
        base_model.trainable = False
        logger.info("MobileNetV2 backbone frozen.")
    else:
        base_model.trainable = True

    # Extract skip connections for U-Net
    skip_layers = [
        "block_1_expand_relu",   # 128x128 (if 256x256 input)
        "block_3_expand_relu",   # 64x64
        "block_6_expand_relu",   # 32x32
        "block_13_expand_relu",  # 16x16
        "out_relu"               # 8x8 (bottleneck)
    ]
    
    skips = [base_model.get_layer(name).output for name in skip_layers]
    bottleneck = skips[-1]
    
    # 2. IMPROVED CLASSIFICATION HEAD
    # Optimized for 80-90% accuracy with deeper layers and normalization
    cls_x = layers.GlobalAveragePooling2D(name="cls_gap")(bottleneck)
    
    cls_x = layers.Dense(512, activation="relu", name="cls_dense_1")(cls_x)
    cls_x = layers.BatchNormalization(name="cls_bn_1")(cls_x)
    cls_x = layers.Dropout(0.5, name="cls_dropout_1")(cls_x)
    
    cls_x = layers.Dense(256, activation="relu", name="cls_dense_2")(cls_x)
    cls_x = layers.BatchNormalization(name="cls_bn_2")(cls_x)
    cls_x = layers.Dropout(0.3, name="cls_dropout_2")(cls_x)
    
    cls_output = layers.Dense(NUM_CLS_CLASSES, activation="softmax", name="cls_output")(cls_x)
    
    # 3. U-NET DECODER HEAD (Segmentation)
    d1 = decoder_block(bottleneck, skips[3], 256, name="dec1")
    d2 = decoder_block(d1, skips[2], 128, name="dec2")
    d3 = decoder_block(d2, skips[1], 64, name="dec3")
    d4 = decoder_block(d3, skips[0], 32, name="dec4")
    
    seg_x = layers.UpSampling2D(size=(2, 2), interpolation="bilinear", name="seg_final_upsample")(d4)
    seg_output = layers.Conv2D(NUM_SEG_CLASSES, (1, 1), activation="softmax", name="seg_output")(seg_x)
    
    # Construct Model
    model = Model(inputs=inputs, outputs=[cls_output, seg_output], name="Pothole_DualHead_V3")
    
    return model

def unfreeze_top_layers(model, num_layers=15):
    """
    Optimized unfreezing for Stage 2 fine-tuning.
    1. Unfreezes the top N layers of the model.
    2. Keeps ALL BatchNormalization layers frozen (even if in the top N) 
       to maintain stable mean/variance statistics.
    """
    model.trainable = True
    
    # Calculate how many layers to freeze from the bottom
    num_total_layers = len(model.layers)
    freeze_until = num_total_layers - num_layers
    
    for i, layer in enumerate(model.layers):
        if i < freeze_until:
            layer.trainable = False
        else:
            # Check if it's a BatchNormalization layer
            if isinstance(layer, layers.BatchNormalization):
                layer.trainable = False
            else:
                layer.trainable = True
        
    logger.info(f"Unfrozen the top {num_layers} non-BN layers for stable fine-tuning.")
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
