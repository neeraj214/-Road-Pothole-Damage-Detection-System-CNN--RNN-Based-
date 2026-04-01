"""
download_model.py — Downloads the trained model at container startup.

The model is too large for git, so it lives on Hugging Face Model Hub.
Set the MODEL_URL environment variable in your Space settings to the
direct download link of the zipped model.

How to upload your model:
  1. Go to https://huggingface.co/new
  2. Create a new model repo (e.g. road-pothole-model)
  3. Zip the models/best_model_dual_v6_deeper_tf/ folder:
       zip -r best_model_dual_v6_deeper_tf.zip best_model_dual_v6_deeper_tf/
  4. Upload the zip via the HF web UI or Git LFS
  5. Copy the raw download URL and set it as MODEL_URL in Space settings
"""

import os
import zipfile
import logging
import shutil
import glob

logger = logging.getLogger(__name__)

MODEL_DIR = "models"
MODEL_NAME = "best_model_dual_v6_deeper_tf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)


def model_is_ready() -> bool:
    matches = glob.glob(
        os.path.join(MODEL_DIR, "**", "saved_model.pb"),
        recursive=True
    )
    return len(matches) > 0

def download_model() -> bool:
    """
    Downloads and extracts the model from MODEL_URL if it isn't already present.
    Returns True if model is available (whether downloaded now or pre-existing).
    """
    if model_is_ready():
        logger.info(f"Model already present — skipping download.")
        return True

    MODEL_URL = os.getenv("MODEL_URL", "").strip()

    if not MODEL_URL:
        logger.warning("=" * 60)
        logger.warning("MODEL_URL environment variable is not set.")
        logger.warning("The API will start but /predict returns 503.")
        logger.warning("")
        logger.warning("To fix, upload your model to HF Model Hub and set:")
        logger.warning("  MODEL_URL = <direct zip download URL>")
        logger.warning("")
        logger.warning("See download_model.py docstring for step-by-step instructions.")
        logger.warning("=" * 60)
        return False

    logger.info(f"Downloading model from: {MODEL_URL}")
    os.makedirs(MODEL_DIR, exist_ok=True)
    zip_path = os.path.join(MODEL_DIR, "model_download.zip")

    try:
        import requests  # imported here so the rest of the app works without it
        response = requests.get(MODEL_URL, stream=True, timeout=300)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)

        logger.info(f"Download complete ({downloaded / 1024 / 1024:.1f} MB). Extracting...")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(MODEL_DIR)

        # After extraction, find where saved_model.pb actually landed
        matches = glob.glob("models/**/saved_model.pb", recursive=True)
        if matches:
            actual_dir = os.path.dirname(matches[0])
            target_dir = MODEL_PATH  # models/best_model_dual_v6_deeper_tf
            
            if actual_dir != target_dir and not os.path.exists(target_dir):
                shutil.move(actual_dir, target_dir)
                logger.info(f"Moved model from {actual_dir} to {target_dir}")

        # Remove zip file after extraction
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        for root, dirs, files in os.walk("models/"):
            for f in files:
                logger.info(f"Found: {os.path.join(root, f)}")

        logger.info(f"Model extracted. Ready: {model_is_ready()}")
        return model_is_ready()

    except Exception as e:
        logger.error(f"Model download failed: {e}")
        # Clean up partial download
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = download_model()
    exit(0 if success else 1)
