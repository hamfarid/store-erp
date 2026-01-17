"""Model mixin definitions"""

from datetime import datetime
from typing import Optional


class TimestampMixin:
    """Mixin for created_at and updated_at"""
    created_at: datetime
    updated_at: datetime


class SoftDeleteMixin:
    """Mixin for soft delete"""
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None


class AuditMixin:
    """Mixin for audit trail"""
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

