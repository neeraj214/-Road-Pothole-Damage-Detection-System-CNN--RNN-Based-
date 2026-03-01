# 🛣️ Road Pothole & Damage Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10%2B-orange.svg?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.6%2B-green.svg?style=for-the-badge&logo=opencv)](https://opencv.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.15%2B-red.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An advanced deep learning system designed to automatically detect and classify road potholes and surface damage using Convolutional Neural Networks (CNN). This project focuses on high accuracy and real-time deployment potential.

---

## 🚀 Key Features

- **CNN-Based Detection**: Leverages Transfer Learning with **MobileNetV2** for optimized performance.
- **Automated Data Pipeline**: Robust data loading and preprocessing with real-time augmentation.
- **Production Ready**: Modular structure designed for scalability and maintainability.
- **Interactive UI**: (Upcoming) Streamlit-based dashboard for easy image and video analysis.

---

## 📂 Project Structure

```text
Road-Pothole-Damage-Detection-System/
│
├── data/
│   ├── raw/             # Training, validation, and test images
│   └── processed/       # Preprocessed image data
│
├── models/              # Saved model checkpoints (.h5, .keras)
│
├── src/                 # Core Source Code
│   ├── config.py        # Centralized hyperparameters & paths
│   ├── data_loader.py   # Data generators & augmentation
│   ├── model.py         # CNN architecture implementation
│   ├── train.py         # Training scripts
│   └── utils.py         # Helper functions
│
├── app.py               # Streamlit application
└── requirements.txt     # Project dependencies
```

---

## 🛠️ Tech Stack

- **Deep Learning**: TensorFlow / Keras
- **Computer Vision**: OpenCV
- **Data Augmentation**: Albumentations / Keras Preprocessing
- **Web App**: Streamlit

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/neeraj214/-Road-Pothole-Damage-Detection-System-CNN--RNN-Based-.git
   cd -Road-Pothole-Damage-Detection-System-CNN--RNN-Based-
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Preparation**:
   Place your dataset in `data/raw/` following this structure:
   ```text
   data/raw/
   ├── train/
   │   ├── pothole/
   │   └── normal/
   ├── val/
   └── test/
   ```

---

## 🧪 Usage

### Training the Model
To start training the CNN model with the configured hyperparameters:
```bash
python -m src.train
```
This will:
- Load data from `data/raw/`
- Build the MobileNetV2-based model
- Train with EarlyStopping, ModelCheckpoint, and ReduceLROnPlateau
- Save the best model to `models/best_model.h5`
- Save the final model to `models/final_model.h5`

---

## 🏗️ Phase-wise Progress

- [x] **PHASE 1**: Project Setup & Configuration
- [x] **PHASE 2**: Data Pipeline & Preprocessing
- [x] **PHASE 3**: CNN Model Implementation
- [x] **PHASE 4**: Model Training & Evaluation
- [ ] **PHASE 5**: Streamlit App Development (Current)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <sub>Developed with ❤️ by <a href="https://github.com/neeraj214">Neeraj Negi</a></sub>
</div>
