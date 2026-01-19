"""
/home/ubuntu/implemented_files/v3/src/modules/ai_agent/models.py

ملف نماذج قاعدة البيانات لمديول وكلاء الذكاء الاصطناعي

يحتوي هذا الملف على تعريفات نماذج قاعدة البيانات لمديول وكلاء الذكاء الاصطناعي، بما في ذلك:
- نموذج الوكيل الأساسي
- أنواع الوكلاء
- أدوار الوكلاء
- حالات الوكلاء
- سجلات تنفيذ المهام
- إحصائيات الوكلاء
"""

import enum
import uuid
from datetime import datetime
from typing import Dict

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
    Table,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Constants for repeated string literals
AI_AGENTS_ID_FK = "ai_agents.id"

Base = declarative_base()

# جدول العلاقات بين الوكلاء والقدرات
agent_capability = Table(
    "agent_capability",
    Base.metadata,
    Column(
        "agent_id",
        String(36),
        ForeignKey(AI_AGENTS_ID_FK),
        primary_key=True),
    Column(
        "capability_id",
        String(36),
        ForeignKey("capabilities.id"),
        primary_key=True))

# جدول العلاقات بين الوكلاء والمديولات
agent_module = Table(
    "agent_module",
    Base.metadata,
    Column(
        "agent_id",
        String(36),
        ForeignKey(AI_AGENTS_ID_FK),
        primary_key=True),
    Column(
        "module_id",
        String(36),
        ForeignKey("modules.id"),
        primary_key=True))


class AgentType(enum.Enum):
    """أنواع وكلاء الذكاء الاصطناعي"""
    ASSISTANT = "assistant"
    SPECIALIST = "specialist"
    SUPERVISOR = "supervisor"
    AUTONOMOUS = "autonomous"
    COLLABORATIVE = "collaborative"


class AgentRole(enum.Enum):
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


class AgentStatus(enum.Enum):
    """حالات الوكيل"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class TaskStatus(enum.Enum):
    """حالات تنفيذ المهام"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class AIAgent(Base):
    """نموذج وكيل الذكاء الاصطناعي"""
    __tablename__ = 'ai_agents'

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    agent_type = Column(Enum(AgentType), nullable=False, index=True)
    role = Column(Enum(AgentRole), nullable=False, index=True)
    status = Column(
        Enum(AgentStatus),
        nullable=False,
        default=AgentStatus.ACTIVE,
        index=True)

    # بيانات التكوين
    provider = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    system_prompt = Column(Text, nullable=True)
    temperature = Column(Float, default=0.7, nullable=False)
    max_tokens = Column(Integer, default=2000, nullable=False)
    memory_retention = Column(Integer, default=10, nullable=False)

    # بيانات الصلاحيات
    created_by = Column(String(36), nullable=True, index=True)
    owner_id = Column(String(36), nullable=True, index=True)
    is_public = Column(Boolean, default=False, nullable=False, index=True)
    access_level = Column(
        String(50),
        default="private",
        nullable=False,
        index=True)

    # بيانات الإنشاء والتحديث
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)
    last_used_at = Column(DateTime, nullable=True)

    # بيانات إضافية
    metadata = Column(JSON, nullable=True)
    settings = Column(JSON, nullable=True)
    avatar_url = Column(String(1024), nullable=True)

    # العلاقات
    capabilities = relationship(
        "Capability",
        secondary=agent_capability,
        back_populates="agents")
    modules = relationship(
        "Module",
        secondary=agent_module,
        back_populates="agents")
    tasks = relationship(
        "AgentTask",
        back_populates="agent",
        cascade="all, delete-orphan")
    conversations = relationship(
        "AgentConversation",
        back_populates="agent",
        cascade="all, delete-orphan")
    stats = relationship("AgentStats", back_populates="agent")
    feedback = relationship("AgentFeedback", back_populates="agent")

    def __repr__(self):
        """تمثيل نصي للوكيل"""
        return f"<AIAgent(id='{self.id}', name='{self.name}', type='{self.agent_type}', role='{self.role}')>"

    def to_dict(self) -> Dict:
        """تحويل الوكيل إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agent_type": self.agent_type.value if self.agent_type else None,
            "role": self.role.value if self.role else None,
            "status": self.status.value if self.status else None,
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "memory_retention": self.memory_retention,
            "created_by": self.created_by,
            "owner_id": self.owner_id,
            "is_public": self.is_public,
            "access_level": self.access_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "metadata": self.metadata,
            "settings": self.settings,
            "avatar_url": self.avatar_url,
            "capabilities": [
                capability.name for capability in self.capabilities] if self.capabilities else [],
            "modules": [
                module.name for module in self.modules] if self.modules else []}


class Capability(Base):
    """نموذج قدرات الوكلاء"""
    __tablename__ = 'capabilities'

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # العلاقات
    agents = relationship(
        "AIAgent",
        secondary=agent_capability,
        back_populates="capabilities")

    def __repr__(self):
        """تمثيل نصي للقدرة"""
        return f"<Capability(id={self.id}, name='{self.name}')>"


class Module(Base):
    """نموذج المديولات المتاحة للوكلاء"""
    __tablename__ = 'modules'

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # العلاقات
    agents = relationship(
        "AIAgent",
        secondary=agent_module,
        back_populates="modules")

    def __repr__(self):
        """تمثيل نصي للمديول"""
        return f"<Module(id={self.id}, name='{self.name}', enabled={self.is_enabled})>"


class AgentTask(Base):
    """نموذج مهام الوكلاء"""
    __tablename__ = 'agent_tasks'

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))
    agent_id = Column(
        String(36),
        ForeignKey(
            AI_AGENTS_ID_FK,
            ondelete='CASCADE'),
        nullable=False,
        index=True)
    user_id = Column(String(36), nullable=True, index=True)
    task_type = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING,
        index=True)

    # بيانات التنفيذ
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    token_usage = Column(JSON, nullable=True)

    # بيانات الإنشاء والتحديث
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # العلاقات
    agent = relationship("AIAgent", back_populates="tasks")

    def __repr__(self):
        """تمثيل نصي للمهمة"""
        return f"<AgentTask(id='{self.id}', agent_id='{self.agent_id}', status='{self.status}')>"

    def to_dict(self) -> Dict:
        """تحويل المهمة إلى قاموس"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "user_id": self.user_id,
            "task_type": self.task_type,
            "description": self.description,
            "status": self.status.value if self.status else None,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "error_message": self.error_message,
            "execution_time_ms": self.execution_time_ms,
            "token_usage": self.token_usage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None}


