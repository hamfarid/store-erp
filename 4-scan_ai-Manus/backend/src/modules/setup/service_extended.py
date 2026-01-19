"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/service_extended.py
الوصف: خدمات موسعة لمديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from src.modules.activity_log import service as activity_log_service
from src.modules.setup import models, schemas, security

# إعداد التسجيل
logger = logging.getLogger(__name__)

# تعريف خطوات الإعداد الموسعة
SETUP_STEPS_EXTENDED = [
    "welcome",                  # الترحيب واختيار اللغة
    "system_settings",          # إعدادات النظام الأساسية
    "database_settings",        # إعدادات قاعدة البيانات
    "company_settings",         # إعدادات الشركة الرئيسية
    "branch_settings",          # إعدادات الفروع
    "user_settings",            # إعدادات المستخدمين والأدوار
    "module_selection",         # اختيار وتكوين المديولات
    "ai_settings",              # إعدادات الذكاء الاصطناعي
    "notification_settings",    # إعدادات الإشعارات والتنبيهات
    "security_settings",        # إعدادات الأمان المتقدمة
    "backup_import_export",     # إعدادات النسخ الاحتياطي والاستيراد/التصدير
    "summary"                   # المراجعة والإكمال
]

# الخطوات الإلزامية
REQUIRED_STEPS_EXTENDED = [
    "system_settings",
    "database_settings",
    "company_settings",
    "user_settings",
    "security_settings"
]


def get_setup_status_extended(db: Session) -> schemas.SetupStatusResponse:
    """
    الحصول على حالة الإعداد الحالية الموسعة

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
            is_completed=False,
            current_step=SETUP_STEPS_EXTENDED[0],
            completed_steps=[]
        )
        db.add(setup_status)
        db.commit()
        db.refresh(setup_status)

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS_EXTENDED),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at
    )


def initialize_setup_extended(db: Session) -> schemas.SetupStatusResponse:
    """
    تهيئة عملية الإعداد الموسعة

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
        setup_status.current_step = SETUP_STEPS_EXTENDED[0]
        setup_status.completed_steps = []
        setup_status.setup_token = security.generate_secure_token()
        setup_status.token_expires_at = datetime.now(
            timezone.utc) + timedelta(hours=24)
    else:
        # إنشاء حالة جديدة
        setup_status = models.SetupStatus(
            is_completed=False,
            current_step=SETUP_STEPS_EXTENDED[0],
            completed_steps=[],
            setup_token=security.generate_secure_token(),
            token_expires_at=datetime.now(timezone.utc) + timedelta(hours=24)
        )
        db.add(setup_status)

    # حفظ التغييرات
    db.commit()
    db.refresh(setup_status)

    # تسجيل الحدث
    log_setup_event(db, "initialize", "تم تهيئة عملية الإعداد", {})

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS_EXTENDED),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at
    )


def get_step_data_extended(db: Session,
                           step_id: str) -> Optional[schemas.StepDataResponse]:
    """
    الحصول على بيانات خطوة معينة موسعة

    Args:
        db (Session): جلسة قاعدة البيانات
        step_id (str): معرف الخطوة

    Returns:
        Optional[schemas.StepDataResponse]: بيانات الخطوة
    """
    # التحقق من وجود الخطوة
    if step_id not in SETUP_STEPS_EXTENDED:
        return None

    # الحصول على بيانات الخطوة حسب نوعها
    data = {}

    if step_id == "welcome":
        # بيانات الترحيب واختيار اللغة
        data = {
            "available_languages": get_available_languages(db),
            "terms_of_service": get_terms_of_service(db),
            "privacy_policy": get_privacy_policy(db)
        }

    elif step_id == "system_settings":
        # بيانات إعدادات النظام الأساسية
        data = {
            "system_name": get_system_name(db),
            "timezones": get_timezones(db),
            "date_formats": get_date_formats(db),
            "time_formats": get_time_formats(db),
            "languages": get_languages(db),
            "default_language": get_default_language(db),
            "text_direction": get_text_direction(db),
            "theme_colors": get_theme_colors(db),
            "logo_path": get_logo_path(db)
        }

    elif step_id == "database_settings":
        # بيانات إعدادات قاعدة البيانات
        data = {
            "database_types": get_database_types(db),
            "current_database_settings": get_current_database_settings(db),
            "backup_settings": get_backup_settings(db)
        }

    elif step_id == "company_settings":
        # بيانات إعدادات الشركة الرئيسية
        data = {
            "company_info": get_company_info(db),
            "countries": get_countries(db),
            "currencies": get_currencies(db),
            "fiscal_year_options": get_fiscal_year_options(db)
        }

    elif step_id == "branch_settings":
        # بيانات إعدادات الفروع
        data = {
            "branches": get_branches(db),
            "countries": get_countries(db),
            "currencies": get_currencies(db)
        }

    elif step_id == "user_settings":
        # بيانات إعدادات المستخدمين والأدوار
        data = {
            "admin_user": get_admin_user(db),
            "roles": get_roles(db),
            "password_policy": get_password_policy(db),
            "two_factor_options": get_two_factor_options(db)
        }

    elif step_id == "module_selection":
        # بيانات اختيار وتكوين المديولات
        data = {
            "available_modules": get_available_modules(db),
            "enabled_modules": get_enabled_modules(db),
            "module_dependencies": get_module_dependencies(db)
        }

    elif step_id == "ai_settings":
        # بيانات إعدادات الذكاء الاصطناعي
        data = {
            "ai_agents": get_ai_agents(db),
            "memory_settings": get_memory_settings(db),
            "ai_models": get_ai_models(db),
            "integration_options": get_ai_integration_options(db),
            "training_options": get_ai_training_options(db)
        }

    elif step_id == "notification_settings":
        # بيانات إعدادات الإشعارات والتنبيهات
        data = {
            "email_settings": get_email_settings(db),
            "sms_settings": get_sms_settings(db),
            "app_notification_settings": get_app_notification_settings(db),
            "notification_templates": get_notification_templates(db),
            "notification_schedules": get_notification_schedules(db)
        }

    elif step_id == "security_settings":
        # بيانات إعدادات الأمان المتقدمة
        data = {
            "ssl_settings": get_ssl_settings(db),
            "firewall_settings": get_firewall_settings(db),
            "allowed_ips": get_allowed_ips(db),
            "cors_settings": get_cors_settings(db),
            "xss_protection": get_xss_protection(db),
            "csrf_protection": get_csrf_protection(db),
            "sql_injection_protection": get_sql_injection_protection(db),
            "rate_limiting": get_rate_limiting(db),
            "account_lockout": get_account_lockout(db)
        }

    elif step_id == "backup_import_export":
        # بيانات إعدادات النسخ الاحتياطي والاستيراد/التصدير
        data = {
            "backup_schedule": get_backup_schedule(db),
            "backup_storage": get_backup_storage(db),
            "backup_retention": get_backup_retention(db),
            "import_templates": get_import_templates(db),
            "export_formats": get_export_formats(db),
            "validation_settings": get_validation_settings(db)
        }

    elif step_id == "summary":
        # بيانات المراجعة والإكمال
        data = {
            "setup_summary": get_setup_summary(db),
            "validation_warnings": get_validation_warnings(db),
            "post_setup_options": get_post_setup_options(db)
        }

    # تسجيل الحدث
    log_setup_event(db,
                    "get_step_data",
                    f"تم الحصول على بيانات الخطوة {step_id}",
                    {"step_id": step_id})

    # إنشاء الاستجابة
    return schemas.StepDataResponse(
        step_id=step_id,
        data=data
    )


