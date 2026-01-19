"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/activity_log/schemas.py
الوصف: مخططات سجل النشاط
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

# Constants for repeated string literals
MODULE_ID_DESC = "معرف المديول"
ACTION_ID_DESC = "معرف الإجراء"
USER_ID_DESC = "معرف المستخدم"
ACTIVITY_LOG_ID_DESC = "معرف سجل النشاط"


class ActivityLogBase(BaseModel):
    """المخطط الأساسي لسجل النشاط"""
    module_id: str = Field(..., description=MODULE_ID_DESC)
    action_id: str = Field(..., description=ACTION_ID_DESC)
    log_type: str = Field(..., description="نوع السجل")
    description: str = Field(..., description="وصف النشاط")
    log_data: Optional[Dict[str, Any]] = Field(None, description="بيانات السجل")
    user_id: Optional[int] = Field(None, description=USER_ID_DESC)
    ip_address: Optional[str] = Field(None, description="عنوان IP")
    user_agent: Optional[str] = Field(None, description="وكيل المستخدم")


class ActivityLogCreate(ActivityLogBase):
    """مخطط إنشاء سجل نشاط"""
    pass


class ActivityLogUpdate(BaseModel):
    """مخطط تحديث سجل نشاط"""
    module_id: Optional[str] = Field(None, description=MODULE_ID_DESC)
    action_id: Optional[str] = Field(None, description=ACTION_ID_DESC)
    log_type: Optional[str] = Field(None, description="نوع السجل")
    description: Optional[str] = Field(None, description="وصف النشاط")
    log_data: Optional[Dict[str, Any]] = Field(None, description="بيانات السجل")
    user_id: Optional[int] = Field(None, description=USER_ID_DESC)
    ip_address: Optional[str] = Field(None, description="عنوان IP")
    user_agent: Optional[str] = Field(None, description="وكيل المستخدم")


class ActivityLogInDB(ActivityLogBase):
    """مخطط سجل النشاط في قاعدة البيانات"""
    id: int = Field(..., description="معرف السجل")
    created_at: datetime = Field(..., description="تاريخ الإنشاء")
    updated_at: Optional[datetime] = Field(None, description="تاريخ التحديث")

    class Config:
        """إعدادات المخطط"""
        orm_mode = True


class ActivityLogResponse(ActivityLogBase):
    """نموذج استجابة سجل النشاط"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SystemLogBase(BaseModel):
    """النموذج الأساسي لسجل النظام"""
    activity_log_id: int = Field(..., description=ACTIVITY_LOG_ID_DESC)
    component: str = Field(..., description="المكون")
    event_type: str = Field(..., description="نوع الحدث")
    severity: str = Field(..., description="مستوى الخطورة (critical, error, warning, info, debug)")
    message: str = Field(..., description="الرسالة")
    details: Optional[Dict[str, Any]] = Field(None, description="تفاصيل إضافية")


class SystemLogCreate(SystemLogBase):
    """نموذج إنشاء سجل النظام"""
    pass


class SystemLogResponse(SystemLogBase):
    """نموذج استجابة سجل النظام"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogBase(BaseModel):
    """النموذج الأساسي لسجل المستخدم"""
    activity_log_id: int = Field(..., description=ACTIVITY_LOG_ID_DESC)
    user_id: int = Field(..., description=USER_ID_DESC)
    session_id: Optional[str] = Field(None, description="معرف الجلسة")
    action_type: str = Field(..., description="نوع الإجراء")
    resource_type: Optional[str] = Field(None, description="نوع المورد")
    resource_id: Optional[str] = Field(None, description="معرف المورد")
    before_state: Optional[Dict[str, Any]] = Field(None, description="الحالة قبل التغيير")
    after_state: Optional[Dict[str, Any]] = Field(None, description="الحالة بعد التغيير")


class UserLogCreate(UserLogBase):
    """نموذج إنشاء سجل المستخدم"""
    pass


class UserLogResponse(UserLogBase):
    """نموذج استجابة سجل المستخدم"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AILogBase(BaseModel):
    """النموذج الأساسي لسجل الذكاء الاصطناعي"""
    activity_log_id: int = Field(..., description=ACTIVITY_LOG_ID_DESC)
    agent_id: str = Field(..., description="معرف الوكيل")
    agent_type: str = Field(..., description="نوع الوكيل")
    interaction_type: str = Field(..., description="نوع التفاعل (query, response, a2a_communication)")
    query: Optional[str] = Field(None, description="الاستعلام")
    response: Optional[str] = Field(None, description="الاستجابة")
    tokens_used: Optional[int] = Field(None, description="عدد الرموز المستخدمة")
    processing_time: Optional[int] = Field(None, description="وقت المعالجة (بالمللي ثانية)")
    confidence_score: Optional[int] = Field(None, description="درجة الثقة")


class AILogCreate(AILogBase):
    """نموذج إنشاء سجل الذكاء الاصطناعي"""
    pass


class AILogResponse(AILogBase):
    """نموذج استجابة سجل الذكاء الاصطناعي"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class LogModuleBase(BaseModel):
    """النموذج الأساسي لمديول السجل"""
    module_id: str = Field(..., description=MODULE_ID_DESC)
    name: str = Field(..., description="اسم المديول")
    name_ar: Optional[str] = Field(None, description="اسم المديول بالعربية")
    description: Optional[str] = Field(None, description="وصف المديول")
    is_active: int = Field(1, description="حالة التفعيل")


