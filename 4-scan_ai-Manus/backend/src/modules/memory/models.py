"""
نماذج قاعدة البيانات لمديول الذاكرة المركزية

يحتوي هذا الملف على تعريفات نماذج قاعدة البيانات لمديول الذاكرة المركزية، بما في ذلك:
- نموذج الذاكرة الأساسي
- أنواع الذاكرة
- فئات الذاكرة
- صلاحيات الوصول للذاكرة
- العلاقات بين النماذج
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
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Constants for repeated string literals
MEMORIES_ID_FK = 'memories.id'

# جدول العلاقات بين الذاكرة والعلامات
memory_tags = Table(
    'memory_tags', Base.metadata, Column(
        'memory_id', String(36), ForeignKey(
            MEMORIES_ID_FK, ondelete='CASCADE'), primary_key=True), Column(
                'tag_id', Integer, ForeignKey(
                    'tags.id', ondelete='CASCADE'), primary_key=True))

# جدول العلاقات بين الذاكرة والكيانات
memory_entities = Table(
    'memory_entities', Base.metadata, Column(
        'memory_id', String(36), ForeignKey(
            MEMORIES_ID_FK, ondelete='CASCADE'), primary_key=True), Column(
                'entity_id', Integer, ForeignKey(
                    'entities.id', ondelete='CASCADE'), primary_key=True))


class MemoryType(enum.Enum):
    """أنواع الذاكرة المدعومة"""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    AI_MODEL_METADATA = "ai_model_metadata"
    AI_USAGE_STATISTICS = "ai_usage_statistics"
    AI_PERFORMANCE = "ai_performance"
    AI_MODEL_VERSION = "ai_model_version"


class MemoryCategory(enum.Enum):
    """فئات الذاكرة المدعومة"""
    PLANT_DATA = "plant_data"
    DISEASE_DATA = "disease_data"
    USER_INTERACTION = "user_interaction"
    SYSTEM_EVENT = "system_event"
    SEARCH_HISTORY = "search_history"
    DIAGNOSIS_RESULT = "diagnosis_result"
    AI_AGENT_INTERACTION = "ai_agent_interaction"
    EXTERNAL_SOURCE = "external_source"


class MemoryAccess(enum.Enum):
    """مستويات الوصول للذاكرة"""
    PRIVATE = "private"
    GROUP = "group"
    MODULE = "module"
    SYSTEM = "system"
    PUBLIC = "public"


class Memory(Base):
    """نموذج الذاكرة الأساسي"""
    __tablename__ = 'memories'

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    memory_type = Column(Enum(MemoryType), nullable=False, index=True)
    category = Column(Enum(MemoryCategory), nullable=False, index=True)
    access_level = Column(
        Enum(MemoryAccess),
        nullable=False,
        default=MemoryAccess.PRIVATE,
        index=True)

    # بيانات التضمين (embedding)
    embedding = Column(JSON, nullable=True)
    embedding_model = Column(String(100), nullable=True)

    # بيانات المصدر
    source_module = Column(String(100), nullable=True, index=True)
    source_id = Column(String(255), nullable=True)
    source_url = Column(String(1024), nullable=True)

    # بيانات المستخدم
    created_by = Column(String(36), nullable=True, index=True)
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

    # بيانات الأهمية والاحتفاظ
    importance_score = Column(Float, default=0.0, nullable=False, index=True)
    retention_days = Column(Integer, default=365, nullable=False)
    expiry_date = Column(DateTime, nullable=True, index=True)
    is_archived = Column(Boolean, default=False, nullable=False, index=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)

    # بيانات إضافية - تم تغيير الاسم من metadata إلى extra_data لتجنب تعارض
    # الاسم المحجوز
    extra_data = Column(JSON, nullable=True)

    # العلاقات
    tags = relationship(
        "Tag",
        secondary=memory_tags,
        back_populates="memories")
    entities = relationship(
        "Entity",
        secondary=memory_entities,
        back_populates="memories")
    access_logs = relationship(
        "MemoryAccessLog",
        back_populates="memory",
        cascade="all, delete-orphan")

    def __repr__(self):
        """تمثيل نصي للذاكرة"""
        return f"<Memory(id='{self.id}', title='{self.title}', type='{self.memory_type}', category='{self.category}')>"

    def to_dict(self) -> Dict:
        """تحويل الذاكرة إلى قاموس"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "memory_type": self.memory_type.value if self.memory_type else None,
            "category": self.category.value if self.category else None,
            "access_level": self.access_level.value if self.access_level else None,
            "source_module": self.source_module,
            "source_id": self.source_id,
            "source_url": self.source_url,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "importance_score": self.importance_score,
            "retention_days": self.retention_days,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "is_archived": self.is_archived,
            "is_deleted": self.is_deleted,
            "extra_data": self.extra_data,  # تم تغيير الاسم من metadata إلى extra_data
            "tags": [tag.name for tag in self.tags] if self.tags else [],
            "entities": [entity.to_dict() for entity in self.entities] if self.entities else []
        }


