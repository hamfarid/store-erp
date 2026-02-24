#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 إصلاح نقاط النهاية المفقودة
Fix Missing Endpoints Script

يقوم بإنشاء وإصلاح نقاط النهاية المفقودة:
- /api/categories
- /api/warehouses  
- /api/users
- تحديث app.py لتسجيل المخططات الجديدة
"""

import os
from pathlib import Path

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def create_categories_route():
    """إنشاء مسار الفئات"""
    print_step("إنشاء مسار الفئات...")
    
    categories_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/categories.py
مسارات إدارة الفئات
Categories Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.category import Category
from src.auth import token_required
import logging

logger = logging.getLogger(__name__)

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/api/categories', methods=['GET'])
@token_required
def get_categories():
    """الحصول على قائمة الفئات"""
    try:
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'data': [category.to_dict() for category in categories],
            'total': len(categories)
        })
    except Exception as e:
        logger.error(f"خطأ في الحصول على الفئات: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على الفئات'
        }), 500

@categories_bp.route('/api/categories', methods=['POST'])
@token_required
def create_category():
    """إنشاء فئة جديدة"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({
                'success': False,
                'error': 'اسم الفئة مطلوب'
            }), 400
        
        category = Category(
            name=data['name'],
            description=data.get('description', ''),
            parent_id=data.get('parent_id')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': category.to_dict(),
            'message': 'تم إنشاء الفئة بنجاح'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء الفئة: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في إنشاء الفئة'
        }), 500

@categories_bp.route('/api/categories/<int:category_id>', methods=['GET'])
@token_required
def get_category(category_id):
    """الحصول على فئة محددة"""
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify({
            'success': True,
            'data': category.to_dict()
        })
    except Exception as e:
        logger.error(f"خطأ في الحصول على الفئة: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على الفئة'
        }), 500

@categories_bp.route('/api/categories/<int:category_id>', methods=['PUT'])
@token_required
def update_category(category_id):
    """تحديث فئة"""
    try:
        category = Category.query.get_or_404(category_id)
        data = request.get_json()
        
        if data.get('name'):
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'parent_id' in data:
            category.parent_id = data['parent_id']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': category.to_dict(),
            'message': 'تم تحديث الفئة بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث الفئة: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في تحديث الفئة'
        }), 500

@categories_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
@token_required
def delete_category(category_id):
    """حذف فئة"""
    try:
        category = Category.query.get_or_404(category_id)
        
        # التحقق من وجود منتجات في هذه الفئة
        if category.products:
            return jsonify({
                'success': False,
                'error': 'لا يمكن حذف فئة تحتوي على منتجات'
            }), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حذف الفئة بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف الفئة: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في حذف الفئة'
        }), 500
