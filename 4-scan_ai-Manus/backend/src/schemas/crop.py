"""
FILE: backend/src/schemas/crop.py
PURPOSE: Crop Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class CropBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    category: str = Field(..., pattern="^(vegetables|fruits|grains|herbs|trees|flowers|other)$")
    growing_season: Optional[str] = None
    water_needs: str = Field(default="medium", pattern="^(low|medium|high)$")
    sunlight_needs: str = Field(default="full", pattern="^(full|partial|shade)$")
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    growth_duration: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    care_tips: Optional[str] = None
    common_diseases: Optional[str] = None
    image_url: Optional[str] = None


class CropCreate(CropBase):
    pass


class CropUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    growing_season: Optional[str] = None
    water_needs: Optional[str] = None
    sunlight_needs: Optional[str] = None
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    growth_duration: Optional[int] = None
    description: Optional[str] = None
    care_tips: Optional[str] = None
    image_url: Optional[str] = None


class CropInDB(CropBase, TimestampMixin, BaseSchema):
    id: int


class CropResponse(CropInDB):
    disease_count: Optional[int] = None
    farm_count: Optional[int] = None


class CropListResponse(BaseModel):
    items: List[CropResponse]
    total: int
    page: int
    limit: int
    total_pages: int


__all__ = ['CropBase', 'CropCreate', 'CropUpdate', 'CropInDB', 'CropResponse', 'CropListResponse']
