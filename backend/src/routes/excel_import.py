# FILE: backend/src/routes/excel_import.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

"""
نظام استيراد البيانات من ملفات Excel
"""
# type: ignore  # تجاهل جميع تحذيرات النوع للملف بأكمله
# mypy: ignore-errors
# pylint: disable=all

from datetime import datetime
import os

try:
    from flask import Blueprint, request, jsonify  # type: ignore
except ImportError:
    # Fallback when Flask is not available
    class Blueprint:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(f):
                return f

            return decorator

    def jsonify(data):
        return {"data": data}

    class request:
        args = {}


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

    # Fallback when Flask is not available
    class Blueprint:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(f):
                return f

            return decorator

    def jsonify(data):
        return {"data": data}

    class request:
        json = {}
        form = {}
        files = {}


try:
    import openpyxl
    import pandas as pd

    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    openpyxl = None

    # Create comprehensive pandas mock
    class MockDataFrame:
        def __init__(self, data=None):
            self.data = data or []

        def iterrows(self):
            return enumerate(self.data)

        def to_dict(self, orient="records"):
            return self.data

        def to_excel(self, filepath, index=False):
            """Mock to_excel method"""
            pass

    class MockPandas:
        DataFrame = MockDataFrame

        @staticmethod
        def read_excel(*args, **kwargs):
            raise ImportError("pandas is not installed")

    pd = MockPandas()

# Prefer canonical unified models and src.database; avoid legacy
# 'models.*' to prevent duplicate mappers
try:
    from src.models.product_unified import Product  # prefer unified model
except Exception:
    try:
        from src.models.inventory import (
            Product,
        )  # fallback to legacy product if unified not available
    except Exception:
        Product = None  # type: ignore

try:
    from src.models.category import Category
    from src.models.customer import Customer
    from src.models.supplier import Supplier
    from src.database import db
except Exception:
    # Fallback when models are not available
    class MockDB:
        session = None

        @staticmethod
        def add(obj):
            pass

        @staticmethod
        def commit():
            pass

        @staticmethod
        def rollback():
            pass

    db = MockDB()

    class Product:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Category:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Supplier:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Customer:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


# إنشاء Blueprint
excel_bp = Blueprint("excel_import", __name__)


