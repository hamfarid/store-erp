"""
FILE: backend/src/api/v1/equipment.py | PURPOSE: Equipment API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Equipment Management API Routes

Handles CRUD operations for equipment.

Version: 1.1.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.equipment import Equipment
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/equipment", tags=["equipment"])


# Pydantic Schemas
class EquipmentCreate(BaseModel):
    name: str
    type: str  # tractor, harvester, irrigation, sprayer, other
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    farm_id: Optional[int] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    status: str = "operational"  # operational, maintenance, out_of_service
    notes: Optional[str] = None


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    farm_id: Optional[int] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class EquipmentResponse(BaseModel):
    id: int
    name: str
    type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    farm_id: Optional[int] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EquipmentListResponse(BaseModel):
    success: bool = True
    data: List[EquipmentResponse]
    total: int


# Routes
@router.get("", response_model=EquipmentListResponse)
async def get_equipment(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    farm_id: Optional[int] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of equipment with pagination and filtering"""
    query = db.query(Equipment).filter(Equipment.deleted_at.is_(None))

    # Apply filters
    if farm_id:
        query = query.filter(Equipment.farm_id == farm_id)

    if type:
        query = query.filter(Equipment.type == type)

    if status:
        query = query.filter(Equipment.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Equipment.name.ilike(search_term),
                Equipment.brand.ilike(search_term),
                Equipment.model.ilike(search_term),
                Equipment.serial_number.ilike(search_term)
            )
        )

    total = query.count()
    equipment_list = query.order_by(Equipment.name).offset(skip).limit(limit).all()

    return EquipmentListResponse(success=True, data=equipment_list, total=total)


@router.get("/{equipment_id}", response_model=EquipmentResponse)
async def get_equipment_item(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get equipment by ID"""
    equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id,
        Equipment.deleted_at.is_(None)
    ).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment


@router.post("", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    equipment_data: EquipmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new equipment"""
    # Check for duplicate serial number
    if equipment_data.serial_number:
        existing = db.query(Equipment).filter(
            Equipment.serial_number == equipment_data.serial_number,
            Equipment.deleted_at.is_(None)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Equipment with this serial number already exists"
            )

    new_equipment = Equipment(
        name=equipment_data.name,
        type=equipment_data.type,
        brand=equipment_data.brand,
        model=equipment_data.model,
        serial_number=equipment_data.serial_number,
        farm_id=equipment_data.farm_id,
        purchase_date=equipment_data.purchase_date,
        purchase_price=equipment_data.purchase_price,
        status=equipment_data.status,
        notes=equipment_data.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)

    return new_equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
async def update_equipment(
    equipment_id: int,
    equipment_data: EquipmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update equipment"""
    equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id,
        Equipment.deleted_at.is_(None)
    ).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    # Check for duplicate serial number if changing it
    if equipment_data.serial_number and equipment_data.serial_number != equipment.serial_number:
        existing = db.query(Equipment).filter(
            Equipment.serial_number == equipment_data.serial_number,
            Equipment.id != equipment_id,
            Equipment.deleted_at.is_(None)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Equipment with this serial number already exists"
            )

    # Update fields
    update_data = equipment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(equipment, field, value)

    equipment.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(equipment)

    return equipment


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(
    equipment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete equipment (soft delete)"""
    equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id,
        Equipment.deleted_at.is_(None)
    ).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    equipment.deleted_at = datetime.utcnow()
    equipment.updated_at = datetime.utcnow()

    db.commit()

    return None
