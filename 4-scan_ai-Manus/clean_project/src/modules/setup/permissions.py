"""
وحدة إدارة الصلاحيات
Permissions management module
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.modules.setup import models
from src.modules.setup.activity_integration import log_security_event
from src.modules.auth import service as auth_service
from src.modules.auth.models import User, Role, Permission

# إعداد التسجيل
logger = logging.getLogger(__name__)

# تعريف ثوابت الصلاحيات
PERM_SETUP_VIEW = "setup.view"
PERM_SETUP_MANAGE = "setup.manage"
PERM_SETUP_WELCOME_VIEW = "setup.welcome.view"
PERM_SETUP_SYSTEM_VIEW = "setup.system.view"
PERM_SETUP_DATABASE_VIEW = "setup.database.view"
PERM_SETUP_COMPANY_VIEW = "setup.company.view"
PERM_SETUP_BRANCH_VIEW = "setup.branch.view"
PERM_SETUP_USER_VIEW = "setup.user.view"
PERM_SETUP_MODULE_VIEW = "setup.module.view"
PERM_SETUP_AI_VIEW = "setup.ai.view"
PERM_SETUP_NOTIFICATION_VIEW = "setup.notification.view"
PERM_SETUP_SECURITY_VIEW = "setup.security.view"
PERM_SETUP_BACKUP_VIEW = "setup.backup.view"
PERM_SETUP_SUMMARY_VIEW = "setup.summary.view"
PERM_SETUP_USERS_UPDATE = "setup.users.update"

# Error messages
ERR_MODEL_SECTION_NOT_FOUND = "قسم النماذج غير موجود"
ERR_NO_USER_MANAGEMENT_PERMISSION = "ليس لديك صلاحية لإدارة المستخدمين"

# تعريف الصلاحيات
SETUP_PERMISSIONS = {
    # صلاحيات عامة
    "setup:view": "عرض معالج الإعداد",
    "setup:manage": "إدارة معالج الإعداد",
    "setup:complete": "إكمال عملية الإعداد",

    # صلاحيات الخطوات
    "setup:step:welcome:view": "عرض خطوة الترحيب",
    "setup:step:welcome:update": "تحديث خطوة الترحيب",

    "setup:step:system_settings:view": "عرض خطوة إعدادات النظام",
    "setup:step:system_settings:update": "تحديث خطوة إعدادات النظام",

    "setup:step:database_settings:view": "عرض خطوة إعدادات قاعدة البيانات",
    "setup:step:database_settings:update": "تحديث خطوة إعدادات قاعدة البيانات",

    "setup:step:company_settings:view": "عرض خطوة إعدادات الشركة",
    "setup:step:company_settings:update": "تحديث خطوة إعدادات الشركة",

    "setup:step:branch_settings:view": "عرض خطوة إعدادات الفروع",
    "setup:step:branch_settings:update": "تحديث خطوة إعدادات الفروع",

    "setup:step:user_settings:view": "عرض خطوة إعدادات المستخدمين",
    "setup:step:user_settings:update": "تحديث خطوة إعدادات المستخدمين",

    "setup:step:module_selection:view": "عرض خطوة اختيار المديولات",
    "setup:step:module_selection:update": "تحديث خطوة اختيار المديولات",

    "setup:step:ai_settings:view": "عرض خطوة إعدادات الذكاء الاصطناعي",
    "setup:step:ai_settings:update": "تحديث خطوة إعدادات الذكاء الاصطناعي",

    "setup:step:notification_settings:view": "عرض خطوة إعدادات الإشعارات",
    "setup:step:notification_settings:update": "تحديث خطوة إعدادات الإشعارات",

    "setup:step:security_settings:view": "عرض خطوة إعدادات الأمان",
    "setup:step:security_settings:update": "تحديث خطوة إعدادات الأمان",

    "setup:step:backup_import_export:view": "عرض خطوة إعدادات النسخ الاحتياطي والاستيراد/التصدير",
    "setup:step:backup_import_export:update": "تحديث خطوة إعدادات النسخ الاحتياطي والاستيراد/التصدير",

    "setup:step:summary:view": "عرض خطوة المراجعة والإكمال",
    "setup:step:summary:update": "تحديث خطوة المراجعة والإكمال",

    # صلاحيات الأمان
    "setup:security:view": "عرض إعدادات الأمان",
    "setup:security:manage": "إدارة إعدادات الأمان",
    "setup:security:logs:view": "عرض سجلات الأمان",

    # صلاحيات النسخ الاحتياطي
    "setup:backup:create": "إنشاء نسخة احتياطية",
    "setup:backup:restore": "استعادة نسخة احتياطية",
    "setup:backup:view": "عرض النسخ الاحتياطية",

    # صلاحيات الاستيراد/التصدير
    "setup:import:execute": "تنفيذ عملية استيراد",
    "setup:export:execute": "تنفيذ عملية تصدير",

    # صلاحيات إدارة المستخدمين
    "setup:users:create": "إنشاء مستخدمين",
    "setup:users:view": "عرض المستخدمين",
    "setup:users:update": "تحديث المستخدمين",
    "setup:users:delete": "حذف المستخدمين",

    # صلاحيات إدارة الأدوار
    "setup:roles:create": "إنشاء أدوار",
    "setup:roles:view": "عرض الأدوار",
    "setup:roles:update": "تحديث الأدوار",
    "setup:roles:delete": "حذف الأدوار",

    # صلاحيات إدارة الصلاحيات
    "setup:permissions:assign": "تعيين صلاحيات",
    "setup:permissions:view": "عرض الصلاحيات",
    "setup:permissions:revoke": "إلغاء صلاحيات"
}

# تعريف الأدوار الافتراضية
DEFAULT_ROLES = {
    "setup_admin": {
        "name": "مسؤول الإعداد",
        "description": "دور مسؤول الإعداد مع صلاحيات كاملة على معالج الإعداد",
        "permissions": list(SETUP_PERMISSIONS.keys())
    },
    "setup_user": {
        "name": "مستخدم الإعداد",
        "description": "دور مستخدم الإعداد مع صلاحيات محدودة على معالج الإعداد",
        "permissions": [
            "setup:view",
            "setup:step:welcome:view",
            "setup:step:system_settings:view",
            "setup:step:database_settings:view",
            "setup:step:company_settings:view",
            "setup:step:branch_settings:view",
            "setup:step:user_settings:view",
            "setup:step:module_selection:view",
            "setup:step:ai_settings:view",
            "setup:step:notification_settings:view",
            "setup:step:security_settings:view",
            "setup:step:backup_import_export:view",
            "setup:step:summary:view"
        ]
    }
}

# تعريف متطلبات الصلاحيات للعمليات
OPERATION_PERMISSIONS = {
    "initialize_setup": ["setup:manage"],
    "reset_setup": ["setup:manage"],
    "get_setup_status": ["setup:view"],
    "get_step_data": {
        "welcome": ["setup:step:welcome:view"],
        "system_settings": ["setup:step:system_settings:view"],
        "database_settings": ["setup:step:database_settings:view"],
        "company_settings": ["setup:step:company_settings:view"],
        "branch_settings": ["setup:step:branch_settings:view"],
        "user_settings": ["setup:step:user_settings:view"],
        "module_selection": ["setup:step:module_selection:view"],
        "ai_settings": ["setup:step:ai_settings:view"],
        "notification_settings": ["setup:step:notification_settings:view"],
        "security_settings": ["setup:step:security_settings:view", "setup:security:view"],
        "backup_import_export": ["setup:step:backup_import_export:view", "setup:backup:view"],
        "summary": ["setup:step:summary:view"]
    },
    "update_step_data": {
        "welcome": ["setup:step:welcome:update"],
        "system_settings": ["setup:step:system_settings:update"],
        "database_settings": ["setup:step:database_settings:update"],
        "company_settings": ["setup:step:company_settings:update"],
        "branch_settings": ["setup:step:branch_settings:update"],
        "user_settings": ["setup:step:user_settings:update", "setup:users:update"],
        "module_selection": ["setup:step:module_selection:update"],
        "ai_settings": ["setup:step:ai_settings:update"],
        "notification_settings": ["setup:step:notification_settings:update"],
        "security_settings": ["setup:step:security_settings:update", "setup:security:manage"],
        "backup_import_export": ["setup:step:backup_import_export:update", "setup:backup:view"],
        "summary": ["setup:step:summary:update"]
    },
    "next_step": ["setup:manage"],
    "previous_step": ["setup:manage"],
    "validate_step_data": {
        "welcome": ["setup:step:welcome:view"],
        "system_settings": ["setup:step:system_settings:view"],
        "database_settings": ["setup:step:database_settings:view"],
        "company_settings": ["setup:step:company_settings:view"],
        "branch_settings": ["setup:step:branch_settings:view"],
        "user_settings": ["setup:step:user_settings:view"],
        "module_selection": ["setup:step:module_selection:view"],
        "ai_settings": ["setup:step:ai_settings:view"],
        "notification_settings": ["setup:step:notification_settings:view"],
        "security_settings": ["setup:step:security_settings:view", "setup:security:view"],
        "backup_import_export": ["setup:step:backup_import_export:view", "setup:backup:view"],
        "summary": ["setup:step:summary:view"]
    },
    "complete_setup": ["setup:complete", "setup:manage"],
    "create_backup": ["setup:backup:create"],
    "restore_backup": ["setup:backup:restore"],
    "import_data": ["setup:import:execute"],
    "export_data": ["setup:export:execute"],
    "create_user": ["setup:users:create"],
    "update_user": ["setup:users:update"],
    "delete_user": ["setup:users:delete"],
    "create_role": ["setup:roles:create"],
    "update_role": ["setup:roles:update"],
    "delete_role": ["setup:roles:delete"],
    "assign_permission": ["setup:permissions:assign"],
    "revoke_permission": ["setup:permissions:revoke"],
    "view_security_logs": ["setup:security:logs:view"]
}


def initialize_setup_permissions(db: Session) -> None:
    """
    تهيئة صلاحيات معالج الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
    """
    # إنشاء الصلاحيات
    for permission_code, permission_description in SETUP_PERMISSIONS.items():
        # التحقق من وجود الصلاحية
        existing_permission = db.query(Permission).filter(Permission.code == permission_code).first()

        if not existing_permission:
            # إنشاء الصلاحية
            new_permission = Permission(
                code=permission_code,
                name=permission_description,
                description=permission_description,
                module="setup"
            )
            db.add(new_permission)

    # حفظ التغييرات
    db.commit()

    # إنشاء الأدوار الافتراضية
    for role_code, role_data in DEFAULT_ROLES.items():
        # التحقق من وجود الدور
        existing_role = db.query(Role).filter(Role.code == role_code).first()

        if not existing_role:
            # إنشاء الدور
            new_role = Role(
                code=role_code,
                name=role_data["name"],
                description=role_data["description"]
            )
            db.add(new_role)
            db.commit()

            # تعيين الصلاحيات للدور
            for permission_code in role_data["permissions"]:
                permission = db.query(Permission).filter(Permission.code == permission_code).first()
                if permission:
                    auth_service.assign_permission_to_role(db, new_role.id, permission.id)
        else:
            # تحديث الصلاحيات للدور
            existing_permissions = auth_service.get_role_permissions(db, existing_role.id)
            existing_permission_codes = [p.code for p in existing_permissions]

            # إضافة الصلاحيات الجديدة
            for permission_code in role_data["permissions"]:
                if permission_code not in existing_permission_codes:
                    permission = db.query(Permission).filter(Permission.code == permission_code).first()
                    if permission:
                        auth_service.assign_permission_to_role(db, existing_role.id, permission.id)


def check_setup_permission(
    db: Session,
    user_id: int,
    permission_code: str,
    step_id: Optional[str] = None
) -> bool:
    """
    التحقق من صلاحية معالج الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
        user_id (int): معرف المستخدم
        permission_code (str): رمز الصلاحية
        step_id (Optional[str]): معرف الخطوة

    Returns:
        bool: ما إذا كان المستخدم يملك الصلاحية
    """
    # التحقق من وجود المستخدم
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    # التحقق من صلاحية المستخدم
    if user.is_superuser:
        return True

    # تحديد الصلاحيات المطلوبة
    required_permissions = []

    if step_id and permission_code in OPERATION_PERMISSIONS:
        # التحقق من صلاحيات العملية للخطوة
        step_permissions = OPERATION_PERMISSIONS[permission_code]
        if isinstance(step_permissions, dict) and step_id in step_permissions:
            required_permissions = step_permissions[step_id]
        else:
            required_permissions = step_permissions if isinstance(step_permissions, list) else [step_permissions]
    elif permission_code in OPERATION_PERMISSIONS:
        # التحقق من صلاحيات العملية
        required_permissions = OPERATION_PERMISSIONS[permission_code]
        if not isinstance(required_permissions, list):
            required_permissions = [required_permissions]
    else:
        # التحقق من الصلاحية المباشرة
        required_permissions = [permission_code]

    # التحقق من امتلاك المستخدم لأي من الصلاحيات المطلوبة
    for required_permission in required_permissions:
        if auth_service.check_user_permission(db, user_id, required_permission):
            return True

    return False


def check_setup_token_permission(
    db: Session,
    token: str,
    permission_code: str,
    step_id: Optional[str] = None,
    ip_address: Optional[str] = None
) -> bool:
    """
    التحقق من صلاحية رمز الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
        token (str): رمز الإعداد
        permission_code (str): رمز الصلاحية
        step_id (Optional[str]): معرف الخطوة
        ip_address (Optional[str]): عنوان IP

    Returns:
        bool: ما إذا كان الرمز يملك الصلاحية
    """
    # التحقق من وجود حالة الإعداد
    setup_status = db.query(models.SetupStatus).first()
    if not setup_status:
        return False

    # التحقق من صحة الرمز
    if setup_status.setup_token != token:
        log_token_validation_error(db, "محاولة استخدام رمز إعداد غير صالح", permission_code, step_id, ip_address)
        return False

    # التحقق من انتهاء صلاحية الرمز
    if setup_status.token_expires_at < datetime.now(timezone.utc):
        log_token_validation_error(
            db,
            "محاولة استخدام رمز إعداد منتهي الصلاحية",
            permission_code,
            step_id,
            ip_address,
            expired_at=setup_status.token_expires_at.isoformat()
        )
        return False

    # رمز الإعداد صالح، منح جميع الصلاحيات
    return True


def log_token_validation_error(
    db: Session,
    description: str,
    permission_code: str,
    step_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    expired_at: Optional[str] = None
) -> None:
    """تسجيل خطأ التحقق من الرمز"""
    data = {
        "token": "********",  # لا نخزن الرمز الفعلي في السجل
        "permission_code": permission_code,
        "step_id": step_id
    }
    if expired_at:
        data["expired_at"] = expired_at

    log_security_event(
        db=db,
        event_type="token_validation_error",
        description=description,
        data=data,
        ip_address=ip_address
    )


def get_required_permissions_for_operation(
    operation: str,
    step_id: Optional[str] = None
) -> List[str]:
    """
    الحصول على الصلاحيات المطلوبة للعملية

    Args:
        operation (str): العملية
        step_id (Optional[str]): معرف الخطوة

    Returns:
        List[str]: الصلاحيات المطلوبة
    """
    # تحديد الصلاحيات المطلوبة
    required_permissions = []

    if operation in OPERATION_PERMISSIONS:
        # التحقق من صلاحيات العملية للخطوة
        if step_id and isinstance(OPERATION_PERMISSIONS[operation], dict) and step_id in OPERATION_PERMISSIONS[operation]:
            required_permissions = OPERATION_PERMISSIONS[operation][step_id]
        else:
            required_permissions = OPERATION_PERMISSIONS[operation]
            if not isinstance(required_permissions, list):
                required_permissions = [required_permissions]

    return required_permissions


def validate_operation_permission(
    db: Session,
    user_id: Optional[int],
    token: Optional[str],
    operation: str,
    step_id: Optional[str] = None,
    ip_address: Optional[str] = None
) -> Dict[str, Any]:
    """
    التحقق من صلاحية العملية

    Args:
        db (Session): جلسة قاعدة البيانات
        user_id (Optional[int]): معرف المستخدم
        token (Optional[str]): رمز الإعداد
        operation (str): العملية
        step_id (Optional[str]): معرف الخطوة
        ip_address (Optional[str]): عنوان IP

    Returns:
        Dict[str, Any]: نتيجة التحقق
    """
    # تحديد الصلاحيات المطلوبة
    required_permissions = get_required_permissions_for_operation(operation, step_id)

    # التحقق من وجود صلاحيات مطلوبة
    if not required_permissions:
        return {
            "is_allowed": False,
            "message": f"لا توجد صلاحيات محددة للعملية {operation}"
        }

    # التحقق من صلاحية المستخدم
    if user_id:
        return validate_user_permission(db, user_id, operation, step_id, required_permissions, ip_address)

    # التحقق من صلاحية رمز الإعداد
    if token:
        return validate_token_permission(db, token, operation, step_id, ip_address)

    # لا يوجد مستخدم أو رمز
    return {
        "is_allowed": False,
        "message": "يجب توفير معرف المستخدم أو رمز الإعداد"
    }


def validate_user_permission(
    db: Session,
    user_id: int,
    operation: str,
    step_id: Optional[str],
    required_permissions: List[str],
    ip_address: Optional[str]
) -> Dict[str, Any]:
    """التحقق من صلاحية المستخدم"""
    # التحقق من امتلاك المستخدم لأي من الصلاحيات المطلوبة
    for required_permission in required_permissions:
        if auth_service.check_user_permission(db, user_id, required_permission):
            return {
                "is_allowed": True,
                "message": "تم التحقق من الصلاحية بنجاح"
            }

    # تسجيل محاولة الوصول غير المصرح بها
    log_security_event(
        db=db,
        event_type="permission_error",
        description=f"محاولة تنفيذ عملية {operation} بدون صلاحية",
        data={
            "user_id": user_id,
            "operation": operation,
            "step_id": step_id,
            "required_permissions": required_permissions
        },
        user_id=user_id,
        ip_address=ip_address
    )

    return {
        "is_allowed": False,
        "message": "ليس لديك الصلاحية اللازمة لتنفيذ هذه العملية",
        "required_permissions": required_permissions
    }


def validate_token_permission(
    db: Session,
    token: str,
    operation: str,
    step_id: Optional[str],
    ip_address: Optional[str]
) -> Dict[str, Any]:
    """التحقق من صلاحية الرمز"""
    if check_setup_token_permission(db, token, operation, step_id, ip_address):
        return {
            "is_allowed": True,
            "message": "تم التحقق من صلاحية الرمز بنجاح"
        }

    return {
        "is_allowed": False,
        "message": "رمز الإعداد غير صالح أو منتهي الصلاحية"
    }


def assign_setup_admin_role(db: Session, user_id: int) -> bool:
    """
    تعيين دور مسؤول الإعداد للمستخدم

    Args:
        db (Session): جلسة قاعدة البيانات
        user_id (int): معرف المستخدم

    Returns:
        bool: نجاح العملية
    """
    # التحقق من وجود المستخدم
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    # البحث عن دور مسؤول الإعداد
    setup_admin_role = db.query(Role).filter(Role.code == "setup_admin").first()
    if not setup_admin_role:
        # تهيئة صلاحيات معالج الإعداد
        initialize_setup_permissions(db)

        # البحث عن دور مسؤول الإعداد مرة أخرى
        setup_admin_role = db.query(Role).filter(Role.code == "setup_admin").first()
        if not setup_admin_role:
            return False

    # تعيين الدور للمستخدم
    auth_service.assign_role_to_user(db, user_id, setup_admin_role.id)

    return True


def get_user_setup_permissions(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """
    الحصول على صلاحيات معالج الإعداد للمستخدم

    Args:
        db (Session): جلسة قاعدة البيانات
        user_id (int): معرف المستخدم

    Returns:
        List[Dict[str, Any]]: صلاحيات المستخدم
    """
    # التحقق من وجود المستخدم
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []

    # الحصول على صلاحيات المستخدم
    user_permissions = auth_service.get_user_permissions(db, user_id)

    # تصفية صلاحيات معالج الإعداد
    setup_permissions = []
    for permission in user_permissions:
        if permission.code.startswith("setup:"):
            setup_permissions.append({
                "code": permission.code,
                "name": permission.name,
                "description": permission.description
            })

    return setup_permissions


def get_user_setup_roles(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """
    الحصول على أدوار معالج الإعداد للمستخدم

    Args:
        db (Session): جلسة قاعدة البيانات
        user_id (int): معرف المستخدم

    Returns:
        List[Dict[str, Any]]: أدوار المستخدم
    """
    # التحقق من وجود المستخدم
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []

    # الحصول على أدوار المستخدم
    user_roles = auth_service.get_user_roles(db, user_id)

    # تصفية أدوار معالج الإعداد
    setup_roles = []
    for role in user_roles:
        if role.code in DEFAULT_ROLES:
            setup_roles.append({
                "code": role.code,
                "name": role.name,
                "description": role.description
            })

    return setup_roles


def create_initial_admin_user(
    db: Session,
    username: str,
    password: str,
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> Optional[User]:
    """
    إنشاء مستخدم مسؤول أولي

    Args:
        db (Session): جلسة قاعدة البيانات
        username (str): اسم المستخدم
        password (str): كلمة المرور
        email (str): البريد الإلكتروني
        first_name (Optional[str]): الاسم الأول
        last_name (Optional[str]): الاسم الأخير

    Returns:
        Optional[User]: المستخدم المنشأ
    """
    # التحقق من وجود مستخدم بنفس اسم المستخدم أو البريد الإلكتروني
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return None

    # إنشاء المستخدم
    user = auth_service.create_user(
        db=db,
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
        is_superuser=True
    )

    # تعيين دور مسؤول الإعداد للمستخدم
    assign_setup_admin_role(db, user.id)

    return user
