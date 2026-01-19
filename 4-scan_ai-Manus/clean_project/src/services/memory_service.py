# File: /home/ubuntu/clean_project/src/services/memory_service.py
"""
خدمة الذاكرة للذكاء الاصطناعي - نظام شامل لإدارة الذاكرة قصيرة وطويلة المدى
AI Memory Service - Comprehensive system for managing short-term and long-term memory

هذه الخدمة توفر:
- إدارة الذاكرة قصيرة المدى (جلسات المحادثة)
- إدارة الذاكرة طويلة المدى (قاعدة المعرفة)
- تخزين السياق والتفضيلات
- البحث الذكي في الذاكرة
- تحليل الأنماط والتعلم
"""

import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import aioredis
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, or_, desc, func

# استيراد النماذج والتعدادات من وحدة ai_management
try:
    from ..modules.ai_management.memory_and_learning import (
        MemoryType, AccessLevel, AIKnowledgeEntry, Base
    )
    from ..core.config import get_settings
    from ..database import get_db_session
except ImportError:
    # Fallback للاختبار
    from enum import Enum
    
    class MemoryType(str, Enum):
        SHORT_TERM = "short_term"
        LONG_TERM = "long_term"
        CONTEXT = "context"
        KNOWLEDGE = "knowledge"
        PREFERENCES = "preferences"
    
    class AccessLevel(str, Enum):
        PRIVATE = "private"
        SHARED = "shared"
        PUBLIC = "public"

