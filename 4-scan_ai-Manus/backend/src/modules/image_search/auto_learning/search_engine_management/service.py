# /home/ubuntu/image_search_integration/auto_learning/search_engine_management/service.py
# pylint: disable=too-many-lines

"""
خدمة إدارة محركات البحث المتقدمة للبحث الذاتي الذكي

هذا الملف يحتوي على تنفيذ خدمة إدارة محركات البحث المتقدمة،
مع دعم توزيع الحمل والتوازن ومراقبة الأداء والتكامل مع الذاكرة المركزية.
"""

import logging
import random
import traceback
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session

from modules.image_search.auto_learning.search_engine_management.models import (
    ResponseFormatEnum,
    SearchEngine,
    SearchEngineLoadBalancer,
    SearchEngineLoadBalancerMapping,
    SearchEngineMaintenanceLog,
    SearchEngineParameter,
    SearchEngineUsageLog,
)
from modules.image_search.auto_learning.search_engine_management.schemas import (
    LoadBalancerStrategyEnum,
    SearchEngineCreate,
    SearchEngineLoadBalancerCreate,
    SearchEngineLoadBalancerMappingResponse,
    SearchEngineLoadBalancerResponse,
    SearchEngineParameterCreate,
    SearchEngineParameterResponse,
    SearchEngineParameterUpdate,
    SearchEngineResponse,
    SearchEngineStatistics,
    SearchEngineUpdate,
    SearchEngineUsageLogCreate,
    SearchEngineUsageLogResponse,
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

# Constants for permission error messages
PERMISSION_ERROR_UPDATE_ENGINE = "ليس لديك صلاحية تحديث محرك بحث"
PERMISSION_ERROR_READ_ENGINES = "ليس لديك صلاحية قراءة محركات البحث"


class SearchEngineManagementService:
    """خدمة إدارة محركات البحث المتقدمة"""

    def __init__(self, db: Session, user_id: Optional[int] = None):
        """
        تهيئة خدمة إدارة محركات البحث

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
            resource (str): المورد المطلوب (engine, parameter, log, balancer, mapping)

        العوائد:
            bool: True إذا كان المستخدم يملك الصلاحية، False خلاف ذلك
        """
        if not self.permission_service:
            return True  # إذا كانت خدمة الصلاحيات غير متوفرة، نفترض أن المستخدم يملك الصلاحية

        resource_map = {
            "engine": "auto_learning.search_engine",
            "parameter": "auto_learning.search_engine_parameter",
            "log": "auto_learning.search_engine_log",
            "balancer": "auto_learning.search_engine_balancer",
            "mapping": "auto_learning.search_engine_balancer_mapping"
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
                "module": "search_engine_management",
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "user_id": self.user_id,
                "data": data
            }

            self.memory_service.store_memory(
                "search_engine_management", memory_data)
        except Exception as e:
            logger.error(
                "حدث خطأ أثناء تسجيل الإجراء في الذاكرة المركزية: %s",
                str(e))

    def _parameter_to_response(
            self,
            param: SearchEngineParameter) -> SearchEngineParameterResponse:
        """
        تحويل نموذج معلمة محرك البحث إلى نموذج الاستجابة

        المعلمات:
            param (SearchEngineParameter): نموذج معلمة محرك البحث

        العوائد:
            SearchEngineParameterResponse: نموذج استجابة معلمة محرك البحث
        """
        return SearchEngineParameterResponse(
            id=param.id,
            engine_id=param.engine_id,
            name=param.name,
            display_name=param.display_name,
            description=param.description,
            param_type=param.param_type,
            required=param.required,
            default_value=param.default_value,
            validation_regex=param.validation_regex,
            options=param.options,
            created_at=param.created_at,
            updated_at=param.updated_at
        )

    def _engine_to_response(
            self,
            engine: SearchEngine) -> SearchEngineResponse:
        """
        تحويل نموذج محرك البحث إلى نموذج الاستجابة

        المعلمات:
            engine (SearchEngine): نموذج محرك البحث

        العوائد:
            SearchEngineResponse: نموذج استجابة محرك البحث
        """
        parameters = [self._parameter_to_response(
            param) for param in engine.parameters]

        return SearchEngineResponse(
            id=engine.id,
            name=engine.name,
            display_name=engine.display_name,
            description=engine.description,
            base_url=engine.base_url,
            api_key_required=engine.api_key_required,
            api_key=engine.api_key,  # قد نحتاج إلى إخفاء المفتاح في الاستجابة
            request_method=engine.request_method,
            request_headers=engine.request_headers,
            response_format=engine.response_format,
            image_path=engine.image_path,
            source_path=engine.source_path,
            title_path=engine.title_path,
            description_path=engine.description_path,
            max_results_per_query=engine.max_results_per_query,
            rate_limit=engine.rate_limit,
            timeout=engine.timeout,
            retry_count=engine.retry_count,
            retry_delay=engine.retry_delay,
            weight=engine.weight,
            max_daily_requests=engine.max_daily_requests,
            current_daily_requests=engine.current_daily_requests,
            last_reset_date=engine.last_reset_date,
            total_requests=engine.total_requests,
            successful_requests=engine.successful_requests,
            failed_requests=engine.failed_requests,
            total_results=engine.total_results,
            avg_response_time=engine.avg_response_time,
            last_request_time=engine.last_request_time,
            last_success_time=engine.last_success_time,
            last_failure_time=engine.last_failure_time,
            last_error_message=engine.last_error_message,
            is_active=engine.is_active,
            created_at=engine.created_at,
            updated_at=engine.updated_at,
            created_by=engine.created_by,
            updated_by=engine.updated_by,
            parameters=parameters
        )

    # ===== إدارة محركات البحث =====

    def create_engine(
            self,
            engine_data: SearchEngineCreate) -> SearchEngineResponse:
        """
        إنشاء محرك بحث جديد

        المعلمات:
            engine_data (SearchEngineCreate): بيانات محرك البحث الجديد

        العوائد:
            SearchEngineResponse: نموذج استجابة محرك البحث

        يرفع:
            ValueError: إذا كان محرك البحث موجود مسبقاً
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إنشاء محرك بحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "engine"):
            raise PermissionError("ليس لديك صلاحية إنشاء محرك بحث")

        try:
            # التحقق من عدم وجود محرك البحث مسبقاً
            existing_engine = self.db.query(SearchEngine).filter(
                SearchEngine.name == engine_data.name
            ).first()

            if existing_engine:
                raise ValueError(
                    f"محرك البحث موجود مسبقاً: {engine_data.name}")

            # إنشاء محرك بحث جديد
            new_engine = SearchEngine(
                name=engine_data.name,
                display_name=engine_data.display_name,
                description=engine_data.description,
                base_url=engine_data.base_url,
                api_key_required=engine_data.api_key_required,
                api_key=engine_data.api_key,
                request_method=engine_data.request_method,
                request_headers=engine_data.request_headers,
                response_format=engine_data.response_format,
                image_path=engine_data.image_path,
                source_path=engine_data.source_path,
                title_path=engine_data.title_path,
                description_path=engine_data.description_path,
                max_results_per_query=engine_data.max_results_per_query,
                rate_limit=engine_data.rate_limit,
                timeout=engine_data.timeout,
                retry_count=engine_data.retry_count,
                retry_delay=engine_data.retry_delay,
                weight=engine_data.weight,
                max_daily_requests=engine_data.max_daily_requests,
                is_active=engine_data.is_active,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by=self.user_id,
                updated_by=self.user_id
            )

            self.db.add(new_engine)
            self.db.commit()
            self.db.refresh(new_engine)

            # إضافة معلمات محرك البحث
            if engine_data.parameters:
                for param_data in engine_data.parameters:
                    param = SearchEngineParameter(
                        engine_id=new_engine.id,
                        name=param_data.name,
                        display_name=param_data.display_name,
                        description=param_data.description,
                        param_type=param_data.param_type,
                        required=param_data.required,
                        default_value=param_data.default_value,
                        validation_regex=param_data.validation_regex,
                        options=param_data.options,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    self.db.add(param)

                self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("create_engine", {
                "engine_id": new_engine.id,
                "name": new_engine.name,
                "display_name": new_engine.display_name
            })

            logger.info("تم إنشاء محرك بحث جديد: %s", new_engine.name)

            return self._engine_to_response(new_engine)

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء إنشاء محرك بحث: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def update_engine(
            self,
            engine_id: int,
            engine_data: SearchEngineUpdate) -> SearchEngineResponse:
        """
        تحديث محرك بحث موجود

        المعلمات:
            engine_id (int): معرف محرك البحث
            engine_data (SearchEngineUpdate): بيانات التحديث

        العوائد:
            SearchEngineResponse: نموذج استجابة محرك البحث

        يرفع:
            ValueError: إذا كان محرك البحث غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث محرك بحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "engine"):
            raise PermissionError("ليس لديك صلاحية تحديث محرك بحث")

        try:
            # البحث عن محرك البحث
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.id == engine_id).first()

            if not engine:
                raise ValueError(f"محرك البحث غير موجود: {engine_id}")

            # تحديث البيانات
            update_data = engine_data.dict(
                exclude_unset=True, exclude={"parameters"})
            for key, value in update_data.items():
                setattr(engine, key, value)

            engine.updated_at = datetime.now()
            engine.updated_by = self.user_id

            self.db.commit()
            self.db.refresh(engine)

            # تحديث معلمات محرك البحث إذا تم توفيرها
            if engine_data.parameters:
                # حذف المعلمات الحالية
                self.db.query(SearchEngineParameter).filter(
                    SearchEngineParameter.engine_id == engine_id
                ).delete()

                # إضافة المعلمات الجديدة
                for param_data in engine_data.parameters:
                    param = SearchEngineParameter(
                        engine_id=engine.id,
                        name=param_data.name,
                        display_name=param_data.display_name,
                        description=param_data.description,
                        param_type=param_data.param_type,
                        required=param_data.required,
                        default_value=param_data.default_value,
                        validation_regex=param_data.validation_regex,
                        options=param_data.options,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    self.db.add(param)

                self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_engine", {
                "engine_id": engine.id,
                "name": engine.name,
                "updated_fields": list(update_data.keys())
            })

            logger.info("تم تحديث محرك البحث: %s", engine.name)

            return self._engine_to_response(engine)

        except Exception as e:
            self.db.rollback()
            logger.error("حدث خطأ أثناء تحديث محرك بحث: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def delete_engine(self, engine_id: int) -> bool:
        """
        حذف محرك بحث

        المعلمات:
            engine_id (int): معرف محرك البحث

        العوائد:
            bool: True إذا تم الحذف بنجاح

        يرفع:
            ValueError: إذا كان محرك البحث غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية حذف محرك بحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("delete", "engine"):
            raise PermissionError("ليس لديك صلاحية حذف محرك بحث")

        try:
            # البحث عن محرك البحث
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.id == engine_id).first()

            if not engine:
                raise ValueError(f"محرك البحث غير موجود: {engine_id}")

            # حفظ معلومات محرك البحث قبل الحذف
            engine_info = {
                "engine_id": engine.id,
                "name": engine.name,
                "display_name": engine.display_name
            }

            # حذف معلمات محرك البحث
            self.db.query(SearchEngineParameter).filter(
                SearchEngineParameter.engine_id == engine_id
            ).delete()

            # حذف سجلات الاستخدام
            self.db.query(SearchEngineUsageLog).filter(
                SearchEngineUsageLog.engine_id == engine_id
            ).delete()

            # حذف سجلات الصيانة
            self.db.query(SearchEngineMaintenanceLog).filter(
                SearchEngineMaintenanceLog.engine_id == engine_id
            ).delete()

            # حذف روابط موازن الحمل
            self.db.query(SearchEngineLoadBalancerMapping).filter(
                SearchEngineLoadBalancerMapping.engine_id == engine_id
            ).delete()

            # حذف محرك البحث
            self.db.delete(engine)
            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("delete_engine", engine_info)

            logger.info(f"تم حذف محرك البحث: {engine_info['name']}")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء حذف محرك بحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_engine_by_id(
            self,
            engine_id: int) -> Optional[SearchEngineResponse]:
        """
        الحصول على محرك بحث بواسطة المعرف

        المعلمات:
            engine_id (int): معرف محرك البحث

        العوائد:
            Optional[SearchEngineResponse]: نموذج استجابة محرك البحث، أو None إذا لم يكن موجوداً

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة محرك بحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "engine"):
            raise PermissionError("ليس لديك صلاحية قراءة محرك بحث")

        try:
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.id == engine_id).first()

            if not engine:
                return None

            return self._engine_to_response(engine)

        except Exception as e:
            logger.error(f"حدث خطأ أثناء البحث عن محرك بحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_engine_by_name(self, name: str) -> Optional[SearchEngineResponse]:
        """
        الحصول على محرك بحث بواسطة الاسم

        المعلمات:
            name (str): اسم محرك البحث

        العوائد:
            Optional[SearchEngineResponse]: نموذج استجابة محرك البحث، أو None إذا لم يكن موجوداً

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة محرك بحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "engine"):
            raise PermissionError("ليس لديك صلاحية قراءة محرك بحث")

        try:
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.name == name).first()

            if not engine:
                return None

            return self._engine_to_response(engine)

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء البحث عن محرك بحث بواسطة الاسم: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_engines(self,
                    skip: int = 0,
                    limit: int = 100,
                    is_active: Optional[bool] = None,
                    api_key_required: Optional[bool] = None,
                    search_query: Optional[str] = None,
                    sort_by: str = "name",
                    sort_order: str = "asc") -> Tuple[List[SearchEngineResponse],
                                                      int]:
        """
        الحصول على قائمة محركات البحث مع دعم التصفية والترتيب

        المعلمات:
            skip (int): عدد العناصر التي يتم تخطيها
            limit (int): الحد الأقصى لعدد العناصر المسترجعة
            is_active (Optional[bool]): تصفية حسب حالة النشاط
            api_key_required (Optional[bool]): تصفية حسب الحاجة لمفتاح API
            search_query (Optional[str]): البحث في اسم محرك البحث والاسم المعروض والوصف
            sort_by (str): حقل الترتيب
            sort_order (str): اتجاه الترتيب (asc, desc)

        العوائد:
            Tuple[List[SearchEngineResponse], int]: قائمة محركات البحث والعدد الإجمالي

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة محركات البحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "engine"):
            raise PermissionError("ليس لديك صلاحية قراءة محركات البحث")

        try:
            # بناء الاستعلام
            query = self.db.query(SearchEngine)

            # تطبيق التصفية
            if is_active is not None:
                query = query.filter(SearchEngine.is_active == is_active)

            if api_key_required is not None:
                query = query.filter(
                    SearchEngine.api_key_required == api_key_required)

            if search_query:
                search_query = f"%{search_query}%"
                query = query.filter(
                    or_(
                        SearchEngine.name.ilike(search_query),
                        SearchEngine.display_name.ilike(search_query),
                        SearchEngine.description.ilike(search_query)
                    )
                )

            # الحصول على العدد الإجمالي
            total_count = query.count()

            # تطبيق الترتيب
            if sort_order.lower() == "desc":
                query = query.order_by(desc(getattr(SearchEngine, sort_by)))
            else:
                query = query.order_by(asc(getattr(SearchEngine, sort_by)))

            # تطبيق التقسيم
            engines = query.offset(skip).limit(limit).all()

            return [self._engine_to_response(engine)
                    for engine in engines], total_count

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء الحصول على قائمة محركات البحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_active_search_engines(self) -> List[SearchEngineResponse]:
        """
        الحصول على محركات البحث النشطة

        العوائد:
            List[SearchEngineResponse]: قائمة محركات البحث النشطة

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة محركات البحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "engine"):
            raise PermissionError("ليس لديك صلاحية قراءة محركات البحث")

        try:
            # البحث عن محركات البحث النشطة
            engines = self.db.query(SearchEngine).filter(
                SearchEngine.is_active
            ).order_by(
                asc(SearchEngine.name)
            ).all()

            return [self._engine_to_response(engine) for engine in engines]

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء الحصول على محركات البحث النشطة: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def update_engine_status(self, engine_id: int, is_active: bool) -> bool:
        """
        تحديث حالة محرك البحث (نشط/غير نشط)

        المعلمات:
            engine_id (int): معرف محرك البحث
            is_active (bool): الحالة الجديدة

        العوائد:
            bool: True إذا تم التحديث بنجاح

        يرفع:
            ValueError: إذا كان محرك البحث غير موجود
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث محرك بحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "engine"):
            raise PermissionError("ليس لديك صلاحية تحديث محرك بحث")

        try:
            # البحث عن محرك البحث
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.id == engine_id).first()

            if not engine:
                raise ValueError(f"محرك البحث غير موجود: {engine_id}")

            # تحديث الحالة
            engine.is_active = is_active
            engine.updated_at = datetime.now()
            engine.updated_by = self.user_id

            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_engine_status", {
                "engine_id": engine.id,
                "name": engine.name,
                "is_active": is_active
            })

            status_text = "نشط" if is_active else "غير نشط"
            logger.info(
                f"تم تحديث حالة محرك البحث {engine.name}: {status_text}")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء تحديث حالة محرك البحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def update_engine_api_key(self, engine_id: int, api_key: str) -> bool:
        """
        تحديث مفتاح API لمحرك البحث

        المعلمات:
            engine_id (int): معرف محرك البحث
            api_key (str): مفتاح API الجديد

        العوائد:
            bool: True إذا تم التحديث بنجاح

        يرفع:
            ValueError: إذا كان محرك البحث غير موجود أو لا يتطلب مفتاح API
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث محرك بحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "engine"):
            raise PermissionError("ليس لديك صلاحية تحديث محرك بحث")

        try:
            # البحث عن محرك البحث
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.id == engine_id).first()

            if not engine:
                raise ValueError(f"محرك البحث غير موجود: {engine_id}")

            # التحقق من أن محرك البحث يتطلب مفتاح API
            if not engine.api_key_required:
                raise ValueError(
                    f"محرك البحث {engine.name} لا يتطلب مفتاح API")

            # تحديث مفتاح API
            engine.api_key = api_key
            engine.updated_at = datetime.now()
            engine.updated_by = self.user_id

            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_engine_api_key", {
                "engine_id": engine.id,
                "name": engine.name
            })

            logger.info(f"تم تحديث مفتاح API لمحرك البحث: {engine.name}")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(
                f"حدث خطأ أثناء تحديث مفتاح API لمحرك البحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_engine_statistics(self) -> SearchEngineStatistics:
        """
        الحصول على إحصائيات محركات البحث

        العوائد:
            SearchEngineStatistics: إحصائيات محركات البحث

        يرفع:
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة محركات البحث
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "engine"):
            raise PermissionError(PERMISSION_ERROR_READ_ENGINES)

        try:
            # إجمالي عدد محركات البحث
            # pylint: disable=not-callable
            total_engines = self.db.query(
                func.count(SearchEngine.id)).scalar() or 0

            # عدد محركات البحث النشطة
            # pylint: disable=not-callable
            active_engines = self.db.query(func.count(SearchEngine.id)).filter(
                SearchEngine.is_active
            ).scalar() or 0

            # عدد محركات البحث التي تتطلب مفتاح API
            # pylint: disable=not-callable
            api_key_required_engines = self.db.query(
                func.count(
                    SearchEngine.id)).filter(
                SearchEngine.api_key_required).scalar() or 0

            # عدد محركات البحث التي تتطلب مفتاح API ولكن لا تملك مفتاحاً
            # pylint: disable=not-callable
            missing_api_key_engines = self.db.query(
                func.count(
                    SearchEngine.id)).filter(
                SearchEngine.api_key_required,
                (SearchEngine.api_key is None) | (
                    SearchEngine.api_key == "")).scalar() or 0

            # إحصائيات آخر 24 ساعة
            time_24h_ago = datetime.now() - timedelta(hours=24)

            # pylint: disable=not-callable
            total_requests_24h = self.db.query(func.count(SearchEngineUsageLog.id)).filter(
                SearchEngineUsageLog.request_time >= time_24h_ago).scalar() or 0

            # pylint: disable=not-callable
            successful_requests_24h = self.db.query(
                func.count(
                    SearchEngineUsageLog.id)).filter(
                SearchEngineUsageLog.request_time >= time_24h_ago,
                SearchEngineUsageLog.is_successful).scalar() or 0

            # pylint: disable=not-callable
            failed_requests_24h = self.db.query(
                func.count(
                    SearchEngineUsageLog.id)).filter(
                SearchEngineUsageLog.request_time >= time_24h_ago,
                SearchEngineUsageLog.is_successful.is_(False)).scalar() or 0

            avg_response_time_24h = self.db.query(
                func.avg(
                    SearchEngineUsageLog.response_time)).filter(
                SearchEngineUsageLog.request_time >= time_24h_ago,
                SearchEngineUsageLog.response_time is not None).scalar() or 0.0

            # محركات البحث الأكثر استخداماً
            # pylint: disable=not-callable
            most_used = self.db.query(
                SearchEngine.id,
                SearchEngine.name,
                SearchEngine.display_name,
                func.count(
                    SearchEngineUsageLog.id).label("usage_count")).join(
                SearchEngineUsageLog,
                SearchEngine.id == SearchEngineUsageLog.engine_id).group_by(
                SearchEngine.id,
                SearchEngine.name,
                SearchEngine.display_name).order_by(
                desc("usage_count")).limit(5).all()

            most_used_engines = [
                {
                    "id": engine_id,
                    "name": name,
                    "display_name": display_name,
                    "usage_count": usage_count
                }
                for engine_id, name, display_name, usage_count in most_used
            ]

            # محركات البحث حسب تنسيق الاستجابة
            engines_by_response_format = {}
            for format_enum in ResponseFormatEnum:
                # pylint: disable=not-callable
                count = self.db.query(func.count(SearchEngine.id)).filter(
                    SearchEngine.response_format == format_enum
                ).scalar() or 0
                engines_by_response_format[format_enum.value] = count

            return SearchEngineStatistics(
                total_engines=total_engines,
                active_engines=active_engines,
                api_key_required_engines=api_key_required_engines,
                missing_api_key_engines=missing_api_key_engines,
                total_requests_24h=total_requests_24h,
                successful_requests_24h=successful_requests_24h,
                failed_requests_24h=failed_requests_24h,
                avg_response_time_24h=avg_response_time_24h,
                most_used_engines=most_used_engines,
                engines_by_response_format=engines_by_response_format
            )

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء الحصول على إحصائيات محركات البحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # ===== إدارة معلمات محركات البحث =====

    def create_parameter(
            self,
            param_data: SearchEngineParameterCreate) -> SearchEngineParameterResponse:
        """
        إنشاء معلمة محرك بحث جديدة

        المعلمات:
            param_data (SearchEngineParameterCreate): بيانات المعلمة الجديدة

        العوائد:
            SearchEngineParameterResponse: نموذج استجابة معلمة محرك البحث

        يرفع:
            ValueError: إذا كان محرك البحث غير موجود أو المعلمة موجودة مسبقاً
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إنشاء معلمة
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "parameter"):
            raise PermissionError("ليس لديك صلاحية إنشاء معلمة محرك بحث")

        try:
            # التحقق من وجود محرك البحث
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.id == param_data.engine_id).first()

            if not engine:
                raise ValueError(
                    f"محرك البحث غير موجود: {param_data.engine_id}")

            # التحقق من عدم وجود المعلمة مسبقاً
            existing_param = self.db.query(SearchEngineParameter).filter(
                SearchEngineParameter.engine_id == param_data.engine_id,
                SearchEngineParameter.name == param_data.name
            ).first()

            if existing_param:
                raise ValueError(
                    f"معلمة محرك البحث موجودة مسبقاً: {param_data.name}")

            # إنشاء معلمة جديدة
            new_param = SearchEngineParameter(
                engine_id=param_data.engine_id,
                name=param_data.name,
                display_name=param_data.display_name,
                description=param_data.description,
                param_type=param_data.param_type,
                required=param_data.required,
                default_value=param_data.default_value,
                validation_regex=param_data.validation_regex,
                options=param_data.options,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            self.db.add(new_param)
            self.db.commit()
            self.db.refresh(new_param)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("create_parameter", {
                "parameter_id": new_param.id,
                "name": new_param.name,
                "engine_id": new_param.engine_id
            })

            logger.info(
                f"تم إنشاء معلمة محرك بحث جديدة: {new_param.name} لمحرك البحث: {engine.name}")

            return self._parameter_to_response(new_param)

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء إنشاء معلمة محرك بحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def update_parameter(
            self,
            param_id: int,
            param_data: SearchEngineParameterUpdate) -> SearchEngineParameterResponse:
        """
        تحديث معلمة محرك بحث موجودة

        المعلمات:
            param_id (int): معرف المعلمة
            param_data (SearchEngineParameterUpdate): بيانات التحديث

        العوائد:
            SearchEngineParameterResponse: نموذج استجابة معلمة محرك البحث

        يرفع:
            ValueError: إذا كانت المعلمة غير موجودة
            PermissionError: إذا لم يكن المستخدم يملك صلاحية تحديث معلمة
        """
        # التحقق من الصلاحيات
        if not self._check_permission("update", "parameter"):
            raise PermissionError("ليس لديك صلاحية تحديث معلمة محرك بحث")

        try:
            # البحث عن المعلمة
            param = self.db.query(SearchEngineParameter).filter(
                SearchEngineParameter.id == param_id).first()

            if not param:
                raise ValueError(f"معلمة محرك البحث غير موجودة: {param_id}")

            # تحديث البيانات
            update_data = param_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(param, key, value)

            param.updated_at = datetime.now()

            self.db.commit()
            self.db.refresh(param)

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("update_parameter", {
                "parameter_id": param.id,
                "name": param.name,
                "engine_id": param.engine_id,
                "updated_fields": list(update_data.keys())
            })

            logger.info(f"تم تحديث معلمة محرك البحث: {param.name}")

            return self._parameter_to_response(param)

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء تحديث معلمة محرك بحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def delete_parameter(self, param_id: int) -> bool:
        """
        حذف معلمة محرك بحث

        المعلمات:
            param_id (int): معرف المعلمة

        العوائد:
            bool: True إذا تم الحذف بنجاح

        يرفع:
            ValueError: إذا كانت المعلمة غير موجودة
            PermissionError: إذا لم يكن المستخدم يملك صلاحية حذف معلمة
        """
        # التحقق من الصلاحيات
        if not self._check_permission("delete", "parameter"):
            raise PermissionError("ليس لديك صلاحية حذف معلمة محرك بحث")

        try:
            # البحث عن المعلمة
            param = self.db.query(SearchEngineParameter).filter(
                SearchEngineParameter.id == param_id).first()

            if not param:
                raise ValueError(f"معلمة محرك البحث غير موجودة: {param_id}")

            # حفظ معلومات المعلمة قبل الحذف
            param_info = {
                "parameter_id": param.id,
                "name": param.name,
                "engine_id": param.engine_id
            }

            # حذف المعلمة
            self.db.delete(param)
            self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("delete_parameter", param_info)

            logger.info(f"تم حذف معلمة محرك البحث: {param_info['name']}")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء حذف معلمة محرك بحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # ===== إدارة سجلات الاستخدام =====

    def log_engine_usage(
            self,
            usage_data: SearchEngineUsageLogCreate) -> SearchEngineUsageLogResponse:
        """
        تسجيل استخدام محرك بحث

        المعلمات:
            usage_data (SearchEngineUsageLogCreate): بيانات الاستخدام

        العوائد:
            SearchEngineUsageLogResponse: نموذج استجابة سجل استخدام محرك البحث

        يرفع:
            ValueError: إذا كان محرك البحث غير موجود
        """
        try:
            # البحث عن محرك البحث
            engine = self.db.query(SearchEngine).filter(
                SearchEngine.id == usage_data.engine_id).first()

            if not engine:
                raise ValueError(
                    f"محرك البحث غير موجود: {usage_data.engine_id}")

            # إضافة سجل استخدام جديد
            usage_log = SearchEngineUsageLog(
                engine_id=usage_data.engine_id,
                query=usage_data.query,
                parameters=usage_data.parameters,
                request_time=datetime.now(),
                response_time=usage_data.response_time,
                status_code=usage_data.status_code,
                results_count=usage_data.results_count,
                is_successful=usage_data.is_successful,
                error_message=usage_data.error_message,
                user_id=usage_data.user_id or self.user_id,
                session_id=usage_data.session_id,
                created_at=datetime.now()
            )

            self.db.add(usage_log)

            # تحديث إحصائيات محرك البحث
            engine.total_requests = (engine.total_requests or 0) + 1
            engine.last_request_time = datetime.now()

            # تحديث عداد الطلبات اليومية
            today = datetime.now().date()
            if engine.last_reset_date is None or engine.last_reset_date.date() < today:
                engine.current_daily_requests = 0
                engine.last_reset_date = datetime.now()

            engine.current_daily_requests = (
                engine.current_daily_requests or 0) + 1

            if usage_data.is_successful:
                engine.successful_requests = (
                    engine.successful_requests or 0) + 1
                engine.total_results = (
                    engine.total_results or 0) + usage_data.results_count
                engine.last_success_time = datetime.now()
                engine.last_error_message = None

                # تحديث متوسط وقت الاستجابة
                if usage_data.response_time is not None:
                    total_response_time = (
                        engine.avg_response_time or 0.0) * (engine.successful_requests - 1)
                    engine.avg_response_time = (
                        total_response_time + usage_data.response_time) / engine.successful_requests
            else:
                engine.failed_requests = (engine.failed_requests or 0) + 1
                engine.last_failure_time = datetime.now()
                engine.last_error_message = usage_data.error_message

            engine.updated_at = datetime.now()

            self.db.commit()
            self.db.refresh(usage_log)

            result_text = "ناجح" if usage_data.is_successful else "فاشل"
            logger.info(
                f"تم تسجيل استخدام محرك البحث {engine.name}: {result_text}")

            return SearchEngineUsageLogResponse(
                id=usage_log.id,
                engine_id=usage_log.engine_id,
                query=usage_log.query,
                parameters=usage_log.parameters,
                request_time=usage_log.request_time,
                response_time=usage_log.response_time,
                status_code=usage_log.status_code,
                results_count=usage_log.results_count,
                is_successful=usage_log.is_successful,
                error_message=usage_log.error_message,
                user_id=usage_log.user_id,
                session_id=usage_log.session_id,
                created_at=usage_log.created_at,
                engine_name=engine.name
            )

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء تسجيل استخدام محرك بحث: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    # ===== إدارة موازنات الحمل =====

    def create_load_balancer(
            self,
            balancer_data: SearchEngineLoadBalancerCreate) -> SearchEngineLoadBalancerResponse:
        """
        إنشاء موازن حمل جديد

        المعلمات:
            balancer_data (SearchEngineLoadBalancerCreate): بيانات موازن الحمل الجديد

        العوائد:
            SearchEngineLoadBalancerResponse: نموذج استجابة موازن الحمل

        يرفع:
            ValueError: إذا كان موازن الحمل موجود مسبقاً
            PermissionError: إذا لم يكن المستخدم يملك صلاحية إنشاء موازن حمل
        """
        # التحقق من الصلاحيات
        if not self._check_permission("create", "balancer"):
            raise PermissionError("ليس لديك صلاحية إنشاء موازن حمل")

        try:
            # التحقق من عدم وجود موازن الحمل مسبقاً
            existing_balancer = self.db.query(SearchEngineLoadBalancer).filter(
                SearchEngineLoadBalancer.name == balancer_data.name
            ).first()

            if existing_balancer:
                raise ValueError(
                    f"موازن الحمل موجود مسبقاً: {balancer_data.name}")

            # إنشاء موازن حمل جديد
            new_balancer = SearchEngineLoadBalancer(
                name=balancer_data.name,
                description=balancer_data.description,
                strategy=balancer_data.strategy,
                is_active=balancer_data.is_active,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by=self.user_id,
                updated_by=self.user_id
            )

            self.db.add(new_balancer)
            self.db.commit()
            self.db.refresh(new_balancer)

            # إضافة روابط محركات البحث
            if balancer_data.engine_mappings:
                for mapping_data in balancer_data.engine_mappings:
                    mapping = SearchEngineLoadBalancerMapping(
                        balancer_id=new_balancer.id,
                        engine_id=mapping_data.engine_id,
                        weight=mapping_data.weight,
                        priority=mapping_data.priority,
                        is_active=mapping_data.is_active,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    self.db.add(mapping)

                self.db.commit()

            # تسجيل الإجراء في الذاكرة المركزية
            self._log_to_memory("create_load_balancer", {
                "balancer_id": new_balancer.id,
                "name": new_balancer.name,
                "strategy": new_balancer.strategy.value
            })

            logger.info(f"تم إنشاء موازن حمل جديد: {new_balancer.name}")

            return self._balancer_to_response(new_balancer)

        except Exception as e:
            self.db.rollback()
            logger.error(f"حدث خطأ أثناء إنشاء موازن حمل: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def _balancer_to_response(
            self,
            balancer: SearchEngineLoadBalancer) -> SearchEngineLoadBalancerResponse:
        """
        تحويل نموذج موازن الحمل إلى نموذج الاستجابة

        المعلمات:
            balancer (SearchEngineLoadBalancer): نموذج موازن الحمل

        العوائد:
            SearchEngineLoadBalancerResponse: نموذج استجابة موازن الحمل
        """
        mappings = [self._mapping_to_response(
            mapping) for mapping in balancer.engine_mappings]

        return SearchEngineLoadBalancerResponse(
            id=balancer.id,
            name=balancer.name,
            description=balancer.description,
            strategy=balancer.strategy,
            is_active=balancer.is_active,
            created_at=balancer.created_at,
            updated_at=balancer.updated_at,
            created_by=balancer.created_by,
            updated_by=balancer.updated_by,
            engine_mappings=mappings
        )

    def _mapping_to_response(
            self,
            mapping: SearchEngineLoadBalancerMapping) -> SearchEngineLoadBalancerMappingResponse:
        """
        تحويل نموذج ربط موازن الحمل إلى نموذج الاستجابة

        المعلمات:
            mapping (SearchEngineLoadBalancerMapping): نموذج ربط موازن الحمل

        العوائد:
            SearchEngineLoadBalancerMappingResponse: نموذج استجابة ربط موازن الحمل
        """
        engine_name = mapping.engine.name if mapping.engine else None
        balancer_name = mapping.balancer.name if mapping.balancer else None

        return SearchEngineLoadBalancerMappingResponse(
            id=mapping.id,
            balancer_id=mapping.balancer_id,
            engine_id=mapping.engine_id,
            weight=mapping.weight,
            priority=mapping.priority,
            is_active=mapping.is_active,
            created_at=mapping.created_at,
            updated_at=mapping.updated_at,
            engine_name=engine_name,
            balancer_name=balancer_name
        )

    # ===== اختيار محرك البحث التالي =====

    def get_next_search_engine(
            self,
            balancer_id: int) -> Optional[SearchEngineResponse]:
        """
        الحصول على محرك البحث التالي من موازن الحمل بناءً على الاستراتيجية

        المعلمات:
            balancer_id (int): معرف موازن الحمل

        العوائد:
            Optional[SearchEngineResponse]: نموذج استجابة محرك البحث التالي، أو None إذا لم يكن هناك محركات بحث متاحة

        يرفع:
            ValueError: إذا كان موازن الحمل غير موجود أو غير نشط
            PermissionError: إذا لم يكن المستخدم يملك صلاحية قراءة موازن الحمل
        """
        # التحقق من الصلاحيات
        if not self._check_permission("read", "balancer"):
            raise PermissionError("ليس لديك صلاحية قراءة موازن الحمل")

        try:
            # البحث عن موازن الحمل
            balancer = self.db.query(SearchEngineLoadBalancer).filter(
                SearchEngineLoadBalancer.id == balancer_id,
                SearchEngineLoadBalancer.is_active
            ).first()

            if not balancer:
                raise ValueError(
                    f"موازن الحمل غير موجود أو غير نشط: {balancer_id}")

            # الحصول على محركات البحث المرتبطة النشطة
            active_mappings = self.db.query(SearchEngineLoadBalancerMapping).join(SearchEngine).filter(
                SearchEngineLoadBalancerMapping.balancer_id == balancer_id,
                SearchEngineLoadBalancerMapping.is_active,
                SearchEngine.is_active).all()

            if not active_mappings:
                logger.warning(
                    f"لا توجد محركات بحث نشطة مرتبطة بموازن الحمل: {balancer.name}")
                return None

            # تطبيق استراتيجية توزيع الحمل
            next_engine_id = None

            if balancer.strategy == LoadBalancerStrategyEnum.ROUND_ROBIN:
                # الحصول على آخر محرك بحث تم استخدامه في هذا الموازن
                last_used_log = self.db.query(SearchEngineUsageLog).join(
                    SearchEngineLoadBalancerMapping,
                    SearchEngineUsageLog.engine_id == SearchEngineLoadBalancerMapping.engine_id).filter(
                    SearchEngineLoadBalancerMapping.balancer_id == balancer_id).order_by(
                    desc(
                        SearchEngineUsageLog.request_time)).first()

                last_used_engine_id = last_used_log.engine_id if last_used_log else None

                # العثور على المحرك التالي في القائمة الدائرية
                engine_ids = [m.engine_id for m in active_mappings]
                if last_used_engine_id in engine_ids:
                    last_index = engine_ids.index(last_used_engine_id)
                    next_index = (last_index + 1) % len(engine_ids)
                    next_engine_id = engine_ids[next_index]
                else:
                    next_engine_id = engine_ids[0]

            elif balancer.strategy == LoadBalancerStrategyEnum.WEIGHTED:
                # توزيع عشوائي مرجح
                total_weight = sum(m.weight for m in active_mappings)
                if total_weight > 0:
                    rand_val = random.uniform(0, total_weight)
                    current_weight = 0
                    for mapping in active_mappings:
                        current_weight += mapping.weight
                        if rand_val <= current_weight:
                            next_engine_id = mapping.engine_id
                            break
                else:
                    # إذا كانت جميع الأوزان صفر، استخدم round robin
                    next_engine_id = active_mappings[0].engine_id

            elif balancer.strategy == LoadBalancerStrategyEnum.LEAST_USED:
                # اختيار المحرك الأقل استخداماً (بناءً على إجمالي الطلبات)
                engine_stats = self.db.query(
                    SearchEngine.id, SearchEngine.total_requests
                ).filter(
                    SearchEngine.id.in_([m.engine_id for m in active_mappings])
                ).order_by(asc(SearchEngine.total_requests)).first()

                if engine_stats:
                    next_engine_id = engine_stats.id

            elif balancer.strategy == LoadBalancerStrategyEnum.PRIORITY:
                # اختيار المحرك ذي الأولوية الأعلى
                prioritized_mappings = sorted(
                    active_mappings, key=lambda m: m.priority, reverse=True)
                next_engine_id = prioritized_mappings[0].engine_id

            elif balancer.strategy == LoadBalancerStrategyEnum.RANDOM:
                # اختيار عشوائي
                next_engine_id = random.choice(
                    [m.engine_id for m in active_mappings])

            else:
                # الاستراتيجية الافتراضية (round robin)
                next_engine_id = active_mappings[0].engine_id

            if next_engine_id:
                # الحصول على بيانات محرك البحث التالي
                next_engine = self.db.query(SearchEngine).filter(
                    SearchEngine.id == next_engine_id).first()
                if next_engine:
                    logger.info(
                        f"تم اختيار محرك البحث التالي من موازن الحمل {balancer.name}: {next_engine.name}")
                    return self._engine_to_response(next_engine)

            logger.warning(
                f"لم يتم العثور على محرك بحث تالٍ لموازن الحمل: {balancer.name}")
            return None

        except Exception as e:
            logger.error(
                f"حدث خطأ أثناء الحصول على محرك البحث التالي: {str(e)}")
            logger.error(traceback.format_exc())
            raise
