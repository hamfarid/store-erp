# FILE: backend/src/routes/excel_templates.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
"""
مسارات قوالب Excel
"""

from flask import Blueprint, jsonify, request, send_file

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

# إنشاء Blueprint
excel_templates_bp = Blueprint("excel_templates", __name__)


@excel_templates_bp.route("/api/excel-templates/products", methods=["GET"])
def get_products_template():
    """الحصول على قالب Excel للمنتجات"""
    try:
        return jsonify({"status": "success", "message": "قالب المنتجات (قيد التطوير)"})
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على القالب: {str(e)}"}
            ),
            500,
        )


@excel_templates_bp.route("/api/excel-templates/customers", methods=["GET"])
def get_customers_template():
    """الحصول على قالب Excel للعملاء"""
    try:
        return jsonify({"status": "success", "message": "قالب العملاء (قيد التطوير)"})
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على القالب: {str(e)}"}
            ),
            500,
        )
