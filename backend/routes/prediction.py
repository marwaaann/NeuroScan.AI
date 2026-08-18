from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from typing import Optional
import logging

from backend.schemas.prediction import PredictResponse, HealthResponse
from backend.services.yolo_service import get_yolo_service

router = APIRouter(tags=["Brain Tumor Detections"])
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB limit

@router.get("/health", response_model=HealthResponse, summary="Check service and model status")
async def health_check():
    """
    Check whether the FastAPI server and YOLOv8 model are loaded and operational.
    """
    yolo_service = get_yolo_service()
    loaded = yolo_service.is_loaded()
    
    return HealthResponse(
        status="healthy" if loaded else "degraded",
        model_loaded=loaded,
        model_path=yolo_service.model_path,
        classes=yolo_service.get_class_list()
    )

@router.post("/predict", response_model=PredictResponse, summary="Run tumor detection on MRI image")
async def predict_tumor(
    file: UploadFile = File(..., description="Uploaded MRI scan image (JPG, JPEG, PNG)"),
    confidence: float = Form(0.50, ge=0.10, le=0.95, description="Confidence threshold between 0.10 and 0.95")
):
    """
    Upload an MRI scan image to detect brain tumors (Glioma, Meningioma, Pituitary).
    Returns bounding box coordinates, detected class names, confidence scores, and annotated base64 image.
    """
    # 1. Validate file presence & filename
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file selected for upload."
        )

    # 2. Validate file extension
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension '.{ext}'. Allowed formats: JPG, JPEG, PNG."
        )

    # 3. Read image bytes & check size limit
    try:
        contents = await file.read()
    except Exception as e:
        logger.error(f"Error reading uploaded file: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read uploaded image file."
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE // (1024 * 1024)}MB."
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    # 4. Invoke YOLO inference service
    yolo_service = get_yolo_service()
    if not yolo_service.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="YOLO model is not loaded on backend server. Please verify best.pt model file."
        )

    try:
        result = yolo_service.predict(image_bytes=contents, conf_threshold=confidence)
        return PredictResponse(**result)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Prediction execution error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during inference: {str(e)}"
        )
