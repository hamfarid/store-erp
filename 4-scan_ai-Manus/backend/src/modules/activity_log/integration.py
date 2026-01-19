"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/activity_log/integration.py
الوصف: ملف تكامل سجل النشاط مع جميع مديولات النظام
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import logging
from functools import wraps
from typing import Any, Dict, List, Optional, Tuple

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from src.modules.activity_log.models import ActivityLog

# إعداد التسجيل
logger = logging.getLogger(__name__)


def _extract_context_from_args(
        args: tuple) -> Tuple[Optional[Session], Optional[dict], Optional[BackgroundTasks]]:
    """استخراج السياق من المعلمات الموضعية"""
    db = None
    current_user = None
    background_tasks = None

    for arg in args:
        if isinstance(arg, Session):
            db = arg
        elif isinstance(arg, BackgroundTasks):
            background_tasks = arg
        elif isinstance(arg, dict) and "id" in arg and "username" in arg:
            current_user = arg

    return db, current_user, background_tasks


def _extract_context_from_kwargs(
        kwargs: dict) -> Tuple[Optional[Session], Optional[dict], Optional[BackgroundTasks]]:
    """استخراج السياق من المعلمات المسمية"""
    db = None
    current_user = None
    background_tasks = None

    for key, value in kwargs.items():
        if key == "db" and isinstance(value, Session):
            db = value
        elif key == "background_tasks" and isinstance(value, BackgroundTasks):
            background_tasks = value
        elif key == "current_user" and isinstance(value, dict) and "id" in value and "username" in value:
            current_user = value

    return db, current_user, background_tasks


def _extract_context(args: tuple,
                     kwargs: dict) -> Tuple[Optional[Session],
                                            Optional[dict],
                                            Optional[BackgroundTasks]]:
    """استخراج السياق من المعلمات"""
    db_args, current_user_args, background_tasks_args = _extract_context_from_args(
        args)
    db_kwargs, current_user_kwargs, background_tasks_kwargs = _extract_context_from_kwargs(
        kwargs)

    return (
        db_args or db_kwargs,
        current_user_args or current_user_kwargs,
        background_tasks_args or background_tasks_kwargs
    )


def _process_include_params(include_params: str) -> Dict[str, bool]:
    """معالجة معلمات التضمين"""
    if not include_params:
        return {}

    params = include_params.split(',')
    return {param.strip(): True for param in params if param.strip()}


def _process_request_data(kwargs: dict,
                          exclude_params: List[str],
                          include_request_data: bool,
                          include_response_data: bool,
                          result: Any) -> Dict[str,
                                               Any]:
    """معالجة بيانات الطلب"""
    request_data = {}
    if include_request_data:
        request_data = {
            k: v for k,
            v in kwargs.items() if k not in exclude_params}
    if include_response_data and result is not None:
        request_data["response"] = result
    return request_data


