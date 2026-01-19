# /home/ubuntu/ai_web_organized/src/modules/internal_diagnosis/models.py

"""
تعريف نماذج البيانات (Data Models) لوحدة محرك التشخيص (internal_diagnosis).

يحتوي هذا الملف على تعريفات Pydantic للنماذج المستخدمة في طلبات التشخيص، نتائج التشخيص،
مدخلات القاعدة المعرفية، وغيرها من هياكل البيانات المستخدمة في الوحدة.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class DiagnosisStatus(str, Enum):
    """حالات عملية التشخيص."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ConfidenceLevel(str, Enum):
    """مستويات الثقة في التشخيص."""
    VERY_LOW = "very_low"  # 0-20%
    LOW = "low"  # 21-40%
    MEDIUM = "medium"  # 41-60%
    HIGH = "high"  # 61-80%
    VERY_HIGH = "very_high"  # 81-100%


class DiagnosisRequest(BaseModel):
    """نموذج طلب التشخيص."""
    symptoms_description: Optional[str] = Field(
        None, description="وصف نصي للأعراض المرصودة")
    image_path: Optional[str] = Field(
        None, description="مسار الصورة المراد تشخيصها")
    plant_type: Optional[str] = Field(
        None, description="نوع النبات (إذا كان معروفًا)")
    location: Optional[str] = Field(
        None,
        description="موقع النبات (للمساعدة في تحديد الأمراض المحتملة بناءً على المنطقة)")
    additional_data: Optional[Dict[str, Any]] = Field(
        None, description="بيانات إضافية قد تكون مفيدة للتشخيص")
    use_external_diagnosis: bool = Field(
        False, description="ما إذا كان يجب استخدام أدوات تشخيص خارجية")
    user_id: Optional[str] = Field(
        None, description="معرف المستخدم الذي طلب التشخيص")

    @validator('image_path')
    def validate_image_path(cls, v):  # pylint: disable=no-self-argument
        """التحقق من صحة مسار الصورة."""
        if v is not None and not v.strip():
            raise ValueError("مسار الصورة لا يمكن أن يكون فارغًا")
        return v

    @validator('symptoms_description')
    def validate_symptoms(cls, v, values):  # pylint: disable=no-self-argument
        """التحقق من وجود إما وصف للأعراض أو مسار صورة."""
        if not v and not values.get('image_path'):
            raise ValueError(
                "يجب توفير إما وصف للأعراض أو مسار صورة أو كليهما")
        return v


class DiagnosisResult(BaseModel):
    """نموذج نتيجة التشخيص الفردية."""
    disease_name: str = Field(..., description="اسم المرض المشخص")
    confidence: float = Field(
        ..., description="مستوى الثقة في التشخيص (0.0 إلى 1.0)")
    confidence_level: ConfidenceLevel = Field(
        ..., description="مستوى الثقة كتصنيف نصي")
    description: Optional[str] = Field(
        None, description="وصف للمرض المشخص")
    treatment_suggestions: List[str] = Field(
        default_factory=list, description="اقتراحات علاجية")
    evidence: List[str] = Field(
        default_factory=list, description="الأدلة التي استند إليها التشخيص")
    source: str = Field(
        "internal", description="مصدر التشخيص (داخلي، خارجي، إلخ)")

    @validator('confidence_level', pre=True, always=True)
    def set_confidence_level(cls, v, values):  # pylint: disable=no-self-argument
        """تعيين مستوى الثقة بناءً على قيمة الثقة الرقمية."""
        if v is not None:
            return v

        confidence = values.get('confidence', 0)
        if confidence < 0.2:
            return ConfidenceLevel.VERY_LOW
        if confidence < 0.4:
            return ConfidenceLevel.LOW
        if confidence < 0.6:
            return ConfidenceLevel.MEDIUM
        if confidence < 0.8:
            return ConfidenceLevel.HIGH
        return ConfidenceLevel.VERY_HIGH


