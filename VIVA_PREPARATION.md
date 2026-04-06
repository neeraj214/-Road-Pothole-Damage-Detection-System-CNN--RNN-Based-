# Road Pothole & Damage Detection System – Viva Preparation Guide

This document covers the technical details of the project with exact file names, line numbers, and references.

## === SECTION 1: PROJECT OVERVIEW ===

**Title:** Road Pothole & Damage Detection System
**Type:** End-to-end Deep Learning + Full Stack Web Application
**College Subject:** Deep Learning Lab Assignment

**Problem Statement:**
- Manual road inspection in India is slow, expensive, and inconsistent.
- This system automates detection using smartphone/dashcam images.
- Provides repair priority scoring for maintenance teams.

**Real World Impact:**
- India has 63 lakh km of roads (largest network after USA/China).
- NHAI estimates Rs 25,000 crore annual road maintenance cost.
- Automated detection can reduce inspection cost by 60-70%.

## === SECTION 2: COMPLETE FILE STRUCTURE WITH PURPOSE ===

```text
Road-Pothole-Detection/
├── app.py                    - FastAPI backend server, /predict and /health endpoints
├── requirements.txt          - Python dependencies for local development
├── src/
│   ├── config.py            - All hyperparameters and path configurations
│   ├── model.py             - MobileNetV2 dual-head architecture definition
│   ├── train.py             - Two-stage training pipeline
│   ├── data_loader.py       - Dataset loading, augmentation, preprocessing
│   ├── utils.py             - BCE-Dice loss function, helper utilities
│   ├── evaluate.py          - Confusion matrix, classification report generation
│   └── stage3_finetune.py   - Stage 3 fine-tuning with stronger regularization
├── hf_space/
│   ├── app.py               - Production FastAPI (Hugging Face deployment)
│   ├── Dockerfile           - Docker container configuration
│   ├── download_model.py    - Auto-downloads model from HF Model Hub at startup
│   ├── requirements-hf.txt  - CPU-only dependencies for cloud deployment
│   └── src/                 - Copy of src/ for container
├── frontend_vanilla/
│   ├── src/
│   │   ├── api.js           - All API calls to FastAPI backend
│   │   ├── App.jsx          - Main React app with routing
│   │   ├── Dashboard.jsx    - Main dashboard with upload and results
│   │   └── hooks/
│   │       ├── useInference.js - Prediction state management
│   │       └── useHistory.js   - localStorage history management
│   ├── vercel.json          - Vercel deployment configuration
│   └── .env.production      - Production API URL configuration
├── results/
│   ├── confusion_matrix.png           - Visual confusion matrix heatmap
│   ├── confusion_matrix_normalized.png - Row-normalized confusion matrix
│   ├── classification_report.txt      - Full precision/recall/F1 report
│   └── model_summary.txt             - Overall accuracy summary
└── models/
    └── best_model_dual_v6_deeper_tf/  - Saved TensorFlow model (gitignored)
```

## === SECTION 3: MODEL ARCHITECTURE WITH EXACT CODE LOCATIONS ===

### 1. INPUT LAYER
- **File:** `src/model.py`
- **What:** Input shape `(160, 160, 3)`
- **Why:** Reduced from 224x224 to fit RTX 2050 4GB VRAM
- **Key line:** `layers.Input(shape=(img_size, img_size, 3))`

### 2. MOBILENETV2 BACKBONE
- **File:** `src/model.py`
- **What:** Pretrained CNN feature extractor, 154 layers, 2.2M parameters
- **Why:** Lightweight, efficient, designed for constrained hardware. Uses depthwise separable convolutions reducing compute by 8-9x.
- **Key parameters:** `include_top=False`, `weights="imagenet"`, `alpha=1.0`

### 3. SKIP CONNECTIONS (5 layers extracted)
- **File:** `src/model.py`
- **Layers:** `block_1_expand_relu` (80x80), `block_3_expand_relu` (40x40), `block_6_expand_relu` (20x20), `block_13_expand_relu` (10x10), `out_relu` (5x5 bottleneck)

