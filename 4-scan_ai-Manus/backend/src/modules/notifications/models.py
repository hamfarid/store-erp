"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/notifications/models.py
الوصف: نماذج قاعدة البيانات لمديول الإشعارات
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.database import Base
from src.modules.notifications.config import (
    NOTIFICATION_CHANNELS,
    NOTIFICATION_PRIORITIES,
    NOTIFICATION_TYPES,
)


class Notification(Base):
    """نموذج الإشعار"""

    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(
        Enum(
            *NOTIFICATION_TYPES.values(),
            name='notification_type'),
        nullable=False)
    priority = Column(
        Enum(
            *NOTIFICATION_PRIORITIES.values(),
            name='notification_priority'),
        nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)
    expires_at = Column(DateTime, nullable=True)

    # العلاقات
    user = relationship("User", back_populates="notifications")
    channels = relationship(
        "NotificationChannel",
        back_populates="notification",
        cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type='{self.type}', is_read={self.is_read})>"


class NotificationChannel(Base):
    """نموذج قناة الإشعار"""

    __tablename__ = 'notification_channels'

    id = Column(Integer, primary_key=True)
    notification_id = Column(
        Integer,
        ForeignKey('notifications.id'),
        nullable=False)
    channel = Column(
        Enum(
            *NOTIFICATION_CHANNELS.values(),
            name='notification_channel'),
        nullable=False)
    status = Column(
        String(20),
        default='pending',
        nullable=False)  # pending, sent, failed
    sent_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)

    # العلاقات
    notification = relationship("Notification", back_populates="channels")

    def __repr__(self):
        return f"<NotificationChannel(id={self.id}, notification_id={self.notification_id}, channel='{self.channel}', status='{self.status}')>"


class NotificationTemplate(Base):
    """نموذج قالب الإشعار"""

    __tablename__ = 'notification_templates'

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(255), nullable=True)
    content_html = Column(Text, nullable=True)
    content_text = Column(Text, nullable=True)
    content_sms = Column(Text, nullable=True)
    content_push = Column(Text, nullable=True)
    variables = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)

    def __repr__(self):
        return f"<NotificationTemplate(id={self.id}, code='{self.code}', name='{self.name}')>"


class NotificationPreference(Base):
    """نموذج تفضيلات الإشعارات"""

    __tablename__ = 'notification_preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    notification_type = Column(
        Enum(
            *NOTIFICATION_TYPES.values(),
            name='notification_type'),
        nullable=False)
    email_enabled = Column(Boolean, default=True, nullable=False)
    in_app_enabled = Column(Boolean, default=True, nullable=False)
    sms_enabled = Column(Boolean, default=False, nullable=False)
    push_enabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)

    # العلاقات
    user = relationship("User", back_populates="notification_preferences")

    def __repr__(self):
        return f"<NotificationPreference(id={self.id}, user_id={self.user_id}, notification_type='{self.notification_type}')>"


class ScheduledNotification(Base):
    """نموذج الإشعار المجدول"""

    __tablename__ = 'scheduled_notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(
        Enum(
            *NOTIFICATION_TYPES.values(),
            name='notification_type'),
        nullable=False)
    priority = Column(
        Enum(
            *NOTIFICATION_PRIORITIES.values(),
            name='notification_priority'),
        nullable=False)
    channels = Column(JSON, nullable=False)  # قائمة بالقنوات المطلوبة
    metadata = Column(JSON, nullable=True)
    scheduled_at = Column(DateTime, nullable=False)
    is_processed = Column(Boolean, default=False, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)

    # العلاقات
    user = relationship("User")

    def __repr__(self):
        return f"<ScheduledNotification(id={self.id}, user_id={self.user_id}, scheduled_at='{self.scheduled_at}', is_processed={self.is_processed})>"


class WebhookSubscription(Base):
    """نموذج اشتراك Webhook"""

    __tablename__ = 'webhook_subscriptions'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    secret = Column(String(255), nullable=True)
    events = Column(JSON, nullable=False)  # قائمة بالأحداث المشترك بها
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)

    def __repr__(self):
        return f"<WebhookSubscription(id={self.id}, name='{self.name}', url='{self.url}', is_active={self.is_active})>"
