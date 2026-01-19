"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/user_management/api.py
الوصف: واجهة برمجة التطبيقات لخدمة أمان المستخدمين
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from src.database import get_db
from src.modules.user_management.security import UserSecurityService
from src.modules.activity_log.integration import ActivityLogger

# تعريف الثوابت
UNKNOWN_USER_AGENT = "غير معروف"

# إنشاء موجه API
router = APIRouter(
    prefix="/api/security",
    tags=["security"],
    responses={404: {"description": "Not found"}},
)

# إنشاء مسجل الأنشطة
activity_logger = ActivityLogger()


@router.post("/unblock-user/{user_id}")
async def unblock_user(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    إلغاء حظر مستخدم

    المعلمات:
        user_id: معرف المستخدم المراد إلغاء حظره
        request: كائن الطلب
        db: جلسة قاعدة البيانات

    العائد:
        رسالة نجاح العملية
    """
    # الحصول على معرف المستخدم المسؤول من الطلب
    admin_id = request.state.user_id

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="يجب تسجيل الدخول لإلغاء حظر المستخدمين"
        )

    # إنشاء خدمة الأمان
    security_service = UserSecurityService(db)

    # إلغاء حظر المستخدم
    success = security_service.unblock_user(user_id, admin_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="لم يتم العثور على المستخدم"
        )

    # تسجيل النشاط
    activity_logger.log_admin_action(
        admin_id=admin_id,
        action="unblock_user",
        target_type="user",
        target_id=user_id,
        details={
            "ip_address": request.client.host,
            "user_agent": request.headers.get("user-agent", UNKNOWN_USER_AGENT)
        }
    )

    return {"message": "تم إلغاء حظر المستخدم بنجاح"}


@router.get("/blocked-users")
async def get_blocked_users(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    الحصول على قائمة المستخدمين المحظورين

    المعلمات:
        request: كائن الطلب
        db: جلسة قاعدة البيانات

    العائد:
        قائمة المستخدمين المحظورين
    """
    # الحصول على معرف المستخدم المسؤول من الطلب
    admin_id = request.state.user_id

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="يجب تسجيل الدخول للوصول إلى قائمة المستخدمين المحظورين"
        )

    # إنشاء خدمة الأمان
    security_service = UserSecurityService(db)

    # الحصول على قائمة المستخدمين المحظورين
    blocked_users = security_service.get_blocked_users()

    # تسجيل النشاط
    activity_logger.log_admin_action(
        admin_id=admin_id,
        action="view_blocked_users",
        target_type="system",
        target_id=None,
        details={
            "ip_address": request.client.host,
            "user_agent": request.headers.get("user-agent", UNKNOWN_USER_AGENT),
            "blocked_users_count": len(blocked_users)
        }
    )

    # تحويل المستخدمين إلى قائمة من القواميس
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "failed_login_attempts": user.failed_login_attempts,
            "locked_until": user.locked_until.isoformat() if user.locked_until else None,
            "is_active": user.is_active
        }
        for user in blocked_users
    ]


@router.get("/is-blocked/{user_id}")
async def is_user_blocked(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    التحقق مما إذا كان المستخدم محظوراً

    المعلمات:
        user_id: معرف المستخدم
        request: كائن الطلب
        db: جلسة قاعدة البيانات

    العائد:
        حالة حظر المستخدم
    """
    # الحصول على معرف المستخدم المسؤول من الطلب
    admin_id = request.state.user_id

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="يجب تسجيل الدخول للتحقق من حالة حظر المستخدم"
        )

    # إنشاء خدمة الأمان
    security_service = UserSecurityService(db)

    # التحقق مما إذا كان المستخدم محظوراً
    is_blocked = security_service.is_user_blocked(user_id)

    return {"is_blocked": is_blocked}


@router.get("/stats")
async def get_security_stats(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    الحصول على إحصائيات الأمان

    المعلمات:
        request: كائن الطلب
        db: جلسة قاعدة البيانات

    العائد:
        إحصائيات الأمان
    """
    # الحصول على معرف المستخدم المسؤول من الطلب
    admin_id = request.state.user_id

    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="يجب تسجيل الدخول للوصول إلى إحصائيات الأمان"
        )

    # إنشاء خدمة الأمان
    security_service = UserSecurityService(db)

    # الحصول على قائمة المستخدمين المحظورين
    blocked_users = security_service.get_blocked_users()

    # تسجيل النشاط
    activity_logger.log_admin_action(
        admin_id=admin_id,
        action="view_security_stats",
        target_type="system",
        target_id=None,
        details={
            "ip_address": request.client.host,
            "user_agent": request.headers.get("user-agent", UNKNOWN_USER_AGENT)
        }
    )

    # إحصائيات الأمان
    return {
        "blocked_users_count": len(blocked_users),
        "blocked_users": [
            {
                "id": user.id,
                "username": user.username,
                "locked_until": user.locked_until.isoformat() if user.locked_until else None
            }
            for user in blocked_users
        ]
    }
