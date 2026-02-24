"""
#!/usr/bin/env python3

نص تشغيل الخادم الخلفي المُحسن
يقوم بتشغيل خادم Flask مع جميع الإعدادات المطلوبة
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def check_requirements():
    """فحص المتطلبات المطلوبة"""
    try:
        import flask
        import flask_cors

        print("✅ جميع المتطلبات متوفرة")
        return True
    except ImportError as e:
        print(f"❌ مكتبة مفقودة: {e}")
        print("💡 لتثبيت المتطلبات:")
        print("   pip install -r requirements.txt")
        return False


def check_port(port=8000):
    """فحص إذا كان المنفذ متاح"""
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
        return True
    except OSError:
        return False


def start_server():
    """تشغيل الخادم"""
    print("🔍 فحص المتطلبات...")
    if not check_requirements():
        return False

    print("🔍 فحص المنفذ 8000...")
    if not check_port(8000):
        print("⚠️ المنفذ 8000 مستخدم بالفعل")
        print("💡 قد يكون الخادم يعمل بالفعل أو استخدم منفذ آخر")

    print("\n🚀 بدء تشغيل خادم نظام إدارة المخزون...")
    print("📍 العنوان: http://172.16.16.27:8000")
    print("🔗 الواجهة الأمامية: http://localhost:5502")
    print("👤 اسم المستخدم: admin")
    print("🔑 كلمة المرور: admin123")
    print("📚 APIs متاحة:")
    print("   - /api/products")
    print("   - /api/customers")
    print("   - /api/suppliers")
    print("   - /api/categories")
    print("   - /api/warehouses")
    print("   - /api/stock-movements")
    print("   - /api/sales-invoices")
    print("   - /accounting/*")
    print("   - /reports/*")
    print("-" * 60)

    try:
        # تشغيل simple_auth.py
        print("▶️ تشغيل الخادم...")
        subprocess.run([sys.executable, "simple_auth.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الخادم بواسطة المستخدم")
    except FileNotFoundError:
        print("❌ ملف simple_auth.py غير موجود")
        print("💡 تأكد من وجود الملف في نفس المجلد")
        return False
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return False

    return True


if __name__ == "__main__":
    start_server()
