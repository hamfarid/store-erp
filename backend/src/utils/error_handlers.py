#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالجات الأخطاء الموحدة
Unified Error Handlers

نظام موحد لمعالجة جميع أنواع الأخطاء في التطبيق
"""

import logging
import traceback
from datetime import datetime, timezone

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

# إعداد Logger
logger = logging.getLogger(__name__)


class APIError(Exception):
    """
    استثناء مخصص لأخطاء API
    Custom API Exception
    """

    def __init__(self, message, status_code=400, payload=None, message_en=None):
        super().__init__()
        self.message = message
        self.message_en = message_en or message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """تحويل إلى قاموس"""
        rv = {
            "success": False,
            "error": self.message,
            "error_en": self.message_en,
            "status_code": self.status_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if self.payload:
            rv["details"] = self.payload
        return rv


class ValidationError(APIError):
    """خطأ في التحقق من البيانات"""

    def __init__(self, message, message_en=None, errors=None):
        super().__init__(
            message=message,
            message_en=message_en or "Validation Error",
            status_code=400,
            payload={"validation_errors": errors} if errors else None,
        )


class NotFoundError(APIError):
    """خطأ عدم العثور على المورد"""

    def __init__(self, resource, message=None, message_en=None):
        msg = message or f"{resource} غير موجود"
        msg_en = message_en or f"{resource} not found"
        super().__init__(message=msg, message_en=msg_en, status_code=404)


class UnauthorizedError(APIError):
    """خطأ عدم التصريح"""

    def __init__(self, message="غير مصرح", message_en="Unauthorized"):
        super().__init__(message=message, message_en=message_en, status_code=401)


class ForbiddenError(APIError):
    """خطأ الوصول ممنوع"""

    def __init__(self, message="الوصول ممنوع", message_en="Forbidden"):
        super().__init__(message=message, message_en=message_en, status_code=403)


class ConflictError(APIError):
    """خطأ التعارض"""

    def __init__(self, message, message_en=None):
        super().__init__(
            message=message, message_en=message_en or "Conflict", status_code=409
        )


class DatabaseError(APIError):
    """خطأ في قاعدة البيانات"""

    def __init__(self, message="خطأ في قاعدة البيانات", message_en="Database Error"):
        super().__init__(message=message, message_en=message_en, status_code=500)


def register_error_handlers(app):
    """
    تسجيل معالجات الأخطاء في التطبيق
    Register error handlers with the Flask app
    """

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """معالج أخطاء API المخصصة"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code

        # تسجيل الخطأ
        logger.warning(f"API Error: {error.message} (Status: {error.status_code})")

        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """معالج أخطاء التحقق"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code

        logger.warning(f"Validation Error: {error.message}")

        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        """معالج خطأ 404"""
        from uuid import uuid4

        trace_id = (
            request.headers.get("X-Request-Id")
            or request.headers.get("X-Trace-Id")
            or str(uuid4())
        )
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "not_found",
                        "message": "Page not found",
                        "details": {"path": request.path},
                        "traceId": trace_id,
                    },
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """معالج خطأ 405"""
        from uuid import uuid4

        trace_id = (
            request.headers.get("X-Request-Id")
            or request.headers.get("X-Trace-Id")
            or str(uuid4())
        )
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "method_not_allowed",
                        "message": "Method not allowed",
                        "details": {"method": request.method, "path": request.path},
                        "traceId": trace_id,
                    },
                }
            ),
            405,
        )

    @app.errorhandler(500)
    def handle_internal_error(error):
        """معالج خطأ 500"""
        # تسجيل الخطأ الكامل
        logger.error(f"Internal Server Error: {str(error)}")
        logger.error(traceback.format_exc())
        from uuid import uuid4

        trace_id = (
            request.headers.get("X-Request-Id")
            or request.headers.get("X-Trace-Id")
            or str(uuid4())
        )
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "internal_error",
                        "message": "Internal server error",
                        "details": None,
                        "traceId": trace_id,
                    },
                }
            ),
            500,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """معالج استثناءات HTTP العامة"""
        from uuid import uuid4

        trace_id = (
            request.headers.get("X-Request-Id")
            or request.headers.get("X-Trace-Id")
            or str(uuid4())
        )
        code_map = {
            400: "bad_request",
            401: "unauthorized",
            403: "forbidden",
            404: "not_found",
        }
        status = getattr(error, "code", 400)
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": code_map.get(status, "bad_request"),
                        "message": error.description or "Request error",
                        "details": {"path": request.path},
                        "traceId": trace_id,
                    },
                }
            ),
            status,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """معالج الأخطاء غير المتوقعة"""
        # تسجيل الخطأ الكامل
        logger.error(f"Unexpected Error: {str(error)}")
        logger.error(traceback.format_exc())
        from uuid import uuid4

        trace_id = (
            request.headers.get("X-Request-Id")
            or request.headers.get("X-Trace-Id")
            or str(uuid4())
        )
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "internal_error",
                        "message": (
                            "An unexpected error occurred"
                            if not app.config.get("DEBUG")
                            else str(error)
                        ),
                        "details": None,
                        "traceId": trace_id,
                    },
                }
            ),
            500,
        )


def success_response(
    data=None,
    message="تمت العملية بنجاح",
    message_en="Operation successful",
    status_code=200,
):
    """
    إنشاء استجابة نجاح موحدة
    Create a unified success response
    """
    response = {
        "success": True,
        "message": message,
        "message_en": message_en,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status_code


def error_response(message, message_en=None, status_code=400, details=None):
    """
    إنشاء استجابة خطأ موحدة + traceId
    Create a unified error response with traceId and standard envelope
    """
    from uuid import uuid4

    trace_id = (
        request.headers.get("X-Request-Id")
        or request.headers.get("X-Trace-Id")
        or str(uuid4())
    )
    # Map status codes to error codes
    code_map = {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "validation_error",
        500: "internal_error",
    }
    payload = {
        "success": False,
        "error": {
            "code": code_map.get(int(status_code), "error"),
            "message": message_en or message,
            "details": details,
            "traceId": trace_id,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return jsonify(payload), status_code


def paginated_response(
    items,
    page,
    per_page,
    total,
    message="تم الحصول على البيانات بنجاح",
    message_en="Data retrieved successfully",
):
    """
    إنشاء استجابة مع تقسيم الصفحات
    Create a paginated response
    """
    import math

    return (
        jsonify(
            {
                "success": True,
                "message": message,
                "message_en": message_en,
                "data": items,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": math.ceil(total / per_page) if per_page > 0 else 0,
                    "has_next": page * per_page < total,
                    "has_prev": page > 1,
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
        ),
        200,
    )
