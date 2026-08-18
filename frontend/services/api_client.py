import requests
import os
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class APIClient:
    """
    Client abstraction for communicating with FastAPI backend API.
    Handles health checks and YOLOv8 image inference requests.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

    def health_check(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Poll GET /health to check if backend server and YOLO model are ready.
        Returns (is_healthy, response_data_or_error_dict).
        """
        try:
            url = f"{self.base_url}/health"
            res = requests.get(url, timeout=2.5)
            if res.status_code == 200:
                data = res.json()
                is_loaded = data.get("model_loaded", False)
                return is_loaded, data
            return False, {"error": f"HTTP {res.status_code}"}
        except Exception as e:
            logger.debug(f"Health check failed: {e}")
            return False, {"error": str(e)}

    def predict_image(
        self,
        image_bytes: bytes,
        filename: str = "mri_scan.jpg",
        confidence: float = 0.50
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Send image bytes via POST /predict to run YOLOv8 model inference.
        Returns (success, result_dict_or_error_dict).
        """
        try:
            url = f"{self.base_url}/predict"
            files = {"file": (filename, image_bytes, "image/jpeg")}
            data = {"confidence": str(confidence)}
            
            res = requests.post(url, files=files, data=data, timeout=30)
            
            if res.status_code == 200:
                return True, res.json()
            else:
                try:
                    err_msg = res.json().get("detail", f"HTTP {res.status_code}")
                except Exception:
                    err_msg = f"HTTP {res.status_code} Error"
                return False, {"error": err_msg}
        except requests.exceptions.Timeout:
            return False, {"error": "Request timed out while running inference."}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Unable to connect to the inference service."}
        except Exception as e:
            return False, {"error": f"An error occurred: {str(e)}"}

# Global singleton client instance
_api_client = APIClient()

def get_api_client() -> APIClient:
    return _api_client
