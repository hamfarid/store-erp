#!/usr/bin/env python3
"""
سكريبت تنظيف النظام من الملفات المكررة وغير المستخدمة
"""

import os
import shutil
from pathlib import Path
import hashlib


def get_file_hash(file_path):
    """حساب hash للملف للمقارنة"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None


def backup_file(file_path):
    """إنشاء نسخة احتياطية"""
    backup_path = f"{file_path}.cleanup_backup"
    try:
        shutil.copy2(file_path, backup_path)
        return True
    except:
        return False


def find_duplicate_files():
    """البحث عن الملفات المكررة"""
    print("🔍 البحث عن الملفات المكررة...")

    file_hashes = {}
    duplicates = []

    # فحص الملفات في النظام
    for root, dirs, files in os.walk("."):
        # تجاهل مجلدات معينة
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["__pycache__", "node_modules"]
        ]

        for file in files:
            if file.endswith((".py", ".jsx", ".js")):
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)

                if file_hash:
                    if file_hash in file_hashes:
                        duplicates.append((file_path, file_hashes[file_hash]))
                    else:
                        file_hashes[file_hash] = file_path

    return duplicates


def remove_backup_files():
    """إزالة ملفات النسخ الاحتياطية القديمة"""
    print("🗑️ إزالة ملفات النسخ الاحتياطية القديمة...")

    backup_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".backup"):
                backup_files.append(os.path.join(root, file))

    removed_count = 0
    for backup_file in backup_files:
        try:
            # التحقق من عمر الملف (أكثر من يوم)
            if os.path.getmtime(backup_file) < (os.time.time() - 86400):
                os.remove(backup_file)
                print(f"✓ تم حذف: {backup_file}")
                removed_count += 1
        except Exception as e:
            print(f"✗ خطأ في حذف {backup_file}: {e}")

    print(f"📊 تم حذف {removed_count} ملف نسخة احتياطية")


def clean_empty_directories():
    """إزالة المجلدات الفارغة"""
    print("📁 إزالة المجلدات الفارغة...")

    removed_count = 0
    for root, dirs, files in os.walk(".", topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"✓ تم حذف المجلد الفارغ: {dir_path}")
                    removed_count += 1
            except:
                pass

    print(f"📊 تم حذف {removed_count} مجلد فارغ")


def find_unused_imports():
    """البحث عن الاستيرادات غير المستخدمة"""
    print("📦 البحث عن الاستيرادات غير المستخدمة...")

    unused_imports = []

    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # البحث عن استيرادات غير مستخدمة بسيطة
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if line.strip().startswith(
                            "import "
                        ) or line.strip().startswith("from "):
                            # فحص بسيط للاستيراد غير المستخدم
                            import_name = line.split()[-1] if "import" in line else None
                            if import_name and import_name not in content.replace(
                                line, ""
                            ):
                                unused_imports.append((file_path, i + 1, line.strip()))

                except Exception as e:
                    continue

    return unused_imports


def optimize_requirements():
    """تحسين ملفات requirements"""
    print("📋 تحسين ملفات requirements...")

    req_files = [
        f
        for f in os.listdir(".")
        if f.startswith("requirements") and f.endswith(".txt")
    ]

    if len(req_files) > 3:
        print(f"⚠️ تم العثور على {len(req_files)} ملف requirements - يُنصح بتوحيدها")

        # اقتراح توحيد الملفات
        main_req = "requirements.txt"
        if os.path.exists(main_req):
            with open(main_req, "r") as f:
                main_content = set(f.read().strip().split("\n"))

            for req_file in req_files:
                if req_file != main_req:
                    try:
                        with open(req_file, "r") as f:
                            file_content = set(f.read().strip().split("\n"))

                        # البحث عن تبعيات إضافية
                        extra_deps = file_content - main_content
                        if extra_deps:
                            print(
                                f"📦 {req_file} يحتوي على تبعيات إضافية: {len(extra_deps)}"
                            )
                    except:
                        continue


def generate_cleanup_report():
    """إنشاء تقرير التنظيف"""
    print("\n" + "=" * 50)
    print("📊 تقرير تنظيف النظام")
    print("=" * 50)

    # إحصائيات الملفات
    total_files = 0
    total_size = 0

    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.startswith("."):
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    total_files += 1
                    total_size += size
                except:
                    continue

    print(f"📁 إجمالي الملفات: {total_files}")
    print(f"💾 إجمالي الحجم: {total_size / (1024*1024):.2f} MB")

    # فحص الملفات المكررة
    duplicates = find_duplicate_files()
    if duplicates:
        print(f"🔄 ملفات مكررة: {len(duplicates)}")
        for dup1, dup2 in duplicates[:5]:  # عرض أول 5 فقط
            print(f"   - {dup1} ≈ {dup2}")

    # فحص الاستيرادات غير المستخدمة
    unused = find_unused_imports()
    if unused:
        print(f"📦 استيرادات غير مستخدمة محتملة: {len(unused)}")

    print("\n✅ تم الانتهاء من تقرير التنظيف")


def main():
    """الدالة الرئيسية"""
    print("🧹 بدء تنظيف النظام...")
    print("=" * 50)

    # إزالة ملفات النسخ الاحتياطية القديمة
    remove_backup_files()

    print()
    # إزالة المجلدات الفارغة
    clean_empty_directories()

    print()
    # تحسين ملفات requirements
    optimize_requirements()

    print()
    # إنشاء تقرير شامل
    generate_cleanup_report()

    print("\n" + "=" * 50)
    print("✅ تم الانتهاء من تنظيف النظام!")
    print("💡 يُنصح بمراجعة التقرير واتخاذ الإجراءات المناسبة")


if __name__ == "__main__":
    main()
