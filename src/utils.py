import matplotlib.pyplot as plt
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plot_training_history(history, save_dir):
    """
    Plots and saves training history (Accuracy and Loss).

    Args:
        history: Keras History object.
        save_dir: Directory to save the plots.
    """
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))

    # Plot Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, 'bo-', label='Training Accuracy')
    plt.plot(epochs, val_acc, 'ro-', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # Plot Loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, 'bo-', label='Training Loss')
    plt.plot(epochs, val_loss, 'ro-', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # Save the plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = os.path.join(save_dir, f"training_history_{timestamp}.png")
    plt.savefig(plot_path)
    plt.close()
    logger.info(f"Training history plot saved to: {plot_path}")

def save_model_summary(model, save_dir):
    """
    Saves model summary to a text file.

    Args:
        model: Keras Model object.
        save_dir: Directory to save the summary.
    """
    summary_path = os.path.join(save_dir, "model_summary.txt")
    with open(summary_path, 'w') as f:
        model.summary(print_fn=lambda x: f.write(x + '\n'))
    logger.info(f"Model summary saved to: {summary_path}")
