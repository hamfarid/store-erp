"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/service.py
الوصف: خدمات مديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.modules.ai import service as ai_service
from src.modules.auth import service as auth_service
from src.modules.backup import service as backup_service
from src.modules.company import service as company_service
from src.modules.module_manager import service as module_service
from src.modules.notification import service as notification_service
from src.modules.security import service as security_service
from src.modules.setup import models, schemas
from src.modules.setup.utils import (
    validate_database_connection,
    validate_email_settings,
)
from src.modules.system_settings import service as system_settings_service

# إعداد التسجيل
logger = logging.getLogger(__name__)

# تعريف خطوات الإعداد
SETUP_STEPS = [
    "welcome",
    "system_settings",
    "database_settings",
    "company_settings",
    "user_settings",
    "module_selection",
    "ai_settings",
    "notification_settings",
    "backup_settings",
    "security_settings",
    "summary",
]

# الخطوات الإلزامية
REQUIRED_STEPS = [
    "system_settings",
    "database_settings",
    "company_settings",
    "user_settings",
    "security_settings",
]


def get_setup_status(db: Session) -> schemas.SetupStatusResponse:
    """
    الحصول على حالة الإعداد الحالية

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد الحالية
    """
    # البحث عن حالة الإعداد في قاعدة البيانات
    setup_status = db.query(models.SetupStatus).first()

    # إذا لم تكن موجودة، إنشاء حالة جديدة
    if not setup_status:
        setup_status = models.SetupStatus(
            is_completed=False, current_step=SETUP_STEPS[0], completed_steps=[]
        )
        db.add(setup_status)
        db.commit()
        db.refresh(setup_status)

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at,
    )


def initialize_setup(db: Session) -> schemas.SetupStatusResponse:
    """
    تهيئة عملية الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد التهيئة
    """
    # البحث عن حالة الإعداد في قاعدة البيانات
    setup_status = db.query(models.SetupStatus).first()

    # إذا كانت موجودة، إعادة تعيينها
    if setup_status:
        setup_status.is_completed = False
        setup_status.current_step = SETUP_STEPS[0]
        setup_status.completed_steps = []
        setup_status.setup_token = secrets.token_urlsafe(32)
        setup_status.token_expires_at = datetime.now(
            timezone.utc) + timedelta(hours=24)
    else:
        # إنشاء حالة جديدة
        setup_status = models.SetupStatus(
            is_completed=False,
            current_step=SETUP_STEPS[0],
            completed_steps=[],
            setup_token=secrets.token_urlsafe(32),
            token_expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
        )
        db.add(setup_status)

    # حفظ التغييرات
    db.commit()
    db.refresh(setup_status)

    # تسجيل نشاط الإعداد
    log_setup_activity(db, "initialize", "info", "تم تهيئة عملية الإعداد")

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at,
    )


def _get_welcome_data() -> Dict[str, Any]:
    """بيانات خطوة الترحيب"""
    return {
        "welcome_message": "مرحباً بك في معالج إعداد نظام Scan AI",
        "version": "3.0.0",
        "release_date": "2025-05-29",
    }


def _get_system_settings_data(db: Session) -> Dict[str, Any]:
    """بيانات إعدادات النظام"""
    system_settings = system_settings_service.get_system_settings(db)
    return {
        "app_name": system_settings.get("app_name", "نظام Scan AI"),
        "language": system_settings.get("language", "ar"),
        "timezone": system_settings.get("timezone", "Africa/Cairo"),
        "date_format": system_settings.get("date_format", "YYYY-MM-DD"),
        "time_format": system_settings.get("time_format", "HH:mm:ss"),
        "theme": system_settings.get("theme", "light"),
        "debug_mode": system_settings.get("debug_mode", False),
    }


def _get_database_settings_data(db: Session) -> Dict[str, Any]:
    """بيانات إعدادات قاعدة البيانات"""
    db_settings = system_settings_service.get_database_settings(db)
    return {
        "db_type": db_settings.get("db_type", "postgresql"),
        "db_host": db_settings.get("db_host", "localhost"),
        "db_port": db_settings.get("db_port", 5432),
        "db_name": db_settings.get("db_name", "scan_ai_db"),
        "db_user": db_settings.get("db_user", "postgres"),
        "db_password": "",
        "connection_pool_size": db_settings.get("connection_pool_size", 10),
        "connection_timeout": db_settings.get("connection_timeout", 30),
    }


