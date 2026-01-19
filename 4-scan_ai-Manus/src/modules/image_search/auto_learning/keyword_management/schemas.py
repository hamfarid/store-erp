# /home/ubuntu/image_search_integration/auto_learning/keyword_management/schemas.py

"""
مخططات البيانات لنظام إدارة الكلمات المفتاحية المتقدم للبحث الذاتي الذكي

هذا الملف يحتوي على تعريفات مخططات البيانات المستخدمة في نظام إدارة الكلمات المفتاحية،
لضمان التحقق من صحة البيانات المدخلة والمخرجة.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PlantPartEnum(str, Enum):
    """تعداد أجزاء النبات"""
    LEAF = "LEAF"  # أوراق
    STEM = "STEM"  # ساق
    ROOT = "ROOT"  # جذور
    FRUIT = "FRUIT"  # ثمار
    FLOWER = "FLOWER"  # أزهار
    SEED = "SEED"  # بذور
    WHOLE_PLANT = "WHOLE_PLANT"  # النبات بالكامل


class ConditionTypeEnum(str, Enum):
    """تعداد أنواع الإصابات"""
    FUNGAL = "FUNGAL"  # فطري
    BACTERIAL = "BACTERIAL"  # بكتيري
    VIRAL = "VIRAL"  # فيروسي
    INSECT = "INSECT"  # حشري
    NUTRIENT_DEFICIENCY = "NUTRIENT_DEFICIENCY"  # نقص عناصر
    NUTRIENT_EXCESS = "NUTRIENT_EXCESS"  # زيادة عناصر
    WATER_DEFICIENCY = "WATER_DEFICIENCY"  # نقص مياه
    WATER_EXCESS = "WATER_EXCESS"  # زيادة مياه
    SALINITY = "SALINITY"  # ملوحة
    ENVIRONMENTAL = "ENVIRONMENTAL"  # بيئي
    OTHER = "OTHER"  # أخرى


class SemanticRelationType(str, Enum):
    """أنواع العلاقات الدلالية"""
    SYNONYM = "SYNONYM"  # مرادف
    BROADER = "BROADER"  # أوسع
    NARROWER = "NARROWER"  # أضيق
    RELATED = "RELATED"  # ذو صلة
    CAUSES = "CAUSES"  # يسبب
    CAUSED_BY = "CAUSED_BY"  # ناتج عن
    TREATS = "TREATS"  # يعالج
    TREATED_BY = "TREATED_BY"  # يعالج بواسطة
    SYMPTOM_OF = "SYMPTOM_OF"  # عرض لـ
    HAS_SYMPTOM = "HAS_SYMPTOM"  # له عرض


# ===== مخططات فئات الكلمات المفتاحية =====

class KeywordCategoryBase(BaseModel):
    """النموذج الأساسي لفئة الكلمات المفتاحية"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(None, regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True


class KeywordCategoryCreate(KeywordCategoryBase):
    """نموذج إنشاء فئة كلمات مفتاحية"""
    pass


