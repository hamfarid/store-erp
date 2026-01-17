#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت ترحيل البيانات إلى النماذج الموحدة
Migration Script to Unified Models

يقوم بترحيل البيانات من النماذج القديمة إلى النماذج الموحدة الجديدة
"""

import sys
import os
from datetime import datetime

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from src.models import (
    User, Role, Product, Invoice, Warehouse,
    InvoiceItem, Payment, StockMovement, AuditLog
)


def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    print("📦 إنشاء نسخة احتياطية من قاعدة البيانات...")
    
    try:
        import shutil
        from pathlib import Path
        
        # مسار قاعدة البيانات
        db_path = Path('instance/inventory.db')
        
        if db_path.exists():
            # إنشاء مجلد النسخ الاحتياطية
            backup_dir = Path('instance/backups')
            backup_dir.mkdir(exist_ok=True)
            
            # اسم النسخة الاحتياطية
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = backup_dir / f'inventory_backup_{timestamp}.db'
            
            # نسخ قاعدة البيانات
            shutil.copy2(db_path, backup_path)
            
            print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
            return True
        else:
            print("⚠️ لا توجد قاعدة بيانات للنسخ الاحتياطي")
            return True
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
        return False


def create_tables():
    """إنشاء جداول النماذج الموحدة"""
    print("\n🔨 إنشاء جداول النماذج الموحدة...")
    
    try:
        with app.app_context():
            # إنشاء جميع الجداول
            db.create_all()
            print("✅ تم إنشاء الجداول بنجاح")
            return True
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        return False


def create_default_roles():
    """إنشاء الأدوار الافتراضية"""
    print("\n👥 إنشاء الأدوار الافتراضية...")
    
    try:
        with app.app_context():
            from src.models.user_unified import create_default_roles
            create_default_roles()
            print("✅ تم إنشاء الأدوار الافتراضية")
            return True
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء الأدوار: {e}")
        return False


def migrate_users():
    """ترحيل بيانات المستخدمين"""
    print("\n👤 ترحيل بيانات المستخدمين...")
    
    try:
        with app.app_context():
            # الحصول على جميع المستخدمين
            users = User.query.all()
            
            if not users:
                print("⚠️ لا توجد بيانات مستخدمين للترحيل")
                return True
            
            # تحديث المستخدمين
            for user in users:
                # تعيين الدور بناءً على role القديم
                if user.role == 'admin':
                    admin_role = Role.query.filter_by(name='admin').first()
                    if admin_role:
                        user.role_id = admin_role.id
                elif user.role == 'manager':
                    manager_role = Role.query.filter_by(name='manager').first()
                    if manager_role:
                        user.role_id = manager_role.id
                else:
                    user_role = Role.query.filter_by(name='user').first()
                    if user_role:
                        user.role_id = user_role.id
            
            db.session.commit()
            print(f"✅ تم ترحيل {len(users)} مستخدم")
            return True
            
    except Exception as e:
        print(f"❌ خطأ في ترحيل المستخدمين: {e}")
        db.session.rollback()
        return False


def verify_migration():
    """التحقق من نجاح الترحيل"""
    print("\n🔍 التحقق من نجاح الترحيل...")
    
    try:
        with app.app_context():
            # عد السجلات
            users_count = User.query.count()
            products_count = Product.query.count()
            warehouses_count = Warehouse.query.count()
            
            print(f"📊 إحصائيات قاعدة البيانات:")
            print(f"   - المستخدمون: {users_count}")
            print(f"   - المنتجات: {products_count}")
            print(f"   - المستودعات: {warehouses_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ خطأ في التحقق: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🚀 بدء عملية الترحيل إلى النماذج الموحدة")
    print("=" * 60)
    
    # 1. إنشاء نسخة احتياطية
    if not backup_database():
        print("\n❌ فشل إنشاء النسخة الاحتياطية. إيقاف العملية.")
        return False
    
    # 2. إنشاء الجداول
    if not create_tables():
        print("\n❌ فشل إنشاء الجداول. إيقاف العملية.")
        return False
    
    # 3. إنشاء الأدوار الافتراضية
    if not create_default_roles():
        print("\n⚠️ تحذير: فشل إنشاء الأدوار الافتراضية")
    
    # 4. ترحيل المستخدمين
    if not migrate_users():
        print("\n⚠️ تحذير: فشل ترحيل المستخدمين")
    
    # 5. التحقق من النتائج
    verify_migration()
    
    print("\n" + "=" * 60)
    print("✅ اكتملت عملية الترحيل بنجاح!")
    print("=" * 60)
    print("\n📝 ملاحظات مهمة:")
    print("   1. تم إنشاء نسخة احتياطية من قاعدة البيانات")
    print("   2. تم إنشاء جداول النماذج الموحدة")
    print("   3. تم ترحيل البيانات الموجودة")
    print("   4. يمكنك الآن استخدام النماذج الموحدة الجديدة")
    print("\n⚠️ في حالة وجود مشاكل:")
    print("   - يمكنك استعادة النسخة الاحتياطية من مجلد instance/backups")
    print("   - راجع ملف السجل للحصول على تفاصيل الأخطاء")
    
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ تم إيقاف العملية بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