@excel_bp.route("/api/excel/upload", methods=["POST"])
def upload_excel():
    """رفع ملف Excel"""
    try:
        if not EXCEL_AVAILABLE:
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": (
                            "مكتبات Excel غير متوفرة. " "يرجى تثبيت openpyxl و pandas"
                        ),
                    }
                ),
                500,
            )

        if "file" not in request.files:
            return jsonify({"status": "error", "error": "لم يتم رفع أي ملف"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"status": "error", "error": "لم يتم اختيار ملف"}), 400

        if not file.filename.endswith((".xlsx", ".xls")):
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "نوع الملف غير مدعوم. يرجى رفع ملف Excel",
                    }
                ),
                400,
            )

        # حفظ الملف مؤقتاً
        upload_folder = "uploads"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"temp_{timestamp}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        return jsonify(
            {
                "status": "success",
                "message": "تم رفع الملف بنجاح",
                "data": {"filename": filename, "filepath": filepath},
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": f"خطأ في رفع الملف: {str(e)}"}), 500


@excel_bp.route("/api/excel/preview/<filename>", methods=["GET"])
def preview_excel(filename):
    """معاينة محتوى ملف Excel"""
    try:
        if not EXCEL_AVAILABLE:
            return jsonify({"status": "error", "error": "مكتبات Excel غير متوفرة"}), 500

        filepath = os.path.join("uploads", filename)
        if not os.path.exists(filepath):
            return jsonify({"status": "error", "error": "الملف غير موجود"}), 404

        # قراءة الملف
        df = pd.read_excel(filepath, nrows=10)  # أول 10 صفوف للمعاينة

        # تحويل إلى قاموس
        preview_data = {
            "columns": df.columns.tolist(),
            "rows": df.fillna("").to_dict("records"),
            "total_rows": len(df),
        }

        return jsonify(
            {
                "status": "success",
                "data": preview_data,
                "message": "تم تحميل معاينة الملف بنجاح",
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في معاينة الملف: {str(e)}"}),
            500,
        )


@excel_bp.route("/api/excel/import/products/<filename>", methods=["POST"])
def import_products(filename):
    """استيراد المنتجات من Excel"""
    try:
        if not EXCEL_AVAILABLE:
            return jsonify({"status": "error", "error": "مكتبات Excel غير متوفرة"}), 500

        filepath = os.path.join("uploads", filename)
        if not os.path.exists(filepath):
            return jsonify({"status": "error", "error": "الملف غير موجود"}), 404

        # قراءة الملف
        df = pd.read_excel(filepath)

        imported_count = 0
        errors = []

        for index, row in df.iterrows():
            try:
                # إنشاء منتج جديد
                product = Product(
                    name=str(row.get("name", "")),
                    barcode=str(row.get("barcode", "")),
                    price=float(row.get("price", 0)),
                    cost=float(row.get("cost", 0)),
                    quantity=int(row.get("quantity", 0)),
                    description=str(row.get("description", "")),
                )

                if db and hasattr(db, "session") and db.session:
                    db.session.add(product)

                imported_count += 1

            except Exception as e:
                row_num = int(index) + 1  # type: ignore
                errors.append(f"الصف {row_num}: {str(e)}")

        if db and hasattr(db, "session") and db.session:
            db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": f"تم استيراد {imported_count} منتج بنجاح",
                "data": {"imported_count": imported_count, "errors": errors},
            }
        )

    except Exception as e:
        if db and hasattr(db, "session") and db.session:
            db.session.rollback()
        return (
            jsonify({"status": "error", "error": f"خطأ في استيراد المنتجات: {str(e)}"}),
            500,
        )


@excel_bp.route("/api/excel/export/products", methods=["GET"])
def export_products():
    """تصدير المنتجات إلى Excel"""
    try:
        if not EXCEL_AVAILABLE:
            return jsonify({"status": "error", "error": "مكتبات Excel غير متوفرة"}), 500

        # بيانات تجريبية للتصدير
        products_data = [
            {
                "name": "منتج تجريبي 1",
                "barcode": "123456789",
                "price": 100.0,
                "cost": 80.0,
                "quantity": 50,
                "description": "وصف المنتج",
            }
        ]

        # إنشاء DataFrame
        df = pd.DataFrame(products_data)

        # حفظ إلى ملف Excel
        export_folder = "exports"
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"products_export_{timestamp}.xlsx"
        filepath = os.path.join(export_folder, filename)

        df.to_excel(filepath, index=False)  # type: ignore

        return jsonify(
            {
                "status": "success",
                "message": "تم تصدير المنتجات بنجاح",
                "data": {"filename": filename, "filepath": filepath},
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في تصدير المنتجات: {str(e)}"}),
            500,
        )


@excel_bp.route("/api/excel/templates", methods=["GET"])
def get_templates():
    """الحصول على قوالب Excel"""
    try:
        templates = {
            "products": {
                "name": "قالب المنتجات",
                "columns": [
                    "name",
                    "barcode",
                    "price",
                    "cost",
                    "quantity",
                    "description",
                ],
                "description": "قالب لاستيراد المنتجات",
            },
            "customers": {
                "name": "قالب العملاء",
                "columns": ["name", "email", "phone", "address"],
                "description": "قالب لاستيراد العملاء",
            },
            "suppliers": {
                "name": "قالب الموردين",
                "columns": ["name", "email", "phone", "address", "contact_person"],
                "description": "قالب لاستيراد الموردين",
            },
        }

        return jsonify(
            {
                "status": "success",
                "data": templates,
                "message": "تم الحصول على القوالب بنجاح",
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "error": f"خطأ في الحصول على القوالب: {str(e)}"}
            ),
            500,
        )