# إعداد التسجيل
logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
    """كائن إدخال الذاكرة"""
    id: Optional[str] = None
    content: str = ""
    memory_type: MemoryType = MemoryType.SHORT_TERM
    access_level: AccessLevel = AccessLevel.PRIVATE
    keywords: List[str] = None
    metadata: Dict[str, Any] = None
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    confidence: float = 1.0
    importance: float = 0.5
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.id is None:
            self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """إنشاء معرف فريد للذاكرة"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]
        timestamp = int(self.created_at.timestamp())
        return f"{self.memory_type.value}_{timestamp}_{content_hash}"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل إلى قاموس"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat() if self.created_at else None
        data['expires_at'] = self.expires_at.isoformat() if self.expires_at else None
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """إنشاء من قاموس"""
        if 'created_at' in data and data['created_at']:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'expires_at' in data and data['expires_at']:
            data['expires_at'] = datetime.fromisoformat(data['expires_at'])
        return cls(**data)

class MemoryService:
    """خدمة إدارة الذاكرة الشاملة"""
    
    def __init__(self, redis_url: str = None, db_session = None):
        """
        تهيئة خدمة الذاكرة
        
        Args:
            redis_url: رابط Redis للذاكرة قصيرة المدى
            db_session: جلسة قاعدة البيانات للذاكرة طويلة المدى
        """
        self.redis_url = redis_url or "redis://localhost:6379"
        self.db_session = db_session
        self.redis_pool = None
        self._memory_cache = {}  # cache محلي للأداء
        
        # إعدادات الذاكرة
        self.short_term_ttl = 3600  # ساعة واحدة
        self.context_ttl = 86400    # يوم واحد
        self.max_cache_size = 1000
        
        logger.info("تم تهيئة خدمة الذاكرة")
    
    async def initialize(self):
        """تهيئة الاتصالات"""
        try:
            # تهيئة Redis للذاكرة قصيرة المدى
            self.redis_pool = aioredis.ConnectionPool.from_url(
                self.redis_url, decode_responses=True
            )
            
            # اختبار الاتصال
            redis = aioredis.Redis(connection_pool=self.redis_pool)
            await redis.ping()
            logger.info("تم الاتصال بـ Redis بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تهيئة Redis: {e}")
            # استخدام cache محلي كبديل
            self.redis_pool = None
    
    async def store_memory(self, entry: MemoryEntry) -> bool:
        """
        تخزين إدخال في الذاكرة
        
        Args:
            entry: إدخال الذاكرة
            
        Returns:
            bool: نجح التخزين أم لا
        """
        try:
            if entry.memory_type in [MemoryType.SHORT_TERM, MemoryType.CONTEXT]:
                return await self._store_short_term(entry)
            else:
                return await self._store_long_term(entry)
        except Exception as e:
            logger.error(f"خطأ في تخزين الذاكرة: {e}")
            return False
    
    async def _store_short_term(self, entry: MemoryEntry) -> bool:
        """تخزين في الذاكرة قصيرة المدى (Redis)"""
        try:
            key = f"memory:{entry.memory_type.value}:{entry.id}"
            data = json.dumps(entry.to_dict(), ensure_ascii=False)
            
            if self.redis_pool:
                redis = aioredis.Redis(connection_pool=self.redis_pool)
                ttl = self.context_ttl if entry.memory_type == MemoryType.CONTEXT else self.short_term_ttl
                await redis.setex(key, ttl, data)
            else:
                # استخدام cache محلي
                self._memory_cache[key] = {
                    'data': data,
                    'expires_at': datetime.utcnow() + timedelta(seconds=self.short_term_ttl)
                }
                self._cleanup_cache()
            
            logger.debug(f"تم تخزين الذاكرة قصيرة المدى: {entry.id}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في تخزين الذاكرة قصيرة المدى: {e}")
            return False
    
    async def _store_long_term(self, entry: MemoryEntry) -> bool:
        """تخزين في الذاكرة طويلة المدى (قاعدة البيانات)"""
        try:
            if not self.db_session:
                logger.warning("لا توجد جلسة قاعدة بيانات للذاكرة طويلة المدى")
                return False
            
            # إنشاء إدخال في قاعدة البيانات
            db_entry = AIKnowledgeEntry(
                content=entry.content,
                keywords=','.join(entry.keywords),
                source=entry.metadata.get('source', ''),
                confidence=entry.confidence,
                entity_links=entry.metadata,
                meta_info={
                    'user_id': entry.user_id,
                    'agent_id': entry.agent_id,
                    'session_id': entry.session_id,
                    'access_level': entry.access_level.value,
                    'importance': entry.importance
                },
                created_at=entry.created_at
            )
            
            self.db_session.add(db_entry)
            self.db_session.commit()
            
            logger.debug(f"تم تخزين الذاكرة طويلة المدى: {entry.id}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في تخزين الذاكرة طويلة المدى: {e}")
            if self.db_session:
                self.db_session.rollback()
            return False
    
    async def retrieve_memory(self, 
                            memory_id: str = None,
                            memory_type: MemoryType = None,
                            user_id: str = None,
                            session_id: str = None,
                            keywords: List[str] = None,
                            limit: int = 10) -> List[MemoryEntry]:
        """
        استرجاع الذاكرة بناءً على المعايير
        
        Args:
            memory_id: معرف الذاكرة المحدد
            memory_type: نوع الذاكرة
            user_id: معرف المستخدم
            session_id: معرف الجلسة
            keywords: كلمات مفتاحية للبحث
            limit: عدد النتائج الأقصى
            
        Returns:
            List[MemoryEntry]: قائمة إدخالات الذاكرة
        """
        try:
            results = []
            
            if memory_id:
                # البحث عن ذاكرة محددة
                entry = await self._get_memory_by_id(memory_id)
                if entry:
                    results.append(entry)
            else:
                # البحث العام
                if memory_type in [MemoryType.SHORT_TERM, MemoryType.CONTEXT]:
                    results.extend(await self._search_short_term(
                        memory_type, user_id, session_id, keywords, limit
                    ))
                else:
                    results.extend(await self._search_long_term(
                        memory_type, user_id, keywords, limit
                    ))
            
            return results
            
        except Exception as e:
            logger.error(f"خطأ في استرجاع الذاكرة: {e}")
            return []
    
    async def _get_memory_by_id(self, memory_id: str) -> Optional[MemoryEntry]:
        """الحصول على ذاكرة بالمعرف"""
        try:
            # البحث في Redis أولاً
            if self.redis_pool:
                redis = aioredis.Redis(connection_pool=self.redis_pool)
                for memory_type in MemoryType:
                    key = f"memory:{memory_type.value}:{memory_id}"
                    data = await redis.get(key)
                    if data:
                        return MemoryEntry.from_dict(json.loads(data))
            
            # البحث في cache المحلي
            for key, cached in self._memory_cache.items():
                if memory_id in key and cached['expires_at'] > datetime.utcnow():
                    return MemoryEntry.from_dict(json.loads(cached['data']))
            
            # البحث في قاعدة البيانات
            if self.db_session:
                db_entry = self.db_session.query(AIKnowledgeEntry).filter(
                    AIKnowledgeEntry.id == memory_id
                ).first()
                if db_entry:
                    return self._db_entry_to_memory(db_entry)
            
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على الذاكرة بالمعرف: {e}")
            return None
    
    async def _search_short_term(self, 
                                memory_type: MemoryType,
                                user_id: str = None,
                                session_id: str = None,
                                keywords: List[str] = None,
                                limit: int = 10) -> List[MemoryEntry]:
        """البحث في الذاكرة قصيرة المدى"""
        results = []
        
        try:
            pattern = f"memory:{memory_type.value}:*"
            
            if self.redis_pool:
                redis = aioredis.Redis(connection_pool=self.redis_pool)
                keys = await redis.keys(pattern)
                
                for key in keys[:limit]:
                    data = await redis.get(key)
                    if data:
                        entry = MemoryEntry.from_dict(json.loads(data))
                        if self._matches_criteria(entry, user_id, session_id, keywords):
                            results.append(entry)
            
            # البحث في cache المحلي
            for key, cached in self._memory_cache.items():
                if (memory_type.value in key and 
                    cached['expires_at'] > datetime.utcnow() and
                    len(results) < limit):
                    entry = MemoryEntry.from_dict(json.loads(cached['data']))
                    if self._matches_criteria(entry, user_id, session_id, keywords):
                        results.append(entry)
            
            return results[:limit]
            
        except Exception as e:
            logger.error(f"خطأ في البحث في الذاكرة قصيرة المدى: {e}")
            return []
    
    async def _search_long_term(self,
                               memory_type: MemoryType = None,
                               user_id: str = None,
                               keywords: List[str] = None,
                               limit: int = 10) -> List[MemoryEntry]:
        """البحث في الذاكرة طويلة المدى"""
        results = []
        
        try:
            if not self.db_session:
                return []
            
            query = self.db_session.query(AIKnowledgeEntry)
            
            # تطبيق المرشحات
            if user_id:
                query = query.filter(
                    AIKnowledgeEntry.meta_info['user_id'].astext == user_id
                )
            
            if keywords:
                keyword_filters = []
                for keyword in keywords:
                    keyword_filters.append(
                        AIKnowledgeEntry.keywords.contains(keyword)
                    )
                    keyword_filters.append(
                        AIKnowledgeEntry.content.contains(keyword)
                    )
                query = query.filter(or_(*keyword_filters))
            
            # ترتيب بالثقة والأهمية
            query = query.order_by(
                desc(AIKnowledgeEntry.confidence),
                desc(AIKnowledgeEntry.created_at)
            ).limit(limit)
            
            for db_entry in query.all():
                memory_entry = self._db_entry_to_memory(db_entry)
                results.append(memory_entry)
            
            return results
            
        except Exception as e:
            logger.error(f"خطأ في البحث في الذاكرة طويلة المدى: {e}")
            return []
    
    def _matches_criteria(self, 
                         entry: MemoryEntry,
                         user_id: str = None,
                         session_id: str = None,
                         keywords: List[str] = None) -> bool:
        """فحص مطابقة المعايير"""
        if user_id and entry.user_id != user_id:
            return False
        
        if session_id and entry.session_id != session_id:
            return False
        
        if keywords:
            content_lower = entry.content.lower()
            entry_keywords = [k.lower() for k in entry.keywords]
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if (keyword_lower not in content_lower and 
                    keyword_lower not in entry_keywords):
                    return False
        
        return True
    
    def _db_entry_to_memory(self, db_entry) -> MemoryEntry:
        """تحويل إدخال قاعدة البيانات إلى MemoryEntry"""
        meta_info = db_entry.meta_info or {}
        
        return MemoryEntry(
            id=str(db_entry.id),
            content=db_entry.content,
            memory_type=MemoryType.LONG_TERM,
            access_level=AccessLevel(meta_info.get('access_level', 'private')),
            keywords=db_entry.keywords.split(',') if db_entry.keywords else [],
            metadata=db_entry.entity_links or {},
            user_id=meta_info.get('user_id'),
            agent_id=meta_info.get('agent_id'),
            session_id=meta_info.get('session_id'),
            confidence=db_entry.confidence,
            importance=meta_info.get('importance', 0.5),
            created_at=db_entry.created_at
        )
    
    async def delete_memory(self, memory_id: str) -> bool:
        """حذف ذاكرة"""
        try:
            deleted = False
            
            # حذف من Redis
            if self.redis_pool:
                redis = aioredis.Redis(connection_pool=self.redis_pool)
                for memory_type in MemoryType:
                    key = f"memory:{memory_type.value}:{memory_id}"
                    result = await redis.delete(key)
                    if result:
                        deleted = True
            
            # حذف من cache المحلي
            keys_to_delete = [k for k in self._memory_cache.keys() if memory_id in k]
            for key in keys_to_delete:
                del self._memory_cache[key]
                deleted = True
            
            # حذف من قاعدة البيانات
            if self.db_session:
                db_entry = self.db_session.query(AIKnowledgeEntry).filter(
                    AIKnowledgeEntry.id == memory_id
                ).first()
                if db_entry:
                    self.db_session.delete(db_entry)
                    self.db_session.commit()
                    deleted = True
            
            if deleted:
                logger.info(f"تم حذف الذاكرة: {memory_id}")
            
            return deleted
            
        except Exception as e:
            logger.error(f"خطأ في حذف الذاكرة: {e}")
            if self.db_session:
                self.db_session.rollback()
            return False
    
    async def clear_session_memory(self, session_id: str) -> bool:
        """مسح ذاكرة جلسة معينة"""
        try:
            cleared = False
            
            # مسح من Redis
            if self.redis_pool:
                redis = aioredis.Redis(connection_pool=self.redis_pool)
                pattern = f"memory:*:*"
                keys = await redis.keys(pattern)
                
                for key in keys:
                    data = await redis.get(key)
                    if data:
                        entry_data = json.loads(data)
                        if entry_data.get('session_id') == session_id:
                            await redis.delete(key)
                            cleared = True
            
            # مسح من cache المحلي
            keys_to_delete = []
            for key, cached in self._memory_cache.items():
                if cached['expires_at'] > datetime.utcnow():
                    entry_data = json.loads(cached['data'])
                    if entry_data.get('session_id') == session_id:
                        keys_to_delete.append(key)
            
            for key in keys_to_delete:
                del self._memory_cache[key]
                cleared = True
            
            logger.info(f"تم مسح ذاكرة الجلسة: {session_id}")
            return cleared
            
        except Exception as e:
            logger.error(f"خطأ في مسح ذاكرة الجلسة: {e}")
            return False
    
    def _cleanup_cache(self):
        """تنظيف cache المحلي"""
        current_time = datetime.utcnow()
        
        # حذف المدخلات المنتهية الصلاحية
        expired_keys = [
            key for key, cached in self._memory_cache.items()
            if cached['expires_at'] <= current_time
        ]
        
        for key in expired_keys:
            del self._memory_cache[key]
        
        # حذف المدخلات الزائدة إذا تجاوز الحد الأقصى
        if len(self._memory_cache) > self.max_cache_size:
            # ترتيب بتاريخ انتهاء الصلاحية وحذف الأقدم
            sorted_items = sorted(
                self._memory_cache.items(),
                key=lambda x: x[1]['expires_at']
            )
            
            excess_count = len(self._memory_cache) - self.max_cache_size
            for key, _ in sorted_items[:excess_count]:
                del self._memory_cache[key]
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """إحصائيات الذاكرة"""
        try:
            stats = {
                'short_term_count': 0,
                'long_term_count': 0,
                'context_count': 0,
                'cache_size': len(self._memory_cache),
                'redis_connected': self.redis_pool is not None
            }
            
            # إحصائيات Redis
            if self.redis_pool:
                redis = aioredis.Redis(connection_pool=self.redis_pool)
                for memory_type in [MemoryType.SHORT_TERM, MemoryType.CONTEXT]:
                    pattern = f"memory:{memory_type.value}:*"
                    keys = await redis.keys(pattern)
                    if memory_type == MemoryType.SHORT_TERM:
                        stats['short_term_count'] = len(keys)
                    else:
                        stats['context_count'] = len(keys)
            
            # إحصائيات قاعدة البيانات
            if self.db_session:
                stats['long_term_count'] = self.db_session.query(
                    func.count(AIKnowledgeEntry.id)
                ).scalar()
            
            return stats
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على إحصائيات الذاكرة: {e}")
            return {}

# مثيل عام للخدمة
_memory_service_instance = None

async def get_memory_service() -> MemoryService:
    """الحصول على مثيل خدمة الذاكرة"""
    global _memory_service_instance
    
    if _memory_service_instance is None:
        try:
            settings = get_settings()
            db_session = get_db_session()
            
            _memory_service_instance = MemoryService(
                redis_url=settings.redis_url,
                db_session=db_session
            )
            await _memory_service_instance.initialize()
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء خدمة الذاكرة: {e}")
            # إنشاء خدمة أساسية بدون اتصالات خارجية
            _memory_service_instance = MemoryService()
    
    return _memory_service_instance

# دوال مساعدة للاستخدام السريع

async def store_short_term_memory(content: str, 
                                 user_id: str = None,
                                 session_id: str = None,
                                 keywords: List[str] = None,
                                 metadata: Dict[str, Any] = None) -> bool:
    """تخزين سريع في الذاكرة قصيرة المدى"""
    service = await get_memory_service()
    entry = MemoryEntry(
        content=content,
        memory_type=MemoryType.SHORT_TERM,
        user_id=user_id,
        session_id=session_id,
        keywords=keywords or [],
        metadata=metadata or {}
    )
    return await service.store_memory(entry)

async def store_long_term_memory(content: str,
                                keywords: List[str] = None,
                                confidence: float = 1.0,
                                importance: float = 0.5,
                                metadata: Dict[str, Any] = None) -> bool:
    """تخزين سريع في الذاكرة طويلة المدى"""
    service = await get_memory_service()
    entry = MemoryEntry(
        content=content,
        memory_type=MemoryType.LONG_TERM,
        keywords=keywords or [],
        confidence=confidence,
        importance=importance,
        metadata=metadata or {}
    )
    return await service.store_memory(entry)

async def search_memory(query: str,
                       memory_type: MemoryType = None,
                       user_id: str = None,
                       limit: int = 10) -> List[MemoryEntry]:
    """البحث السريع في الذاكرة"""
    service = await get_memory_service()
    keywords = query.split() if query else []
    return await service.retrieve_memory(
        memory_type=memory_type,
        user_id=user_id,
        keywords=keywords,
        limit=limit
    )

if __name__ == "__main__":
    # اختبار أساسي للخدمة
    async def test_memory_service():
        print("اختبار خدمة الذاكرة...")
        
        # تخزين ذاكرة قصيرة المدى
        success = await store_short_term_memory(
            content="المستخدم يفضل اللغة العربية",
            user_id="user123",
            session_id="session456",
            keywords=["تفضيلات", "لغة", "عربية"]
        )
        print(f"تخزين الذاكرة قصيرة المدى: {'نجح' if success else 'فشل'}")
        
        # تخزين ذاكرة طويلة المدى
        success = await store_long_term_memory(
            content="النباتات تحتاج إلى ضوء الشمس للنمو",
            keywords=["نباتات", "ضوء", "نمو"],
            confidence=0.95,
            importance=0.8
        )
        print(f"تخزين الذاكرة طويلة المدى: {'نجح' if success else 'فشل'}")
        
        # البحث في الذاكرة
        results = await search_memory("نباتات", limit=5)
        print(f"نتائج البحث: {len(results)} إدخال")
        
        # إحصائيات
        service = await get_memory_service()
        stats = await service.get_memory_stats()
        print(f"إحصائيات الذاكرة: {stats}")
    
    # تشغيل الاختبار
    asyncio.run(test_memory_service())

