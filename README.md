# 🛣️ Road Pothole & Damage Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10%2B-orange.svg?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2%2B-61DAFB.svg?style=for-the-badge&logo=react)](https://reactjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3%2B-38B2AC.svg?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)

An advanced deep learning system designed to automatically detect and classify road potholes and surface damage using Convolutional Neural Networks (CNN). This project features a high-performance **MobileNetV2** backend and a modern **React + TailwindCSS** dashboard.

---

## 🚀 Key Features

- **Multi-Class Detection**: Detects **Potholes**, **Surface Cracks**, and **Healthy Roads** using RDD2022 dataset integration.
- **Transfer Learning**: Optimized MobileNetV2 architecture for high accuracy with low computational overhead.
- **Modern Dashboard**: Responsive React frontend with glassmorphism UI, real-time image preview, and animated results.
- **Production API**: Scalable FastAPI backend with CORS support and automated model loading.
- **Automated Data Pipeline**: Robust processing script to organize multi-national RDD2022 data (India & Japan) into training-ready formats.

---

## 📂 Project Structure

```text
Road-Pothole-Damage-Detection-System/
│
├── data/
│   ├── raw/             # Sorted RDD2022 images (pothole, crack, normal)
│   └── processed/       # Preprocessed image data
│
├── frontend/            # React + Vite + TailwindCSS Frontend
│   ├── src/             # Component-based modular architecture
│   └── vite.config.js   # Vite configuration
│
├── models/              # Saved model checkpoints (.h5)
│
├── src/                 # Core Python Backend Logic
│   ├── config.py        # Centralized hyperparameters (3-class system)
│   ├── data_loader.py   # Data generators & real-time augmentation
│   ├── model.py         # CNN (MobileNetV2) implementation
│   └── train.py         # Training & evaluation scripts
│
├── app.py               # FastAPI production server
└── requirements.txt     # Backend dependencies
```

---

## 🛠️ Tech Stack

- **Deep Learning**: TensorFlow / Keras (MobileNetV2)
- **Backend API**: FastAPI / Uvicorn
- **Frontend**: React 18 / Vite / TailwindCSS / Framer Motion
- **Data Handling**: NumPy / Pillow / OpenCV
- **Dataset**: RDD2022 (Multi-national Road Damage Dataset)

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-.git
   cd -Road-Pothole-Damage-Detection-System-CNN--RNN-Based-
   ```

2. **Backend Setup**:
   ```bash
   pip install -r requirements.txt
   python app.py  # Starts FastAPI on http://localhost:8000
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev    # Starts Vite on http://localhost:5173
   ```

---

## 🧪 Usage

### Training the Model
To train the CNN model on the organized RDD2022 dataset:
```bash
python -m src.train
```
This will:
- Load data from `data/raw/` (3 classes: pothole, crack, normal).
- Build the MobileNetV2-based model.
- Train with **EarlyStopping**, **ModelCheckpoint**, and **ReduceLROnPlateau**.
- Save the best model to `models/best_model.h5`.

---

## 🏗️ Phase-wise Progress

- [x] **PHASE 1**: Project Setup & Configuration
- [x] **PHASE 2**: Data Pipeline & RDD2022 Integration
- [x] **PHASE 3**: CNN Model Implementation (MobileNetV2)
- [x] **PHASE 4**: FastAPI Backend & React Frontend
- [ ] **PHASE 5**: Model Training & Hyperparameter Tuning (Ready to Start)

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