def get_step_data(db: Session, step_id: str) -> schemas.StepDataResponse:
    """
    الحصول على بيانات خطوة معينة

    Args:
        db (Session): جلسة قاعدة البيانات
        step_id (str): معرف الخطوة

    Returns:
        schemas.StepDataResponse: بيانات الخطوة
    """
    # التحقق من صحة معرف الخطوة
    if step_id not in SETUP_STEPS:
        return None

    # الحصول على البيانات حسب نوع الخطوة
    data = {}

    if step_id == "welcome":
        # بيانات خطوة الترحيب
        data = {
            "welcome_message": "مرحباً بك في معالج إعداد نظام Scan AI",
            "version": "3.0.0",
            "release_date": "2025-05-29",
        }

    elif step_id == "system_settings":
        # بيانات إعدادات النظام
        system_settings = system_settings_service.get_system_settings(db)
        data = {
            "app_name": system_settings.get("app_name", "نظام Scan AI"),
            "language": system_settings.get("language", "ar"),
            "timezone": system_settings.get("timezone", "Africa/Cairo"),
            "date_format": system_settings.get("date_format", "YYYY-MM-DD"),
            "time_format": system_settings.get("time_format", "HH:mm:ss"),
            "theme": system_settings.get("theme", "light"),
            "debug_mode": system_settings.get("debug_mode", False),
        }

    elif step_id == "database_settings":
        # بيانات إعدادات قاعدة البيانات
        db_settings = system_settings_service.get_database_settings(db)
        data = {
            "db_type": db_settings.get("db_type", "postgresql"),
            "db_host": db_settings.get("db_host", "localhost"),
            "db_port": db_settings.get("db_port", 5432),
            "db_name": db_settings.get("db_name", "scan_ai_db"),
            "db_user": db_settings.get("db_user", "postgres"),
            "db_password": "",  # لا نعيد كلمة المرور لأسباب أمنية
            "connection_pool_size": db_settings.get("connection_pool_size", 10),
            "connection_timeout": db_settings.get("connection_timeout", 30),
        }

    elif step_id == "company_settings":
        # بيانات إعدادات الشركة
        company = db.query(models.Company).first()
        if company:
            data = {
                "name": company.name,
                "legal_name": company.legal_name,
                "tax_number": company.tax_number,
                "registration_number": company.registration_number,
                "address": company.address,
                "city": company.city,
                "country_code": company.country_code,
                "phone": company.phone,
                "email": company.email,
                "website": company.website,
                "logo_path": company.logo_path,
                "currency_code": company.currency_code,
                "timezone": company.timezone,
                "locale": company.locale,
                "fiscal_year_start": company.fiscal_year_start,
            }
        else:
            data = {
                "name": "",
                "legal_name": "",
                "tax_number": "",
                "registration_number": "",
                "address": "",
                "city": "",
                "country_code": "SA",
                "phone": "",
                "email": "",
                "website": "",
                "logo_path": "",
                "currency_code": "SAR",
                "timezone": "Africa/Cairo",
                "locale": "ar-SA",
                "fiscal_year_start": "01-01",
            }

    elif step_id == "user_settings":
        # بيانات إعدادات المستخدم المسؤول
        admin_settings = auth_service.get_admin_settings(db)
        data = {
            "admin_username": admin_settings.get("admin_username", "admin"),
            "admin_email": admin_settings.get("admin_email", ""),
            "admin_password": "",  # لا نعيد كلمة المرور لأسباب أمنية
            "password_policy": admin_settings.get(
                "password_policy",
                {
                    "min_length": 8,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_special_chars": True,
                },
            ),
        }

    elif step_id == "module_selection":
        # بيانات اختيار المديولات
        modules = module_service.get_all_modules(db)
        data = {
            "available_modules": [
                {
                    "id": module.id,
                    "name": module.name,
                    "description": module.description,
                    "is_core": module.is_core,
                    "is_enabled": module.is_enabled,
                    "dependencies": module.dependencies,
                }
                for module in modules
            ]
        }

    elif step_id == "ai_settings":
        # بيانات إعدادات الذكاء الاصطناعي
        ai_settings = ai_service.get_ai_settings(db)
        data = {
            "central_ai": ai_settings.get(
                "central_ai",
                {
                    "enabled": True,
                    "model_type": "local",
                    "api_key": "",
                    "max_tokens": 2000,
                    "temperature": 0.7,
                    "request_timeout": 60,
                },
            ),
            "agents": ai_settings.get(
                "agents",
                {
                    "max_agents": 10,
                    "default_permissions": ["read", "analyze"],
                    "memory_enabled": True,
                    "memory_retention_days": 30,
                },
            ),
            "vector_db": ai_settings.get(
                "vector_db",
                {
                    "enabled": True,
                    "db_type": "milvus",
                    "host": "localhost",
                    "port": 19530,
                },
            ),
        }

    elif step_id == "notification_settings":
        # بيانات إعدادات الإشعارات
        notification_settings = notification_service.get_notification_settings(
            db)
        data = {
            "email": notification_settings.get(
                "email",
                {
                    "enabled": False,
                    "smtp_server": "",
                    "smtp_port": 587,
                    "smtp_user": "",
                    "smtp_password": "",
                    "from_email": "",
                    "use_tls": True,
                },
            ),
            "sms": notification_settings.get(
                "sms", {"enabled": False, "provider": "", "api_key": ""}
            ),
            "in_app": notification_settings.get(
                "in_app",
                {"enabled": True, "max_notifications": 100, "retention_days": 30},
            ),
        }

    elif step_id == "backup_settings":
        # بيانات إعدادات النسخ الاحتياطي
        backup_settings = backup_service.get_backup_settings(db)
        data = {
            "auto_backup": backup_settings.get(
                "auto_backup",
                {
                    "enabled": True,
                    "frequency": "daily",
                    "time": "02:00",
                    "retention_count": 7,
                },
            ),
            "backup_path": backup_settings.get("backup_path", "backups/"),
            "include_uploads": backup_settings.get("include_uploads", True),
            "include_logs": backup_settings.get("include_logs", False),
            "compress": backup_settings.get("compress", True),
        }

    elif step_id == "security_settings":
        # بيانات إعدادات الأمان
        security_settings = security_service.get_security_settings(db)
        data = {
            "use_ssl": security_settings.get("use_ssl", True),
            "ssl_cert_path": security_settings.get("ssl_cert_path", ""),
            "ssl_key_path": security_settings.get("ssl_key_path", ""),
            # بالدقائق
            "session_timeout": security_settings.get("session_timeout", 30),
            "max_login_attempts": security_settings.get("max_login_attempts", 5),
            "lockout_duration": security_settings.get(
                "lockout_duration", 15
            ),  # بالدقائق
            "password_expiry_days": security_settings.get("password_expiry_days", 90),
            "enable_2fa": security_settings.get("enable_2fa", False),
            "allowed_ips": security_settings.get("allowed_ips", []),
            "cors_origins": security_settings.get("cors_origins", ["*"]),
            "xss_protection": security_settings.get("xss_protection", True),
            "csrf_protection": security_settings.get("csrf_protection", True),
            "sql_injection_protection": security_settings.get(
                "sql_injection_protection", True
            ),
            "rate_limiting": security_settings.get(
                "rate_limiting", {"enabled": True, "requests_per_minute": 60}
            ),
        }

    elif step_id == "summary":
        # بيانات ملخص الإعداد
        setup_status = db.query(models.SetupStatus).first()
        data = {
            "completed_steps": setup_status.completed_steps if setup_status else [],
            "is_ready_to_complete": len(
                setup_status.completed_steps if setup_status else []
            )
            >= len(REQUIRED_STEPS),
            "missing_steps": [
                step
                for step in REQUIRED_STEPS
                if step not in (setup_status.completed_steps if setup_status else [])
            ],
        }

    # إنشاء الاستجابة
    return schemas.StepDataResponse(step_id=step_id, data=data)


