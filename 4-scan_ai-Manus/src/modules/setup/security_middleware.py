"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/security_middleware.py
الوصف: وسيط الأمان لمديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import os
import time
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Callable
from fastapi import Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from src.modules.setup import security
from src.modules.activity_log import service as activity_log_service
from src.database import get_db
from src.modules.setup import models

# إعداد التسجيل
logger = logging.getLogger(__name__)

# قائمة مؤقتة لتخزين محاولات الوصول
access_attempts = {}
blocked_ips = {}
request_counts = {}


async def setup_security_middleware(request: Request, call_next: Callable) -> Response:
    """
    وسيط الأمان لمديول الإعداد

    Args:
        request (Request): طلب HTTP
        call_next (Callable): الدالة التالية في سلسلة الوسطاء

    Returns:
        Response: استجابة HTTP
    """
    # الحصول على عنوان IP للطلب
    client_ip = get_client_ip(request)

    # التحقق من حظر عنوان IP
    if is_ip_blocked(client_ip):
        logger.warning("تم رفض الوصول من عنوان IP محظور: %s", client_ip)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "تم حظر الوصول من عنوان IP الخاص بك"}
        )

    # التحقق من تحديد معدل الطلبات
    if not check_rate_limit(client_ip):
        logger.warning("تم تجاوز معدل الطلبات من عنوان IP: %s", client_ip)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "تم تجاوز معدل الطلبات المسموح به"}
        )

    # تطبيق رؤوس الأمان
    response = await call_next(request)
    apply_security_headers(response)

    # تسجيل الطلب في سجل النشاط
    await log_request(request, response)

    return response


def get_client_ip(request: Request) -> str:
    """
    الحصول على عنوان IP للعميل

    Args:
        request (Request): طلب HTTP

    Returns:
        str: عنوان IP للعميل
    """
    # محاولة الحصول على عنوان IP من رأس X-Forwarded-For
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # الحصول على أول عنوان IP في القائمة
        return forwarded_for.split(",")[0].strip()

    # الحصول على عنوان IP من معلومات الاتصال
    client_host = request.client.host if request.client else "127.0.0.1"
    return client_host


def is_ip_blocked(ip: str) -> bool:
    """
    التحقق من حظر عنوان IP

    Args:
        ip (str): عنوان IP

    Returns:
        bool: ما إذا كان عنوان IP محظوراً
    """
    # التحقق من وجود عنوان IP في قائمة العناوين المحظورة
    if ip in blocked_ips:
        block_info = blocked_ips[ip]

        # التحقق من انتهاء مدة الحظر
        if block_info["expires_at"] > datetime.now(timezone.utc):
            return True
        else:
            # إزالة عنوان IP من قائمة العناوين المحظورة
            del blocked_ips[ip]

    return False


def check_rate_limit(ip: str) -> bool:
    """
    التحقق من تحديد معدل الطلبات

    Args:
        ip (str): عنوان IP

    Returns:
        bool: ما إذا كان الطلب ضمن المعدل المسموح به
    """
    # الإعدادات الافتراضية لتحديد معدل الطلبات
    max_requests = 100
    time_window = 60  # ثواني

    # الحصول على الوقت الحالي
    current_time = time.time()

    # تهيئة سجل الطلبات لعنوان IP إذا لم يكن موجوداً
    if ip not in request_counts:
        request_counts[ip] = {"count": 0, "reset_at": current_time + time_window}

    # التحقق من إعادة تعيين العداد
    if current_time > request_counts[ip]["reset_at"]:
        request_counts[ip] = {"count": 0, "reset_at": current_time + time_window}

    # زيادة عدد الطلبات
    request_counts[ip]["count"] += 1

    # التحقق من تجاوز الحد الأقصى
    if request_counts[ip]["count"] > max_requests:
        return False

    return True


def apply_security_headers(response: Response) -> None:
    """
    تطبيق رؤوس الأمان

    Args:
        response (Response): استجابة HTTP
    """
    # الحصول على رؤوس الأمان
    security_headers = security.apply_security_headers()

    # تطبيق رؤوس الأمان
    for header, value in security_headers.items():
        response.headers[header] = value


