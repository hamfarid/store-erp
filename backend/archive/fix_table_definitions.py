#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 إصلاح مشكلة تعريف الجداول المكررة
Fix Table Definitions Script

يقوم بإصلاح مشكلة "Table 'users' is already defined" في SQLAlchemy:
- إضافة extend_existing=True للنماذج
- إصلاح تعارض تعريفات الجداول
- تحديث النماذج لتجنب التعارض
"""

import os
import re
from pathlib import Path

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def fix_model_file(file_path):
    """إصلاح ملف نموذج واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن تعريفات الجداول
        if 'class ' in content and 'db.Model' in content:
            # إضافة extend_existing=True للجداول
            if '__table_args__' not in content:
                # البحث عن نهاية تعريف الكلاس
                class_pattern = r'(class\s+\w+\([^)]*db\.Model[^)]*\):\s*)'
                match = re.search(class_pattern, content)
                
                if match:
                    # إضافة __table_args__ بعد تعريف الكلاس
                    insert_pos = match.end()
                    table_args = '\n    __table_args__ = {"extend_existing": True}\n'
                    content = content[:insert_pos] + table_args + content[insert_pos:]
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    return True
        
        return False
        
    except Exception as e:
        print_error(f"خطأ في إصلاح {file_path}: {e}")
        return False

def fix_all_models():
    """إصلاح جميع ملفات النماذج"""
    print_step("إصلاح ملفات النماذج...")
    
    models_dir = Path("backend/src/models")
    if not models_dir.exists():
        print_error("مجلد النماذج غير موجود")
        return False
    
    fixed_count = 0
    
    for model_file in models_dir.glob("*.py"):
        if model_file.name == "__init__.py":
            continue
            
        print_step(f"إصلاح {model_file.name}...")
        if fix_model_file(model_file):
            fixed_count += 1
            print_success(f"تم إصلاح {model_file.name}")
    
    print_success(f"تم إصلاح {fixed_count} ملف نموذج")
    return True

def fix_init_file():
    """إصلاح ملف __init__.py في النماذج"""
    print_step("إصلاح ملف __init__.py...")
    
    init_file = Path("backend/src/models/__init__.py")
    if not init_file.exists():
        print_error("ملف __init__.py غير موجود")
        return False
    
    try:
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # إعادة ترتيب الاستيرادات لتجنب التعارض
        new_content = '''# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات
Database Models
"""

from flask_sqlalchemy import SQLAlchemy

# إنشاء كائن قاعدة البيانات
db = SQLAlchemy()

# استيراد النماذج (بعد إنشاء db)
def init_models():
    """تهيئة النماذج"""
    try:
        from .user import User
        from .product import Product
        from .category import Category
        from .warehouse import Warehouse
        from .inventory import Inventory
        from .customer import Customer
        from .supplier import Supplier
        from .sale import Sale
        from .purchase import Purchase
        
        return True
    except ImportError as e:
        print(f"تحذير: لا يمكن استيراد بعض النماذج: {e}")
        return False

# تصدير النماذج المتاحة
__all__ = ['db', 'init_models']
'''
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print_success("تم إصلاح ملف __init__.py")
        return True
        
    except Exception as e:
        print_error(f"خطأ في إصلاح __init__.py: {e}")
        return False

def update_app_py():
    """تحديث app.py لاستخدام النماذج المحدثة"""
    print_step("تحديث app.py...")
    
    app_file = Path("backend/app.py")
    if not app_file.exists():
        print_error("ملف app.py غير موجود")
        return False
    
    try:
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن استيراد النماذج وتحديثه
        if 'from src.models import db' in content:
            # إضافة تهيئة النماذج
            if 'init_models()' not in content:
                # البحث عن مكان إضافة تهيئة النماذج
                db_init_pattern = r'(db\.init_app\(app\))'
                match = re.search(db_init_pattern, content)
                
                if match:
                    insert_pos = match.end()
                    init_code = '\n        \n        # تهيئة النماذج\n        from src.models import init_models\n        init_models()\n'
                    content = content[:insert_pos] + init_code + content[insert_pos:]
                    
                    with open(app_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print_success("تم تحديث app.py")
                    return True
        
        return False
        
    except Exception as e:
        print_error(f"خطأ في تحديث app.py: {e}")
        return False

def main():
    print("🔧 بدء إصلاح مشكلة تعريف الجداول المكررة...")
    print("=" * 60)
    
    success = True
    
    # إصلاح ملف __init__.py أولاً
    if not fix_init_file():
        success = False
    
    # إصلاح ملفات النماذج
    if not fix_all_models():
        success = False
    
    # تحديث app.py
    if not update_app_py():
        print_step("تخطي تحديث app.py (قد يكون محدثاً بالفعل)")
    
    print("=" * 60)
    if success:
        print_success("تم إصلاح مشكلة تعريف الجداول بنجاح!")
        print("📋 يُنصح بإعادة تشغيل الخادم الخلفي")
    else:
        print_error("حدثت بعض المشاكل أثناء الإصلاح")
    
    return success

if __name__ == "__main__":
    main()