class AgentConversation(Base):
    """نموذج محادثات الوكلاء"""
    __tablename__ = 'agent_conversations'

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))
    agent_id = Column(
        String(36),
        ForeignKey(
            AI_AGENTS_ID_FK,
            ondelete='CASCADE'),
        nullable=False,
        index=True)
    user_id = Column(String(36), nullable=True, index=True)
    title = Column(String(255), nullable=True)

    # بيانات المحادثة
    messages = Column(JSON, nullable=False)
    message_count = Column(Integer, default=0, nullable=False)
    token_usage = Column(JSON, nullable=True)

    # بيانات الإنشاء والتحديث
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)
    last_message_at = Column(DateTime, nullable=True, index=True)

    # العلاقات
    agent = relationship("AIAgent", back_populates="conversations")

    def __repr__(self):
        """تمثيل نصي للمحادثة"""
        return f"<AgentConversation(id='{self.id}', agent_id='{self.agent_id}', message_count={self.message_count})>"

    def to_dict(self) -> Dict:
        """تحويل المحادثة إلى قاموس"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "user_id": self.user_id,
            "title": self.title,
            "message_count": self.message_count,
            "token_usage": self.token_usage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None
        }


class AgentStats(Base):
    """نموذج إحصائيات الوكلاء"""
    __tablename__ = 'agent_stats'

    id = Column(String(36), primary_key=True)
    agent_id = Column(
        String(36),
        ForeignKey(
            AI_AGENTS_ID_FK,
            ondelete='CASCADE'),
        nullable=False,
        index=True)
    date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True)

    # إحصائيات الاستخدام
    task_count = Column(Integer, default=0, nullable=False)
    successful_tasks = Column(Integer, default=0, nullable=False)
    failed_tasks = Column(Integer, default=0, nullable=False)
    avg_execution_time_ms = Column(Float, default=0.0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    prompt_tokens = Column(Integer, default=0, nullable=False)
    completion_tokens = Column(Integer, default=0, nullable=False)
    estimated_cost = Column(Float, default=0.0, nullable=False)

    # إحصائيات المستخدمين
    unique_users = Column(Integer, default=0, nullable=False)
    user_satisfaction = Column(Float, nullable=True)

    # العلاقات
    agent = relationship("AIAgent", back_populates="stats")

    def __repr__(self):
        """تمثيل نصي للإحصائيات"""
        return f"<AgentStats(id={self.id}, agent_id='{self.agent_id}', date='{self.date}')>"

    def to_dict(self) -> Dict:
        """تحويل الإحصائيات إلى قاموس"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "date": self.date.isoformat() if self.date else None,
            "task_count": self.task_count,
            "successful_tasks": self.successful_tasks,
            "failed_tasks": self.failed_tasks,
            "avg_execution_time_ms": self.avg_execution_time_ms,
            "total_tokens": self.total_tokens,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "estimated_cost": self.estimated_cost,
            "unique_users": self.unique_users,
            "user_satisfaction": self.user_satisfaction
        }


class AgentFeedback(Base):
    """نموذج تقييمات المستخدمين للوكلاء"""
    __tablename__ = 'agent_feedback'

    id = Column(String(36), primary_key=True)
    agent_id = Column(
        String(36),
        ForeignKey(
            AI_AGENTS_ID_FK,
            ondelete='CASCADE'),
        nullable=False,
        index=True)
    user_id = Column(String(36), nullable=True, index=True)
    task_id = Column(
        String(36),
        ForeignKey(
            'agent_tasks.id',
            ondelete='SET NULL'),
        nullable=True)
    conversation_id = Column(
        String(36),
        ForeignKey(
            'agent_conversations.id',
            ondelete='SET NULL'),
        nullable=True)

    # بيانات التقييم
    rating = Column(Integer, nullable=False, index=True)
    feedback_text = Column(Text, nullable=True)
    categories = Column(JSON, nullable=True)

    # بيانات الإنشاء
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # العلاقات
    agent = relationship("AIAgent", back_populates="feedback")

    def __repr__(self):
        """تمثيل نصي للتقييم"""
        return f"<AgentFeedback(id={self.id}, agent_id='{self.agent_id}', rating={self.rating})>"

    def to_dict(self) -> Dict:
        """تحويل التقييم إلى قاموس"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "conversation_id": self.conversation_id,
            "rating": self.rating,
            "feedback_text": self.feedback_text,
            "categories": self.categories,
            "created_at": self.created_at.isoformat() if self.created_at else None}
