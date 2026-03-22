import os
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, f1_score
import seaborn as sns
from src import config
from src.utils import bce_dice_loss
from src.data_loader import build_generators

# --- GPU CONFIGURATION ---
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU detected: {gpus[0].name}. Memory growth enabled.")
    except RuntimeError as e:
        print(f"❌ GPU config error: {e}")

def load_pothole_model(model_path):
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

def predict_and_visualize(model, image_path, output_dir="results/eval"):
    """Performs inference on a single image and saves visual results."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load and Preprocess
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224)) / 255.0
    img_batch = np.expand_dims(img_resized, axis=0)

    # 2. Inference
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
    
    # Original
    plt.subplot(1, 3, 1)
    plt.imshow(img_resized)
    plt.title(f"Original Image\n({os.path.basename(image_path)})")
    plt.axis('off')

    # Mask
    plt.subplot(1, 3, 2)
    plt.imshow(mask, cmap='jet', vmin=0, vmax=3)
    plt.title("Predicted Damage Mask")
    plt.axis('off')
    
    # Overlay
    plt.subplot(1, 3, 3)
    plt.imshow(img_resized)
    plt.imshow(mask, cmap='jet', alpha=0.4, vmin=0, vmax=3)
    plt.title(f"Overlay: {predicted_class.capitalize()} ({confidence:.2%})")
    plt.axis('off')

    plt.tight_layout()
    save_path = os.path.join(output_dir, f"pred_{os.path.basename(image_path)}")
    plt.savefig(save_path)
    plt.close()
    print(f"📊 Visualization saved to {save_path}")

def evaluate_on_generator(model, generator):
    """Calculates metrics (Confusion Matrix, F1-score) on a dataset generator."""
    print("🚀 Evaluating on validation set...")
    
    all_y_true = []
    all_y_pred = []
    
    for i in range(len(generator)):
        x_batch, y_batch = generator[i]
        y_true = np.argmax(y_batch["cls_output"], axis=1)
        
        preds = model.predict(x_batch, verbose=0)
        y_pred = np.argmax(preds[0], axis=1)
        
        all_y_true.extend(y_true)
        all_y_pred.extend(y_pred)
        
    all_y_true = np.array(all_y_true)
    all_y_pred = np.array(all_y_pred)
    
    # 1. Confusion Matrix
    cm = confusion_matrix(all_y_true, all_y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=config.CLASSES, yticklabels=config.CLASSES)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix - Classification')
    plt.savefig("results/eval/confusion_matrix.png")
    print("✅ Confusion matrix saved to results/eval/confusion_matrix.png")

    # 2. Detailed Report
    print("\n--- Classification Report ---")
    print(classification_report(all_y_true, all_y_pred, target_names=config.CLASSES))
    
    # 3. F1-Score
    f1 = f1_score(all_y_true, all_y_pred, average='weighted')
    print(f"🏆 Weighted F1-Score: {f1:.4f}")

if __name__ == "__main__":
    # Paths
    MODEL_PATH = os.path.join(config.MODELS_DIR, config.MODEL_FILENAME)
    
    # Load Model
    model = load_pothole_model(MODEL_PATH)
    
    # Load Data for Evaluation
    _, val_gen = build_generators(config.DATA_DIR, config.MASK_DIR, batch_size=config.BATCH_SIZE)
    
    # Run Evaluation
    evaluate_on_generator(model, val_gen)
    
    # Run Inference on a few sample images from pothole dir
    pothole_dir = os.path.join(config.DATA_DIR, "pothole")
    if os.path.exists(pothole_dir):
        samples = [os.path.join(pothole_dir, f) for f in os.listdir(pothole_dir)[:3]]
        for sample in samples:
            predict_and_visualize(model, sample)
