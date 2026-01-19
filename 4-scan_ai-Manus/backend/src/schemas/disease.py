"""
FILE: backend/src/schemas/disease.py
PURPOSE: Disease Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class DiseaseBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    name_ar: Optional[str] = None
    scientific_name: Optional[str] = None
    category: str = Field(default="fungal", pattern="^(fungal|bacterial|viral|pest|nutrient|environmental|other)$")
    severity_level: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    symptoms: Optional[str] = None
    symptoms_ar: Optional[str] = None
    causes: Optional[str] = None
    causes_ar: Optional[str] = None
    treatment: Optional[str] = None
    treatment_ar: Optional[str] = None
    prevention: Optional[str] = None
    prevention_ar: Optional[str] = None
    image_url: Optional[str] = None


class DiseaseCreate(DiseaseBase):
    pass


class DiseaseUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    severity_level: Optional[str] = None
    symptoms: Optional[str] = None
    symptoms_ar: Optional[str] = None
    causes: Optional[str] = None
    causes_ar: Optional[str] = None
    treatment: Optional[str] = None
    treatment_ar: Optional[str] = None
    prevention: Optional[str] = None
    prevention_ar: Optional[str] = None
    image_url: Optional[str] = None


class DiseaseInDB(DiseaseBase, TimestampMixin, BaseSchema):
    id: int


class DiseaseResponse(DiseaseInDB):
    diagnosis_count: Optional[int] = None
    affected_crops: List[str] = []


class DiseaseListResponse(BaseModel):
    items: List[DiseaseResponse]
    total: int
    page: int
    limit: int
    total_pages: int


__all__ = ['DiseaseBase', 'DiseaseCreate', 'DiseaseUpdate', 'DiseaseInDB', 'DiseaseResponse', 'DiseaseListResponse']
