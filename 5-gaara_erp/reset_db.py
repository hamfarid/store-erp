#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لإعادة تعيين قاعدة البيانات
Reset database script
"""

import os
from src.database import db
from src.models.user_unified import User, Role, create_default_roles
from werkzeug.security import generate_password_hash

# حذف قاعدة البيانات القديمة
if os.path.exists('inventory.db'):
    os.remove('inventory.db')
    print("✅ تم حذف قاعدة البيانات القديمة")

# إنشاء الجداول
db.create_all()
print("✅ تم إنشاء الجداول")

# إنشاء الأدوار الافتراضية
try:
    create_default_roles()
    print("✅ تم إنشاء الأدوار الافتراضية")
except Exception as e:
    print(f"⚠️ تحذير: {e}")

# إنشاء مستخدم admin
admin = User()
admin.username = 'admin'
admin.email = 'admin@example.com'
admin.full_name = 'Administrator'
admin.password_hash = generate_password_hash('admin123')
admin.role = 'admin'
admin.is_active = True
admin.is_superuser = True

db.session.add(admin)
db.session.commit()

print("✅ تم إنشاء مستخدم admin بنجاح!")
print("   Username: admin")
print("   Password: admin123")
print("   Email: admin@example.com")
print("\n🎉 قاعدة البيانات جاهزة!")

