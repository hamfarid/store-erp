"""
/home/ubuntu/implemented_files/v3/src/modules/ai_agent/config.py

ملف تكوين مديول وكلاء الذكاء الاصطناعي

يحتوي هذا الملف على إعدادات تكوين مديول وكلاء الذكاء الاصطناعي، بما في ذلك:
- إعدادات الاتصال بخدمات الذكاء الاصطناعي
- إعدادات الوكلاء الافتراضية
- إعدادات المراقبة والتسجيل
- إعدادات التكامل مع المديولات الأخرى
"""

from typing import Dict
import os

from pydantic import BaseModel, Field, validator


class AIProviderConfig(BaseModel):
    """تكوين مزود خدمة الذكاء الاصطناعي"""
    name: str = Field(..., description="اسم مزود الخدمة")
    api_key_env_var: str = Field(..., description="متغير البيئة لمفتاح API")
    api_base_url: str = Field(..., description="عنوان URL الأساسي لواجهة API")
    timeout_seconds: int = Field(30, description="مهلة الاتصال بالثواني")
    retry_attempts: int = Field(3, description="عدد محاولات إعادة المحاولة")
    models: Dict[str, Dict[str, str | int | float | bool]] = Field(default_factory=dict, description="النماذج المتاحة وإعداداتها")
    is_enabled: bool = Field(True, description="ما إذا كان المزود ممكّناً")

    @validator('api_key_env_var')
    @classmethod
    def validate_api_key_env_var(cls, v):
        """التحقق من وجود متغير البيئة لمفتاح API"""
        if not os.environ.get(v):
            # تسجيل تحذير بدلاً من رفع استثناء
            print(f"تحذير: متغير البيئة {v} غير موجود")
        return v


class AgentConfig(BaseModel):
    """تكوين الوكيل الافتراضي"""
    default_model: str = Field("gpt-4", description="النموذج الافتراضي")
    default_temperature: float = Field(0.7, description="درجة حرارة النموذج الافتراضية")
    default_max_tokens: int = Field(2000, description="الحد الأقصى للرموز الافتراضي")
    default_timeout_seconds: int = Field(60, description="مهلة تنفيذ المهمة الافتراضية بالثواني")
    default_memory_retention: int = Field(10, description="عدد الرسائل المحتفظ بها في الذاكرة افتراضياً")
    default_system_prompt: str = Field("أنت مساعد ذكي يساعد المستخدمين في نظام Gaara ERP.", description="الرسالة النظامية الافتراضية")
    max_conversation_tokens: int = Field(8000, description="الحد الأقصى لرموز المحادثة")
    enable_function_calling: bool = Field(True, description="تمكين استدعاء الدوال")
    enable_streaming: bool = Field(True, description="تمكين البث المباشر للاستجابات")
    enable_logging: bool = Field(True, description="تمكين تسجيل المحادثات")


class MonitoringConfig(BaseModel):
    """تكوين مراقبة الوكلاء"""
    enable_performance_tracking: bool = Field(True, description="تمكين تتبع الأداء")
    enable_error_tracking: bool = Field(True, description="تمكين تتبع الأخطاء")
    log_level: str = Field("INFO", description="مستوى التسجيل")
    performance_metrics_retention_days: int = Field(90, description="مدة الاحتفاظ بمقاييس الأداء بالأيام")
    alert_on_error: bool = Field(True, description="إرسال تنبيهات عند حدوث أخطاء")
    alert_on_high_latency: bool = Field(True, description="إرسال تنبيهات عند ارتفاع زمن الاستجابة")
    high_latency_threshold_ms: int = Field(5000, description="عتبة زمن الاستجابة المرتفع بالمللي ثانية")
    sampling_rate: float = Field(0.1, description="معدل أخذ العينات للمراقبة المفصلة")


class IntegrationConfig(BaseModel):
    """تكوين تكامل الوكلاء مع المديولات الأخرى"""
    memory_module_enabled: bool = Field(True, description="تمكين التكامل مع مديول الذاكرة")
    a2a_module_enabled: bool = Field(True, description="تمكين التكامل مع مديول A2A")
    permissions_module_enabled: bool = Field(True, description="تمكين التكامل مع مديول الصلاحيات")
    telegram_bot_enabled: bool = Field(False, description="تمكين التكامل مع بوت تيليجرام")
    enable_cross_module_function_calling: bool = Field(True, description="تمكين استدعاء دوال المديولات الأخرى")
    enable_agent_collaboration: bool = Field(True, description="تمكين التعاون بين الوكلاء")