'''
    
    categories_path = Path("backend/src/routes/categories.py")
    with open(categories_path, 'w', encoding='utf-8') as f:
        f.write(categories_code)
    
    print_success("تم إنشاء مسار الفئات")

def create_warehouses_route():
    """إنشاء مسار المستودعات"""
    print_step("إنشاء مسار المستودعات...")
    
    warehouses_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/warehouses.py
مسارات إدارة المستودعات
Warehouses Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.warehouse import Warehouse
from src.auth import token_required
import logging

logger = logging.getLogger(__name__)

warehouses_bp = Blueprint('warehouses', __name__)

@warehouses_bp.route('/api/warehouses', methods=['GET'])
@token_required
def get_warehouses():
    """الحصول على قائمة المستودعات"""
    try:
        warehouses = Warehouse.query.all()
        return jsonify({
            'success': True,
            'data': [warehouse.to_dict() for warehouse in warehouses],
            'total': len(warehouses)
        })
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستودعات: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على المستودعات'
        }), 500

@warehouses_bp.route('/api/warehouses', methods=['POST'])
@token_required
def create_warehouse():
    """إنشاء مستودع جديد"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({
                'success': False,
                'error': 'اسم المستودع مطلوب'
            }), 400
        
        warehouse = Warehouse(
            name=data['name'],
            location=data.get('location', ''),
            description=data.get('description', ''),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(warehouse)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': warehouse.to_dict(),
            'message': 'تم إنشاء المستودع بنجاح'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء المستودع: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في إنشاء المستودع'
        }), 500

@warehouses_bp.route('/api/warehouses/<int:warehouse_id>', methods=['GET'])
@token_required
def get_warehouse(warehouse_id):
    """الحصول على مستودع محدد"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        return jsonify({
            'success': True,
            'data': warehouse.to_dict()
        })
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستودع: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على المستودع'
        }), 500

@warehouses_bp.route('/api/warehouses/<int:warehouse_id>', methods=['PUT'])
@token_required
def update_warehouse(warehouse_id):
    """تحديث مستودع"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        data = request.get_json()
        
        if data.get('name'):
            warehouse.name = data['name']
        if 'location' in data:
            warehouse.location = data['location']
        if 'description' in data:
            warehouse.description = data['description']
        if 'is_active' in data:
            warehouse.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': warehouse.to_dict(),
            'message': 'تم تحديث المستودع بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث المستودع: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في تحديث المستودع'
        }), 500

@warehouses_bp.route('/api/warehouses/<int:warehouse_id>', methods=['DELETE'])
@token_required
def delete_warehouse(warehouse_id):
    """حذف مستودع"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        
        # التحقق من وجود مخزون في هذا المستودع
        if warehouse.inventory_items:
            return jsonify({
                'success': False,
                'error': 'لا يمكن حذف مستودع يحتوي على مخزون'
            }), 400
        
        db.session.delete(warehouse)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حذف المستودع بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف المستودع: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في حذف المستودع'
        }), 500
'''
    
    warehouses_path = Path("backend/src/routes/warehouses.py")
    with open(warehouses_path, 'w', encoding='utf-8') as f:
        f.write(warehouses_code)
    
    print_success("تم إنشاء مسار المستودعات")

def create_users_route():
    """إنشاء مسار المستخدمين"""
    print_step("إنشاء مسار المستخدمين...")
    
    users_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/users.py
مسارات إدارة المستخدمين
Users Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.user import User
from src.auth import token_required, admin_required
from werkzeug.security import generate_password_hash
import logging

logger = logging.getLogger(__name__)

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['GET'])
@token_required
@admin_required
def get_users():
    """الحصول على قائمة المستخدمين"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users],
            'total': len(users)
        })
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدمين: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على المستخدمين'
        }), 500

@users_bp.route('/api/users', methods=['POST'])
@token_required
@admin_required
def create_user():
    """إنشاء مستخدم جديد"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'اسم المستخدم وكلمة المرور مطلوبان'
            }), 400
        
        # التحقق من عدم وجود المستخدم
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'error': 'اسم المستخدم موجود بالفعل'
            }), 400
        
        user = User(
            username=data['username'],
            email=data.get('email', ''),
            full_name=data.get('full_name', ''),
            password_hash=generate_password_hash(data['password']),
            role=data.get('role', 'user'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': 'تم إنشاء المستخدم بنجاح'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء المستخدم: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في إنشاء المستخدم'
        }), 500

@users_bp.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """الحصول على مستخدم محدد"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدم: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في الحصول على المستخدم'
        }), 500

@users_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(user_id):
    """تحديث مستخدم"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if data.get('username'):
            user.username = data['username']
        if data.get('email'):
            user.email = data['email']
        if data.get('full_name'):
            user.full_name = data['full_name']
        if data.get('password'):
            user.password_hash = generate_password_hash(data['password'])
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': 'تم تحديث المستخدم بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث المستخدم: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في تحديث المستخدم'
        }), 500

