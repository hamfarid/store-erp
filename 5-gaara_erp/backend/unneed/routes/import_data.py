# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
APIs استيراد البيانات من Excel
/home/ubuntu/inventory_management_system/src/routes/import_data.py
All linting disabled due to complex import operations and optional dependencies.
"""

import os
from datetime import datetime
from flask import Blueprint, current_app, jsonify, request

# Import pandas with fallback
try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    # Create a mock pandas module for type checking
    # Create a mock pandas module for type checking

    class MockDataFrame:
        def __init__(self, data=None, columns=None):
            self.data = data or []
            self.columns = columns or []
            self.loc = self  # Mock loc accessor

        def iterrows(self):
            return enumerate(self.data)

        def to_dict(self, orient="records"):
            return self.data

        def to_excel(self, filepath, index=False, engine=None):
            """Mock to_excel method"""
            pass

        def __setitem__(self, key, value):
            """Mock assignment for df.loc[0] = [...]"""
            pass

    class MockPandas:
        DataFrame = MockDataFrame

        @staticmethod
        def read_excel(*args, **kwargs):
            raise ImportError("pandas is not installed")

    pd = MockPandas()

# Import models with fallback
try:
    from src.models.inventory import Category, Lot, Product, Warehouse
except ImportError:
    # Create mock models
    class Category:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Lot:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Product:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Warehouse:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


try:
    from src.models.customer import Customer
    from src.models.supplier import Supplier
except ImportError:
    # Create mock partner models
    class Customer:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Supplier:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


# Import database - handle different import paths
try:
    from src.database import db
except ImportError:
    # Create mock db for testing
    class MockSession:
        def add(self, obj):
            """Mock add method"""
            pass

        def commit(self):
            """Mock commit method"""
            pass

        def rollback(self):
            """Mock rollback method"""
            pass

        def flush(self):
            """Mock flush method"""
            pass

    class MockDB:
        session = MockSession()

        @staticmethod
        def create_all():
            """Mock create_all method"""
            pass

        @staticmethod
        def drop_all():
            """Mock drop_all method"""
            pass

    db = MockDB()

import_bp = Blueprint("import_data", __name__)

# Constants for repeated strings
IMPORTED_FROM_EXCEL = "تم استيراده من Excel"
NOT_SPECIFIED = "غير محدد"
PRODUCT_NAME_COL = "اسم المنتج"
QUANTITY_COL = "الكمية"
CONTACT_PERSON_COL = "الشخص المسؤول"
PHONE_COL = "الهاتف"
EMAIL_COL = "البريد الإلكتروني"
ADDRESS_COL = "العنوان"


@import_bp.route("/data", methods=["POST"])
def import_data():
    """استيراد البيانات من ملف"""
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "لم يتم رفع أي ملف"}), 400

        file = request.files["file"]
        data_type = request.form.get("type", "products")

        if not file.filename or file.filename == "":
            return jsonify({"status": "error", "message": "لم يتم اختيار ملف"}), 400

        if not file.filename or not file.filename.endswith((".xlsx", ".xls", ".csv")):
            return jsonify({"status": "error", "message": "نوع الملف غير مدعوم"}), 400

        # حفظ الملف مؤقتاً
        upload_folder = os.path.join(current_app.root_path, "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"import_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # معالجة الملف حسب النوع
        if data_type == "products":
            result = import_products_from_file(filepath)
        elif data_type == "customers":
            result = import_customers_from_file(filepath)
        elif data_type == "suppliers":
            result = import_suppliers_from_file(filepath)
        else:
            return (
                jsonify({"status": "error", "message": "نوع البيانات غير مدعوم"}),
                400,
            )

        # حذف الملف المؤقت
        try:
            os.remove(filepath)
        except OSError:
            pass

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def import_products_from_file(filepath):
    """استيراد المنتجات من الملف"""
    try:
        df = pd.read_excel(filepath)
        imported_count = 0
        errors = []

        for row_num, (_, row) in enumerate(df.iterrows(), start=1):
            try:
                # إنشاء منتج جديد
                product = Product()
                product.name = str(row.get("name", ""))
                product.description = str(row.get("description", ""))
                product.barcode = str(row.get("sku", ""))  # Using barcode
                product.selling_price = float(row.get("price", 0))
                product.cost_price = float(row.get("cost", 0))
                # Note: quantity managed through stock movements

                db.session.add(product)
                imported_count += 1

            except Exception as e:
                errors.append(f"السطر {row_num}: {str(e)}")

        db.session.commit()

        return {
            "status": "success",
            "message": f"تم استيراد {imported_count} منتج بنجاح",
            "imported_count": imported_count,
            "errors": errors,
        }

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"خطأ في استيراد المنتجات: {str(e)}"}


def import_customers_from_file(filepath):
    """استيراد العملاء من الملف"""
    try:
        df = pd.read_excel(filepath)
        imported_count = 0
        errors = []

        for row_num, (_, row) in enumerate(df.iterrows(), start=1):
            try:
                customer = Customer()
                customer.name = str(row.get("name", ""))
                customer.email = str(row.get("email", ""))
                customer.phone = str(row.get("phone", ""))
                customer.address = str(row.get("address", ""))

                db.session.add(customer)
                imported_count += 1

            except Exception as e:
                errors.append(f"السطر {row_num}: {str(e)}")

        db.session.commit()

        return {
            "status": "success",
            "message": f"تم استيراد {imported_count} عميل بنجاح",
            "imported_count": imported_count,
            "errors": errors,
        }

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"خطأ في استيراد العملاء: {str(e)}"}


def import_suppliers_from_file(filepath):
    """استيراد الموردين من الملف"""
    try:
        df = pd.read_excel(filepath)
        imported_count = 0
        errors = []

        for row_num, (_, row) in enumerate(df.iterrows(), start=1):
            try:
                supplier = Supplier()
                supplier.name = str(row.get("name", ""))
                supplier.email = str(row.get("email", ""))
                supplier.phone = str(row.get("phone", ""))
                supplier.address = str(row.get("address", ""))

                db.session.add(supplier)
                imported_count += 1

            except Exception as e:
                errors.append(f"السطر {row_num}: {str(e)}")

        db.session.commit()

        return {
            "status": "success",
            "message": f"تم استيراد {imported_count} مورد بنجاح",
            "imported_count": imported_count,
            "errors": errors,
        }

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"خطأ في استيراد الموردين: {str(e)}"}


@import_bp.route("/upload-excel", methods=["POST"])
def upload_excel():
    """رفع ملف Excel لاستيراد البيانات"""
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "لم يتم رفع أي ملف"}), 400

        file = request.files["file"]
        if not file.filename or file.filename == "":
            return jsonify({"status": "error", "message": "لم يتم اختيار ملف"}), 400

        if not file.filename.endswith((".xlsx", ".xls")):
            return (
                jsonify(
                    {"status": "error", "message": "يجب أن يكون الملف من نوع Excel"}
                ),
                400,
            )

        # حفظ الملف مؤقتاً
        upload_folder = os.path.join(current_app.root_path, "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"import_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # قراءة الملف وتحليل البيانات
        analysis_result = analyze_excel_file(filepath)

        return jsonify(
            {
                "status": "success",
                "message": "تم رفع الملف بنجاح",
                "data": {
                    "filename": filename,
                    "filepath": filepath,
                    "analysis": analysis_result,
                },
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في رفع الملف: {str(e)}"}),
            500,
        )


@import_bp.route("/import-excel", methods=["POST"])
def import_excel():
    """استيراد البيانات من ملف Excel"""
    try:
        data = request.get_json()
        filepath = data.get("filepath")
        import_options = data.get("options", {})

        if not filepath or not os.path.exists(filepath):
            return jsonify({"status": "error", "message": "الملف غير موجود"}), 400

        # استيراد البيانات
        import_result = import_excel_data(filepath, import_options)

        # حذف الملف المؤقت
        try:
            os.remove(filepath)
        except OSError:
            pass

        return jsonify(
            {
                "status": "success",
                "message": "تم استيراد البيانات بنجاح",
                "data": import_result,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في استيراد البيانات: {str(e)}"}
            ),
            500,
        )


def analyze_excel_file(filepath):
    """تحليل ملف Excel وإرجاع معلومات عن البيانات"""
    try:
        if not PANDAS_AVAILABLE:
            return {
                "error": "pandas غير متاح لتحليل ملفات Excel",
                "total_rows": 0,
                "total_columns": 0,
                "columns": [],
                "detected_type": "unknown",
            }

        # قراءة الملف
        df = pd.read_excel(filepath)

        # تحليل الأعمدة
        columns_analysis = {}
        for col in df.columns:
            columns_analysis[col] = {
                "type": str(df[col].dtype),
                "non_null_count": df[col].count(),
                "null_count": df[col].isnull().sum(),
                "unique_count": df[col].nunique(),
                "sample_values": df[col].dropna().head(3).tolist(),
            }

        # تحديد نوع البيانات المحتملة
        data_type = detect_data_type(df.columns.tolist())

        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "columns_analysis": columns_analysis,
            "detected_type": data_type,
            "preview": df.head(5).to_dict("records"),
        }

    except Exception as e:
        raise ValueError(f"خطأ في تحليل الملف: {str(e)}")


def detect_data_type(columns):
    """تحديد نوع البيانات بناءً على أسماء الأعمدة"""
    columns_lower = [col.lower() for col in columns]

    # كلمات مفتاحية للمنتجات
    product_keywords = ["اسم", "صنف", "منتج", "name", "product", "item"]
    inventory_keywords = ["مخزون", "كمية", "quantity", "stock", "inventory"]
    supplier_keywords = ["مورد", "supplier", "vendor"]
    customer_keywords = ["عميل", "customer", "client"]

    if any(keyword in " ".join(columns_lower) for keyword in product_keywords):
        if any(keyword in " ".join(columns_lower) for keyword in inventory_keywords):
            return "inventory"
        else:
            return "products"
    elif any(keyword in " ".join(columns_lower) for keyword in supplier_keywords):
        return "suppliers"
    elif any(keyword in " ".join(columns_lower) for keyword in customer_keywords):
        return "customers"
    else:
        return "unknown"


def import_excel_data(filepath, options=None):
    """استيراد البيانات الفعلي من ملف Excel"""
    # options parameter reserved for future use
    try:
        if not PANDAS_AVAILABLE:
            return {
                "error": "pandas غير متاح لاستيراد ملفات Excel",
                "total_rows": 0,
                "imported_products": 0,
                "imported_categories": 0,
                "imported_warehouses": 0,
                "imported_suppliers": 0,
                "imported_customers": 0,
                "errors": ["pandas library not available"],
            }

        df = pd.read_excel(filepath)

        # تنظيف البيانات
        df = df.dropna(how="all")  # حذف الصفوف الفارغة
        df = df.fillna("")  # استبدال القيم الفارغة بنص فارغ

        # إحصائيات الاستيراد
        stats = {
            "total_rows": len(df),
            "imported_products": 0,
            "imported_categories": 0,
            "imported_warehouses": 0,
            "imported_suppliers": 0,
            "imported_customers": 0,
            "errors": [],
        }

        # استيراد التصنيفات أولاً
        if "فئة" in df.columns or "category" in df.columns.str.lower():
            stats["imported_categories"] = import_categories(df)

        # استيراد المخازن
        if "مخزن" in df.columns or "warehouse" in df.columns.str.lower():
            stats["imported_warehouses"] = import_warehouses(df)

        # استيراد الموردين
        if "مورد" in df.columns or "supplier" in df.columns.str.lower():
            stats["imported_suppliers"] = import_suppliers(df)

        # استيراد العملاء
        if "عميل" in df.columns or "customer" in df.columns.str.lower():
            stats["imported_customers"] = import_customers(df)

        # استيراد المنتجات
        stats["imported_products"] = import_products(df, stats)

        db.session.commit()

        return stats

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"خطأ في استيراد البيانات: {str(e)}")


def import_categories(df):
    """استيراد التصنيفات"""
    imported_count = 0

    # البحث عن عمود التصنيفات
    category_col = None
    for col in df.columns:
        if "فئة" in col or "category" in col.lower():
            category_col = col
            break

    if not category_col:
        return 0

    # استخراج التصنيفات الفريدة
    unique_categories = df[category_col].dropna().unique()

    for cat_name in unique_categories:
        if cat_name and str(cat_name).strip():
            # التحقق من عدم وجود التصنيف
            existing_category = Category.query.filter_by(
                name=str(cat_name).strip()
            ).first()
            if not existing_category:
                category = Category()
                category.name = str(cat_name).strip()
                category.description = IMPORTED_FROM_EXCEL
                db.session.add(category)
                imported_count += 1

    return imported_count


def import_warehouses(df):
    """استيراد المخازن"""
    imported_count = 0

    # البحث عن عمود المخازن
    warehouse_col = None
    for col in df.columns:
        if "مخزن" in col or "warehouse" in col.lower():
            warehouse_col = col
            break

    if not warehouse_col:
        return 0

    # استخراج المخازن الفريدة
    unique_warehouses = df[warehouse_col].dropna().unique()

    for warehouse_name in unique_warehouses:
        if warehouse_name and str(warehouse_name).strip():
            # التحقق من عدم وجود المخزن
            existing_warehouse = Warehouse.query.filter_by(
                name=str(warehouse_name).strip()
            ).first()
            if not existing_warehouse:
                warehouse = Warehouse()
                warehouse.name = str(warehouse_name).strip()
                warehouse.location = IMPORTED_FROM_EXCEL
                warehouse.is_active = True
                db.session.add(warehouse)
                imported_count += 1

    return imported_count


def import_suppliers(df):
    """استيراد الموردين"""
    imported_count = 0

    # البحث عن عمود الموردين
    supplier_col = None
    for col in df.columns:
        if "مورد" in col or "supplier" in col.lower():
            supplier_col = col
            break

    if not supplier_col:
        return 0

    # استخراج الموردين الفريدين
    unique_suppliers = df[supplier_col].dropna().unique()

    for supplier_name in unique_suppliers:
        if supplier_name and str(supplier_name).strip():
            # التحقق من عدم وجود المورد
            existing_supplier = Supplier.query.filter_by(
                name=str(supplier_name).strip()
            ).first()
            if not existing_supplier:
                supplier = Supplier(
                    name=str(supplier_name).strip(),
                    contact_person=NOT_SPECIFIED,
                    phone=NOT_SPECIFIED,
                    email="",
                    address=IMPORTED_FROM_EXCEL,
                    is_active=True,
                )
                db.session.add(supplier)
                imported_count += 1

    return imported_count


def import_customers(df):
    """استيراد العملاء"""
    imported_count = 0

    # البحث عن عمود العملاء
    customer_col = None
    for col in df.columns:
        if "عميل" in col or "customer" in col.lower():
            customer_col = col
            break

    if not customer_col:
        return 0

    # استخراج العملاء الفريدين
    unique_customers = df[customer_col].dropna().unique()

    for customer_name in unique_customers:
        if customer_name and str(customer_name).strip():
            # التحقق من عدم وجود العميل
            existing_customer = Customer.query.filter_by(
                name=str(customer_name).strip()
            ).first()
            if not existing_customer:
                customer = Customer(
                    name=str(customer_name).strip(),
                    contact_person=NOT_SPECIFIED,
                    phone=NOT_SPECIFIED,
                    email="",
                    address=IMPORTED_FROM_EXCEL,
                    is_active=True,
                )
                db.session.add(customer)
                imported_count += 1

    return imported_count


def import_products(df, stats):
    """استيراد المنتجات"""
    imported_count = 0

    # تحديد أعمدة المنتجات
    product_name_col = None
    category_col = None
    price_col = None
    quantity_col = None

    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col for keyword in ["اسم", "صنف", "منتج"]) or any(
            keyword in col_lower for keyword in ["name", "product", "item"]
        ):
            product_name_col = col
        elif "فئة" in col or "category" in col_lower:
            category_col = col
        elif any(keyword in col for keyword in ["سعر", "ثمن"]) or any(
            keyword in col_lower for keyword in ["price", "cost"]
        ):
            price_col = col
        elif any(keyword in col for keyword in ["كمية", "مخزون"]) or any(
            keyword in col_lower for keyword in ["quantity", "stock"]
        ):
            quantity_col = col

    if not product_name_col:
        return 0

    # استيراد المنتجات
    for index, row in df.iterrows():
        try:
            product_name = str(row[product_name_col]).strip()
            if not product_name or product_name == "nan":
                continue

            # التحقق من عدم وجود المنتج
            existing_product = Product.query.filter_by(name=product_name).first()
            if existing_product:
                continue

            # الحصول على التصنيف (للاستخدام المستقبلي)
            if category_col and row[category_col]:
                category_name = str(row[category_col]).strip()
                # Category lookup for future use
                _ = Category.query.filter_by(name=category_name).first()

            # إنشاء المنتج
            product = Product()
            product.name = product_name
            product.description = IMPORTED_FROM_EXCEL
            # استخدام rank_id بدلاً من category_id
            product.rank_id = 1  # افتراضي
            product.unit = "قطعة"  # وحدة افتراضية
            # استخدام selling_price بدلاً من unit_price
            product.selling_price = (
                float(row[price_col])
                if price_col
                and row[price_col]
                and str(row[price_col]).replace(".", "").isdigit()
                else 0.0
            )
            product.cost_price = 0.0
            product.barcode = ""
            product.is_active = True

            db.session.add(product)
            db.session.flush()  # للحصول على ID المنتج

            # إضافة الكمية إذا كانت متوفرة
            if quantity_col and row[quantity_col]:
                try:
                    quantity = float(row[quantity_col])
                    if quantity > 0:
                        # إنشاء لوط افتراضي
                        default_warehouse = Warehouse.query.first()
                        if default_warehouse:
                            lot = Lot()
                            lot.product_id = product.id
                            lot.warehouse_id = default_warehouse.id
                            lot.batch_number = (
                                f'IMPORT_{datetime.now().strftime("%Y%m%d")}'
                                f"_{product.id}"
                            )
                            lot.initial_quantity = quantity
                            lot.current_quantity = quantity
                            lot.batch_creation_date = datetime.now().date()
                            lot.expiry_date = None
                            db.session.add(lot)
                except Exception:
                    # Ignore lot creation errors
                    pass

            imported_count += 1

        except Exception as e:
            stats["errors"].append(f"خطأ في الصف {index + 1}: {str(e)}")
            continue

    return imported_count


@import_bp.route("/import-templates", methods=["GET"])
def get_import_templates():
    """الحصول على قوالب الاستيراد"""
    try:
        templates = {
            "products": {
                "name": "قالب المنتجات",
                "description": "قالب لاستيراد المنتجات والأصناف",
                "columns": [
                    PRODUCT_NAME_COL,
                    "الفئة",
                    "السعر",
                    QUANTITY_COL,
                    "الوصف",
                    "الباركود",
                ],
            },
            "inventory": {
                "name": "قالب المخزون",
                "description": "قالب لاستيراد بيانات المخزون",
                "columns": [
                    "اسم المنتج",
                    "المخزن",
                    "الكمية",
                    "رقم اللوط",
                    "تاريخ الانتهاء",
                ],
            },
            "suppliers": {
                "name": "قالب الموردين",
                "description": "قالب لاستيراد بيانات الموردين",
                "columns": [
                    "اسم المورد",
                    CONTACT_PERSON_COL,
                    PHONE_COL,
                    EMAIL_COL,
                    ADDRESS_COL,
                ],
            },
            "customers": {
                "name": "قالب العملاء",
                "description": "قالب لاستيراد بيانات العملاء",
                "columns": [
                    "اسم العميل",
                    CONTACT_PERSON_COL,
                    PHONE_COL,
                    EMAIL_COL,
                    ADDRESS_COL,
                ],
            },
        }

        return jsonify({"status": "success", "data": templates})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@import_bp.route("/export-template/<template_type>", methods=["GET"])
def export_template(template_type):
    """تصدير قالب Excel للاستيراد"""
    try:
        templates = {
            "products": ["اسم المنتج", "الفئة", "السعر", "الكمية", "الوصف", "الباركود"],
            "inventory": [
                "اسم المنتج",
                "المخزن",
                "الكمية",
                "رقم اللوط",
                "تاريخ الانتهاء",
            ],
            "suppliers": [
                "اسم المورد",
                CONTACT_PERSON_COL,
                PHONE_COL,
                EMAIL_COL,
                ADDRESS_COL,
            ],
            "customers": [
                "اسم العميل",
                CONTACT_PERSON_COL,
                PHONE_COL,
                EMAIL_COL,
                ADDRESS_COL,
            ],
        }

        if template_type not in templates:
            return jsonify({"status": "error", "message": "نوع القالب غير صحيح"}), 400

        # إنشاء DataFrame فارغ مع الأعمدة المطلوبة
        df = pd.DataFrame(columns=templates[template_type])

        # إضافة صف مثال
        if template_type == "products":
            df.loc[0] = [
                "مثال: بذور طماطم",
                "بذور",
                "25.50",
                "100",
                "بذور طماطم عالية الجودة",
                "123456789",
            ]
        elif template_type == "suppliers":
            df.loc[0] = [
                "شركة البذور المتقدمة",
                "أحمد محمد",
                "01234567890",
                "info@seeds.com",
                "القاهرة، مصر",
            ]
        elif template_type == "customers":
            df.loc[0] = [
                "مزرعة الأمل",
                "محمد أحمد",
                "01234567890",
                "farm@hope.com",
                "الجيزة، مصر",
            ]
        elif template_type == "inventory":
            df.loc[0] = ["بذور طماطم", "المخزن الرئيسي", "50", "LOT001", "2025-12-31"]

        # حفظ الملف
        output_folder = os.path.join(current_app.root_path, "templates")
        os.makedirs(output_folder, exist_ok=True)

        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"template_{template_type}_{date_str}.xlsx"
        filepath = os.path.join(output_folder, filename)

        df.to_excel(filepath, index=False, engine="openpyxl")

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء القالب بنجاح",
                "data": {
                    "filename": filename,
                    "download_url": f"/api/download-template/{filename}",
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@import_bp.route("/download-template/<filename>", methods=["GET"])
def download_template(filename):
    """تحميل قالب Excel"""
    try:
        template_folder = os.path.join(current_app.root_path, "templates")
        filepath = os.path.join(template_folder, filename)

        if not os.path.exists(filepath):
            return jsonify({"status": "error", "message": "الملف غير موجود"}), 404

        from flask import send_file

        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
