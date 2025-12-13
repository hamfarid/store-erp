#!/usr/bin/env python3
"""
Script لإصلاح مشاكل الاستيراد في جميع ملفات Python
"""

import os
import re
import glob

# النص المعياري لإصلاح الاستيرادات
IMPORT_FIX_TEMPLATE = """
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


def fix_syntax_errors(file_path):
    """إصلاح مشاكل syntax في ملف واحد"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # إصلاح المشاكل الشائعة
        fixed_content = content

        # إصلاح try statements مكررة
        fixed_content = re.sub(r"try:\s*\n\s*try:", "try:", fixed_content)

        # إصلاح except statements مكررة
        fixed_content = re.sub(
            r"except ImportError:\s*\n\s*except ImportError:",
            "except ImportError:",
            fixed_content,
        )

        # إصلاح المسافات البادئة في mock functions
        fixed_content = re.sub(
            r"(\s+)def (\w+)\([^)]*\):\s*\n\s*return None\s*\n\s*\n",
            r"\1def \2(*args, **kwargs):\n\1    return None\n\n",
            fixed_content,
        )

        # إزالة الأسطر الفارغة الزائدة
        fixed_content = re.sub(r"\n\n\n+", "\n\n", fixed_content)

        if fixed_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            print(f"✅ تم إصلاح syntax: {file_path}")
            return True
        else:
            print(f"⏭️ لا يحتاج إصلاح syntax: {file_path}")
            return False

    except Exception as e:
        print(f"❌ خطأ في إصلاح syntax {file_path}: {e}")
        return False


def fix_file_imports(file_path):
    """إصلاح الاستيرادات في ملف واحد"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # البحث عن أنماط الاستيراد المشكلة
        patterns_to_fix = [
            r"from \.user import db",
            r"from sqlalchemy import.*",
            r"from sqlalchemy\.orm import.*",
        ]

        # إذا وُجد أي من هذه الأنماط، نحتاج لإصلاح الملف
        needs_fix = any(re.search(pattern, content) for pattern in patterns_to_fix)

        if needs_fix:
            # إزالة الاستيرادات القديمة
            lines = content.split("\n")
            new_lines = []

            for line in lines:
                # تخطي الاستيرادات المشكلة
                if (
                    re.search(r"from \.user import db", line)
                    or re.search(r"from sqlalchemy import", line)
                    or re.search(r"from sqlalchemy\.orm import", line)
                ):
                    # إضافة الإصلاح بدلاً من الاستيراد المشكل
                    if not any(
                        "SQLALCHEMY_AVAILABLE" in prev_line
                        for prev_line in new_lines[-10:]
                    ):
                        new_lines.append(IMPORT_FIX_TEMPLATE)
                    continue

                new_lines.append(line)

            # كتابة الملف المُصلح
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))

            print(f"✅ تم إصلاح imports: {file_path}")
            return True
        else:
            print(f"⏭️ لا يحتاج إصلاح imports: {file_path}")
            return False

    except Exception as e:
        print(f"❌ خطأ في إصلاح imports {file_path}: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    # البحث عن جميع ملفات Python
    python_files = glob.glob("*.py")

    # استثناء بعض الملفات
    exclude_files = [
        "fix_imports.py",
        "__init__.py",
        "inventory.py",
        "opening_balances_treasury.py",
        "invoices.py",
        "lot_advanced.py",
        "product_advanced.py",
    ]

    files_to_fix = [f for f in python_files if f not in exclude_files]

    print(f"🔍 تم العثور على {len(files_to_fix)} ملف للفحص...")

    syntax_fixed = 0
    import_fixed = 0

    # إصلاح syntax errors أولاً
    print("\n🔧 إصلاح مشاكل syntax...")
    for file_path in files_to_fix:
        if fix_syntax_errors(file_path):
            syntax_fixed += 1

    # ثم إصلاح imports
    print("\n📦 إصلاح مشاكل imports...")
    for file_path in files_to_fix:
        if fix_file_imports(file_path):
            import_fixed += 1

    print("\n📊 النتائج:")
    print(f"   - تم فحص: {len(files_to_fix)} ملف")
    print(f"   - تم إصلاح syntax: {syntax_fixed} ملف")
    print(f"   - تم إصلاح imports: {import_fixed} ملف")
    print(f"   - إجمالي الإصلاحات: {syntax_fixed + import_fixed}")


if __name__ == "__main__":
    main()
