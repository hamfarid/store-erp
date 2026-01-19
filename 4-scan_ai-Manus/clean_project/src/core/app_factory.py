"""
مصنع التطبيق - إنشاء وتكوين تطبيق FastAPI
Application Factory - Create and configure FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging

from .config import Settings
from .middleware import setup_middleware
from .routes import setup_routes
from .database import init_database
from .exceptions import setup_exception_handlers

logger = logging.getLogger(__name__)

def create_app(settings: Settings) -> FastAPI:
    """
    إنشاء وتكوين تطبيق FastAPI
    Create and configure FastAPI application
    
    Args:
        settings: إعدادات التطبيق
        
    Returns:
        FastAPI: مثيل التطبيق المكون
    """
    
    # إنشاء التطبيق
    app = FastAPI(
        title="Gaara Scan AI System",
        description="نظام الذكاء الاصطناعي لتشخيص أمراض النباتات",
        version="2.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
    )
    
    # إعداد CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
    
    # إعداد Trusted Host
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.gaara-scan.ai"]
        )
    
    # إعداد Middleware المخصص
    setup_middleware(app, settings)
    
    # إعداد معالجات الاستثناءات
    setup_exception_handlers(app)
    
    # إعداد قاعدة البيانات
    init_database(settings)
    
    # إعداد المسارات
    setup_routes(app)
    
    # إضافة أحداث بدء التشغيل والإغلاق
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 بدء تشغيل نظام Gaara Scan AI")
        logger.info(f"📊 وضع التطوير: {settings.DEBUG}")
        logger.info(f"🌐 المنفذ: {settings.APP_PORT}")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("🛑 إيقاف نظام Gaara Scan AI")
    
    # صفحة الصحة الأساسية
    @app.get("/health")
    async def health_check():
        return JSONResponse({
            "status": "healthy",
            "service": "Gaara Scan AI",
            "version": "2.0.0"
        })
    
    return app

