#!/usr/bin/env python3
"""
مشغل الخادم الخلفي البسيط
"""

import os
import sys
import subprocess
from pathlib import Path


def start_server():
    """تشغيل الخادم الخلفي"""
    print("🚀 === تشغيل الخادم الخلفي ===")

    # التأكد من المجلد الصحيح
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    print(f"📁 المجلد الحالي: {backend_dir}")

    # قائمة الخوادم المتاحة
    servers = [
        ("app_with_database.py", "الخادم الرئيسي", 8002),
        ("enhanced_server.py", "الخادم المحسن", 8000),
        ("simple_auth.py", "خادم المصادقة", 8001)
    ]

    print("\n📋 الخوادم المتاحة:")
    for i, (file, name, port) in enumerate(servers, 1):
        print(f"  {i}. {name} ({file}) - المنفذ {port}")

    # اختيار الخادم الافتراضي
    server_choice = 0  # الخادم الرئيسي
    server_file, server_name, server_port = servers[server_choice]

    print(f"\n🔧 تشغيل {server_name}...")
    print(f"📍 المنفذ: {server_port}")
    print(f"🔗 العنوان: http://localhost:{server_port}")
    print("-" * 50)

    try:
        # تشغيل الخادم
        subprocess.run([sys.executable, server_file], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الخادم بواسطة المستخدم")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ خطأ في تشغيل الخادم: {e}")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")


if __name__ == "__main__":
    start_server()
