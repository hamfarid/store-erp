# File: /home/ubuntu/clean_project/src/auth_service.py
"""
مسار الملف: /home/ubuntu/clean_project/src/auth_service.py

خدمة المصادقة والتفويض الكاملة
تتضمن JWT tokens، إدارة الجلسات، والصلاحيات
"""

import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from database_models import User, Permission, UserPermission, get_session, create_database
import hashlib
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """خدمة المصادقة والتفويض"""
    
    def __init__(self, secret_key: str = None, token_expiry_hours: int = 24):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.token_expiry_hours = token_expiry_hours
        self.algorithm = "HS256"
        
        # إنشاء قاعدة البيانات إذا لم تكن موجودة
        self.engine = create_database()
    
    def create_user(self, username: str, email: str, password: str, 
                   full_name: str, is_admin: bool = False) -> Dict[str, Any]:
        """إنشاء مستخدم جديد"""
        session = get_session(self.engine)
        try:
            # التحقق من عدم وجود المستخدم
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                return {
                    "success": False,
                    "message": "اسم المستخدم أو البريد الإلكتروني موجود بالفعل"
                }
            
            # إنشاء المستخدم الجديد
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                is_admin=is_admin
            )
            user.set_password(password)
            
            session.add(user)
            session.commit()
            
            logger.info(f"تم إنشاء مستخدم جديد: {username}")
            
            return {
                "success": True,
                "message": "تم إنشاء المستخدم بنجاح",
                "user_id": user.id
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"خطأ في إنشاء المستخدم: {e}")
            return {
                "success": False,
                "message": "خطأ في إنشاء المستخدم"
            }
        finally:
            session.close()
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """مصادقة المستخدم"""
        session = get_session(self.engine)
        try:
            user = session.query(User).filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if not user or not user.is_active:
                return {
                    "success": False,
                    "message": "اسم المستخدم أو كلمة المرور غير صحيحة"
                }
            
            if not user.check_password(password):
                return {
                    "success": False,
                    "message": "اسم المستخدم أو كلمة المرور غير صحيحة"
                }
            
            # تحديث آخر تسجيل دخول
            user.last_login = datetime.utcnow()
            session.commit()
            
            # إنشاء الرمز المميز
            token = self.create_token(user.id, user.username, user.is_admin)
            
            logger.info(f"تم تسجيل دخول المستخدم: {username}")
            
            return {
                "success": True,
                "message": "تم تسجيل الدخول بنجاح",
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_admin": user.is_admin
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في مصادقة المستخدم: {e}")
            return {
                "success": False,
                "message": "خطأ في تسجيل الدخول"
            }
        finally:
            session.close()
    
    def create_token(self, user_id: int, username: str, is_admin: bool) -> str:
        """إنشاء رمز JWT"""
        payload = {
            "user_id": user_id,
            "username": username,
            "is_admin": is_admin,
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """التحقق من صحة الرمز المميز"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # التحقق من انتهاء صلاحية الرمز
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return {
                    "valid": False,
                    "message": "انتهت صلاحية الرمز المميز"
                }
            
            return {
                "valid": True,
                "user_id": payload["user_id"],
                "username": payload["username"],
                "is_admin": payload["is_admin"]
            }
            
        except jwt.ExpiredSignatureError:
            return {
                "valid": False,
                "message": "انتهت صلاحية الرمز المميز"
            }
        except jwt.InvalidTokenError:
            return {
                "valid": False,
                "message": "رمز مميز غير صالح"
            }
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """الحصول على صلاحيات المستخدم"""
        session = get_session(self.engine)
        try:
            permissions = session.query(Permission).join(UserPermission).filter(
                UserPermission.user_id == user_id
            ).all()
            
            return [perm.name for perm in permissions]
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على صلاحيات المستخدم: {e}")
            return []
        finally:
            session.close()
    
    def check_permission(self, user_id: int, permission_name: str) -> bool:
        """التحقق من صلاحية محددة للمستخدم"""
        session = get_session(self.engine)
        try:
            # التحقق من كون المستخدم مدير
            user = session.query(User).filter(User.id == user_id).first()
            if user and user.is_admin:
                return True
            
            # التحقق من الصلاحية المحددة
            permission = session.query(Permission).join(UserPermission).filter(
                UserPermission.user_id == user_id,
                Permission.name == permission_name
            ).first()
            
            return permission is not None
            
        except Exception as e:
            logger.error(f"خطأ في التحقق من الصلاحية: {e}")
            return False
        finally:
            session.close()
    
    def grant_permission(self, user_id: int, permission_name: str, granted_by: int) -> Dict[str, Any]:
        """منح صلاحية للمستخدم"""
        session = get_session(self.engine)
        try:
            # التحقق من وجود الصلاحية
            permission = session.query(Permission).filter(
                Permission.name == permission_name
            ).first()
            
            if not permission:
                return {
                    "success": False,
                    "message": "الصلاحية غير موجودة"
                }
            
            # التحقق من عدم وجود الصلاحية للمستخدم
            existing = session.query(UserPermission).filter(
                UserPermission.user_id == user_id,
                UserPermission.permission_id == permission.id
            ).first()
            
            if existing:
                return {
                    "success": False,
                    "message": "المستخدم يملك هذه الصلاحية بالفعل"
                }
            
            # منح الصلاحية
            user_permission = UserPermission(
                user_id=user_id,
                permission_id=permission.id,
                granted_by=granted_by
            )
            
            session.add(user_permission)
            session.commit()
            
            logger.info(f"تم منح صلاحية {permission_name} للمستخدم {user_id}")
            
            return {
                "success": True,
                "message": "تم منح الصلاحية بنجاح"
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"خطأ في منح الصلاحية: {e}")
            return {
                "success": False,
                "message": "خطأ في منح الصلاحية"
            }
        finally:
            session.close()
    
    def revoke_permission(self, user_id: int, permission_name: str) -> Dict[str, Any]:
        """إلغاء صلاحية من المستخدم"""
        session = get_session(self.engine)
        try:
            # البحث عن الصلاحية
            user_permission = session.query(UserPermission).join(Permission).filter(
                UserPermission.user_id == user_id,
                Permission.name == permission_name
            ).first()
            
            if not user_permission:
                return {
                    "success": False,
                    "message": "المستخدم لا يملك هذه الصلاحية"
                }
            
            session.delete(user_permission)
            session.commit()
            
            logger.info(f"تم إلغاء صلاحية {permission_name} من المستخدم {user_id}")
            
            return {
                "success": True,
                "message": "تم إلغاء الصلاحية بنجاح"
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"خطأ في إلغاء الصلاحية: {e}")
            return {
                "success": False,
                "message": "خطأ في إلغاء الصلاحية"
            }
        finally:
            session.close()
    
    def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """الحصول على معلومات المستخدم"""
        session = get_session(self.engine)
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {
                    "success": False,
                    "message": "المستخدم غير موجود"
                }
            
            permissions = self.get_user_permissions(user_id)
            
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                    "permissions": permissions
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات المستخدم: {e}")
            return {
                "success": False,
                "message": "خطأ في الحصول على معلومات المستخدم"
            }
        finally:
            session.close()
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """تغيير كلمة المرور"""
        session = get_session(self.engine)
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {
                    "success": False,
                    "message": "المستخدم غير موجود"
                }
            
            if not user.check_password(old_password):
                return {
                    "success": False,
                    "message": "كلمة المرور الحالية غير صحيحة"
                }
            
            user.set_password(new_password)
            session.commit()
            
            logger.info(f"تم تغيير كلمة مرور المستخدم {user.username}")
            
            return {
                "success": True,
                "message": "تم تغيير كلمة المرور بنجاح"
            }
            
        except Exception as e:
            session.rollback()
            logger.error(f"خطأ في تغيير كلمة المرور: {e}")
            return {
                "success": False,
                "message": "خطأ في تغيير كلمة المرور"
            }
        finally:
            session.close()

# إنشاء مثيل خدمة المصادقة العامة
auth_service = AuthService()

def require_auth(token: str) -> Dict[str, Any]:
    """ديكوريتر للتحقق من المصادقة"""
    return auth_service.verify_token(token)

def require_permission(user_id: int, permission: str) -> bool:
    """ديكوريتر للتحقق من الصلاحيات"""
    return auth_service.check_permission(user_id, permission)



def hash_password(password: str) -> str:
    """تشفير كلمة المرور"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """التحقق من كلمة المرور"""
    return hash_password(password) == hashed_password

# إنشاء مثيل خدمة المصادقة العامة
auth_service = AuthService()

def require_auth(token: str) -> Dict[str, Any]:
    """دالة مساعدة للتحقق من المصادقة"""
    return auth_service.verify_token(token)

def require_permission(token: str, permission: str) -> Dict[str, Any]:
    """دالة مساعدة للتحقق من الصلاحيات"""
    auth_result = auth_service.verify_token(token)
    if not auth_result.get("valid"):
        return auth_result
    
    # التحقق من الصلاحية
    has_permission = auth_service.check_permission(
        auth_result["user_id"], 
        permission
    )
    
    if not has_permission:
        return {
            "valid": False,
            "message": "ليس لديك صلاحية للوصول إلى هذا المورد"
        }
    
    return auth_result

