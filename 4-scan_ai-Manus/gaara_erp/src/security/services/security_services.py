"""
خدمات الأمان
يحتوي هذا الملف على خدمات إدارة الأمان والصلاحيات
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import re
import pyotp
import qrcode
from io import BytesIO
import base64

from ..models.security_models import (
    Permission, Role, UserPermission, UserRole, AccessToken,
    LoginAttempt, PasswordReset, SecurityPolicy, ApiKey,
    TwoFactorAuth, SecurityAudit, PermissionScope
)


class PermissionService:
    """خدمة إدارة الصلاحيات"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def create_permission(self, permission_data: Dict[str, Any]) -> Permission:
        """إنشاء صلاحية جديدة"""
        # التحقق من البيانات المطلوبة
        required_fields = ["name", "code", "module"]
        for field in required_fields:
            if field not in permission_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من عدم وجود صلاحية بنفس الكود
        existing_permission = self.get_permission_by_code(permission_data["code"])
        if existing_permission:
            raise ValueError(f"توجد صلاحية بالفعل بالكود {permission_data['code']}")
        
        # إنشاء كائن الصلاحية
        permission = Permission(
            name=permission_data["name"],
            code=permission_data["code"],
            description=permission_data.get("description"),
            module=permission_data["module"],
            scope=permission_data.get("scope", PermissionScope.SYSTEM),
            is_active=permission_data.get("is_active", True)
        )
        
        # حفظ الصلاحية في قاعدة البيانات
        self.db_manager.save_permission(permission)
        
        return permission
    
    def get_all_permissions(self, module: str = None, scope: str = None, is_active: bool = None) -> List[Permission]:
        """الحصول على جميع الصلاحيات"""
        return self.db_manager.get_permissions(module, scope, is_active)
    
    def get_permission(self, permission_id: str) -> Optional[Permission]:
        """الحصول على صلاحية بواسطة المعرف"""
        return self.db_manager.get_permission_by_id(permission_id)
    
    def get_permission_by_code(self, code: str) -> Optional[Permission]:
        """الحصول على صلاحية بواسطة الكود"""
        return self.db_manager.get_permission_by_code(code)
    
    def update_permission(self, permission_id: str, permission_data: Dict[str, Any]) -> Optional[Permission]:
        """تحديث صلاحية"""
        # الحصول على الصلاحية
        permission = self.get_permission(permission_id)
        if not permission:
            return None
        
        # تحديث البيانات
        if "name" in permission_data:
            permission.name = permission_data["name"]
        if "description" in permission_data:
            permission.description = permission_data["description"]
        if "module" in permission_data:
            permission.module = permission_data["module"]
        if "scope" in permission_data:
            permission.scope = permission_data["scope"]
        if "is_active" in permission_data:
            permission.is_active = permission_data["is_active"]
        
        # تحديث وقت التحديث
        permission.updated_at = datetime.now()
        
        # حفظ التغييرات
        self.db_manager.update_permission(permission)
        
        return permission
    
    def delete_permission(self, permission_id: str) -> bool:
        """حذف صلاحية"""
        return self.db_manager.delete_permission(permission_id)
    
    def get_permissions_by_module(self, module: str) -> List[Permission]:
        """الحصول على الصلاحيات حسب الوحدة"""
        return self.db_manager.get_permissions_by_module(module)
    
    def get_permissions_by_scope(self, scope: PermissionScope) -> List[Permission]:
        """الحصول على الصلاحيات حسب النطاق"""
        return self.db_manager.get_permissions_by_scope(scope)


class RoleService:
    """خدمة إدارة الأدوار"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.permission_service = PermissionService(db_manager)
    
    def create_role(self, role_data: Dict[str, Any]) -> Role:
        """إنشاء دور جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["name"]
        for field in required_fields:
            if field not in role_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من الصلاحيات
        permissions = role_data.get("permissions", [])
        for permission_id in permissions:
            permission = self.permission_service.get_permission(permission_id)
            if not permission:
                raise ValueError(f"الصلاحية بالمعرف {permission_id} غير موجودة")
        
        # إنشاء كائن الدور
        role = Role(
            name=role_data["name"],
            description=role_data.get("description"),
            permissions=permissions,
            is_system_role=role_data.get("is_system_role", False),
            is_active=role_data.get("is_active", True),
            created_by=role_data.get("created_by"),
            updated_by=role_data.get("updated_by")
        )
        
        # حفظ الدور في قاعدة البيانات
        self.db_manager.save_role(role)
        
        return role
    
    def get_all_roles(self, is_system_role: bool = None, is_active: bool = None) -> List[Role]:
        """الحصول على جميع الأدوار"""
        return self.db_manager.get_roles(is_system_role, is_active)
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """الحصول على دور بواسطة المعرف"""
        return self.db_manager.get_role_by_id(role_id)
    
    def get_role_by_name(self, name: str) -> Optional[Role]:
        """الحصول على دور بواسطة الاسم"""
        return self.db_manager.get_role_by_name(name)
    
    def update_role(self, role_id: str, role_data: Dict[str, Any]) -> Optional[Role]:
        """تحديث دور"""
        # الحصول على الدور
        role = self.get_role(role_id)
        if not role:
            return None
        
        # التحقق من الصلاحيات
        if "permissions" in role_data:
            permissions = role_data["permissions"]
            for permission_id in permissions:
                permission = self.permission_service.get_permission(permission_id)
                if not permission:
                    raise ValueError(f"الصلاحية بالمعرف {permission_id} غير موجودة")
            role.permissions = permissions
        
        # تحديث البيانات
        if "name" in role_data:
            role.name = role_data["name"]
        if "description" in role_data:
            role.description = role_data["description"]
        if "is_system_role" in role_data:
            role.is_system_role = role_data["is_system_role"]
        if "is_active" in role_data:
            role.is_active = role_data["is_active"]
        if "updated_by" in role_data:
            role.updated_by = role_data["updated_by"]
        
        # تحديث وقت التحديث
        role.updated_at = datetime.now()
        
        # حفظ التغييرات
        self.db_manager.update_role(role)
        
        return role
    
    def delete_role(self, role_id: str) -> bool:
        """حذف دور"""
        # التحقق من عدم وجود مستخدمين مرتبطين بالدور
        user_roles = self.db_manager.get_user_roles_by_role(role_id)
        if user_roles:
            raise ValueError("لا يمكن حذف الدور لأنه مرتبط بمستخدمين")
        
        return self.db_manager.delete_role(role_id)
    
    def get_role_permissions(self, role_id: str) -> List[Permission]:
        """الحصول على صلاحيات الدور"""
        role = self.get_role(role_id)
        if not role:
            return []
        
        permissions = []
        for permission_id in role.permissions:
            permission = self.permission_service.get_permission(permission_id)
            if permission:
                permissions.append(permission)
        
        return permissions
    
    def add_permission_to_role(self, role_id: str, permission_id: str) -> Optional[Role]:
        """إضافة صلاحية إلى دور"""
        # الحصول على الدور
        role = self.get_role(role_id)
        if not role:
            return None
        
        # الحصول على الصلاحية
        permission = self.permission_service.get_permission(permission_id)
        if not permission:
            raise ValueError(f"الصلاحية بالمعرف {permission_id} غير موجودة")
        
        # إضافة الصلاحية إلى الدور
        if permission_id not in role.permissions:
            role.permissions.append(permission_id)
            role.updated_at = datetime.now()
            self.db_manager.update_role(role)
        
        return role
    
    def remove_permission_from_role(self, role_id: str, permission_id: str) -> Optional[Role]:
        """إزالة صلاحية من دور"""
        # الحصول على الدور
        role = self.get_role(role_id)
        if not role:
            return None
        
        # إزالة الصلاحية من الدور
        if permission_id in role.permissions:
            role.permissions.remove(permission_id)
            role.updated_at = datetime.now()
            self.db_manager.update_role(role)
        
        return role


