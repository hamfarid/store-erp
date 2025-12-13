#!/usr/bin/env python3
"""
فحص شامل للواجهة الخلفية
ملف: backend_comprehensive_check.py
"""

import os
import sys
import json
import requests
import sqlite3
import importlib.util
from datetime import datetime
from pathlib import Path


class BackendComprehensiveChecker:
    """فئة فحص شامل للواجهة الخلفية"""

    def __init__(self):
        self.base_dir = Path(__file__).parent / "backend"
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'backend_structure': {},
            'api_endpoints': {},
            'database': {},
            'authentication': {},
            'models': {},
            'routes': {},
            'services': {},
            'summary': {
                'total_checks': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
        self.api_base_url = "http://172.16.16.27:8000"

    def log_check(self, category, name, status, message=""):
        """تسجيل نتيجة الفحص"""
        if category not in self.results:
            self.results[category] = {}

        self.results[category][name] = {
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }

        self.results['summary']['total_checks'] += 1
        if status == 'passed':
            self.results['summary']['passed'] += 1
            print(f"✅ {category}/{name}")
        elif status == 'failed':
            self.results['summary']['failed'] += 1
            print(f"❌ {category}/{name}: {message}")
        elif status == 'warning':
            self.results['summary']['warnings'] += 1
            print(f"⚠️ {category}/{name}: {message}")

        if message and status == 'passed':
            print(f"   ℹ️ {message}")

    def check_backend_structure(self):
        """فحص هيكل Backend"""
        print("\n🏗️ فحص هيكل Backend...")

        # فحص المجلدات الأساسية
        required_dirs = [
            "src",
            "src/models",
            "src/routes",
            "src/services",
            "src/config",
            "instance",
            "flask_session"
        ]

        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            if full_path.exists():
                self.log_check('backend_structure',
                    f'directory_{dir_path.replace("/", "_")}',
                    'passed')
            else:
                self.log_check('backend_structure',
                    f'directory_{dir_path.replace("/", "_")}',
                    'failed',
                    f'مجلد {dir_path} غير موجود')

        # فحص الملفات الأساسية
        required_files = [
            "src/main.py",
            "src/auth.py",
            "requirements.txt",
            "start_server.py"
        ]

        for file_path in required_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                self.log_check('backend_structure',
                    f'file_{file_path.replace("/", "_").replace(".", "_")}',
                    'passed',
                    f'حجم: {size} بايت')
            else:
                self.log_check('backend_structure',
                    f'file_{file_path.replace("/", "_").replace(".", "_")}',
                    'failed',
                    f'ملف {file_path} غير موجود')

    def check_database(self):
        """فحص قاعدة البيانات"""
        print("\n🗄️ فحص قاعدة البيانات...")

        db_paths = [
            self.base_dir / "instance" / "inventory.db",
            self.base_dir / "instance" / "inventory_enhanced.db"
        ]

        db_found = False
        for db_path in db_paths:
            if db_path.exists():
                db_found = True
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    # فحص الجداول
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()

                    self.log_check('database',
                        'connection',
                        'passed',
                        f'متصل بـ {db_path.name}')
                    self.log_check('database',
                        'tables_count',
                        'passed',
                        f'{len(tables)} جدول')

                    # فحص جداول أساسية
                    required_tables = ['users',
                        'products',
                        'categories',
                        'warehouses']
                    table_names = [table[0] for table in tables]

                    for table in required_tables:
                        if table in table_names:
                            cursor.execute(f"SELECT COUNT(*) FROM {table}")
                            count = cursor.fetchone()[0]
                            self.log_check('database',
                                f'table_{table}',
                                'passed',
                                f'{count} سجل')
                        else:
                            self.log_check('database',
                                f'table_{table}',
                                'warning',
                                f'جدول {table} غير موجود')

                    conn.close()
                    break

                except Exception as e:
                    self.log_check('database', 'connection', 'failed', str(e))

        if not db_found:
            self.log_check('database',
                'existence',
                'failed',
                'لا توجد قاعدة بيانات')

    def check_models(self):
        """فحص النماذج"""
        print("\n📋 فحص النماذج...")

        models_dir = self.base_dir / "src" / "models"
        if not models_dir.exists():
            self.log_check('models',
                'directory',
                'failed',
                'مجلد models غير موجود')
            return

        # فحص ملفات النماذج
        model_files = [
            "user.py",
            "inventory.py",
            "accounting_system.py",
            "partners.py",
            "invoices.py"
        ]

        for model_file in model_files:
            model_path = models_dir / model_file
            if model_path.exists():
                try:
                    # فحص محتوى الملف
                    with open(model_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # فحص وجود فئات النماذج
                    if 'class ' in content and 'db.Model' in content:
                        classes = content.count('class ')
                        self.log_check('models',
                            f'file_{model_file.replace(".", "_")}',
                            'passed',
                            f'{classes} فئة')
                    else:
                        self.log_check('models',
                            f'file_{model_file.replace(".", "_")}',
                            'warning',
                            'لا يحتوي على نماذج صحيحة')

                except Exception as e:
                    self.log_check('models',
                        f'file_{model_file.replace(".", "_")}',
                        'failed',
                        str(e))
            else:
                self.log_check('models',
                    f'file_{model_file.replace(".", "_")}',
                    'warning',
                    f'ملف {model_file} غير موجود')

    def check_routes(self):
        """فحص المسارات"""
        print("\n🛣️ فحص المسارات...")

        routes_dir = self.base_dir / "src" / "routes"
        if not routes_dir.exists():
            self.log_check('routes',
                'directory',
                'failed',
                'مجلد routes غير موجود')
            return

        # فحص ملفات المسارات
        route_files = list(routes_dir.glob("*.py"))

        for route_file in route_files:
            if route_file.name == "__init__.py":
                continue

            try:
                with open(route_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # فحص وجود blueprints و routes
                if 'Blueprint' in content:
                    routes_count = content.count('@')  # تقريبي لعدد المسارات
                    self.log_check('routes',
                        f'file_{route_file.stem}',
                        'passed',
                        f'~{routes_count} مسار')
                else:
                    self.log_check('routes',
                        f'file_{route_file.stem}',
                        'warning',
                        'لا يحتوي على Blueprint')

            except Exception as e:
                self.log_check('routes',
                    f'file_{route_file.stem}',
                    'failed',
                    str(e))

    def check_api_endpoints(self):
        """فحص نقاط API"""
        print("\n🌐 فحص نقاط API...")

        # قائمة نقاط API المطلوب فحصها
        endpoints = [
            ("/api/health", "فحص الصحة"),
            ("/api/auth/login", "تسجيل الدخول"),
            ("/dashboard/data", "بيانات لوحة التحكم"),
            ("/api/products", "المنتجات"),
            ("/api/categories", "الفئات"),
            ("/api/customers", "العملاء"),
            ("/api/suppliers", "الموردين"),
            ("/api/warehouses", "المخازن"),
            ("/accounting/cash-boxes", "الصناديق"),
            ("/accounting/payment-vouchers", "قسائم الدفع"),
            ("/batch_management/batches", "اللوطات"),
            ("/reports/inventory-report", "تقارير المخزون")
        ]

        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.api_base_url}{endpoint}",
                    timeout=5)

                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            self.log_check('api_endpoints',
                                f'endpoint_{endpoint.replace("/", "_").replace("-", "_")}',
                                'passed',
                                f'Status: {response.status_code}')
                        else:
                            self.log_check('api_endpoints',
                                f'endpoint_{endpoint.replace("/", "_").replace("-", "_")}',
                                'warning',
                                'استجابة غير JSON')
                    except Exception:
                        self.log_check('api_endpoints',
                            f'endpoint_{endpoint.replace("/", "_").replace("-", "_")}',
                            'warning',
                            'استجابة غير JSON صحيحة')
                elif response.status_code == 401:
                    self.log_check('api_endpoints',
                        f'endpoint_{endpoint.replace("/", "_").replace("-", "_")}',
                        'passed',
                        'يتطلب مصادقة (طبيعي)')
                else:
                    self.log_check('api_endpoints',
                        f'endpoint_{endpoint.replace("/", "_").replace("-", "_")}',
                        'failed',
                        f'Status: {response.status_code}')

            except requests.exceptions.ConnectionError:
                self.log_check('api_endpoints',
                    f'endpoint_{endpoint.replace("/", "_").replace("-", "_")}',
                    'failed',
                    'الخادم غير متاح')
            except Exception as e:
                self.log_check('api_endpoints',
                    f'endpoint_{endpoint.replace("/", "_").replace("-", "_")}',
                    'failed',
                    str(e))

    def check_authentication(self):
        """فحص نظام المصادقة"""
        print("\n🔐 فحص نظام المصادقة...")

        # فحص ملف المصادقة
        auth_file = self.base_dir / "src" / "auth.py"
        if auth_file.exists():
            try:
                with open(auth_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # فحص وجود فئات ووظائف المصادقة
                auth_components = [
                    ('AuthManager', 'مدير المصادقة'),
                    ('login_required', 'ديكوريتر المصادقة'),
                    ('hash_password', 'تشفير كلمة المرور'),
                    ('verify_password', 'التحقق من كلمة المرور')
                ]

                for component, description in auth_components:
                    if component in content:
                        self.log_check('authentication',
                            f'component_{component}',
                            'passed',
                            description)
                    else:
                        self.log_check('authentication',
                            f'component_{component}',
                            'warning',
                            f'{description} غير موجود')

            except Exception as e:
                self.log_check('authentication',
                    'file_auth_py',
                    'failed',
                    str(e))
        else:
            self.log_check('authentication',
                'file_auth_py',
                'failed',
                'ملف auth.py غير موجود')

        # اختبار تسجيل الدخول
        try:
            login_data = {
                "username": "admin",
                "password": "admin123"
            }

            response = requests.post(
                f"{self.api_base_url}/api/auth/login",
                json=login_data,
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('token'):
                    self.log_check('authentication',
                        'login_test',
                        'passed',
                        'تسجيل الدخول يعمل')
                else:
                    self.log_check('authentication',
                        'login_test',
                        'failed',
                        'استجابة تسجيل دخول غير صحيحة')
            else:
                self.log_check('authentication',
                    'login_test',
                    'failed',
                    f'فشل تسجيل الدخول: {response.status_code}')

        except Exception as e:
            self.log_check('authentication', 'login_test', 'failed', str(e))

    def check_services(self):
        """فحص الخدمات"""
        print("\n⚙️ فحص الخدمات...")

        services_dir = self.base_dir / "src" / "services"
        if services_dir.exists():
            service_files = list(services_dir.glob("*.py"))

            for service_file in service_files:
                if service_file.name == "__init__.py":
                    continue

                try:
                    with open(service_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'class ' in content or 'def ' in content:
                        self.log_check('services',
                            f'file_{service_file.stem}',
                            'passed',
                            'يحتوي على خدمات')
                    else:
                        self.log_check('services',
                            f'file_{service_file.stem}',
                            'warning',
                            'فارغ أو غير مكتمل')

                except Exception as e:
                    self.log_check('services',
                        f'file_{service_file.stem}',
                        'failed',
                        str(e))
        else:
            self.log_check('services',
                'directory',
                'warning',
                'مجلد services غير موجود')

    def run_all_checks(self):
        """تشغيل جميع الفحوصات"""
        print("🚀 === بدء فحص شامل للواجهة الخلفية ===")
        print(f"⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 المجلد: {self.base_dir}")

        # تشغيل جميع الفحوصات
        self.check_backend_structure()
        self.check_database()
        self.check_models()
        self.check_routes()
        self.check_api_endpoints()
        self.check_authentication()
        self.check_services()

        # عرض النتائج النهائية
        self.print_summary()

        # حفظ النتائج
        self.save_results()

        return self.results

    def print_summary(self):
        """عرض ملخص النتائج"""
        print("\n📊 === ملخص فحص الواجهة الخلفية ===")
        summary = self.results['summary']

        print(f"إجمالي الفحوصات: {summary['total_checks']}")
        print(f"نجح: {summary['passed']}")
        print(f"فشل: {summary['failed']}")
        print(f"تحذيرات: {summary['warnings']}")

        if summary['total_checks'] > 0:
            success_rate = (summary['passed'] / summary['total_checks']) * 100
            print(f"معدل النجاح: {success_rate:.1f}%")

            if success_rate >= 90:
                print("🎉 الواجهة الخلفية تعمل بشكل ممتاز!")
            elif success_rate >= 70:
                print("✅ الواجهة الخلفية تعمل مع بعض التحذيرات")
            else:
                print("⚠️ الواجهة الخلفية تحتاج إلى إصلاحات")

        # عرض الأخطاء والتحذيرات
        print("\n📋 تفاصيل الفئات:")
        for category, checks in self.results.items():
            if category == 'summary' or category == 'timestamp':
                continue

            if isinstance(checks, dict):
                passed = sum(1 for check in checks.values() if isinstance(check,
                    dict) and check.get('status') == 'passed')
                total = len(checks)
                if total > 0:
                    rate = (passed / total) * 100
                    print(f"📂 {category}: {passed}/{total} ({rate:.1f}%)")

    def save_results(self):
        """حفظ النتائج في ملف"""
        results_file = self.base_dir.parent / "backend_check_results.json"
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 تم حفظ النتائج في: {results_file}")
        except Exception as e:
            print(f"❌ خطأ في حفظ النتائج: {e}")


def main():
    """الدالة الرئيسية"""
    checker = BackendComprehensiveChecker()
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
