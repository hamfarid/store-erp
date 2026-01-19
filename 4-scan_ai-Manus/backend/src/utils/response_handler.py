"""
API Response Handler
=====================

Purpose: Standardize all API responses for consistency across the application.
Provides bilingual messages (Arabic/English) and structured error handling.

Features:
- Consistent response format
- Bilingual support (AR/EN)
- Pagination helpers
- Error response formatting
- Success response helpers

Usage:
    from src.utils.response_handler import APIResponse, success, error, paginated
    
    # Success response
    return success(data=user.to_dict(), message="User created")
    
    # Error response
    return error(code="USER_NOT_FOUND", message="User not found", status=404)
    
    # Paginated response
    return paginated(items=users, total=100, page=1, per_page=20)

Author: Global System v35.0
Date: 2026-01-17
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ============================================
# Response Models
# ============================================

class APIResponse(BaseModel):
    """
    Standard API response model.
    
    Attributes:
        success: Whether the request was successful
        message: English message
        message_ar: Arabic message
        data: Response payload
        error: Error details (if any)
        meta: Additional metadata
        timestamp: Response timestamp
    """
    success: bool = True
    message: Optional[str] = None
    message_ar: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None
    timestamp: str = None
    
    def __init__(self, **data):
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        super().__init__(**data)


class PaginationMeta(BaseModel):
    """
    Pagination metadata model.
    
    Attributes:
        total: Total number of items
        page: Current page number
        per_page: Items per page
        total_pages: Total number of pages
        has_next: Whether there's a next page
        has_prev: Whether there's a previous page
    """
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ErrorDetail(BaseModel):
    """
    Error detail model.
    
    Attributes:
        code: Error code (e.g., "USER_NOT_FOUND")
        message: English error message
        message_ar: Arabic error message
        field: Field name (for validation errors)
        details: Additional error details
    """
    code: str
    message: str
    message_ar: Optional[str] = None
    field: Optional[str] = None
    details: Optional[Any] = None


# ============================================
# Bilingual Messages
# ============================================

MESSAGES = {
    # Success messages
    "SUCCESS": {
        "en": "Operation completed successfully",
        "ar": "تمت العملية بنجاح"
    },
    "CREATED": {
        "en": "Resource created successfully",
        "ar": "تم إنشاء المورد بنجاح"
    },
    "UPDATED": {
        "en": "Resource updated successfully",
        "ar": "تم تحديث المورد بنجاح"
    },
    "DELETED": {
        "en": "Resource deleted successfully",
        "ar": "تم حذف المورد بنجاح"
    },
    "FETCHED": {
        "en": "Data retrieved successfully",
        "ar": "تم استرجاع البيانات بنجاح"
    },
    
    # Error messages
    "NOT_FOUND": {
        "en": "Resource not found",
        "ar": "المورد غير موجود"
    },
    "UNAUTHORIZED": {
        "en": "Authentication required",
        "ar": "يتطلب تسجيل الدخول"
    },
    "FORBIDDEN": {
        "en": "Access denied",
        "ar": "تم رفض الوصول"
    },
    "VALIDATION_ERROR": {
        "en": "Validation error",
        "ar": "خطأ في التحقق من البيانات"
    },
    "SERVER_ERROR": {
        "en": "Internal server error",
        "ar": "خطأ داخلي في الخادم"
    },
    "BAD_REQUEST": {
        "en": "Invalid request",
        "ar": "طلب غير صالح"
    },
    "CONFLICT": {
        "en": "Resource already exists",
        "ar": "المورد موجود بالفعل"
    },
    "RATE_LIMITED": {
        "en": "Too many requests, please try again later",
        "ar": "طلبات كثيرة جداً، يرجى المحاولة لاحقاً"
    },
    "ACCOUNT_LOCKED": {
        "en": "Account is temporarily locked",
        "ar": "الحساب مقفل مؤقتاً"
    },
    "INVALID_CREDENTIALS": {
        "en": "Invalid email or password",
        "ar": "البريد الإلكتروني أو كلمة المرور غير صحيحة"
    },
    "SESSION_EXPIRED": {
        "en": "Session has expired, please login again",
        "ar": "انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى"
    },
    "FILE_TOO_LARGE": {
        "en": "File size exceeds the limit",
        "ar": "حجم الملف يتجاوز الحد المسموح"
    },
    "INVALID_FILE_TYPE": {
        "en": "Invalid file type",
        "ar": "نوع الملف غير مدعوم"
    },
    "DIAGNOSIS_IN_PROGRESS": {
        "en": "Diagnosis is being processed",
        "ar": "جاري معالجة التشخيص"
    },
    "DIAGNOSIS_COMPLETE": {
        "en": "Diagnosis completed successfully",
        "ar": "اكتمل التشخيص بنجاح"
    },
    "NO_DISEASE_DETECTED": {
        "en": "No disease detected - plant appears healthy",
        "ar": "لم يتم اكتشاف مرض - النبات يبدو سليماً"
    }
}


def get_message(key: str, lang: str = "en") -> str:
    """
    Get a bilingual message by key.
    
    Args:
        key: Message key
        lang: Language code ('en' or 'ar')
        
    Returns:
        str: Localized message
    """
    msg = MESSAGES.get(key, {"en": key, "ar": key})
    return msg.get(lang, msg.get("en", key))


# ============================================
# Response Helpers
# ============================================

def success(
    data: Any = None,
    message: Optional[str] = None,
    message_ar: Optional[str] = None,
    message_key: str = "SUCCESS",
    meta: Optional[Dict] = None,
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    Create a success response.
    
    Args:
        data: Response payload
        message: English message (overrides message_key)
        message_ar: Arabic message (overrides message_key)
        message_key: Key for bilingual message lookup
        meta: Additional metadata
        status_code: HTTP status code
        
    Returns:
        JSONResponse: Formatted success response
    """
    response = APIResponse(
        success=True,
        message=message or get_message(message_key, "en"),
        message_ar=message_ar or get_message(message_key, "ar"),
        data=data,
        meta=meta
    )
    
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(exclude_none=True)
    )


