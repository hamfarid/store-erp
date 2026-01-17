# FILE: backend/src/routes/export.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
APIs التصدير والطباعة
/home/ubuntu/inventory_management_system/src/routes/export.py
All linting disabled due to complex export operations and optional dependencies.
"""

import io
import os
import tempfile
from datetime import datetime, timedelta

# Import pandas with fallback
try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None

try:
    from flask import Blueprint, current_app, jsonify, request, send_file
except ImportError:
    Blueprint = None
    current_app = None
    jsonify = None
    request = None
    send_file = None

# P0.2.4: Import error envelope helpers
try:
    from src.middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes,
    )
except ImportError:
    # Fallback when middleware is not available
    def success_response(data=None, message="Success", code="SUCCESS", status_code=200):
        return {"success": True, "data": data, "message": message}, status_code

    def error_response(message, code=None, details=None, status_code=400):
        return {"success": False, "message": message, "code": code}, status_code

    class ErrorCodes:
        SYS_INTERNAL_ERROR = "SYS_001"


import logging

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    REPORTLAB_AVAILABLE = True
except ImportError:
    colors = None
    A4 = None
    letter = None
    ParagraphStyle = None
    getSampleStyleSheet = None
    inch = None
    pdfmetrics = None
    TTFont = None
    Paragraph = None
    SimpleDocTemplate = None
    Spacer = None
    Table = None
    TableStyle = None
    REPORTLAB_AVAILABLE = False
# Import auth functions
try:
    from auth import login_required, has_permission, Permissions, AuthManager
except ImportError:
    # Create mock auth functions
    def login_required(f):
        return f

    def has_permission(permission):
        def decorator(f):
            return f

        return decorator

    class Permissions:
        ADMIN = "admin"

    class AuthManager:
        @staticmethod
        def authenticate(username, password):
            return True


from src.models.inventory import Category, Lot, Product, Warehouse, StockMovement
from src.models.customer import Customer
from src.models.supplier import Supplier

# Import database - handle different import paths
try:
    from database import db
except ImportError:
    # Create mock db for testing
    class MockDB:
        session = None

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

    db = MockDB()

export_bp = Blueprint("export", __name__)


def safe_excel_export(data, sheet_name="Sheet1", filename="export.xlsx"):
    """Safely export data to Excel with pandas fallback"""
    if not PANDAS_AVAILABLE:
        # Return JSON if pandas not available
        return (
            jsonify(
                {
                    "status": "error",
                    "error": "Excel export requires pandas library",
                    "data": data,
                    "format": "json",
                }
            ),
            400,
        )

    try:
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        output.seek(0)
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": f"Excel export failed: {str(e)}",
                    "data": data,
                    "format": "json",
                }
            ),
            500,
        )


@export_bp.route("/data", methods=["GET"])
@login_required
def export_data():
    """تصدير البيانات بصيغ مختلفة"""
    try:
        data_type = request.args.get("data_type", "products")
        format_type = request.args.get("format_type", "excel")

        if data_type == "products":
            if format_type == "pd":
                return export_products_pdf()
            else:
                return export_products_excel()
        elif data_type == "inventory":
            if format_type == "pd":
                return export_inventory_pdf()
            else:
                return export_inventory_excel()
        elif data_type == "customers":
            return export_customers_excel()
        elif data_type == "suppliers":
            return export_suppliers_excel()
        else:
            return (
                jsonify({"status": "error", "message": "نوع البيانات غير مدعوم"}),
                400,
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def export_products_pdf():
    """تصدير المنتجات إلى PDF"""
    try:
        products = Product.query.all()

        # إنشاء ملف PDF مؤقت
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        # إعداد المحتوى
        story = []
        styles = getSampleStyleSheet()

        # العنوان
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontName=ARABIC_FONT,
            fontSize=16,
            alignment=1,  # وسط
        )
        story.append(Paragraph("تقرير المنتجات", title_style))
        story.append(Spacer(1, 12))

        # جدول البيانات
        data = [["الاسم", "الوصف", "السعر", "الكمية"]]
        for product in products:
            data.append(
                [
                    product.name or "",
                    product.description or "",
                    f"{product.price:.2f}" if product.price else "0.00",
                    str(product.quantity or 0),
                ]
            )

        table = Table(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), ARABIC_FONT),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(table)
        doc.build(story)

        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'products_report_{datetime.now().strftime("%Y%m%d")}.pd',
            mimetype="application/pdf",
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def export_inventory_excel_basic():
    """تصدير المخزون إلى Excel - النسخة الأساسية"""
    try:
        products = Product.query.all()

        data = []
        for product in products:
            data.append(
                {
                    "الاسم": product.name or "",
                    "الوصف": product.description or "",
                    "الكمية": product.quantity or 0,
                    "السعر": product.price or 0,
                    "القيمة الإجمالية": (product.price or 0) * (product.quantity or 0),
                }
            )

        df = pd.DataFrame(data)

        # إنشاء ملف Excel مؤقت
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="المخزون", index=False)

        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'inventory_report_{datetime.now().strftime("%Y%m%d")}.xlsx',
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# تسجيل خط عربي للـ PDF
try:
    # محاولة استخدام خط عربي إذا كان متوفراً
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.tt"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("Arabic", font_path))
        ARABIC_FONT = "Arabic"
    else:
        ARABIC_FONT = "Helvetica"
except BaseException:
    ARABIC_FONT = "Helvetica"


@export_bp.route("/products/excel", methods=["GET"])
@login_required
@has_permission(Permissions.REPORTS_EXPORT)
def export_products_excel():
    """تصدير المنتجات إلى Excel"""
    try:
        # جلب البيانات
        products = Product.query.all()

        # تحضير البيانات للتصدير
        data = []
        for product in products:
            data.append(
                {
                    "الرقم": product.id,
                    "اسم المنتج": product.name,
                    "الباركود": product.barcode,
                    "الفئة": product.category.name if product.category else "",
                    "المجموعة": product.group.name if product.group else "",
                    "الرتبة": product.rank.name if product.rank else "",
                    "الوحدة": product.unit,
                    "سعر الشراء": product.purchase_price,
                    "سعر البيع": product.sale_price,
                    "الكمية المتاحة": product.available_quantity,
                    "الحد الأدنى": product.minimum_quantity,
                    "تاريخ الإنشاء": (
                        product.created_at.strftime("%Y-%m-%d")
                        if product.created_at
                        else ""
                    ),
                    "ملاحظات": product.notes or "",
                }
            )

        # إنشاء DataFrame
        df = pd.DataFrame(data)

        # إنشاء ملف Excel في الذاكرة
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="المنتجات", index=False)

            # تنسيق الورقة
            worksheet = writer.sheets["المنتجات"]

            # تعديل عرض الأعمدة
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except BaseException:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        # إرسال الملف
        filename = f'products_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في تصدير المنتجات: {str(e)}"}),
            500,
        )


@export_bp.route("/inventory/excel", methods=["GET"])
@login_required
@has_permission(Permissions.REPORTS_EXPORT)
def export_inventory_excel():
    """تصدير تقرير المخزون إلى Excel"""
    try:
        # جلب البيانات مع الكميات
        products = Product.query.all()

        data = []
        for product in products:
            # حساب الكميات من اللوطات
            total_quantity = 0
            batches = Lot.query.filter_by(product_id=product.id).all()
            for lot in batches:
                total_quantity += lot.quantity

            data.append(
                {
                    "الرقم": product.id,
                    "اسم المنتج": product.name,
                    "الباركود": product.barcode,
                    "الفئة": product.category.name if product.category else "",
                    "الوحدة": product.unit,
                    "الكمية المتاحة": total_quantity,
                    "الحد الأدنى": product.minimum_quantity,
                    "سعر الشراء": product.purchase_price,
                    "سعر البيع": product.sale_price,
                    "قيمة المخزون (شراء)": total_quantity
                    * (product.purchase_price or 0),
                    "قيمة المخزون (بيع)": total_quantity * (product.sale_price or 0),
                    "الحالة": (
                        "نفاد"
                        if total_quantity <= (product.minimum_quantity or 0)
                        else "متوفر"
                    ),
                }
            )

        df = pd.DataFrame(data)

        # إضافة صف الإجماليات
        if not df.empty:
            totals = {
                "الرقم": "",
                "اسم المنتج": "الإجمالي",
                "الباركود": "",
                "الفئة": "",
                "الوحدة": "",
                "الكمية المتاحة": df["الكمية المتاحة"].sum(),
                "الحد الأدنى": "",
                "سعر الشراء": "",
                "سعر البيع": "",
                "قيمة المخزون (شراء)": df["قيمة المخزون (شراء)"].sum(),
                "قيمة المخزون (بيع)": df["قيمة المخزون (بيع)"].sum(),
                "الحالة": "",
            }
            df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

        # إنشاء ملف Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="تقرير المخزون", index=False)

            worksheet = writer.sheets["تقرير المخزون"]

            # تنسيق الأعمدة
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except BaseException:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        filename = f'inventory_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "error": f"خطأ في تصدير تقرير المخزون: {str(e)}"}
            ),
            500,
        )


@export_bp.route("/inventory/pd", methods=["GET"])
@login_required
@has_permission(Permissions.REPORTS_EXPORT)
def export_inventory_pdf():
    """تصدير تقرير المخزون إلى PDF"""
    try:
        # جلب البيانات
        products = Product.query.all()

        # إنشاء ملف PDF مؤقت
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pd")
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)

        # إعداد الأنماط
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontName=ARABIC_FONT,
            fontSize=16,
            alignment=1,  # وسط
            spaceAfter=30,
        )

        # محتوى PDF
        story = []

        # العنوان
        title = Paragraph("تقرير المخزون", title_style)
        story.append(title)
        story.append(Spacer(1, 12))

        # تاريخ التقرير
        date_text = f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        date_para = Paragraph(date_text, styles["Normal"])
        story.append(date_para)
        story.append(Spacer(1, 20))

        # إعداد بيانات الجدول
        data = [
            ["اسم المنتج", "الفئة", "الكمية", "سعر الشراء", "سعر البيع", "قيمة المخزون"]
        ]

        total_value = 0
        for product in products:
            # حساب الكمية الإجمالية
            total_quantity = 0
            batches = Lot.query.filter_by(product_id=product.id).all()
            for lot in batches:
                total_quantity += lot.quantity

            inventory_value = total_quantity * (product.purchase_price or 0)
            total_value += inventory_value

            data.append(
                [
                    (
                        product.name[:20] + "..."
                        if len(product.name) > 20
                        else product.name
                    ),
                    product.category.name if product.category else "",
                    str(total_quantity),
                    f"{product.purchase_price or 0:.2f}",
                    f"{product.sale_price or 0:.2f}",
                    f"{inventory_value:.2f}",
                ]
            )

        # إضافة صف الإجمالي
        data.append(["الإجمالي", "", "", "", "", f"{total_value:.2f}"])

        # إنشاء الجدول
        table = Table(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), ARABIC_FONT),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -2), colors.beige),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, -1), (-1, -1), ARABIC_FONT),
                    ("FONTSIZE", (0, -1), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(table)

        # بناء PDF
        doc.build(story)

        # إرسال الملف
        filename = f'inventory_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pd'
        return send_file(
            temp_file.name,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": f"خطأ في تصدير PDF: {str(e)}"}), 500


@export_bp.route("/movements/excel", methods=["GET"])
@login_required
@has_permission(Permissions.REPORTS_EXPORT)
def export_movements_excel():
    """تصدير حركات المخزون إلى Excel"""
    try:
        # الحصول على فلتر التاريخ
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        # بناء الاستعلام
        query = StockMovement.query

        if start_date:
            query = query.filter(StockMovement.movement_date >= start_date)
        if end_date:
            query = query.filter(StockMovement.movement_date <= end_date)

        movements = query.order_by(StockMovement.movement_date.desc()).all()

        # تحضير البيانات
        data = []
        for movement in movements:
            data.append(
                {
                    "الرقم": movement.id,
                    "تاريخ الحركة": (
                        movement.movement_date.strftime("%Y-%m-%d")
                        if movement.movement_date
                        else ""
                    ),
                    "نوع الحركة": movement.movement_type,
                    "المنتج": movement.product.name if movement.product else "",
                    "الكمية": movement.quantity,
                    "السعر": movement.price,
                    "القيمة الإجمالية": movement.quantity * (movement.price or 0),
                    "المخزن": movement.warehouse.name if movement.warehouse else "",
                    "العميل/المورد": (
                        movement.customer.name
                        if movement.customer
                        else (movement.supplier.name if movement.supplier else "")
                    ),
                    "المستخدم": movement.user.full_name if movement.user else "",
                    "ملاحظات": movement.notes or "",
                }
            )

        df = pd.DataFrame(data)

        # إنشاء ملف Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="حركات المخزون", index=False)

            worksheet = writer.sheets["حركات المخزون"]

            # تنسيق الأعمدة
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except BaseException:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        filename = f'stock_movements_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "error": f"خطأ في تصدير حركات المخزون: {str(e)}"}
            ),
            500,
        )


@export_bp.route("/customers/excel", methods=["GET"])
@login_required
@has_permission(Permissions.REPORTS_EXPORT)
def export_customers_excel():
    """تصدير العملاء إلى Excel"""
    try:
        customers = Customer.query.all()

        data = []
        for customer in customers:
            data.append(
                {
                    "الرقم": customer.id,
                    "اسم العميل": customer.name,
                    "رقم الهاتف": customer.phone or "",
                    "البريد الإلكتروني": customer.email or "",
                    "العنوان": customer.address or "",
                    "المدينة": customer.city or "",
                    "الرصيد": customer.balance or 0,
                    "حد الائتمان": customer.credit_limit or 0,
                    "مندوب المبيعات": (
                        customer.salesperson.full_name if customer.salesperson else ""
                    ),
                    "تاريخ الإنشاء": (
                        customer.created_at.strftime("%Y-%m-%d")
                        if customer.created_at
                        else ""
                    ),
                    "ملاحظات": customer.notes or "",
                }
            )

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="العملاء", index=False)

            worksheet = writer.sheets["العملاء"]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except BaseException:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        filename = f'customers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في تصدير العملاء: {str(e)}"}),
            500,
        )


@export_bp.route("/suppliers/excel", methods=["GET"])
@login_required
@has_permission(Permissions.REPORTS_EXPORT)
def export_suppliers_excel():
    """تصدير الموردين إلى Excel"""
    try:
        suppliers = Supplier.query.all()

        data = []
        for supplier in suppliers:
            data.append(
                {
                    "الرقم": supplier.id,
                    "اسم المورد": supplier.name,
                    "رقم الهاتف": supplier.phone or "",
                    "البريد الإلكتروني": supplier.email or "",
                    "العنوان": supplier.address or "",
                    "المدينة": supplier.city or "",
                    "الرصيد": supplier.balance or 0,
                    "تاريخ الإنشاء": (
                        supplier.created_at.strftime("%Y-%m-%d")
                        if supplier.created_at
                        else ""
                    ),
                    "ملاحظات": supplier.notes or "",
                }
            )

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name="الموردين", index=False)

            worksheet = writer.sheets["الموردين"]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except BaseException:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        filename = f'suppliers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في تصدير الموردين: {str(e)}"}),
            500,
        )
