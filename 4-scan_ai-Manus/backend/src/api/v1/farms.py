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
from ...models.sensor import Sensor
from ...models.diagnosis import Diagnosis
from ...models.worker import Worker
from ...services.cache_service import get_cache
from ...utils.cache import (
    TTL_MEDIUM, build_farm_stats_key, invalidate_farm_cache,
    invalidate_list_cache, CACHE_PREFIX_FARM
)
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


FarmPartialUpdate = FarmUpdate


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


@router.get("/search", response_model=List[FarmResponse])
async def search_farms(
    query: str = Query(..., min_length=2),
    location: Optional[str] = None,
    min_area: Optional[float] = None,
    max_area: Optional[float] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search and filter farms"""
    query_obj = db.query(Farm).filter(Farm.deleted_at.is_(None))

    # Text search
    if query:
        query_obj = query_obj.filter(
            or_(
                Farm.name.ilike(f"%{query}%"),
                Farm.description.ilike(f"%{query}%")
            )
        )

    if location:
        query_obj = query_obj.filter(Farm.location.ilike(f"%{location}%"))

    if min_area:
        query_obj = query_obj.filter(Farm.area >= min_area)

    if max_area:
        query_obj = query_obj.filter(Farm.area <= max_area)

    # Permissions
    if current_user.role != "ADMIN":
        query_obj = query_obj.filter(Farm.owner_id == current_user.id)

    farms = query_obj.offset(skip).limit(limit).all()
    return farms


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



@router.patch("/{farm_id}", response_model=FarmResponse)
async def update_farm_partial(
    farm_id: int,
    farm_update: FarmPartialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Partial update of farm data"""
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
    update_data = farm_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(farm, field, value)

    farm.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(farm)

    # Invalidate cache for this farm
    await invalidate_farm_cache(farm_id)

    return farm


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

    # Invalidate cache for this farm
    await invalidate_farm_cache(farm_id)

    return farm


@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_farm(
    farm_id: int,
    permanent: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a farm (soft delete or permanent)"""
    # Use specific query depending on desired behavior
    # For permanent delete, we might want to find even soft-deleted ones?
    # The prompt implies we delete an existing farm.
    # If it's already soft deleted, 'deleted_at' is NOT None.
    # Assuming we look for active farms first.
    
    query = db.query(Farm).filter(Farm.id == farm_id)
    if not permanent:
         query = query.filter(Farm.deleted_at.is_(None))

    # Filter by owner unless admin
    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    farm = query.first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    if permanent and current_user.role == "ADMIN":
        db.delete(farm)
    else:
        if farm.deleted_at: # Already soft deleted
            # If finding soft deleted items is allowed (e.g. for permanent delete logic above if I adjusted query),
            # but here query filtered for deleted_at is None (unless modified).
            # If I want to allow permanent delete of ALREADY soft deleted items, I need to adjust the query logic.
            # But adhering to the prompt:
            # "if permanent and is_admin: db.delete(farm) else: soft delete"
            pass
        
        farm.deleted_at = datetime.utcnow()
        farm.updated_at = datetime.utcnow()

    db.commit()

    # Invalidate cache for this farm
    await invalidate_farm_cache(farm_id)

    return None


@router.get("/{farm_id}/stats", response_model=FarmStatsResponse)
async def get_farm_stats(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get farm statistics (cached for 5 minutes)"""
    # Check cache first
    cache = get_cache()
    cache_key = build_farm_stats_key(farm_id, current_user.id)
    cached = await cache.get(cache_key)
    if cached is not None:
        return FarmStatsResponse(**cached)

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

    # Calculate actual stats from related tables
    sensors_count = db.query(Sensor).filter(
        Sensor.farm_id == farm_id,
        Sensor.deleted_at.is_(None)
    ).count()

    diagnoses_count = db.query(Diagnosis).filter(
        Diagnosis.farm_id == farm_id,
        Diagnosis.deleted_at.is_(None)
    ).count()

    workers_count = db.query(Worker).filter(
        Worker.farm_id == farm_id,
        Worker.deleted_at.is_(None)
    ).count()

    # Count sensors with alert conditions (value outside thresholds)
    active_alerts = db.query(Sensor).filter(
        Sensor.farm_id == farm_id,
        Sensor.deleted_at.is_(None),
        Sensor.status == 'active',
        Sensor.value.isnot(None),
        or_(
            (Sensor.min_threshold.isnot(None)) & (
                Sensor.value < Sensor.min_threshold),
            (Sensor.max_threshold.isnot(None)) & (
                Sensor.value > Sensor.max_threshold)
        )
    ).count()

    result = FarmStatsResponse(
        total_area=farm.area,
        crops_count=workers_count,
        sensors_count=sensors_count,
        diagnoses_count=diagnoses_count,
        active_alerts=active_alerts
    )

    # Cache the result for 5 minutes
    await cache.set(cache_key, result.model_dump(), TTL_MEDIUM)

    return result
