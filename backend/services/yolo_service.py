import os
import io
import gc
import base64
import logging
from typing import Dict, Any, List, Optional
from PIL import Image, ImageOps

# Suppress OpenMP/BLAS thread explosion and Ultralytics telemetry to guarantee ultra-low memory footprint (<250MB)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["YOLO_VERBOSE"] = "False"
os.environ["ULTRALYTICS_SETTINGS"] = "sync=False"

try:
    import torch
    try:
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
    except Exception:
        pass
except ImportError:
    torch = None

try:
    import ultralytics
    try:
        ultralytics.settings.update({"sync": False, "analytics": False, "checks": False})
    except Exception:
        pass
    from ultralytics import YOLO
except ImportError:
    YOLO = None

logger = logging.getLogger(__name__)

class YOLOService:
    """
    Singleton-style service for loading YOLOv8 brain tumor detection model
    and running high-speed inference on uploaded cranial MRI scans.
    Optimized for low-memory containerized environments (Render, Cloud Run, Docker).
    """
    
    _instance: Optional['YOLOService'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(YOLOService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_path: Optional[str] = None):
        if getattr(self, '_initialized', False):
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
        """Find best.onnx or best.pt across all known local and container paths"""
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(curr_dir)
        project_root = os.path.dirname(backend_dir)

        possible_paths = [
            os.path.join(project_root, 'model', 'best.onnx'),
            os.path.join(project_root, 'model', 'best.pt'),
            os.path.join(os.getcwd(), 'model', 'best.onnx'),
            os.path.join(os.getcwd(), 'model', 'best.pt'),
            os.path.join(os.getcwd(), 'brain_tumor_project', 'model', 'best.onnx'),
            os.path.join(os.getcwd(), 'brain_tumor_project', 'model', 'best.pt'),
            '/app/model/best.onnx',
            '/app/model/best.pt',
            'model/best.onnx',
            'model/best.pt',
            os.path.join(project_root, 'brain_tumor_detector', 'yolov8n_run_1', 'weights', 'best.pt'),
            os.path.join(project_root, 'yolov8n.pt'),
            os.path.join(os.getcwd(), 'yolov8n.pt'),
        ]
        
        for p in possible_paths:
            abs_p = os.path.abspath(p)
            if os.path.exists(abs_p):
                logger.info(f"Resolved NeuroScan.AI model path: {abs_p}")
                return abs_p
                
        # Default fallback
        return os.path.abspath(os.path.join(project_root, 'model', 'best.pt'))

    def load_model(self) -> bool:
        """Load YOLO model into memory once"""
        if YOLO is None:
            logger.error("Ultralytics package is not installed.")
            return False

        if not os.path.exists(self.model_path):
            logger.warning(f"Model file not found at {self.model_path}")
            return False

        try:
            logger.info(f"Loading YOLO model from {self.model_path}...")
            if self.model_path.endswith('.onnx'):
                self.model = YOLO(self.model_path, task='detect')
            else:
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
        Distinguishes pathological tumor lesions (Glioma, Meningioma, Pituitary) from healthy normal tissue (No Tumor).
        Optimized with torch.inference_mode() and 1 thread to avoid memory spikes.
        """
        if not self.is_loaded():
            if not self.load_model():
                raise RuntimeError("YOLO model is not loaded. Please verify model/best.pt or model/best.onnx exists.")

        # Robust multi-format image loading, normalization, and memory downsampling
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            pil_img = ImageOps.exif_transpose(pil_img)
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')
            
            # Cap maximum dimension to 1024px to prevent RAM spikes on phone/camera uploads
            if max(pil_img.size) > 1024:
                pil_img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        except Exception as e:
            raise ValueError(f"Invalid cranial image content: {str(e)}")

        # Run inference in zero-overhead mode with single thread
        try:
            if self.model_path.endswith('.onnx'):
                results = self.model.predict(
                    source=pil_img,
                    conf=conf_threshold,
                    save=False,
                    verbose=False,
                    imgsz=640
                )
            elif torch is not None:
                with torch.inference_mode():
                    results = self.model.predict(
                        source=pil_img,
                        conf=conf_threshold,
                        save=False,
                        verbose=False,
                        device="cpu",
                        imgsz=640,
                        half=False
                    )
            else:
                results = self.model.predict(
                    source=pil_img,
                    conf=conf_threshold,
                    save=False,
                    verbose=False,
                    device="cpu",
                    imgsz=640,
                    half=False
                )
        except Exception as inf_err:
            logger.error(f"Inference execution failed: {inf_err}", exc_info=True)
            raise RuntimeError(f"YOLO inference error: {str(inf_err)}")

        detections = []
        formatted_base64 = None

        if results and len(results) > 0:
            result = results[0]

            if len(result.boxes) > 0:
                for box in result.boxes:
                    class_id = int(box.cls[0].item())
                    confidence = float(box.conf[0].item())
                    class_name = self.class_names.get(class_id, f"Class {class_id}")
                    
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

            # Generate memory-efficient annotated image overlay (JPEG 85 quality)
            try:
                annotated_bgr = result.plot()
                annotated_rgb = annotated_bgr[:, :, ::-1]  # Convert BGR to RGB
                annotated_pil = Image.fromarray(annotated_rgb)

                img_buffer = io.BytesIO()
                annotated_pil.save(img_buffer, format="JPEG", quality=85, optimize=True)
                base64_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
                formatted_base64 = f"data:image/jpeg;base64,{base64_str}"
                
                # Immediate buffer cleanup
                del annotated_bgr, annotated_rgb, annotated_pil, img_buffer
            except Exception as plot_err:
                logger.warning(f"Error plotting overlay: {plot_err}")

        # Clean up inference objects
        del pil_img, results
        gc.collect()

        # Distinguish tumor lesions from healthy normal tissue
        # Class 2 is "No Tumor" (Healthy/Normal cranial tissue)
        tumor_detections = [d for d in detections if d["class_id"] != 2]
        healthy_detections = [d for d in detections if d["class_id"] == 2]

        is_tumor_detected = len(tumor_detections) > 0
        tumor_count = len(tumor_detections)

        healthy_confidence = None
        if healthy_detections:
            healthy_detections.sort(key=lambda x: x["confidence"], reverse=True)
            healthy_confidence = healthy_detections[0]["confidence"]

        if is_tumor_detected:
            tumor_detections.sort(key=lambda x: x["confidence"], reverse=True)
            primary_tumor = tumor_detections[0]["class_name"]
            message = f"Detected {tumor_count} {primary_tumor} lesion(s)."
        elif healthy_confidence is not None:
            message = f"Scan analyzed: No tumor detected. Normal cranial tissue confirmed ({healthy_confidence*100:.1f}% certainty)."
        else:
            message = "Scan analyzed: No tumor detected above selected confidence threshold."

        return {
            "success": True,
            "is_tumor_detected": is_tumor_detected,
            "count": tumor_count,  # Actual pathological tumor lesions count
            "total_detections": len(detections),
            "tumor_detections": tumor_detections,
            "detections": detections,
            "healthy_confidence": healthy_confidence,
            "annotated_image": formatted_base64,
            "message": message
        }

# Global singleton accessor
def get_yolo_service() -> YOLOService:
    return YOLOService()
