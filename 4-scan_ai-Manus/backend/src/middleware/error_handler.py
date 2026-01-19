"""
Global Error Handler Middleware
================================

Purpose: Catch and handle all exceptions consistently across the API.
Provides bilingual error messages and proper logging.

Features:
- Catches all unhandled exceptions
- Provides consistent error response format
- Bilingual error messages (AR/EN)
- Request ID tracking
- Error logging with context
- Different handling for different exception types

Usage:
    from src.middleware.error_handler import ErrorHandlerMiddleware
    
    app = FastAPI()
    app.add_middleware(ErrorHandlerMiddleware)

Author: Global System v35.0
Date: 2026-01-17
"""

import logging
import traceback
import uuid
from datetime import datetime
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


# ============================================
# Error Response Format
# ============================================

def create_error_response(
    request_id: str,
    code: str,
    message: str,
    message_ar: str,
    status_code: int,
    details: dict = None,
    path: str = None
) -> JSONResponse:
    """
    Create a standardized error response.
    
    Args:
        request_id: Unique request identifier
        code: Error code
        message: English error message
        message_ar: Arabic error message
        status_code: HTTP status code
        details: Additional error details
        path: Request path
        
    Returns:
        JSONResponse: Formatted error response
    """
    content = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "message_ar": message_ar,
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
    }
    
    if details:
        content["error"]["details"] = details
    
    if path:
        content["error"]["path"] = path
    
    return JSONResponse(
        status_code=status_code,
        content=content,
        headers={"X-Request-ID": request_id}
    )


# ============================================
# Error Mappings
# ============================================

# HTTP status code to error info mapping
HTTP_ERROR_MESSAGES = {
    400: {
        "code": "BAD_REQUEST",
        "message": "Bad request",
        "message_ar": "طلب غير صالح"
    },
    401: {
        "code": "UNAUTHORIZED",
        "message": "Authentication required",
        "message_ar": "يتطلب تسجيل الدخول"
    },
    403: {
        "code": "FORBIDDEN",
        "message": "Access denied",
        "message_ar": "تم رفض الوصول"
    },
    404: {
        "code": "NOT_FOUND",
        "message": "Resource not found",
        "message_ar": "المورد غير موجود"
    },
    405: {
        "code": "METHOD_NOT_ALLOWED",
        "message": "Method not allowed",
        "message_ar": "الطريقة غير مسموحة"
    },
    408: {
        "code": "REQUEST_TIMEOUT",
        "message": "Request timeout",
        "message_ar": "انتهت مهلة الطلب"
    },
    409: {
        "code": "CONFLICT",
        "message": "Resource conflict",
        "message_ar": "تعارض في المورد"
    },
    413: {
        "code": "PAYLOAD_TOO_LARGE",
        "message": "Request payload too large",
        "message_ar": "حجم الطلب كبير جداً"
    },
    422: {
        "code": "VALIDATION_ERROR",
        "message": "Validation error",
        "message_ar": "خطأ في التحقق من البيانات"
    },
    423: {
        "code": "LOCKED",
        "message": "Resource is locked",
        "message_ar": "المورد مقفل"
    },
    429: {
        "code": "TOO_MANY_REQUESTS",
        "message": "Too many requests",
        "message_ar": "طلبات كثيرة جداً"
    },
    500: {
        "code": "INTERNAL_ERROR",
        "message": "Internal server error",
        "message_ar": "خطأ داخلي في الخادم"
    },
    502: {
        "code": "BAD_GATEWAY",
        "message": "Bad gateway",
        "message_ar": "خطأ في البوابة"
    },
    503: {
        "code": "SERVICE_UNAVAILABLE",
        "message": "Service temporarily unavailable",
        "message_ar": "الخدمة غير متاحة مؤقتاً"
    },
    504: {
        "code": "GATEWAY_TIMEOUT",
        "message": "Gateway timeout",
        "message_ar": "انتهت مهلة البوابة"
    }
}


def get_error_info(status_code: int) -> dict:
    """Get error info for a status code."""
    return HTTP_ERROR_MESSAGES.get(status_code, {
        "code": f"HTTP_{status_code}",
        "message": "An error occurred",
        "message_ar": "حدث خطأ"
    })


# ============================================
# Validation Error Formatter
# ============================================

def format_validation_errors(errors: list) -> list:
    """
    Format Pydantic validation errors for API response.
    
    Args:
        errors: List of validation error dicts
        
    Returns:
        list: Formatted error list
    """
    formatted = []
    
    for error in errors:
        loc = error.get("loc", [])
        field = ".".join(str(x) for x in loc if x != "body")
        
        formatted.append({
            "field": field,
            "message": error.get("msg", "Invalid value"),
            "type": error.get("type", "value_error")
        })
    
    return formatted


