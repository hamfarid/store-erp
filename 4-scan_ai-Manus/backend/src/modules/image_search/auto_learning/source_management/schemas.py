# /home/ubuntu/image_search_integration/auto_learning/source_management/schemas.py

"""
مخططات البيانات لنظام إدارة المصادر الموثوقة للبحث الذاتي الذكي

هذا الملف يحتوي على تعريفات مخططات البيانات المستخدمة في نظام إدارة المصادر الموثوقة،
لضمان التحقق من صحة البيانات المدخلة والمخرجة.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class SourceTypeEnum(str, Enum):
    """تعداد أنواع المصادر"""
    ACADEMIC = "ACADEMIC"  # أكاديمي
    GOVERNMENT = "GOVERNMENT"  # حكومي
    COMMERCIAL = "COMMERCIAL"  # تجاري
    BLOG = "BLOG"  # مدونة
    FORUM = "FORUM"  # منتدى
    SOCIAL_MEDIA = "SOCIAL_MEDIA"  # وسائل التواصل الاجتماعي
    NEWS = "NEWS"  # أخبار
    RESEARCH = "RESEARCH"  # بحث علمي
    EDUCATIONAL = "EDUCATIONAL"  # تعليمي
    OTHER = "OTHER"  # أخرى


# ===== مخططات فئات المصادر =====

class SourceCategoryBase(BaseModel):
    """النموذج الأساسي لفئة المصادر"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(
        None, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True


class SourceCategoryCreate(SourceCategoryBase):
    """نموذج إنشاء فئة مصادر"""


class SourceCategoryUpdate(BaseModel):
    """نموذج تحديث فئة مصادر"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(
        None, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class SourceCategoryResponse(SourceCategoryBase):
    """نموذج استجابة فئة مصادر"""
    id: int
    created_at: datetime
    updated_at: datetime
    sources_count: Optional[int] = 0
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True


# ===== مخططات المصادر الموثوقة =====

class ContactInfo(BaseModel):
    """نموذج معلومات الاتصال"""
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None


class TrustedSourceBase(BaseModel):
    """النموذج الأساسي للمصدر الموثوق"""
    name: str = Field(..., min_length=2, max_length=200)
    url: str = Field(..., max_length=500)
    description: Optional[str] = None
    category_id: Optional[int] = None
    source_type: Optional[SourceTypeEnum] = None
    trust_level: int = Field(50, ge=0, le=100)
    is_academic: bool = False
    is_government: bool = False
    is_commercial: bool = False
    metadata: Optional[Dict[str, Any]] = None
    contact_info: Optional[ContactInfo] = None
    is_active: bool = True
    is_verified: bool = False
    verification_notes: Optional[str] = None


class TrustedSourceCreate(TrustedSourceBase):
    """نموذج إنشاء مصدر موثوق"""
    @validator('url')
    @classmethod
    def validate_url(cls, v):
        """التحقق من صحة عنوان URL"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('يجب أن يبدأ عنوان URL بـ http:// أو https://')
        return v


class TrustedSourceUpdate(BaseModel):
    """نموذج تحديث مصدر موثوق"""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    category_id: Optional[int] = None
    source_type: Optional[SourceTypeEnum] = None
    trust_level: Optional[int] = Field(None, ge=0, le=100)
    is_academic: Optional[bool] = None
    is_government: Optional[bool] = None
    is_commercial: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
    contact_info: Optional[ContactInfo] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    verification_notes: Optional[str] = None

    @validator('url')
    @classmethod
    def validate_url(cls, v):
        """التحقق من صحة عنوان URL"""
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError('يجب أن يبدأ عنوان URL بـ http:// أو https://')
        return v


class TrustedSourceResponse(TrustedSourceBase):
    """نموذج استجابة مصدر موثوق"""
    id: int
    domain: str
    usage_count: Optional[int] = 0
    success_count: Optional[int] = 0
    success_rate: Optional[float] = 0.0
    last_used_at: Optional[datetime] = None
    verification_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    category_name: Optional[str] = None

    class Config:
        orm_mode = True


