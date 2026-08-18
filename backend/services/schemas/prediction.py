from pydantic import BaseModel, Field
from typing import List, Optional

class BoundingBox(BaseModel):
    x1: float = Field(..., description="Top-left X coordinate")
    y1: float = Field(..., description="Top-left Y coordinate")
    x2: float = Field(..., description="Bottom-right X coordinate")
    y2: float = Field(..., description="Bottom-right Y coordinate")

class DetectionItem(BaseModel):
    class_id: int = Field(..., description="Numeric class index")
    class_name: str = Field(..., description="Tumor class label (Glioma, Meningioma, No Tumor, Pituitary)")
    confidence: float = Field(..., description="Detection confidence score between 0 and 1")
    bbox: BoundingBox = Field(..., description="Bounding box coordinates")

class PredictResponse(BaseModel):
    success: bool = Field(True, description="Indicates whether inference completed successfully")
    count: int = Field(..., description="Number of tumor bounding box detections")
    detections: List[DetectionItem] = Field(default_factory=list, description="List of detected tumor bounding boxes")
    annotated_image: Optional[str] = Field(None, description="Base64-encoded PNG image with drawn bounding boxes")
    message: str = Field(..., description="Summary message of the detection results")

class HealthResponse(BaseModel):
    status: str = Field("healthy", description="Backend service health status")
    model_loaded: bool = Field(..., description="Indicates if YOLOv8 model is loaded in memory")
    model_path: str = Field(..., description="Path to loaded PyTorch/YOLO model weights")
    classes: List[str] = Field(default_factory=list, description="List of dataset tumor class names")
