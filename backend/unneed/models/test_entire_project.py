#!/usr/bin/env python3
"""
Script شامل لاختبار جميع ملفات Python في المشروع
"""

import os
import sys
import glob
import importlib.util
import traceback
from pathlib import Path


def find_all_python_files(root_dir):
    """البحث عن جميع ملفات Python في المشروع"""
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        # تجاهل مجلدات معينة
        dirs[:] = [
            d
            for d in dirs
            if d not in ["__pycache__", ".git", ".venv", "venv", "node_modules"]
        ]

        for file in files:
            if file.endswith(".py") and not file.startswith("test_"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, root_dir)
                python_files.append(relative_path)

    return sorted(python_files)


def test_file_syntax(file_path):
    """اختبار syntax الملف"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # محاولة compile الكود
        compile(content, file_path, "exec")
        return True, None
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def test_file_import(file_path):
    """اختبار استيراد الملف"""
    try:
        # تحويل المسار إلى module name
        module_name = file_path.replace("/", ".").replace("\\", ".").replace(".py", "")

        # محاولة استيراد الملف
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return False, "Could not create module spec"

        module = importlib.util.module_from_spec(spec)

        # إضافة المسار إلى sys.path مؤقتاً
        original_path = sys.path.copy()
        file_dir = os.path.dirname(os.path.abspath(file_path))
        if file_dir not in sys.path:
            sys.path.insert(0, file_dir)

        try:
            spec.loader.exec_module(module)
            return True, None
        finally:
            sys.path = original_path

    except ImportError as e:
        return False, f"Import Error: {e}"
    except Exception as e:
        return False, f"Runtime Error: {e}"


def main():
    """الدالة الرئيسية"""
    # تحديد المجلد الجذر للمشروع
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, "..", "..", "..")
    project_root = os.path.abspath(project_root)

    print(f"🔍 فحص المشروع في: {project_root}")
    print("=" * 80)

    # البحث عن جميع ملفات Python
    python_files = find_all_python_files(project_root)

    print(f"📁 تم العثور على {len(python_files)} ملف Python")
    print("=" * 80)

    syntax_passed = 0
    syntax_failed = 0
    import_passed = 0
    import_failed = 0

    failed_files = []

    for file_path in python_files:
        full_path = os.path.join(project_root, file_path)
        print(f"\n📄 اختبار: {file_path}")

        # اختبار syntax
        syntax_ok, syntax_error = test_file_syntax(full_path)
        if syntax_ok:
            print(f"  ✅ Syntax: صحيح")
            syntax_passed += 1

            # اختبار الاستيراد فقط إذا كان syntax صحيح
            import_ok, import_error = test_file_import(full_path)
            if import_ok:
                print(f"  ✅ Import: نجح")
                import_passed += 1
            else:
                print(f"  ❌ Import: فشل - {import_error}")
                import_failed += 1
                failed_files.append((file_path, "import", import_error))
        else:
            print(f"  ❌ Syntax: فشل - {syntax_error}")
            syntax_failed += 1
            import_failed += 1  # نعتبر الاستيراد فاشل أيضاً
            failed_files.append((file_path, "syntax", syntax_error))

    # النتائج النهائية
    print("\n" + "=" * 80)
    print(f"📊 النتائج النهائية:")
    print(f"   📁 إجمالي الملفات: {len(python_files)}")
    print(f"   ✅ Syntax صحيح: {syntax_passed}")
    print(f"   ❌ Syntax خاطئ: {syntax_failed}")
    print(f"   ✅ Import نجح: {import_passed}")
    print(f"   ❌ Import فشل: {import_failed}")

    success_rate = (import_passed / len(python_files)) * 100
    print(f"   📈 معدل النجاح: {success_rate:.1f}%")

    if failed_files:
        print(f"\n❌ الملفات الفاشلة ({len(failed_files)}):")
        for file_path, error_type, error_msg in failed_files:
            print(f"   - {file_path} ({error_type}): {error_msg}")
    else:
        print(f"\n🎉 جميع الملفات تعمل بشكل مثالي!")

    return len(failed_files) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