def validate_step_data(
    db: Session, step_id: str, data: Dict[str, Any]
) -> schemas.ValidationResult:
    """
    التحقق من صحة بيانات الخطوة

    Args:
        db (Session): جلسة قاعدة البيانات
        step_id (str): معرف الخطوة
        data (Dict[str, Any]): بيانات الخطوة

    Returns:
        schemas.ValidationResult: نتيجة التحقق
    """
    errors = []

    # التحقق من صحة البيانات حسب نوع الخطوة
    if step_id == "system_settings":
        if "app_name" in data and not data["app_name"]:
            errors.append("اسم التطبيق مطلوب")
        if "language" in data and data["language"] not in ["ar", "en"]:
            errors.append("اللغة غير مدعومة")

    elif step_id == "database_settings":
        if "db_type" in data and data["db_type"] not in [
            "postgresql",
            "mysql",
            "sqlite",
        ]:
            errors.append("نوع قاعدة البيانات غير مدعوم")
        if "db_host" in data and not data["db_host"]:
            errors.append("اسم المضيف مطلوب")
        if "db_name" in data and not data["db_name"]:
            errors.append("اسم قاعدة البيانات مطلوب")

    elif step_id == "company_settings":
        if "name" in data and not data["name"]:
            errors.append("اسم الشركة مطلوب")
        if "country_code" in data and not data["country_code"]:
            errors.append("رمز الدولة مطلوب")
        if "currency_code" in data and not data["currency_code"]:
            errors.append("رمز العملة مطلوب")

    elif step_id == "user_settings":
        if "admin_username" in data and not data["admin_username"]:
            errors.append("اسم المستخدم المسؤول مطلوب")
        if "admin_email" in data and not data["admin_email"]:
            errors.append("البريد الإلكتروني للمسؤول مطلوب")
        if "admin_password" in data:
            password = data["admin_password"]
            if not password:
                errors.append("كلمة مرور المسؤول مطلوبة")
            elif len(password) < 8:
                errors.append("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
            elif "password_policy" in data:
                policy = data["password_policy"]
                if policy.get("require_uppercase", True) and not any(
                    c.isupper() for c in password
                ):
                    errors.append(
                        "كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل"
                    )
                if policy.get("require_lowercase", True) and not any(
                    c.islower() for c in password
                ):
                    errors.append(
                        "كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل"
                    )
                if policy.get("require_numbers", True) and not any(
                    c.isdigit() for c in password
                ):
                    errors.append(
                        "كلمة المرور يجب أن تحتوي على رقم واحد على الأقل")
                if policy.get("require_special_chars", True) and not any(
                    not c.isalnum() for c in password
                ):
                    errors.append(
                        "كلمة المرور يجب أن تحتوي على حرف خاص واحد على الأقل")

    elif step_id == "ai_settings":
        if "central_ai" in data and "model_type" in data["central_ai"]:
            if data["central_ai"]["model_type"] not in ["local", "cloud"]:
                errors.append("نوع نموذج الذكاء الاصطناعي غير مدعوم")
            if data["central_ai"]["model_type"] == "cloud" and not data[
                "central_ai"
            ].get("api_key"):
                errors.append(
                    "مفتاح API مطلوب لنموذج الذكاء الاصطناعي السحابي")

    elif step_id == "notification_settings":
        if "email" in data and data["email"].get("enabled", False):
            if not data["email"].get("smtp_server"):
                errors.append(
                    "خادم SMTP مطلوب عند تفعيل الإشعارات عبر البريد الإلكتروني"
                )
            if not data["email"].get("smtp_user"):
                errors.append(
                    "اسم مستخدم SMTP مطلوب عند تفعيل الإشعارات عبر البريد الإلكتروني"
                )
            if not data["email"].get("smtp_password"):
                errors.append(
                    "كلمة مرور SMTP مطلوبة عند تفعيل الإشعارات عبر البريد الإلكتروني"
                )
            if not data["email"].get("from_email"):
                errors.append(
                    "عنوان البريد الإلكتروني المرسل مطلوب عند تفعيل الإشعارات عبر البريد الإلكتروني"
                )

    elif step_id == "security_settings":
        if "use_ssl" in data and data["use_ssl"]:
            if not data.get("ssl_cert_path"):
                errors.append("مسار شهادة SSL مطلوب عند تفعيل SSL")
            if not data.get("ssl_key_path"):
                errors.append("مسار مفتاح SSL مطلوب عند تفعيل SSL")

    # إنشاء نتيجة التحقق
    return schemas.ValidationResult(is_valid=len(errors) == 0, errors=errors)


def update_step_data(
    db: Session, step_id: str, data: Dict[str, Any]
) -> schemas.StepUpdateResponse:
    """
    تحديث بيانات خطوة معينة

    Args:
        db (Session): جلسة قاعدة البيانات
        step_id (str): معرف الخطوة
        data (Dict[str, Any]): بيانات الخطوة الجديدة

    Returns:
        schemas.StepUpdateResponse: نتيجة تحديث الخطوة
    """
    # التحقق من صحة معرف الخطوة
    if step_id not in SETUP_STEPS:
        return schemas.StepUpdateResponse(
            success=False, message=f"معرف الخطوة غير صالح: {step_id}"
        )

    # تحديث البيانات حسب نوع الخطوة
    try:
        if step_id == "system_settings":
            system_settings_service.update_system_settings(db, data)

        elif step_id == "database_settings":
            system_settings_service.update_database_settings(db, data)

        elif step_id == "company_settings":
            company = db.query(models.Company).first()
            if company:
                for key, value in data.items():
                    if hasattr(company, key):
                        setattr(company, key, value)
                db.commit()
                db.refresh(company)
            else:
                company = models.Company(**data)
                db.add(company)
                db.commit()
                db.refresh(company)

        elif step_id == "user_settings":
            auth_service.update_admin_settings(db, data)

        elif step_id == "module_selection":
            if "available_modules" in data:
                for module_data in data["available_modules"]:
                    module_service.update_module_status(
                        db, module_data["id"], module_data["is_enabled"]
                    )

        elif step_id == "ai_settings":
            ai_service.update_ai_settings(db, data)

        elif step_id == "notification_settings":
            notification_service.update_notification_settings(db, data)

        elif step_id == "backup_settings":
            backup_service.update_backup_settings(db, data)

        elif step_id == "security_settings":
            security_service.update_security_settings(db, data)

        # تحديث حالة الإعداد
        setup_status = db.query(models.SetupStatus).first()
        if setup_status:
            if step_id not in setup_status.completed_steps:
                setup_status.completed_steps.append(step_id)
            db.commit()
            db.refresh(setup_status)

        # تسجيل نشاط الإعداد
        log_setup_activity(
            db,
            step_id,
            "info",
            f"تم تحديث بيانات الخطوة {step_id}")

        return schemas.StepUpdateResponse(
            success=True, message=f"تم تحديث بيانات الخطوة {step_id} بنجاح"
        )

    except Exception as e:
        # تسجيل الخطأ
        log_setup_activity(
            db,
            step_id,
            "error",
            f"فشل في تحديث بيانات الخطوة {step_id}",
            {"error": str(e)},
        )

        return schemas.StepUpdateResponse(
            success=False, message=f"فشل في تحديث بيانات الخطوة {step_id}: {str(e)}")


def next_step(db: Session) -> schemas.SetupStatusResponse:
    """
    الانتقال إلى الخطوة التالية

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد الانتقال
    """
    # الحصول على حالة الإعداد
    setup_status = db.query(models.SetupStatus).first()
    if not setup_status:
        setup_status = models.SetupStatus(
            is_completed=False, current_step=SETUP_STEPS[0], completed_steps=[]
        )
        db.add(setup_status)
        db.commit()
        db.refresh(setup_status)

    # الحصول على الخطوة الحالية والتالية
    current_index = (
        SETUP_STEPS.index(setup_status.current_step)
        if setup_status.current_step in SETUP_STEPS
        else 0
    )
    next_index = min(current_index + 1, len(SETUP_STEPS) - 1)
    next_step_id = SETUP_STEPS[next_index]

    # تحديث الخطوة الحالية
    setup_status.current_step = next_step_id
    db.commit()
    db.refresh(setup_status)

    # تسجيل نشاط الإعداد
    log_setup_activity(
        db, next_step_id, "info", f"تم الانتقال إلى الخطوة {next_step_id}"
    )

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at,
    )


