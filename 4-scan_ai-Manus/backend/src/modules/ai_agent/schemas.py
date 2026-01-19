"""
/home/ubuntu/implemented_files/v3/src/modules/ai_agent/schemas.py

ملف مخططات البيانات لمديول وكلاء الذكاء الاصطناعي

يحتوي هذا الملف على تعريفات مخططات البيانات المستخدمة في مديول وكلاء الذكاء الاصطناعي،
بما في ذلك مخططات التحقق من صحة البيانات ومخططات الاستجابة.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

AGENT_TYPE_DESC = "نوع الوكيل"
AGENT_ROLE_DESC = "دور الوكيل"
AI_PROVIDER_DESC = "مزود خدمة الذكاء الاصطناعي"
IS_PUBLIC_DESC = "ما إذا كان الوكيل عاماً"
METADATA_DESC = "بيانات وصفية إضافية"
CAPABILITIES_DESC = "قائمة القدرات"
MODULES_DESC = "قائمة المديولات"
AGENT_STATUS_DESC = "حالة الوكيل"
AGENT_ID_DESC = "معرف الوكيل"
PAGE_NUM_DESC = "رقم الصفحة الحالية"
PAGE_SIZE_DESC = "حجم الصفحة"
TOTAL_PAGES_DESC = "العدد الإجمالي للصفحات"
USER_ID_DESC = "معرف المستخدم"
TASK_STATUS_DESC = "حالة المهمة"
OUTPUT_DATA_DESC = "بيانات الإخراج"
ERROR_MSG_DESC = "رسالة الخطأ"
EXECUTION_TIME_DESC = "وقت التنفيذ بالمللي ثانية"
TOKEN_USAGE_DESC = "استخدام الرموز"
TASK_ID_DESC = "معرف المهمة"
MESSAGES_DESC = "قائمة الرسائل"
CONVERSATION_ID_DESC = "معرف المحادثة"

# تعريفات الأنواع المستخدمة في المخططات


class AgentTypeEnum(str, Enum):
    """أنواع وكلاء الذكاء الاصطناعي"""
    ASSISTANT = "assistant"
    SPECIALIST = "specialist"
    SUPERVISOR = "supervisor"
    AUTONOMOUS = "autonomous"
    COLLABORATIVE = "collaborative"


class AgentRoleEnum(str, Enum):
    """أدوار وكلاء الذكاء الاصطناعي"""
    GENERAL = "general"
    PLANT_DIAGNOSIS = "plant_diagnosis"
    RESEARCH = "research"
    DATA_ANALYSIS = "data_analysis"
    CUSTOMER_SUPPORT = "customer_support"
    FARM_MANAGEMENT = "farm_management"
    INVENTORY_MANAGEMENT = "inventory_management"
    SALES_ASSISTANT = "sales_assistant"
    SYSTEM_ADMIN = "system_admin"
    DEVELOPER = "developer"


class AgentStatusEnum(str, Enum):
    """حالات وكلاء الذكاء الاصطناعي"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    TRAINING = "training"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class TaskStatusEnum(str, Enum):
    """حالات تنفيذ المهام"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class MessageRoleEnum(str, Enum):
    """أدوار الرسائل في المحادثات"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

# مخططات القدرات والمديولات


class CapabilityBase(BaseModel):
    """المخطط الأساسي للقدرة"""
    name: str = Field(..., min_length=1, max_length=100,
                      description="اسم القدرة")
    description: Optional[str] = Field(None, description="وصف القدرة")
    category: Optional[str] = Field(None, description="فئة القدرة")


class CapabilityCreate(CapabilityBase):
    """مخطط إنشاء القدرة"""


class CapabilityResponse(CapabilityBase):
    """مخطط استجابة القدرة"""
    id: int = Field(..., description="معرف القدرة")
    created_at: datetime = Field(..., description="تاريخ إنشاء القدرة")

    class Config:
        orm_mode = True


class ModuleBase(BaseModel):
    """المخطط الأساسي للمديول"""
    name: str = Field(..., min_length=1, max_length=100,
                      description="اسم المديول")
    description: Optional[str] = Field(None, description="وصف المديول")
    is_enabled: bool = Field(True, description="ما إذا كان المديول ممكّناً")


