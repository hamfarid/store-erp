"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/memory/schemas.py

مخططات البيانات لمديول الذاكرة المركزية

يحتوي هذا الملف على تعريفات مخططات البيانات لمديول الذاكرة المركزية، بما في ذلك:
- مخططات إنشاء وتحديث الذاكرة
- مخططات استجابة الذاكرة
- مخططات البحث في الذاكرة
- مخططات الإحصائيات
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
import enum

# Constants for repeated string literals
DESC_ADDITIONAL_METADATA = "بيانات وصفية إضافية"
DESC_MEMORY_TYPE = "نوع الذاكرة"
DESC_MEMORY_CATEGORY = "فئة الذاكرة"
DESC_MEMORY_ACCESS_LEVEL = "مستوى الوصول للذاكرة"
DESC_SOURCE_MODULE = "المديول المصدر"
DESC_TAGS_LIST = "قائمة العلامات"
DESC_USER_CREATOR_ID = "معرف المستخدم الذي أنشأ الذاكرة"
DESC_COUNT = "العدد"

# تعريفات الأنواع المستخدمة في المخططات


class MemoryTypeEnum(str, enum.Enum):
    """أنواع الذاكرة المدعومة"""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"


class MemoryCategoryEnum(str, enum.Enum):
    """فئات الذاكرة المدعومة"""
    PLANT_DATA = "plant_data"
    DISEASE_DATA = "disease_data"
    USER_INTERACTION = "user_interaction"
    SYSTEM_EVENT = "system_event"
    SEARCH_HISTORY = "search_history"
    DIAGNOSIS_RESULT = "diagnosis_result"
    AI_AGENT_INTERACTION = "ai_agent_interaction"
    EXTERNAL_SOURCE = "external_source"


class MemoryAccessEnum(str, enum.Enum):
    """مستويات الوصول للذاكرة"""
    PRIVATE = "private"
    GROUP = "group"
    MODULE = "module"
    SYSTEM = "system"
    PUBLIC = "public"


class MemoryActionEnum(str, enum.Enum):
    """أنواع الإجراءات على الذاكرة"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    ARCHIVE = "archive"
    RESTORE = "restore"
    SEARCH = "search"

# مخططات العلامات والكيانات


class TagBase(BaseModel):
    """المخطط الأساسي للعلامة"""
    name: str = Field(..., min_length=1, max_length=100, description="اسم العلامة")
    description: Optional[str] = Field(None, description="وصف العلامة")


class TagCreate(TagBase):
    """مخطط إنشاء العلامة"""
    pass


class TagResponse(TagBase):
    """مخطط استجابة العلامة"""
    id: int = Field(..., description="معرف العلامة")
    created_at: datetime = Field(..., description="تاريخ إنشاء العلامة")

    class Config:
        orm_mode = True


class EntityBase(BaseModel):
    """المخطط الأساسي للكيان"""
    name: str = Field(..., min_length=1, max_length=255, description="اسم الكيان")
    entity_type: str = Field(..., min_length=1, max_length=100, description="نوع الكيان")
    source: Optional[str] = Field(None, description="مصدر الكيان")
    meta_data: Optional[Dict[str, Any]] = Field(None, description=DESC_ADDITIONAL_METADATA)


class EntityCreate(EntityBase):
    """مخطط إنشاء الكيان"""
    pass


class EntityResponse(EntityBase):
    """مخطط استجابة الكيان"""
    id: int = Field(..., description="معرف الكيان")
    created_at: datetime = Field(..., description="تاريخ إنشاء الكيان")

    class Config:
        orm_mode = True

# مخططات الذاكرة


class MemoryBase(BaseModel):
    """المخطط الأساسي للذاكرة"""
    title: str = Field(..., min_length=1, max_length=255, description="عنوان الذاكرة")
    content: str = Field(..., min_length=1, description="محتوى الذاكرة")
    summary: Optional[str] = Field(None, description="ملخص الذاكرة")
    memory_type: MemoryTypeEnum = Field(..., description=DESC_MEMORY_TYPE)
    category: MemoryCategoryEnum = Field(..., description=DESC_MEMORY_CATEGORY)
    access_level: MemoryAccessEnum = Field(MemoryAccessEnum.PRIVATE, description=DESC_MEMORY_ACCESS_LEVEL)
    source_module: Optional[str] = Field(None, description=DESC_SOURCE_MODULE)
    source_id: Optional[str] = Field(None, description="معرف المصدر")
    source_url: Optional[str] = Field(None, description="رابط المصدر")
    importance_score: float = Field(0.0, ge=0.0, le=1.0, description="درجة أهمية الذاكرة")
    retention_days: int = Field(365, ge=1, description="عدد أيام الاحتفاظ بالذاكرة")
    meta_data: Optional[Dict[str, Any]] = Field(None, description=DESC_ADDITIONAL_METADATA)
    tags: Optional[List[str]] = Field(None, description=DESC_TAGS_LIST)


class MemoryCreate(MemoryBase):
    """مخطط إنشاء الذاكرة"""
    created_by: Optional[str] = Field(None, description=DESC_USER_CREATOR_ID)

    @validator('tags', pre=True, always=True)
    def set_tags(cls, v):
        """التحقق من صحة العلامات"""
        if v is None:
            return []
        return v


class MemoryUpdate(BaseModel):
    """مخطط تحديث الذاكرة"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="عنوان الذاكرة")
    content: Optional[str] = Field(None, min_length=1, description="محتوى الذاكرة")
    summary: Optional[str] = Field(None, description="ملخص الذاكرة")
    memory_type: Optional[MemoryTypeEnum] = Field(None, description=DESC_MEMORY_TYPE)
    category: Optional[MemoryCategoryEnum] = Field(None, description=DESC_MEMORY_CATEGORY)
    access_level: Optional[MemoryAccessEnum] = Field(None, description=DESC_MEMORY_ACCESS_LEVEL)
    source_module: Optional[str] = Field(None, description=DESC_SOURCE_MODULE)
    source_id: Optional[str] = Field(None, description="معرف المصدر")
    source_url: Optional[str] = Field(None, description="رابط المصدر")
    importance_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="درجة أهمية الذاكرة")
    retention_days: Optional[int] = Field(None, ge=1, description="عدد أيام الاحتفاظ بالذاكرة")
    meta_data: Optional[Dict[str, Any]] = Field(None, description=DESC_ADDITIONAL_METADATA)
    tags: Optional[List[str]] = Field(None, description=DESC_TAGS_LIST)
    is_archived: Optional[bool] = Field(None, description="حالة أرشفة الذاكرة")


