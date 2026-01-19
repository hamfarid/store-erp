"""
معالجات الاستثناءات - إدارة الأخطاء والاستثناءات
Exception Handlers - Error and exception management
"""

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    """
    إعداد معالجات الاستثناءات
    Setup exception handlers
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        معالج استثناءات HTTP
        HTTP exception handler
        """
        logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code,
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        معالج أخطاء التحقق من صحة البيانات
        Validation error handler
        """
        logger.warning(f"Validation Error: {exc.errors()}")
        
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": "خطأ في التحقق من صحة البيانات",
                "details": exc.errors(),
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        معالج استثناءات Starlette
        Starlette exception handler
        """
        logger.error(f"Starlette Exception: {exc.status_code} - {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail or "خطأ في الخادم",
                "status_code": exc.status_code,
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        معالج الاستثناءات العامة
        General exception handler
        """
        logger.error(f"Unhandled Exception: {type(exc).__name__} - {str(exc)}")
        
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "خطأ داخلي في الخادم",
                "type": type(exc).__name__,
                "path": str(request.url.path)
            }
        )

