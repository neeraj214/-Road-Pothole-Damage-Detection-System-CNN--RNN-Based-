# Road Pothole & Damage Detection System

An end-to-end deep learning system for automatic detection and
classification of road damage using MobileNetV2 with a dual-head
architecture for simultaneous classification and segmentation.

## Tech Stack
- **Model**: TensorFlow 2.x, MobileNetV2 (transfer learning)
- **Backend**: FastAPI, Uvicorn
- **Frontend**: React 18, TailwindCSS, Vite
- **Dataset**: RDD2022 India + Japan (19,892 images)

## Model Performance
| Metric | Score |
|---|---|
| Overall val accuracy | 75.47% |
| Normal road accuracy | 69.1% |
| Crack accuracy | 80.3% |
| Pothole accuracy | 77.2% |
| Segmentation IoU | 85.4% |

## Architecture
- Shared MobileNetV2 backbone (pretrained on ImageNet)
- Classification head: GAP + GMP → Dense layers → Normal/Crack/Pothole
- Segmentation head: Lightweight U-Net decoder → pixel-level damage maps
- Repair Priority Score (RPS) for maintenance urgency

## Setup

### Backend
```bash
pip install -r requirements.txt
python app.py
# API runs at http://localhost:8000
```

### Frontend
```bash
cd frontend_vanilla
npm install
npm run dev
# Dashboard runs at http://localhost:5173
```

## API Endpoints
- `GET /health` — API and model status
- `POST /predict` — Upload road image, returns class + RPS + segmentation

## Dataset
RDD2022 — https://github.com/sekilab/RoadDamageDetector
