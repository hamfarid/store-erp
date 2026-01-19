"""
ML Diagnosis API - Gaara Scan AI v4.3.1
API endpoints for ML-based disease diagnosis
"""

import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from ...services.ml_service import ml_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ml", tags=["ML Diagnosis"])


class DiagnosisRequest(BaseModel):
    """Disease diagnosis request model"""
    symptoms: List[str]
    crop_type: str
    environmental_conditions: Optional[Dict] = None


class DiagnosisResponse(BaseModel):
    """Disease diagnosis response model"""
    success: bool
    data: Optional[Dict] = None
    message: str


@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_disease(request: DiagnosisRequest):
    """
    Diagnose plant disease based on symptoms

    - **symptoms**: List of observed symptoms
    - **crop_type**: Type of crop (e.g., tomato, wheat)
    - **environmental_conditions**: Optional environmental data
    """
    try:
        result = await ml_client.diagnose_disease(
            symptoms=request.symptoms,
            crop_type=request.crop_type,
            environmental_conditions=request.environmental_conditions
        )

        return DiagnosisResponse(
            success=True,
            data=result,
            message="Diagnosis completed successfully"
        )

    except Exception as e:
        logger.error(f"Diagnosis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-image", response_model=DiagnosisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image for disease detection

    - **file**: Image file to analyze
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only images are allowed."
            )

        result = await ml_client.analyze_image(file)

        return DiagnosisResponse(
            success=True,
            data=result,
            message="Image analyzed successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """
    List available ML models
    """
    try:
        result = await ml_client.list_models()
        return {
            "success": True,
            "data": result,
            "message": "Models retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Failed to list models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def ml_service_health():
    """
    Check ML service health status
    """
    try:
        result = await ml_client.health_check()
        return {
            "success": True,
            "data": result,
            "message": "Health check completed"
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "success": False,
            "data": None,
            "message": f"ML service is unavailable: {str(e)}"
        }
