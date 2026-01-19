"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/notifications/schemas.py
الوصف: مخططات البيانات لمديول الإشعارات
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from src.modules.notifications.config import (
    NOTIFICATION_CHANNELS,
    NOTIFICATION_PRIORITIES,
    NOTIFICATION_TYPES,
)

# Constants for repeated string literals
NOTIFICATION_TYPE_DESCRIPTION = "نوع الإشعار"
NOTIFICATION_CHANNELS_DESCRIPTION = "قنوات الإشعار"


class NotificationCreateSchema(BaseModel):
    """مخطط إنشاء إشعار"""

    user_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    type: str = Field(..., description=NOTIFICATION_TYPE_DESCRIPTION)
    priority: str = Field(..., description="أولوية الإشعار")
    channels: List[str] = Field(
        default_factory=list,
        description=NOTIFICATION_CHANNELS_DESCRIPTION)
    metadata: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None

    @validator('type')
    def validate_type(cls, v):
        if v not in NOTIFICATION_TYPES.values():
            raise ValueError(
                f"نوع الإشعار غير صالح. القيم المسموح بها: {', '.join(NOTIFICATION_TYPES.values())}")
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v not in NOTIFICATION_PRIORITIES.values():
            raise ValueError(
                f"أولوية الإشعار غير صالحة. القيم المسموح بها: {', '.join(NOTIFICATION_PRIORITIES.values())}")
        return v

    @validator('channels')
    def validate_channels(cls, v):
        for channel in v:
            if channel not in NOTIFICATION_CHANNELS.values():
                raise ValueError(
                    f"قناة الإشعار غير صالحة. القيم المسموح بها: {', '.join(NOTIFICATION_CHANNELS.values())}")
        return v


class NotificationSchema(NotificationCreateSchema):
    """مخطط الإشعار"""

    id: int
    is_read: bool = False
    is_archived: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NotificationChannelSchema(BaseModel):
    """مخطط قناة الإشعار"""

    id: int
    notification_id: int
    channel: str
    status: str
    sent_at: Optional[datetime] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NotificationTemplateCreateSchema(BaseModel):
    """مخطط إنشاء قالب إشعار"""

    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    subject: Optional[str] = Field(None, max_length=255)
    content_html: Optional[str] = None
    content_text: Optional[str] = None
    content_sms: Optional[str] = None
    content_push: Optional[str] = None
    variables: Optional[Dict[str, str]] = None
    is_active: bool = True


class NotificationTemplateSchema(NotificationTemplateCreateSchema):
    """مخطط قالب الإشعار"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NotificationPreferenceCreateSchema(BaseModel):
    """مخطط إنشاء تفضيلات الإشعارات"""

    user_id: int
    notification_type: str = Field(...,
                                   description=NOTIFICATION_TYPE_DESCRIPTION)
    email_enabled: bool = True
    in_app_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = False

    @validator('notification_type')
    def validate_notification_type(cls, v):
        if v not in NOTIFICATION_TYPES.values():
            raise ValueError(
                f"نوع الإشعار غير صالح. القيم المسموح بها: {', '.join(NOTIFICATION_TYPES.values())}")
        return v


class NotificationPreferenceSchema(NotificationPreferenceCreateSchema):
    """مخطط تفضيلات الإشعارات"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ScheduledNotificationCreateSchema(BaseModel):
    """مخطط إنشاء إشعار مجدول"""

    user_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    type: str = Field(..., description=NOTIFICATION_TYPE_DESCRIPTION)
    priority: str = Field(..., description="أولوية الإشعار")
    channels: List[str] = Field(...,
                                description=NOTIFICATION_CHANNELS_DESCRIPTION)
    metadata: Optional[Dict[str, Any]] = None
    scheduled_at: datetime = Field(..., description="وقت الجدولة")

    @validator('type')
    def validate_type(cls, v):
        if v not in NOTIFICATION_TYPES.values():
            raise ValueError(
                f"نوع الإشعار غير صالح. القيم المسموح بها: {', '.join(NOTIFICATION_TYPES.values())}")
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v not in NOTIFICATION_PRIORITIES.values():
            raise ValueError(
                f"أولوية الإشعار غير صالحة. القيم المسموح بها: {', '.join(NOTIFICATION_PRIORITIES.values())}")
        return v

    @validator('channels')
    def validate_channels(cls, v):
        for channel in v:
            if channel not in NOTIFICATION_CHANNELS.values():
                raise ValueError(
                    f"قناة الإشعار غير صالحة. القيم المسموح بها: {', '.join(NOTIFICATION_CHANNELS.values())}")
        return v

    @validator('scheduled_at')
    def validate_scheduled_at(cls, v):
        if v < datetime.now(timezone.utc):
            raise ValueError("وقت الجدولة يجب أن يكون في المستقبل")
        return v


class ScheduledNotificationSchema(ScheduledNotificationCreateSchema):
    """مخطط الإشعار المجدول"""

    id: int
    is_processed: bool = False
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class WebhookSubscriptionCreateSchema(BaseModel):
    """مخطط إنشاء اشتراك Webhook"""

    name: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., min_length=1, max_length=255)
    secret: Optional[str] = Field(None, max_length=255)
    events: List[str] = Field(..., description="الأحداث المشترك بها")
    is_active: bool = True


class WebhookSubscriptionSchema(WebhookSubscriptionCreateSchema):
    """مخطط اشتراك Webhook"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NotificationBulkActionSchema(BaseModel):
    """مخطط إجراء جماعي للإشعارات"""

    notification_ids: List[int] = Field(..., description="معرفات الإشعارات")
    action: str = Field(..., description="الإجراء المطلوب")

    @validator('action')
    def validate_action(cls, v):
        allowed_actions = [
            'mark_read',
            'mark_unread',
            'archive',
            'unarchive',
            'delete']
        if v not in allowed_actions:
            raise ValueError(
                f"الإجراء غير صالح. القيم المسموح بها: {', '.join(allowed_actions)}")
        return v


class NotificationFilterSchema(BaseModel):
    """مخطط تصفية الإشعارات"""

    user_id: Optional[int] = None
    type: Optional[str] = None
    priority: Optional[str] = None
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @validator('type')
    def validate_type(cls, v):
        if v and v not in NOTIFICATION_TYPES.values():
            raise ValueError(
                f"نوع الإشعار غير صالح. القيم المسموح بها: {', '.join(NOTIFICATION_TYPES.values())}")
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v and v not in NOTIFICATION_PRIORITIES.values():
            raise ValueError(
                f"أولوية الإشعار غير صالحة. القيم المسموح بها: {', '.join(NOTIFICATION_PRIORITIES.values())}")
        return v


class NotificationSendTestSchema(BaseModel):
    """مخطط إرسال إشعار اختباري"""

    template_code: str = Field(..., description="رمز القالب")
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    channels: List[str] = Field(...,
                                description=NOTIFICATION_CHANNELS_DESCRIPTION)

    @validator('channels')
    def validate_channels(cls, v):
        for channel in v:
            if channel not in NOTIFICATION_CHANNELS.values():
                raise ValueError(
                    f"قناة الإشعار غير صالحة. القيم المسموح بها: {', '.join(NOTIFICATION_CHANNELS.values())}")
        return v
