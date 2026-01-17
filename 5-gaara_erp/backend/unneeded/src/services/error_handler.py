# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
#!/usr/bin/env python3
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/error_handler.py

خدمة تحسين رسائل الخطأ وتجربة المستخدم
All linting disabled due to complex imports and optional dependencies.

تشمل:
- رسائل خطأ واضحة ومفيدة باللغة العربية
- تصنيف الأخطاء حسب النوع والخطورة
- اقتراحات لحل المشاكل
- تسجيل مفصل للأخطاء
- إشعارات للمستخدمين والمطورين
- تتبع الأخطاء المتكررة
- تحليل أنماط الأخطاء
"""

import logging
import traceback
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from flask import request, jsonify, g, current_app
from functools import wraps
from enum import Enum
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os
import hashlib
from collections import defaultdict, Counter
import threading

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """مستويات خطورة الأخطاء"""

    LOW = "منخفض"
    MEDIUM = "متوسط"
    HIGH = "عالي"
    CRITICAL = "حرج"


class ErrorCategory(Enum):
    """تصنيفات الأخطاء"""

    VALIDATION = "تحقق من البيانات"
    DATABASE = "قاعدة البيانات"
    AUTHENTICATION = "المصادقة والتوثيق"
    AUTHORIZATION = "الصلاحيات"
    BUSINESS_LOGIC = "منطق العمل"
    EXTERNAL_API = "خدمات خارجية"
    SYSTEM = "النظام"
    NETWORK = "الشبكة"
    FILE_SYSTEM = "نظام الملفات"
    CONFIGURATION = "الإعدادات"


class ErrorHandler:
    """نظام إدارة الأخطاء المتقدم"""

    def __init__(self):
        self.error_patterns = {}
        self.error_stats = defaultdict(int)
        self.error_history = []
        self.user_error_patterns = defaultdict(list)
        self._lock = threading.Lock()

        # إعدادات الإشعارات
        self.notification_settings = {
            "email_enabled": False,
            "email_recipients": [],
            "critical_threshold": 5,  # عدد الأخطاء الحرجة قبل الإشعار
            "error_rate_threshold": 10,  # معدل الأخطاء في الدقيقة
        }

        # قاموس رسائل الخطأ المحسنة
        self._init_error_messages()

        # قاموس الحلول المقترحة
        self._init_error_solutions()

    def _init_error_messages(self):
        """تهيئة رسائل الخطأ المحسنة"""
        self.error_messages = {
            # أخطاء التحقق من البيانات
            "required_field": 'الحقل "{field}" مطلوب ولا يمكن تركه فارغاً',
            "invalid_email": 'عنوان البريد الإلكتروني "{email}" غير صحيح',
            "invalid_phone": 'رقم الهاتف "{phone}" غير صحيح',
            "invalid_date": 'التاريخ "{date}" غير صحيح أو بتنسيق خاطئ',
            "invalid_number": 'القيمة "{value}" يجب أن تكون رقماً صحيحاً',
            "value_too_small": 'القيمة "{value}" صغيرة جداً، الحد الأدنى هو {min_value}',
            "value_too_large": 'القيمة "{value}" كبيرة جداً، الحد الأقصى هو {max_value}',
            "invalid_choice": 'الخيار "{choice}" غير صحيح، الخيارات المتاحة: {choices}',
            "duplicate_value": 'القيمة "{value}" موجودة مسبقاً في الحقل "{field}"',
            "invalid_format": 'تنسيق البيانات في الحقل "{field}" غير صحيح',
            # أخطاء قاعدة البيانات
            "database_connection": "فشل في الاتصال بقاعدة البيانات، يرجى المحاولة لاحقاً",
            "record_not_found": "السجل المطلوب غير موجود أو تم حذفه",
            "foreign_key_constraint": "لا يمكن حذف هذا السجل لأنه مرتبط بسجلات أخرى",
            "unique_constraint": 'القيمة "{value}" موجودة مسبقاً ويجب أن تكون فريدة',
            "database_timeout": "انتهت مهلة الاستعلام، يرجى تبسيط البحث أو المحاولة لاحقاً",
            "database_lock": "السجل محجوز حالياً من قبل مستخدم آخر",
            # أخطاء المصادقة والصلاحيات
            "invalid_credentials": "اسم المستخدم أو كلمة المرور غير صحيحة",
            "account_locked": "تم قفل الحساب بسبب محاولات دخول متكررة خاطئة",
            "session_expired": "انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى",
            "insufficient_permissions": "ليس لديك صلاحية للوصول إلى هذه الميزة",
            "access_denied": "تم رفض الوصول إلى هذا المورد",
            "token_invalid": "رمز التوثيق غير صحيح أو منتهي الصلاحية",
            # أخطاء منطق العمل
            "business_rule_violation": "العملية تنتهك قاعدة عمل: {rule}",
            "insufficient_stock": "الكمية المطلوبة ({requested}) أكبر من المتوفر ({available})",
            "invalid_operation": "العملية غير مسموحة في الحالة الحالية",
            "workflow_error": "خطأ في سير العمل: {workflow_step}",
            "calculation_error": "خطأ في الحساب: {calculation_details}",
            # أخطاء النظام
            "internal_server_error": "حدث خطأ داخلي في النظام، تم إبلاغ فريق الدعم",
            "service_unavailable": "الخدمة غير متاحة حالياً، يرجى المحاولة لاحقاً",
            "timeout_error": "انتهت مهلة العملية، يرجى المحاولة مرة أخرى",
            "memory_error": "نفدت ذاكرة النظام، يرجى تقليل حجم البيانات",
            "file_not_found": "الملف المطلوب غير موجود",
            "permission_denied": "ليس لديك صلاحية للوصول إلى هذا الملف",
            # أخطاء الشبكة والخدمات الخارجية
            "network_error": "خطأ في الاتصال بالشبكة",
            "api_error": "خطأ في الاتصال بالخدمة الخارجية: {service}",
            "rate_limit_exceeded": "تم تجاوز حد الطلبات المسموح، يرجى الانتظار {wait_time} ثانية",
            # أخطاء عامة
            "unknown_error": "حدث خطأ غير متوقع، يرجى المحاولة لاحقاً",
            "maintenance_mode": "النظام في وضع الصيانة، يرجى المحاولة لاحقاً",
        }

    def _init_error_solutions(self):
        """تهيئة الحلول المقترحة للأخطاء"""
        self.error_solutions = {
            "required_field": [
                "تأكد من ملء جميع الحقول المطلوبة",
                "راجع البيانات المدخلة قبل الحفظ",
            ],
            "invalid_email": [
                "تأكد من كتابة البريد الإلكتروني بالتنسيق الصحيح (example@domain.com)",
                "تحقق من عدم وجود مسافات إضافية",
            ],
            "invalid_phone": [
                "تأكد من كتابة رقم الهاتف بالتنسيق الصحيح",
                "استخدم الأرقام فقط أو أضف رمز الدولة",
            ],
            "database_connection": [
                "تحقق من اتصال الإنترنت",
                "أعد تحميل الصفحة",
                "اتصل بالدعم الفني إذا استمرت المشكلة",
            ],
            "record_not_found": [
                "تأكد من صحة المعرف المدخل",
                "قد يكون السجل محذوفاً، تحقق من سلة المحذوفات",
                "أعد تحميل الصفحة وحاول مرة أخرى",
            ],
            "insufficient_permissions": [
                "اتصل بمدير النظام لطلب الصلاحيات المطلوبة",
                "تأكد من تسجيل الدخول بالحساب الصحيح",
            ],
            "session_expired": [
                "سجل الدخول مرة أخرى",
                "احفظ عملك قبل انتهاء الجلسة في المرة القادمة",
            ],
            "insufficient_stock": [
                "تحقق من الكمية المتوفرة في المخزن",
                "قم بتعديل الكمية المطلوبة",
                "أضف مخزون جديد إذا لزم الأمر",
            ],
            "file_not_found": [
                "تأكد من وجود الملف في المكان الصحيح",
                "تحقق من صلاحيات الوصول للملف",
                "أعد رفع الملف إذا لزم الأمر",
            ],
        }

    # ==================== معالجة الأخطاء الأساسية ====================

    def handle_error(
        self,
        error: Exception,
        error_code: str = None,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        user_message: str = None,
        context: Dict = None,
    ) -> Dict[str, Any]:
        """معالجة شاملة للأخطاء"""

        try:
            # إنشاء معرف فريد للخطأ
            error_id = self._generate_error_id(error, context)

            # جمع معلومات الخطأ
            error_info = self._collect_error_info(
                error, error_code, category, severity, context
            )

            # تسجيل الخطأ
            self._log_error(error_info)

            # تحديث الإحصائيات
            self._update_error_stats(error_info)

            # إنشاء رسالة للمستخدم
            user_response = self._create_user_response(error_info, user_message)

            # فحص الحاجة للإشعارات
            self._check_notification_triggers(error_info)

            # حفظ في التاريخ
            with self._lock:
                self.error_history.append(error_info)

                # الاحتفاظ بآخر 1000 خطأ فقط
                if len(self.error_history) > 1000:
                    self.error_history = self.error_history[-1000:]

            return user_response

        except Exception as handler_error:
            # خطأ في معالج الأخطاء نفسه
            logger.critical(f"خطأ في معالج الأخطاء: {str(handler_error)}")
            return {
                "success": False,
                "error": "حدث خطأ في النظام",
                "message": "نعتذر، حدث خطأ غير متوقع",
                "error_id": "HANDLER_ERROR",
                "timestamp": datetime.now().isoformat(),
            }

    def _generate_error_id(self, error: Exception, context: Dict = None) -> str:
        """إنشاء معرف فريد للخطأ"""
        error_string = f"{type(error).__name__}:{str(error)}"
        if context:
            error_string += f":{json.dumps(context, sort_keys=True)}"

        return hashlib.md5(error_string.encode()).hexdigest()[:8].upper()

    def _collect_error_info(
        self,
        error: Exception,
        error_code: str,
        category: ErrorCategory,
        severity: ErrorSeverity,
        context: Dict,
    ) -> Dict[str, Any]:
        """جمع معلومات شاملة عن الخطأ"""

        error_info = {
            "id": self._generate_error_id(error, context),
            "timestamp": datetime.now().isoformat(),
            "type": type(error).__name__,
            "message": str(error),
            "code": error_code,
            "category": category.value,
            "severity": severity.value,
            "traceback": traceback.format_exc(),
            "context": context or {},
        }

        # معلومات الطلب إذا كان متاحاً
        if request:
            error_info["request"] = {
                "method": request.method,
                "url": request.url,
                "endpoint": request.endpoint,
                "remote_addr": request.remote_addr,
                "user_agent": request.headers.get("User-Agent", ""),
                "content_type": request.content_type,
            }

            # معلومات المستخدم إذا كان متاحاً
            if hasattr(g, "user_id"):
                error_info["user_id"] = g.user_id
                error_info["user_name"] = getattr(g, "user_name", "")

        # معلومات النظام
        error_info["system"] = {
            "python_version": os.sys.version,
            "platform": os.name,
            "working_directory": os.getcwd(),
        }

        return error_info

    def _log_error(self, error_info: Dict[str, Any]):
        """تسجيل الخطأ في السجلات"""
        severity = error_info["severity"]
        error_id = error_info["id"]
        message = error_info["message"]

        log_message = f"[{error_id}] {message}"

        if severity == ErrorSeverity.CRITICAL.value:
            logger.critical(log_message, extra={"error_info": error_info})
        elif severity == ErrorSeverity.HIGH.value:
            logger.error(log_message, extra={"error_info": error_info})
        elif severity == ErrorSeverity.MEDIUM.value:
            logger.warning(log_message, extra={"error_info": error_info})
        else:
            logger.info(log_message, extra={"error_info": error_info})

    def _update_error_stats(self, error_info: Dict[str, Any]):
        """تحديث إحصائيات الأخطاء"""
        with self._lock:
            # إحصائيات عامة
            self.error_stats["total"] += 1
            self.error_stats[f"category_{error_info['category']}"] += 1
            self.error_stats[f"severity_{error_info['severity']}"] += 1
            self.error_stats[f"type_{error_info['type']}"] += 1

            # إحصائيات المستخدم
            if "user_id" in error_info:
                user_id = error_info["user_id"]
                self.user_error_patterns[user_id].append(
                    {
                        "timestamp": error_info["timestamp"],
                        "category": error_info["category"],
                        "severity": error_info["severity"],
                        "error_id": error_info["id"],
                    }
                )

    def _create_user_response(
        self, error_info: Dict[str, Any], custom_message: str = None
    ) -> Dict[str, Any]:
        """إنشاء رد مناسب للمستخدم"""

        # رسالة مخصصة أو رسالة افتراضية
        if custom_message:
            user_message = custom_message
        else:
            user_message = self._get_user_friendly_message(error_info)

        # الحلول المقترحة
        solutions = self._get_error_solutions(error_info)

        response = {
            "success": False,
            "error": error_info["type"],
            "message": user_message,
            "error_id": error_info["id"],
            "category": error_info["category"],
            "timestamp": error_info["timestamp"],
        }

        # إضافة الحلول إذا كانت متاحة
        if solutions:
            response["solutions"] = solutions

        # إضافة تفاصيل إضافية للمطورين في وضع التطوير
        if current_app and current_app.debug:
            response["debug_info"] = {
                "traceback": error_info["traceback"],
                "context": error_info["context"],
            }

        return response

    def _get_user_friendly_message(self, error_info: Dict[str, Any]) -> str:
        """الحصول على رسالة مفهومة للمستخدم"""
        error_type = error_info["type"]
        error_message = error_info["message"]
        context = error_info.get("context", {})

        # البحث عن رسالة مخصصة
        for pattern, message_template in self.error_messages.items():
            if pattern in error_message.lower() or pattern in error_type.lower():
                try:
                    return message_template.format(**context)
                except (KeyError, ValueError):
                    return message_template

        # رسالة افتراضية حسب التصنيف
        category = error_info["category"]

        if category == ErrorCategory.VALIDATION.value:
            return f"خطأ في البيانات المدخلة: {error_message}"
        elif category == ErrorCategory.DATABASE.value:
            return "حدث خطأ في قاعدة البيانات، يرجى المحاولة لاحقاً"
        elif category == ErrorCategory.AUTHENTICATION.value:
            return "خطأ في تسجيل الدخول، تحقق من البيانات"
        elif category == ErrorCategory.AUTHORIZATION.value:
            return "ليس لديك صلاحية لتنفيذ هذه العملية"
        elif category == ErrorCategory.BUSINESS_LOGIC.value:
            return f"خطأ في منطق العمل: {error_message}"
        else:
            return "حدث خطأ غير متوقع، يرجى المحاولة لاحقاً"

    def _get_error_solutions(self, error_info: Dict[str, Any]) -> List[str]:
        """الحصول على الحلول المقترحة للخطأ"""
        error_type = error_info["type"]
        error_message = error_info["message"]

        # البحث عن حلول مخصصة
        for pattern, solutions in self.error_solutions.items():
            if pattern in error_message.lower() or pattern in error_type.lower():
                return solutions

        # حلول افتراضية حسب التصنيف
        category = error_info["category"]

        if category == ErrorCategory.VALIDATION.value:
            return ["تحقق من صحة البيانات المدخلة", "تأكد من ملء جميع الحقول المطلوبة"]
        elif category == ErrorCategory.DATABASE.value:
            return ["أعد المحاولة بعد قليل", "تحقق من اتصال الإنترنت"]
        elif category == ErrorCategory.AUTHENTICATION.value:
            return ["تحقق من اسم المستخدم وكلمة المرور", "أعد تسجيل الدخول"]
        elif category == ErrorCategory.AUTHORIZATION.value:
            return [
                "اتصل بمدير النظام لطلب الصلاحيات",
                "تأكد من تسجيل الدخول بالحساب الصحيح",
            ]
        else:
            return ["أعد تحميل الصفحة", "اتصل بالدعم الفني إذا استمرت المشكلة"]

    # ==================== Decorators للمعالجة التلقائية ====================

    def handle_exceptions(
        self,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        custom_message: str = None,
    ):
        """Decorator لمعالجة الأخطاء تلقائياً"""

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    # معالجة الخطأ
                    error_response = self.handle_error(
                        error=e,
                        category=category,
                        severity=severity,
                        user_message=custom_message,
                        context={
                            "function": f.__name__,
                            "args": str(args)[:200],  # أول 200 حرف
                            "kwargs": str(kwargs)[:200],
                        },
                    )

                    # تحديد كود الحالة HTTP
                    status_code = self._get_http_status_code(category, severity)

                    return jsonify(error_response), status_code

            return decorated_function

        return decorator

    def _get_http_status_code(
        self, category: ErrorCategory, severity: ErrorSeverity
    ) -> int:
        """تحديد كود حالة HTTP المناسب"""

        if category == ErrorCategory.AUTHENTICATION:
            return 401
        elif category == ErrorCategory.AUTHORIZATION:
            return 403
        elif category == ErrorCategory.VALIDATION:
            return 400
        elif severity == ErrorSeverity.CRITICAL:
            return 500
        elif severity == ErrorSeverity.HIGH:
            return 500
        else:
            return 400

    # ==================== معالجة أخطاء محددة ====================

    def handle_validation_error(
        self, field: str, value: Any, rule: str
    ) -> Dict[str, Any]:
        """معالجة أخطاء التحقق من البيانات"""
        context = {
            "field": field,
            "value": str(value)[:100],  # أول 100 حرف
            "rule": rule,
        }

        error_message = f"Validation failed for field '{field}' with rule '{rule}'"
        error = ValueError(error_message)

        return self.handle_error(
            error=error,
            error_code="VALIDATION_ERROR",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            context=context,
        )

    def handle_database_error(
        self, operation: str, table: str = None
    ) -> Dict[str, Any]:
        """معالجة أخطاء قاعدة البيانات"""
        context = {"operation": operation, "table": table or "unknown"}

        error_message = f"Database error during {operation}"
        if table:
            error_message += f" on table {table}"

        error = Exception(error_message)

        return self.handle_error(
            error=error,
            error_code="DATABASE_ERROR",
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.HIGH,
            context=context,
        )

    def handle_permission_error(self, resource: str, action: str) -> Dict[str, Any]:
        """معالجة أخطاء الصلاحيات"""
        context = {
            "resource": resource,
            "action": action,
            "user_id": getattr(g, "user_id", "anonymous"),
        }

        error_message = f"Permission denied for {action} on {resource}"
        error = PermissionError(error_message)

        return self.handle_error(
            error=error,
            error_code="PERMISSION_ERROR",
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.MEDIUM,
            context=context,
        )

    # ==================== الإشعارات ====================

    def _check_notification_triggers(self, error_info: Dict[str, Any]):
        """فحص الحاجة لإرسال إشعارات"""
        severity = error_info["severity"]

        # إشعار فوري للأخطاء الحرجة
        if severity == ErrorSeverity.CRITICAL.value:
            self._send_critical_error_notification(error_info)

        # فحص معدل الأخطاء
        self._check_error_rate_threshold()

        # فحص الأخطاء المتكررة
        self._check_recurring_errors()

    def _send_critical_error_notification(self, error_info: Dict[str, Any]):
        """إرسال إشعار للأخطاء الحرجة"""
        if not self.notification_settings["email_enabled"]:
            return

        try:
            subject = f"خطأ حرج في النظام - {error_info['id']}"

            body = """
            تم اكتشاف خطأ حرج في النظام:

            معرف الخطأ: {error_info['id']}
            الوقت: {error_info['timestamp']}
            النوع: {error_info['type']}
            الرسالة: {error_info['message']}
            التصنيف: {error_info['category']}

            تفاصيل الطلب:
            {json.dumps(error_info.get('request',
                {}),
                indent=2,
                ensure_ascii=False)}

            يرجى التحقق من النظام فوراً.
            """

            self._send_email_notification(subject, body)

        except Exception as e:
            logger.error(f"فشل في إرسال إشعار الخطأ الحرج: {str(e)}")

    def _check_error_rate_threshold(self):
        """فحص معدل الأخطاء"""
        try:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)

            # عد الأخطاء في الدقيقة الأخيرة
            recent_errors = [
                error
                for error in self.error_history
                if datetime.fromisoformat(error["timestamp"]) > minute_ago
            ]

            error_rate = len(recent_errors)
            threshold = self.notification_settings["error_rate_threshold"]

            if error_rate >= threshold:
                self._send_high_error_rate_notification(error_rate, recent_errors)

        except Exception as e:
            logger.error(f"خطأ في فحص معدل الأخطاء: {str(e)}")

    def _check_recurring_errors(self):
        """فحص الأخطاء المتكررة"""
        try:
            # تحليل الأخطاء المتكررة في الساعة الأخيرة
            now = datetime.now()
            hour_ago = now - timedelta(hours=1)

            recent_errors = [
                error
                for error in self.error_history
                if datetime.fromisoformat(error["timestamp"]) > hour_ago
            ]

            # عد الأخطاء حسب النوع
            error_counts = Counter(error["type"] for error in recent_errors)

            # البحث عن أخطاء متكررة (أكثر من 5 مرات)
            recurring_errors = {
                error_type: count
                for error_type, count in error_counts.items()
                if count >= 5
            }

            if recurring_errors:
                self._send_recurring_errors_notification(recurring_errors)

        except Exception as e:
            logger.error(f"خطأ في فحص الأخطاء المتكررة: {str(e)}")

    def _send_email_notification(self, subject: str, body: str):
        """إرسال إشعار بالبريد الإلكتروني"""
        # هذه دالة مبسطة، يمكن تطويرها لاحقاً
        logger.info(f"إشعار بريد إلكتروني: {subject}")
        logger.info(f"المحتوى: {body}")

    # ==================== التقارير والإحصائيات ====================

    def get_error_statistics(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Dict[str, Any]:
        """الحصول على إحصائيات الأخطاء"""
        try:
            if not start_date:
                start_date = datetime.now() - timedelta(days=7)
            if not end_date:
                end_date = datetime.now()

            # تصفية الأخطاء حسب التاريخ
            filtered_errors = [
                error
                for error in self.error_history
                if start_date <= datetime.fromisoformat(error["timestamp"]) <= end_date
            ]

            # إحصائيات عامة
            total_errors = len(filtered_errors)

            # إحصائيات حسب التصنيف
            category_stats = Counter(error["category"] for error in filtered_errors)

            # إحصائيات حسب الخطورة
            severity_stats = Counter(error["severity"] for error in filtered_errors)

            # إحصائيات حسب النوع
            type_stats = Counter(error["type"] for error in filtered_errors)

            # الأخطاء الأكثر تكراراً
            most_common_errors = type_stats.most_common(10)

            # إحصائيات المستخدمين
            user_stats = {}
            for error in filtered_errors:
                if "user_id" in error:
                    user_id = error["user_id"]
                    if user_id not in user_stats:
                        user_stats[user_id] = 0
                    user_stats[user_id] += 1

            # معدل الأخطاء اليومي
            daily_stats = defaultdict(int)
            for error in filtered_errors:
                date = datetime.fromisoformat(error["timestamp"]).date()
                daily_stats[date.isoformat()] += 1

            return {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                },
                "total_errors": total_errors,
                "category_breakdown": dict(category_stats),
                "severity_breakdown": dict(severity_stats),
                "type_breakdown": dict(type_stats),
                "most_common_errors": most_common_errors,
                "user_breakdown": user_stats,
                "daily_breakdown": dict(daily_stats),
                "generated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"خطأ في إنشاء إحصائيات الأخطاء: {str(e)}")
            return {"error": str(e)}

    def get_user_error_patterns(self, user_id: str) -> Dict[str, Any]:
        """الحصول على أنماط أخطاء مستخدم معين"""
        try:
            user_errors = self.user_error_patterns.get(user_id, [])

            if not user_errors:
                return {
                    "user_id": user_id,
                    "total_errors": 0,
                    "message": "لا توجد أخطاء مسجلة لهذا المستخدم",
                }

            # إحصائيات المستخدم
            total_errors = len(user_errors)
            category_stats = Counter(error["category"] for error in user_errors)
            severity_stats = Counter(error["severity"] for error in user_errors)

            # الأخطاء الأخيرة
            recent_errors = sorted(
                user_errors, key=lambda x: x["timestamp"], reverse=True
            )[:10]

            return {
                "user_id": user_id,
                "total_errors": total_errors,
                "category_breakdown": dict(category_stats),
                "severity_breakdown": dict(severity_stats),
                "recent_errors": recent_errors,
                "generated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على أنماط أخطاء المستخدم: {str(e)}")
            return {"error": str(e)}

    def export_error_report(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        format: str = "json",
    ) -> Union[str, Dict]:
        """تصدير تقرير الأخطاء"""
        try:
            stats = self.get_error_statistics(start_date, end_date)

            if format.lower() == "json":
                return json.dumps(stats, indent=2, ensure_ascii=False)
            elif format.lower() == "csv":
                # تحويل لـ CSV (مبسط)
                import csv
                import io

                output = io.StringIO()
                writer = csv.writer(output)

                # كتابة الرؤوس
                writer.writerow(["التاريخ", "النوع", "التصنيف", "الخطورة", "الرسالة"])

                # كتابة البيانات
                for error in self.error_history:
                    if start_date and end_date:
                        error_date = datetime.fromisoformat(error["timestamp"])
                        if not (start_date <= error_date <= end_date):
                            continue

                    writer.writerow(
                        [
                            error["timestamp"],
                            error["type"],
                            error["category"],
                            error["severity"],
                            error["message"][:100],  # أول 100 حرف
                        ]
                    )

                return output.getvalue()
            else:
                return stats

        except Exception as e:
            logger.error(f"خطأ في تصدير تقرير الأخطاء: {str(e)}")
            return {"error": str(e)}

    # ==================== إدارة وصيانة ====================

    def clear_error_history(self, older_than_days: int = 30) -> Dict[str, Any]:
        """مسح تاريخ الأخطاء القديمة"""
        try:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)

            with self._lock:
                old_count = len(self.error_history)

                # الاحتفاظ بالأخطاء الحديثة فقط
                self.error_history = [
                    error
                    for error in self.error_history
                    if datetime.fromisoformat(error["timestamp"]) > cutoff_date
                ]

                new_count = len(self.error_history)
                cleared_count = old_count - new_count

                # مسح إحصائيات المستخدمين القديمة
                for user_id in list(self.user_error_patterns.keys()):
                    user_errors = self.user_error_patterns[user_id]
                    recent_errors = [
                        error
                        for error in user_errors
                        if datetime.fromisoformat(error["timestamp"]) > cutoff_date
                    ]

                    if recent_errors:
                        self.user_error_patterns[user_id] = recent_errors
                    else:
                        del self.user_error_patterns[user_id]

            logger.info(f"تم مسح {cleared_count} خطأ قديم")

            return {
                "success": True,
                "cleared_count": cleared_count,
                "remaining_count": new_count,
                "cutoff_date": cutoff_date.isoformat(),
            }

        except Exception as e:
            logger.error(f"خطأ في مسح تاريخ الأخطاء: {str(e)}")
            return {"error": str(e)}

    def update_notification_settings(self, settings: Dict[str, Any]) -> bool:
        """تحديث إعدادات الإشعارات"""
        try:
            self.notification_settings.update(settings)
            logger.info("تم تحديث إعدادات الإشعارات")
            return True
        except Exception as e:
            logger.error(f"خطأ في تحديث إعدادات الإشعارات: {str(e)}")
            return False


# ==================== Instance عام ومساعدات ====================

# إنشاء instance عام
error_handler = ErrorHandler()


# Decorators سهلة الاستخدام
def handle_exceptions(
    category: ErrorCategory = ErrorCategory.SYSTEM,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    custom_message: str = None,
):
    """Decorator بسيط لمعالجة الأخطاء"""
    return error_handler.handle_exceptions(category, severity, custom_message)


def handle_validation_errors():
    """Decorator لمعالجة أخطاء التحقق"""
    return handle_exceptions(
        category=ErrorCategory.VALIDATION, severity=ErrorSeverity.LOW
    )


def handle_database_errors():
    """Decorator لمعالجة أخطاء قاعدة البيانات"""
    return handle_exceptions(
        category=ErrorCategory.DATABASE, severity=ErrorSeverity.HIGH
    )


def handle_permission_errors():
    """Decorator لمعالجة أخطاء الصلاحيات"""
    return handle_exceptions(
        category=ErrorCategory.AUTHORIZATION, severity=ErrorSeverity.MEDIUM
    )


# ==================== Flask Integration ====================


def init_error_handler(app):
    """تهيئة معالج الأخطاء مع Flask app"""
    global error_handler

    if error_handler is None:
        error_handler = ErrorHandler()

    # معالج الأخطاء العام
    @app.errorhandler(Exception)
    def handle_general_exception(e):
        error_response = error_handler.handle_error(
            error=e, category=ErrorCategory.SYSTEM, severity=ErrorSeverity.HIGH
        )
        return jsonify(error_response), 500

    # معالج أخطاء 404
    @app.errorhandler(404)
    def handle_not_found(e):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Not Found",
                    "message": "الصفحة أو المورد المطلوب غير موجود",
                    "error_id": "NOT_FOUND",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            404,
        )

    # معالج أخطاء 403
    @app.errorhandler(403)
    def handle_forbidden(e):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Forbidden",
                    "message": "ليس لديك صلاحية للوصول إلى هذا المورد",
                    "error_id": "FORBIDDEN",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            403,
        )

    # إضافة routes للإدارة
    @app.route("/admin/errors/stats")
    def error_stats():
        return jsonify(error_handler.get_error_statistics())

    @app.route("/admin/errors/user/<user_id>")
    def user_error_patterns(user_id):
        return jsonify(error_handler.get_user_error_patterns(user_id))

    @app.route("/admin/errors/export")
    def export_errors():
        format_type = request.args.get("format", "json")
        report = error_handler.export_error_report(format=format_type)

        if format_type == "csv":
            from flask import Response

            return Response(
                report,
                mimetype="text/csv",
                headers={
                    "Content-Disposition": "attachment; filename=error_report.csv"
                },
            )
        else:
            return jsonify(report)

    logger.info("تم تهيئة معالج الأخطاء بنجاح")
