import cv2
import numpy as np
import json
from pathlib import Path

def generate_masks(ann_json_path, img_dir, out_mask_dir):
    """
    Converts COCO bounding box annotations to pixel-level severity masks.
    
    Severity Mapping:
    - D00 (longitudinal crack) -> 1
    - D10 (alligator crack)    -> 2
    - D40 (pothole)            -> 3
    - Background               -> 0
    """
    ann_json_path = Path(ann_json_path)
    img_dir = Path(img_dir)
    out_mask_dir = Path(out_mask_dir)
    
    # Create output directory if it doesn't exist
    out_mask_dir.mkdir(parents=True, exist_ok=True)
    
    if not ann_json_path.exists():
        print(f"Error: Annotation file not found at {ann_json_path}")
        return

    print(f"Loading annotations from {ann_json_path}...")
    with open(ann_json_path, 'r') as f:
        data = json.load(f)
        
    images = {img['id']: img for img in data['images']}
    annotations = data['annotations']
    categories = {cat['id']: cat['name'] for cat in data['categories']}
    
    # Define mapping from RDD2022 category names to severity indices
    name_to_severity = {
        "D00": 1,
        "D10": 2,
        "D40": 3
    }
    
    # Map COCO category IDs to severity values
    id_to_severity = {}
    for cat_id, name in categories.items():
        if name in name_to_severity:
            id_to_severity[cat_id] = name_to_severity[name]
        else:
            # Handle cases where names might have prefixes or be different
            for key in name_to_severity:
                if key in name:
                    id_to_severity[cat_id] = name_to_severity[key]
                    break
    
    # Group annotations by image_id
    img_to_anns = {}
    for ann in annotations:
        img_id = ann['image_id']
        if img_id not in img_to_anns:
            img_to_anns[img_id] = []
        img_to_anns[img_id].append(ann)
        
    count = 0
    total_images = len(images)
    print(f"Processing {total_images} images...")
    
    for img_id, img_info in images.items():
        file_name = img_info['file_name']
        height = img_info['height']
        width = img_info['width']
        
        # Create empty mask (same size as original image)
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # Get annotations for this image
        anns = img_to_anns.get(img_id, [])
        
        for ann in anns:
            cat_id = ann['category_id']
            severity = id_to_severity.get(cat_id, 0)
            
            if severity > 0:
                bbox = ann['bbox'] # [x, y, width, height]
                x, y, w, h = map(int, bbox)
                
                # Fill bounding box with severity value
                # Ensure coordinates are within image bounds
                y_end = min(y + h, height)
                x_end = min(x + w, width)
                mask[y:y_end, x:x_end] = severity
        
        # Resize mask to 224x224 using Nearest Neighbor interpolation
        mask_resized = cv2.resize(mask, (224, 224), interpolation=cv2.INTER_NEAREST)
        
        # Save mask as {image_stem}_mask.png
        image_stem = Path(file_name).stem
        mask_path = out_mask_dir / f"{image_stem}_mask.png"
        cv2.imwrite(str(mask_path), mask_resized)
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count}/{total_images} images...")
            
    print(f"Finished. Total masks generated: {count}")

if __name__ == "__main__":
    # Default paths as per requirements
    ann_json_path = "data/raw/annotations/instances_train.json"
    img_dir       = "data/raw/images/train"
    out_mask_dir  = "data/processed/masks"
    
    generate_masks(ann_json_path, img_dir, out_mask_dir)
