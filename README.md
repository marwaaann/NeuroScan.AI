# NeuroScan.AI: Intelligent Brain Tumor Detection System

<p align="center">
  <img src="frontend/favicon.png" alt="NeuroScan.AI Logo" width="80" height="80" />
</p>

<p align="center">
  <strong>Clinical Computer-Vision & Deep Learning Pipeline for MRI Brain Tumor Detection</strong>
</p>

<p align="center">
  <a href="https://neuroscan-ai-lp16.onrender.com"><img src="https://img.shields.io/badge/Render-Live%20Demo-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo on Render" /></a>
  <a href="https://neuroscanai-ahwmpetaryjhq9pm3qv4et.streamlit.app"><img src="https://img.shields.io/badge/Streamlit%20Cloud-Live%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit Cloud App" /></a>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logo=yolo&logoColor=black" alt="YOLOv8" />
  <img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Ready" />
</p>

---

## 🌐 Live Deployments

You can test and interact with the live application directly in your browser:

| Platform | Deployment URL | Status | Description |
| :--- | :--- | :--- | :--- |
| **Render (Primary)** | [**https://neuroscan-ai-lp16.onrender.com**](https://neuroscan-ai-lp16.onrender.com) | ![Live](https://img.shields.io/badge/Status-Active-brightgreen) | Containerized Docker deployment on Render cloud infrastructure. |
| **Streamlit Cloud** | [**https://neuroscanai-ahwmpetaryjhq9pm3qv4et.streamlit.app**](https://neuroscanai-ahwmpetaryjhq9pm3qv4et.streamlit.app) | ![Live](https://img.shields.io/badge/Status-Active-brightgreen) | Native serverless hosting on Streamlit Community Cloud. |

---

## 📖 Overview

**NeuroScan.AI** is an end-to-end medical computer-vision application engineered to assist clinicians, researchers, and radiologists in detecting and localizing brain tumors from Magnetic Resonance Imaging (MRI) scans. Powered by a custom-trained **Ultralytics YOLOv8** model, it delivers real-time bounding-box detection, confidence scoring, and diagnostic analytics across four distinct tissue classes.

---

## 🎯 Architecture Overview

```text
                           CLIENT / BROWSER
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │    Streamlit FRONTEND   │
                     │  • Custom UI Theme      │
                     │  • Sample Scan Testing  │
                     │  • Diagnostic Dashboard │
                     └────────────┬────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 │ HTTP (Dual Architecture Support)│
                 ▼                                 ▼
      ┌─────────────────────┐           ┌─────────────────────┐
      │   FastAPI BACKEND   │           │ Standalone Fallback │
      │  (Microservice API) │           │ (In-Process YOLOv8) │
      └──────────┬──────────┘           └──────────┬──────────┘
                 │                                 │
                 └────────────────┬────────────────┘
                                  │ PyTorch Inference
                                  ▼
                     ┌─────────────────────────┐
                     │   Trained YOLOv8 Model  │
                     │     (model/best.pt)     │
                     └────────────┬────────────┘
                                  │ Structured Detections + Annotated Image
                                  ▼
                     ┌─────────────────────────┐
                     │ Visual Bounding Boxes   │
                     │ & Confidence Analytics  │
                     └─────────────────────────┘
```

---

## 🌟 Key Features

- **🎯 High-Precision Tumor Detection**: Custom-trained YOLOv8 object detection model identifying precise bounding coordinates (`x1, y1, x2, y2`) and confidence scores.
- **🖼️ Built-in Sample Scans**: Pre-loaded with verified brain MRI scans for instantaneous one-click testing without requiring manual file uploads.
- **🎨 Modern Clinical UI**: Custom Light/Dark-mode styling, responsive layout, side-by-side original vs. annotated scan comparison, and one-click annotated image export.
- **📈 Comprehensive Model Analytics**: Interactive exploration of validation performance metrics, confusion matrices, Precision-Recall curves, and training loss progression.
- **⚡ Dual-Mode Execution**:
  - **Microservice Mode**: Scalable two-tier setup with FastAPI backend and Streamlit frontend.
  - **Standalone Cloud Mode**: Automatically runs in-process inference when deployed on single-container platforms (Render, Streamlit Cloud, Hugging Face).
- **🐳 Production Containerization**: Pre-configured with `Dockerfile` and `.dockerignore` for portable container deployment anywhere.

---

## 🏷️ Classification Labels

The model is trained to identify and categorize four tissue types:

| Class ID | Tumor Label | Clinical Description |
| :---: | :--- | :--- |
| `0` | **Glioma** | Primary tumor originating in the glial cells of the brain or spinal cord |
| `1` | **Meningioma** | Typically benign tumor arising from the meningeal membranes surrounding the brain |
| `2` | **No Tumor** | Normal brain MRI scan displaying healthy tissue with no detected lesions |
| `3` | **Pituitary** | Abnormal growth developing in the pituitary gland at the base of the brain |

---

## 📊 Empirical Model Performance

Evaluated on rigorous validation subsets with high-resolution 640×640 MRI tensors:

| Metric | Score | Details |
| :--- | :---: | :--- |
| **mAP@50** | **96.31%** | Mean Average Precision at IoU threshold 0.50 |
| **Precision** | **93.87%** | Low false-positive rate across all tumor classes |
| **Recall** | **94.01%** | Sensitivity in identifying present tumors |
| **Input Resolution** | **640 × 640** | Normalized RGB Tensor Matrix |
| **Inference Latency** | **~25–45 ms** | Real-time prediction speed on standard CPU/GPU |

---

## 📂 Project Structure

```text
NeuroScan.AI/
├── frontend/                     # Streamlit web application
│   ├── app.py                    # Main dashboard entry point & routing
│   ├── components/               # Modular UI components (sidebar, cards)
│   ├── pages/                    # Multi-view pages (detection, analytics, overview, login)
│   ├── services/                 # API client with intelligent standalone fallback
│   ├── styles/                   # Modern clinical CSS stylesheets
│   └── favicon.png               # Custom branding favicon
│
├── backend/                      # FastAPI REST microservice
│   ├── main.py                   # FastAPI server entry point & CORS configuration
│   ├── routes/                   # API route handlers (/health, /predict)
│   ├── services/                 # Model loading singleton (yolo_service.py)
│   └── schemas/                  # Pydantic request & response models
│
├── model/
│   └── best.pt                   # Trained YOLOv8 PyTorch model weights (6.2 MB)
│
├── samples/                      # Verified sample MRI scans for 1-click testing
│   ├── sample_glioma.jpg
│   ├── sample_scan_1.jpg
│   └── sample_scan_2.jpg
│
├── training/                     # Offline pipeline & model development
│   ├── train_yolo.py             # Model training script
│   ├── validate_model.py         # Evaluation & metrics validation script
│   ├── predict.py                # Standalone test inference script
│   └── brain_tumor_dataset.yaml  # Dataset configuration
│
├── legacy_flask_app/             # Previous Flask prototype (archived for reference)
│   ├── app.py
│   ├── templates/
│   └── README.md
│
├── .streamlit/
│   └── config.toml               # Streamlit theme & UI configuration
│
├── Dockerfile                    # Container configuration for Docker/Render/Railway
├── .dockerignore                 # Container build exclusion rules
├── requirements.txt              # Production Python dependencies
├── start_webapp.bat              # Local 1-click Windows launcher
└── README.md                     # Comprehensive project documentation
```

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/marwaaann/NeuroScan.AI.git
cd NeuroScan.AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Locally

#### Option A: Quick Launcher (Windows)
Double-click `start_webapp.bat` or run:
```cmd
start_webapp.bat
```
This automatically boots the FastAPI backend on port 8000 and the Streamlit frontend on port 8501.

#### Option B: Run Streamlit Standalone
```bash
streamlit run frontend/app.py --server.port 8501
```
Open your browser at **`http://localhost:8501`**.

#### Option C: Run with Docker
```bash
docker build -t neuroscan-ai .
docker run -p 8501:8501 neuroscan-ai
```
Open your browser at **`http://localhost:8501`**.

---

## 📡 API Reference (FastAPI Backend)

When running the backend server (`uvicorn backend.main:app --port 8000`), interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

### `GET /health`
Returns system status and model loading readiness.

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": ".../model/best.pt",
  "classes": ["Glioma", "Meningioma", "No Tumor", "Pituitary"]
}
```

### `POST /predict`
Upload an MRI scan image to perform YOLOv8 tumor detection.

- **Parameters**:
  - `file`: Multipart form-data image file (`.jpg`, `.jpeg`, `.png`)
  - `confidence`: Confidence threshold between `0.10` and `0.95` (default: `0.50`)

- **Sample Response**:
```json
{
  "success": true,
  "count": 1,
  "detections": [
    {
      "class_id": 0,
      "class_name": "Glioma",
      "confidence": 0.9465,
      "bbox": {
        "x1": 166.76,
        "y1": 199.74,
        "x2": 267.77,
        "y2": 288.88
      }
    }
  ],
  "annotated_image": "data:image/png;base64,iVBORw0KG...",
  "message": "Found 1 tumor detection(s)."
}
```

### `POST /contact`
Submit a consultation or research inquiry to the persistent SQLite database.

- **Payload**:
```json
{
  "full_name": "Dr. Sharma",
  "phone": "+91 9988776655",
  "location": "Delhi NCR",
  "email": "sharma@hospital.org",
  "message": "Inquiring about hospital PACS pilot integration"
}
```

- **Sample Response**:
```json
{
  "status": "success",
  "message": "Consultation request received successfully.",
  "contact_id": 1
}
```

---

## 📄 Research Paper & Academic Citation

This project is built upon the academic research paper:
> **"Brain Tumor Detection Using YOLOv8 and YOLOv11"**  
> *Rishabh\*, Marwan\*, Devendra Kumar, Hamza, Sudhanshu Garg, Sarvaswa Kumar Tiwari*  
> **Indian Institute of Information Technology Sonepat (IIIT Sonepat)**, Haryana, India  
> Department of Computer Science

### Key Empirical Results
- **Overall System Accuracy:** ~95%
- **Validation mAP:** 0.95 (YOLOv11) / 96.31% mAP@50 (YOLOv8)
- **Real-Time Inference Speed:** 92 FPS (~32ms per slice)
- **Pathology Class Distribution (7,000–8,000 Multi-Planar Scans):**
  - **Meningioma:** 99% Accuracy (~1,900 scans)
  - **No Tumor (Healthy):** 100% Accuracy (~1,300–1,500 scans)
  - **Pituitary Adenoma:** 94% Accuracy (~1,600 scans)
  - **Glioma:** 90% Accuracy (~2,200 scans)

---

## ⚠️ Medical Disclaimer

> **RESEARCH AND EDUCATIONAL USE ONLY**
> 
> Nuroscan is developed for academic, educational, and computational research purposes. The model predictions, bounding boxes, and probability scores generated by this system **do not constitute medical diagnoses** or definitive clinical conclusions. This software should never be utilized as a sole substitute for professional evaluation, consultation, or diagnosis by a licensed radiologist or healthcare provider.

---

## 👥 Authors & Contributors

- **Marwan Shafi** ([@marwaaann](https://github.com/marwaaann)) — Lead Author & Architect
- **Rishabh** — Lead Author & Research Lead (IIIT Sonepat)
- **Devendra Kumar**, **Hamza**, **Sudhanshu Garg**, **Sarvaswa Kumar Tiwari** — Research Contributors (IIIT Sonepat)
- Repository: [github.com/marwaaann/NeuroScan.AI](https://github.com/marwaaann/NeuroScan.AI)
