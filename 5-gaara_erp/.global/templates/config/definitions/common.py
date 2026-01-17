"""
File: config/definitions/common.py
Common definitions used across the entire project

This file contains general-purpose enums, types, and classes
that are used throughout the application.
"""

from enum import Enum
from typing import TypedDict, Literal, Any


# ============================================================================
# Status Enums
# ============================================================================

class Status(str, Enum):
    """General status enum for entities"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"
    ARCHIVED = "archived"


class UserRole(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"
    VIEWER = "viewer"


class Environment(str, Enum):
    """Application environment"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


# ============================================================================
# Response Types
# ============================================================================

class APIResponse(TypedDict):
    """Standard API response structure"""
    success: bool
    message: str
    data: dict[str, Any] | list[Any] | None
    errors: list[str] | None
    timestamp: str


class ErrorResponse(TypedDict):
    """Standard error response structure"""
    success: bool
    message: str
    error_code: str
    error_id: str | None
    details: dict[str, Any] | None


class PaginatedResponse(TypedDict):
    """Paginated response structure"""
    success: bool
    data: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# Common Types
# ============================================================================

HTTPMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
SortOrder = Literal["asc", "desc"]
DateFormat = Literal["ISO", "US", "EU", "UNIX"]


# ============================================================================
# Constants
# ============================================================================

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1

# Date formats
ISO_DATE_FORMAT = "%Y-%m-%d"
ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
US_DATE_FORMAT = "%m/%d/%Y"
EU_DATE_FORMAT = "%d/%m/%Y"


# ============================================================================
# Validation Constants
# ============================================================================

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50

# Email regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Phone regex pattern (international)
PHONE_REGEX = r'^\+?[1-9]\d{1,14}$'


# ============================================================================
# Export all
# ============================================================================

__all__ = [
    # Enums
    'Status',
    'UserRole',
    'Environment',
    # Response Types
    'APIResponse',
    'ErrorResponse',
    'PaginatedResponse',
    # Types
    'HTTPMethod',
    'SortOrder',
    'DateFormat',
    # Constants
    'DEFAULT_PAGE_SIZE',
    'MAX_PAGE_SIZE',
    'MIN_PAGE_SIZE',
    'ISO_DATE_FORMAT',
    'ISO_DATETIME_FORMAT',
    'US_DATE_FORMAT',
    'EU_DATE_FORMAT',
    'MIN_PASSWORD_LENGTH',
    'MAX_PASSWORD_LENGTH',
    'MIN_USERNAME_LENGTH',
    'MAX_USERNAME_LENGTH',
    'EMAIL_REGEX',
    'PHONE_REGEX',
]
