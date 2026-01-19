"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/ai_management/permissions_integration.py
الوصف: ملف تكامل الصلاحيات مع مديول إدارة الذكاء الاصطناعي
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from typing import Dict, List, Optional, Any
import logging

from src.modules.ai_management.models import AIModel, ModelPermission, ModelRole
from src.modules.permissions.models import Role, UserRole
from src.modules.permissions.service import PermissionService
from src.database import get_db
logger = logging.getLogger(__name__)

# تعريف الثوابت للصلاحيات
PERMISSION_CREATE = "ai_model:create"
PERMISSION_READ = "ai_model:read"
PERMISSION_UPDATE = "ai_model:update"
PERMISSION_TRAIN = "ai_model:train"
PERMISSION_EVALUATE = "ai_model:evaluate"
PERMISSION_VIEW_METRICS = "ai_model:view_metrics"
PERMISSION_MANAGE_VERSIONS = "ai_model:manage_versions"
PERMISSION_MANAGE_DATASETS = "ai_model:manage_datasets"


class AIManagementPermissionsIntegration:
    """فئة تكامل الصلاحيات مع مديول إدارة الذكاء الاصطناعي"""

    def __init__(self, permission_service: Optional[PermissionService] = None):
        """
        تهيئة فئة تكامل الصلاحيات مع مديول إدارة الذكاء الاصطناعي

        المعلمات:
            permission_service: خدمة الصلاحيات (اختياري)
        """
        if permission_service is None:
            # Get a database session for the PermissionService
            db = next(get_db())
            self.permission_service = PermissionService(db)
        else:
            self.permission_service = permission_service
        self._register_default_permissions()
        self._register_default_roles()

    def _register_default_permissions(self) -> None:
        """تسجيل الصلاحيات الافتراضية لإدارة الذكاء الاصطناعي"""
        default_permissions = [
            {
                "name": PERMISSION_CREATE,
                "description": "إنشاء نموذج ذكاء اصطناعي جديد",
                "module": "ai_management",
                "is_system": True,
            },
            {
                "name": PERMISSION_READ,
                "description": "عرض نماذج الذكاء الاصطناعي",
                "module": "ai_management",
                "is_system": True,
            },
            {
                "name": PERMISSION_UPDATE,
                "description": "تحديث نموذج ذكاء اصطناعي",
                "module": "ai_management",
                "is_system": True,
            },
            {
                "name": PERMISSION_TRAIN,
                "description": "تدريب نموذج ذكاء اصطناعي",
                "module": "ai_management",
                "is_system": True,
            },
            {
                "name": PERMISSION_EVALUATE,
                "description": "تقييم نموذج ذكاء اصطناعي",
                "module": "ai_management",
                "is_system": True,
            },
            {
                "name": PERMISSION_VIEW_METRICS,
                "description": "عرض مقاييس نموذج ذكاء اصطناعي",
                "module": "ai_management",
                "is_system": True,
            },
            {
                "name": PERMISSION_MANAGE_VERSIONS,
                "description": "إدارة إصدارات نموذج ذكاء اصطناعي",
                "module": "ai_management",
                "is_system": True,
            },
            {
                "name": PERMISSION_MANAGE_DATASETS,
                "description": "إدارة مجموعات البيانات لنموذج ذكاء اصطناعي",
                "module": "ai_management",
                "is_system": True,
            },
        ]

        for permission_data in default_permissions:
            try:
                self.permission_service.create_permission_if_not_exists(
                    name=permission_data["name"],
                    description=permission_data["description"],
                    module=permission_data["module"],
                    is_system=permission_data["is_system"],
                )
            except Exception as e:
                logger.error(f"خطأ في تسجيل الصلاحية {permission_data['name']}: {str(e)}")

    def _register_default_roles(self) -> None:
        """تسجيل الأدوار الافتراضية لإدارة الذكاء الاصطناعي"""
        default_roles = [
            {
                "name": "ai_admin",
                "description": "مدير الذكاء الاصطناعي",
                "permissions": [
                    "ai_model:create", "ai_model:read", "ai_model:update", "ai_model:delete",
                    "ai_model:deploy", "ai_model:train", "ai_model:evaluate", "ai_model:view_metrics",
                    "ai_model:manage_versions", "ai_model:manage_datasets", "ai_model:manage_providers",
                    "ai_model:manage_api_keys"
                ],
                "is_system": True,
            },
            {
                "name": "ai_user",
                "description": "مستخدم نماذج الذكاء الاصطناعي",
                "permissions": [
                    "ai_model:read", "ai_model:view_metrics"
                ],
                "is_system": True,
            },
            {
                "name": "ai_developer",
                "description": "مطور نماذج الذكاء الاصطناعي",
                "permissions": [
                    "ai_model:create", "ai_model:read", "ai_model:update", "ai_model:train",
                    "ai_model:evaluate", "ai_model:view_metrics", "ai_model:manage_versions",
                    "ai_model:manage_datasets"
                ],
                "is_system": True,
            },
        ]

        for role_data in default_roles:
            try:
                role = self.permission_service.create_role_if_not_exists(
                    name=role_data["name"],
                    description=role_data["description"],
                    is_system=role_data["is_system"],
                )

                # إضافة الصلاحيات للدور
                for permission_name in role_data["permissions"]:
                    permission = self.permission_service.get_permission_by_name(permission_name)
                    if permission:
                        self.permission_service.assign_permission_to_role(role.id, permission.id)
                    else:
                        logger.warning(f"الصلاحية {permission_name} غير موجودة")
            except Exception as e:
                logger.error(f"خطأ في تسجيل الدور {role_data['name']}: {str(e)}")

    def check_model_permission(self, user_id: int, model_id: int, permission_name: str) -> bool:
        """
        التحقق من صلاحية المستخدم للوصول إلى نموذج ذكاء اصطناعي

        المعلمات:
            user_id: معرف المستخدم
            model_id: معرف نموذج الذكاء الاصطناعي
            permission_name: اسم الصلاحية المطلوبة

        العائد:
            bool: صحيح إذا كان المستخدم يملك الصلاحية، خطأ في حالة العكس
        """
        try:
            # التحقق من صلاحية المستخدم العامة
            has_permission = self.permission_service.check_user_permission(user_id, permission_name)
            if not has_permission:
                return False

            # التحقق من صلاحية المستخدم الخاصة بالنموذج
            model_permission = ModelPermission.query.filter_by(
                user_id=user_id, model_id=model_id
            ).first()

            if model_permission:
                return True

            # التحقق من أدوار المستخدم للنموذج
            model_roles = ModelRole.query.filter_by(model_id=model_id).all()
            user_roles = UserRole.query.filter_by(user_id=user_id).all()
            user_role_ids = [ur.role_id for ur in user_roles]

            for model_role in model_roles:
                if model_role.role_id in user_role_ids:
                    return True

            return False
        except Exception as e:
            logger.error(f"خطأ في التحقق من صلاحية المستخدم: {str(e)}")
            return False

    def assign_model_permission(self, user_id: int, model_id: int, permission_type: str) -> bool:
        """
        تعيين صلاحية للمستخدم على نموذج ذكاء اصطناعي

        المعلمات:
            user_id: معرف المستخدم
            model_id: معرف نموذج الذكاء الاصطناعي
            permission_type: نوع الصلاحية (read, write, execute, admin)

        العائد:
            bool: صحيح إذا تم تعيين الصلاحية بنجاح، خطأ في حالة العكس
        """
        try:
            # التحقق من وجود الصلاحية
            existing_permission = ModelPermission.query.filter_by(
                user_id=user_id, model_id=model_id
            ).first()

            if existing_permission:
                existing_permission.permission_type = permission_type
            else:
                new_permission = ModelPermission(
                    user_id=user_id,
                    model_id=model_id,
                    permission_type=permission_type
                )
                from src.modules.ai_management.service import db
                db.session.add(new_permission)

            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"خطأ في تعيين صلاحية المستخدم: {str(e)}")
            db.session.rollback()
            return False

    def revoke_model_permission(self, user_id: int, model_id: int) -> bool:
        """
        إلغاء صلاحية المستخدم على نموذج ذكاء اصطناعي

        المعلمات:
            user_id: معرف المستخدم
            model_id: معرف نموذج الذكاء الاصطناعي

        العائد:
            bool: صحيح إذا تم إلغاء الصلاحية بنجاح، خطأ في حالة العكس
        """
        try:
            permission = ModelPermission.query.filter_by(
                user_id=user_id, model_id=model_id
            ).first()

            if permission:
                from src.modules.ai_management.service import db
                db.session.delete(permission)
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"خطأ في إلغاء صلاحية المستخدم: {str(e)}")
            db.session.rollback()
            return False

    def get_user_models(self, user_id: int) -> List[Dict[str, Any]]:
        """
        الحصول على نماذج الذكاء الاصطناعي المتاحة للمستخدم

        المعلمات:
            user_id: معرف المستخدم

        العائد:
            List[Dict[str, Any]]: قائمة بنماذج الذكاء الاصطناعي المتاحة للمستخدم
        """
        try:
            # التحقق من صلاحية المستخدم العامة
            has_permission = self.permission_service.check_user_permission(user_id, "ai_model:read")
            if not has_permission:
                return []

            # الحصول على نماذج الذكاء الاصطناعي المتاحة للمستخدم
            user_permissions = ModelPermission.query.filter_by(user_id=user_id).all()
            model_ids = [up.model_id for up in user_permissions]

            # الحصول على أدوار المستخدم
            user_roles = UserRole.query.filter_by(user_id=user_id).all()
            user_role_ids = [ur.role_id for ur in user_roles]

            # الحصول على نماذج الذكاء الاصطناعي المتاحة للأدوار
            model_roles = ModelRole.query.filter(ModelRole.role_id.in_(user_role_ids)).all()
            for model_role in model_roles:
                if model_role.model_id not in model_ids:
                    model_ids.append(model_role.model_id)

            # الحصول على نماذج الذكاء الاصطناعي العامة
            public_models = AIModel.query.filter_by(is_public=True).all()
            for model in public_models:
                if model.id not in model_ids:
                    model_ids.append(model.id)

            # الحصول على تفاصيل نماذج الذكاء الاصطناعي
            models = AIModel.query.filter(AIModel.id.in_(model_ids)).all()
            result = []
            for model in models:
                model_data = {
                    "id": model.id,
                    "name": model.name,
                    "description": model.description,
                    "provider": model.provider,
                    "version": model.version,
                    "status": model.status,
                    "is_public": model.is_public,
                    "created_at": model.created_at.isoformat() if model.created_at else None,
                    "updated_at": model.updated_at.isoformat() if model.updated_at else None,
                }
                result.append(model_data)

            return result
        except Exception as e:
            logger.error("خطأ في الحصول على نماذج الذكاء الاصطناعي المتاحة للمستخدم: %s", str(e))
            return []

    def create_model_role(self, model_id: int, role_id: int) -> bool:
        """
        إنشاء دور لنموذج ذكاء اصطناعي

        المعلمات:
            model_id: معرف نموذج الذكاء الاصطناعي
            role_id: معرف الدور

        العائد:
            bool: صحيح إذا تم إنشاء الدور بنجاح، خطأ في حالة العكس
        """
        try:
            # التحقق من وجود الدور
            existing_role = ModelRole.query.filter_by(
                model_id=model_id, role_id=role_id
            ).first()

            if not existing_role:
                new_role = ModelRole(
                    model_id=model_id,
                    role_id=role_id
                )
                from src.modules.ai_management.service import db
                db.session.add(new_role)
                db.session.commit()
            return True
        except Exception as e:
            logger.error(f"خطأ في إنشاء دور لنموذج ذكاء اصطناعي: {str(e)}")
            db.session.rollback()
            return False

    def delete_model_role(self, model_id: int, role_id: int) -> bool:
        """
        حذف دور من نموذج ذكاء اصطناعي

        المعلمات:
            model_id: معرف نموذج الذكاء الاصطناعي
            role_id: معرف الدور

        العائد:
            bool: صحيح إذا تم حذف الدور بنجاح، خطأ في حالة العكس
        """
        try:
            role = ModelRole.query.filter_by(
                model_id=model_id, role_id=role_id
            ).first()

            if role:
                from src.modules.ai_management.service import db
                db.session.delete(role)
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"خطأ في حذف دور من نموذج ذكاء اصطناعي: {str(e)}")
            db.session.rollback()
            return False

    def get_model_roles(self, model_id: int) -> List[Dict[str, Any]]:
        """
        الحصول على أدوار نموذج ذكاء اصطناعي

        المعلمات:
            model_id: معرف نموذج الذكاء الاصطناعي

        العائد:
            List[Dict[str, Any]]: قائمة بأدوار نموذج الذكاء الاصطناعي
        """
        try:
            model_roles = ModelRole.query.filter_by(model_id=model_id).all()
            role_ids = [mr.role_id for mr in model_roles]
            roles = Role.query.filter(Role.id.in_(role_ids)).all()

            result = []
            for role in roles:
                role_data = {
                    "id": role.id,
                    "name": role.name,
                    "description": role.description,
                    "is_system": role.is_system,
                    "created_at": role.created_at.isoformat() if role.created_at else None,
                    "updated_at": role.updated_at.isoformat() if role.updated_at else None,
                }
                result.append(role_data)

            return result
        except Exception as e:
            logger.error("خطأ في الحصول على أدوار نموذج ذكاء اصطناعي: %s", str(e))
            return []

    def get_model_permissions(self, model_id: int) -> List[Dict[str, Any]]:
        """
        الحصول على صلاحيات نموذج ذكاء اصطناعي

        المعلمات:
            model_id: معرف نموذج الذكاء الاصطناعي

        العائد:
            List[Dict[str, Any]]: قائمة بصلاحيات نموذج الذكاء الاصطناعي
        """
        try:
            model_permissions = ModelPermission.query.filter_by(model_id=model_id).all()
            result = []
            for permission in model_permissions:
                permission_data = {
                    "id": permission.id,
                    "user_id": permission.user_id,
                    "model_id": permission.model_id,
                    "permission_type": permission.permission_type,
                    "created_at": permission.created_at.isoformat() if permission.created_at else None,
                    "updated_at": permission.updated_at.isoformat() if permission.updated_at else None,
                }
                result.append(permission_data)

            return result
        except Exception as e:
            logger.error("خطأ في الحصول على صلاحيات نموذج ذكاء اصطناعي: %s", str(e))
            return []

    def sync_model_permissions(self) -> bool:
        """
        مزامنة صلاحيات نماذج الذكاء الاصطناعي مع نظام الصلاحيات العام

        العائد:
            bool: صحيح إذا تمت المزامنة بنجاح، خطأ في حالة العكس
        """
        try:
            # إعادة تسجيل الصلاحيات الافتراضية
            self._register_default_permissions()
            self._register_default_roles()
            return True
        except Exception as e:
            logger.error("خطأ في مزامنة صلاحيات نماذج الذكاء الاصطناعي: %s", str(e))
            return False

    def create_audit_log(self, user_id: int, model_id: int, action: str, details: Dict[str, Any]) -> bool:
        """
        إنشاء سجل تدقيق لعمليات الصلاحيات على نماذج الذكاء الاصطناعي

        المعلمات:
            user_id: معرف المستخدم
            model_id: معرف نموذج الذكاء الاصطناعي
            action: نوع العملية
            details: تفاصيل العملية

        العائد:
            bool: صحيح إذا تم إنشاء السجل بنجاح، خطأ في حالة العكس
        """
        try:
            from src.modules.ai_management.service import create_model_audit_log
            create_model_audit_log(
                user_id=user_id,
                model_id=model_id,
                action=f"permission_{action}",
                details=details
            )
            return True
        except Exception as e:
            logger.error("خطأ في إنشاء سجل تدقيق: %s", str(e))
            return False
