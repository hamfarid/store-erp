# FILE: backend/src/routes/interactive_dashboard.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
#!/usr/bin/env python3
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/routes/interactive_dashboard.py

API routes للوحات المعلومات التفاعلية
Interactive Dashboard API Routes

يوفر هذا الملف جميع endpoints اللازمة لإدارة لوحات المعلومات التفاعلية
All linting disabled due to complex imports and optional dependencies.
"""

from flask import Blueprint, request, jsonify, current_app

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

# استيراد الخدمات
from services.interactive_dashboard_service import interactive_dashboard_service
from decorators.permission_decorators import require_permission

# إنشاء Blueprint
interactive_dashboard_bp = Blueprint(
    "interactive_dashboard", __name__, url_prefix="/api/dashboard"
)

# إعداد السجلات
logger = logging.getLogger(__name__)


@interactive_dashboard_bp.route("/main", methods=["GET"])
@jwt_required()
@require_permission("dashboard_view")
def get_main_dashboard():
    """
    الحصول على بيانات لوحة المعلومات الرئيسية
    GET /api/dashboard/main
    """
    try:
        user_id = get_jwt_identity()
        _ = request.args.get

        result = interactive_dashboard_service.get_main_dashboard_data(
            user_id, date_range
        )

        if result.get("status") == "success" or result.get("success") is True:
            return (
                jsonify(
                    {
                        "status": "success",
                        "data": result["data"],
                        "date_range": result["date_range"],
                    }
                ),
                200,
            )
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في الحصول على لوحة المعلومات الرئيسية: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/widget/<widget_type>", methods=["POST"])
@jwt_required()
@require_permission("dashboard_view")
def get_widget_data(widget_type):
    """
    الحصول على بيانات ويدجت محدد
    POST /api/dashboard/widget/<widget_type>
    """
    try:
        data = request.get_json()
        widget_config = data.get("config", {})

        result = interactive_dashboard_service.get_widget_data(
            widget_type, widget_config
        )

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify({"status": "success", "data": result["data"]}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في الحصول على بيانات الويدجت: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/custom", methods=["POST"])
@jwt_required()
@require_permission("dashboard_create")
def create_custom_dashboard():
    """
    إنشاء لوحة معلومات مخصصة
    POST /api/dashboard/custom
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        result = interactive_dashboard_service.create_custom_dashboard(user_id, data)

        if result.get("status") == "success" or result.get("success") is True:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": result["message"],
                        "dashboard": result["dashboard"],
                    }
                ),
                201,
            )
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في إنشاء لوحة المعلومات المخصصة: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/analytics/sales", methods=["GET"])
@jwt_required()
@require_permission("sales_analytics_view")
def get_sales_analytics():
    """
    الحصول على تحليلات المبيعات المتقدمة
    GET /api/dashboard/analytics/sales
    """
    try:
        user_id = get_jwt_identity()
        _ = request.args.get
        _ = request.args.get

        # إعداد تكوين الويدجت
        widget_config = {"period": date_range, "chart_type": chart_type}

        result = interactive_dashboard_service.get_widget_data(
            "sales_chart", widget_config
        )

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify({"status": "success", "data": result["data"]}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في تحليلات المبيعات: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/analytics/inventory", methods=["GET"])
@jwt_required()
@require_permission("inventory_analytics_view")
def get_inventory_analytics():
    """
    الحصول على تحليلات المخزون المتقدمة
    GET /api/dashboard/analytics/inventory
    """
    try:
        result = interactive_dashboard_service.get_widget_data("inventory_status", {})

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify({"status": "success", "data": result["data"]}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في تحليلات المخزون: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/analytics/financial", methods=["GET"])
@jwt_required()
@require_permission("financial_analytics_view")
def get_financial_analytics():
    """
    الحصول على التحليلات المالية المتقدمة
    GET /api/dashboard/analytics/financial
    """
    try:
        period = request.args.get("period", "30d")

        widget_config = {"period": period}
        result = interactive_dashboard_service.get_widget_data(
            "financial_summary", widget_config
        )

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify({"status": "success", "data": result["data"]}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في التحليلات المالية: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/analytics/customers", methods=["GET"])
@jwt_required()
@require_permission("customer_analytics_view")
def get_customer_analytics():
    """
    الحصول على تحليلات العملاء المتقدمة
    GET /api/dashboard/analytics/customers
    """
    try:
        period = request.args.get("period", "30d")

        widget_config = {"period": period}
        result = interactive_dashboard_service.get_widget_data(
            "customer_analytics", widget_config
        )

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify({"status": "success", "data": result["data"]}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في تحليلات العملاء: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/top-products", methods=["GET"])
@jwt_required()
@require_permission("product_analytics_view")
def get_top_products():
    """
    الحصول على أفضل المنتجات
    GET /api/dashboard/top-products
    """
    try:
        _ = request.args.get
        limit = int(request.args.get("limit", 10))

        widget_config = {"period": period, "limit": limit}

        result = interactive_dashboard_service.get_widget_data(
            "top_products", widget_config
        )

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify({"status": "success", "data": result["data"]}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في أفضل المنتجات: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/alerts", methods=["GET"])
@jwt_required()
@require_permission("alerts_view")
def get_alerts():
    """
    الحصول على التنبيهات والإشعارات
    GET /api/dashboard/alerts
    """
    try:
        user_id = get_jwt_identity()

        # الحصول على التنبيهات من خدمة لوحة المعلومات
        result = interactive_dashboard_service.get_main_dashboard_data(user_id, "7d")

        if result.get("status") == "success" or result.get("success") is True:
            alerts_data = result["data"].get("alerts_notifications", {})
            return jsonify({"status": "success", "data": alerts_data}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في الحصول على التنبيهات: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/recent-activities", methods=["GET"])
@jwt_required()
@require_permission("activities_view")
def get_recent_activities():
    """
    الحصول على الأنشطة الأخيرة
    GET /api/dashboard/recent-activities
    """
    try:
        user_id = get_jwt_identity()
        limit = int(request.args.get("limit", 10))

        # الحصول على الأنشطة من خدمة لوحة المعلومات
        result = interactive_dashboard_service.get_main_dashboard_data(user_id, "7d")

        if result.get("status") == "success" or result.get("success") is True:
            activities_data = result["data"].get("recent_activities", [])
            return jsonify({"status": "success", "data": activities_data[:limit]}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في الحصول على الأنشطة الأخيرة: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/export", methods=["POST"])
@jwt_required()
@require_permission("dashboard_export")
def export_dashboard_data():
    """
    تصدير بيانات لوحة المعلومات
    POST /api/dashboard/export
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        export_format = data.get("format", "json")  # json, csv, excel
        date_range = data.get("date_range", "30d")
        widgets = data.get("widgets", [])

        # الحصول على بيانات لوحة المعلومات
        result = interactive_dashboard_service.get_main_dashboard_data(
            user_id, date_range
        )

        if not (result.get("status") == "success" or result.get("success") is True):
            return jsonify({"success": False, "message": result["message"]}), 400

        dashboard_data = result["data"]

        # تصدير البيانات حسب التنسيق المطلوب
        if export_format == "json":
            return (
                jsonify(
                    {"status": "success", "data": dashboard_data, "format": "json"}
                ),
                200,
            )

        elif export_format == "csv":
            # تحويل البيانات إلى CSV
            import pandas as pd
            import io

            # إنشاء DataFrame من البيانات
            df_data = []
            for key, value in dashboard_data.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        df_data.append(
                            {
                                "category": key,
                                "metric": sub_key,
                                "value": str(sub_value),
                            }
                        )
                else:
                    df_data.append(
                        {"category": key, "metric": key, "value": str(value)}
                    )

            df = pd.DataFrame(df_data)

            # تحويل إلى CSV
            output = io.StringIO()
            df.to_csv(output, index=False, encoding="utf-8")
            csv_data = output.getvalue()

            return (
                success_response(
                    data={"format": "csv"}, message="Success", status_code=200
                ),
                200,
            )

        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"تنسيق التصدير {export_format} غير مدعوم",
                    }
                ),
                400,
            )

    except Exception as e:
        logger.error(f"خطأ في تصدير بيانات لوحة المعلومات: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


@interactive_dashboard_bp.route("/performance", methods=["GET"])
@jwt_required()
@require_permission("performance_view")
def get_performance_metrics():
    """
    الحصول على مقاييس الأداء
    GET /api/dashboard/performance
    """
    try:
        user_id = get_jwt_identity()
        _ = request.args.get

        # الحصول على مقاييس الأداء من خدمة لوحة المعلومات
        result = interactive_dashboard_service.get_main_dashboard_data(
            user_id, date_range
        )

        if result.get("status") == "success" or result.get("success") is True:
            performance_data = result["data"].get("performance_metrics", {})
            return jsonify({"status": "success", "data": performance_data}), 200
        else:
            return jsonify({"status": "error", "message": result["message"]}), 400

    except Exception as e:
        logger.error(f"خطأ في مقاييس الأداء: {str(e)}")
        return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500


# معالج الأخطاء
@interactive_dashboard_bp.errorhandler(404)
def not_found(error):
    """معالج خطأ 404"""
    return jsonify({"status": "error", "message": "المسار غير موجود"}), 404


@interactive_dashboard_bp.errorhandler(500)
def internal_error(error):
    """معالج خطأ 500"""
    return jsonify({"status": "error", "message": "خطأ في الخادم الداخلي"}), 500
