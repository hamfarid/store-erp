"""
FILE: backend/src/api/v1/tenants.py | PURPOSE: Tenant management API
OWNER: Backend Team | LAST-AUDITED: 2026-01-31

Tenant API - Multi-tenant Management

Provides CRUD operations for tenant management (admin only).

Version: 1.0.0
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.tenant import Tenant
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])


# ============================================
# Pydantic Schemas
# ============================================

class TenantBase(BaseModel):
    """Base tenant schema"""
    name: str = Field(..., min_length=2, max_length=255)
    name_ar: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = "Saudi Arabia"
    logo_url: Optional[str] = None
    primary_color: Optional[str] = "#0F6CBD"


class TenantCreate(TenantBase):
    """Create tenant schema"""
    slug: Optional[str] = None
    plan: str = Field(default="free", pattern="^(free|pro|enterprise)$")
    max_users: int = Field(default=5, ge=1, le=1000)
    max_farms: int = Field(default=10, ge=1, le=10000)


class TenantUpdate(BaseModel):
    """Update tenant schema"""
    name: Optional[str] = None
    name_ar: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    plan: Optional[str] = None
    max_users: Optional[int] = None
    max_farms: Optional[int] = None
    is_active: Optional[bool] = None
    features: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None


class TenantResponse(BaseModel):
    """Tenant response schema"""
    id: int
    name: str
    name_ar: Optional[str]
    slug: str
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    city: Optional[str]
    country: Optional[str]
    logo_url: Optional[str]
    primary_color: Optional[str]
    plan: str
    max_users: int
    max_farms: int
    is_active: bool
    is_verified: bool
    user_count: Optional[int] = 0
    farm_count: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True


class TenantListResponse(BaseModel):
    """Tenant list response"""
    success: bool = True
    items: List[TenantResponse]
    total: int
    page: int
    limit: int


# ============================================
# Helper Functions
# ============================================

def generate_slug(name: str) -> str:
    """Generate URL-friendly slug from name"""
    slug = name.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug[:100]


def require_admin(current_user: User):
    """Require admin role for tenant management"""
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required for tenant management"
        )


# ============================================
# API Endpoints
# ============================================

@router.get("", response_model=TenantListResponse)
async def list_tenants(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    plan: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tenants (admin only)"""
    require_admin(current_user)

    query = db.query(Tenant).filter(Tenant.deleted_at.is_(None))

    if search:
        query = query.filter(
            Tenant.name.ilike(f"%{search}%") |
            Tenant.slug.ilike(f"%{search}%") |
            Tenant.email.ilike(f"%{search}%")
        )

    if plan:
        query = query.filter(Tenant.plan == plan)

    if is_active is not None:
        query = query.filter(Tenant.is_active == is_active)

    total = query.count()
    tenants = query.order_by(Tenant.created_at.desc()).offset(skip).limit(limit).all()

    return TenantListResponse(
        items=tenants,
        total=total,
        page=(skip // limit) + 1,
        limit=limit
    )


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific tenant by ID (admin only)"""
    require_admin(current_user)

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.deleted_at.is_(None)
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    # Get user and farm counts
    user_count = db.query(User).filter(
        User.tenant_id == tenant_id,
        User.deleted_at.is_(None)
    ).count()

    from ...models.farm import Farm
    farm_count = db.query(Farm).filter(
        Farm.tenant_id == tenant_id,
        Farm.deleted_at.is_(None)
    ).count()

    return TenantResponse(
        **tenant.to_dict(),
        user_count=user_count,
        farm_count=farm_count
    )


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    data: TenantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new tenant (admin only)"""
    require_admin(current_user)

    # Generate slug if not provided
    slug = data.slug or generate_slug(data.name)

    # Check if slug already exists
    existing = db.query(Tenant).filter(Tenant.slug == slug).first()
    if existing:
        # Append a number to make it unique
        base_slug = slug
        counter = 1
        while existing:
            slug = f"{base_slug}-{counter}"
            existing = db.query(Tenant).filter(Tenant.slug == slug).first()
            counter += 1

    # Create tenant
    tenant = Tenant(
        name=data.name,
        name_ar=data.name_ar,
        slug=slug,
        email=data.email,
        phone=data.phone,
        website=data.website,
        address=data.address,
        city=data.city,
        country=data.country,
        logo_url=data.logo_url,
        primary_color=data.primary_color,
        plan=data.plan,
        max_users=data.max_users,
        max_farms=data.max_farms,
        is_active=True,
        is_verified=False
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return TenantResponse(**tenant.to_dict(), user_count=0, farm_count=0)


@router.patch("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: int,
    data: TenantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a tenant (admin only)"""
    require_admin(current_user)

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.deleted_at.is_(None)
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tenant, field, value)

    tenant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(tenant)

    return TenantResponse(**tenant.to_dict())


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soft delete a tenant (admin only)"""
    require_admin(current_user)

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.deleted_at.is_(None)
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    # Soft delete
    tenant.deleted_at = datetime.utcnow()
    tenant.is_active = False
    db.commit()

    return None


@router.post("/{tenant_id}/verify", response_model=TenantResponse)
async def verify_tenant(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify a tenant (admin only)"""
    require_admin(current_user)

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.deleted_at.is_(None)
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    tenant.is_verified = True
    tenant.verified_at = datetime.utcnow()
    db.commit()
    db.refresh(tenant)

    return TenantResponse(**tenant.to_dict())


class TenantStatsResponse(BaseModel):
    """Tenant statistics response"""
    tenant_id: int
    tenant_name: str
    user_count: int
    farm_count: int
    diagnoses_this_month: int
    plan: str
    limits: Dict[str, int]
    usage_percentage: Dict[str, float]


@router.get("/{tenant_id}/stats", response_model=TenantStatsResponse)
async def get_tenant_stats(
    tenant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tenant usage statistics (admin only)"""
    require_admin(current_user)

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.deleted_at.is_(None)
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    # Count users
    user_count = db.query(User).filter(
        User.tenant_id == tenant_id,
        User.deleted_at.is_(None)
    ).count()

    # Count farms
    from ...models.farm import Farm
    farm_count = db.query(Farm).filter(
        Farm.tenant_id == tenant_id,
        Farm.deleted_at.is_(None)
    ).count()

    # Count diagnoses this month
    from ...models.diagnosis import Diagnosis
    from sqlalchemy import func
    first_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    diagnoses_count = db.query(func.count(Diagnosis.id)).join(Farm).filter(
        Farm.tenant_id == tenant_id,
        Diagnosis.created_at >= first_of_month
    ).scalar() or 0

    # Calculate usage percentages
    user_pct = (user_count / tenant.max_users * 100) if tenant.max_users else 0
    farm_pct = (farm_count / tenant.max_farms * 100) if tenant.max_farms else 0
    diag_pct = (
        diagnoses_count / tenant.max_diagnoses_per_month * 100
    ) if tenant.max_diagnoses_per_month else 0

    return TenantStatsResponse(
        tenant_id=tenant.id,
        tenant_name=tenant.name,
        user_count=user_count,
        farm_count=farm_count,
        diagnoses_this_month=diagnoses_count,
        plan=tenant.plan,
        limits={
            "max_users": tenant.max_users,
            "max_farms": tenant.max_farms,
            "max_diagnoses_per_month": tenant.max_diagnoses_per_month
        },
        usage_percentage={
            "users": round(user_pct, 1),
            "farms": round(farm_pct, 1),
            "diagnoses": round(diag_pct, 1)
        }
    )
