"""
ملف تكوين مديول الذاكرة المركزية

يحتوي هذا الملف على إعدادات وتكوينات مديول الذاكرة المركزية، بما في ذلك:
- إعدادات الاتصال بقاعدة البيانات
- تكوينات الذاكرة قصيرة وطويلة المدى
- إعدادات التكامل مع مديولات الذكاء الاصطناعي
- تكوينات الأمان والصلاحيات
- إعدادات التخزين والاسترجاع
"""

import os
from typing import Dict, List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# تحميل متغيرات البيئة
load_dotenv()


class MemoryDatabaseSettings(BaseModel):
    """إعدادات قاعدة بيانات الذاكرة"""
    connection_string: str = Field(
        default=os.getenv(
            "MEMORY_DB_CONNECTION_STRING",
            "sqlite:///memory.db"),
        description="سلسلة الاتصال بقاعدة بيانات الذاكرة")
    pool_size: int = Field(
        default=int(os.getenv("MEMORY_DB_POOL_SIZE", "10")),
        description="حجم تجمع الاتصالات"
    )
    max_overflow: int = Field(
        default=int(os.getenv("MEMORY_DB_MAX_OVERFLOW", "20")),
        description="الحد الأقصى للفيض"
    )
    pool_timeout: int = Field(
        default=int(os.getenv("MEMORY_DB_POOL_TIMEOUT", "30")),
        description="مهلة تجمع الاتصالات بالثواني"
    )
    pool_recycle: int = Field(
        default=int(os.getenv("MEMORY_DB_POOL_RECYCLE", "1800")),
        description="إعادة تدوير تجمع الاتصالات بالثواني"
    )


class MemoryRetentionSettings(BaseModel):
    """إعدادات الاحتفاظ بالذاكرة"""
    short_term_days: int = Field(
        default=int(os.getenv("MEMORY_SHORT_TERM_DAYS", "30")),
        description="عدد أيام الاحتفاظ بالذاكرة قصيرة المدى"
    )
    long_term_days: int = Field(
        default=int(os.getenv("MEMORY_LONG_TERM_DAYS", "365")),
        description="عدد أيام الاحتفاظ بالذاكرة طويلة المدى"
    )
    permanent_retention: bool = Field(
        default=os.getenv(
            "MEMORY_PERMANENT_RETENTION",
            "False").lower() == "true",
        description="الاحتفاظ الدائم بالذاكرة")
    auto_archive: bool = Field(
        default=os.getenv("MEMORY_AUTO_ARCHIVE", "True").lower() == "true",
        description="أرشفة تلقائية للذاكرة"
    )
    archive_frequency_days: int = Field(
        default=int(os.getenv("MEMORY_ARCHIVE_FREQUENCY_DAYS", "90")),
        description="تكرار الأرشفة بالأيام"
    )


class MemorySecuritySettings(BaseModel):
    """إعدادات أمان الذاكرة"""
    encryption_enabled: bool = Field(
        default=os.getenv(
            "MEMORY_ENCRYPTION_ENABLED",
            "True").lower() == "true",
        description="تمكين تشفير الذاكرة")
    encryption_algorithm: str = Field(
        default=os.getenv("MEMORY_ENCRYPTION_ALGORITHM", "AES-256"),
        description="خوارزمية التشفير"
    )
    access_control_enabled: bool = Field(
        default=os.getenv(
            "MEMORY_ACCESS_CONTROL_ENABLED",
            "True").lower() == "true",
        description="تمكين التحكم في الوصول")
    default_access_level: str = Field(
        default=os.getenv("MEMORY_DEFAULT_ACCESS_LEVEL", "private"),
        description="مستوى الوصول الافتراضي"
    )
    audit_logging: bool = Field(
        default=os.getenv("MEMORY_AUDIT_LOGGING", "True").lower() == "true",
        description="تسجيل تدقيق الوصول"
    )


