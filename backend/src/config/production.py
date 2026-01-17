"""
إعدادات الإنتاج لنظام إدارة المخزون
ملف: production.py

T21: Integrated with HashiCorp Vault for secret management
"""

import os
from datetime import timedelta
from typing import Any, Optional

# Import Vault client for secret management
try:
    from vault_client import get_secret

    VAULT_AVAILABLE = True
except ImportError:
    # Fallback if Vault client not available
    VAULT_AVAILABLE = False

    def get_secret(
        path: str, field: Optional[str] = None, fallback_env: Optional[str] = None
    ) -> Any:
        """Fallback function when Vault is not available"""
        if fallback_env:
            return os.environ.get(fallback_env)
        return None


class ProductionConfig:
    """إعدادات الإنتاج"""

    # إعدادات قاعدة البيانات (T21: Vault Integration)
    # Try to get database config from Vault
    _db_config = get_secret("database", fallback_env="DATABASE_URL")

    if _db_config and isinstance(_db_config, dict):
        # Build PostgreSQL connection string from Vault secrets
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{_db_config.get('username')}:"
            f"{_db_config.get('password')}@"
            f"{_db_config.get('host', 'localhost')}:"
            f"{_db_config.get('port', 5432)}/"
            f"{_db_config.get('database')}"
        )
    else:
        # Fallback to environment variable or SQLite
        SQLALCHEMY_DATABASE_URI = (
            os.environ.get("DATABASE_URL") or "sqlite:///instance/inventory.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_timeout": 20,
        "pool_recycle": -1,
        "pool_pre_ping": True,
    }

    # إعدادات الأمان (T21: Vault Integration)
    # Try Vault first, fallback to environment variables
    SECRET_KEY = (
        get_secret("flask", field="secret_key", fallback_env="SECRET_KEY")
        or "dev-secret-key-change-in-production"
    )

    JWT_SECRET_KEY = (
        get_secret("flask", field="jwt_secret", fallback_env="JWT_SECRET_KEY")
        or "jwt-secret-key"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # إعدادات الجلسة
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "inventory_"
    SESSION_FILE_DIR = "flask_session"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # إعدادات CORS
    CORS_ORIGINS = ["http://localhost:5502", "http://172.16.16.27:5502"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    # إعدادات الخادم
    HOST = "172.16.16.27"
    PORT = 8000
    DEBUG = False
    TESTING = False

    # إعدادات الملفات
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {"txt", "pd", "png", "jpg", "jpeg", "gi", "xlsx", "xls", "csv"}

    # إعدادات البريد الإلكتروني (T21: Vault Integration)
    _mail_config = get_secret("mail", fallback_env=None)

    if _mail_config and isinstance(_mail_config, dict):
        MAIL_SERVER = _mail_config.get("server") or os.environ.get("MAIL_SERVER")
        MAIL_PORT = int(_mail_config.get("port", 587))
        MAIL_USE_TLS = _mail_config.get("use_tls", True)
        MAIL_USERNAME = _mail_config.get("username") or os.environ.get("MAIL_USERNAME")
        MAIL_PASSWORD = _mail_config.get("password") or os.environ.get("MAIL_PASSWORD")
    else:
        # Fallback to environment variables
        MAIL_SERVER = os.environ.get("MAIL_SERVER")
        MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
        MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in [
            "true",
            "on",
            "1",
        ]
        MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
        MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # إعدادات التسجيل
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/inventory.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

    # إعدادات النسخ الاحتياطي
    BACKUP_ENABLED = True
    BACKUP_INTERVAL = 24  # ساعة
    BACKUP_RETENTION = 30  # يوم
    BACKUP_PATH = "backups"

    # إعدادات API
    API_RATE_LIMIT = "1000 per hour"
    API_TIMEOUT = 30  # ثانية

    # إعدادات التقارير
    REPORTS_CACHE_TIMEOUT = 300  # 5 دقائق
    REPORTS_MAX_RECORDS = 10000

    # إعدادات الأمان المتقدمة (T21: Vault Integration)
    SECURITY_PASSWORD_SALT = (
        get_secret(
            "flask", field="password_salt", fallback_env="SECURITY_PASSWORD_SALT"
        )
        or "password-salt"
    )

    SECURITY_REGISTERABLE = False
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True

    # إعدادات المصادقة
    AUTH_TOKEN_EXPIRY = 3600  # ثانية
    AUTH_MAX_LOGIN_ATTEMPTS = 5
    AUTH_LOCKOUT_DURATION = 300  # ثانية

    # إعدادات الإشعارات
    NOTIFICATIONS_ENABLED = True
    NOTIFICATIONS_EMAIL = True
    NOTIFICATIONS_SMS = False

    # إعدادات التكامل
    INTEGRATION_ENABLED = True
    INTEGRATION_TIMEOUT = 30

    # Resilience / Circuit Breaker (defaults)
    CIRCUIT_BREAKER_ENABLED = True
    CIRCUIT_BREAKER_DEFAULTS = {
        "failure_threshold": 0.5,
        "rolling_window_seconds": 60,
        "min_throughput": 20,
        "open_state_seconds": 60.0,
        "half_open_max_in_flight": 10,
        "success_quorum_percent": 0.8,
        "retries": 2,
        "timeout_seconds": 10.0,
        "backoff_base": 0.25,
        "backoff_factor": 2.0,
        "jitter": 0.2,
    }
    # Optional per-service overrides (empty by default)
    CIRCUIT_BREAKER_SERVICES: dict = {}

    @staticmethod
    def init_app(app):
        """تهيئة التطبيق بالإعدادات"""

        # إنشاء المجلدات المطلوبة
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs(app.config["BACKUP_PATH"], exist_ok=True)
        os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)

        # إعداد التسجيل
        import logging
        from logging.handlers import RotatingFileHandler

        if not app.debug:
            file_handler = RotatingFileHandler(
                app.config["LOG_FILE"],
                maxBytes=app.config["LOG_MAX_SIZE"],
                backupCount=app.config["LOG_BACKUP_COUNT"],
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info("نظام إدارة المخزون بدأ التشغيل")


class DevelopmentConfig(ProductionConfig):
    """إعدادات التطوير"""

    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"

    # قاعدة بيانات التطوير
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/inventory_dev.db"

    # إعدادات أمان أقل صرامة للتطوير
    AUTH_MAX_LOGIN_ATTEMPTS = 10
    AUTH_LOCKOUT_DURATION = 60


class TestingConfig(ProductionConfig):
    """إعدادات الاختبار"""

    TESTING = True
    DEBUG = True

    # قاعدة بيانات الاختبار
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # تعطيل الحماية للاختبار
    WTF_CSRF_ENABLED = False
    AUTH_MAX_LOGIN_ATTEMPTS = 1000


# قاموس الإعدادات
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
