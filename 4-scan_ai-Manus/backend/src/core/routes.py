"""
إعداد المسارات - تسجيل جميع مسارات API
Routes Setup - Register all API routes
"""

from fastapi import FastAPI

# Import new v1 API routes (canonical).
# IMPORTANT: import each router independently so one heavy dependency failure
# (e.g., numpy/cv2) doesn't disable all core APIs like auth/health.
from importlib import import_module


def _import_router(module_path: str):
    try:
        mod = import_module(module_path)
        return getattr(mod, "router")
    except Exception as e:  # pragma: no cover
        print(f"Warning: Could not import {module_path}: {e}")
        return None


analytics_router = _import_router("src.api.v1.analytics")
auth_v1_router = _import_router("src.api.v1.auth")
breeding_router = _import_router("src.api.v1.breeding")
companies_router = _import_router("src.api.v1.companies")
crops_router = _import_router("src.api.v1.crops")
diagnosis_v1_router = _import_router("src.api.v1.diagnosis")
diseases_router = _import_router("src.api.v1.diseases")
equipment_router = _import_router("src.api.v1.equipment")
farms_router = _import_router("src.api.v1.farms")
health_v1_router = _import_router("src.api.v1.health")
inventory_router = _import_router("src.api.v1.inventory")
reports_v1_router = _import_router("src.api.v1.reports")
sensors_router = _import_router("src.api.v1.sensors")
settings_router = _import_router("src.api.v1.settings")
setup_router = _import_router("src.api.v1.setup")
upload_v1_router = _import_router("src.api.v1.upload")
users_router = _import_router("src.api.v1.users")

# Optional/auxiliary v1 routers (may require heavier deps)
try:
    from ..api.v1.data_management import router as data_management_router
except Exception as e:  # pragma: no cover
    print(f"Warning: Could not import Data Management API (v1): {e}")
    data_management_router = None

try:
    from ..api.v1.scheduled_updates import router as scheduled_updates_router
except Exception as e:  # pragma: no cover
    print(f"Warning: Could not import Scheduled Updates API (v1): {e}")
    scheduled_updates_router = None

try:
    from ..api.v1.crawler import router as crawler_router
except Exception as e:  # pragma: no cover
    print(f"Warning: Could not import Image Crawler API (v1): {e}")
    crawler_router = None

try:
    from ..api.v1.ml_diagnosis import router as ml_diagnosis_router
except Exception as e:  # pragma: no cover
    print(f"Warning: Could not import ML Diagnosis API (v1): {e}")
    ml_diagnosis_router = None

try:
    from ..api.v1.two_factor import router as two_factor_router
except Exception as e:  # pragma: no cover
    print(f"Warning: Could not import Two-Factor Authentication API (v1): {e}")
    two_factor_router = None

# Import legacy routes (if they exist) - These are deprecated and optional
try:
    from src.api.auth import router as auth_router
    from src.api.diagnosis import router as diagnosis_router
    from src.api.health import router as health_router
    from src.api.model_management import router as model_management_router
    from src.api.reports import router as reports_router
    from src.api.upload import router as upload_router
except ImportError:
    # Legacy APIs are deprecated - v1 APIs are used instead
    health_router = None
    auth_router = None
    upload_router = None
    diagnosis_router = None
    reports_router = None
    model_management_router = None

# استيراد APIs الجديدة (اختيارية)
# Import new APIs (optional - advanced features)
try:
    from src.api.advanced_vision import advanced_vision_bp
    from src.api.generative_ai import generative_ai_bp
except ImportError:
    # Advanced vision and generative AI are optional features
    generative_ai_bp = None
    advanced_vision_bp = None


