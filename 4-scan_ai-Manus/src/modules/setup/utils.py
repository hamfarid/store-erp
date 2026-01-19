"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/utils.py
الوصف: أدوات مساعدة لمديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from typing import Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from sqlalchemy import create_engine

# إعداد التسجيل
logger = logging.getLogger(__name__)


def validate_database_connection(
    db_type: str,
    host: str,
    port: int,
    name: str,
    user: str,
    password: str
) -> Dict[str, Any]:
    """
    اختبار اتصال قاعدة البيانات

    Args:
        db_type (str): نوع قاعدة البيانات
        host (str): المضيف
        port (int): المنفذ
        name (str): اسم قاعدة البيانات
        user (str): اسم المستخدم
        password (str): كلمة المرور

    Returns:
        Dict[str, Any]: نتيجة الاختبار
    """
    try:
        # إنشاء سلسلة الاتصال حسب نوع قاعدة البيانات
        if db_type == "postgresql":
            connection_string = f"postgresql://{user}:{password}@{host}:{port}/{name}"
        elif db_type == "mysql":
            connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"
        elif db_type == "sqlite":
            connection_string = f"sqlite:///{name}"
        else:
            return {"success": False, "error": f"نوع قاعدة البيانات غير مدعوم: {db_type}"}

        # محاولة الاتصال
        engine = create_engine(connection_string)
        connection = engine.connect()
        connection.close()

        return {"success": True}

    except Exception as e:
        logger.error(f"فشل اختبار اتصال قاعدة البيانات: {str(e)}")
        return {"success": False, "error": str(e)}


def validate_email_settings(
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    from_email: str,
    use_tls: bool,
    test_recipient: str
) -> Dict[str, Any]:
    """
    اختبار إعدادات البريد الإلكتروني

    Args:
        smtp_server (str): خادم SMTP
        smtp_port (int): منفذ SMTP
        smtp_user (str): اسم مستخدم SMTP
        smtp_password (str): كلمة مرور SMTP
        from_email (str): البريد الإلكتروني المرسل
        use_tls (bool): استخدام TLS
        test_recipient (str): البريد الإلكتروني المستلم للاختبار

    Returns:
        Dict[str, Any]: نتيجة الاختبار
    """
    try:
        # إنشاء رسالة اختبار
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = test_recipient
        message["Subject"] = "اختبار إعدادات البريد الإلكتروني - نظام Scan AI"

        body = """
        هذه رسالة اختبار من نظام Scan AI.

        تم إرسال هذه الرسالة للتحقق من صحة إعدادات البريد الإلكتروني.

        مع تحيات،
        فريق Scan AI
        """

        message.attach(MIMEText(body, "plain"))

        # إنشاء اتصال SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()

        # تفعيل TLS إذا كان مطلوباً
        if use_tls:
            server.starttls()
            server.ehlo()

        # تسجيل الدخول إلى الخادم
        server.login(smtp_user, smtp_password)

        # إرسال الرسالة
        server.sendmail(from_email, test_recipient, message.as_string())

        # إغلاق الاتصال
        server.quit()

        return {"success": True}

    except Exception as e:
        logger.error(f"فشل اختبار إعدادات البريد الإلكتروني: {str(e)}")
        return {"success": False, "error": str(e)}


def generate_setup_report(setup_status: Dict[str, Any]) -> str:
    """
    إنشاء تقرير الإعداد

    Args:
        setup_status (Dict[str, Any]): حالة الإعداد

    Returns:
        str: تقرير الإعداد
    """
    report = """
    # تقرير إعداد نظام Scan AI

    ## حالة الإعداد

    """

    if setup_status.get("is_completed", False):
        report += "- **حالة الإعداد:** مكتمل ✅\n"
    else:
        report += "- **حالة الإعداد:** غير مكتمل ❌\n"

    report += f"- **الخطوة الحالية:** {setup_status.get('current_step', 'غير معروفة')}\n"
    report += f"- **الخطوات المكتملة:** {len(setup_status.get('completed_steps', []))}/{setup_status.get('total_steps', 0)}\n\n"

    report += "## تفاصيل الخطوات\n\n"

    for step in setup_status.get("all_steps", []):
        if step in setup_status.get("completed_steps", []):
            report += f"- {step}: مكتمل ✅\n"
        elif step == setup_status.get("current_step"):
            report += f"- {step}: قيد التنفيذ 🔄\n"
        else:
            report += f"- {step}: قيد الانتظار ⏳\n"

    report += "\n## ملاحظات\n\n"

    if not setup_status.get("is_completed", False):
        report += "- يجب إكمال جميع الخطوات الإلزامية قبل استخدام النظام.\n"
        report += "- يمكن تعديل الإعدادات لاحقاً من خلال لوحة التحكم.\n"
    else:
        report += "- تم إكمال إعداد النظام بنجاح.\n"
        report += "- يمكن الوصول إلى النظام الآن واستخدامه بشكل كامل.\n"

    return report