class MemoryAIIntegrationSettings(BaseModel):
    """إعدادات تكامل الذكاء الاصطناعي"""
    enabled: bool = Field(
        default=os.getenv(
            "MEMORY_AI_INTEGRATION_ENABLED",
            "True").lower() == "true",
        description="تمكين تكامل الذكاء الاصطناعي")
    embedding_model: str = Field(
        default=os.getenv("MEMORY_EMBEDDING_MODEL", "text-embedding-3-small"),
        description="نموذج التضمين"
    )
    embedding_dimension: int = Field(
        default=int(os.getenv("MEMORY_EMBEDDING_DIMENSION", "1536")),
        description="أبعاد التضمين"
    )
    similarity_threshold: float = Field(
        default=float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.75")),
        description="عتبة التشابه"
    )
    max_tokens_per_chunk: int = Field(
        default=int(os.getenv("MEMORY_MAX_TOKENS_PER_CHUNK", "1000")),
        description="الحد الأقصى للرموز لكل جزء"
    )
    auto_summarization: bool = Field(
        default=os.getenv(
            "MEMORY_AUTO_SUMMARIZATION",
            "True").lower() == "true",
        description="تلخيص تلقائي")


class MemoryConfig(BaseModel):
    """التكوين الرئيسي لمديول الذاكرة"""
    module_name: str = "memory"
    module_version: str = "3.0.0"
    module_description: str = "مديول الذاكرة المركزية لنظام Gaara ERP"

    database: MemoryDatabaseSettings = MemoryDatabaseSettings()
    retention: MemoryRetentionSettings = MemoryRetentionSettings()
    security: MemorySecuritySettings = MemorySecuritySettings()
    ai_integration: MemoryAIIntegrationSettings = MemoryAIIntegrationSettings()

    # إعدادات عامة
    max_memory_size_mb: int = Field(
        default=int(
            os.getenv(
                "MEMORY_MAX_SIZE_MB",
                "10240")),
        # 10 GB افتراضياً
        description="الحد الأقصى لحجم الذاكرة بالميجابايت"
    )
    cache_enabled: bool = Field(
        default=os.getenv("MEMORY_CACHE_ENABLED", "True").lower() == "true",
        description="تمكين التخزين المؤقت"
    )
    cache_ttl_seconds: int = Field(
        default=int(os.getenv("MEMORY_CACHE_TTL_SECONDS", "3600")),
        description="مدة صلاحية التخزين المؤقت بالثواني"
    )

    # تكوينات التكامل مع المديولات الأخرى
    integrations: Dict[str, bool] = Field(
        default={
            "ai_agent_module": True,
            "plant_diagnosis": True,
            "image_search": True,
            "permissions": True,
            "auth": True,
        },
        description="تكوينات التكامل مع المديولات الأخرى"
    )

    def get_memory_types(self) -> List[str]:
        """الحصول على أنواع الذاكرة المدعومة"""
        return [
            "short_term",
            "long_term",
            "semantic",
            "episodic",
            "procedural"]

    def get_memory_categories(self) -> List[str]:
        """الحصول على فئات الذاكرة المدعومة"""
        return [
            "plant_data", "disease_data", "user_interaction",
            "system_event", "search_history", "diagnosis_result",
            "ai_agent_interaction", "external_source"
        ]

    def get_access_levels(self) -> List[str]:
        """الحصول على مستويات الوصول المدعومة"""
        return ["private", "group", "module", "system", "public"]

    def is_module_integration_enabled(self, module_name: str) -> bool:
        """التحقق مما إذا كان التكامل مع مديول معين ممكّناً"""
        return self.integrations.get(module_name, False)

    def to_dict(self) -> Dict:
        """تحويل التكوين إلى قاموس"""
        return self.dict()

    class Config:
        """تكوين النموذج"""
        validate_assignment = True
        arbitrary_types_allowed = True
        extra = "forbid"


# إنشاء كائن التكوين الافتراضي
default_config = MemoryConfig()