class ModuleCreate(ModuleBase):
    """مخطط إنشاء المديول"""


class ModuleResponse(ModuleBase):
    """مخطط استجابة المديول"""
    id: int = Field(..., description="معرف المديول")
    created_at: datetime = Field(..., description="تاريخ إنشاء المديول")

    class Config:
        orm_mode = True

# مخططات الوكلاء


class AIAgentBase(BaseModel):
    """المخطط الأساسي للوكيل"""
    name: str = Field(..., min_length=1, max_length=255,
                      description="اسم الوكيل")
    description: Optional[str] = Field(None, description="وصف الوكيل")
    agent_type: AgentTypeEnum = Field(..., description=AGENT_TYPE_DESC)
    role: AgentRoleEnum = Field(..., description=AGENT_ROLE_DESC)
    provider: str = Field(..., description=AI_PROVIDER_DESC)
    model: str = Field(..., description="نموذج الذكاء الاصطناعي")
    system_prompt: Optional[str] = Field(None, description="الرسالة النظامية")
    temperature: float = Field(
        0.7, ge=0.0, le=1.0, description="درجة حرارة النموذج")
    max_tokens: int = Field(2000, ge=1, description="الحد الأقصى للرموز")
    memory_retention: int = Field(
        10, ge=1, description="عدد الرسائل المحتفظ بها في الذاكرة")
    is_public: bool = Field(False, description=IS_PUBLIC_DESC)
    access_level: str = Field("private", description="مستوى الوصول")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)
    settings: Optional[Dict[str, Any]] = Field(
        None, description="إعدادات الوكيل")
    avatar_url: Optional[str] = Field(None, description="رابط الصورة الرمزية")
    capabilities: List[str] = Field([], description=CAPABILITIES_DESC)
    modules: List[str] = Field([], description=MODULES_DESC)


class AIAgentCreate(AIAgentBase):
    """مخطط إنشاء الوكيل"""
    capabilities: Optional[List[str]] = Field(
        None, description=CAPABILITIES_DESC)
    modules: Optional[List[str]] = Field(None, description=MODULES_DESC)

    @validator('capabilities', 'modules', pre=True, always=True)
    @classmethod
    def set_lists(cls, v):
        """التحقق من صحة القوائم"""
        if v is None:
            return []
        return v


class AIAgentUpdate(BaseModel):
    """مخطط تحديث الوكيل"""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="اسم الوكيل")
    description: Optional[str] = Field(None, description="وصف الوكيل")
    agent_type: Optional[AgentTypeEnum] = Field(
        None, description=AGENT_TYPE_DESC)
    role: Optional[AgentRoleEnum] = Field(None, description=AGENT_ROLE_DESC)
    status: Optional[AgentStatusEnum] = Field(
        None, description=AGENT_STATUS_DESC)
    provider: Optional[str] = Field(None, description=AI_PROVIDER_DESC)
    model: Optional[str] = Field(None, description="نموذج الذكاء الاصطناعي")
    system_prompt: Optional[str] = Field(None, description="الرسالة النظامية")
    temperature: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="درجة حرارة النموذج")
    max_tokens: Optional[int] = Field(
        None, ge=1, description="الحد الأقصى للرموز")
    memory_retention: Optional[int] = Field(
        None, ge=1, description="عدد الرسائل المحتفظ بها في الذاكرة")
    is_public: Optional[bool] = Field(None, description=IS_PUBLIC_DESC)
    access_level: Optional[str] = Field(None, description="مستوى الوصول")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)
    settings: Optional[Dict[str, Any]] = Field(
        None, description="إعدادات الوكيل")
    avatar_url: Optional[str] = Field(None, description="رابط الصورة الرمزية")
    capabilities: Optional[List[str]] = Field(
        None, description=CAPABILITIES_DESC)
    modules: Optional[List[str]] = Field(None, description=MODULES_DESC)


