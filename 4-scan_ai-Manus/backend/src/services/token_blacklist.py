"""
Token Blacklist Service with Redis
خدمة قائمة الحظر للرموز مع Redis

Version: 1.0.0
Created: 2025-12-19

Features:
- Token blacklisting for logout
- Automatic expiration
- Fallback to in-memory storage
- Thread-safe operations
"""

import hashlib
import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Set
from threading import Lock

logger = logging.getLogger(__name__)

# ===== In-Memory Fallback =====
# قائمة حظر مؤقتة في الذاكرة (fallback)
_memory_blacklist: Set[str] = set()
_memory_blacklist_lock = Lock()
_memory_expiry: dict = {}


class TokenBlacklist:
    """
    خدمة قائمة حظر الرموز
    Token Blacklist Service

    Supports Redis for distributed systems with in-memory fallback.
    """

    def __init__(self, redis_url: Optional[str] = None):
        """
        تهيئة خدمة قائمة الحظر

        Args:
            redis_url: عنوان Redis (اختياري)
        """
        self.redis_client = None
        self.redis_available = False
        self.prefix = "gaara:blacklist:"

        # محاولة الاتصال بـ Redis
        redis_url = redis_url or os.getenv("REDIS_URL")
        if redis_url:
            try:
                import redis
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
                self.redis_client.ping()
                self.redis_available = True
                logger.info("✅ Token blacklist connected to Redis")
            except ImportError:
                logger.warning("⚠️ Redis package not installed, using in-memory storage")
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed, using in-memory storage: {e}")

    def _hash_token(self, token: str) -> str:
        """
        تشفير الرمز للتخزين الآمن
        Hash token for secure storage
        """
        return hashlib.sha256(token.encode()).hexdigest()

    def add(self, token: str, expires_in: int = 86400) -> bool:
        """
        إضافة رمز إلى قائمة الحظر
        Add token to blacklist

        Args:
            token: الرمز المراد حظره
            expires_in: مدة الصلاحية بالثواني (افتراضي: 24 ساعة)

        Returns:
            bool: نجاح العملية
        """
        token_hash = self._hash_token(token)

        try:
            if self.redis_available and self.redis_client:
                # استخدام Redis مع انتهاء صلاحية تلقائي
                self.redis_client.setex(
                    f"{self.prefix}{token_hash}",
                    expires_in,
                    "1"
                )
                logger.debug(f"Token blacklisted in Redis (expires in {expires_in}s)")
                return True
            else:
                # استخدام الذاكرة المحلية
                with _memory_blacklist_lock:
                    _memory_blacklist.add(token_hash)
                    _memory_expiry[token_hash] = datetime.utcnow() + timedelta(seconds=expires_in)
                logger.debug(f"Token blacklisted in memory (expires in {expires_in}s)")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to blacklist token: {e}")
            return False

    def is_blacklisted(self, token: str) -> bool:
        """
        التحقق من وجود الرمز في قائمة الحظر
        Check if token is blacklisted

        Args:
            token: الرمز المراد التحقق منه

        Returns:
            bool: True إذا كان الرمز محظوراً
        """
        token_hash = self._hash_token(token)

        try:
            if self.redis_available and self.redis_client:
                result = self.redis_client.exists(f"{self.prefix}{token_hash}")
                return bool(result)
            else:
                with _memory_blacklist_lock:
                    # تنظيف الرموز المنتهية
                    self._cleanup_expired()
                    return token_hash in _memory_blacklist
        except Exception as e:
            logger.error(f"❌ Error checking token blacklist: {e}")
            return False  # في حالة الخطأ، نفترض أن الرمز صالح

    def remove(self, token: str) -> bool:
        """
        إزالة رمز من قائمة الحظر
        Remove token from blacklist

        Args:
            token: الرمز المراد إزالته

        Returns:
            bool: نجاح العملية
        """
        token_hash = self._hash_token(token)

        try:
            if self.redis_available and self.redis_client:
                self.redis_client.delete(f"{self.prefix}{token_hash}")
                return True
            else:
                with _memory_blacklist_lock:
                    _memory_blacklist.discard(token_hash)
                    _memory_expiry.pop(token_hash, None)
                return True
        except Exception as e:
            logger.error(f"❌ Failed to remove token from blacklist: {e}")
            return False

    def _cleanup_expired(self) -> int:
        """
        تنظيف الرموز المنتهية من الذاكرة
        Cleanup expired tokens from memory

        Returns:
            int: عدد الرموز المحذوفة
        """
        now = datetime.utcnow()
        expired = [
            token_hash for token_hash, expiry in _memory_expiry.items()
            if expiry < now
        ]

        for token_hash in expired:
            _memory_blacklist.discard(token_hash)
            del _memory_expiry[token_hash]

        if expired:
            logger.debug(f"Cleaned up {len(expired)} expired tokens")

        return len(expired)

    def clear_all(self) -> bool:
        """
        مسح جميع الرموز من قائمة الحظر
        Clear all tokens from blacklist

        ⚠️ تحذير: استخدم بحذر - يؤدي لتسجيل خروج جميع المستخدمين

        Returns:
            bool: نجاح العملية
        """
        try:
            if self.redis_available and self.redis_client:
                # حذف جميع المفاتيح ذات البادئة
                keys = self.redis_client.keys(f"{self.prefix}*")
                if keys:
                    self.redis_client.delete(*keys)
                logger.info(f"Cleared {len(keys)} tokens from Redis blacklist")
                return True
            else:
                with _memory_blacklist_lock:
                    count = len(_memory_blacklist)
                    _memory_blacklist.clear()
                    _memory_expiry.clear()
                logger.info(f"Cleared {count} tokens from memory blacklist")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to clear blacklist: {e}")
            return False

    def count(self) -> int:
        """
        عدد الرموز في قائمة الحظر
        Count tokens in blacklist

        Returns:
            int: عدد الرموز
        """
        try:
            if self.redis_available and self.redis_client:
                keys = self.redis_client.keys(f"{self.prefix}*")
                return len(keys)
            else:
                with _memory_blacklist_lock:
                    self._cleanup_expired()
                    return len(_memory_blacklist)
        except Exception as e:
            logger.error(f"❌ Error counting blacklisted tokens: {e}")
            return 0

    def health_check(self) -> dict:
        """
        فحص صحة الخدمة
        Service health check

        Returns:
            dict: حالة الخدمة
        """
        return {
            "service": "token_blacklist",
            "redis_available": self.redis_available,
            "storage": "redis" if self.redis_available else "memory",
            "token_count": self.count(),
            "status": "healthy"
        }


