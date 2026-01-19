"""
FILE: backend/src/api/v1/crops.py | PURPOSE: Crops API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Crops Management API Routes

Handles CRUD operations for crops.

Version: 1.1.0
"""

import json
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.crop import Crop
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/crops", tags=["crops"])


# Pydantic Schemas
class CropCreate(BaseModel):
    name: str
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    category: str  # vegetables, fruits, grains, herbs, trees, flowers
    growing_season: Optional[str] = None
    water_needs: str = "medium"  # low, medium, high
    sunlight_needs: str = "full"  # full, partial, shade
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    growth_duration: Optional[int] = None  # days
    description: Optional[str] = None
    care_tips: Optional[str] = None
    common_diseases: Optional[List[str]] = None
    image_url: Optional[str] = None


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
    common_diseases: Optional[List[str]] = None
    image_url: Optional[str] = None


class CropResponse(BaseModel):
    id: int
    name: str
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    category: str
    growing_season: Optional[str] = None
    water_needs: str
    sunlight_needs: str
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    growth_duration: Optional[int] = None
    description: Optional[str] = None
    care_tips: Optional[str] = None
    common_diseases: Optional[List[str]] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CropListResponse(BaseModel):
    success: bool = True
    data: List[CropResponse]
    total: int


# Helper function to parse common_diseases
def parse_diseases(diseases_str: Optional[str]) -> Optional[List[str]]:
    if not diseases_str:
        return None
    try:
        return json.loads(diseases_str)
    except json.JSONDecodeError:
        return diseases_str.split(",") if diseases_str else None


# Routes
@router.get("", response_model=CropListResponse)
async def get_crops(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    search: Optional[str] = None,
    water_needs: Optional[str] = None,
    sunlight_needs: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of crops with pagination and filtering"""
    query = db.query(Crop).filter(Crop.deleted_at.is_(None))

    # Apply filters
    if category:
        query = query.filter(Crop.category == category)

    if water_needs:
        query = query.filter(Crop.water_needs == water_needs)

    if sunlight_needs:
        query = query.filter(Crop.sunlight_needs == sunlight_needs)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Crop.name.ilike(search_term),
                Crop.name_en.ilike(search_term),
                Crop.scientific_name.ilike(search_term),
                Crop.description.ilike(search_term)
            )
        )

    total = query.count()
    crops = query.order_by(Crop.name).offset(skip).limit(limit).all()

    # Convert to response format with parsed diseases
    response_crops = []
    for crop in crops:
        crop_dict = {
            "id": crop.id,
            "name": crop.name,
            "name_en": crop.name_en,
            "scientific_name": crop.scientific_name,
            "category": crop.category,
            "growing_season": crop.growing_season,
            "water_needs": crop.water_needs,
            "sunlight_needs": crop.sunlight_needs,
            "temperature_min": crop.temperature_min,
            "temperature_max": crop.temperature_max,
            "growth_duration": crop.growth_duration,
            "description": crop.description,
            "care_tips": crop.care_tips,
            "common_diseases": parse_diseases(crop.common_diseases),
            "image_url": crop.image_url,
            "created_at": crop.created_at,
            "updated_at": crop.updated_at
        }
        response_crops.append(CropResponse(**crop_dict))

    return CropListResponse(success=True, data=response_crops, total=total)


@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get crop by ID"""
    crop = db.query(Crop).filter(
        Crop.id == crop_id,
        Crop.deleted_at.is_(None)
    ).first()

    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    # Parse common_diseases
    crop_dict = {
        "id": crop.id,
        "name": crop.name,
        "name_en": crop.name_en,
        "scientific_name": crop.scientific_name,
        "category": crop.category,
        "growing_season": crop.growing_season,
        "water_needs": crop.water_needs,
        "sunlight_needs": crop.sunlight_needs,
        "temperature_min": crop.temperature_min,
        "temperature_max": crop.temperature_max,
        "growth_duration": crop.growth_duration,
        "description": crop.description,
        "care_tips": crop.care_tips,
        "common_diseases": parse_diseases(crop.common_diseases),
        "image_url": crop.image_url,
        "created_at": crop.created_at,
        "updated_at": crop.updated_at
    }

    return CropResponse(**crop_dict)


@router.post("", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
async def create_crop(
    crop_data: CropCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new crop"""
    # Convert common_diseases list to JSON string
    diseases_str = None
    if crop_data.common_diseases:
        diseases_str = json.dumps(crop_data.common_diseases)

    new_crop = Crop(
        name=crop_data.name,
        name_en=crop_data.name_en,
        scientific_name=crop_data.scientific_name,
        category=crop_data.category,
        growing_season=crop_data.growing_season,
        water_needs=crop_data.water_needs,
        sunlight_needs=crop_data.sunlight_needs,
        temperature_min=crop_data.temperature_min,
        temperature_max=crop_data.temperature_max,
        growth_duration=crop_data.growth_duration,
        description=crop_data.description,
        care_tips=crop_data.care_tips,
        common_diseases=diseases_str,
        image_url=crop_data.image_url,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)

    # Return with parsed diseases
    return CropResponse(
        id=new_crop.id,
        name=new_crop.name,
        name_en=new_crop.name_en,
        scientific_name=new_crop.scientific_name,
        category=new_crop.category,
        growing_season=new_crop.growing_season,
        water_needs=new_crop.water_needs,
        sunlight_needs=new_crop.sunlight_needs,
        temperature_min=new_crop.temperature_min,
        temperature_max=new_crop.temperature_max,
        growth_duration=new_crop.growth_duration,
        description=new_crop.description,
        care_tips=new_crop.care_tips,
        common_diseases=crop_data.common_diseases,
        image_url=new_crop.image_url,
        created_at=new_crop.created_at,
        updated_at=new_crop.updated_at
    )


@router.put("/{crop_id}", response_model=CropResponse)
async def update_crop(
    crop_id: int,
    crop_data: CropUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update crop"""
    crop = db.query(Crop).filter(
        Crop.id == crop_id,
        Crop.deleted_at.is_(None)
    ).first()

    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    # Update fields
    update_data = crop_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "common_diseases" and value is not None:
            value = json.dumps(value)
        setattr(crop, field, value)

    crop.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(crop)

    # Return with parsed diseases
    return CropResponse(
        id=crop.id,
        name=crop.name,
        name_en=crop.name_en,
        scientific_name=crop.scientific_name,
        category=crop.category,
        growing_season=crop.growing_season,
        water_needs=crop.water_needs,
        sunlight_needs=crop.sunlight_needs,
        temperature_min=crop.temperature_min,
        temperature_max=crop.temperature_max,
        growth_duration=crop.growth_duration,
        description=crop.description,
        care_tips=crop.care_tips,
        common_diseases=parse_diseases(crop.common_diseases),
        image_url=crop.image_url,
        created_at=crop.created_at,
        updated_at=crop.updated_at
    )


@router.delete("/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete crop (soft delete)"""
    crop = db.query(Crop).filter(
        Crop.id == crop_id,
        Crop.deleted_at.is_(None)
    ).first()

    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    crop.deleted_at = datetime.utcnow()
    crop.updated_at = datetime.utcnow()

    db.commit()

    return None
