# FILE: backend/src/validators/supplier_validators.py
# PURPOSE: Pydantic validators for Suppliers module
# OWNER: Gaara Store Team
# RELATED: contracts/openapi.yaml, backend/src/models/supplier.py
# LAST-AUDITED: 2025-10-27

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class SupplierStatus(str, Enum):
    """Supplier status enumeration"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BLACKLISTED = "blacklisted"


class SupplierCreateRequest(BaseModel):
    """Request to create a new supplier"""

    name: str = Field(..., min_length=1, max_length=100, description="Supplier name")
    name_ar: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Supplier name in Arabic"
    )
    email: EmailStr = Field(..., description="Supplier email")
    phone: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$", description="Supplier phone")
    address: str = Field(
        ..., min_length=1, max_length=200, description="Supplier address"
    )
    city: str = Field(..., min_length=1, max_length=50, description="City")
    country: str = Field(..., min_length=1, max_length=50, description="Country")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal code")
    contact_person: str = Field(
        ..., min_length=1, max_length=100, description="Contact person name"
    )
    payment_terms: Optional[str] = Field(
        None, max_length=100, description="Payment terms"
    )
    tax_id: Optional[str] = Field(None, max_length=50, description="Tax ID")
    is_active: bool = Field(default=True, description="Is supplier active")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Tech Supplies Inc",
                "name_ar": "شركة توريد التقنية",
                "email": "contact@techsupplies.com",
                "phone": "+966501234567",
                "address": "123 Business Street",
                "city": "Riyadh",
                "country": "Saudi Arabia",
                "postal_code": "12345",
                "contact_person": "Ahmed Al-Rashid",
                "payment_terms": "Net 30",
                "tax_id": "1234567890",
                "is_active": True,
            }
        }


class SupplierUpdateRequest(BaseModel):
    """Request to update a supplier"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_ar: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    address: Optional[str] = Field(None, min_length=1, max_length=200)
    city: Optional[str] = Field(None, min_length=1, max_length=50)
    country: Optional[str] = Field(None, min_length=1, max_length=50)
    postal_code: Optional[str] = Field(None, max_length=20)
    contact_person: Optional[str] = Field(None, min_length=1, max_length=100)
    payment_terms: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {"name": "Updated Tech Supplies", "phone": "+966501234567"}
        }


class SupplierResponse(BaseModel):
    """Supplier response"""

    id: str = Field(..., description="Supplier ID")
    name: str = Field(..., description="Supplier name")
    name_ar: Optional[str] = Field(None, description="Supplier name in Arabic")
    email: str = Field(..., description="Supplier email")
    phone: str = Field(..., description="Supplier phone")
    address: str = Field(..., description="Supplier address")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")
    postal_code: Optional[str] = Field(None, description="Postal code")
    contact_person: str = Field(..., description="Contact person name")
    payment_terms: Optional[str] = Field(None, description="Payment terms")
    tax_id: Optional[str] = Field(None, description="Tax ID")
    status: SupplierStatus = Field(..., description="Supplier status")
    is_active: bool = Field(..., description="Is supplier active")
    total_orders: int = Field(default=0, description="Total orders from supplier")
    total_spent: float = Field(default=0.0, description="Total amount spent")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "sup_123456",
                "name": "Tech Supplies Inc",
                "name_ar": "شركة توريد التقنية",
                "email": "contact@techsupplies.com",
                "phone": "+966501234567",
                "address": "123 Business Street",
                "city": "Riyadh",
                "country": "Saudi Arabia",
                "postal_code": "12345",
                "contact_person": "Ahmed Al-Rashid",
                "payment_terms": "Net 30",
                "tax_id": "1234567890",
                "status": "active",
                "is_active": True,
                "total_orders": 25,
                "total_spent": 50000.00,
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-15T15:30:00Z",
            }
        }


class SupplierListResponse(BaseModel):
    """List of suppliers response"""

    success: bool = Field(default=True)
    message: str = Field(default="Suppliers retrieved successfully")
    traceId: str = Field(..., description="Trace ID for debugging")
    data: Optional[dict] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Suppliers retrieved successfully",
                "traceId": "trace_123456",
                "data": {
                    "items": [],
                    "total": 0,
                    "page": 1,
                    "per_page": 10,
                    "pages": 0,
                },
            }
        }
