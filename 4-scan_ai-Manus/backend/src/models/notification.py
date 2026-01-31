"""
FILE: backend/src/models/notification.py | PURPOSE: Notification model
OWNER: Backend Team | RELATED: user.py | LAST-AUDITED: 2026-01-31

Notification model for storing user notifications.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.core.database import Base


class NotificationType(str, Enum):
    """Notification types"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    ALERT = "alert"
    DIAGNOSIS = "diagnosis"
    SYSTEM = "system"


class Notification(Base):
    """Notification model for storing user notifications."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(SQLEnum(NotificationType), default=NotificationType.INFO)
    is_read = Column(Boolean, default=False, index=True)
    link = Column(String(500), nullable=True)
    data = Column(Text, nullable=True)  # JSON data
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    read_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.id}: {self.title}>"

    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.utcnow()