class AIAgentResponse(AIAgentBase):
    """مخطط استجابة الوكيل"""
    id: str = Field(..., description=AGENT_ID_DESC)
    status: AgentStatusEnum = Field(..., description=AGENT_STATUS_DESC)
    created_by: Optional[str] = Field(
        None, description="معرف المستخدم الذي أنشأ الوكيل")
    owner_id: Optional[str] = Field(None, description="معرف مالك الوكيل")
    created_at: datetime = Field(..., description="تاريخ إنشاء الوكيل")
    updated_at: datetime = Field(..., description="تاريخ تحديث الوكيل")
    last_used_at: Optional[datetime] = Field(
        None, description="تاريخ آخر استخدام")
    capabilities: List[str] = Field([], description=CAPABILITIES_DESC)
    modules: List[str] = Field([], description=MODULES_DESC)

    class Config:
        orm_mode = True


class AIAgentList(BaseModel):
    """مخطط قائمة الوكلاء"""
    items: List[AIAgentResponse] = Field(..., description="قائمة الوكلاء")
    total: int = Field(..., description="العدد الإجمالي للوكلاء")
    page: int = Field(1, description=PAGE_NUM_DESC)
    page_size: int = Field(10, description=PAGE_SIZE_DESC)
    total_pages: int = Field(..., description=TOTAL_PAGES_DESC)

# مخططات المهام


class AgentTaskBase(BaseModel):
    """المخطط الأساسي للمهمة"""
    agent_id: str = Field(..., description=AGENT_ID_DESC)
    task_type: str = Field(..., description="نوع المهمة")
    description: Optional[str] = Field(None, description="وصف المهمة")
    input_data: Optional[Dict[str, Any]] = Field(
        None, description="بيانات الإدخال")


class AgentTaskCreate(AgentTaskBase):
    """مخطط إنشاء المهمة"""
    user_id: Optional[str] = Field(None, description=USER_ID_DESC)


class AgentTaskUpdate(BaseModel):
    """مخطط تحديث المهمة"""
    status: Optional[TaskStatusEnum] = Field(
        None, description=TASK_STATUS_DESC)
    output_data: Optional[Dict[str, Any]] = Field(
        None, description=OUTPUT_DATA_DESC)
    error_message: Optional[str] = Field(None, description=ERROR_MSG_DESC)
    execution_time_ms: Optional[int] = Field(
        None, description=EXECUTION_TIME_DESC)
    token_usage: Optional[Dict[str, int]] = Field(
        None, description=TOKEN_USAGE_DESC)


class AgentTaskResponse(AgentTaskBase):
    """مخطط استجابة المهمة"""
    id: str = Field(..., description=TASK_ID_DESC)
    user_id: Optional[str] = Field(None, description=USER_ID_DESC)
    status: TaskStatusEnum = Field(..., description=TASK_STATUS_DESC)
    output_data: Optional[Dict[str, Any]] = Field(
        None, description=OUTPUT_DATA_DESC)
    error_message: Optional[str] = Field(None, description=ERROR_MSG_DESC)
    execution_time_ms: Optional[int] = Field(
        None, description=EXECUTION_TIME_DESC)
    token_usage: Optional[Dict[str, int]] = Field(
        None, description=TOKEN_USAGE_DESC)
    created_at: datetime = Field(..., description="تاريخ إنشاء المهمة")
    started_at: Optional[datetime] = Field(
        None, description="تاريخ بدء المهمة")
    completed_at: Optional[datetime] = Field(
        None, description="تاريخ اكتمال المهمة")

    class Config:
        orm_mode = True


class AgentTaskList(BaseModel):
    """مخطط قائمة المهام"""
    items: List[AgentTaskResponse] = Field(..., description="قائمة المهام")
    total: int = Field(..., description="العدد الإجمالي للمهام")
    page: int = Field(1, description=PAGE_NUM_DESC)
    page_size: int = Field(10, description=PAGE_SIZE_DESC)
    total_pages: int = Field(..., description=TOTAL_PAGES_DESC)

# مخططات المحادثات


class MessageBase(BaseModel):
    """المخطط الأساسي للرسالة"""
    role: MessageRoleEnum = Field(..., description="دور الرسالة")
    content: str = Field(..., description="محتوى الرسالة")
    timestamp: Optional[datetime] = Field(None, description="توقيت الرسالة")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)


