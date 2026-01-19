# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/feedback/models.py
"""
نماذج قاعدة البيانات لوحدة التغذية الراجعة
توفر هذه الوحدة نماذج قاعدة البيانات اللازمة لتخزين وإدارة التغذية الراجعة من المستخدمين
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.database import Base

from .config import FeedbackPriority, FeedbackStatus, FeedbackType


class Feedback(Base):
    """نموذج التغذية الراجعة"""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    priority = Column(Enum(FeedbackPriority), default=FeedbackPriority.MEDIUM)
    status = Column(Enum(FeedbackStatus), default=FeedbackStatus.NEW)

    # معلومات المستخدم
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="feedback")

    # معلومات الوحدة
    module_name = Column(String(100), nullable=True)

    # معلومات التتبع
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    # العلاقات
    comments = relationship(
        "FeedbackComment",
        back_populates="feedback",
        cascade="all, delete-orphan")
    attachments = relationship(
        "FeedbackAttachment",
        back_populates="feedback",
        cascade="all, delete-orphan")
    votes = relationship(
        "FeedbackVote",
        back_populates="feedback",
        cascade="all, delete-orphan")


class FeedbackComment(Base):
    """نموذج تعليقات التغذية الراجعة"""
    __tablename__ = "feedback_comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    # العلاقات
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    feedback = relationship("Feedback", back_populates="comments")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User")

    # معلومات التتبع
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class FeedbackAttachment(Base):
    """نموذج مرفقات التغذية الراجعة"""
    __tablename__ = "feedback_attachments"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)  # حجم الملف بالبايت

    # العلاقات
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    feedback = relationship("Feedback", back_populates="attachments")

    # معلومات التتبع
    created_at = Column(DateTime, default=datetime.utcnow)


class FeedbackVote(Base):
    """نموذج تصويتات التغذية الراجعة"""
    __tablename__ = "feedback_votes"

    id = Column(Integer, primary_key=True, index=True)
    is_upvote = Column(Boolean, default=True)

    # العلاقات
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    feedback = relationship("Feedback", back_populates="votes")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    # معلومات التتبع
    created_at = Column(DateTime, default=datetime.utcnow)


class FeedbackTag(Base):
    """نموذج وسوم التغذية الراجعة"""
    __tablename__ = "feedback_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    color = Column(String(7), nullable=True)  # لون الوسم بصيغة HEX (#RRGGBB)

    # معلومات التتبع
    created_at = Column(DateTime, default=datetime.utcnow)


class FeedbackTagAssociation(Base):
    """نموذج ربط الوسوم بالتغذية الراجعة"""
    __tablename__ = "feedback_tag_associations"

    feedback_id = Column(Integer, ForeignKey("feedback.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("feedback_tags.id"), primary_key=True)

    # معلومات التتبع
    created_at = Column(DateTime, default=datetime.utcnow)
