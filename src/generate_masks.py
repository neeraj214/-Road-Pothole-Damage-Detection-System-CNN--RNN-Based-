import json
import cv2
import numpy as np
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def generate_masks(ann_json_path, img_dir, out_mask_dir):
    """
    Converts COCO-format bounding box annotations into pixel-level severity masks.
    
    Args:
        ann_json_path (str/Path): Path to COCO JSON annotation file.
        img_dir (str/Path): Directory containing original images.
        out_mask_dir (str/Path): Directory to save generated masks.
    """
    ann_json_path = Path(ann_json_path)
    img_dir = Path(img_dir)
    out_mask_dir = Path(out_mask_dir)
    out_mask_dir.mkdir(parents=True, exist_ok=True)

    if not ann_json_path.exists():
        logger.error(f"Annotation file not found: {ann_json_path}")
        return

    logger.info(f"Reading annotations from {ann_json_path}...")
    with open(ann_json_path, "r") as f:
        coco_data = json.load(f)

    # Category Mapping (RDD2022 -> Severity Index)
    # D00: longitudinal crack -> 1
    # D10: alligator crack -> 2
    # D40: pothole -> 3
    # Others or Background -> 0
    cat_id_to_severity = {}
    for cat in coco_data.get("categories", []):
        name = cat["name"].upper()
        if "D00" in name:
            cat_id_to_severity[cat["id"]] = 1
        elif "D10" in name:
            cat_id_to_severity[cat["id"]] = 2
        elif "D40" in name:
            cat_id_to_severity[cat["id"]] = 3
        else:
            cat_id_to_severity[cat["id"]] = 0

    # Group annotations by image_id
    img_id_to_anns = {}
    for ann in coco_data.get("annotations", []):
        img_id = ann["image_id"]
        if img_id not in img_id_to_anns:
            img_id_to_anns[img_id] = []
        img_id_to_anns[img_id].append(ann)

    processed_count = 0
    total_images = len(coco_data.get("images", []))
    logger.info(f"Processing {total_images} images...")

    for img_info in coco_data.get("images", []):
        img_id = img_info["id"]
        file_name = img_info["file_name"]
        height = img_info["height"]
        width = img_info["width"]
        
        # Create empty mask (H x W, single-channel uint8)
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # Fill bounding boxes if annotations exist
        if img_id in img_id_to_anns:
            for ann in img_id_to_anns[img_id]:
                cat_id = ann["category_id"]
                severity = cat_id_to_severity.get(cat_id, 0)
                if severity == 0:
                    continue
                
                # Bounding box in COCO format [x, y, w, h]
                x, y, w, h = map(int, ann["bbox"])
                
                # Fill rectangle with severity value
                # Note: x+w and y+h are the bottom-right corner
                cv2.rectangle(mask, (x, y), (x + w, y + h), int(severity), -1)
        
        # Resize mask to 224x224 using NEAREST interpolation
        # This preserves discrete class values (0, 1, 2, 3)
        mask_resized = cv2.resize(mask, (224, 224), interpolation=cv2.INTER_NEAREST)
        
        # Save mask as {image_stem}_mask.png
        image_stem = Path(file_name).stem
        mask_filename = f"{image_stem}_mask.png"
        mask_path = out_mask_dir / mask_filename
        
        cv2.imwrite(str(mask_path), mask_resized)
        
        processed_count += 1
        if processed_count % 500 == 0:
            logger.info(f"Processed {processed_count}/{total_images} images...")

    logger.info(f"Finished! Total masks generated: {processed_count}")
    logger.info(f"Masks saved to: {out_mask_dir}")

if __name__ == "__main__":
    # Default paths for RDD2022
    ann_json_path = "data/raw/annotations/instances_train.json"
    img_dir       = "data/raw/images/train"
    out_mask_dir  = "data/processed/masks"
    
    # Check if directories exist, if not log a warning
    if not Path(ann_json_path).parent.exists():
        logger.warning(f"Path not found: {Path(ann_json_path).parent}. Please ensure RDD2022 data is present.")
    
    generate_masks(ann_json_path, img_dir, out_mask_dir)
