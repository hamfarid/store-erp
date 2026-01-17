#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.56: Export Routes

API endpoints for exporting data to various formats.
"""

import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from src.routes.auth_unified import token_required
from src.permissions import require_permission, Permissions
from src.utils.export import (
    create_exporter,
    get_content_type,
    get_file_extension,
    ExportConfig,
    ExportColumn,
    PRODUCTS_EXPORT_CONFIG,
    INVOICES_EXPORT_CONFIG,
    CUSTOMERS_EXPORT_CONFIG,
)

logger = logging.getLogger(__name__)

export_bp = Blueprint("export", __name__, url_prefix="/api/export")


# =============================================================================
# Helper Functions
# =============================================================================


def create_export_response(data: bytes, filename: str, format: str):
    """Create Flask response for file download."""
    response = make_response(data)
    response.headers["Content-Type"] = get_content_type(format)
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{filename}{get_file_extension(format)}"'
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# =============================================================================
# Routes
# =============================================================================


@export_bp.route("/products", methods=["GET"])
@token_required
@require_permission(Permissions.REPORTS_EXPORT)
def export_products():
    """
    Export products to Excel, PDF, CSV, or JSON.

    Query params:
        format: xlsx, pdf, csv, json (default: xlsx)
        search: Filter by name/sku
        category_id: Filter by category
    """
    from src.models.product import Product
    from src.database import db

    format = request.args.get("format", "xlsx")
    search = request.args.get("search", "")
    category_id = request.args.get("category_id", type=int)

    # Build query
    query = Product.query

    if search:
        query = query.filter(
            db.or_(Product.name.ilike(f"%{search}%"), Product.sku.ilike(f"%{search}%"))
        )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    products = query.all()

    # Convert to dicts
    data = [p.to_dict() for p in products]

    # Export
    try:
        exporter = create_exporter(format, PRODUCTS_EXPORT_CONFIG)
        export_data = exporter.export(data)

        filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return create_export_response(export_data, filename, format)

    except ImportError as e:
        return (
            jsonify(
                {"success": False, "error": {"code": "EXPORT_ERROR", "message": str(e)}}
            ),
            500,
        )
    except Exception as e:
        logger.error(f"Export error: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "EXPORT_ERROR",
                        "message": "Failed to export data",
                    },
                }
            ),
            500,
        )


@export_bp.route("/invoices", methods=["GET"])
@token_required
@require_permission(Permissions.REPORTS_EXPORT)
def export_invoices():
    """
    Export invoices to Excel, PDF, CSV, or JSON.

    Query params:
        format: xlsx, pdf, csv, json (default: xlsx)
        type: sale, purchase
        status: paid, pending, overdue
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
    """
    from src.models.invoice import Invoice
    from src.database import db

    format = request.args.get("format", "xlsx")
    invoice_type = request.args.get("type")
    status = request.args.get("status")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    # Build query
    query = Invoice.query

    if invoice_type:
        query = query.filter(Invoice.type == invoice_type)

    if status:
        query = query.filter(Invoice.status == status)

    if from_date:
        query = query.filter(Invoice.created_at >= from_date)

    if to_date:
        query = query.filter(Invoice.created_at <= to_date)

    invoices = query.order_by(Invoice.created_at.desc()).all()

    # Convert to dicts
    data = [i.to_dict() for i in invoices]

    # Export
    try:
        exporter = create_exporter(format, INVOICES_EXPORT_CONFIG)
        export_data = exporter.export(data)

        filename = f"invoices_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return create_export_response(export_data, filename, format)

    except Exception as e:
        logger.error(f"Export error: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "EXPORT_ERROR",
                        "message": "Failed to export data",
                    },
                }
            ),
            500,
        )


@export_bp.route("/customers", methods=["GET"])
@token_required
@require_permission(Permissions.REPORTS_EXPORT)
def export_customers():
    """
    Export customers to Excel, PDF, CSV, or JSON.

    Query params:
        format: xlsx, pdf, csv, json (default: xlsx)
        search: Filter by name/email/phone
    """
    from src.models.partners import Customer
    from src.database import db

    format = request.args.get("format", "xlsx")
    search = request.args.get("search", "")

    # Build query
    query = Customer.query

    if search:
        query = query.filter(
            db.or_(
                Customer.name.ilike(f"%{search}%"),
                Customer.email.ilike(f"%{search}%"),
                Customer.phone.ilike(f"%{search}%"),
            )
        )

    customers = query.all()

    # Convert to dicts
    data = [c.to_dict() for c in customers]

    # Export
    try:
        exporter = create_exporter(format, CUSTOMERS_EXPORT_CONFIG)
        export_data = exporter.export(data)

        filename = f"customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return create_export_response(export_data, filename, format)

    except Exception as e:
        logger.error(f"Export error: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "EXPORT_ERROR",
                        "message": "Failed to export data",
                    },
                }
            ),
            500,
        )


@export_bp.route("/suppliers", methods=["GET"])
@token_required
@require_permission(Permissions.REPORTS_EXPORT)
def export_suppliers():
    """Export suppliers to various formats."""
    from src.models.partners import Supplier
    from src.database import db

    format = request.args.get("format", "xlsx")
    search = request.args.get("search", "")

    query = Supplier.query

    if search:
        query = query.filter(
            db.or_(
                Supplier.name.ilike(f"%{search}%"), Supplier.email.ilike(f"%{search}%")
            )
        )

    suppliers = query.all()
    data = [s.to_dict() for s in suppliers]

    config = ExportConfig(
        title="Suppliers Report",
        columns=[
            ExportColumn("id", "ID", 8, "number"),
            ExportColumn("name", "Name", 25),
            ExportColumn("email", "Email", 25),
            ExportColumn("phone", "Phone", 15),
            ExportColumn("contact_person", "Contact Person", 20),
            ExportColumn("balance", "Balance", 12, "currency"),
        ],
        include_totals=True,
        totals_columns=["balance"],
    )

    try:
        exporter = create_exporter(format, config)
        export_data = exporter.export(data)

        filename = f"suppliers_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return create_export_response(export_data, filename, format)

    except Exception as e:
        logger.error(f"Export error: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "EXPORT_ERROR",
                        "message": "Failed to export data",
                    },
                }
            ),
            500,
        )


@export_bp.route("/custom", methods=["POST"])
@token_required
@require_permission(Permissions.REPORTS_ADVANCED)
def export_custom():
    """
    Export custom data with user-defined columns.

    Request body:
    {
        "title": "Custom Report",
        "format": "xlsx",
        "columns": [
            {"key": "name", "label": "Name", "width": 25},
            {"key": "value", "label": "Value", "format": "currency"}
        ],
        "data": [...],
        "include_totals": true,
        "totals_columns": ["value"]
    }
    """
    body = request.get_json()

    title = body.get("title", "Custom Export")
    format = body.get("format", "xlsx")
    columns_data = body.get("columns", [])
    data = body.get("data", [])
    include_totals = body.get("include_totals", False)
    totals_columns = body.get("totals_columns", [])

    if not columns_data:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Columns are required",
                    },
                }
            ),
            400,
        )

    if not data:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Data is required",
                    },
                }
            ),
            400,
        )

    # Build config
    columns = [
        ExportColumn(
            key=col.get("key"),
            label=col.get("label", col.get("key")),
            width=col.get("width", 15),
            format=col.get("format"),
        )
        for col in columns_data
    ]

    config = ExportConfig(
        title=title,
        columns=columns,
        include_totals=include_totals,
        totals_columns=totals_columns,
    )

    try:
        exporter = create_exporter(format, config)
        export_data = exporter.export(data)

        filename = f"custom_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return create_export_response(export_data, filename, format)

    except Exception as e:
        logger.error(f"Export error: {e}")
        return (
            jsonify(
                {"success": False, "error": {"code": "EXPORT_ERROR", "message": str(e)}}
            ),
            500,
        )


__all__ = ["export_bp"]
