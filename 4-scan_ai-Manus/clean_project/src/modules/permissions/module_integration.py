"""
ملف تكامل المديولات مع نظام الصلاحيات

يوفر هذا الملف وظائف لتكامل مديولات النظام المختلفة مع نظام الصلاحيات.
يتم استخدام هذه الوظائف لتسجيل المديولات وميزاتها في نظام الصلاحيات،
وتحديد الصلاحيات المطلوبة للوصول إلى كل ميزة.
"""

from typing import Dict, List, Optional, Set
import logging
from sqlalchemy.orm import Session

from .service import PermissionService
from .config import REQUIRED_INTEGRATION_MODULES, PermissionType, PermissionScope

# إعداد المسجل
logger = logging.getLogger(__name__)


class ModuleIntegration:
    """
    فئة لإدارة تكامل المديولات مع نظام الصلاحيات
    """

    def __init__(self, db: Session, permission_service: Optional[PermissionService] = None):
        """
        تهيئة كائن تكامل المديولات

        المعلمات:
            db (Session): جلسة قاعدة البيانات
            permission_service (PermissionService, optional): خدمة الصلاحيات
        """
        self.db = db
        self.permission_service = permission_service or PermissionService(db)
        self._registered_modules: Set[str] = set()

    def register_module(self, module_name: str, features: List[str]) -> bool:
        """
        تسجيل مديول في نظام الصلاحيات

        المعلمات:
            module_name (str): اسم المديول
            features (List[str]): قائمة بميزات المديول

        العوائد:
            bool: True إذا تم التسجيل بنجاح، False خلاف ذلك
        """
        if module_name in self._registered_modules:
            logger.warning(f"المديول {module_name} مسجل بالفعل")
            return False

        try:
            # إنشاء صلاحيات للمديول
            for feature in features:
                for perm_type in PermissionType:
                    permission_name = f"{module_name}.{feature}.{perm_type.value}"
                    self.permission_service.create_permission(
                        name=permission_name,
                        description=f"صلاحية {perm_type.value} لميزة {feature} في مديول {module_name}",
                        scope=PermissionScope.FEATURE.value
                    )

            # إنشاء صلاحيات على مستوى المديول
            for perm_type in PermissionType:
                permission_name = f"{module_name}.{perm_type.value}"
                self.permission_service.create_permission(
                    name=permission_name,
                    description=f"صلاحية {perm_type.value} لجميع ميزات مديول {module_name}",
                    scope=PermissionScope.MODULE.value
                )

            self._registered_modules.add(module_name)
            logger.info(f"تم تسجيل المديول {module_name} بنجاح")
            return True

        except Exception as e:
            logger.error(f"خطأ أثناء تسجيل المديول {module_name}: {str(e)}")
            return False

    def unregister_module(self, module_name: str) -> bool:
        """
        إلغاء تسجيل مديول من نظام الصلاحيات

        المعلمات:
            module_name (str): اسم المديول

        العوائد:
            bool: True إذا تم إلغاء التسجيل بنجاح، False خلاف ذلك
        """
        if module_name not in self._registered_modules:
            logger.warning(f"المديول {module_name} غير مسجل")
            return False

        try:
            # حذف جميع الصلاحيات المتعلقة بالمديول
            permissions = self.permission_service.get_permissions_by_prefix(f"{module_name}.")
            for permission in permissions:
                self.permission_service.delete_permission(permission.id)

            self._registered_modules.remove(module_name)
            logger.info(f"تم إلغاء تسجيل المديول {module_name} بنجاح")
            return True

        except Exception as e:
            logger.error(f"خطأ أثناء إلغاء تسجيل المديول {module_name}: {str(e)}")
            return False

    def assign_module_permissions_to_role(
        self,
        module_name: str,
        role_name: str,
        permission_types: List[PermissionType]
    ) -> bool:
        """
        تعيين صلاحيات مديول لدور معين

        المعلمات:
            module_name (str): اسم المديول
            role_name (str): اسم الدور
            permission_types (List[PermissionType]): أنواع الصلاحيات المراد تعيينها

        العوائد:
            bool: True إذا تم التعيين بنجاح، False خلاف ذلك
        """
        try:
            role = self.permission_service.get_role_by_name(role_name)
            if not role:
                logger.error(f"الدور {role_name} غير موجود")
                return False

            for perm_type in permission_types:
                permission_name = f"{module_name}.{perm_type.value}"
                permission = self.permission_service.get_permission_by_name(permission_name)
                if permission:
                    self.permission_service.assign_permission_to_role(role.id, permission.id)

            logger.info(f"تم تعيين صلاحيات المديول {module_name} للدور {role_name} بنجاح")
            return True

        except Exception as e:
            logger.error(f"خطأ أثناء تعيين صلاحيات المديول {module_name} للدور {role_name}: {str(e)}")
            return False

    def check_required_integrations(self) -> Dict[str, bool]:
        """
        التحقق من تكامل جميع المديولات المطلوبة مع نظام الصلاحيات

        العوائد:
            Dict[str, bool]: قاموس يحتوي على حالة تكامل كل مديول
        """
        result = {}
        for module in REQUIRED_INTEGRATION_MODULES:
            result[module] = module in self._registered_modules
        return result

    def get_registered_modules(self) -> Set[str]:
        """
        الحصول على قائمة المديولات المسجلة

        العوائد:
            Set[str]: مجموعة بأسماء المديولات المسجلة
        """
        return self._registered_modules.copy()


# دالة مساعدة لتسجيل المديولات
def register_all_modules(db: Session) -> Dict[str, bool]:
    """
    تسجيل جميع المديولات المطلوبة في نظام الصلاحيات

    المعلمات:
        db (Session): جلسة قاعدة البيانات

    العوائد:
        Dict[str, bool]: قاموس يحتوي على نتيجة تسجيل كل مديول
    """
    integration = ModuleIntegration(db)
    results = {}

    # تعريف المديولات وميزاتها
    modules_features = {
        "auth": ["users", "login", "logout", "reset_password", "profile"],
        "ai_agent_module": ["agents", "conversations", "settings", "templates"],
        "ai_management": ["models", "settings", "usage", "logs"],
        "plant_diagnosis": ["diagnose", "history", "reports", "settings"],
        "image_search": ["search", "upload", "gallery", "settings", "auto_learning"],
        "memory": ["store", "retrieve", "manage", "settings"],
    }

    # تسجيل كل مديول
    for module, features in modules_features.items():
        results[module] = integration.register_module(module, features)

    return results
