"""
Middleware مخصص للتطبيق
Custom Middleware for the application

Enhanced with SSTI Protection - Version 2.0.0
"""

import logging
import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

# Import SSTI Protection
try:
    from src.modules.security.ssti_protection import SSTIMiddleware
    SSTI_AVAILABLE = True
except ImportError:
    SSTI_AVAILABLE = False

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI, settings):
    """
    إعداد Middleware المخصص
    Setup custom middleware

    Includes:
    - Request logging
    - Security headers
    - SSTI Protection
    """

    # ===== SSTI Protection Middleware =====
    if SSTI_AVAILABLE:
        app.add_middleware(
            SSTIMiddleware,
            enabled=True,
            strict_mode=True,
            exempt_paths=[
                "/docs",
                "/redoc",
                "/openapi.json",
                "/health",
                "/api/auth/login",
                "/api/auth/register",
            ],
            log_attempts=True,
            notify_admin=not settings.DEBUG
        )
        logger.info("[OK] SSTI Protection middleware enabled")
    else:
        logger.warning("[WARN] SSTI Protection not available - module not found")

    @app.middleware("http")
    async def logging_middleware(
            request: Request,
            call_next: Callable) -> Response:
        """
        Middleware لتسجيل الطلبات
        Request logging middleware
        """
        # ===== Request/body size limits =====
        # Helps mitigate oversized payload attacks and reduces risk of native-library crashes.
        try:
            content_length = request.headers.get("content-length")
            content_type = (request.headers.get("content-type") or "").lower()

            is_multipart = "multipart/form-data" in content_type
            if content_length:
                try:
                    length = int(content_length)
                except ValueError:
                    length = None
                if length is not None:
                    limit = settings.max_multipart_body_bytes if is_multipart else settings.max_json_body_bytes
                    if length > limit:
                        return JSONResponse(
                            status_code=413,
                            content={"error": "حجم الطلب كبير جداً"},
                        )
            # If no Content-Length and it's not multipart, do a bounded stream read to enforce limit.
            if (not content_length) and (not is_multipart):
                limit = settings.max_json_body_bytes
                body = bytearray()
                async for chunk in request.stream():
                    body.extend(chunk)
                    if len(body) > limit:
                        return JSONResponse(
                            status_code=413,
                            content={"error": "حجم الطلب كبير جداً"},
                        )
                # Make body available for downstream handlers.
                request._body = bytes(body)  # type: ignore[attr-defined]
        except Exception:
            # Best-effort; do not break requests if limit logic fails.
            pass

        # إنشاء معرف فريد للطلب
        request_id = str(uuid.uuid4())[:8]

        # تسجيل بداية الطلب
        start_time = time.time()
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - بدء الطلب")

        # معالجة الطلب
        try:
            response = await call_next(request)

            # حساب وقت المعالجة
            process_time = time.time() - start_time

            # تسجيل انتهاء الطلب
            logger.info(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"الحالة: {response.status_code} - "
                f"الوقت: {process_time:.3f}s"
            )

            # إضافة معرف الطلب للاستجابة
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # تسجيل الأخطاء
            process_time = time.time() - start_time
            logger.exception(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"خطأ: {str(e)} - "
                f"الوقت: {process_time:.3f}s"
            )

            # In development, re-raise to surface full stack traces in console.
            if getattr(settings, "DEBUG", False):
                raise

            # إرجاع استجابة خطأ
            return JSONResponse(
                status_code=500,
                content={
                    "error": "خطأ داخلي في الخادم",
                    "request_id": request_id
                },
                headers={
                    "X-Request-ID": request_id,
                    "X-Process-Time": str(process_time)
                }
            )

    @app.middleware("http")
    async def security_headers_middleware(
            request: Request,
            call_next: Callable) -> Response:
        """
        Middleware لإضافة رؤوس الأمان الشاملة
        Comprehensive Security headers middleware
        Version: 1.1.0 - Enhanced with CSP and additional headers
        """
        response = await call_next(request)

        # ===== رؤوس الأمان الأساسية =====
        # Basic Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # ===== Content Security Policy =====
        # سياسة أمان المحتوى
        # In production we tighten script policy by removing unsafe-eval.
        script_src = "script-src 'self' 'unsafe-inline'" if settings.DEBUG else "script-src 'self' 'unsafe-inline'"

        # Allow frontend -> backend API calls for configured origins.
        allowed_connect = ["'self'", "https:", "wss:", "ws:"]
        try:
            for origin in getattr(settings, "ALLOWED_ORIGINS", []) or []:
                allowed_connect.append(origin)
        except Exception:
            pass

        csp_directives = [
            "default-src 'self'",
            script_src,
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com data:",
            "img-src 'self' data: https: blob:",
            f"connect-src {' '.join(allowed_connect)}",
            "frame-ancestors 'none'",
            "form-action 'self'",
            "base-uri 'self'",
            "object-src 'none'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # ===== رؤوس إضافية =====
        # Additional Security Headers
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(self), "
            "payment=(), usb=(), magnetometer=(), accelerometer=()"
        )
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # ===== HSTS في بيئة الإنتاج =====
        # HSTS in production
        if not settings.DEBUG:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response
