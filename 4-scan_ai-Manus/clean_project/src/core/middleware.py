"""
Middleware مخصص للتطبيق
Custom Middleware for the application
"""

import time
import logging
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import uuid

logger = logging.getLogger(__name__)

def setup_middleware(app: FastAPI, settings):
    """
    إعداد Middleware المخصص
    Setup custom middleware
    """
    
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next: Callable) -> Response:
        """
        Middleware لتسجيل الطلبات
        Request logging middleware
        """
        # إنشاء معرف فريد للطلب
        request_id = str(uuid.uuid4())[:8]
        
        # تسجيل بداية الطلب
        start_time = time.time()
        logger.info(f"[{request_id}] {request.method} {request.url.path} - بدء الطلب")
        
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
            logger.error(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"خطأ: {str(e)} - "
                f"الوقت: {process_time:.3f}s"
            )
            
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
    async def security_headers_middleware(request: Request, call_next: Callable) -> Response:
        """
        Middleware لإضافة رؤوس الأمان
        Security headers middleware
        """
        response = await call_next(request)
        
        # إضافة رؤوس الأمان
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        if not settings.DEBUG:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

