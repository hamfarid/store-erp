"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/error_handling/decorators.py
الوصف: مزخرفات لتسهيل معالجة الأخطاء في النظام
المؤلف: فريق Scan AI
تاريخ الإنشاء: 30 مايو 2025
"""

import functools
import traceback
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from .error_manager import get_error_manager
from .error_types import ErrorData, ErrorSeverity, ErrorType


def catch_errors(
    error_type: ErrorType = ErrorType.APPLICATION_ERROR,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    module_name: Optional[str] = None,
    raise_original: bool = True
):
    """
    مزخرف لالتقاط ومعالجة الأخطاء في الدوال

    Args:
        error_type: نوع الخطأ (اختياري، الافتراضي هو APPLICATION_ERROR)
        severity: شدة الخطأ (اختياري، الافتراضي هو ERROR)
        module_name: اسم الوحدة، إذا كان None سيتم استخدام اسم الوحدة الحالية
        raise_original: ما إذا كان يجب إعادة رفع الاستثناء الأصلي بعد معالجته

    Returns:
        مزخرف الدالة
    """
    def decorator(func):
        # استخدام اسم الوحدة من الدالة إذا لم يتم تحديده
        nonlocal module_name
        if module_name is None:
            module_name = func.__module__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # الحصول على معرف المستخدم الحالي إذا كان متاحاً
                user_id = None
                try:
                    from ..security.security_middleware import get_current_user_id
                    user_id = get_current_user_id()
                except ImportError:
                    pass

                # معالجة الخطأ
                error_manager = get_error_manager()
                error_data = error_manager.handle_exception(
                    exception=e,
                    error_type=error_type,
                    severity=severity,
                    module_name=module_name,
                    function_name=func.__name__,
                    user_id=user_id,
                    details={
                        "args": str(args),
                        "kwargs": str(kwargs)
                    }
                )

                # إعادة رفع الاستثناء الأصلي إذا كان مطلوباً
                if raise_original:
                    raise

                return error_data

        return wrapper

    return decorator


def api_error_handler(func):
    """
    مزخرف لمعالجة الأخطاء في واجهات برمجة التطبيقات

    Args:
        func: الدالة المراد تزيينها

    Returns:
        الدالة المزينة
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            # معالجة استثناءات HTTP
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            # الحصول على معرف المستخدم الحالي إذا كان متاحاً
            user_id = None
            try:
                from ..security.security_middleware import get_current_user_id
                user_id = get_current_user_id()
            except ImportError:
                pass

            # إنشاء تفاصيل الخطأ
            details = {
                "status_code": e.status_code,
                "headers": dict(e.headers) if e.headers else {}
            }

            # إضافة معلومات الطلب إذا كانت متوفرة
            if request:
                details["request_path"] = request.url.path
                details["request_method"] = request.method
                details["user_agent"] = request.headers.get("user-agent")
                details["ip_address"] = request.client.host if request.client else None

            # معالجة الخطأ
            error_manager = get_error_manager()
            error_data = ErrorData(
                error_type=ErrorType.HTTP_ERROR,
                severity=ErrorSeverity.WARNING if e.status_code < 500 else ErrorSeverity.ERROR,
                message=str(
                    e.detail),
                code=f"http_{e.status_code}",
                details=details,
                user_id=user_id,
                module_name=func.__module__,
                function_name=func.__name__,
                http_status_code=e.status_code)
            error_manager.handle_error(error_data)

            # إعادة رفع الاستثناء لمعالجته بواسطة FastAPI
            raise
        except Exception as e:
            # معالجة الاستثناءات العامة
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            # الحصول على معرف المستخدم الحالي إذا كان متاحاً
            user_id = None
            try:
                from ..security.security_middleware import get_current_user_id
                user_id = get_current_user_id()
            except ImportError:
                pass

            # إنشاء تفاصيل الخطأ
            details = {
                "traceback": traceback.format_exc()
            }

            # إضافة معلومات الطلب إذا كانت متوفرة
            if request:
                details["request_path"] = request.url.path
                details["request_method"] = request.method
                details["user_agent"] = request.headers.get("user-agent")
                details["ip_address"] = request.client.host if request.client else None

            # معالجة الخطأ
            error_manager = get_error_manager()
            error_data = error_manager.handle_exception(
                exception=e,
                error_type=ErrorType.APPLICATION_ERROR,
                severity=ErrorSeverity.ERROR,
                module_name=func.__module__,
                function_name=func.__name__,
                user_id=user_id,
                details=details
            )

            # إنشاء استجابة JSON للخطأ
            error_response = error_data.to_user_friendly_dict()
            return JSONResponse(
                status_code=500,
                content={"error": error_response}
            )

    return wrapper