def previous_step(db: Session) -> schemas.SetupStatusResponse:
    """
    العودة إلى الخطوة السابقة

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد العودة
    """
    # الحصول على حالة الإعداد
    setup_status = db.query(models.SetupStatus).first()
    if not setup_status:
        setup_status = models.SetupStatus(
            is_completed=False, current_step=SETUP_STEPS[0], completed_steps=[]
        )
        db.add(setup_status)
        db.commit()
        db.refresh(setup_status)

    # الحصول على الخطوة الحالية والسابقة
    current_index = (
        SETUP_STEPS.index(setup_status.current_step)
        if setup_status.current_step in SETUP_STEPS
        else 0
    )
    prev_index = max(current_index - 1, 0)
    prev_step_id = SETUP_STEPS[prev_index]

    # تحديث الخطوة الحالية
    setup_status.current_step = prev_step_id
    db.commit()
    db.refresh(setup_status)

    # تسجيل نشاط الإعداد
    log_setup_activity(
        db,
        prev_step_id,
        "info",
        f"تم العودة إلى الخطوة {prev_step_id}")

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at,
    )


def validate_setup_completion(db: Session) -> schemas.ValidationResult:
    """
    التحقق من اكتمال جميع الخطوات الإلزامية

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.ValidationResult: نتيجة التحقق
    """
    # الحصول على حالة الإعداد
    setup_status = db.query(models.SetupStatus).first()
    if not setup_status:
        return schemas.ValidationResult(
            is_valid=False, errors=["لم يتم العثور على حالة الإعداد"]
        )

    # التحقق من اكتمال جميع الخطوات الإلزامية
    missing_steps = [
        step for step in REQUIRED_STEPS if step not in setup_status.completed_steps]

    # إنشاء نتيجة التحقق
    return schemas.ValidationResult(
        is_valid=len(missing_steps) == 0,
        errors=[f"الخطوة {step} غير مكتملة" for step in missing_steps]
        if missing_steps
        else [],
    )


