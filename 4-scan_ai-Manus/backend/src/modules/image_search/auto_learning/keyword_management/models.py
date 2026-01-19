# /home/ubuntu/image_search_integration/auto_learning/keyword_management/models.py

"""
نماذج قاعدة البيانات لنظام إدارة الكلمات المفتاحية المتقدم للبحث الذاتي الذكي

هذا الملف يحتوي على تعريفات نماذج قاعدة البيانات المستخدمة في نظام إدارة الكلمات المفتاحية،
مع دعم التصنيف المتقدم حسب نوع النبات وأنواع الإصابات وأجزاء النبات.
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


class PlantPartEnum(str, enum.Enum):
    """تعداد أجزاء النبات"""
    LEAF = "LEAF"  # أوراق
    STEM = "STEM"  # ساق
    ROOT = "ROOT"  # جذور
    FRUIT = "FRUIT"  # ثمار
    FLOWER = "FLOWER"  # أزهار
    SEED = "SEED"  # بذور
    WHOLE_PLANT = "WHOLE_PLANT"  # النبات بالكامل


class ConditionTypeEnum(str, enum.Enum):
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


class KeywordCategory(Base):
    """نموذج فئة الكلمات المفتاحية"""
    __tablename__ = "keyword_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(20), nullable=True)  # لون الفئة (HEX code)
    icon = Column(String(50), nullable=True)  # أيقونة الفئة
    parent_id = Column(
        Integer,
        ForeignKey("keyword_categories.id"),
        nullable=True)  # الفئة الأب (للتصنيف الهرمي)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    keywords = relationship("SearchKeyword", back_populates="category")
    children = relationship(
        "KeywordCategory",
        backref="parent",
        remote_side=[id])


class SearchKeyword(Base):
    """نموذج الكلمة المفتاحية للبحث"""
    __tablename__ = "search_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(200), index=True, nullable=False)
    description = Column(Text, nullable=True)

    # التصنيف
    plant_type = Column(String(100), index=True, nullable=True)  # نوع النبات
    condition_type = Column(
        Enum(ConditionTypeEnum),
        index=True,
        nullable=True)  # نوع الإصابة
    plant_part = Column(
        Enum(PlantPartEnum),
        index=True,
        nullable=True)  # جزء النبات
    category_id = Column(
        Integer,
        ForeignKey("keyword_categories.id"),
        nullable=True)

    # إعدادات البحث
    priority = Column(Integer, default=0)  # أولوية البحث (أعلى = أهم)
    max_results = Column(Integer, default=50)  # الحد الأقصى لعدد النتائج
    min_trust_level = Column(Float, default=0.0)  # الحد الأدنى لمستوى الثقة
    # البحث في المصادر الموثوقة فقط
    trusted_sources_only = Column(Boolean, default=False)
    # محركات البحث المستخدمة (JSON array)
    search_engines = Column(JSON, nullable=True)

    # العلاقات الدلالية
    # العلاقات الدلالية مع كلمات مفتاحية أخرى
    semantic_relations = Column(JSON, nullable=True)

    # الإحصائيات
    search_count = Column(Integer, default=0)  # عدد مرات البحث
    success_count = Column(Integer, default=0)  # عدد مرات النجاح
    success_rate = Column(Float, default=0.0)  # معدل النجاح
    total_results = Column(Integer, default=0)  # إجمالي عدد النتائج
    last_search_at = Column(DateTime, nullable=True)  # آخر وقت بحث

    # الحالة
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # معرف المستخدم الذي أنشأ الكلمة المفتاحية
    created_by = Column(Integer, nullable=True)
    # معرف المستخدم الذي قام بآخر تحديث
    updated_by = Column(Integer, nullable=True)

    # العلاقات
    category = relationship("KeywordCategory", back_populates="keywords")
    search_results = relationship(
        "KeywordSearchResult",
        back_populates="keyword")
    condition_id = Column(
        Integer,
        ForeignKey("plant_conditions.id"),
        nullable=True)  # ربط بإصابة محددة
    condition = relationship("PlantCondition", back_populates="keywords")


class KeywordSearchResult(Base):
    """نموذج نتيجة البحث عن كلمة مفتاحية"""
    __tablename__ = "keyword_search_results"

    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(
        Integer,
        ForeignKey("search_keywords.id"),
        nullable=False)
    search_engine = Column(String(100), nullable=False)  # محرك البحث المستخدم
    source_url = Column(String(500), nullable=False)  # رابط المصدر
    title = Column(String(500), nullable=True)  # عنوان النتيجة
    snippet = Column(Text, nullable=True)  # مقتطف من النتيجة
    image_url = Column(String(500), nullable=True)  # رابط الصورة
    thumbnail_url = Column(String(500), nullable=True)  # رابط الصورة المصغرة
    trust_level = Column(Float, default=0.0)  # مستوى الثقة
    is_saved = Column(Boolean, default=False)  # هل تم حفظ النتيجة
    metadata = Column(JSON, nullable=True)  # بيانات وصفية إضافية
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    keyword = relationship("SearchKeyword", back_populates="search_results")


class KeywordSearchSession(Base):
    """نموذج جلسة البحث عن الكلمات المفتاحية"""
    __tablename__ = "keyword_search_sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    total_keywords = Column(Integer, default=0)
    successful_keywords = Column(Integer, default=0)
    total_results = Column(Integer, default=0)
    saved_results = Column(Integer, default=0)
    # running, completed, failed
    status = Column(String(50), default="running")
    error_message = Column(Text, nullable=True)
    # معرف المستخدم الذي بدأ الجلسة
    created_by = Column(Integer, nullable=True)

    # العلاقات
    session_keywords = relationship("SessionKeyword", back_populates="session")


class SessionKeyword(Base):
    """نموذج الكلمات المفتاحية في جلسة البحث"""
    __tablename__ = "session_keywords"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer,
        ForeignKey("keyword_search_sessions.id"),
        nullable=False)
    keyword_id = Column(
        Integer,
        ForeignKey("search_keywords.id"),
        nullable=False)
    # pending, running, completed, failed
    status = Column(String(50), default="pending")
    results_count = Column(Integer, default=0)
    saved_count = Column(Integer, default=0)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # العلاقات
    session = relationship(
        "KeywordSearchSession",
        back_populates="session_keywords")
    keyword = relationship("SearchKeyword")