async def log_request(request: Request, response: Response) -> None:
    """
    تسجيل الطلب في سجل النشاط

    Args:
        request (Request): طلب HTTP
        response (Response): استجابة HTTP
    """
    # الحصول على معلومات الطلب
    client_ip = get_client_ip(request)
    method = request.method
    url = str(request.url)
    status_code = response.status_code
    user_agent = request.headers.get("User-Agent", "")

    # تحديد نوع الحدث
    event_type = "setup_request"
    if status_code >= 400:
        event_type = "setup_error"

    # تسجيل الحدث في سجل النشاط
    try:
        # الحصول على جلسة قاعدة البيانات
        db = next(get_db())

        # تسجيل النشاط - fix parameter names
        await activity_log_service.log_activity(
            db=db,
            log_type="system",
            module_id="setup",
            action_id=event_type,
            description=f"طلب {method} إلى {url}",
            details={
                "client_ip": client_ip,
                "method": method,
                "url": url,
                "status_code": status_code,
                "user_agent": user_agent
            },
            ip_address=client_ip,
            user_agent=user_agent
        )
    except Exception as e:
        logger.error("خطأ في تسجيل الطلب: %s", str(e))


def block_ip(ip: str, duration: int = 30) -> None:
    """
    حظر عنوان IP

    Args:
        ip (str): عنوان IP
        duration (int): مدة الحظر بالدقائق
    """
    # إضافة عنوان IP إلى قائمة العناوين المحظورة
    blocked_ips[ip] = {
        "blocked_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=duration),
        "reason": "تجاوز الحد الأقصى لمحاولات الوصول"
    }

    logger.warning("تم حظر عنوان IP %s لمدة %s دقيقة", ip, duration)


def track_login_attempt(ip: str, username: str, success: bool) -> bool:
    """
    تتبع محاولة تسجيل الدخول

    Args:
        ip (str): عنوان IP
        username (str): اسم المستخدم
        success (bool): نجاح محاولة تسجيل الدخول

    Returns:
        bool: ما إذا كان يجب حظر عنوان IP
    """
    # الإعدادات الافتراضية لقفل الحساب
    max_attempts = 5
    lockout_duration = 30  # دقائق

    # إعادة تعيين محاولات الوصول في حالة النجاح
    if success:
        if ip in access_attempts and username in access_attempts[ip]:
            del access_attempts[ip][username]
        return False

    # تهيئة سجل محاولات الوصول لعنوان IP إذا لم يكن موجوداً
    if ip not in access_attempts:
        access_attempts[ip] = {}

    # تهيئة سجل محاولات الوصول لاسم المستخدم إذا لم يكن موجوداً
    if username not in access_attempts[ip]:
        access_attempts[ip][username] = {"count": 0, "last_attempt": datetime.utcnow()}

    # زيادة عدد محاولات الوصول
    access_attempts[ip][username]["count"] += 1
    access_attempts[ip][username]["last_attempt"] = datetime.utcnow()

    # التحقق من تجاوز الحد الأقصى
    if access_attempts[ip][username]["count"] >= max_attempts:
        # حظر عنوان IP
        block_ip(ip, lockout_duration)
        return True

    return False