def created(
    data: Any = None,
    message: Optional[str] = None,
    message_ar: Optional[str] = None
) -> JSONResponse:
    """Create a 201 Created response."""
    return success(
        data=data,
        message=message,
        message_ar=message_ar,
        message_key="CREATED",
        status_code=status.HTTP_201_CREATED
    )


def updated(
    data: Any = None,
    message: Optional[str] = None,
    message_ar: Optional[str] = None
) -> JSONResponse:
    """Create an update success response."""
    return success(
        data=data,
        message=message,
        message_ar=message_ar,
        message_key="UPDATED"
    )


def deleted(
    message: Optional[str] = None,
    message_ar: Optional[str] = None
) -> JSONResponse:
    """Create a delete success response."""
    return success(
        message=message,
        message_ar=message_ar,
        message_key="DELETED"
    )


def error(
    code: str,
    message: Optional[str] = None,
    message_ar: Optional[str] = None,
    message_key: Optional[str] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    field: Optional[str] = None,
    details: Optional[Any] = None
) -> JSONResponse:
    """
    Create an error response.
    
    Args:
        code: Error code (e.g., "USER_NOT_FOUND")
        message: English error message
        message_ar: Arabic error message
        message_key: Key for bilingual message lookup
        status_code: HTTP status code
        field: Field name (for validation errors)
        details: Additional error details
        
    Returns:
        JSONResponse: Formatted error response
    """
    # Use message_key if no explicit messages provided
    if message_key and not message:
        message = get_message(message_key, "en")
    if message_key and not message_ar:
        message_ar = get_message(message_key, "ar")
    
    error_detail = ErrorDetail(
        code=code,
        message=message or code,
        message_ar=message_ar,
        field=field,
        details=details
    )
    
    response = APIResponse(
        success=False,
        message=message,
        message_ar=message_ar,
        error=error_detail.model_dump(exclude_none=True)
    )
    
    logger.warning(f"API Error: {code} - {message}")
    
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(exclude_none=True)
    )


def not_found(
    resource: str = "Resource",
    resource_ar: str = "المورد"
) -> JSONResponse:
    """Create a 404 Not Found response."""
    return error(
        code="NOT_FOUND",
        message=f"{resource} not found",
        message_ar=f"{resource_ar} غير موجود",
        status_code=status.HTTP_404_NOT_FOUND
    )