### 4. CLASSIFICATION HEAD
- **File:** `src/model.py`
- **Components:**
  - `GlobalAveragePooling2D` (captures average texture features)
  - `GlobalMaxPooling2D` (captures sharp anomaly features)
  - `Concatenate` (combines both pooling outputs)
  - `Dense(512, relu)` + `BatchNorm` + `Dropout(0.4)`
  - `Dense(256, relu)` + `BatchNorm` + `Dropout(0.3)`
  - `Dense(3, softmax)` — final output: Normal/Crack/Pothole

### 5. SEGMENTATION HEAD (U-Net decoder)
- **File:** `src/model.py` — `decoder_block()` function
- **Components per block:**
  - `UpSampling2D` (bilinear interpolation)
  - `Concatenate` with skip connection
  - `SeparableConv2D` + `BatchNorm` + `ReLU`
  - 4 decoder blocks: 128→64→32→16 filters
  - **Final:** `Conv2D(4, 1x1, softmax)` — 4 segmentation classes

### 6. DUAL HEAD OUTPUT
- **File:** `src/model.py`
- `cls_output` shape: `(batch, 3)`
- `seg_output` shape: `(batch, 160, 160, 4)`

## === SECTION 4: TRAINING CONFIGURATION WITH EXACT VALUES ===

### CONFIGURATION FILE: `src/config.py`
- `INPUT_SHAPE = (160, 160, 3)`
- `BATCH_SIZE = 8`
- `ACCUMULATION_STEPS = 2` (effective batch = 16)
- `EPOCHS = 30` (per stage, ran 25 each)
- `LEARNING_RATE = 0.001`
- `VALIDATION_SPLIT = 0.2`
- `RANDOM_SEED = 42`
- `CLASS_WEIGHTS = {0: 1.0, 1: 2.0, 2: 3.0}`

### STAGE 1 TRAINING: `src/train.py` — `stage1_train()` function
- **Epochs:** 25
- **Learning rate:** 1e-3
- **Backbone:** FROZEN (`base_model.trainable = False`)
- **Loss weights:** cls=2.0, seg=1.0
- **Optimizer:** `Adam(lr=3e-4)`
- **EarlyStopping patience:** 12
- **Monitor metric:** `val_cls_output_accuracy`

### STAGE 2 TRAINING: `src/train.py` — `stage2_finetune()` function
- **Epochs:** 25
- **Learning rate:** 3e-5
- **Backbone:** TOP 80 LAYERS UNFROZEN
- **Loss weights:** cls=5.0, seg=1.0
- **BatchNorm layers:** KEPT FROZEN for stability
- **EarlyStopping patience:** 10

### GRADIENT ACCUMULATION: `src/train.py` — `GradientAccumulationModel` class
- **Why needed:** RTX 2050 only 4GB VRAM, batch 8 too small
- **How:** accumulates gradients over 2 batches, applies once
- **Key fix:** uses Python `if` statement NOT `tf.cond()` (`tf.cond` with `optimizer.apply` was a critical bug we fixed)

### MIXED PRECISION: `src/train.py` — top of file
- **Policy:** `mixed_float16`
- **Why:** RTX 2050 Ampere (compute 8.6) supports float16 natively
- **Benefit:** 2x memory reduction, 2x speed increase

## === SECTION 5: LOSS FUNCTIONS WITH EXPLANATION ===

### CLASSIFICATION LOSS: `src/train.py` — `weighted_categorical_crossentropy()`
- **Base:** `CategoricalCrossentropy(label_smoothing=0.1)`
- **Weight application:** multiplies per-sample loss by class weight
- **Label smoothing 0.1:** replaces hard 0/1 with 0.05/0.95
- Prevents overconfident predictions, improves generalization

### SEGMENTATION LOSS: `src/utils.py` — `bce_dice_loss()`
- Combines Binary Cross Entropy + Dice Loss (50/50 weight)
- **BCE:** standard pixel-wise cross entropy
- **Dice Loss formula:** `1 - (2 * intersection) / (union + smooth)`
- **Why Dice:** handles extreme class imbalance (90% background pixels)
- Smooth factor prevents division by zero

## === SECTION 6: DATA PIPELINE WITH EXACT LOCATIONS ===