def complete_setup(db: Session) -> schemas.SetupCompletionResponse:
    """
    إكمال عملية الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupCompletionResponse: نتيجة إكمال الإعداد
    """
    # الحصول على حالة الإعداد
    setup_status = db.query(models.SetupStatus).first()
    if not setup_status:
        return schemas.SetupCompletionResponse(
            success=False, message="لم يتم العثور على حالة الإعداد"
        )

    try:
        # تحديث حالة الإعداد
        setup_status.is_completed = True
        setup_status.current_step = SETUP_STEPS[-1]  # الخطوة الأخيرة
        db.commit()
        db.refresh(setup_status)

        # تنفيذ الإجراءات اللازمة بعد الإعداد
        _post_setup_actions(db)

        # تسجيل نشاط الإعداد
        log_setup_activity(
            db,
            "complete",
            "info",
            "تم إكمال عملية الإعداد بنجاح")

        return schemas.SetupCompletionResponse(
            success=True, message="تم إكمال عملية الإعداد بنجاح"
        )

    except Exception as e:
        # تسجيل الخطأ
        log_setup_activity(
            db, "complete", "error", "فشل في إكمال عملية الإعداد", {
                "error": str(e)})

        return schemas.SetupCompletionResponse(
            success=False, message=f"فشل في إكمال عملية الإعداد: {str(e)}"
        )


