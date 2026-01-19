# /home/ubuntu/image_search_integration/schemas.py
"""
مخططات البيانات لمديول البحث عن صور الإصابات والآفات النباتية
Data schemas for plant disease and pest image search module
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

# تعريف الثوابت للنصوص المتكررة
SEARCH_QUERY = "استعلام البحث"
RESULTS_COUNT = "عدد النتائج المطلوبة"
IMAGE_ID = "معرف الصورة"
FILENAME = "اسم الملف"
FILEPATH = "مسار الملف"
DISEASE_ID = "معرف المرض"
PEST_ID = "معرف الآفة"
SCIENTIFIC_NAME = "الاسم العلمي"


class ImageSource(str, Enum):
    """مصادر الصور المختلفة"""
    UPLOAD = "upload"  # تم رفعها من قبل المستخدم
    INTERNET = "internet"  # تم جلبها من الإنترنت
    SYSTEM = "system"  # صورة نظام افتراضية
    EXTERNAL_API = "external_api"  # تم جلبها من API خارجي
    OTHER = "other"  # مصدر آخر


class ImageStatus(str, Enum):
    """حالات الصور المختلفة"""
    ACTIVE = "active"  # نشطة وجاهزة للاستخدام
    PENDING = "pending"  # قيد المراجعة
    ARCHIVED = "archived"  # مؤرشفة
    DELETED = "deleted"  # محذوفة


class ConfidenceLevel(str, Enum):
    """مستويات الثقة في تصنيف الصور"""
    VERY_LOW = "very_low"  # منخفضة جداً (0-20%)
    LOW = "low"  # منخفضة (21-40%)
    MEDIUM = "medium"  # متوسطة (41-60%)
    HIGH = "high"  # عالية (61-80%)
    VERY_HIGH = "very_high"  # عالية جداً (81-100%)


class ImageSearchRequest(BaseModel):
    """طلب البحث عن صور"""
    query: str = Field(..., description=SEARCH_QUERY)
    count: int = Field(10, description=RESULTS_COUNT, ge=1, le=100)
    search_params: Dict[str, Any] = Field(default_factory=dict, description="معلمات البحث الإضافية")


class ImageSearchResponse(BaseModel):
    """استجابة البحث عن صور"""
    query: str = Field(..., description=SEARCH_QUERY)
    results_count: int = Field(..., description=RESULTS_COUNT)
    image_urls: List[str] = Field(..., description="قائمة عناوين URL للصور")
    search_id: int = Field(..., description="معرف البحث")


class ImageCollectionRequest(BaseModel):
    """طلب جمع صور"""
    keywords: List[str] = Field(..., description="قائمة الكلمات المفتاحية للبحث")
    max_images_per_keyword: int = Field(20, description="الحد الأقصى لعدد الصور لكل كلمة مفتاحية", ge=1, le=100)


class ImageMetadata(BaseModel):
    """البيانات الوصفية للصورة"""
    id: int = Field(..., description=IMAGE_ID)
    filename: str = Field(..., description=FILENAME)
    file_path: str = Field(..., description=FILEPATH)
    source_url: Optional[str] = Field(None, description="عنوان URL المصدر")
    query: Optional[str] = Field(None, description=SEARCH_QUERY)


class ImageCollectionResponse(BaseModel):
    """استجابة جمع صور"""
    keywords: List[str] = Field(..., description="قائمة الكلمات المفتاحية للبحث")
    total_collected: int = Field(..., description="إجمالي عدد الصور المجمعة")
    stored_images: List[Dict[str, Any]] = Field(..., description="قائمة الصور المخزنة")


class DiseaseImageSearchRequest(BaseModel):
    """طلب البحث عن صور مرض نباتي"""
    disease_id: int = Field(..., description=DISEASE_ID)
    count: int = Field(10, description=RESULTS_COUNT, ge=1, le=100)


class PestImageSearchRequest(BaseModel):
    """طلب البحث عن صور آفة زراعية"""
    pest_id: int = Field(..., description=PEST_ID)
    count: int = Field(10, description=RESULTS_COUNT, ge=1, le=100)


class CropImageSearchRequest(BaseModel):
    """طلب البحث عن صور محصول زراعي"""
    crop_id: int = Field(..., description="معرف المحصول")
    condition: Optional[str] = Field(None, description="حالة المحصول (مثل 'صحي'، 'مريض')")
    count: int = Field(10, description=RESULTS_COUNT, ge=1, le=100)


class ImageUploadResponse(BaseModel):
    """استجابة رفع صورة"""
    id: int = Field(..., description=IMAGE_ID)
    filename: str = Field(..., description=FILENAME)
    file_path: str = Field(..., description=FILEPATH)
    title: str = Field(..., description="عنوان الصورة")
    message: str = Field(..., description="رسالة النجاح")


class ImageTagBase(BaseModel):
    """نموذج وسم الصورة الأساسي"""
    name: str = Field(..., description="اسم الوسم")
    description: Optional[str] = Field(None, description="وصف الوسم")


class ImageTagCreate(ImageTagBase):
    """نموذج إنشاء وسم صورة"""
    pass


class ImageTagResponse(ImageTagBase):
    """نموذج استجابة وسم صورة"""
    id: int = Field(..., description=IMAGE_ID)

    class Config:
        orm_mode = True


class DiseaseBase(BaseModel):
    """نموذج المرض النباتي الأساسي"""
    name: str = Field(..., description="اسم المرض")
    scientific_name: Optional[str] = Field(None, description=SCIENTIFIC_NAME)
    description: Optional[str] = Field(None, description="وصف المرض")
    symptoms: Optional[str] = Field(None, description="أعراض المرض")
    causes: Optional[str] = Field(None, description="أسباب المرض")
    treatment: Optional[str] = Field(None, description="علاج المرض")
    prevention: Optional[str] = Field(None, description="الوقاية من المرض")


class DiseaseCreate(DiseaseBase):
    """نموذج إنشاء مرض نباتي"""
    pass


class DiseaseResponse(DiseaseBase):
    """نموذج استجابة مرض نباتي"""
    id: int = Field(..., description=DISEASE_ID)

    class Config:
        orm_mode = True


class PestBase(BaseModel):
    """نموذج الآفة الزراعية الأساسي"""
    name: str = Field(..., description="اسم الآفة")
    scientific_name: Optional[str] = Field(None, description=SCIENTIFIC_NAME)
    description: Optional[str] = Field(None, description="وصف الآفة")
    symptoms: Optional[str] = Field(None, description="أعراض الإصابة بالآفة")
    lifecycle: Optional[str] = Field(None, description="دورة حياة الآفة")
    control_methods: Optional[str] = Field(None, description="طرق المكافحة")


class PestCreate(PestBase):
    """نموذج إنشاء آفة زراعية"""
    pass


class PestResponse(PestBase):
    """نموذج استجابة آفة زراعية"""
    id: int = Field(..., description=PEST_ID)

    class Config:
        orm_mode = True


class CropBase(BaseModel):
    """نموذج المحصول الزراعي الأساسي"""
    name: str = Field(..., description="اسم المحصول")
    scientific_name: Optional[str] = Field(None, description=SCIENTIFIC_NAME)
    description: Optional[str] = Field(None, description="وصف المحصول")


class CropCreate(CropBase):
    """نموذج إنشاء محصول زراعي"""
    pass


class CropResponse(CropBase):
    """نموذج استجابة محصول زراعي"""
    id: int = Field(..., description="معرف المحصول")

    class Config:
        orm_mode = True


class PlantImageBase(BaseModel):
    """نموذج صورة النبات الأساسي"""
    title: Optional[str] = Field(None, description="عنوان الصورة")
    description: Optional[str] = Field(None, description="وصف الصورة")
    source: ImageSource = Field(default=ImageSource.UPLOAD, description="مصدر الصورة")
    source_url: Optional[str] = Field(None, description="رابط المصدر")
    status: ImageStatus = Field(default=ImageStatus.ACTIVE, description="حالة الصورة")
    disease_id: Optional[int] = Field(None, description=DISEASE_ID)
    pest_id: Optional[int] = Field(None, description=PEST_ID)
    metadata: Optional[Dict[str, Any]] = Field(None, description="بيانات وصفية إضافية")


class PlantImageCreate(PlantImageBase):
    """نموذج إنشاء صورة نبات"""
    filename: str = Field(..., description=FILENAME)
    file_path: str = Field(..., description=FILEPATH)
    file_size: Optional[int] = Field(None, description="حجم الملف بالبايت")
    file_format: Optional[str] = Field(None, description="صيغة الملف")
    crop_ids: Optional[List[int]] = Field(None, description="قائمة معرفات المحاصيل")
    tag_ids: Optional[List[int]] = Field(None, description="قائمة معرفات الوسوم")


class PlantImageResponse(PlantImageBase):
    """نموذج استجابة صورة نبات"""
    id: int = Field(..., description=IMAGE_ID)
    filename: str = Field(..., description=FILENAME)
    file_path: str = Field(..., description=FILEPATH)
    file_size: Optional[int] = Field(None, description="حجم الملف بالبايت")
    file_format: Optional[str] = Field(None, description="صيغة الملف")
    created_at: datetime = Field(..., description="تاريخ الإنشاء")
    updated_at: datetime = Field(..., description="تاريخ التحديث")
    crops: Optional[List[CropResponse]] = Field(None, description="قائمة المحاصيل")
    tags: Optional[List[ImageTagResponse]] = Field(None, description="قائمة الوسوم")
    disease: Optional[DiseaseResponse] = Field(None, description=DISEASE_ID)
    pest: Optional[PestResponse] = Field(None, description=PEST_ID)

    class Config:
        orm_mode = True
