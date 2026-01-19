"""
إعداد المسارات - تسجيل جميع مسارات API
Routes Setup - Register all API routes
"""

from fastapi import FastAPI
from flask import Flask
from src.api.health import router as health_router
from src.api.auth import router as auth_router
from src.api.upload import router as upload_router
from src.api.diagnosis import router as diagnosis_router
from src.api.reports import router as reports_router
from src.api.model_management import router as model_management_router

# استيراد APIs الجديدة
try:
    from src.api.generative_ai import generative_ai_bp
    from src.api.advanced_vision import advanced_vision_bp
except ImportError as e:
    print(f"Warning: Could not import new APIs: {e}")
    generative_ai_bp = None
    advanced_vision_bp = None

def setup_routes(app: FastAPI):
    """
    إعداد جميع مسارات التطبيق لـ FastAPI
    Setup all application routes for FastAPI
    """
    
    # المسارات الأساسية
    app.include_router(
        health_router,
        prefix="/api/v1",
        tags=["Health"]
    )
    
    # مسارات المصادقة
    app.include_router(
        auth_router,
        prefix="/api/v1/auth",
        tags=["Authentication"]
    )
    
    # مسارات رفع الملفات
    app.include_router(
        upload_router,
        prefix="/api/v1/upload",
        tags=["File Upload"]
    )
    
    # مسارات التشخيص
    app.include_router(
        diagnosis_router,
        prefix="/api/v1/diagnosis",
        tags=["Plant Diagnosis"]
    )
    
    # مسارات التقارير
    app.include_router(
        reports_router,
        prefix="/api/v1/reports",
        tags=["Reports"]
    )
    
    # مسارات إدارة النماذج
    app.include_router(
        model_management_router,
        prefix="/api/v1/models",
        tags=["Model Management"]
    )

def setup_flask_routes(app: Flask):
    """
    إعداد مسارات Flask للتقنيات المتقدمة
    Setup Flask routes for advanced technologies
    """
    
    # تسجيل APIs الجديدة
    if generative_ai_bp:
        app.register_blueprint(generative_ai_bp)
        print("Registered Generative AI API")
    
    if advanced_vision_bp:
        app.register_blueprint(advanced_vision_bp)
        print("Registered Advanced Vision API")
    
    # إضافة CORS للتطبيق
    try:
        from flask_cors import CORS
        CORS(app, origins="*")
        print("CORS enabled for Flask app")
    except ImportError:
        print("Warning: flask-cors not available")

def setup_hybrid_routes(fastapi_app: FastAPI, flask_app: Flask):
    """
    إعداد مسارات هجينة لكل من FastAPI و Flask
    Setup hybrid routes for both FastAPI and Flask
    """
    
    # إعداد مسارات FastAPI
    setup_routes(fastapi_app)
    
    # إعداد مسارات Flask
    setup_flask_routes(flask_app)
    
    print("Hybrid routing setup completed")