def _post_setup_actions(db: Session) -> None:
    """
    تنفيذ الإجراءات اللازمة بعد إكمال الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
    """
    # تهيئة المديولات المفعلة
    modules = module_service.get_enabled_modules(db)
    for module in modules:
        try:
            # استدعاء دالة التهيئة للمديول إذا كانت موجودة
            module_service.initialize_module(db, module.id)
            log_setup_activity(
                db,
                "initialize_module",
                "info",
                f"تم تهيئة المديول {module.name}")
        except Exception as e:
            log_setup_activity(
                db,
                "initialize_module",
                "error",
                f"فشل في تهيئة المديول {module.name}",
                {"error": str(e)},
            )

    # إنشاء نسخة احتياطية أولية
    try:
        backup_service.create_backup(
            db, "initial_setup", "نسخة احتياطية بعد الإعداد الأولي"
        )
        log_setup_activity(db, "initial_backup", "info",
                           "تم إنشاء نسخة احتياطية أولية")
    except Exception as e:
        log_setup_activity(
            db,
            "initial_backup",
            "error",
            "فشل في إنشاء نسخة احتياطية أولية",
            {"error": str(e)},
        )


def test_database_connection(
    connection_data: schemas.DatabaseConnectionTest,
) -> schemas.DatabaseConnectionTestResponse:
    """
    اختبار اتصال قاعدة البيانات

    Args:
        connection_data (schemas.DatabaseConnectionTest): بيانات الاتصال

    Returns:
        schemas.DatabaseConnectionTestResponse: نتيجة اختبار الاتصال
    """
    try:
        # اختبار الاتصال
        result = validate_database_connection(
            db_type=connection_data.db_type,
            host=connection_data.host,
            port=connection_data.port,
            name=connection_data.name,
            user=connection_data.user,
            password=connection_data.password,
        )

        if result["success"]:
            return schemas.DatabaseConnectionTestResponse(
                success=True, message="تم الاتصال بقاعدة البيانات بنجاح"
            )
        else:
            return schemas.DatabaseConnectionTestResponse(
                success=False, message=f"فشل الاتصال بقاعدة البيانات: {result['error']}")

    except Exception as e:
        return schemas.DatabaseConnectionTestResponse(
            success=False, message=f"فشل الاتصال بقاعدة البيانات: {str(e)}"
        )


