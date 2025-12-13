#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
نظام التسجيل المتقدم
Advanced Logging System
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from functools import wraps
import traceback


class AdvancedLogger:
    def __init__(self, log_dir="../../logs"):
        self.log_dir = Path(__file__).parent / log_dir
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            # Fallback to /tmp for Docker environments with volume mount issues
            self.log_dir = Path("/tmp/logs")
            self.log_dir.mkdir(parents=True, exist_ok=True)
            print(f"⚠️ Using fallback log directory: {self.log_dir}")

        # إعداد ملفات السجل
        self.setup_loggers()

        # إحصائيات
        self.stats = {
            "clicks": 0,
            "routes": 0,
            "errors": 0,
            "api_calls": 0,
            "session_start": datetime.now().isoformat(),
        }

    def setup_loggers(self):
        """إعداد أنواع مختلفة من السجلات"""

        # سجل النقرات
        self.click_logger = self._create_logger("clicks", self.log_dir / "clicks.log")

        # سجل المسارات
        self.route_logger = self._create_logger("routes", self.log_dir / "routes.log")

        # سجل الأخطاء
        self.error_logger = self._create_logger("errors", self.log_dir / "errors.log")

        # سجل API
        self.api_logger = self._create_logger("api", self.log_dir / "api_calls.log")

        # سجل النظام العام
        self.system_logger = self._create_logger("system", self.log_dir / "system.log")

    def _create_logger(self, name, log_file):
        """إنشاء logger مخصص"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # تجنب إضافة handlers متعددة
        if logger.handlers:
            return logger

        # إعداد formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def log_click(
        self, button_id, button_text, user_id=None, page=None, additional_data=None
    ):
        """تسجيل النقرات على الأزرار"""
        self.stats["clicks"] += 1

        click_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "button_click",
            "button_id": button_id,
            "button_text": button_text,
            "user_id": user_id,
            "page": page,
            "session_id": self._get_session_id(),
            "additional_data": additional_data or {},
        }

        self.click_logger.info(json.dumps(click_data, ensure_ascii=False))
        return click_data

    def log_route(
        self, route, method="GET", user_id=None, params=None, response_time=None
    ):
        """تسجيل المسارات المستخدمة"""
        self.stats["routes"] += 1

        route_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "route_access",
            "route": route,
            "method": method,
            "user_id": user_id,
            "params": params or {},
            "response_time": response_time,
            "session_id": self._get_session_id(),
        }

        self.route_logger.info(json.dumps(route_data, ensure_ascii=False))
        return route_data

    def log_error(self, error, context=None, user_id=None, route=None):
        """تسجيل الأخطاء"""
        self.stats["errors"] += 1

        error_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "error",
            "error_message": str(error),
            "error_type": type(error).__name__,
            "traceback": traceback.format_exc(),
            "context": context or {},
            "user_id": user_id,
            "route": route,
            "session_id": self._get_session_id(),
        }

        self.error_logger.error(json.dumps(error_data, ensure_ascii=False))
        return error_data

    def log_api_call(
        self,
        endpoint,
        method,
        status_code,
        response_time,
        user_id=None,
        request_data=None,
    ):
        """تسجيل استدعاءات API"""
        self.stats["api_calls"] += 1

        api_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "api_call",
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time": response_time,
            "user_id": user_id,
            "request_data": request_data or {},
            "session_id": self._get_session_id(),
        }

        self.api_logger.info(json.dumps(api_data, ensure_ascii=False))
        return api_data

    def log_system_event(self, event_type, description, data=None):
        """تسجيل أحداث النظام"""
        system_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "system_event",
            "event_type": event_type,
            "description": description,
            "data": data or {},
            "session_id": self._get_session_id(),
        }

        self.system_logger.info(json.dumps(system_data, ensure_ascii=False))
        return system_data

    def _get_session_id(self):
        """الحصول على معرف الجلسة"""
        # يمكن تحسين هذا لاحقاً
        return f"session_{datetime.now().strftime('%Y%m%d_%H')}"

    def get_stats(self):
        """الحصول على إحصائيات الجلسة"""
        return {
            **self.stats,
            "uptime": (
                datetime.now() - datetime.fromisoformat(self.stats["session_start"])
            ).total_seconds(),
        }

    def save_daily_summary(self):
        """حفظ ملخص يومي"""
        today = datetime.now().strftime("%Y-%m-%d")
        summary_file = self.log_dir / f"daily_summary_{today}.json"

        summary = {
            "date": today,
            "stats": self.get_stats(),
            "generated_at": datetime.now().isoformat(),
        }

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)


# Decorators للتسجيل التلقائي


def log_route_access(logger_instance):
    """Decorator لتسجيل الوصول للمسارات"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            route = getattr(func, "__name__", "unknown")

            try:
                result = func(*args, **kwargs)
                response_time = (datetime.now() - start_time).total_seconds()

                logger_instance.log_route(route=route, response_time=response_time)

                return result

            except Exception as e:
                logger_instance.log_error(
                    error=e, context={"function": route, "args": str(args)[:200]}
                )
                raise

        return wrapper

    return decorator


def log_api_endpoint(logger_instance):
    """Decorator لتسجيل نقاط النهاية API"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            endpoint = getattr(func, "__name__", "unknown")

            try:
                result = func(*args, **kwargs)
                response_time = (datetime.now() - start_time).total_seconds()

                # تحديد status code من النتيجة
                status_code = 200
                if hasattr(result, "status_code"):
                    status_code = result.status_code

                logger_instance.log_api_call(
                    endpoint=endpoint,
                    method="POST",  # يمكن تحسين هذا
                    status_code=status_code,
                    response_time=response_time,
                )

                return result

            except Exception as e:
                logger_instance.log_api_call(
                    endpoint=endpoint,
                    method="POST",
                    status_code=500,
                    response_time=(datetime.now() - start_time).total_seconds(),
                )
                logger_instance.log_error(error=e, context={"endpoint": endpoint})
                raise

        return wrapper

    return decorator


# إنشاء instance عام
advanced_logger = AdvancedLogger()


# دوال مساعدة سريعة
def log_click(button_id, button_text, **kwargs):
    return advanced_logger.log_click(button_id, button_text, **kwargs)


def log_route(route, **kwargs):
    return advanced_logger.log_route(route, **kwargs)


def log_error(error, **kwargs):
    return advanced_logger.log_error(error, **kwargs)


def log_api(endpoint, method, status_code, response_time, **kwargs):
    return advanced_logger.log_api_call(
        endpoint, method, status_code, response_time, **kwargs
    )


def log_system(event_type, description, **kwargs):
    return advanced_logger.log_system_event(event_type, description, **kwargs)


def get_logging_stats():
    return advanced_logger.get_stats()


if __name__ == "__main__":
    # اختبار النظام
    print("🧪 اختبار نظام التسجيل...")

    # تسجيل أمثلة
    log_click("btn_save", "حفظ", user_id="admin", page="products")
    log_route("/api/products", method="GET", response_time=0.15)
    log_system("startup", "تم بدء تشغيل النظام")

    # عرض الإحصائيات
    stats = get_logging_stats()
    print(f"📊 الإحصائيات: {json.dumps(stats, ensure_ascii=False, indent=2)}")

    print("✅ تم اختبار نظام التسجيل بنجاح!")
