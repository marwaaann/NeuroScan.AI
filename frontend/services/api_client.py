import os
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class APIClient:
    """
    High-performance client abstraction for Nuroscan inference and consultations.
    Automatically prioritizes ultra-fast in-process PyTorch YOLO inference when available locally,
    eliminating network latency, socket timeouts, and Render cold-start delays.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        self.explicit_api_url = os.getenv("API_BASE_URL")
        self.base_url = base_url or self.explicit_api_url
        
        # Check direct in-process YOLO engine availability
        self._direct_yolo = None
        self._use_direct = False
        self._cached_health = None
        
        # If API_BASE_URL is not explicitly set, prefer ultra-fast local engine
        if not self.explicit_api_url:
            try:
                from backend.services.yolo_service import get_yolo_service
                svc = get_yolo_service()
                if svc.is_loaded():
                    self._direct_yolo = svc
                    self._use_direct = True
                    logger.info("Nuroscan Engine running in direct high-speed in-process mode.")
            except Exception as e:
                logger.debug(f"Direct engine check: {e}")

    def health_check(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Fast health check. If in direct mode, returns instantaneously without network blocking.
        """
        if self._use_direct and self._direct_yolo:
            return True, {
                "status": "healthy",
                "model_loaded": True,
                "model_path": self._direct_yolo.model_path,
                "classes": self._direct_yolo.get_class_list(),
                "mode": "standalone"
            }

        # If base_url is configured or direct was not initialized:
        target_url = self.base_url or "http://127.0.0.1:8000"
        try:
            import requests
            url = f"{target_url}/health"
            res = requests.get(url, timeout=0.8)
            if res.status_code == 200:
                data = res.json()
                return data.get("model_loaded", False), data
            return False, {"error": f"HTTP {res.status_code}"}
        except Exception as e:
            # Fallback to direct YOLO service
            try:
                from backend.services.yolo_service import get_yolo_service
                svc = get_yolo_service()
                if svc.is_loaded():
                    self._direct_yolo = svc
                    self._use_direct = True
                    return True, {
                        "status": "healthy",
                        "model_loaded": True,
                        "model_path": svc.model_path,
                        "classes": svc.get_class_list(),
                        "mode": "standalone"
                    }
            except Exception:
                pass
            return False, {"error": str(e)}

    def predict_image(
        self,
        image_bytes: bytes,
        filename: str = "mri_scan.jpg",
        confidence: float = 0.50
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Perform high-speed YOLOv8 brain tumor detection.
        Executes in-process (sub-35ms) if available; otherwise calls remote microservice.
        """
        # 1. Fast-path in-process inference (instant, zero network latency)
        if self._use_direct and self._direct_yolo:
            try:
                res = self._direct_yolo.predict(image_bytes=image_bytes, conf_threshold=confidence)
                return True, res
            except Exception as direct_err:
                logger.error(f"In-process prediction error: {direct_err}")
                return False, {"error": str(direct_err)}

        # 2. Remote API path
        target_url = self.base_url or "http://127.0.0.1:8000"
        mime_type = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
        
        try:
            import requests
            url = f"{target_url}/predict"
            files = {"file": (filename, image_bytes, mime_type)}
            data = {"confidence": str(confidence)}
            
            res = requests.post(url, files=files, data=data, timeout=8)
            if res.status_code == 200:
                return True, res.json()
            else:
                try:
                    err_msg = res.json().get("detail", f"HTTP {res.status_code}")
                except Exception:
                    err_msg = f"HTTP {res.status_code} Error"
                return False, {"error": err_msg}
        except Exception as net_err:
            # Fallback to direct YOLOService
            try:
                from backend.services.yolo_service import get_yolo_service
                svc = get_yolo_service()
                if svc.is_loaded():
                    self._direct_yolo = svc
                    self._use_direct = True
                    result = svc.predict(image_bytes=image_bytes, conf_threshold=confidence)
                    return True, result
            except Exception as direct_err:
                logger.error(f"Direct inference fallback error: {direct_err}")
            return False, {"error": f"Inference service unavailable: {str(net_err)}"}

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
