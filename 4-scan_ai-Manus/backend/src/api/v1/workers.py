"""
FILE: backend/src/api/v1/workers.py | PURPOSE: Worker management API routes | OWNER: Backend Team

Worker Management API Routes

Handles CRUD operations for farm workers.

Version: 1.0.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.worker import Worker
from ...models.farm import Farm
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/workers", tags=["workers"])


# Pydantic Schemas
class WorkerCreate(BaseModel):
    farm_id: int
    name: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None


class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    farm_id: Optional[int] = None


class WorkerResponse(BaseModel):
    id: int
    farm_id: int
    name: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkerListResponse(BaseModel):
    success: bool = True
    data: List[WorkerResponse]
    total: int


# Routes

@router.get("", response_model=WorkerListResponse)
async def list_workers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    farm_id: Optional[int] = None,
    role: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all workers with filtering"""
    query = db.query(Worker).join(Farm).filter(Worker.deleted_at.is_(None))

    # Filter ownership
    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    # Apply filters
    if farm_id:
        query = query.filter(Worker.farm_id == farm_id)
    
    if role:
        query = query.filter(Worker.role == role)
        
    if status:
        query = query.filter(Worker.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Worker.name.ilike(search_term),
                Worker.email.ilike(search_term),
                Worker.phone.ilike(search_term),
                Worker.role.ilike(search_term)
            )
        )

    total = query.count()
    workers = query.order_by(Worker.name).offset(skip).limit(limit).all()

    return WorkerListResponse(success=True, data=workers, total=total)


@router.get("/search", response_model=List[WorkerResponse])
async def search_workers(
    query: str = Query(..., min_length=2),
    farm_id: Optional[int] = None,
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Advanced search for workers"""
    query_obj = db.query(Worker).join(Farm).filter(Worker.deleted_at.is_(None))

    # Permissions
    if current_user.role != "ADMIN":
        query_obj = query_obj.filter(Farm.owner_id == current_user.id)

    # Search logic
    if query:
        query_obj = query_obj.filter(
            or_(
                Worker.name.ilike(f"%{query}%"),
                Worker.role.ilike(f"%{query}%"),
                Worker.notes.ilike(f"%{query}%")
            )
        )

    if farm_id:
        query_obj = query_obj.filter(Worker.farm_id == farm_id)

    if role:
        query_obj = query_obj.filter(Worker.role.ilike(f"%{role}%"))

    workers = query_obj.offset(skip).limit(limit).all()
    return workers


@router.get("/{worker_id}", response_model=WorkerResponse)
async def get_worker(
    worker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific worker details"""
    query = db.query(Worker).join(Farm).filter(
        Worker.id == worker_id,
        Worker.deleted_at.is_(None)
    )

    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    worker = query.first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    return worker


@router.post("", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def create_worker(
    worker_data: WorkerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new worker"""
    # Verify farm ownership
    farm = db.query(Farm).filter(
        Farm.id == worker_data.farm_id,
        Farm.deleted_at.is_(None)
    ).first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    if current_user.role != "ADMIN" and farm.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add worker to this farm")

    new_worker = Worker(
        farm_id=worker_data.farm_id,
        name=worker_data.name,
        role=worker_data.role,
        phone=worker_data.phone,
        email=worker_data.email,
        address=worker_data.address,
        status=worker_data.status,
        notes=worker_data.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)

    return new_worker


@router.patch("/{worker_id}", response_model=WorkerResponse)
async def update_worker(
    worker_id: int,
    worker_update: WorkerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update worker details"""
    query = db.query(Worker).join(Farm).filter(
        Worker.id == worker_id,
        Worker.deleted_at.is_(None)
    )

    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    worker = query.first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # If updating farm_id, verify new farm ownership
    if worker_update.farm_id is not None:
        new_farm = db.query(Farm).filter(
            Farm.id == worker_update.farm_id,
            Farm.deleted_at.is_(None)
        ).first()
        if not new_farm:
            raise HTTPException(status_code=404, detail="New farm not found")
        if current_user.role != "ADMIN" and new_farm.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized for target farm")

    update_data = worker_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(worker, field, value)

    worker.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(worker)

    return worker


@router.delete("/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(
    worker_id: int,
    permanent: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a worker (soft or permanent)"""
    query = db.query(Worker).join(Farm).filter(Worker.id == worker_id)
    
    if not permanent:
        query = query.filter(Worker.deleted_at.is_(None))

    if current_user.role != "ADMIN":
        query = query.filter(Farm.owner_id == current_user.id)

    worker = query.first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    if permanent and current_user.role == "ADMIN":
        db.delete(worker)
    else:
        worker.deleted_at = datetime.utcnow()
        worker.updated_at = datetime.utcnow()

    db.commit()
    return None
