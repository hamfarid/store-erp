"""
نظام التخزين المؤقت المتقدم
Advanced Caching System
"""

import time
from typing import Any, Optional
from functools import wraps


class AdvancedCache:
    """نظام تخزين مؤقت متقدم في الذاكرة"""

    def __init__(self):
        self._cache = {}
        self._timestamps = {}
        self._access_count = {}

    def set(self, key: str, value: Any, ttl: int = 3600):
        """حفظ قيمة في التخزين المؤقت"""
        self._cache[key] = value
        self._timestamps[key] = time.time() + ttl
        self._access_count[key] = 0

    def get(self, key: str) -> Optional[Any]:
        """جلب قيمة من التخزين المؤقت"""
        if key not in self._cache:
            return None

        # فحص انتهاء الصلاحية
        if time.time() > self._timestamps.get(key, 0):
            self.delete(key)
            return None

        self._access_count[key] += 1
        return self._cache[key]

    def delete(self, key: str):
        """حذف قيمة من التخزين المؤقت"""
        self._cache.pop(key, None)
        self._timestamps.pop(key, None)
        self._access_count.pop(key, None)

    def clear(self):
        """مسح جميع البيانات المؤقتة"""
        self._cache.clear()
        self._timestamps.clear()
        self._access_count.clear()

    def get_stats(self):
        """إحصائيات التخزين المؤقت"""
        total_items = len(self._cache)
        total_access = sum(self._access_count.values())

        return {
            "total_items": total_items,
            "total_access": total_access,
            "memory_usage": len(str(self._cache)),
            "most_accessed": (
                max(self._access_count.items(), key=lambda x: x[1])
                if self._access_count
                else None
            ),
        }


# إنشاء instance عام
cache = AdvancedCache()


def cached(ttl: int = 3600, key_prefix: str = ""):
    """decorator للتخزين المؤقت التلقائي"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # إنشاء مفتاح فريد
            cache_key = f"{key_prefix}{func.__name__}_{hash(str(args) + str(kwargs))}"

            # محاولة جلب من التخزين المؤقت
            result = cache.get(cache_key)
            if result is not None:
                return result

            # تنفيذ الدالة وحفظ النتيجة
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


def cache_api_response(endpoint: str, data: Any, ttl: int = 300):
    """تخزين مؤقت لاستجابات API"""
    cache.set(f"api_{endpoint}", data, ttl)


def get_cached_api_response(endpoint: str) -> Optional[Any]:
    """جلب استجابة API من التخزين المؤقت"""
    return cache.get(f"api_{endpoint}")


class LoginLockoutManager:
    """Tracks failed login attempts and locks accounts after repeated failures."""

    def __init__(self, max_attempts: int = 5, lockout_duration: int = 900):
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration
        self._failed_attempts: dict[str, int] = {}
        self._lockout_times: dict[str, float] = {}

    def record_failed_attempt(self, username: str) -> None:
        count = self._failed_attempts.get(username, 0) + 1
        self._failed_attempts[username] = count

        if count >= self.max_attempts:
            self._lockout_times[username] = time.time() + self.lockout_duration

    def is_locked(self, username: str) -> tuple[bool, float | None]:
        unlock_time = self._lockout_times.get(username)
        if unlock_time is None:
            return False, None

        now = time.time()
        if now >= unlock_time:
            self._lockout_times.pop(username, None)
            self._failed_attempts[username] = 0
            return False, None

        return True, unlock_time

    def get_remaining_attempts(self, username: str) -> int:
        attempts = self._failed_attempts.get(username, 0)
        return max(0, self.max_attempts - attempts)

    def reset_attempts(self, username: str) -> None:
        self._failed_attempts.pop(username, None)
        self._lockout_times.pop(username, None)

    def unlock_account(self, username: str) -> None:
        self._lockout_times.pop(username, None)
        self._failed_attempts[username] = 0


login_lockout_manager = LoginLockoutManager(max_attempts=5, lockout_duration=900)


class JWTRevocationList:
    """In-memory JWT revocation list (development-safe)."""

    def __init__(self):
        self._revoked: set[str] = set()

    def revoke(self, jti: str) -> None:
        if jti:
            self._revoked.add(jti)

    def is_revoked(self, jti: str) -> bool:
        return bool(jti and jti in self._revoked)


jwt_revocation_list = JWTRevocationList()
