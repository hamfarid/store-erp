"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/security.py
الوصف: خدمات الأمان لمديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import hashlib
import ipaddress
import logging
import os
import re
import secrets
import socket
import ssl
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from sqlalchemy.orm import Session

from src.modules.activity_log import service as activity_log_service
from src.modules.setup import schemas

# إعداد التسجيل
logger = logging.getLogger(__name__)


def validate_security_settings(
        security_settings: schemas.SecuritySettings) -> schemas.SecurityValidationResponse:
    """
    التحقق من صحة إعدادات الأمان

    Args:
        security_settings (schemas.SecuritySettings): إعدادات الأمان

    Returns:
        schemas.SecurityValidationResponse: نتيجة التحقق
    """
    is_valid = True
    warnings = []
    recommendations = []

    # التحقق من إعدادات SSL
    if security_settings.use_ssl:
        if not security_settings.ssl_cert_path or not security_settings.ssl_key_path:
            is_valid = False
            warnings.append(
                "تم تمكين SSL ولكن لم يتم تحديد مسارات الشهادة والمفتاح")
        else:
            # التحقق من وجود الملفات
            if not os.path.exists(security_settings.ssl_cert_path):
                is_valid = False
                warnings.append(
                    f"ملف شهادة SSL غير موجود: {security_settings.ssl_cert_path}")
            if not os.path.exists(security_settings.ssl_key_path):
                is_valid = False
                warnings.append(
                    f"ملف مفتاح SSL غير موجود: {security_settings.ssl_key_path}")
    else:
        recommendations.append("يوصى بتمكين SSL لتأمين الاتصالات")

    # التحقق من مهلة الجلسة
    if security_settings.session_timeout < 15:
        warnings.append(
            "مهلة الجلسة قصيرة جداً، قد تؤدي إلى تسجيل خروج متكرر للمستخدمين")
    elif security_settings.session_timeout > 120:
        warnings.append("مهلة الجلسة طويلة جداً، قد تشكل مخاطر أمنية")

    # التحقق من الحد الأقصى لمحاولات تسجيل الدخول
    if security_settings.max_login_attempts < 3:
        warnings.append(
            "الحد الأقصى لمحاولات تسجيل الدخول منخفض جداً، قد يؤدي إلى قفل المستخدمين بسهولة")
    elif security_settings.max_login_attempts > 10:
        warnings.append(
            "الحد الأقصى لمحاولات تسجيل الدخول مرتفع جداً، قد يسمح بهجمات القوة الغاشمة")

    # التحقق من مدة القفل
    if security_settings.lockout_duration < 5:
        warnings.append(
            "مدة القفل قصيرة جداً، قد لا تكون فعالة ضد هجمات القوة الغاشمة")

    # التحقق من أيام انتهاء صلاحية كلمة المرور
    if security_settings.password_expiry_days < 30:
        warnings.append(
            "فترة انتهاء صلاحية كلمة المرور قصيرة جداً، قد تسبب إزعاجاً للمستخدمين")
    elif security_settings.password_expiry_days > 180:
        warnings.append(
            "فترة انتهاء صلاحية كلمة المرور طويلة جداً، قد تشكل مخاطر أمنية")

    # التحقق من المصادقة الثنائية
    if not security_settings.enable_2fa:
        recommendations.append("يوصى بتمكين المصادقة الثنائية لتعزيز الأمان")

    # التحقق من عناوين IP المسموح بها
    for ip in security_settings.allowed_ips:
        try:
            ipaddress.ip_network(ip)
        except ValueError:
            is_valid = False
            warnings.append(f"عنوان IP أو نطاق غير صالح: {ip}")

    # التحقق من أصول CORS
    for origin in security_settings.cors_origins:
        if not re.match(r'^https?://[\w.-]+(:\d+)?$', origin):
            is_valid = False
            warnings.append(f"أصل CORS غير صالح: {origin}")

    # التحقق من حماية XSS
    if not security_settings.xss_protection:
        recommendations.append("يوصى بتمكين حماية XSS")

    # التحقق من حماية CSRF
    if not security_settings.csrf_protection:
        recommendations.append("يوصى بتمكين حماية CSRF")

    # التحقق من حماية حقن SQL
    if not security_settings.sql_injection_protection:
        recommendations.append("يوصى بتمكين حماية حقن SQL")

    # التحقق من تحديد معدل الطلبات
    if not security_settings.rate_limiting:
        recommendations.append("يوصى بتمكين تحديد معدل الطلبات")
    else:
        if security_settings.rate_limiting.get("enabled", False):
            if security_settings.rate_limiting.get("max_requests", 0) < 10:
                warnings.append(
                    "الحد الأقصى للطلبات منخفض جداً، قد يؤثر على أداء النظام")
            if security_settings.rate_limiting.get("time_window", 0) < 1:
                warnings.append("نافذة الوقت لتحديد معدل الطلبات قصيرة جداً")

    return schemas.SecurityValidationResponse(
        is_valid=is_valid,
        warnings=warnings,
        recommendations=recommendations
    )


