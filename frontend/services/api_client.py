import os
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class APIClient:
    """
    High-performance client abstraction for NeuroScan.AI inference and consultations.
    Automatically prioritizes ultra-fast in-process PyTorch YOLO inference when available locally,
    eliminating network latency, socket timeouts, and Render cold-start delays.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        self.explicit_api_url = os.getenv("API_BASE_URL")
        self.base_url = base_url or self.explicit_api_url
        
        # Check direct in-process YOLO engine availability
        self._direct_yolo = None
        self._use_direct = False
        self._ensure_direct_engine()

    def _ensure_direct_engine(self) -> bool:
        """Initialize or verify direct in-process YOLO engine"""
        if self._direct_yolo and self._direct_yolo.is_loaded():
            return True
        try:
            from backend.services.yolo_service import get_yolo_service
            svc = get_yolo_service()
            if svc.is_loaded():
                self._direct_yolo = svc
                self._use_direct = True
                logger.info("NeuroScan.AI Engine running in direct high-speed in-process mode.")
                return True
        except Exception as e:
            logger.debug(f"Direct engine check: {e}")
        return False

    def health_check(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Fast health check. Guaranteed instantaneous response when direct model is available.
        """
        if self._ensure_direct_engine() and self._direct_yolo:
            return True, {
                "status": "healthy",
                "model_loaded": True,
                "model_path": self._direct_yolo.model_path,
                "classes": self._direct_yolo.get_class_list(),
                "mode": "in-process"
            }

        # If direct model is unavailable and an external base_url is configured:
        if self.base_url and not ("127.0.0.1" in self.base_url or "localhost" in self.base_url):
            try:
                import requests
                url = f"{self.base_url}/health"
                res = requests.get(url, timeout=1.5)
                if res.status_code == 200:
                    data = res.json()
                    return data.get("model_loaded", False), data
                return False, {"error": f"HTTP {res.status_code}"}
            except Exception as e:
                return False, {"error": str(e)}

        return False, {"error": "NeuroScan.AI YOLO model weights not found locally."}

    def predict_image(
        self,
        image_bytes: bytes,
        filename: str = "mri_scan.jpg",
        confidence: float = 0.50
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Perform high-speed YOLOv8 brain tumor detection.
        Executes in-process (sub-35ms) directly, eliminating network hops and timeouts.
        """
        # 1. Primary: Ultra-fast in-process inference
        if self._ensure_direct_engine() and self._direct_yolo:
            try:
                res = self._direct_yolo.predict(image_bytes=image_bytes, conf_threshold=confidence)
                return True, res
            except Exception as direct_err:
                logger.error(f"In-process prediction error: {direct_err}", exc_info=True)
                return False, {"error": f"Inference error: {str(direct_err)}"}

        # 2. Secondary fallback: only if external API server is explicitly configured
        if self.base_url and not ("127.0.0.1" in self.base_url or "localhost" in self.base_url):
            mime_type = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
            try:
                import requests
                url = f"{self.base_url}/predict"
                files = {"file": (filename, image_bytes, mime_type)}
                data = {"confidence": str(confidence)}
                
                res = requests.post(url, files=files, data=data, timeout=5)
                if res.status_code == 200:
                    return True, res.json()
                else:
                    try:
                        err_msg = res.json().get("detail", f"HTTP {res.status_code}")
                    except Exception:
                        err_msg = f"HTTP {res.status_code} Error"
                    return False, {"error": err_msg}
            except Exception as net_err:
                return False, {"error": f"Inference service connection error: {str(net_err)}"}

        return False, {"error": "Local NeuroScan.AI model could not be loaded. Please ensure model/best.pt exists."}

    def submit_contact(
        self,
        full_name: str,
        phone: str,
        location: str,
        email: Optional[str] = None,
        message: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Submit consultation request.
        Directly saves to SQLite database without unnecessary network hops.
        """
        # In standalone/direct mode, save immediately to SQLite
        if self._use_direct or not self.explicit_api_url:
            try:
                from backend.services.contact_service import create_contact
                rec = create_contact(
                    full_name=full_name,
                    phone=phone,
                    location=location,
                    email=email,
                    message=message
                )
                return True, {
                    "status": "success",
                    "message": "Consultation request saved directly to database.",
                    "contact_id": rec["id"]
                }
            except Exception as db_err:
                logger.error(f"Direct DB contact creation error: {db_err}")
                return False, {"error": f"Failed to store contact request: {str(db_err)}"}

        payload = {
            "full_name": full_name,
            "phone": phone,
            "location": location,
            "email": email or "",
            "message": message or ""
        }
        try:
            import requests
            url = f"{self.base_url}/contact"
            res = requests.post(url, json=payload, timeout=3)
            if res.status_code == 200:
                return True, res.json()
            else:
                try:
                    err = res.json().get("detail", f"HTTP {res.status_code}")
                except Exception:
                    err = f"HTTP {res.status_code} Error"
                return False, {"error": err}
        except Exception:
            try:
                from backend.services.contact_service import create_contact
                rec = create_contact(
                    full_name=full_name,
                    phone=phone,
                    location=location,
                    email=email,
                    message=message
                )
                return True, {
                    "status": "success",
                    "message": "Consultation request saved directly to database (fallback).",
                    "contact_id": rec["id"]
                }
            except Exception as db_err:
                return False, {"error": f"Failed to store contact: {str(db_err)}"}

# Global singleton client instance
_api_client = APIClient()

def get_api_client() -> APIClient:
    return _api_client
