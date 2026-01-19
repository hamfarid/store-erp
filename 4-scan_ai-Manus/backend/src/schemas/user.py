"""
FILE: backend/src/schemas/user.py
PURPOSE: User Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19

Version: 1.0.0
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from .common import BaseSchema, TimestampMixin


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    company_id: Optional[int] = None
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    language: Optional[str] = Field(None, pattern="^(ar|en)$")
    timezone: Optional[str] = None


class UserPasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserInDB(UserBase, TimestampMixin, BaseSchema):
    """User as stored in database"""
    id: int
    role: str = "user"
    is_active: bool = True
    is_verified: bool = False
    avatar_url: Optional[str] = None
    language: str = "ar"
    timezone: Optional[str] = None
    company_id: Optional[int] = None
    last_login_at: Optional[datetime] = None


class UserResponse(UserInDB):
    """User response schema (excludes sensitive data)"""
    company_name: Optional[str] = None
    farm_count: Optional[int] = None
    diagnosis_count: Optional[int] = None


class UserListResponse(BaseModel):
    """User list response"""
    items: List[UserResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class UserProfile(UserResponse):
    """Extended user profile"""
    farms: List["FarmSummary"] = []
    recent_diagnoses: List["DiagnosisSummary"] = []
    stats: "UserStats"


class UserStats(BaseModel):
    """User statistics"""
    total_farms: int = 0
    total_diagnoses: int = 0
    total_reports: int = 0
    diagnoses_this_month: int = 0
    account_age_days: int = 0


class FarmSummary(BaseModel):
    """Farm summary for user profile"""
    id: int
    name: str
    location: str
    
    class Config:
        from_attributes = True


class DiagnosisSummary(BaseModel):
    """Diagnosis summary for user profile"""
    id: int
    disease: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


UserProfile.model_rebuild()


# Admin schemas
class UserAdminUpdate(BaseModel):
    """Admin user update schema"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, pattern="^(admin|manager|user)$")
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    company_id: Optional[int] = None


class UserRoleUpdate(BaseModel):
    """Update user role"""
    role: str = Field(..., pattern="^(admin|manager|user)$")


__all__ = [
    'UserBase',
    'UserCreate',
    'UserUpdate',
    'UserPasswordChange',
    'UserInDB',
    'UserResponse',
    'UserListResponse',
    'UserProfile',
    'UserStats',
    'UserAdminUpdate',
    'UserRoleUpdate',
]
