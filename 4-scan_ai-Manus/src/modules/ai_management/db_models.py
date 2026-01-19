# File: /home/ubuntu/ai_web_organized/src/modules/ai_management/db_models.py
"""
from flask import g
نماذج قاعدة البيانات لإدارة الذكاء الصناعي
توفر هذه الوحدة نماذج قاعدة البيانات للتعامل مع وكلاء الذكاء الصناعي وإحصائياتهم وإعداداتهم وصلاحياتهم
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime


Base = declarative_base()


# Constants for cascade options
CASCADE_ALL_DELETE_ORPHAN = "all, delete-orphan"
AI_AGENTS_ID = "ai_agents.id"


class AgentStatus(enum.Enum):
    """تعداد لحالات وكيل الذكاء الصناعي"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    STOPPED = "stopped"


class AgentType(enum.Enum):
    """تعداد لأنواع وكيل الذكاء الصناعي"""
    SYSTEM = "system"
    MODULE = "module"
    USER = "user"


class Agent(Base):
    """نموذج وكيل الذكاء الصناعي"""
    __tablename__ = 'ai_agents'

    id = Column(String(50), primary_key=True)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    type = Column(Enum(AgentType), nullable=False)
    model = Column(String(50), nullable=False)
    status = Column(
        Enum(AgentStatus),
        nullable=False,
        default=AgentStatus.ACTIVE)
    description_ar = Column(Text)
    description_en = Column(Text)
    avatar = Column(String(255))
    cpu_usage = Column(Float, default=0)
    ram_usage = Column(Float, default=0)
    requests_per_minute = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    last_active = Column(DateTime, default=datetime.now)

    # العلاقات
    stats = relationship(
        "AgentStat",
        back_populates="agent",
        cascade=CASCADE_ALL_DELETE_ORPHAN)
    roles = relationship(
        "AgentRole",
        back_populates="agent",
        cascade=CASCADE_ALL_DELETE_ORPHAN)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "nameAr": self.name_ar,
            "nameEn": self.name_en,
            "type": self.type.value,
            "model": self.model,
            "status": self.status.value,
            "descriptionAr": self.description_ar,
            "descriptionEn": self.description_en,
            "avatar": self.avatar,
            "cpuUsage": self.cpu_usage,
            "ramUsage": self.ram_usage,
            "requestsPerMinute": self.requests_per_minute,
            "createdAt": self.created_at.isoformat(),
            "lastActive": self.last_active.isoformat()
        }


class AgentStat(Base):
    """نموذج إحصائيات وكيل الذكاء الصناعي"""
    __tablename__ = 'ai_agent_stats'

    id = Column(Integer, primary_key=True)
    agent_id = Column(String(50), ForeignKey(AI_AGENTS_ID), nullable=False)
    date = Column(DateTime, default=datetime.now)
    requests = Column(Integer, default=0)
    tokens = Column(Integer, default=0)
    average_response_time = Column(Float, default=0)
    success_rate = Column(Float, default=0)

    # العلاقات
    agent = relationship("Agent", back_populates="stats")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "agentId": self.agent_id,
            "date": self.date.isoformat(),
            "requests": self.requests,
            "tokens": self.tokens,
            "averageResponseTime": self.average_response_time,
            "successRate": self.success_rate
        }


class AISettings(Base):
    """نموذج إعدادات الذكاء الصناعي"""
    __tablename__ = 'ai_settings'

    id = Column(Integer, primary_key=True)
    default_model = Column(String(50), nullable=False)
    memory_retention_days = Column(Integer, default=30)
    log_level = Column(String(20), default="info")
    resource_limits = Column(JSON)  # يخزن حدود الموارد كـ JSON
    auto_suspend = Column(JSON)  # يخزن إعدادات التعليق التلقائي كـ JSON
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "defaultModel": self.default_model,
            "memoryRetentionDays": self.memory_retention_days,
            "logLevel": self.log_level,
            "resourceLimits": self.resource_limits,
            "autoSuspend": self.auto_suspend,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }


class Role(Base):
    """نموذج الدور في نظام الصلاحيات"""
    __tablename__ = 'ai_roles'

    id = Column(String(50), primary_key=True)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    permissions = Column(JSON)  # يخزن الصلاحيات كـ JSON

    # العلاقات
    user_roles = relationship(
        "UserRole",
        back_populates="role",
        cascade=CASCADE_ALL_DELETE_ORPHAN)
    agent_roles = relationship(
        "AgentRole",
        back_populates="role",
        cascade=CASCADE_ALL_DELETE_ORPHAN)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "nameAr": self.name_ar,
            "nameEn": self.name_en,
            "permissions": self.permissions
        }


class UserRole(Base):
    """نموذج ربط المستخدم بالدور"""
    __tablename__ = 'ai_user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    role_id = Column(String(50), ForeignKey('ai_roles.id'), nullable=False)

    # العلاقات
    role = relationship("Role", back_populates="user_roles")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "userId": self.user_id,
            "roleId": self.role_id
        }


class AgentRole(Base):
    """نموذج ربط الوكيل بالدور"""
    __tablename__ = 'ai_agent_roles'

    id = Column(Integer, primary_key=True)
    agent_id = Column(String(50), ForeignKey(AI_AGENTS_ID), nullable=False)
    role_id = Column(String(50), ForeignKey('ai_roles.id'), nullable=False)

    # العلاقات
    agent = relationship("Agent", back_populates="roles")
    role = relationship("Role", back_populates="agent_roles")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "agentId": self.agent_id,
            "roleId": self.role_id
        }


class AIUsageStats(Base):
    """نموذج إحصائيات استخدام الذكاء الصناعي العامة"""
    __tablename__ = 'ai_usage_stats'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    total_requests = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    average_response_time = Column(Float, default=0)
    success_rate = Column(Float, default=0)
    model_usage = Column(JSON)  # يخزن استخدام النماذج كـ JSON

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "totalRequests": self.total_requests,
            "totalTokens": self.total_tokens,
            "averageResponseTime": self.average_response_time,
            "successRate": self.success_rate,
            "modelUsage": self.model_usage
        }


class DailyUsage(Base):
    """نموذج الاستخدام اليومي للذكاء الصناعي"""
    __tablename__ = 'ai_daily_usage'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    requests = Column(Integer, default=0)
    tokens = Column(Integer, default=0)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "date": self.date.strftime("%Y-%m-%d"),
            "requests": self.requests,
            "tokens": self.tokens
        }


class AIConversation(Base):
    """نموذج محادثات الذكاء الصناعي"""
    __tablename__ = 'ai_conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    agent_id = Column(String(50), ForeignKey('ai_agents.id'), nullable=False)
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime)

    # العلاقات
    messages = relationship(
        "AIMessage",
        back_populates="conversation",
        cascade="all, delete-orphan")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "userId": self.user_id,
            "agentId": self.agent_id,
            "startTime": self.start_time.isoformat(),
            "endTime": self.end_time.isoformat() if self.end_time is not None else None,
            "messages": [message.to_dict() for message in self.messages]
        }


class MessageType(enum.Enum):
    """تعداد لأنواع الرسائل"""
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


class AIMessage(Base):
    """نموذج رسائل الذكاء الصناعي"""
    __tablename__ = 'ai_messages'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(
        Integer,
        ForeignKey('ai_conversations.id'),
        nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    tokens = Column(Integer, default=0)

    # العلاقات
    conversation = relationship("AIConversation", back_populates="messages")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "conversationId": self.conversation_id,
            "messageType": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "tokens": self.tokens
        }
