"""
FILE: backend/src/api/v1/sensors.py | PURPOSE: Sensors API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Sensors Management API Routes

Handles CRUD operations for IoT sensors and real-time data.

Version: 1.1.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.sensor import Sensor
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/sensors", tags=["sensors"])


# Pydantic Schemas
class SensorCreate(BaseModel):
    name: str
    type: str  # temperature, humidity, soil_moisture, light, wind, ph
    serial_number: Optional[str] = None
    farm_id: Optional[int] = None
    location: Optional[str] = None
    unit: Optional[str] = None
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    notes: Optional[str] = None


class SensorUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    unit: Optional[str] = None
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    status: Optional[str] = None  # active, inactive, maintenance
    notes: Optional[str] = None


class SensorReadingCreate(BaseModel):
    value: float
    unit: Optional[str] = None


class SensorReadingResponse(BaseModel):
    sensor_id: int
    value: float
    unit: Optional[str] = None
    timestamp: datetime


class SensorResponse(BaseModel):
    id: int
    name: str
    type: str
    serial_number: Optional[str] = None
    farm_id: Optional[int] = None
    location: Optional[str] = None
    status: str
    value: Optional[float] = None
    unit: Optional[str] = None
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    battery_level: Optional[int] = None
    last_update: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SensorListResponse(BaseModel):
    success: bool = True
    data: List[SensorResponse]
    total: int


# Routes
@router.get("", response_model=SensorListResponse)
async def get_sensors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    farm_id: Optional[int] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of sensors with pagination and filtering"""
    query = db.query(Sensor).filter(Sensor.deleted_at.is_(None))

    # Apply filters
    if farm_id:
        query = query.filter(Sensor.farm_id == farm_id)

    if type:
        query = query.filter(Sensor.type == type)

    if status:
        query = query.filter(Sensor.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Sensor.name.ilike(search_term),
                Sensor.serial_number.ilike(search_term),
                Sensor.location.ilike(search_term)
            )
        )

    total = query.count()
    sensors = query.order_by(Sensor.created_at.desc()).offset(skip).limit(limit).all()

    return SensorListResponse(success=True, data=sensors, total=total)


@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(
    sensor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sensor by ID"""
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.deleted_at.is_(None)
    ).first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    return sensor


@router.get("/{sensor_id}/readings", response_model=List[SensorReadingResponse])
async def get_sensor_readings(
    sensor_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sensor readings history"""
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.deleted_at.is_(None)
    ).first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # For now, return the current value as the only reading
    # TODO: Implement SensorReading model for historical data
    if sensor.value is not None:
        return [
            SensorReadingResponse(
                sensor_id=sensor.id,
                value=sensor.value,
                unit=sensor.unit,
                timestamp=sensor.last_update or sensor.updated_at or datetime.utcnow()
            )
        ]
    return []


@router.post("", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor(
    sensor_data: SensorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new sensor"""
    # Check for duplicate serial number
    if sensor_data.serial_number:
        existing = db.query(Sensor).filter(
            Sensor.serial_number == sensor_data.serial_number
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    new_sensor = Sensor(
        name=sensor_data.name,
        type=sensor_data.type,
        serial_number=sensor_data.serial_number,
        farm_id=sensor_data.farm_id,
        location=sensor_data.location,
        unit=sensor_data.unit,
        min_threshold=sensor_data.min_threshold,
        max_threshold=sensor_data.max_threshold,
        notes=sensor_data.notes,
        status="active",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)

    return new_sensor


@router.put("/{sensor_id}", response_model=SensorResponse)
async def update_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update sensor"""
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.deleted_at.is_(None)
    ).first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # Update fields
    update_data = sensor_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sensor, field, value)

    sensor.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(sensor)

    return sensor


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sensor(
    sensor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete sensor (soft delete)"""
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.deleted_at.is_(None)
    ).first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    sensor.deleted_at = datetime.utcnow()
    sensor.status = "inactive"
    sensor.updated_at = datetime.utcnow()

    db.commit()

    return None


@router.post("/{sensor_id}/readings", response_model=SensorReadingResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_reading(
    sensor_id: int,
    reading: SensorReadingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new sensor reading"""
    sensor = db.query(Sensor).filter(
        Sensor.id == sensor_id,
        Sensor.deleted_at.is_(None)
    ).first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # Update sensor's current value
    sensor.value = reading.value
    if reading.unit:
        sensor.unit = reading.unit
    sensor.last_update = datetime.utcnow()
    sensor.updated_at = datetime.utcnow()

    # Check thresholds and update status if needed
    if sensor.min_threshold and reading.value < sensor.min_threshold:
        sensor.status = "warning"
    elif sensor.max_threshold and reading.value > sensor.max_threshold:
        sensor.status = "warning"
    else:
        sensor.status = "active"

    db.commit()

    return SensorReadingResponse(
        sensor_id=sensor.id,
        value=reading.value,
        unit=reading.unit or sensor.unit,
        timestamp=sensor.last_update
    )