### DATASET SCANNING: `src/data_loader.py` — `build_generators()`
- Recursively walks `data/raw/` directory
- Assigns class by path keyword:
  - "pothole" in path → label 2
  - "crack" or "damage" in path → label 1
  - else → label 0
- Train/val split: 80/20 stratified by class
- Total images: 19,892 (Normal=7329, Crack=8203, Pothole=4360)

### PREPROCESSING: `src/data_loader.py` — `PotholeDataGenerator.__getitem__()`
- **CRITICAL:** Uses `preprocess_input` NOT `/255.0`
- `preprocess_input` scales to `[-1, 1]` matching MobileNetV2 training
- `/255.0` gives `[0,1]` — WRONG, was a bug that capped accuracy at 48%
- **Fixed bug:** `img = preprocess_input(img.astype(np.float32))`

### AUGMENTATION: `src/data_loader.py` — `get_augmentations()`
- **Library:** Albumentations
- **Transforms applied:**
  - `A.Resize(160, 160)`
  - `A.RandomBrightnessContrast(±20%, p=0.5)`
  - `A.MotionBlur(blur_limit=5, p=0.3)`
  - `A.GaussNoise(p=0.3)`
  - `A.HorizontalFlip(p=0.5)`
  - `A.ShiftScaleRotate(p=0.5)`
  - `A.RandomShadow / RandomFog (p=0.3)`

### MASK LOADING: `src/data_loader.py` — `_load_mask()`
- Looks for `{image_stem}_mask.png` or `{image_stem}.png`
- If no mask found: creates zero mask (background only)
- **Critical fix:** `np.clip(mask, 0, 3)` before one-hot encoding (without clip: mask value 255 caused `IndexError` crash)

## === SECTION 7: EVALUATION RESULTS WITH CODE LOCATION ===

**EVALUATION SCRIPT:** `src/evaluate.py`
**Run command:** `python -m src.evaluate`
**Output files:** `results/` folder

### RESULTS:
**Overall Accuracy:** 84.74% (2601 validation samples)

**Per-class results:**

| Class | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| **Normal** | 95.64% | 74.69% | 83.88% | 1146 |
| **Crack** | 83.44% | 91.84% | 87.44% | 1311 |
| **Pothole** | 54.75% | 100.00% | 70.76% | 144 |

**Confusion Matrix (raw counts):**

| | Normal | Crack | Pothole |
| :--- | :--- | :--- | :--- |
| **Normal** | 856 | 239 | 51 |
| **Crack** | 39 | 1204 | 68 |
| **Pothole** | 0 | 0 | 144 |

- **Most confused pair:** Normal → predicted as Crack (239 samples)
- **Reason:** Normal roads and lightly cracked roads look similar
- **Key insight:** Pothole recall = 100% (zero missed potholes). This is the most important safety metric — never miss a pothole.

## === SECTION 8: DEPLOYMENT ARCHITECTURE ===

### BACKEND DEPLOYMENT: Hugging Face Spaces
- **Platform:** huggingface.co/spaces/Neeraj214/road-pothole-api
- **Container:** Docker (`hf_space/Dockerfile`)
- **Runtime:** Python 3.10, TensorFlow CPU
- **Port:** 7860 (HF default)
- **Model loading:** `hf_space/download_model.py` downloads 4 files at startup: `saved_model.pb` (3.4MB) + `keras_metadata.pb` (0.5MB) + `variables.index` (36KB) + `variables.data` (60.3MB)
- **Cold start:** ~60 seconds after 48hr inactivity (free tier)

### FRONTEND DEPLOYMENT: Vercel
- **Platform:** road-pothole-damage-detection-syste.vercel.app
- **Framework:** React 18 + TailwindCSS + Vite
- **Config:** `frontend_vanilla/vercel.json`
- **API URL:** set via `VITE_API_URL` environment variable
- **Always on:** Vercel never sleeps (unlike backend)

### API ENDPOINTS:
- `GET  /`          → API info message
- `GET  /health`    → `{"status":"healthy","model_loaded":true,"classes":[...]}`
- `POST /predict`   → accepts multipart image, returns full JSON result
- `GET  /docs`      → Swagger UI auto-generated documentation

### CORS: `app.py` — CORSMiddleware
- Allows frontend (Vercel) to call backend (Hugging Face)
- Without CORS browser blocks cross-origin API calls