class LogModuleCreate(LogModuleBase):
    """نموذج إنشاء مديول السجل"""
    pass


class LogModuleResponse(LogModuleBase):
    """نموذج استجابة مديول السجل"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LogActionBase(BaseModel):
    """النموذج الأساسي لإجراء السجل"""
    action_id: str = Field(..., description=ACTION_ID_DESC)
    name: str = Field(..., description="اسم الإجراء")
    name_ar: Optional[str] = Field(None, description="اسم الإجراء بالعربية")
    description: Optional[str] = Field(None, description="وصف الإجراء")
    module_id: str = Field(..., description=MODULE_ID_DESC)
    is_active: int = Field(1, description="حالة التفعيل")


class LogActionCreate(LogActionBase):
    """نموذج إنشاء إجراء السجل"""
    pass


class LogActionResponse(LogActionBase):
    """نموذج استجابة إجراء السجل"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LogRetentionPolicyBase(BaseModel):
    """النموذج الأساسي لسياسة الاحتفاظ بالسجلات"""
    log_type: str = Field(..., description="نوع السجل (system, user, ai)")
    retention_days: int = Field(..., description="عدد أيام الاحتفاظ")
    archive_enabled: int = Field(0, description="تفعيل الأرشفة")
    archive_path: Optional[str] = Field(None, description="مسار الأرشيف")


class LogRetentionPolicyCreate(LogRetentionPolicyBase):
    """نموذج إنشاء سياسة الاحتفاظ بالسجلات"""
    pass


class LogRetentionPolicyResponse(LogRetentionPolicyBase):
    """نموذج استجابة سياسة الاحتفاظ بالسجلات"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ActivityLogFilter(BaseModel):
    """نموذج تصفية سجل النشاط"""
    log_type: Optional[str] = Field(None, description="نوع السجل (system, user, ai)")
    module_id: Optional[str] = Field(None, description="معرف المديول")
    action_id: Optional[str] = Field(None, description="معرف الإجراء")
    user_id: Optional[int] = Field(None, description="معرف المستخدم")
    status: Optional[str] = Field(None, description="حالة السجل")
    start_date: Optional[datetime] = Field(None, description="تاريخ البداية")
    end_date: Optional[datetime] = Field(None, description="تاريخ النهاية")
    search: Optional[str] = Field(None, description="نص البحث")
    page: int = Field(1, description="رقم الصفحة")
    page_size: int = Field(20, description="حجم الصفحة")


class ActivityLogExport(BaseModel):
    """نموذج تصدير سجل النشاط"""
    filter: ActivityLogFilter = Field(..., description="معايير التصفية")
    export_format: str = Field("csv", description="صيغة التصدير (csv, xlsx, pdf)")


class ActivityLogStatistics(BaseModel):
    """نموذج إحصائيات سجل النشاط"""
    total_logs: int = Field(..., description="إجمالي السجلات")
    logs_by_type: Dict[str, int] = Field(..., description="السجلات حسب النوع")
    logs_by_module: Dict[str, int] = Field(..., description="السجلات حسب المديول")
    logs_by_status: Dict[str, int] = Field(..., description="السجلات حسب الحالة")
    logs_by_date: Dict[str, int] = Field(..., description="السجلات حسب التاريخ")


class PaginatedActivityLogs(BaseModel):
    """نموذج سجلات النشاط المقسمة إلى صفحات"""
    items: List[ActivityLogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Aliases for backward compatibility
class UserActionLogCreate(ActivityLogCreate):
    """Alias for backward compatibility"""
    pass


class SystemActionLogCreate(ActivityLogCreate):
    """Alias for backward compatibility"""
    pass


class AIActionLogCreate(ActivityLogCreate):
    """Alias for backward compatibility"""
    pass


class UserActionLogResponse(ActivityLogResponse):
    """Alias for backward compatibility"""
    pass


class SystemActionLogResponse(ActivityLogResponse):
    """Alias for backward compatibility"""
    pass


class AIActionLogResponse(ActivityLogResponse):
    """Alias for backward compatibility"""
    pass


class AIInteractionLogCreate(BaseModel):
    """نموذج إنشاء سجل تفاعل الذكاء الاصطناعي"""
    module_id: str = Field(..., description=MODULE_ID_DESC)
    action_id: str = Field(..., description=ACTION_ID_DESC)
    user_id: Optional[int] = Field(None, description=USER_ID_DESC)
    description: str = Field(..., description="وصف التفاعل")
    agent_id: str = Field(..., description="معرف الوكيل")
    agent_type: str = Field(..., description="نوع الوكيل")
    interaction_type: str = Field(..., description="نوع التفاعل")
    query: Optional[str] = Field(None, description="الاستعلام")
    response: Optional[str] = Field(None, description="الاستجابة")
    tokens_used: Optional[int] = Field(None, description="عدد الرموز المستخدمة")
    processing_time: Optional[int] = Field(None, description="وقت المعالجة (بالمللي ثانية)")
    confidence_score: Optional[float] = Field(None, description="درجة الثقة")
    status: str = Field("success", description="حالة التفاعل")
