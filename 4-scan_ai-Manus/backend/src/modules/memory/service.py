"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/memory/service.py

خدمة إدارة الذاكرة المركزية

يوفر هذا الملف خدمة إدارة الذاكرة المركزية لنظام Gaara ERP، بما في ذلك:
- إنشاء وتحديث واسترجاع وحذف الذكريات
- البحث في الذاكرة (نصي ودلالي)
- إدارة العلامات والكيانات
- إدارة الصلاحيات والوصول
- تحليل وإحصاء البيانات
- التكامل مع الذكاء الاصطناعي
"""

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session

from .ai_integration import ai_integration
from .config import default_config as config
from .models import (
    Entity,
    Memory,
    MemoryAccess,
    MemoryAccessLog,
    MemoryCategory,
    MemoryStats,
    MemoryType,
    Tag,
)
from .schemas import (
    EntityCreate,
    MemoryAccessLogCreate,
    MemoryCreate,
    MemoryList,
    MemoryResponse,
    MemorySearch,
    MemoryUpdate,
    SemanticSearchResult,
    SemanticSearchResults,
    TagCreate,
)

# إعداد التسجيل
logger = logging.getLogger(__name__)


class MemoryService:
    """خدمة إدارة الذاكرة المركزية"""

    def __init__(self, db: Session):
        """
        تهيئة خدمة إدارة الذاكرة

        المعلمات:
            db (Session): جلسة قاعدة البيانات
        """
        self.db = db
        self.config = config

    # ==================== وظائف إدارة الذاكرة ====================

    def create_memory(self, memory_data: MemoryCreate) -> Memory:
        """
        إنشاء ذاكرة جديدة

        المعلمات:
            memory_data (MemoryCreate): بيانات الذاكرة المراد إنشاؤها

        العوائد:
            Memory: كائن الذاكرة المنشأ
        """
        try:
            # إنشاء كائن الذاكرة
            memory_dict = memory_data.dict(exclude={"tags"})
            memory_id = str(uuid.uuid4())
            memory_dict["id"] = memory_id

            # حساب تاريخ انتهاء الصلاحية
            if memory_dict.get("retention_days"):
                expiry_date = datetime.now(
                    timezone.utc) + timedelta(days=memory_dict["retention_days"])
                memory_dict["expiry_date"] = expiry_date

            # إنشاء ملخص إذا كان التلخيص التلقائي ممكّناً
            if config.ai_integration.auto_summarization and not memory_dict.get(
                    "summary"):
                memory_dict["summary"] = ai_integration.generate_summary(
                    memory_data.content)

            # إنشاء التضمين إذا كان التكامل مع الذكاء الاصطناعي ممكّناً
            if config.ai_integration.enabled:
                embedding = ai_integration.generate_embedding(
                    memory_data.content)
                memory_dict["embedding"] = embedding
                memory_dict["embedding_model"] = config.ai_integration.embedding_model

            # إنشاء كائن الذاكرة
            memory = Memory(**memory_dict)

            # إضافة العلامات
            if memory_data.tags:
                for tag_name in memory_data.tags:
                    tag = self.db.query(Tag).filter(
                        Tag.name == tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        self.db.add(tag)
                        self.db.flush()
                    memory.tags.append(tag)

            # حفظ الذاكرة في قاعدة البيانات
            self.db.add(memory)
            self.db.commit()
            self.db.refresh(memory)

            # تسجيل عملية الإنشاء
            self._log_memory_access(
                MemoryAccessLogCreate(
                    memory_id=memory.id,
                    user_id=memory_data.created_by,
                    action="create",
                    success=True
                )
            )

            logger.info("تم إنشاء ذاكرة جديدة بنجاح: %s", memory.id)
            return memory

        except Exception as e:
            self.db.rollback()
            logger.error("فشل إنشاء ذاكرة جديدة: %s", str(e))
            raise

    def get_memory(
            self,
            memory_id: str,
            user_id: Optional[str] = None) -> Optional[Memory]:
        """
        استرجاع ذاكرة بواسطة المعرف

        المعلمات:
            memory_id (str): معرف الذاكرة
            user_id (Optional[str]): معرف المستخدم للتحقق من الصلاحيات

        العوائد:
            Optional[Memory]: كائن الذاكرة إذا وجد، وإلا None
        """
        try:
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id,
                Memory.is_deleted.is_(False)
            ).first()

            if memory:
                # التحقق من صلاحيات الوصول
                if not self._check_memory_access(memory, user_id):
                    logger.warning(
                        "تم رفض الوصول للذاكرة %s للمستخدم %s",
                        memory_id,
                        user_id)
                    return None

                # تسجيل عملية القراءة
                self._log_memory_access(
                    MemoryAccessLogCreate(
                        memory_id=memory.id,
                        user_id=user_id,
                        action="read",
                        success=True
                    )
                )

                return memory

            return None

        except Exception as e:
            logger.error("فشل استرجاع الذاكرة %s: %s", memory_id, str(e))
            return None

    def update_memory(
            self,
            memory_id: str,
            memory_data: MemoryUpdate,
            user_id: Optional[str] = None) -> Optional[Memory]:
        """
        تحديث ذاكرة موجودة

        المعلمات:
            memory_id (str): معرف الذاكرة
            memory_data (MemoryUpdate): بيانات التحديث
            user_id (Optional[str]): معرف المستخدم للتحقق من الصلاحيات

        العوائد:
            Optional[Memory]: كائن الذاكرة المحدث إذا نجح التحديث، وإلا None
        """
        try:
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id,
                Memory.is_deleted.is_(False)
            ).first()

            if not memory:
                logger.warning(
                    "لم يتم العثور على الذاكرة %s للتحديث", memory_id)
                return None

            # التحقق من صلاحيات التحديث
            if not self._check_memory_access(memory, user_id, "update"):
                logger.warning(
                    "تم رفض تحديث الذاكرة %s للمستخدم %s",
                    memory_id,
                    user_id)
                return None

            # تحديث حقول الذاكرة
            update_data = memory_data.dict(exclude_unset=True)

            # تحديث العلامات إذا تم توفيرها
            if "tags" in update_data:
                # إزالة جميع العلامات الحالية
                memory.tags = []

                # إضافة العلامات الجديدة
                for tag_name in update_data["tags"]:
                    tag = self.db.query(Tag).filter(
                        Tag.name == tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        self.db.add(tag)
                        self.db.flush()
                    memory.tags.append(tag)

                # إزالة العلامات من بيانات التحديث
                del update_data["tags"]

            # تحديث تاريخ التعديل
            update_data["updated_at"] = datetime.now(timezone.utc)

            # تطبيق التحديثات
            for field, value in update_data.items():
                setattr(memory, field, value)

            # حفظ التغييرات
            self.db.commit()
            self.db.refresh(memory)

            # تسجيل عملية التحديث
            self._log_memory_access(
                MemoryAccessLogCreate(
                    memory_id=memory.id,
                    user_id=user_id,
                    action="update",
                    success=True
                )
            )

            logger.info("تم تحديث الذاكرة %s بنجاح", memory_id)
            return memory

        except Exception as e:
            self.db.rollback()
            logger.error("فشل تحديث الذاكرة %s: %s", memory_id, str(e))
            return None

    def delete_memory(
            self,
            memory_id: str,
            user_id: Optional[str] = None,
            permanent: bool = False) -> bool:
        """
        حذف ذاكرة

        المعلمات:
            memory_id (str): معرف الذاكرة
            user_id (Optional[str]): معرف المستخدم للتحقق من الصلاحيات
            permanent (bool): ما إذا كان الحذف دائماً أم منطقياً

        العوائد:
            bool: True إذا نجح الحذف، وإلا False
        """
        try:
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id).first()

            if not memory:
                logger.warning("لم يتم العثور على الذاكرة %s للحذف", memory_id)
                return False

            # التحقق من صلاحيات الحذف
            if not self._check_memory_access(memory, user_id, "delete"):
                logger.warning(
                    "تم رفض حذف الذاكرة %s للمستخدم %s",
                    memory_id,
                    user_id)
                return False

            if permanent:
                # حذف دائم
                self.db.delete(memory)
            else:
                # حذف منطقي
                memory.is_deleted = True

            # حفظ التغييرات
            self.db.commit()

            # تسجيل عملية الحذف
            self._log_memory_access(
                MemoryAccessLogCreate(
                    memory_id=memory.id,
                    user_id=user_id,
                    action="delete",
                    success=True,
                    details={"permanent": permanent}
                )
            )

            logger.info(
                "تم حذف الذاكرة بنجاح: %s (دائم: %s)",
                memory_id,
                permanent)
            return True

        except Exception as e:
            self.db.rollback()
            logger.error("فشل حذف الذاكرة %s: %s", memory_id, str(e))
            return False

    def archive_memory(
            self,
            memory_id: str,
            user_id: Optional[str] = None) -> bool:
        """
        أرشفة ذاكرة

        المعلمات:
            memory_id (str): معرف الذاكرة
            user_id (Optional[str]): معرف المستخدم للتحقق من الصلاحيات

        العوائد:
            bool: True إذا نجحت الأرشفة، وإلا False
        """
        try:
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id,
                Memory.is_deleted.is_(False)
            ).first()

            if not memory:
                logger.warning(
                    "لم يتم العثور على الذاكرة %s للأرشفة", memory_id)
                return False

            # التحقق من صلاحيات الأرشفة
            if not self._check_memory_access(memory, user_id, "archive"):
                logger.warning(
                    "تم رفض أرشفة الذاكرة %s للمستخدم %s",
                    memory_id,
                    user_id)
                return False

            # أرشفة الذاكرة
            memory.is_archived = True

            # حفظ التغييرات
            self.db.commit()

            # تسجيل عملية الأرشفة
            self._log_memory_access(
                MemoryAccessLogCreate(
                    memory_id=memory.id,
                    user_id=user_id,
                    action="archive",
                    success=True
                )
            )

            logger.info("تم أرشفة الذاكرة بنجاح: %s", memory_id)
            return True

        except Exception as e:
            self.db.rollback()
            logger.error("فشل أرشفة الذاكرة %s: %s", memory_id, str(e))
            return False

    def restore_memory(
            self,
            memory_id: str,
            user_id: Optional[str] = None) -> bool:
        """
        استعادة ذاكرة مؤرشفة أو محذوفة

        المعلمات:
            memory_id (str): معرف الذاكرة
            user_id (Optional[str]): معرف المستخدم للتحقق من الصلاحيات

        العوائد:
            bool: True إذا نجحت الاستعادة، وإلا False
        """
        try:
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id).first()

            if not memory:
                logger.warning(
                    "لم يتم العثور على الذاكرة %s للاستعادة", memory_id)
                return False

            # التحقق من صلاحيات الاستعادة
            if not self._check_memory_access(memory, user_id, "restore"):
                logger.warning(
                    "تم رفض استعادة الذاكرة %s للمستخدم %s",
                    memory_id,
                    user_id)
                return False

            # استعادة الذاكرة
            memory.is_archived = False
            memory.is_deleted = False

            # حفظ التغييرات
            self.db.commit()

            # تسجيل عملية الاستعادة
            self._log_memory_access(
                MemoryAccessLogCreate(
                    memory_id=memory.id,
                    user_id=user_id,
                    action="restore",
                    success=True
                )
            )

            logger.info("تم استعادة الذاكرة بنجاح: %s", memory_id)
            return True

        except Exception as e:
            self.db.rollback()
            logger.error("فشل استعادة الذاكرة %s: %s", memory_id, str(e))
            return False

    # ==================== وظائف البحث في الذاكرة ====================

    def search_memories(self, search_params: MemorySearch,
                        user_id: Optional[str] = None) -> MemoryList:
        """
        البحث في الذاكرة

        المعلمات:
            search_params (MemorySearch): معلمات البحث
            user_id (Optional[str]): معرف المستخدم للتحقق من الصلاحيات

        العوائد:
            MemoryList: قائمة الذكريات المطابقة لمعلمات البحث
        """
        try:
            # بناء استعلام البحث
            query = self.db.query(Memory)

            # تطبيق معلمات البحث
            if not search_params.include_deleted:
                query = query.filter(Memory.is_deleted.is_(False))

            if not search_params.include_archived:
                query = query.filter(Memory.is_archived.is_(False))

            if search_params.query:
                query = query.filter(
                    or_(
                        Memory.title.ilike(f"%{search_params.query}%"),
                        Memory.content.ilike(f"%{search_params.query}%"),
                        Memory.summary.ilike(f"%{search_params.query}%")
                    )
                )

            if search_params.memory_type:
                query = query.filter(
                    Memory.memory_type == search_params.memory_type)

            if search_params.category:
                query = query.filter(Memory.category == search_params.category)

            if search_params.access_level:
                query = query.filter(
                    Memory.access_level == search_params.access_level)

            if search_params.source_module:
                query = query.filter(
                    Memory.source_module == search_params.source_module)

            if search_params.created_by:
                query = query.filter(
                    Memory.created_by == search_params.created_by)

            if search_params.created_after:
                query = query.filter(
                    Memory.created_at >= search_params.created_after)

            if search_params.created_before:
                query = query.filter(
                    Memory.created_at <= search_params.created_before)

            if search_params.tags:
                for tag in search_params.tags:
                    query = query.filter(Memory.tags.any(Tag.name == tag))

            if search_params.min_importance:
                query = query.filter(
                    Memory.importance_score >= search_params.min_importance)

            # تطبيق الترتيب
            if search_params.sort_by == "created_at":
                if search_params.sort_order == "desc":
                    query = query.order_by(desc(Memory.created_at))
                else:
                    query = query.order_by(asc(Memory.created_at))
            elif search_params.sort_by == "importance":
                if search_params.sort_order == "desc":
                    query = query.order_by(desc(Memory.importance_score))
                else:
                    query = query.order_by(asc(Memory.importance_score))
            elif search_params.sort_by == "title":
                if search_params.sort_order == "desc":
                    query = query.order_by(desc(Memory.title))
                else:
                    query = query.order_by(asc(Memory.title))

            # تطبيق التصفيح
            total = query.count()
            query = query.offset(search_params.skip).limit(search_params.limit)

            # تنفيذ الاستعلام
            memories = query.all()

            # تصفية النتائج حسب صلاحيات المستخدم
            if user_id:
                memories = [
                    m for m in memories if self._check_memory_access(
                        m, user_id)]

            # تسجيل عملية البحث
            logger.info(
                "تم تنفيذ بحث في الذاكرة: %s نتيجة من أصل %s",
                len(memories),
                total)

            # إرجاع النتائج
            return MemoryList(
                items=[
                    MemoryResponse.from_orm(m) for m in memories],
                total=total,
                page=search_params.skip //
                search_params.limit +
                1 if search_params.limit > 0 else 1,
                page_size=search_params.limit,
                pages=(
                    total +
                    search_params.limit -
                    1) //
                search_params.limit if search_params.limit > 0 else 1)

        except Exception as e:
            logger.error("فشل البحث في الذاكرة: %s", str(e))
            return MemoryList(
                items=[],
                total=0,
                page=1,
                page_size=search_params.limit,
                pages=0)

    def semantic_search(
            self,
            query: str,
            limit: int = 10,
            threshold: float = 0.7,
            user_id: Optional[str] = None) -> SemanticSearchResults:
        """
        البحث الدلالي في الذاكرة

        المعلمات:
            query (str): استعلام البحث
            limit (int): الحد الأقصى لعدد النتائج
            threshold (float): عتبة التشابه الدلالي (0-1)
            user_id (Optional[str]): معرف المستخدم للتحقق من الصلاحيات

        العوائد:
            SemanticSearchResults: نتائج البحث الدلالي
        """
        try:
            if not config.ai_integration.enabled:
                logger.warning(
                    "البحث الدلالي غير ممكّن: تكامل الذكاء الاصطناعي غير مفعّل")
                return SemanticSearchResults(results=[], query=query)

            # إنشاء تضمين للاستعلام
            query_embedding = ai_integration.generate_embedding(query)

            # استرجاع جميع الذكريات التي تحتوي على تضمين
            memories = self.db.query(Memory).filter(
                Memory.embedding.isnot(None),
                Memory.is_deleted.is_(False)
            ).all()

            # تصفية الذكريات حسب صلاحيات المستخدم
            if user_id:
                memories = [
                    m for m in memories if self._check_memory_access(
                        m, user_id)]

            # حساب درجة التشابه لكل ذاكرة
            results = []
            for memory in memories:
                similarity = ai_integration.calculate_similarity(
                    query_embedding, memory.embedding)
                if similarity >= threshold:
                    results.append(
                        SemanticSearchResult(
                            memory=MemoryResponse.from_orm(memory),
                            similarity=similarity
                        )
                    )

            # ترتيب النتائج حسب درجة التشابه (تنازلياً)
            results.sort(key=lambda x: x.similarity, reverse=True)

            # تطبيق الحد الأقصى لعدد النتائج
            results = results[:limit]

            # تسجيل عملية البحث
            logger.info(
                "تم تنفيذ بحث دلالي في الذاكرة: %s نتيجة",
                len(results))

            # إرجاع النتائج
            return SemanticSearchResults(
                results=results, query=query, total=len(results))

        except Exception as e:
            logger.error("فشل البحث الدلالي في الذاكرة: %s", str(e))
            return SemanticSearchResults(results=[], query=query)

    # ==================== وظائف إدارة العلامات والكيانات ====================

    def get_all_tags(self) -> List[Tag]:
        """
        استرجاع جميع العلامات

        العوائد:
            List[Tag]: قائمة جميع العلامات
        """
        try:
            return self.db.query(Tag).all()
        except Exception as e:
            logger.error("فشل استرجاع العلامات: %s", str(e))
            return []

    def create_tag(self, tag_data: TagCreate) -> Optional[Tag]:
        """
        إنشاء علامة جديدة

        المعلمات:
            tag_data (TagCreate): بيانات العلامة

        العوائد:
            Optional[Tag]: كائن العلامة المنشأ، أو None في حالة الفشل
        """
        try:
            # التحقق من وجود العلامة
            existing_tag = self.db.query(Tag).filter(
                Tag.name == tag_data.name).first()
            if existing_tag:
                return existing_tag

            # إنشاء علامة جديدة
            tag = Tag(**tag_data.dict())
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)

            logger.info("تم إنشاء علامة جديدة: %s", tag.name)
            return tag

        except Exception as e:
            self.db.rollback()
            logger.error("فشل إنشاء علامة: %s", str(e))
            return None

    def get_all_entities(self) -> List[Entity]:
        """
        استرجاع جميع الكيانات

        العوائد:
            List[Entity]: قائمة جميع الكيانات
        """
        try:
            return self.db.query(Entity).all()
        except Exception as e:
            logger.error("فشل استرجاع الكيانات: %s", str(e))
            return []

    def create_entity(self, entity_data: EntityCreate) -> Optional[Entity]:
        """
        إنشاء كيان جديد

        المعلمات:
            entity_data (EntityCreate): بيانات الكيان

        العوائد:
            Optional[Entity]: كائن الكيان المنشأ، أو None في حالة الفشل
        """
        try:
            # التحقق من وجود الكيان
            existing_entity = self.db.query(Entity).filter(
                Entity.name == entity_data.name,
                Entity.entity_type == entity_data.entity_type
            ).first()

            if existing_entity:
                return existing_entity

            # تحويل metadata إلى entity_data
            entity_dict = entity_data.dict()
            if "metadata" in entity_dict:
                entity_dict["entity_data"] = entity_dict.pop("metadata")

            # إنشاء كيان جديد
            entity = Entity(**entity_dict)
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)

            logger.info(
                "تم إنشاء كيان جديد: %s (%s)",
                entity.name,
                entity.entity_type)
            return entity

        except Exception as e:
            self.db.rollback()
            logger.error("فشل إنشاء كيان: %s", str(e))
            return None

    # ==================== وظائف إدارة الصلاحيات والوصول ====================

    def _check_memory_access(
            self,
            memory: Memory,
            user_id: Optional[str],
            action: str = "read") -> bool:
        """
        التحقق من صلاحيات الوصول للذاكرة

        المعلمات:
            memory (Memory): كائن الذاكرة
            user_id (Optional[str]): معرف المستخدم
            action (str): نوع العملية (read, update, delete, archive, restore)

        العوائد:
            bool: True إذا كان المستخدم يملك الصلاحية، وإلا False
        """
        # إذا كان المستخدم هو منشئ الذاكرة، فلديه جميع الصلاحيات
        if user_id and memory.created_by == user_id:
            return True

        # التحقق من مستوى الوصول
        if memory.access_level == MemoryAccess.PUBLIC:
            # الذاكرة عامة، يمكن للجميع قراءتها
            if action == "read":
                return True

        elif memory.access_level == MemoryAccess.SYSTEM:
            # الذاكرة على مستوى النظام، يمكن للمسؤولين الوصول إليها
            # هنا يجب التحقق من صلاحيات المستخدم في النظام
            # (تنفيذ منطق التحقق من صلاحيات المسؤول)
            pass

        elif memory.access_level == MemoryAccess.MODULE:
            # الذاكرة على مستوى المديول، يمكن للمستخدمين المصرح لهم بالمديول الوصول إليها
            # (تنفيذ منطق التحقق من صلاحيات المديول)
            pass

        elif memory.access_level == MemoryAccess.GROUP:
            # الذاكرة على مستوى المجموعة، يمكن لأعضاء المجموعة الوصول إليها
            # (تنفيذ منطق التحقق من عضوية المجموعة)
            pass

        # افتراضياً، إذا لم يتم التحقق من أي من الشروط أعلاه، فلا يملك المستخدم
        # الصلاحية
        return False

    def _log_memory_access(self, log_data: MemoryAccessLogCreate) -> None:
        """
        تسجيل عملية الوصول للذاكرة

        المعلمات:
            log_data (MemoryAccessLogCreate): بيانات السجل
        """
        try:
            log = MemoryAccessLog(**log_data.dict())
            self.db.add(log)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error("فشل تسجيل عملية الوصول للذاكرة: %s", str(e))

    # ==================== وظائف الإحصاء والتحليل ====================

    def generate_memory_stats(self) -> Optional[MemoryStats]:
        """
        إنشاء إحصائيات الذاكرة

        العوائد:
            Optional[MemoryStats]: كائن إحصائيات الذاكرة، أو None في حالة الفشل
        """
        try:
            # حساب إجمالي الذكريات
            total_memories = self.db.query(Memory).count()

            # حساب الذكريات النشطة
            active_memories = self.db.query(Memory).filter(
                Memory.is_archived.is_(False),
                Memory.is_deleted.is_(False)
            ).count()

            # حساب الذكريات المؤرشفة
            archived_memories = self.db.query(Memory).filter(
                Memory.is_archived.is_(True),
                Memory.is_deleted.is_(False)
            ).count()

            # حساب الذكريات المحذوفة
            deleted_memories = self.db.query(Memory).filter(
                Memory.is_deleted.is_(True)
            ).count()

            # حساب متوسط درجة الأهمية
            avg_importance = self.db.query(
                func.avg(
                    Memory.importance_score)).filter(
                Memory.is_deleted.is_(False)).scalar() or 0.0

            # حساب إحصائيات أنواع الذاكرة
            memory_type_counts = {}
            for memory_type in MemoryType:
                count = self.db.query(Memory).filter(
                    Memory.memory_type == memory_type,
                    Memory.is_deleted.is_(False)
                ).count()
                memory_type_counts[memory_type.value] = count

            # حساب إحصائيات فئات الذاكرة
            category_counts = {}
            for category in MemoryCategory:
                count = self.db.query(Memory).filter(
                    Memory.category == category,
                    Memory.is_deleted.is_(False)
                ).count()
                category_counts[category.value] = count

            # حساب إحصائيات مستويات الوصول
            access_level_counts = {}
            for access_level in MemoryAccess:
                count = self.db.query(Memory).filter(
                    Memory.access_level == access_level,
                    Memory.is_deleted.is_(False)
                ).count()
                access_level_counts[access_level.value] = count

            # إنشاء كائن الإحصائيات
            stats = MemoryStats(
                date=datetime.now(timezone.utc),
                total_memories=total_memories,
                active_memories=active_memories,
                archived_memories=archived_memories,
                deleted_memories=deleted_memories,
                avg_importance_score=float(avg_importance),
                memory_type_counts=memory_type_counts,
                category_counts=category_counts,
                access_level_counts=access_level_counts
            )

            # حفظ الإحصائيات في قاعدة البيانات
            self.db.add(stats)
            self.db.commit()
            self.db.refresh(stats)

            logger.info("تم إنشاء إحصائيات الذاكرة بنجاح")
            return stats

        except Exception as e:
            self.db.rollback()
            logger.error("فشل إنشاء إحصائيات الذاكرة: %s", str(e))
            return None

    def get_memory_stats_history(self, days: int = 30) -> List[MemoryStats]:
        """
        استرجاع سجل إحصائيات الذاكرة

        المعلمات:
            days (int): عدد الأيام للاسترجاع

        العوائد:
            List[MemoryStats]: قائمة إحصائيات الذاكرة
        """
        try:
            start_date = datetime.now(timezone.utc) - timedelta(days=days)

            stats = self.db.query(MemoryStats).filter(
                MemoryStats.date >= start_date
            ).order_by(MemoryStats.date).all()

            return stats

        except Exception as e:
            logger.error("فشل استرجاع سجل إحصائيات الذاكرة: %s", str(e))
            return []

    def cleanup_expired_memories(self) -> int:
        """
        تنظيف الذكريات منتهية الصلاحية

        العوائد:
            int: عدد الذكريات التي تم تنظيفها
        """
        try:
            # البحث عن الذكريات منتهية الصلاحية
            expired_memories = self.db.query(Memory).filter(
                Memory.expiry_date.isnot(None),
                Memory.expiry_date <= datetime.now(timezone.utc),
                Memory.is_deleted.is_(False)
            ).all()

            # تحديث حالة الذكريات منتهية الصلاحية
            count = 0
            for memory in expired_memories:
                if config.memory.auto_delete_expired:
                    # حذف الذكريات منتهية الصلاحية
                    memory.is_deleted = True
                else:
                    # أرشفة الذكريات منتهية الصلاحية
                    memory.is_archived = True

                # تسجيل عملية التنظيف
                self._log_memory_access(
                    MemoryAccessLogCreate(
                        memory_id=memory.id,
                        action="cleanup",
                        success=True,
                        details={
                            "reason": "expired",
                            "action": "delete" if config.memory.auto_delete_expired else "archive"}))

                count += 1

            # حفظ التغييرات
            if count > 0:
                self.db.commit()
                logger.info("تم تنظيف %s ذكريات منتهية الصلاحية", count)

            return count

        except Exception as e:
            self.db.rollback()
            logger.error("فشل تنظيف الذكريات منتهية الصلاحية: %s", str(e))
            return 0

    # ==================== وظائف التكامل مع الذكاء الاصطناعي =================

    def extract_entities_from_memory(self, memory_id: str) -> bool:
        """
        استخراج الكيانات من الذاكرة باستخدام الذكاء الاصطناعي

        المعلمات:
            memory_id (str): معرف الذاكرة

        العوائد:
            bool: True إذا نجحت العملية، وإلا False
        """
        try:
            if not config.ai_integration.enabled:
                logger.warning(
                    "استخراج الكيانات غير ممكّن: تكامل الذكاء الاصطناعي غير مفعّل")
                return False

            # استرجاع الذاكرة
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id).first()
            if not memory:
                logger.warning(
                    "لم يتم العثور على الذاكرة %s لاستخراج الكيانات",
                    memory_id)
                return False

            # استخراج الكيانات من محتوى الذاكرة
            entities = ai_integration.extract_entities(memory.content)

            # إضافة الكيانات إلى الذاكرة
            for entity_data in entities:
                # تحويل metadata إلى entity_data
                if "metadata" in entity_data:
                    entity_data["entity_data"] = entity_data.pop("metadata")

                # إنشاء أو استرجاع الكيان
                entity = self.db.query(Entity).filter(
                    Entity.name == entity_data["name"],
                    Entity.entity_type == entity_data["entity_type"]
                ).first()

                if not entity:
                    entity = Entity(**entity_data)
                    self.db.add(entity)
                    self.db.flush()

                # إضافة الكيان إلى الذاكرة إذا لم يكن موجوداً بالفعل
                if entity not in memory.entities:
                    memory.entities.append(entity)

            # حفظ التغييرات
            self.db.commit()

            logger.info(
                "تم استخراج %s كيانات من الذاكرة %s",
                len(entities),
                memory_id)
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(
                "فشل استخراج الكيانات من الذاكرة %s: %s",
                memory_id,
                str(e))
            return False

    def generate_memory_summary(self, memory_id: str) -> bool:
        """
        إنشاء ملخص للذاكرة باستخدام الذكاء الاصطناعي

        المعلمات:
            memory_id (str): معرف الذاكرة

        العوائد:
            bool: True إذا نجحت العملية، وإلا False
        """
        try:
            if not config.ai_integration.enabled:
                logger.warning(
                    "إنشاء الملخص غير ممكّن: تكامل الذكاء الاصطناعي غير مفعّل")
                return False

            # استرجاع الذاكرة
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id).first()
            if not memory:
                logger.warning(
                    "لم يتم العثور على الذاكرة %s لإنشاء الملخص",
                    memory_id)
                return False

            # إنشاء ملخص للذاكرة
            summary = ai_integration.generate_summary(memory.content)

            # تحديث الذاكرة
            memory.summary = summary

            # حفظ التغييرات
            self.db.commit()

            logger.info("تم إنشاء ملخص للذاكرة %s", memory_id)
            return True

        except Exception as e:
            self.db.rollback()
            logger.error("فشل إنشاء ملخص للذاكرة %s: %s", memory_id, str(e))
            return False

    def update_memory_embedding(self, memory_id: str) -> bool:
        """
        تحديث تضمين الذاكرة باستخدام الذكاء الاصطناعي

        المعلمات:
            memory_id (str): معرف الذاكرة

        العوائد:
            bool: True إذا نجحت العملية، وإلا False
        """
        try:
            if not config.ai_integration.enabled:
                logger.warning(
                    "تحديث التضمين غير ممكّن: تكامل الذكاء الاصطناعي غير مفعّل")
                return False

            # استرجاع الذاكرة
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id).first()
            if not memory:
                logger.warning(
                    "لم يتم العثور على الذاكرة %s لتحديث التضمين",
                    memory_id)
                return False

            # إنشاء تضمين للذاكرة
            embedding = ai_integration.generate_embedding(memory.content)

            # تحديث الذاكرة
            memory.embedding = embedding
            memory.embedding_model = config.ai_integration.embedding_model

            # حفظ التغييرات
            self.db.commit()

            logger.info("تم تحديث تضمين الذاكرة %s", memory_id)
            return True

        except Exception as e:
            self.db.rollback()
            logger.error("فشل تحديث تضمين الذاكرة %s: %s", memory_id, str(e))
            return False

    def calculate_memory_importance(self, memory_id: str) -> bool:
        """
        حساب درجة أهمية الذاكرة باستخدام الذكاء الاصطناعي

        المعلمات:
            memory_id (str): معرف الذاكرة

        العوائد:
            bool: True إذا نجحت العملية، وإلا False
        """
        try:
            if not config.ai_integration.enabled:
                logger.warning(
                    "حساب درجة الأهمية غير ممكّن: تكامل الذكاء الاصطناعي غير مفعّل")
                return False

            # استرجاع الذاكرة
            memory = self.db.query(Memory).filter(
                Memory.id == memory_id).first()
            if not memory:
                logger.warning(
                    "لم يتم العثور على الذاكرة %s لحساب درجة الأهمية",
                    memory_id)
                return False

            # حساب درجة أهمية الذاكرة
            importance = ai_integration.calculate_importance(
                content=memory.content,
                category=memory.category.value if memory.category else None,
                memory_type=memory.memory_type.value if memory.memory_type else None,
                access_count=self.db.query(MemoryAccessLog).filter(
                    MemoryAccessLog.memory_id == memory.id,
                    MemoryAccessLog.action == "read").count())

            # تحديث الذاكرة
            memory.importance_score = importance

            # حفظ التغييرات
            self.db.commit()

            logger.info(
                "تم حساب درجة أهمية الذاكرة %s: %s",
                memory_id,
                importance)
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(
                "فشل حساب درجة أهمية الذاكرة %s: %s",
                memory_id,
                str(e))
            return False

    def batch_process_memories(
            self, action: str, filter_params: Optional[Dict] = None) -> Tuple[int, int]:
        """
        معالجة دفعة من الذكريات

        المعلمات:
            action (str): نوع المعالجة (extract_entities, generate_summary, update_embedding, calculate_importance)
            filter_params (Optional[Dict]): معلمات التصفية

        العوائد:
            Tuple[int, int]: (عدد الذكريات التي تمت معالجتها بنجاح، إجمالي عدد الذكريات)
        """
        try:
            # بناء استعلام البحث
            query = self.db.query(Memory)

            # تطبيق معلمات التصفية
            if filter_params:
                if filter_params.get("is_deleted") is not None:
                    query = query.filter(
                        Memory.is_deleted == filter_params["is_deleted"])

                if filter_params.get("is_archived") is not None:
                    query = query.filter(
                        Memory.is_archived == filter_params["is_archived"])

                if filter_params.get("memory_type"):
                    query = query.filter(
                        Memory.memory_type == filter_params["memory_type"])

                if filter_params.get("category"):
                    query = query.filter(
                        Memory.category == filter_params["category"])

                if filter_params.get("created_after"):
                    query = query.filter(
                        Memory.created_at >= filter_params["created_after"])

                if filter_params.get("created_before"):
                    query = query.filter(
                        Memory.created_at <= filter_params["created_before"])

                if filter_params.get("limit"):
                    query = query.limit(filter_params["limit"])

            # تنفيذ الاستعلام
            memories = query.all()
            total = len(memories)

            # معالجة الذكريات
            success_count = 0
            for memory in memories:
                result = False

                if action == "extract_entities":
                    result = self.extract_entities_from_memory(memory.id)
                elif action == "generate_summary":
                    result = self.generate_memory_summary(memory.id)
                elif action == "update_embedding":
                    result = self.update_memory_embedding(memory.id)
                elif action == "calculate_importance":
                    result = self.calculate_memory_importance(memory.id)

                if result:
                    success_count += 1

            logger.info(
                "تمت معالجة %s من أصل %s ذكريات بنجاح (%s)",
                success_count,
                total,
                action)
            return success_count, total

        except Exception as e:
            logger.error(
                "فشل معالجة دفعة من الذكريات (%s): %s",
                action,
                str(e))
            return 0, 0
