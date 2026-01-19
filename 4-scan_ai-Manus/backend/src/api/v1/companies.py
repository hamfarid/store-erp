"""
FILE: backend/src/api/v1/companies.py | PURPOSE: Companies API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Companies Management API Routes

Handles CRUD operations for companies.

Version: 1.1.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.company import Company
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/companies", tags=["companies"])


# Pydantic Schemas
class CompanyCreate(BaseModel):
    name: str
    name_en: Optional[str] = None
    type: str  # farm, supplier, distributor, research, government, other
    industry: Optional[str] = None
    registration_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: str = "Saudi Arabia"
    description: Optional[str] = None
    employees_count: Optional[int] = None
    founded_year: Optional[int] = None
    logo_url: Optional[str] = None


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    type: Optional[str] = None
    industry: Optional[str] = None
    registration_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    employees_count: Optional[int] = None
    founded_year: Optional[int] = None
    logo_url: Optional[str] = None
    status: Optional[str] = None  # active, inactive, pending


class CompanyResponse(BaseModel):
    id: int
    name: str
    name_en: Optional[str] = None
    type: str
    industry: Optional[str] = None
    registration_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: str
    description: Optional[str] = None
    employees_count: Optional[int] = None
    founded_year: Optional[int] = None
    logo_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyListResponse(BaseModel):
    success: bool = True
    data: List[CompanyResponse]
    total: int


# Routes
@router.get("", response_model=CompanyListResponse)
async def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    type: Optional[str] = None,
    status: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of companies with pagination and filtering"""
    query = db.query(Company).filter(Company.deleted_at.is_(None))

    # Apply filters
    if type:
        query = query.filter(Company.type == type)

    if status:
        query = query.filter(Company.status == status)

    if city:
        query = query.filter(Company.city == city)

    if country:
        query = query.filter(Company.country == country)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Company.name.ilike(search_term),
                Company.name_en.ilike(search_term),
                Company.description.ilike(search_term),
                Company.registration_number.ilike(search_term)
            )
        )

    total = query.count()
    companies = query.order_by(Company.name).offset(skip).limit(limit).all()

    return CompanyListResponse(success=True, data=companies, total=total)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get company by ID"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    ).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company"""
    # Check for duplicate registration number
    if company_data.registration_number:
        existing = db.query(Company).filter(
            Company.registration_number == company_data.registration_number,
            Company.deleted_at.is_(None)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Company with this registration number already exists"
            )

    new_company = Company(
        name=company_data.name,
        name_en=company_data.name_en,
        type=company_data.type,
        industry=company_data.industry,
        registration_number=company_data.registration_number,
        email=company_data.email,
        phone=company_data.phone,
        website=company_data.website,
        address=company_data.address,
        city=company_data.city,
        country=company_data.country,
        description=company_data.description,
        employees_count=company_data.employees_count,
        founded_year=company_data.founded_year,
        logo_url=company_data.logo_url,
        status="active",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update company"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    ).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Check for duplicate registration number if changing it
    if company_data.registration_number and company_data.registration_number != company.registration_number:
        existing = db.query(Company).filter(
            Company.registration_number == company_data.registration_number,
            Company.id != company_id,
            Company.deleted_at.is_(None)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Company with this registration number already exists"
            )

    # Update fields
    update_data = company_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    company.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(company)

    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete company (soft delete)"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    ).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    company.deleted_at = datetime.utcnow()
    company.updated_at = datetime.utcnow()

    db.commit()

    return None
