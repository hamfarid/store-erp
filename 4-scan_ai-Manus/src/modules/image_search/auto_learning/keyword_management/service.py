# /home/ubuntu/image_search_integration/auto_learning/keyword_management/service.py

"""
خدمة إدارة الكلمات المفتاحية المتقدمة للبحث الذاتي الذكي

هذا الملف يحتوي على تنفيذ خدمة إدارة الكلمات المفتاحية المتقدمة،
مع دعم التصنيف المتقدم، تحليل الأداء، والتكامل مع الذاكرة المركزية.
"""

import logging
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session

from modules.image_search.auto_learning.keyword_management.models import (
    ConditionTypeEnum,
    KeywordCategory,
    PlantPartEnum,
    SearchKeyword
)
from modules.image_search.auto_learning.keyword_management.schemas import (
    KeywordCategoryCreate,
    KeywordCategoryResponse,
    KeywordStatistics,
    SearchKeywordCreate,
    SearchKeywordResponse,
    SearchKeywordUpdate,
    SemanticRelation
)

# استيراد خدمة الذاكرة المركزية
try:
    from ....memory_service.client import MemoryServiceClient
    memory_service_available = True
except ImportError:
    memory_service_available = False
    logging.warning("خدمة الذاكرة المركزية غير متوفرة. سيتم تعطيل ميزات التكامل مع الذاكرة.")

# استيراد خدمة الصلاحيات
try:
    from ....permissions.service import PermissionService
    permission_service_available = True
except ImportError:
    permission_service_available = False
    logging.warning("خدمة الصلاحيات غير متوفرة. سيتم تعطيل التحقق من الصلاحيات.")

logger = logging.getLogger(__name__)

# Add constants at the top of the file
NO_UPDATE_PERMISSION = "ليس لديك صلاحية تحديث كلمة مفتاحية"
NO_READ_PERMISSION = "ليس لديك صلاحية قراءة الكلمات المفتاحية"


