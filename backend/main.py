from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.routes.prediction import router as prediction_router
from backend.services.yolo_service import get_yolo_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("neuroscan_backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for initializing YOLO model on startup"""
    logger.info("Initializing NeuroScan AI Backend Service...")
    service = get_yolo_service()
    if service.is_loaded():
        logger.info("YOLOv8 Model successfully loaded into memory.")
    else:
        logger.warning("YOLOv8 Model failed to load during startup.")
    yield
    logger.info("Shutting down NeuroScan AI Backend Service.")

app = FastAPI(
    title="NeuroScan AI Enterprise API",
    description="FastAPI Backend for YOLOv8 Brain Tumor Detection in MRI Scans",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Streamlit frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(prediction_router)

@app.get("/", summary="Root endpoint")
async def root():
    return {
        "brand": "NeuroScan AI Enterprise",
        "status": "online",
        "documentation": "/docs",
        "health_check": "/health",
        "prediction_endpoint": "/predict"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
