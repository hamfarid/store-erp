"""
FILE: backend/src/api/v1/farms.py | PURPOSE: Farm management API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Farm Management API Routes

Handles CRUD operations for farms.

Version: 1.1.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.farm import Farm
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/farms", tags=["farms"])


# Pydantic Schemas
class FarmCreate(BaseModel):
    name: str
    location: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area: float
    area_unit: str = "hectare"
    crop_type: Optional[str] = None
    soil_type: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class FarmUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area: Optional[float] = None
    area_unit: Optional[str] = None
    crop_type: Optional[str] = None
    soil_type: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[str] = None


class FarmResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    location: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area: float
    area_unit: str
    crop_type: Optional[str] = None
    soil_type: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    is_active: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FarmListResponse(BaseModel):
    success: bool = True
    data: List[FarmResponse]
    total: int


class FarmStatsResponse(BaseModel):
    total_area: float
    crops_count: int
    sensors_count: int
    diagnoses_count: int
    active_alerts: int


# Routes
@router.get("", response_model=FarmListResponse)
async def list_farms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    crop_type: Optional[str] = None,
    soil_type: Optional[str] = None,
    is_active: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all farms for current user with filtering"""
    query = db.query(Farm).filter(Farm.deleted_at.is_(None))

    # Filter by owner unless admin
    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    # Apply filters
    if crop_type:
        query = query.filter(Farm.crop_type == crop_type)

    if soil_type:
        query = query.filter(Farm.soil_type == soil_type)

    if is_active:
        query = query.filter(Farm.is_active == is_active)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Farm.name.ilike(search_term),
                Farm.location.ilike(search_term),
                Farm.description.ilike(search_term)
            )
        )

    total = query.count()
    farms = query.order_by(Farm.name).offset(skip).limit(limit).all()

    return FarmListResponse(success=True, data=farms, total=total)


@router.get("/{farm_id}", response_model=FarmResponse)
async def get_farm(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific farm"""
    query = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.deleted_at.is_(None)
    )

    # Filter by owner unless admin
    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    farm = query.first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    return farm


@router.post("", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
async def create_farm(
    farm_data: FarmCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new farm"""
    new_farm = Farm(
        owner_id=current_user.id,
        name=farm_data.name,
        location=farm_data.location,
        address=farm_data.address,
        latitude=farm_data.latitude,
        longitude=farm_data.longitude,
        area=farm_data.area,
        area_unit=farm_data.area_unit,
        crop_type=farm_data.crop_type,
        soil_type=farm_data.soil_type,
        description=farm_data.description,
        notes=farm_data.notes,
        is_active="active",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm


@router.put("/{farm_id}", response_model=FarmResponse)
async def update_farm(
    farm_id: int,
    farm_data: FarmUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a farm"""
    query = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.deleted_at.is_(None)
    )

    # Filter by owner unless admin
    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    farm = query.first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    # Update fields
    update_data = farm_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(farm, field, value)

    farm.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(farm)

    return farm


@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_farm(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a farm (soft delete)"""
    query = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.deleted_at.is_(None)
    )

    # Filter by owner unless admin
    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    farm = query.first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    farm.deleted_at = datetime.utcnow()
    farm.updated_at = datetime.utcnow()

    db.commit()

    return None


@router.get("/{farm_id}/stats", response_model=FarmStatsResponse)
async def get_farm_stats(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get farm statistics"""
    query = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.deleted_at.is_(None)
    )

    # Filter by owner unless admin
    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    farm = query.first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    # TODO: Calculate actual stats from related tables
    return FarmStatsResponse(
        total_area=farm.area,
        crops_count=0,
        sensors_count=0,
        diagnoses_count=0,
        active_alerts=0
    )
