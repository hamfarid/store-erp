"""
ML Service - Gaara Scan AI v6.0.0
Disease diagnosis and image analysis service
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
import os
from datetime import datetime, timezone
import tempfile
from pathlib import Path

# MLflow Integration
import mlflow
from mlflow.pytorch import autolog as pytorch_autolog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import YOLO detector (lazy loading to handle missing dependencies)
yolo_detector = None


def get_yolo_detector():
    """Lazy load YOLO detector to handle missing dependencies gracefully"""
    global yolo_detector
    if yolo_detector is None:
        try:
            from yolo_detector import YOLODetector
            yolo_detector = YOLODetector()
            logger.info("YOLO detector loaded successfully")
        except ImportError as e:
            logger.warning(f"YOLO detector not available: {e}")
        except Exception as e:
            logger.error(f"Failed to load YOLO detector: {e}")
    return yolo_detector


# Disease knowledge base for symptom-based diagnosis
DISEASE_KNOWLEDGE_BASE = {
    "tomato": {
        "early_blight": {
            "symptoms": ["brown spots", "concentric rings", "yellowing leaves"],
            "recommendations": [
                "Remove affected leaves immediately",
                "Apply copper-based fungicide",
                "Improve air circulation between plants",
                "Avoid overhead watering"
            ]
        },
        "late_blight": {
            "symptoms": ["water-soaked lesions", "white mold", "rapid wilting"],
            "recommendations": [
                "Remove and destroy infected plants",
                "Apply fungicide preventively",
                "Ensure good drainage",
                "Rotate crops annually"
            ]
        },
        "leaf_mold": {
            "symptoms": ["yellow spots", "fuzzy mold", "curling leaves"],
            "recommendations": [
                "Increase ventilation",
                "Reduce humidity",
                "Apply sulfur-based fungicide",
                "Remove lower leaves"
            ]
        }
    },
    "potato": {
        "late_blight": {
            "symptoms": ["dark lesions", "white growth", "rotting tubers"],
            "recommendations": [
                "Destroy infected plants",
                "Apply preventive fungicide",
                "Harvest early if infection spreads",
                "Store tubers in cool, dry conditions"
            ]
        }
    },
    "wheat": {
        "rust": {
            "symptoms": ["orange pustules", "yellow streaks", "stunted growth"],
            "recommendations": [
                "Apply fungicide at first sign",
                "Plant resistant varieties",
                "Remove volunteer wheat",
                "Rotate with non-host crops"
            ]
        }
    }
}

# Initialize MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://ml-platform-mlflow:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "scan-ai-manus-diagnosis")

try:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    # Enable autologging for PyTorch models (YOLO uses PyTorch)
    pytorch_autolog()
    logger.info(f"✅ MLflow initialized: {MLFLOW_TRACKING_URI}")
    logger.info(f"✅ MLflow experiment: {MLFLOW_EXPERIMENT_NAME}")
except Exception as e:
    logger.warning(f"⚠️ MLflow initialization warning: {e}")
    logger.warning("   Continuing without MLflow tracking...")

# Initialize FastAPI app
app = FastAPI(
    title="Gaara Scan AI - ML Service",
    description="Disease diagnosis and image analysis service",
    version="4.3.1"
)

# CORS middleware - Configure allowed origins from environment
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:1505"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Models
class DiagnosisRequest(BaseModel):
    """Disease diagnosis request"""
    symptoms: List[str]
    crop_type: str
    environmental_conditions: Optional[Dict] = None

class DiagnosisResponse(BaseModel):
    """Disease diagnosis response"""
    success: bool
    disease_name: Optional[str] = None
    confidence: Optional[float] = None
    recommendations: Optional[List[str]] = None
    message: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str

# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="6.0.0",
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics endpoint"""
    import psutil
    from fastapi.responses import PlainTextResponse
    
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        metrics_text = f"""# HELP ml_service_up Whether the ML service is up
# TYPE ml_service_up gauge
ml_service_up 1
# HELP ml_service_cpu_usage_percent CPU usage percentage
# TYPE ml_service_cpu_usage_percent gauge
ml_service_cpu_usage_percent {cpu}
# HELP ml_service_memory_usage_percent Memory usage percentage
# TYPE ml_service_memory_usage_percent gauge
ml_service_memory_usage_percent {memory.percent}
# HELP ml_service_memory_available_bytes Available memory in bytes
# TYPE ml_service_memory_available_bytes gauge
ml_service_memory_available_bytes {memory.available}
"""
        return PlainTextResponse(content=metrics_text, media_type="text/plain")
    except Exception as e:
        return PlainTextResponse(
            content=f"# Error collecting metrics: {str(e)}\nml_service_up 0\n",
            media_type="text/plain"
        )

