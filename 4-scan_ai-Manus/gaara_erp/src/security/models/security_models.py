"""
نماذج بيانات وحدة الأمان
يحتوي هذا الملف على نماذج البيانات المتعلقة بالأمان والوصول
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
import hashlib
import secrets
import re


class PermissionScope(str, Enum):
    """نطاق الصلاحية"""
    SYSTEM = "system"  # صلاحية على مستوى النظام
    COUNTRY = "country"  # صلاحية على مستوى الدولة
    COMPANY = "company"  # صلاحية على مستوى الشركة
    BRANCH = "branch"  # صلاحية على مستوى الفرع


class Permission:
    """نموذج الصلاحية"""
    
    def __init__(
        self,
        id: str = None,
        name: str = None,
        code: str = None,
        description: str = None,
        module: str = None,
        scope: PermissionScope = PermissionScope.SYSTEM,
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.code = code
        self.description = description
        self.module = module
        self.scope = scope
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "module": self.module,
            "scope": self.scope,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Permission':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description"),
            module=data.get("module"),
            scope=data.get("scope", PermissionScope.SYSTEM),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class Role:
    """نموذج الدور"""
    
    def __init__(
        self,
        id: str = None,
        name: str = None,
        description: str = None,
        permissions: List[str] = None,
        is_system_role: bool = False,
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None,
        created_by: str = None,
        updated_by: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.permissions = permissions or []
        self.is_system_role = is_system_role
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.created_by = created_by
        self.updated_by = updated_by
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
            "is_system_role": self.is_system_role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Role':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            permissions=data.get("permissions", []),
            is_system_role=data.get("is_system_role", False),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            created_by=data.get("created_by"),
            updated_by=data.get("updated_by")
        )


class UserPermission:
    """نموذج صلاحية المستخدم"""
    
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        permission_id: str = None,
        country_id: str = None,
        company_id: str = None,
        branch_id: str = None,
        granted_at: datetime = None,
        granted_by: str = None,
        expires_at: datetime = None,
        is_active: bool = True
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.permission_id = permission_id
        self.country_id = country_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.granted_at = granted_at or datetime.now()
        self.granted_by = granted_by
        self.expires_at = expires_at
        self.is_active = is_active
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "permission_id": self.permission_id,
            "country_id": self.country_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "granted_at": self.granted_at.isoformat(),
            "granted_by": self.granted_by,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPermission':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            permission_id=data.get("permission_id"),
            country_id=data.get("country_id"),
            company_id=data.get("company_id"),
            branch_id=data.get("branch_id"),
            granted_at=data.get("granted_at"),
            granted_by=data.get("granted_by"),
            expires_at=data.get("expires_at"),
            is_active=data.get("is_active", True)
        )


class UserRole:
    """نموذج دور المستخدم"""
    
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        role_id: str = None,
        country_id: str = None,
        company_id: str = None,
        branch_id: str = None,
        granted_at: datetime = None,
        granted_by: str = None,
        expires_at: datetime = None,
        is_active: bool = True
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.role_id = role_id
        self.country_id = country_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.granted_at = granted_at or datetime.now()
        self.granted_by = granted_by
        self.expires_at = expires_at
        self.is_active = is_active
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id,
            "country_id": self.country_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "granted_at": self.granted_at.isoformat(),
            "granted_by": self.granted_by,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserRole':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            role_id=data.get("role_id"),
            country_id=data.get("country_id"),
            company_id=data.get("company_id"),
            branch_id=data.get("branch_id"),
            granted_at=data.get("granted_at"),
            granted_by=data.get("granted_by"),
            expires_at=data.get("expires_at"),
            is_active=data.get("is_active", True)
        )


class AccessToken:
    """نموذج رمز الوصول"""
    
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        token: str = None,
        refresh_token: str = None,
        expires_at: datetime = None,
        created_at: datetime = None,
        ip_address: str = None,
        user_agent: str = None,
        is_revoked: bool = False
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.token = token or self._generate_token()
        self.refresh_token = refresh_token or self._generate_token()
        self.expires_at = expires_at or (datetime.now() + timedelta(hours=24))
        self.created_at = created_at or datetime.now()
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.is_revoked = is_revoked
    
    def _generate_token(self) -> str:
        """توليد رمز عشوائي"""
        return secrets.token_hex(32)
    
    def is_expired(self) -> bool:
        """التحقق مما إذا كان الرمز منتهي الصلاحية"""
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "is_revoked": self.is_revoked
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AccessToken':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            token=data.get("token"),
            refresh_token=data.get("refresh_token"),
            expires_at=data.get("expires_at"),
            created_at=data.get("created_at"),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            is_revoked=data.get("is_revoked", False)
        )


class LoginAttempt:
    """نموذج محاولة تسجيل الدخول"""
    
    def __init__(
        self,
        id: str = None,
        username: str = None,
        ip_address: str = None,
        user_agent: str = None,
        success: bool = False,
        failure_reason: str = None,
        attempted_at: datetime = None
    ):
        self.id = id or str(uuid.uuid4())
        self.username = username
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.success = success
        self.failure_reason = failure_reason
        self.attempted_at = attempted_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "username": self.username,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "success": self.success,
            "failure_reason": self.failure_reason,
            "attempted_at": self.attempted_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LoginAttempt':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            username=data.get("username"),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            success=data.get("success", False),
            failure_reason=data.get("failure_reason"),
            attempted_at=data.get("attempted_at")
        )


class PasswordReset:
    """نموذج إعادة تعيين كلمة المرور"""
    
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        token: str = None,
        expires_at: datetime = None,
        created_at: datetime = None,
        is_used: bool = False,
        used_at: datetime = None,
        ip_address: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.token = token or self._generate_token()
        self.expires_at = expires_at or (datetime.now() + timedelta(hours=24))
        self.created_at = created_at or datetime.now()
        self.is_used = is_used
        self.used_at = used_at
        self.ip_address = ip_address
    
    def _generate_token(self) -> str:
        """توليد رمز عشوائي"""
        return secrets.token_hex(16)
    
    def is_expired(self) -> bool:
        """التحقق مما إذا كان الرمز منتهي الصلاحية"""
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "is_used": self.is_used,
            "used_at": self.used_at.isoformat() if self.used_at else None,
            "ip_address": self.ip_address
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PasswordReset':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            token=data.get("token"),
            expires_at=data.get("expires_at"),
            created_at=data.get("created_at"),
            is_used=data.get("is_used", False),
            used_at=data.get("used_at"),
            ip_address=data.get("ip_address")
        )


class SecurityPolicy:
    """نموذج سياسة الأمان"""
    
    def __init__(
        self,
        id: str = None,
        name: str = None,
        description: str = None,
        password_min_length: int = 8,
        password_require_uppercase: bool = True,
        password_require_lowercase: bool = True,
        password_require_numbers: bool = True,
        password_require_special_chars: bool = True,
        password_expiry_days: int = 90,
        max_login_attempts: int = 5,
        lockout_duration_minutes: int = 30,
        session_timeout_minutes: int = 60,
        is_default: bool = False,
        is_active: bool = True,
        created_at: datetime = None,
        updated_at: datetime = None,
        created_by: str = None,
        updated_by: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.password_min_length = password_min_length
        self.password_require_uppercase = password_require_uppercase
        self.password_require_lowercase = password_require_lowercase
        self.password_require_numbers = password_require_numbers
        self.password_require_special_chars = password_require_special_chars
        self.password_expiry_days = password_expiry_days
        self.max_login_attempts = max_login_attempts
        self.lockout_duration_minutes = lockout_duration_minutes
        self.session_timeout_minutes = session_timeout_minutes
        self.is_default = is_default
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.created_by = created_by
        self.updated_by = updated_by
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """التحقق من صحة كلمة المرور"""
        is_valid = True
        errors = []
        
        # التحقق من الطول
        if len(password) < self.password_min_length:
            is_valid = False
            errors.append(f"يجب أن تكون كلمة المرور {self.password_min_length} أحرف على الأقل")
        
        # التحقق من وجود حرف كبير
        if self.password_require_uppercase and not re.search(r'[A-Z]', password):
            is_valid = False
            errors.append("يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل")
        
        # التحقق من وجود حرف صغير
        if self.password_require_lowercase and not re.search(r'[a-z]', password):
            is_valid = False
            errors.append("يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل")
        
        # التحقق من وجود رقم
        if self.password_require_numbers and not re.search(r'[0-9]', password):
            is_valid = False
            errors.append("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل")
        
        # التحقق من وجود حرف خاص
        if self.password_require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            is_valid = False
            errors.append("يجب أن تحتوي كلمة المرور على حرف خاص واحد على الأقل")
        
        return {
            "is_valid": is_valid,
            "errors": errors
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "password_min_length": self.password_min_length,
            "password_require_uppercase": self.password_require_uppercase,
            "password_require_lowercase": self.password_require_lowercase,
            "password_require_numbers": self.password_require_numbers,
            "password_require_special_chars": self.password_require_special_chars,
            "password_expiry_days": self.password_expiry_days,
            "max_login_attempts": self.max_login_attempts,
            "lockout_duration_minutes": self.lockout_duration_minutes,
            "session_timeout_minutes": self.session_timeout_minutes,
            "is_default": self.is_default,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecurityPolicy':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            password_min_length=data.get("password_min_length", 8),
            password_require_uppercase=data.get("password_require_uppercase", True),
            password_require_lowercase=data.get("password_require_lowercase", True),
            password_require_numbers=data.get("password_require_numbers", True),
            password_require_special_chars=data.get("password_require_special_chars", True),
            password_expiry_days=data.get("password_expiry_days", 90),
            max_login_attempts=data.get("max_login_attempts", 5),
            lockout_duration_minutes=data.get("lockout_duration_minutes", 30),
            session_timeout_minutes=data.get("session_timeout_minutes", 60),
            is_default=data.get("is_default", False),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            created_by=data.get("created_by"),
            updated_by=data.get("updated_by")
        )


class ApiKey:
    """نموذج مفتاح API"""
    
    def __init__(
        self,
        id: str = None,
        name: str = None,
        key: str = None,
        user_id: str = None,
        permissions: List[str] = None,
        expires_at: datetime = None,
        created_at: datetime = None,
        created_by: str = None,
        is_active: bool = True,
        last_used_at: datetime = None,
        last_ip_address: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.key = key or self._generate_key()
        self.user_id = user_id
        self.permissions = permissions or []
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now()
        self.created_by = created_by
        self.is_active = is_active
        self.last_used_at = last_used_at
        self.last_ip_address = last_ip_address
    
    def _generate_key(self) -> str:
        """توليد مفتاح API عشوائي"""
        prefix = "gra_"
        random_part = secrets.token_hex(16)
        return f"{prefix}{random_part}"
    
    def is_expired(self) -> bool:
        """التحقق مما إذا كان المفتاح منتهي الصلاحية"""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "key": self.key,
            "user_id": self.user_id,
            "permissions": self.permissions,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "is_active": self.is_active,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "last_ip_address": self.last_ip_address
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApiKey':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            key=data.get("key"),
            user_id=data.get("user_id"),
            permissions=data.get("permissions", []),
            expires_at=data.get("expires_at"),
            created_at=data.get("created_at"),
            created_by=data.get("created_by"),
            is_active=data.get("is_active", True),
            last_used_at=data.get("last_used_at"),
            last_ip_address=data.get("last_ip_address")
        )


class TwoFactorAuth:
    """نموذج المصادقة الثنائية"""
    
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        method: str = None,  # "app", "sms", "email"
        secret_key: str = None,
        backup_codes: List[str] = None,
        is_enabled: bool = False,
        enabled_at: datetime = None,
        last_verified_at: datetime = None
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.method = method
        self.secret_key = secret_key
        self.backup_codes = backup_codes or []
        self.is_enabled = is_enabled
        self.enabled_at = enabled_at
        self.last_verified_at = last_verified_at
    
    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """توليد رموز النسخ الاحتياطي"""
        self.backup_codes = [secrets.token_hex(4).upper() for _ in range(count)]
        return self.backup_codes
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "method": self.method,
            "secret_key": self.secret_key,
            "backup_codes": self.backup_codes,
            "is_enabled": self.is_enabled,
            "enabled_at": self.enabled_at.isoformat() if self.enabled_at else None,
            "last_verified_at": self.last_verified_at.isoformat() if self.last_verified_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TwoFactorAuth':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            method=data.get("method"),
            secret_key=data.get("secret_key"),
            backup_codes=data.get("backup_codes", []),
            is_enabled=data.get("is_enabled", False),
            enabled_at=data.get("enabled_at"),
            last_verified_at=data.get("last_verified_at")
        )


class SecurityAudit:
    """نموذج تدقيق الأمان"""
    
    def __init__(
        self,
        id: str = None,
        user_id: str = None,
        action: str = None,
        resource_type: str = None,
        resource_id: str = None,
        ip_address: str = None,
        user_agent: str = None,
        details: Dict[str, Any] = None,
        timestamp: datetime = None
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.action = action
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.details = details or {}
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecurityAudit':
        """إنشاء كائن من قاموس"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            action=data.get("action"),
            resource_type=data.get("resource_type"),
            resource_id=data.get("resource_id"),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            details=data.get("details", {}),
            timestamp=data.get("timestamp")
        )
