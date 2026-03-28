import os
import logging
import tensorflow as tf
import numpy as np
import cv2
from pathlib import Path
from sklearn.model_selection import train_test_split
import albumentations as A

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_augmentations(img_size=224):
    """
    Advanced Albumentations pipeline for high-accuracy classification.
    """
    return A.Compose([
        A.Resize(img_size, img_size),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.MotionBlur(blur_limit=5, p=0.3),
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
        A.HorizontalFlip(p=0.5),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5),
        A.OneOf([
            A.RandomShadow(p=0.2),
            A.RandomFog(p=0.1),
        ], p=0.3),
    ], additional_targets={'mask': 'mask'}, is_check_shapes=False)

class PotholeDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, img_paths, cls_labels, mask_dir, batch_size=16, augment=False, img_size=224):
        self.img_paths = img_paths
        self.cls_labels = cls_labels
        self.mask_dir = Path(mask_dir)
        self.batch_size = batch_size
        self.augment = augment
        self.img_size = img_size
        self.aug_pipeline = get_augmentations(img_size) if augment else A.Resize(img_size, img_size)
        self.indices = np.arange(len(self.img_paths))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.img_paths) / self.batch_size))

    def on_epoch_end(self):
        if self.augment:
            np.random.shuffle(self.indices)

    def _load_mask(self, img_path):
        """Construct mask path, load, resize, and one-hot encode."""
        image_stem = Path(img_path).stem
        # Check for multiple possible mask naming conventions
        mask_variants = [f"{image_stem}_mask.png", f"{image_stem}.png"]
        mask_path = None
        for variant in mask_variants:
            if (self.mask_dir / variant).exists():
                mask_path = self.mask_dir / variant
                break
        
        if mask_path:
            mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            mask = cv2.resize(mask, (self.img_size, self.img_size), interpolation=cv2.INTER_NEAREST)
        else:
            mask = np.zeros((self.img_size, self.img_size), dtype=np.uint8)
            
        return mask

    def __getitem__(self, index):
        batch_indices = self.indices[index * self.batch_size : (index + 1) * self.batch_size]
        
        X = []
        Y_cls = []
        Y_seg = []
        
        for i in batch_indices:
            img_path = self.img_paths[i]
            img = cv2.imread(img_path)
            if img is None: continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize image to target size BEFORE augmentation to match mask
            img = cv2.resize(img, (self.img_size, self.img_size))
            
            # Load and resize mask (already uses INTER_NEAREST)
            mask = self._load_mask(img_path)
            
            # Apply Albumentations
            if self.augment:
                augmented = self.aug_pipeline(image=img, mask=mask)
                img = augmented['image']
                mask = augmented['mask']
            else:
                # Still need to ensure output size matches config
                img = cv2.resize(img, (self.img_size, self.img_size))
                mask = cv2.resize(mask, (self.img_size, self.img_size), interpolation=cv2.INTER_NEAREST)
                
            # Normalize image
            img = img.astype(np.float32) / 255.0
            
            # One-hot encode mask (4 classes)
            mask_one_hot = np.eye(4)[mask.astype(int)]
            
            X.append(img)
            
            # Labels
            cls_label = self.cls_labels[i]
            Y_cls.append(cls_label)
            Y_seg.append(mask_one_hot)
            
        return np.array(X), \
               {"cls_output": np.array(Y_cls), "seg_output": np.array(Y_seg)}

def build_generators(data_dir, mask_dir, batch_size=8, val_split=0.2, img_size=160):
    """
    Improved recursive scanner that returns tf.data.Dataset for OOM efficiency.
    """
    img_paths = []
    cls_labels = []
    
    logger.info(f"🔍 Scanning {data_dir} for images...")
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                img_path = os.path.join(root, file)
                path_lower = img_path.lower()
                
                # Dynamic Class Assignment
                if "pothole" in path_lower: label_idx = 2
                elif "crack" in path_lower or "damage" in path_lower: label_idx = 1
                else: label_idx = 0
                
                img_paths.append(img_path)
                label = np.zeros(3, dtype=np.float32)
                label[label_idx] = 1.0
                cls_labels.append(label)

    if not img_paths:
        raise ValueError(f"No images found in {data_dir}")

    # Log Distribution
    dist = np.sum(cls_labels, axis=0)
    logger.info(f"📊 Dataset: Normal={int(dist[0])}, Crack={int(dist[1])}, Pothole={int(dist[2])}")

    train_imgs, val_imgs, train_labels, val_labels = train_test_split(
        img_paths, cls_labels, 
        test_size=val_split, 
        stratify=np.argmax(cls_labels, axis=1), 
        random_state=42
    )
    
    # Create PotholeDataGenerator instances
    train_gen = PotholeDataGenerator(train_imgs, train_labels, mask_dir, batch_size=batch_size, augment=True, img_size=img_size)
    val_gen = PotholeDataGenerator(val_imgs, val_labels, mask_dir, batch_size=batch_size, augment=False, img_size=img_size)
    
    # Convert to tf.data.Dataset for better performance and prefetching
    def generator_fn(gen):
        for i in range(len(gen)):
            yield gen[i]

    output_signature = (
        tf.TensorSpec(shape=(None, img_size, img_size, 3), dtype=tf.float32),
        {
            "cls_output": tf.TensorSpec(shape=(None, 3), dtype=tf.float32),
            "seg_output": tf.TensorSpec(shape=(None, img_size, img_size, 4), dtype=tf.float32)
        }
    )

    train_ds = tf.data.Dataset.from_generator(
        lambda: generator_fn(train_gen),
        output_signature=output_signature
    ).prefetch(tf.data.AUTOTUNE)

    val_ds = tf.data.Dataset.from_generator(
        lambda: generator_fn(val_gen),
        output_signature=output_signature
    ).prefetch(tf.data.AUTOTUNE)
    
    # Add caching for validation to speed up training if RAM allows
    val_ds = val_ds.cache()
    
    return train_ds, val_ds


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
        split_dir = os.path.join(config.RAW_DATA_DIR, split)
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
