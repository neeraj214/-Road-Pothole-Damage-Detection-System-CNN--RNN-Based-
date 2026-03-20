import os
import logging
import tensorflow as tf
import numpy as np
import cv2
from pathlib import Path
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PotholeDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, img_paths, cls_labels, mask_dir, batch_size=16, augment=False):
        self.img_paths = img_paths
        self.cls_labels = cls_labels
        self.mask_dir = Path(mask_dir)
        self.batch_size = batch_size
        self.augment = augment
        self.indices = np.arange(len(self.img_paths))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.img_paths) / self.batch_size))

    def on_epoch_end(self):
        if self.augment:
            np.random.shuffle(self.indices)

    def _load_mask(self, img_path):
        image_stem = Path(img_path).stem
        mask_path = self.mask_dir / f"{image_stem}_mask.png"
        
        if mask_path.exists():
            mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            mask = cv2.resize(mask, (224, 224), interpolation=cv2.INTER_NEAREST)
        else:
            mask = np.zeros((224, 224), dtype=np.uint8)
            
        # One-hot encode to (224, 224, 4)
        mask_one_hot = tf.keras.utils.to_categorical(mask, num_classes=4)
        return mask_one_hot

    def _augment(self, img, mask):
        # IDENTICAL spatial transforms
        if np.random.rand() > 0.5:
            img = cv2.flip(img, 1)
            mask = cv2.flip(mask, 1)
            
        if np.random.rand() > 0.5:
            img = cv2.flip(img, 0)
            mask = cv2.flip(mask, 0)

        # Brightness jitter applies to img only
        if np.random.rand() > 0.5:
            brightness = np.random.uniform(0.8, 1.2)
            img = np.clip(img * brightness, 0, 1)

        return img, mask

    def __getitem__(self, index):
        batch_indices = self.indices[index * self.batch_size : (index + 1) * self.batch_size]
        
        X = []
        Y_cls = []
        Y_seg = []
        
        for i in batch_indices:
            img_path = self.img_paths[i]
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224)) / 255.0
            
            mask = self._load_mask(img_path)
            
            if self.augment:
                img, mask = self._augment(img, mask)
                
            X.append(img)
            Y_cls.append(self.cls_labels[i])
            Y_seg.append(mask)
            
        return np.array(X), {
            "cls_output": np.array(Y_cls),
            "seg_output": np.array(Y_seg)
        }

def build_generators(data_dir, mask_dir, batch_size=16, val_split=0.15):
    img_paths = []
    cls_labels = []
    
    classes = ["normal", "crack", "pothole"]
    for idx, cls_name in enumerate(classes):
        cls_dir = os.path.join(data_dir, cls_name)
        if not os.path.exists(cls_dir):
            continue
            
        for img_name in os.listdir(cls_dir):
            if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_paths.append(os.path.join(cls_dir, img_name))
                # One-hot encode classification label
                label = np.zeros(3)
                label[idx] = 1
                cls_labels.append(label)
                
    train_imgs, val_imgs, train_labels, val_labels = train_test_split(
        img_paths, cls_labels, test_size=val_split, stratify=np.argmax(cls_labels, axis=1), random_state=42
    )
    
    train_gen = PotholeDataGenerator(train_imgs, train_labels, mask_dir, batch_size=batch_size, augment=True)
    val_gen = PotholeDataGenerator(val_imgs, val_labels, mask_dir, batch_size=batch_size, augment=False)
    
    return train_gen, val_gen

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