@app.post("/api/v1/diagnose", response_model=DiagnosisResponse)
async def diagnose_disease(request: DiagnosisRequest):
    """
    Diagnose plant disease based on symptoms and crop type with MLflow logging
    """
    start_time = datetime.now(timezone.utc)
    
    try:
        logger.info(f"Diagnosis request for crop: {request.crop_type}")

        # Start MLflow run for diagnosis
        with mlflow.start_run(run_name=f"diagnosis-{request.crop_type}-{start_time.strftime('%Y%m%d-%H%M%S')}"):
            # Log parameters
            mlflow.log_params({
                "crop_type": request.crop_type,
                "symptoms_count": len(request.symptoms),
                "has_environmental_conditions": request.environmental_conditions is not None
            })
            
            # Symptom-based diagnosis using knowledge base
            crop_type = request.crop_type.lower()
            symptoms = [s.lower() for s in request.symptoms]

            best_match = None
            best_score = 0.0
            best_recommendations = []

            if crop_type in DISEASE_KNOWLEDGE_BASE:
                crop_diseases = DISEASE_KNOWLEDGE_BASE[crop_type]
                for disease_name, disease_info in crop_diseases.items():
                    disease_symptoms = [s.lower() for s in disease_info["symptoms"]]
                    # Calculate symptom match score
                    matches = sum(
                        1 for s in symptoms
                        if any(ds in s or s in ds for ds in disease_symptoms)
                    )
                    score = matches / max(len(disease_symptoms), 1)

                    if score > best_score:
                        best_score = score
                        best_match = disease_name.replace("_", " ").title()
                        best_recommendations = disease_info["recommendations"]

            # Calculate confidence
            confidence = min(best_score + 0.3, 0.95) if best_match and best_score > 0.3 else 0.0
            
            # Log metrics
            mlflow.log_metrics({
                "diagnosis_confidence": confidence,
                "symptom_match_score": best_score,
                "diagnosis_success": 1.0 if best_match else 0.0
            })
            
            # Set tags
            mlflow.set_tags({
                "crop_type": request.crop_type,
                "disease_detected": best_match or "none",
                "diagnosis_method": "symptom_based"
            })
            
            # Calculate processing time
            processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            mlflow.log_metric("processing_time_seconds", processing_time)
            
            # Log environmental conditions if provided
            if request.environmental_conditions:
                mlflow.log_params(request.environmental_conditions)

            if best_match and best_score > 0.3:
                return DiagnosisResponse(
                    success=True,
                    disease_name=best_match,
                    confidence=confidence,
                    recommendations=best_recommendations,
                    message="Diagnosis completed based on symptom analysis"
                )
            else:
                return DiagnosisResponse(
                    success=True,
                    disease_name=None,
                    confidence=0.0,
                    recommendations=[
                        "Consult with a local agricultural expert",
                        "Take clear photos of affected areas",
                        "Monitor plant health over the next few days"
                    ],
                    message="Unable to determine specific disease. Please provide more symptoms or use image analysis."
                )

    except Exception as e:
        logger.error(f"Diagnosis error: {str(e)}")
        # Log error to MLflow
        try:
            with mlflow.start_run(run_name=f"diagnosis-error-{start_time.strftime('%Y%m%d-%H%M%S')}"):
                mlflow.log_param("error", str(e))
                mlflow.log_metric("diagnosis_success", 0.0)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image for disease detection using YOLO model with MLflow logging
    """
    start_time = datetime.now(timezone.utc)
    
    try:
        logger.info(f"Image analysis request: {file.filename}")

        # Start MLflow run for image analysis
        with mlflow.start_run(run_name=f"image-analysis-{start_time.strftime('%Y%m%d-%H%M%S')}"):
            # Log parameters
            mlflow.log_params({
                "filename": file.filename,
                "content_type": file.content_type,
                "analysis_method": "yolo"
            })

            # Validate file type
            if not file.content_type.startswith("image/"):
                mlflow.log_metric("analysis_success", 0.0)
                raise HTTPException(
                    status_code=400,
                    detail="Invalid file type. Only images are allowed."
                )

            # Read image bytes
            image_bytes = await file.read()
            image_size = len(image_bytes)
            mlflow.log_metric("image_size_bytes", image_size)

            # Try YOLO detection
            detector = get_yolo_detector()
            if detector is not None:
                detections = detector.detect_from_bytes(image_bytes)
                
                # Log detection metrics
                mlflow.log_metric("detections_count", len(detections) if detections else 0)
                mlflow.log_metric("yolo_available", 1.0)

                if detections:
                    # Get the detection with highest confidence
                    best_detection = max(detections, key=lambda x: x["confidence"])
                    disease_name = best_detection["class_name"].replace("_", " ").title()
                    confidence = best_detection["confidence"]
                    
                    # Log metrics
                    mlflow.log_metrics({
                        "detection_confidence": confidence,
                        "analysis_success": 1.0
                    })
                    mlflow.set_tags({
                        "disease_detected": disease_name,
                        "analysis_method": "yolo"
                    })
                    
                    # Get recommendations based on detected disease
                    recommendations = _get_recommendations_for_disease(disease_name)

                    return {
                        "success": True,
                        "filename": file.filename,
                        "disease_detected": True,
                        "disease_name": disease_name,
                        "confidence": round(confidence, 3),
                        "detections": detections,
                        "recommendations": recommendations,
                        "message": "Image analyzed successfully with YOLO model"
                    }
                else:
                    # No detections found
                    mlflow.log_metrics({
                        "analysis_success": 0.0,
                        "detections_count": 0,
                        "detection_confidence": 0.0
                    })
                    processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                    mlflow.log_metric("processing_time_seconds", processing_time)
                    mlflow.set_tags({
                        "disease_detected": "none",
                        "analysis_method": "yolo"
                    })
                    return {
                        "success": True,
                        "filename": file.filename,
                        "disease_detected": False,
                        "disease_name": None,
                        "confidence": 0.0,
                        "message": "No disease detected in the image"
                    }
            else:
                # Fallback response when YOLO is not available
                logger.warning("YOLO detector not available, returning fallback")
                mlflow.log_metrics({
                    "yolo_available": 0.0,
                    "analysis_success": 0.0,
                    "detections_count": 0
                })
                processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                mlflow.log_metric("processing_time_seconds", processing_time)
                mlflow.set_tags({
                    "disease_detected": "none",
                    "analysis_method": "fallback",
                    "yolo_available": "false"
                })
                return {
                    "success": True,
                    "filename": file.filename,
                    "disease_detected": False,
                    "disease_name": None,
                    "confidence": 0.0,
                    "message": "ML model not available. Please try again later."
                }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image analysis error: {str(e)}")
        # Log error to MLflow
        try:
            with mlflow.start_run(run_name=f"image-analysis-error-{start_time.strftime('%Y%m%d-%H%M%S')}"):
                mlflow.log_param("error", str(e))
                mlflow.log_metric("analysis_success", 0.0)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))


def _get_recommendations_for_disease(disease_name: str) -> List[str]:
    """Get treatment recommendations for a detected disease"""
    disease_lower = disease_name.lower().replace(" ", "_")

    # Search through knowledge base
    for crop_diseases in DISEASE_KNOWLEDGE_BASE.values():
        if disease_lower in crop_diseases:
            return crop_diseases[disease_lower]["recommendations"]

    # Default recommendations
    return [
        "Consult with a local agricultural expert",
        "Remove affected plant parts",
        "Improve air circulation",
        "Monitor nearby plants for spread"
    ]

@app.get("/api/v1/models")
async def list_models():
    """List available ML models"""
    return {
        "success": True,
        "models": [
            {
                "name": "disease_classifier_v1",
                "version": "1.0.0",
                "type": "classification",
                "status": "active"
            },
            {
                "name": "image_segmentation_v1",
                "version": "1.0.0",
                "type": "segmentation",
                "status": "active"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 4101))
    uvicorn.run(app, host="0.0.0.0", port=port)