def test_email_settings(
    email_settings: schemas.EmailSettingsTest,
) -> schemas.EmailSettingsTestResponse:
    """
    اختبار إعدادات البريد الإلكتروني

    Args:
        email_settings (schemas.EmailSettingsTest): إعدادات البريد الإلكتروني

    Returns:
        schemas.EmailSettingsTestResponse: نتيجة اختبار إعدادات البريد الإلكتروني
    """
    try:
        # اختبار إعدادات البريد الإلكتروني
        result = validate_email_settings(
            smtp_server=email_settings.smtp_server,
            smtp_port=email_settings.smtp_port,
            smtp_user=email_settings.smtp_user,
            smtp_password=email_settings.smtp_password,
            from_email=email_settings.from_email,
            use_tls=email_settings.use_tls,
            test_recipient=email_settings.test_recipient,
        )

        if result["success"]:
            return schemas.EmailSettingsTestResponse(
                success=True, message="تم إرسال بريد إلكتروني اختباري بنجاح"
            )
        else:
            return schemas.EmailSettingsTestResponse(
                success=False,
                message=f"فشل إرسال بريد إلكتروني اختباري: {result['error']}",
            )

    except Exception as e:
        return schemas.EmailSettingsTestResponse(
            success=False, message=f"فشل إرسال بريد إلكتروني اختباري: {str(e)}"
        )


def get_available_modules(db: Session) -> List[schemas.ModuleInfo]:
    """
    الحصول على قائمة المديولات المتاحة

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        List[schemas.ModuleInfo]: قائمة المديولات المتاحة
    """
    modules = module_service.get_all_modules(db)
    return [
        schemas.ModuleInfo(
            id=module.id,
            name=module.name,
            description=module.description,
            is_core=module.is_core,
            is_enabled=module.is_enabled,
            dependencies=module.dependencies,
            version=module.version,
            author=module.author,
        )
        for module in modules
    ]


