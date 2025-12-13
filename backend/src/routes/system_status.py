# FILE: backend/src/routes/system_status.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

"""
نقطة نهاية حالة النظام
System Status Endpoint
"""

from flask import Blueprint, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from datetime import datetime
import os
import sys

# إنشاء Blueprint
status_bp = Blueprint("status", __name__)


@status_bp.route("/api/system/status", methods=["GET"])
def get_system_status():
    """الحصول على حالة النظام"""
    try:
        # فحص النماذج المتوفرة
        available_models = []
        model_errors = []

        models_to_check = [
            ("models.user", "User"),
            ("models.customer", "Customer"),
            ("models.supplier", "Supplier"),
            ("models.inventory", "Product"),
            ("models.inventory", "Category"),
            ("models.inventory", "Warehouse"),
        ]

        for module_name, model_name in models_to_check:
            try:
                module = __import__(module_name, fromlist=[model_name])
                model = getattr(module, model_name)
                available_models.append(f"{module_name}.{model_name}")
            except Exception as e:
                model_errors.append(f"{module_name}.{model_name}: {str(e)}")

        # فحص قاعدة البيانات
        db_status = "غير متوفرة"
        try:
            from database import db

            db_status = "متوفرة"
        except Exception as e:
            db_status = f"خطأ: {str(e)}"

        # فحص الخدمات
        services_status = {
            "database": db_status,
            "models_available": len(available_models),
            "models_errors": len(model_errors),
            "python_version": sys.version,
            "flask_env": os.environ.get("FLASK_ENV", "development"),
        }

        return jsonify(
            {
                "success": True,
                "data": {
                    "system_name": "Complete Inventory Management System",
                    "version": "1.5.0",
                    "status": "running",
                    "timestamp": datetime.now().isoformat(),
                    "services": services_status,
                    "available_models": available_models,
                    "model_errors": model_errors,
                    "temp_api_available": True,
                    "recommendations": [
                        "استخدم /api/temp/* للوصول للبيانات التجريبية",
                        "تحقق من ملفات النماذج في src/models/",
                        "راجع سجلات الخادم للأخطاء التفصيلية",
                    ],
                },
                "message": "تم الحصول على حالة النظام بنجاح",
            }
        )

    except Exception as e:
        return error_response(
            message="خطأ في الحصول على حالة النظام",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@status_bp.route("/api/system/health", methods=["GET"])
def health_check():
    """فحص صحة النظام"""
    try:
        return jsonify(
            {
                "success": True,
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "message": "النظام يعمل بشكل طبيعي",
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "success": False,
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )
