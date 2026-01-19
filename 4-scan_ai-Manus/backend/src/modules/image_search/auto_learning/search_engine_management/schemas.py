# /home/ubuntu/image_search_integration/auto_learning/search_engine_management/schemas.py

"""
مخططات البيانات لنظام إدارة محركات البحث للبحث الذاتي الذكي

هذا الملف يحتوي على تعريفات مخططات البيانات المستخدمة في نظام إدارة محركات البحث،
لضمان التحقق من صحة البيانات المدخلة والمخرجة.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class RequestMethodEnum(str, Enum):
    """تعداد طرق الطلب"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class ResponseFormatEnum(str, Enum):
    """تعداد تنسيقات الاستجابة"""
    JSON = "JSON"
    XML = "XML"
    HTML = "HTML"
    TEXT = "TEXT"


class ParamTypeEnum(str, Enum):
    """تعداد أنواع المعلمات"""
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"


class LoadBalancerStrategyEnum(str, Enum):
    """تعداد استراتيجيات توزيع الحمل"""
    ROUND_ROBIN = "round_robin"
    WEIGHTED = "weighted"
    LEAST_USED = "least_used"
    PRIORITY = "priority"
    RANDOM = "random"


# ===== مخططات معلمات محرك البحث =====

class SearchEngineParameterBase(BaseModel):
    """النموذج الأساسي لمعلمة محرك البحث"""
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    param_type: ParamTypeEnum = ParamTypeEnum.STRING
    required: bool = False
    default_value: Optional[str] = None
    validation_regex: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None


class SearchEngineParameterCreate(SearchEngineParameterBase):
    """نموذج إنشاء معلمة محرك بحث"""
    engine_id: int


class SearchEngineParameterUpdate(BaseModel):
    """نموذج تحديث معلمة محرك بحث"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    display_name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    param_type: Optional[ParamTypeEnum] = None
    required: Optional[bool] = None
    default_value: Optional[str] = None
    validation_regex: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None


class SearchEngineParameterResponse(SearchEngineParameterBase):
    """نموذج استجابة معلمة محرك بحث"""
    id: int
    engine_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ===== مخططات محركات البحث =====

class SearchEngineBase(BaseModel):
    """النموذج الأساسي لمحرك البحث"""
    name: str = Field(..., min_length=2, max_length=100)
    display_name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None

    # إعدادات الاتصال
    base_url: str = Field(..., min_length=5, max_length=500)
    api_key_required: bool = False
    api_key: Optional[str] = Field(None, max_length=500)
    request_method: RequestMethodEnum = RequestMethodEnum.GET
    request_headers: Optional[Dict[str, str]] = None
    response_format: ResponseFormatEnum = ResponseFormatEnum.JSON

    # مسارات استخراج البيانات
    image_path: Optional[str] = Field(None, max_length=200)
    source_path: Optional[str] = Field(None, max_length=200)
    title_path: Optional[str] = Field(None, max_length=200)
    description_path: Optional[str] = Field(None, max_length=200)

    # إعدادات الأداء
    max_results_per_query: int = Field(10, ge=1, le=100)
    rate_limit: int = Field(60, ge=1)
    timeout: int = Field(30, ge=1, le=300)
    retry_count: int = Field(3, ge=0, le=10)
    retry_delay: int = Field(5, ge=1, le=60)

    # إعدادات توزيع الحمل
    weight: int = Field(1, ge=1, le=100)
    max_daily_requests: int = Field(1000, ge=1)

    # الحالة
    is_active: bool = True


class SearchEngineCreate(SearchEngineBase):
    """نموذج إنشاء محرك بحث"""
    parameters: Optional[List[SearchEngineParameterBase]] = None

    @classmethod
    @validator('base_url')
    def validate_base_url(cls, v):
        """التحقق من صحة عنوان URL الأساسي"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError(
                'يجب أن يبدأ عنوان URL الأساسي بـ http:// أو https://')
        return v


class SearchEngineUpdate(BaseModel):
    """نموذج تحديث محرك بحث"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    display_name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None

    # إعدادات الاتصال
    base_url: Optional[str] = Field(None, min_length=5, max_length=500)
    api_key_required: Optional[bool] = None
    api_key: Optional[str] = Field(None, max_length=500)
    request_method: Optional[RequestMethodEnum] = None
    request_headers: Optional[Dict[str, str]] = None
    response_format: Optional[ResponseFormatEnum] = None

    # مسارات استخراج البيانات
    image_path: Optional[str] = Field(None, max_length=200)
    source_path: Optional[str] = Field(None, max_length=200)
    title_path: Optional[str] = Field(None, max_length=200)
    description_path: Optional[str] = Field(None, max_length=200)

    # إعدادات الأداء
    max_results_per_query: Optional[int] = Field(None, ge=1, le=100)
    rate_limit: Optional[int] = Field(None, ge=1)
    timeout: Optional[int] = Field(None, ge=1, le=300)
    retry_count: Optional[int] = Field(None, ge=0, le=10)
    retry_delay: Optional[int] = Field(None, ge=1, le=60)

    # إعدادات توزيع الحمل
    weight: Optional[int] = Field(None, ge=1, le=100)
    max_daily_requests: Optional[int] = Field(None, ge=1)

    # الحالة
    is_active: Optional[bool] = None

    # معلمات محرك البحث
    parameters: Optional[List[SearchEngineParameterBase]] = None

    @classmethod
    @validator('base_url')
    def validate_base_url(cls, v):
        """التحقق من صحة عنوان URL الأساسي"""
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError(
                'يجب أن يبدأ عنوان URL الأساسي بـ http:// أو https://')
        return v


class SearchEngineResponse(SearchEngineBase):
    """نموذج استجابة محرك بحث"""
    id: int

    # إحصائيات الأداء
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_results: int = 0
    avg_response_time: float = 0.0
    current_daily_requests: int = 0
    last_request_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    last_failure_time: Optional[datetime] = None
    last_reset_date: Optional[datetime] = None

    # معلومات الإنشاء والتحديث
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    # معلمات محرك البحث
    parameters: Optional[List[SearchEngineParameterResponse]] = None

    class Config:
        orm_mode = True


# ===== مخططات سجل الاستخدام =====

class SearchEngineUsageLogBase(BaseModel):
    """النموذج الأساسي لسجل استخدام محرك البحث"""
    engine_id: int
    query: str = Field(..., max_length=500)
    parameters: Optional[Dict[str, Any]] = None
    response_time: Optional[float] = None
    status_code: Optional[int] = None
    results_count: int = 0
    is_successful: bool = True
    error_message: Optional[str] = None
    user_id: Optional[int] = None
    session_id: Optional[str] = Field(None, max_length=100)


class SearchEngineUsageLogCreate(SearchEngineUsageLogBase):
    """نموذج إنشاء سجل استخدام محرك بحث"""


class SearchEngineUsageLogResponse(SearchEngineUsageLogBase):
    """نموذج استجابة سجل استخدام محرك بحث"""
    id: int
    request_time: datetime
    created_at: datetime
    engine_name: Optional[str] = None

    class Config:
        orm_mode = True


# ===== مخططات سجل الصيانة =====

class SearchEngineMaintenanceLogBase(BaseModel):
    """النموذج الأساسي لسجل صيانة محرك البحث"""
    engine_id: int
    maintenance_type: str = Field(..., max_length=100)
    description: Optional[str] = None
    performed_by: Optional[int] = None
    is_successful: bool = True
    notes: Optional[str] = None


class SearchEngineMaintenanceLogCreate(SearchEngineMaintenanceLogBase):
    """نموذج إنشاء سجل صيانة محرك بحث"""


class SearchEngineMaintenanceLogUpdate(BaseModel):
    """نموذج تحديث سجل صيانة محرك بحث"""
    end_time: datetime
    is_successful: bool
    notes: Optional[str] = None


class SearchEngineMaintenanceLogResponse(SearchEngineMaintenanceLogBase):
    """نموذج استجابة سجل صيانة محرك بحث"""
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    created_at: datetime
    engine_name: Optional[str] = None

    class Config:
        orm_mode = True


# ===== مخططات موازن الحمل =====

class SearchEngineLoadBalancerMappingBase(BaseModel):
    """النموذج الأساسي لربط محرك البحث بموازن الحمل"""
    engine_id: int
    weight: int = Field(1, ge=1, le=100)
    priority: int = Field(0, ge=0, le=100)
    is_active: bool = True


class SearchEngineLoadBalancerMappingCreate(
        SearchEngineLoadBalancerMappingBase):
    """نموذج إنشاء ربط محرك البحث بموازن الحمل"""
    balancer_id: int


class SearchEngineLoadBalancerMappingUpdate(BaseModel):
    """نموذج تحديث ربط محرك البحث بموازن الحمل"""
    weight: Optional[int] = Field(None, ge=1, le=100)
    priority: Optional[int] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None


class SearchEngineLoadBalancerMappingResponse(
        SearchEngineLoadBalancerMappingBase):
    """نموذج استجابة ربط محرك البحث بموازن الحمل"""
    id: int
    balancer_id: int
    created_at: datetime
    updated_at: datetime
    engine_name: Optional[str] = None
    balancer_name: Optional[str] = None

    class Config:
        orm_mode = True


class SearchEngineLoadBalancerBase(BaseModel):
    """النموذج الأساسي لموازن الحمل لمحركات البحث"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    strategy: LoadBalancerStrategyEnum = LoadBalancerStrategyEnum.ROUND_ROBIN
    is_active: bool = True


class SearchEngineLoadBalancerCreate(SearchEngineLoadBalancerBase):
    """نموذج إنشاء موازن الحمل لمحركات البحث"""
    engine_mappings: Optional[List[SearchEngineLoadBalancerMappingBase]] = None


class SearchEngineLoadBalancerUpdate(BaseModel):
    """نموذج تحديث موازن الحمل لمحركات البحث"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    strategy: Optional[LoadBalancerStrategyEnum] = None
    is_active: Optional[bool] = None
    engine_mappings: Optional[List[SearchEngineLoadBalancerMappingBase]] = None


class SearchEngineLoadBalancerResponse(SearchEngineLoadBalancerBase):
    """نموذج استجابة موازن الحمل لمحركات البحث"""
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    engine_mappings: Optional[List[SearchEngineLoadBalancerMappingResponse]] = None

    class Config:
        orm_mode = True


# ===== مخططات الإحصائيات =====

class SearchEngineStatistics(BaseModel):
    """نموذج إحصائيات محركات البحث"""
    total_engines: int
    active_engines: int
    api_key_required_engines: int
    missing_api_key_engines: int
    total_requests_24h: int = 0
    successful_requests_24h: int = 0
    failed_requests_24h: int = 0
    avg_response_time_24h: float = 0.0
    most_used_engines: List[Dict[str, Any]] = []
    engines_by_response_format: Dict[str, int] = {}


class SearchEnginePerformanceMetrics(BaseModel):
    """نموذج مقاييس أداء محرك البحث"""
    engine_id: int
    name: str
    display_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    avg_response_time: float
    total_results: int
    avg_results_per_query: float
    last_request_time: Optional[datetime] = None


class SearchEnginePerformanceResponse(BaseModel):
    """نموذج استجابة مقاييس أداء محركات البحث"""
    metrics: List[SearchEnginePerformanceMetrics]
    total_count: int
    page: int
    page_size: int
    total_pages: int
