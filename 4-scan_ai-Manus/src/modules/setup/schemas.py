"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/schemas.py
الوصف: مخططات بيانات مديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SetupStatusResponse(BaseModel):
    """نموذج استجابة حالة الإعداد"""
    is_completed: bool = Field(..., description="ما إذا كان الإعداد مكتملاً")
    current_step: str = Field(..., description="الخطوة الحالية")
    completed_steps: List[str] = Field(default_factory=list, description="الخطوات المكتملة")
    total_steps: int = Field(..., description="إجمالي عدد الخطوات")
    setup_token: Optional[str] = Field(None, description="رمز الإعداد")
    token_expires_at: Optional[datetime] = Field(None, description="تاريخ انتهاء صلاحية الرمز")


class StepDataResponse(BaseModel):
    """نموذج استجابة بيانات الخطوة"""
    step_id: str = Field(..., description="معرف الخطوة")
    data: Dict[str, Any] = Field(..., description="بيانات الخطوة")


class ValidationResult(BaseModel):
    """نموذج نتيجة التحقق"""
    is_valid: bool = Field(..., description="ما إذا كانت البيانات صالحة")
    errors: List[str] = Field(default_factory=list, description="قائمة الأخطاء")


class StepUpdateResponse(BaseModel):
    """نموذج استجابة تحديث الخطوة"""
    success: bool = Field(..., description="ما إذا كان التحديث ناجحاً")
    message: str = Field(..., description="رسالة التحديث")


class SetupCompletionResponse(BaseModel):
    """نموذج استجابة إكمال الإعداد"""
    success: bool = Field(..., description="ما إذا كان الإكمال ناجحاً")
    message: str = Field(..., description="رسالة الإكمال")


class DatabaseConnectionTest(BaseModel):
    """نموذج اختبار اتصال قاعدة البيانات"""
    db_type: str = Field(..., description="نوع قاعدة البيانات")
    host: str = Field(..., description="المضيف")
    port: int = Field(..., description="المنفذ")
    name: str = Field(..., description="اسم قاعدة البيانات")
    user: str = Field(..., description="اسم المستخدم")
    password: str = Field(..., description="كلمة المرور")


class DatabaseConnectionTestResponse(BaseModel):
    """نموذج استجابة اختبار اتصال قاعدة البيانات"""
    success: bool = Field(..., description="ما إذا كان الاختبار ناجحاً")
    message: str = Field(..., description="رسالة الاختبار")


class EmailSettingsTest(BaseModel):
    """نموذج اختبار إعدادات البريد الإلكتروني"""
    smtp_server: str = Field(..., description="خادم SMTP")
    smtp_port: int = Field(..., description="منفذ SMTP")
    smtp_user: str = Field(..., description="اسم مستخدم SMTP")
    smtp_password: str = Field(..., description="كلمة مرور SMTP")
    from_email: str = Field(..., description="البريد الإلكتروني المرسل")
    use_tls: bool = Field(True, description="استخدام TLS")
    test_recipient: str = Field(..., description="البريد الإلكتروني المستلم للاختبار")


class EmailSettingsTestResponse(BaseModel):
    """نموذج استجابة اختبار إعدادات البريد الإلكتروني"""
    success: bool = Field(..., description="ما إذا كان الاختبار ناجحاً")
    message: str = Field(..., description="رسالة الاختبار")


class ModuleInfo(BaseModel):
    """نموذج معلومات المديول"""
    id: str = Field(..., description="معرف المديول")
    name: str = Field(..., description="اسم المديول")
    description: str = Field(..., description="وصف المديول")
    is_core: bool = Field(..., description="ما إذا كان المديول أساسياً")
    is_enabled: bool = Field(..., description="ما إذا كان المديول مفعلاً")
    dependencies: List[str] = Field(default_factory=list, description="اعتماديات المديول")
    version: str = Field(..., description="إصدار المديول")
    author: str = Field(..., description="مؤلف المديول")


class CountryInfo(BaseModel):
    """نموذج معلومات الدولة"""
    code: str = Field(..., description="رمز الدولة")
    name: str = Field(..., description="اسم الدولة")
    name_ar: str = Field(..., description="اسم الدولة بالعربية")
    flag_emoji: str = Field(..., description="رمز علم الدولة")
    calling_code: str = Field(..., description="رمز الاتصال الدولي")


class CurrencyInfo(BaseModel):
    """نموذج معلومات العملة"""
    code: str = Field(..., description="رمز العملة")
    name: str = Field(..., description="اسم العملة")
    name_ar: str = Field(..., description="اسم العملة بالعربية")
    symbol: str = Field(..., description="رمز العملة")


class TimezoneInfo(BaseModel):
    """نموذج معلومات المنطقة الزمنية"""
    value: str = Field(..., description="قيمة المنطقة الزمنية")
    text: str = Field(..., description="نص المنطقة الزمنية")
    offset: str = Field(..., description="فارق التوقيت")


class LanguageInfo(BaseModel):
    """نموذج معلومات اللغة"""
    code: str = Field(..., description="رمز اللغة")
    name: str = Field(..., description="اسم اللغة")
    name_native: str = Field(..., description="اسم اللغة الأصلي")
    rtl: bool = Field(..., description="ما إذا كانت اللغة من اليمين إلى اليسار")


class SecuritySettings(BaseModel):
    """نموذج إعدادات الأمان"""
    use_ssl: bool = Field(..., description="استخدام SSL")
    ssl_cert_path: Optional[str] = Field(None, description="مسار شهادة SSL")
    ssl_key_path: Optional[str] = Field(None, description="مسار مفتاح SSL")
    session_timeout: int = Field(..., description="مهلة الجلسة (بالدقائق)")
    max_login_attempts: int = Field(..., description="الحد الأقصى لمحاولات تسجيل الدخول")
    lockout_duration: int = Field(..., description="مدة القفل (بالدقائق)")
    password_expiry_days: int = Field(..., description="أيام انتهاء صلاحية كلمة المرور")
    enable_2fa: bool = Field(..., description="تفعيل المصادقة الثنائية")
    allowed_ips: List[str] = Field(default_factory=list, description="عناوين IP المسموح بها")
    cors_origins: List[str] = Field(default_factory=list, description="أصول CORS")
    xss_protection: bool = Field(..., description="حماية XSS")
    csrf_protection: bool = Field(..., description="حماية CSRF")
    sql_injection_protection: bool = Field(..., description="حماية حقن SQL")
    rate_limiting: Dict[str, Any] = Field(..., description="تحديد معدل الطلبات")


class SecurityValidationResponse(BaseModel):
    """نموذج استجابة التحقق من صحة إعدادات الأمان"""
    is_valid: bool = Field(..., description="ما إذا كانت الإعدادات صالحة")
    warnings: List[str] = Field(default_factory=list, description="قائمة التحذيرات")
    recommendations: List[str] = Field(default_factory=list, description="قائمة التوصيات")


class SetupLogEntry(BaseModel):
    """نموذج إدخال سجل الإعداد"""
    id: int = Field(..., description="معرف السجل")
    step: str = Field(..., description="الخطوة")
    status: str = Field(..., description="الحالة")
    message: str = Field(..., description="الرسالة")
    details: Dict[str, Any] = Field(default_factory=dict, description="التفاصيل")
    created_at: datetime = Field(..., description="تاريخ الإنشاء")
