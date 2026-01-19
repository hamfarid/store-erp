# /home/ubuntu/image_search_integration/auto_learning/source_management/models.py

"""
نماذج قاعدة البيانات لنظام إدارة المصادر الموثوقة للبحث الذاتي الذكي

هذا الملف يحتوي على تعريفات نماذج قاعدة البيانات المستخدمة في نظام إدارة المصادر الموثوقة،
مع دعم تقييم ديناميكي لمستويات الثقة.
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


class SourceTypeEnum(str, enum.Enum):
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


class SourceCategory(Base):
    """نموذج فئة المصادر"""
    __tablename__ = "source_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(20), nullable=True)  # لون الفئة (HEX code)
    icon = Column(String(50), nullable=True)  # أيقونة الفئة
    parent_id = Column(
        Integer,
        ForeignKey("source_categories.id"),
        nullable=True)  # الفئة الأب (للتصنيف الهرمي)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # معرف المستخدم الذي أنشأ الفئة
    created_by = Column(Integer, nullable=True)
    # معرف المستخدم الذي قام بآخر تحديث
    updated_by = Column(Integer, nullable=True)

    # العلاقات
    sources = relationship("TrustedSource", back_populates="category")
    children = relationship(
        "SourceCategory",
        backref="parent",
        remote_side=[id])


class TrustedSource(Base):
    """نموذج المصدر الموثوق"""
    __tablename__ = "trusted_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True, nullable=False)
    url = Column(String(500), nullable=False)
    domain = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # التصنيف
    category_id = Column(
        Integer,
        ForeignKey("source_categories.id"),
        nullable=True)
    source_type = Column(
        Enum(SourceTypeEnum),
        index=True,
        nullable=True)  # نوع المصدر

    # مستوى الثقة والتصنيف
    trust_level = Column(Integer, default=50)  # مستوى الثقة (0-100)
    is_academic = Column(Boolean, default=False)  # هل المصدر أكاديمي
    is_government = Column(Boolean, default=False)  # هل المصدر حكومي
    is_commercial = Column(Boolean, default=False)  # هل المصدر تجاري

    # البيانات الوصفية
    metadata = Column(JSON, nullable=True)  # بيانات وصفية إضافية
    contact_info = Column(JSON, nullable=True)  # معلومات الاتصال

    # الإحصائيات
    usage_count = Column(Integer, default=0)  # عدد مرات الاستخدام
    success_count = Column(Integer, default=0)  # عدد مرات النجاح
    success_rate = Column(Float, default=0.0)  # معدل النجاح
    last_used_at = Column(DateTime, nullable=True)  # آخر وقت استخدام

    # الحالة
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # هل تم التحقق من المصدر
    verification_date = Column(DateTime, nullable=True)  # تاريخ التحقق
    verification_notes = Column(Text, nullable=True)  # ملاحظات التحقق
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # معرف المستخدم الذي أنشأ المصدر
    created_by = Column(Integer, nullable=True)
    # معرف المستخدم الذي قام بآخر تحديث
    updated_by = Column(Integer, nullable=True)

    # العلاقات
    category = relationship("SourceCategory", back_populates="sources")
    ratings = relationship("SourceRating", back_populates="source")
    blacklist_entries = relationship(
        "SourceBlacklistEntry",
        back_populates="source")
    verification_history = relationship(
        "SourceVerification", back_populates="source")


class SourceRating(Base):
    """نموذج تقييم المصدر"""
    __tablename__ = "source_ratings"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(
        Integer,
        ForeignKey("trusted_sources.id"),
        nullable=False)
    rating = Column(Integer, nullable=False)  # التقييم (0-100)
    comment = Column(Text, nullable=True)  # تعليق
    user_id = Column(Integer, nullable=True)  # معرف المستخدم الذي قام بالتقييم
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    source = relationship("TrustedSource", back_populates="ratings")


class SourceBlacklistEntry(Base):
    """نموذج إدخال القائمة السوداء للمصادر"""
    __tablename__ = "source_blacklist_entries"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(
        Integer,
        ForeignKey("trusted_sources.id"),
        nullable=False)
    reason = Column(Text, nullable=False)  # سبب الإدراج في القائمة السوداء
    start_date = Column(DateTime, default=datetime.now)  # تاريخ بدء الإدراج
    # تاريخ انتهاء الإدراج (null = دائم)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    # معرف المستخدم الذي أنشأ الإدخال
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    source = relationship("TrustedSource", back_populates="blacklist_entries")


class SourceVerification(Base):
    """نموذج تاريخ التحقق من المصدر"""
    __tablename__ = "source_verifications"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(
        Integer,
        ForeignKey("trusted_sources.id"),
        nullable=False)
    verification_date = Column(DateTime, default=datetime.now)  # تاريخ التحقق
    is_verified = Column(Boolean, default=False)  # نتيجة التحقق
    verification_method = Column(String(100), nullable=True)  # طريقة التحقق
    verification_notes = Column(Text, nullable=True)  # ملاحظات التحقق
    # معرف المستخدم الذي قام بالتحقق
    verified_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    source = relationship(
        "TrustedSource",
        back_populates="verification_history")


class SourceUsageLog(Base):
    """نموذج سجل استخدام المصدر"""
    __tablename__ = "source_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(
        Integer,
        ForeignKey("trusted_sources.id"),
        nullable=False)
    usage_date = Column(DateTime, default=datetime.now)  # تاريخ الاستخدام
    # نوع الاستخدام (search, verification, etc.)
    usage_type = Column(String(50), nullable=False)
    # معرف الكلمة المفتاحية المستخدمة (إن وجدت)
    keyword_id = Column(Integer, nullable=True)
    # معرف محرك البحث المستخدم (إن وجد)
    search_engine_id = Column(Integer, nullable=True)
    results_count = Column(Integer, default=0)  # عدد النتائج
    success = Column(Boolean, default=True)  # هل كان الاستخدام ناجحاً
    notes = Column(Text, nullable=True)  # ملاحظات
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    source = relationship("TrustedSource")
