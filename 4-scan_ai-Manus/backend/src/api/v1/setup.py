"""
Setup Wizard API Endpoints
==========================

Initial setup and onboarding for new users/organizations.

@author Global System v35.0
@date 2026-01-19
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import os

from ...core.database import get_db
from ...models.user import User
from ...models.company import Company
from .auth import get_current_user

router = APIRouter(prefix="/setup", tags=["Setup"])


# ==================
# Schemas
# ==================

class OrganizationSetup(BaseModel):
    """Organization setup data"""
    company_name: str = Field(..., min_length=2, max_length=100)
    company_type: str = Field(..., description="farm/cooperative/research/company/individual")
    industry: Optional[str] = "agriculture"
    employee_count: Optional[int] = None


class LocationSetup(BaseModel):
    """Location setup data"""
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    timezone: Optional[str] = "UTC"


class ProfileSetup(BaseModel):
    """Profile setup data"""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = None


class PreferencesSetup(BaseModel):
    """Preferences setup data"""
    language: str = "en"
    theme: str = "light"
    notifications: bool = True
    email_alerts: bool = True
    measurement_unit: str = "metric"


class CompleteSetupRequest(BaseModel):
    """Complete setup request"""
    # Organization
    companyName: str = Field(..., alias="companyName")
    companyType: str = Field("farm", alias="companyType")
    industry: Optional[str] = "agriculture"
    employeeCount: Optional[int] = Field(None, alias="employeeCount")
    
    # Location
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    timezone: Optional[str] = "UTC"
    
    # Profile
    firstName: str = Field(..., alias="firstName")
    lastName: str = Field(..., alias="lastName")
    phone: Optional[str] = None
    
    # Preferences
    language: str = "en"
    theme: str = "light"
    notifications: bool = True
    emailAlerts: bool = Field(True, alias="emailAlerts")
    measurementUnit: str = Field("metric", alias="measurementUnit")

    class Config:
        populate_by_name = True


class SetupStatusResponse(BaseModel):
    """Setup status response"""
    completed: bool
    current_step: Optional[str] = None
    steps_completed: list = []
    missing_steps: list = []


class SetupCompleteResponse(BaseModel):
    """Setup complete response"""
    success: bool
    message: str
    user_id: int
    company_id: Optional[int] = None


# ==================
# Endpoints
# ==================

@router.get("/status", response_model=SetupStatusResponse)
async def get_setup_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get setup wizard status for current user
    """
    steps_completed = []
    missing_steps = []
    
    # Check profile
    if current_user.first_name and current_user.last_name:
        steps_completed.append("profile")
    else:
        missing_steps.append("profile")
    
    # Check organization
    if hasattr(current_user, 'company_id') and current_user.company_id:
        steps_completed.append("organization")
    else:
        missing_steps.append("organization")
    
    # Check location
    if hasattr(current_user, 'timezone') and current_user.timezone:
        steps_completed.append("location")
    else:
        missing_steps.append("location")
    
    # Check preferences
    if hasattr(current_user, 'language') and current_user.language:
        steps_completed.append("preferences")
    else:
        missing_steps.append("preferences")
    
    completed = len(missing_steps) == 0
    current_step = missing_steps[0] if missing_steps else None
    
    return SetupStatusResponse(
        completed=completed,
        current_step=current_step,
        steps_completed=steps_completed,
        missing_steps=missing_steps
    )


@router.post("/complete", response_model=SetupCompleteResponse)
async def complete_setup(
    data: CompleteSetupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Complete the setup wizard
    """
    company_id = None
    
    try:
        # Create or update company
        if data.companyName:
            company = Company(
                name=data.companyName,
                type=data.companyType,
                industry=data.industry,
                employee_count=data.employeeCount,
                country=data.country,
                city=data.city,
                address=data.address,
                created_by=current_user.id
            )
            db.add(company)
            db.flush()
            company_id = company.id
            
            # Link user to company
            if hasattr(current_user, 'company_id'):
                current_user.company_id = company_id
        
        # Update user profile
        current_user.first_name = data.firstName
        current_user.last_name = data.lastName
        
        if data.phone and hasattr(current_user, 'phone'):
            current_user.phone = data.phone
        
        # Update location preferences
        if hasattr(current_user, 'country'):
            current_user.country = data.country
        if hasattr(current_user, 'city'):
            current_user.city = data.city
        if hasattr(current_user, 'timezone'):
            current_user.timezone = data.timezone
        
        # Update user preferences
        if hasattr(current_user, 'language'):
            current_user.language = data.language
        if hasattr(current_user, 'theme'):
            current_user.theme = data.theme
        if hasattr(current_user, 'email_notifications'):
            current_user.email_notifications = data.emailAlerts
        if hasattr(current_user, 'push_notifications'):
            current_user.push_notifications = data.notifications
        if hasattr(current_user, 'measurement_unit'):
            current_user.measurement_unit = data.measurementUnit
        
        # Mark setup as complete
        if hasattr(current_user, 'setup_completed'):
            current_user.setup_completed = True
        if hasattr(current_user, 'setup_completed_at'):
            current_user.setup_completed_at = datetime.utcnow()
        
        db.commit()
        
        return SetupCompleteResponse(
            success=True,
            message="Setup completed successfully",
            user_id=current_user.id,
            company_id=company_id
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete setup: {str(e)}"
        )


@router.post("/upload-logo")
async def upload_company_logo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload company logo during setup
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed: JPEG, PNG, GIF, WebP"
        )
    
    # Validate file size (max 5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 5MB"
        )
    
    # Save file
    upload_dir = "uploads/logos"
    os.makedirs(upload_dir, exist_ok=True)
    
    ext = file.filename.split('.')[-1] if '.' in file.filename else 'png'
    filename = f"company_{current_user.id}_{datetime.utcnow().timestamp()}.{ext}"
    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, "wb") as f:
        f.write(contents)
    
    return {
        "success": True,
        "filename": filename,
        "path": f"/uploads/logos/{filename}"
    }


@router.post("/skip")
async def skip_setup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Skip the setup wizard (can be completed later)
    """
    if hasattr(current_user, 'setup_skipped'):
        current_user.setup_skipped = True
    if hasattr(current_user, 'setup_skipped_at'):
        current_user.setup_skipped_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Setup skipped. You can complete it later in Settings."
    }
