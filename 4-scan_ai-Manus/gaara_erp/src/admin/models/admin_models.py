"""
نماذج بيانات وحدة الإدارة
يحتوي هذا الملف على تعريف نماذج البيانات الخاصة بوحدة الإدارة
"""

import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Union
from enum import Enum


class UserRole(str, Enum):
    """تعداد أدوار المستخدمين"""
    ADMIN = "admin"  # مدير النظام
    MANAGER = "manager"  # مدير
    SUPPORT_MANAGER = "support_manager"  # مدير الدعم والتطوير
    SUPPORT_ENGINEER = "support_engineer"  # مهندس دعم فني
    DEVELOPMENT_ENGINEER = "development_engineer"  # مهندس تطوير
    USER = "user"  # مستخدم عادي


class PermissionLevel(str, Enum):
    """تعداد مستويات الصلاحيات"""
    READ = "read"  # قراءة فقط
    WRITE = "write"  # قراءة وكتابة
    ADMIN = "admin"  # إدارة كاملة
    NONE = "none"  # بدون صلاحيات


class User:
    """نموذج بيانات المستخدم"""
    
    def __init__(
        self,
        user_id: str,
        username: str,
        email: str,
        password_hash: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        role: Union[UserRole, str] = UserRole.USER,
        is_active: bool = True,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        country_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None,
        permissions: Optional[Dict[str, Union[PermissionLevel, str]]] = None,
        supervisor_id: Optional[str] = None,
        employee_id: Optional[str] = None,
        profile_image: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None
    ):
        """
        تهيئة كائن المستخدم
        
        المعاملات:
            user_id: معرف المستخدم
            username: اسم المستخدم
            email: البريد الإلكتروني
            password_hash: تجزئة كلمة المرور
            first_name: الاسم الأول (اختياري)
            last_name: الاسم الأخير (اختياري)
            role: دور المستخدم (اختياري، افتراضي: USER)
            is_active: ما إذا كان المستخدم نشطًا (اختياري، افتراضي: True)
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            country_id: معرف الدولة (اختياري)
            created_at: تاريخ الإنشاء (اختياري)
            last_login: تاريخ آخر تسجيل دخول (اختياري)
            permissions: صلاحيات المستخدم (اختياري)
            supervisor_id: معرف المشرف (اختياري)
            employee_id: معرف الموظف (اختياري)
            profile_image: مسار صورة الملف الشخصي (اختياري)
            settings: إعدادات المستخدم (اختياري)
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role if isinstance(role, UserRole) else UserRole(role)
        self.is_active = is_active
        self.company_id = company_id
        self.branch_id = branch_id
        self.country_id = country_id
        self.created_at = created_at or datetime.now()
        self.last_login = last_login
        self.permissions = permissions or {}
        self.supervisor_id = supervisor_id
        self.employee_id = employee_id
        self.profile_image = profile_image
        self.settings = settings or {}
    
    @property
    def full_name(self) -> str:
        """الحصول على الاسم الكامل للمستخدم"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username
    
    def has_permission(self, permission_key: str, required_level: Union[PermissionLevel, str] = PermissionLevel.READ) -> bool:
        """
        التحقق مما إذا كان المستخدم لديه الصلاحية المطلوبة
        
        المعاملات:
            permission_key: مفتاح الصلاحية
            required_level: المستوى المطلوب (اختياري، افتراضي: READ)
            
        العائد:
            True إذا كان المستخدم لديه الصلاحية المطلوبة، False خلاف ذلك
        """
        # المدير لديه جميع الصلاحيات
        if self.role == UserRole.ADMIN:
            return True
        
        # التحقق من الصلاحية المحددة
        if permission_key in self.permissions:
            user_level = self.permissions[permission_key]
            user_level = user_level if isinstance(user_level, PermissionLevel) else PermissionLevel(user_level)
            required_level = required_level if isinstance(required_level, PermissionLevel) else PermissionLevel(required_level)
            
            # مستوى ADMIN يتضمن جميع الصلاحيات
            if user_level == PermissionLevel.ADMIN:
                return True
            
            # مستوى WRITE يتضمن صلاحيات READ
            if user_level == PermissionLevel.WRITE and required_level == PermissionLevel.READ:
                return True
            
            # التحقق من تطابق المستويات
            return user_level == required_level
        
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن المستخدم إلى قاموس
        
        العائد:
            قاموس يمثل المستخدم
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "role": self.role.value if isinstance(self.role, UserRole) else self.role,
            "is_active": self.is_active,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "country_id": self.country_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "permissions": {k: v.value if isinstance(v, PermissionLevel) else v for k, v in self.permissions.items()},
            "supervisor_id": self.supervisor_id,
            "employee_id": self.employee_id,
            "profile_image": self.profile_image,
            "settings": self.settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        إنشاء كائن مستخدم من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات المستخدم
            
        العائد:
            كائن المستخدم
        """
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        created_at = data.get('created_at')
        if created_at and isinstance(created_at, str):
            data['created_at'] = datetime.fromisoformat(created_at)
        
        last_login = data.get('last_login')
        if last_login and isinstance(last_login, str):
            data['last_login'] = datetime.fromisoformat(last_login)
        
        # حذف الحقول المحسوبة
        data.pop('full_name', None)
        
        return cls(**data)


class Country:
    """نموذج بيانات الدولة"""
    
    def __init__(
        self,
        country_id: str,
        name: str,
        code: str,
        currency: Optional[str] = None,
        currency_code: Optional[str] = None,
        flag_image: Optional[str] = None,
        is_active: bool = True
    ):
        """
        تهيئة كائن الدولة
        
        المعاملات:
            country_id: معرف الدولة
            name: اسم الدولة
            code: رمز الدولة
            currency: اسم العملة (اختياري)
            currency_code: رمز العملة (اختياري)
            flag_image: مسار صورة العلم (اختياري)
            is_active: ما إذا كانت الدولة نشطة (اختياري، افتراضي: True)
        """
        self.country_id = country_id
        self.name = name
        self.code = code
        self.currency = currency
        self.currency_code = currency_code
        self.flag_image = flag_image
        self.is_active = is_active
        self.companies: List[Company] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن الدولة إلى قاموس
        
        العائد:
            قاموس يمثل الدولة
        """
        return {
            "country_id": self.country_id,
            "name": self.name,
            "code": self.code,
            "currency": self.currency,
            "currency_code": self.currency_code,
            "flag_image": self.flag_image,
            "is_active": self.is_active,
            "companies": [company.to_dict() for company in self.companies] if hasattr(self, 'companies') else []
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Country':
        """
        إنشاء كائن دولة من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات الدولة
            
        العائد:
            كائن الدولة
        """
        # حذف الشركات من البيانات
        companies_data = data.pop('companies', [])
        
        # إنشاء كائن الدولة
        country = cls(**data)
        
        # إضافة الشركات إذا كانت موجودة
        if companies_data:
            from .company_models import Company
            country.companies = [Company.from_dict(company_data) for company_data in companies_data]
        
        return country


class Company:
    """نموذج بيانات الشركة"""
    
    def __init__(
        self,
        company_id: str,
        name: str,
        country_id: str,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        logo: Optional[str] = None,
        tax_number: Optional[str] = None,
        registration_number: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        """
        تهيئة كائن الشركة
        
        المعاملات:
            company_id: معرف الشركة
            name: اسم الشركة
            country_id: معرف الدولة
            address: العنوان (اختياري)
            phone: رقم الهاتف (اختياري)
            email: البريد الإلكتروني (اختياري)
            website: الموقع الإلكتروني (اختياري)
            logo: مسار شعار الشركة (اختياري)
            tax_number: الرقم الضريبي (اختياري)
            registration_number: رقم التسجيل (اختياري)
            is_active: ما إذا كانت الشركة نشطة (اختياري، افتراضي: True)
            created_at: تاريخ الإنشاء (اختياري)
        """
        self.company_id = company_id
        self.name = name
        self.country_id = country_id
        self.address = address
        self.phone = phone
        self.email = email
        self.website = website
        self.logo = logo
        self.tax_number = tax_number
        self.registration_number = registration_number
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.branches: List['Branch'] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن الشركة إلى قاموس
        
        العائد:
            قاموس يمثل الشركة
        """
        return {
            "company_id": self.company_id,
            "name": self.name,
            "country_id": self.country_id,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "logo": self.logo,
            "tax_number": self.tax_number,
            "registration_number": self.registration_number,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "branches": [branch.to_dict() for branch in self.branches] if hasattr(self, 'branches') else []
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Company':
        """
        إنشاء كائن شركة من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات الشركة
            
        العائد:
            كائن الشركة
        """
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        created_at = data.get('created_at')
        if created_at and isinstance(created_at, str):
            data['created_at'] = datetime.fromisoformat(created_at)
        
        # حذف الفروع من البيانات
        branches_data = data.pop('branches', [])
        
        # إنشاء كائن الشركة
        company = cls(**data)
        
        # إضافة الفروع إذا كانت موجودة
        if branches_data:
            company.branches = [Branch.from_dict(branch_data) for branch_data in branches_data]
        
        return company


class Branch:
    """نموذج بيانات فرع الشركة"""
    
    def __init__(
        self,
        branch_id: str,
        name: str,
        company_id: str,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        manager_id: Optional[str] = None,
        is_main_branch: bool = False,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        """
        تهيئة كائن فرع الشركة
        
        المعاملات:
            branch_id: معرف الفرع
            name: اسم الفرع
            company_id: معرف الشركة
            address: العنوان (اختياري)
            phone: رقم الهاتف (اختياري)
            email: البريد الإلكتروني (اختياري)
            manager_id: معرف المدير (اختياري)
            is_main_branch: ما إذا كان الفرع الرئيسي (اختياري، افتراضي: False)
            is_active: ما إذا كان الفرع نشطًا (اختياري، افتراضي: True)
            created_at: تاريخ الإنشاء (اختياري)
        """
        self.branch_id = branch_id
        self.name = name
        self.company_id = company_id
        self.address = address
        self.phone = phone
        self.email = email
        self.manager_id = manager_id
        self.is_main_branch = is_main_branch
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن فرع الشركة إلى قاموس
        
        العائد:
            قاموس يمثل فرع الشركة
        """
        return {
            "branch_id": self.branch_id,
            "name": self.name,
            "company_id": self.company_id,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "manager_id": self.manager_id,
            "is_main_branch": self.is_main_branch,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Branch':
        """
        إنشاء كائن فرع شركة من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات فرع الشركة
            
        العائد:
            كائن فرع الشركة
        """
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        created_at = data.get('created_at')
        if created_at and isinstance(created_at, str):
            data['created_at'] = datetime.fromisoformat(created_at)
        
        return cls(**data)


class SystemLog:
    """نموذج بيانات سجل النظام"""
    
    def __init__(
        self,
        log_id: str,
        action: str,
        user_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        module: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        status: Optional[str] = None,
        duration_ms: Optional[int] = None
    ):
        """
        تهيئة كائن سجل النظام
        
        المعاملات:
            log_id: معرف السجل
            action: الإجراء المتخذ
            user_id: معرف المستخدم (اختياري)
            timestamp: الطابع الزمني (اختياري)
            details: تفاصيل إضافية (اختياري)
            ip_address: عنوان IP (اختياري)
            module: الوحدة المتأثرة (اختياري)
            entity_type: نوع الكيان المتأثر (اختياري)
            entity_id: معرف الكيان المتأثر (اختياري)
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            status: حالة الإجراء (اختياري)
            duration_ms: مدة الإجراء بالميلي ثانية (اختياري)
        """
        self.log_id = log_id
        self.action = action
        self.user_id = user_id
        self.timestamp = timestamp or datetime.now()
        self.details = details or {}
        self.ip_address = ip_address
        self.module = module
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.status = status
        self.duration_ms = duration_ms
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن سجل النظام إلى قاموس
        
        العائد:
            قاموس يمثل سجل النظام
        """
        return {
            "log_id": self.log_id,
            "action": self.action,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "details": self.details,
            "ip_address": self.ip_address,
            "module": self.module,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "status": self.status,
            "duration_ms": self.duration_ms
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemLog':
        """
        إنشاء كائن سجل نظام من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات سجل النظام
            
        العائد:
            كائن سجل النظام
        """
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        timestamp = data.get('timestamp')
        if timestamp and isinstance(timestamp, str):
            data['timestamp'] = datetime.fromisoformat(timestamp)
        
        return cls(**data)


class SystemSetting:
    """نموذج بيانات إعدادات النظام"""
    
    def __init__(
        self,
        setting_id: str,
        key: str,
        value: Any,
        description: Optional[str] = None,
        category: Optional[str] = None,
        is_global: bool = True,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        data_type: Optional[str] = None,
        is_sensitive: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None
    ):
        """
        تهيئة كائن إعدادات النظام
        
        المعاملات:
            setting_id: معرف الإعداد
            key: مفتاح الإعداد
            value: قيمة الإعداد
            description: وصف الإعداد (اختياري)
            category: فئة الإعداد (اختياري)
            is_global: ما إذا كان الإعداد عامًا (اختياري، افتراضي: True)
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            data_type: نوع البيانات (اختياري)
            is_sensitive: ما إذا كان الإعداد حساسًا (اختياري، افتراضي: False)
            created_at: تاريخ الإنشاء (اختياري)
            updated_at: تاريخ التحديث (اختياري)
            created_by: معرف المستخدم الذي أنشأ الإعداد (اختياري)
            updated_by: معرف المستخدم الذي حدث الإعداد (اختياري)
        """
        self.setting_id = setting_id
        self.key = key
        self.value = value
        self.description = description
        self.category = category
        self.is_global = is_global
        self.company_id = company_id
        self.branch_id = branch_id
        self.data_type = data_type or self._infer_data_type(value)
        self.is_sensitive = is_sensitive
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or self.created_at
        self.created_by = created_by
        self.updated_by = updated_by
    
    def _infer_data_type(self, value: Any) -> str:
        """
        استنتاج نوع البيانات من القيمة
        
        المعاملات:
            value: القيمة
            
        العائد:
            نوع البيانات كسلسلة نصية
        """
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, dict):
            return "json"
        elif isinstance(value, list):
            return "array"
        else:
            return "string"
    
    def get_typed_value(self) -> Any:
        """
        الحصول على القيمة بالنوع المناسب
        
        العائد:
            القيمة بالنوع المناسب
        """
        if not self.data_type or not self.value:
            return self.value
        
        try:
            if self.data_type == "boolean":
                if isinstance(self.value, bool):
                    return self.value
                return self.value.lower() in ("true", "yes", "1", "t", "y")
            elif self.data_type == "integer":
                return int(self.value)
            elif self.data_type == "float":
                return float(self.value)
            elif self.data_type == "json":
                if isinstance(self.value, dict):
                    return self.value
                import json
                return json.loads(self.value)
            elif self.data_type == "array":
                if isinstance(self.value, list):
                    return self.value
                import json
                return json.loads(self.value)
            else:
                return str(self.value)
        except Exception:
            # إذا فشل التحويل، إرجاع القيمة الأصلية
            return self.value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن إعدادات النظام إلى قاموس
        
        العائد:
            قاموس يمثل إعدادات النظام
        """
        return {
            "setting_id": self.setting_id,
            "key": self.key,
            "value": self.value,
            "description": self.description,
            "category": self.category,
            "is_global": self.is_global,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "data_type": self.data_type,
            "is_sensitive": self.is_sensitive,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemSetting':
        """
        إنشاء كائن إعدادات نظام من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات إعدادات النظام
            
        العائد:
            كائن إعدادات النظام
        """
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        created_at = data.get('created_at')
        if created_at and isinstance(created_at, str):
            data['created_at'] = datetime.fromisoformat(created_at)
        
        updated_at = data.get('updated_at')
        if updated_at and isinstance(updated_at, str):
            data['updated_at'] = datetime.fromisoformat(updated_at)
        
        return cls(**data)


class ServerStatus:
    """نموذج بيانات حالة الخادم"""
    
    def __init__(
        self,
        status_id: str,
        timestamp: Optional[datetime] = None,
        cpu_usage: Optional[float] = None,
        memory_usage: Optional[float] = None,
        disk_usage: Optional[float] = None,
        active_users: Optional[int] = None,
        system_uptime: Optional[int] = None,
        database_size: Optional[float] = None,
        database_connections: Optional[int] = None,
        api_requests_count: Optional[int] = None,
        average_response_time: Optional[float] = None,
        error_count: Optional[int] = None,
        warning_count: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        تهيئة كائن حالة الخادم
        
        المعاملات:
            status_id: معرف الحالة
            timestamp: الطابع الزمني (اختياري)
            cpu_usage: استخدام وحدة المعالجة المركزية (%) (اختياري)
            memory_usage: استخدام الذاكرة (%) (اختياري)
            disk_usage: استخدام القرص (%) (اختياري)
            active_users: عدد المستخدمين النشطين (اختياري)
            system_uptime: وقت تشغيل النظام (بالثواني) (اختياري)
            database_size: حجم قاعدة البيانات (بالميجابايت) (اختياري)
            database_connections: عدد اتصالات قاعدة البيانات (اختياري)
            api_requests_count: عدد طلبات API (اختياري)
            average_response_time: متوسط وقت الاستجابة (بالميلي ثانية) (اختياري)
            error_count: عدد الأخطاء (اختياري)
            warning_count: عدد التحذيرات (اختياري)
            details: تفاصيل إضافية (اختياري)
        """
        self.status_id = status_id
        self.timestamp = timestamp or datetime.now()
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.disk_usage = disk_usage
        self.active_users = active_users
        self.system_uptime = system_uptime
        self.database_size = database_size
        self.database_connections = database_connections
        self.api_requests_count = api_requests_count
        self.average_response_time = average_response_time
        self.error_count = error_count
        self.warning_count = warning_count
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن حالة الخادم إلى قاموس
        
        العائد:
            قاموس يمثل حالة الخادم
        """
        return {
            "status_id": self.status_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "disk_usage": self.disk_usage,
            "active_users": self.active_users,
            "system_uptime": self.system_uptime,
            "database_size": self.database_size,
            "database_connections": self.database_connections,
            "api_requests_count": self.api_requests_count,
            "average_response_time": self.average_response_time,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServerStatus':
        """
        إنشاء كائن حالة خادم من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات حالة الخادم
            
        العائد:
            كائن حالة الخادم
        """
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        timestamp = data.get('timestamp')
        if timestamp and isinstance(timestamp, str):
            data['timestamp'] = datetime.fromisoformat(timestamp)
        
        return cls(**data)


class UserStatistics:
    """نموذج بيانات إحصائيات المستخدمين"""
    
    def __init__(
        self,
        stats_id: str,
        timestamp: Optional[datetime] = None,
        total_users: int = 0,
        active_users: int = 0,
        inactive_users: int = 0,
        daily_active_users: int = 0,
        weekly_active_users: int = 0,
        monthly_active_users: int = 0,
        yearly_active_users: int = 0,
        new_users_today: int = 0,
        new_users_this_week: int = 0,
        new_users_this_month: int = 0,
        new_users_this_year: int = 0,
        users_by_role: Optional[Dict[str, int]] = None,
        users_by_country: Optional[Dict[str, int]] = None,
        users_by_company: Optional[Dict[str, int]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        تهيئة كائن إحصائيات المستخدمين
        
        المعاملات:
            stats_id: معرف الإحصائيات
            timestamp: الطابع الزمني (اختياري)
            total_users: إجمالي عدد المستخدمين (اختياري)
            active_users: عدد المستخدمين النشطين (اختياري)
            inactive_users: عدد المستخدمين غير النشطين (اختياري)
            daily_active_users: عدد المستخدمين النشطين يوميًا (اختياري)
            weekly_active_users: عدد المستخدمين النشطين أسبوعيًا (اختياري)
            monthly_active_users: عدد المستخدمين النشطين شهريًا (اختياري)
            yearly_active_users: عدد المستخدمين النشطين سنويًا (اختياري)
            new_users_today: عدد المستخدمين الجدد اليوم (اختياري)
            new_users_this_week: عدد المستخدمين الجدد هذا الأسبوع (اختياري)
            new_users_this_month: عدد المستخدمين الجدد هذا الشهر (اختياري)
            new_users_this_year: عدد المستخدمين الجدد هذا العام (اختياري)
            users_by_role: عدد المستخدمين حسب الدور (اختياري)
            users_by_country: عدد المستخدمين حسب الدولة (اختياري)
            users_by_company: عدد المستخدمين حسب الشركة (اختياري)
            details: تفاصيل إضافية (اختياري)
        """
        self.stats_id = stats_id
        self.timestamp = timestamp or datetime.now()
        self.total_users = total_users
        self.active_users = active_users
        self.inactive_users = inactive_users
        self.daily_active_users = daily_active_users
        self.weekly_active_users = weekly_active_users
        self.monthly_active_users = monthly_active_users
        self.yearly_active_users = yearly_active_users
        self.new_users_today = new_users_today
        self.new_users_this_week = new_users_this_week
        self.new_users_this_month = new_users_this_month
        self.new_users_this_year = new_users_this_year
        self.users_by_role = users_by_role or {}
        self.users_by_country = users_by_country or {}
        self.users_by_company = users_by_company or {}
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن إحصائيات المستخدمين إلى قاموس
        
        العائد:
            قاموس يمثل إحصائيات المستخدمين
        """
        return {
            "stats_id": self.stats_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "total_users": self.total_users,
            "active_users": self.active_users,
            "inactive_users": self.inactive_users,
            "daily_active_users": self.daily_active_users,
            "weekly_active_users": self.weekly_active_users,
            "monthly_active_users": self.monthly_active_users,
            "yearly_active_users": self.yearly_active_users,
            "new_users_today": self.new_users_today,
            "new_users_this_week": self.new_users_this_week,
            "new_users_this_month": self.new_users_this_month,
            "new_users_this_year": self.new_users_this_year,
            "users_by_role": self.users_by_role,
            "users_by_country": self.users_by_country,
            "users_by_company": self.users_by_company,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserStatistics':
        """
        إنشاء كائن إحصائيات مستخدمين من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات إحصائيات المستخدمين
            
        العائد:
            كائن إحصائيات المستخدمين
        """
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        timestamp = data.get('timestamp')
        if timestamp and isinstance(timestamp, str):
            data['timestamp'] = datetime.fromisoformat(timestamp)
        
        return cls(**data)


class BackupInfo:
    """نموذج بيانات معلومات النسخ الاحتياطي"""
    
    def __init__(
        self,
        backup_id: str,
        filename: str,
        created_at: Optional[datetime] = None,
        created_by: Optional[str] = None,
        size_bytes: Optional[int] = None,
        backup_type: str = "full",
        status: str = "completed",
        description: Optional[str] = None,
        storage_path: Optional[str] = None,
        is_encrypted: bool = False,
        encryption_key_id: Optional[str] = None,
        database_version: Optional[str] = None,
        system_version: Optional[str] = None,
        includes_files: bool = True,
        includes_database: bool = True,
        retention_days: Optional[int] = None,
        is_automatic: bool = False,
        completion_time: Optional[datetime] = None,
        duration_seconds: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        تهيئة كائن معلومات النسخ الاحتياطي
        
        المعاملات:
            backup_id: معرف النسخة الاحتياطية
            filename: اسم الملف
            created_at: تاريخ الإنشاء (اختياري)
            created_by: معرف المستخدم الذي أنشأ النسخة الاحتياطية (اختياري)
            size_bytes: حجم النسخة الاحتياطية بالبايت (اختياري)
            backup_type: نوع النسخة الاحتياطية (اختياري، افتراضي: "full")
            status: حالة النسخة الاحتياطية (اختياري، افتراضي: "completed")
            description: وصف النسخة الاحتياطية (اختياري)
            storage_path: مسار التخزين (اختياري)
            is_encrypted: ما إذا كانت النسخة الاحتياطية مشفرة (اختياري، افتراضي: False)
            encryption_key_id: معرف مفتاح التشفير (اختياري)
            database_version: إصدار قاعدة البيانات (اختياري)
            system_version: إصدار النظام (اختياري)
            includes_files: ما إذا كانت النسخة الاحتياطية تتضمن الملفات (اختياري، افتراضي: True)
            includes_database: ما إذا كانت النسخة الاحتياطية تتضمن قاعدة البيانات (اختياري، افتراضي: True)
            retention_days: عدد أيام الاحتفاظ (اختياري)
            is_automatic: ما إذا كانت النسخة الاحتياطية تلقائية (اختياري، افتراضي: False)
            completion_time: وقت الاكتمال (اختياري)
            duration_seconds: مدة النسخ الاحتياطي بالثواني (اختياري)
            details: تفاصيل إضافية (اختياري)
        """
        self.backup_id = backup_id
        self.filename = filename
        self.created_at = created_at or datetime.now()
        self.created_by = created_by
        self.size_bytes = size_bytes
        self.backup_type = backup_type
        self.status = status
        self.description = description
        self.storage_path = storage_path
        self.is_encrypted = is_encrypted
        self.encryption_key_id = encryption_key_id
        self.database_version = database_version
        self.system_version = system_version
        self.includes_files = includes_files
        self.includes_database = includes_database
        self.retention_days = retention_days
        self.is_automatic = is_automatic
        self.completion_time = completion_time
        self.duration_seconds = duration_seconds
        self.details = details or {}
    
    @property
    def size_formatted(self) -> str:
        """
        الحصول على حجم النسخة الاحتياطية بتنسيق مقروء
        
        العائد:
            حجم النسخة الاحتياطية بتنسيق مقروء
        """
        if self.size_bytes is None:
            return "غير معروف"
        
        # تحويل الحجم إلى تنسيق مقروء (كيلوبايت، ميجابايت، جيجابايت)
        size_kb = self.size_bytes / 1024
        if size_kb < 1024:
            return f"{size_kb:.2f} كيلوبايت"
        
        size_mb = size_kb / 1024
        if size_mb < 1024:
            return f"{size_mb:.2f} ميجابايت"
        
        size_gb = size_mb / 1024
        return f"{size_gb:.2f} جيجابايت"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن معلومات النسخ الاحتياطي إلى قاموس
        
        العائد:
            قاموس يمثل معلومات النسخ الاحتياطي
        """
        return {
            "backup_id": self.backup_id,
            "filename": self.filename,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "size_bytes": self.size_bytes,
            "size_formatted": self.size_formatted,
            "backup_type": self.backup_type,
            "status": self.status,
            "description": self.description,
            "storage_path": self.storage_path,
            "is_encrypted": self.is_encrypted,
            "encryption_key_id": self.encryption_key_id,
            "database_version": self.database_version,
            "system_version": self.system_version,
            "includes_files": self.includes_files,
            "includes_database": self.includes_database,
            "retention_days": self.retention_days,
            "is_automatic": self.is_automatic,
            "completion_time": self.completion_time.isoformat() if self.completion_time else None,
            "duration_seconds": self.duration_seconds,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupInfo':
        """
        إنشاء كائن معلومات نسخ احتياطي من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات معلومات النسخ الاحتياطي
            
        العائد:
            كائن معلومات النسخ الاحتياطي
        """
        # حذف الحقول المحسوبة
        data.pop('size_formatted', None)
        
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        created_at = data.get('created_at')
        if created_at and isinstance(created_at, str):
            data['created_at'] = datetime.fromisoformat(created_at)
        
        completion_time = data.get('completion_time')
        if completion_time and isinstance(completion_time, str):
            data['completion_time'] = datetime.fromisoformat(completion_time)
        
        return cls(**data)
