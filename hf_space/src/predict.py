import os
import argparse
import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
from src import config
from src.utils import bce_dice_loss

def load_model(model_path):
    """Loads the dual-head model with custom objects."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    
    model = tf.keras.models.load_model(
        model_path,
        custom_objects={"bce_dice_loss": bce_dice_loss},
        compile=False
    )
    print(f"✅ Model loaded from {model_path}")
    return model

def predict_single_image(model, image_path, output_path=None):
    """Performs prediction on a single image and visualizes results."""
    # 1. Load and preprocess image
    img = Image.open(image_path).convert('RGB')
    original_size = img.size
    img_resized = img.resize((config.INPUT_SHAPE[0], config.INPUT_SHAPE[1]))
    img_array = np.array(img_resized) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)

    # 2. Prediction
    predictions = model.predict(img_batch)
    cls_pred = predictions[0][0]
    seg_pred = predictions[1][0] # (H, W, 4)

    # 3. Post-process
    class_idx = np.argmax(cls_pred)
    confidence = cls_pred[class_idx]
    predicted_class = config.CLASSES[class_idx]
    
    mask = np.argmax(seg_pred, axis=-1) # (H, W) with values 0-3

    # 4. Visualization
    plt.figure(figsize=(15, 5))
    
    # Original Image
    plt.subplot(1, 3, 1)
    plt.imshow(img_resized)
    plt.title(f"Original Image\n({os.path.basename(image_path)})")
    plt.axis('off')

    # Predicted Mask
    plt.subplot(1, 3, 2)
    plt.imshow(mask, cmap='jet', vmin=0, vmax=3)
    plt.title("Predicted Mask (0-3)")
    plt.axis('off')
    
    # Overlay
    plt.subplot(1, 3, 3)
    plt.imshow(img_resized)
    plt.imshow(mask, cmap='jet', alpha=0.5, vmin=0, vmax=3)
    plt.title(f"Prediction: {predicted_class.capitalize()} ({confidence:.2%})")
    plt.axis('off')

    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        print(f"📊 Visualization saved to {output_path}")
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pothole Detection Prediction Script")
    parser.get_default("image_path")
    parser.add_argument("--image", type=str, help="Path to the input image")
    parser.add_argument("--model", type=str, default=os.path.join(config.MODELS_DIR, config.MODEL_FILENAME), help="Path to the model file")
    parser.add_argument("--output", type=str, default="results/prediction_test.png", help="Path to save the output visualization")
    
    args = parser.parse_args()
    
    if not args.image:
        print("❌ Please provide an image path using --image <path_to_image>")
    else:
        model = load_model(args.model)
        predict_single_image(model, args.image, args.output)