class AIAgentConfig(BaseModel):
    """التكوين الرئيسي لمديول وكلاء الذكاء الاصطناعي"""
    providers: Dict[str, AIProviderConfig] = Field(default_factory=dict, description="مزودو خدمات الذكاء الاصطناعي")
    default_provider: str = Field("openai", description="مزود الخدمة الافتراضي")
    agent: AgentConfig = Field(default_factory=AgentConfig, description="تكوين الوكيل الافتراضي")
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig, description="تكوين المراقبة")
    integration: IntegrationConfig = Field(default_factory=IntegrationConfig, description="تكوين التكامل")
    enable_module: bool = Field(True, description="تمكين المديول")
    debug_mode: bool = Field(False, description="وضع التصحيح")
    cache_enabled: bool = Field(True, description="تمكين التخزين المؤقت للاستجابات")
    cache_ttl_seconds: int = Field(3600, description="مدة صلاحية التخزين المؤقت بالثواني")
    rate_limit_per_minute: int = Field(60, description="حد معدل الطلبات في الدقيقة")
    max_parallel_requests: int = Field(10, description="الحد الأقصى للطلبات المتوازية")


# تكوين مزودي خدمات الذكاء الاصطناعي
openai_provider = AIProviderConfig(
    name="OpenAI",
    api_key_env_var="OPENAI_API_KEY",
    api_base_url="https://api.openai.com/v1",
    models={
        "gpt-4": {
            "description": "أحدث نموذج GPT-4 من OpenAI",
            "max_tokens": 8192,
            "supports_function_calling": True,
            "supports_vision": False,
            "cost_per_1k_tokens_input": 0.03,
            "cost_per_1k_tokens_output": 0.06
        },
        "gpt-4-vision": {
            "description": "نموذج GPT-4 مع دعم الرؤية",
            "max_tokens": 8192,
            "supports_function_calling": True,
            "supports_vision": True,
            "cost_per_1k_tokens_input": 0.03,
            "cost_per_1k_tokens_output": 0.06
        },
        "gpt-3.5-turbo": {
            "description": "نموذج GPT-3.5 Turbo من OpenAI",
            "max_tokens": 4096,
            "supports_function_calling": True,
            "supports_vision": False,
            "cost_per_1k_tokens_input": 0.0015,
            "cost_per_1k_tokens_output": 0.002
        }
    }
)

anthropic_provider = AIProviderConfig(
    name="Anthropic",
    api_key_env_var="ANTHROPIC_API_KEY",
    api_base_url="https://api.anthropic.com/v1",
    models={
        "claude-3-opus": {
            "description": "أحدث نموذج Claude 3 Opus من Anthropic",
            "max_tokens": 100000,
            "supports_function_calling": True,
            "supports_vision": True,
            "cost_per_1k_tokens_input": 0.015,
            "cost_per_1k_tokens_output": 0.075
        },
        "claude-3-sonnet": {
            "description": "نموذج Claude 3 Sonnet من Anthropic",
            "max_tokens": 100000,
            "supports_function_calling": True,
            "supports_vision": True,
            "cost_per_1k_tokens_input": 0.003,
            "cost_per_1k_tokens_output": 0.015
        }
    }
)

# التكوين الافتراضي
default_config = AIAgentConfig(
    providers={
        "openai": openai_provider,
        "anthropic": anthropic_provider
    },
    default_provider="openai",
    agent=AgentConfig(
        default_model="gpt-4",
        default_temperature=0.7,
        default_max_tokens=2000,
        default_system_prompt="أنت مساعد ذكي يساعد المستخدمين في نظام Gaara ERP الزراعي. يجب أن تكون إجاباتك دقيقة ومفيدة ومختصرة."
    ),
    monitoring=MonitoringConfig(
        log_level="INFO",
        performance_metrics_retention_days=90
    ),
    integration=IntegrationConfig(
        memory_module_enabled=True,
        a2a_module_enabled=True,
        permissions_module_enabled=True
    ),
    enable_module=True,
    debug_mode=False,
    cache_enabled=True,
    cache_ttl_seconds=3600,
    rate_limit_per_minute=60,
    max_parallel_requests=10
)

# تصدير الدوال والكائنات
__all__ = ['AIAgentConfig', 'default_config']
