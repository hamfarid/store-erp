"""
File: config/definitions/core.py
Core definitions for base models and mixins
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, Field


# ============================================================================
# Base Models
# ============================================================================

class BaseModel(PydanticBaseModel):
    """Base model for all Pydantic models"""

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True


# ============================================================================
# Mixins
# ============================================================================

class TimestampMixin(BaseModel):
    """Mixin for created_at and updated_at timestamps"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SoftDeleteMixin(BaseModel):
    """Mixin for soft delete functionality"""
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = None


class AuditMixin(BaseModel):
    """Mixin for audit trail"""
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


# ============================================================================
# Export
# ============================================================================

__all__ = [
    'BaseModel',
    'TimestampMixin',
    'SoftDeleteMixin',
    'AuditMixin',
]