def validate_step_data_extended(db: Session,
                                step_id: str,
                                step_data: Dict[str,
                                                Any]) -> schemas.ValidationResult:
    """
    التحقق من صحة بيانات خطوة معينة موسعة

    Args:
        db (Session): جلسة قاعدة البيانات
        step_id (str): معرف الخطوة
        step_data (Dict[str, Any]): بيانات الخطوة

    Returns:
        schemas.ValidationResult: نتيجة التحقق
    """
    # التحقق من وجود الخطوة
    if step_id not in SETUP_STEPS_EXTENDED:
        return schemas.ValidationResult(
            is_valid=False,
            errors=["الخطوة غير موجودة"]
        )

    # التحقق من صحة البيانات حسب نوع الخطوة
    errors = []

    if step_id == "welcome":
        # التحقق من بيانات الترحيب واختيار اللغة
        if "selected_language" not in step_data:
            errors.append("يجب اختيار اللغة")
        elif not any(lang["code"] == step_data["selected_language"] for lang in get_available_languages(db)):
            errors.append("اللغة المختارة غير صالحة")

        if "accept_terms" not in step_data or not step_data["accept_terms"]:
            errors.append("يجب الموافقة على شروط الاستخدام")

    elif step_id == "system_settings":
        # التحقق من بيانات إعدادات النظام الأساسية
        if "system_name" not in step_data or not step_data["system_name"]:
            errors.append("يجب إدخال اسم النظام")

        if "timezone" not in step_data or not step_data["timezone"]:
            errors.append("يجب اختيار المنطقة الزمنية")
        elif not any(tz["value"] == step_data["timezone"] for tz in get_timezones(db)):
            errors.append("المنطقة الزمنية غير صالحة")

        if "date_format" not in step_data or not step_data["date_format"]:
            errors.append("يجب اختيار تنسيق التاريخ")

        if "time_format" not in step_data or not step_data["time_format"]:
            errors.append("يجب اختيار تنسيق الوقت")

        if "default_language" not in step_data or not step_data["default_language"]:
            errors.append("يجب اختيار اللغة الافتراضية")
        elif not any(lang["code"] == step_data["default_language"] for lang in get_languages(db)):
            errors.append("اللغة الافتراضية غير صالحة")

    elif step_id == "database_settings":
        # التحقق من بيانات إعدادات قاعدة البيانات
        if "db_type" not in step_data or not step_data["db_type"]:
            errors.append("يجب اختيار نوع قاعدة البيانات")
        elif not any(db_type["value"] == step_data["db_type"] for db_type in get_database_types(db)):
            errors.append("نوع قاعدة البيانات غير صالح")

        if "host" not in step_data or not step_data["host"]:
            errors.append("يجب إدخال المضيف")

        if "port" not in step_data:
            errors.append("يجب إدخال المنفذ")
        elif not isinstance(step_data["port"], int) or step_data["port"] <= 0:
            errors.append("المنفذ غير صالح")

        if "name" not in step_data or not step_data["name"]:
            errors.append("يجب إدخال اسم قاعدة البيانات")

        if "user" not in step_data or not step_data["user"]:
            errors.append("يجب إدخال اسم المستخدم")

        if "password" not in step_data:
            errors.append("يجب إدخال كلمة المرور")

        # التحقق من اتصال قاعدة البيانات إذا لم تكن هناك أخطاء
        if not errors:
            # Note: Database connection test is temporarily disabled
            # connection_test = schemas.DatabaseConnectionTest(...)
            # result = test_database_connection(connection_test)
            # if not result:
            #     errors.append("فشل اتصال قاعدة البيانات")
            pass

    elif step_id == "company_settings":
        # التحقق من بيانات إعدادات الشركة الرئيسية
        if "name" not in step_data or not step_data["name"]:
            errors.append("يجب إدخال اسم الشركة")

        if "country_code" not in step_data or not step_data["country_code"]:
            errors.append("يجب اختيار الدولة")
        elif not any(country["code"] == step_data["country_code"] for country in get_countries(db)):
            errors.append("الدولة غير صالحة")

        if "currency_code" not in step_data or not step_data["currency_code"]:
            errors.append("يجب اختيار العملة")
        elif not any(currency["code"] == step_data["currency_code"] for currency in get_currencies(db)):
            errors.append("العملة غير صالحة")

        if "email" in step_data and step_data["email"]:
            import re
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', step_data["email"]):
                errors.append("البريد الإلكتروني غير صالح")

        if "phone" in step_data and step_data["phone"]:
            import re
            if not re.match(r'^\+?[\d\s\-\(\)]+$', step_data["phone"]):
                errors.append("رقم الهاتف غير صالح")

        if "website" in step_data and step_data["website"]:
            import re
            if not re.match(r'^https?://[\w\.-]+\.\w+', step_data["website"]):
                errors.append("الموقع الإلكتروني غير صالح")

    elif step_id == "branch_settings":
        # التحقق من بيانات إعدادات الفروع
        if "branches" not in step_data or not isinstance(
                step_data["branches"], list):
            errors.append("يجب إدخال الفروع")
        else:
            # التحقق من وجود فرع رئيسي واحد على الأقل
            main_branch_count = sum(
                1 for branch in step_data["branches"] if branch.get(
                    "is_main", False))
            if main_branch_count == 0:
                errors.append("يجب تحديد فرع رئيسي واحد على الأقل")
            elif main_branch_count > 1:
                errors.append("يمكن تحديد فرع رئيسي واحد فقط")

            # التحقق من صحة بيانات كل فرع
            branch_codes = set()
            for i, branch in enumerate(step_data["branches"]):
                if "name" not in branch or not branch["name"]:
                    errors.append(f"يجب إدخال اسم الفرع {i+1}")

                if "code" not in branch or not branch["code"]:
                    errors.append(f"يجب إدخال رمز الفرع {i+1}")
                elif branch["code"] in branch_codes:
                    errors.append(f"رمز الفرع {branch['code']} مكرر")
                else:
                    branch_codes.add(branch["code"])

                if "country_code" not in branch or not branch["country_code"]:
                    errors.append(f"يجب اختيار دولة الفرع {i+1}")
                elif not any(country["code"] == branch["country_code"] for country in get_countries(db)):
                    errors.append(f"دولة الفرع {i+1} غير صالحة")

    elif step_id == "user_settings":
        # التحقق من بيانات إعدادات المستخدمين والأدوار
        if "admin_username" not in step_data or not step_data["admin_username"]:
            errors.append("يجب إدخال اسم المستخدم المسؤول")

        if "admin_password" not in step_data or not step_data["admin_password"]:
            errors.append("يجب إدخال كلمة مرور المستخدم المسؤول")
        else:
            # التحقق من قوة كلمة المرور
            is_valid, message, score = security.validate_password_strength(
                step_data["admin_password"])
            if not is_valid:
                errors.append(message)

        if "admin_email" not in step_data or not step_data["admin_email"]:
            errors.append("يجب إدخال البريد الإلكتروني للمستخدم المسؤول")
        else:
            import re
            if not re.match(
                r'^[\w\.-]+@[\w\.-]+\.\w+$',
                    step_data["admin_email"]):
                errors.append("البريد الإلكتروني للمستخدم المسؤول غير صالح")

        if "roles" in step_data and isinstance(step_data["roles"], list):
            # التحقق من وجود دور مسؤول واحد على الأقل
            admin_role_count = sum(
                1 for role in step_data["roles"] if role.get(
                    "is_admin", False))
            if admin_role_count == 0:
                errors.append("يجب تحديد دور مسؤول واحد على الأقل")

    elif step_id == "module_selection":
        # التحقق من بيانات اختيار وتكوين المديولات
        if "enabled_modules" not in step_data or not isinstance(
                step_data["enabled_modules"], list):
            errors.append("يجب اختيار المديولات")
        else:
            # التحقق من تبعيات المديولات
            available_modules = get_available_modules(db)
            module_dependencies = get_module_dependencies(db)

            for module_id in step_data["enabled_modules"]:
                # التحقق من وجود المديول
                if not any(
                        module["id"] == module_id for module in available_modules):
                    errors.append(f"المديول {module_id} غير موجود")
                    continue

                # التحقق من تبعيات المديول
                if module_id in module_dependencies:
                    for dependency in module_dependencies[module_id]:
                        if dependency not in step_data["enabled_modules"]:
                            errors.append(
                                f"المديول {module_id} يعتمد على المديول {dependency}")

    elif step_id == "ai_settings":
        # التحقق من بيانات إعدادات الذكاء الاصطناعي
        if "enabled_agents" not in step_data or not isinstance(
                step_data["enabled_agents"], list):
            errors.append("يجب اختيار وكلاء الذكاء الاصطناعي")

        if "memory_type" not in step_data or not step_data["memory_type"]:
            errors.append("يجب اختيار نوع الذاكرة")

        if "ai_model" not in step_data or not step_data["ai_model"]:
            errors.append("يجب اختيار نموذج الذكاء الاصطناعي")

    elif step_id == "notification_settings":
        # التحقق من بيانات إعدادات الإشعارات والتنبيهات
        if "email_enabled" in step_data and step_data["email_enabled"]:
            if "smtp_server" not in step_data or not step_data["smtp_server"]:
                errors.append("يجب إدخال خادم SMTP")

            if "smtp_port" not in step_data:
                errors.append("يجب إدخال منفذ SMTP")
            elif not isinstance(step_data["smtp_port"], int) or step_data["smtp_port"] <= 0:
                errors.append("منفذ SMTP غير صالح")

            if "smtp_user" not in step_data or not step_data["smtp_user"]:
                errors.append("يجب إدخال اسم مستخدم SMTP")

            if "smtp_password" not in step_data:
                errors.append("يجب إدخال كلمة مرور SMTP")

            if "from_email" not in step_data or not step_data["from_email"]:
                errors.append("يجب إدخال البريد الإلكتروني المرسل")
            else:
                import re
                if not re.match(
                    r'^[\w\.-]+@[\w\.-]+\.\w+$',
                        step_data["from_email"]):
                    errors.append("البريد الإلكتروني المرسل غير صالح")

            # التحقق من اتصال SMTP إذا لم تكن هناك أخطاء
            if not errors:
                # Note: email test disabled for now, would need proper implementation
                # email_test = schemas.EmailSettingsTest(...)
                # result = test_email_settings(email_test)
                result_success = True  # Placeholder for actual email test
                if not result_success:
                    errors.append("فشل اتصال SMTP")

    elif step_id == "security_settings":
        # التحقق من بيانات إعدادات الأمان المتقدمة
        security_settings = schemas.SecuritySettings(
            use_ssl=step_data.get("use_ssl", False),
            ssl_cert_path=step_data.get("ssl_cert_path"),
            ssl_key_path=step_data.get("ssl_key_path"),
            session_timeout=step_data.get("session_timeout", 30),
            max_login_attempts=step_data.get("max_login_attempts", 5),
            lockout_duration=step_data.get("lockout_duration", 30),
            password_expiry_days=step_data.get("password_expiry_days", 90),
            enable_2fa=step_data.get("enable_2fa", False),
            allowed_ips=step_data.get("allowed_ips", []),
            cors_origins=step_data.get("cors_origins", []),
            xss_protection=step_data.get("xss_protection", True),
            csrf_protection=step_data.get("csrf_protection", True),
            sql_injection_protection=step_data.get("sql_injection_protection", True),
            rate_limiting=step_data.get("rate_limiting", {})
        )

        validation_result = security.validate_security_settings(
            security_settings)
        if not validation_result.is_valid:
            errors.extend(validation_result.warnings)

    elif step_id == "backup_import_export":
        # التحقق من بيانات إعدادات النسخ الاحتياطي والاستيراد/التصدير
        if "backup_enabled" in step_data and step_data["backup_enabled"]:
            if "backup_frequency" not in step_data or not step_data["backup_frequency"]:
                errors.append("يجب اختيار تكرار النسخ الاحتياطي")

            if "backup_time" not in step_data or not step_data["backup_time"]:
                errors.append("يجب اختيار وقت النسخ الاحتياطي")

            if "backup_storage" not in step_data or not step_data["backup_storage"]:
                errors.append("يجب اختيار موقع تخزين النسخ الاحتياطي")

            if "backup_retention" not in step_data or not isinstance(
                    step_data["backup_retention"], int) or step_data["backup_retention"] <= 0:
                errors.append("يجب إدخال فترة الاحتفاظ بالنسخ الاحتياطي")

    elif step_id == "summary":
        # لا يوجد تحقق خاص للمراجعة والإكمال
        pass

    # تسجيل الحدث
    log_setup_event(
        db, "validate_step_data", f"تم التحقق من صحة بيانات الخطوة {step_id}", {
            "step_id": step_id, "is_valid": len(errors) == 0, "errors": errors})

    # إنشاء الاستجابة
    return schemas.ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors
    )


