#!/usr/bin/env python3
"""
سكريبت فحص شامل لتنصيب وتشغيل النظام
ملف: system_deployment_check.py
"""

import os
import sys
import subprocess
import json
import time
import requests
from datetime import datetime
from pathlib import Path
import shutil


class SystemDeploymentChecker:
    """فئة فحص تنصيب وتشغيل النظام"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backend_dir = self.base_dir / "backend"
        self.frontend_dir = self.base_dir / "frontend"
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }

    def log_check(self, name, status, message="", level="info"):
        """تسجيل نتيجة الفحص"""
        self.results['checks'].append({
            'name': name,
            'status': status,
            'message': message,
            'level': level,
            'timestamp': datetime.now().isoformat()
        })

        self.results['summary']['total'] += 1
        if status == 'passed':
            self.results['summary']['passed'] += 1
            print(f"✅ {name}")
        elif status == 'failed':
            self.results['summary']['failed'] += 1
            print(f"❌ {name}: {message}")
        elif status == 'warning':
            self.results['summary']['warnings'] += 1
            print(f"⚠️ {name}: {message}")

        if message and level == "info":
            print(f"   ℹ️ {message}")

    def check_python_environment(self):
        """فحص بيئة Python"""
        print("\n🐍 فحص بيئة Python...")

        # فحص إصدار Python
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 8:
            self.log_check(
                "Python Version",
                "passed",
                f"Python {python_version.major}.{python_version.minor}.{python_version.micro}"
            )
        else:
            self.log_check(
                "Python Version",
                "failed",
                f"Python {python_version.major}.{python_version.minor} - يتطلب 3.8+"
            )

        # فحص pip
        try:
            result = subprocess.run([sys.executable,
                                     "-m",
                                     "pip",
                                     "--version"],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                self.log_check("pip Installation",
                               "passed",
                               result.stdout.strip())
            else:
                self.log_check("pip Installation", "failed", "pip غير متاح")
        except Exception as e:
            self.log_check("pip Installation", "failed", str(e))

    def check_backend_setup(self):
        """فحص إعداد Backend"""
        print("\n🔧 فحص إعداد Backend...")

        # فحص وجود مجلد Backend
        if self.backend_dir.exists():
            self.log_check("Backend Directory", "passed")
        else:
            self.log_check("Backend Directory", "failed", "مجلد Backend غير موجود")
            return

        # فحص ملف requirements
        requirements_files = [
            "requirements.txt",
            "requirements_comprehensive.txt",
            "requirements_integrated.txt"
        ]

        found_requirements = False
        for req_file in requirements_files:
            req_path = self.backend_dir / req_file
            if req_path.exists():
                self.log_check(f"Requirements File ({req_file})", "passed")
                found_requirements = True
                break

        if not found_requirements:
            self.log_check("Requirements Files", "failed", "لا توجد ملفات requirements")

        # فحص البيئة الافتراضية
        venv_path = self.backend_dir / "venv"
        if venv_path.exists():
            self.log_check("Virtual Environment", "passed")
        else:
            self.log_check("Virtual Environment", "warning", "البيئة الافتراضية غير موجودة")

        # فحص قاعدة البيانات
        db_paths = [
            self.backend_dir / "instance" / "inventory.db",
            self.backend_dir / "src" / "inventory.db"
        ]

        db_found = False
        for db_path in db_paths:
            if db_path.exists():
                size = db_path.stat().st_size
                self.log_check("Database File", "passed", f"حجم: {size} بايت")
                db_found = True
                break

        if not db_found:
            self.log_check("Database File", "warning", "قاعدة البيانات غير موجودة")

        # فحص ملفات الخادم
        server_files = [
            "src/main.py",
            "start_server.py",
            "run_server.py"
        ]

        for server_file in server_files:
            server_path = self.backend_dir / server_file
            if server_path.exists():
                self.log_check(f"Server File ({server_file})", "passed")
            else:
                self.log_check(f"Server File ({server_file})", "warning", "غير موجود")

    def check_frontend_setup(self):
        """فحص إعداد Frontend"""
        print("\n⚛️ فحص إعداد Frontend...")

        # فحص وجود مجلد Frontend
        if self.frontend_dir.exists():
            self.log_check("Frontend Directory", "passed")
        else:
            self.log_check("Frontend Directory", "failed", "مجلد Frontend غير موجود")
            return

        # فحص package.json
        package_json = self.frontend_dir / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)

                self.log_check("package.json", "passed", f"اسم المشروع: {package_data.get('name', 'غير محدد')}")

                # فحص السكريبتات المطلوبة
                scripts = package_data.get('scripts', {})
                required_scripts = ['dev', 'build', 'preview']

                for script in required_scripts:
                    if script in scripts:
                        self.log_check(f"Script ({script})", "passed")
                    else:
                        self.log_check(f"Script ({script})", "warning", "غير موجود")

            except Exception as e:
                self.log_check("package.json", "failed", f"خطأ في قراءة الملف: {e}")
        else:
            self.log_check("package.json", "failed", "ملف package.json غير موجود")

        # فحص node_modules
        node_modules = self.frontend_dir / "node_modules"
        if node_modules.exists():
            # عد المكتبات المثبتة
            try:
                packages_count = len([d for d in node_modules.iterdir() if d.is_dir()])
                self.log_check("Node Modules",
                    "passed",
                    f"{packages_count} مكتبة مثبتة")
            except:
                self.log_check("Node Modules", "passed", "موجود")
        else:
            self.log_check("Node Modules", "warning", "المكتبات غير مثبتة - تشغيل npm install")

        # فحص ملفات التكوين
        config_files = [
            "vite.config.js",
            "tailwind.config.js",
            "index.html"
        ]

        for config_file in config_files:
            config_path = self.frontend_dir / config_file
            if config_path.exists():
                self.log_check(f"Config File ({config_file})", "passed")
            else:
                self.log_check(f"Config File ({config_file})", "warning", "غير موجود")

    def check_network_connectivity(self):
        """فحص الاتصال الشبكي"""
        print("\n🌐 فحص الاتصال الشبكي...")

        # فحص Backend
        backend_urls = [
            "http://172.16.16.27:8000",
            "http://localhost:8000",
            "http://127.0.0.1:8000"
        ]

        backend_accessible = False
        for url in backend_urls:
            try:
                response = requests.get(f"{url}/api/health", timeout=5)
                if response.status_code == 200:
                    self.log_check(f"Backend Connectivity ({url})", "passed")
                    backend_accessible = True
                    break
                else:
                    self.log_check(f"Backend Connectivity ({url})", "warning", f"Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.log_check(f"Backend Connectivity ({url})", "failed", str(e))

        if not backend_accessible:
            self.log_check("Backend Overall", "failed", "Backend غير متاح على أي منفذ")

        # فحص Frontend
        frontend_urls = [
            "http://localhost:3004",
            "http://127.0.0.1:3004"
        ]

        for url in frontend_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.log_check(f"Frontend Connectivity ({url})", "passed")
                    break
                else:
                    self.log_check(f"Frontend Connectivity ({url})", "warning", f"Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.log_check(f"Frontend Connectivity ({url})", "failed", str(e))

    def check_system_resources(self):
        """فحص موارد النظام"""
        print("\n💻 فحص موارد النظام...")

        # فحص مساحة القرص
        try:
            total, used, free = shutil.disk_usage(self.base_dir)

            free_gb = free // (1024**3)
            if free_gb > 1:
                self.log_check("Disk Space", "passed", f"{free_gb} GB متاح")
            else:
                self.log_check("Disk Space", "warning", f"{free_gb} GB متاح - قليل")
        except Exception as e:
            self.log_check("Disk Space", "failed", str(e))

        # فحص الذاكرة (إذا كان psutil متاح)
        try:
            import psutil
            memory = psutil.virtual_memory()
            available_gb = memory.available // (1024**3)

            if available_gb > 2:
                self.log_check("Memory", "passed", f"{available_gb} GB متاح")
            else:
                self.log_check("Memory", "warning", f"{available_gb} GB متاح - قليل")
        except ImportError:
            self.log_check("Memory Check", "warning", "psutil غير مثبت")
        except Exception as e:
            self.log_check("Memory", "failed", str(e))

    def run_all_checks(self):
        """تشغيل جميع الفحوصات"""
        print("🚀 === بدء فحص تنصيب وتشغيل النظام ===")
        print(f"⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 المجلد: {self.base_dir}")

        # تشغيل جميع الفحوصات
        self.check_python_environment()
        self.check_backend_setup()
        self.check_frontend_setup()
        self.check_network_connectivity()
        self.check_system_resources()

        # عرض النتائج النهائية
        self.print_summary()

        # حفظ النتائج
        self.save_results()

        return self.results

    def print_summary(self):
        """عرض ملخص النتائج"""
        print("\n📊 === ملخص فحص التنصيب ===")
        summary = self.results['summary']

        print(f"إجمالي الفحوصات: {summary['total']}")
        print(f"نجح: {summary['passed']}")
        print(f"فشل: {summary['failed']}")
        print(f"تحذيرات: {summary['warnings']}")

        if summary['total'] > 0:
            success_rate = (summary['passed'] / summary['total']) * 100
            print(f"معدل النجاح: {success_rate:.1f}%")

            if success_rate >= 90:
                print("🎉 النظام جاهز للتشغيل!")
            elif success_rate >= 70:
                print("✅ النظام يعمل مع بعض التحذيرات")
            else:
                print("⚠️ النظام يحتاج إلى إصلاحات")

        # عرض الأخطاء والتحذيرات
        failed_checks = [c for c in self.results['checks'] if c['status'] == 'failed']
        if failed_checks:
            print("\n❌ الفحوصات الفاشلة:")
            for check in failed_checks:
                print(f"  - {check['name']}: {check['message']}")

        warning_checks = [c for c in self.results['checks'] if c['status'] == 'warning']
        if warning_checks:
            print("\n⚠️ التحذيرات:")
            for check in warning_checks:
                print(f"  - {check['name']}: {check['message']}")

    def save_results(self):
        """حفظ النتائج في ملف"""
        results_file = self.base_dir / "deployment_check_results.json"
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 تم حفظ النتائج في: {results_file}")
        except Exception as e:
            print(f"❌ خطأ في حفظ النتائج: {e}")


def main():
    """الدالة الرئيسية"""
    checker = SystemDeploymentChecker()
    results = checker.run_all_checks()

    # إرجاع كود الخروج حسب النتائج
    if results['summary']['failed'] > 0:
        sys.exit(1)
    elif results['summary']['warnings'] > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