class MemoryResponse(MemoryBase):
    """مخطط استجابة الذاكرة"""
    id: str = Field(..., description="معرف الذاكرة")
    created_by: Optional[str] = Field(None, description=DESC_USER_CREATOR_ID)
    created_at: datetime = Field(..., description="تاريخ إنشاء الذاكرة")
    updated_at: datetime = Field(..., description="تاريخ تحديث الذاكرة")
    expiry_date: Optional[datetime] = Field(None, description="تاريخ انتهاء صلاحية الذاكرة")
    is_archived: bool = Field(False, description="حالة أرشفة الذاكرة")
    is_deleted: bool = Field(False, description="حالة حذف الذاكرة")
    entities: List[EntityResponse] = Field([], description="قائمة الكيانات")
    tags: List[str] = Field([], description=DESC_TAGS_LIST)

    class Config:
        orm_mode = True


class MemoryList(BaseModel):
    """مخطط قائمة الذاكرة"""
    items: List[MemoryResponse] = Field(..., description="قائمة الذكريات")
    total: int = Field(..., description="العدد الإجمالي للذكريات")
    page: int = Field(1, description="رقم الصفحة الحالية")
    page_size: int = Field(10, description="حجم الصفحة")
    total_pages: int = Field(..., description="العدد الإجمالي للصفحات")

# مخططات البحث في الذاكرة