def unauthorized(
    message: Optional[str] = None,
    message_ar: Optional[str] = None
) -> JSONResponse:
    """Create a 401 Unauthorized response."""
    return error(
        code="UNAUTHORIZED",
        message=message,
        message_ar=message_ar,
        message_key="UNAUTHORIZED",
        status_code=status.HTTP_401_UNAUTHORIZED
    )


def forbidden(
    message: Optional[str] = None,
    message_ar: Optional[str] = None
) -> JSONResponse:
    """Create a 403 Forbidden response."""
    return error(
        code="FORBIDDEN",
        message=message,
        message_ar=message_ar,
        message_key="FORBIDDEN",
        status_code=status.HTTP_403_FORBIDDEN
    )


def validation_error(
    errors: List[Dict[str, Any]]
) -> JSONResponse:
    """
    Create a 422 Validation Error response.
    
    Args:
        errors: List of validation errors
        
    Returns:
        JSONResponse: Formatted validation error response
    """
    return error(
        code="VALIDATION_ERROR",
        message="Validation error",
        message_ar="خطأ في التحقق من البيانات",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=errors
    )


def server_error(
    message: Optional[str] = None,
    message_ar: Optional[str] = None
) -> JSONResponse:
    """Create a 500 Internal Server Error response."""
    return error(
        code="SERVER_ERROR",
        message=message,
        message_ar=message_ar,
        message_key="SERVER_ERROR",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def rate_limited(
    retry_after: int = 60
) -> JSONResponse:
    """
    Create a 429 Too Many Requests response.
    
    Args:
        retry_after: Seconds until rate limit resets
        
    Returns:
        JSONResponse: Formatted rate limit response
    """
    response = error(
        code="RATE_LIMITED",
        message_key="RATE_LIMITED",
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        details={"retry_after": retry_after}
    )
    response.headers["Retry-After"] = str(retry_after)
    return response


# ============================================
# Pagination Helper
# ============================================

def paginated(
    items: List[Any],
    total: int,
    page: int = 1,
    per_page: int = 20,
    message: Optional[str] = None,
    message_ar: Optional[str] = None
) -> JSONResponse:
    """
    Create a paginated response.
    
    Args:
        items: List of items for current page
        total: Total number of items
        page: Current page number
        per_page: Items per page
        message: English message
        message_ar: Arabic message
        
    Returns:
        JSONResponse: Paginated response with metadata
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
    
    pagination = PaginationMeta(
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return success(
        data=items,
        message=message or get_message("FETCHED", "en"),
        message_ar=message_ar or get_message("FETCHED", "ar"),
        meta={"pagination": pagination.model_dump()}
    )


# ============================================
# Diagnosis-Specific Responses
# ============================================

def diagnosis_result(
    disease_name: str,
    disease_name_ar: str,
    confidence: float,
    severity: str,
    recommendations: List[str],
    recommendations_ar: List[str],
    image_url: Optional[str] = None,
    treatment: Optional[Dict] = None
) -> JSONResponse:
    """
    Create a diagnosis result response.
    
    Args:
        disease_name: English disease name
        disease_name_ar: Arabic disease name
        confidence: Confidence score (0-1)
        severity: Severity level
        recommendations: English recommendations
        recommendations_ar: Arabic recommendations
        image_url: Analyzed image URL
        treatment: Treatment information
        
    Returns:
        JSONResponse: Diagnosis result response
    """
    data = {
        "disease": {
            "name": disease_name,
            "name_ar": disease_name_ar
        },
        "confidence": round(confidence * 100, 1),
        "severity": severity,
        "recommendations": recommendations,
        "recommendations_ar": recommendations_ar,
        "image_url": image_url,
        "treatment": treatment,
        "diagnosed_at": datetime.utcnow().isoformat() + 'Z'
    }
    
    return success(
        data=data,
        message_key="DIAGNOSIS_COMPLETE"
    )


def healthy_plant() -> JSONResponse:
    """Create a response for healthy plant (no disease detected)."""
    return success(
        data={
            "disease": None,
            "confidence": 100,
            "status": "healthy",
            "diagnosed_at": datetime.utcnow().isoformat() + 'Z'
        },
        message_key="NO_DISEASE_DETECTED"
    )
