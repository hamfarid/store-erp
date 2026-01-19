# File: /home/ubuntu/clean_project/src/permissions_service.py
"""
مسار الملف: /home/ubuntu/clean_project/src/permissions_service.py

خدمة إدارة الصلاحيات والأمان
تتضمن نظام صلاحيات متقدم، تشفير البيانات، وحماية من الهجمات
"""

from enum import Enum
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import secrets
import json
import logging
from functools import wraps

class PermissionType(Enum):
    """أنواع الصلاحيات"""
    READ = "read"                    # قراءة
    WRITE = "write"                  # كتابة/تعديل
    DELETE = "delete"                # حذف
    ADMIN = "admin"                  # إدارة
    APPROVE = "approve"              # موافقة
    VIEW_SUMMARY = "view_summary"    # اطلاع بدون تفاصيل

class ResourceType(Enum):
    """أنواع الموارد"""
    DIAGNOSIS = "diagnosis"
    USER_MANAGEMENT = "user_management"
    AI_MANAGEMENT = "ai_management"
    SYSTEM_SETTINGS = "system_settings"
    REPORTS = "reports"
    ACTIVITY_LOG = "activity_log"
    FILE_MANAGEMENT = "file_management"
    DATABASE = "database"

@dataclass
class Permission:
    """صلاحية واحدة"""
    resource: ResourceType
    permission_type: PermissionType
    granted_by: int  # معرف المستخدم الذي منح الصلاحية
    granted_at: datetime
    expires_at: Optional[datetime] = None
    conditions: Optional[Dict[str, Any]] = None  # شروط إضافية

@dataclass
class Role:
    """دور مستخدم"""
    id: int
    name: str
    description: str
    permissions: List[Permission]
    is_system_role: bool = False  # أدوار النظام لا يمكن حذفها
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class SecurityEvent:
    """حدث أمني"""
    timestamp: datetime
    user_id: Optional[int]
    event_type: str
    description: str
    ip_address: str
    user_agent: str
    severity: str  # low, medium, high, critical
    additional_data: Optional[Dict[str, Any]] = None