class MemorySearch(BaseModel):
    """مخطط البحث في الذاكرة"""
    query: Optional[str] = Field(None, description="نص البحث")
    memory_type: Optional[MemoryTypeEnum] = Field(None, description=DESC_MEMORY_TYPE)
    category: Optional[MemoryCategoryEnum] = Field(None, description=DESC_MEMORY_CATEGORY)
    access_level: Optional[MemoryAccessEnum] = Field(None, description=DESC_MEMORY_ACCESS_LEVEL)
    source_module: Optional[str] = Field(None, description=DESC_SOURCE_MODULE)
    tags: Optional[List[str]] = Field(None, description=DESC_TAGS_LIST)
    created_by: Optional[str] = Field(None, description=DESC_USER_CREATOR_ID)
    created_after: Optional[datetime] = Field(None, description="تاريخ الإنشاء بعد")
    created_before: Optional[datetime] = Field(None, description="تاريخ الإنشاء قبل")
    min_importance: Optional[float] = Field(None, ge=0.0, le=1.0, description="الحد الأدنى لدرجة الأهمية")
    include_archived: bool = Field(False, description="تضمين الذكريات المؤرشفة")
    include_deleted: bool = Field(False, description="تضمين الذكريات المحذوفة")
    semantic_search: bool = Field(False, description="تمكين البحث الدلالي")
    page: int = Field(1, ge=1, description="رقم الصفحة")
    page_size: int = Field(10, ge=1, le=100, description="حجم الصفحة")
    sort_by: str = Field("created_at", description="حقل الفرز")
    sort_order: str = Field("desc", description="ترتيب الفرز")


class SemanticSearchResult(BaseModel):
    """مخطط نتيجة البحث الدلالي"""
    memory: MemoryResponse = Field(..., description="الذاكرة")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="درجة التشابه")


class SemanticSearchResults(BaseModel):
    """مخطط نتائج البحث الدلالي"""
    items: List[SemanticSearchResult] = Field(..., description="قائمة نتائج البحث")
    total: int = Field(..., description="العدد الإجمالي للنتائج")
    query: str = Field(..., description="نص البحث")

# مخططات سجل الوصول للذاكرة


class MemoryAccessLogBase(BaseModel):
    """المخطط الأساسي لسجل الوصول للذاكرة"""
    memory_id: str = Field(..., description="معرف الذاكرة")
    user_id: Optional[str] = Field(None, description="معرف المستخدم")
    module: Optional[str] = Field(None, description="المديول")
    action: MemoryActionEnum = Field(..., description="الإجراء")
    ip_address: Optional[str] = Field(None, description="عنوان IP")
    user_agent: Optional[str] = Field(None, description="وكيل المستخدم")
    success: bool = Field(True, description="نجاح الإجراء")
    details: Optional[Dict[str, Any]] = Field(None, description="تفاصيل إضافية")


class MemoryAccessLogCreate(MemoryAccessLogBase):
    """مخطط إنشاء سجل الوصول للذاكرة"""
    pass


class MemoryAccessLogResponse(MemoryAccessLogBase):
    """مخطط استجابة سجل الوصول للذاكرة"""
    id: int = Field(..., description="معرف سجل الوصول")
    timestamp: datetime = Field(..., description="توقيت الإجراء")

    class Config:
        orm_mode = True

# مخططات إحصائيات الذاكرة


class MemoryTypeCount(BaseModel):
    """مخطط عدد الذكريات حسب النوع"""
    memory_type: MemoryTypeEnum = Field(..., description=DESC_MEMORY_TYPE)
    count: int = Field(..., description=DESC_COUNT)


class MemoryCategoryCount(BaseModel):
    """مخطط عدد الذكريات حسب الفئة"""
    category: MemoryCategoryEnum = Field(..., description=DESC_MEMORY_CATEGORY)
    count: int = Field(..., description=DESC_COUNT)


class MemoryAccessLevelCount(BaseModel):
    """مخطط عدد الذكريات حسب مستوى الوصول"""
    access_level: MemoryAccessEnum = Field(..., description=DESC_MEMORY_ACCESS_LEVEL)
    count: int = Field(..., description=DESC_COUNT)


class MemoryStats(BaseModel):
    """مخطط إحصائيات الذاكرة"""
    total_memories: int = Field(..., description="العدد الإجمالي للذكريات")
    active_memories: int = Field(..., description="عدد الذكريات النشطة")
    archived_memories: int = Field(..., description="عدد الذكريات المؤرشفة")
    deleted_memories: int = Field(..., description="عدد الذكريات المحذوفة")
    total_size_bytes: int = Field(..., description="الحجم الإجمالي بالبايت")
    avg_importance_score: float = Field(..., description="متوسط درجة الأهمية")
    memory_type_counts: List[MemoryTypeCount] = Field(..., description="عدد الذكريات حسب النوع")
    category_counts: List[MemoryCategoryCount] = Field(..., description="عدد الذكريات حسب الفئة")
    access_level_counts: List[MemoryAccessLevelCount] = Field(..., description="عدد الذكريات حسب مستوى الوصول")
    date: datetime = Field(..., description="تاريخ الإحصائيات")

    class Config:
        orm_mode = True
