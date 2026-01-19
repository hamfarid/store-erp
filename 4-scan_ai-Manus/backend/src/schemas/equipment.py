"""
FILE: backend/src/schemas/equipment.py
PURPOSE: Equipment Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class EquipmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    equipment_type: str = Field(..., pattern="^(tractor|harvester|irrigation|sprayer|seeder|plow|other)$")
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    status: str = Field(default="operational", pattern="^(operational|maintenance|repair|retired)$")
    condition: str = Field(default="good", pattern="^(excellent|good|fair|poor)$")
    location: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    farm_id: int


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    equipment_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    status: Optional[str] = None
    condition: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None


class EquipmentInDB(EquipmentBase, TimestampMixin, BaseSchema):
    id: int
    farm_id: int


class EquipmentResponse(EquipmentInDB):
    farm_name: Optional[str] = None
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None


class EquipmentListResponse(BaseModel):
    items: List[EquipmentResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class MaintenanceRecord(BaseModel):
    equipment_id: int
    maintenance_type: str
    description: str
    cost: Optional[float] = None
    performed_by: Optional[str] = None
    performed_at: datetime


__all__ = ['EquipmentBase', 'EquipmentCreate', 'EquipmentUpdate', 'EquipmentInDB', 'EquipmentResponse', 'EquipmentListResponse', 'MaintenanceRecord']
