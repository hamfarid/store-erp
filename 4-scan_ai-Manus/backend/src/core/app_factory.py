"""
FILE: backend/src/core/app_factory.py | PURPOSE: Application factory | OWNER: Backend Team | LAST-AUDITED: 2026-01-31

مصنع التطبيق - إنشاء وتكوين تطبيق FastAPI
Application Factory - Create and configure FastAPI application

Version: 2.2.0 - Integrated comprehensive error handler with bilingual support
"""

import logging
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, Response

from .config import Settings
from .database import init_database
from .middleware import setup_middleware
from .rate_limiting import setup_rate_limiting
from .routes import setup_routes
from ..middleware.error_handler import setup_exception_handlers

# Prometheus metrics
try:
    from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
    PROMETHEUS_ENABLED = True
except ImportError:
    PROMETHEUS_ENABLED = False

logger = logging.getLogger(__name__)

# Define metrics if prometheus is available
if PROMETHEUS_ENABLED:
    REQUEST_COUNT = Counter(
        'scan_ai_requests_total',
        'Total number of requests',
        ['method', 'endpoint', 'status']
    )
    REQUEST_LATENCY = Histogram(
        'scan_ai_request_latency_seconds',
        'Request latency in seconds',
        buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    )


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
        allowed_hosts = [
            "localhost",
            "127.0.0.1",
            "*.gaara-scan.ai",
            "backend",  # Docker service name
            "*",        # Allow all hosts in containerized environment (includes Docker IPs)
        ]
        # FastAPI's TestClient uses host 'testserver' by default.
        if os.environ.get("PYTEST_CURRENT_TEST") or "pytest" in sys.modules:
            allowed_hosts.append("testserver")
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=allowed_hosts,
        )

    # إعداد Middleware المخصص
    setup_middleware(app, settings)

    # إعداد تحديد معدل الطلبات
    # Setup Rate Limiting
    setup_rate_limiting(app)

    # إعداد معالجات الاستثناءات
    setup_exception_handlers(app)

    # إعداد قاعدة البيانات
    init_database(settings)

    # إعداد المسارات
    setup_routes(app)

    # إضافة أحداث بدء التشغيل والإغلاق
    @app.on_event("startup")
    async def startup_event():
        logger.info("[START] بدء تشغيل نظام Gaara Scan AI")
        logger.info("[INFO] وضع التطوير: %s", settings.DEBUG)
        logger.info("[PORT] المنفذ: %s", settings.APP_PORT)

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("[STOP] إيقاف نظام Gaara Scan AI")

    # صفحة الصحة الأساسية
    @app.get("/health")
    async def health_check():
        return JSONResponse({
            "status": "healthy",
            "service": "Gaara Scan AI",
            "version": "2.0.0"
        })

    # Prometheus metrics endpoint
    @app.get("/api/v1/metrics")
    async def prometheus_metrics():
        """Prometheus metrics endpoint for monitoring"""
        if PROMETHEUS_ENABLED:
            return Response(
                content=generate_latest(),
                media_type=CONTENT_TYPE_LATEST
            )
        return JSONResponse(
            {"error": "Prometheus metrics not available"},
            status_code=503
        )

    return app