# ===== مخططات تقييمات المصادر =====

class SourceRatingBase(BaseModel):
    """النموذج الأساسي لتقييم المصدر"""
    source_id: int
    rating: int = Field(..., ge=0, le=100)
    comment: Optional[str] = None
    user_id: Optional[int] = None


class SourceRatingCreate(SourceRatingBase):
    """نموذج إنشاء تقييم مصدر"""


class SourceRatingResponse(SourceRatingBase):
    """نموذج استجابة تقييم مصدر"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ===== مخططات القائمة السوداء =====

class SourceBlacklistEntryBase(BaseModel):
    """النموذج الأساسي لإدخال القائمة السوداء"""
    source_id: int
    reason: str
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    is_active: bool = True


class SourceBlacklistEntryCreate(SourceBlacklistEntryBase):
    """نموذج إنشاء إدخال القائمة السوداء"""


class SourceBlacklistEntryUpdate(BaseModel):
    """نموذج تحديث إدخال القائمة السوداء"""
    reason: Optional[str] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class SourceBlacklistEntryResponse(SourceBlacklistEntryBase):
    """نموذج استجابة إدخال القائمة السوداء"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    source_name: Optional[str] = None
    source_domain: Optional[str] = None

    class Config:
        orm_mode = True


# ===== مخططات التحقق من المصادر =====

class SourceVerificationBase(BaseModel):
    """النموذج الأساسي للتحقق من المصدر"""
    source_id: int
    is_verified: bool
    verification_method: Optional[str] = None
    verification_notes: Optional[str] = None
    verified_by: Optional[int] = None


class SourceVerificationCreate(SourceVerificationBase):
    """نموذج إنشاء تحقق من المصدر"""


class SourceVerificationResponse(SourceVerificationBase):
    """نموذج استجابة التحقق من المصدر"""
    id: int
    verification_date: datetime
    created_at: datetime
    source_name: Optional[str] = None
    source_domain: Optional[str] = None

    class Config:
        orm_mode = True


# ===== مخططات سجل استخدام المصادر =====

class SourceUsageLogBase(BaseModel):
    """النموذج الأساسي لسجل استخدام المصدر"""
    source_id: int
    usage_type: str
    keyword_id: Optional[int] = None
    search_engine_id: Optional[int] = None
    results_count: int = 0
    success: bool = True
    notes: Optional[str] = None


class SourceUsageLogCreate(SourceUsageLogBase):
    """نموذج إنشاء سجل استخدام المصدر"""


class SourceUsageLogResponse(SourceUsageLogBase):
    """نموذج استجابة سجل استخدام المصدر"""
    id: int
    usage_date: datetime
    created_at: datetime
    source_name: Optional[str] = None
    source_domain: Optional[str] = None

    class Config:
        orm_mode = True


# ===== مخططات الإحصائيات =====

class SourceStatistics(BaseModel):
    """نموذج إحصائيات المصادر الموثوقة"""
    total_sources: int
    active_sources: int
    avg_trust_level: float
    academic_sources: int
    government_sources: int
    commercial_sources: int
    most_trusted_sources: List[Dict[str, Any]]
    blacklisted_sources: int = 0
    verified_sources: int = 0
    sources_by_type: Dict[str, int] = {}


class SourceAnalytics(BaseModel):
    """نموذج تحليلات المصادر"""
    source_id: int
    name: str
    domain: str
    usage_count: int
    success_rate: float
    trust_level: int
    last_used_at: Optional[datetime] = None
    category_name: Optional[str] = None
    source_type: Optional[str] = None


class SourceAnalyticsResponse(BaseModel):
    """نموذج استجابة تحليلات المصادر"""
    analytics: List[SourceAnalytics]
    total_count: int
    page: int
    page_size: int
    total_pages: int
