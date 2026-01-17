# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Comprehensive Logging System
Records all backend activity: startup, requests, database changes, user actions
"""

import logging
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from logging.handlers import RotatingFileHandler
from functools import wraps
from flask import request, g
import traceback

# استيراد JWT Manager لاستخراج معلومات المستخدم
JWT_AVAILABLE = False
try:
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from jwt_manager import JWTManager

    JWT_AVAILABLE = True
except ImportError:
    try:
        from src.jwt_manager import JWTManager

        JWT_AVAILABLE = True
    except ImportError:
        pass


class ComprehensiveLogger:
    """Comprehensive logging system for all backend operations"""

    def __init__(self, app=None):
        self.app = app
        self.log_dir = Path(__file__).parent.parent.parent / "logs"
        self.loggers = {}

        if app:
            self.init_app(app)

    def _extract_user_from_jwt(self):
        """استخراج معلومات المستخدم من JWT token إن وجد"""
        try:
            # محاولة الحصول على التوكن من Authorization header
            auth_header = request.headers.get("Authorization", "")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None, None

            token = auth_header[7:]  # إزالة 'Bearer '

            if not JWT_AVAILABLE:
                return None, None

            # فك تشفير التوكن (بدون verify لتجنب مشاكل الأداء)
            payload = JWTManager.decode_token(token, verify=False)
            if not payload:
                return None, None

            user_id = payload.get("user_id")
            if not user_id:
                return None, None

            # محاولة الحصول على اسم المستخدم من قاعدة البيانات
            try:
                # استيراد lazy لتجنب circular imports
                from src.models.user import User

                user = User.query.get(user_id)
                if user and hasattr(user, "username"):
                    return user_id, user.username
            except Exception as e:
                # فشل الاستعلام من DB، استخدم user_id فقط
                pass

            # Return user_id with generic username
            return user_id, f"user_{user_id}"

        except Exception as e:
            # أي خطأ → تجاهل واستخدم anonymous
            return None, None

    def init_app(self, app):
        """Initialize logging system with Flask app"""
        self.app = app
        self._create_log_directories()
        self._setup_loggers()
        self._register_handlers()

    def _create_log_directories(self):
        """Create all log directories"""
        directories = [
            "startup",
            "requests",
            "database",
            "errors",
            "security",
            "performance",
        ]

        for directory in directories:
            (self.log_dir / directory).mkdir(parents=True, exist_ok=True)

    def _setup_loggers(self):
        """Setup all specialized loggers"""
        log_configs = {
            "startup": {
                "file": self.log_dir / "startup" / "startup.log",
                "level": logging.INFO,
                "format": "%(asctime)s - [STARTUP] - %(levelname)s - %(message)s",
            },
            "requests": {
                "file": self.log_dir / "requests" / "requests.log",
                "level": logging.INFO,
                "format": "%(asctime)s - [REQUEST] - %(message)s",
            },
            "database": {
                "file": self.log_dir / "database" / "database.log",
                "level": logging.INFO,
                "format": "%(asctime)s - [DATABASE] - %(message)s",
            },
            "errors": {
                "file": self.log_dir / "errors" / "errors.log",
                "level": logging.ERROR,
                "format": "%(asctime)s - [ERROR] - %(levelname)s - %(message)s",
            },
            "security": {
                "file": self.log_dir / "security" / "security.log",
                "level": logging.WARNING,
                "format": "%(asctime)s - [SECURITY] - %(levelname)s - %(message)s",
            },
            "performance": {
                "file": self.log_dir / "performance" / "performance.log",
                "level": logging.INFO,
                "format": "%(asctime)s - [PERFORMANCE] - %(message)s",
            },
        }

        for name, config in log_configs.items():
            logger = logging.getLogger(f"comprehensive.{name}")
            logger.setLevel(config["level"])
            logger.handlers.clear()

            # Rotating file handler (10MB max, keep 10 backups)
            handler = RotatingFileHandler(
                config["file"],
                maxBytes=10 * 1024 * 1024,
                backupCount=10,
                encoding="utf-8",  # 10MB
            )

            formatter = logging.Formatter(config["format"], datefmt="%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            self.loggers[name] = logger

    def _register_handlers(self):
        """Register Flask request handlers"""
        if not self.app:
            return

        @self.app.before_request
        def log_request_start():
            """Log request start"""
            g.start_time = datetime.now(timezone.utc)

            # Get client IP
            if request.headers.get("X-Forwarded-For"):
                ip = request.headers.get("X-Forwarded-For").split(",")[0]
            else:
                ip = request.remote_addr

            # Get user info - أولاً من g.current_user، ثم من JWT
            user = getattr(g, "current_user", None)
            if user:
                user_id = user.id
                username = user.username
            else:
                # محاولة استخراج من JWT header
                user_id, username = self._extract_user_from_jwt()
                if user_id is None:
                    user_id = "anonymous"
                    username = "anonymous"

            # Log request
            self.log_request(
                method=request.method,
                path=request.path,
                ip=ip,
                user_id=user_id,
                username=username,
                headers=dict(request.headers),
                query_params=dict(request.args),
                body=self._get_safe_body(),
            )

        @self.app.after_request
        def log_request_end(response):
            """Log request end"""
            if hasattr(g, "start_time"):
                duration = (datetime.now(timezone.utc) - g.start_time).total_seconds()

                # Get client IP
                if request.headers.get("X-Forwarded-For"):
                    ip = request.headers.get("X-Forwarded-For").split(",")[0]
                else:
                    ip = request.remote_addr

                # Get user info - أولاً من g.current_user، ثم من JWT
                user = getattr(g, "current_user", None)
                if user:
                    user_id = user.id
                    username = user.username
                else:
                    # محاولة استخراج من JWT header
                    user_id, username = self._extract_user_from_jwt()
                    if user_id is None:
                        user_id = "anonymous"
                        username = "anonymous"

                # Log response
                self.log_response(
                    method=request.method,
                    path=request.path,
                    status_code=response.status_code,
                    duration=duration,
                    ip=ip,
                    user_id=user_id,
                    username=username,
                )

                # Log performance if slow
                if duration > 1.0:  # Slow request (>1 second)
                    self.log_performance(
                        event="slow_request",
                        duration=duration,
                        method=request.method,
                        path=request.path,
                        ip=ip,
                        user_id=user_id,
                    )

            return response

        @self.app.errorhandler(Exception)
        def log_exception(error):
            """Log unhandled exceptions"""
            self.log_error(
                error=str(error),
                traceback=traceback.format_exc(),
                method=request.method,
                path=request.path,
                ip=request.remote_addr,
            )
            raise error

    def _get_safe_body(self):
        """Get request body safely (hide passwords)"""
        try:
            if request.is_json:
                body = request.get_json()
                if isinstance(body, dict):
                    # Hide sensitive fields
                    safe_body = body.copy()
                    for key in ["password", "token", "secret", "api_key"]:
                        if key in safe_body:
                            safe_body[key] = "***HIDDEN***"
                    return safe_body
                return body
            return None
        except Exception:
            return None

    def log_startup(self, event, **kwargs):
        """Log startup events"""
        message = self._format_log_message(event, **kwargs)
        self.loggers["startup"].info(message)

    def log_request(self, method, path, ip, user_id, username, **kwargs):
        """Log HTTP request"""
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": method,
            "path": path,
            "ip": ip,
            "user_id": user_id,
            "username": username,
            **kwargs,
        }
        self.loggers["requests"].info(json.dumps(data, ensure_ascii=False))

    def log_response(self, method, path, status_code, duration, ip, user_id, username):
        """Log HTTP response"""
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_seconds": round(duration, 3),
            "ip": ip,
            "user_id": user_id,
            "username": username,
        }
        self.loggers["requests"].info(json.dumps(data, ensure_ascii=False))

    def log_database(self, operation, table, **kwargs):
        """Log database operations"""
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": operation,  # INSERT, UPDATE, DELETE, SELECT
            "table": table,
            "user_id": (
                getattr(g, "current_user", {}).get("id", "system")
                if hasattr(g, "current_user")
                else "system"
            ),
            **kwargs,
        }
        self.loggers["database"].info(json.dumps(data, ensure_ascii=False))

    def log_error(self, error, **kwargs):
        """Log errors"""
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(error),
            **kwargs,
        }
        self.loggers["errors"].error(json.dumps(data, ensure_ascii=False))

    def log_security(self, event, **kwargs):
        """Log security events"""
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "ip": request.remote_addr if request else "unknown",
            **kwargs,
        }
        self.loggers["security"].warning(json.dumps(data, ensure_ascii=False))

    def log_performance(self, event, duration, **kwargs):
        """Log performance metrics"""
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "duration_seconds": round(duration, 3),
            **kwargs,
        }
        self.loggers["performance"].info(json.dumps(data, ensure_ascii=False))

    def _format_log_message(self, event, **kwargs):
        """Format log message"""
        parts = [f"EVENT={event}"]
        for key, value in kwargs.items():
            parts.append(f"{key.upper()}={value}")
        return " | ".join(parts)


# Global logger instance
comprehensive_logger = ComprehensiveLogger()


def log_database_change(operation, table):
    """Decorator to log database changes"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Log the database operation
            comprehensive_logger.log_database(
                operation=operation,
                table=table,
                function=func.__name__,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )

            return result

        return wrapper

    return decorator