# ===== Singleton Instance =====
_blacklist_instance: Optional[TokenBlacklist] = None


def get_token_blacklist() -> TokenBlacklist:
    """الحصول على مثيل قائمة الحظر"""
    global _blacklist_instance
    if _blacklist_instance is None:
        redis_url = os.getenv("REDIS_URL")
        if not redis_url:
            # بناء URL من المتغيرات الفردية
            redis_host = os.getenv("REDIS_HOST", "localhost")
            redis_port = os.getenv("REDIS_PORT", "6379")
            redis_db = os.getenv("REDIS_DB", "0")
            redis_password = os.getenv("REDIS_PASSWORD", "")

            if redis_password:
                redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
            else:
                redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"

        _blacklist_instance = TokenBlacklist(redis_url)

    return _blacklist_instance


# ===== Convenience Functions =====

def blacklist_token(token: str, expires_in: int = 86400) -> bool:
    """إضافة رمز إلى قائمة الحظر"""
    return get_token_blacklist().add(token, expires_in)


def is_token_blacklisted(token: str) -> bool:
    """التحقق من حظر الرمز"""
    return get_token_blacklist().is_blacklisted(token)


def remove_from_blacklist(token: str) -> bool:
    """إزالة رمز من قائمة الحظر"""
    return get_token_blacklist().remove(token)