class AgentConversationBase(BaseModel):
    """المخطط الأساسي للمحادثة"""
    agent_id: str = Field(..., description=AGENT_ID_DESC)
    title: Optional[str] = Field(None, description="عنوان المحادثة")


class AgentConversationCreate(AgentConversationBase):
    """مخطط إنشاء المحادثة"""
    user_id: Optional[str] = Field(None, description=USER_ID_DESC)
    messages: List[MessageBase] = Field([], description=MESSAGES_DESC)


class AgentConversationUpdate(BaseModel):
    """مخطط تحديث المحادثة"""
    title: Optional[str] = Field(None, description="عنوان المحادثة")
    messages: Optional[List[MessageBase]] = Field(
        None, description=MESSAGES_DESC)
    token_usage: Optional[Dict[str, int]] = Field(
        None, description=TOKEN_USAGE_DESC)


class AgentConversationResponse(AgentConversationBase):
    """مخطط استجابة المحادثة"""
    id: str = Field(..., description=CONVERSATION_ID_DESC)
    user_id: Optional[str] = Field(None, description=USER_ID_DESC)
    message_count: int = Field(0, description="عدد الرسائل")
    token_usage: Optional[Dict[str, int]] = Field(
        None, description=TOKEN_USAGE_DESC)
    created_at: datetime = Field(..., description="تاريخ إنشاء المحادثة")
    updated_at: datetime = Field(..., description="تاريخ تحديث المحادثة")
    last_message_at: Optional[datetime] = Field(
        None, description="تاريخ آخر رسالة")

    class Config:
        orm_mode = True


class AgentConversationDetailResponse(AgentConversationResponse):
    """مخطط استجابة تفاصيل المحادثة"""
    messages: List[MessageBase] = Field([], description=MESSAGES_DESC)


class AgentConversationList(BaseModel):
    """مخطط قائمة المحادثات"""
    items: List[AgentConversationResponse] = Field(
        ..., description="قائمة المحادثات")
    total: int = Field(..., description="العدد الإجمالي للمحادثات")
    page: int = Field(1, description=PAGE_NUM_DESC)
    page_size: int = Field(10, description=PAGE_SIZE_DESC)
    total_pages: int = Field(..., description=TOTAL_PAGES_DESC)

# مخططات التقييمات والإحصائيات


class AgentFeedbackBase(BaseModel):
    """المخطط الأساسي للتقييم"""
    agent_id: str = Field(..., description=AGENT_ID_DESC)
    rating: int = Field(..., ge=1, le=5, description="التقييم (1-5)")
    feedback_text: Optional[str] = Field(None, description="نص التقييم")
    categories: Optional[List[str]] = Field(None, description="فئات التقييم")


class AgentFeedbackCreate(AgentFeedbackBase):
    """مخطط إنشاء التقييم"""
    user_id: Optional[str] = Field(None, description=USER_ID_DESC)
    task_id: Optional[str] = Field(None, description=TASK_ID_DESC)
    conversation_id: Optional[str] = Field(
        None, description=CONVERSATION_ID_DESC)


class AgentFeedbackResponse(AgentFeedbackBase):
    """مخطط استجابة التقييم"""
    id: int = Field(..., description="معرف التقييم")
    user_id: Optional[str] = Field(None, description=USER_ID_DESC)
    task_id: Optional[str] = Field(None, description=TASK_ID_DESC)
    conversation_id: Optional[str] = Field(
        None, description=CONVERSATION_ID_DESC)
    created_at: datetime = Field(..., description="تاريخ إنشاء التقييم")

    class Config:
        orm_mode = True


