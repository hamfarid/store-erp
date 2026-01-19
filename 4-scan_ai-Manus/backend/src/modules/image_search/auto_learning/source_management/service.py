# /home/ubuntu/image_search_integration/auto_learning/source_management/service.py

"""
خدمة إدارة المصادر الموثوقة المتقدمة للبحث الذاتي الذكي

هذا الملف يحتوي على تنفيذ خدمة إدارة المصادر الموثوقة المتقدمة،
مع دعم تقييم ديناميكي لمستويات الثقة والتكامل مع الذاكرة المركزية.
"""

import logging
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session

from .models import (
    SourceAnalytics,
    SourceBlacklistEntry,
    SourceCategory,
    SourceRating,
    SourceTypeEnum,
    SourceUsageLog,
    SourceVerification,
    TrustedSource,
)
from .schemas import (
    SourceAnalyticsCreate,
    SourceBlacklistEntryCreate,
    SourceBlacklistEntryResponse,
    SourceBlacklistEntryUpdate,
    SourceCategoryCreate,
    SourceCategoryResponse,
    SourceCategoryUpdate,
    SourceRatingCreate,
    SourceRatingResponse,
    SourceStatistics,
    SourceUsageLogCreate,
    SourceUsageLogResponse,
    SourceVerificationCreate,
    SourceVerificationResponse,
    TrustedSourceCreate,
    TrustedSourceResponse,
    TrustedSourceUpdate,
)

# استيراد خدمة الذاكرة المركزية
try:
    from ....memory_service.client import MemoryServiceClient
    memory_service_available = True
except ImportError:
    memory_service_available = False
    logging.warning(
        "خدمة الذاكرة المركزية غير متوفرة. سيتم تعطيل ميزات التكامل مع الذاكرة.")

# استيراد خدمة الصلاحيات
try:
    from ....permissions.service import PermissionService
    permission_service_available = True
except ImportError:
    permission_service_available = False
    logging.warning(
        "خدمة الصلاحيات غير متوفرة. سيتم تعطيل التحقق من الصلاحيات.")

logger = logging.getLogger(__name__)

# Add constant at the top of the file
NO_READ_SOURCE_PERMISSION = "ليس لديك صلاحية قراءة المصادر الموثوقة"
SOURCE_NOT_FOUND = "المصدر غير موجود"
SOURCE_ALREADY_EXISTS = "المصدر موجود بالفعل"
SOURCE_UPDATED_SUCCESS = "تم تحديث المصدر بنجاح"
SOURCE_DELETED_SUCCESS = "تم حذف المصدر بنجاح"
SOURCE_CATEGORY_NOT_FOUND = "فئة المصدر غير موجودة"
SOURCE_CATEGORY_ALREADY_EXISTS = "فئة المصدر موجودة بالفعل"
SOURCE_CATEGORY_UPDATED_SUCCESS = "تم تحديث فئة المصدر بنجاح"
SOURCE_CATEGORY_DELETED_SUCCESS = "تم حذف فئة المصدر بنجاح"
SOURCE_BLACKLIST_ENTRY_NOT_FOUND = "المصدر غير موجود في القائمة السوداء"
SOURCE_BLACKLIST_ENTRY_ALREADY_EXISTS = "المصدر موجود بالفعل في القائمة السوداء"
SOURCE_BLACKLIST_ENTRY_UPDATED_SUCCESS = "تم تحديث المصدر في القائمة السوداء بنجاح"
SOURCE_BLACKLIST_ENTRY_DELETED_SUCCESS = "تم حذف المصدر من القائمة السوداء بنجاح"
SOURCE_ANALYTICS_NOT_FOUND = "تحليلات المصدر غير موجودة"
SOURCE_ANALYTICS_UPDATED_SUCCESS = "تم تحديث تحليلات المصدر بنجاح"
SOURCE_ANALYTICS_DELETED_SUCCESS = "تم حذف تحليلات المصدر بنجاح"
SOURCE_ANALYTICS_CREATED_SUCCESS = "تم إنشاء تحليلات المصدر بنجاح"


