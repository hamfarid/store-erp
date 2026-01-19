"""
معالجة الأخطاء المحسنة - نظام شامل لمعالجة الاستثناءات
Enhanced Error Handling - Comprehensive exception handling system
"""

import logging
import traceback
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logger = logging.getLogger(__name__)


class ErrorCode:
    """رموز الأخطاء المعيارية"""

    # أخطاء عامة
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"

    # أخطاء قاعدة البيانات
    DATABASE_ERROR = "DATABASE_ERROR"
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    FOREIGN_KEY_CONSTRAINT = "FOREIGN_KEY_CONSTRAINT"

    # أخطاء الذكاء الاصطناعي
    AI_MODEL_ERROR = "AI_MODEL_ERROR"
    AI_PREDICTION_ERROR = "AI_PREDICTION_ERROR"
    AI_TRAINING_ERROR = "AI_TRAINING_ERROR"

    # أخطاء الملفات
    FILE_UPLOAD_ERROR = "FILE_UPLOAD_ERROR"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_SIZE_ERROR = "FILE_SIZE_ERROR"
    FILE_TYPE_ERROR = "FILE_TYPE_ERROR"

    # أخطاء المصادقة
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"

    # أخطاء الأعمال
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    RESOURCE_LOCKED = "RESOURCE_LOCKED"


class CustomException(Exception):
    """استثناء مخصص للنظام"""

    def __init__(
        self,
        message: str,
        error_code: str = ErrorCode.INTERNAL_SERVER_ERROR,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)


class ValidationException(CustomException):
    """استثناء التحقق من صحة البيانات"""

    def __init__(
        self,
        message: str,
        field_errors: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"field_errors": field_errors or {}}
        )


class BusinessRuleException(CustomException):
    """استثناء قواعد الأعمال"""

    def __init__(self, message: str, rule: str):
        super().__init__(
            message=message,
            error_code=ErrorCode.BUSINESS_RULE_VIOLATION,
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"violated_rule": rule}
        )


class AIException(CustomException):
    """استثناء الذكاء الاصطناعي"""

    def __init__(
        self,
        message: str,
        model_name: Optional[str] = None,
        operation: Optional[str] = None
    ):
        super().__init__(
            message=message,
            error_code=ErrorCode.AI_MODEL_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={
                "model_name": model_name,
                "operation": operation
            }
        )


class FileException(CustomException):
    """استثناء الملفات"""

    def __init__(
        self,
        message: str,
        filename: Optional[str] = None,
        file_size: Optional[int] = None
    ):
        super().__init__(
            message=message,
            error_code=ErrorCode.FILE_UPLOAD_ERROR,
            status_code=status.HTTP_400_BAD_REQUEST,
            details={
                "filename": filename,
                "file_size": file_size
            }
        )


class ErrorHandler:
    """معالج الأخطاء الرئيسي"""

    @staticmethod
    def format_error_response(
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        تنسيق استجابة الخطأ
        Format error response
        """
        return {
            "success": False,
            "error": {
                "code": error_code,
                "message": message,
                "details": details or {},
                "timestamp": datetime.now().isoformat(),
                "request_id": request_id
            }
        }

    @staticmethod
    def log_error(
        error: Exception,
        request: Optional[Request] = None,
        user_id: Optional[int] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ):
        """
        تسجيل الخطأ مع السياق
        Log error with context
        """
        context = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }

        if request:
            context.update({
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "client_ip": request.client.host if request.client else None
            })

        if additional_context:
            context.update(additional_context)

        logger.error("خطأ في النظام: %s", error, extra=context)

    @staticmethod
    def handle_database_error(error: SQLAlchemyError) -> CustomException:
        """
        معالجة أخطاء قاعدة البيانات
        Handle database errors
        """
        if isinstance(error, IntegrityError):
            if "UNIQUE constraint failed" in str(
                    error) or "Duplicate entry" in str(error):
                return CustomException(
                    message="البيانات موجودة مسبقاً",
                    error_code=ErrorCode.DUPLICATE_ENTRY,
                    status_code=status.HTTP_409_CONFLICT
                )
            if "FOREIGN KEY constraint failed" in str(error):
                return CustomException(
                    message="انتهاك قيد المفتاح الخارجي",
                    error_code=ErrorCode.FOREIGN_KEY_CONSTRAINT,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        return CustomException(
            message="خطأ في قاعدة البيانات",
            error_code=ErrorCode.DATABASE_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"original_error": str(error)}
        )

    @staticmethod
    def handle_validation_error(error: ValidationError) -> ValidationException:
        """
        معالجة أخطاء التحقق
        Handle validation errors
        """
        field_errors = {}
        for err in error.errors():
            field = ".".join(str(loc) for loc in err["loc"])
            field_errors[field] = err["msg"]

        return ValidationException(
            message="بيانات غير صحيحة",
            field_errors=field_errors
        )


class ErrorMiddleware:
    """وسطاء معالجة الأخطاء"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            request = Request(scope, receive)
            response = await self.handle_exception(exc, request)
            await response(scope, receive, send)

    async def handle_exception(
            self,
            exc: Exception,
            request: Request) -> JSONResponse:
        """
        معالجة الاستثناءات
        Handle exceptions
        """
        request_id = getattr(request.state, "request_id", None)

        # تسجيل الخطأ
        ErrorHandler.log_error(exc, request)

        # معالجة الاستثناءات المخصصة
        if isinstance(exc, CustomException):
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorHandler.format_error_response(
                    error_code=exc.error_code,
                    message=exc.message,
                    details=exc.details,
                    request_id=request_id
                )
            )

        # معالجة أخطاء FastAPI
        elif isinstance(exc, HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorHandler.format_error_response(
                    error_code="HTTP_EXCEPTION",
                    message=exc.detail,
                    request_id=request_id
                )
            )

        # معالجة أخطاء التحقق
        elif isinstance(exc, ValidationError):
            validation_exc = ErrorHandler.handle_validation_error(exc)
            return JSONResponse(
                status_code=validation_exc.status_code,
                content=ErrorHandler.format_error_response(
                    error_code=validation_exc.error_code,
                    message=validation_exc.message,
                    details=validation_exc.details,
                    request_id=request_id
                )
            )

        # معالجة أخطاء قاعدة البيانات
        elif isinstance(exc, SQLAlchemyError):
            db_exc = ErrorHandler.handle_database_error(exc)
            return JSONResponse(
                status_code=db_exc.status_code,
                content=ErrorHandler.format_error_response(
                    error_code=db_exc.error_code,
                    message=db_exc.message,
                    details=db_exc.details,
                    request_id=request_id
                )
            )

        # الأخطاء غير المتوقعة
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ErrorHandler.format_error_response(
                    error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                    message="خطأ داخلي في الخادم",
                    details={
                        "original_error": str(exc)} if logger.level <= logging.DEBUG else {},
                    request_id=request_id))