def setup_routes(app: FastAPI):
    """
    إعداد جميع مسارات التطبيق لـ FastAPI
    Setup all application routes for FastAPI
    """

    # ============================================================================
    # NEW V1 API ROUTES (Canonical - Production Ready)
    # ============================================================================

    # Health Check API (v1)
    if health_v1_router:
        app.include_router(health_v1_router)
        print("[OK] Registered: Health Check API (v1)")

    # Authentication API (v1)
    if auth_v1_router:
        app.include_router(auth_v1_router)
        print("[OK] Registered: Authentication API (v1)")

    # Upload API (v1)
    if upload_v1_router:
        app.include_router(upload_v1_router)
        print("[OK] Registered: Upload API (v1)")

    # Farms API (v1)
    if farms_router:
        app.include_router(farms_router)
        print("[OK] Registered: Farms API (v1)")

    # Diagnosis API (v1)
    if diagnosis_v1_router:
        app.include_router(diagnosis_v1_router)
        print("[OK] Registered: Diagnosis API (v1)")

    # Reports API (v1)
    if reports_v1_router:
        app.include_router(reports_v1_router)
        print("[OK] Registered: Reports API (v1)")

    # Crops API (v1)
    if crops_router:
        app.include_router(crops_router)
        print("[OK] Registered: Crops API (v1)")

    # Diseases API (v1)
    if diseases_router:
        app.include_router(diseases_router)
        print("[OK] Registered: Diseases API (v1)")

    # Sensors API (v1)
    if sensors_router:
        app.include_router(sensors_router)
        print("[OK] Registered: Sensors API (v1)")

    # Equipment API (v1)
    if equipment_router:
        app.include_router(equipment_router)
        print("[OK] Registered: Equipment API (v1)")

    # Inventory API (v1)
    if inventory_router:
        app.include_router(inventory_router)
        print("[OK] Registered: Inventory API (v1)")

    # Users API (v1)
    if users_router:
        app.include_router(users_router)
        print("[OK] Registered: Users API (v1)")

    # Companies API (v1)
    if companies_router:
        app.include_router(companies_router)
        print("[OK] Registered: Companies API (v1)")

    # Breeding API (v1)
    if breeding_router:
        app.include_router(breeding_router)
        print("[OK] Registered: Breeding API (v1)")

    # Analytics API (v1)
    if analytics_router:
        app.include_router(analytics_router)
        print("[OK] Registered: Analytics API (v1)")

    # Settings API (v1)
    if settings_router:
        app.include_router(settings_router)
        print("[OK] Registered: Settings API (v1)")

    # Setup Wizard API (v1)
    if setup_router:
        app.include_router(setup_router)
        print("[OK] Registered: Setup Wizard API (v1)")

    # =========================================================================
    # AUXILIARY V1 ROUTES (mounted under /api/v1)
    # =========================================================================

    if data_management_router:
        app.include_router(data_management_router, prefix="/api/v1")
        print("[OK] Registered: Data Management API (v1)")

    if scheduled_updates_router:
        app.include_router(scheduled_updates_router, prefix="/api/v1")
        print("[OK] Registered: Scheduled Updates API (v1)")

    if crawler_router:
        app.include_router(crawler_router, prefix="/api/v1")
        print("[OK] Registered: Image Crawler API (v1)")

    if ml_diagnosis_router:
        app.include_router(ml_diagnosis_router, prefix="/api/v1")
        print("[OK] Registered: ML Diagnosis API (v1)")

    if two_factor_router:
        app.include_router(two_factor_router, prefix="/api/v1")
        print("[OK] Registered: Two-Factor Authentication API (v1)")

    # ============================================================================
    # LEGACY ROUTES (For backward compatibility)
    # ============================================================================

    # المسارات الأساسية
    if health_router:
        app.include_router(
            health_router,
            prefix="/api/v1",
            tags=["Health"]
        )
        print("[OK] Registered: Health API (legacy)")

    # مسارات المصادقة
    if auth_router:
        app.include_router(
            auth_router,
            prefix="/api/v1/auth",
            tags=["Authentication"]
        )
        print("[OK] Registered: Auth API (legacy)")

    # مسارات رفع الملفات
    if upload_router:
        app.include_router(
            upload_router,
            prefix="/api/v1/upload",
            tags=["File Upload"]
        )
        print("[OK] Registered: Upload API (legacy)")

    # مسارات التشخيص
    if diagnosis_router:
        app.include_router(
            diagnosis_router,
            prefix="/api/v1/diagnosis",
            tags=["Plant Diagnosis"]
        )
        print("[OK] Registered: Diagnosis API (legacy)")

    # مسارات التقارير
    if reports_router:
        app.include_router(
            reports_router,
            prefix="/api/v1/reports",
            tags=["Reports"]
        )
        print("[OK] Registered: Reports API (legacy)")

    # مسارات إدارة النماذج
    if model_management_router:
        app.include_router(
            model_management_router,
            prefix="/api/v1/models",
            tags=["Model Management"]
        )
        print("[OK] Registered: Model Management API (legacy)")


# Flask routes are deprecated - keeping stub for backwards compatibility
def setup_flask_routes(app):
    """
    إعداد مسارات Flask للتقنيات المتقدمة (deprecated)
    Setup Flask routes for advanced technologies (deprecated)

    Note: This function is deprecated. The project now uses FastAPI exclusively.
    """
    print("Warning: Flask routes are deprecated. Use FastAPI routes instead.")


def setup_hybrid_routes(fastapi_app: FastAPI, flask_app=None):
    """
    إعداد مسارات هجينة لكل من FastAPI و Flask (deprecated)
    Setup hybrid routes for both FastAPI and Flask (deprecated)

    Note: Flask support is deprecated. This function now only sets up FastAPI routes.
    """

    # إعداد مسارات FastAPI
    setup_routes(fastapi_app)

    if flask_app:
        print("Warning: Flask routes are deprecated. Ignoring flask_app parameter.")

    print("Routing setup completed (FastAPI only)")
