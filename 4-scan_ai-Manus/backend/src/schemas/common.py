"""
FILE: backend/src/schemas/common.py
PURPOSE: Common Pydantic schemas and base classes
OWNER: Backend Team
LAST-AUDITED: 2026-01-19

Version: 1.0.0
"""

from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    
    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(default=None, description="Sort field")
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str
    message_ar: Optional[str] = None


class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool = False
    error: str
    error_ar: Optional[str] = None
    details: Optional[dict] = None


class DeleteResponse(BaseModel):
    """Delete operation response"""
    success: bool = True
    message: str = "Successfully deleted"
    deleted_id: int


class BulkDeleteResponse(BaseModel):
    """Bulk delete operation response"""
    success: bool = True
    deleted_count: int
    deleted_ids: List[int]


class StatusUpdate(BaseModel):
    """Status update request"""
    status: str
    reason: Optional[str] = None


class SearchParams(BaseModel):
    """Search parameters"""
    query: str = Field(..., min_length=1, max_length=200)
    fields: Optional[List[str]] = None
    exact_match: bool = False


class DateRangeFilter(BaseModel):
    """Date range filter"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class LocationFilter(BaseModel):
    """Location filter for geo queries"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=10, ge=0, le=500)


__all__ = [
    'BaseSchema',
    'TimestampMixin',
    'PaginationParams',
    'PaginatedResponse',
    'SuccessResponse',
    'ErrorResponse',
    'DeleteResponse',
    'BulkDeleteResponse',
    'StatusUpdate',
    'SearchParams',
    'DateRangeFilter',
    'LocationFilter',
]
