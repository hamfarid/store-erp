# FILE: backend/src/validators/auth_validators.py | PURPOSE: Pydantic
# schemas for authentication endpoints | OWNER: Backend | RELATED:
# contracts/openapi.yaml | LAST-AUDITED: 2025-10-27

"""
Authentication Pydantic Validators

Provides schemas for authentication endpoints:
- LoginRequestSchema: Login request validation
- LoginResponseSchema: Login response validation
- RefreshRequestSchema: Token refresh request validation
- RefreshResponseSchema: Token refresh response validation
- UserSchema: User object validation
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration"""

    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class LoginRequestSchema(BaseModel):
    """
    Login request schema

    Aligned with OpenAPI spec: #/components/schemas/LoginRequest
    """

    username: str = Field(..., min_length=1, max_length=100, description="Username")
    password: str = Field(..., min_length=1, description="Password")
    mfa_code: Optional[str] = Field(
        None, pattern=r"^\d{6}$", description="TOTP code (required if MFA enabled)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123",
                "mfa_code": "123456",
            }
        }


class UserSchema(BaseModel):
    """
    User object schema

    Aligned with OpenAPI spec: #/components/schemas/User
    """

    id: int = Field(..., ge=1, description="User ID")
    username: str = Field(..., min_length=1, max_length=100, description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: str = Field(..., min_length=1, max_length=255, description="Full name")
    role: UserRole = Field(..., description="User role")
    mfa_enabled: bool = Field(False, description="MFA enabled status")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "admin",
                "email": "admin@gaaragroup.com",
                "full_name": "مدير النظام",
                "role": "admin",
                "mfa_enabled": False,
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
            }
        }


class LoginResponseDataSchema(BaseModel):
    """Login response data schema"""

    access_token: str = Field(..., description="JWT access token (15 minutes)")
    refresh_token: str = Field(..., description="JWT refresh token (7 days)")
    user: UserSchema = Field(..., description="User object")


class LoginResponseSchema(BaseModel):
    """
    Login response schema

    Aligned with OpenAPI spec: #/components/schemas/LoginResponse
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    traceId: str = Field(..., description="Request trace ID")
    data: LoginResponseDataSchema = Field(..., description="Login response data")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "data": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                    "user": {
                        "id": 1,
                        "username": "admin",
                        "email": "admin@gaaragroup.com",
                        "full_name": "مدير النظام",
                        "role": "admin",
                        "mfa_enabled": False,
                    },
                },
            }
        }


class RefreshRequestSchema(BaseModel):
    """
    Token refresh request schema

    Aligned with OpenAPI spec: #/components/schemas/RefreshRequest
    """

    refresh_token: str = Field(..., min_length=1, description="JWT refresh token")

    class Config:
        json_schema_extra = {"example": {"refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."}}


class RefreshResponseDataSchema(BaseModel):
    """Refresh response data schema"""

    access_token: str = Field(..., description="New JWT access token")


class RefreshResponseSchema(BaseModel):
    """
    Token refresh response schema

    Aligned with OpenAPI spec: #/components/schemas/RefreshResponse
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    traceId: str = Field(..., description="Request trace ID")
    data: RefreshResponseDataSchema = Field(..., description="Refresh response data")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Token refreshed successfully",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "data": {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."},
            }
        }


class UserResponseDataSchema(BaseModel):
    """User response data schema"""

    user: UserSchema = Field(..., description="User object")


class UserResponseSchema(BaseModel):
    """
    User response schema

    Aligned with OpenAPI spec: #/components/schemas/UserResponse
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    traceId: str = Field(..., description="Request trace ID")
    data: UserSchema = Field(..., description="User object")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User retrieved successfully",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "data": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@gaaragroup.com",
                    "full_name": "مدير النظام",
                    "role": "admin",
                    "mfa_enabled": False,
                },
            }
        }
