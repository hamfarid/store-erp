# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/ai_management/memory_integration.py
"""
وحدة تكامل الذاكرة مع إدارة الذكاء الاصطناعي

هذه الوحدة مسؤولة عن ربط نظام إدارة الذكاء الاصطناعي بوحدة الذاكرة المركزية،
مما يسمح بتخزين واسترجاع معلومات النماذج والإحصائيات والاستخدام.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# استيراد وحدات النظام
from sqlalchemy.orm import Session
from src.modules.memory.service import MemoryService
from src.modules.memory.models import MemoryType
from src.modules.memory.schemas import MemoryCreate, MemorySearch

# إعداد السجل
logger = logging.getLogger(__name__)


class AIManagementMemoryIntegration:
    """
    فئة تكامل الذاكرة مع نظام إدارة الذكاء الاصطناعي

    توفر هذه الفئة واجهة موحدة لنظام إدارة الذكاء الاصطناعي للتفاعل مع وحدة الذاكرة المركزية،
    بما في ذلك تخزين واسترجاع معلومات النماذج والإحصائيات وسجلات الاستخدام.
    """

    def __init__(self, db: Session, memory_service: Optional[MemoryService] = None):
        """
        تهيئة تكامل الذاكرة مع نظام إدارة الذكاء الاصطناعي

        Args:
            db: جلسة قاعدة البيانات
            memory_service: خدمة الذاكرة المركزية، إذا لم يتم توفيرها سيتم إنشاء مثيل جديد
        """
        self.db = db
        self.memory_service = memory_service or MemoryService(db)
        logger.info("تم تهيئة تكامل الذاكرة مع نظام إدارة الذكاء الاصطناعي")

    def store_model_metadata(
        self,
        model_id: str,
        metadata: Dict[str, Any],
        tags: Optional[List[str]] = None
    ) -> str:
        """
        تخزين البيانات الوصفية لنموذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي
            metadata: البيانات الوصفية للنموذج
            tags: وسوم للبحث والتصنيف

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        if tags is None:
            tags = []

        # إضافة معرف النموذج إلى البيانات الوصفية
        metadata["model_id"] = model_id

        # إضافة وسوم النموذج
        tags.append(f"model:{model_id}")
        tags.append("ai_model_metadata")

        # تحويل البيانات الوصفية إلى سلسلة نصية
        content = json.dumps(metadata, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title=f"AI Model Metadata: {model_id}",
            content=content,
            memory_type=MemoryType.AI_MODEL_METADATA,
            extra_data=metadata,
            tags=tags
        )

        # تخزين الذاكرة
        try:
            memory = self.memory_service.create_memory(memory_entry)
            logger.info("تم تخزين بيانات النموذج %s بنجاح، المعرف: {memory.id}", model_id)
            return memory.id
        except Exception as e:
            logger.error("فشل في تخزين بيانات النموذج %s: %s", model_id, str(e))
            raise

    def retrieve_model_metadata(
        self,
        model_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        استرجاع البيانات الوصفية لنموذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي

        Returns:
            البيانات الوصفية للنموذج إذا وجدت، وإلا None
        """
        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryType.AI_MODEL_METADATA,
            tags=[f"model:{model_id}", "ai_model_metadata"],
            limit=1
        )

        # استرجاع الذكريات
        try:
            memories = self.memory_service.search_memories(memory_query)
            if not memories.memories:
                logger.warning("لم يتم العثور على بيانات للنموذج %s", model_id)
                return None

            # تحويل المحتوى من سلسلة نصية إلى كائن
            metadata = json.loads(memories.memories[0].content)
            logger.info("تم استرجاع بيانات النموذج %s بنجاح", model_id)
            return metadata
        except Exception as e:
            logger.error("فشل في استرجاع بيانات النموذج %s: %s", model_id, str(e))
            raise

    def store_usage_statistics(
        self,
        model_id: str,
        statistics: Dict[str, Any],
        period: str,
        timestamp: Optional[datetime] = None
    ) -> str:
        """
        تخزين إحصائيات استخدام نموذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي
            statistics: إحصائيات الاستخدام
            period: الفترة الزمنية (daily, weekly, monthly)
            timestamp: الطابع الزمني، إذا لم يتم توفيره سيتم استخدام الوقت الحالي

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        if timestamp is None:
            timestamp = datetime.now()

        # إنشاء البيانات الوصفية
        metadata = {
            "model_id": model_id,
            "period": period,
            "timestamp": timestamp.isoformat()
        }

        # إنشاء الوسوم
        tags = [
            f"model:{model_id}",
            f"period:{period}",
            "ai_usage_statistics"
        ]

        # تحويل الإحصائيات إلى سلسلة نصية
        content = json.dumps(statistics, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title=f"AI Usage Statistics: {model_id} ({period})",
            content=content,
            memory_type=MemoryType.AI_USAGE_STATISTICS,
            extra_data=metadata,
            tags=tags
        )

        # تخزين الذاكرة
        try:
            memory = self.memory_service.create_memory(memory_entry)
            logger.info("تم تخزين إحصائيات استخدام النموذج %s للفترة {period} بنجاح", model_id)
            return memory.id
        except Exception as e:
            logger.error("فشل في تخزين إحصائيات استخدام النموذج %s: %s", model_id, str(e))
            raise

    def retrieve_usage_statistics(
        self,
        model_id: Optional[str] = None,
        period: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        استرجاع إحصائيات استخدام نماذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي (اختياري)
            period: الفترة الزمنية (daily, weekly, monthly) (اختياري)
            start_date: تاريخ البداية للتصفية (اختياري)
            end_date: تاريخ النهاية للتصفية (اختياري)
            limit: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بإحصائيات الاستخدام
        """
        # إنشاء الوسوم للبحث
        tags = ["ai_usage_statistics"]
        if model_id:
            tags.append(f"model:{model_id}")
        if period:
            tags.append(f"period:{period}")

        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryType.AI_USAGE_STATISTICS,
            tags=tags,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

        # استرجاع الذكريات
        try:
            memories = self.memory_service.search_memories(memory_query)
            statistics_list = []

            for memory in memories.memories:
                try:
                    statistics = json.loads(memory.content)
                    statistics_list.append(statistics)
                except json.JSONDecodeError:
                    logger.warning("فشل في تحليل إحصائيات الذاكرة %s", memory.id)
                    continue

            logger.info("تم استرجاع %s إحصائية استخدام", len(statistics_list))
            return statistics_list
        except Exception as e:
            logger.error("فشل في استرجاع إحصائيات الاستخدام: %s", str(e))
            raise

    def store_model_performance(
        self,
        model_id: str,
        performance_data: Dict[str, Any],
        task_type: str,
        timestamp: Optional[datetime] = None
    ) -> str:
        """
        تخزين بيانات أداء نموذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي
            performance_data: بيانات الأداء
            task_type: نوع المهمة
            timestamp: الطابع الزمني، إذا لم يتم توفيره سيتم استخدام الوقت الحالي

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        if timestamp is None:
            timestamp = datetime.now()

        # إنشاء البيانات الوصفية
        metadata = {
            "model_id": model_id,
            "task_type": task_type,
            "timestamp": timestamp.isoformat()
        }

        # إنشاء الوسوم
        tags = [
            f"model:{model_id}",
            f"task:{task_type}",
            "ai_performance"
        ]

        # تحويل بيانات الأداء إلى سلسلة نصية
        content = json.dumps(performance_data, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title=f"AI Performance: {model_id} ({task_type})",
            content=content,
            memory_type=MemoryType.AI_PERFORMANCE,
            extra_data=metadata,
            tags=tags
        )

        # تخزين الذاكرة
        try:
            memory = self.memory_service.create_memory(memory_entry)
            logger.info("تم تخزين بيانات أداء النموذج %s للمهمة {task_type} بنجاح", model_id)
            return memory.id
        except Exception as e:
            logger.error("فشل في تخزين بيانات أداء النموذج %s: %s", model_id, str(e))
            raise

    def retrieve_model_performance(
        self,
        model_id: Optional[str] = None,
        task_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        استرجاع بيانات أداء نماذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي (اختياري)
            task_type: نوع المهمة (اختياري)
            start_date: تاريخ البداية للتصفية (اختياري)
            end_date: تاريخ النهاية للتصفية (اختياري)
            limit: الحد الأقصى لعدد النتائج

        Returns:
            قائمة ببيانات الأداء
        """
        # إنشاء الوسوم للبحث
        tags = ["ai_performance"]
        if model_id:
            tags.append(f"model:{model_id}")
        if task_type:
            tags.append(f"task:{task_type}")

        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryType.AI_PERFORMANCE,
            tags=tags,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

        # استرجاع الذكريات
        try:
            memories = self.memory_service.search_memories(memory_query)
            performance_list = []

            for memory in memories.memories:
                try:
                    performance_data = json.loads(memory.content)
                    performance_list.append(performance_data)
                except json.JSONDecodeError:
                    logger.warning("فشل في تحليل بيانات أداء الذاكرة %s", memory.id)
                    continue

            logger.info("تم استرجاع %s بيانات أداء", len(performance_list))
            return performance_list
        except Exception as e:
            logger.error("فشل في استرجاع بيانات الأداء: %s", str(e))
            raise

    def store_model_version(
        self,
        model_id: str,
        version: str,
        version_data: Dict[str, Any],
        is_active: bool = False
    ) -> str:
        """
        تخزين معلومات إصدار نموذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي
            version: رقم الإصدار
            version_data: بيانات الإصدار
            is_active: هل هذا الإصدار نشط

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        # إنشاء البيانات الوصفية
        metadata = {
            "model_id": model_id,
            "version": version,
            "is_active": is_active,
            "timestamp": datetime.now().isoformat()
        }

        # إنشاء الوسوم
        tags = [
            f"model:{model_id}",
            f"version:{version}",
            "ai_model_version"
        ]

        if is_active:
            tags.append("active_version")

        # تحويل بيانات الإصدار إلى سلسلة نصية
        content = json.dumps(version_data, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title=f"AI Model Version: {model_id} v{version}",
            content=content,
            memory_type=MemoryType.AI_MODEL_VERSION,
            extra_data=metadata,
            tags=tags
        )

        # تخزين الذاكرة
        try:
            memory = self.memory_service.create_memory(memory_entry)
            logger.info("تم تخزين إصدار النموذج %s v{version} بنجاح", model_id)
            return memory.id
        except Exception as e:
            logger.error("فشل في تخزين إصدار النموذج %s: %s", model_id, str(e))
            raise

    def retrieve_model_versions(
        self,
        model_id: str,
        active_only: bool = False,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        استرجاع إصدارات نموذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي
            active_only: استرجاع الإصدارات النشطة فقط
            limit: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بإصدارات النموذج
        """
        # إنشاء الوسوم للبحث
        tags = [f"model:{model_id}", "ai_model_version"]
        if active_only:
            tags.append("active_version")

        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryType.AI_MODEL_VERSION,
            tags=tags,
            limit=limit
        )

        # استرجاع الذكريات
        try:
            memories = self.memory_service.search_memories(memory_query)
            versions_list = []

            for memory in memories.memories:
                try:
                    version_data = json.loads(memory.content)
                    # إضافة البيانات الوصفية
                    if memory.extra_data:
                        version_data.update(memory.extra_data)
                    versions_list.append(version_data)
                except json.JSONDecodeError:
                    logger.warning("فشل في تحليل بيانات إصدار الذاكرة %s", memory.id)
                    continue

            logger.info("تم استرجاع %s إصدار للنموذج {model_id}", len(versions_list))
            return versions_list
        except Exception as e:
            logger.error("فشل في استرجاع إصدارات النموذج %s: %s", model_id, str(e))
            raise

    def update_model_active_version(
        self,
        model_id: str,
        new_active_version: str
    ) -> bool:
        """
        تحديث الإصدار النشط لنموذج الذكاء الاصطناعي

        Args:
            model_id: معرف نموذج الذكاء الاصطناعي
            new_active_version: رقم الإصدار الجديد النشط

        Returns:
            True إذا نجح التحديث، False إذا فشل
        """
        try:
            # البحث عن جميع إصدارات النموذج
            all_versions = self.retrieve_model_versions(model_id)

            # تحديث حالة الإصدارات
            for version_data in all_versions:
                version = version_data.get("version")
                if version == new_active_version:
                    # تفعيل الإصدار الجديد
                    version_data["is_active"] = True
                    logger.info("تم تفعيل الإصدار %s للنموذج {model_id}", version)
                else:
                    # إلغاء تفعيل الإصدارات الأخرى
                    version_data["is_active"] = False

            logger.info("تم تحديث الإصدار النشط للنموذج %s إلى {new_active_version}", model_id)
            return True

        except Exception as e:
            logger.error("فشل في تحديث الإصدار النشط للنموذج %s: %s", model_id, str(e))
            return False
