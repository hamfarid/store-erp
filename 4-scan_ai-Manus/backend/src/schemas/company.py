"""
FILE: backend/src/schemas/company.py
PURPOSE: Company Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from .common import BaseSchema, TimestampMixin


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    name_ar: Optional[str] = None
    registration_number: Optional[str] = None
    tax_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyInDB(CompanyBase, TimestampMixin, BaseSchema):
    id: int
    is_active: bool = True


class CompanyResponse(CompanyInDB):
    user_count: Optional[int] = None
    farm_count: Optional[int] = None


class CompanyListResponse(BaseModel):
    items: List[CompanyResponse]
    total: int
    page: int
    limit: int
    total_pages: int


__all__ = ['CompanyBase', 'CompanyCreate', 'CompanyUpdate', 'CompanyInDB', 'CompanyResponse', 'CompanyListResponse']