def setup_error_handlers(app):
    """
    إعداد معالجات الأخطاء
    Setup error handlers
    """

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        ErrorHandler.log_error(exc, request)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorHandler.format_error_response(
                error_code=exc.error_code,
                message=exc.message,
                details=exc.details,
                request_id=getattr(request.state, "request_id", None)
            )
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
            request: Request, exc: ValidationError):
        validation_exc = ErrorHandler.handle_validation_error(exc)
        ErrorHandler.log_error(validation_exc, request)
        return JSONResponse(
            status_code=validation_exc.status_code,
            content=ErrorHandler.format_error_response(
                error_code=validation_exc.error_code,
                message=validation_exc.message,
                details=validation_exc.details,
                request_id=getattr(request.state, "request_id", None)
            )
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(
            request: Request, exc: SQLAlchemyError):
        db_exc = ErrorHandler.handle_database_error(exc)
        ErrorHandler.log_error(db_exc, request)
        return JSONResponse(
            status_code=db_exc.status_code,
            content=ErrorHandler.format_error_response(
                error_code=db_exc.error_code,
                message=db_exc.message,
                details=db_exc.details,
                request_id=getattr(request.state, "request_id", None)
            )
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        ErrorHandler.log_error(exc, request)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorHandler.format_error_response(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                message="خطأ داخلي في الخادم",
                request_id=getattr(request.state, "request_id", None)
            )
        )


class ErrorReporter:
    """مُبلغ الأخطاء للمراقبة والتنبيهات"""

    def __init__(self):
        self.error_counts = {}
        self.critical_errors = []

    def report_error(
        self,
        error: Exception,
        severity: str = "medium",
        context: Optional[Dict[str, Any]] = None
    ):
        """
        إبلاغ عن خطأ للمراقبة
        Report error for monitoring
        """
        error_key = f"{type(error).__name__}:{str(error)[:100]}"

        # عد الأخطاء
        if error_key not in self.error_counts:
            self.error_counts[error_key] = 0
        self.error_counts[error_key] += 1

        # الأخطاء الحرجة
        if severity == "critical":
            self.critical_errors.append({
                "error": str(error),
                "timestamp": datetime.now(),
                "context": context or {}
            })

            # إرسال تنبيه فوري (يمكن تطويره لاحقاً)
            logger.critical("خطأ حرج: %s", error, extra=context or {})

    def get_error_statistics(self) -> Dict[str, Any]:
        """
        جلب إحصائيات الأخطاء
        Get error statistics
        """
        return {
            "total_errors": sum(self.error_counts.values()),
            "unique_errors": len(self.error_counts),
            "most_common_errors": sorted(
                self.error_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "critical_errors_count": len(self.critical_errors),
            "recent_critical_errors": (
                self.critical_errors[-5:] if self.critical_errors else []
            )
        }


# مثيل عام لمُبلغ الأخطاء
error_reporter = ErrorReporter()
