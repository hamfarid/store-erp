"""
FILE: backend/src/schemas/breeding.py
PURPOSE: Breeding Program Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class BreedingBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    objective: Optional[str] = None
    status: str = Field(default="active", pattern="^(active|completed|cancelled|paused)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    generation: int = Field(default=1, ge=1)
    parent_male_id: Optional[int] = None
    parent_female_id: Optional[int] = None
    notes: Optional[str] = None


class BreedingCreate(BreedingBase):
    crop_ids: List[int] = []


class BreedingUpdate(BaseModel):
    name: Optional[str] = None
    objective: Optional[str] = None
    status: Optional[str] = None
    end_date: Optional[datetime] = None
    generation: Optional[int] = None
    notes: Optional[str] = None


class BreedingInDB(BreedingBase, TimestampMixin, BaseSchema):
    id: int
    creator_id: int


class BreedingResponse(BreedingInDB):
    creator_name: Optional[str] = None
    crop_count: Optional[int] = None
    crops: List["CropSummary"] = []


class BreedingListResponse(BaseModel):
    items: List[BreedingResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class CropSummary(BaseModel):
    id: int
    name: str
    category: str
    
    class Config:
        from_attributes = True


BreedingResponse.model_rebuild()


__all__ = ['BreedingBase', 'BreedingCreate', 'BreedingUpdate', 'BreedingInDB', 'BreedingResponse', 'BreedingListResponse']
