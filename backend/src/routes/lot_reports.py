# FILE: backend/src/routes/lot_reports.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
# ملف: /home/ubuntu/complete_inventory_system/backend/src/routes/batch_reports.py
# تقارير اللوطات المتخصصة
# All linting disabled due to complex imports and optional dependencies.

from flask import Blueprint, request, jsonify, send_file

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging
from datetime import datetime, date, timedelta
from sqlalchemy import and_, or_, desc, asc, func
from src.models.inventory import db, Lot, Product, Warehouse, StockMovement
from src.models.supplier import Supplier

# Lotm (Ministry Lot) model not yet implemented
try:
    from src.models.inventory import Lotm
except ImportError:
    Lotm = None  # Will be None if not available

# Import SalesInvoice with fallback for circular dependencies
try:
    from models.sales_advanced import SalesInvoice, SalesInvoiceItem
except (ImportError, Exception):
    SalesInvoice = None
    SalesInvoiceItem = None
import io
import csv
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

batch_reports_bp = Blueprint("batch_reports", __name__)


@batch_reports_bp.route("/reports/lot-tracking/<batch_number>", methods=["GET"])
def get_batch_tracking_report(batch_number):
    """تقرير تتبع اللوط الشامل - مشتريات، مبيعات، مخازن"""
    try:
        lot = Lot.query.filter_by(batch_number=batch_number).first()
        if not lot:
            return jsonify({"status": "error", "message": "اللوط غير موجود"}), 404

        # الحصول على جميع حركات المخزن للوط
        movements = (
            StockMovement.query.filter_by(batch_id=lot.id)
            .order_by(StockMovement.movement_date.desc())
            .all()
        )  # type: ignore

        # الحصول على المشتريات المرتبطة باللوط
        purchase_movements = StockMovement.query.filter(
            StockMovement.batch_id == lot.id,
            StockMovement.movement_type.in_(["فاتورة_مشتريات", "رصيد_افتتاحي"]),
        ).all()
        purchases_data = []
        for movement in purchase_movements:
            purchases_data.append(
                {
                    "movement_id": movement.id,
                    "reference_number": movement.reference_number,
                    "date": (
                        movement.created_at.date().isoformat()
                        if movement.created_at
                        else None
                    ),
                    "supplier_name": (
                        movement.supplier.name if movement.supplier else None
                    ),
                    "quantity": movement.quantity_in,
                    "unit_price": movement.unit_price,
                    "total_price": movement.total_amount,
                    "notes": movement.notes,
                }
            )

        # الحصول على المبيعات المرتبطة باللوط
        sale_movements = StockMovement.query.filter(
            StockMovement.batch_id == lot.id,
            StockMovement.movement_type == "فاتورة_مبيعات",
        ).all()
        sales_data = []
        for movement in sale_movements:
            sales_data.append(
                {
                    "movement_id": movement.id,
                    "reference_number": movement.reference_number,
                    "date": (
                        movement.created_at.date().isoformat()
                        if movement.created_at
                        else None
                    ),
                    "customer_name": (
                        movement.customer.name if movement.customer else None
                    ),
                    "quantity": movement.quantity_out,
                    "unit_price": movement.unit_price,
                    "total_price": movement.total_amount,
                    "notes": movement.notes,
                }
            )

        # تجميع حركات المخزن حسب النوع
        movements_by_type = {
            "purchases": [],
            "sales": [],
            "transfers": [],
            "adjustments": [],
        }

        for movement in movements:
            movement_data = {
                "id": movement.id,
                "date": movement.date.isoformat() if movement.date else None,
                "type": movement.type,
                "quantity": movement.quantity,
                "warehouse_from": (
                    movement.warehouse_from.name if movement.warehouse_from else None
                ),
                "warehouse_to": (
                    movement.warehouse_to.name if movement.warehouse_to else None
                ),
                "reference_number": movement.reference_number,
                "notes": movement.notes,
                "created_by": movement.created_by,
                "created_at": (
                    movement.created_at.isoformat() if movement.created_at else None
                ),
            }

            if movement.type in movements_by_type:
                movements_by_type[movement.type].append(movement_data)

        # حساب الإحصائيات
        total_purchased = sum(item["quantity"] for item in purchases_data)
        total_sold = sum(item["quantity"] for item in sales_data)
        total_transferred_in = sum(
            m["quantity"] for m in movements_by_type["transfers"] if m["quantity"] > 0
        )
        total_transferred_out = sum(
            abs(m["quantity"])
            for m in movements_by_type["transfers"]
            if m["quantity"] < 0
        )
        total_adjustments = sum(m["quantity"] for m in movements_by_type["adjustments"])

        # الحصول على معلومات لوط الوزارة
        ministry_batches_data = []
        if Lotm is not None:
            ministry_batches = Lotm.query.filter_by(batch_id=lot.id).all()
            ministry_batches_data = [lotm.to_dict() for lotm in ministry_batches]

        return jsonify(
            {
                "status": "success",
                "lot": lot.to_dict(),
                "ministry_batches": ministry_batches_data,
                "tracking_data": {
                    "purchases": purchases_data,
                    "sales": sales_data,
                    "movements": movements_by_type,
                },
                "statistics": {
                    "total_purchased": total_purchased,
                    "total_sold": total_sold,
                    "total_transferred_in": total_transferred_in,
                    "total_transferred_out": total_transferred_out,
                    "total_adjustments": total_adjustments,
                    "current_quantity": lot.current_quantity,
                    "quantity_percentage": lot.quantity_percentage,
                    "is_expired": lot.is_expired,
                    "days_to_expiry": lot.days_to_expiry,
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@batch_reports_bp.route("/reports/product-batches/<int:product_id>", methods=["GET"])
def get_product_batches_report(product_id):
    """تقرير شامل للوطات حسب الصنف"""
    try:
        product = Product.query.get_or_404(product_id)

        # معاملات الفلترة
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get

        # بناء الاستعلام
        query = Lot.query.filter_by(product_id=product_id)

        if not include_expired:
            query = query.filter(
                or_(Lot.expiry_date.is_(None), Lot.expiry_date >= date.today())
            )

        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)

        if supplier_id:
            query = query.filter_by(supplier_id=supplier_id)

        if status:
            query = query.filter_by(status=status)

        batches = query.order_by(Lot.batch_creation_date.desc()).all()

        # تجميع البيانات لكل لوط
        batches_data = []
        for lot in batches:
            batch_data = lot.to_dict()

            # إضافة معلومات المشتريات والمبيعات
            purchase_movements = StockMovement.query.filter(
                StockMovement.batch_id == lot.id,
                StockMovement.movement_type.in_(["فاتورة_مشتريات", "رصيد_افتتاحي"]),
            ).all()
            sale_movements = StockMovement.query.filter(
                StockMovement.batch_id == lot.id,
                StockMovement.movement_type == "فاتورة_مبيعات",
            ).all()

            batch_data["purchase_history"] = [
                {
                    "reference_number": movement.reference_number,
                    "date": (
                        movement.created_at.date().isoformat()
                        if movement.created_at
                        else None
                    ),
                    "quantity": movement.quantity_in,
                    "unit_price": movement.unit_price,
                }
                for movement in purchase_movements
            ]

            batch_data["sales_history"] = [
                {
                    "reference_number": movement.reference_number,
                    "date": (
                        movement.created_at.date().isoformat()
                        if movement.created_at
                        else None
                    ),
                    "quantity": movement.quantity_out,
                    "unit_price": movement.unit_price,
                }
                for movement in sale_movements
            ]

            # إضافة معلومات لوط الوزارة
            batch_data["ministry_batches"] = []
            if Lotm is not None:
                ministry_batches = Lotm.query.filter_by(batch_id=lot.id).all()
                batch_data["ministry_batches"] = [
                    lotm.to_dict() for lotm in ministry_batches
                ]

            batches_data.append(batch_data)

        # حساب الإحصائيات الإجمالية
        total_batches = len(batches)
        total_initial_quantity = sum(lot.initial_quantity for lot in batches)
        total_current_quantity = sum(lot.current_quantity for lot in batches)
        expired_batches = [lot for lot in batches if lot.is_expired]
        low_stock_batches = [lot for lot in batches if lot.quantity_percentage < 20]

        # إحصائيات حسب المورد
        supplier_stats = {}
        for lot in batches:
            if lot.supplier:
                supplier_name = lot.supplier.name
                if supplier_name not in supplier_stats:
                    supplier_stats[supplier_name] = {
                        "batches_count": 0,
                        "total_quantity": 0,
                        "current_quantity": 0,
                    }
                supplier_stats[supplier_name]["batches_count"] += 1
                supplier_stats[supplier_name]["total_quantity"] += lot.initial_quantity
                supplier_stats[supplier_name][
                    "current_quantity"
                ] += lot.current_quantity

        # إحصائيات حسب المخزن
        warehouse_stats = {}
        for lot in batches:
            if lot.warehouse:
                warehouse_name = lot.warehouse.name
                if warehouse_name not in warehouse_stats:
                    warehouse_stats[warehouse_name] = {
                        "batches_count": 0,
                        "total_quantity": 0,
                        "current_quantity": 0,
                    }
                warehouse_stats[warehouse_name]["batches_count"] += 1
                warehouse_stats[warehouse_name][
                    "total_quantity"
                ] += lot.initial_quantity
                warehouse_stats[warehouse_name][
                    "current_quantity"
                ] += lot.current_quantity

        return jsonify(
            {
                "status": "success",
                "product": product.to_dict(),
                "batches": batches_data,
                "statistics": {
                    "total_batches": total_batches,
                    "total_initial_quantity": total_initial_quantity,
                    "total_current_quantity": total_current_quantity,
                    "expired_batches_count": len(expired_batches),
                    "low_stock_batches_count": len(low_stock_batches),
                    "average_quantity_percentage": (
                        sum(lot.quantity_percentage for lot in batches) / total_batches
                        if total_batches > 0
                        else 0
                    ),
                    "supplier_stats": supplier_stats,
                    "warehouse_stats": warehouse_stats,
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@batch_reports_bp.route("/reports/ministry-batches-status", methods=["GET"])
def get_ministry_batches_status_report():
    """تقرير حالة لوطات الوزارة"""
    try:
        # Check if Lotm model is available
        if Lotm is None:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Ministry batch tracking not available",
                    }
                ),
                501,
            )

        # معاملات الفلترة
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get

        # بناء الاستعلام
        query = Lotm.query

        if approval_status:
            query = query.filter_by(approval_status=approval_status)

        if expired_certificates:
            query = query.filter(Lotm.certificate_expiry < date.today())

        if renewal_due:
            query = query.filter(Lotm.renewal_date <= date.today())

        ministry_batches = query.order_by(Lotm.test_date.desc()).all()

        # تجميع البيانات
        ministry_batches_data = []
        for lotm in ministry_batches:
            lotm_data = lotm.to_dict()
            # إضافة معلومات اللوط الأساسي
            lotm_data["base_lot"] = lotm.lot.to_dict() if lotm.lot else None
            ministry_batches_data.append(lotm_data)

        # حساب الإحصائيات
        total_ministry_batches = len(ministry_batches)
        approved_batches = [
            lotm for lotm in ministry_batches if lotm.approval_status == "approved"
        ]
        pending_batches = [
            lotm for lotm in ministry_batches if lotm.approval_status == "pending"
        ]
        rejected_batches = [
            lotm for lotm in ministry_batches if lotm.approval_status == "rejected"
        ]
        expired_certificates_count = len(
            [lotm for lotm in ministry_batches if lotm.is_certificate_expired]
        )
        renewal_due_count = len(
            [lotm for lotm in ministry_batches if lotm.is_renewal_due]
        )

        # متوسط نقاط الجودة
        quality_scores = [
            lotm.quality_score for lotm in ministry_batches if lotm.quality_score
        ]
        average_quality_score = (
            sum(quality_scores) / len(quality_scores) if quality_scores else 0
        )

        return jsonify(
            {
                "status": "success",
                "ministry_batches": ministry_batches_data,
                "statistics": {
                    "total_ministry_batches": total_ministry_batches,
                    "approved_count": len(approved_batches),
                    "pending_count": len(pending_batches),
                    "rejected_count": len(rejected_batches),
                    "expired_certificates_count": expired_certificates_count,
                    "renewal_due_count": renewal_due_count,
                    "average_quality_score": round(average_quality_score, 2),
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@batch_reports_bp.route("/reports/lot-movements/<batch_number>", methods=["GET"])
def get_batch_movements_report(batch_number):
    """تقرير حركات اللوط التفصيلي"""
    try:
        lot = Lot.query.filter_by(batch_number=batch_number).first()
        if not lot:
            return jsonify({"status": "error", "message": "اللوط غير موجود"}), 404

        # الحصول على جميع حركات المخزن
        movements = (
            StockMovement.query.filter_by(batch_id=lot.id)
            .order_by(StockMovement.created_at.desc())
            .all()
        )

        # تجميع الحركات حسب التاريخ والنوع
        movements_data = []
        running_balance = 0

        for movement in movements:
            running_balance += movement.quantity

            movement_data = {
                "id": movement.id,
                "date": movement.date.isoformat() if movement.date else None,
                "type": movement.type,
                "type_display": {
                    "purchase": "شراء",
                    "sale": "بيع",
                    "transfer": "نقل",
                    "adjustment": "تسوية",
                }.get(movement.type, movement.type),
                "quantity": movement.quantity,
                "running_balance": running_balance,
                "warehouse_from": (
                    movement.warehouse_from.name if movement.warehouse_from else None
                ),
                "warehouse_to": (
                    movement.warehouse_to.name if movement.warehouse_to else None
                ),
                "reference_number": movement.reference_number,
                "notes": movement.notes,
                "created_by": movement.created_by,
                "created_at": (
                    movement.created_at.isoformat() if movement.created_at else None
                ),
            }

            movements_data.append(movement_data)

        # عكس الترتيب للحصول على الرصيد الصحيح
        movements_data.reverse()

        # إعادة حساب الرصيد الجاري
        running_balance = 0
        for movement in movements_data:
            running_balance += movement["quantity"]
            movement["running_balance"] = running_balance

        return jsonify(
            {
                "status": "success",
                "lot": lot.to_dict(),
                "movements": movements_data,
                "summary": {
                    "total_movements": len(movements_data),
                    "final_balance": lot.current_quantity,
                    "initial_quantity": lot.initial_quantity,
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@batch_reports_bp.route("/reports/export/lot-tracking/<batch_number>", methods=["GET"])
def export_batch_tracking_report(batch_number):
    """تصدير تقرير تتبع اللوط إلى PDF"""
    try:
        lot = Lot.query.filter_by(batch_number=batch_number).first()
        if not lot:
            return jsonify({"status": "error", "message": "اللوط غير موجود"}), 404

        # إنشاء ملف PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))

        # تحديد الأنماط
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=16,
            spaceAfter=30,
            alignment=1,  # وسط
        )

        # محتوى التقرير
        story = []

        # العنوان
        title = Paragraph(f"تقرير تتبع اللوط: {lot.batch_number}", title_style)
        story.append(title)
        story.append(Spacer(1, 20))

        # معلومات اللوط الأساسية
        batch_info_data = [
            ["رقم اللوط", lot.batch_number],
            ["اسم المنتج", lot.product.name if lot.product else ""],
            ["المخزن", lot.warehouse.name if lot.warehouse else ""],
            [
                "تاريخ الإنشاء",
                (
                    lot.batch_creation_date.strftime("%Y-%m-%d")
                    if lot.batch_creation_date
                    else ""
                ),
            ],
            ["الكمية الأصلية", str(lot.initial_quantity)],
            ["الكمية الحالية", str(lot.current_quantity)],
            ["المورد", lot.supplier.name if lot.supplier else ""],
        ]

        batch_info_table = Table(batch_info_data, colWidths=[150, 200])
        batch_info_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(batch_info_table)
        story.append(Spacer(1, 30))

        # حركات المخزن
        movements = (
            StockMovement.query.filter_by(batch_id=lot.id)
            .order_by(StockMovement.created_at.desc())
            .all()
        )

        if movements:
            movements_title = Paragraph("حركات المخزن", styles["Heading2"])
            story.append(movements_title)
            story.append(Spacer(1, 10))

            movements_data = [["التاريخ", "النوع", "الكمية", "المرجع", "ملاحظات"]]

            for movement in movements:
                movements_data.append(
                    [
                        movement.date.strftime("%Y-%m-%d") if movement.date else "",
                        movement.type,
                        str(movement.quantity),
                        movement.reference_number or "",
                        movement.notes or "",
                    ]
                )

            movements_table = Table(movements_data, colWidths=[80, 80, 80, 100, 150])
            movements_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(movements_table)

        # بناء المستند
        doc.build(story)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'batch_tracking_{batch_number}_{datetime.now().strftime("%Y%m%d")}.pd',
            mimetype="application/pdf",
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