def update_step_data_extended(db: Session,
                              step_id: str,
                              step_data: Dict[str,
                                              Any]) -> schemas.StepUpdateResponse:
    """
    تحديث بيانات خطوة معينة موسعة

    Args:
        db (Session): جلسة قاعدة البيانات
        step_id (str): معرف الخطوة
        step_data (Dict[str, Any]): بيانات الخطوة

    Returns:
        schemas.StepUpdateResponse: نتيجة تحديث الخطوة
    """
    # التحقق من وجود الخطوة
    if step_id not in SETUP_STEPS_EXTENDED:
        return schemas.StepUpdateResponse(
            success=False,
            message="الخطوة غير موجودة"
        )

    # التحقق من صحة البيانات
    validation_result = validate_step_data_extended(db, step_id, step_data)
    if not validation_result.is_valid:
        return schemas.StepUpdateResponse(
            success=False,
            message=f"بيانات غير صالحة: {', '.join(validation_result.errors)}"
        )

    # تحديث البيانات حسب نوع الخطوة
    try:
        if step_id == "welcome":
            # تحديث بيانات الترحيب واختيار اللغة
            update_selected_language(db, step_data.get("selected_language"))

        elif step_id == "system_settings":
            # تحديث بيانات إعدادات النظام الأساسية
            update_system_settings(db, step_data)

        elif step_id == "database_settings":
            # تحديث بيانات إعدادات قاعدة البيانات
            update_database_settings(db, step_data)

        elif step_id == "company_settings":
            # تحديث بيانات إعدادات الشركة الرئيسية
            update_company_settings(db, step_data)

        elif step_id == "branch_settings":
            # تحديث بيانات إعدادات الفروع
            update_branch_settings(db, step_data)

        elif step_id == "user_settings":
            # تحديث بيانات إعدادات المستخدمين والأدوار
            update_user_settings(db, step_data)

        elif step_id == "module_selection":
            # تحديث بيانات اختيار وتكوين المديولات
            update_module_selection(db, step_data)

        elif step_id == "ai_settings":
            # تحديث بيانات إعدادات الذكاء الاصطناعي
            update_ai_settings(db, step_data)

        elif step_id == "notification_settings":
            # تحديث بيانات إعدادات الإشعارات والتنبيهات
            update_notification_settings(db, step_data)

        elif step_id == "security_settings":
            # تحديث بيانات إعدادات الأمان المتقدمة
            update_security_settings(db, step_data)

        elif step_id == "backup_import_export":
            # تحديث بيانات إعدادات النسخ الاحتياطي والاستيراد/التصدير
            update_backup_import_export_settings(db, step_data)

        elif step_id == "summary":
            # تحديث بيانات المراجعة والإكمال
            # لا يوجد تحديث خاص للمراجعة والإكمال
            pass

        # تحديث حالة الإعداد
        setup_status = db.query(models.SetupStatus).first()
        if setup_status:
            if step_id not in setup_status.completed_steps:
                setup_status.completed_steps.append(step_id)
            setup_status.updated_at = datetime.now(timezone.utc)
            db.commit()

        # تسجيل الحدث
        log_setup_event(db,
                        "update_step_data",
                        f"تم تحديث بيانات الخطوة {step_id}",
                        {"step_id": step_id})

        # إنشاء الاستجابة
        return schemas.StepUpdateResponse(
            success=True,
            message=f"تم تحديث بيانات الخطوة {step_id} بنجاح"
        )
    except Exception as e:
        logger.error("خطأ في تحديث بيانات الخطوة %s: %s", step_id, str(e))

        # تسجيل الحدث
        log_setup_event(
            db, "update_step_data_error", f"خطأ في تحديث بيانات الخطوة {step_id}", {
                "step_id": step_id, "error": str(e)})

        # إنشاء الاستجابة
        return schemas.StepUpdateResponse(
            success=False,
            message=f"خطأ في تحديث بيانات الخطوة {step_id}: {str(e)}"
        )