class DiagnosisResponse(BaseModel):
    """نموذج الاستجابة الكاملة لطلب التشخيص."""
    diagnosis_id: str = Field(..., description="معرف فريد لعملية التشخيص")
    status: DiagnosisStatus = Field(
        ..., description="حالة عملية التشخيص")
    results: List[DiagnosisResult] = Field(
        default_factory=list, description="نتائج التشخيص (قد تكون متعددة)")
    external_results: List[DiagnosisResult] = Field(
        default_factory=list, description="نتائج من أنظمة تشخيص خارجية")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="وقت إجراء التشخيص")
    error_message: Optional[str] = Field(
        None, description="رسالة خطأ في حالة فشل التشخيص")
    request_data: DiagnosisRequest = Field(
        ..., description="بيانات الطلب الأصلي")


class KnowledgeBaseEntry(BaseModel):
    """نموذج مدخل في القاعدة المعرفية."""
    entry_id: Optional[str] = Field(
        None, description="معرف فريد للمدخل (يتم توليده تلقائيًا إذا لم يتم توفيره)")
    disease_name: str = Field(..., description="اسم المرض")
    scientific_name: Optional[str] = Field(
        None, description="الاسم العلمي للمرض")
    symptoms: List[str] = Field(
        ..., description="قائمة بالأعراض المرتبطة بالمرض")
    description: str = Field(..., description="وصف تفصيلي للمرض")
    affected_plants: List[str] = Field(
        ..., description="أنواع النباتات التي يمكن أن تتأثر بهذا المرض")
    treatments: List[str] = Field(
        ..., description="قائمة بالعلاجات الممكنة")
    prevention: List[str] = Field(
        ..., description="إجراءات وقائية للحماية من المرض")
    regions: Optional[List[str]] = Field(
        None, description="المناطق الجغرافية التي ينتشر فيها المرض")
    severity: Optional[str] = Field(
        None, description="مستوى خطورة المرض (منخفض، متوسط، عالي)")
    images: Optional[List[str]] = Field(
        None, description="مسارات لصور مرجعية للمرض")
    references: Optional[List[str]] = Field(
        None, description="مراجع علمية أو مصادر للمعلومات")
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="تاريخ آخر تحديث للمدخل")
    created_by: Optional[str] = Field(
        None, description="معرف المستخدم الذي أنشأ المدخل")

    @validator('symptoms', 'treatments', 'prevention', 'affected_plants')
    def validate_non_empty_lists(cls, v, field):  # pylint: disable=no-self-argument
        """التحقق من أن القوائم الإلزامية ليست فارغة."""
        if not v:
            raise ValueError(
                f"يجب أن تحتوي {field.name} على عنصر واحد على الأقل")
        return v


class DiagnosisHistoryEntry(BaseModel):
    """نموذج مدخل في سجل التشخيصات."""
    diagnosis_id: str = Field(..., description="معرف فريد لعملية التشخيص")
    user_id: Optional[str] = Field(
        None, description="معرف المستخدم الذي طلب التشخيص")
    timestamp: datetime = Field(
        ..., description="وقت إجراء التشخيص")
    request_summary: str = Field(
        ..., description="ملخص لطلب التشخيص")
    result_summary: str = Field(
        ..., description="ملخص لنتيجة التشخيص")
    status: DiagnosisStatus = Field(
        ..., description="حالة عملية التشخيص")
    full_response: Optional[DiagnosisResponse] = Field(
        None, description="الاستجابة الكاملة للتشخيص")


class ExternalDiagnosisSystem(BaseModel):
    """نموذج لتكوين نظام تشخيص خارجي."""
    system_id: str = Field(..., description="معرف فريد للنظام الخارجي")
    name: str = Field(..., description="اسم النظام الخارجي")
    api_url: str = Field(...,
                         description="عنوان URL لواجهة API الخاصة بالنظام")
    api_key: Optional[str] = Field(
        None, description="مفتاح API للمصادقة (إذا كان مطلوبًا)")
    enabled: bool = Field(
        True, description="ما إذا كان النظام ممكّنًا للاستخدام")
    timeout_seconds: int = Field(
        30, description="مهلة الانتظار بالثواني لطلبات API")
    priority: int = Field(
        1, description="أولوية النظام (الأرقام الأصغر = أولوية أعلى)")
    description: Optional[str] = Field(
        None, description="وصف للنظام وقدراته")
    last_checked: Optional[datetime] = Field(
        None, description="آخر وقت تم فيه التحقق من توفر النظام")
    is_available: bool = Field(
        True, description="ما إذا كان النظام متاحًا حاليًا")
