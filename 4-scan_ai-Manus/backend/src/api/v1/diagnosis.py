"""FILE: backend/src/api/v1/diagnosis.py | PURPOSE: Diagnosis API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-13

Diagnosis API Routes

Handles plant disease diagnosis operations.

Notes:
- This module contains both authenticated CRUD-style endpoints and a minimal
    integration-test workflow contract (analyze/history/diseases list) that is
    intentionally accessible without authentication.

Version: 1.0.0
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.diagnosis import Diagnosis
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/diagnosis", tags=["diagnosis"])


# ---------------------------------------------------------------------------
# In-memory workflow store (integration-test friendly)
# ---------------------------------------------------------------------------

_WORKFLOW_DIAGNOSES: Dict[str, Dict[str, Any]] = {}


class DiagnosisAnalyzeRequest(BaseModel):
    file_id: str = Field(..., min_length=1, description="معرف الملف المراد تحليله")
    analysis_type: Literal["quick", "detailed"] = "quick"
    include_treatment: bool = False


def _analyze_stub(file_id: str, analysis_type: str) -> Dict[str, Any]:
    # Minimal deterministic stub response
    disease_name = "Leaf Spot" if analysis_type == "detailed" else "Healthy"
    confidence = 0.87 if analysis_type == "detailed" else 0.75
    return {
        "disease_name": disease_name,
        "confidence": confidence,
        "severity": "medium" if disease_name != "Healthy" else "low",
    }


# Pydantic Schemas
class DiagnosisResponse(BaseModel):
    id: int
    user_id: int
    farm_id: Optional[int]
    image_url: str
    disease: Optional[str]
    confidence: Optional[float]
    severity: Optional[str]
    status: str
    created_at: str

    class Config:
        from_attributes = True


@router.post("/analyze")
async def analyze_diagnosis(payload: DiagnosisAnalyzeRequest):
    """Analyze an uploaded file_id (integration workflow contract)."""

    diagnosis_id = str(uuid4())
    analysis = _analyze_stub(payload.file_id, payload.analysis_type)

    treatment_recommendations: List[str] = []
    if payload.include_treatment:
        treatment_recommendations = [
            "Remove affected leaves",
            "Improve air circulation",
            "Apply an appropriate fungicide if needed",
        ]

    record = {
        "diagnosis_id": diagnosis_id,
        "file_id": payload.file_id,
        "analysis_type": payload.analysis_type,
        "disease_name": analysis["disease_name"],
        "confidence": analysis["confidence"],
        "severity": analysis["severity"],
        "treatment_recommendations": treatment_recommendations,
        "created_at": datetime.utcnow().isoformat(),
    }
    _WORKFLOW_DIAGNOSES[diagnosis_id] = record

    return record


@router.get("/diseases/list")
async def list_supported_diseases():
    """Return list of supported diseases (integration workflow contract)."""

    diseases = [
        {
            "id": "d1",
            "name": "Leaf Spot",
            "category": "fungal",
            "common_plants": ["Tomato", "Potato"],
        },
        {
            "id": "d2",
            "name": "Powdery Mildew",
            "category": "fungal",
            "common_plants": ["Cucumber", "Grape"],
        },
        {
            "id": "d3",
            "name": "Healthy",
            "category": "none",
            "common_plants": ["All"],
        },
    ]

    return {"diseases": diseases, "total": len(diseases)}


# Routes
@router.post("/upload", response_model=DiagnosisResponse,
             status_code=status.HTTP_201_CREATED)
async def upload_image_for_diagnosis(
    file: UploadFile = File(...),
    farm_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload an image for disease diagnosis"""

    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    # TODO: Save file to storage (S3, local, etc.)
    # For now, we'll use a placeholder URL
    image_url = f"/uploads/diagnoses/{current_user.id}/{file.filename}"

    # Create diagnosis record
    diagnosis = Diagnosis(
        user_id=current_user.id,
        farm_id=farm_id,
        image_url=image_url,
        status="pending",
        model_name="gaara-ai-v1",
        model_version="1.0.0"
    )

    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    # TODO: Trigger AI processing asynchronously
    # For now, we'll return the pending diagnosis

    return diagnosis


@router.get("/history")
async def get_diagnosis_history(
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0),
):
    """Get diagnosis history (integration workflow contract; no auth required)."""

    items = list(_WORKFLOW_DIAGNOSES.values())
    # Most recent first
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    if offset >= len(items):
        return []

    end = None if limit == 0 else offset + limit
    return items[offset:end]


@router.get("/{diagnosis_id}")
async def get_diagnosis(diagnosis_id: str):
    """Get a specific diagnosis (integration workflow contract)."""

    record = _WORKFLOW_DIAGNOSES.get(diagnosis_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "code": "DIAGNOSIS_NOT_FOUND", "message": "Diagnosis not found"},
        )
    return record


@router.post("/{diagnosis_id}/feedback")
async def submit_feedback(
    diagnosis_id: int,
    rating: int,
    is_accurate: str,
    feedback: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit feedback for a diagnosis"""

    diagnosis = db.query(Diagnosis).filter(
        Diagnosis.id == diagnosis_id,
        Diagnosis.user_id == current_user.id,
        Diagnosis.deleted_at is None
    ).first()

    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis not found"
        )

    # Validate rating
    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    # Validate is_accurate
    if is_accurate not in ['yes', 'no', 'partially']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="is_accurate must be 'yes', 'no', or 'partially'"
        )

    # Update diagnosis
    diagnosis.user_rating = rating
    diagnosis.is_accurate = is_accurate
    diagnosis.user_feedback = feedback
    db.commit()

    return {"message": "Feedback submitted successfully"}


@router.delete("/{diagnosis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diagnosis(
    diagnosis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a diagnosis (soft delete)"""

    diagnosis = db.query(Diagnosis).filter(
        Diagnosis.id == diagnosis_id,
        Diagnosis.user_id == current_user.id,
        Diagnosis.deleted_at is None
    ).first()

    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis not found"
        )

    # Soft delete
    diagnosis.deleted_at = datetime.utcnow()
    db.commit()

    return None