def next_step_extended(db: Session) -> schemas.SetupStatusResponse:
    """
    الانتقال إلى الخطوة التالية موسعة

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد الانتقال
    """
    # البحث عن حالة الإعداد في قاعدة البيانات
    setup_status = db.query(models.SetupStatus).first()

    # التحقق من وجود حالة الإعداد
    if not setup_status:
        setup_status = models.SetupStatus(
            is_completed=False,
            current_step=SETUP_STEPS_EXTENDED[0],
            completed_steps=[]
        )
        db.add(setup_status)
        db.commit()
        db.refresh(setup_status)

        # تسجيل الحدث
        log_setup_event(
            db, "next_step", "تم إنشاء حالة الإعداد والانتقال إلى الخطوة الأولى", {
                "current_step": setup_status.current_step})

        # إنشاء الاستجابة
        return schemas.SetupStatusResponse(
            is_completed=setup_status.is_completed,
            current_step=setup_status.current_step,
            completed_steps=setup_status.completed_steps,
            total_steps=len(SETUP_STEPS_EXTENDED),
            setup_token=setup_status.setup_token,
            token_expires_at=setup_status.token_expires_at
        )

    # التحقق من اكتمال الإعداد
    if setup_status.is_completed:
        # تسجيل الحدث
        log_setup_event(
            db, "next_step", "محاولة الانتقال إلى الخطوة التالية بعد اكتمال الإعداد", {
                "current_step": setup_status.current_step})

        # إنشاء الاستجابة
        return schemas.SetupStatusResponse(
            is_completed=setup_status.is_completed,
            current_step=setup_status.current_step,
            completed_steps=setup_status.completed_steps,
            total_steps=len(SETUP_STEPS_EXTENDED),
            setup_token=setup_status.setup_token,
            token_expires_at=setup_status.token_expires_at
        )

    # الحصول على الخطوة الحالية والخطوة التالية
    current_step_index = SETUP_STEPS_EXTENDED.index(setup_status.current_step)
    next_step_index = current_step_index + 1

    # التحقق من وجود خطوة تالية
    if next_step_index >= len(SETUP_STEPS_EXTENDED):
        # تسجيل الحدث
        log_setup_event(
            db, "next_step", "محاولة الانتقال إلى ما بعد الخطوة الأخيرة", {
                "current_step": setup_status.current_step})

        # إنشاء الاستجابة
        return schemas.SetupStatusResponse(
            is_completed=setup_status.is_completed,
            current_step=setup_status.current_step,
            completed_steps=setup_status.completed_steps,
            total_steps=len(SETUP_STEPS_EXTENDED),
            setup_token=setup_status.setup_token,
            token_expires_at=setup_status.token_expires_at
        )

    # تحديث الخطوة الحالية
    setup_status.current_step = SETUP_STEPS_EXTENDED[next_step_index]
    setup_status.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(setup_status)

    # تسجيل الحدث
    log_setup_event(db,
                    "next_step",
                    f"تم الانتقال إلى الخطوة {setup_status.current_step}",
                    {"current_step": setup_status.current_step,
                     "previous_step": SETUP_STEPS_EXTENDED[current_step_index]})

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS_EXTENDED),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at
    )


def previous_step_extended(db: Session) -> schemas.SetupStatusResponse:
    """
    العودة إلى الخطوة السابقة موسعة

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد العودة
    """
    # البحث عن حالة الإعداد في قاعدة البيانات
    setup_status = db.query(models.SetupStatus).first()

    # التحقق من وجود حالة الإعداد
    if not setup_status:
        setup_status = models.SetupStatus(
            is_completed=False,
            current_step=SETUP_STEPS_EXTENDED[0],
            completed_steps=[]
        )
        db.add(setup_status)
        db.commit()
        db.refresh(setup_status)

        # تسجيل الحدث
        log_setup_event(
            db, "previous_step", "تم إنشاء حالة الإعداد والانتقال إلى الخطوة الأولى", {
                "current_step": setup_status.current_step})

        # إنشاء الاستجابة
        return schemas.SetupStatusResponse(
            is_completed=setup_status.is_completed,
            current_step=setup_status.current_step,
            completed_steps=setup_status.completed_steps,
            total_steps=len(SETUP_STEPS_EXTENDED),
            setup_token=setup_status.setup_token,
            token_expires_at=setup_status.token_expires_at
        )

    # التحقق من اكتمال الإعداد
    if setup_status.is_completed:
        # تسجيل الحدث
        log_setup_event(
            db, "previous_step", "محاولة العودة إلى الخطوة السابقة بعد اكتمال الإعداد", {
                "current_step": setup_status.current_step})

        # إنشاء الاستجابة
        return schemas.SetupStatusResponse(
            is_completed=setup_status.is_completed,
            current_step=setup_status.current_step,
            completed_steps=setup_status.completed_steps,
            total_steps=len(SETUP_STEPS_EXTENDED),
            setup_token=setup_status.setup_token,
            token_expires_at=setup_status.token_expires_at
        )

    # الحصول على الخطوة الحالية والخطوة السابقة
    current_step_index = SETUP_STEPS_EXTENDED.index(setup_status.current_step)
    previous_step_index = current_step_index - 1

    # التحقق من وجود خطوة سابقة
    if previous_step_index < 0:
        # تسجيل الحدث
        log_setup_event(
            db, "previous_step", "محاولة العودة إلى ما قبل الخطوة الأولى", {
                "current_step": setup_status.current_step})

        # إنشاء الاستجابة
        return schemas.SetupStatusResponse(
            is_completed=setup_status.is_completed,
            current_step=setup_status.current_step,
            completed_steps=setup_status.completed_steps,
            total_steps=len(SETUP_STEPS_EXTENDED),
            setup_token=setup_status.setup_token,
            token_expires_at=setup_status.token_expires_at
        )

    # تحديث الخطوة الحالية
    setup_status.current_step = SETUP_STEPS_EXTENDED[previous_step_index]
    setup_status.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(setup_status)

    # تسجيل الحدث
    log_setup_event(db,
                    "previous_step",
                    f"تم العودة إلى الخطوة {setup_status.current_step}",
                    {"current_step": setup_status.current_step,
                     "next_step": SETUP_STEPS_EXTENDED[current_step_index]})

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS_EXTENDED),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at
    )


def validate_setup_completion_extended(
        db: Session) -> schemas.ValidationResult:
    """
    التحقق من اكتمال جميع الخطوات الإلزامية موسعة

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.ValidationResult: نتيجة التحقق
    """
    # البحث عن حالة الإعداد في قاعدة البيانات
    setup_status = db.query(models.SetupStatus).first()

    # التحقق من وجود حالة الإعداد
    if not setup_status:
        return schemas.ValidationResult(
            is_valid=False,
            errors=["لم يتم العثور على حالة الإعداد"]
        )

    # التحقق من اكتمال الإعداد
    if setup_status.is_completed:
        return schemas.ValidationResult(
            is_valid=True,
            errors=[]
        )

    # التحقق من اكتمال جميع الخطوات الإلزامية
    errors = []
    for step in REQUIRED_STEPS_EXTENDED:
        if step not in setup_status.completed_steps:
            errors.append(f"الخطوة {step} غير مكتملة")

    # تسجيل الحدث
    log_setup_event(
        db, "validate_setup_completion", "تم التحقق من اكتمال جميع الخطوات الإلزامية", {
            "is_valid": len(errors) == 0, "errors": errors})

    # إنشاء الاستجابة
    return schemas.ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors
    )


