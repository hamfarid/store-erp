# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/feedback/api.py
"""
واجهة برمجة التطبيقات لوحدة التغذية الراجعة
توفر هذه الوحدة واجهات برمجية للتعامل مع التغذية الراجعة من المستخدمين
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from src.modules.auth.api import check_permission, get_current_user

from . import config, schemas
from .service import feedback_service

# إعداد التسجيل
logger = logging.getLogger(__name__)

# إنشاء موجه API
router = APIRouter(
    prefix="/api/feedback",
    tags=["feedback"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Dict[str, Any])
async def create_feedback(
    feedback_data: schemas.FeedbackCreate,
    current_user: dict = Depends(get_current_user)
):
    """إنشاء تغذية راجعة جديدة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.ADD_FEEDBACK):
            raise HTTPException(status_code=403,
                                detail="ليس لديك صلاحية لإضافة تغذية راجعة")

        feedback = feedback_service.create_feedback(
            feedback_data, current_user["id"])

        return {
            "status": "success",
            "data": {
                "id": feedback.id,
                "title": feedback.title,
                "feedback_type": str(feedback.feedback_type.value),
                "status": str(feedback.status.value)
            },
            "message": "تم إنشاء التغذية الراجعة بنجاح"
        }
    except Exception as e:
        logger.error(f"خطأ في إنشاء تغذية راجعة جديدة: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Dict[str, Any])
async def get_all_feedback(
    status: Optional[str] = None,
    feedback_type: Optional[str] = None,
    priority: Optional[str] = None,
    module_name: Optional[str] = None,
    user_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search_query: Optional[str] = None,
    tags: Optional[List[int]] = Query(None),
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_desc: bool = True,
    include_details: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على قائمة التغذية الراجعة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.VIEW_FEEDBACK):
            raise HTTPException(status_code=403,
                                detail="ليس لديك صلاحية لعرض التغذية الراجعة")

        # تحويل المعلمات
        filter_params = schemas.FeedbackFilter(
            status=getattr(
                config.FeedbackStatus,
                status.upper()) if status else None,
            feedback_type=getattr(
                config.FeedbackType,
                feedback_type.upper()) if feedback_type else None,
            priority=getattr(
                config.FeedbackPriority,
                priority.upper()) if priority else None,
            module_name=module_name,
            user_id=user_id,
            start_date=datetime.fromisoformat(start_date) if start_date else None,
            end_date=datetime.fromisoformat(end_date) if end_date else None,
            search_query=search_query,
            tags=tags,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)

        # الحصول على التغذية الراجعة
        feedbacks, total_count = feedback_service.get_all_feedback(
            filter_params,
            current_user["id"],
            include_details
        )

        return {
            "status": "success",
            "data": feedbacks,
            "meta": {
                "total": total_count,
                "skip": skip,
                "limit": limit
            }
        }
    except Exception as e:
        logger.error(f"خطأ في الحصول على قائمة التغذية الراجعة: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{feedback_id}", response_model=Dict[str, Any])
async def get_feedback(
    feedback_id: int,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على تغذية راجعة بواسطة المعرف"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.VIEW_FEEDBACK):
            raise HTTPException(status_code=403,
                                detail="ليس لديك صلاحية لعرض التغذية الراجعة")

        feedback = feedback_service.get_feedback_by_id(
            feedback_id, current_user["id"])
        if not feedback:
            raise HTTPException(
                status_code=404,
                detail="التغذية الراجعة غير موجودة")

        # التحقق من صلاحية عرض التفاصيل
        if not check_permission(
                current_user,
                config.FeedbackPermissions.VIEW_FEEDBACK_DETAILS):
            # إزالة الحقول التفصيلية
            if "comments" in feedback:
                del feedback["comments"]
            if "attachments" in feedback:
                del feedback["attachments"]

        return {
            "status": "success",
            "data": feedback
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"خطأ في الحصول على التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{feedback_id}", response_model=Dict[str, Any])
async def update_feedback(
    feedback_id: int,
    feedback_data: schemas.FeedbackUpdate,
    current_user: dict = Depends(get_current_user)
):
    """تحديث تغذية راجعة"""
    try:
        feedback = feedback_service.update_feedback(
            feedback_id, feedback_data, current_user["id"])
        if not feedback:
            raise HTTPException(
                status_code=404,
                detail="التغذية الراجعة غير موجودة")

        return {
            "status": "success",
            "data": {
                "id": feedback.id,
                "title": feedback.title,
                "feedback_type": str(feedback.feedback_type.value),
                "status": str(feedback.status.value),
                "priority": str(feedback.priority.value)
            },
            "message": "تم تحديث التغذية الراجعة بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في تحديث التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{feedback_id}", response_model=Dict[str, Any])
async def delete_feedback(
    feedback_id: int,
    current_user: dict = Depends(get_current_user)
):
    """حذف تغذية راجعة"""
    try:
        result = feedback_service.delete_feedback(
            feedback_id, current_user["id"])
        if not result:
            raise HTTPException(
                status_code=404,
                detail="التغذية الراجعة غير موجودة")

        return {
            "status": "success",
            "message": "تم حذف التغذية الراجعة بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في حذف التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{feedback_id}/comments", response_model=Dict[str, Any])
async def add_comment(
    feedback_id: int,
    comment_data: schemas.CommentCreate,
    current_user: dict = Depends(get_current_user)
):
    """إضافة تعليق على التغذية الراجعة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.ADD_FEEDBACK):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لإضافة تعليقات")

        comment = feedback_service.add_comment(
            feedback_id,
            comment_data.content,
            current_user["id"]
        )

        if not comment:
            raise HTTPException(
                status_code=404,
                detail="التغذية الراجعة غير موجودة")

        return {
            "status": "success",
            "data": {
                "id": comment.id,
                "content": comment.content,
                "user_id": comment.user_id,
                "created_at": comment.created_at
            },
            "message": "تم إضافة التعليق بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"خطأ في إضافة تعليق على التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{feedback_id}/comments", response_model=Dict[str, Any])
async def get_comments(
    feedback_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على تعليقات التغذية الراجعة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(
                current_user,
                config.FeedbackPermissions.VIEW_FEEDBACK_DETAILS):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لعرض التعليقات")

        comments = feedback_service.get_comments(feedback_id, skip, limit)

        return {
            "status": "success",
            "data": comments
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"خطأ في الحصول على تعليقات التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/comments/{comment_id}", response_model=Dict[str, Any])
async def delete_comment(
    comment_id: int,
    current_user: dict = Depends(get_current_user)
):
    """حذف تعليق"""
    try:
        result = feedback_service.delete_comment(
            comment_id, current_user["id"])
        if not result:
            raise HTTPException(status_code=404, detail="التعليق غير موجود")

        return {
            "status": "success",
            "message": "تم حذف التعليق بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في حذف التعليق {comment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{feedback_id}/vote", response_model=Dict[str, Any])
async def add_vote(
    feedback_id: int,
    vote_data: schemas.VoteCreate,
    current_user: dict = Depends(get_current_user)
):
    """إضافة تصويت على التغذية الراجعة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.ADD_FEEDBACK):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية للتصويت")

        vote = feedback_service.add_vote(
            feedback_id,
            current_user["id"],
            vote_data.is_upvote
        )

        if not vote:
            raise HTTPException(
                status_code=404,
                detail="التغذية الراجعة غير موجودة")

        return {
            "status": "success",
            "data": {
                "id": vote.id,
                "is_upvote": vote.is_upvote
            },
            "message": "تم إضافة التصويت بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"خطأ في إضافة تصويت على التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{feedback_id}/vote", response_model=Dict[str, Any])
async def remove_vote(
    feedback_id: int,
    current_user: dict = Depends(get_current_user)
):
    """إزالة تصويت"""
    try:
        result = feedback_service.remove_vote(feedback_id, current_user["id"])
        if not result:
            raise HTTPException(status_code=404, detail="التصويت غير موجود")

        return {
            "status": "success",
            "message": "تم إزالة التصويت بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"خطأ في إزالة تصويت من التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{feedback_id}/votes", response_model=Dict[str, Any])
async def get_vote_count(
    feedback_id: int,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على عدد التصويتات"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.VIEW_FEEDBACK):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لعرض التصويتات")

        votes = feedback_service.get_vote_count(feedback_id)

        return {
            "status": "success",
            "data": votes
        }
    except Exception as e:
        logger.error(
            f"خطأ في الحصول على عدد تصويتات التغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{feedback_id}/attachments", response_model=Dict[str, Any])
async def add_attachment(
    feedback_id: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """إضافة مرفق للتغذية الراجعة"""
    try:
        attachment = await feedback_service.add_attachment(
            feedback_id,
            file,
            current_user["id"]
        )

        if not attachment:
            raise HTTPException(
                status_code=404,
                detail="التغذية الراجعة غير موجودة")

        return {
            "status": "success",
            "data": {
                "id": attachment.id,
                "file_name": attachment.file_name,
                "file_path": attachment.file_path,
                "file_type": attachment.file_type,
                "file_size": attachment.file_size
            },
            "message": "تم إضافة المرفق بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"خطأ في إضافة مرفق للتغذية الراجعة {feedback_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/attachments/{attachment_id}", response_model=Dict[str, Any])
async def delete_attachment(
    attachment_id: int,
    current_user: dict = Depends(get_current_user)
):
    """حذف مرفق"""
    try:
        result = feedback_service.delete_attachment(
            attachment_id, current_user["id"])
        if not result:
            raise HTTPException(status_code=404, detail="المرفق غير موجود")

        return {
            "status": "success",
            "message": "تم حذف المرفق بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في حذف المرفق {attachment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tags", response_model=Dict[str, Any])
async def create_tag(
    tag_data: schemas.TagCreate,
    current_user: dict = Depends(get_current_user)
):
    """إنشاء وسم جديد"""
    try:
        tag = feedback_service.create_tag(tag_data, current_user["id"])

        return {
            "status": "success",
            "data": {
                "id": tag.id,
                "name": tag.name,
                "description": tag.description,
                "color": tag.color
            },
            "message": "تم إنشاء الوسم بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إنشاء وسم جديد: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tags", response_model=Dict[str, Any])
async def get_all_tags(
    current_user: dict = Depends(get_current_user)
):
    """الحصول على جميع الوسوم"""
    try:
        tags = feedback_service.get_all_tags()

        return {
            "status": "success",
            "data": tags
        }
    except Exception as e:
        logger.error(f"خطأ في الحصول على الوسوم: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{feedback_id}/tags/{tag_id}", response_model=Dict[str, Any])
async def add_tag_to_feedback(
    feedback_id: int,
    tag_id: int,
    current_user: dict = Depends(get_current_user)
):
    """إضافة وسم إلى تغذية راجعة"""
    try:
        result = feedback_service.add_tag_to_feedback(
            feedback_id, tag_id, current_user["id"])
        if not result:
            raise HTTPException(status_code=404,
                                detail="التغذية الراجعة أو الوسم غير موجود")

        return {
            "status": "success",
            "message": "تم إضافة الوسم إلى التغذية الراجعة بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إضافة وسم إلى التغذية الراجعة: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{feedback_id}/tags/{tag_id}", response_model=Dict[str, Any])
async def remove_tag_from_feedback(
    feedback_id: int,
    tag_id: int,
    current_user: dict = Depends(get_current_user)
):
    """إزالة وسم من تغذية راجعة"""
    try:
        result = feedback_service.remove_tag_from_feedback(
            feedback_id, tag_id, current_user["id"])
        if not result:
            raise HTTPException(
                status_code=404,
                detail="الارتباط بين التغذية الراجعة والوسم غير موجود")

        return {
            "status": "success",
            "message": "تم إزالة الوسم من التغذية الراجعة بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إزالة وسم من التغذية الراجعة: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics", response_model=Dict[str, Any])
async def get_feedback_statistics(
    current_user: dict = Depends(get_current_user)
):
    """الحصول على إحصائيات التغذية الراجعة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.MANAGE_FEEDBACK):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لعرض إحصائيات التغذية الراجعة")

        stats = feedback_service.get_feedback_statistics()

        return {
            "status": "success",
            "data": stats
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في الحصول على إحصائيات التغذية الراجعة: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending", response_model=Dict[str, Any])
async def get_trending_feedback(
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على التغذية الراجعة الأكثر شعبية"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.VIEW_FEEDBACK):
            raise HTTPException(status_code=403,
                                detail="ليس لديك صلاحية لعرض التغذية الراجعة")

        feedbacks = feedback_service.get_trending_feedback(limit)

        return {
            "status": "success",
            "data": feedbacks
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"خطأ في الحصول على التغذية الراجعة الأكثر شعبية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup", response_model=Dict[str, Any])
async def cleanup_old_feedback(
    current_user: dict = Depends(get_current_user)
):
    """تنظيف التغذية الراجعة القديمة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user,
                                config.FeedbackPermissions.MANAGE_FEEDBACK):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لتنظيف التغذية الراجعة")

        result = feedback_service.cleanup_old_feedback()

        return {
            "status": "success",
            "data": result,
            "message": f"تم حذف {result['total_deleted']} من التغذية الراجعة القديمة بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في تنظيف التغذية الراجعة القديمة: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