class UserPermissionService:
    """خدمة إدارة صلاحيات المستخدمين"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.permission_service = PermissionService(db_manager)
        self.role_service = RoleService(db_manager)
    
    def assign_permission_to_user(self, user_permission_data: Dict[str, Any]) -> UserPermission:
        """تعيين صلاحية لمستخدم"""
        # التحقق من البيانات المطلوبة
        required_fields = ["user_id", "permission_id"]
        for field in required_fields:
            if field not in user_permission_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من وجود المستخدم
        user_id = user_permission_data["user_id"]
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"المستخدم بالمعرف {user_id} غير موجود")
        
        # التحقق من وجود الصلاحية
        permission_id = user_permission_data["permission_id"]
        permission = self.permission_service.get_permission(permission_id)
        if not permission:
            raise ValueError(f"الصلاحية بالمعرف {permission_id} غير موجودة")
        
        # التحقق من عدم وجود نفس الصلاحية للمستخدم
        existing_permission = self.db_manager.get_user_permission(
            user_id, permission_id,
            user_permission_data.get("country_id"),
            user_permission_data.get("company_id"),
            user_permission_data.get("branch_id")
        )
        if existing_permission:
            raise ValueError("الصلاحية موجودة بالفعل للمستخدم")
        
        # إنشاء كائن صلاحية المستخدم
        user_permission = UserPermission(
            user_id=user_id,
            permission_id=permission_id,
            country_id=user_permission_data.get("country_id"),
            company_id=user_permission_data.get("company_id"),
            branch_id=user_permission_data.get("branch_id"),
            granted_by=user_permission_data.get("granted_by"),
            expires_at=user_permission_data.get("expires_at"),
            is_active=user_permission_data.get("is_active", True)
        )
        
        # حفظ صلاحية المستخدم في قاعدة البيانات
        self.db_manager.save_user_permission(user_permission)
        
        return user_permission
    
    def assign_role_to_user(self, user_role_data: Dict[str, Any]) -> UserRole:
        """تعيين دور لمستخدم"""
        # التحقق من البيانات المطلوبة
        required_fields = ["user_id", "role_id"]
        for field in required_fields:
            if field not in user_role_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من وجود المستخدم
        user_id = user_role_data["user_id"]
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"المستخدم بالمعرف {user_id} غير موجود")
        
        # التحقق من وجود الدور
        role_id = user_role_data["role_id"]
        role = self.role_service.get_role(role_id)
        if not role:
            raise ValueError(f"الدور بالمعرف {role_id} غير موجود")
        
        # التحقق من عدم وجود نفس الدور للمستخدم
        existing_role = self.db_manager.get_user_role(
            user_id, role_id,
            user_role_data.get("country_id"),
            user_role_data.get("company_id"),
            user_role_data.get("branch_id")
        )
        if existing_role:
            raise ValueError("الدور موجود بالفعل للمستخدم")
        
        # إنشاء كائن دور المستخدم
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            country_id=user_role_data.get("country_id"),
            company_id=user_role_data.get("company_id"),
            branch_id=user_role_data.get("branch_id"),
            granted_by=user_role_data.get("granted_by"),
            expires_at=user_role_data.get("expires_at"),
            is_active=user_role_data.get("is_active", True)
        )
        
        # حفظ دور المستخدم في قاعدة البيانات
        self.db_manager.save_user_role(user_role)
        
        return user_role
    
    def get_user_permissions(self, user_id: str, country_id: str = None, company_id: str = None, branch_id: str = None) -> List[Permission]:
        """الحصول على صلاحيات المستخدم"""
        # الحصول على صلاحيات المستخدم المباشرة
        user_permissions = self.db_manager.get_user_permissions_by_user(user_id)
        
        # الحصول على أدوار المستخدم
        user_roles = self.db_manager.get_user_roles_by_user(user_id)
        
        # جمع جميع الصلاحيات
        permissions = []
        permission_ids = set()
        
        # إضافة الصلاحيات المباشرة
        for user_permission in user_permissions:
            # التحقق من النطاق
            if self._check_permission_scope(user_permission, country_id, company_id, branch_id):
                permission = self.permission_service.get_permission(user_permission.permission_id)
                if permission and permission.is_active and permission.id not in permission_ids:
                    permissions.append(permission)
                    permission_ids.add(permission.id)
        
        # إضافة صلاحيات الأدوار
        for user_role in user_roles:
            # التحقق من النطاق
            if self._check_role_scope(user_role, country_id, company_id, branch_id):
                role = self.role_service.get_role(user_role.role_id)
                if role and role.is_active:
                    for permission_id in role.permissions:
                        if permission_id not in permission_ids:
                            permission = self.permission_service.get_permission(permission_id)
                            if permission and permission.is_active:
                                permissions.append(permission)
                                permission_ids.add(permission.id)
        
        return permissions
    
    def get_user_roles(self, user_id: str, country_id: str = None, company_id: str = None, branch_id: str = None) -> List[Role]:
        """الحصول على أدوار المستخدم"""
        # الحصول على أدوار المستخدم
        user_roles = self.db_manager.get_user_roles_by_user(user_id)
        
        # جمع الأدوار
        roles = []
        role_ids = set()
        
        for user_role in user_roles:
            # التحقق من النطاق
            if self._check_role_scope(user_role, country_id, company_id, branch_id):
                role = self.role_service.get_role(user_role.role_id)
                if role and role.is_active and role.id not in role_ids:
                    roles.append(role)
                    role_ids.add(role.id)
        
        return roles
    
    def _check_permission_scope(self, user_permission: UserPermission, country_id: str = None, company_id: str = None, branch_id: str = None) -> bool:
        """التحقق من نطاق الصلاحية"""
        # التحقق من أن الصلاحية نشطة
        if not user_permission.is_active:
            return False
        
        # التحقق من تاريخ انتهاء الصلاحية
        if user_permission.expires_at and datetime.now() > user_permission.expires_at:
            return False
        
        # الحصول على الصلاحية
        permission = self.permission_service.get_permission(user_permission.permission_id)
        if not permission or not permission.is_active:
            return False
        
        # التحقق من النطاق
        if permission.scope == PermissionScope.SYSTEM:
            return True
        
        if permission.scope == PermissionScope.COUNTRY:
            # إذا كانت الصلاحية على مستوى الدولة
            if user_permission.country_id:
                # إذا كان هناك تحديد للدولة
                if country_id:
                    return user_permission.country_id == country_id
                return True
            return False
        
        if permission.scope == PermissionScope.COMPANY:
            # إذا كانت الصلاحية على مستوى الشركة
            if user_permission.company_id:
                # إذا كان هناك تحديد للشركة
                if company_id:
                    return user_permission.company_id == company_id
                return True
            return False
        
        if permission.scope == PermissionScope.BRANCH:
            # إذا كانت الصلاحية على مستوى الفرع
            if user_permission.branch_id:
                # إذا كان هناك تحديد للفرع
                if branch_id:
                    return user_permission.branch_id == branch_id
                return True
            return False
        
        return False
    
    def _check_role_scope(self, user_role: UserRole, country_id: str = None, company_id: str = None, branch_id: str = None) -> bool:
        """التحقق من نطاق الدور"""
        # التحقق من أن الدور نشط
        if not user_role.is_active:
            return False
        
        # التحقق من تاريخ انتهاء الدور
        if user_role.expires_at and datetime.now() > user_role.expires_at:
            return False
        
        # التحقق من النطاق
        if not user_role.country_id and not user_role.company_id and not user_role.branch_id:
            # إذا كان الدور على مستوى النظام
            return True
        
        if user_role.country_id:
            # إذا كان الدور على مستوى الدولة
            if country_id:
                return user_role.country_id == country_id
            return True
        
        if user_role.company_id:
            # إذا كان الدور على مستوى الشركة
            if company_id:
                return user_role.company_id == company_id
            return True
        
        if user_role.branch_id:
            # إذا كان الدور على مستوى الفرع
            if branch_id:
                return user_role.branch_id == branch_id
            return True
        
        return False
    
    def has_permission(self, user_id: str, permission_code: str, country_id: str = None, company_id: str = None, branch_id: str = None) -> bool:
        """التحقق مما إذا كان المستخدم لديه صلاحية معينة"""
        # الحصول على الصلاحية
        permission = self.permission_service.get_permission_by_code(permission_code)
        if not permission:
            return False
        
        # الحصول على صلاحيات المستخدم
        permissions = self.get_user_permissions(user_id, country_id, company_id, branch_id)
        
        # التحقق من وجود الصلاحية
        for user_permission in permissions:
            if user_permission.code == permission_code:
                return True
        
        return False
    
    def revoke_permission_from_user(self, user_permission_id: str) -> bool:
        """إلغاء صلاحية من مستخدم"""
        return self.db_manager.delete_user_permission(user_permission_id)
    
    def revoke_role_from_user(self, user_role_id: str) -> bool:
        """إلغاء دور من مستخدم"""
        return self.db_manager.delete_user_role(user_role_id)
    
    def get_users_by_permission(self, permission_id: str) -> List[Dict[str, Any]]:
        """الحصول على المستخدمين الذين لديهم صلاحية معينة"""
        # الحصول على صلاحيات المستخدمين
        user_permissions = self.db_manager.get_user_permissions_by_permission(permission_id)
        
        # الحصول على الأدوار التي تحتوي على الصلاحية
        roles = self.db_manager.get_roles_by_permission(permission_id)
        
        # جمع المستخدمين
        users = []
        user_ids = set()
        
        # إضافة المستخدمين الذين لديهم الصلاحية مباشرة
        for user_permission in user_permissions:
            if user_permission.user_id not in user_ids:
                user = self.db_manager.get_user_by_id(user_permission.user_id)
                if user:
                    users.append({
                        "user": user,
                        "source": "direct",
                        "granted_at": user_permission.granted_at,
                        "expires_at": user_permission.expires_at
                    })
                    user_ids.add(user_permission.user_id)
        
        # إضافة المستخدمين الذين لديهم الصلاحية من خلال الأدوار
        for role in roles:
            user_roles = self.db_manager.get_user_roles_by_role(role.id)
            for user_role in user_roles:
                if user_role.user_id not in user_ids:
                    user = self.db_manager.get_user_by_id(user_role.user_id)
                    if user:
                        users.append({
                            "user": user,
                            "source": "role",
                            "role": role,
                            "granted_at": user_role.granted_at,
                            "expires_at": user_role.expires_at
                        })
                        user_ids.add(user_role.user_id)
        
        return users
    
    def get_users_by_role(self, role_id: str) -> List[Dict[str, Any]]:
        """الحصول على المستخدمين الذين لديهم دور معين"""
        # الحصول على أدوار المستخدمين
        user_roles = self.db_manager.get_user_roles_by_role(role_id)
        
        # جمع المستخدمين
        users = []
        
        for user_role in user_roles:
            user = self.db_manager.get_user_by_id(user_role.user_id)
            if user:
                users.append({
                    "user": user,
                    "granted_at": user_role.granted_at,
                    "expires_at": user_role.expires_at,
                    "country_id": user_role.country_id,
                    "company_id": user_role.company_id,
                    "branch_id": user_role.branch_id
                })
        
        return users


class AuthService:
    """خدمة المصادقة"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_permission_service = UserPermissionService(db_manager)
    
    def authenticate(self, username: str, password: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """مصادقة المستخدم"""
        # تسجيل محاولة تسجيل الدخول
        login_attempt = LoginAttempt(
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False
        )
        
        # التحقق من عدد محاولات تسجيل الدخول الفاشلة
        failed_attempts = self.db_manager.get_failed_login_attempts(username, ip_address, minutes=30)
        if len(failed_attempts) >= 5:
            login_attempt.failure_reason = "تم تجاوز الحد الأقصى لمحاولات تسجيل الدخول"
            self.db_manager.save_login_attempt(login_attempt)
            return {
                "success": False,
                "message": "تم تجاوز الحد الأقصى لمحاولات تسجيل الدخول. يرجى المحاولة مرة أخرى بعد 30 دقيقة."
            }
        
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_username(username)
        if not user:
            login_attempt.failure_reason = "اسم المستخدم غير موجود"
            self.db_manager.save_login_attempt(login_attempt)
            return {
                "success": False,
                "message": "اسم المستخدم أو كلمة المرور غير صحيحة"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            login_attempt.failure_reason = "المستخدم غير نشط"
            self.db_manager.save_login_attempt(login_attempt)
            return {
                "success": False,
                "message": "الحساب غير نشط. يرجى الاتصال بالمسؤول."
            }
        
        # التحقق من كلمة المرور
        if not self._verify_password(password, user.password_hash):
            login_attempt.failure_reason = "كلمة المرور غير صحيحة"
            self.db_manager.save_login_attempt(login_attempt)
            return {
                "success": False,
                "message": "اسم المستخدم أو كلمة المرور غير صحيحة"
            }
        
        # التحقق من تاريخ انتهاء كلمة المرور
        if user.password_expires_at and datetime.now() > user.password_expires_at:
            login_attempt.failure_reason = "كلمة المرور منتهية الصلاحية"
            self.db_manager.save_login_attempt(login_attempt)
            return {
                "success": False,
                "message": "كلمة المرور منتهية الصلاحية. يرجى إعادة تعيين كلمة المرور.",
                "require_password_reset": True,
                "user_id": user.id
            }
        
        # التحقق من المصادقة الثنائية
        two_factor_auth = self.db_manager.get_two_factor_auth_by_user(user.id)
        if two_factor_auth and two_factor_auth.is_enabled:
            login_attempt.success = True
            self.db_manager.save_login_attempt(login_attempt)
            return {
                "success": True,
                "require_2fa": True,
                "user_id": user.id,
                "two_factor_method": two_factor_auth.method
            }
        
        # إنشاء رمز الوصول
        access_token = self._create_access_token(user.id, ip_address, user_agent)
        
        # تحديث آخر تسجيل دخول للمستخدم
        user.last_login_at = datetime.now()
        user.last_login_ip = ip_address
        self.db_manager.update_user(user)
        
        # تسجيل محاولة تسجيل الدخول الناجحة
        login_attempt.success = True
        self.db_manager.save_login_attempt(login_attempt)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user.id, "login", "user", user.id,
            ip_address, user_agent, {"method": "password"}
        )
        
        return {
            "success": True,
            "user": user.to_dict(),
            "access_token": access_token.token,
            "refresh_token": access_token.refresh_token,
            "expires_at": access_token.expires_at.isoformat()
        }
    
    def verify_two_factor(self, user_id: str, code: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """التحقق من المصادقة الثنائية"""
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # الحصول على المصادقة الثنائية
        two_factor_auth = self.db_manager.get_two_factor_auth_by_user(user_id)
        if not two_factor_auth or not two_factor_auth.is_enabled:
            return {
                "success": False,
                "message": "المصادقة الثنائية غير مفعلة"
            }
        
        # التحقق من الرمز
        if two_factor_auth.method == "app":
            # التحقق من رمز التطبيق
            totp = pyotp.TOTP(two_factor_auth.secret_key)
            if not totp.verify(code):
                return {
                    "success": False,
                    "message": "رمز التحقق غير صحيح"
                }
        elif code in two_factor_auth.backup_codes:
            # استخدام رمز النسخ الاحتياطي
            two_factor_auth.backup_codes.remove(code)
            self.db_manager.update_two_factor_auth(two_factor_auth)
        else:
            return {
                "success": False,
                "message": "رمز التحقق غير صحيح"
            }
        
        # تحديث آخر تحقق
        two_factor_auth.last_verified_at = datetime.now()
        self.db_manager.update_two_factor_auth(two_factor_auth)
        
        # إنشاء رمز الوصول
        access_token = self._create_access_token(user.id, ip_address, user_agent)
        
        # تحديث آخر تسجيل دخول للمستخدم
        user.last_login_at = datetime.now()
        user.last_login_ip = ip_address
        self.db_manager.update_user(user)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user.id, "login", "user", user.id,
            ip_address, user_agent, {"method": "2fa", "two_factor_method": two_factor_auth.method}
        )
        
        return {
            "success": True,
            "user": user.to_dict(),
            "access_token": access_token.token,
            "refresh_token": access_token.refresh_token,
            "expires_at": access_token.expires_at.isoformat()
        }
    
    def refresh_token(self, refresh_token: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """تحديث رمز الوصول"""
        # الحصول على رمز الوصول
        access_token = self.db_manager.get_access_token_by_refresh_token(refresh_token)
        if not access_token:
            return {
                "success": False,
                "message": "رمز التحديث غير صالح"
            }
        
        # التحقق من أن الرمز غير ملغي
        if access_token.is_revoked:
            return {
                "success": False,
                "message": "رمز التحديث ملغي"
            }
        
        # التحقق من تاريخ انتهاء الرمز
        if access_token.is_expired():
            return {
                "success": False,
                "message": "رمز التحديث منتهي الصلاحية"
            }
        
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(access_token.user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        # إلغاء الرمز القديم
        access_token.is_revoked = True
        self.db_manager.update_access_token(access_token)
        
        # إنشاء رمز جديد
        new_access_token = self._create_access_token(user.id, ip_address, user_agent)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user.id, "token_refresh", "user", user.id,
            ip_address, user_agent, {}
        )
        
        return {
            "success": True,
            "user": user.to_dict(),
            "access_token": new_access_token.token,
            "refresh_token": new_access_token.refresh_token,
            "expires_at": new_access_token.expires_at.isoformat()
        }
    
    def logout(self, token: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """تسجيل الخروج"""
        # الحصول على رمز الوصول
        access_token = self.db_manager.get_access_token_by_token(token)
        if not access_token:
            return {
                "success": False,
                "message": "رمز الوصول غير صالح"
            }
        
        # إلغاء الرمز
        access_token.is_revoked = True
        self.db_manager.update_access_token(access_token)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            access_token.user_id, "logout", "user", access_token.user_id,
            ip_address, user_agent, {}
        )
        
        return {
            "success": True,
            "message": "تم تسجيل الخروج بنجاح"
        }
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """التحقق من رمز الوصول"""
        # الحصول على رمز الوصول
        access_token = self.db_manager.get_access_token_by_token(token)
        if not access_token:
            return {
                "success": False,
                "message": "رمز الوصول غير صالح"
            }
        
        # التحقق من أن الرمز غير ملغي
        if access_token.is_revoked:
            return {
                "success": False,
                "message": "رمز الوصول ملغي"
            }
        
        # التحقق من تاريخ انتهاء الرمز
        if access_token.is_expired():
            return {
                "success": False,
                "message": "رمز الوصول منتهي الصلاحية"
            }
        
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(access_token.user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        return {
            "success": True,
            "user": user.to_dict()
        }
    
    def change_password(self, user_id: str, current_password: str, new_password: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """تغيير كلمة المرور"""
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من كلمة المرور الحالية
        if not self._verify_password(current_password, user.password_hash):
            return {
                "success": False,
                "message": "كلمة المرور الحالية غير صحيحة"
            }
        
        # التحقق من سياسة كلمة المرور
        security_policy = self.db_manager.get_default_security_policy()
        if security_policy:
            validation_result = security_policy.validate_password(new_password)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "message": "كلمة المرور لا تتوافق مع سياسة الأمان",
                    "errors": validation_result["errors"]
                }
        
        # تحديث كلمة المرور
        user.password_hash = self._hash_password(new_password)
        user.password_changed_at = datetime.now()
        
        # تحديث تاريخ انتهاء كلمة المرور
        if security_policy and security_policy.password_expiry_days > 0:
            user.password_expires_at = datetime.now() + timedelta(days=security_policy.password_expiry_days)
        else:
            user.password_expires_at = None
        
        # حفظ التغييرات
        self.db_manager.update_user(user)
        
        # إلغاء جميع رموز الوصول
        self.db_manager.revoke_all_access_tokens(user_id)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user_id, "password_change", "user", user_id,
            ip_address, user_agent, {}
        )
        
        return {
            "success": True,
            "message": "تم تغيير كلمة المرور بنجاح"
        }
    
    def reset_password_request(self, email: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """طلب إعادة تعيين كلمة المرور"""
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_email(email)
        if not user:
            return {
                "success": False,
                "message": "البريد الإلكتروني غير مسجل"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        # إنشاء طلب إعادة تعيين كلمة المرور
        password_reset = PasswordReset(
            user_id=user.id,
            ip_address=ip_address
        )
        
        # حفظ الطلب
        self.db_manager.save_password_reset(password_reset)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user.id, "password_reset_request", "user", user.id,
            ip_address, user_agent, {}
        )
        
        # إرسال بريد إلكتروني (يمكن تنفيذه في خدمة منفصلة)
        # TODO: إرسال بريد إلكتروني
        
        return {
            "success": True,
            "message": "تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني"
        }
    
    def reset_password(self, token: str, new_password: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """إعادة تعيين كلمة المرور"""
        # الحصول على طلب إعادة تعيين كلمة المرور
        password_reset = self.db_manager.get_password_reset_by_token(token)
        if not password_reset:
            return {
                "success": False,
                "message": "رمز إعادة تعيين كلمة المرور غير صالح"
            }
        
        # التحقق من أن الطلب غير مستخدم
        if password_reset.is_used:
            return {
                "success": False,
                "message": "رمز إعادة تعيين كلمة المرور مستخدم بالفعل"
            }
        
        # التحقق من تاريخ انتهاء الطلب
        if password_reset.is_expired():
            return {
                "success": False,
                "message": "رمز إعادة تعيين كلمة المرور منتهي الصلاحية"
            }
        
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(password_reset.user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        # التحقق من سياسة كلمة المرور
        security_policy = self.db_manager.get_default_security_policy()
        if security_policy:
            validation_result = security_policy.validate_password(new_password)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "message": "كلمة المرور لا تتوافق مع سياسة الأمان",
                    "errors": validation_result["errors"]
                }
        
        # تحديث كلمة المرور
        user.password_hash = self._hash_password(new_password)
        user.password_changed_at = datetime.now()
        
        # تحديث تاريخ انتهاء كلمة المرور
        if security_policy and security_policy.password_expiry_days > 0:
            user.password_expires_at = datetime.now() + timedelta(days=security_policy.password_expiry_days)
        else:
            user.password_expires_at = None
        
        # حفظ التغييرات
        self.db_manager.update_user(user)
        
        # تحديث طلب إعادة تعيين كلمة المرور
        password_reset.is_used = True
        password_reset.used_at = datetime.now()
        self.db_manager.update_password_reset(password_reset)
        
        # إلغاء جميع رموز الوصول
        self.db_manager.revoke_all_access_tokens(user.id)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user.id, "password_reset", "user", user.id,
            ip_address, user_agent, {}
        )
        
        return {
            "success": True,
            "message": "تم إعادة تعيين كلمة المرور بنجاح"
        }
    
    def setup_two_factor(self, user_id: str, method: str = "app") -> Dict[str, Any]:
        """إعداد المصادقة الثنائية"""
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        # التحقق من الطريقة
        if method not in ["app", "sms", "email"]:
            return {
                "success": False,
                "message": "طريقة المصادقة الثنائية غير صالحة"
            }
        
        # إنشاء المصادقة الثنائية
        two_factor_auth = TwoFactorAuth(
            user_id=user_id,
            method=method
        )
        
        # توليد المفتاح السري
        if method == "app":
            two_factor_auth.secret_key = pyotp.random_base32()
        
        # توليد رموز النسخ الاحتياطي
        two_factor_auth.generate_backup_codes()
        
        # حفظ المصادقة الثنائية
        self.db_manager.save_two_factor_auth(two_factor_auth)
        
        # إنشاء رمز QR للتطبيق
        qr_code = None
        if method == "app":
            totp = pyotp.TOTP(two_factor_auth.secret_key)
            uri = totp.provisioning_uri(user.email, issuer_name="Gaara ERP")
            
            # إنشاء رمز QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # تحويل الصورة إلى Base64
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return {
            "success": True,
            "two_factor_auth": {
                "method": two_factor_auth.method,
                "secret_key": two_factor_auth.secret_key,
                "backup_codes": two_factor_auth.backup_codes,
                "qr_code": qr_code
            }
        }
    
    def enable_two_factor(self, user_id: str, code: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """تفعيل المصادقة الثنائية"""
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        # الحصول على المصادقة الثنائية
        two_factor_auth = self.db_manager.get_two_factor_auth_by_user(user_id)
        if not two_factor_auth:
            return {
                "success": False,
                "message": "المصادقة الثنائية غير معدة"
            }
        
        # التحقق من أن المصادقة الثنائية غير مفعلة
        if two_factor_auth.is_enabled:
            return {
                "success": False,
                "message": "المصادقة الثنائية مفعلة بالفعل"
            }
        
        # التحقق من الرمز
        if two_factor_auth.method == "app":
            # التحقق من رمز التطبيق
            totp = pyotp.TOTP(two_factor_auth.secret_key)
            if not totp.verify(code):
                return {
                    "success": False,
                    "message": "رمز التحقق غير صحيح"
                }
        
        # تفعيل المصادقة الثنائية
        two_factor_auth.is_enabled = True
        two_factor_auth.enabled_at = datetime.now()
        two_factor_auth.last_verified_at = datetime.now()
        
        # حفظ التغييرات
        self.db_manager.update_two_factor_auth(two_factor_auth)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user_id, "two_factor_enable", "user", user_id,
            ip_address, user_agent, {"method": two_factor_auth.method}
        )
        
        return {
            "success": True,
            "message": "تم تفعيل المصادقة الثنائية بنجاح"
        }
    
    def disable_two_factor(self, user_id: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """تعطيل المصادقة الثنائية"""
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        # الحصول على المصادقة الثنائية
        two_factor_auth = self.db_manager.get_two_factor_auth_by_user(user_id)
        if not two_factor_auth:
            return {
                "success": False,
                "message": "المصادقة الثنائية غير معدة"
            }
        
        # التحقق من أن المصادقة الثنائية مفعلة
        if not two_factor_auth.is_enabled:
            return {
                "success": False,
                "message": "المصادقة الثنائية غير مفعلة"
            }
        
        # تعطيل المصادقة الثنائية
        two_factor_auth.is_enabled = False
        
        # حفظ التغييرات
        self.db_manager.update_two_factor_auth(two_factor_auth)
        
        # إنشاء سجل تدقيق الأمان
        self._create_security_audit(
            user_id, "two_factor_disable", "user", user_id,
            ip_address, user_agent, {"method": two_factor_auth.method}
        )
        
        return {
            "success": True,
            "message": "تم تعطيل المصادقة الثنائية بنجاح"
        }
    
    def _hash_password(self, password: str) -> str:
        """تشفير كلمة المرور"""
        # استخدام خوارزمية تشفير قوية
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def _verify_password(self, password: str, stored_password: str) -> bool:
        """التحقق من كلمة المرور"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def _create_access_token(self, user_id: str, ip_address: str = None, user_agent: str = None) -> AccessToken:
        """إنشاء رمز الوصول"""
        # إنشاء رمز الوصول
        access_token = AccessToken(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # حفظ رمز الوصول
        self.db_manager.save_access_token(access_token)
        
        return access_token
    
    def _create_security_audit(self, user_id: str, action: str, resource_type: str, resource_id: str, ip_address: str = None, user_agent: str = None, details: Dict[str, Any] = None) -> SecurityAudit:
        """إنشاء سجل تدقيق الأمان"""
        # إنشاء سجل تدقيق الأمان
        security_audit = SecurityAudit(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details or {}
        )
        
        # حفظ سجل تدقيق الأمان
        self.db_manager.save_security_audit(security_audit)
        
        return security_audit


class ApiKeyService:
    """خدمة إدارة مفاتيح API"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.permission_service = PermissionService(db_manager)
    
    def create_api_key(self, api_key_data: Dict[str, Any]) -> ApiKey:
        """إنشاء مفتاح API جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["name", "user_id"]
        for field in required_fields:
            if field not in api_key_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من وجود المستخدم
        user_id = api_key_data["user_id"]
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"المستخدم بالمعرف {user_id} غير موجود")
        
        # التحقق من الصلاحيات
        permissions = api_key_data.get("permissions", [])
        for permission_id in permissions:
            permission = self.permission_service.get_permission(permission_id)
            if not permission:
                raise ValueError(f"الصلاحية بالمعرف {permission_id} غير موجودة")
        
        # إنشاء كائن مفتاح API
        api_key = ApiKey(
            name=api_key_data["name"],
            user_id=user_id,
            permissions=permissions,
            expires_at=api_key_data.get("expires_at"),
            created_by=api_key_data.get("created_by"),
            is_active=api_key_data.get("is_active", True)
        )
        
        # حفظ مفتاح API في قاعدة البيانات
        self.db_manager.save_api_key(api_key)
        
        return api_key
    
    def get_all_api_keys(self, user_id: str = None, is_active: bool = None) -> List[ApiKey]:
        """الحصول على جميع مفاتيح API"""
        return self.db_manager.get_api_keys(user_id, is_active)
    
    def get_api_key(self, api_key_id: str) -> Optional[ApiKey]:
        """الحصول على مفتاح API بواسطة المعرف"""
        return self.db_manager.get_api_key_by_id(api_key_id)
    
    def get_api_key_by_key(self, key: str) -> Optional[ApiKey]:
        """الحصول على مفتاح API بواسطة المفتاح"""
        return self.db_manager.get_api_key_by_key(key)
    
    def update_api_key(self, api_key_id: str, api_key_data: Dict[str, Any]) -> Optional[ApiKey]:
        """تحديث مفتاح API"""
        # الحصول على مفتاح API
        api_key = self.get_api_key(api_key_id)
        if not api_key:
            return None
        
        # التحقق من الصلاحيات
        if "permissions" in api_key_data:
            permissions = api_key_data["permissions"]
            for permission_id in permissions:
                permission = self.permission_service.get_permission(permission_id)
                if not permission:
                    raise ValueError(f"الصلاحية بالمعرف {permission_id} غير موجودة")
            api_key.permissions = permissions
        
        # تحديث البيانات
        if "name" in api_key_data:
            api_key.name = api_key_data["name"]
        if "expires_at" in api_key_data:
            api_key.expires_at = api_key_data["expires_at"]
        if "is_active" in api_key_data:
            api_key.is_active = api_key_data["is_active"]
        
        # حفظ التغييرات
        self.db_manager.update_api_key(api_key)
        
        return api_key
    
    def delete_api_key(self, api_key_id: str) -> bool:
        """حذف مفتاح API"""
        return self.db_manager.delete_api_key(api_key_id)
    
    def verify_api_key(self, key: str, ip_address: str = None) -> Dict[str, Any]:
        """التحقق من مفتاح API"""
        # الحصول على مفتاح API
        api_key = self.get_api_key_by_key(key)
        if not api_key:
            return {
                "success": False,
                "message": "مفتاح API غير صالح"
            }
        
        # التحقق من أن المفتاح نشط
        if not api_key.is_active:
            return {
                "success": False,
                "message": "مفتاح API غير نشط"
            }
        
        # التحقق من تاريخ انتهاء المفتاح
        if api_key.is_expired():
            return {
                "success": False,
                "message": "مفتاح API منتهي الصلاحية"
            }
        
        # الحصول على المستخدم
        user = self.db_manager.get_user_by_id(api_key.user_id)
        if not user:
            return {
                "success": False,
                "message": "المستخدم غير موجود"
            }
        
        # التحقق من أن المستخدم نشط
        if not user.is_active:
            return {
                "success": False,
                "message": "الحساب غير نشط"
            }
        
        # تحديث آخر استخدام للمفتاح
        api_key.last_used_at = datetime.now()
        api_key.last_ip_address = ip_address
        self.db_manager.update_api_key(api_key)
        
        return {
            "success": True,
            "user": user.to_dict(),
            "permissions": api_key.permissions
        }
    
    def regenerate_api_key(self, api_key_id: str) -> Optional[ApiKey]:
        """إعادة توليد مفتاح API"""
        # الحصول على مفتاح API
        api_key = self.get_api_key(api_key_id)
        if not api_key:
            return None
        
        # إعادة توليد المفتاح
        api_key.key = api_key._generate_key()
        
        # حفظ التغييرات
        self.db_manager.update_api_key(api_key)
        
        return api_key


class SecurityPolicyService:
    """خدمة إدارة سياسات الأمان"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def create_security_policy(self, policy_data: Dict[str, Any]) -> SecurityPolicy:
        """إنشاء سياسة أمان جديدة"""
        # التحقق من البيانات المطلوبة
        required_fields = ["name"]
        for field in required_fields:
            if field not in policy_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # إنشاء كائن سياسة الأمان
        security_policy = SecurityPolicy(
            name=policy_data["name"],
            description=policy_data.get("description"),
            password_min_length=policy_data.get("password_min_length", 8),
            password_require_uppercase=policy_data.get("password_require_uppercase", True),
            password_require_lowercase=policy_data.get("password_require_lowercase", True),
            password_require_numbers=policy_data.get("password_require_numbers", True),
            password_require_special_chars=policy_data.get("password_require_special_chars", True),
            password_expiry_days=policy_data.get("password_expiry_days", 90),
            max_login_attempts=policy_data.get("max_login_attempts", 5),
            lockout_duration_minutes=policy_data.get("lockout_duration_minutes", 30),
            session_timeout_minutes=policy_data.get("session_timeout_minutes", 60),
            is_default=policy_data.get("is_default", False),
            is_active=policy_data.get("is_active", True),
            created_by=policy_data.get("created_by"),
            updated_by=policy_data.get("updated_by")
        )
        
        # إذا كانت السياسة الافتراضية، تعطيل السياسات الافتراضية الأخرى
        if security_policy.is_default:
            self.db_manager.disable_default_security_policies()
        
        # حفظ سياسة الأمان في قاعدة البيانات
        self.db_manager.save_security_policy(security_policy)
        
        return security_policy
    
    def get_all_security_policies(self, is_active: bool = None) -> List[SecurityPolicy]:
        """الحصول على جميع سياسات الأمان"""
        return self.db_manager.get_security_policies(is_active)
    
    def get_security_policy(self, policy_id: str) -> Optional[SecurityPolicy]:
        """الحصول على سياسة أمان بواسطة المعرف"""
        return self.db_manager.get_security_policy_by_id(policy_id)
    
    def get_default_security_policy(self) -> Optional[SecurityPolicy]:
        """الحصول على سياسة الأمان الافتراضية"""
        return self.db_manager.get_default_security_policy()
    
    def update_security_policy(self, policy_id: str, policy_data: Dict[str, Any]) -> Optional[SecurityPolicy]:
        """تحديث سياسة أمان"""
        # الحصول على سياسة الأمان
        security_policy = self.get_security_policy(policy_id)
        if not security_policy:
            return None
        
        # تحديث البيانات
        if "name" in policy_data:
            security_policy.name = policy_data["name"]
        if "description" in policy_data:
            security_policy.description = policy_data["description"]
        if "password_min_length" in policy_data:
            security_policy.password_min_length = policy_data["password_min_length"]
        if "password_require_uppercase" in policy_data:
            security_policy.password_require_uppercase = policy_data["password_require_uppercase"]
        if "password_require_lowercase" in policy_data:
            security_policy.password_require_lowercase = policy_data["password_require_lowercase"]
        if "password_require_numbers" in policy_data:
            security_policy.password_require_numbers = policy_data["password_require_numbers"]
        if "password_require_special_chars" in policy_data:
            security_policy.password_require_special_chars = policy_data["password_require_special_chars"]
        if "password_expiry_days" in policy_data:
            security_policy.password_expiry_days = policy_data["password_expiry_days"]
        if "max_login_attempts" in policy_data:
            security_policy.max_login_attempts = policy_data["max_login_attempts"]
        if "lockout_duration_minutes" in policy_data:
            security_policy.lockout_duration_minutes = policy_data["lockout_duration_minutes"]
        if "session_timeout_minutes" in policy_data:
            security_policy.session_timeout_minutes = policy_data["session_timeout_minutes"]
        if "is_active" in policy_data:
            security_policy.is_active = policy_data["is_active"]
        if "updated_by" in policy_data:
            security_policy.updated_by = policy_data["updated_by"]
        
        # إذا كانت السياسة الافتراضية، تعطيل السياسات الافتراضية الأخرى
        if "is_default" in policy_data and policy_data["is_default"] and not security_policy.is_default:
            security_policy.is_default = True
            self.db_manager.disable_default_security_policies()
        
        # تحديث وقت التحديث
        security_policy.updated_at = datetime.now()
        
        # حفظ التغييرات
        self.db_manager.update_security_policy(security_policy)
        
        return security_policy
    
    def delete_security_policy(self, policy_id: str) -> bool:
        """حذف سياسة أمان"""
        # الحصول على سياسة الأمان
        security_policy = self.get_security_policy(policy_id)
        if not security_policy:
            return False
        
        # التحقق من أن السياسة ليست الافتراضية
        if security_policy.is_default:
            raise ValueError("لا يمكن حذف سياسة الأمان الافتراضية")
        
        return self.db_manager.delete_security_policy(policy_id)
    
    def set_default_security_policy(self, policy_id: str) -> Optional[SecurityPolicy]:
        """تعيين سياسة أمان كافتراضية"""
        # الحصول على سياسة الأمان
        security_policy = self.get_security_policy(policy_id)
        if not security_policy:
            return None
        
        # التحقق من أن السياسة نشطة
        if not security_policy.is_active:
            raise ValueError("لا يمكن تعيين سياسة أمان غير نشطة كافتراضية")
        
        # تعطيل السياسات الافتراضية الأخرى
        self.db_manager.disable_default_security_policies()
        
        # تعيين السياسة كافتراضية
        security_policy.is_default = True
        security_policy.updated_at = datetime.now()
        
        # حفظ التغييرات
        self.db_manager.update_security_policy(security_policy)
        
        return security_policy


class SecurityAuditService:
    """خدمة إدارة سجلات تدقيق الأمان"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def create_security_audit(self, audit_data: Dict[str, Any]) -> SecurityAudit:
        """إنشاء سجل تدقيق أمان جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["user_id", "action", "resource_type", "resource_id"]
        for field in required_fields:
            if field not in audit_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # إنشاء كائن سجل تدقيق الأمان
        security_audit = SecurityAudit(
            user_id=audit_data["user_id"],
            action=audit_data["action"],
            resource_type=audit_data["resource_type"],
            resource_id=audit_data["resource_id"],
            ip_address=audit_data.get("ip_address"),
            user_agent=audit_data.get("user_agent"),
            details=audit_data.get("details", {})
        )
        
        # حفظ سجل تدقيق الأمان في قاعدة البيانات
        self.db_manager.save_security_audit(security_audit)
        
        return security_audit
    
    def get_security_audits(
        self,
        user_id: str = None,
        action: str = None,
        resource_type: str = None,
        resource_id: str = None,
        ip_address: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[SecurityAudit], int]:
        """الحصول على سجلات تدقيق الأمان"""
        return self.db_manager.get_security_audits(
            user_id, action, resource_type, resource_id,
            ip_address, start_date, end_date, limit, offset
        )
    
    def get_security_audit(self, audit_id: str) -> Optional[SecurityAudit]:
        """الحصول على سجل تدقيق أمان بواسطة المعرف"""
        return self.db_manager.get_security_audit_by_id(audit_id)
    
    def delete_security_audits_older_than(self, days: int) -> int:
        """حذف سجلات تدقيق الأمان الأقدم من عدد معين من الأيام"""
        # التحقق من عدد الأيام
        if days < 1:
            raise ValueError("يجب أن يكون عدد الأيام أكبر من صفر")
        
        # حساب التاريخ
        date = datetime.now() - timedelta(days=days)
        
        # حذف السجلات
        return self.db_manager.delete_security_audits_older_than(date)
