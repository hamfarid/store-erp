#!/usr/bin/env python3
"""
Gaara ERP System Startup Script
===============================

This script provides an easy way to start the Gaara ERP system with all necessary components.
It handles both development and production environments.

Usage:
    python start_system.py [--production] [--port PORT] [--help]

Options:
    --production    Start in production mode
    --port PORT     Specify port number (default: 9551)
    --help          Show this help message
"""

import os
import sys
import subprocess
import argparse
import time
import signal
from pathlib import Path
from datetime import datetime

# Ensure Django settings are discoverable for tooling/linting
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')

# Constants
MANAGE_PY = 'manage.py'
DEFAULT_DEV_PORT = 9551
DEFAULT_FRONTEND_PORT = 5173
PYTHON_MIN_VERSION = (3, 11)
HEALTH_CHECK_TIMEOUT = 30
MIGRATION_TIMEOUT = 120
DB_CHECK_TIMEOUT = 30


class GaaraERPStarter:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.frontend_dir = self.base_dir / 'gaara_erp' / 'main-frontend'
        self.processes = []

    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 GAARA ERP SYSTEM 🚀                    ║
║                                                              ║
║              نظام جارا لتخطيط موارد المؤسسات                ║
║                                                              ║
║                    الإصدار 1.0 - 2024                       ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def check_requirements(self):
        """Check if all requirements are met"""
        print("🔍 فحص المتطلبات...")

        # Check Python version
        if sys.version_info < PYTHON_MIN_VERSION:
            print(
                f"❌ خطأ: يتطلب Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} أو أحدث")
            return False

        # Check if virtual environment exists
        venv_path = self.base_dir / '.venv'
        if not venv_path.exists():
            print("❌ خطأ: البيئة الافتراضية غير موجودة")
            print("   قم بتشغيل: python -m venv .venv")
            return False

        # Check if gaara_erp directory exists
        if not self.gaara_dir.exists():
            print("❌ خطأ: مجلد gaara_erp غير موجود")
            return False

        print("✅ جميع المتطلبات متوفرة")
        return True

    def activate_venv(self):
        """Activate virtual environment"""
        if os.name == 'nt':  # Windows
            activate_script = self.base_dir / '.venv' / 'Scripts' / 'activate.bat'
            python_exe = self.base_dir / '.venv' / 'Scripts' / 'python.exe'
        else:  # Linux/macOS
            activate_script = self.base_dir / '.venv' / 'bin' / 'activate'
            python_exe = self.base_dir / '.venv' / 'bin' / 'python'

        if not python_exe.exists():
            print("❌ خطأ: لم يتم العثور على Python في البيئة الافتراضية")
            return False

        # Set environment to use virtual environment Python
        os.environ['VIRTUAL_ENV'] = str(self.base_dir / '.venv')
        os.environ['PATH'] = str(self.base_dir / '.venv' / (
            'Scripts' if os.name == 'nt' else 'bin')) + os.pathsep + os.environ['PATH']

        print("✅ تم تفعيل البيئة الافتراضية")
        return True

    def check_database(self):
        """Check database connection and run migrations if needed"""
        print("🗄️  فحص قاعدة البيانات...")

        os.chdir(self.gaara_dir)

        try:
            # Check database connection
            result = subprocess.run([
                sys.executable, MANAGE_PY, 'check', '--database', 'default'
            ], capture_output=True, text=True, timeout=DB_CHECK_TIMEOUT)

            if result.returncode != 0:
                print("⚠️  تحذير: مشكلة في قاعدة البيانات")
                print("🔧 تطبيق الترحيلات...")

                # Run migrations
                migrate_result = subprocess.run([
                    sys.executable, MANAGE_PY, 'migrate'
                ], capture_output=True, text=True, timeout=MIGRATION_TIMEOUT)

                if migrate_result.returncode != 0:
                    print("❌ خطأ في تطبيق الترحيلات:")
                    print(migrate_result.stderr)
                    return False

            print("✅ قاعدة البيانات جاهزة")
            return True

        except subprocess.TimeoutExpired:
            print("❌ انتهت مهلة فحص قاعدة البيانات")
            return False
        except Exception as e:
            print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
            return False

    def create_superuser_if_needed(self):
        """Create superuser if none exists"""
        print("👤 فحص المستخدم الإداري...")

        try:
            # Check if superuser exists
            check_result = subprocess.run([
                sys.executable, MANAGE_PY, 'shell', '-c',
                'from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())'
            ], capture_output=True, text=True, timeout=HEALTH_CHECK_TIMEOUT)

            if 'True' not in check_result.stdout:
                print("⚠️  لا يوجد مستخدم إداري")
                print("👤 إنشاء مستخدم إداري افتراضي...")

                # Create default superuser
                create_result = subprocess.run([
                    sys.executable, MANAGE_PY, 'shell', '-c',
                    '''
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser("admin", "admin@gaara-erp.com", "admin123")
    print("تم إنشاء مستخدم إداري: admin / admin123")
                    '''
                ], capture_output=True, text=True, timeout=30)

                if create_result.returncode == 0:
                    print("✅ تم إنشاء المستخدم الإداري بنجاح")
                    print("📝 اسم المستخدم: admin")
                    print("🔑 كلمة المرور: admin123")
                    print("⚠️  يُنصح بتغيير كلمة المرور بعد تسجيل الدخول")
                else:
                    print("⚠️  تحذير: فشل في إنشاء المستخدم الإداري")
            else:
                print("✅ المستخدم الإداري موجود")

        except Exception as e:
            print(f"⚠️  تحذير: خطأ في فحص المستخدم الإداري: {e}")

    def check_system_health(self):
        """Perform comprehensive system health check"""
        print("🔍 فحص صحة النظام الشامل...")

        health_score = 0
        total_checks = 5

        try:
            # Check 1: Django system check
            result = subprocess.run([
                sys.executable, MANAGE_PY, 'check'
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                print("   ✅ فحص نظام Django: ناجح")
                health_score += 1
            else:
                print("   ❌ فحص نظام Django: فشل")

            # Check 2: Database connectivity
            db_result = subprocess.run([
                sys.executable, MANAGE_PY, 'shell', '-c',
                'from django.db import connection; connection.ensure_connection(); print("DB_OK")'
            ], capture_output=True, text=True, timeout=HEALTH_CHECK_TIMEOUT)

            if 'DB_OK' in db_result.stdout:
                print("   ✅ اتصال قاعدة البيانات: ناجح")
                health_score += 1
            else:
                print("   ❌ اتصال قاعدة البيانات: فشل")

            # Check 3: Static files
            static_path = self.gaara_dir / 'staticfiles'
            if static_path.exists() and any(static_path.iterdir()):
                print("   ✅ الملفات الثابتة: موجودة")
                health_score += 1
            else:
                print("   ⚠️  الملفات الثابتة: غير موجودة")

            # Check 4: Media directory
            media_path = self.gaara_dir / 'media'
            media_path.mkdir(exist_ok=True)
            print("   ✅ مجلد الوسائط: جاهز")
            health_score += 1

            # Check 5: Logs directory
            logs_path = self.gaara_dir / 'logs'
            logs_path.mkdir(exist_ok=True)
            print("   ✅ مجلد السجلات: جاهز")
            health_score += 1

            health_percentage = (health_score / total_checks) * 100
            print(
                f"📊 نتيجة فحص الصحة: {health_score}/{total_checks} ({health_percentage:.1f}%)")

            if health_percentage >= 80:
                print("✅ النظام في حالة صحية جيدة")
                return True
            else:
                print("⚠️  النظام يحتاج إلى انتباه")
                return False

        except Exception as e:
            print(f"❌ خطأ في فحص صحة النظام: {e}")
            return False

    def collect_static(self, production=False):
        """Collect static files for production"""
        if production:
            print("📁 جمع الملفات الثابتة...")

            try:
                result = subprocess.run([
                    sys.executable, MANAGE_PY, 'collectstatic', '--noinput'
                ], capture_output=True, text=True, timeout=60)

                if result.returncode == 0:
                    print("✅ تم جمع الملفات الثابتة")
                else:
                    print("⚠️  تحذير: مشكلة في جمع الملفات الثابتة")

            except Exception as e:
                print(f"⚠️  تحذير: خطأ في جمع الملفات الثابتة: {e}")

    def start_backend(self, production=False, port=9551):
        """Start Django backend server"""
        print(f"🚀 بدء تشغيل الخادم الخلفي على المنفذ {port}...")

        os.chdir(self.gaara_dir)

        if production:
            # Use production settings
            os.environ['DJANGO_SETTINGS_MODULE'] = 'gaara_erp.production_settings'
            cmd = [sys.executable, MANAGE_PY, 'runserver',
                   f'0.0.0.0:{port}', '--settings=gaara_erp.production_settings']
        else:
            # Use development settings
            cmd = [sys.executable, MANAGE_PY, 'runserver', f'0.0.0.0:{port}']

        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.processes.append(('backend', process))

            # Wait a moment to check if server started successfully
            time.sleep(3)
            if process.poll() is None:
                print("✅ تم بدء تشغيل الخادم الخلفي بنجاح")
                print(f"🌐 الخادم متاح على: http://localhost:{port}")
                return True
            else:
                print("❌ فشل في بدء تشغيل الخادم الخلفي")
                return False

        except Exception as e:
            print(f"❌ خطأ في بدء تشغيل الخادم الخلفي: {e}")
            return False

    def start_frontend(self):
        """Start React frontend development server"""
        if not self.frontend_dir.exists():
            print("⚠️  مجلد الواجهة الأمامية غير موجود، تخطي...")
            return True

        print("🎨 بدء تشغيل الواجهة الأمامية...")

        os.chdir(self.frontend_dir)

        # Check if node_modules exists
        if not (self.frontend_dir / 'node_modules').exists():
            print("📦 تثبيت تبعيات الواجهة الأمامية...")
            try:
                subprocess.run(['npm', 'install'], check=True, timeout=300)
            except subprocess.CalledProcessError:
                print("⚠️  فشل في تثبيت التبعيات، جاري المحاولة مع yarn...")
                try:
                    subprocess.run(['yarn', 'install'],
                                   check=True, timeout=300)
                except subprocess.CalledProcessError:
                    print("❌ فشل في تثبيت تبعيات الواجهة الأمامية")
                    return False

        try:
            # Try npm first, then yarn
            try:
                process = subprocess.Popen(
                    ['npm', 'run', 'dev'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            except FileNotFoundError:
                process = subprocess.Popen(
                    ['yarn', 'dev'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            self.processes.append(('frontend', process))

            # Wait a moment to check if server started
            time.sleep(5)
            if process.poll() is None:
                print("✅ تم بدء تشغيل الواجهة الأمامية بنجاح")
                print("🌐 الواجهة متاحة على: http://localhost:5173")
                return True
            else:
                print("❌ فشل في بدء تشغيل الواجهة الأمامية")
                return False

        except Exception as e:
            print(f"❌ خطأ في بدء تشغيل الواجهة الأمامية: {e}")
            return False

    def monitor_processes(self):
        """Monitor running processes"""
        print("\n🔍 مراقبة العمليات الجارية...")
        print("اضغط Ctrl+C للإيقاف")
        print("-" * 50)

        try:
            while True:
                all_running = True
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"⚠️  العملية {name} توقفت")
                        all_running = False

                if not all_running:
                    print("❌ بعض العمليات توقفت، إيقاف النظام...")
                    break

                time.sleep(5)

        except KeyboardInterrupt:
            print("\n🛑 تم طلب إيقاف النظام...")

        self.stop_all_processes()

    def stop_all_processes(self):
        """Stop all running processes"""
        print("🛑 إيقاف جميع العمليات...")

        for name, process in self.processes:
            if process.poll() is None:
                print(f"⏹️  إيقاف {name}...")
                process.terminate()

                # Wait for graceful shutdown
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print(f"⚠️  إجبار إيقاف {name}...")
                    process.kill()

        print("✅ تم إيقاف جميع العمليات")

    def setup_environment_files(self):
        """Setup environment files if they don't exist"""
        print("📁 إعداد ملفات البيئة...")

        env_file = self.base_dir / '.env'
        if not env_file.exists():
            print("⚠️  ملف .env غير موجود، إنشاء ملف افتراضي...")

            env_content = """# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Language and Timezone
LANGUAGE_CODE=ar
TIME_ZONE=Asia/Riyadh

# Company Settings
COMPANY_NAME=شركة جارا للأنظمة
SUPPORT_EMAIL=support@gaara-erp.com

# AI Features (Optional)
AI_FEATURES_ENABLED=True
OPENAI_API_KEY=

# Email Settings (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
"""

            try:
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(env_content)
                print("✅ تم إنشاء ملف .env افتراضي")
            except Exception as e:
                print(f"⚠️  تحذير: فشل في إنشاء ملف .env: {e}")
        else:
            print("✅ ملف .env موجود")

    def show_system_info(self, production=False, port=9551):
        """Display system information and access URLs"""
        print("\n" + "="*60)
        print("🎉 تم بدء تشغيل نظام Gaara ERP بنجاح!")
        print("="*60)

        print("\n🌐 روابط الوصول:")
        if not production:
            print("   📱 الواجهة الأمامية: http://localhost:5173")
        print(f"   🔧 الخادم الخلفي: http://localhost:{port}")
        print(f"   👨‍💼 لوحة الإدارة: http://localhost:{port}/admin")
        print(f"   🔌 API: http://localhost:{port}/api")

        print("\n👤 معلومات تسجيل الدخول الافتراضية:")
        print("   📝 اسم المستخدم: admin")
        print("   🔑 كلمة المرور: admin123")
        print("   ⚠️  يُنصح بتغيير كلمة المرور فور تسجيل الدخول")

        print("\n📚 الأدلة المتاحة:")
        print("   📖 دليل المستخدم: USER_GUIDE.md")
        print("   🚀 دليل النشر: DEPLOYMENT_GUIDE.md")

        print("\n🔧 أوامر مفيدة:")
        print("   ⏹️  إيقاف النظام: Ctrl+C")
        print("   🔄 إعادة التشغيل: أعد تشغيل هذا السكريبت")

        print("\n" + "="*60)

    def run(self, production=False, port=9551):
        """Main run method"""
        self.print_banner()

        if not self.check_requirements():
            return False

        if not self.activate_venv():
            return False

        self.setup_environment_files()

        if not self.check_database():
            return False

        self.create_superuser_if_needed()

        if not self.check_system_health():
            print("⚠️  تحذير: النظام ليس في حالة مثلى، لكن سيتم المتابعة...")

        self.collect_static(production)

        if not self.start_backend(production, port):
            return False

        if not production:  # Only start frontend in development
            self.start_frontend()

        self.show_system_info(production, port)
        self.monitor_processes()
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Gaara ERP System Startup Script')
    parser.add_argument('--production', action='store_true',
                        help='Start in production mode')
    parser.add_argument('--port', type=int, default=9551,
                        help='Port number for backend server')

    args = parser.parse_args()

    starter = GaaraERPStarter()

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 تم طلب إيقاف النظام...")
        starter.stop_all_processes()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    success = starter.run(production=args.production, port=args.port)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
