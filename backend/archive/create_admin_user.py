#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إنشاء مستخدم إداري افتراضي
Create Default Admin User
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import db
from src.models.user import User
from werkzeug.security import generate_password_hash
from flask import Flask

def create_admin_user():
    """إنشاء مستخدم إداري افتراضي"""
    
    # إعداد التطبيق
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    db.init_app(app)
    
    with app.app_context():
        # التحقق من وجود مستخدم إداري
        admin_user = User.query.filter_by(role='admin').first()
        
        if admin_user:
            print(f"✅ المستخدم الإداري موجود بالفعل: {admin_user.username}")
            return
        
        # إنشاء مستخدم إداري جديد
        admin = User(
            username='admin',
            email='admin@store.com',
            full_name='مدير النظام',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        
        # إضافة جميع الصلاحيات
        admin.set_permissions([
            'read_all', 'write_all', 'delete_all', 'admin_panel',
            'user_management', 'system_settings', 'reports_access'
        ])
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ تم إنشاء المستخدم الإداري بنجاح!")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: admin123")
        print("   ⚠️  يرجى تغيير كلمة المرور بعد أول تسجيل دخول")

if __name__ == "__main__":
    create_admin_user()
