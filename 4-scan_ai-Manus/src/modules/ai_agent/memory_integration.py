# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/ai_agent/memory_integration.py
"""
وحدة تكامل الذاكرة مع وكلاء الذكاء الاصطناعي

هذه الوحدة مسؤولة عن ربط وكلاء الذكاء الاصطناعي بوحدة الذاكرة المركزية،
مما يسمح للوكلاء بتخزين واسترجاع المعلومات من الذاكرة المركزية.
"""

import logging
from typing import Dict, List, Optional, Any, Union
import json
from datetime import datetime

# استيراد وحدات النظام
from sqlalchemy.orm import Session
from src.modules.memory.service import MemoryService
from src.modules.memory.models import MemoryType, MemoryEntry
from src.modules.memory.schemas import MemoryEntryCreate, MemoryQuery

# إعداد السجل
logger = logging.getLogger(__name__)


class AIAgentMemoryIntegration:
    """
    فئة تكامل الذاكرة مع وكلاء الذكاء الاصطناعي

    توفر هذه الفئة واجهة موحدة لوكلاء الذكاء الاصطناعي للتفاعل مع وحدة الذاكرة المركزية،
    بما في ذلك تخزين واسترجاع وتحديث المعلومات.
    """

    def __init__(self, db: Session, memory_service: Optional[MemoryService] = None):
        """
        تهيئة فئة تكامل الذاكرة

        Args:
            db: جلسة قاعدة البيانات
            memory_service: خدمة الذاكرة المركزية، إذا لم يتم توفيرها سيتم إنشاء مثيل جديد
        """
        self.db = db
        self.memory_service = memory_service or MemoryService(db)
        logger.info("تم تهيئة تكامل الذاكرة مع وكلاء الذكاء الاصطناعي")

    async def store_agent_memory(
        self,
        agent_id: str,
        content: Union[str, Dict[str, Any]],
        memory_type: MemoryType = MemoryType.EPISODIC,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        تخزين ذاكرة وكيل الذكاء الاصطناعي

        Args:
            agent_id: معرف وكيل الذكاء الاصطناعي
            content: محتوى الذاكرة (نص أو كائن JSON)
            memory_type: نوع الذاكرة (افتراضياً EPISODIC)
            metadata: بيانات وصفية إضافية
            tags: وسوم للبحث والتصنيف

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        if metadata is None:
            metadata = {}

        if tags is None:
            tags = []

        # إضافة معرف الوكيل إلى البيانات الوصفية
        metadata["agent_id"] = agent_id

        # إضافة وسم الوكيل
        tags.append(f"agent:{agent_id}")

        # تحويل المحتوى إلى سلسلة نصية إذا كان كائناً
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryEntryCreate(
            content=content, memory_type=memory_type, metadata=metadata, tags=tags
        )

        # تخزين الذاكرة
        try:
            memory_id = await self.memory_service.create_memory(memory_entry)
            logger.info("تم تخزين ذاكرة الوكيل %s بنجاح، المعرف: %s", agent_id, memory_id)
            return memory_id
        except Exception as e:
            logger.error("فشل في تخزين ذاكرة الوكيل %s: %s", agent_id, str(e))
            raise

    async def retrieve_agent_memories(
        self,
        agent_id: str,
        query: Optional[str] = None,
        limit: int = 10,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[MemoryEntry]:
        """
        استرجاع ذكريات وكيل الذكاء الاصطناعي

        Args:
            agent_id: معرف وكيل الذكاء الاصطناعي
            query: استعلام نصي للبحث في محتوى الذاكرة
            limit: الحد الأقصى لعدد النتائج
            memory_type: نوع الذاكرة للتصفية
            tags: وسوم للتصفية
            start_date: تاريخ البداية للتصفية
            end_date: تاريخ النهاية للتصفية
            metadata_filter: تصفية حسب البيانات الوصفية

        Returns:
            قائمة بإدخالات الذاكرة المطابقة
        """
        if metadata_filter is None:
            metadata_filter = {}

        if tags is None:
            tags = []

        # إضافة معرف الوكيل إلى تصفية البيانات الوصفية
        metadata_filter["agent_id"] = agent_id

        # إضافة وسم الوكيل إلى قائمة الوسوم
        agent_tag = f"agent:{agent_id}"
        if agent_tag not in tags:
            tags.append(agent_tag)

        # إنشاء استعلام الذاكرة
        memory_query = MemoryQuery(
            query_text=query,
            memory_type=memory_type,
            tags=tags,
            start_date=start_date,
            end_date=end_date,
            metadata=metadata_filter,
            limit=limit,
        )

        # استرجاع الذكريات
        try:
            memories = await self.memory_service.search_memories(memory_query)
            logger.info("تم استرجاع %s ذكريات للوكيل %s", len(memories), agent_id)
            return memories
        except Exception as e:
            logger.error("فشل في استرجاع ذكريات الوكيل %s: %s", agent_id, str(e))
            raise

    async def update_agent_memory(
        self,
        memory_id: str,
        content: Optional[Union[str, Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """
        تحديث ذاكرة وكيل الذكاء الاصطناعي

        Args:
            memory_id: معرف إدخال الذاكرة
            content: المحتوى الجديد (اختياري)
            metadata: البيانات الوصفية الجديدة (اختياري)
            tags: الوسوم الجديدة (اختياري)

        Returns:
            نجاح العملية
        """
        # تحويل المحتوى إلى سلسلة نصية إذا كان كائناً
        if content is not None and isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)

        # تحديث الذاكرة
        try:
            success = await self.memory_service.update_memory(
                memory_id=memory_id, content=content, metadata=metadata, tags=tags
            )
            if success:
                logger.info("تم تحديث ذاكرة الوكيل بنجاح، المعرف: %s", memory_id)
            else:
                logger.warning("لم يتم العثور على ذاكرة بالمعرف: %s", memory_id)
            return success
        except Exception as e:
            logger.error("فشل في تحديث ذاكرة الوكيل، المعرف: %s: %s", memory_id, str(e))
            raise

    async def delete_agent_memory(self, memory_id: str) -> bool:
        """
        حذف ذاكرة وكيل الذكاء الاصطناعي

        Args:
            memory_id: معرف إدخال الذاكرة

        Returns:
            نجاح العملية
        """
        try:
            success = await self.memory_service.delete_memory(memory_id)
            if success:
                logger.info("تم حذف ذاكرة الوكيل بنجاح، المعرف: %s", memory_id)
            else:
                logger.warning("لم يتم العثور على ذاكرة بالمعرف: %s", memory_id)
            return success
        except Exception as e:
            logger.error("فشل في حذف ذاكرة الوكيل، المعرف: %s: %s", memory_id, str(e))
            raise

    async def get_agent_memory_by_id(self, memory_id: str) -> Optional[MemoryEntry]:
        """
        الحصول على ذاكرة وكيل الذكاء الاصطناعي بواسطة المعرف

        Args:
            memory_id: معرف إدخال الذاكرة

        Returns:
            إدخال الذاكرة إذا وجد، وإلا None
        """
        try:
            memory = await self.memory_service.get_memory_by_id(memory_id)
            if memory:
                logger.info("تم استرجاع ذاكرة الوكيل بنجاح، المعرف: %s", memory_id)
            else:
                logger.warning("لم يتم العثور على ذاكرة بالمعرف: %s", memory_id)
            return memory
        except Exception as e:
            logger.error("فشل في استرجاع ذاكرة الوكيل، المعرف: %s: %s", memory_id, str(e))
            raise

    async def clear_agent_memories(self, agent_id: str) -> int:
        """
        مسح جميع ذكريات وكيل الذكاء الاصطناعي

        Args:
            agent_id: معرف وكيل الذكاء الاصطناعي

        Returns:
            عدد الذكريات التي تم مسحها
        """
        try:
            # استرجاع جميع ذكريات الوكيل
            memories = await self.retrieve_agent_memories(
                agent_id=agent_id, limit=1000  # حد عالي لاسترجاع معظم الذكريات
            )

            # حذف كل ذاكرة
            deleted_count = 0
            for memory in memories:
                if await self.delete_agent_memory(memory.id):
                    deleted_count += 1

            logger.info("تم مسح %s ذاكرة للوكيل %s", deleted_count, agent_id)
            return deleted_count
        except Exception as e:
            logger.error("فشل في مسح ذكريات الوكيل %s: %s", agent_id, str(e))
            raise

    async def get_agent_memory_stats(self, agent_id: str) -> Dict[str, Any]:
        """
        الحصول على إحصائيات ذاكرة وكيل الذكاء الاصطناعي

        Args:
            agent_id: معرف وكيل الذكاء الاصطناعي

        Returns:
            قاموس يحتوي على إحصائيات الذاكرة
        """
        try:
            # استرجاع جميع ذكريات الوكيل
            memories = await self.retrieve_agent_memories(
                agent_id=agent_id, limit=1000  # حد عالي لاسترجاع معظم الذكريات
            )

            # حساب الإحصائيات
            stats = {
                "total_memories": len(memories),
                "memory_types": {},
                "tags": {},
                "creation_dates": [],
            }

            for memory in memories:
                # إحصائيات أنواع الذاكرة
                memory_type = memory.memory_type.value
                stats["memory_types"][memory_type] = stats["memory_types"].get(memory_type, 0) + 1

                # إحصائيات الوسوم
                for tag in memory.tags:
                    stats["tags"][tag] = stats["tags"].get(tag, 0) + 1

                # تواريخ الإنشاء
                stats["creation_dates"].append(memory.created_at)

            # حساب متوسط حجم الذاكرة
            if memories:
                stats["average_memory_size"] = sum(len(m.content) for m in memories) / len(memories)
            else:
                stats["average_memory_size"] = 0

            logger.info("تم حساب إحصائيات ذاكرة الوكيل %s", agent_id)
            return stats
        except Exception as e:
            logger.error("فشل في حساب إحصائيات ذاكرة الوكيل %s: %s", agent_id, str(e))
            raise