@users_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_id):
    """حذف مستخدم"""
    try:
        user = User.query.get_or_404(user_id)
        
        # منع حذف المستخدم الحالي
        current_user = getattr(request, 'current_user', None)
        if current_user and current_user.id == user_id:
            return jsonify({
                'success': False,
                'error': 'لا يمكن حذف المستخدم الحالي'
            }), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حذف المستخدم بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف المستخدم: {e}")
        return jsonify({
            'success': False,
            'error': 'فشل في حذف المستخدم'
        }), 500
'''
    
    users_path = Path("backend/src/routes/users.py")
    with open(users_path, 'w', encoding='utf-8') as f:
        f.write(users_code)
    
    print_success("تم إنشاء مسار المستخدمين")

def create_missing_models():
    """إنشاء النماذج المفقودة"""
    print_step("إنشاء النماذج المفقودة...")
    
    # إنشاء نموذج الفئات
    category_model = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/models/category.py
نموذج الفئات
Category Model
"""

from src.database import db
from datetime import datetime

class Category(db.Model):
    """نموذج الفئات"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    parent = db.relationship('Category', remote_side=[id], backref='children')
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'products_count': len(self.products) if self.products else 0
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'
'''
    
    category_path = Path("backend/src/models/category.py")
    with open(category_path, 'w', encoding='utf-8') as f:
        f.write(category_model)
    
    # إنشاء نموذج المستودعات
    warehouse_model = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/models/warehouse.py
نموذج المستودعات
Warehouse Model
"""

from src.database import db
from datetime import datetime

class Warehouse(db.Model):
    """نموذج المستودعات"""
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    inventory_items = db.relationship('Inventory', backref='warehouse', lazy=True)
    
    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'inventory_count': len(self.inventory_items) if self.inventory_items else 0
        }
    
    def __repr__(self):
        return f'<Warehouse {self.name}>'
'''
    
    warehouse_path = Path("backend/src/models/warehouse.py")
    with open(warehouse_path, 'w', encoding='utf-8') as f:
        f.write(warehouse_model)
    
    print_success("تم إنشاء النماذج المفقودة")

def update_app_py():
    """تحديث app.py لتسجيل المخططات الجديدة"""
    print_step("تحديث app.py...")
    
    app_py_path = Path("backend/app.py")
    
    # قراءة المحتوى الحالي
    with open(app_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة المخططات الجديدة
    new_blueprints = """        ('routes.categories', 'categories_bp'),
        ('routes.warehouses', 'warehouses_bp'),
        ('routes.users', 'users_bp'),"""
    
    # البحث عن قائمة المخططات وإضافة الجديدة
    import re
    pattern = r"(blueprints_to_register = \[)(.*?)(\])"
    
    def replace_blueprints(match):
        start = match.group(1)
        existing = match.group(2)
        end = match.group(3)
        
        # إضافة المخططات الجديدة إذا لم تكن موجودة
        if 'categories_bp' not in existing:
            existing += f"\n{new_blueprints}"
        
        return f"{start}{existing}{end}"
    
    content = re.sub(pattern, replace_blueprints, content, flags=re.DOTALL)
    
    # كتابة المحتوى المحدث
    with open(app_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print_success("تم تحديث app.py")

def main():
    print("🔧 بدء إصلاح نقاط النهاية المفقودة...")
    print("=" * 50)
    
    # إنشاء النماذج المفقودة
    create_missing_models()
    
    # إنشاء المسارات المفقودة
    create_categories_route()
    create_warehouses_route()
    create_users_route()
    
    # تحديث app.py
    update_app_py()
    
    print("=" * 50)
    print_success("تم إصلاح نقاط النهاية المفقودة بنجاح!")
    print("📋 المسارات المضافة:")
    print("   - /api/categories")
    print("   - /api/warehouses")
    print("   - /api/users")
    print("📋 النماذج المضافة:")
    print("   - Category")
    print("   - Warehouse")

if __name__ == "__main__":
    main()
