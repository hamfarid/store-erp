"""
FILE: backend/src/api/v1/users.py | PURPOSE: Users API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Users Management API Routes

Handles CRUD operations for users.

Version: 1.1.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/users", tags=["users"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Pydantic Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role: str = "USER"  # ADMIN, MANAGER, USER, GUEST
    is_active: bool = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    mfa_enabled: bool
    avatar_url: Optional[str] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    success: bool = True
    data: List[UserResponse]
    total: int
    page: int
    per_page: int
    pages: int


# Routes
@router.get("", response_model=UserListResponse)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of users with pagination and filtering (Admin only)"""
    # Check if user is admin
    if current_user.role not in ["ADMIN", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")

    # Build query
    query = db.query(User).filter(User.deleted_at.is_(None))

    # Apply filters
    if role:
        query = query.filter(User.role == role.upper())

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.name.ilike(search_term),
                User.email.ilike(search_term),
                User.phone.ilike(search_term)
            )
        )

    # Get total count
    total = query.count()

    # Apply pagination
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

    # Calculate pagination info
    page = (skip // limit) + 1
    pages = (total + limit - 1) // limit

    return UserListResponse(
        success=True,
        data=users,
        total=total,
        page=page,
        per_page=limit,
        pages=pages
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    # Users can view their own profile, admins can view any
    if current_user.id != user_id and current_user.role not in ["ADMIN", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at.is_(None)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new user (Admin only)"""
    # Check if user is admin
    if current_user.role not in ["ADMIN", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        phone=user_data.phone,
        role=user_data.role.upper(),
        is_active=user_data.is_active,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user"""
    # Users can update their own profile, admins can update any
    if current_user.id != user_id and current_user.role not in ["ADMIN", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # Get user
    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at.is_(None)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check email uniqueness if being updated
    if user_data.email and user_data.email != user.email:
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "role" and value:
            value = value.upper()
        setattr(user, field, value)

    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user - Soft delete (Admin only)"""
    # Check if user is admin
    if current_user.role not in ["ADMIN", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")

    # Prevent self-deletion
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    # Get user
    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at.is_(None)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Soft delete
    user.deleted_at = datetime.utcnow()
    user.is_active = False
    user.updated_at = datetime.utcnow()

    db.commit()

    return None
