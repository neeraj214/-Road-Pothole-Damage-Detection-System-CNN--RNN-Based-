import os
import logging
import tensorflow as tf
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_preprocess_image(image_path, mask_path, class_id, target_size, num_classes, num_seg_classes):
    """Loads and preprocesses an image and its corresponding mask and label."""
    # 1. Image
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, target_size)
    img = tf.cast(img, tf.float32) / 255.0

    # 2. Mask (Expected to be grayscale with values 0, 1, 2, 3)
    mask = tf.io.read_file(mask_path)
    mask = tf.image.decode_png(mask, channels=1)
    mask = tf.image.resize(mask, target_size, method="nearest")
    mask = tf.cast(mask, tf.int32)
    # One-hot encode mask to shape (H, W, num_seg_classes)
    mask = tf.one_hot(tf.squeeze(mask, axis=-1), depth=num_seg_classes)

    # 3. Label (One-hot encoding)
    label = tf.one_hot(class_id, depth=num_classes)

    return img, {"classification_output": label, "segmentation_output": mask}

def get_data_generators(config):
    """
    Creates tf.data.Dataset generators for images, masks, and classification labels.
    """
    datasets = {}
    target_size = config.INPUT_SHAPE[:2]
    num_classes = len(config.CLASSES)
    num_seg_classes = config.NUM_SEG_CLASSES

    for split in ["train", "val", "test"]:
        # ... (same directory logic)
        split_dir = os.path.join(config.RAW_DATA_DIR, split)
        # ... (rest of the path collection logic remains similar)
        # Assuming the directory structure is maintained
        image_paths = []
        mask_paths = []
        class_ids = []

        if not os.path.exists(split_dir):
            continue

        images_root = os.path.join(split_dir, "images")
        masks_root = os.path.join(split_dir, "masks")

        if not os.path.exists(images_root) or not os.path.exists(masks_root):
            continue

        for idx, class_name in enumerate(config.CLASSES):
            class_img_dir = os.path.join(images_root, class_name)
            class_mask_dir = os.path.join(masks_root, class_name)

            if not os.path.exists(class_img_dir):
                continue

            for img_name in os.listdir(class_img_dir):
                img_path = os.path.join(class_img_dir, img_name)
                mask_name = os.path.splitext(img_name)[0] + ".png"
                mask_path = os.path.join(class_mask_dir, mask_name)

                if os.path.exists(mask_path):
                    image_paths.append(img_path)
                    mask_paths.append(mask_path)
                    class_ids.append(idx)

        if not image_paths:
            continue

        dataset = tf.data.Dataset.from_tensor_slices((image_paths, mask_paths, class_ids))
        if split == "train":
            dataset = dataset.shuffle(buffer_size=len(image_paths), seed=config.RANDOM_SEED)

        dataset = dataset.map(
            lambda img_p, mask_p, cid: load_and_preprocess_image(img_p, mask_p, cid, target_size, num_classes, num_seg_classes),
            num_parallel_calls=tf.data.AUTOTUNE
        )

        dataset = dataset.batch(config.BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
        datasets[split] = dataset

    return datasets.get("train"), datasets.get("val"), datasets.get("test")
