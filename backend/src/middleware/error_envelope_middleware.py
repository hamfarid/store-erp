"""
P1.26: Unified Error Envelope Middleware
==========================================
Provides standardized success/error response helpers for all API endpoints.
This module implements a consistent response envelope pattern with:
- Request ID tracking for debugging
- Timestamps for logging
- Structured error codes
- Support for both positional and keyword arguments
"""

import uuid
import logging
from datetime import datetime, timezone
from functools import wraps
from flask import jsonify, request, g, has_request_context

logger = logging.getLogger(__name__)


def get_request_id():
    """Get or generate a unique request ID for tracking."""
    if has_request_context():
        if not hasattr(g, "request_id"):
            g.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:8]
        return g.request_id
    return str(uuid.uuid4())[:8]


def get_timestamp():
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def success_response(data=None, message=None, status_code=200, meta=None):
    """
    Return a standardized success envelope.

    Args:
        data: Optional payload to include under "data"
        message: Optional human-readable message
        status_code: HTTP status code (default 200)
        meta: Optional metadata (pagination, timing, etc.)

    Returns:
        JSON response with structure:
        {
            "success": true,
            "status": "success",
            "data": {...},
            "message": "...",
            "meta": {...},
            "request_id": "abc123",
            "timestamp": "2025-12-01T..."
        }
    """
    response = {
        "success": True,
        "status": "success",
        "request_id": get_request_id(),
        "timestamp": get_timestamp(),
    }

    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    if meta:
        response["meta"] = meta

    return jsonify(response), status_code


def error_response(
    message=None,
    error_code=None,
    status_code=400,
    details=None,
    code=None,
    field=None,
    **_kwargs,
):
    """
    Return a standardized error envelope.

    Accepts both positional style (message, error_code, status_code, details)
    and keyword style (message=..., code=..., status_code=..., details=...).

    Args:
        message: Human-readable error message
        error_code: Error code string (e.g., "VAL_INVALID_FORMAT")
        status_code: HTTP status code (default 400)
        details: Additional error details (dict or list)
        code: Alias for error_code
        field: Field name that caused the error (for validation errors)

    Returns:
        JSON response with structure:
        {
            "success": false,
            "status": "error",
            "error": {
                "code": "ERROR_CODE",
                "message": "...",
                "details": {...},
                "field": "..."
            },
            "request_id": "abc123",
            "timestamp": "2025-12-01T..."
        }
    """
    err_code = error_code or code or "SYS_INTERNAL_ERROR"

    payload = {
        "success": False,
        "status": "error",
        "error": {
            "code": err_code,
            "message": message or get_default_message(err_code),
        },
        "request_id": get_request_id(),
        "timestamp": get_timestamp(),
    }

    if details:
        payload["error"]["details"] = details
    if field:
        payload["error"]["field"] = field

    # Log error for debugging
    logger.warning(
        f"API Error [{err_code}]: {message} | request_id={get_request_id()} | status={status_code}"
    )

    return jsonify(payload), status_code


def get_default_message(error_code):
    """Get default message for an error code."""
    messages = {
        "DB_DUPLICATE_ENTRY": "A record with this value already exists",
        "DB_NOT_FOUND": "Record not found in database",
        "DB_ERROR": "Database operation failed",
        "VAL_INVALID_FORMAT": "Invalid data format",
        "VAL_MISSING_FIELD": "Required field is missing",
        "VAL_DUPLICATE_VALUE": "Duplicate value not allowed",
        "VAL_INVALID_REFERENCE": "Referenced entity not found",
        "RES_NOT_FOUND": "Resource not found",
        "SYS_INTERNAL_ERROR": "An internal server error occurred",
        "AUTH_INVALID_CREDENTIALS": "Invalid username or password",
        "AUTH_UNAUTHORIZED": "You are not authorized to perform this action",
        "AUTH_INVALID_TOKEN": "Invalid or malformed token",
        "AUTH_ACCOUNT_LOCKED": "Account is temporarily locked",
        "AUTH_TOKEN_EXPIRED": "Token has expired",
        "AUTH_TOKEN_REVOKED": "Token has been revoked",
        "AUTH_INSUFFICIENT_PERMISSIONS": "Insufficient permissions for this action",
        "RATE_LIMIT_EXCEEDED": "Too many requests. Please try again later",
    }
    return messages.get(error_code, "An error occurred")


def paginated_response(items, total, page, per_page, message=None):
    """
    Return a standardized paginated response.

    Args:
        items: List of items for current page
        total: Total number of items
        page: Current page number
        per_page: Items per page
        message: Optional message

    Returns:
        JSON response with pagination metadata
    """
    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return success_response(
        data=items,
        message=message,
        meta={
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
                "has_next": page < pages,
                "has_prev": page > 1,
            }
        },
    )


