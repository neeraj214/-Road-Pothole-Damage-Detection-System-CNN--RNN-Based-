import os
import requests
import logging

logger = logging.getLogger(__name__)

MODEL_DIR = "models/best_model_dual_v6_deeper_tf"
VARIABLES_DIR = f"{MODEL_DIR}/variables"
BASE_URL = "https://huggingface.co/Neeraj214/road-pothole-model/resolve/main"

FILES_TO_DOWNLOAD = [
    (f"{BASE_URL}/saved_model.pb",
     f"{MODEL_DIR}/saved_model.pb"),
    (f"{BASE_URL}/keras_metadata.pb",
     f"{MODEL_DIR}/keras_metadata.pb"),
    (f"{BASE_URL}/variables/variables.index",
     f"{VARIABLES_DIR}/variables.index"),
    (f"{BASE_URL}/variables/variables.data-00000-of-00001",
     f"{VARIABLES_DIR}/variables.data-00000-of-00001"),
]

def download_file(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    logger.info(f"Downloading {os.path.basename(dest_path)}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    size_mb = os.path.getsize(dest_path) / (1024 * 1024)
    logger.info(f"Saved {os.path.basename(dest_path)} ({size_mb:.1f} MB)")

def model_is_ready():
    return os.path.exists(f"{MODEL_DIR}/saved_model.pb")

def download_model():
    if model_is_ready():
        logger.info(f"Model already exists at {MODEL_DIR}")
        return True

    logger.info("Downloading model files individually from Hugging Face...")
    try:
        for url, dest in FILES_TO_DOWNLOAD:
            download_file(url, dest)
        logger.info("All model files downloaded successfully.")
        return model_is_ready()
    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    download_model()
