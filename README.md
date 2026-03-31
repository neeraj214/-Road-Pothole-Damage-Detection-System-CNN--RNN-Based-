# 🛣️ Road Pothole & Damage Detection System

[![GitHub License](https://img.shields.io/github/license/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-)](https://github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-)](https://github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-)](https://github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-/network/members)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://www.tensorflow.org/)

An end-to-end deep learning system for automatic detection and classification of road damage. This system utilizes a **MobileNetV2** backbone with a **dual-head architecture**, performing both classification and semantic segmentation simultaneously for smarter road maintenance.

---

## 🚀 Key Features
- **Dual-Head Intelligence**: Simultaneous classification of damage type and pixel-level segmentation.
- **Efficient Architecture**: Lightweight MobileNetV2 optimized for real-time mobile/embedded deployment.
- **Automated Repair Insights**: Calculates a **Repair Priority Score (RPS)** based on damage severity and area.
- **Full-Stack Solution**: FastAPI backend for serving and a modern React dashboard for visualization.

## 📊 Model Performance

| Metric | Score |
|---|---|
| **Overall Val Accuracy** | **84.74%** |
| Normal recall | 74.69% |
| Crack recall | 91.84% |
| Pothole recall | 100.00% |
| Normal F1-score | 0.839 |
| Crack F1-score | 0.874 |
| Pothole F1-score | 0.708 |
| Weighted F1-score | 0.850 |
| Segmentation IoU | 85.4% |
| Val samples tested | 2,601 |

## 🛠️ Architecture
- **Backbone**: MobileNetV2 (Pre-trained on ImageNet)
- **Classification Head**: Global Average Pooling + Global Max Pooling → Dense Layers → 3-way softmax (Normal/Crack/Pothole)
- **Segmentation Head**: Custom lightweight Decoder block (Skip connections) → 1x1 Conv → Damage Map
- **Processing**: Weighted Hybrid Loss (Categorical Cross-Entropy + Dice Loss)

---

## ⚙️ Setup & Installation

### 🔧 Backend (API)
```bash
pip install -r requirements.txt
python app.py
# API runs at http://localhost:8000
```

### 💻 Frontend (Dashboard)
```bash
cd frontend_vanilla
npm install
npm run dev
# Dashboard runs at http://localhost:5173
```

## 📡 API Endpoints
- `GET /health` — Status check for API and Model.
- `POST /predict` — Upload image to receive **Damage Class**, **RPS**, and **Segmentation Overlay**.

## 📂 Dataset
This project is trained on the **RDD2022 (Road Damage Dataset)**.
- **Link**: [sekilab/RoadDamageDetector](https://github.com/sekilab/RoadDamageDetector)
- **Samples Used**: ~19,892 images (India + Japan subsets)

---

## 🎨 Visualization Samples
*Visualizations and confusion matrices can be found in the `/results` directory.*

- [Confusion Matrix](results/confusion_matrix.png)
- [Normalized Matrix](results/confusion_matrix_normalized.png)
- [Training History](results/stage2_v6_deeper_history.png)
