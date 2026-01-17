#!/usr/bin/env python3
"""
سكريبت إصلاح مشاكل الاستيراد في النظام
"""

import os
import re
import shutil
from pathlib import Path


def backup_file(file_path):
    """إنشاء نسخة احتياطية من الملف"""
    backup_path = f"{file_path}.backup"
    shutil.copy2(file_path, backup_path)
    print(f"✓ تم إنشاء نسخة احتياطية: {backup_path}")


def fix_customer_imports():
    """إصلاح استيرادات Customer"""
    files_to_fix = [
        "src/routes/excel_import.py",
        "src/routes/excel_import_clean.py",
        "src/routes/export.py",
        "src/routes/import_data.py",
        "src/routes/partners.py",
        "src/routes/reports.py",
        "src/routes/settings.py",
        "src/services/automation_service.py",
        "src/services/customer_supplier_accounts_service.py",
        "src/services/interactive_dashboard_service.py",
        "src/services/permission_service.py",
        "src/services/report_service.py",
    ]

    pattern = r"from models\.partners import.*Customer"
    replacement = "from models.customer import Customer"

    fixed_count = 0

    for file_path in files_to_fix:
        if os.path.exists(file_path):
            try:
                backup_file(file_path)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # إصلاح الاستيراد
                if "from models.partners import" in content and "Customer" in content:
                    # استبدال الاستيراد المختلط
                    content = re.sub(
                        r"from models\.partners import ([^,]*,\s*)?Customer(,\s*[^,]*)?",
                        lambda m: f"from models.customer import Customer\nfrom models.partners import {m.group(1) or ''}{m.group(2) or ''}".replace(
                            "import ,", "import"
                        ).replace(
                            "import \n", ""
                        ),
                        content,
                    )

                    # تنظيف الأسطر الفارغة
                    content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"✓ تم إصلاح: {file_path}")
                fixed_count += 1

            except Exception as e:
                print(f"✗ خطأ في إصلاح {file_path}: {e}")
        else:
            print(f"⚠ الملف غير موجود: {file_path}")

    print(f"\n📊 تم إصلاح {fixed_count} ملف")


def remove_duplicate_supplier():
    """إزالة تعريف Supplier المكرر من partners.py"""
    file_path = "src/models/partners.py"

    if os.path.exists(file_path):
        backup_file(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # البحث عن بداية ونهاية تعريف Supplier
        supplier_start = None
        supplier_end = None

        for i, line in enumerate(lines):
            if "class Supplier(db.Model):" in line:
                supplier_start = i
            elif (
                supplier_start is not None
                and line.startswith("class ")
                and "Supplier" not in line
            ):
                supplier_end = i
                break

        if supplier_start is not None:
            if supplier_end is None:
                supplier_end = len(lines)

            # إزالة تعريف Supplier
            new_lines = lines[:supplier_start] + lines[supplier_end:]

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            print(f"✓ تم حذف تعريف Supplier المكرر من {file_path}")
        else:
            print(f"⚠ لم يتم العثور على تعريف Supplier في {file_path}")


def update_models_init():
    """تحديث ملف models/__init__.py"""
    file_path = "src/models/__init__.py"

    new_content = '''# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات - إصدار موحد ومحسن
Unified and Enhanced Database Models Package
"""

# استيراد قاعدة البيانات
try:
    from .user import db
except ImportError:
    class MockDB:
        class Model:
            pass
        def __init__(self):
            pass
    db = MockDB()

# استيراد النماذج الأساسية
try:
    from .user import User, Role
except ImportError:
    User = None
    Role = None

try:
    from .inventory import Category, Warehouse, Product, StockMovement
except ImportError:
    Category = None
    Warehouse = None
    Product = None
    StockMovement = None

try:
    from .customer import Customer
except ImportError:
    Customer = None

try:
    from .supplier import Supplier
except ImportError:
    Supplier = None

try:
    from .invoice import Invoice, InvoiceItem, Payment
except ImportError:
    Invoice = None
    InvoiceItem = None
    Payment = None

# التعدادات والثوابت الموحدة
class UserRole:
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"

class ProductType:
    SIMPLE = "simple"
    VARIABLE = "variable"
    SERVICE = "service"

class MovementType:
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"

class InvoiceStatus:
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

# قائمة التصدير الموحدة
__all__ = [
    'db',
    'User', 'Role',
    'Category', 'Warehouse', 'Product', 'StockMovement',
    'Customer',
    'Supplier', 
    'Invoice', 'InvoiceItem', 'Payment',
    'UserRole', 'ProductType', 'MovementType', 'InvoiceStatus'
]
'''

    backup_file(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ تم تحديث {file_path}")


def main():
    """الدالة الرئيسية"""
    print("🔧 بدء إصلاح مشاكل الاستيراد في النظام...")
    print("=" * 50)

    print("\n1️⃣ إصلاح استيرادات Customer...")
    fix_customer_imports()

    print("\n2️⃣ إزالة تعريف Supplier المكرر...")
    remove_duplicate_supplier()

    print("\n3️⃣ تحديث ملف models/__init__.py...")
    update_models_init()

    print("\n" + "=" * 50)
    print("✅ تم الانتهاء من إصلاح مشاكل الاستيراد!")
    print("📝 تم إنشاء نسخ احتياطية من جميع الملفات المعدلة")
    print("🧪 يُنصح بإجراء اختبارات شاملة للتأكد من سلامة النظام")


if __name__ == "__main__":
    main()
