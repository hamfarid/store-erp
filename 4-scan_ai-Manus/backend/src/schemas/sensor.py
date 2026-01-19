"""
FILE: backend/src/schemas/sensor.py
PURPOSE: Sensor Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class SensorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    sensor_type: str = Field(..., pattern="^(temperature|humidity|soil_moisture|ph|light|rain|wind|pressure|other)$")
    model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str = Field(default="active", pattern="^(active|inactive|maintenance|offline)$")
    battery_level: Optional[int] = Field(None, ge=0, le=100)
    notes: Optional[str] = None


class SensorCreate(SensorBase):
    farm_id: int


class SensorUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    battery_level: Optional[int] = None
    notes: Optional[str] = None


class SensorInDB(SensorBase, TimestampMixin, BaseSchema):
    id: int
    farm_id: int


class SensorResponse(SensorInDB):
    farm_name: Optional[str] = None
    last_reading: Optional["SensorReadingResponse"] = None
    readings_count: Optional[int] = None


class SensorListResponse(BaseModel):
    items: List[SensorResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class SensorReadingBase(BaseModel):
    value: float
    unit: str = Field(..., max_length=20)
    quality: str = Field(default="good", pattern="^(good|fair|poor|invalid)$")


class SensorReadingCreate(SensorReadingBase):
    sensor_id: int


class SensorReadingResponse(SensorReadingBase, BaseSchema):
    id: int
    sensor_id: int
    recorded_at: datetime


class SensorReadingListResponse(BaseModel):
    items: List[SensorReadingResponse]
    total: int
    sensor_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SensorAlert(BaseModel):
    sensor_id: int
    sensor_name: str
    alert_type: str
    message: str
    severity: str
    value: float
    threshold: float
    created_at: datetime


__all__ = ['SensorBase', 'SensorCreate', 'SensorUpdate', 'SensorInDB', 'SensorResponse', 'SensorListResponse', 
           'SensorReadingBase', 'SensorReadingCreate', 'SensorReadingResponse', 'SensorReadingListResponse', 'SensorAlert']
