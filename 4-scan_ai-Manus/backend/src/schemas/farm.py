"""
FILE: backend/src/schemas/farm.py
PURPOSE: Farm Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19

Version: 1.0.0
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from .common import BaseSchema, TimestampMixin


class FarmBase(BaseModel):
    """Base farm schema"""
    name: str = Field(..., min_length=2, max_length=255, description="Farm name")
    location: str = Field(..., min_length=2, max_length=500, description="Location description")
    address: Optional[str] = Field(None, max_length=1000)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    area: float = Field(..., gt=0, description="Farm area")
    area_unit: str = Field(default="hectare", pattern="^(hectare|acre|sqm)$")
    crop_type: Optional[str] = Field(None, max_length=100)
    soil_type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    notes: Optional[str] = None


class FarmCreate(FarmBase):
    """Schema for creating a farm"""
    pass


class FarmUpdate(BaseModel):
    """Schema for updating a farm"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    location: Optional[str] = Field(None, min_length=2, max_length=500)
    address: Optional[str] = Field(None, max_length=1000)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    area: Optional[float] = Field(None, gt=0)
    area_unit: Optional[str] = Field(None, pattern="^(hectare|acre|sqm)$")
    crop_type: Optional[str] = Field(None, max_length=100)
    soil_type: Optional[str] = Field(None, max_length=100)
    is_active: Optional[str] = Field(None, pattern="^(active|inactive|archived)$")
    description: Optional[str] = None
    notes: Optional[str] = None


class FarmInDB(FarmBase, TimestampMixin, BaseSchema):
    """Farm schema as stored in database"""
    id: int
    owner_id: int
    is_active: str = "active"


class FarmResponse(FarmInDB):
    """Farm response schema"""
    owner_name: Optional[str] = None
    crop_count: Optional[int] = None
    diagnosis_count: Optional[int] = None
    sensor_count: Optional[int] = None


class FarmListResponse(BaseModel):
    """Farm list response"""
    items: List[FarmResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class FarmWithCrops(FarmResponse):
    """Farm with crops relationship"""
    crops: List["CropSummary"] = []


class FarmStats(BaseModel):
    """Farm statistics"""
    total_farms: int
    active_farms: int
    total_area: float
    total_diagnoses: int
    healthy_percentage: float
    recent_alerts: int


class CropSummary(BaseModel):
    """Crop summary for relationships"""
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True


FarmWithCrops.model_rebuild()


__all__ = [
    'FarmBase',
    'FarmCreate',
    'FarmUpdate',
    'FarmInDB',
    'FarmResponse',
    'FarmListResponse',
    'FarmWithCrops',
    'FarmStats',
]
