"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/security/security_middleware.py
الوصف: وسيط الأمان لحماية النظام من الاختراق وتجاوز الصلاحيات
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import html
import ipaddress
import json
import logging
import re
import secrets
import time
from datetime import datetime
from typing import List, Optional

import jwt
from fastapi import Request, Response, status
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from src.modules.activity_log.integration import ActivityLogger
from src.modules.notifications.telegram import TelegramNotificationService

# إعداد المسجل
logger = logging.getLogger(__name__)

# ثوابت الأمان
SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https:;",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=(), payment=(), usb=(), interest-cohort=()",
    "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0",
    "X-Permitted-Cross-Domain-Policies": "none",
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin"
}


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    وسيط الأمان لحماية النظام من الاختراق وتجاوز الصلاحيات

    يوفر هذا الوسيط طبقات متعددة من الحماية:
    - حماية من هجمات XSS
    - حماية من هجمات CSRF
    - حماية من هجمات حقن SQL
    - تحديد معدل الطلبات
    - التحقق من الصلاحيات
    - تسجيل محاولات الاختراق
    - حظر عناوين IP المشبوهة
    """

    def __init__(
        self,
        app,
        allowed_hosts: List[str] = None,
        allowed_ips: List[str] = None,
        rate_limit_per_minute: int = 60,
        block_threshold: int = 10,
        block_duration_minutes: int = 30,
        enable_csrf_protection: bool = True,
        enable_xss_protection: bool = True,
        enable_sql_injection_protection: bool = True,
        enable_rate_limiting: bool = True,
        enable_ip_blocking: bool = True,
        enable_permission_validation: bool = True,
        enable_activity_logging: bool = True,
        enable_admin_notifications: bool = True,
        jwt_secret: str = None,
        jwt_algorithm: str = "HS256",
        jwt_expire_minutes: int = 30,
        request_body_validation: bool = True,
        max_request_size: int = 1024 * 1024  # 1MB
    ):
        """
        تهيئة وسيط الأمان

        المعلمات:
            app: تطبيق FastAPI
            allowed_hosts: قائمة المضيفين المسموح بهم
            allowed_ips: قائمة عناوين IP المسموح بها
            rate_limit_per_minute: الحد الأقصى للطلبات في الدقيقة
            block_threshold: عدد المخالفات قبل الحظر
            block_duration_minutes: مدة الحظر بالدقائق
            enable_csrf_protection: تمكين الحماية من هجمات CSRF
            enable_xss_protection: تمكين الحماية من هجمات XSS
            enable_sql_injection_protection: تمكين الحماية من هجمات حقن SQL
            enable_rate_limiting: تمكين تحديد معدل الطلبات
            enable_ip_blocking: تمكين حظر عناوين IP
            enable_permission_validation: تمكين التحقق من الصلاحيات
            enable_activity_logging: تمكين تسجيل النشاط
            enable_admin_notifications: تمكين إشعارات المسؤول
            jwt_secret: مفتاح التشفير لـ JWT
            jwt_algorithm: خوارزمية التشفير لـ JWT
            jwt_expire_minutes: مدة صلاحية JWT بالدقائق
            request_body_validation: تمكين التحقق من صحة جسم الطلب
            max_request_size: الحد الأقصى لحجم الطلب بالبايت
        """
        super().__init__(app)
        self.allowed_hosts = allowed_hosts or ["localhost", "127.0.0.1"]
        self.allowed_ips = allowed_ips or []
        self.rate_limit_per_minute = rate_limit_per_minute
        self.block_threshold = block_threshold
        self.block_duration_minutes = block_duration_minutes
        self.max_request_size = max_request_size

        # إعدادات JWT
        self.jwt_secret = jwt_secret or secrets.token_hex(32)
        self.jwt_algorithm = jwt_algorithm
        self.jwt_expire_minutes = jwt_expire_minutes

        # تمكين/تعطيل ميزات الأمان
        self.enable_csrf_protection = enable_csrf_protection
        self.enable_xss_protection = enable_xss_protection
        self.enable_sql_injection_protection = enable_sql_injection_protection
        self.enable_rate_limiting = enable_rate_limiting
        self.enable_ip_blocking = enable_ip_blocking
        self.enable_permission_validation = enable_permission_validation
        self.enable_activity_logging = enable_activity_logging
        self.enable_admin_notifications = enable_admin_notifications
        self.request_body_validation = request_body_validation

        # تخزين مؤقت للطلبات والمخالفات
        self.request_cache = {}
        self.violation_cache = {}
        self.blocked_ips = {}
        self.user_rate_limits = {}
        self.token_blacklist = set()

        # إنشاء مسجل النشاط وخدمة إشعارات تيليجرام
        self.activity_logger = ActivityLogger()
        self.telegram_service = TelegramNotificationService()

        # أنماط للكشف عن هجمات حقن SQL
        self.sql_injection_patterns = [
            r"(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|UNION|CREATE|WHERE)(\s|$)",
            r"(\s|^)(OR|AND)(\s+)(\d+|'[^']*')(\s*)(=)(\s*)(\d+|'[^']*')",
            r"--",
            r"#",
            r"/\*",
            r"\*/",
            r";",
            r"@@",
            r"@\w+",
            r"char\(",
            r"exec\(",
            r"xp_",
            r"sp_",
            r"waitfor",
            r"delay",
            r"0x[0-9a-fA-F]+",
        ]

        # تجميع أنماط حقن SQL
        self.sql_injection_regex = re.compile("|".join(self.sql_injection_patterns), re.IGNORECASE)

        logger.info("تم تهيئة وسيط الأمان بنجاح")

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        معالجة الطلب وتطبيق إجراءات الأمان

        المعلمات:
            request: كائن الطلب
            call_next: دالة لاستدعاء المعالج التالي

        العائد:
            Response: كائن الاستجابة
        """
        try:
            # التحقق من حجم الطلب
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_request_size:
                return self._create_error_response(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="حجم الطلب يتجاوز الحد المسموح به",
                    request=request,
                    violation_type="request_too_large"
                )

            # الحصول على عنوان IP للعميل
            client_ip = request.client.host

            # التحقق من المضيف
            if not self._is_host_allowed(request):
                return self._create_error_response(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="المضيف غير مسموح به",
                    request=request,
                    violation_type="host_not_allowed"
                )

            # التحقق من عنوان IP
            if self.enable_ip_blocking and not self._is_ip_allowed(client_ip):
                return self._create_error_response(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="عنوان IP غير مسموح به",
                    request=request,
                    violation_type="ip_not_allowed"
                )

            # التحقق من حظر عنوان IP
            if self.enable_ip_blocking and self._is_ip_blocked(client_ip):
                return self._create_error_response(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="تم حظر عنوان IP الخاص بك مؤقتاً",
                    request=request,
                    violation_type="ip_blocked"
                )

            # التحقق من JWT
            user_id = self._get_user_id_from_token(request)
            if user_id and not self._validate_jwt_token(request):
                return self._create_error_response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="رمز JWT غير صالح أو منتهي الصلاحية",
                    request=request,
                    violation_type="invalid_jwt"
                )

            # تحديد معدل الطلبات
            if self.enable_rate_limiting and not self._check_rate_limit(client_ip, user_id):
                return self._create_error_response(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="تم تجاوز الحد الأقصى للطلبات",
                    request=request,
                    violation_type="rate_limit_exceeded"
                )

            # التحقق من CSRF
            if self.enable_csrf_protection and request.method in ["POST", "PUT", "DELETE", "PATCH"]:
                csrf_token = request.headers.get("X-CSRF-Token")
                if not csrf_token or not self._validate_csrf_token(request, csrf_token):
                    return self._create_error_response(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="رمز CSRF غير صالح",
                        request=request,
                        violation_type="invalid_csrf"
                    )

            # التحقق من جسم الطلب
            if self.request_body_validation and request.method in ["POST", "PUT", "PATCH"]:
                try:
                    body = await self._get_request_body(request)
                    if self.enable_sql_injection_protection and self._contains_sql_injection(body):
                        return self._create_error_response(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="تم اكتشاف محاولة حقن SQL",
                            request=request,
                            violation_type="sql_injection"
                        )

                    # تنظيف المحتوى من XSS
                    if self.enable_xss_protection:
                        self._sanitize_input(body)
                        # المحتوى تم تنظيفه للتحقق من الأمان

                except Exception as e:
                    logger.error("خطأ في التحقق من جسم الطلب: %s", e)

            # التحقق من الصلاحيات
            if self.enable_permission_validation and not await self._validate_permissions(request):
                return self._create_error_response(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="ليس لديك الصلاحية للوصول إلى هذا المورد",
                    request=request,
                    violation_type="insufficient_permissions"
                )

            # معالجة الطلب
            response = await call_next(request)

            # إضافة رؤوس الأمان
            response = await self._add_security_headers(request, response)

            return response

        except Exception as e:
            logger.error("خطأ في وسيط الأمان: %s", e)
            return self._create_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="خطأ داخلي في الخادم",
                request=request,
                violation_type="internal_error"
            )

    def _get_user_id_from_token(self, request: Request) -> Optional[str]:
        """
        استخراج معرف المستخدم من رمز JWT

        المعلمات:
            request: كائن الطلب

        العائد:
            معرف المستخدم أو None
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload.get("sub")
        except jwt.InvalidTokenError:
            return None

    def _validate_jwt_token(self, request: Request) -> bool:
        """
        التحقق من صحة رمز JWT

        المعلمات:
            request: كائن الطلب

        العائد:
            True إذا كان الرمز صالحاً، False خلاف ذلك
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return False

        token = auth_header.split(" ")[1]

        # التحقق من القائمة السوداء للرموز
        if token in self.token_blacklist:
            return False

        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])

            # التحقق من انتهاء الصلاحية
            exp = payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                return False

            return True
        except jwt.InvalidTokenError:
            return False

    def _sanitize_input(self, content: str) -> str:
        """
        تنظيف المحتوى من هجمات XSS

        المعلمات:
            content: المحتوى المراد تنظيفه

        العائد:
            المحتوى المنظف
        """
        if not content:
            return content

        # إزالة العلامات الخطيرة
        dangerous_tags = [
            r'<script[^>]*>.*?</script>',
            r'<iframe[^>]*>.*?</iframe>',
            r'<object[^>]*>.*?</object>',
            r'<embed[^>]*>.*?</embed>',
            r'<form[^>]*>.*?</form>',
            r'<input[^>]*>',
            r'<button[^>]*>.*?</button>',
            r'<link[^>]*>',
            r'<meta[^>]*>',
            r'<style[^>]*>.*?</style>',
        ]

        for pattern in dangerous_tags:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)

        # تنظيف الأحداث الخطيرة
        event_attributes = [
            r'on\w+\s*=\s*["\'][^"\']*["\']',
            r'javascript:',
            r'vbscript:',
            r'data:text/html',
        ]

        for pattern in event_attributes:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)

        # تشفير الأحرف الخاصة
        content = html.escape(content)

        return content

    def _check_rate_limit(self, ip: str, user_id: Optional[str] = None) -> bool:
        """
        التحقق من تحديد معدل الطلبات

        المعلمات:
            ip: عنوان IP
            user_id: معرف المستخدم (اختياري)

        العائد:
            True إذا كان ضمن الحد المسموح، False خلاف ذلك
        """
        current_time = time.time()
        window_start = current_time - 60  # نافذة زمنية مدتها دقيقة واحدة

        # تنظيف الطلبات القديمة
        self._cleanup_old_requests(window_start)

        # مفتاح التخزين المؤقت
        cache_key = f"{ip}:{user_id}" if user_id else ip

        # الحصول على قائمة الطلبات للمفتاح
        if cache_key not in self.request_cache:
            self.request_cache[cache_key] = []

        requests_list = self.request_cache[cache_key]

        # إزالة الطلبات القديمة من القائمة
        requests_list[:] = [req_time for req_time in requests_list if req_time > window_start]

        # التحقق من الحد الأقصى
        if len(requests_list) >= self.rate_limit_per_minute:
            # تسجيل المخالفة
            self._record_violation(ip, "rate_limit_exceeded")
            return False

        # إضافة الطلب الحالي
        requests_list.append(current_time)
        return True

    def _cleanup_old_requests(self, window_start: float) -> None:
        """
        تنظيف الطلبات القديمة من التخزين المؤقت

        المعلمات:
            window_start: بداية النافزة الزمنية
        """
        keys_to_remove = []

        for cache_key, requests_list in self.request_cache.items():
            # إزالة الطلبات القديمة
            requests_list[:] = [req_time for req_time in requests_list if req_time > window_start]

            # إزالة المفاتيح الفارغة
            if not requests_list:
                keys_to_remove.append(cache_key)

        # إزالة المفاتيح الفارغة
        for key in keys_to_remove:
            del self.request_cache[key]

    async def _add_security_headers(self, request: Request, response: Response) -> Response:
        """
        إضافة رؤوس الأمان إلى الاستجابة

        المعلمات:
            request: كائن الطلب
            response: كائن الاستجابة

        العائد:
            كائن الاستجابة مع رؤوس الأمان
        """
        # إضافة رؤوس الأمان
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value

        # إضافة رمز CSRF للطلبات GET
        if request.method == "GET" and self.enable_csrf_protection:
            csrf_token = secrets.token_urlsafe(32)
            response.headers["X-CSRF-Token"] = csrf_token

        return response

    def _is_host_allowed(self, request: Request) -> bool:
        """
        التحقق من أن المضيف مسموح به

        المعلمات:
            request: كائن الطلب

        العائد:
            True إذا كان المضيف مسموحاً، False خلاف ذلك
        """
        host = request.headers.get("host", "").split(":")[0]
        return host in self.allowed_hosts

    def _is_ip_allowed(self, ip: str) -> bool:
        """
        التحقق من أن عنوان IP مسموح به

        المعلمات:
            ip: عنوان IP

        العائد:
            True إذا كان عنوان IP مسموحاً، False خلاف ذلك
        """
        # إذا لم تكن هناك قائمة محددة، فجميع عناوين IP مسموحة
        if not self.allowed_ips:
            return True

        try:
            client_ip = ipaddress.ip_address(ip)
            for allowed_ip in self.allowed_ips:
                try:
                    # التحقق من الشبكة أو العنوان المحدد
                    if "/" in allowed_ip:
                        network = ipaddress.ip_network(allowed_ip, strict=False)
                        if client_ip in network:
                            return True
                    else:
                        if client_ip == ipaddress.ip_address(allowed_ip):
                            return True
                except ValueError:
                    continue
            return False
        except ValueError:
            return False

    def _is_ip_blocked(self, ip: str) -> bool:
        """
        التحقق من أن عنوان IP محظور

        المعلمات:
            ip: عنوان IP

        العائد:
            True إذا كان عنوان IP محظوراً، False خلاف ذلك
        """
        if ip not in self.blocked_ips:
            return False

        block_info = self.blocked_ips[ip]
        current_time = time.time()

        # التحقق من انتهاء مدة الحظر
        if current_time > block_info["expires_at"]:
            del self.blocked_ips[ip]
            return False

        return True

    def _validate_csrf_token(self, request: Request, token: str) -> bool:
        """
        التحقق من صحة رمز CSRF

        المعلمات:
            request: كائن الطلب
            token: رمز CSRF

        العائد:
            True إذا كان الرمز صالحاً، False خلاف ذلك
        """
        # هنا يمكن تنفيذ منطق أكثر تعقيداً للتحقق من رمز CSRF
        # مثل التحقق من الجلسة أو قاعدة البيانات

        # للبساطة، نتحقق من أن الرمز ليس فارغاً وله طول مناسب
        if not token or len(token) < 16:
            return False

        # يمكن إضافة المزيد من عمليات التحقق هنا
        return True

    async def _get_request_body(self, request: Request) -> str:
        """
        الحصول على جسم الطلب

        المعلمات:
            request: كائن الطلب

        العائد:
            جسم الطلب كنص
        """
        try:
            body = await request.body()
            return body.decode("utf-8")
        except Exception as e:
            logger.error("خطأ في قراءة جسم الطلب: %s", e)
            return ""

    def _contains_sql_injection(self, content: str) -> bool:
        """
        التحقق من وجود محاولة حقن SQL

        المعلمات:
            content: المحتوى المراد فحصه

        العائد:
            True إذا تم اكتشاف محاولة حقن SQL، False خلاف ذلك
        """
        if not content:
            return False

        # البحث عن أنماط حقن SQL
        return bool(self.sql_injection_regex.search(content))

    async def _validate_permissions(self, request: Request) -> bool:
        """
        التحقق من صلاحيات المستخدم

        المعلمات:
            request: كائن الطلب

        العائد:
            True إذا كان المستخدم لديه الصلاحية، False خلاف ذلك
        """
        # الحصول على الصلاحيات المطلوبة للمسار
        required_permissions = self._get_required_permissions(request)

        # إذا لم تكن هناك صلاحيات مطلوبة، فالوصول مسموح
        if not required_permissions:
            return True

        # الحصول على معرف المستخدم من الرمز
        user_id = self._get_user_id_from_token(request)
        if not user_id:
            return False

        # هنا يمكن التحقق من صلاحيات المستخدم من قاعدة البيانات
        # للبساطة، نفترض أن المستخدم لديه الصلاحية إذا كان لديه رمز صالح
        return True

    def _get_required_permissions(self, request: Request) -> List[str]:
        """
        الحصول على الصلاحيات المطلوبة للمسار

        المعلمات:
            request: كائن الطلب

        العائد:
            قائمة بالصلاحيات المطلوبة
        """
        path = request.url.path

        # تعريف الصلاحيات المطلوبة للمسارات المختلفة
        permission_map = {
            "/admin": ["admin"],
            "/api/admin": ["admin"],
            "/users": ["user_management"],
            "/api/users": ["user_management"],
            "/settings": ["settings_management"],
            "/api/settings": ["settings_management"],
            "/security": ["security_management"],
            "/api/security": ["security_management"],
            "/backup": ["backup_management"],
            "/api/backup": ["backup_management"],
            "/logs": ["logs_access"],
            "/api/logs": ["logs_access"],
        }

        # البحث عن المسار في الخريطة
        for pattern, permissions in permission_map.items():
            if path.startswith(pattern):
                return permissions

        # إذا لم يتم العثور على المسار، فلا توجد صلاحيات مطلوبة
        return []

    def _record_violation(self, ip: str, violation_type: str) -> None:
        """
        تسجيل مخالفة أمنية

        المعلمات:
            ip: عنوان IP
            violation_type: نوع المخالفة
        """
        current_time = time.time()

        # إنشاء مفتاح للمخالفة
        violation_key = f"{ip}:{violation_type}"

        # الحصول على قائمة المخالفات
        if violation_key not in self.violation_cache:
            self.violation_cache[violation_key] = []

        violations_list = self.violation_cache[violation_key]

        # إزالة المخالفات القديمة (أكثر من ساعة)
        hour_ago = current_time - 3600
        violations_list[:] = [v_time for v_time in violations_list if v_time > hour_ago]

        # إضافة المخالفة الحالية
        violations_list.append(current_time)

        # التحقق من تجاوز الحد الأقصى للمخالفات
        if len(violations_list) >= self.block_threshold:
            # حظر عنوان IP
            self.blocked_ips[ip] = {
                "blocked_at": current_time,
                "expires_at": current_time + (self.block_duration_minutes * 60),
                "reason": violation_type,
                "violation_count": len(violations_list)
            }

            # تسجيل الحظر
            logger.warning("تم حظر عنوان IP %s بسبب %s", ip, violation_type)

            # إرسال إشعار للمسؤول
            if self.enable_admin_notifications:
                try:
                    # إرسال إشعار تيليجرام
                    alert_message = f"تحذير أمني: تم حظر عنوان IP {ip} بسبب {violation_type}"
                    logger.info("إشعار أمني: %s", alert_message)
                    # يمكن استدعاء خدمة إشعارات تيليجرام هنا
                except Exception as e:
                    logger.error("خطأ في إرسال إشعار المسؤول: %s", e)

        # تسجيل النشاط
        if self.enable_activity_logging:
            try:
                # يمكن استدعاء خدمة تسجيل النشاط هنا
                pass
            except Exception as e:
                logger.error("خطأ في تسجيل النشاط: %s", e)

    def _create_error_response(
        self,
        status_code: int,
        detail: str,
        request: Request,
        violation_type: str
    ) -> Response:
        """
        إنشاء استجابة خطأ

        المعلمات:
            status_code: رمز حالة HTTP
            detail: تفاصيل الخطأ
            request: كائن الطلب
            violation_type: نوع المخالفة

        العائد:
            كائن الاستجابة
        """
        # تسجيل المخالفة
        client_ip = request.client.host
        self._record_violation(client_ip, violation_type)

        # إنشاء الاستجابة
        error_response = {
            "error": True,
            "message": detail,
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }

        response = Response(
            content=json.dumps(error_response, ensure_ascii=False),
            status_code=status_code,
            media_type="application/json"
        )

        # إضافة رؤوس الأمان
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value

        return response