# ============================================
# Error Handler Middleware
# ============================================

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.
    
    Catches all exceptions and returns consistent error responses.
    Logs errors with context for debugging.
    
    Example:
        app = FastAPI()
        app.add_middleware(ErrorHandlerMiddleware)
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> JSONResponse:
        """
        Process request and handle any exceptions.
        
        Args:
            request: Incoming request
            call_next: Next middleware/handler
            
        Returns:
            Response or error response
        """
        # Generate unique request ID
        request_id = str(uuid.uuid4())[:8]
        
        # Add request ID to state for logging
        request.state.request_id = request_id
        
        try:
            # Process request
            response = await call_next(request)
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as exc:
            # Log the error
            logger.error(
                f"[{request_id}] Unhandled exception: {type(exc).__name__}: {exc}",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "method": request.method,
                    "client": request.client.host if request.client else "unknown"
                }
            )
            
            # Log traceback for debugging
            logger.debug(f"[{request_id}] Traceback:\n{traceback.format_exc()}")
            
            # Return generic error response
            error_info = get_error_info(500)
            
            return create_error_response(
                request_id=request_id,
                code=error_info["code"],
                message=error_info["message"],
                message_ar=error_info["message_ar"],
                status_code=500,
                path=request.url.path
            )


# ============================================
# Exception Handlers
# ============================================

def setup_exception_handlers(app: FastAPI) -> None:
    """
    Setup FastAPI exception handlers.
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        """Handle HTTPException."""
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4())[:8])
        
        error_info = get_error_info(exc.status_code)
        
        # Use exception detail if provided
        message = exc.detail if isinstance(exc.detail, str) else error_info["message"]
        
        # Handle dict details (bilingual messages)
        details = None
        message_ar = error_info["message_ar"]
        
        if isinstance(exc.detail, dict):
            message = exc.detail.get("message", error_info["message"])
            message_ar = exc.detail.get("message_ar", error_info["message_ar"])
            details = {k: v for k, v in exc.detail.items() if k not in ["message", "message_ar"]}
        
        return create_error_response(
            request_id=request_id,
            code=error_info["code"],
            message=message,
            message_ar=message_ar,
            status_code=exc.status_code,
            details=details if details else None,
            path=request.url.path
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle request validation errors."""
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4())[:8])
        
        errors = format_validation_errors(exc.errors())
        
        logger.warning(
            f"[{request_id}] Validation error: {errors}",
            extra={"path": request.url.path}
        )
        
        return create_error_response(
            request_id=request_id,
            code="VALIDATION_ERROR",
            message="Request validation failed",
            message_ar="فشل التحقق من صحة الطلب",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": errors},
            path=request.url.path
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors."""
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4())[:8])
        
        errors = format_validation_errors(exc.errors())
        
        return create_error_response(
            request_id=request_id,
            code="VALIDATION_ERROR",
            message="Data validation failed",
            message_ar="فشل التحقق من صحة البيانات",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": errors},
            path=request.url.path
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all other exceptions."""
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4())[:8])
        
        logger.error(
            f"[{request_id}] Unhandled exception: {type(exc).__name__}: {exc}",
            extra={
                "path": request.url.path,
                "traceback": traceback.format_exc()
            }
        )
        
        return create_error_response(
            request_id=request_id,
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            message_ar="حدث خطأ غير متوقع",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            path=request.url.path
        )


# ============================================
# Custom Exceptions
# ============================================

class APIException(HTTPException):
    """
    Custom API exception with bilingual support.
    
    Example:
        raise APIException(
            status_code=404,
            code="USER_NOT_FOUND",
            message="User not found",
            message_ar="المستخدم غير موجود"
        )
    """
    
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        message_ar: str = None,
        details: dict = None
    ):
        detail = {
            "code": code,
            "message": message,
            "message_ar": message_ar or message
        }
        if details:
            detail.update(details)
        
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(APIException):
    """Resource not found exception."""
    
    def __init__(
        self,
        resource: str = "Resource",
        resource_ar: str = "المورد"
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=f"{resource} not found",
            message_ar=f"{resource_ar} غير موجود"
        )


class UnauthorizedException(APIException):
    """Authentication required exception."""
    
    def __init__(self, message: str = None, message_ar: str = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message or "Authentication required",
            message_ar=message_ar or "يتطلب تسجيل الدخول"
        )


class ForbiddenException(APIException):
    """Access denied exception."""
    
    def __init__(self, message: str = None, message_ar: str = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message or "Access denied",
            message_ar=message_ar or "تم رفض الوصول"
        )


class ConflictException(APIException):
    """Resource conflict exception."""
    
    def __init__(
        self,
        resource: str = "Resource",
        resource_ar: str = "المورد"
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            message=f"{resource} already exists",
            message_ar=f"{resource_ar} موجود بالفعل"
        )


class RateLimitException(APIException):
    """Rate limit exceeded exception."""
    
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMITED",
            message="Too many requests, please try again later",
            message_ar="طلبات كثيرة جداً، يرجى المحاولة لاحقاً",
            details={"retry_after": retry_after}
        )