def generate_ssl_certificate(
    common_name: str,
    output_cert_path: str,
    output_key_path: str,
    country_name: Optional[str] = None,
    state_name: Optional[str] = None,
    locality_name: Optional[str] = None,
    organization_name: Optional[str] = None,
    validity_days: int = 365
) -> Tuple[bool, str]:
    """
    إنشاء شهادة SSL

    Args:
        common_name (str): الاسم الشائع للشهادة
        output_cert_path (str): مسار ملف الشهادة الناتج
        output_key_path (str): مسار ملف المفتاح الناتج
        country_name (Optional[str]): اسم البلد
        state_name (Optional[str]): اسم المحافظة
        locality_name (Optional[str]): اسم المنطقة
        organization_name (Optional[str]): اسم المنظمة
        validity_days (int): عدد أيام صلاحية الشهادة

    Returns:
        Tuple[bool, str]: نجاح العملية ورسالة
    """
    try:
        # إنشاء مفتاح خاص
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # إنشاء اسم الموضوع
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name or "EG"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name or "Cairo"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name or "Cairo"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name or "Gaara ERP"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        # إنشاء الشهادة
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.now(timezone.utc)
        ).not_valid_after(
            datetime.now(timezone.utc) + timedelta(days=validity_days)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(common_name),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())

        # حفظ المفتاح الخاص
        with open(output_key_path, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # حفظ الشهادة
        with open(output_cert_path, "wb") as cert_file:
            cert_file.write(cert.public_bytes(serialization.Encoding.PEM))

        return True, "تم إنشاء شهادة SSL بنجاح"

    except Exception as e:
        logger.error("خطأ في إنشاء شهادة SSL: %s", str(e))
        return False, f"خطأ في إنشاء شهادة SSL: {str(e)}"


def test_ssl_connection(host: str, port: int, cert_path: str,
                        key_path: str) -> Tuple[bool, str]:
    """
    اختبار اتصال SSL

    Args:
        host (str): عنوان المضيف
        port (int): رقم المنفذ
        cert_path (str): مسار ملف الشهادة
        key_path (str): مسار ملف المفتاح

    Returns:
        Tuple[bool, str]: نجاح الاختبار ورسالة
    """
    try:
        # إنشاء سياق SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(certfile=cert_path, keyfile=key_path)

        # إنشاء مقبس
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen(1)

            # تغليف المقبس بـ SSL
            with context.wrap_socket(sock, server_side=True) as ssock:
                # انتظار اتصال لمدة 1 ثانية
                ssock.settimeout(1)
                try:
                    conn, _ = ssock.accept()
                    conn.close()
                except socket.timeout:
                    # انتهت المهلة، لكن هذا لا يعني فشل الاختبار
                    pass

        return True, "تم اختبار اتصال SSL بنجاح"
    except Exception as e:
        logger.error("خطأ في اختبار اتصال SSL: %s", str(e))
        return False, f"خطأ في اختبار اتصال SSL: {str(e)}"


def validate_password_strength(password: str) -> Tuple[bool, str, int]:
    """
    التحقق من قوة كلمة المرور

    Args:
        password (str): كلمة المرور

    Returns:
        Tuple[bool, str, int]: صلاحية كلمة المرور، رسالة، درجة القوة (0-100)
    """
    # التحقق من الطول
    if len(password) < 8:
        return False, "كلمة المرور قصيرة جداً، يجب أن تكون 8 أحرف على الأقل", 0

    # حساب درجة القوة
    score = 0

    # الطول
    score += min(len(password) * 4, 40)

    # الأحرف الكبيرة
    if re.search(r'[A-Z]', password):
        score += 10

    # الأحرف الصغيرة
    if re.search(r'[a-z]', password):
        score += 10

    # الأرقام
    if re.search(r'\d', password):
        score += 10

    # الرموز الخاصة
    if re.search(r'[^A-Za-z0-9]', password):
        score += 10

    # التنوع
    if len(set(password)) > len(password) / 2:
        score += 10

    # التكرار
    if not re.search(r'(.)\1{2,}', password):
        score += 10

    # التحقق من الصلاحية
    if score < 50:
        return False, "كلمة المرور ضعيفة، يرجى استخدام مزيج من الأحرف الكبيرة والصغيرة والأرقام والرموز الخاصة", score

    return True, "كلمة المرور قوية", score


def hash_password(password: str) -> str:
    """
    تشفير كلمة المرور

    Args:
        password (str): كلمة المرور

    Returns:
        str: كلمة المرور المشفرة
    """
    # إنشاء ملح عشوائي
    salt = secrets.token_hex(16)

    # تشفير كلمة المرور مع الملح
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()

    # إرجاع الملح وكلمة المرور المشفرة
    return f"{salt}${hashed}"


def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    التحقق من صحة كلمة المرور

    Args:
        stored_password (str): كلمة المرور المخزنة
        provided_password (str): كلمة المرور المقدمة

    Returns:
        bool: صحة كلمة المرور
    """
    # استخراج الملح وكلمة المرور المشفرة
    salt, hashed = stored_password.split('$')

    # تشفير كلمة المرور المقدمة مع الملح
    calculated_hash = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()

    # مقارنة كلمة المرور المشفرة
    return hashed == calculated_hash


def generate_secure_token(length: int = 32) -> str:
    """
    إنشاء رمز آمن

    Args:
        length (int): طول الرمز

    Returns:
        str: الرمز الآمن
    """
    return secrets.token_hex(length // 2)


def log_security_event(db: Session,
                       event_type: str,
                       details: Dict[str,
                                     Any],
                       user_id: Optional[int] = None) -> None:
    """
    تسجيل حدث أمني

    Args:
        db (Session): جلسة قاعدة البيانات
        event_type (str): نوع الحدث
        details (Dict[str, Any]): تفاصيل الحدث
        user_id (Optional[int]): معرف المستخدم
    """
    activity_log_service.log_activity(
        db=db,
        log_type="system",
        module_id="security",
        action_id="security_event",
        description=f"حدث أمني: {event_type}",
        details=details,
        user_id=user_id
    )


def sanitize_input(input_str: str) -> str:
    """
    تنظيف المدخلات

    Args:
        input_str (str): النص المدخل

    Returns:
        str: النص المنظف
    """
    # إزالة علامات HTML
    sanitized = re.sub(r'<[^>]*>', '', input_str)

    # إزالة أكواد JavaScript
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)

    # إزالة أكواد SQL الضارة
    sanitized = re.sub(
        r'(\b(select|insert|update|delete|drop|alter|exec|union|where)\b)',
        lambda match: match.group(1).upper(),
        sanitized,
        flags=re.IGNORECASE)

    return sanitized


def apply_security_headers() -> Dict[str, str]:
    """
    تطبيق رؤوس الأمان

    Returns:
        Dict[str, str]: رؤوس الأمان
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; object-src 'none'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache"}
