#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة المصادقة والتفويض لنظام Gaara ERP
"""

import os
import logging
import jwt
import bcrypt
import datetime
from functools import wraps
from dotenv import load_dotenv

# إعداد التسجيل
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()

class AuthManager:
    """مدير المصادقة والتفويض لنظام Gaara ERP"""
    
    _instance = None
    
    def __new__(cls):
        """تنفيذ نمط Singleton لضمان وجود نسخة واحدة فقط من مدير المصادقة"""
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """تهيئة مدير المصادقة"""
        if self._initialized:
            return
            
        from .database.db_manager import DatabaseManager
        
        # الحصول على مدير قاعدة البيانات
        self.db_manager = DatabaseManager()
        
        # إعدادات المصادقة
        self.jwt_secret = os.getenv('JWT_SECRET', 'gaara_erp_secret_key')
        self.jwt_algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        self.jwt_expiration = int(os.getenv('JWT_EXPIRATION', '86400'))  # 24 ساعة
        
        self._initialized = True
        logger.info("تم تهيئة مدير المصادقة بنجاح")
    
    def hash_password(self, password):
        """تشفير كلمة المرور باستخدام bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """التحقق من صحة كلمة المرور"""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    def authenticate_user(self, username, password):
        """مصادقة المستخدم باستخدام اسم المستخدم وكلمة المرور"""
        try:
            # البحث عن المستخدم في قاعدة البيانات
            query = """
                SELECT user_id, username, email, password_hash, first_name, last_name, 
                       is_active, is_admin
                FROM erp.users
                WHERE username = %s
            """
            result = self.db_manager.execute_query(query, (username,))
            
            if not result:
                logger.warning(f"محاولة تسجيل دخول فاشلة: المستخدم {username} غير موجود")
                return None
            
            user = result[0]
            
            # التحقق من حالة المستخدم
            if not user['is_active']:
                logger.warning(f"محاولة تسجيل دخول فاشلة: المستخدم {username} غير نشط")
                return None
            
            # التحقق من كلمة المرور
            if not self.verify_password(password, user['password_hash']):
                logger.warning(f"محاولة تسجيل دخول فاشلة: كلمة مرور خاطئة للمستخدم {username}")
                return None
            
            # تحديث آخر تسجيل دخول
            update_query = """
                UPDATE erp.users
                SET last_login = CURRENT_TIMESTAMP
                WHERE user_id = %s
            """
            self.db_manager.execute_query(update_query, (user['user_id'],), fetch=False)
            
            # إنشاء رمز JWT
            token = self.generate_token(user)
            
            # إعداد بيانات المستخدم للإرجاع
            user_data = {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'is_admin': user['is_admin'],
                'token': token
            }
            
            # الحصول على أدوار المستخدم
            roles = self.get_user_roles(user['user_id'])
            user_data['roles'] = roles
            
            # الحصول على صلاحيات المستخدم
            permissions = self.get_user_permissions(user['user_id'])
            user_data['permissions'] = permissions
            
            logger.info(f"تم تسجيل دخول المستخدم {username} بنجاح")
            return user_data
            
        except Exception as e:
            logger.error(f"خطأ أثناء مصادقة المستخدم: {str(e)}")
            return None
    
    def generate_token(self, user):
        """إنشاء رمز JWT للمستخدم"""
        payload = {
            'user_id': user['user_id'],
            'username': user['username'],
            'is_admin': user['is_admin'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.jwt_expiration)
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token
    
    def verify_token(self, token):
        """التحقق من صحة رمز JWT"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("رمز JWT منتهي الصلاحية")
            return None
        except jwt.InvalidTokenError:
            logger.warning("رمز JWT غير صالح")
            return None
    
    def get_user_roles(self, user_id):
        """الحصول على أدوار المستخدم"""
        query = """
            SELECT r.role_id, r.role_name, r.description
            FROM erp.roles r
            JOIN erp.user_roles ur ON r.role_id = ur.role_id
            WHERE ur.user_id = %s AND r.is_active = TRUE
        """
        return self.db_manager.execute_query(query, (user_id,))
    
    def get_user_permissions(self, user_id):
        """الحصول على صلاحيات المستخدم"""
        query = """
            SELECT DISTINCT p.permission_id, p.permission_code, p.description, p.module
            FROM erp.permissions p
            JOIN erp.role_permissions rp ON p.permission_id = rp.permission_id
            JOIN erp.user_roles ur ON rp.role_id = ur.role_id
            WHERE ur.user_id = %s
        """
        return self.db_manager.execute_query(query, (user_id,))
    
    def has_permission(self, user_id, permission_code):
        """التحقق مما إذا كان المستخدم لديه صلاحية محددة"""
        query = """
            SELECT COUNT(*) as count
            FROM erp.permissions p
            JOIN erp.role_permissions rp ON p.permission_id = rp.permission_id
            JOIN erp.user_roles ur ON rp.role_id = ur.role_id
            JOIN erp.roles r ON ur.role_id = r.role_id
            WHERE ur.user_id = %s AND p.permission_code = %s AND r.is_active = TRUE
        """
        result = self.db_manager.execute_query(query, (user_id, permission_code))
        return result[0]['count'] > 0
    
    def is_admin(self, user_id):
        """التحقق مما إذا كان المستخدم مديرًا للنظام"""
        query = """
            SELECT is_admin
            FROM erp.users
            WHERE user_id = %s
        """
        result = self.db_manager.execute_query(query, (user_id,))
        return result and result[0]['is_admin']
    
    def require_auth(self, f):
        """مزخرف للتحقق من المصادقة"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # الحصول على رمز JWT من الطلب
            # هذا مثال فقط، يجب تعديله حسب إطار العمل المستخدم
            # مثال: token = request.headers.get('Authorization')
            
            if not token:
                return {'message': 'رمز المصادقة مفقود'}, 401
            
            # التحقق من صحة الرمز
            payload = self.verify_token(token)
            if not payload:
                return {'message': 'رمز المصادقة غير صالح أو منتهي الصلاحية'}, 401
            
            # إضافة بيانات المستخدم إلى الطلب
            # مثال: request.user = payload
            
            return f(*args, **kwargs)
        return decorated
    
    def require_permission(self, permission_code):
        """مزخرف للتحقق من الصلاحية"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                # الحصول على بيانات المستخدم من الطلب
                # مثال: user_id = request.user['user_id']
                user_id = None
                
                if not user_id:
                    return {'message': 'غير مصرح'}, 401
                
                # التحقق من الصلاحية
                if not self.has_permission(user_id, permission_code) and not self.is_admin(user_id):
                    return {'message': 'ليس لديك صلاحية للوصول إلى هذا المورد'}, 403
                
                return f(*args, **kwargs)
            return decorated
        return decorator

# نموذج استخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # تهيئة مدير المصادقة
    auth_manager = AuthManager()
    
    # مثال على تشفير كلمة المرور
    hashed_password = auth_manager.hash_password("password123")
    print(f"كلمة المرور المشفرة: {hashed_password}")
    
    # مثال على التحقق من كلمة المرور
    is_valid = auth_manager.verify_password("password123", hashed_password)
    print(f"كلمة المرور صحيحة: {is_valid}")
