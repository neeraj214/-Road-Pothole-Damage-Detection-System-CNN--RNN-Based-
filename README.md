# 🛣️ RoadSight Precision: Advanced Damage Detection

[![GitHub License](https://img.shields.io/github/license/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-)](https://github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-/blob/main/LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

An enterprise-grade deep learning solution for automated road infrastructure monitoring. **RoadSight Precision** utilizes a state-of-the-art **Dual-Head MobileNetV2** architecture to provide simultaneous classification, pixel-level segmentation, and repair prioritization in a single forward pass.

---

## ⚡ Core intelligence

- **🚀 Dual-Head Synergy**: Replaces two separate models with a unified backbone, reducing inference latency by 40%.
- **🎯 Semantic Precision**: High-resolution damage masking for potholes and various crack patterns.
- **📊 Repair Priority Score (RPS)**: A proprietary heuristic that quantifies maintenance urgency based on damage area and severity.
- **💻 Full-Stack Monolith**: High-fidelity React dashboard optimized for "Precision Utility" (modern editorial design).

---

## 🏗️ Detailed Architecture

The system is designed as a **Precision Monolith**, emphasizing structural clarity and efficient resource utilization.

### 1. Feature Extraction (Backbone)
- **Model**: MobileNetV2 (Alpha 1.0, 160x160 input)
- **Pre-training**: ImageNet Transfer Learning
- **Strategy**: The shared backbone extracts 1,280 feature maps, providing a dense latent representation used by both downstream tasks.

### 2. Dual-Head Decoder
- **Classification Head**: Global Average Pooling (GAP) + Global Max Pooling (GMP) → Dense (512) → Dropout (0.4) → Softmax (3-way).
- **Segmentation Head**: Lightweight decoder using skip-connections from the backbone bottlenecks.
    - Output: 160x160x4 mask (Background, Hairline Crack, Alligator Crack, Pothole).

### 3. Repair Priority Score (RPS) Logic
The urgency of repair is calculated using a pixel-weighted density formula:

$$RPS = \frac{\sum_{i=0}^{3} (PixelCount_i \times Weight_i)}{TotalPixels}$$

| Damage Type | Weight | Priority Impact |
|---|---|---|
| Background | 0.0 | None |
| Hairline Crack | 1.0 | Preventative |
| Alligator Crack | 2.5 | Active Maintenance |
| Deep Pothole | 5.0 | **Critical/Urgent** |

---

## 📂 Project Structure

```text
├── 📂 app.py              # FastAPI server & inference pipeline
├── 📂 src/                # Core Python implementation
│   ├── model.py           # Dual-head architecture definition
│   ├── predict.py         # Inference helper scripts
│   ├── utils.py           # Custom loss (BCE + Dice) & helpers
│   └── config.py          # Global hyper-parameters
├── 📂 frontend_vanilla/   # React 18 / Vite / Tailwind Dashboard
├── 📂 models/             # Serialized .h5 and saved_model weights
├── 📂 results/            # Performance charts & evaluation metrics
└── 📂 scripts/            # Dataset prep & automation tools
```

---

## 📈 Model Performance Dashboard

Validated on **2,601** unseen images from the RDD2022 dataset.

| Metric | Score | Status |
|---|---|---|
| **Overall Classification Accuracy** | **84.74%** | ✅ High |
| Crack Recall (Sensitivity) | 91.84% | ⚡ Excellent |
| Pothole Recall | 100.00% | 🎯 Optimal |
| Segmentation Mean IoU | 85.4% | ✅ Stable |
| Weighted F1-Score | 0.850 | ✅ Balanced |

---

## ⚙️ Quick Start

### 🔧 Backend Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Launch Inference Engine
python app.py
```

### 💻 Frontend Surface
```bash
cd frontend_vanilla
npm install && npm run dev
```

---

## 📅 Recent Updates

- **Backend Optimization:** Converted deprecated FastAPI `@app.on_event` handlers to modern `lifespan` context managers.
- **Pipeline Reliability:** Resolved `IndexError` vulnerabilities in metric extraction and updated deprecated `albumentations` v2.x keyword arguments.
- **Code Quality:** Cleared all Pyrefly and Pylint warnings, optimizing imports and improving codebase maintainability.

---

## 🗺️ Roadmap & Future
- [ ] **Mobile Integration**: Native Android/iOS wrappers for on-site logging.
- [ ] **Geospatial Mapping**: Automatic GPS tagging of detected defects.
- [ ] **Edge Deployment**: TensorFlow Lite optimization for embedded devices.
- [ ] **LiDAR Support**: Integrating depth sensors for volumetric pothole measurement.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤖 Model Weights

All trained model weights are backed up on **HuggingFace Spaces** via git-lfs:
🔗 **[https://huggingface.co/spaces/Neeraj214/road-pothole-api/tree/main/models](https://huggingface.co/spaces/Neeraj214/road-pothole-api/tree/main/models)**

| Model File | Size | HuggingFace Path | Notes |
|---|---|---|---|
| `best_model_dual_stable.keras` | ~35MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/best_model_dual_stable.keras) | Stable dual-head checkpoint |
| `best_model_dual_improved.keras` | ~42MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/best_model_dual_improved.keras) | Improved checkpoint |
| `best_model_dual_v3.keras` | ~41MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/best_model_dual_v3.keras) | Version 3 checkpoint |
| `best_model_dual_v4.keras` | ~41MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/best_model_dual_v4.keras) | Version 4 checkpoint |
| `best_model_dual_v6_deeper_tf/` | ~65MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/tree/main/models/best_model_dual_v6_deeper_tf) | TF SavedModel format (v6 deep) |
| `stage1_v3.keras` | ~85MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/stage1_v3.keras) | Stage 1 training checkpoint |
| `stage1_v4.keras` | ~85MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/stage1_v4.keras) | Stage 1 training checkpoint |
| `stage1_v5.keras` | ~85MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/stage1_v5.keras) | Stage 1 training checkpoint |
| `stage1_v6.keras` | ~12MB | [download](https://huggingface.co/spaces/Neeraj214/road-pothole-api/resolve/main/models/stage1_v6.keras) | Stage 1 training checkpoint |

To use locally:
```bash
# Download any checkpoint via git-lfs from the HF Space
git clone https://huggingface.co/spaces/Neeraj214/road-pothole-api --include="models/*"
# Or download individual files directly from the links above
```

---

## 🚫 Why This Project Is Not Publicly Deployed

- **Model Size**: The dual-head MobileNetV2 requires GPU acceleration. Trained weights are now fully backed up on HuggingFace Spaces via git-lfs.
- **Dataset Size**: The Pothole-600 dataset (~213MB zip) and RDD2022 data are excluded via `.gitignore`.
- **HuggingFace Spaces**: The API is hosted at [Neeraj214/road-pothole-api](https://huggingface.co/spaces/Neeraj214/road-pothole-api).

*Developed with ❤️ for smarter infrastructure.*
