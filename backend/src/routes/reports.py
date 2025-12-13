# FILE: backend/src/routes/reports.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# pylint: disable=all
# flake8: noqa
"""
APIs نظام التقارير والطباعة
/home/ubuntu/inventory_management_system/src/routes/reports.py
"""

import io
import json
import os
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, make_response, request, send_file

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import func, or_
from src.models.inventory import Category
from src.models.product_unified import Product
from src.models.warehouse_unified import Warehouse
from src.models.supporting_models import StockMovement
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.database import db

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/api/reports", methods=["GET"])
def get_available_reports():
    """
    الحصول على قائمة التقارير المتاحة
    Get list of available reports
    """
    try:
        reports_list = [
            {
                "id": "stock_valuation",
                "name": "تقرير تقييم المخزون",
                "name_en": "Stock Valuation Report",
                "endpoint": "/stock-valuation",
                "method": "GET",
                "description": "تقرير شامل بقيمة المخزون الحالي",
            },
            {
                "id": "low_stock",
                "name": "تقرير المخزون المنخفض",
                "name_en": "Low Stock Report",
                "endpoint": "/low-stock",
                "method": "GET",
                "description": "المنتجات التي وصلت للحد الأدنى",
            },
            {
                "id": "inventory",
                "name": "تقرير الجرد",
                "name_en": "Inventory Report",
                "endpoint": "/inventory-report",
                "method": "GET",
                "description": "تقرير تفصيلي بالمخزون",
            },
            {
                "id": "stock_movements",
                "name": "تقرير حركة المخزون",
                "name_en": "Stock Movements Report",
                "endpoint": "/stock-movements-report",
                "method": "GET",
                "description": "تقرير بحركات الإضافة والسحب",
            },
            {
                "id": "sales",
                "name": "تقرير المبيعات",
                "name_en": "Sales Report",
                "endpoint": "/sales-report",
                "method": "GET",
                "description": "تقرير المبيعات حسب الفترة",
            },
            {
                "id": "purchases",
                "name": "تقرير المشتريات",
                "name_en": "Purchases Report",
                "endpoint": "/purchases-report",
                "method": "GET",
                "description": "تقرير المشتريات حسب الفترة",
            },
            {
                "id": "dashboard",
                "name": "تقارير لوحة التحكم",
                "name_en": "Dashboard Reports",
                "endpoint": "/dashboard-reports",
                "method": "GET",
                "description": "تقارير سريعة للوحة التحكم",
            },
        ]

        return success_response(
            data=reports_list,
            message="تم الحصول على قائمة التقارير بنجاح",
            status_code=200,
        )

    except Exception as e:
        logging.error(f"خطأ في الحصول على قائمة التقارير: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على التقارير",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@reports_bp.route("/stock-valuation", methods=["GET"])
def stock_valuation_report():
    """تقرير تقييم المخزون"""
    try:
        # الحصول على جميع المنتجات مع قيمها
        products = Product.query.filter_by(is_active=True).all()

        total_value = 0
        items = []

        for product in products:
            item_value = (product.current_stock or 0) * (product.cost_price or 0)
            total_value += item_value

            items.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "sku": product.sku,
                    "current_stock": product.current_stock or 0,
                    "cost_price": float(product.cost_price or 0),
                    "total_value": float(item_value),
                    "category": (
                        product.category.name if product.category else "غير محدد"
                    ),
                }
            )

        return jsonify(
            {
                "status": "success",
                "data": {
                    "items": items,
                    "total_value": float(total_value),
                    "total_items": len(items),
                    "generated_at": datetime.now().isoformat(),
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reports_bp.route("/low-stock", methods=["GET"])
def low_stock_report():
    """تقرير المنتجات منخفضة المخزون"""
    try:
        # البحث عن المنتجات التي مخزونها أقل من الحد الأدنى
        products = Product.query.filter(Product.is_active.is_(True)).all()

        items = []
        for product in products:
            current_stock = product.get_current_stock()
            min_quantity = product.reorder_quantity or 0
            if current_stock <= min_quantity:
                shortage = max(0, min_quantity - current_stock)
                items.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "sku": getattr(product, "sku", ""),
                        "current_stock": current_stock,
                        "min_quantity": min_quantity,
                        "shortage": shortage,
                        "category": (
                            getattr(product.rank, "name", "غير محدد")
                            if hasattr(product, "rank")
                            else "غير محدد"
                        ),
                        "cost_price": float(product.cost_price or 0),
                    }
                )

        return jsonify(
            {
                "status": "success",
                "data": {
                    "items": items,
                    "total_items": len(items),
                    "generated_at": datetime.now().isoformat(),
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# تسجيل خط عربي للـ PDF
try:
    # يمكن استخدام خط عربي مثل Arial Unicode MS أو Tahoma
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.tt"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("Arabic", font_path))
except BaseException:
    pass


@reports_bp.route("/inventory-report", methods=["GET"])
def inventory_report():
    """تقرير المخزون الحالي"""
    try:
        # معاملات البحث والفلترة
        warehouse_id = request.args.get("warehouse_id", type=int)
        category_id = request.args.get("category_id", type=int)
        include_zero_stock_param = request.args.get("include_zero_stock", "false")
        include_zero_stock = include_zero_stock_param.lower() == "true"
        low_stock_only = request.args.get("low_stock_only", "false").lower() == "true"

        # بناء الاستعلام
        query = (
            db.session.query(
                Product.id,
                Product.name,
                Product.unit,
                Product.reorder_quantity,
                Product.selling_price,
                Product.cost_price,
                Category.name.label("category_name"),
                ProductGroup.name.label("group_name"),
                Rank.name.label("rank_name"),
            )
            .join(Rank)
            .join(ProductGroup)
            .join(Category)
        )

        if category_id:
            query = query.filter(Category.id == category_id)

        products = query.filter(Product.is_active).all()

        # حساب الكميات الحالية لكل منتج
        inventory_data = []
        for product in products:
            # حساب الكمية الحالية من حركات المخزون
            stock_in_query = db.session.query(
                func.sum(StockMovement.quantity_in)
            ).filter(StockMovement.product_id == product.id)
            if warehouse_id:
                stock_in_query = stock_in_query.filter(
                    StockMovement.warehouse_id == warehouse_id
                )
            stock_in = stock_in_query.scalar() or 0

            stock_out_query = db.session.query(
                func.sum(StockMovement.quantity_out)
            ).filter(StockMovement.product_id == product.id)
            if warehouse_id:
                stock_out_query = stock_out_query.filter(
                    StockMovement.warehouse_id == warehouse_id
                )
            stock_out = stock_out_query.scalar() or 0

            current_stock = stock_in - stock_out

            # فلترة المخزون المنخفض إذا طُلب ذلك
            if low_stock_only and current_stock > product.reorder_quantity:
                continue

            # حساب قيمة المخزون
            stock_value = current_stock * (product.cost_price or 0)

            inventory_data.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "category": product.category_name,
                    "group": product.group_name,
                    "rank": product.rank_name,
                    "unit": product.unit,
                    "current_stock": current_stock,
                    "reorder_quantity": product.reorder_quantity,
                    "cost_price": product.cost_price,
                    "selling_price": product.selling_price,
                    "stock_value": stock_value,
                    "status": (
                        "منخفض"
                        if current_stock <= product.reorder_quantity
                        else "طبيعي"
                    ),
                }
            )

        # إحصائيات إجمالية
        total_products = len(inventory_data)
        total_value = sum(item["stock_value"] for item in inventory_data)
        low_stock_count = sum(1 for item in inventory_data if item["status"] == "منخفض")

        return jsonify(
            {
                "status": "success",
                "data": {
                    "inventory": inventory_data,
                    "summary": {
                        "total_products": total_products,
                        "total_value": total_value,
                        "low_stock_count": low_stock_count,
                        "report_date": datetime.now().isoformat(),
                    },
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reports_bp.route("/stock-movements-report", methods=["GET"])
def stock_movements_report():
    """تقرير حركات المخزون"""
    try:
        # معاملات البحث والفلترة
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        product_id = request.args.get("product_id", type=int)
        warehouse_id = request.args.get("warehouse_id", type=int)
        movement_type = request.args.get("movement_type")

        # تحديد التواريخ الافتراضية (آخر 30 يوم)
        if not end_date:
            end_date = datetime.now().date()
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if not start_date:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        # بناء الاستعلام
        query = (
            db.session.query(
                StockMovement.id,
                StockMovement.movement_type,
                StockMovement.movement_date,
                StockMovement.quantity_in,
                StockMovement.quantity_out,
                StockMovement.unit_price,
                StockMovement.total_amount,
                StockMovement.reference_number,
                StockMovement.notes,
                Product.name.label("product_name"),
                Warehouse.name.label("warehouse_name"),
                Customer.name.label("customer_name"),
                Supplier.name.label("supplier_name"),
            )
            .join(Product)
            .join(Warehouse)
            .outerjoin(Customer)
            .outerjoin(Supplier)
        )

        # تطبيق الفلاتر
        query = query.filter(
            StockMovement.movement_date >= start_date,
            StockMovement.movement_date <= end_date,
        )

        if product_id:
            query = query.filter(StockMovement.product_id == product_id)
        if warehouse_id:
            query = query.filter(StockMovement.warehouse_id == warehouse_id)
        if movement_type:
            query = query.filter(StockMovement.movement_type == movement_type)

        movements = query.order_by(StockMovement.movement_date.desc()).all()

        # تحويل البيانات
        movements_data = []
        total_in = 0
        total_out = 0
        total_value = 0

        for movement in movements:
            movements_data.append(
                {
                    "id": movement.id,
                    "date": movement.movement_date.isoformat(),
                    "type": movement.movement_type,
                    "product_name": movement.product_name,
                    "warehouse_name": movement.warehouse_name,
                    "customer_name": movement.customer_name,
                    "supplier_name": movement.supplier_name,
                    "quantity_in": movement.quantity_in,
                    "quantity_out": movement.quantity_out,
                    "unit_price": movement.unit_price,
                    "total_amount": movement.total_amount,
                    "reference_number": movement.reference_number,
                    "notes": movement.notes,
                }
            )

            total_in += movement.quantity_in or 0
            total_out += movement.quantity_out or 0
            total_value += movement.total_amount or 0

        return jsonify(
            {
                "status": "success",
                "data": {
                    "movements": movements_data,
                    "summary": {
                        "total_movements": len(movements_data),
                        "total_quantity_in": total_in,
                        "total_quantity_out": total_out,
                        "total_value": total_value,
                        "period": {
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat(),
                        },
                    },
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reports_bp.route("/sales-report", methods=["GET"])
def sales_report():
    """تقرير المبيعات"""
    try:
        # معاملات البحث والفلترة
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        customer_id = request.args.get("customer_id", type=int)
        product_id = request.args.get("product_id", type=int)

        # تحديد التواريخ الافتراضية
        if not end_date:
            end_date = datetime.now().date()
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if not start_date:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        # استعلام المبيعات (حركات الصادر)
        query = (
            db.session.query(
                StockMovement.movement_date,
                StockMovement.quantity_out,
                StockMovement.unit_price,
                StockMovement.total_amount,
                Product.name.label("product_name"),
                Customer.name.label("customer_name"),
            )
            .join(Product)
            .outerjoin(Customer)
            .filter(
                StockMovement.movement_type == "sale",
                StockMovement.movement_date >= start_date,
                StockMovement.movement_date <= end_date,
            )
        )

        if customer_id:
            query = query.filter(StockMovement.customer_id == customer_id)
        if product_id:
            query = query.filter(StockMovement.product_id == product_id)

        sales = query.order_by(StockMovement.movement_date.desc()).all()

        # تحويل البيانات وحساب الإحصائيات
        sales_data = []
        total_quantity = 0
        total_amount = 0

        for sale in sales:
            sales_data.append(
                {
                    "date": sale.movement_date.isoformat(),
                    "product_name": sale.product_name,
                    "customer_name": sale.customer_name or "عميل نقدي",
                    "quantity": sale.quantity_out,
                    "unit_price": sale.unit_price,
                    "total_amount": sale.total_amount,
                }
            )

            total_quantity += sale.quantity_out or 0
            total_amount += sale.total_amount or 0

        return jsonify(
            {
                "status": "success",
                "data": {
                    "sales": sales_data,
                    "summary": {
                        "total_sales": len(sales_data),
                        "total_quantity": total_quantity,
                        "total_amount": total_amount,
                        "average_sale": (
                            total_amount / len(sales_data) if sales_data else 0
                        ),
                        "period": {
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat(),
                        },
                    },
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reports_bp.route("/purchases-report", methods=["GET"])
def purchases_report():
    """تقرير المشتريات"""
    try:
        # معاملات البحث والفلترة
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        supplier_id = request.args.get("supplier_id", type=int)
        product_id = request.args.get("product_id", type=int)

        # تحديد التواريخ الافتراضية
        if not end_date:
            end_date = datetime.now().date()
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if not start_date:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        # استعلام المشتريات (حركات الوارد)
        query = (
            db.session.query(
                StockMovement.movement_date,
                StockMovement.quantity_in,
                StockMovement.unit_price,
                StockMovement.total_amount,
                Product.name.label("product_name"),
                Supplier.name.label("supplier_name"),
            )
            .join(Product)
            .outerjoin(Supplier)
            .filter(
                StockMovement.movement_type == "purchase",
                StockMovement.movement_date >= start_date,
                StockMovement.movement_date <= end_date,
            )
        )

        if supplier_id:
            query = query.filter(StockMovement.supplier_id == supplier_id)
        if product_id:
            query = query.filter(StockMovement.product_id == product_id)

        purchases = query.order_by(StockMovement.movement_date.desc()).all()

        # تحويل البيانات وحساب الإحصائيات
        purchases_data = []
        total_quantity = 0
        total_amount = 0

        for purchase in purchases:
            purchases_data.append(
                {
                    "date": purchase.movement_date.isoformat(),
                    "product_name": purchase.product_name,
                    "supplier_name": purchase.supplier_name or "مورد نقدي",
                    "quantity": purchase.quantity_in,
                    "unit_price": purchase.unit_price,
                    "total_amount": purchase.total_amount,
                }
            )

            total_quantity += purchase.quantity_in or 0
            total_amount += purchase.total_amount or 0

        return jsonify(
            {
                "status": "success",
                "data": {
                    "purchases": purchases_data,
                    "summary": {
                        "total_purchases": len(purchases_data),
                        "total_quantity": total_quantity,
                        "total_amount": total_amount,
                        "average_purchase": (
                            total_amount / len(purchases_data) if purchases_data else 0
                        ),
                        "period": {
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat(),
                        },
                    },
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reports_bp.route("/print-inventory-report", methods=["POST"])
def print_inventory_report():
    """طباعة تقرير المخزون كـ PDF"""
    try:
        data = request.get_json()
        inventory_data = data.get("inventory", [])
        summary = data.get("summary", {})

        # إنشاء ملف PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # إعداد الأنماط
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # وسط
            fontName=(
                "Arabic"
                if "Arabic" in pdfmetrics.getRegisteredFontNames()
                else "Helvetica-Bold"
            ),
        )

        # محتوى التقرير
        story = []

        # العنوان
        title = Paragraph("تقرير المخزون الحالي", title_style)
        story.append(title)
        story.append(Spacer(1, 12))

        # معلومات التقرير
        report_info = [
            ["تاريخ التقرير:", summary.get("report_date", "")[:10]],
            ["إجمالي الأصناف:", str(summary.get("total_products", 0))],
            ["قيمة المخزون الإجمالية:", f"{summary.get('total_value', 0):,.2f} جنيه"],
            ["عدد الأصناف المنخفضة:", str(summary.get("low_stock_count", 0))],
        ]

        info_table = Table(report_info, colWidths=[2 * inch, 2 * inch])
        info_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(info_table)
        story.append(Spacer(1, 20))

        # جدول البيانات
        if inventory_data:
            # رؤوس الأعمدة
            headers = [
                "اسم الصنف",
                "الفئة",
                "الكمية الحالية",
                "الوحدة",
                "سعر التكلفة",
                "قيمة المخزون",
                "الحالة",
            ]

            # بيانات الجدول
            table_data = [headers]
            for item in inventory_data:
                row = [
                    item.get("product_name", ""),
                    item.get("category", ""),
                    str(item.get("current_stock", 0)),
                    item.get("unit", ""),
                    f"{item.get('cost_price', 0):.2f}",
                    f"{item.get('stock_value', 0):.2f}",
                    item.get("status", ""),
                ]
                table_data.append(row)

            # إنشاء الجدول
            table = Table(table_data, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        # تنسيق الرأس
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        # تنسيق البيانات
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        # تلوين الصفوف بالتناوب
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.lightgrey],
                        ),
                    ]
                )
            )

            story.append(table)

        # بناء PDF
        doc.build(story)
        buffer.seek(0)

        # إرسال الملف
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'inventory_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pd',
            mimetype="application/pdf",
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reports_bp.route("/dashboard-reports", methods=["GET"])
def dashboard_reports():
    """تقارير لوحة المعلومات"""
    try:
        # إحصائيات سريعة
        total_products = Product.query.filter_by(is_active=True).count()
        total_warehouses = Warehouse.query.filter_by(is_active=True).count()
        total_customers = Customer.query.filter_by(is_active=True).count()
        total_suppliers = Supplier.query.filter_by(is_active=True).count()

        # حركات اليوم
        today = datetime.now().date()
        today_movements = StockMovement.query.filter(
            func.date(StockMovement.movement_date) == today
        ).count()

        # المبيعات الشهرية
        start_of_month = datetime.now().replace(day=1).date()
        monthly_sales = (
            db.session.query(func.sum(StockMovement.total_amount))
            .filter(
                StockMovement.movement_type == "sale",
                StockMovement.movement_date >= start_of_month,
            )
            .scalar()
            or 0
        )

        # المشتريات الشهرية
        monthly_purchases = (
            db.session.query(func.sum(StockMovement.total_amount))
            .filter(
                StockMovement.movement_type == "purchase",
                StockMovement.movement_date >= start_of_month,
            )
            .scalar()
            or 0
        )

        # الأصناف المنخفضة
        low_stock_products = []
        products = Product.query.filter_by(is_active=True).all()
        for product in products:
            stock_in = (
                db.session.query(func.sum(StockMovement.quantity_in))
                .filter(StockMovement.product_id == product.id)
                .scalar()
                or 0
            )

            stock_out = (
                db.session.query(func.sum(StockMovement.quantity_out))
                .filter(StockMovement.product_id == product.id)
                .scalar()
                or 0
            )

            current_stock = stock_in - stock_out

            if current_stock <= product.reorder_quantity:
                low_stock_products.append(
                    {
                        "product_name": product.name,
                        "current_stock": current_stock,
                        "reorder_quantity": product.reorder_quantity,
                    }
                )

        return jsonify(
            {
                "status": "success",
                "data": {
                    "totals": {
                        "products": total_products,
                        "warehouses": total_warehouses,
                        "customers": total_customers,
                        "suppliers": total_suppliers,
                    },
                    "activity": {
                        "today_movements": today_movements,
                        "monthly_sales": monthly_sales,
                        "monthly_purchases": monthly_purchases,
                    },
                    "alerts": {
                        "low_stock_count": len(low_stock_products),
                        "low_stock_products": low_stock_products[:5],  # أول 5 فقط
                    },
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