def _prepare_log_data(
    module_id: str,
    action_id: str,
    log_type: str,
    description: str,
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """تحضير بيانات السجل"""
    log_data = {
        "module_id": module_id,
        "action_id": action_id,
        "log_type": log_type,
        "description": description,
        **kwargs
    }

    if include_request_data and result and "request" in result:
        log_data["request_data"] = result["request"]

    if include_response_data and result and "response" in result:
        log_data["response_data"] = result["response"]

    return log_data


def _create_description(
    module_id: str,
    action_id: str,
    log_type: str,
    result: Optional[Dict[str, Any]] = None
) -> str:
    """إنشاء وصف للسجل"""
    description = f"{module_id} - {action_id} - {log_type}"

    if result and "error" in result:
        description += f" - Error: {result['error']}"

    return description


def _log_system_error(
    module_id: str,
    action_id: str,
    error: str,
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """تسجيل خطأ النظام"""
    description = _create_description(
        module_id, action_id, "system_error", result)
    log_data = _prepare_log_data(
        module_id=module_id,
        action_id=action_id,
        log_type="system_error",
        description=description,
        include_request_data=include_request_data,
        include_response_data=include_response_data,
        result=result,
        error=error,
        **kwargs
    )
    _log_activity(log_data)


def _log_user_error(
    module_id: str,
    action_id: str,
    error: str,
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """تسجيل خطأ المستخدم"""
    description = _create_description(
        module_id, action_id, "user_error", result)
    log_data = _prepare_log_data(
        module_id=module_id,
        action_id=action_id,
        log_type="user_error",
        description=description,
        include_request_data=include_request_data,
        include_response_data=include_response_data,
        result=result,
        error=error,
        **kwargs
    )
    _log_activity(log_data)


def _log_ai_error(
    module_id: str,
    action_id: str,
    error: str,
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """تسجيل خطأ الذكاء الاصطناعي"""
    description = _create_description(module_id, action_id, "ai_error", result)
    log_data = _prepare_log_data(
        module_id=module_id,
        action_id=action_id,
        log_type="ai_error",
        description=description,
        include_request_data=include_request_data,
        include_response_data=include_response_data,
        result=result,
        error=error,
        **kwargs
    )
    _log_activity(log_data)


def _log_error(
    module_id: str,
    action_id: str,
    error: str,
    log_type: str = "system_error",
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """تسجيل خطأ"""
    error_handlers = {
        "system_error": _log_system_error,
        "user_error": _log_user_error,
        "ai_error": _log_ai_error
    }

    handler = error_handlers.get(log_type, _log_system_error)
    handler(
        module_id=module_id,
        action_id=action_id,
        error=error,
        include_request_data=include_request_data,
        include_response_data=include_response_data,
        result=result,
        **kwargs
    )


def _log_system_activity(
    module_id: str,
    action_id: str,
    description: str,
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """تسجيل نشاط النظام"""
    log_data = _prepare_log_data(
        module_id=module_id,
        action_id=action_id,
        log_type="system",
        description=description,
        include_request_data=include_request_data,
        include_response_data=include_response_data,
        result=result,
        **kwargs
    )
    _log_activity(log_data)


def _log_user_activity(
    module_id: str,
    action_id: str,
    description: str,
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """تسجيل نشاط المستخدم"""
    log_data = _prepare_log_data(
        module_id=module_id,
        action_id=action_id,
        log_type="user",
        description=description,
        include_request_data=include_request_data,
        include_response_data=include_response_data,
        result=result,
        **kwargs
    )
    _log_activity(log_data)


def _log_ai_activity(
    module_id: str,
    action_id: str,
    description: str,
    include_request_data: bool = False,
    include_response_data: bool = False,
    result: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """تسجيل نشاط الذكاء الاصطناعي"""
    log_data = _prepare_log_data(
        module_id=module_id,
        action_id=action_id,
        log_type="ai",
        description=description,
        include_request_data=include_request_data,
        include_response_data=include_response_data,
        result=result,
        **kwargs
    )
    _log_activity(log_data)


def _log_activity(log_data: Dict[str, Any]) -> None:
    """تسجيل النشاط"""
    try:
        activity_log = ActivityLog.from_dict(log_data)
        _save_activity_async(activity_log)
    except Exception as e:
        print(f"Error logging activity: {str(e)}")


async def _save_activity_async(activity_log: ActivityLog) -> None:
    """حفظ سجل النشاط بشكل غير متزامن"""
    try:
        from src.database import async_session
        async with async_session() as session:
            session.add(activity_log)
            await session.commit()
    except Exception as e:
        print(f"Error saving activity log: {str(e)}")


def log_activity(
    module_id: str,
    action_id: str,
    log_type: str = "user",
    include_request_data: bool = False,
    include_response_data: bool = False
):
    """مزخرف لتسجيل النشاط"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # تنفيذ الوظيفة
                result = await func(*args, **kwargs)

                # تحضير بيانات السجل
                activity_data = _prepare_log_data(
                    module_id=module_id,
                    action_id=action_id,
                    log_type=log_type,
                    description=_create_description(
                        module_id,
                        action_id,
                        log_type,
                        result
                    ),
                    include_request_data=include_request_data,
                    include_response_data=include_response_data,
                    result=result
                )

                # تسجيل النشاط
                _log_activity(activity_data)

                return result

            except Exception as e:
                # تسجيل الخطأ
                _log_error(
                    module_id=module_id,
                    action_id=action_id,
                    error=str(e),
                    log_type=log_type,
                    include_request_data=include_request_data,
                    include_response_data=include_response_data,
                    result={"error": str(e)}
                )
                raise

        return wrapper
    return decorator


def log_system_startup(app):
    """مزخرف لتسجيل بدء تشغيل النظام"""
    @app.on_event("startup")
    async def startup_event():
        try:
            activity_data = _prepare_log_data(
                module_id="system",
                action_id="startup",
                log_type="system",
                description="بدء تشغيل النظام",
                include_request_data=True,
                include_response_data=True,
                result={"version": "1.0.0"}
            )
            _log_activity(activity_data)
        except Exception as e:
            logger.error(f"خطأ في تسجيل بدء تشغيل النظام: {str(e)}")


def log_system_shutdown(app):
    """مزخرف لتسجيل إيقاف النظام"""
    @app.on_event("shutdown")
    async def shutdown_event():
        try:
            activity_data = _prepare_log_data(
                module_id="system",
                action_id="shutdown",
                log_type="system",
                description="إيقاف النظام",
                include_request_data=True,
                include_response_data=True,
                result={"reason": "normal"}
            )
            _log_activity(activity_data)
        except Exception as e:
            logger.error(f"خطأ في تسجيل إيقاف النظام: {str(e)}")


async def log_login_attempt(
    username: str,
    success: bool,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    user_id: Optional[int] = None
):
    """تسجيل محاولة تسجيل الدخول"""
    status = "success" if success else "error"
    description = f"محاولة تسجيل دخول {'ناجحة' if success else 'فاشلة'} للمستخدم {username}"

    activity_data = _prepare_log_data(
        module_id="auth",
        action_id="login",
        log_type="user",
        description=description,
        include_request_data=True,
        include_response_data=True,
        result={
            "status": status,
            "ip_address": ip_address,
            "user_agent": user_agent},
        current_user={
            "id": user_id,
            "username": username} if user_id else None)

    _log_activity(activity_data)


async def log_permission_check(
    user_id: int,
    module_id: str,
    permission: str,
    granted: bool,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """تسجيل فحص الصلاحية"""
    status = "success" if granted else "error"
    description = f"فحص صلاحية {permission} في {module_id} {'ممنوح' if granted else 'مرفوض'}"
    log_data = {
        "status": status,
        "permission": permission,
        "ip_address": ip_address,
        "user_agent": user_agent
    }

    activity_data = _prepare_log_data(
        module_id="auth",
        action_id="permission_check",
        log_type="user",
        description=description,
        include_request_data=True,
        include_response_data=True,
        result=log_data,
        current_user={"id": user_id}
    )

    _log_activity(activity_data)


async def log_data_change(
    user_id: int,
    module_id: str,
    action_id: str,
    resource_type: str,
    resource_id: str,
    description: str,
    before_state: Optional[Dict[str, Any]] = None,
    after_state: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """تسجيل تغيير البيانات"""
    log_data = {
        "resource_type": resource_type,
        "resource_id": resource_id,
        "before_state": before_state,
        "after_state": after_state,
        "ip_address": ip_address,
        "user_agent": user_agent
    }

    activity_data = _prepare_log_data(
        module_id=module_id,
        action_id=action_id,
        log_type="user",
        description=description,
        include_request_data=True,
        include_response_data=True,
        result=log_data,
        current_user={"id": user_id}
    )

    _log_activity(activity_data)


async def log_ai_query(
    agent_id: str,
    agent_type: str,
    module_id: str,
    query: str,
    response: str,
    user_id: Optional[int] = None,
    tokens_used: Optional[int] = None,
    processing_time: Optional[int] = None,
    confidence_score: Optional[int] = None
):
    """تسجيل استعلام الذكاء الاصطناعي"""
    log_data = {
        "query": query,
        "response": response,
        "tokens_used": tokens_used,
        "processing_time": processing_time,
        "confidence_score": confidence_score
    }

    activity_data = _prepare_log_data(
        module_id=module_id,
        action_id="ai_query",
        log_type="ai",
        description=f"استعلام من {agent_type} {agent_id}",
        include_request_data=True,
        include_response_data=True,
        result=log_data,
        current_user={"id": user_id} if user_id else None
    )

    _log_activity(activity_data)


async def log_a2a_communication(
    sender_id: str,
    sender_type: str,
    receiver_id: str,
    receiver_type: str,
    module_id: str,
    message: str,
    response: Optional[str] = None,
    user_id: Optional[int] = None
):
    """تسجيل اتصال بين وكلاء الذكاء الاصطناعي"""
    log_data = {
        "sender_id": sender_id,
        "sender_type": sender_type,
        "receiver_id": receiver_id,
        "receiver_type": receiver_type,
        "message": message,
        "response": response
    }

    activity_data = _prepare_log_data(
        module_id=module_id,
        action_id="a2a_communication",
        log_type="ai",
        description=f"تواصل من {sender_type} {sender_id} إلى {receiver_type} {receiver_id}",
        include_request_data=True,
        include_response_data=True,
        result=log_data,
        current_user={
            "id": user_id} if user_id else None)

    _log_activity(activity_data)
