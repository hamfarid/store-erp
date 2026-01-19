"""
FILE: backend/src/api/v1/breeding.py | PURPOSE: Breeding API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Breeding Programs Management API Routes

Handles CRUD operations for breeding programs.

Version: 1.1.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.breeding import BreedingProgram
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/breeding", tags=["breeding"])


# Pydantic Schemas
class BreedingProgramCreate(BaseModel):
    name: str
    description: Optional[str] = None
    crop_type: str
    objective: str
    method: str  # hybridization, selection, mutation, tissue_culture, marker_assisted
    status: str = "planning"  # planning, in_progress, testing, completed, cancelled
    farm_id: Optional[int] = None
    start_date: Optional[datetime] = None
    expected_end_date: Optional[datetime] = None
    parent_varieties: Optional[str] = None
    target_traits: Optional[str] = None
    notes: Optional[str] = None


class BreedingProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    crop_type: Optional[str] = None
    objective: Optional[str] = None
    method: Optional[str] = None
    status: Optional[str] = None
    farm_id: Optional[int] = None
    start_date: Optional[datetime] = None
    expected_end_date: Optional[datetime] = None
    parent_varieties: Optional[str] = None
    target_traits: Optional[str] = None
    notes: Optional[str] = None
    progress: Optional[int] = Field(None, ge=0, le=100)


class BreedingProgramResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    crop_type: str
    objective: str
    method: str
    status: str
    user_id: int
    farm_id: Optional[int] = None
    start_date: Optional[datetime] = None
    expected_end_date: Optional[datetime] = None
    parent_varieties: Optional[str] = None
    target_traits: Optional[str] = None
    notes: Optional[str] = None
    progress: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BreedingListResponse(BaseModel):
    success: bool = True
    data: List[BreedingProgramResponse]
    total: int


# Routes
@router.get("", response_model=BreedingListResponse)
async def get_breeding_programs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    crop_type: Optional[str] = None,
    method: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of breeding programs with pagination and filtering"""
    query = db.query(BreedingProgram).filter(BreedingProgram.deleted_at.is_(None))

    # Filter by current user's programs (unless admin)
    if current_user.role != "ADMIN":
        query = query.filter(BreedingProgram.user_id == current_user.id)

    # Apply filters
    if status:
        query = query.filter(BreedingProgram.status == status)

    if crop_type:
        query = query.filter(BreedingProgram.crop_type == crop_type)

    if method:
        query = query.filter(BreedingProgram.method == method)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                BreedingProgram.name.ilike(search_term),
                BreedingProgram.description.ilike(search_term),
                BreedingProgram.objective.ilike(search_term)
            )
        )

    total = query.count()
    programs = query.order_by(BreedingProgram.created_at.desc()).offset(skip).limit(limit).all()

    return BreedingListResponse(success=True, data=programs, total=total)


@router.get("/{program_id}", response_model=BreedingProgramResponse)
async def get_breeding_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get breeding program by ID"""
    query = db.query(BreedingProgram).filter(
        BreedingProgram.id == program_id,
        BreedingProgram.deleted_at.is_(None)
    )

    # Filter by ownership unless admin
    if current_user.role != "ADMIN":
        query = query.filter(BreedingProgram.user_id == current_user.id)

    program = query.first()

    if not program:
        raise HTTPException(status_code=404, detail="Breeding program not found")

    return program


@router.post("", response_model=BreedingProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_breeding_program(
    program_data: BreedingProgramCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new breeding program"""
    new_program = BreedingProgram(
        name=program_data.name,
        description=program_data.description,
        crop_type=program_data.crop_type,
        objective=program_data.objective,
        method=program_data.method,
        status=program_data.status,
        user_id=current_user.id,
        farm_id=program_data.farm_id,
        start_date=program_data.start_date,
        expected_end_date=program_data.expected_end_date,
        parent_varieties=program_data.parent_varieties,
        target_traits=program_data.target_traits,
        notes=program_data.notes,
        progress=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_program)
    db.commit()
    db.refresh(new_program)

    return new_program


@router.put("/{program_id}", response_model=BreedingProgramResponse)
async def update_breeding_program(
    program_id: int,
    program_data: BreedingProgramUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update breeding program"""
    query = db.query(BreedingProgram).filter(
        BreedingProgram.id == program_id,
        BreedingProgram.deleted_at.is_(None)
    )

    # Filter by ownership unless admin
    if current_user.role != "ADMIN":
        query = query.filter(BreedingProgram.user_id == current_user.id)

    program = query.first()

    if not program:
        raise HTTPException(status_code=404, detail="Breeding program not found")

    # Update fields
    update_data = program_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(program, field, value)

    program.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(program)

    return program


@router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_breeding_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete breeding program (soft delete)"""
    query = db.query(BreedingProgram).filter(
        BreedingProgram.id == program_id,
        BreedingProgram.deleted_at.is_(None)
    )

    # Filter by ownership unless admin
    if current_user.role != "ADMIN":
        query = query.filter(BreedingProgram.user_id == current_user.id)

    program = query.first()

    if not program:
        raise HTTPException(status_code=404, detail="Breeding program not found")

    program.deleted_at = datetime.utcnow()
    program.updated_at = datetime.utcnow()

    db.commit()

    return None
