#!/usr/bin/env python3
"""
سكريبت إصلاح سريع للمشاكل العاجلة
Quick Fix Script for Critical Issues
"""

import os
import shutil
import re
from datetime import datetime


class QuickFixer:
    def __init__(self):
        self.fixes_applied = []
        self.backup_dir = f"quick_fix_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def create_backup(self, file_path):
        """إنشاء نسخة احتياطية من الملف"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        backup_path = os.path.join(self.backup_dir, os.path.basename(file_path))
        shutil.copy2(file_path, backup_path)
        return backup_path

    def fix_sqlalchemy_issue(self):
        """إصلاح مشكلة SQLAlchemy"""
        print("🔧 إصلاح مشكلة SQLAlchemy...")

        app_file = "app.py"
        if os.path.exists(app_file):
            self.create_backup(app_file)

            with open(app_file, "r", encoding="utf-8") as f:
                content = f.read()

            # البحث عن مشكلة init_app
            if "db.init_app(app)" not in content:
                # إضافة db.init_app(app) في المكان المناسب
                pattern = r"(app = Flask\(__name__\).*?\n)"
                replacement = r"\1    db.init_app(app)\n"

                if re.search(pattern, content, re.DOTALL):
                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

                    with open(app_file, "w", encoding="utf-8") as f:
                        f.write(content)

                    self.fixes_applied.append("✅ إصلاح SQLAlchemy initialization")
                else:
                    self.fixes_applied.append("⚠️ لم يتم العثور على نمط Flask app")
            else:
                self.fixes_applied.append("ℹ️ SQLAlchemy initialization موجود بالفعل")
        else:
            self.fixes_applied.append("❌ ملف app.py غير موجود")

    def remove_hardcoded_passwords(self):
        """إزالة كلمات المرور الثابتة"""
        print("🔒 إزالة كلمات المرور الثابتة...")

        files_to_check = [
            "create_admin_direct.py",
            "create_admin_user.py",
            "simple_reports_server.js",
        ]

        for file_path in files_to_check:
            if os.path.exists(file_path):
                self.create_backup(file_path)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # استبدال كلمات المرور الثابتة
                patterns = [
                    (
                        r"password='admin123'",
                        "password=os.getenv('ADMIN_PASSWORD', 'change_me')",
                    ),
                    (
                        r'password === "admin123"',
                        "password === process.env.ADMIN_PASSWORD",
                    ),
                    (
                        r"password.*=.*'admin123'",
                        "password=os.getenv('ADMIN_PASSWORD', 'change_me')",
                    ),
                ]

                modified = False
                for pattern, replacement in patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        modified = True

                if modified:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.fixes_applied.append(
                        f"✅ إزالة كلمات مرور ثابتة من {file_path}"
                    )
                else:
                    self.fixes_applied.append(
                        f"ℹ️ لا توجد كلمات مرور ثابتة في {file_path}"
                    )

    def cleanup_duplicate_databases(self):
        """تنظيف قواعد البيانات المكررة"""
        print("🗄️ تنظيف قواعد البيانات المكررة...")

        # قائمة قواعد البيانات المكررة للحذف
        duplicate_dbs = [
            "src/inventory.db",
            "src/instance/inventory.db",
            "instance/inventory_encrypted_test_983efc.db",
            "instance/locktest_smoke.db",
        ]

        # الاحتفاظ بقاعدة البيانات الرئيسية
        main_db = "instance/inventory.db"

        if os.path.exists(main_db):
            for db_path in duplicate_dbs:
                if os.path.exists(db_path):
                    # إنشاء نسخة احتياطية
                    backup_path = self.create_backup(db_path)

                    # حذف الملف المكرر
                    os.remove(db_path)
                    self.fixes_applied.append(f"✅ حذف قاعدة بيانات مكررة: {db_path}")
                    self.fixes_applied.append(f"💾 نسخة احتياطية: {backup_path}")
        else:
            self.fixes_applied.append("⚠️ قاعدة البيانات الرئيسية غير موجودة")

    def remove_test_files_from_production(self):
        """إزالة ملفات الاختبار من الإنتاج"""
        print("🧪 إزالة ملفات الاختبار...")

        # إنشاء مجلد للملفات المحذوفة
        test_archive = "test_files_archive"
        if not os.path.exists(test_archive):
            os.makedirs(test_archive)

        # ملفات الاختبار للنقل
        test_patterns = ["test_*.py", "*test*.py", "*debug*.py", "requirements-dev.txt"]

        import glob

        moved_count = 0

        for pattern in test_patterns:
            for file_path in glob.glob(pattern):
                if os.path.isfile(file_path):
                    # نقل الملف بدلاً من حذفه
                    dest_path = os.path.join(test_archive, os.path.basename(file_path))
                    shutil.move(file_path, dest_path)
                    moved_count += 1
                    self.fixes_applied.append(
                        f"📦 نقل ملف اختبار: {file_path} -> {dest_path}"
                    )

        if moved_count > 0:
            self.fixes_applied.append(
                f"✅ تم نقل {moved_count} ملف اختبار إلى {test_archive}"
            )
        else:
            self.fixes_applied.append("ℹ️ لم يتم العثور على ملفات اختبار للنقل")

    def fix_duplicate_files(self):
        """إصلاح الملفات المكررة"""
        print("📁 إصلاح الملفات المكررة...")

        # قائمة الملفات المكررة للحذف (الاحتفاظ بالنسخة في src/)
        duplicate_files = [
            ("database.py", "src/database.py"),  # حذف الأول، الاحتفاظ بالثاني
        ]

        for duplicate, keep in duplicate_files:
            if os.path.exists(duplicate) and os.path.exists(keep):
                self.create_backup(duplicate)
                os.remove(duplicate)
                self.fixes_applied.append(
                    f"✅ حذف ملف مكرر: {duplicate} (الاحتفاظ بـ {keep})"
                )
            elif os.path.exists(duplicate):
                self.fixes_applied.append(
                    f"ℹ️ ملف {duplicate} موجود ولكن {keep} غير موجود"
                )

    def update_env_security(self):
        """تحديث إعدادات الأمان في .env"""
        print("🔐 تحديث إعدادات الأمان...")

        env_file = ".env"
        if os.path.exists(env_file):
            self.create_backup(env_file)

            with open(env_file, "r", encoding="utf-8") as f:
                content = f.read()

            # إضافة متغيرات أمان جديدة إذا لم تكن موجودة
            security_vars = [
                "ADMIN_PASSWORD=change_this_password_immediately",
                "PRODUCTION_MODE=True",
                "DEBUG_MODE=False",
            ]

            modified = False
            for var in security_vars:
                var_name = var.split("=")[0]
                if var_name not in content:
                    content += f"\n# Added by quick_fix\n{var}\n"
                    modified = True

            if modified:
                with open(env_file, "w", encoding="utf-8") as f:
                    f.write(content)
                self.fixes_applied.append("✅ إضافة متغيرات أمان جديدة إلى .env")
            else:
                self.fixes_applied.append("ℹ️ متغيرات الأمان موجودة بالفعل")
        else:
            self.fixes_applied.append("⚠️ ملف .env غير موجود")

    def generate_report(self):
        """إنشاء تقرير الإصلاحات"""
        print("\n" + "=" * 60)
        print("📊 تقرير الإصلاحات السريعة")
        print("=" * 60)

        print(f"🕒 وقت التنفيذ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 مجلد النسخ الاحتياطية: {self.backup_dir}")
        print(f"🔧 عدد الإصلاحات: {len(self.fixes_applied)}")

        print("\n📋 تفاصيل الإصلاحات:")
        print("-" * 40)

        for i, fix in enumerate(self.fixes_applied, 1):
            print(f"{i:2d}. {fix}")

        # حفظ التقرير
        report_file = f"quick_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("تقرير الإصلاحات السريعة\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"وقت التنفيذ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"مجلد النسخ الاحتياطية: {self.backup_dir}\n")
            f.write(f"عدد الإصلاحات: {len(self.fixes_applied)}\n\n")
            f.write("تفاصيل الإصلاحات:\n")
            f.write("-" * 30 + "\n")
            for i, fix in enumerate(self.fixes_applied, 1):
                f.write(f"{i:2d}. {fix}\n")

        print(f"\n💾 تم حفظ التقرير في: {report_file}")

        # تقييم النجاح
        success_count = len([fix for fix in self.fixes_applied if fix.startswith("✅")])
        total_count = len(self.fixes_applied)
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0

        print(f"\n📈 معدل النجاح: {success_rate:.1f}% ({success_count}/{total_count})")

        if success_rate >= 80:
            print("🎉 الإصلاحات تمت بنجاح!")
        elif success_rate >= 60:
            print("👍 معظم الإصلاحات تمت بنجاح")
        else:
            print("⚠️ بعض الإصلاحات تحتاج مراجعة يدوية")

    def run_all_fixes(self):
        """تشغيل جميع الإصلاحات"""
        print("🚀 بدء الإصلاحات السريعة...")
        print("=" * 60)

        # تشغيل جميع الإصلاحات
        self.fix_sqlalchemy_issue()
        self.remove_hardcoded_passwords()
        self.cleanup_duplicate_databases()
        self.remove_test_files_from_production()
        self.fix_duplicate_files()
        self.update_env_security()

        # إنشاء التقرير
        self.generate_report()


def main():
    """الدالة الرئيسية"""
    fixer = QuickFixer()
    fixer.run_all_fixes()


if __name__ == "__main__":
    main()
