#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 إصلاح نظام المصادقة والمستخدمين
Fix Authentication System Script

يقوم بإصلاح وتحسين نظام المصادقة:
- إنشاء مستخدم إداري افتراضي
- إصلاح مسارات المصادقة
- تحديث نظام الصلاحيات
- إضافة decorators للأمان
"""

import os
import sys
from pathlib import Path
from werkzeug.security import generate_password_hash

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def create_admin_decorators():
    """إنشاء decorators للصلاحيات"""
    print_step("إنشاء decorators للصلاحيات...")
    
    decorators_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/decorators/auth_decorators.py
مزخرفات المصادقة والصلاحيات
Authentication and Authorization Decorators
"""

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from src.models.user import User
import logging

logger = logging.getLogger(__name__)

def token_required(f):
    """مزخرف للتحقق من وجود رمز المصادقة"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # البحث عن الرمز في الرأس
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({
                    'success': False,
                    'error': 'تنسيق رمز المصادقة غير صحيح'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'رمز المصادقة مطلوب'
            }), 401
        
        try:
            # فك تشفير الرمز
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
            
            if not current_user or not current_user.is_active:
                return jsonify({
                    'success': False,
                    'error': 'المستخدم غير موجود أو غير نشط'
                }), 401
            
            # إضافة المستخدم الحالي للطلب
            request.current_user = current_user
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'error': 'انتهت صلاحية رمز المصادقة'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'رمز المصادقة غير صحيح'
            }), 401
        except Exception as e:
            logger.error(f"خطأ في التحقق من الرمز: {e}")
            return jsonify({
                'success': False,
                'error': 'خطأ في التحقق من المصادقة'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """مزخرف للتحقق من صلاحيات الإدارة"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = getattr(request, 'current_user', None)
        
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'المصادقة مطلوبة'
            }), 401
        
        if current_user.role != 'admin':
            return jsonify({
                'success': False,
                'error': 'صلاحيات الإدارة مطلوبة'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated

def permission_required(permission):
    """مزخرف للتحقق من صلاحية محددة"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = getattr(request, 'current_user', None)
            
            if not current_user:
                return jsonify({
                    'success': False,
                    'error': 'المصادقة مطلوبة'
                }), 401
            
            # التحقق من الصلاحية
            if not current_user.has_permission(permission):
                return jsonify({
                    'success': False,
                    'error': f'الصلاحية {permission} مطلوبة'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator
'''
    
    # إنشاء مجلد decorators إذا لم يكن موجوداً
    decorators_dir = Path("backend/src/decorators")
    decorators_dir.mkdir(exist_ok=True)
    
    # إنشاء ملف __init__.py
    init_file = decorators_dir / "__init__.py"
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write("# Decorators package\\n")
    
    # كتابة ملف decorators
    decorators_path = decorators_dir / "auth_decorators.py"
    with open(decorators_path, 'w', encoding='utf-8') as f:
        f.write(decorators_code)
    
    print_success("تم إنشاء decorators للصلاحيات")

def update_user_model():
    """تحديث نموذج المستخدم"""
    print_step("تحديث نموذج المستخدم...")
    
    user_model_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/models/user.py
نموذج المستخدمين المحدث
Updated User Model
"""

from src.database import db
from datetime import datetime
from werkzeug.security import check_password_hash
import json

class User(db.Model):
    """نموذج المستخدمين"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    full_name = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')  # admin, manager, user
    is_active = db.Column(db.Boolean, default=True)
    permissions = db.Column(db.Text)  # JSON string للصلاحيات
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)
    
    def get_permissions(self):
        """الحصول على قائمة الصلاحيات"""
        if self.permissions:
            try:
                return json.loads(self.permissions)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_permissions(self, permissions_list):
        """تعيين قائمة الصلاحيات"""
        self.permissions = json.dumps(permissions_list)
    
    def has_permission(self, permission):
        """التحقق من وجود صلاحية محددة"""
        if self.role == 'admin':
            return True  # الإدارة لديها جميع الصلاحيات
        
        user_permissions = self.get_permissions()
        return permission in user_permissions
    
    def add_permission(self, permission):
        """إضافة صلاحية"""
        permissions = self.get_permissions()
        if permission not in permissions:
            permissions.append(permission)
            self.set_permissions(permissions)
    
    def remove_permission(self, permission):
        """إزالة صلاحية"""
        permissions = self.get_permissions()
        if permission in permissions:
            permissions.remove(permission)
            self.set_permissions(permissions)
    
    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'permissions': self.get_permissions(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
'''
    
    user_model_path = Path("backend/src/models/user.py")
    with open(user_model_path, 'w', encoding='utf-8') as f:
        f.write(user_model_code)
    
    print_success("تم تحديث نموذج المستخدم")

def update_auth_routes():
    """تحديث مسارات المصادقة"""
    print_step("تحديث مسارات المصادقة...")
    
    auth_routes_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/auth_routes.py
مسارات المصادقة المحدثة
Updated Authentication Routes
"""

from flask import Blueprint, request, jsonify, current_app
from src.database import db
from src.models.user import User
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """تسجيل الدخول"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'اسم المستخدم وكلمة المرور مطلوبان'
            }), 400
        
        # البحث عن المستخدم
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'الحساب غير نشط'
            }), 401
        
        # تحديث آخر تسجيل دخول
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # إنشاء رمز المصادقة
        token_payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'data': {
                'token': token,
                'user': user.to_dict()
            },
            'message': 'تم تسجيل الدخول بنجاح'
        })
        
    except Exception as e:
        logger.error(f"خطأ في تسجيل الدخول: {e}")
        return jsonify({
            'success': False,
            'error': 'خطأ في تسجيل الدخول'
        }), 500

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """تسجيل الخروج"""
    return jsonify({
        'success': True,
        'message': 'تم تسجيل الخروج بنجاح'
    })

@auth_bp.route('/api/auth/verify', methods=['GET'])
def verify_token():
    """التحقق من صحة الرمز"""
    token = None
    
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({
                'success': False,
                'error': 'تنسيق رمز المصادقة غير صحيح'
            }), 401
    
    if not token:
        return jsonify({
            'success': False,
            'error': 'رمز المصادقة مطلوب'
        }), 401
    
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.filter_by(id=data['user_id']).first()
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'المستخدم غير موجود أو غير نشط'
            }), 401
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'valid': True
            }
        })
        
    except jwt.ExpiredSignatureError:
        return jsonify({
            'success': False,
            'error': 'انتهت صلاحية رمز المصادقة'
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'success': False,
            'error': 'رمز المصادقة غير صحيح'
        }), 401
    except Exception as e:
        logger.error(f"خطأ في التحقق من الرمز: {e}")
        return jsonify({
            'success': False,
            'error': 'خطأ في التحقق من المصادقة'
        }), 500

@auth_bp.route('/api/auth/change-password', methods=['POST'])
def change_password():
    """تغيير كلمة المرور"""
    from src.decorators.auth_decorators import token_required
    
    @token_required
    def _change_password():
        try:
            data = request.get_json()
            current_user = request.current_user
            
            if not data or not data.get('current_password') or not data.get('new_password'):
                return jsonify({
                    'success': False,
                    'error': 'كلمة المرور الحالية والجديدة مطلوبتان'
                }), 400
            
            # التحقق من كلمة المرور الحالية
            if not current_user.check_password(data['current_password']):
                return jsonify({
                    'success': False,
                    'error': 'كلمة المرور الحالية غير صحيحة'
                }), 400
            
            # تحديث كلمة المرور
            from werkzeug.security import generate_password_hash
            current_user.password_hash = generate_password_hash(data['new_password'])
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'تم تغيير كلمة المرور بنجاح'
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"خطأ في تغيير كلمة المرور: {e}")
            return jsonify({
                'success': False,
                'error': 'خطأ في تغيير كلمة المرور'
            }), 500
    
    return _change_password()
'''
    
    auth_routes_path = Path("backend/src/routes/auth_routes.py")
    with open(auth_routes_path, 'w', encoding='utf-8') as f:
        f.write(auth_routes_code)
    
    print_success("تم تحديث مسارات المصادقة")

def create_admin_user_script():
    """إنشاء سكريبت لإنشاء مستخدم إداري"""
    print_step("إنشاء سكريبت المستخدم الإداري...")
    
    admin_script = '''#!/usr/bin/env python3
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
'''
    
    admin_script_path = Path("backend/create_admin_user.py")
    with open(admin_script_path, 'w', encoding='utf-8') as f:
        f.write(admin_script)
    
    print_success("تم إنشاء سكريبت المستخدم الإداري")

def update_imports_in_routes():
    """تحديث الاستيرادات في المسارات"""
    print_step("تحديث الاستيرادات في المسارات...")
    
    routes_to_update = [
        "backend/src/routes/categories.py",
        "backend/src/routes/warehouses.py", 
        "backend/src/routes/users.py"
    ]
    
    for route_path in routes_to_update:
        if Path(route_path).exists():
            with open(route_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # استبدال الاستيرادات القديمة
            content = content.replace(
                "from src.auth import token_required",
                "from src.decorators.auth_decorators import token_required"
            )
            content = content.replace(
                "from src.auth import token_required, admin_required",
                "from src.decorators.auth_decorators import token_required, admin_required"
            )
            
            with open(route_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print_success("تم تحديث الاستيرادات في المسارات")

def main():
    print("🔐 بدء إصلاح نظام المصادقة والمستخدمين...")
    print("=" * 60)
    
    # إنشاء decorators للصلاحيات
    create_admin_decorators()
    
    # تحديث نموذج المستخدم
    update_user_model()
    
    # تحديث مسارات المصادقة
    update_auth_routes()
    
    # إنشاء سكريبت المستخدم الإداري
    create_admin_user_script()
    
    # تحديث الاستيرادات
    update_imports_in_routes()
    
    print("=" * 60)
    print_success("تم إصلاح نظام المصادقة والمستخدمين بنجاح!")
    print("📋 التحسينات المطبقة:")
    print("   - إنشاء decorators للصلاحيات")
    print("   - تحديث نموذج المستخدم")
    print("   - تحسين مسارات المصادقة")
    print("   - إنشاء سكريبت المستخدم الإداري")
    print("   - تحديث الاستيرادات")
    print()
    print("📋 الخطوات التالية:")
    print("   1. تشغيل: python3 backend/create_admin_user.py")
    print("   2. إعادة تشغيل الخادم الخلفي")

if __name__ == "__main__":
    main()