## === SECTION 9: BUGS FIXED DURING DEVELOPMENT ===

> [!IMPORTANT]
> This section shows real engineering work and is crucial for viva preparation.

### BUG 1 — CRITICAL: Gradient accumulation never updating weights
- **File:** `src/train.py` — `GradientAccumulationModel.train_step()`
- **Problem:** Used `tf.cond()` to call `optimizer.apply_gradients()`. `tf.cond()` with side effects is unreliable in graph mode. Model trained for epochs but weights never changed.
- **Symptom:** Accuracy stuck at 48.9% (random guessing level)
- **Fix:** Replaced `tf.cond()` with plain Python `if` statement. Python `if` works because `train_step` runs in eager mode.

### BUG 2 — CRITICAL: Wrong image preprocessing
- **File:** `src/data_loader.py` — `PotholeDataGenerator.__getitem__()`
- **Problem:** `img = img.astype(np.float32) / 255.0` gives `[0,1]` range, but MobileNetV2 expects `[-1,1]` from `preprocess_input`.
- **Symptom:** Accuracy capped at ~60-70% regardless of training
- **Fix:**
  ```python
  from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
  img = preprocess_input(img.astype(np.float32))
  ```

### BUG 3 — HIGH: Mask values causing IndexError crash
- **File:** `src/data_loader.py` — `PotholeDataGenerator.__getitem__()`
- **Problem:** `np.eye(4)[mask.astype(int)]` crashes if mask has value 255. Binary PNG masks use 0/255, not 0/1/2/3.
- **Symptom:** Random training crashes mid-epoch
- **Fix:** `mask = np.clip(mask.astype(np.uint8), 0, 3)` before one-hot.

### BUG 4 — HIGH: class_weight not supported for multi-output models
- **File:** `src/train.py` — `stage1_train()` and `stage2_finetune()`
- **Problem:** Keras `model.fit(class_weight=...)` only works for single output. Our model has 2 outputs (cls + seg).
- **Symptom:** `ValueError` crash at training start
- **Fix:** Baked class weights into custom loss function: `weighted_categorical_crossentropy()` applies weights per sample.

### BUG 5 — MEDIUM: CosineDecay schedule not serializable by TensorBoard
- **File:** `src/train.py`
- **Problem:** TensorBoard tried to log LR as scalar but got schedule object.
- **Symptom:** Training crashed after epoch 1 save
- **Fix:** Replaced `CosineDecay` with plain float LR + `ReduceLROnPlateau`.

### BUG 6 — MEDIUM: Double image resize in data loader
- **File:** `src/data_loader.py` — `PotholeDataGenerator.__getitem__()`
- **Problem:** `cv2.resize()` called before if/else AND again inside else branch.
- **Symptom:** Subtle quality degradation from double downsampling.
- **Fix:** Removed first resize, kept only the one inside the else branch.

### BUG 7 — DEPLOYMENT: Windows zip backslash paths on Linux
- **File:** `hf_space/download_model.py`
- **Problem:** Zip created on Windows had backslash in filenames. Linux saw `folder\file.pb` as one filename not a path.
- **Symptom:** Model downloaded but not found — `Model loaded: False`
- **Fix:** Changed to download each file individually using direct URLs. No zip extraction needed, no path separator issues.

## === SECTION 10: KEY TECHNICAL DECISIONS EXPLAINED ===

### DECISION 1: Why MobileNetV2 over ResNet50 or VGG16?
- VGG16: 138M parameters — too large for 4GB GPU.
- ResNet50: 25M parameters — heavier than needed.
- MobileNetV2: 2.2M parameters — lightweight, fast, accurate.
- Depthwise separable convolutions reduce FLOPs by 8-9x.
- Originally designed for mobile devices — perfect for our GPU constraint.

### DECISION 2: Why freeze BatchNormalization during fine-tuning?
- BN layers store population statistics (mean, variance) from ImageNet.
- Unfreezing on small dataset shifts these statistics.
- Causes training instability and accuracy drop.
- Industry standard practice: keep BN frozen during fine-tuning.