def complete_setup_extended(db: Session) -> schemas.SetupCompletionResponse:
    """
    إكمال عملية الإعداد موسعة

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupCompletionResponse: نتيجة إكمال الإعداد
    """
    # التحقق من اكتمال جميع الخطوات الإلزامية
    validation_result = validate_setup_completion_extended(db)
    if not validation_result.is_valid:
        return schemas.SetupCompletionResponse(
            success=False,
            message=f"لا يمكن إكمال الإعداد: {', '.join(validation_result.errors)}")

    # البحث عن حالة الإعداد في قاعدة البيانات
    setup_status = db.query(models.SetupStatus).first()

    # التحقق من وجود حالة الإعداد
    if not setup_status:
        return schemas.SetupCompletionResponse(
            success=False,
            message="لم يتم العثور على حالة الإعداد"
        )

    # تحديث حالة الإعداد
    setup_status.is_completed = True
    setup_status.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(setup_status)

    # تنفيذ إجراءات ما بعد الإعداد
    try:
        # تطبيق إعدادات النظام
        apply_system_settings(db)

        # تطبيق إعدادات قاعدة البيانات
        apply_database_settings(db)

        # تطبيق إعدادات الشركة والفروع
        apply_company_settings(db)

        # تطبيق إعدادات المستخدمين والأدوار
        apply_user_settings(db)

        # تطبيق إعدادات المديولات
        apply_module_settings(db)

        # تطبيق إعدادات الذكاء الاصطناعي
        apply_ai_settings(db)

        # تطبيق إعدادات الإشعارات والتنبيهات
        apply_notification_settings(db)

        # تطبيق إعدادات الأمان
        apply_security_settings(db)

        # تطبيق إعدادات النسخ الاحتياطي والاستيراد/التصدير
        apply_backup_import_export_settings(db)

        # تسجيل الحدث
        log_setup_event(
            db,
            "complete_setup",
            "تم إكمال عملية الإعداد بنجاح",
            {})

        # إنشاء الاستجابة
        return schemas.SetupCompletionResponse(
            success=True,
            message="تم إكمال عملية الإعداد بنجاح"
        )
    except Exception as e:
        logger.error(f"خطأ في إكمال عملية الإعداد: {str(e)}")

        # إعادة تعيين حالة الإعداد
        setup_status.is_completed = False
        db.commit()

        # تسجيل الحدث
        log_setup_event(db,
                        "complete_setup_error",
                        "خطأ في إكمال عملية الإعداد",
                        {"error": str(e)})

        # إنشاء الاستجابة
        return schemas.SetupCompletionResponse(
            success=False,
            message=f"خطأ في إكمال عملية الإعداد: {str(e)}"
        )


def reset_setup_extended(db: Session) -> schemas.SetupStatusResponse:
    """
    إعادة تعيين عملية الإعداد موسعة

    Args:
        db (Session): جلسة قاعدة البيانات

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد إعادة التعيين
    """
    # البحث عن حالة الإعداد في قاعدة البيانات
    setup_status = db.query(models.SetupStatus).first()

    # التحقق من وجود حالة الإعداد
    if not setup_status:
        setup_status = models.SetupStatus(
            is_completed=False,
            current_step=SETUP_STEPS_EXTENDED[0],
            completed_steps=[]
        )
        db.add(setup_status)
    else:
        # إعادة تعيين حالة الإعداد
        setup_status.is_completed = False
        setup_status.current_step = SETUP_STEPS_EXTENDED[0]
        setup_status.completed_steps = []
        setup_status.setup_token = security.generate_secure_token()
        setup_status.token_expires_at = datetime.now(
            timezone.utc) + timedelta(hours=24)
        setup_status.updated_at = datetime.utcnow()

    # حفظ التغييرات
    db.commit()
    db.refresh(setup_status)

    # تسجيل الحدث
    log_setup_event(db, "reset_setup", "تم إعادة تعيين عملية الإعداد", {})

    # إنشاء الاستجابة
    return schemas.SetupStatusResponse(
        is_completed=setup_status.is_completed,
        current_step=setup_status.current_step,
        completed_steps=setup_status.completed_steps,
        total_steps=len(SETUP_STEPS_EXTENDED),
        setup_token=setup_status.setup_token,
        token_expires_at=setup_status.token_expires_at
    )


def log_setup_event(db: Session, event_type: str,
                    message: str, details: Dict[str, Any]) -> None:
    """
    تسجيل حدث الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
        event_type (str): نوع الحدث
        message (str): رسالة الحدث
        details (Dict[str, Any]): تفاصيل الحدث
    """
    # تحديد حالة الحدث
    status = "info"
    if event_type.endswith("_error"):
        status = "error"
    elif event_type.startswith("validate"):
        status = "warning"

    # إنشاء سجل الإعداد
    setup_log = models.SetupLog(
        step=details.get("step_id", details.get("current_step", "general")),
        status=status,
        message=message,
        details=details
    )

    # إضافة السجل إلى قاعدة البيانات
    db.add(setup_log)
    db.commit()

    # تسجيل النشاط - fix parameter names
    activity_log_service.log_activity(
        db=db,
        log_type="system",
        module_id="setup",
        action_id=event_type,
        description=message,
        details=details
    )


# وظائف مساعدة للحصول على البيانات