def validate_security_configuration(security_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    التحقق من صحة إعدادات الأمان

    Args:
        security_settings (Dict[str, Any]): إعدادات الأمان

    Returns:
        Dict[str, Any]: نتيجة التحقق
    """
    warnings = []
    recommendations = []

    # التحقق من استخدام SSL
    if not security_settings.get("use_ssl", False):
        warnings.append("لم يتم تفعيل SSL، مما قد يعرض البيانات للخطر أثناء النقل.")
        recommendations.append("قم بتفعيل SSL وتوفير شهادة SSL صالحة لتأمين الاتصالات.")

    # التحقق من مهلة الجلسة
    session_timeout = security_settings.get("session_timeout", 30)
    if session_timeout > 60:
        warnings.append(f"مهلة الجلسة طويلة جداً ({session_timeout} دقيقة)، مما قد يزيد من مخاطر الأمان.")
        recommendations.append("قم بتقليل مهلة الجلسة إلى 30 دقيقة أو أقل.")

    # التحقق من الحد الأقصى لمحاولات تسجيل الدخول
    max_login_attempts = security_settings.get("max_login_attempts", 5)
    if max_login_attempts > 10:
        warnings.append(f"الحد الأقصى لمحاولات تسجيل الدخول مرتفع جداً ({max_login_attempts})، مما قد يسمح بهجمات القوة الغاشمة.")
        recommendations.append("قم بتقليل الحد الأقصى لمحاولات تسجيل الدخول إلى 5 محاولات.")

    # التحقق من مدة انتهاء صلاحية كلمة المرور
    password_expiry_days = security_settings.get("password_expiry_days", 90)
    if password_expiry_days > 180:
        warnings.append(f"مدة انتهاء صلاحية كلمة المرور طويلة جداً ({password_expiry_days} يوم)، مما قد يقلل من أمان النظام.")
        recommendations.append("قم بتقليل مدة انتهاء صلاحية كلمة المرور إلى 90 يوم أو أقل.")

    # التحقق من تفعيل المصادقة الثنائية
    if not security_settings.get("enable_2fa", False):
        warnings.append("لم يتم تفعيل المصادقة الثنائية، مما يقلل من مستوى الأمان.")
        recommendations.append("قم بتفعيل المصادقة الثنائية لزيادة مستوى الأمان.")

    # التحقق من حماية XSS
    if not security_settings.get("xss_protection", True):
        warnings.append("لم يتم تفعيل حماية XSS، مما قد يعرض النظام لهجمات البرمجة النصية عبر المواقع.")
        recommendations.append("قم بتفعيل حماية XSS لحماية النظام من هجمات البرمجة النصية عبر المواقع.")

    # التحقق من حماية CSRF
    if not security_settings.get("csrf_protection", True):
        warnings.append("لم يتم تفعيل حماية CSRF، مما قد يعرض النظام لهجمات تزوير الطلبات عبر المواقع.")
        recommendations.append("قم بتفعيل حماية CSRF لحماية النظام من هجمات تزوير الطلبات عبر المواقع.")

    # التحقق من حماية حقن SQL
    if not security_settings.get("sql_injection_protection", True):
        warnings.append("لم يتم تفعيل حماية حقن SQL، مما قد يعرض قاعدة البيانات للخطر.")
        recommendations.append("قم بتفعيل حماية حقن SQL لحماية قاعدة البيانات من هجمات الحقن.")

    # التحقق من تحديد معدل الطلبات
    rate_limiting = security_settings.get("rate_limiting", {})
    if not rate_limiting.get("enabled", True):
        warnings.append("لم يتم تفعيل تحديد معدل الطلبات، مما قد يعرض النظام لهجمات الحرمان من الخدمة.")
        recommendations.append("قم بتفعيل تحديد معدل الطلبات لحماية النظام من هجمات الحرمان من الخدمة.")
    elif rate_limiting.get("requests_per_minute", 60) > 100:
        warnings.append(f"معدل الطلبات المسموح به مرتفع جداً ({rate_limiting.get('requests_per_minute', 60)} طلب في الدقيقة)، مما قد يقلل من فعالية الحماية.")
        recommendations.append("قم بتقليل معدل الطلبات المسموح به إلى 60 طلب في الدقيقة أو أقل.")

    # تحديد مستوى الأمان الإجمالي
    security_level = "مرتفع"
    if len(warnings) > 0:
        security_level = "متوسط"
    if len(warnings) > 3:
        security_level = "منخفض"

    return {
        "is_valid": len(warnings) == 0,
        "security_level": security_level,
        "warnings": warnings,
        "recommendations": recommendations
    }


def check_module_dependencies(module_id: str, enabled_modules: list) -> Dict[str, Any]:
    """
    التحقق من اعتماديات المديول

    Args:
        module_id (str): معرف المديول
        enabled_modules (list): قائمة المديولات المفعلة

    Returns:
        Dict[str, Any]: نتيجة التحقق
    """
    # قائمة الاعتماديات لكل مديول
    dependencies = {
        "accounting": ["core"],
        "hr": ["core"],
        "inventory": ["core"],
        "sales": ["core", "inventory"],
        "purchasing": ["core", "inventory"],
        "production": ["core", "inventory"],
        "projects": ["core"],
        "ai_agent": ["core", "memory"],
        "memory": ["core"],
        "internal_diagnosis": ["core"],
        "disease_diagnosis": ["core", "ai_agent"],
        "image_processing": ["core", "ai_agent"],
        "setup": ["core"],
        "activity_log": ["core"],
        "backup": ["core"],
        "security": ["core"],
        "notification": ["core"],
        "system_settings": ["core"],
        "user_management": ["core"],
        "company": ["core"],
        "module_manager": ["core"]
    }

    # الحصول على اعتماديات المديول
    module_dependencies = dependencies.get(module_id, [])

    # التحقق من تفعيل جميع الاعتماديات
    missing_dependencies = [dep for dep in module_dependencies if dep not in enabled_modules]

    return {
        "is_valid": len(missing_dependencies) == 0,
        "missing_dependencies": missing_dependencies
    }


def get_module_integration_points(module_id: str) -> Dict[str, Any]:
    """
    الحصول على نقاط تكامل المديول مع مديول الإعداد

    Args:
        module_id (str): معرف المديول

    Returns:
        Dict[str, Any]: نقاط التكامل
    """
    # نقاط التكامل لكل مديول
    integration_points = {
        "core": {
            "setup": ["system_settings", "database_settings"],
            "config": ["general_settings", "logging_settings"],
            "data": ["initial_data"]
        },
        "accounting": {
            "setup": ["chart_of_accounts", "fiscal_year"],
            "config": ["accounting_settings", "tax_settings"],
            "data": ["opening_balances"]
        },
        "hr": {
            "setup": ["departments", "job_positions"],
            "config": ["hr_settings", "payroll_settings"],
            "data": ["employee_data"]
        },
        "inventory": {
            "setup": ["warehouses", "locations"],
            "config": ["inventory_settings", "uom_settings"],
            "data": ["initial_stock"]
        },
        "sales": {
            "setup": ["sales_teams", "territories"],
            "config": ["sales_settings", "pricing_settings"],
            "data": ["customer_data"]
        },
        "purchasing": {
            "setup": ["purchase_teams"],
            "config": ["purchasing_settings"],
            "data": ["supplier_data"]
        },
        "ai_agent": {
            "setup": ["ai_models", "agent_types"],
            "config": ["ai_settings", "memory_settings"],
            "data": ["initial_knowledge"]
        },
        "memory": {
            "setup": ["memory_stores"],
            "config": ["memory_settings", "retention_settings"],
            "data": ["initial_memories"]
        },
        "internal_diagnosis": {
            "setup": ["diagnosis_models"],
            "config": ["diagnosis_settings"],
            "data": ["baseline_data"]
        },
        "disease_diagnosis": {
            "setup": ["disease_models", "treatment_database"],
            "config": ["diagnosis_settings", "image_processing_settings"],
            "data": ["disease_data", "treatment_data"]
        },
        "image_processing": {
            "setup": ["image_models"],
            "config": ["image_processing_settings"],
            "data": ["reference_images"]
        },
        "activity_log": {
            "setup": ["log_categories"],
            "config": ["logging_settings", "retention_settings"],
            "data": []
        },
        "backup": {
            "setup": ["backup_locations"],
            "config": ["backup_settings", "schedule_settings"],
            "data": []
        },
        "security": {
            "setup": ["security_roles"],
            "config": ["security_settings", "password_policy"],
            "data": ["default_permissions"]
        },
        "user_management": {
            "setup": ["user_roles"],
            "config": ["user_settings", "authentication_settings"],
            "data": ["admin_user"]
        }
    }

    return integration_points.get(module_id, {
        "setup": [],
        "config": [],
        "data": []
    })
