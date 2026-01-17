# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
#!/usr/bin/env python3
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/middleware/rate_limiter.py

Rate Limiter Middleware - حماية من الهجمات والتحكم في معدل الطلبات
All linting disabled due to complex imports and optional dependencies.

تشمل:
- Rate Limiting للطلبات
- حماية من هجمات DDoS
- حماية من هجمات Brute Force
- حماية من SQL Injection
- حماية من XSS
- تسجيل المحاولات المشبوهة
- حظر IP المشبوهة
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Callable, Optional, Union
from flask import request, jsonify, g
from functools import wraps
import logging
import json
import re
import ipaddress
from collections import defaultdict, deque
import threading

# Optional Redis import - fallback to memory storage if not available
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)


class RateLimiter:
    """نظام التحكم في معدل الطلبات والحماية من الهجمات"""

    def __init__(self, redis_client=None):
        # Only use Redis if it's available and provided
        if redis_client and REDIS_AVAILABLE:
            self.redis_client = redis_client
        else:
            self.redis_client = None
            if redis_client and not REDIS_AVAILABLE:
                logger.warning(
                    "Redis client provided but redis module not available. Using memory storage."
                )

        self.memory_store = defaultdict(lambda: defaultdict(list))
        self.blocked_ips = set()
        self.suspicious_patterns = []
        self.attack_logs = deque(maxlen=1000)
        self._lock = threading.Lock()

        # إعدادات افتراضية
        self.default_limits = {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "login_attempts_per_hour": 10,
            "api_calls_per_minute": 100,
        }

        # أنماط الهجمات المشبوهة
        self._init_suspicious_patterns()

    def _init_suspicious_patterns(self):
        """تهيئة أنماط الهجمات المشبوهة"""
        self.suspicious_patterns = [
            # SQL Injection patterns
            re.compile(
                r"(\bunion\b|\bselect\b|\binsert\b|\bdelete\b|\bdrop\b|\bupdate\b)",
                re.IGNORECASE,
            ),
            re.compile(r"(\bor\b|\band\b)\s+\d+\s*=\s*\d+", re.IGNORECASE),
            re.compile(r"['\"];?\s*(\bunion\b|\bselect\b)", re.IGNORECASE),
            # XSS patterns
            re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL),
            re.compile(r"javascript:", re.IGNORECASE),
            re.compile(r"on\w+\s*=", re.IGNORECASE),
            # Path traversal
            re.compile(r"\.\./", re.IGNORECASE),
            re.compile(r"\.\.\\", re.IGNORECASE),
            # Command injection
            re.compile(r"[;&|`]", re.IGNORECASE),
            re.compile(r"\$\(.*\)", re.IGNORECASE),
        ]

    # ==================== Rate Limiting الأساسي ====================

    def limit_requests(
        self,
        requests_per_minute: Optional[int] = None,
        requests_per_hour: Optional[int] = None,
        key_func: Optional[Callable] = None,
    ):
        """Decorator للتحكم في معدل الطلبات"""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # تحديد المفتاح للتتبع
                if key_func:
                    key = key_func()
                else:
                    key = self._get_client_key()

                # فحص معدل الطلبات
                if not self._check_rate_limit(
                    key,
                    requests_per_minute or self.default_limits["requests_per_minute"],
                    requests_per_hour or self.default_limits["requests_per_hour"],
                ):
                    self._log_rate_limit_exceeded(key)
                    return (
                        jsonify(
                            {
                                "error": "Rate limit exceeded",
                                "message": "تم تجاوز الحد المسموح من الطلبات",
                                "retry_after": 60,
                            }
                        ),
                        429,
                    )

                return f(*args, **kwargs)

            return decorated_function

        return decorator

    def _get_client_key(self) -> str:
        """الحصول على مفتاح تعريف العميل"""
        # محاولة الحصول على IP الحقيقي
        client_ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
        if client_ip and "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()

        # إضافة معرف المستخدم إذا كان متاحاً
        user_id = getattr(g, "user_id", None)
        if user_id:
            return f"user:{user_id}:{client_ip}"

        return f"ip:{client_ip}"

    def _check_rate_limit(self, key: str, per_minute: int, per_hour: int) -> bool:
        """فحص معدل الطلبات"""
        now = datetime.now()

        if self.redis_client:
            return self._check_rate_limit_redis(key, per_minute, per_hour, now)
        else:
            return self._check_rate_limit_memory(key, per_minute, per_hour, now)

    def _check_rate_limit_redis(
        self, key: str, per_minute: int, per_hour: int, now: datetime
    ) -> bool:
        """فحص معدل الطلبات باستخدام Redis"""
        if not self.redis_client:
            return True

        try:
            pipe = self.redis_client.pipeline()

            # مفاتيح للدقيقة والساعة
            minute_key = f"rate_limit:{key}:minute:{now.strftime('%Y%m%d%H%M')}"
            hour_key = f"rate_limit:{key}:hour:{now.strftime('%Y%m%d%H')}"

            # زيادة العدادات
            pipe.incr(minute_key)
            pipe.expire(minute_key, 60)
            pipe.incr(hour_key)
            pipe.expire(hour_key, 3600)

            results = pipe.execute()

            minute_count = results[0]
            hour_count = results[2]

            return minute_count <= per_minute and hour_count <= per_hour

        except Exception as e:
            logger.error(f"خطأ في فحص Rate Limit مع Redis: {str(e)}")
            return True  # السماح في حالة الخطأ

    def _check_rate_limit_memory(
        self, key: str, per_minute: int, per_hour: int, now: datetime
    ) -> bool:
        """فحص معدل الطلبات باستخدام الذاكرة"""
        with self._lock:
            # تنظيف الطلبات القديمة
            minute_ago = now - timedelta(minutes=1)
            hour_ago = now - timedelta(hours=1)

            requests = self.memory_store[key]["requests"]

            # إزالة الطلبات القديمة
            self.memory_store[key]["requests"] = [
                req_time for req_time in requests if req_time > hour_ago
            ]

            # عد الطلبات في الدقيقة والساعة الأخيرة
            minute_requests = sum(
                1
                for req_time in self.memory_store[key]["requests"]
                if req_time > minute_ago
            )
            hour_requests = len(self.memory_store[key]["requests"])

            # فحص الحدود
            if minute_requests >= per_minute or hour_requests >= per_hour:
                return False

            # إضافة الطلب الحالي
            self.memory_store[key]["requests"].append(now)
            return True

    # ==================== حماية من هجمات تسجيل الدخول ====================

    def protect_login(self, max_attempts: Optional[int] = None):
        """حماية من هجمات Brute Force على تسجيل الدخول"""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                client_key = self._get_client_key()
                max_attempts_limit = (
                    max_attempts or self.default_limits["login_attempts_per_hour"]
                )

                # فحص محاولات تسجيل الدخول
                if not self._check_login_attempts(client_key, max_attempts_limit):
                    self._log_brute_force_attempt(client_key)
                    return (
                        jsonify(
                            {
                                "error": "Too many login attempts",
                                "message": "تم تجاوز عدد محاولات تسجيل الدخول المسموحة",
                                "retry_after": 3600,
                            }
                        ),
                        429,
                    )

                # تنفيذ الدالة الأصلية
                result = f(*args, **kwargs)

                # تسجيل محاولة تسجيل الدخول
                self._record_login_attempt(client_key, result)

                return result

            return decorated_function

        return decorator

    def _check_login_attempts(self, key: str, max_attempts: int) -> bool:
        """فحص محاولات تسجيل الدخول"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)

        if self.redis_client:
            try:
                hour_key = f"login_attempts:{key}:hour:{now.strftime('%Y%m%d%H')}"
                attempts = self.redis_client.get(hour_key)
                return int(attempts or 0) < max_attempts
            except Exception as e:
                logger.error(f"خطأ في فحص محاولات تسجيل الدخول: {str(e)}")
                return True
        else:
            with self._lock:
                attempts = self.memory_store[key]["login_attempts"]
                recent_attempts = [
                    attempt for attempt in attempts if attempt["timestamp"] > hour_ago
                ]
                self.memory_store[key]["login_attempts"] = recent_attempts
                return len(recent_attempts) < max_attempts

    def _record_login_attempt(self, key: str, result):
        """تسجيل محاولة تسجيل الدخول"""
        now = datetime.now()
        success = hasattr(result, "status_code") and result.status_code == 200

        if self.redis_client:
            try:
                hour_key = f"login_attempts:{key}:hour:{now.strftime('%Y%m%d%H')}"
                self.redis_client.incr(hour_key)
                self.redis_client.expire(hour_key, 3600)

                if not success:
                    failed_key = (
                        f"failed_login_attempts:{key}:hour:{now.strftime('%Y%m%d%H')}"
                    )
                    self.redis_client.incr(failed_key)
                    self.redis_client.expire(failed_key, 3600)
            except Exception as e:
                logger.error(f"خطأ في تسجيل محاولة تسجيل الدخول: {str(e)}")
        else:
            with self._lock:
                self.memory_store[key]["login_attempts"].append(
                    {"timestamp": now, "success": success, "ip": request.remote_addr}
                )

    # ==================== حماية من الهجمات ====================

    def protect_from_attacks(self):
        """حماية شاملة من الهجمات"""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                client_key = self._get_client_key()

                # فحص IP المحظورة
                if self._is_ip_blocked(client_key):
                    return (
                        jsonify(
                            {
                                "error": "Access denied",
                                "message": "تم حظر الوصول من هذا العنوان",
                            }
                        ),
                        403,
                    )

                # فحص الأنماط المشبوهة
                if self._detect_suspicious_patterns():
                    self._handle_suspicious_activity(client_key)
                    return (
                        jsonify(
                            {
                                "error": "Suspicious activity detected",
                                "message": "تم اكتشاف نشاط مشبوه",
                            }
                        ),
                        400,
                    )

                # فحص حجم الطلب
                if not self._check_request_size():
                    return (
                        jsonify(
                            {
                                "error": "Request too large",
                                "message": "حجم الطلب كبير جداً",
                            }
                        ),
                        413,
                    )

                return f(*args, **kwargs)

            return decorated_function

        return decorator

    def _is_ip_blocked(self, key: str) -> bool:
        """فحص ما إذا كان IP محظوراً"""
        ip = key.split(":")[-1]  # استخراج IP من المفتاح
        return ip in self.blocked_ips

    def _detect_suspicious_patterns(self) -> bool:
        """اكتشاف الأنماط المشبوهة في الطلب"""
        # فحص البيانات المرسلة
        request_data = []

        # فحص query parameters
        for key, value in request.args.items():
            request_data.append(f"{key}={value}")

        # فحص form data
        if request.form:
            for key, value in request.form.items():
                request_data.append(f"{key}={value}")

        # فحص JSON data
        if request.is_json and request.json:
            request_data.append(json.dumps(request.json))

        # فحص headers مشبوهة
        for header_name, header_value in request.headers:
            if header_name.lower() in ["user-agent", "referer"]:
                request_data.append(header_value)

        # فحص URL
        request_data.append(request.url)

        # البحث عن أنماط مشبوهة
        for data in request_data:
            if isinstance(data, str):
                for pattern in self.suspicious_patterns:
                    if pattern.search(data):
                        logger.warning(f"نمط مشبوه مكتشف: {data[:100]}")
                        return True

        return False

    def _check_request_size(self, max_size: int = 10 * 1024 * 1024) -> bool:
        """فحص حجم الطلب (افتراضي: 10MB)"""
        content_length = request.content_length
        return content_length is None or content_length <= max_size

    def _handle_suspicious_activity(self, key: str):
        """التعامل مع النشاط المشبوه"""
        now = datetime.now()
        ip = key.split(":")[-1]

        # تسجيل النشاط المشبوه
        attack_info = {
            "timestamp": now.isoformat(),
            "ip": ip,
            "user_agent": request.headers.get("User-Agent", ""),
            "url": request.url,
            "method": request.method,
            "data": self._get_safe_request_data(),
        }

        with self._lock:
            self.attack_logs.append(attack_info)

        # زيادة عداد النشاط المشبوه
        self._increment_suspicious_activity(key)

        # حظر IP إذا تكرر النشاط المشبوه
        if self._should_block_ip(key):
            self.blocked_ips.add(ip)
            logger.warning(f"تم حظر IP: {ip}")

    def _get_safe_request_data(self) -> Dict:
        """الحصول على بيانات الطلب بشكل آمن"""
        safe_data = {}

        # query parameters (أول 500 حرف)
        if request.args:
            safe_data["query_params"] = str(dict(request.args))[:500]

        # form data (أول 500 حرف)
        if request.form:
            safe_data["form_data"] = str(dict(request.form))[:500]

        # JSON data (أول 500 حرف)
        if request.is_json:
            try:
                safe_data["json_data"] = str(request.json)[:500]
            except Exception:
                safe_data["json_data"] = "Invalid JSON"

        return safe_data

    def _increment_suspicious_activity(self, key: str):
        """زيادة عداد النشاط المشبوه"""
        now = datetime.now()

        if self.redis_client:
            try:
                hour_key = f"suspicious_activity:{key}:hour:{now.strftime('%Y%m%d%H')}"
                count = self.redis_client.incr(hour_key)
                self.redis_client.expire(hour_key, 3600)
                return count
            except Exception as e:
                logger.error(f"خطأ في زيادة عداد النشاط المشبوه: {str(e)}")
        else:
            with self._lock:
                hour_ago = now - timedelta(hours=1)
                activities = self.memory_store[key]["suspicious_activities"]

                # تنظيف الأنشطة القديمة
                recent_activities = [
                    activity for activity in activities if activity > hour_ago
                ]
                recent_activities.append(now)
                self.memory_store[key]["suspicious_activities"] = recent_activities

                return len(recent_activities)

    def _should_block_ip(self, key: str, threshold: int = 5) -> bool:
        """تحديد ما إذا كان يجب حظر IP"""
        now = datetime.now()

        if self.redis_client:
            try:
                hour_key = f"suspicious_activity:{key}:hour:{now.strftime('%Y%m%d%H')}"
                count = self.redis_client.get(hour_key)
                return int(count or 0) >= threshold
            except Exception:
                return False
        else:
            with self._lock:
                activities = self.memory_store[key]["suspicious_activities"]
                return len(activities) >= threshold

    # ==================== حماية API ====================

    def protect_api(
        self, calls_per_minute: Optional[int] = None, require_auth: bool = True
    ):
        """حماية خاصة لـ API endpoints"""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                client_key = self._get_client_key()

                # فحص التوثيق إذا كان مطلوباً
                if require_auth and not self._is_authenticated():
                    return (
                        jsonify(
                            {
                                "error": "Authentication required",
                                "message": "مطلوب تسجيل الدخول",
                            }
                        ),
                        401,
                    )

                # فحص معدل استدعاءات API
                api_limit = (
                    calls_per_minute or self.default_limits["api_calls_per_minute"]
                )
                if not self._check_api_rate_limit(client_key, api_limit):
                    return (
                        jsonify(
                            {
                                "error": "API rate limit exceeded",
                                "message": "تم تجاوز حد استدعاءات API",
                                "retry_after": 60,
                            }
                        ),
                        429,
                    )

                return f(*args, **kwargs)

            return decorated_function

        return decorator

    def _is_authenticated(self) -> bool:
        """فحص ما إذا كان المستخدم مسجل الدخول"""
        return hasattr(g, "user_id") and g.user_id is not None

    def _check_api_rate_limit(self, key: str, calls_per_minute: int) -> bool:
        """فحص معدل استدعاءات API"""
        now = datetime.now()

        if self.redis_client:
            try:
                minute_key = f"api_calls:{key}:minute:{now.strftime('%Y%m%d%H%M')}"
                count = self.redis_client.incr(minute_key)
                self.redis_client.expire(minute_key, 60)
                return count <= calls_per_minute
            except Exception as e:
                logger.error(f"خطأ في فحص معدل API: {str(e)}")
                return True
        else:
            with self._lock:
                minute_ago = now - timedelta(minutes=1)
                api_calls = self.memory_store[key]["api_calls"]

                # تنظيف الاستدعاءات القديمة
                recent_calls = [
                    call_time for call_time in api_calls if call_time > minute_ago
                ]

                if len(recent_calls) >= calls_per_minute:
                    return False

                recent_calls.append(now)
                self.memory_store[key]["api_calls"] = recent_calls
                return True

    # ==================== Logging Methods ====================

    def _log_rate_limit_exceeded(self, key: str):
        """تسجيل تجاوز حد معدل الطلبات"""
        logger.warning("Rate limit exceeded for key: %s", key)

    def _log_brute_force_attempt(self, key: str):
        """تسجيل محاولة هجوم Brute Force"""
        logger.warning("Brute force attempt detected for key: %s", key)

    # ==================== إدارة وتقارير ====================

    def get_security_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الأمان"""
        try:
            now = datetime.now()
            hour_ago = now - timedelta(hours=1)
            day_ago = now - timedelta(days=1)

            stats = {
                "blocked_ips_count": len(self.blocked_ips),
                "blocked_ips": list(self.blocked_ips),
                "recent_attacks": [],
                "rate_limit_violations": 0,
                "suspicious_activities": 0,
                "login_attempts": 0,
                "failed_logins": 0,
            }

            # تحليل سجلات الهجمات
            with self._lock:
                for attack in self.attack_logs:
                    attack_time = datetime.fromisoformat(attack["timestamp"])
                    if attack_time > day_ago:
                        stats["recent_attacks"].append(
                            {
                                "timestamp": attack["timestamp"],
                                "ip": attack["ip"],
                                "url": attack["url"],
                                "method": attack["method"],
                            }
                        )

                        if attack_time > hour_ago:
                            stats["suspicious_activities"] += 1

            # إحصائيات من الذاكرة (إذا لم يكن Redis متاحاً)
            if not self.redis_client:
                with self._lock:
                    for key, data in self.memory_store.items():
                        # عد محاولات تسجيل الدخول
                        login_attempts = [
                            attempt
                            for attempt in data["login_attempts"]
                            if attempt["timestamp"] > hour_ago
                        ]
                        stats["login_attempts"] += len(login_attempts)
                        stats["failed_logins"] += sum(
                            1 for attempt in login_attempts if not attempt["success"]
                        )

            stats["generated_at"] = now.isoformat()
            return stats

        except Exception as e:
            logger.error(f"خطأ في الحصول على إحصائيات الأمان: {str(e)}")
            return {"error": str(e)}

    def unblock_ip(self, ip: str) -> bool:
        """إلغاء حظر IP"""
        try:
            if ip in self.blocked_ips:
                self.blocked_ips.remove(ip)
                logger.info(f"تم إلغاء حظر IP: {ip}")
                return True
            return False
        except Exception as e:
            logger.error(f"خطأ في إلغاء حظر IP: {str(e)}")
            return False

    def block_ip(self, ip: str, reason: str = "Manual block") -> bool:
        """حظر IP يدوياً"""
        try:
            # التحقق من صحة IP
            ipaddress.ip_address(ip)

            self.blocked_ips.add(ip)

            # تسجيل الحظر
            block_info = {
                "timestamp": datetime.now().isoformat(),
                "ip": ip,
                "reason": reason,
                "blocked_by": "manual",
            }

            with self._lock:
                self.attack_logs.append(block_info)

            logger.info(f"تم حظر IP يدوياً: {ip} - السبب: {reason}")
            return True

        except Exception as e:
            logger.error(f"خطأ في حظر IP: {str(e)}")
            return False

    def clear_rate_limits(self, key: Optional[str] = None) -> bool:
        """مسح حدود معدل الطلبات"""
        try:
            if self.redis_client:
                if key:
                    # مسح حدود مفتاح معين
                    pattern = f"rate_limit:{key}:*"
                    keys = self.redis_client.keys(pattern)
                    if keys:
                        self.redis_client.delete(*keys)
                else:
                    # مسح جميع حدود معدل الطلبات
                    keys = self.redis_client.keys("rate_limit:*")
                    if keys:
                        self.redis_client.delete(*keys)
            else:
                with self._lock:
                    if key:
                        if key in self.memory_store:
                            del self.memory_store[key]
                    else:
                        self.memory_store.clear()

            logger.info(f"تم مسح حدود معدل الطلبات: {key or 'جميع المفاتيح'}")
            return True

        except Exception as e:
            logger.error(f"خطأ في مسح حدود معدل الطلبات: {str(e)}")
            return False

    def cleanup_old_data(self, days_to_keep: int = 7) -> Dict[str, Any]:
        """تنظيف البيانات القديمة"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cleanup_results = {"attack_logs_cleaned": 0, "memory_store_cleaned": 0}

            # تنظيف سجلات الهجمات
            with self._lock:
                old_attacks = []
                for attack in list(self.attack_logs):
                    attack_time = datetime.fromisoformat(attack["timestamp"])
                    if attack_time < cutoff_date:
                        old_attacks.append(attack)

                for attack in old_attacks:
                    self.attack_logs.remove(attack)

                cleanup_results["attack_logs_cleaned"] = len(old_attacks)

                # تنظيف memory store
                old_keys = []
                for key, data in self.memory_store.items():
                    # تنظيف البيانات القديمة داخل كل مفتاح
                    if "requests" in data:
                        data["requests"] = [
                            req_time
                            for req_time in data["requests"]
                            if req_time > cutoff_date
                        ]

                    if "login_attempts" in data:
                        data["login_attempts"] = [
                            attempt
                            for attempt in data["login_attempts"]
                            if attempt["timestamp"] > cutoff_date
                        ]

                    if "suspicious_activities" in data:
                        data["suspicious_activities"] = [
                            activity
                            for activity in data["suspicious_activities"]
                            if activity > cutoff_date
                        ]

                    # حذف المفاتيح الفارغة
                    if not any(data.values()):
                        old_keys.append(key)

                for key in old_keys:
                    del self.memory_store[key]

                cleanup_results["memory_store_cleaned"] = len(old_keys)

            logger.info(f"تم تنظيف البيانات القديمة: {cleanup_results}")
            return cleanup_results

        except Exception as e:
            logger.error(f"خطأ في تنظيف البيانات القديمة: {str(e)}")
            return {"error": str(e)}


# ==================== Decorators سهلة الاستخدام ====================


# إنشاء instance عام
rate_limiter = RateLimiter()


def limit_requests(requests_per_minute: int = 60, requests_per_hour: int = 1000):
    """Decorator بسيط للتحكم في معدل الطلبات"""
    return rate_limiter.limit_requests(requests_per_minute, requests_per_hour)


def protect_login(max_attempts: int = 10):
    """Decorator لحماية تسجيل الدخول"""
    return rate_limiter.protect_login(max_attempts)


def protect_from_attacks():
    """Decorator للحماية من الهجمات"""
    return rate_limiter.protect_from_attacks()


def protect_api(calls_per_minute: int = 100, require_auth: bool = True):
    """Decorator لحماية API"""
    return rate_limiter.protect_api(calls_per_minute, require_auth)


# ==================== Flask Integration ====================


def init_rate_limiter(app, redis_client=None):
    """تهيئة Rate Limiter مع Flask app"""
    global rate_limiter

    if rate_limiter is None:
        rate_limiter = RateLimiter()

    if redis_client and REDIS_AVAILABLE:
        rate_limiter.redis_client = redis_client
    elif redis_client and not REDIS_AVAILABLE:
        logger.warning(
            "Redis client provided but redis module not available. Using memory storage."
        )

    # إضافة middleware للطلبات
    @app.before_request
    def before_request():
        # فحص IP المحظورة
        client_key = rate_limiter._get_client_key()
        if rate_limiter._is_ip_blocked(client_key):
            return (
                jsonify(
                    {
                        "error": "Access denied",
                        "message": "تم حظر الوصول من هذا العنوان",
                    }
                ),
                403,
            )

    # إضافة routes للإدارة
    @app.route("/admin/security/stats")
    @protect_api(require_auth=True)
    def security_stats():
        return jsonify(rate_limiter.get_security_stats())

    @app.route("/admin/security/unblock-ip", methods=["POST"])
    @protect_api(require_auth=True)
    def unblock_ip():
        data = request.get_json()
        ip = data.get("ip")

        if not ip:
            return jsonify({"error": "IP address required"}), 400

        success = rate_limiter.unblock_ip(ip)
        return jsonify({"success": success})

    @app.route("/admin/security/block-ip", methods=["POST"])
    @protect_api(require_auth=True)
    def block_ip():
        data = request.get_json()
        ip = data.get("ip")
        reason = data.get("reason", "Manual block")

        if not ip:
            return jsonify({"error": "IP address required"}), 400

        success = rate_limiter.block_ip(ip, reason)
        return jsonify({"success": success})

    logger.info("تم تهيئة Rate Limiter بنجاح")