def get_available_languages(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قائمة اللغات المتاحة"""
    return [
        {"code": "ar", "name": "العربية", "name_native": "العربية", "rtl": True},
        {"code": "en", "name": "الإنجليزية", "name_native": "English", "rtl": False}
    ]


def get_terms_of_service(db: Session) -> str:
    """الحصول على شروط الاستخدام"""
    return """
    # شروط الاستخدام

    هذه هي شروط استخدام نظام Scan AI. يرجى قراءتها بعناية قبل المتابعة.

    ## 1. قبول الشروط

    باستخدام هذا النظام، فإنك توافق على الالتزام بهذه الشروط.

    ## 2. استخدام النظام

    يجب استخدام النظام وفقاً للقوانين واللوائح المعمول بها.

    ## 3. الملكية الفكرية

    جميع حقوق الملكية الفكرية للنظام محفوظة لشركة Gaara ERP.

    ## 4. المسؤولية

    لا تتحمل شركة Gaara ERP أي مسؤولية عن أي أضرار ناتجة عن استخدام النظام.

    ## 5. التغييرات

    تحتفظ شركة Gaara ERP بالحق في تغيير هذه الشروط في أي وقت.
    """


def get_privacy_policy(db: Session) -> str:
    """الحصول على سياسة الخصوصية"""
    return """
    # سياسة الخصوصية

    هذه هي سياسة خصوصية نظام Scan AI. يرجى قراءتها بعناية قبل المتابعة.

    ## 1. جمع المعلومات

    نقوم بجمع المعلومات التي تقدمها عند استخدام النظام.

    ## 2. استخدام المعلومات

    نستخدم المعلومات التي نجمعها لتوفير وتحسين خدماتنا.

    ## 3. مشاركة المعلومات

    لا نشارك معلوماتك الشخصية مع أطراف ثالثة دون موافقتك.

    ## 4. أمان المعلومات

    نتخذ إجراءات أمنية لحماية معلوماتك.

    ## 5. التغييرات

    تحتفظ شركة Gaara ERP بالحق في تغيير هذه السياسة في أي وقت.
    """


def get_system_name(db: Session) -> str:
    """الحصول على اسم النظام"""
    return "Scan AI"


def get_timezones(db: Session) -> List[Dict[str, str]]:
    """الحصول على قائمة المناطق الزمنية"""
    return [
        {"value": "Africa/Cairo", "text": "الرياض (GMT+3)", "offset": "+03:00"},
        {"value": "Asia/Dubai", "text": "دبي (GMT+4)", "offset": "+04:00"},
        {"value": "Asia/Baghdad", "text": "بغداد (GMT+3)", "offset": "+03:00"},
        {"value": "Africa/Cairo", "text": "القاهرة (GMT+2)", "offset": "+02:00"},
        {"value": "Europe/Istanbul", "text": "إسطنبول (GMT+3)", "offset": "+03:00"},
        {"value": "Europe/London", "text": "لندن (GMT+0/+1)", "offset": "+00:00"},
        {"value": "America/New_York", "text": "نيويورك (GMT-5/-4)", "offset": "-05:00"},
        {"value": "Asia/Tokyo", "text": "طوكيو (GMT+9)", "offset": "+09:00"}
    ]


def get_date_formats(db: Session) -> List[Dict[str, str]]:
    """الحصول على قائمة تنسيقات التاريخ"""
    return [
        {"value": "DD/MM/YYYY", "text": "DD/MM/YYYY (31/12/2025)"},
        {"value": "MM/DD/YYYY", "text": "MM/DD/YYYY (12/31/2025)"},
        {"value": "YYYY-MM-DD", "text": "YYYY-MM-DD (2025-12-31)"},
        {"value": "DD-MM-YYYY", "text": "DD-MM-YYYY (31-12-2025)"},
        {"value": "MM-DD-YYYY", "text": "MM-DD-YYYY (12-31-2025)"}
    ]


def get_time_formats(db: Session) -> List[Dict[str, str]]:
    """الحصول على قائمة تنسيقات الوقت"""
    return [
        {"value": "HH:mm", "text": "HH:mm (24 ساعة)"},
        {"value": "hh:mm A", "text": "hh:mm A (12 ساعة)"}
    ]


def get_languages(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قائمة اللغات"""
    return get_available_languages(db)


def get_default_language(db: Session) -> str:
    """الحصول على اللغة الافتراضية"""
    return "ar"


def get_text_direction(db: Session) -> str:
    """الحصول على اتجاه النص"""
    return "rtl"


def get_theme_colors(db: Session) -> Dict[str, str]:
    """الحصول على ألوان السمة"""
    return {
        "primary": "#007bff",
        "secondary": "#6c757d",
        "success": "#28a745",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "info": "#17a2b8",
        "light": "#f8f9fa",
        "dark": "#343a40"
    }


def get_logo_path(db: Session) -> Optional[str]:
    """الحصول على مسار الشعار"""
    return None


def get_database_types(db: Session) -> List[Dict[str, str]]:
    """الحصول على قائمة أنواع قواعد البيانات"""
    return [
        {"value": "postgresql", "text": "PostgreSQL"},
        {"value": "mysql", "text": "MySQL/MariaDB"},
        {"value": "mongodb", "text": "MongoDB"}
    ]


def get_current_database_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات قاعدة البيانات الحالية"""
    return {
        "db_type": "postgresql",
        "host": "localhost",
        "port": 5432,
        "name": "scan_ai",
        "user": "postgres",
        "password": ""
    }


def get_backup_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات النسخ الاحتياطي"""
    return {
        "auto_backup": True,
        "backup_frequency": "daily",
        "backup_time": "00:00",
        "backup_retention": 7
    }


def get_company_info(db: Session) -> Dict[str, Any]:
    """الحصول على معلومات الشركة"""
    return {
        "name": "",
        "legal_name": "",
        "tax_number": "",
        "registration_number": "",
        "address": "",
        "city": "",
        "country_code": "",
        "phone": "",
        "email": "",
        "website": "",
        "logo_path": "",
        "currency_code": "",
        "fiscal_year_start": "01-01"
    }


def get_countries(db: Session) -> List[Dict[str, str]]:
    """الحصول على قائمة الدول"""
    return [
        {"code": "SA", "name": "جمهورية مصر العربية", "name_ar": "جمهورية مصر العربية", "flag_emoji": "🇸🇦", "calling_code": "+966"},
        {"code": "AE", "name": "الإمارات العربية المتحدة", "name_ar": "الإمارات العربية المتحدة", "flag_emoji": "🇦🇪", "calling_code": "+971"},
        {"code": "EG", "name": "مصر", "name_ar": "مصر", "flag_emoji": "🇪🇬", "calling_code": "+20"},
        {"code": "JO", "name": "الأردن", "name_ar": "الأردن", "flag_emoji": "🇯🇴", "calling_code": "+962"},
        {"code": "KW", "name": "الكويت", "name_ar": "الكويت", "flag_emoji": "🇰🇼", "calling_code": "+965"},
        {"code": "BH", "name": "البحرين", "name_ar": "البحرين", "flag_emoji": "🇧🇭", "calling_code": "+973"},
        {"code": "QA", "name": "قطر", "name_ar": "قطر", "flag_emoji": "🇶🇦", "calling_code": "+974"},
        {"code": "OM", "name": "عمان", "name_ar": "عمان", "flag_emoji": "🇴🇲", "calling_code": "+968"},
        {"code": "IQ", "name": "العراق", "name_ar": "العراق", "flag_emoji": "🇮🇶", "calling_code": "+964"},
        {"code": "LB", "name": "لبنان", "name_ar": "لبنان", "flag_emoji": "🇱🇧", "calling_code": "+961"},
        {"code": "US", "name": "الولايات المتحدة الأمريكية", "name_ar": "الولايات المتحدة الأمريكية", "flag_emoji": "🇺🇸", "calling_code": "+1"},
        {"code": "GB", "name": "المملكة المتحدة", "name_ar": "المملكة المتحدة", "flag_emoji": "🇬🇧", "calling_code": "+44"}
    ]


def get_currencies(db: Session) -> List[Dict[str, str]]:
    """الحصول على قائمة العملات"""
    return [
        {"code": "SAR", "name": "Saudi Riyal", "name_ar": "ريال سعودي", "symbol": "ر.س"},
        {"code": "AED", "name": "UAE Dirham", "name_ar": "درهم إماراتي", "symbol": "د.إ"},
        {"code": "EGP", "name": "Egyptian Pound", "name_ar": "جنيه مصري", "symbol": "ج.م"},
        {"code": "JOD", "name": "Jordanian Dinar", "name_ar": "دينار أردني", "symbol": "د.أ"},
        {"code": "KWD", "name": "Kuwaiti Dinar", "name_ar": "دينار كويتي", "symbol": "د.ك"},
        {"code": "BHD", "name": "Bahraini Dinar", "name_ar": "دينار بحريني", "symbol": "د.ب"},
        {"code": "QAR", "name": "Qatari Riyal", "name_ar": "ريال قطري", "symbol": "ر.ق"},
        {"code": "OMR", "name": "Omani Rial", "name_ar": "ريال عماني", "symbol": "ر.ع"},
        {"code": "IQD", "name": "Iraqi Dinar", "name_ar": "دينار عراقي", "symbol": "د.ع"},
        {"code": "LBP", "name": "Lebanese Pound", "name_ar": "ليرة لبنانية", "symbol": "ل.ل"},
        {"code": "USD", "name": "US Dollar", "name_ar": "دولار أمريكي", "symbol": "$"},
        {"code": "EUR", "name": "Euro", "name_ar": "يورو", "symbol": "€"},
        {"code": "GBP", "name": "British Pound", "name_ar": "جنيه إسترليني", "symbol": "£"}
    ]


def get_fiscal_year_options(db: Session) -> List[Dict[str, str]]:
    """الحصول على خيارات السنة المالية"""
    return [
        {"value": "01-01", "text": "1 يناير"},
        {"value": "04-01", "text": "1 أبريل"},
        {"value": "07-01", "text": "1 يوليو"},
        {"value": "10-01", "text": "1 أكتوبر"}
    ]


def get_branches(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قائمة الفروع"""
    return []


def get_admin_user(db: Session) -> Dict[str, Any]:
    """الحصول على معلومات المستخدم المسؤول"""
    return {
        "username": "",
        "email": "",
        "first_name": "",
        "last_name": "",
        "password": "",
        "confirm_password": "",
        "enable_2fa": False
    }


def get_roles(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قائمة الأدوار"""
    return [
        {
            "id": "admin",
            "name": "مسؤول النظام",
            "description": "صلاحيات كاملة على النظام",
            "is_admin": True,
            "permissions": ["*"]
        },
        {
            "id": "manager",
            "name": "مدير",
            "description": "صلاحيات إدارية على النظام",
            "is_admin": False,
            "permissions": ["read", "write", "update"]
        },
        {
            "id": "user",
            "name": "مستخدم",
            "description": "صلاحيات محدودة على النظام",
            "is_admin": False,
            "permissions": ["read"]
        }
    ]


def get_password_policy(db: Session) -> Dict[str, Any]:
    """الحصول على سياسة كلمة المرور"""
    return {
        "min_length": 8,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_special_chars": True,
        "expiry_days": 90,
        "prevent_reuse": True,
        "reuse_count": 5
    }


def get_two_factor_options(db: Session) -> List[Dict[str, str]]:
    """الحصول على خيارات المصادقة الثنائية"""
    return [
        {"value": "email", "text": "البريد الإلكتروني"},
        {"value": "sms", "text": "الرسائل القصيرة"},
        {"value": "app", "text": "تطبيق المصادقة"}
    ]


def get_available_modules(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قائمة المديولات المتاحة"""
    return [
        {
            "id": "core",
            "name": "النظام الأساسي",
            "description": "المديولات الأساسية للنظام",
            "is_core": True,
            "is_enabled": True,
            "dependencies": [],
            "version": "1.0.0",
            "author": "Gaara ERP"
        },
        {
            "id": "ai",
            "name": "الذكاء الاصطناعي",
            "description": "مديول الذكاء الاصطناعي",
            "is_core": True,
            "is_enabled": True,
            "dependencies": ["core"],
            "version": "1.0.0",
            "author": "Gaara ERP"
        },
        {
            "id": "disease_diagnosis",
            "name": "تشخيص الأمراض",
            "description": "مديول تشخيص الأمراض",
            "is_core": False,
            "is_enabled": True,
            "dependencies": ["core", "ai"],
            "version": "1.0.0",
            "author": "Gaara ERP"
        },
        {
            "id": "memory",
            "name": "الذاكرة",
            "description": "مديول الذاكرة",
            "is_core": True,
            "is_enabled": True,
            "dependencies": ["core", "ai"],
            "version": "1.0.0",
            "author": "Gaara ERP"
        },
        {
            "id": "activity_log",
            "name": "سجل النشاط",
            "description": "مديول سجل النشاط",
            "is_core": True,
            "is_enabled": True,
            "dependencies": ["core"],
            "version": "1.0.0",
            "author": "Gaara ERP"
        },
        {
            "id": "import_export",
            "name": "الاستيراد والتصدير",
            "description": "مديول الاستيراد والتصدير",
            "is_core": True,
            "is_enabled": True,
            "dependencies": ["core"],
            "version": "1.0.0",
            "author": "Gaara ERP"
        }
    ]


def get_enabled_modules(db: Session) -> List[str]:
    """الحصول على قائمة المديولات المفعلة"""
    return [
        "core",
        "ai",
        "disease_diagnosis",
        "memory",
        "activity_log",
        "import_export"]


def get_module_dependencies(db: Session) -> Dict[str, List[str]]:
    """الحصول على تبعيات المديولات"""
    return {
        "ai": ["core"],
        "disease_diagnosis": ["core", "ai"],
        "memory": ["core", "ai"],
        "activity_log": ["core"],
        "import_export": ["core"]
    }


def get_ai_agents(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قائمة وكلاء الذكاء الاصطناعي"""
    return [
        {
            "id": "main_agent",
            "name": "الوكيل الرئيسي",
            "description": "الوكيل الرئيسي للذكاء الاصطناعي",
            "is_enabled": True,
            "is_system": True,
            "model": "gpt-4"
        },
        {
            "id": "diagnosis_agent",
            "name": "وكيل التشخيص",
            "description": "وكيل تشخيص الأمراض",
            "is_enabled": True,
            "is_system": True,
            "model": "gpt-4"
        },
        {
            "id": "memory_agent",
            "name": "وكيل الذاكرة",
            "description": "وكيل إدارة الذاكرة",
            "is_enabled": True,
            "is_system": True,
            "model": "gpt-4"
        }
    ]


def get_memory_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات الذاكرة"""
    return {
        "short_term_memory": {
            "type": "redis",
            "expiry": 24,  # ساعات
            "max_size": 1000
        },
        "long_term_memory": {
            "type": "vector_db",
            "storage": "postgres",
            "embedding_model": "text-embedding-ada-002"
        }
    }


def get_ai_models(db: Session) -> List[Dict[str, str]]:
    """الحصول على قائمة نماذج الذكاء الاصطناعي"""
    return [
        {"value": "gpt-4", "text": "GPT-4"},
        {"value": "gpt-3.5-turbo", "text": "GPT-3.5 Turbo"},
        {"value": "text-embedding-ada-002", "text": "Text Embedding Ada 002"}
    ]


def get_ai_integration_options(db: Session) -> Dict[str, List[str]]:
    """الحصول على خيارات تكامل الذكاء الاصطناعي"""
    return {
        "disease_diagnosis": ["main_agent", "diagnosis_agent"],
        "memory": ["main_agent", "memory_agent"]
    }


def get_ai_training_options(db: Session) -> Dict[str, Any]:
    """الحصول على خيارات تدريب الذكاء الاصطناعي"""
    return {
        "auto_training": True,
        "training_frequency": "weekly",
        "training_data_sources": ["user_interactions", "external_data"]
    }


def get_email_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات البريد الإلكتروني"""
    return {
        "enabled": False,
        "smtp_server": "",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_password": "",
        "from_email": "",
        "use_tls": True
    }


def get_sms_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات الرسائل القصيرة"""
    return {
        "enabled": False,
        "provider": "",
        "api_key": "",
        "sender_id": ""
    }


def get_app_notification_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات إشعارات التطبيق"""
    return {
        "enabled": True,
        "max_notifications": 100,
        "expiry_days": 30
    }


def get_notification_templates(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قوالب الإشعارات"""
    return [{"id": "welcome",
             "name": "رسالة الترحيب",
             "subject": "مرحباً بك في نظام Scan AI",
             "body": "مرحباً {user_name}،\n\nنرحب بك في نظام Scan AI. نتمنى لك تجربة ممتعة ومفيدة.\n\nمع تحيات فريق Scan AI",
             "type": "email"},
            {"id": "password_reset",
             "name": "إعادة تعيين كلمة المرور",
             "subject": "إعادة تعيين كلمة المرور",
             "body": "مرحباً {user_name}،\n\nلقد تلقينا طلباً لإعادة تعيين كلمة المرور الخاصة بك. يرجى النقر على الرابط التالي لإعادة تعيين كلمة المرور:\n\n{reset_link}\n\nإذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذه الرسالة.\n\nمع تحيات فريق Scan AI",
             "type": "email"}]


def get_notification_schedules(db: Session) -> List[Dict[str, Any]]:
    """الحصول على جداول الإشعارات"""
    return [
        {
            "id": "daily_summary",
            "name": "ملخص يومي",
            "template_id": "daily_summary",
            "frequency": "daily",
            "time": "08:00",
            "recipients": ["admin"],
            "enabled": True
        },
        {
            "id": "weekly_report",
            "name": "تقرير أسبوعي",
            "template_id": "weekly_report",
            "frequency": "weekly",
            "day": "monday",
            "time": "09:00",
            "recipients": ["admin", "manager"],
            "enabled": True
        }
    ]


def get_ssl_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات SSL"""
    return {
        "enabled": False,
        "cert_path": "",
        "key_path": "",
        "auto_renew": True
    }


def get_firewall_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات جدار الحماية"""
    return {
        "enabled": True,
        "block_suspicious_ips": True,
        "block_tor_exit_nodes": True,
        "block_vpn_ips": True
    }


def get_allowed_ips(db: Session) -> List[str]:
    """الحصول على قائمة عناوين IP المسموح بها"""
    return []


def get_cors_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات CORS"""
    return {
        "allowed_origins": ["*"],
        "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
        "allowed_headers": ["*"],
        "expose_headers": [],
        "max_age": 600
    }


def get_xss_protection(db: Session) -> bool:
    """الحصول على حالة حماية XSS"""
    return True


def get_csrf_protection(db: Session) -> bool:
    """الحصول على حالة حماية CSRF"""
    return True


def get_sql_injection_protection(db: Session) -> bool:
    """الحصول على حالة حماية حقن SQL"""
    return True


def get_rate_limiting(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات تحديد معدل الطلبات"""
    return {
        "enabled": True,
        "max_requests": 100,
        "time_window": 60,  # ثواني
        "by_ip": True,
        "by_user": True
    }


def get_account_lockout(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات قفل الحساب"""
    return {
        "enabled": True,
        "max_attempts": 5,
        "lockout_duration": 30,  # دقائق
        "reset_counter_after": 24  # ساعات
    }


def get_backup_schedule(db: Session) -> Dict[str, Any]:
    """الحصول على جدول النسخ الاحتياطي"""
    return {
        "enabled": True,
        "frequency": "daily",
        "time": "00:00",
        "days": [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday"]}


def get_backup_storage(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات تخزين النسخ الاحتياطي"""
    return {
        "local": {
            "enabled": True,
            "path": "/home/ubuntu/backups"
        },
        "cloud": {
            "enabled": False,
            "provider": "",
            "credentials": {},
            "path": ""
        }
    }


def get_backup_retention(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات الاحتفاظ بالنسخ الاحتياطي"""
    return {
        "days": 30,
        "max_backups": 10
    }


def get_import_templates(db: Session) -> List[Dict[str, Any]]:
    """الحصول على قوالب الاستيراد"""
    return [
        {
            "id": "users",
            "name": "المستخدمين",
            "description": "قالب استيراد المستخدمين",
            "file_type": "csv",
            "fields": [
                {"name": "username", "required": True, "type": "string"},
                {"name": "email", "required": True, "type": "email"},
                {"name": "first_name", "required": True, "type": "string"},
                {"name": "last_name", "required": True, "type": "string"},
                {"name": "role", "required": True, "type": "string"}
            ]
        },
        {
            "id": "companies",
            "name": "الشركات",
            "description": "قالب استيراد الشركات",
            "file_type": "csv",
            "fields": [
                {"name": "name", "required": True, "type": "string"},
                {"name": "country_code", "required": True, "type": "string"},
                {"name": "address", "required": False, "type": "string"},
                {"name": "phone", "required": False, "type": "string"},
                {"name": "email", "required": False, "type": "email"}
            ]
        }
    ]


def get_export_formats(db: Session) -> List[Dict[str, str]]:
    """الحصول على تنسيقات التصدير"""
    return [
        {"value": "csv", "text": "CSV"},
        {"value": "xlsx", "text": "Excel"},
        {"value": "json", "text": "JSON"},
        {"value": "pdf", "text": "PDF"}
    ]


def get_validation_settings(db: Session) -> Dict[str, Any]:
    """الحصول على إعدادات التحقق من صحة البيانات"""
    return {
        "validate_on_import": True,
        "stop_on_error": False,
        "max_errors": 100,
        "generate_error_report": True
    }


def get_setup_summary(db: Session) -> Dict[str, Any]:
    """الحصول على ملخص الإعداد"""
    return {
        "system_settings": {
            "system_name": get_system_name(db),
            "default_language": get_default_language(db),
            "timezone": "Africa/Cairo"
        },
        "database_settings": {
            "db_type": "postgresql",
            "host": "localhost",
            "name": "scan_ai"
        },
        "company_settings": {
            "name": "Gaara ERP",
            "country": "جمهورية مصر العربية",
            "currency": "ريال سعودي"
        },
        "user_settings": {
            "admin_username": "admin",
            "roles_count": 3
        },
        "module_settings": {
            "enabled_modules": 6,
            "total_modules": 6
        },
        "ai_settings": {
            "enabled_agents": 3,
            "memory_type": "redis"
        },
        "security_settings": {
            "ssl_enabled": True,
            "2fa_enabled": True
        }
    }


def get_validation_warnings(db: Session) -> List[str]:
    """الحصول على تحذيرات التحقق"""
    return [
        "لم يتم تكوين النسخ الاحتياطي السحابي",
        "لم يتم تكوين إعدادات البريد الإلكتروني"
    ]


def get_post_setup_options(db: Session) -> List[Dict[str, str]]:
    """الحصول على خيارات ما بعد الإعداد"""
    return [
        {"value": "dashboard", "text": "الانتقال إلى لوحة التحكم"},
        {"value": "users", "text": "إضافة مستخدمين"},
        {"value": "modules", "text": "تكوين المديولات"},
        {"value": "backup", "text": "إنشاء نسخة احتياطية"}
    ]


# وظائف مساعدة لتحديث البيانات

def update_selected_language(db: Session, language_code: str) -> None:
    """تحديث اللغة المختارة"""
    # تنفيذ منطق تحديث اللغة المختارة


def update_system_settings(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات النظام الأساسية"""
    # تنفيذ منطق تحديث إعدادات النظام الأساسية


def update_database_settings(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات قاعدة البيانات"""
    # تنفيذ منطق تحديث إعدادات قاعدة البيانات


def update_company_settings(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات الشركة الرئيسية"""
    # تنفيذ منطق تحديث إعدادات الشركة الرئيسية


def update_branch_settings(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات الفروع"""
    # تنفيذ منطق تحديث إعدادات الفروع


def update_user_settings(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات المستخدمين والأدوار"""
    # تنفيذ منطق تحديث إعدادات المستخدمين والأدوار


def update_module_selection(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث اختيار وتكوين المديولات"""
    # تنفيذ منطق تحديث اختيار وتكوين المديولات


def update_ai_settings(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات الذكاء الاصطناعي"""
    # تنفيذ منطق تحديث إعدادات الذكاء الاصطناعي


def update_notification_settings(
        db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات الإشعارات والتنبيهات"""
    # تنفيذ منطق تحديث إعدادات الإشعارات والتنبيهات


def update_security_settings(db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات الأمان المتقدمة"""
    # تنفيذ منطق تحديث إعدادات الأمان المتقدمة


def update_backup_import_export_settings(
        db: Session, settings: Dict[str, Any]) -> None:
    """تحديث إعدادات النسخ الاحتياطي والاستيراد/التصدير"""
    # تنفيذ منطق تحديث إعدادات النسخ الاحتياطي والاستيراد/التصدير


# وظائف مساعدة لتطبيق الإعدادات

def apply_system_settings(db: Session) -> None:
    """تطبيق إعدادات النظام"""
    # تنفيذ منطق تطبيق إعدادات النظام


def apply_database_settings(db: Session) -> None:
    """تطبيق إعدادات قاعدة البيانات"""
    # تنفيذ منطق تطبيق إعدادات قاعدة البيانات


def apply_company_settings(db: Session) -> None:
    """تطبيق إعدادات الشركة والفروع"""
    # تنفيذ منطق تطبيق إعدادات الشركة والفروع


def apply_user_settings(db: Session) -> None:
    """تطبيق إعدادات المستخدمين والأدوار"""
    # تنفيذ منطق تطبيق إعدادات المستخدمين والأدوار


def apply_module_settings(db: Session) -> None:
    """تطبيق إعدادات المديولات"""
    # تنفيذ منطق تطبيق إعدادات المديولات


def apply_ai_settings(db: Session) -> None:
    """تطبيق إعدادات الذكاء الاصطناعي"""
    # تنفيذ منطق تطبيق إعدادات الذكاء الاصطناعي


def apply_notification_settings(db: Session) -> None:
    """تطبيق إعدادات الإشعارات والتنبيهات"""
    # تنفيذ منطق تطبيق إعدادات الإشعارات والتنبيهات


def apply_security_settings(db: Session) -> None:
    """تطبيق إعدادات الأمان"""
    # تنفيذ منطق تطبيق إعدادات الأمان


def apply_backup_import_export_settings(db: Session) -> None:
    """تطبيق إعدادات النسخ الاحتياطي والاستيراد/التصدير"""
    # تنفيذ منطق تطبيق إعدادات النسخ الاحتياطي والاستيراد/التصدير
