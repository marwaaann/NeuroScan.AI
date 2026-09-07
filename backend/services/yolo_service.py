import os
import io
import base64
import logging
from typing import Dict, Any, List, Optional
from PIL import Image
import numpy as np

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

logger = logging.getLogger(__name__)

class YOLOService:
    """
    Singleton-style service for loading YOLOv8 brain tumor detection model
    and running inference on uploaded MRI scans.
    """
    
    _instance: Optional['YOLOService'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(YOLOService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_path: Optional[str] = None):
        if self._initialized:
            return
        
        self.model = None
        self.model_path = model_path or self._resolve_model_path()
        self.class_names = {
            0: "Glioma",
            1: "Meningioma",
            2: "No Tumor",
            3: "Pituitary"
        }
        self.load_model()
        self._initialized = True

    def _resolve_model_path(self) -> str:
        """Find model/best.pt across relative paths"""
        possible_paths = [
            os.path.join(os.getcwd(), 'model', 'best.pt'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'model', 'best.pt'),
            'model/best.pt',
            'brain_tumor_detector/yolov8n_run_1/weights/best.pt',
            '../model/best.pt',
            os.path.join(os.getcwd(), 'yolov8n.pt'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'yolov8n.pt'),
            'yolov8n.pt'
        ]
        
        for p in possible_paths:
            abs_p = os.path.abspath(p)
            if os.path.exists(abs_p):
                logger.info(f"Resolved model path: {abs_p}")
                return abs_p
                
        # Default fallback path
        return os.path.abspath(os.path.join(os.getcwd(), 'model', 'best.pt'))

    def load_model(self) -> bool:
        """Load YOLO model into memory once"""
        if YOLO is None:
            logger.error("Ultralytics package is not installed.")
            return False

        if not os.path.exists(self.model_path):
            logger.warning(f"Model file not found at {self.model_path}")
            return False

        try:
            logger.info(f"Loading YOLOv8 model from {self.model_path}...")
            self.model = YOLO(self.model_path)
            
            # Sync model class names if available
            if hasattr(self.model, 'names') and isinstance(self.model.names, dict):
                self.class_names = {int(k): str(v) for k, v in self.model.names.items()}
            logger.info(f"Model loaded successfully with classes: {self.class_names}")
            return True
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}", exc_info=True)
            self.model = None
            return False

    def is_loaded(self) -> bool:
        return self.model is not None

    def get_class_list(self) -> List[str]:
        return [self.class_names.get(i, f"Class_{i}") for i in sorted(self.class_names.keys())]

    def predict(self, image_bytes: bytes, conf_threshold: float = 0.5) -> Dict[str, Any]:
        """
        Run inference on image bytes and return structured results with base64 annotated image.
        """
        if not self.is_loaded():
            # Attempt reloading if model wasn't ready
            if not self.load_model():
                raise RuntimeError("YOLO model is not loaded. Please verify model/best.pt exists.")

        # Load and convert image
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')
        except Exception as e:
            raise ValueError(f"Invalid image content: {str(e)}")

        # Run inference
        results = self.model.predict(
            source=pil_img,
            conf=conf_threshold,
            save=False,
            verbose=False
        )

        if not results or len(results) == 0:
            return {
                "success": True,
                "count": 0,
                "detections": [],
                "annotated_image": None,
                "message": "No tumor detected above selected confidence threshold."
            }

        result = results[0]
        detections = []

        if len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                class_name = self.class_names.get(class_id, f"Class {class_id}")
                
                # Coordinates
                coords = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                
                detections.append({
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": round(confidence, 4),
                    "bbox": {
                        "x1": round(coords[0], 2),
                        "y1": round(coords[1], 2),
                        "x2": round(coords[2], 2),
                        "y2": round(coords[3], 2)
                    }
                })

        # Generate annotated image
        annotated_bgr = result.plot()
        annotated_rgb = annotated_bgr[:, :, ::-1]  # Convert BGR to RGB numpy
        annotated_pil = Image.fromarray(annotated_rgb)

        img_buffer = io.BytesIO()
        annotated_pil.save(img_buffer, format="PNG")
        base64_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        formatted_base64 = f"data:image/png;base64,{base64_str}"

        count = len(detections)
        message = f"Found {count} tumor detection(s)." if count > 0 else "No tumor detected above selected confidence threshold."

        return {
            "success": True,
            "count": count,
            "detections": detections,
            "annotated_image": formatted_base64,
            "message": message
        }

# Global singleton accessor
def get_yolo_service() -> YOLOService:
    return YOLOService()
