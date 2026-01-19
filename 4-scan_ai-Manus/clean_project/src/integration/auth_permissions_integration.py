"""
/home/ubuntu/implemented_files/v3/src/integration/auth_permissions_integration.py

ملف تكامل المصادقة والصلاحيات في نظام Gaara ERP
يوفر هذا الملف الوظائف والفئات اللازمة لربط مديول المصادقة مع مديول الصلاحيات
"""

import logging
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any

# استيراد المديولات الداخلية
from src.modules.authentication.service import AuthenticationService
from src.modules.authentication.models import AuthToken, LoginAttempt, MFAMethod
from src.modules.authentication.schemas import TokenData, LoginRequest, MFAVerifyRequest
from src.modules.permissions.service import PermissionService
from src.modules.permissions.models import Role, Permission, UserRole
from src.modules.user_management.service import UserManagementService
from src.modules.user_management.models import User, UserProfile, UserPreference

# إعداد السجل
logger = logging.getLogger(__name__)


class AuthPermissionsIntegration:
    """
    فئة تكامل المصادقة والصلاحيات
    توفر هذه الفئة الوظائف اللازمة لربط مديول المصادقة مع مديول الصلاحيات
    """

    def __init__(
        self,
        auth_service: Optional[AuthenticationService] = None,
        permission_service: Optional[PermissionService] = None,
        user_service: Optional[UserManagementService] = None
    ):
        """
        تهيئة فئة تكامل المصادقة والصلاحيات

        المعلمات:
            auth_service: خدمة المصادقة
            permission_service: خدمة الصلاحيات
            user_service: خدمة إدارة المستخدمين
        """
        self.auth_service = auth_service or AuthenticationService()
        self.permission_service = permission_service or PermissionService()
        self.user_service = user_service or UserManagementService()
        logger.info("تم تهيئة تكامل المصادقة والصلاحيات")

    async def authenticate_and_get_permissions(
        self,
        username: str,
        password: str,
        ip_address: str = None,
        user_agent: str = None
    ) -> Tuple[TokenData, List[Permission]]:
        """
        مصادقة المستخدم والحصول على صلاحياته

        المعلمات:
            username: اسم المستخدم
            password: كلمة المرور
            ip_address: عنوان IP للمستخدم (اختياري)
            user_agent: وكيل المستخدم (اختياري)

        العوائد:
            Tuple[TokenData, List[Permission]]: بيانات الرمز وقائمة الصلاحيات
        """
        # مصادقة المستخدم
        login_request = LoginRequest(
            username=username,
            password=password,
            ip_address=ip_address,
            user_agent=user_agent
        )

        token_data = await self.auth_service.login(login_request)

        if not token_data:
            logger.error(f"فشل تسجيل الدخول للمستخدم: {username}")
            raise ValueError("بيانات الاعتماد غير صالحة")

        # الحصول على صلاحيات المستخدم
        permissions = await self.permission_service.get_user_permissions(token_data.user_id)

        logger.info(f"تم مصادقة المستخدم والحصول على الصلاحيات: {username} (ID: {token_data.user_id})")

        return token_data, permissions

    async def verify_token_and_permission(
        self,
        token: str,
        required_permission: str,
        resource_id: str = None
    ) -> Tuple[TokenData, bool]:
        """
        التحقق من صحة الرمز والصلاحية

        المعلمات:
            token: رمز المصادقة
            required_permission: الصلاحية المطلوبة
            resource_id: معرف المورد (اختياري)

        العوائد:
            Tuple[TokenData, bool]: بيانات الرمز وحالة الصلاحية
        """
        # التحقق من صحة الرمز
        token_data = await self.auth_service.verify_token(token)

        if not token_data:
            logger.error("رمز المصادقة غير صالح أو منتهي الصلاحية")
            raise ValueError("رمز المصادقة غير صالح أو منتهي الصلاحية")

        # التحقق من الصلاحية
        has_permission = await self.permission_service.check_permission(
            user_id=token_data.user_id,
            permission=required_permission,
            resource_id=resource_id
        )

        if has_permission:
            logger.info(f"المستخدم {token_data.user_id} لديه الصلاحية: {required_permission}")
        else:
            logger.warning(f"المستخدم {token_data.user_id} ليس لديه الصلاحية: {required_permission}")

        return token_data, has_permission

    async def assign_default_roles_to_new_user(
        self,
        user_id: str,
        organization_id: str = None,
        is_admin: bool = False
    ) -> List[Role]:
        """
        تعيين الأدوار الافتراضية للمستخدم الجديد

        المعلمات:
            user_id: معرف المستخدم
            organization_id: معرف المؤسسة (اختياري)
            is_admin: ما إذا كان المستخدم مسؤولاً

        العوائد:
            List[Role]: قائمة الأدوار المعينة
        """
        # الحصول على المستخدم
        user = await self.user_service.get_user(user_id)

        if not user:
            logger.error(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")
            raise ValueError(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")

        # تحديد الأدوار الافتراضية
        default_roles = []

        # دور المستخدم الأساسي
        basic_user_role = await self.permission_service.get_role_by_name("basic_user")
        if basic_user_role:
            default_roles.append(basic_user_role)

        # دور المسؤول إذا كان مطلوباً
        if is_admin:
            admin_role = await self.permission_service.get_role_by_name("admin")
            if admin_role:
                default_roles.append(admin_role)

        # دور المؤسسة إذا كان متاحاً
        if organization_id:
            org_role_name = f"org_{organization_id}_member"
            org_role = await self.permission_service.get_role_by_name(org_role_name)
            if org_role:
                default_roles.append(org_role)

        # تعيين الأدوار للمستخدم
        assigned_roles = []
        for role in default_roles:
            success = await self.permission_service.assign_role_to_user(user_id, role.id)
            if success:
                assigned_roles.append(role)
                logger.info(f"تم تعيين الدور {role.name} للمستخدم {user.username} (ID: {user_id})")
            else:
                logger.error(f"فشل تعيين الدور {role.name} للمستخدم {user.username} (ID: {user_id})")

        return assigned_roles

    async def revoke_user_sessions_on_permission_change(
        self,
        user_id: str,
        admin_user_id: str = None
    ) -> int:
        """
        إلغاء جلسات المستخدم عند تغيير الصلاحيات

        المعلمات:
            user_id: معرف المستخدم
            admin_user_id: معرف المستخدم المسؤول الذي قام بالتغيير (اختياري)

        العوائد:
            int: عدد الجلسات الملغاة
        """
        # الحصول على المستخدم
        user = await self.user_service.get_user(user_id)

        if not user:
            logger.error(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")
            raise ValueError(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")

        # إلغاء جميع رموز المستخدم
        revoked_count = await self.auth_service.revoke_all_user_tokens(user_id)

        # تسجيل الحدث
        logger.info(f"تم إلغاء {revoked_count} جلسة للمستخدم {user.username} (ID: {user_id}) بعد تغيير الصلاحيات")

        if admin_user_id:
            admin_user = await self.user_service.get_user(admin_user_id)
            admin_username = admin_user.username if admin_user else "غير معروف"
            logger.info(f"تم تغيير الصلاحيات بواسطة المسؤول: {admin_username} (ID: {admin_user_id})")

        return revoked_count

    async def get_user_roles_and_permissions(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        الحصول على أدوار وصلاحيات المستخدم

        المعلمات:
            user_id: معرف المستخدم

        العوائد:
            Dict[str, Any]: قاموس يحتوي على أدوار وصلاحيات المستخدم
        """
        # الحصول على المستخدم
        user = await self.user_service.get_user(user_id)

        if not user:
            logger.error(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")
            raise ValueError(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")

        # الحصول على أدوار المستخدم
        roles = await self.permission_service.get_user_roles(user_id)

        # الحصول على صلاحيات المستخدم
        permissions = await self.permission_service.get_user_permissions(user_id)

        # تجميع البيانات
        result = {
            "user_id": user_id,
            "username": user.username,
            "roles": [
                {
                    "id": role.id,
                    "name": role.name,
                    "description": role.description
                }
                for role in roles
            ],
            "permissions": [
                {
                    "id": permission.id,
                    "name": permission.name,
                    "description": permission.description,
                    "resource_type": permission.resource_type
                }
                for permission in permissions
            ],
            "is_admin": any(role.name == "admin" for role in roles),
            "timestamp": datetime.utcnow().isoformat()
        }

        logger.info(f"تم استرجاع أدوار وصلاحيات المستخدم {user.username} (ID: {user_id})")

        return result

    async def check_multi_level_permission(
        self,
        user_id: str,
        permission_hierarchy: List[Dict[str, str]]
    ) -> bool:
        """
        التحقق من الصلاحية متعددة المستويات

        المعلمات:
            user_id: معرف المستخدم
            permission_hierarchy: تسلسل هرمي للصلاحيات
                [
                    {"permission": "view_country", "resource_id": "country_123"},
                    {"permission": "view_company", "resource_id": "company_456"},
                    {"permission": "view_branch", "resource_id": "branch_789"}
                ]

        العوائد:
            bool: ما إذا كان المستخدم يمتلك الصلاحية
        """
        # الحصول على المستخدم
        user = await self.user_service.get_user(user_id)

        if not user:
            logger.error(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")
            raise ValueError(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")

        # التحقق من كل مستوى في التسلسل الهرمي
        for level in permission_hierarchy:
            permission_name = level.get("permission")
            resource_id = level.get("resource_id")

            has_permission = await self.permission_service.check_permission(
                user_id=user_id,
                permission=permission_name,
                resource_id=resource_id
            )

            if has_permission:
                # إذا كان المستخدم يمتلك الصلاحية على هذا المستوى، فلا داعي للتحقق من المستويات الأدنى
                logger.info(f"المستخدم {user.username} (ID: {user_id}) لديه الصلاحية {permission_name} على المورد {resource_id}")
                return True

        # إذا وصلنا إلى هنا، فإن المستخدم لا يمتلك أي صلاحية في التسلسل الهرمي
        logger.warning(f"المستخدم {user.username} (ID: {user_id}) ليس لديه أي صلاحية في التسلسل الهرمي")
        return False

    async def create_audit_log_for_permission_change(
        self,
        user_id: str,
        admin_user_id: str,
        action: str,
        role_id: str = None,
        permission_id: str = None,
        resource_id: str = None,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        إنشاء سجل تدقيق لتغيير الصلاحية

        المعلمات:
            user_id: معرف المستخدم المتأثر
            admin_user_id: معرف المستخدم المسؤول الذي قام بالتغيير
            action: الإجراء (add_role, remove_role, add_permission, remove_permission)
            role_id: معرف الدور (اختياري)
            permission_id: معرف الصلاحية (اختياري)
            resource_id: معرف المورد (اختياري)
            details: تفاصيل إضافية (اختياري)

        العوائد:
            Dict[str, Any]: سجل التدقيق
        """
        # الحصول على المستخدم المتأثر
        user = await self.user_service.get_user(user_id)
        if not user:
            logger.error(f"لم يتم العثور على المستخدم المتأثر بالمعرف: {user_id}")
            raise ValueError(f"لم يتم العثور على المستخدم المتأثر بالمعرف: {user_id}")

        # الحصول على المستخدم المسؤول
        admin_user = await self.user_service.get_user(admin_user_id)
        if not admin_user:
            logger.error(f"لم يتم العثور على المستخدم المسؤول بالمعرف: {admin_user_id}")
            raise ValueError(f"لم يتم العثور على المستخدم المسؤول بالمعرف: {admin_user_id}")

        # الحصول على معلومات الدور إذا كان متاحاً
        role_info = None
        if role_id:
            role = await self.permission_service.get_role(role_id)
            if role:
                role_info = {
                    "id": role.id,
                    "name": role.name,
                    "description": role.description
                }

        # الحصول على معلومات الصلاحية إذا كانت متاحة
        permission_info = None
        if permission_id:
            permission = await self.permission_service.get_permission(permission_id)
            if permission:
                permission_info = {
                    "id": permission.id,
                    "name": permission.name,
                    "description": permission.description,
                    "resource_type": permission.resource_type
                }

        # إنشاء سجل التدقيق
        audit_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "affected_user": {
                "id": user_id,
                "username": user.username
            },
            "admin_user": {
                "id": admin_user_id,
                "username": admin_user.username
            },
            "role": role_info,
            "permission": permission_info,
            "resource_id": resource_id,
            "details": details or {}
        }

        # تسجيل الحدث
        logger.info(f"تم إنشاء سجل تدقيق لتغيير الصلاحية: {action} للمستخدم {user.username} بواسطة {admin_user.username}")

        # هنا يمكن إضافة منطق لتخزين سجل التدقيق في قاعدة البيانات

        return audit_log

    async def sync_user_permissions_with_organization(
        self,
        user_id: str,
        organization_id: str,
        admin_user_id: str = None
    ) -> Dict[str, Any]:
        """
        مزامنة صلاحيات المستخدم مع المؤسسة

        المعلمات:
            user_id: معرف المستخدم
            organization_id: معرف المؤسسة
            admin_user_id: معرف المستخدم المسؤول الذي قام بالتغيير (اختياري)

        العوائد:
            Dict[str, Any]: نتيجة المزامنة
        """
        # الحصول على المستخدم
        user = await self.user_service.get_user(user_id)
        if not user:
            logger.error(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")
            raise ValueError(f"لم يتم العثور على المستخدم بالمعرف: {user_id}")

        # الحصول على أدوار المؤسسة
        org_roles = await self.permission_service.get_organization_roles(organization_id)

        # الحصول على أدوار المستخدم الحالية
        current_user_roles = await self.permission_service.get_user_roles(user_id)
        current_role_ids = [role.id for role in current_user_roles]

        # تحديد الأدوار التي يجب إضافتها
        roles_to_add = []
        for role in org_roles:
            if role.id not in current_role_ids:
                roles_to_add.append(role)

        # إضافة الأدوار الجديدة
        added_roles = []
        for role in roles_to_add:
            success = await self.permission_service.assign_role_to_user(user_id, role.id)
            if success:
                added_roles.append(role)

                # إنشاء سجل تدقيق
                if admin_user_id:
                    await self.create_audit_log_for_permission_change(
                        user_id=user_id,
                        admin_user_id=admin_user_id,
                        action="add_role",
                        role_id=role.id,
                        details={"organization_id": organization_id, "sync": True}
                    )

        # تجميع نتيجة المزامنة
        result = {
            "user_id": user_id,
            "username": user.username,
            "organization_id": organization_id,
            "added_roles": [
                {
                    "id": role.id,
                    "name": role.name,
                    "description": role.description
                }
                for role in added_roles
            ],
            "total_roles_after_sync": len(current_role_ids) + len(added_roles),
            "timestamp": datetime.utcnow().isoformat()
        }

        logger.info(f"تمت مزامنة صلاحيات المستخدم {user.username} (ID: {user_id}) مع المؤسسة (ID: {organization_id})")

        return result
