#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعادة إنشاء قاعدة البيانات بالكامل
Recreate Database Script
"""

import os
import sys
import shutil
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def backup_old_database():
    """نسخ احتياطي لقاعدة البيانات القديمة"""
    db_paths = [
        'instance/inventory.db',
        'instance/inventory_encrypted.db',
        'inventory_system.db'
    ]
    
    backup_dir = f'database_archive/backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    os.makedirs(backup_dir, exist_ok=True)
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            backup_path = os.path.join(backup_dir, os.path.basename(db_path))
            shutil.copy2(db_path, backup_path)
            print(f"✅ تم نسخ {db_path} إلى {backup_path}")
    
    return backup_dir

def delete_old_databases():
    """حذف قواعد البيانات القديمة"""
    db_paths = [
        'instance/inventory.db',
        'instance/inventory.db-shm',
        'instance/inventory.db-wal',
        'instance/inventory_encrypted.db',
        'instance/inventory_encrypted.db-shm',
        'instance/inventory_encrypted.db-wal',
        'inventory_system.db',
        'inventory_system.db-shm',
        'inventory_system.db-wal'
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✅ تم حذف {db_path}")

def create_new_database():
    """إنشاء قاعدة بيانات جديدة"""
    try:
        from app import app
        from database import create_tables, create_default_data

        with app.app_context():
            # إنشاء الجداول
            print("📊 إنشاء الجداول...")
            if create_tables(app):
                print("✅ تم إنشاء الجداول بنجاح")
            else:
                print("❌ فشل في إنشاء الجداول")
                return False

            # إنشاء البيانات الأساسية
            print("👤 إنشاء البيانات الأساسية...")
            if create_default_data():
                print("✅ تم إنشاء البيانات الأساسية بنجاح")
            else:
                print("❌ فشل في إنشاء البيانات الأساسية")
                return False

            return True

    except Exception as e:
        print("❌ خطأ في إنشاء قاعدة البيانات: {}".format(e))
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🔄 إعادة إنشاء قاعدة البيانات")
    print("=" * 60)
    
    # 1. نسخ احتياطي
    print("\n📦 الخطوة 1: نسخ احتياطي...")
    backup_dir = backup_old_database()
    print(f"✅ تم حفظ النسخة الاحتياطية في: {backup_dir}")
    
    # 2. حذف القديم
    print("\n🗑️  الخطوة 2: حذف قواعد البيانات القديمة...")
    delete_old_databases()
    print("✅ تم حذف قواعد البيانات القديمة")
    
    # 3. إنشاء جديد
    print("\n🆕 الخطوة 3: إنشاء قاعدة بيانات جديدة...")
    success = create_new_database()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ تم إعادة إنشاء قاعدة البيانات بنجاح!")
        print("=" * 60)
        print("\n📝 بيانات الدخول:")
        print("   Username: admin")
        print("   Password: u-fZEk2jsOQN3bwvFrj93A")
        print("\n🚀 الخطوات التالية:")
        print("   1. شغّل Backend:")
        print("      python app.py")
        print("\n   2. شغّل Frontend (Terminal جديد):")
        print("      cd ../frontend")
        print("      npm run dev")
        print("\n   3. افتح المتصفح:")
        print("      http://localhost:5502")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ فشل في إعادة إنشاء قاعدة البيانات!")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())

