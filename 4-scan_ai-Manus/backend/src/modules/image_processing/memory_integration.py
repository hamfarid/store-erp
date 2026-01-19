# File:
# /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/image_processing/memory_integration.py
"""
وحدة تكامل الذاكرة مع معالجة الصور

هذه الوحدة مسؤولة عن ربط وحدة معالجة الصور بوحدة الذاكرة المركزية،
مما يسمح بتخزين واسترجاع معلومات الصور ونتائج المعالجة.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import psutil

# استيراد وحدات النظام
from sqlalchemy.orm import Session

from src.modules.memory.schemas import (
    MemoryCategoryEnum,
    MemoryCreate,
    MemorySearch,
    MemoryTypeEnum,
)
from src.modules.memory.service import MemoryService

# إعداد السجل
logger = logging.getLogger(__name__)


class ImageProcessingMemoryIntegration:
    """
    فئة تكامل الذاكرة مع معالجة الصور

    توفر هذه الفئة واجهة موحدة لوحدة معالجة الصور للتفاعل مع وحدة الذاكرة المركزية،
    بما في ذلك تخزين واسترجاع معلومات الصور ونتائج المعالجة.
    """

    def __init__(
            self,
            db: Session,
            memory_service: Optional[MemoryService] = None):
        """
        تهيئة فئة تكامل الذاكرة

        Args:
            db: جلسة قاعدة البيانات
            memory_service: خدمة الذاكرة المركزية، إذا لم يتم توفيرها سيتم إنشاء مثيل جديد
        """
        self.db = db
        self.memory_service = memory_service or MemoryService(db)
        logger.info("تم تهيئة تكامل الذاكرة مع معالجة الصور")

    async def store_image_metadata(
        self,
        image_id: str,
        metadata: Dict[str, Any],
        tags: Optional[List[str]] = None
    ) -> str:
        """
        تخزين البيانات الوصفية للصورة

        Args:
            image_id: معرف الصورة
            metadata: البيانات الوصفية للصورة
            tags: وسوم للبحث والتصنيف

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        if tags is None:
            tags = []

        # إضافة معرف الصورة إلى البيانات الوصفية
        metadata["image_id"] = image_id

        # إضافة وسوم الصورة
        tags.append(f"image:{image_id}")
        tags.append("image_metadata")

        # تحويل البيانات الوصفية إلى سلسلة نصية
        content = json.dumps(metadata, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title="Image Metadata: " + image_id,
            content=content,
            memory_type=MemoryTypeEnum.SEMANTIC,
            category=MemoryCategoryEnum.EXTERNAL_SOURCE,
            meta_data=metadata,
            tags=tags
        )

        # تخزين الذاكرة
        try:
            memory_id = await self.memory_service.create_memory(memory_entry)
            logger.info(
                "تم تخزين بيانات الصورة %s بنجاح، المعرف: %s",
                image_id,
                memory_id)
            return memory_id
        except Exception as e:
            logger.error("فشل في تخزين بيانات الصورة %s: %s", image_id, str(e))
            raise

    async def retrieve_image_metadata(
        self,
        image_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        استرجاع البيانات الوصفية للصورة

        Args:
            image_id: معرف الصورة

        Returns:
            البيانات الوصفية للصورة إذا وجدت، وإلا None
        """
        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryTypeEnum.SEMANTIC,
            tags=["image:" + image_id, "image_metadata"],
            page_size=1
        )

        # استرجاع الذكريات
        try:
            memories = await self.memory_service.search_memories(memory_query)
            if not memories:
                logger.warning("لم يتم العثور على بيانات للصورة %s", image_id)
                return None

            # تحويل المحتوى من سلسلة نصية إلى كائن
            metadata = json.loads(memories[0].content)
            logger.info("تم استرجاع بيانات الصورة %s بنجاح", image_id)
            return metadata
        except Exception as e:
            logger.error(
                "فشل في استرجاع بيانات الصورة %s: %s",
                image_id,
                str(e))
            raise

    async def store_processing_result(
        self,
        image_id: str,
        process_type: str,
        result: Dict[str, Any],
        output_path: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        تخزين نتيجة معالجة الصورة

        Args:
            image_id: معرف الصورة
            process_type: نوع المعالجة (مثل "classification", "detection", "enhancement")
            result: نتيجة المعالجة
            output_path: مسار الصورة الناتجة (اختياري)
            tags: وسوم إضافية للبحث والتصنيف

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        if tags is None:
            tags = []

        # إنشاء البيانات الوصفية
        metadata = {
            "image_id": image_id,
            "process_type": process_type,
            "timestamp": datetime.now().isoformat()
        }

        # إضافة مسار الصورة الناتجة إذا تم توفيره
        if output_path:
            metadata["output_path"] = output_path

        # إضافة وسوم
        tags.extend([
            f"image:{image_id}",
            f"process:{process_type}",
            "image_processing_result"
        ])

        # تحويل النتيجة إلى سلسلة نصية
        content = json.dumps(result, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title="Processing Result: " + image_id + " - " + process_type,
            content=content,
            memory_type=MemoryTypeEnum.PROCEDURAL,
            category=MemoryCategoryEnum.SYSTEM_EVENT,
            meta_data=metadata,
            tags=tags
        )

        # تخزين الذاكرة
        try:
            memory_id = await self.memory_service.create_memory(memory_entry)
            logger.info(
                "تم تخزين نتيجة معالجة الصورة %s من نوع %s بنجاح",
                image_id,
                process_type)
            return memory_id
        except Exception as e:
            logger.error(
                "فشل في تخزين نتيجة معالجة الصورة %s: %s",
                image_id,
                str(e))
            raise

    async def retrieve_processing_results(
        self,
        image_id: Optional[str] = None,
        process_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        استرجاع نتائج معالجة الصور

        Args:
            image_id: معرف الصورة (اختياري)
            process_type: نوع المعالجة (اختياري)
            start_date: تاريخ البداية للتصفية (اختياري)
            end_date: تاريخ النهاية للتصفية (اختياري)
            limit: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بنتائج المعالجة
        """
        # إنشاء الوسوم للتصفية
        tags = ["image_processing_result"]
        if image_id:
            tags.append("image:" + image_id)
        if process_type:
            tags.append("process:" + process_type)

        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryTypeEnum.PROCEDURAL,
            tags=tags,
            created_after=start_date,
            created_before=end_date,
            page_size=limit
        )

        # استرجاع الذكريات
        try:
            memories = await self.memory_service.search_memories(memory_query)

            # تحويل المحتوى من سلسلة نصية إلى كائن
            results_list = []
            for memory in memories:
                result = json.loads(memory.content)
                # إضافة البيانات الوصفية إلى النتيجة
                if hasattr(memory, 'meta_data') and memory.meta_data:
                    result.update(memory.meta_data)
                results_list.append(result)

            logger.info("تم استرجاع %s نتيجة معالجة", len(results_list))
            return results_list
        except Exception as e:
            logger.error("فشل في استرجاع نتائج المعالجة: %s", str(e))
            raise

    async def store_image_history(
        self,
        image_id: str,
        action: str,
        details: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> str:
        """
        تخزين سجل تاريخ الصورة

        Args:
            image_id: معرف الصورة
            action: الإجراء المتخذ على الصورة
            details: تفاصيل الإجراء
            user_id: معرف المستخدم الذي قام بالإجراء (اختياري)

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        # إنشاء البيانات الوصفية
        metadata = {
            "image_id": image_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }

        if user_id:
            metadata["user_id"] = user_id

        # إنشاء الوسوم
        tags = [
            "image:" + image_id,
            "action:" + action,
            "image_history"
        ]

        if user_id:
            tags.append("user:" + user_id)

        # تحويل التفاصيل إلى سلسلة نصية
        content = json.dumps(details, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title="Image History: " + image_id + " - " + action,
            content=content,
            memory_type=MemoryTypeEnum.EPISODIC,
            category=MemoryCategoryEnum.USER_INTERACTION,
            meta_data=metadata,
            tags=tags,
            created_by=user_id
        )

        # تخزين الذاكرة
        try:
            memory_id = await self.memory_service.create_memory(memory_entry)
            logger.info(
                "تم تخزين سجل تاريخ الصورة %s للإجراء %s بنجاح",
                image_id,
                action)
            return memory_id
        except Exception as e:
            logger.error(
                "فشل في تخزين سجل تاريخ الصورة %s: %s",
                image_id,
                str(e))
            raise

    async def retrieve_image_history(
        self,
        image_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        استرجاع سجل تاريخ الصورة

        Args:
            image_id: معرف الصورة
            start_date: تاريخ البداية للتصفية (اختياري)
            end_date: تاريخ النهاية للتصفية (اختياري)
            limit: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بسجل تاريخ الصورة
        """
        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryTypeEnum.EPISODIC,
            tags=["image:" + image_id, "image_history"],
            created_after=start_date,
            created_before=end_date,
            page_size=limit
        )

        # استرجاع الذكريات
        try:
            memories = await self.memory_service.search_memories(memory_query)

            # تحويل المحتوى من سلسلة نصية إلى كائن
            history_list = []
            for memory in memories:
                history_entry = json.loads(memory.content)
                # إضافة البيانات الوصفية إلى الإدخال
                if hasattr(memory, 'meta_data') and memory.meta_data:
                    history_entry.update(memory.meta_data)
                history_list.append(history_entry)

            logger.info(
                "تم استرجاع %s إدخال من سجل تاريخ الصورة %s",
                len(history_list),
                image_id)
            return history_list
        except Exception as e:
            logger.error(
                "فشل في استرجاع سجل تاريخ الصورة %s: %s",
                image_id,
                str(e))
            raise

    async def store_image_collection(
        self,
        collection_id: str,
        name: str,
        description: str,
        image_ids: List[str],
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        تخزين مجموعة صور

        Args:
            collection_id: معرف المجموعة
            name: اسم المجموعة
            description: وصف المجموعة
            image_ids: قائمة معرفات الصور في المجموعة
            metadata: بيانات وصفية إضافية (اختياري)
            tags: وسوم إضافية للبحث والتصنيف (اختياري)

        Returns:
            معرف إدخال الذاكرة المخزن
        """
        if metadata is None:
            metadata = {}
        if tags is None:
            tags = []

        # إنشاء البيانات الوصفية
        collection_metadata = {
            "collection_id": collection_id,
            "name": name,
            "description": description,
            "image_count": len(image_ids),
            "timestamp": datetime.now().isoformat()
        }
        collection_metadata.update(metadata)

        # إنشاء محتوى المجموعة
        collection_content = {
            "collection_id": collection_id,
            "name": name,
            "description": description,
            "image_ids": image_ids,
            "metadata": metadata
        }

        # إنشاء الوسوم
        collection_tags = [
            "collection:" + collection_id,
            "image_collection"
        ]
        collection_tags.extend(tags)

        # إضافة وسوم للصور المضمنة
        for image_id in image_ids:
            collection_tags.append("image:" + image_id)

        # تحويل المحتوى إلى سلسلة نصية
        content = json.dumps(collection_content, ensure_ascii=False)

        # إنشاء إدخال الذاكرة
        memory_entry = MemoryCreate(
            title="Image Collection: " + name,
            content=content,
            memory_type=MemoryTypeEnum.LONG_TERM,
            category=MemoryCategoryEnum.EXTERNAL_SOURCE,
            meta_data=collection_metadata,
            tags=collection_tags
        )

        # تخزين الذاكرة
        try:
            memory_id = await self.memory_service.create_memory(memory_entry)
            logger.info(
                "تم تخزين مجموعة الصور %s (%s) بنجاح مع %s صور",
                collection_id,
                name,
                len(image_ids))
            return memory_id
        except Exception as e:
            logger.error(
                "فشل في تخزين مجموعة الصور %s: %s",
                collection_id,
                str(e))
            raise

    async def retrieve_image_collection(
        self,
        collection_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        استرجاع مجموعة صور

        Args:
            collection_id: معرف المجموعة

        Returns:
            بيانات المجموعة إذا وجدت، وإلا None
        """
        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            memory_type=MemoryTypeEnum.LONG_TERM,
            tags=["collection:" + collection_id, "image_collection"],
            page_size=1
        )

        # استرجاع الذكريات
        try:
            memories = await self.memory_service.search_memories(memory_query)
            if not memories:
                logger.warning(
                    "لم يتم العثور على مجموعة الصور %s",
                    collection_id)
                return None

            # تحويل المحتوى من سلسلة نصية إلى كائن
            collection_data = json.loads(memories[0].content)
            logger.info("تم استرجاع مجموعة الصور %s بنجاح", collection_id)
            return collection_data
        except Exception as e:
            logger.error(
                "فشل في استرجاع مجموعة الصور %s: %s",
                collection_id,
                str(e))
            raise

    async def search_images(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        البحث في الصور

        Args:
            query: نص البحث
            tags: وسوم للتصفية (اختياري)
            metadata_filter: مرشح البيانات الوصفية (اختياري)
            start_date: تاريخ البداية للتصفية (اختياري)
            end_date: تاريخ النهاية للتصفية (اختياري)
            limit: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بنتائج البحث
        """
        if tags is None:
            tags = []
        if metadata_filter is None:
            metadata_filter = {}

        # إضافة وسوم البحث في الصور
        search_tags = ["image_metadata"] + tags

        # إنشاء استعلام الذاكرة
        memory_query = MemorySearch(
            query=query,
            memory_type=MemoryTypeEnum.SEMANTIC,
            tags=search_tags,
            created_after=start_date,
            created_before=end_date,
            page_size=limit,
            semantic_search=True
        )

        # استرجاع الذكريات
        try:
            memories = await self.memory_service.search_memories(memory_query)

            # تحويل المحتوى من سلسلة نصية إلى كائن
            results_list = []
            for memory in memories:
                image_data = json.loads(memory.content)
                # إضافة البيانات الوصفية إلى النتيجة
                if hasattr(memory, 'meta_data') and memory.meta_data:
                    image_data.update(memory.meta_data)
                results_list.append(image_data)

            logger.info(
                "تم العثور على %s صورة مطابقة للبحث",
                len(results_list))
            return results_list
        except Exception as e:
            logger.error("فشل في البحث في الصور: %s", str(e))
            raise

    async def get_similar_images(
        self,
        image_id: str,
        similarity_threshold: float = 0.7,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        الحصول على صور مشابهة

        Args:
            image_id: معرف الصورة المرجعية
            similarity_threshold: عتبة التشابه (0.0 - 1.0)
            limit: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بالصور المشابهة
        """
        # أولاً، استرجاع بيانات الصورة المرجعية
        reference_metadata = await self.retrieve_image_metadata(image_id)
        if not reference_metadata:
            logger.warning("لم يتم العثور على الصورة المرجعية %s", image_id)
            return []

        # استخراج الميزات المهمة للمقارنة
        reference_features = reference_metadata.get("features", {})

        # البحث في جميع الصور
        all_images_query = MemorySearch(
            memory_type=MemoryTypeEnum.SEMANTIC,
            tags=["image_metadata"],
            page_size=1000  # حد أعلى للبحث الأولي
        )

        try:
            memories = await self.memory_service.search_memories(all_images_query)

            # حساب التشابه مع كل صورة
            similar_images = []
            for memory in memories:
                image_data = json.loads(memory.content)
                current_image_id = image_data.get("image_id")

                # تجاهل الصورة المرجعية نفسها
                if current_image_id == image_id:
                    continue

                # حساب التشابه (هذا مثال بسيط، يمكن تحسينه)
                current_features = image_data.get("features", {})
                similarity_score = self._calculate_similarity(
                    reference_features, current_features)

                if similarity_score >= similarity_threshold:
                    image_data["similarity_score"] = similarity_score
                    similar_images.append(image_data)

            # ترتيب النتائج حسب درجة التشابه
            similar_images.sort(
                key=lambda x: x["similarity_score"],
                reverse=True)

            # تحديد النتائج حسب الحد المطلوب
            similar_images = similar_images[:limit]

            logger.info(
                "تم العثور على %s صورة مشابهة للصورة %s",
                len(similar_images),
                image_id)
            return similar_images
        except Exception as e:
            logger.error(
                "فشل في البحث عن صور مشابهة للصورة %s: %s",
                image_id,
                str(e))
            raise


def get_memory_usage():
    return psutil.Process().memory_info().rss / 1024 / 1024
