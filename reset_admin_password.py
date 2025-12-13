#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لإعادة تعيين كلمة مرور المستخدم admin
Reset admin password script
"""

import sys
import os

from src.models.user_unified import User
from werkzeug.security import generate_password_hash

try:
    from src.database import db
except Exception:
    from database import db

try:
    from app import create_app
except Exception:
    from backend.app import create_app  # fallback when running from repo root

def reset_admin_password():
    """إعادة تعيين كلمة مرور admin"""
    app = create_app()
    
    with app.app_context():
        # البحث عن المستخدم admin
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ المستخدم admin غير موجود!")
            print("Creating admin user...")
            
            # إنشاء مستخدم admin جديد
            admin = User()
            admin.username = 'admin'
            admin.email = 'admin@example.com'
            admin.full_name = 'System Administrator'
            admin.role_id = 1
            admin.is_active = True
            db.session.add(admin)
        
        # تعيين كلمة المرور
        new_password = 'u-fZEk2jsOQN3bwvFrj93A'
        admin.password_hash = generate_password_hash(new_password)
        
        try:
            db.session.commit()
            print("✅ تم إعادة تعيين كلمة مرور admin بنجاح!")
            print("Username: admin")
            print(f"Password: {new_password}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    reset_admin_password()