def sanitize_request_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    تنظيف بيانات الطلب

    Args:
        data (Dict[str, Any]): بيانات الطلب

    Returns:
        Dict[str, Any]: بيانات الطلب المنظفة
    """
    # نسخ البيانات
    sanitized_data = {}

    # تنظيف كل قيمة
    for key, value in data.items():
        if isinstance(value, str):
            # تنظيف النص
            sanitized_data[key] = security.sanitize_input(value)
        elif isinstance(value, dict):
            # تنظيف القاموس بشكل متكرر
            sanitized_data[key] = sanitize_request_data(value)
        elif isinstance(value, list):
            # تنظيف القائمة بشكل متكرر
            sanitized_data[key] = [
                sanitize_request_data(item) if isinstance(item, dict) else
                security.sanitize_input(item) if isinstance(item, str) else
                item
                for item in value
            ]
        else:
            # نسخ القيمة كما هي
            sanitized_data[key] = value

    return sanitized_data


def validate_setup_token(token: str) -> bool:
    """
    التحقق من صحة رمز الإعداد

    Args:
        token (str): رمز الإعداد

    Returns:
        bool: صحة رمز الإعداد
    """
    # الحصول على جلسة قاعدة البيانات
    db = next(get_db())

    # البحث عن حالة الإعداد
    setup_status = db.query(models.SetupStatus).first()

    # التحقق من وجود حالة الإعداد
    if not setup_status:
        return False

    # التحقق من صحة رمز الإعداد
    if setup_status.setup_token != token:
        return False

    # التحقق من انتهاء صلاحية رمز الإعداد
    if setup_status.token_expires_at < datetime.utcnow():
        return False

    return True


def setup_cors_middleware(app, allowed_origins: List[str] = None):
    """
    إعداد وسيط CORS

    Args:
        app: تطبيق FastAPI
        allowed_origins (List[str]): قائمة الأصول المسموح بها
    """
    if allowed_origins is None:
        allowed_origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
        max_age=600
    )


def setup_trusted_hosts_middleware(app, allowed_hosts: List[str] = None):
    """
    إعداد وسيط المضيفين الموثوقين

    Args:
        app: تطبيق FastAPI
        allowed_hosts (List[str]): قائمة المضيفين المسموح بهم
    """
    if allowed_hosts is None:
        allowed_hosts = ["*"]

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts
    )


def validate_ssl_config(cert_path: str, key_path: str) -> Dict[str, Any]:
    """
    التحقق من صحة تكوين SSL

    Args:
        cert_path (str): مسار ملف الشهادة
        key_path (str): مسار ملف المفتاح

    Returns:
        Dict[str, Any]: نتيجة التحقق
    """
    result = {
        "is_valid": False,
        "errors": [],
        "warnings": [],
        "expiry_date": None
    }

    # التحقق من وجود الملفات
    if not os.path.exists(cert_path):
        result["errors"].append(f"ملف شهادة SSL غير موجود: {cert_path}")

    if not os.path.exists(key_path):
        result["errors"].append(f"ملف مفتاح SSL غير موجود: {key_path}")

    # إذا كانت هناك أخطاء، إرجاع النتيجة
    if result["errors"]:
        return result

    try:
        # قراءة ملف الشهادة
        with open(cert_path, "rb") as cert_file:
            cert_data = cert_file.read()

        # قراءة ملف المفتاح
        with open(key_path, "rb") as key_file:
            key_data = key_file.read()

        # تحليل الشهادة - imports already moved to top
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        # التحقق من تاريخ انتهاء الصلاحية
        expiry_date = cert.not_valid_after
        result["expiry_date"] = expiry_date

        # التحقق من قرب انتهاء الصلاحية
        if expiry_date < datetime.now(timezone.utc) + timedelta(days=30):
            result["warnings"].append(f"شهادة SSL ستنتهي صلاحيتها قريباً: {expiry_date}")

        # التحقق من توافق المفتاح مع الشهادة - import already moved to top
        private_key = serialization.load_pem_private_key(
            key_data,
            password=None,
            backend=default_backend()
        )

        # التحقق من توافق المفتاح العام للشهادة مع المفتاح الخاص
        cert_public_key = cert.public_key().public_numbers()
        private_key_public_numbers = private_key.public_key().public_numbers()

        if cert_public_key != private_key_public_numbers:
            result["errors"].append("المفتاح الخاص لا يتوافق مع الشهادة")

        # إذا لم تكن هناك أخطاء، تعيين is_valid إلى True
        if not result["errors"]:
            result["is_valid"] = True

        return result
    except Exception as e:
        result["errors"].append(f"خطأ في التحقق من تكوين SSL: {str(e)}")
        return result
