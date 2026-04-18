import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import MobileNetV2
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
NUM_SEG_CLASSES = 4   # background + 3 damage types (hairline crack, alligator crack, pothole)
NUM_CLS_CLASSES = 3   # normal / crack / pothole

def decoder_block(x, skip, filters, name):
    """
    Lightweight Decoder Block: UpSampling2D -> Concatenate -> SeparableConv2D -> BN -> ReLU
    """
    x = layers.UpSampling2D(size=(2, 2), interpolation="bilinear", name=f"{name}_upsample")(x)
    x = layers.Concatenate(name=f"{name}_concat")([x, skip])
    
    # Lightweight Separable Conv instead of heavy Conv2D
    x = layers.SeparableConv2D(filters, (3, 3), padding="same", name=f"{name}_sepconv1")(x)
    x = layers.BatchNormalization(name=f"{name}_bn1")(x)
    x = layers.Activation("relu", name=f"{name}_relu1")(x)
    
    return x

def build_dual_head_model(img_size=160, freeze_base=True):
    """
    Builds a memory-optimized dual-head model for RTX 2050 (4GB).
    """
    logger.info(f"Building OOM-optimized Model with input size: ({img_size}, {img_size}, 3)")
    
    inputs = layers.Input(shape=(img_size, img_size, 3), name="input_image")
    
    # 1. SHARED BACKBONE: MobileNetV2
    base_model = MobileNetV2(
        include_top=False,
        weights="imagenet",
        input_tensor=inputs,
        alpha=1.0 
    )
    
    if freeze_base:
        base_model.trainable = False
        logger.info("MobileNetV2 backbone frozen.")
    else:
        base_model.trainable = True

    # Extract skip connections for U-Net
    skip_layers = [
        "block_1_expand_relu",   # 80x80 (if 160x160 input)
        "block_3_expand_relu",   # 40x40
        "block_6_expand_relu",   # 20x20
        "block_13_expand_relu",  # 10x10
        "out_relu"               # 5x5 (bottleneck)
    ]
    
    skips = [base_model.get_layer(name).output for name in skip_layers]
    bottleneck = skips[-1]
    
    # 2. STRONGER CLASSIFICATION HEAD (GAP + GMP concatenation)
    gap = layers.GlobalAveragePooling2D(name="cls_gap")(bottleneck)
    gmp = layers.GlobalMaxPooling2D(name="cls_gmp")(bottleneck)
    cls_x = layers.Concatenate(name="cls_pool_concat")([gap, gmp])
    
    cls_x = layers.Dense(512, activation="relu", name="cls_dense_1")(cls_x)
    cls_x = layers.BatchNormalization(name="cls_bn_1")(cls_x)
    cls_x = layers.Dropout(0.4, name="cls_dropout_1")(cls_x)
    
    cls_x = layers.Dense(256, activation="relu", name="cls_dense_2")(cls_x)
    cls_x = layers.BatchNormalization(name="cls_bn_2")(cls_x)
    cls_x = layers.Dropout(0.3, name="cls_dropout_2")(cls_x)
    
    cls_output = layers.Dense(NUM_CLS_CLASSES, activation="softmax", dtype='float32', name="cls_output")(cls_x)
    
    # 3. LIGHTWEIGHT DECODER HEAD (Reduced filters for OOM fix)
    d1 = decoder_block(bottleneck, skips[3], 128, name="dec1") 
    d2 = decoder_block(d1, skips[2], 64, name="dec2") 
    d3 = decoder_block(d2, skips[1], 32, name="dec3") 
    d4 = decoder_block(d3, skips[0], 16, name="dec4") 
    
    seg_x = layers.UpSampling2D(size=(2, 2), interpolation="bilinear", name="seg_final_upsample")(d4)
    seg_output = layers.Conv2D(NUM_SEG_CLASSES, (1, 1), activation="softmax", dtype='float32', name="seg_output")(seg_x)
    
    # Construct Model
    model = Model(inputs=inputs, outputs=[cls_output, seg_output], name="Pothole_DualHead_V4")
    
    return model

def unfreeze_top_layers(model, num_layers=80):
    """
    Optimized unfreezing for Stage 2 fine-tuning.
    1. Unfreezes the top N layers of the entire model, including the backbone.
    2. Keeps ALL BatchNormalization layers frozen for stability.
    """
    # 1. Unfreeze the main model
    model.trainable = True
    
    # 2. Handle Backbone (MobileNetV2) specifically if it's a nested model
    backbone = None
    for layer in model.layers:
        if "mobilenetv2" in layer.name.lower():
            backbone = layer
            break
            
    if backbone:
        backbone.trainable = True
        # Calculate how many layers to freeze in the backbone
        # MobileNetV2 has ~154 layers. We unfreeze the top 'num_layers'
        num_backbone_layers = len(backbone.layers)
        freeze_until = max(0, num_backbone_layers - num_layers)
        
        for i, layer in enumerate(backbone.layers):
            if i < freeze_until:
                layer.trainable = False
            else:
                # Keep BN frozen even in unfreezing zone
                if isinstance(layer, layers.BatchNormalization) or "bn" in layer.name.lower():
                    layer.trainable = False
                else:
                    layer.trainable = True
        logger.info(f"Unfrozen top {num_layers} layers of backbone {backbone.name} (BN layers remain frozen).")

    # 3. Ensure Head layers are unfrozen but BN remains frozen
    for layer in model.layers:
        if "mobilenetv2" not in layer.name.lower():
            if isinstance(layer, layers.BatchNormalization) or "bn" in layer.name.lower():
                layer.trainable = False
            else:
                layer.trainable = True
                
    return model

if __name__ == "__main__":
    import numpy as np  # only needed for the architecture smoke-test below
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
