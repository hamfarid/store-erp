#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعدادات نظام التسجيل (Logging)
Logging Configuration System

نظام متقدم لتسجيل جميع الأحداث والأخطاء في التطبيق
"""

import logging
import logging.handlers
import os
from datetime import datetime, timezone
import json


class JSONFormatter(logging.Formatter):
    """
    Formatter لتحويل السجلات إلى JSON
    JSON Formatter for logs
    """

    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # إضافة معلومات الاستثناء إذا وجدت
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # إضافة معلومات إضافية
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if hasattr(record, "ip_address"):
            log_data["ip_address"] = record.ip_address

        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """
    Formatter ملون للطباعة في Console
    Colored Formatter for console output
    """

    # ألوان ANSI
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        # إضافة اللون
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )

        return super().format(record)


def setup_logging(app):
    """
    إعداد نظام التسجيل
    Setup logging system
    """

    # إنشاء مجلد السجلات إذا لم يكن موجوداً
    logs_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs"
    )
    os.makedirs(logs_dir, exist_ok=True)

    # الحصول على مستوى التسجيل من الإعدادات
    log_level = app.config.get("LOG_LEVEL", "INFO")

    # إعداد Logger الرئيسي
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))

    # إزالة المعالجات القديمة
    root_logger.handlers = []

    # ===== معالج Console =====
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # استخدام Formatter ملون للـ Console
    console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    console_formatter = ColoredFormatter(console_format, datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(console_formatter)

    root_logger.addHandler(console_handler)

    # ===== معالج ملف عام =====
    general_log_file = os.path.join(logs_dir, "app.log")
    file_handler = logging.handlers.RotatingFileHandler(
        general_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",  # 10 MB
    )
    file_handler.setLevel(logging.INFO)

    file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_formatter = logging.Formatter(file_format, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)

    root_logger.addHandler(file_handler)

    # ===== معالج ملف الأخطاء =====
    error_log_file = os.path.join(logs_dir, "errors.log")
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",  # 10 MB
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)

    root_logger.addHandler(error_handler)

    # ===== معالج JSON للتحليل =====
    json_log_file = os.path.join(logs_dir, "app.json.log")
    json_handler = logging.handlers.RotatingFileHandler(
        json_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",  # 10 MB
    )
    json_handler.setLevel(logging.INFO)
    json_handler.setFormatter(JSONFormatter())

    root_logger.addHandler(json_handler)

    # ===== معالج ملف الوصول (Access Log) =====
    access_log_file = os.path.join(logs_dir, "access.log")
    access_handler = logging.handlers.RotatingFileHandler(
        access_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",  # 10 MB
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(file_formatter)

    # إنشاء logger منفصل للوصول
    access_logger = logging.getLogger("access")
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)
    access_logger.propagate = False

    # ===== معالج ملف قاعدة البيانات =====
    db_log_file = os.path.join(logs_dir, "database.log")
    db_handler = logging.handlers.RotatingFileHandler(
        db_log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"  # 10 MB
    )
    db_handler.setLevel(logging.WARNING)
    db_handler.setFormatter(file_formatter)

    # إنشاء logger منفصل لقاعدة البيانات
    db_logger = logging.getLogger("sqlalchemy")
    db_logger.addHandler(db_handler)
    db_logger.setLevel(logging.WARNING)
    db_logger.propagate = False

    # تسجيل رسالة بدء التشغيل
    app.logger.info("=" * 80)
    app.logger.info("🚀 تم بدء تشغيل التطبيق | Application Started")
    app.logger.info(f"📝 مستوى التسجيل: {log_level} | Log Level: {log_level}")
    app.logger.info(f"📁 مجلد السجلات: {logs_dir} | Logs Directory: {logs_dir}")
    app.logger.info("=" * 80)


def log_request(request, response=None, user_id=None):
    """
    تسجيل طلب HTTP
    Log HTTP request
    """
    access_logger = logging.getLogger("access")

    log_data = {
        "method": request.method,
        "path": request.path,
        "ip": request.remote_addr,
        "user_agent": request.user_agent.string if request.user_agent else None,
    }

    if user_id:
        log_data["user_id"] = user_id

    if response:
        log_data["status_code"] = response.status_code

    access_logger.info(json.dumps(log_data, ensure_ascii=False))


def log_database_query(query, duration=None):
    """
    تسجيل استعلام قاعدة البيانات
    Log database query
    """
    db_logger = logging.getLogger("database")

    log_data = {
        "query": str(query),
    }

    if duration:
        log_data["duration_ms"] = duration

    db_logger.debug(json.dumps(log_data, ensure_ascii=False))


def log_user_activity(user_id, action, details=None, ip_address=None):
    """
    تسجيل نشاط المستخدم
    Log user activity
    """
    activity_logger = logging.getLogger("activity")

    log_data = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if details:
        log_data["details"] = details

    if ip_address:
        log_data["ip_address"] = ip_address

    activity_logger.info(json.dumps(log_data, ensure_ascii=False))


def log_security_event(event_type, details, severity="WARNING"):
    """
    تسجيل حدث أمني
    Log security event
    """
    security_logger = logging.getLogger("security")

    log_data = {
        "event_type": event_type,
        "details": details,
        "timestamp": datetime.utcnow().isoformat(),
    }

    level = getattr(logging, severity.upper(), logging.WARNING)
    security_logger.log(level, json.dumps(log_data, ensure_ascii=False))


# إنشاء loggers مخصصة
def get_logger(name):
    """
    الحصول على logger مخصص
    Get a custom logger
    """
    return logging.getLogger(name)