class Tag(Base):
    """نموذج العلامات"""
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # العلاقات
    memories = relationship(
        "Memory",
        secondary=memory_tags,
        back_populates="tags")

    def __repr__(self):
        """تمثيل نصي للعلامة"""
        return f"<Tag(id={self.id}, name='{self.name}')>"


class Entity(Base):
    """نموذج الكيانات"""
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True)
    source = Column(String(100), nullable=True)
    # تم تغيير الاسم من metadata إلى entity_data
    entity_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # العلاقات
    memories = relationship(
        "Memory",
        secondary=memory_entities,
        back_populates="entities")

    # قيود فريدة
    __table_args__ = (
        UniqueConstraint('name', 'entity_type', name='uix_entity_name_type'),
    )

    def __repr__(self):
        """تمثيل نصي للكيان"""
        return f"<Entity(id={self.id}, name='{self.name}', type='{self.entity_type}')>"

    def to_dict(self) -> Dict:
        """تحويل الكيان إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "entity_type": self.entity_type,
            "source": self.source,
            "entity_data": self.entity_data  # تم تغيير الاسم من metadata إلى entity_data
        }


class MemoryAccessLog(Base):
    """نموذج سجل الوصول للذاكرة"""
    __tablename__ = 'memory_access_logs'

    id = Column(Integer, primary_key=True)
    memory_id = Column(
        String(36),
        ForeignKey(
            MEMORIES_ID_FK,
            ondelete='CASCADE'),
        nullable=False,
        index=True)
    user_id = Column(String(36), nullable=True, index=True)
    module = Column(String(100), nullable=True, index=True)
    action = Column(String(50), nullable=False, index=True)
    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    success = Column(Boolean, default=True, nullable=False)
    details = Column(JSON, nullable=True)

    # العلاقات
    memory = relationship("Memory", back_populates="access_logs")

    def __repr__(self):
        """تمثيل نصي لسجل الوصول"""
        return f"<MemoryAccessLog(id={self.id}, memory_id='{self.memory_id}', action='{self.action}', timestamp='{self.timestamp}')>"

    def to_dict(self) -> Dict:
        """تحويل سجل الوصول إلى قاموس"""
        return {
            "id": self.id,
            "memory_id": self.memory_id,
            "user_id": self.user_id,
            "module": self.module,
            "action": self.action,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "success": self.success,
            "details": self.details}


class MemoryStats(Base):
    """نموذج إحصائيات الذاكرة"""
    __tablename__ = 'memory_stats'

    id = Column(Integer, primary_key=True)
    date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True)
    total_memories = Column(Integer, default=0, nullable=False)
    active_memories = Column(Integer, default=0, nullable=False)
    archived_memories = Column(Integer, default=0, nullable=False)
    deleted_memories = Column(Integer, default=0, nullable=False)
    total_size_bytes = Column(Integer, default=0, nullable=False)
    avg_importance_score = Column(Float, default=0.0, nullable=False)
    memory_type_counts = Column(JSON, nullable=True)
    category_counts = Column(JSON, nullable=True)
    access_level_counts = Column(JSON, nullable=True)

    def __repr__(self):
        """تمثيل نصي لإحصائيات الذاكرة"""
        return f"<MemoryStats(id={self.id}, date='{self.date}', total_memories={self.total_memories})>"

    def to_dict(self) -> Dict:
        """تحويل إحصائيات الذاكرة إلى قاموس"""
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "total_memories": self.total_memories,
            "active_memories": self.active_memories,
            "archived_memories": self.archived_memories,
            "deleted_memories": self.deleted_memories,
            "total_size_bytes": self.total_size_bytes,
            "avg_importance_score": self.avg_importance_score,
            "memory_type_counts": self.memory_type_counts,
            "category_counts": self.category_counts,
            "access_level_counts": self.access_level_counts
        }
