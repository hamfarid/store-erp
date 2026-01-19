"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/activity_log/models.py
الوصف: نماذج بيانات مديول سجل النشاط
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base

# Constants for repeated string literals
ACTIVITY_LOGS_ID_FK = "activity_logs.id"


class ActivityLog(Base):
    """نموذج سجل النشاط"""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(String(50), nullable=False, index=True)
    action_id = Column(String(50), nullable=False, index=True)
    log_type = Column(String(20), nullable=False, index=True)
    description = Column(Text, nullable=False)
    log_data = Column(JSON, nullable=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(
            timezone=True),
        server_default=func.now(),
        nullable=False)  # pylint: disable=not-callable
    updated_at = Column(
        DateTime(
            timezone=True),
        onupdate=func.now(),
        nullable=True)  # pylint: disable=not-callable

    # العلاقات
    user = relationship("User", back_populates="activity_logs")

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            "id": self.id,
            "module_id": self.module_id,
            "action_id": self.action_id,
            "log_type": self.log_type,
            "description": self.description,
            "log_data": self.log_data,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None}

    @classmethod
    def from_dict(cls, data):
        """إنشاء نموذج من قاموس"""
        return cls(
            module_id=data.get("module_id"),
            action_id=data.get("action_id"),
            log_type=data.get("log_type"),
            description=data.get("description"),
            log_data=data.get("log_data"),
            user_id=data.get("user_id"),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent")
        )

    def update(self, data):
        """تحديث النموذج من قاموس"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        """تمثيل النموذج كنص"""
        return f"<ActivityLog(id={self.id}, module_id='{self.module_id}', action_id='{self.action_id}', log_type='{self.log_type}')>"


class SystemLog(Base):
    """نموذج سجل النظام"""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    activity_log_id = Column(
        Integer,
        ForeignKey(ACTIVITY_LOGS_ID_FK),
        nullable=False)
    component = Column(String(50), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    # critical, error, warning, info, debug
    severity = Column(String(20), nullable=False, index=True)
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # العلاقات
    activity_log = relationship("ActivityLog")

    # الفهارس
    __table_args__ = (
        Index('idx_system_log_severity', 'severity'),
        Index('idx_system_log_created_at', 'created_at'),
    )


class UserLog(Base):
    """نموذج سجل المستخدم"""
    __tablename__ = "user_logs"

    id = Column(Integer, primary_key=True, index=True)
    activity_log_id = Column(
        Integer,
        ForeignKey(ACTIVITY_LOGS_ID_FK),
        nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True)
    session_id = Column(String(100), nullable=True, index=True)
    action_type = Column(String(50), nullable=False, index=True)
    resource_type = Column(String(50), nullable=True, index=True)
    resource_id = Column(String(50), nullable=True)
    before_state = Column(JSON, nullable=True)
    after_state = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # العلاقات
    activity_log = relationship("ActivityLog")
    user = relationship("User")

    # الفهارس
    __table_args__ = (
        Index('idx_user_log_action_type', 'action_type'),
        Index('idx_user_log_created_at', 'created_at'),
    )


class AILog(Base):
    """نموذج سجل الذكاء الاصطناعي"""
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, index=True)
    activity_log_id = Column(
        Integer,
        ForeignKey(ACTIVITY_LOGS_ID_FK),
        nullable=False)
    agent_id = Column(String(50), nullable=False, index=True)
    agent_type = Column(String(50), nullable=False, index=True)
    # query, response, a2a_communication
    interaction_type = Column(String(50), nullable=False, index=True)
    query = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    processing_time = Column(Integer, nullable=True)  # بالمللي ثانية
    confidence_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # العلاقات
    activity_log = relationship("ActivityLog")

    # الفهارس
    __table_args__ = (
        Index('idx_ai_log_agent_id', 'agent_id'),
        Index('idx_ai_log_interaction_type', 'interaction_type'),
        Index('idx_ai_log_created_at', 'created_at'),
    )


class LogModule(Base):
    """نموذج مديولات السجل"""
    __tablename__ = "log_modules"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class LogAction(Base):
    """نموذج إجراءات السجل"""
    __tablename__ = "log_actions"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    module_id = Column(
        String(50),
        ForeignKey("log_modules.module_id"),
        nullable=False)
    is_active = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    # العلاقات
    module = relationship("LogModule")


class LogRetentionPolicy(Base):
    """نموذج سياسة الاحتفاظ بالسجلات"""
    __tablename__ = "log_retention_policies"

    id = Column(Integer, primary_key=True, index=True)
    log_type = Column(
        String(20),
        nullable=False,
        unique=True)  # system, user, ai
    retention_days = Column(Integer, nullable=False, default=90)
    archive_enabled = Column(Integer, default=0, nullable=False)
    archive_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