class KeywordManagementService:
    """خدمة إدارة الكلمات المفتاحية المتقدمة"""

    def __init__(self, db: Session, user_id: Optional[int] = None):
        """
        تهيئة خدمة إدارة الكلمات المفتاحية

        المعلمات:
            db (Session): جلسة قاعدة البيانات
            user_id (Optional[int]): معرف المستخدم الحالي (للتحقق من الصلاحيات)
        """
        self.db = db
        self.user_id = user_id

        # تهيئة خدمة الذاكرة المركزية إذا كانت متوفرة
        if memory_service_available:
            self.memory_service = MemoryServiceClient()
        else:
            self.memory_service = None

        # تهيئة خدمة الصلاحيات إذا كانت متوفرة
        if permission_service_available and user_id:
            self.permission_service = PermissionService(db, user_id)
        else:
            self.permission_service = None

    def _check_permission(self, action: str, resource: str) -> bool:
        """
        التحقق من صلاحيات المستخدم

        المعلمات:
            action (str): الإجراء المطلوب (create, read, update, delete)
            resource (str): المورد المطلوب (keyword, category, search_result, search_session)

        العوائد:
            bool: True إذا كان المستخدم يملك الصلاحية، False خلاف ذلك
        """
        if not self.permission_service:
            return True  # إذا كانت خدمة الصلاحيات غير متوفرة، نفترض أن المستخدم يملك الصلاحية

        resource_map = {
            "keyword": "auto_learning.keyword",
            "category": "auto_learning.keyword_category",
            "search_result": "auto_learning.search_result",
            "search_session": "auto_learning.search_session"
        }

        resource_name = resource_map.get(resource, resource)

        return self.permission_service.check_permission(action, resource_name)

    def _log_to_memory(self, action: str, data: Dict[str, Any]) -> None:
        """
        تسجيل الإجراء في الذاكرة المركزية

        المعلمات:
            action (str): الإجراء المنفذ
            data (Dict[str, Any]): بيانات الإجراء
        """
        if not self.memory_service:
            return

        try:
            memory_data = {
                "module": "keyword_management",
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "user_id": self.user_id,
                "data": data
            }

            self.memory_service.store_memory("keyword_management", memory_data)
        except Exception as e:
            logger.error("حدث خطأ أثناء تسجيل الإجراء في الذاكرة المركزية: %s", str(e))

    def _keyword_to_response(self, keyword: SearchKeyword) -> SearchKeywordResponse:
        """
        تحويل نموذج الكلمة المفتاحية إلى نموذج الاستجابة

        المعلمات:
            keyword (SearchKeyword): نموذج الكلمة المفتاحية

        العوائد:
            SearchKeywordResponse: نموذج استجابة الكلمة المفتاحية
        """
        category_name = keyword.category.name if keyword.category else None

        return SearchKeywordResponse(
            id=keyword.id,
            keyword=keyword.keyword,
            description=keyword.description,
            plant_type=keyword.plant_type,
            condition_type=keyword.condition_type,
            plant_part=keyword.plant_part,
            category_id=keyword.category_id,
            priority=keyword.priority,
            max_results=keyword.max_results,
            min_trust_level=keyword.min_trust_level,
            trusted_sources_only=keyword.trusted_sources_only,
            search_engines=keyword.search_engines,
            semantic_relations=keyword.semantic_relations,
            search_count=keyword.search_count,
            success_count=keyword.success_count,
            success_rate=keyword.success_rate,
            total_results=keyword.total_results,
            last_search_at=keyword.last_search_at,
            is_active=keyword.is_active,
            created_at=keyword.created_at,
            updated_at=keyword.updated_at,
            created_by=keyword.created_by,
            updated_by=keyword.updated_by,
            category_name=category_name,
            condition_id=keyword.condition_id
        )

    def _category_to_response(self, category: KeywordCategory) -> KeywordCategoryResponse:
        """
        تحويل نموذج فئة الكلمات المفتاحية إلى نموذج الاستجابة

        المعلمات:
            category (KeywordCategory): نموذج فئة الكلمات المفتاحية

        العوائد:
            KeywordCategoryResponse: نموذج استجابة فئة الكلمات المفتاحية
        """
        # حساب عدد الكلمات المفتاحية في الفئة
        # pylint: disable=not-callable
        keywords_count = self.db.query(func.count(SearchKeyword.id)).filter(
            SearchKeyword.category_id == category.id
        ).scalar() or 0

        return KeywordCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            color=category.color,
            icon=category.icon,
            parent_id=category.parent_id,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
            keywords_count=keywords_count
        )

    # ===== إدارة الكلمات المفتاحية =====

    def create_keyword(self, keyword_data: SearchKeywordCreate) -> SearchKeywordResponse:
        """
        إنشاء كلمة مفتاحية جديدة

        المعلمات:
            keyword_data (SearchKeywordCreate): بيانات الكلمة المفتاحية الجديدة

        العوائد:
            SearchKeywordResponse: نموذج استجابة الكلمة المفتاحية

        يرفع:
            ValueError: إذا كانت الكلمة المفتاحية موجودة مسبقاً
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إنشاء كلمة مفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "keyword"):
            raise PermissionError("ليس لديك صلاحية إنشاء كلمة مفتاحية")

        try:
            # التحقق من عدم وجود الكلمة المفتاحية مسبقاً
            existing_keyword = self.db.query(SearchKeyword).filter(
                SearchKeyword.keyword == keyword_data.keyword,
                SearchKeyword.plant_type == keyword_data.plant_type,
                SearchKeyword.condition_type == keyword_data.condition_type,
                SearchKeyword.plant_part == keyword_data.plant_part
            ).first()

            if existing_keyword:
                raise ValueError(f"الكلمة المفتاحية موجودة مسبقاً: {keyword_data.keyword}")

            # إنشاء كلمة مفتاحية جديدة
            new_keyword = SearchKeyword(
                keyword=keyword_data.keyword,
                description=keyword_data.description,
                plant_type=keyword_data.plant_type,
                condition_type=keyword_data.condition_type,
                plant_part=keyword_data.plant_part,
                category_id=keyword_data.category_id,
                priority=keyword_data.priority,
                max_results=keyword_data.max_results,
                min_trust_level=keyword_data.min_trust_level,
                trusted_sources_only=keyword_data.trusted_sources_only,
                search_engines=keyword_data.search_engines,
                semantic_relations=self._process_semantic_relations(keyword_data.semantic_relations),
                is_active=keyword_data.is_active,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by=self.user_id,
                updated_by=self.user_id,
                condition_id=keyword_data.condition_id
            )

            self.db.add(new_keyword)
            self.db.commit()
            self.db.refresh(new_keyword)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("create_keyword", {
                "keyword_id": new_keyword.id,
                "keyword": new_keyword.keyword,
                "plant_type": new_keyword.plant_type,
                "condition_type": new_keyword.condition_type,
                "plant_part": new_keyword.plant_part
            })

            logger.info("تم إنشاء كلمة مفتاحية جديدة: %s", new_keyword.keyword)

            return self._keyword_to_response(new_keyword)

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء إنشاء كلمة مفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def _process_semantic_relations(self, relations: Optional[List[SemanticRelation]]) -> Optional[List[Dict[str, Any]]]:
        """
        معالجة العلاقات الدلالية

        المعلمات:
            relations (Optional[List[SemanticRelation]]): قائمة العلاقات الدلالية

        العوائد:
            Optional[List[Dict[str, Any]]]: قائمة العلاقات الدلالية بعد المعالجة
        """
        if not relations:
            return None

        processed_relations = []
        for relation in relations:
            # التحقق من وجود الكلمة المفتاحية المرتبطة
            related_keyword = self.db.query(SearchKeyword).filter(
                SearchKeyword.id == relation.related_keyword_id
            ).first()

            if not related_keyword:
                logger.warning(f"الكلمة المفتاحية المرتبطة غير موجودة: {relation.related_keyword_id}")
                continue

            processed_relations.append({
                "related_keyword_id": relation.related_keyword_id,
                "related_keyword": related_keyword.keyword,
                "relation_type": relation.relation_type,
                "confidence": relation.confidence,
                "notes": relation.notes
            })

        return processed_relations

    def update_keyword(self, keyword_id: int, keyword_data: SearchKeywordUpdate) -> SearchKeywordResponse:
        """
        تحديث كلمة مفتاحية موجودة

        المعلمات:
            keyword_id (int): معرف الكلمة المفتاحية
            keyword_data (SearchKeywordUpdate): بيانات التحديث

        العوائد:
            SearchKeywordResponse: نموذج استجابة الكلمة المفتاحية

        يرفع:
            ValueError: إذا كانت الكلمة المفتاحية غير موجودة
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث كلمة مفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "keyword"):
            raise PermissionError(NO_UPDATE_PERMISSION)

        try:
            # البحث عن الكلمة المفتاحية
            keyword = self.db.query(SearchKeyword).filter(SearchKeyword.id == keyword_id).first()

            if not keyword:
                raise ValueError(f"الكلمة المفتاحية غير موجودة: {keyword_id}")

            # تحديث البيانات
            update_data = keyword_data.dict(exclude_unset=True)

            # معالجة العلاقات الدلالية إذا كانت موجودة
            if "semantic_relations" in update_data:
                update_data["semantic_relations"] = self._process_semantic_relations(update_data["semantic_relations"])

            for key, value in update_data.items():
                setattr(keyword, key, value)

            keyword.updated_at = datetime.now()
            keyword.updated_by = self.user_id

            self.db.commit()
            self.db.refresh(keyword)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_keyword", {
                "keyword_id": keyword.id,
                "keyword": keyword.keyword,
                "updated_fields": list(update_data.keys())
            })

            logger.info("تم تحديث الكلمة المفتاحية: %s", keyword.keyword)

            return self._keyword_to_response(keyword)

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء تحديث كلمة مفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def delete_keyword(self, keyword_id: int) -> bool:
        """
        حذف كلمة مفتاحية

        المعلمات:
            keyword_id (int): معرف الكلمة المفتاحية

        العوائد:
            bool: True إذا تم الحذف بنجاح

        يرفع:
            ValueError: إذا كانت الكلمة المفتاحية غير موجودة
            PermissionError: إذا لم يكن المستخدم يملك صلاحية حذف كلمة مفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("delete", "keyword"):
            raise PermissionError("ليس لديك صلاحية حذف كلمة مفتاحية")

        try:
            # البحث عن الكلمة المفتاحية
            keyword = self.db.query(SearchKeyword).filter(SearchKeyword.id == keyword_id).first()

            if not keyword:
                raise ValueError(f"الكلمة المفتاحية غير موجودة: {keyword_id}")

            # حفظ معلومات الكلمة المفتاحية قبل الحذف
            keyword_info = {
                "keyword_id": keyword.id,
                "keyword": keyword.keyword,
                "plant_type": keyword.plant_type,
                "condition_type": keyword.condition_type,
                "plant_part": keyword.plant_part
            }

            # حذف الكلمة المفتاحية
            self.db.delete(keyword)
            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("delete_keyword", keyword_info)

            logger.info("تم حذف الكلمة المفتاحية: %s", keyword_info['keyword'])

            return True

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء حذف كلمة مفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def get_keyword_by_id(self, keyword_id: int) -> Optional[SearchKeywordResponse]:
        """
        الحصول على كلمة مفتاحية بواسطة المعرف

        المعلمات:
            keyword_id (int): معرف الكلمة المفتاحية

        العوائد:
            Optional[SearchKeywordResponse]: نموذج استجابة الكلمة المفتاحية، أو None إذا لم تكن موجودة

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة كلمة مفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "keyword"):
            raise PermissionError(NO_READ_PERMISSION)

        try:
            keyword = self.db.query(SearchKeyword).filter(SearchKeyword.id == keyword_id).first()

            if not keyword:
                return None

            return self._keyword_to_response(keyword)

        except Exception as e:
            logger.error("حدث خطأ أثناء البحث عن كلمة مفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def get_keywords(self,
                     skip: int = 0,
                     limit: int = 100,
                     plant_type: Optional[str] = None,
                     condition_type: Optional[ConditionTypeEnum] = None,
                     plant_part: Optional[PlantPartEnum] = None,
                     category_id: Optional[int] = None,
                     is_active: Optional[bool] = None,
                     search_query: Optional[str] = None,
                     sort_by: str = "priority",
                     sort_order: str = "desc") -> Tuple[List[SearchKeywordResponse], int]:
        """
        الحصول على قائمة الكلمات المفتاحية مع دعم التصفية والترتيب

        المعلمات:
            skip (int): عدد العناصر التي يتم تخطيها
            limit (int): الحد الأقصى لعدد العناصر المسترجعة
            plant_type (Optional[str]): تصفية حسب نوع النبات
            condition_type (Optional[ConditionTypeEnum]): تصفية حسب نوع الإصابة
            plant_part (Optional[PlantPartEnum]): تصفية حسب جزء النبات
            category_id (Optional[int]): تصفية حسب فئة الكلمات المفتاحية
            is_active (Optional[bool]): تصفية حسب حالة النشاط
            search_query (Optional[str]): البحث في الكلمات المفتاحية والوصف
            sort_by (str): حقل الترتيب
            sort_order (str): اتجاه الترتيب (asc, desc)

        العوائد:
            Tuple[List[SearchKeywordResponse], int]: قائمة الكلمات المفتاحية والعدد الإجمالي

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة الكلمات المفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "keyword"):
            raise PermissionError(NO_READ_PERMISSION)

        try:
            # بناء الاستعلام
            query = self.db.query(SearchKeyword)

            # تطبيق التصفية
            if plant_type:
                query = query.filter(SearchKeyword.plant_type == plant_type)

            if condition_type:
                query = query.filter(SearchKeyword.condition_type == condition_type)

            if plant_part:
                query = query.filter(SearchKeyword.plant_part == plant_part)

            if category_id:
                query = query.filter(SearchKeyword.category_id == category_id)

            if is_active is not None:
                query = query.filter(SearchKeyword.is_active == is_active)

            if search_query:
                search_query = f"%{search_query}%"
                query = query.filter(
                    or_(
                        SearchKeyword.keyword.ilike(search_query),
                        SearchKeyword.description.ilike(search_query)
                    )
                )

            # الحصول على العدد الإجمالي
            total_count = query.count()

            # تطبيق الترتيب
            if sort_order.lower() == "asc":
                query = query.order_by(asc(getattr(SearchKeyword, sort_by)))
            else:
                query = query.order_by(desc(getattr(SearchKeyword, sort_by)))

            # تطبيق التقسيم
            keywords = query.offset(skip).limit(limit).all()

            return [self._keyword_to_response(keyword) for keyword in keywords], total_count

        except Exception as e:
            logger.error("حدث خطأ أثناء الحصول على قائمة الكلمات المفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def get_priority_keywords(self, limit: int = 10) -> List[SearchKeywordResponse]:
        """
        الحصول على الكلمات المفتاحية ذات الأولوية العالية

        المعلمات:
            limit (int): الحد الأقصى لعدد العناصر المسترجعة

        العوائد:
            List[SearchKeywordResponse]: قائمة الكلمات المفتاحية ذات الأولوية العالية

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة الكلمات المفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "keyword"):
            raise PermissionError(NO_READ_PERMISSION)

        try:
            # البحث عن الكلمات المفتاحية النشطة وترتيبها حسب الأولوية
            keywords = self.db.query(SearchKeyword).filter(
                SearchKeyword.is_active
            ).order_by(
                desc(SearchKeyword.priority),
                asc(SearchKeyword.last_search_at)
            ).limit(limit).all()

            return [self._keyword_to_response(keyword) for keyword in keywords]

        except Exception as e:
            logger.error("حدث خطأ أثناء الحصول على الكلمات المفتاحية ذات الأولوية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def update_keyword_last_search(self, keyword_id: int) -> bool:
        """
        تحديث آخر وقت بحث للكلمة المفتاحية

        المعلمات:
            keyword_id (int): معرف الكلمة المفتاحية

        العوائد:
            bool: True إذا تم التحديث بنجاح

        يرفع:
            ValueError: إذا كانت الكلمة المفتاحية غير موجودة
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث كلمة مفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "keyword"):
            raise PermissionError(NO_UPDATE_PERMISSION)

        try:
            # البحث عن الكلمة المفتاحية
            keyword = self.db.query(SearchKeyword).filter(SearchKeyword.id == keyword_id).first()

            if not keyword:
                raise ValueError(f"الكلمة المفتاحية غير موجودة: {keyword_id}")

            # تحديث آخر وقت بحث
            keyword.last_search_at = datetime.now()
            keyword.search_count = (keyword.search_count or 0) + 1

            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_keyword_last_search", {
                "keyword_id": keyword.id,
                "keyword": keyword.keyword,
                "search_count": keyword.search_count
            })

            return True

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء تحديث آخر وقت بحث للكلمة المفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def update_keyword_success_rate(self, keyword_id: int, success: bool, results_count: int) -> bool:
        """
        تحديث معدل نجاح الكلمة المفتاحية

        المعلمات:
            keyword_id (int): معرف الكلمة المفتاحية
            success (bool): هل كان البحث ناجحاً
            results_count (int): عدد النتائج

        العوائد:
            bool: True إذا تم التحديث بنجاح

        يرفع:
            ValueError: إذا كانت الكلمة المفتاحية غير موجودة
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث كلمة مفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "keyword"):
            raise PermissionError(NO_UPDATE_PERMISSION)

        try:
            # البحث عن الكلمة المفتاحية
            keyword = self.db.query(SearchKeyword).filter(SearchKeyword.id == keyword_id).first()

            if not keyword:
                raise ValueError(f"الكلمة المفتاحية غير موجودة: {keyword_id}")

            # تحديث معدل النجاح
            keyword.success_count = (keyword.success_count or 0) + (1 if success else 0)
            keyword.total_results = (keyword.total_results or 0) + results_count

            # حساب معدل النجاح
            if keyword.search_count and keyword.search_count > 0:
                keyword.success_rate = (keyword.success_count / keyword.search_count) * 100

            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_keyword_success_rate", {
                "keyword_id": keyword.id,
                "keyword": keyword.keyword,
                "success": success,
                "results_count": results_count,
                "success_rate": keyword.success_rate
            })

            return True

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء تحديث معدل نجاح الكلمة المفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def get_keyword_statistics(self) -> KeywordStatistics:
        """
        الحصول على إحصائيات الكلمات المفتاحية

        العوائد:
            KeywordStatistics: إحصائيات الكلمات المفتاحية

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة الكلمات المفتاحية
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "keyword"):
            raise PermissionError(NO_READ_PERMISSION)

        try:
            # إجمالي عدد الكلمات المفتاحية
            # pylint: disable=not-callable
            total_keywords = self.db.query(func.count(SearchKeyword.id)).scalar() or 0

            # عدد الكلمات المفتاحية النشطة
            # pylint: disable=not-callable
            active_keywords = self.db.query(func.count(SearchKeyword.id)).filter(
                SearchKeyword.is_active
            ).scalar() or 0

            # متوسط معدل النجاح
            avg_success_rate = self.db.query(func.avg(SearchKeyword.success_rate)).scalar() or 0

            # إجمالي عدد عمليات البحث
            # pylint: disable=not-callable
            total_searches = self.db.query(func.sum(SearchKeyword.search_count)).scalar() or 0

            # إجمالي عدد النتائج
            # pylint: disable=not-callable
            total_results = self.db.query(func.sum(SearchKeyword.total_results)).scalar() or 0

            # الكلمات المفتاحية الأكثر نجاحاً
            most_successful = self.db.query(SearchKeyword).filter(
                SearchKeyword.success_rate is not None,
                SearchKeyword.search_count > 0
            ).order_by(
                desc(SearchKeyword.success_rate),
                desc(SearchKeyword.search_count)
            ).limit(5).all()

            most_successful_keywords = [
                {
                    "id": kw.id,
                    "keyword": kw.keyword,
                    "success_rate": kw.success_rate,
                    "search_count": kw.search_count,
                    "total_results": kw.total_results,
                    "plant_type": kw.plant_type,
                    "condition_type": kw.condition_type.value if kw.condition_type else None,
                    "plant_part": kw.plant_part.value if kw.plant_part else None
                }
                for kw in most_successful
            ]

            # الكلمات المفتاحية الأقل نجاحاً
            least_successful = self.db.query(SearchKeyword).filter(
                SearchKeyword.success_rate is not None,
                SearchKeyword.search_count > 3  # تجاهل الكلمات ذات عدد بحث قليل
            ).order_by(
                asc(SearchKeyword.success_rate),
                desc(SearchKeyword.search_count)
            ).limit(5).all()

            least_successful_keywords = [
                {
                    "id": kw.id,
                    "keyword": kw.keyword,
                    "success_rate": kw.success_rate,
                    "search_count": kw.search_count,
                    "total_results": kw.total_results,
                    "plant_type": kw.plant_type,
                    "condition_type": kw.condition_type.value if kw.condition_type else None,
                    "plant_part": kw.plant_part.value if kw.plant_part else None
                }
                for kw in least_successful
            ]

            return KeywordStatistics(
                total_keywords=total_keywords,
                active_keywords=active_keywords,
                avg_success_rate=avg_success_rate,
                total_searches=total_searches,
                total_results=total_results,
                most_successful_keywords=most_successful_keywords,
                least_successful_keywords=least_successful_keywords
            )

        except Exception as e:
            logger.error("حدث خطأ أثناء الحصول على إحصائيات الكلمات المفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    # ===== إدارة فئات الكلمات المفتاحية =====

    def create_category(self, category_data: KeywordCategoryCreate) -> KeywordCategoryResponse:
        """
        إنشاء فئة كلمات مفتاحية جديدة

        المعلمات:
            category_data (KeywordCategoryCreate): بيانات الفئة الجديدة

        العوائد:
            KeywordCategoryResponse: نموذج استجابة فئة الكلمات المفتاحية

        يرفع:
            ValueError: إذا كانت الفئة موجودة مسبقاً
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إنشاء فئة
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "category"):
            raise PermissionError("ليس لديك صلاحية إنشاء فئة كلمات مفتاحية")

        try:
            # التحقق من عدم وجود الفئة مسبقاً
            existing_category = self.db.query(KeywordCategory).filter(
                KeywordCategory.name == category_data.name
            ).first()

            if existing_category:
                raise ValueError(f"فئة الكلمات المفتاحية موجودة مسبقاً: {category_data.name}")

            # إنشاء فئة جديدة
            new_category = KeywordCategory(
                name=category_data.name,
                description=category_data.description,
                color=category_data.color,
                icon=category_data.icon,
                parent_id=category_data.parent_id,
                is_active=category_data.is_active,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            self.db.add(new_category)
            self.db.commit()
            self.db.refresh(new_category)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("create_category", {
                "category_id": new_category.id,
                "category_name": new_category.name
            })

            logger.info("تم إنشاء فئة كلمات مفتاحية جديدة: %s", new_category.name)

            return self._category_to_response(new_category)

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء إنشاء فئة كلمات مفتاحية: %s", str(e))
            logger.error(traceback.format_exc())
            raise
