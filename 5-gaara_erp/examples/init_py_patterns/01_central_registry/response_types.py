"""Response type definitions"""

from typing import TypedDict, Any


class APIResponse(TypedDict):
    """Standard API response"""
    success: bool
    message: str
    data: dict[str, Any] | list[Any] | None


class ErrorResponse(TypedDict):
    """Error response"""
    success: bool
    message: str
    error_code: str
    details: dict[str, Any] | None


class PaginatedResponse(TypedDict):
    """Paginated response"""
    success: bool
    data: list[Any]
    total: int
    page: int
    page_size: int

