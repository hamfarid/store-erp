# FILE: backend/src/validators/user_validators.py
# PURPOSE: Pydantic validators for Users module
# OWNER: Gaara Store Team
# RELATED: contracts/openapi.yaml, backend/src/models/user.py
# LAST-AUDITED: 2025-10-27

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration"""

    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """User status enumeration"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class UserCreateRequest(BaseModel):
    """Request to create a new user"""

    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=8, max_length=100, description="User password (min 8 chars)"
    )
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(
        None, pattern=r"^\+?[1-9]\d{1,14}$", description="Phone number"
    )
    role: UserRole = Field(default=UserRole.STAFF, description="User role")
    is_active: bool = Field(default=True, description="Is user active")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@gaaragroup.com",
                "password": "SecurePassword123!",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+966501234567",
                "role": "staff",
                "is_active": True,
            }
        }


class UserUpdateRequest(BaseModel):
    """Request to update a user"""

    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.updated@gaaragroup.com",
                "phone": "+966501234567",
                "role": "manager",
            }
        }


class UserPasswordChangeRequest(BaseModel):
    """Request to change user password"""

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ..., min_length=8, max_length=100, description="New password"
    )
    confirm_password: str = Field(..., description="Confirm new password")

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "OldPassword123!",
                "new_password": "NewPassword456!",
                "confirm_password": "NewPassword456!",
            }
        }


class UserResponse(BaseModel):
    """User response"""

    id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    phone: Optional[str] = Field(None, description="Phone number")
    role: UserRole = Field(..., description="User role")
    status: UserStatus = Field(..., description="User status")
    is_active: bool = Field(..., description="Is user active")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "usr_123456",
                "username": "john_doe",
                "email": "john@gaaragroup.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+966501234567",
                "role": "staff",
                "status": "active",
                "is_active": True,
                "last_login": "2025-01-15T10:30:00Z",
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-15T15:30:00Z",
            }
        }


class UserListResponse(BaseModel):
    """List of users response"""

    success: bool = Field(default=True)
    message: str = Field(default="Users retrieved successfully")
    traceId: str = Field(..., description="Trace ID for debugging")
    data: Optional[dict] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Users retrieved successfully",
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


class UserPermissionRequest(BaseModel):
    """Request to update user permissions"""

    permissions: List[str] = Field(..., description="List of permission codes")

    class Config:
        json_schema_extra = {
            "example": {
                "permissions": ["products.read", "products.create", "products.update"]
            }
        }


class UserRoleChangeRequest(BaseModel):
    """Request to change user role"""

    role: UserRole = Field(..., description="New user role")
    reason: Optional[str] = Field(
        None, max_length=500, description="Reason for role change"
    )

    class Config:
        json_schema_extra = {
            "example": {"role": "manager", "reason": "Promotion to team lead"}
        }