class PermissionsService:
    """خدمة إدارة الصلاحيات"""
    
    def __init__(self):
        self.user_permissions: Dict[int, Set[Permission]] = {}
        self.user_roles: Dict[int, Set[int]] = {}  # user_id -> role_ids
        self.roles: Dict[int, Role] = {}
        self.security_events: List[SecurityEvent] = []
        self.failed_login_attempts: Dict[str, List[datetime]] = {}
        self.blocked_ips: Set[str] = set()
        self.session_tokens: Dict[str, Dict[str, Any]] = {}
        
        self.setup_default_roles()
        self.setup_logging()
    
    def setup_logging(self):
        """إعداد نظام السجلات الأمنية"""
        self.security_logger = logging.getLogger('security')
        handler = logging.FileHandler('security.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.security_logger.addHandler(handler)
        self.security_logger.setLevel(logging.INFO)
    
    def setup_default_roles(self):
        """إعداد الأدوار الافتراضية"""
        # دور المسؤول العام
        admin_permissions = []
        for resource in ResourceType:
            for permission_type in PermissionType:
                admin_permissions.append(Permission(
                    resource=resource,
                    permission_type=permission_type,
                    granted_by=0,  # النظام
                    granted_at=datetime.now()
                ))
        
        admin_role = Role(
            id=1,
            name="مسؤول النظام",
            description="صلاحيات كاملة على جميع أجزاء النظام",
            permissions=admin_permissions,
            is_system_role=True,
            created_at=datetime.now()
        )
        
        # دور المستخدم العادي
        user_permissions = [
            Permission(ResourceType.DIAGNOSIS, PermissionType.READ, 0, datetime.now()),
            Permission(ResourceType.DIAGNOSIS, PermissionType.WRITE, 0, datetime.now()),
            Permission(ResourceType.REPORTS, PermissionType.VIEW_SUMMARY, 0, datetime.now()),
            Permission(ResourceType.ACTIVITY_LOG, PermissionType.READ, 0, datetime.now()),
        ]
        
        user_role = Role(
            id=2,
            name="مستخدم عادي",
            description="صلاحيات أساسية للاستخدام العادي",
            permissions=user_permissions,
            is_system_role=True,
            created_at=datetime.now()
        )
        
        # دور المحلل
        analyst_permissions = user_permissions + [
            Permission(ResourceType.REPORTS, PermissionType.READ, 0, datetime.now()),
            Permission(ResourceType.AI_MANAGEMENT, PermissionType.READ, 0, datetime.now()),
            Permission(ResourceType.ACTIVITY_LOG, PermissionType.READ, 0, datetime.now()),
        ]
        
        analyst_role = Role(
            id=3,
            name="محلل",
            description="صلاحيات التحليل والتقارير",
            permissions=analyst_permissions,
            is_system_role=True,
            created_at=datetime.now()
        )
        
        self.roles[1] = admin_role
        self.roles[2] = user_role
        self.roles[3] = analyst_role
    
    def assign_role_to_user(self, user_id: int, role_id: int, assigned_by: int) -> bool:
        """تعيين دور لمستخدم"""
        try:
            if role_id not in self.roles:
                raise ValueError(f"الدور {role_id} غير موجود")
            
            if user_id not in self.user_roles:
                self.user_roles[user_id] = set()
            
            self.user_roles[user_id].add(role_id)
            
            # تسجيل الحدث الأمني
            self.log_security_event(
                user_id=assigned_by,
                event_type="role_assigned",
                description=f"تم تعيين الدور {role_id} للمستخدم {user_id}",
                severity="medium"
            )
            
            return True
            
        except Exception as e:
            self.security_logger.error(f"فشل في تعيين الدور: {e}")
            return False
    
    def remove_role_from_user(self, user_id: int, role_id: int, removed_by: int) -> bool:
        """إزالة دور من مستخدم"""
        try:
            if user_id in self.user_roles and role_id in self.user_roles[user_id]:
                self.user_roles[user_id].remove(role_id)
                
                # تسجيل الحدث الأمني
                self.log_security_event(
                    user_id=removed_by,
                    event_type="role_removed",
                    description=f"تم إزالة الدور {role_id} من المستخدم {user_id}",
                    severity="medium"
                )
                
                return True
            return False
            
        except Exception as e:
            self.security_logger.error(f"فشل في إزالة الدور: {e}")
            return False
    
    def grant_permission(self, user_id: int, permission: Permission, granted_by: int) -> bool:
        """منح صلاحية مباشرة لمستخدم"""
        try:
            if user_id not in self.user_permissions:
                self.user_permissions[user_id] = set()
            
            permission.granted_by = granted_by
            permission.granted_at = datetime.now()
            
            self.user_permissions[user_id].add(permission)
            
            # تسجيل الحدث الأمني
            self.log_security_event(
                user_id=granted_by,
                event_type="permission_granted",
                description=f"تم منح صلاحية {permission.permission_type.value} على {permission.resource.value} للمستخدم {user_id}",
                severity="medium"
            )
            
            return True
            
        except Exception as e:
            self.security_logger.error(f"فشل في منح الصلاحية: {e}")
            return False
    
    def revoke_permission(self, user_id: int, resource: ResourceType, permission_type: PermissionType, revoked_by: int) -> bool:
        """إلغاء صلاحية من مستخدم"""
        try:
            if user_id not in self.user_permissions:
                return False
            
            # البحث عن الصلاحية وإزالتها
            permission_to_remove = None
            for perm in self.user_permissions[user_id]:
                if perm.resource == resource and perm.permission_type == permission_type:
                    permission_to_remove = perm
                    break
            
            if permission_to_remove:
                self.user_permissions[user_id].remove(permission_to_remove)
                
                # تسجيل الحدث الأمني
                self.log_security_event(
                    user_id=revoked_by,
                    event_type="permission_revoked",
                    description=f"تم إلغاء صلاحية {permission_type.value} على {resource.value} من المستخدم {user_id}",
                    severity="medium"
                )
                
                return True
            
            return False
            
        except Exception as e:
            self.security_logger.error(f"فشل في إلغاء الصلاحية: {e}")
            return False
    
    def check_permission(self, user_id: int, resource: ResourceType, permission_type: PermissionType, context: Optional[Dict[str, Any]] = None) -> bool:
        """فحص صلاحية مستخدم"""
        try:
            # فحص الصلاحيات المباشرة
            if user_id in self.user_permissions:
                for perm in self.user_permissions[user_id]:
                    if (perm.resource == resource and 
                        perm.permission_type == permission_type and
                        self.is_permission_valid(perm, context)):
                        return True
            
            # فحص الصلاحيات من الأدوار
            if user_id in self.user_roles:
                for role_id in self.user_roles[user_id]:
                    if role_id in self.roles:
                        role = self.roles[role_id]
                        for perm in role.permissions:
                            if (perm.resource == resource and 
                                perm.permission_type == permission_type and
                                self.is_permission_valid(perm, context)):
                                return True
            
            return False
            
        except Exception as e:
            self.security_logger.error(f"خطأ في فحص الصلاحية: {e}")
            return False
    
    def is_permission_valid(self, permission: Permission, context: Optional[Dict[str, Any]] = None) -> bool:
        """فحص صحة الصلاحية"""
        # فحص انتهاء الصلاحية
        if permission.expires_at and datetime.now() > permission.expires_at:
            return False
        
        # فحص الشروط الإضافية
        if permission.conditions and context:
            for condition_key, condition_value in permission.conditions.items():
                if condition_key not in context or context[condition_key] != condition_value:
                    return False
        
        return True
    
    def get_user_permissions(self, user_id: int) -> List[Permission]:
        """الحصول على جميع صلاحيات المستخدم"""
        all_permissions = []
        
        # الصلاحيات المباشرة
        if user_id in self.user_permissions:
            all_permissions.extend(self.user_permissions[user_id])
        
        # الصلاحيات من الأدوار
        if user_id in self.user_roles:
            for role_id in self.user_roles[user_id]:
                if role_id in self.roles:
                    all_permissions.extend(self.roles[role_id].permissions)
        
        return all_permissions
    
    def create_role(self, name: str, description: str, permissions: List[Permission], created_by: int) -> int:
        """إنشاء دور جديد"""
        try:
            role_id = max(self.roles.keys()) + 1 if self.roles else 1
            
            role = Role(
                id=role_id,
                name=name,
                description=description,
                permissions=permissions,
                is_system_role=False,
                created_at=datetime.now()
            )
            
            self.roles[role_id] = role
            
            # تسجيل الحدث الأمني
            self.log_security_event(
                user_id=created_by,
                event_type="role_created",
                description=f"تم إنشاء دور جديد: {name}",
                severity="medium"
            )
            
            return role_id
            
        except Exception as e:
            self.security_logger.error(f"فشل في إنشاء الدور: {e}")
            raise
    
    def delete_role(self, role_id: int, deleted_by: int) -> bool:
        """حذف دور"""
        try:
            if role_id not in self.roles:
                return False
            
            role = self.roles[role_id]
            
            # منع حذف أدوار النظام
            if role.is_system_role:
                raise ValueError("لا يمكن حذف أدوار النظام")
            
            # إزالة الدور من جميع المستخدمين
            for user_id in self.user_roles:
                if role_id in self.user_roles[user_id]:
                    self.user_roles[user_id].remove(role_id)
            
            # حذف الدور
            del self.roles[role_id]
            
            # تسجيل الحدث الأمني
            self.log_security_event(
                user_id=deleted_by,
                event_type="role_deleted",
                description=f"تم حذف الدور: {role.name}",
                severity="high"
            )
            
            return True
            
        except Exception as e:
            self.security_logger.error(f"فشل في حذف الدور: {e}")
            return False
    
    def log_security_event(self, event_type: str, description: str, severity: str = "low", 
                          user_id: Optional[int] = None, ip_address: str = "", 
                          user_agent: str = "", additional_data: Optional[Dict[str, Any]] = None):
        """تسجيل حدث أمني"""
        event = SecurityEvent(
            timestamp=datetime.now(),
            user_id=user_id,
            event_type=event_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            severity=severity,
            additional_data=additional_data
        )
        
        self.security_events.append(event)
        
        # تسجيل في ملف السجل
        log_message = f"[{severity.upper()}] {event_type}: {description}"
        if user_id:
            log_message += f" (User: {user_id})"
        if ip_address:
            log_message += f" (IP: {ip_address})"
        
        if severity == "critical":
            self.security_logger.critical(log_message)
        elif severity == "high":
            self.security_logger.error(log_message)
        elif severity == "medium":
            self.security_logger.warning(log_message)
        else:
            self.security_logger.info(log_message)
    
    def track_failed_login(self, identifier: str, ip_address: str) -> bool:
        """تتبع محاولات تسجيل الدخول الفاشلة"""
        now = datetime.now()
        
        # تنظيف المحاولات القديمة (أكثر من ساعة)
        cutoff_time = now - timedelta(hours=1)
        
        if identifier not in self.failed_login_attempts:
            self.failed_login_attempts[identifier] = []
        
        # إزالة المحاولات القديمة
        self.failed_login_attempts[identifier] = [
            attempt for attempt in self.failed_login_attempts[identifier]
            if attempt > cutoff_time
        ]
        
        # إضافة المحاولة الجديدة
        self.failed_login_attempts[identifier].append(now)
        
        # فحص عدد المحاولات
        attempt_count = len(self.failed_login_attempts[identifier])
        
        # حظر بعد 5 محاولات فاشلة
        if attempt_count >= 5:
            self.blocked_ips.add(ip_address)
            
            self.log_security_event(
                event_type="account_locked",
                description=f"تم حظر الحساب {identifier} بعد {attempt_count} محاولات فاشلة",
                severity="high",
                ip_address=ip_address
            )
            
            return True  # محظور
        
        return False  # غير محظور
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """فحص ما إذا كان IP محظور"""
        return ip_address in self.blocked_ips
    
    def unblock_ip(self, ip_address: str, unblocked_by: int):
        """إلغاء حظر IP"""
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            
            self.log_security_event(
                user_id=unblocked_by,
                event_type="ip_unblocked",
                description=f"تم إلغاء حظر IP: {ip_address}",
                severity="medium",
                ip_address=ip_address
            )
    
    def create_secure_session(self, user_id: int, ip_address: str, user_agent: str) -> str:
        """إنشاء جلسة آمنة"""
        session_token = secrets.token_urlsafe(32)
        
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "last_activity": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }
        
        self.session_tokens[session_token] = session_data
        
        self.log_security_event(
            user_id=user_id,
            event_type="session_created",
            description="تم إنشاء جلسة جديدة",
            severity="low",
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return session_token
    
    def validate_session(self, session_token: str, ip_address: str, user_agent: str) -> Optional[int]:
        """التحقق من صحة الجلسة"""
        if session_token not in self.session_tokens:
            return None
        
        session_data = self.session_tokens[session_token]
        
        # فحص انتهاء الصلاحية
        if datetime.now() > session_data["expires_at"]:
            del self.session_tokens[session_token]
            return None
        
        # فحص IP (اختياري - يمكن تعطيله للمستخدمين المتنقلين)
        # if session_data["ip_address"] != ip_address:
        #     return None
        
        # تحديث آخر نشاط
        session_data["last_activity"] = datetime.now()
        
        return session_data["user_id"]
    
    def invalidate_session(self, session_token: str, user_id: Optional[int] = None):
        """إلغاء الجلسة"""
        if session_token in self.session_tokens:
            session_data = self.session_tokens[session_token]
            del self.session_tokens[session_token]
            
            self.log_security_event(
                user_id=user_id or session_data.get("user_id"),
                event_type="session_invalidated",
                description="تم إلغاء الجلسة",
                severity="low"
            )
    
    def get_security_report(self, days: int = 7) -> Dict[str, Any]:
        """إنشاء تقرير أمني"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        recent_events = [
            event for event in self.security_events
            if event.timestamp > cutoff_time
        ]
        
        # تجميع الأحداث حسب النوع
        events_by_type = {}
        events_by_severity = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        for event in recent_events:
            if event.event_type not in events_by_type:
                events_by_type[event.event_type] = 0
            events_by_type[event.event_type] += 1
            events_by_severity[event.severity] += 1
        
        return {
            "period": f"آخر {days} أيام",
            "total_events": len(recent_events),
            "events_by_type": events_by_type,
            "events_by_severity": events_by_severity,
            "blocked_ips_count": len(self.blocked_ips),
            "active_sessions": len(self.session_tokens),
            "failed_login_attempts": len(self.failed_login_attempts)
        }

# مثيل عام للخدمة
permissions_service = PermissionsService()

def require_permission(resource: ResourceType, permission_type: PermissionType):
    """ديكوريتر للتحقق من الصلاحيات"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # استخراج معرف المستخدم من السياق
            # يجب تطبيق هذا حسب إطار العمل المستخدم
            user_id = kwargs.get('current_user_id') or getattr(func, 'current_user_id', None)
            
            if not user_id:
                raise PermissionError("معرف المستخدم مطلوب")
            
            if not permissions_service.check_permission(user_id, resource, permission_type):
                raise PermissionError(f"ليس لديك صلاحية {permission_type.value} على {resource.value}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    # اختبار الخدمة
    print("بدء اختبار خدمة الصلاحيات...")
    
    # تعيين دور لمستخدم
    permissions_service.assign_role_to_user(1, 2, 0)  # تعيين دور مستخدم عادي
    
    # فحص صلاحية
    has_permission = permissions_service.check_permission(1, ResourceType.DIAGNOSIS, PermissionType.READ)
    print(f"صلاحية القراءة للتشخيص: {has_permission}")
    
    # إنشاء تقرير أمني
    report = permissions_service.get_security_report()
    print(f"التقرير الأمني: {json.dumps(report, ensure_ascii=False, indent=2)}")
    
    print("انتهى اختبار خدمة الصلاحيات")

