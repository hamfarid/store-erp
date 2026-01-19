"""
FILE: backend/src/schemas/diagnosis.py
PURPOSE: Diagnosis Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19

Version: 1.0.0
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .common import BaseSchema, TimestampMixin


class DiagnosisBase(BaseModel):
    """Base diagnosis schema"""
    farm_id: Optional[int] = None
    notes: Optional[str] = None


class DiagnosisCreate(DiagnosisBase):
    """Schema for creating a diagnosis (image upload)"""
    pass


class DiagnosisResult(BaseModel):
    """ML diagnosis result"""
    disease: str
    disease_ar: Optional[str] = None
    confidence: float = Field(..., ge=0, le=1)
    severity: str = Field(..., pattern="^(low|medium|high|critical|healthy)$")
    recommendations: List[str] = []
    recommendations_ar: List[str] = []
    affected_area_percentage: Optional[float] = Field(None, ge=0, le=100)
    plant_health_score: Optional[float] = Field(None, ge=0, le=100)


class DiagnosisUpdate(BaseModel):
    """Schema for updating diagnosis feedback"""
    user_rating: Optional[int] = Field(None, ge=1, le=5)
    user_feedback: Optional[str] = None
    is_accurate: Optional[str] = Field(None, pattern="^(yes|no|partially)$")


class DiagnosisInDB(DiagnosisBase, TimestampMixin, BaseSchema):
    """Diagnosis as stored in database"""
    id: int
    user_id: int
    image_url: str
    thumbnail_url: Optional[str] = None
    disease: Optional[str] = None
    disease_ar: Optional[str] = None
    confidence: Optional[float] = None
    severity: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    processing_time: Optional[float] = None
    recommendations: Optional[List[str]] = None
    recommendations_ar: Optional[List[str]] = None
    affected_area_percentage: Optional[float] = None
    plant_health_score: Optional[float] = None
    status: str = "completed"
    error_message: Optional[str] = None
    user_rating: Optional[int] = None
    user_feedback: Optional[str] = None
    is_accurate: Optional[str] = None


class DiagnosisResponse(DiagnosisInDB):
    """Diagnosis response with additional data"""
    user_name: Optional[str] = None
    farm_name: Optional[str] = None
    disease_info: Optional[Dict[str, Any]] = None


class DiagnosisListResponse(BaseModel):
    """Diagnosis list response"""
    items: List[DiagnosisResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class DiagnosisStats(BaseModel):
    """Diagnosis statistics"""
    total_diagnoses: int
    diagnoses_today: int
    diagnoses_this_week: int
    diagnoses_this_month: int
    average_confidence: float
    healthy_percentage: float
    most_common_disease: Optional[str] = None
    most_common_disease_count: int = 0
    severity_distribution: Dict[str, int] = {}
    accuracy_feedback: Dict[str, int] = {}


class DiagnosisHistoryItem(BaseModel):
    """Simplified diagnosis for history lists"""
    id: int
    image_url: str
    disease: Optional[str] = None
    confidence: Optional[float] = None
    severity: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BatchDiagnosisRequest(BaseModel):
    """Request for batch diagnosis"""
    farm_id: Optional[int] = None
    image_urls: List[str] = Field(..., min_length=1, max_length=10)


class BatchDiagnosisResponse(BaseModel):
    """Response for batch diagnosis"""
    total_submitted: int
    successful: int
    failed: int
    results: List[DiagnosisResponse]
    errors: List[Dict[str, Any]] = []


__all__ = [
    'DiagnosisBase',
    'DiagnosisCreate',
    'DiagnosisResult',
    'DiagnosisUpdate',
    'DiagnosisInDB',
    'DiagnosisResponse',
    'DiagnosisListResponse',
    'DiagnosisStats',
    'DiagnosisHistoryItem',
    'BatchDiagnosisRequest',
    'BatchDiagnosisResponse',
]