class SourceManagementService:
    """خدمة إدارة المصادر الموثوقة المتقدمة"""

    def __init__(self, db: Session, user_id: Optional[int] = None):
        """
        تهيئة خدمة إدارة المصادر الموثوقة

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
            resource (str): المورد المطلوب (source, category, rating, blacklist, verification)

        العوائد:
            bool: True إذا كان المستخدم يملك الصلاحية، False خلاف ذلك
        """
        if not self.permission_service:
            return True  # إذا كانت خدمة الصلاحيات غير متوفرة، نفترض أن المستخدم يملك الصلاحية

        resource_map = {
            "source": "auto_learning.trusted_source",
            "category": "auto_learning.source_category",
            "rating": "auto_learning.source_rating",
            "blacklist": "auto_learning.source_blacklist",
            "verification": "auto_learning.source_verification"
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
                "module": "source_management",
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "user_id": self.user_id,
                "data": data
            }

            self.memory_service.store_memory("source_management", memory_data)
        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء تسجيل الإجراء في الذاكرة المركزية: {str(e)}")

    def _extract_domain(self, url: str) -> str:
        """
        استخراج النطاق من عنوان URL

        المعلمات:
            url (str): عنوان URL

        العوائد:
            str: النطاق المستخرج
        """
        # إزالة البروتوكول
        domain = url.lower()
        if "://" in domain:
            domain = domain.split("://")[1]

        # إزالة المسار والاستعلام
        if "/" in domain:
            domain = domain.split("/")[0]

        # إزالة المنفذ
        if ":" in domain:
            domain = domain.split(":")[0]

        # إزالة www. إذا كانت موجودة
        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    def _source_to_response(
            self,
            source: TrustedSource) -> TrustedSourceResponse:
        """
        تحويل نموذج المصدر الموثوق إلى نموذج الاستجابة

        المعلمات:
            source (TrustedSource): نموذج المصدر الموثوق

        العوائد:
            TrustedSourceResponse: نموذج استجابة المصدر الموثوق
        """
        category_name = source.category.name if source.category else None

        return TrustedSourceResponse(
            id=source.id,
            name=source.name,
            url=source.url,
            domain=source.domain,
            description=source.description,
            category_id=source.category_id,
            source_type=source.source_type,
            trust_level=source.trust_level,
            is_academic=source.is_academic,
            is_government=source.is_government,
            is_commercial=source.is_commercial,
            metadata=source.metadata,
            contact_info=source.contact_info,
            usage_count=source.usage_count,
            success_count=source.success_count,
            success_rate=source.success_rate,
            last_used_at=source.last_used_at,
            is_active=source.is_active,
            is_verified=source.is_verified,
            verification_date=source.verification_date,
            verification_notes=source.verification_notes,
            created_at=source.created_at,
            updated_at=source.updated_at,
            created_by=source.created_by,
            updated_by=source.updated_by,
            category_name=category_name
        )

    def _category_to_response(
            self,
            category: SourceCategory) -> SourceCategoryResponse:
        """
        تحويل نموذج فئة المصادر إلى نموذج الاستجابة

        المعلمات:
            category (SourceCategory): نموذج فئة المصادر

        العوائد:
            SourceCategoryResponse: نموذج استجابة فئة المصادر
        """
        # حساب عدد المصادر في الفئة
        sources_count = self.db.query(func.count(TrustedSource.id)).filter(
            TrustedSource.category_id == category.id
        ).scalar() or 0

        return SourceCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            color=category.color,
            icon=category.icon,
            parent_id=category.parent_id,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
            sources_count=sources_count,
            created_by=category.created_by,
            updated_by=category.updated_by
        )

    # ===== إدارة المصادر الموثوقة =====

    def create_source(
            self,
            source_data: TrustedSourceCreate) -> TrustedSourceResponse:
        """
        إنشاء مصدر موثوق جديد

        المعلمات:
            source_data (TrustedSourceCreate): بيانات المصدر الموثوق الجديد

        العوائد:
            TrustedSourceResponse: نموذج استجابة المصدر الموثوق

        يرفع:
            ValueError: إذا كان المصدر موجود مسبقاً
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إنشاء مصدر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "source"):
            raise PermissionError("ليس لديك صلاحية إنشاء مصدر موثوق")

        try:
            # استخراج النطاق من عنوان URL
            domain = self._extract_domain(source_data.url)

            # التحقق من عدم وجود المصدر مسبقاً
            existing_source = self.db.query(TrustedSource).filter(
                TrustedSource.domain == domain
            ).first()

            if existing_source:
                raise ValueError(f"المصدر الموثوق موجود مسبقاً: {domain}")

            # إنشاء مصدر موثوق جديد
            new_source = TrustedSource(
                name=source_data.name,
                url=source_data.url,
                domain=domain,
                description=source_data.description,
                category_id=source_data.category_id,
                source_type=source_data.source_type,
                trust_level=source_data.trust_level,
                is_academic=source_data.is_academic,
                is_government=source_data.is_government,
                is_commercial=source_data.is_commercial,
                metadata=source_data.metadata,
                contact_info=source_data.contact_info,
                is_active=source_data.is_active,
                is_verified=source_data.is_verified,
                verification_notes=source_data.verification_notes,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by=self.user_id,
                updated_by=self.user_id
            )

            self.db.add(new_source)
            self.db.commit()
            self.db.refresh(new_source)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("create_source", {
                "source_id": new_source.id,
                "name": new_source.name,
                "domain": new_source.domain,
                "trust_level": new_source.trust_level
            })

            logger.info(
                f"تم إنشاء مصدر موثوق جديد: {new_source.name} ({domain})")

            return self._source_to_response(new_source)

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء إنشاء مصدر موثوق: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def update_source(
            self,
            source_id: int,
            source_data: TrustedSourceUpdate) -> TrustedSourceResponse:
        """
        تحديث مصدر موثوق موجود

        المعلمات:
            source_id (int): معرف المصدر الموثوق
            source_data (TrustedSourceUpdate): بيانات التحديث

        العوائد:
            TrustedSourceResponse: نموذج استجابة المصدر الموثوق

        يرفع:
            ValueError: إذا كان المصدر غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث مصدر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "source"):
            raise PermissionError("ليس لديك صلاحية تحديث مصدر موثوق")

        try:
            # البحث عن المصدر
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == source_id).first()

            if not source:
                raise ValueError(f"المصدر الموثوق غير موجود: {source_id}")

            # تحديث البيانات
            update_data = source_data.dict(exclude_unset=True)

            # إذا تم تحديث عنوان URL، قم بتحديث النطاق أيضاً
            if 'url' in update_data:
                update_data['domain'] = self._extract_domain(
                    update_data['url'])

            for key, value in update_data.items():
                setattr(source, key, value)

            source.updated_at = datetime.now()
            source.updated_by = self.user_id

            self.db.commit()
            self.db.refresh(source)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_source", {
                "source_id": source.id,
                "name": source.name,
                "domain": source.domain,
                "updated_fields": list(update_data.keys())
            })

            logger.info(
                f"تم تحديث المصدر الموثوق: {source.name} ({source.domain})")

            return self._source_to_response(source)

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء تحديث مصدر موثوق: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def delete_source(self, source_id: int) -> bool:
        """
        حذف مصدر موثوق

        المعلمات:
            source_id (int): معرف المصدر الموثوق

        العوائد:
            bool: True إذا تم الحذف بنجاح

        يرفع:
            ValueError: إذا كان المصدر غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية حذف مصدر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("delete", "source"):
            raise PermissionError("ليس لديك صلاحية حذف مصدر موثوق")

        try:
            # البحث عن المصدر
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == source_id).first()

            if not source:
                raise ValueError(f"المصدر الموثوق غير موجود: {source_id}")

            # حفظ معلومات المصدر قبل الحذف
            source_info = {
                "source_id": source.id,
                "name": source.name,
                "domain": source.domain,
                "trust_level": source.trust_level
            }

            # حذف المصدر
            self.db.delete(source)
            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("delete_source", source_info)

            logger.info(
                f"تم حذف المصدر الموثوق: {source_info['name']} ({source_info['domain']})")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء حذف مصدر موثوق: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_source_by_id(
            self,
            source_id: int) -> Optional[TrustedSourceResponse]:
        """
        الحصول على مصدر موثوق بواسطة المعرف

        المعلمات:
            source_id (int): معرف المصدر الموثوق

        العوائد:
            Optional[TrustedSourceResponse]: نموذج استجابة المصدر الموثوق، أو None إذا لم يكن موجوداً

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة مصدر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "source"):
            raise PermissionError("ليس لديك صلاحية قراءة مصدر موثوق")

        try:
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == source_id).first()

            if not source:
                return None

            return self._source_to_response(source)

        except Exception as e:
            logger.error(f"حدث خطأ أثناء البحث عن مصدر موثوق: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_source_by_domain(
            self,
            domain: str) -> Optional[TrustedSourceResponse]:
        """
        الحصول على مصدر موثوق بواسطة النطاق

        المعلمات:
            domain (str): نطاق المصدر

        العوائد:
            Optional[TrustedSourceResponse]: نموذج استجابة المصدر الموثوق، أو None إذا لم يكن موجوداً

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة مصدر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "source"):
            raise PermissionError("ليس لديك صلاحية قراءة مصدر موثوق")

        try:
            # تنظيف النطاق
            clean_domain = self._extract_domain(domain)

            source = self.db.query(TrustedSource).filter(
                TrustedSource.domain == clean_domain).first()

            if not source:
                return None

            return self._source_to_response(source)

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء البحث عن مصدر موثوق بواسطة النطاق: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_sources(self,
                    skip: int = 0,
                    limit: int = 100,
                    category_id: Optional[int] = None,
                    source_type: Optional[SourceTypeEnum] = None,
                    is_active: Optional[bool] = None,
                    is_verified: Optional[bool] = None,
                    min_trust_level: Optional[int] = None,
                    is_academic: Optional[bool] = None,
                    is_government: Optional[bool] = None,
                    is_commercial: Optional[bool] = None,
                    search_query: Optional[str] = None,
                    sort_by: str = "trust_level",
                    sort_order: str = "desc") -> Tuple[List[TrustedSourceResponse],
                                                       int]:
        """
        الحصول على قائمة المصادر الموثوقة مع دعم التصفية والترتيب

        المعلمات:
            skip (int): عدد العناصر التي يتم تخطيها
            limit (int): الحد الأقصى لعدد العناصر المسترجعة
            category_id (Optional[int]): تصفية حسب فئة المصادر
            source_type (Optional[SourceTypeEnum]): تصفية حسب نوع المصدر
            is_active (Optional[bool]): تصفية حسب حالة النشاط
            is_verified (Optional[bool]): تصفية حسب حالة التحقق
            min_trust_level (Optional[int]): تصفية حسب الحد الأدنى لمستوى الثقة
            is_academic (Optional[bool]): تصفية حسب كون المصدر أكاديمي
            is_government (Optional[bool]): تصفية حسب كون المصدر حكومي
            is_commercial (Optional[bool]): تصفية حسب كون المصدر تجاري
            search_query (Optional[str]): البحث في اسم المصدر والوصف والنطاق
            sort_by (str): حقل الترتيب
            sort_order (str): اتجاه الترتيب (asc, desc)

        العوائد:
            Tuple[List[TrustedSourceResponse], int]: قائمة المصادر الموثوقة والعدد الإجمالي

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة المصادر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "source"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)

        try:
            query = self.db.query(TrustedSource)

            # تطبيق التصفية
            if category_id is not None:
                query = query.filter(TrustedSource.category_id == category_id)
            if source_type is not None:
                query = query.filter(TrustedSource.source_type == source_type)
            if is_active is not None:
                query = query.filter(TrustedSource.is_active == is_active)
            if is_verified is not None:
                query = query.filter(TrustedSource.is_verified == is_verified)
            if min_trust_level is not None:
                query = query.filter(
                    TrustedSource.trust_level >= min_trust_level)
            if is_academic is not None:
                query = query.filter(TrustedSource.is_academic == is_academic)
            if is_government is not None:
                query = query.filter(
                    TrustedSource.is_government == is_government)
            if is_commercial is not None:
                query = query.filter(
                    TrustedSource.is_commercial == is_commercial)
            if search_query:
                query = query.filter(
                    or_(
                        TrustedSource.name.ilike(f"%{search_query}%"),
                        TrustedSource.description.ilike(f"%{search_query}%"),
                        TrustedSource.url.ilike(f"%{search_query}%")
                    )
                )

            # الحصول على العدد الإجمالي
            total_count = query.count()

            # تطبيق الترتيب
            if sort_order.lower() == "desc":
                query = query.order_by(desc(getattr(TrustedSource, sort_by)))
            else:
                query = query.order_by(asc(getattr(TrustedSource, sort_by)))

            # تطبيق التقسيم
            sources = query.offset(skip).limit(limit).all()

            return [self._source_to_response(source)
                    for source in sources], total_count

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء الحصول على قائمة المصادر الموثوقة: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_trusted_sources(
            self,
            min_trust_level: int = 50) -> List[TrustedSourceResponse]:
        """
        الحصول على المصادر الموثوقة النشطة

        المعلمات:
            min_trust_level (int): الحد الأدنى لمستوى الثقة

        العوائد:
            List[TrustedSourceResponse]: قائمة المصادر الموثوقة النشطة

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة المصادر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "source"):
            raise PermissionError("ليس لديك صلاحية قراءة المصادر الموثوقة")

        try:
            # البحث عن المصادر الموثوقة النشطة
            sources = self.db.query(TrustedSource).filter(
                TrustedSource.is_active,
                TrustedSource.trust_level >= min_trust_level
            ).order_by(
                desc(TrustedSource.trust_level)
            ).all()

            return [self._source_to_response(source) for source in sources]

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء الحصول على المصادر الموثوقة: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def update_source_trust_level(
            self,
            source_id: int,
            new_rating: int) -> bool:
        """
        تحديث مستوى الثقة للمصدر بناءً على تقييم جديد

        المعلمات:
            source_id (int): معرف المصدر الموثوق
            new_rating (int): التقييم الجديد (0-100)

        العوائد:
            bool: True إذا تم التحديث بنجاح

        يرفع:
            ValueError: إذا كان المصدر غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث مصدر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "source"):
            raise PermissionError("ليس لديك صلاحية تحديث مصدر موثوق")

        try:
            # البحث عن المصدر
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == source_id).first()

            if not source:
                raise ValueError(f"المصدر الموثوق غير موجود: {source_id}")

            # إضافة تقييم جديد
            rating = SourceRating(
                source_id=source_id,
                rating=new_rating,
                user_id=self.user_id,
                created_at=datetime.now()
            )

            self.db.add(rating)

            # حساب متوسط التقييمات
            avg_rating = self.db.query(func.avg(SourceRating.rating)).filter(
                SourceRating.source_id == source_id
            ).scalar() or 0

            # تحديث مستوى الثقة
            source.trust_level = int(avg_rating)
            source.updated_at = datetime.now()
            source.updated_by = self.user_id

            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_source_trust_level", {
                "source_id": source.id,
                "name": source.name,
                "domain": source.domain,
                "new_rating": new_rating,
                "new_trust_level": source.trust_level
            })

            logger.info(
                f"تم تحديث مستوى الثقة للمصدر {source.name}: {source.trust_level}")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء تحديث مستوى الثقة للمصدر: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def add_source_rating(
            self,
            rating_data: SourceRatingCreate) -> SourceRatingResponse:
        """
        إضافة تقييم جديد لمصدر

        المعلمات:
            rating_data (SourceRatingCreate): بيانات التقييم الجديد

        العوائد:
            SourceRatingResponse: نموذج استجابة تقييم المصدر

        يرفع:
            ValueError: إذا كان المصدر غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إضافة تقييم
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "rating"):
            raise PermissionError("ليس لديك صلاحية إضافة تقييم لمصدر")

        try:
            # البحث عن المصدر
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == rating_data.source_id).first()

            if not source:
                raise ValueError(
                    f"المصدر الموثوق غير موجود: {rating_data.source_id}")

            # إضافة تقييم جديد
            rating = SourceRating(
                source_id=rating_data.source_id,
                rating=rating_data.rating,
                comment=rating_data.comment,
                user_id=rating_data.user_id or self.user_id,
                created_at=datetime.now()
            )

            self.db.add(rating)

            # حساب متوسط التقييمات
            avg_rating = self.db.query(func.avg(SourceRating.rating)).filter(
                SourceRating.source_id == rating_data.source_id
            ).scalar() or 0

            # تحديث مستوى الثقة
            source.trust_level = int(avg_rating)
            source.updated_at = datetime.now()
            source.updated_by = self.user_id

            self.db.commit()
            self.db.refresh(rating)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("add_source_rating", {
                "source_id": source.id,
                "name": source.name,
                "domain": source.domain,
                "rating": rating_data.rating,
                "new_trust_level": source.trust_level
            })

            logger.info(
                f"تم إضافة تقييم جديد للمصدر {source.name}: {rating_data.rating}")

            return SourceRatingResponse(
                id=rating.id,
                source_id=rating.source_id,
                rating=rating.rating,
                comment=rating.comment,
                user_id=rating.user_id,
                created_at=rating.created_at
            )

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء إضافة تقييم للمصدر: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_source_statistics(self) -> SourceStatistics:
        """
        الحصول على إحصائيات المصادر الموثوقة

        العوائد:
            SourceStatistics: إحصائيات المصادر الموثوقة

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة المصادر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "source"):
            raise PermissionError("ليس لديك صلاحية قراءة المصادر الموثوقة")

        try:
            # إجمالي عدد المصادر
            total_sources = self.db.query(
                func.count(TrustedSource.id)).scalar() or 0

            # عدد المصادر النشطة
            active_sources = self.db.query(
                func.count(
                    TrustedSource.id)).filter(
                TrustedSource.is_active).scalar() or 0

            # متوسط مستوى الثقة
            avg_trust_level = self.db.query(
                func.avg(TrustedSource.trust_level)).scalar() or 0

            # عدد المصادر الأكاديمية
            academic_sources = self.db.query(
                func.count(
                    TrustedSource.id)).filter(
                TrustedSource.is_academic).scalar() or 0

            # عدد المصادر الحكومية
            government_sources = self.db.query(
                func.count(
                    TrustedSource.id)).filter(
                TrustedSource.is_government).scalar() or 0

            # عدد المصادر التجارية
            commercial_sources = self.db.query(
                func.count(
                    TrustedSource.id)).filter(
                TrustedSource.is_commercial).scalar() or 0

            # عدد المصادر في القائمة السوداء
            blacklisted_sources = self.db.query(
                func.count(
                    TrustedSource.id)).join(
                SourceBlacklistEntry,
                TrustedSource.id == SourceBlacklistEntry.source_id).filter(
                SourceBlacklistEntry.is_active).scalar() or 0

            # عدد المصادر المتحقق منها
            verified_sources = self.db.query(
                func.count(
                    TrustedSource.id)).filter(
                TrustedSource.is_verified).scalar() or 0

            # المصادر الأكثر ثقة
            most_trusted = self.db.query(TrustedSource).order_by(
                desc(TrustedSource.trust_level)
            ).limit(5).all()

            most_trusted_sources = [
                {
                    "id": src.id,
                    "name": src.name,
                    "domain": src.domain,
                    "trust_level": src.trust_level,
                    "source_type": src.source_type.value if src.source_type else None
                }
                for src in most_trusted
            ]

            # المصادر حسب النوع
            sources_by_type = {}
            for source_type in SourceTypeEnum:
                count = self.db.query(func.count(TrustedSource.id)).filter(
                    TrustedSource.source_type == source_type
                ).scalar() or 0
                sources_by_type[source_type.value] = count

            return SourceStatistics(
                total_sources=total_sources,
                active_sources=active_sources,
                avg_trust_level=avg_trust_level,
                academic_sources=academic_sources,
                government_sources=government_sources,
                commercial_sources=commercial_sources,
                blacklisted_sources=blacklisted_sources,
                verified_sources=verified_sources,
                most_trusted_sources=most_trusted_sources,
                sources_by_type=sources_by_type
            )

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء الحصول على إحصائيات المصادر الموثوقة: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # ===== إدارة فئات المصادر =====

    def create_category(
            self,
            category_data: SourceCategoryCreate) -> SourceCategoryResponse:
        """
        إنشاء فئة مصادر جديدة

        المعلمات:
            category_data (SourceCategoryCreate): بيانات الفئة الجديدة

        العوائد:
            SourceCategoryResponse: نموذج استجابة فئة المصادر

        يرفع:
            ValueError: إذا كانت الفئة موجودة مسبقاً
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إنشاء فئة
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "category"):
            raise PermissionError("ليس لديك صلاحية إنشاء فئة مصادر")

        try:
            # التحقق من عدم وجود الفئة مسبقاً
            existing_category = self.db.query(SourceCategory).filter(
                SourceCategory.name == category_data.name
            ).first()

            if existing_category:
                raise ValueError(
                    f"فئة المصادر موجودة مسبقاً: {category_data.name}")

            # إنشاء فئة جديدة
            new_category = SourceCategory(
                name=category_data.name,
                description=category_data.description,
                color=category_data.color,
                icon=category_data.icon,
                parent_id=category_data.parent_id,
                is_active=category_data.is_active,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by=self.user_id,
                updated_by=self.user_id
            )

            self.db.add(new_category)
            self.db.commit()
            self.db.refresh(new_category)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("create_category", {
                "category_id": new_category.id,
                "name": new_category.name
            })

            logger.info(f"تم إنشاء فئة مصادر جديدة: {new_category.name}")

            return self._category_to_response(new_category)

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء إنشاء فئة مصادر: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def delete_source_category(self, category_id: int) -> bool:
        """
        حذف فئة مصادر

        المعلمات:
            category_id (int): معرف الفئة المصادر

        العوائد:
            bool: True إذا تم الحذف بنجاح

        يرفع:
            ValueError: إذا كانت الفئة غير موجودة
            PermissionError: إذا لم يكن المستخدم يملك صلاحية حذف فئة مصادر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("delete", "category"):
            raise PermissionError("ليس لديك صلاحية حذف فئة مصادر")

        try:
            # البحث عن الفئة
            category = self.db.query(SourceCategory).filter(
                SourceCategory.id == category_id).first()

            if not category:
                raise ValueError(f"فئة المصادر غير موجودة: {category_id}")

            # حذف الفئة
            self.db.delete(category)
            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("delete_category", {
                "category_id": category.id,
                "name": category.name
            })

            logger.info(f"تم حذف الفئة المصادر: {category.name}")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء حذف الفئة المصادر: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # ===== إدارة القائمة السوداء =====

    def add_to_blacklist(
            self,
            blacklist_data: SourceBlacklistEntryCreate) -> SourceBlacklistEntryResponse:
        """
        إضافة مصدر إلى القائمة السوداء

        المعلمات:
            blacklist_data (SourceBlacklistEntryCreate): بيانات إدخال القائمة السوداء

        العوائد:
            SourceBlacklistEntryResponse: نموذج استجابة إدخال القائمة السوداء

        يرفع:
            ValueError: إذا كان المصدر غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إدارة القائمة السوداء
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "blacklist"):
            raise PermissionError("ليس لديك صلاحية إدارة القائمة السوداء")

        try:
            # البحث عن المصدر
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == blacklist_data.source_id).first()

            if not source:
                raise ValueError(
                    f"المصدر الموثوق غير موجود: {blacklist_data.source_id}")

            # التحقق من عدم وجود إدخال نشط في القائمة السوداء
            existing_entry = self.db.query(SourceBlacklistEntry).filter(
                SourceBlacklistEntry.source_id == blacklist_data.source_id,
                SourceBlacklistEntry.is_active
            ).first()

            if existing_entry:
                raise ValueError(
                    f"المصدر موجود بالفعل في القائمة السوداء: {source.name}")

            # إضافة إدخال جديد
            new_entry = SourceBlacklistEntry(
                source_id=blacklist_data.source_id,
                reason=blacklist_data.reason,
                start_date=blacklist_data.start_date,
                end_date=blacklist_data.end_date,
                is_active=blacklist_data.is_active,
                created_by=self.user_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            self.db.add(new_entry)

            # تعطيل المصدر
            source.is_active = False
            source.updated_at = datetime.now()
            source.updated_by = self.user_id

            self.db.commit()
            self.db.refresh(new_entry)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("add_to_blacklist", {
                "source_id": source.id,
                "name": source.name,
                "domain": source.domain,
                "reason": blacklist_data.reason
            })

            logger.info(f"تم إضافة المصدر {source.name} إلى القائمة السوداء")

            return SourceBlacklistEntryResponse(
                id=new_entry.id,
                source_id=new_entry.source_id,
                reason=new_entry.reason,
                start_date=new_entry.start_date,
                end_date=new_entry.end_date,
                is_active=new_entry.is_active,
                created_by=new_entry.created_by,
                created_at=new_entry.created_at,
                updated_at=new_entry.updated_at,
                source_name=source.name,
                source_domain=source.domain
            )

        except Exception as e:
            self.db.rollback()
            logger.error(
                f"حدث خطأ أثناء إضافة مصدر إلى القائمة السوداء: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # ===== إدارة التحقق من المصادر =====

    def verify_source(
            self,
            verification_data: SourceVerificationCreate) -> SourceVerificationResponse:
        """
        التحقق من مصدر

        المعلمات:
            verification_data (SourceVerificationCreate): بيانات التحقق

        العوائد:
            SourceVerificationResponse: نموذج استجابة التحقق من المصدر

        يرفع:
            ValueError: إذا كان المصدر غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية التحقق من المصادر
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "verification"):
            raise PermissionError("ليس لديك صلاحية التحقق من المصادر")

        try:
            # البحث عن المصدر
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == verification_data.source_id).first()

            if not source:
                raise ValueError(
                    f"المصدر الموثوق غير موجود: {verification_data.source_id}")

            # إضافة سجل تحقق جديد
            verification = SourceVerification(
                source_id=verification_data.source_id,
                is_verified=verification_data.is_verified,
                verification_method=verification_data.verification_method,
                verification_notes=verification_data.verification_notes,
                verified_by=verification_data.verified_by or self.user_id,
                verification_date=datetime.now(),
                created_at=datetime.now()
            )

            self.db.add(verification)

            # تحديث حالة التحقق للمصدر
            source.is_verified = verification_data.is_verified
            source.verification_date = datetime.now()
            source.verification_notes = verification_data.verification_notes
            source.updated_at = datetime.now()
            source.updated_by = self.user_id

            self.db.commit()
            self.db.refresh(verification)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("verify_source", {
                "source_id": source.id,
                "name": source.name,
                "domain": source.domain,
                "is_verified": verification_data.is_verified,
                "verification_method": verification_data.verification_method
            })

            logger.info(
                f"تم التحقق من المصدر {source.name}: {verification_data.is_verified}")

            return SourceVerificationResponse(
                id=verification.id,
                source_id=verification.source_id,
                is_verified=verification.is_verified,
                verification_method=verification.verification_method,
                verification_notes=verification.verification_notes,
                verified_by=verification.verified_by,
                verification_date=verification.verification_date,
                created_at=verification.created_at,
                source_name=source.name,
                source_domain=source.domain
            )

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء التحقق من مصدر: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # ===== تسجيل استخدام المصادر =====

    def log_source_usage(
            self,
            usage_data: SourceUsageLogCreate) -> SourceUsageLogResponse:
        """
        تسجيل استخدام مصدر

        المعلمات:
            usage_data (SourceUsageLogCreate): بيانات الاستخدام

        العوائد:
            SourceUsageLogResponse: نموذج استجابة سجل استخدام المصدر

        يرفع:
            ValueError: إذا كان المصدر غير موجود
        """
        try:
            # البحث عن المصدر
            source = self.db.query(TrustedSource).filter(
                TrustedSource.id == usage_data.source_id).first()

            if not source:
                raise ValueError(
                    f"المصدر الموثوق غير موجود: {usage_data.source_id}")

            # إضافة سجل استخدام جديد
            usage_log = SourceUsageLog(
                source_id=usage_data.source_id,
                usage_date=datetime.now(),
                usage_type=usage_data.usage_type,
                keyword_id=usage_data.keyword_id,
                search_engine_id=usage_data.search_engine_id,
                results_count=usage_data.results_count,
                success=usage_data.success,
                notes=usage_data.notes,
                created_at=datetime.now()
            )

            self.db.add(usage_log)

            # تحديث إحصائيات المصدر
            source.usage_count = (source.usage_count or 0) + 1
            source.success_count = (
                source.success_count or 0) + (1 if usage_data.success else 0)

            # حساب معدل النجاح
            if source.usage_count > 0:
                source.success_rate = (
                    source.success_count / source.usage_count) * 100

            source.last_used_at = datetime.now()
            source.updated_at = datetime.now()

            self.db.commit()
            self.db.refresh(usage_log)

            logger.info(
                f"تم تسجيل استخدام المصدر {source.name}: {usage_data.usage_type}")

            return SourceUsageLogResponse(
                id=usage_log.id,
                source_id=usage_log.source_id,
                usage_date=usage_log.usage_date,
                usage_type=usage_log.usage_type,
                keyword_id=usage_log.keyword_id,
                search_engine_id=usage_log.search_engine_id,
                results_count=usage_log.results_count,
                success=usage_log.success,
                notes=usage_log.notes,
                created_at=usage_log.created_at,
                source_name=source.name,
                source_domain=source.domain
            )

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء تسجيل استخدام مصدر: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_source(self, source_id: int) -> TrustedSource:
        if not self._check_permission("read", "source"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        source = self.db.query(TrustedSource).filter(
            TrustedSource.id == source_id).first()
        if not source:
            raise ValueError(SOURCE_NOT_FOUND)
        return source

    def get_source_category(self, category_id: int) -> SourceCategory:
        if not self._check_permission("read", "source"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        category = self.db.query(SourceCategory).filter(
            SourceCategory.id == category_id).first()
        if not category:
            raise ValueError(SOURCE_CATEGORY_NOT_FOUND)
        return category

    def update_source_category(
            self,
            category_id: int,
            category: SourceCategoryUpdate) -> SourceCategory:
        if not self._check_permission("update", "source"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        db_category = self.db.query(SourceCategory).filter(
            SourceCategory.id == category_id).first()
        if not db_category:
            raise ValueError(SOURCE_CATEGORY_NOT_FOUND)
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def get_source_blacklist_entry(
            self, entry_id: int) -> SourceBlacklistEntry:
        if not self._check_permission("read", "blacklist"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        entry = self.db.query(SourceBlacklistEntry).filter(
            SourceBlacklistEntry.id == entry_id).first()
        if not entry:
            raise ValueError(SOURCE_BLACKLIST_ENTRY_NOT_FOUND)
        return entry

    def create_source_blacklist_entry(
            self, entry: SourceBlacklistEntryCreate) -> SourceBlacklistEntry:
        if not self._check_permission("create", "blacklist"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        existing_entry = self.db.query(SourceBlacklistEntry).filter(
            SourceBlacklistEntry.url == entry.url).first()
        if existing_entry:
            raise ValueError(SOURCE_BLACKLIST_ENTRY_ALREADY_EXISTS)
        db_entry = SourceBlacklistEntry(**entry.dict())
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        return db_entry

    def update_source_blacklist_entry(
            self,
            entry_id: int,
            entry: SourceBlacklistEntryUpdate,
            user_id: int) -> SourceBlacklistEntry:
        if not self._check_permission("update", "blacklist"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        db_entry = self.db.query(SourceBlacklistEntry).filter(
            SourceBlacklistEntry.id == entry_id).first()
        if not db_entry:
            raise ValueError(SOURCE_BLACKLIST_ENTRY_NOT_FOUND)
        for key, value in entry.dict(exclude_unset=True).items():
            setattr(db_entry, key, value)
        self.db.commit()
        self.db.refresh(db_entry)
        return db_entry

    def delete_source_analytics(self, source_id: int, user_id: int) -> bool:
        if not self._check_permission("delete", "source"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        db_analytics = self.db.query(SourceAnalytics).filter(
            SourceAnalytics.source_id == source_id).first()
        if not db_analytics:
            raise ValueError(SOURCE_ANALYTICS_NOT_FOUND)
        self.db.delete(db_analytics)
        self.db.commit()
        return True

    def create_source_analytics(
            self, analytics: SourceAnalyticsCreate) -> SourceAnalytics:
        if not self._check_permission("create", "source"):
            raise PermissionError(NO_READ_SOURCE_PERMISSION)
        db_analytics = SourceAnalytics(**analytics.dict())
        self.db.add(db_analytics)
        self.db.commit()
        self.db.refresh(db_analytics)
        return db_analytics
