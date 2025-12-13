#!/usr/bin/env python3
"""
Script شامل لإصلاح جميع مشاكل ملفات Python
"""

import glob
import re
import os

# النص المعياري للاستيرادات الآمنة
SAFE_IMPORTS = """
try:
    from sqlalchemy import (
        Column, Integer, String, Float, DateTime, Boolean,
        Text, Enum, Date, ForeignKey, Numeric
    )
    from sqlalchemy.orm import relationship
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # SQLAlchemy not available - create mock objects
    def Column(*args, **kwargs):
        return None
    def Integer():
        return None
    def String(length=None):
        return None
    def Float():
        return None
    def DateTime():
        return None
    def Boolean():
        return None
    def Text():
        return None
    def Enum(*args, **kwargs):
        return None
    def Date():
        return None
    def ForeignKey(*args, **kwargs):
        return None
    def Numeric(*args, **kwargs):
        return None
    def relationship(*args, **kwargs):
        return None
    SQLALCHEMY_AVAILABLE = False

# محاولة استيراد قاعدة البيانات
try:
    from database import db  # type: ignore
except ImportError:
    try:
        from ..database import db  # type: ignore
    except ImportError:
        try:
            from user import db  # type: ignore
        except ImportError:
            # إنشاء mock db إذا لم تكن متوفرة
            class MockDB:
                class Model:
                    def __init__(self, **kwargs):
                        for key, value in kwargs.items():
                            setattr(self, key, value)
                    def to_dict(self):
                        return {}
                Column = Column
                Integer = Integer
                String = String
                Float = Float
                DateTime = DateTime
                Boolean = Boolean
                Text = Text
                Enum = Enum
                Date = Date
                ForeignKey = ForeignKey
                Numeric = Numeric
                relationship = relationship
            db = MockDB()
"""


def clean_file_completely(file_path):
    """تنظيف ملف بالكامل وإعادة بنائه"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        clean_lines = []

        # إضافة header إذا كان موجود
        for line in lines[:10]:  # أول 10 أسطر للبحث عن header
            if line.startswith('"""') or line.startswith("#"):
                clean_lines.append(line)
            elif line.strip() == "":
                clean_lines.append(line)
            else:
                break

        # إضافة الاستيرادات الأساسية
        clean_lines.append("")
        clean_lines.append("from datetime import datetime, timezone")
        clean_lines.append("import enum")
        clean_lines.append(SAFE_IMPORTS)
        clean_lines.append("")

        # إضافة باقي الكود مع تنظيف
        in_class = False
        in_function = False
        indent_level = 0

        for line in lines:
            stripped = line.strip()

            # تخطي الاستيرادات القديمة
            if (
                stripped.startswith("from sqlalchemy")
                or stripped.startswith("from user import")
                or stripped.startswith("from ..database import")
                or stripped.startswith("from database import")
                or stripped.startswith("try:")
                and "sqlalchemy"
                in content[content.find(line) : content.find(line) + 200]
                or stripped.startswith("except ImportError:")
                or stripped.startswith("SQLALCHEMY_AVAILABLE")
                or stripped.startswith("def Column(")
                or stripped.startswith("def Integer(")
                or stripped.startswith("def String(")
                or stripped.startswith("class MockDB")
            ):
                continue

            # تخطي الأسطر الفارغة الزائدة
            if (
                stripped == ""
                and len(clean_lines) > 0
                and clean_lines[-1].strip() == ""
            ):
                continue

            # إضافة الكود المفيد
            if (
                stripped.startswith("class ")
                or stripped.startswith("def ")
                or stripped.startswith("from datetime")
                or stripped.startswith("import enum")
                or stripped  # أي سطر غير فارغ
                or (not stripped and in_class)
            ):  # أسطر فارغة داخل الكلاسات

                clean_lines.append(line)

        # كتابة الملف النظيف
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(clean_lines))

        print(f"✅ تم تنظيف: {file_path}")
        return True

    except Exception as e:
        print(f"❌ خطأ في تنظيف {file_path}: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    # البحث عن جميع ملفات Python
    python_files = glob.glob("*.py")

    # استثناء بعض الملفات
    exclude_files = [
        "fix_all_files.py",
        "fix_imports.py",
        "__init__.py",
        "inventory.py",
        "opening_balances_treasury.py",
        "invoices.py",
        "lot_advanced.py",
        "product_advanced.py",
        "user.py",
    ]

    files_to_fix = [f for f in python_files if f not in exclude_files]

    print(f"🔍 تم العثور على {len(files_to_fix)} ملف للتنظيف...")

    cleaned_count = 0
    for file_path in files_to_fix:
        if clean_file_completely(file_path):
            cleaned_count += 1

    print(f"\n📊 النتائج:")
    print(f"   - تم فحص: {len(files_to_fix)} ملف")
    print(f"   - تم تنظيف: {cleaned_count} ملف")


if __name__ == "__main__":
    main()
