# /home/ubuntu/image_search_integration/auto_learning/search_engine_management/models.py

"""
نماذج قاعدة البيانات لنظام إدارة محركات البحث للبحث الذاتي الذكي

هذا الملف يحتوي على تعريفات نماذج قاعدة البيانات المستخدمة في نظام إدارة محركات البحث،
مع دعم توزيع الحمل والتوازن ومراقبة الأداء.
"""

import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RequestMethodEnum(str, enum.Enum):
    """تعداد طرق الطلب"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class ResponseFormatEnum(str, enum.Enum):
    """تعداد تنسيقات الاستجابة"""
    JSON = "JSON"
    XML = "XML"
    HTML = "HTML"
    TEXT = "TEXT"


class ParamTypeEnum(str, enum.Enum):
    """تعداد أنواع المعلمات"""
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"


class SearchEngine(Base):
    """نموذج محرك البحث"""
    __tablename__ = "search_engines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # إعدادات الاتصال
    base_url = Column(String(500), nullable=False)
    api_key_required = Column(Boolean, default=False)
    api_key = Column(String(500), nullable=True)
    request_method = Column(
        Enum(RequestMethodEnum),
        default=RequestMethodEnum.GET)
    request_headers = Column(JSON, nullable=True)
    response_format = Column(
        Enum(ResponseFormatEnum),
        default=ResponseFormatEnum.JSON)

    # مسارات استخراج البيانات
    # مسار استخراج الصورة من الاستجابة
    image_path = Column(String(200), nullable=True)
    # مسار استخراج المصدر من الاستجابة
    source_path = Column(String(200), nullable=True)
    # مسار استخراج العنوان من الاستجابة
    title_path = Column(String(200), nullable=True)
    # مسار استخراج الوصف من الاستجابة
    description_path = Column(String(200), nullable=True)

    # إعدادات الأداء
    # الحد الأقصى لعدد النتائج لكل استعلام
    max_results_per_query = Column(Integer, default=10)
    # الحد الأقصى لعدد الطلبات في الدقيقة
    rate_limit = Column(Integer, default=60)
    timeout = Column(Integer, default=30)  # مهلة الاتصال بالثواني
    retry_count = Column(Integer, default=3)  # عدد محاولات إعادة المحاولة
    retry_delay = Column(Integer, default=5)  # التأخير بين المحاولات بالثواني

    # إعدادات توزيع الحمل
    # وزن محرك البحث في توزيع الحمل (أعلى = أولوية أعلى)
    weight = Column(Integer, default=1)
    # الحد الأقصى لعدد الطلبات اليومية
    max_daily_requests = Column(Integer, default=1000)
    current_daily_requests = Column(
        Integer, default=0)  # عدد الطلبات الحالية اليوم
    # تاريخ آخر إعادة تعيين للعداد
    last_reset_date = Column(DateTime, nullable=True)

    # إحصائيات الأداء
    total_requests = Column(Integer, default=0)  # إجمالي عدد الطلبات
    successful_requests = Column(Integer, default=0)  # عدد الطلبات الناجحة
    failed_requests = Column(Integer, default=0)  # عدد الطلبات الفاشلة
    total_results = Column(Integer, default=0)  # إجمالي عدد النتائج
    # متوسط وقت الاستجابة بالثواني
    avg_response_time = Column(Float, default=0.0)
    last_request_time = Column(DateTime, nullable=True)  # وقت آخر طلب
    last_success_time = Column(DateTime, nullable=True)  # وقت آخر طلب ناجح
    last_failure_time = Column(DateTime, nullable=True)  # وقت آخر طلب فاشل
    last_error_message = Column(Text, nullable=True)  # رسالة آخر خطأ

    # الحالة
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # معرف المستخدم الذي أنشأ محرك البحث
    created_by = Column(Integer, nullable=True)
    # معرف المستخدم الذي قام بآخر تحديث
    updated_by = Column(Integer, nullable=True)

    # العلاقات
    parameters = relationship("SearchEngineParameter", back_populates="engine")
    usage_logs = relationship("SearchEngineUsageLog", back_populates="engine")
    maintenance_logs = relationship(
        "SearchEngineMaintenanceLog",
        back_populates="engine")


class SearchEngineParameter(Base):
    """نموذج معلمة محرك البحث"""
    __tablename__ = "search_engine_parameters"

    id = Column(Integer, primary_key=True, index=True)
    engine_id = Column(
        Integer,
        ForeignKey("search_engines.id"),
        nullable=False)
    name = Column(String(100), nullable=False)  # اسم المعلمة في الطلب
    display_name = Column(String(200), nullable=False)  # اسم العرض
    description = Column(Text, nullable=True)  # وصف المعلمة
    param_type = Column(
        Enum(ParamTypeEnum),
        default=ParamTypeEnum.STRING)  # نوع المعلمة
    required = Column(Boolean, default=False)  # هل المعلمة مطلوبة
    default_value = Column(String(500), nullable=True)  # القيمة الافتراضية
    # تعبير منتظم للتحقق من صحة القيمة
    validation_regex = Column(String(500), nullable=True)
    options = Column(JSON, nullable=True)  # خيارات القيمة (للقوائم المنسدلة)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    engine = relationship("SearchEngine", back_populates="parameters")


class SearchEngineUsageLog(Base):
    """نموذج سجل استخدام محرك البحث"""
    __tablename__ = "search_engine_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    engine_id = Column(
        Integer,
        ForeignKey("search_engines.id"),
        nullable=False)
    query = Column(String(500), nullable=False)  # الاستعلام المستخدم
    parameters = Column(JSON, nullable=True)  # المعلمات المستخدمة
    request_time = Column(DateTime, default=datetime.now)  # وقت الطلب
    response_time = Column(Float, nullable=True)  # وقت الاستجابة بالثواني
    status_code = Column(Integer, nullable=True)  # رمز حالة الاستجابة
    results_count = Column(Integer, default=0)  # عدد النتائج
    is_successful = Column(Boolean, default=True)  # هل كان الطلب ناجحاً
    error_message = Column(Text, nullable=True)  # رسالة الخطأ (إن وجدت)
    user_id = Column(Integer, nullable=True)  # معرف المستخدم الذي قام بالطلب
    session_id = Column(String(100), nullable=True)  # معرف الجلسة
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    engine = relationship("SearchEngine", back_populates="usage_logs")


class SearchEngineMaintenanceLog(Base):
    """نموذج سجل صيانة محرك البحث"""
    __tablename__ = "search_engine_maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)
    engine_id = Column(
        Integer,
        ForeignKey("search_engines.id"),
        nullable=False)
    # نوع الصيانة (تحديث، إعادة تعيين، إلخ)
    maintenance_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)  # وصف الصيانة
    # معرف المستخدم الذي قام بالصيانة
    performed_by = Column(Integer, nullable=True)
    start_time = Column(DateTime, default=datetime.now)  # وقت بدء الصيانة
    end_time = Column(DateTime, nullable=True)  # وقت انتهاء الصيانة
    is_successful = Column(Boolean, default=True)  # هل كانت الصيانة ناجحة
    notes = Column(Text, nullable=True)  # ملاحظات إضافية
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    engine = relationship("SearchEngine", back_populates="maintenance_logs")


class SearchEngineLoadBalancer(Base):
    """نموذج موازن الحمل لمحركات البحث"""
    __tablename__ = "search_engine_load_balancers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    # استراتيجية توزيع الحمل (round_robin, weighted, least_used)
    strategy = Column(String(50), default="round_robin")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # معرف المستخدم الذي أنشأ الموازن
    created_by = Column(Integer, nullable=True)
    # معرف المستخدم الذي قام بآخر تحديث
    updated_by = Column(Integer, nullable=True)

    # العلاقات
    engine_mappings = relationship(
        "SearchEngineLoadBalancerMapping",
        back_populates="balancer")


class SearchEngineLoadBalancerMapping(Base):
    """نموذج ربط محرك البحث بموازن الحمل"""
    __tablename__ = "search_engine_load_balancer_mappings"

    id = Column(Integer, primary_key=True, index=True)
    balancer_id = Column(
        Integer,
        ForeignKey("search_engine_load_balancers.id"),
        nullable=False)
    engine_id = Column(
        Integer,
        ForeignKey("search_engines.id"),
        nullable=False)
    weight = Column(Integer, default=1)  # وزن محرك البحث في هذا الموازن
    priority = Column(Integer, default=0)  # أولوية محرك البحث (أعلى = أهم)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    balancer = relationship(
        "SearchEngineLoadBalancer",
        back_populates="engine_mappings")
    engine = relationship("SearchEngine")
