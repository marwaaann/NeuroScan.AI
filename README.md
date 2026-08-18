# NeuroScan AI: AI-Powered Brain Tumor Detection Web Application

NeuroScan AI is a production-style medical computer-vision application that detects and classifies brain tumors in Magnetic Resonance Imaging (MRI) scans using **Ultralytics YOLOv8**, **FastAPI**, and **Streamlit**.

---

## 🎯 Architecture Overview

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │    Streamlit    │
                  │    FRONTEND     │
                  │  (Port 8501)    │
                  └────────┬────────┘
                           │  HTTP POST /predict
                           ▼
                  ┌─────────────────┐
                  │     FastAPI     │
                  │     BACKEND     │
                  │  (Port 8000)    │
                  └────────┬────────┘
                           │  Inference
                           ▼
                  ┌─────────────────┐
                  │   YOLOv8 Model  │
                  │  (model/best.pt)│
                  └────────┬────────┘
                           │  Structured Results
                           ▼
                  ┌─────────────────┐
                  │  JSON Response  │
                  │ Detections+BBox │
                  └─────────────────┘
```

---

## 🌟 Key Features

- **🚀 FastAPI Microservice Backend**: Dedicated RESTful API endpoint for high-speed model inference, health checks, and JSON response formatting.
- **🎨 Streamlit AI Dashboard**: Modern dark medical theme with live server connection badges, interactive sliders, side-by-side MRI comparisons, and image download tools.
- **🎯 YOLOv8 Object Detection**: Utilizes custom-trained PyTorch weights (`model/best.pt`) to locate tumor boundaries (`x1, y1, x2, y2`) and output confidence scores.
- **📈 Real Empirical Analytics**: Visualizes validation mAP@50 (96.31%), Precision (93.87%), Recall (94.01%), loss progression, and confusion matrices directly from dataset metrics.
- **🔒 Robust Validation & Safety**: Input image validation (JPG, JPEG, PNG), upload size safeguards, slider confidence bounds, and prominent medical disclaimers.

---

## 🏷️ Class Mapping (4 Classes)

| Class ID | Tumor Class Label | Description |
| :--- | :--- | :--- |
| `0` | **Glioma** | Primary brain tumor originating from glial cells |
| `1` | **Meningioma** | Tumor arising from brain membranes (meninges) |
| `2` | **No Tumor** | MRI scan showing healthy brain tissue |
| `3` | **Pituitary** | Tumor located in the pituitary gland |

---

## 📂 Project Directory Structure

```text
brain_tumor_project/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI server entry point & CORS
│   ├── routes/
│   │   ├── __init__.py
│   │   └── prediction.py        # /health and /predict API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── yolo_service.py      # Thread-safe YOLOv8 model loading & inference
│   └── schemas/
│       ├── __init__.py
│       └── prediction.py        # Pydantic request/response schemas
│
├── frontend/
│   └── app.py                   # Streamlit web application (NeuroScan AI UI)
│
├── model/
│   └── best.pt                  # Reused trained YOLOv8 PyTorch model weights
│
├── training/
│   ├── train_yolo.py            # Preserved YOLOv8 training pipeline
│   └── validate_model.py       # Preserved validation script
│
├── brain_tumor_dataset.yaml     # Dataset class mapping configuration
├── predict.py                   # Preserved CLI testing script
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies

Ensure Python 3.10+ is installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend API

Launch the backend inference server on port 8000:

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive Swagger documentation is available at: `http://127.0.0.1:8000/docs`.

### 3. Start the Streamlit Frontend UI

In a separate terminal window, launch the frontend dashboard:

```bash
python -m streamlit run frontend/app.py --server.port 8501
```

Open your browser at `http://localhost:8501`.

---

## 📡 API Endpoints

### `GET /health`
Returns system status and model readiness.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "C:/Users/.../model/best.pt",
  "classes": ["Glioma", "Meningioma", "No Tumor", "Pituitary"]
}
```

### `POST /predict`
Upload an MRI image to perform YOLOv8 tumor detection.

**Request Form Data**:
- `file`: Image file (`.jpg`, `.jpeg`, `.png`)
- `confidence`: Confidence threshold float (`0.10` to `0.95`, default `0.50`)

**Response**:
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

---

## ⚠️ Medical Disclaimer

> **RESEARCH AND EDUCATIONAL USE ONLY**
>
> NeuroScan AI is a machine-learning research prototype. Its predictions are model inferences and **do not constitute medical diagnoses**. They should never replace evaluation by a qualified radiologist or healthcare professional.
