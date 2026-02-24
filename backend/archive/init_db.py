#!/usr/bin/env python3
# type: ignore
"""
Script إعداد قاعدة البيانات المبسط
Simple Database Setup Script

Note: SQLAlchemy model attributes are dynamically generated,
so type checkers may not recognize them properly.
"""

import os
import sys
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# إضافة مسار src إلى Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# تحميل متغيرات البيئة
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# إنشاء التطبيق
app = Flask(__name__)

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

# إنشاء مجلد instance
instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
os.makedirs(instance_dir, exist_ok=True)

# إنشاء قاعدة البيانات
db = SQLAlchemy(app)

# تعريف النماذج الأساسية


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """تعيين كلمة المرور"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    price = db.Column(db.Float, default=0)
    cost = db.Column(db.Float, default=0)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(50), default='قطعة')
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def create_database():
    """إنشاء قاعدة البيانات والجداول"""
    print("🔧 إنشاء قاعدة البيانات...")

    try:
        with app.app_context():
            # إنشاء جميع الجداول
            db.create_all()
            print("✅ تم إنشاء قاعدة البيانات والجداول بنجاح")
            return True

    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        return False


def create_admin_user():
    """إنشاء المستخدم الرئيسي"""
    print("👤 إنشاء المستخدم الرئيسي...")

    try:
        with app.app_context():
            # التحقق من وجود المستخدم الرئيسي
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@inventory.com',
                    full_name='مدير النظام',
                    role='admin',
                    is_active=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ تم إنشاء المستخدم الرئيسي")
                print("   📧 البريد الإلكتروني: admin@inventory.com")
                print("   🔑 اسم المستخدم: admin")
                print("   🔒 كلمة المرور: admin123")
            else:
                print("⚠️  المستخدم الرئيسي موجود بالفعل")

            return True

    except Exception as e:
        print(f"❌ خطأ في إنشاء المستخدم الرئيسي: {e}")
        return False


def create_sample_data():
    """إنشاء بيانات تجريبية"""
    print("📊 إنشاء البيانات التجريبية...")

    try:
        with app.app_context():
            # إنشاء فئات تجريبية
            categories = [
                {'name': 'بذور', 'description': 'جميع أنواع البذور الزراعية'},
                {'name': 'أسمدة', 'description': 'الأسمدة الكيماوية والعضوية'},
                {'name': 'مبيدات', 'description': 'مبيدات الآفات والحشرات'},
                {'name': 'أدوات زراعية',
                    'description': 'الأدوات والمعدات الزراعية'}
            ]

            for cat_data in categories:
                existing = Category.query.filter_by(
                    name=cat_data['name']).first()
                if not existing:
                    category = Category(
                        name=cat_data['name'],
                        description=cat_data['description']
                    )
                    db.session.add(category)

            # إنشاء منتجات تجريبية
            seed_category = Category.query.filter_by(name='بذور').first()
            if seed_category:
                products = [
                    {'name': 'بذور طماطم',
                        'code': 'TOM001',
                        'price': 25.0,
                        'cost': 15.0,
                        'quantity': 100},
                    {'name': 'بذور خيار',
                        'code': 'CUC001',
                        'price': 20.0,
                        'cost': 12.0,
                        'quantity': 150},
                    {'name': 'بذور فلفل',
                        'code': 'PEP001',
                        'price': 30.0,
                        'cost': 18.0,
                        'quantity': 80}
                ]

                for prod_data in products:
                    existing = Product.query.filter_by(
                        code=prod_data['code']).first()
                    if not existing:
                        product = Product(
                            name=prod_data['name'],
                            code=prod_data['code'],
                            category_id=seed_category.id,
                            price=prod_data['price'],
                            cost=prod_data['cost'],
                            quantity=prod_data['quantity'],
                            unit='عبوة'
                        )
                        db.session.add(product)

            db.session.commit()
            print("✅ تم إنشاء البيانات التجريبية")
            return True

    except Exception as e:
        print(f"❌ خطأ في إنشاء البيانات التجريبية: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إعداد نظام إدارة المخزون")
    print("=" * 50)

    success_count = 0
    total_steps = 3

    # الخطوة 1: إنشاء قاعدة البيانات
    if create_database():
        success_count += 1

    # الخطوة 2: إنشاء المستخدم الرئيسي
    if create_admin_user():
        success_count += 1

    # الخطوة 3: إنشاء البيانات التجريبية
    if create_sample_data():
        success_count += 1

    print("=" * 50)
    print(f"📊 النتائج: {success_count}/{total_steps} خطوات مكتملة")

    if success_count == total_steps:
        print("🎉 تم إعداد النظام بنجاح!")
        print("\n📋 معلومات تسجيل الدخول:")
        print("   👤 اسم المستخدم: admin")
        print("   🔑 كلمة المرور: admin123")
        print("\n🚀 يمكنك الآن بدء تشغيل النظام")
        return True
    else:
        print("⚠️  تم إعداد النظام جزئياً")
        return False


if __name__ == '__main__':
    main()
