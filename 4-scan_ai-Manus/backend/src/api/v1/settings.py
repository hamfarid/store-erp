"""
Settings API Endpoints
======================

User preferences and application settings management.

@author Global System v35.0
@date 2026-01-19
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from ...core.database import get_db
from ...models.user import User
from .auth import get_current_user

router = APIRouter(prefix="/settings", tags=["Settings"])


# ==================
# Schemas
# ==================

class UserPreferences(BaseModel):
    """User preferences schema"""
    language: Optional[str] = Field(None, description="Preferred language (en/ar)")
    theme: Optional[str] = Field(None, description="UI theme (light/dark/system)")
    timezone: Optional[str] = Field(None, description="User timezone")
    date_format: Optional[str] = Field(None, description="Date format preference")
    measurement_unit: Optional[str] = Field(None, description="Measurement unit (metric/imperial)")


class NotificationSettings(BaseModel):
    """Notification settings schema"""
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    disease_alerts: Optional[bool] = True
    weather_alerts: Optional[bool] = True
    report_reminders: Optional[bool] = True
    marketing_emails: Optional[bool] = False
    weekly_digest: Optional[bool] = True


class SecuritySettings(BaseModel):
    """Security settings schema"""
    two_factor_enabled: Optional[bool] = False
    session_timeout: Optional[int] = Field(30, description="Session timeout in minutes")
    login_notifications: Optional[bool] = True


class SettingsResponse(BaseModel):
    """Complete settings response"""
    preferences: UserPreferences
    notifications: NotificationSettings
    security: SecuritySettings


class SettingsUpdate(BaseModel):
    """Settings update schema"""
    preferences: Optional[UserPreferences] = None
    notifications: Optional[NotificationSettings] = None
    security: Optional[SecuritySettings] = None


# ==================
# Endpoints
# ==================

@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all user settings
    """
    # Get user preferences from database or return defaults
    preferences = UserPreferences(
        language=getattr(current_user, 'language', 'en'),
        theme=getattr(current_user, 'theme', 'light'),
        timezone=getattr(current_user, 'timezone', 'UTC'),
        date_format=getattr(current_user, 'date_format', 'YYYY-MM-DD'),
        measurement_unit=getattr(current_user, 'measurement_unit', 'metric')
    )
    
    notifications = NotificationSettings(
        email_notifications=getattr(current_user, 'email_notifications', True),
        push_notifications=getattr(current_user, 'push_notifications', True),
        disease_alerts=getattr(current_user, 'disease_alerts', True),
        weather_alerts=getattr(current_user, 'weather_alerts', True),
        report_reminders=getattr(current_user, 'report_reminders', True),
        marketing_emails=getattr(current_user, 'marketing_emails', False),
        weekly_digest=getattr(current_user, 'weekly_digest', True)
    )
    
    security = SecuritySettings(
        two_factor_enabled=getattr(current_user, 'two_factor_enabled', False),
        session_timeout=getattr(current_user, 'session_timeout', 30),
        login_notifications=getattr(current_user, 'login_notifications', True)
    )
    
    return SettingsResponse(
        preferences=preferences,
        notifications=notifications,
        security=security
    )


@router.patch("", response_model=SettingsResponse)
async def update_settings(
    settings: SettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user settings
    """
    # Update preferences
    if settings.preferences:
        for key, value in settings.preferences.dict(exclude_unset=True).items():
            if hasattr(current_user, key):
                setattr(current_user, key, value)
    
    # Update notifications
    if settings.notifications:
        for key, value in settings.notifications.dict(exclude_unset=True).items():
            if hasattr(current_user, key):
                setattr(current_user, key, value)
    
    # Update security
    if settings.security:
        for key, value in settings.security.dict(exclude_unset=True).items():
            if hasattr(current_user, key):
                setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    # Return updated settings
    return await get_settings(current_user, db)


@router.get("/notifications", response_model=NotificationSettings)
async def get_notification_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get notification settings only
    """
    return NotificationSettings(
        email_notifications=getattr(current_user, 'email_notifications', True),
        push_notifications=getattr(current_user, 'push_notifications', True),
        disease_alerts=getattr(current_user, 'disease_alerts', True),
        weather_alerts=getattr(current_user, 'weather_alerts', True),
        report_reminders=getattr(current_user, 'report_reminders', True),
        marketing_emails=getattr(current_user, 'marketing_emails', False),
        weekly_digest=getattr(current_user, 'weekly_digest', True)
    )


@router.patch("/notifications", response_model=NotificationSettings)
async def update_notification_settings(
    settings: NotificationSettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update notification settings
    """
    for key, value in settings.dict(exclude_unset=True).items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return await get_notification_settings(current_user, db)


@router.get("/preferences", response_model=UserPreferences)
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user preferences only
    """
    return UserPreferences(
        language=getattr(current_user, 'language', 'en'),
        theme=getattr(current_user, 'theme', 'light'),
        timezone=getattr(current_user, 'timezone', 'UTC'),
        date_format=getattr(current_user, 'date_format', 'YYYY-MM-DD'),
        measurement_unit=getattr(current_user, 'measurement_unit', 'metric')
    )


@router.patch("/preferences", response_model=UserPreferences)
async def update_user_preferences(
    preferences: UserPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user preferences
    """
    for key, value in preferences.dict(exclude_unset=True).items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return await get_user_preferences(current_user, db)


@router.get("/security", response_model=SecuritySettings)
async def get_security_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get security settings only
    """
    return SecuritySettings(
        two_factor_enabled=getattr(current_user, 'two_factor_enabled', False),
        session_timeout=getattr(current_user, 'session_timeout', 30),
        login_notifications=getattr(current_user, 'login_notifications', True)
    )


@router.patch("/security", response_model=SecuritySettings)
async def update_security_settings(
    settings: SecuritySettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update security settings
    """
    for key, value in settings.dict(exclude_unset=True).items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return await get_security_settings(current_user, db)