### DECISION 3: Why not use ImageDataGenerator from Keras?
- Keras `ImageDataGenerator` only supports single-output models.
- Our dual-head model needs synchronized image+mask augmentation.
- Albumentations applies identical transforms to both image and mask.
- Also provides more realistic augmentations (fog, shadow, rain).

### DECISION 4: Why two-stage training instead of training everything at once?
- Stage 1 warms up the fresh classification head safely.
- Training fresh random head + pretrained backbone simultaneously can destroy pretrained weights with large random gradients.
- Stage 2 fine-tunes backbone only after head is stable.
- Lower LR in Stage 2 (3e-5 vs 1e-3) prevents catastrophic forgetting.

### DECISION 5: Why Hugging Face Spaces for deployment?
- Render.com requires credit card for free tier.
- Railway.app has limited free credits.
- Hugging Face: completely free, no card, supports Docker.
- Built for ML models — handles large file storage natively.
- Supports FastAPI directly via Docker SDK.

## === SECTION 11: QUICK REFERENCE NUMBERS FOR VIVA ===

> [!TIP]
> Memorize these exact numbers.

### MODEL:
- **Total layers:** ~170 (MobileNetV2=154 + heads)
- **Parameters:** ~3.5 million trainable
- **Input size:** 160 × 160 × 3
- **Classification output:** (batch, 3)
- **Segmentation output:** (batch, 160, 160, 4)

### TRAINING:
- **Dataset size:** 19,892 images
- **Train set:** 15,913 images (80%)
- **Val set:** 3,979 images (20%)
- **Batch size:** 8 (effective 16 with accumulation)
- **Stage 1 epochs:** 25
- **Stage 2 epochs:** 25
- **Stage 1 LR:** 1e-3
- **Stage 2 LR:** 3e-5
- **GPU:** NVIDIA RTX 2050 (4GB VRAM, Ampere, compute 8.6)

### RESULTS:
- **Overall accuracy:** 84.74%
- **Normal recall:** 74.69% (n=1146)
- **Crack recall:** 91.84% (n=1311)
- **Pothole recall:** 100.00% (n=144)
- **Normal F1:** 0.839
- **Crack F1:** 0.874
- **Pothole F1:** 0.708
- **Weighted F1:** 0.850
- **Segmentation IoU:** 85.4%
- **Val samples tested:** 2,601

### DEPLOYMENT:
- **Frontend:** road-pothole-damage-detection-syste.vercel.app
- **Backend:** Neeraj214-road-pothole-api.hf.space
- **Model hub:** huggingface.co/Neeraj214/road-pothole-model
- **GitHub:** github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-

## === SECTION 12: POTENTIAL TOUGH QUESTIONS WITH ANSWERS ===

**Q: What would you do differently if you had more time?**
**A:** Three things:
1. Download full CRDDC2022 dataset (47k images) to push past 85%
2. Increase input size to 224x224 on a better GPU (T4 or A100)
3. Add GPS metadata to map damage locations geographically

**Q: Why is your pothole precision only 54% despite 100% recall?**
**A:** Precision-recall tradeoff. The weighted loss function pushes model to never miss a pothole (100% recall) but this causes it to also flag some cracks and normal roads as potholes (low precision). For road safety, missing a pothole is more dangerous than a false alarm, so we deliberately optimized for recall over precision.

**Q: Your model has 8% train-val gap — is it overfitting?**
**A:** Slight overfitting yes. We addressed it with dropout (0.3-0.55), L2 regularization (1e-3), strong augmentation, and label smoothing. The 84.74% on clean evaluation shows the model generalizes well despite the gap. Gap also partly due to augmentation on train set making train accuracy appear lower than actual model capability.

**Q: How does your RPS score work?**
**A:** RPS = sum(pixel_count[i] * weight[i]) / total_pixels
Weights: Background=0, Hairline Crack=1.0, Alligator Crack=2.5, Deep Pothole=5.0
Score of 0 = perfectly healthy road
Score approaching 5 = entirely deep pothole
Gives maintenance teams a single actionable urgency number

**Q: What is the inference time of your model?**
**A:** Local GPU (RTX 2050): ~42ms per image. Hugging Face CPU: ~200-500ms per image. Fast enough for batch processing of road survey images.
