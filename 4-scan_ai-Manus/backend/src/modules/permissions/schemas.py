"""
مخططات البيانات لمديول الصلاحيات

يحتوي هذا الملف على تعريف مخططات البيانات (schemas) الخاصة بمديول الصلاحيات في نظام Gaara ERP.
تستخدم هذه المخططات للتحقق من صحة البيانات المدخلة والمخرجة في واجهات API.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PermissionBase(BaseModel):
    """
    المخطط الأساسي للصلاحية
    """
    name: str = Field(...,
                      description="اسم الصلاحية",
                      example="auth.users.read")
    description: Optional[str] = Field(None, description="وصف الصلاحية")
    scope: str = Field(..., description="نطاق الصلاحية", example="feature")
    is_active: bool = Field(True, description="حالة تفعيل الصلاحية")


class PermissionCreate(PermissionBase):
    """
    مخطط إنشاء صلاحية جديدة
    """


class PermissionUpdate(BaseModel):
    """
    مخطط تحديث صلاحية موجودة
    """
    description: Optional[str] = Field(None, description="وصف الصلاحية")
    is_active: Optional[bool] = Field(None, description="حالة تفعيل الصلاحية")


class Permission(PermissionBase):
    """
    مخطط الصلاحية الكامل
    """
    id: int = Field(..., description="معرف الصلاحية")
    created_at: datetime = Field(..., description="تاريخ إنشاء الصلاحية")
    updated_at: Optional[datetime] = Field(
        None, description="تاريخ آخر تحديث للصلاحية")

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    """
    المخطط الأساسي للدور
    """
    name: str = Field(..., description="اسم الدور", example="admin")
    display_name: str = Field(...,
                              description="اسم العرض للدور",
                              example="مدير النظام")
    description: Optional[str] = Field(None, description="وصف الدور")
    is_system: bool = Field(False, description="هل هو دور نظام (لا يمكن حذفه)")
    is_active: bool = Field(True, description="حالة تفعيل الدور")


class RoleCreate(RoleBase):
    """
    مخطط إنشاء دور جديد
    """
    permissions: Optional[List[str]] = Field(
        None, description="قائمة بأسماء الصلاحيات المراد تعيينها للدور")


class RoleUpdate(BaseModel):
    """
    مخطط تحديث دور موجود
    """
    display_name: Optional[str] = Field(None, description="اسم العرض للدور")
    description: Optional[str] = Field(None, description="وصف الدور")
    is_active: Optional[bool] = Field(None, description="حالة تفعيل الدور")


class Role(RoleBase):
    """
    مخطط الدور الكامل
    """
    id: int = Field(..., description="معرف الدور")
    created_at: datetime = Field(..., description="تاريخ إنشاء الدور")
    updated_at: Optional[datetime] = Field(
        None, description="تاريخ آخر تحديث للدور")
    permissions: List[Permission] = Field(
        [], description="قائمة بالصلاحيات المعينة للدور")

    class Config:
        orm_mode = True


class RolePermissionBase(BaseModel):
    """
    المخطط الأساسي للعلاقة بين الدور والصلاحية
    """
    role_id: int = Field(..., description="معرف الدور")
    permission_id: int = Field(..., description="معرف الصلاحية")


class RolePermissionCreate(RolePermissionBase):
    """
    مخطط إنشاء علاقة بين دور وصلاحية
    """


class RolePermission(RolePermissionBase):
    """
    مخطط العلاقة بين الدور والصلاحية الكامل
    """
    id: int = Field(..., description="معرف العلاقة")
    created_at: datetime = Field(..., description="تاريخ إنشاء العلاقة")

    class Config:
        orm_mode = True


class UserRoleBase(BaseModel):
    """
    المخطط الأساسي للعلاقة بين المستخدم والدور
    """
    user_id: int = Field(..., description="معرف المستخدم")
    role_id: int = Field(..., description="معرف الدور")


class UserRoleCreate(UserRoleBase):
    """
    مخطط إنشاء علاقة بين مستخدم ودور
    """
    created_by: Optional[int] = Field(
        None, description="معرف المستخدم الذي أنشأ العلاقة")


class UserRole(UserRoleBase):
    """
    مخطط العلاقة بين المستخدم والدور الكامل
    """
    id: int = Field(..., description="معرف العلاقة")
    created_at: datetime = Field(..., description="تاريخ إنشاء العلاقة")
    created_by: Optional[int] = Field(
        None, description="معرف المستخدم الذي أنشأ العلاقة")
    role: Role = Field(..., description="معلومات الدور")

    class Config:
        orm_mode = True


class AgentRoleBase(BaseModel):
    """
    المخطط الأساسي للعلاقة بين وكيل الذكاء الاصطناعي والدور
    """
    agent_id: int = Field(..., description="معرف وكيل الذكاء الاصطناعي")
    role_id: int = Field(..., description="معرف الدور")


class AgentRoleCreate(AgentRoleBase):
    """
    مخطط إنشاء علاقة بين وكيل ذكاء اصطناعي ودور
    """
    created_by: Optional[int] = Field(
        None, description="معرف المستخدم الذي أنشأ العلاقة")


class AgentRole(AgentRoleBase):
    """
    مخطط العلاقة بين وكيل الذكاء الاصطناعي والدور الكامل
    """
    id: int = Field(..., description="معرف العلاقة")
    created_at: datetime = Field(..., description="تاريخ إنشاء العلاقة")
    created_by: Optional[int] = Field(
        None, description="معرف المستخدم الذي أنشأ العلاقة")
    role: Role = Field(..., description="معلومات الدور")

    class Config:
        orm_mode = True


class PermissionCheck(BaseModel):
    """
    مخطط للتحقق من صلاحية
    """
    user_id: Optional[int] = Field(None, description="معرف المستخدم")
    agent_id: Optional[int] = Field(
        None, description="معرف وكيل الذكاء الاصطناعي")
    permission: str = Field(..., description="اسم الصلاحية المراد التحقق منها")
    resource_id: Optional[int] = Field(
        None, description="معرف المورد (للصلاحيات على مستوى السجل)")

    @validator('user_id', 'agent_id')
    def validate_ids(cls, v, values):
        """التحقق من وجود معرف مستخدم أو معرف وكيل على الأقل"""
        if 'user_id' in values and values['user_id'] is None and 'agent_id' in values and values['agent_id'] is None:
            raise ValueError(
                "يجب توفير معرف المستخدم أو معرف الوكيل على الأقل")
        return v


class PermissionCheckResult(BaseModel):
    """
    مخطط نتيجة التحقق من صلاحية
    """
    has_permission: bool = Field(...,
                                 description="هل يملك المستخدم/الوكيل الصلاحية")
    details: Optional[str] = Field(None, description="تفاصيل إضافية")


class PermissionAuditLogBase(BaseModel):
    """
    المخطط الأساسي لسجل تدقيق الصلاحيات
    """
    user_id: Optional[int] = Field(None, description="معرف المستخدم")
    agent_id: Optional[int] = Field(
        None, description="معرف وكيل الذكاء الاصطناعي")
    action: str = Field(..., description="نوع العملية")
    resource_type: str = Field(..., description="نوع المورد")
    resource_id: Optional[int] = Field(None, description="معرف المورد")
    details: Optional[str] = Field(None, description="تفاصيل إضافية")
    success: bool = Field(True, description="هل نجحت العملية")
    ip_address: Optional[str] = Field(None, description="عنوان IP للمستخدم")


class PermissionAuditLogCreate(PermissionAuditLogBase):
    """
    مخطط إنشاء سجل تدقيق صلاحيات جديد
    """


class PermissionAuditLog(PermissionAuditLogBase):
    """
    مخطط سجل تدقيق الصلاحيات الكامل
    """
    id: int = Field(..., description="معرف السجل")
    created_at: datetime = Field(..., description="تاريخ إنشاء السجل")

    class Config:
        orm_mode = True


class ModuleIntegrationInfo(BaseModel):
    """
    مخطط معلومات تكامل المديول مع نظام الصلاحيات
    """
    module_name: str = Field(..., description="اسم المديول")
    features: List[str] = Field(..., description="قائمة بميزات المديول")
    is_registered: bool = Field(...,
                                description="هل المديول مسجل في نظام الصلاحيات")
    permissions_count: int = Field(...,
                                   description="عدد الصلاحيات المسجلة للمديول")


class ModuleIntegrationStatus(BaseModel):
    """
    مخطط حالة تكامل المديولات مع نظام الصلاحيات
    """
    modules: List[ModuleIntegrationInfo] = Field(...,
                                                 description="قائمة بمعلومات تكامل المديولات")
    total_registered: int = Field(...,
                                  description="إجمالي عدد المديولات المسجلة")
    total_required: int = Field(...,
                                description="إجمالي عدد المديولات المطلوبة")
    integration_percentage: float = Field(...,
                                          description="نسبة اكتمال التكامل")
