"""
FILE: backend/src/api/v1/notifications.py | PURPOSE: Notifications API
OWNER: Backend Team | RELATED: notification.py, websocket.py | LAST-AUDITED: 2026-01-31

API endpoints for managing user notifications.
"""

import json
import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.auth import get_current_user
from src.models.user import User
from src.models.notification import Notification, NotificationType

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])


class NotificationCreate(BaseModel):
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    link: Optional[str] = None
    data: Optional[dict] = None


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    link: Optional[str]
    data: Optional[dict]
    created_at: datetime
    read_at: Optional[datetime]

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    success: bool
    data: List[NotificationResponse]
    total: int
    unread_count: int


@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    unread_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user notifications with pagination."""
    query = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.deleted_at.is_(None)
    )
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    total = query.count()
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.deleted_at.is_(None),
        Notification.is_read == False
    ).count()
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    data = []
    for n in notifications:
        data.append(NotificationResponse(
            id=n.id, title=n.title, message=n.message, type=n.type.value,
            is_read=n.is_read, link=n.link,
            data=json.loads(n.data) if n.data else None,
            created_at=n.created_at, read_at=n.read_at
        ))
    
    return NotificationListResponse(success=True, data=data, total=total, unread_count=unread_count)


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark notification as read."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"success": True, "message": "Notification marked as read"}


@router.post("/read-all")
async def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read."""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True, "read_at": datetime.utcnow()})
    db.commit()
    
    return {"success": True, "message": "All notifications marked as read"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete a notification."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"success": True, "message": "Notification deleted"}


@router.get("/unread-count")
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread notifications."""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.deleted_at.is_(None),
        Notification.is_read == False
    ).count()
    
    return {"success": True, "unread_count": count}