class KeywordCategoryUpdate(BaseModel):
    """نموذج تحديث فئة كلمات مفتاحية"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(None, regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class KeywordCategoryResponse(KeywordCategoryBase):
    """نموذج استجابة فئة كلمات مفتاحية"""
    id: int
    created_at: datetime
    updated_at: datetime
    keywords_count: Optional[int] = 0

    class Config:
        orm_mode = True


# ===== مخططات العلاقات الدلالية =====

class SemanticRelation(BaseModel):
    """نموذج العلاقة الدلالية"""
    related_keyword_id: int
    relation_type: SemanticRelationType
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    notes: Optional[str] = None


# ===== مخططات الكلمات المفتاحية =====

class SearchKeywordBase(BaseModel):
    """النموذج الأساسي للكلمة المفتاحية"""
    keyword: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    plant_type: Optional[str] = None
    condition_type: Optional[ConditionTypeEnum] = None
    plant_part: Optional[PlantPartEnum] = None
    category_id: Optional[int] = None
    priority: int = Field(0, ge=0, le=100)
    max_results: int = Field(50, ge=1, le=1000)
    min_trust_level: float = Field(0.0, ge=0.0, le=1.0)
    trusted_sources_only: bool = False
    search_engines: Optional[List[str]] = None
    condition_id: Optional[int] = None
    is_active: bool = True


class SearchKeywordCreate(SearchKeywordBase):
    """نموذج إنشاء كلمة مفتاحية"""
    semantic_relations: Optional[List[SemanticRelation]] = None


class SearchKeywordUpdate(BaseModel):
    """نموذج تحديث كلمة مفتاحية"""
    keyword: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    plant_type: Optional[str] = None
    condition_type: Optional[ConditionTypeEnum] = None
    plant_part: Optional[PlantPartEnum] = None
    category_id: Optional[int] = None
    priority: Optional[int] = Field(None, ge=0, le=100)
    max_results: Optional[int] = Field(None, ge=1, le=1000)
    min_trust_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    trusted_sources_only: Optional[bool] = None
    search_engines: Optional[List[str]] = None
    semantic_relations: Optional[List[SemanticRelation]] = None
    condition_id: Optional[int] = None
    is_active: Optional[bool] = None


class SearchKeywordResponse(SearchKeywordBase):
    """نموذج استجابة كلمة مفتاحية"""
    id: int
    search_count: Optional[int] = 0
    success_count: Optional[int] = 0
    success_rate: Optional[float] = 0.0
    total_results: Optional[int] = 0
    last_search_at: Optional[datetime] = None
    semantic_relations: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    category_name: Optional[str] = None

    class Config:
        orm_mode = True


# ===== مخططات نتائج البحث =====

class KeywordSearchResultBase(BaseModel):
    """النموذج الأساسي لنتيجة البحث"""
    keyword_id: int
    search_engine: str
    source_url: str = Field(..., max_length=500)
    title: Optional[str] = Field(None, max_length=500)
    snippet: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    trust_level: float = Field(0.0, ge=0.0, le=1.0)
    is_saved: bool = False
    metadata: Optional[Dict[str, Any]] = None


class KeywordSearchResultCreate(KeywordSearchResultBase):
    """نموذج إنشاء نتيجة بحث"""
    pass


class KeywordSearchResultUpdate(BaseModel):
    """نموذج تحديث نتيجة بحث"""
    title: Optional[str] = Field(None, max_length=500)
    snippet: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    trust_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_saved: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class KeywordSearchResultResponse(KeywordSearchResultBase):
    """نموذج استجابة نتيجة بحث"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ===== مخططات جلسات البحث =====

class KeywordSearchSessionBase(BaseModel):
    """النموذج الأساسي لجلسة البحث"""
    created_by: Optional[int] = None


class KeywordSearchSessionCreate(KeywordSearchSessionBase):
    """نموذج إنشاء جلسة بحث"""
    keywords: List[int]  # قائمة معرفات الكلمات المفتاحية


class KeywordSearchSessionUpdate(BaseModel):
    """نموذج تحديث جلسة بحث"""
    end_time: Optional[datetime] = None
    total_keywords: Optional[int] = None
    successful_keywords: Optional[int] = None
    total_results: Optional[int] = None
    saved_results: Optional[int] = None
    status: Optional[str] = None
    error_message: Optional[str] = None


class SessionKeywordUpdate(BaseModel):
    """نموذج تحديث كلمة مفتاحية في جلسة"""
    status: Optional[str] = None
    results_count: Optional[int] = None
    saved_count: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None


class SessionKeywordResponse(BaseModel):
    """نموذج استجابة كلمة مفتاحية في جلسة"""
    id: int
    session_id: int
    keyword_id: int
    keyword: str
    status: str
    results_count: int
    saved_count: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        orm_mode = True


class KeywordSearchSessionResponse(BaseModel):
    """نموذج استجابة جلسة بحث"""
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    total_keywords: int
    successful_keywords: int
    total_results: int
    saved_results: int
    status: str
    error_message: Optional[str] = None
    created_by: Optional[int] = None
    session_keywords: List[SessionKeywordResponse]

    class Config:
        orm_mode = True


# ===== مخططات الإحصائيات =====

class KeywordStatistics(BaseModel):
    """نموذج إحصائيات الكلمات المفتاحية"""
    total_keywords: int
    active_keywords: int
    avg_success_rate: float
    total_searches: int
    total_results: int
    most_successful_keywords: List[Dict[str, Any]]
    least_successful_keywords: List[Dict[str, Any]]


class KeywordAnalytics(BaseModel):
    """نموذج تحليلات الكلمات المفتاحية"""
    keyword_id: int
    keyword: str
    search_count: int
    success_rate: float
    total_results: int
    last_search_at: Optional[datetime] = None
    category_name: Optional[str] = None
    plant_type: Optional[str] = None
    condition_type: Optional[str] = None
    plant_part: Optional[str] = None


class KeywordAnalyticsResponse(BaseModel):
    """نموذج استجابة تحليلات الكلمات المفتاحية"""
    analytics: List[KeywordAnalytics]
    total_count: int
    page: int
    page_size: int
    total_pages: int