class AgentStatsBase(BaseModel):
    """المخطط الأساسي للإحصائيات"""
    agent_id: str = Field(..., description=AGENT_ID_DESC)
    date: datetime = Field(..., description="تاريخ الإحصائيات")
    task_count: int = Field(0, description="عدد المهام")
    successful_tasks: int = Field(0, description="عدد المهام الناجحة")
    failed_tasks: int = Field(0, description="عدد المهام الفاشلة")
    avg_execution_time_ms: float = Field(
        0.0, description="متوسط وقت التنفيذ بالمللي ثانية")
    total_tokens: int = Field(0, description="إجمالي الرموز")
    prompt_tokens: int = Field(0, description="رموز الإدخال")
    completion_tokens: int = Field(0, description="رموز الإخراج")
    estimated_cost: float = Field(0.0, description="التكلفة التقديرية")
    unique_users: int = Field(0, description="عدد المستخدمين الفريدين")
    user_satisfaction: Optional[float] = Field(
        None, description="رضا المستخدمين")


class AgentStatsResponse(AgentStatsBase):
    """مخطط استجابة الإحصائيات"""
    id: int = Field(..., description="معرف الإحصائيات")

    class Config:
        orm_mode = True

# مخططات البحث والتصفية


class AIAgentSearch(BaseModel):
    """مخطط البحث في الوكلاء"""
    query: Optional[str] = Field(None, description="نص البحث")
    agent_type: Optional[AgentTypeEnum] = Field(
        None, description=AGENT_TYPE_DESC)
    role: Optional[AgentRoleEnum] = Field(None, description=AGENT_ROLE_DESC)
    status: Optional[AgentStatusEnum] = Field(
        None, description=AGENT_STATUS_DESC)
    provider: Optional[str] = Field(None, description=AI_PROVIDER_DESC)
    is_public: Optional[bool] = Field(None, description=IS_PUBLIC_DESC)
    capabilities: Optional[List[str]] = Field(
        None, description=CAPABILITIES_DESC)
    modules: Optional[List[str]] = Field(None, description=MODULES_DESC)
    created_by: Optional[str] = Field(
        None, description="معرف المستخدم الذي أنشأ الوكيل")
    owner_id: Optional[str] = Field(None, description="معرف مالك الوكيل")
    page: int = Field(1, ge=1, description=PAGE_NUM_DESC)
    page_size: int = Field(10, ge=1, le=100, description=PAGE_SIZE_DESC)
    sort_by: str = Field("created_at", description="حقل الفرز")
    sort_order: str = Field("desc", description="ترتيب الفرز")

# مخططات التفاعل مع الوكلاء


class AgentMessageRequest(BaseModel):
    """مخطط طلب إرسال رسالة للوكيل"""
    agent_id: str = Field(..., description=AGENT_ID_DESC)
    conversation_id: Optional[str] = Field(
        None, description=CONVERSATION_ID_DESC)
    message: str = Field(..., description="نص الرسالة")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)


class AgentMessageResponse(BaseModel):
    """مخطط استجابة الرسالة من الوكيل"""
    conversation_id: str = Field(..., description=CONVERSATION_ID_DESC)
    message: MessageBase = Field(..., description="الرسالة")
    token_usage: Optional[Dict[str, int]] = Field(
        None, description=TOKEN_USAGE_DESC)
    execution_time_ms: Optional[int] = Field(
        None, description=EXECUTION_TIME_DESC)


class AgentTaskRequest(BaseModel):
    """مخطط طلب تنفيذ مهمة بواسطة الوكيل"""
    agent_id: str = Field(..., description=AGENT_ID_DESC)
    task_type: str = Field(..., description="نوع المهمة")
    description: Optional[str] = Field(None, description="وصف المهمة")
    input_data: Dict[str, Any] = Field(..., description="بيانات الإدخال")
    async_execution: bool = Field(
        False, description="ما إذا كان التنفيذ غير متزامن")


class AgentTaskResultResponse(BaseModel):
    """مخطط استجابة نتيجة المهمة"""
    task_id: str = Field(..., description=TASK_ID_DESC)
    status: TaskStatusEnum = Field(..., description=TASK_STATUS_DESC)
    output_data: Optional[Dict[str, Any]] = Field(
        None, description=OUTPUT_DATA_DESC)
    error_message: Optional[str] = Field(None, description=ERROR_MSG_DESC)
    execution_time_ms: Optional[int] = Field(
        None, description=EXECUTION_TIME_DESC)
    token_usage: Optional[Dict[str, int]] = Field(
        None, description=TOKEN_USAGE_DESC)