def get_countries(db: Session) -> List[schemas.CountryInfo]:
    """
    الحصول على قائمة الدول

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        List[schemas.CountryInfo]: قائمة الدول
    """
    countries = company_service.get_countries(db)
    return [
        schemas.CountryInfo(
            code=country.code,
            name=country.name,
            name_ar=country.name_ar,
            flag_emoji=country.flag_emoji,
            calling_code=country.calling_code,
        )
        for country in countries
    ]


def get_currencies(db: Session) -> List[schemas.CurrencyInfo]:
    """
    الحصول على قائمة العملات

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        List[schemas.CurrencyInfo]: قائمة العملات
    """
    currencies = company_service.get_currencies(db)
    return [
        schemas.CurrencyInfo(
            code=currency.code,
            name=currency.name,
            name_ar=currency.name_ar,
            symbol=currency.symbol,
        )
        for currency in currencies
    ]


def get_timezones(db: Session) -> List[schemas.TimezoneInfo]:
    """
    الحصول على قائمة المناطق الزمنية

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        List[schemas.TimezoneInfo]: قائمة المناطق الزمنية
    """
    timezones = system_settings_service.get_timezones(db)
    return [
        schemas.TimezoneInfo(
            value=timezone.value, text=timezone.text, offset=timezone.offset
        )
        for timezone in timezones
    ]


def get_languages(db: Session) -> List[schemas.LanguageInfo]:
    """
    الحصول على قائمة اللغات

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        List[schemas.LanguageInfo]: قائمة اللغات
    """
    languages = system_settings_service.get_languages(db)
    return [
        schemas.LanguageInfo(
            code=language.code,
            name=language.name,
            name_native=language.name_native,
            rtl=language.rtl,
        )
        for language in languages
    ]


def reset_setup(db: Session) -> schemas.SetupStatusResponse:
    """
    إعادة تعيين عملية الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد إعادة التعيين
    """
    # الحصول على حالة الإعداد
    setup_status = db.query(models.SetupStatus).first()
    if not setup_status:
        setup_status = models.SetupStatus(
            is_completed=False, current_step=SETUP_STEPS[0], completed_steps=[]
        )
        db.add(setup_status)
    else:
        # إعادة تعيين حالة الإعداد
        setup_status.is_completed = False
        setup_status.current_step = SETUP_STEPS[0]
        setup_status.completed_steps = []
        setup_status.setup_token = secrets.token_urlsafe(32)
        setup_status.token_expires_at = datetime.utcnow() + timedelta(hours=24)

    # حفظ التغييرات
    db.commit()
    db.refresh(setup_status)

    # تسجيل نشاط الإعداد
    log_setup_activity(db, "reset", "warning", "تم إعادة تعيين عملية الإعداد")

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at,
    )


def get_setup_logs(db: Session) -> List[schemas.SetupLogEntry]:
    """
    الحصول على سجلات الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        List[schemas.SetupLogEntry]: سجلات الإعداد
    """
    logs = (
        db.query(models.SetupLog)
        .order_by(desc(models.SetupLog.created_at))
        .limit(100)
        .all()
    )
    return [
        schemas.SetupLogEntry(
            id=log.id,
            step=log.step,
            status=log.status,
            message=log.message,
            details=log.details,
            created_at=log.created_at,
        )
        for log in logs
    ]


def log_setup_activity(db: Session,
                       step: str,
                       status: str,
                       message: str,
                       details: Dict[str,
                                     Any] = None) -> None:
    """
    تسجيل نشاط الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
        step (str): الخطوة
        status (str): الحالة (success, error, warning, info)
        message (str): الرسالة
        details (Dict[str, Any], optional): تفاصيل إضافية
    """
    try:
        # إنشاء سجل جديد
        log = models.SetupLog(
            step=step, status=status, message=message, details=details or {}
        )
        db.add(log)
        db.commit()

        # تسجيل في سجل النظام أيضًا
        logger.info(f"[Setup] {status.upper()}: {message}")
    except Exception as e:
        # تسجيل الخطأ في سجل النظام فقط
        logger.error(f"فشل في تسجيل نشاط الإعداد: {str(e)}")