def handle_exceptions(func):
    """
    Decorator to catch and format exceptions as error responses.

    Usage:
        @handle_exceptions
        def my_route():
            ...
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return error_response(
                message=str(e),
                error_code=ErrorCodes.VAL_INVALID_FORMAT,
                status_code=400,
            )
        except KeyError as e:
            return error_response(
                message=f"Missing required field: {e}",
                error_code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )
        except PermissionError as e:
            return error_response(
                message=str(e), error_code=ErrorCodes.AUTH_UNAUTHORIZED, status_code=403
            )
        except Exception as e:
            logger.exception(f"Unhandled exception in {func.__name__}: {e}")
            return error_response(
                message="An internal server error occurred",
                error_code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=500,
            )

    return wrapper


class ErrorCodes:
    """
    P1.26: Central error code registry used by the error envelope.

    Error codes follow the pattern: CATEGORY_SPECIFIC_ERROR
    Categories:
    - DB: Database errors
    - VAL: Validation errors
    - RES: Resource errors
    - SYS: System errors
    - AUTH: Authentication/Authorization errors
    - RATE: Rate limiting errors
    - FILE: File operation errors
    - INT: Integration errors
    """

    # =====================================================================
    # Database errors (DB_*)
    # =====================================================================
    DB_DUPLICATE_ENTRY = "DB_DUPLICATE_ENTRY"
    DB_NOT_FOUND = "DB_NOT_FOUND"
    DB_ERROR = "DB_ERROR"
    DB_CONNECTION_ERROR = "DB_CONNECTION_ERROR"
    DB_CONSTRAINT_VIOLATION = "DB_CONSTRAINT_VIOLATION"
    DB_TRANSACTION_ERROR = "DB_TRANSACTION_ERROR"

    # =====================================================================
    # Validation errors (VAL_*)
    # =====================================================================
    VAL_INVALID_FORMAT = "VAL_INVALID_FORMAT"
    VAL_MISSING_FIELD = "VAL_MISSING_FIELD"
    VAL_DUPLICATE_VALUE = "VAL_DUPLICATE_VALUE"
    VAL_INVALID_REFERENCE = "VAL_INVALID_REFERENCE"
    VAL_INVALID_TYPE = "VAL_INVALID_TYPE"
    VAL_OUT_OF_RANGE = "VAL_OUT_OF_RANGE"
    VAL_STRING_TOO_LONG = "VAL_STRING_TOO_LONG"
    VAL_STRING_TOO_SHORT = "VAL_STRING_TOO_SHORT"
    VAL_INVALID_EMAIL = "VAL_INVALID_EMAIL"
    VAL_INVALID_PHONE = "VAL_INVALID_PHONE"
    VAL_INVALID_DATE = "VAL_INVALID_DATE"
    VAL_INVALID_JSON = "VAL_INVALID_JSON"

    # =====================================================================
    # Resource errors (RES_*)
    # =====================================================================
    RES_NOT_FOUND = "RES_NOT_FOUND"
    RES_ALREADY_EXISTS = "RES_ALREADY_EXISTS"
    RES_IN_USE = "RES_IN_USE"
    RES_LOCKED = "RES_LOCKED"
    RES_DELETED = "RES_DELETED"

    # =====================================================================
    # System errors (SYS_*)
    # =====================================================================
    SYS_INTERNAL_ERROR = "SYS_INTERNAL_ERROR"
    SYS_MAINTENANCE = "SYS_MAINTENANCE"
    SYS_SERVICE_UNAVAILABLE = "SYS_SERVICE_UNAVAILABLE"
    SYS_TIMEOUT = "SYS_TIMEOUT"
    SYS_CONFIGURATION_ERROR = "SYS_CONFIGURATION_ERROR"

    # =====================================================================
    # Authentication & Authorization errors (AUTH_*)
    # =====================================================================
    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    AUTH_UNAUTHORIZED = "AUTH_UNAUTHORIZED"
    AUTH_INVALID_TOKEN = "AUTH_INVALID_TOKEN"
    AUTH_ACCOUNT_LOCKED = "AUTH_ACCOUNT_LOCKED"
    AUTH_ACCOUNT_DISABLED = "AUTH_ACCOUNT_DISABLED"
    AUTH_MFA_REQUIRED = "AUTH_MFA_REQUIRED"
    AUTH_MFA_INVALID = "AUTH_MFA_INVALID"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_TOKEN_REVOKED = "AUTH_TOKEN_REVOKED"
    AUTH_INSUFFICIENT_PERMISSIONS = "AUTH_INSUFFICIENT_PERMISSIONS"
    AUTH_SESSION_EXPIRED = "AUTH_SESSION_EXPIRED"
    AUTH_PASSWORD_EXPIRED = "AUTH_PASSWORD_EXPIRED"

    # =====================================================================
    # Rate limiting errors (RATE_*)
    # =====================================================================
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    RATE_QUOTA_EXCEEDED = "RATE_QUOTA_EXCEEDED"

    # =====================================================================
    # File operation errors (FILE_*)
    # =====================================================================
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    FILE_INVALID_TYPE = "FILE_INVALID_TYPE"
    FILE_UPLOAD_ERROR = "FILE_UPLOAD_ERROR"

    # =====================================================================
    # Integration errors (INT_*)
    # =====================================================================
    INT_EXTERNAL_SERVICE_ERROR = "INT_EXTERNAL_SERVICE_ERROR"
    INT_API_ERROR = "INT_API_ERROR"
    INT_TIMEOUT = "INT_TIMEOUT"


# Export all public symbols
__all__ = [
    "success_response",
    "error_response",
    "paginated_response",
    "handle_exceptions",
    "ErrorCodes",
    "get_request_id",
    "get_timestamp",
]
