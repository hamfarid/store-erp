# -*- coding: utf-8 -*-
"""
إعدادات JWT الموحدة
Unified JWT Configuration

جميع إعدادات JWT يجب أن تستخدم هذا الملف لضمان الاتساق
All JWT settings should use this file to ensure consistency
"""

import os
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class JWTConfig:
    """
    إعدادات JWT المركزية
    Centralized JWT Configuration
    
    تضمن هذه الفئة استخدام قيم موحدة عبر التطبيق
    This class ensures consistent values across the application
    """
    
    # ==========================================================================
    # Token Expiration - STANDARDIZED VALUES
    # ==========================================================================
    
    # Access Token: Short-lived (15 minutes)
    # Used for API requests, frequent refresh expected
    ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    
    # Refresh Token: Long-lived (7 days)
    # Used to obtain new access tokens without re-authentication
    REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    
    # ==========================================================================
    # Algorithm
    # ==========================================================================
    
    # HS256 for symmetric signing (single service)
    # Use RS256 for microservices with asymmetric keys
    ALGORITHM = "HS256"
    
    # ==========================================================================
    # Secret Keys - MUST be from environment
    # ==========================================================================
    
    @classmethod
    def get_secret_key(cls) -> str:
        """
        Get JWT secret key from environment.
        
        ⚠️ WARNING: Generates a random key if not set (development only)
        ⚠️ تحذير: يولد مفتاح عشوائي إذا لم يتم تعيينه (للتطوير فقط)
        """
        key = os.getenv("JWT_SECRET_KEY")
        if not key:
            import secrets
            key = secrets.token_hex(32)
            logger.warning(
                "JWT_SECRET_KEY not set! Using auto-generated key. "
                "This is NOT safe for production!"
            )
        return key
    
    @classmethod
    def get_refresh_secret_key(cls) -> str:
        """
        Get separate secret for refresh tokens.
        Falls back to main secret if not set.
        """
        return os.getenv("JWT_REFRESH_SECRET_KEY") or cls.get_secret_key()
    
    # ==========================================================================
    # Additional Security Settings
    # ==========================================================================
    
    # Token header location
    TOKEN_LOCATION = ["headers"]
    HEADER_NAME = "Authorization"
    HEADER_TYPE = "Bearer"
    
    # CSRF Protection (for cookies only)
    CSRF_PROTECT = False  # Set True if using cookie-based tokens
    
    # Token blocklist (for logout)
    BLOCKLIST_ENABLED = True
    
    @classmethod
    def apply_to_app(cls, app):
        """
        Apply JWT configuration to Flask app.
        
        Usage:
            from src.config.jwt_config import JWTConfig
            JWTConfig.apply_to_app(app)
        """
        app.config["JWT_SECRET_KEY"] = cls.get_secret_key()
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = cls.ACCESS_TOKEN_EXPIRES
        app.config["JWT_REFRESH_TOKEN_EXPIRES"] = cls.REFRESH_TOKEN_EXPIRES
        app.config["JWT_ALGORITHM"] = cls.ALGORITHM
        app.config["JWT_TOKEN_LOCATION"] = cls.TOKEN_LOCATION
        app.config["JWT_HEADER_NAME"] = cls.HEADER_NAME
        app.config["JWT_HEADER_TYPE"] = cls.HEADER_TYPE
        app.config["JWT_CSRF_CHECK_FORM"] = cls.CSRF_PROTECT
        app.config["JWT_BLACKLIST_ENABLED"] = cls.BLOCKLIST_ENABLED
        
        logger.info(
            f"JWT configured: Access={cls.ACCESS_TOKEN_EXPIRES}, "
            f"Refresh={cls.REFRESH_TOKEN_EXPIRES}"
        )


# ==========================================================================
# Quick Access Constants (for importing)
# ==========================================================================

JWT_SECRET_KEY = JWTConfig.get_secret_key()
JWT_ACCESS_TOKEN_EXPIRES = JWTConfig.ACCESS_TOKEN_EXPIRES
JWT_REFRESH_TOKEN_EXPIRES = JWTConfig.REFRESH_TOKEN_EXPIRES
JWT_ALGORITHM = JWTConfig.ALGORITHM


# ==========================================================================
# Development/Production Helpers
# ==========================================================================

def is_production() -> bool:
    """Check if running in production mode."""
    return os.getenv("FLASK_ENV") == "production" or os.getenv("ENV") == "production"


def validate_jwt_config():
    """
    Validate JWT configuration is safe for production.
    Call this during app startup.
    """
    issues = []
    
    # Check secret key is set
    if not os.getenv("JWT_SECRET_KEY"):
        issues.append("JWT_SECRET_KEY environment variable not set")
    
    # Check secret key length
    key = os.getenv("JWT_SECRET_KEY", "")
    if len(key) < 32:
        issues.append(f"JWT_SECRET_KEY too short ({len(key)} chars, need 32+)")
    
    if is_production() and issues:
        raise ValueError(f"JWT Configuration Errors: {'; '.join(issues)}")
    elif issues:
        for issue in issues:
            logger.warning(f"JWT Config Warning: {issue}")


__all__ = [
    "JWTConfig",
    "JWT_SECRET_KEY",
    "JWT_ACCESS_TOKEN_EXPIRES",
    "JWT_REFRESH_TOKEN_EXPIRES",
    "JWT_ALGORITHM",
    "validate_jwt_config",
]
