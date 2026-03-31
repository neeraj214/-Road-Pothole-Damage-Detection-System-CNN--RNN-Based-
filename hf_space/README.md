---
title: Road Pothole Detection API
emoji: 🛣️
colorFrom: red
colorTo: orange
sdk: docker
pinned: false
---

# Road Pothole Detection API

FastAPI backend for road pothole and damage detection using
MobileNetV2 dual-head architecture.

## Endpoints
- `GET /` — API root / welcome message
- `GET /health` — API status and model load state
- `POST /predict` — Upload road image, returns damage classification

## Model
MobileNetV2 dual-head: 84.74% accuracy on RDD2022 dataset

### Classification Head
Predicts one of three classes: **Normal**, **Crack**, **Pothole**

### Segmentation Head
Pixel-level damage map: Background · Hairline Crack · Alligator Crack · Deep Pothole

### Repair Priority Score (RPS)
Weighted damage metric used to prioritise road repair scheduling.

## Usage

```bash
curl -X POST "https://YOUR_USERNAME-road-pothole-api.hf.space/predict" \
     -F "file=@road_image.jpg"
```

## Environment Variables
| Variable | Description | Default |
|---|---|---|
| `MODEL_URL` | Direct URL to zipped model on HF Model Hub | *(none — model downloads on first start)* |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins | `*` |
