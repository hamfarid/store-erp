# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/feedback/service.py
"""
خدمة إدارة التغذية الراجعة
توفر هذه الوحدة خدمات لإدارة التغذية الراجعة من المستخدمين
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import func, desc, or_
from fastapi import UploadFile, HTTPException

from src.database import get_db
from src.modules.notifications.service import notification_service
from src.modules.permissions.service import has_permission
from . import models, schemas, config

# إعداد التسجيل
logger = logging.getLogger(__name__)


class FeedbackService:
    """خدمة إدارة التغذية الراجعة"""

    def __init__(self):
        """تهيئة خدمة التغذية الراجعة"""
        self.db = next(get_db())

    def create_feedback(self, feedback_data: schemas.FeedbackCreate, user_id: Optional[int] = None) -> models.Feedback:
        """إنشاء تغذية راجعة جديدة"""
        try:
            # إنشاء كائن التغذية الراجعة
            feedback = models.Feedback(
                title=feedback_data.title,
                description=feedback_data.description,
                feedback_type=feedback_data.feedback_type,
                priority=feedback_data.priority,
                status=config.FeedbackStatus.NEW,
                user_id=user_id,
                module_name=feedback_data.module_name
            )

            # إضافة إلى قاعدة البيانات
            self.db.add(feedback)
            self.db.commit()
            self.db.refresh(feedback)

            # إرسال إشعار للمسؤولين
            if config.FEEDBACK_SETTINGS["notify_admins_on_new_feedback"]:
                self._notify_admins_new_feedback(feedback)

            return feedback
        except Exception as e:
            self.db.rollback()
            logger.error("خطأ في إنشاء تغذية راجعة جديدة: %s", str(e))
            raise

    def get_feedback_by_id(self, feedback_id: int, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """الحصول على تغذية راجعة بواسطة المعرف"""
        feedback = self.db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()

        if not feedback:
            return None

        # تحويل إلى قاموس
        result = self._feedback_to_dict(feedback)

        # إضافة معلومات التصويت للمستخدم الحالي
        if user_id:
            user_vote = self.db.query(models.FeedbackVote).filter(
                models.FeedbackVote.feedback_id == feedback_id,
                models.FeedbackVote.user_id == user_id
            ).first()

            if user_vote:
                result["user_vote"] = user_vote.is_upvote

        return result

    def get_all_feedback(
        self,
        filter_params: schemas.FeedbackFilter,
        user_id: Optional[int] = None,
        include_details: bool = False
    ) -> Tuple[List[Dict[str, Any]], int]:
        """الحصول على قائمة التغذية الراجعة مع إمكانية التصفية"""
        query = self.db.query(models.Feedback)

        # تطبيق المرشحات
        if filter_params.status:
            query = query.filter(models.Feedback.status == filter_params.status)
        if filter_params.feedback_type:
            query = query.filter(models.Feedback.feedback_type == filter_params.feedback_type)
        if filter_params.priority:
            query = query.filter(models.Feedback.priority == filter_params.priority)
        if filter_params.module_name:
            query = query.filter(models.Feedback.module_name == filter_params.module_name)
        if filter_params.user_id:
            query = query.filter(models.Feedback.user_id == filter_params.user_id)
        if filter_params.start_date:
            query = query.filter(models.Feedback.created_at >= filter_params.start_date)
        if filter_params.end_date:
            query = query.filter(models.Feedback.created_at <= filter_params.end_date)
        if filter_params.search_query:
            search = f"%{filter_params.search_query}%"
            query = query.filter(
                or_(
                    models.Feedback.title.ilike(search),
                    models.Feedback.description.ilike(search)
                )
            )
        if filter_params.tags and len(filter_params.tags) > 0:
            query = query.join(models.FeedbackTagAssociation).filter(
                models.FeedbackTagAssociation.tag_id.in_(filter_params.tags)
            )

        # الحصول على العدد الإجمالي
        total_count = query.count()

        # ترتيب النتائج
        if filter_params.sort_by == "vote_count":
            # ترتيب حسب عدد التصويتات
            subquery = self.db.query(
                models.FeedbackVote.feedback_id,
                func.count(models.FeedbackVote.id).label("vote_count")
            ).filter(models.FeedbackVote.is_upvote).group_by(
                models.FeedbackVote.feedback_id
            ).subquery()

            query = query.outerjoin(
                subquery,
                models.Feedback.id == subquery.c.feedback_id
            )

            if filter_params.sort_desc:
                query = query.order_by(desc(subquery.c.vote_count.nullsfirst()))
            else:
                query = query.order_by(subquery.c.vote_count.nullslast())
        else:
            # ترتيب حسب الحقل المحدد
            sort_column = getattr(models.Feedback, filter_params.sort_by, models.Feedback.created_at)

            if filter_params.sort_desc:
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)

        # تطبيق الصفحات
        query = query.offset(filter_params.skip).limit(filter_params.limit)

        # الحصول على النتائج
        feedbacks = query.all()

        # تحويل النتائج إلى قواميس
        results = []
        for feedback in feedbacks:
            result = self._feedback_to_dict(feedback, include_details)

            # إضافة معلومات التصويت للمستخدم الحالي
            if user_id:
                user_vote = self.db.query(models.FeedbackVote).filter(
                    models.FeedbackVote.feedback_id == feedback.id,
                    models.FeedbackVote.user_id == user_id
                ).first()

                if user_vote:
                    result["user_vote"] = user_vote.is_upvote

            results.append(result)

        return results, total_count

    def update_feedback(
        self,
        feedback_id: int,
        feedback_data: schemas.FeedbackUpdate,
        user_id: int
    ) -> Optional[models.Feedback]:
        """تحديث التغذية الراجعة"""
        feedback = self.db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        if not feedback:
            return None

        # التحقق من الصلاحيات
        is_owner = feedback.user_id == user_id
        can_edit = has_permission(user_id, config.FeedbackPermissions.EDIT_FEEDBACK)
        can_manage = has_permission(user_id, config.FeedbackPermissions.MANAGE_FEEDBACK)

        if not (is_owner or can_edit or can_manage):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتعديل هذه التغذية الراجعة")

        # تحديث الحقول
        old_status = feedback.status

        if feedback_data.title is not None:
            feedback.title = feedback_data.title
        if feedback_data.description is not None:
            feedback.description = feedback_data.description
        if feedback_data.feedback_type is not None:
            feedback.feedback_type = feedback_data.feedback_type
        if feedback_data.priority is not None and can_manage:
            feedback.priority = feedback_data.priority
        if feedback_data.status is not None and can_manage:
            feedback.status = feedback_data.status
        if feedback_data.module_name is not None and can_manage:
            feedback.module_name = feedback_data.module_name

        feedback.updated_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(feedback)

        # إرسال إشعار للمستخدم إذا تغيرت الحالة
        if old_status != feedback.status and feedback.user_id and config.FEEDBACK_SETTINGS["notify_user_on_status_change"]:
            self._notify_user_status_change(feedback, old_status, user_id)

        return feedback

    def delete_feedback(self, feedback_id: int, user_id: int) -> bool:
        """حذف التغذية الراجعة"""
        feedback = self.db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        if not feedback:
            return False

        # التحقق من الصلاحيات
        is_owner = feedback.user_id == user_id
        can_delete = has_permission(user_id, config.FeedbackPermissions.DELETE_FEEDBACK)

        if not (is_owner or can_delete):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف هذه التغذية الراجعة")

        # حذف التغذية الراجعة
        self.db.delete(feedback)
        self.db.commit()

        return True

    def add_comment(
        self,
        feedback_id: int,
        content: str,
        user_id: int
    ) -> Optional[models.FeedbackComment]:
        """إضافة تعليق على التغذية الراجعة"""
        feedback = self.db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        if not feedback:
            return None

        # التحقق من تمكين التعليقات
        if not config.FEEDBACK_SETTINGS["enable_comments"]:
            raise HTTPException(status_code=400, detail="التعليقات غير مفعلة")

        # إنشاء التعليق
        comment = models.FeedbackComment(
            content=content,
            feedback_id=feedback_id,
            user_id=user_id
        )

        # إضافة إلى قاعدة البيانات
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        # إرسال إشعارات
        if user_id and feedback.user_id and user_id != feedback.user_id:
            self._notify_user_new_comment(feedback, comment, user_id)

        return comment

    def get_comments(self, feedback_id: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """الحصول على تعليقات التغذية الراجعة"""
        comments = self.db.query(models.FeedbackComment).filter(
            models.FeedbackComment.feedback_id == feedback_id
        ).order_by(
            desc(models.FeedbackComment.created_at)
        ).offset(skip).limit(limit).all()

        # تحويل إلى قواميس
        results = []
        for comment in comments:
            result = {
                "id": comment.id,
                "content": comment.content,
                "feedback_id": comment.feedback_id,
                "user_id": comment.user_id,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at
            }

            # إضافة اسم المستخدم إذا كان متاحاً
            if comment.user_id:
                # هنا يمكن استدعاء خدمة المستخدمين للحصول على اسم المستخدم
                # لكن لتبسيط الأمور، سنضيف اسماً افتراضياً
                result["user_name"] = f"مستخدم {comment.user_id}"

            results.append(result)

        return results

    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        """حذف تعليق"""
        comment = self.db.query(models.FeedbackComment).filter(models.FeedbackComment.id == comment_id).first()
        if not comment:
            return False

        # التحقق من الصلاحيات
        is_owner = comment.user_id == user_id
        can_manage = has_permission(user_id, config.FeedbackPermissions.MANAGE_FEEDBACK)

        if not (is_owner or can_manage):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف هذا التعليق")

        # حذف التعليق
        self.db.delete(comment)
        self.db.commit()

        return True

    def add_vote(
        self,
        feedback_id: int,
        user_id: int,
        is_upvote: bool = True
    ) -> Optional[models.FeedbackVote]:
        """إضافة تصويت على التغذية الراجعة"""
        feedback = self.db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        if not feedback:
            return None

        # التحقق من تمكين التصويت
        if not config.FEEDBACK_SETTINGS["enable_voting"]:
            raise HTTPException(status_code=400, detail="التصويت غير مفعل")

        # التحقق من وجود تصويت سابق
        existing_vote = self.db.query(models.FeedbackVote).filter(
            models.FeedbackVote.feedback_id == feedback_id,
            models.FeedbackVote.user_id == user_id
        ).first()

        if existing_vote:
            # تحديث التصويت الموجود
            existing_vote.is_upvote = is_upvote
            existing_vote.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(existing_vote)
            return existing_vote
        else:
            # إنشاء تصويت جديد
            vote = models.FeedbackVote(
                feedback_id=feedback_id,
                user_id=user_id,
                is_upvote=is_upvote
            )

            # إضافة إلى قاعدة البيانات
            self.db.add(vote)
            self.db.commit()
            self.db.refresh(vote)

            return vote

    def remove_vote(self, feedback_id: int, user_id: int) -> bool:
        """إزالة تصويت"""
        vote = self.db.query(models.FeedbackVote).filter(
            models.FeedbackVote.feedback_id == feedback_id,
            models.FeedbackVote.user_id == user_id
        ).first()

        if not vote:
            return False

        # حذف التصويت
        self.db.delete(vote)
        self.db.commit()

        return True

    def get_vote_count(self, feedback_id: int) -> Dict[str, int]:
        """الحصول على عدد التصويتات"""
        upvotes = self.db.query(func.count(models.FeedbackVote.id)).filter(
            models.FeedbackVote.feedback_id == feedback_id,
            models.FeedbackVote.is_upvote
        ).scalar()

        downvotes = self.db.query(func.count(models.FeedbackVote.id)).filter(
            models.FeedbackVote.feedback_id == feedback_id,
            models.FeedbackVote.is_upvote.is_(False)
        ).scalar()

        return {
            "upvotes": upvotes,
            "downvotes": downvotes,
            "total": upvotes - downvotes
        }

    async def add_attachment(
        self,
        feedback_id: int,
        file: UploadFile,
        user_id: int
    ) -> Optional[models.FeedbackAttachment]:
        """إضافة مرفق للتغذية الراجعة"""
        feedback = self.db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        if not feedback:
            return None

        # التحقق من تمكين المرفقات
        if not config.FEEDBACK_SETTINGS["enable_attachments"]:
            raise HTTPException(status_code=400, detail="المرفقات غير مفعلة")

        # التحقق من الصلاحيات
        is_owner = feedback.user_id == user_id
        can_edit = has_permission(user_id, config.FeedbackPermissions.EDIT_FEEDBACK)
        can_manage = has_permission(user_id, config.FeedbackPermissions.MANAGE_FEEDBACK)

        if not (is_owner or can_edit or can_manage):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإضافة مرفقات لهذه التغذية الراجعة")

        # التحقق من عدد المرفقات
        attachment_count = self.db.query(func.count(models.FeedbackAttachment.id)).filter(
            models.FeedbackAttachment.feedback_id == feedback_id
        ).scalar()

        if attachment_count >= config.FEEDBACK_SETTINGS["max_attachments_per_feedback"]:
            raise HTTPException(status_code=400, detail="تم تجاوز الحد الأقصى لعدد المرفقات")

        # التحقق من نوع الملف
        if file.content_type not in config.FEEDBACK_SETTINGS["allowed_attachment_types"]:
            raise HTTPException(status_code=400, detail="نوع الملف غير مدعوم")

        # قراءة محتوى الملف
        contents = await file.read()

        # التحقق من حجم الملف
        file_size = len(contents)
        max_size = config.FEEDBACK_SETTINGS["max_attachment_size_mb"] * 1024 * 1024

        if file_size > max_size:
            raise HTTPException(status_code=400, detail="حجم الملف أكبر من الحد المسموح به")

        # حفظ الملف (هنا يمكن استخدام خدمة تخزين الملفات)
        # لتبسيط الأمور، سنفترض أن الملف تم حفظه ونستخدم مساراً افتراضياً
        file_path = f"/uploads/feedback/{feedback_id}/{file.filename}"

        # إنشاء المرفق
        attachment = models.FeedbackAttachment(
            file_name=file.filename,
            file_path=file_path,
            file_type=file.content_type,
            file_size=file_size,
            feedback_id=feedback_id
        )

        # إضافة إلى قاعدة البيانات
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)

        return attachment

    def delete_attachment(self, attachment_id: int, user_id: int) -> bool:
        """حذف مرفق"""
        attachment = self.db.query(models.FeedbackAttachment).filter(
            models.FeedbackAttachment.id == attachment_id
        ).first()

        if not attachment:
            return False

        # الحصول على التغذية الراجعة
        feedback = self.db.query(models.Feedback).filter(
            models.Feedback.id == attachment.feedback_id
        ).first()

        if not feedback:
            return False

        # التحقق من الصلاحيات
        is_owner = feedback.user_id == user_id
        can_edit = has_permission(user_id, config.FeedbackPermissions.EDIT_FEEDBACK)
        can_manage = has_permission(user_id, config.FeedbackPermissions.MANAGE_FEEDBACK)

        if not (is_owner or can_edit or can_manage):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف مرفقات هذه التغذية الراجعة")

        # حذف المرفق
        self.db.delete(attachment)
        self.db.commit()

        # هنا يمكن حذف الملف من نظام الملفات أو خدمة التخزين

        return True

    def create_tag(self, tag_data: schemas.TagCreate, user_id: int) -> models.FeedbackTag:
        """إنشاء وسم جديد"""
        # التحقق من الصلاحيات
        if not has_permission(user_id, config.FeedbackPermissions.MANAGE_FEEDBACK):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإنشاء وسوم")

        # التحقق من عدم وجود وسم بنفس الاسم
        existing_tag = self.db.query(models.FeedbackTag).filter(
            models.FeedbackTag.name == tag_data.name
        ).first()

        if existing_tag:
            raise HTTPException(status_code=400, detail="يوجد وسم بنفس الاسم بالفعل")

        # إنشاء الوسم
        tag = models.FeedbackTag(
            name=tag_data.name,
            description=tag_data.description,
            color=tag_data.color
        )

        # إضافة إلى قاعدة البيانات
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)

        return tag

    def get_all_tags(self) -> List[Dict[str, Any]]:
        """الحصول على جميع الوسوم"""
        tags = self.db.query(models.FeedbackTag).all()

        # تحويل إلى قواميس
        results = []
        for tag in tags:
            results.append({
                "id": tag.id,
                "name": tag.name,
                "description": tag.description,
                "color": tag.color,
                "created_at": tag.created_at
            })

        return results

    def add_tag_to_feedback(self, feedback_id: int, tag_id: int, user_id: int) -> bool:
        """إضافة وسم إلى تغذية راجعة"""
        # التحقق من الصلاحيات
        if not has_permission(user_id, config.FeedbackPermissions.MANAGE_FEEDBACK):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإضافة وسوم")

        # التحقق من وجود التغذية الراجعة
        feedback = self.db.query(models.Feedback).filter(
            models.Feedback.id == feedback_id
        ).first()

        if not feedback:
            return False

        # التحقق من وجود الوسم
        tag = self.db.query(models.FeedbackTag).filter(
            models.FeedbackTag.id == tag_id
        ).first()

        if not tag:
            return False

        # التحقق من عدم وجود ارتباط سابق
        existing_association = self.db.query(models.FeedbackTagAssociation).filter(
            models.FeedbackTagAssociation.feedback_id == feedback_id,
            models.FeedbackTagAssociation.tag_id == tag_id
        ).first()

        if existing_association:
            return True  # الارتباط موجود بالفعل

        # إنشاء الارتباط
        association = models.FeedbackTagAssociation(
            feedback_id=feedback_id,
            tag_id=tag_id
        )

        # إضافة إلى قاعدة البيانات
        self.db.add(association)
        self.db.commit()

        return True

    def remove_tag_from_feedback(self, feedback_id: int, tag_id: int, user_id: int) -> bool:
        """إزالة وسم من تغذية راجعة"""
        # التحقق من الصلاحيات
        if not has_permission(user_id, config.FeedbackPermissions.MANAGE_FEEDBACK):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإزالة وسوم")

        # البحث عن الارتباط
        association = self.db.query(models.FeedbackTagAssociation).filter(
            models.FeedbackTagAssociation.feedback_id == feedback_id,
            models.FeedbackTagAssociation.tag_id == tag_id
        ).first()

        if not association:
            return False

        # حذف الارتباط
        self.db.delete(association)
        self.db.commit()

        return True

    def get_feedback_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات التغذية الراجعة"""
        stats = {}

        # إحصائيات حسب النوع
        type_stats = self.db.query(
            models.Feedback.feedback_type,
            func.count(models.Feedback.id)
        ).group_by(models.Feedback.feedback_type).all()
        stats["by_type"] = {str(t[0].value): t[1] for t in type_stats}

        # إحصائيات حسب الحالة
        status_stats = self.db.query(
            models.Feedback.status,
            func.count(models.Feedback.id)
        ).group_by(models.Feedback.status).all()
        stats["by_status"] = {str(s[0].value): s[1] for s in status_stats}

        # إحصائيات حسب الأولوية
        priority_stats = self.db.query(
            models.Feedback.priority,
            func.count(models.Feedback.id)
        ).group_by(models.Feedback.priority).all()
        stats["by_priority"] = {str(p[0].value): p[1] for p in priority_stats}

        # إحصائيات حسب الوحدة
        module_stats = self.db.query(
            models.Feedback.module_name,
            func.count(models.Feedback.id)
        ).filter(models.Feedback.module_name.isnot(None)).group_by(models.Feedback.module_name).all()
        stats["by_module"] = {m[0]: m[1] for m in module_stats}

        # إحصائيات زمنية
        now = datetime.now(timezone.utc)
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)

        stats["time_periods"] = {
            "last_24h": self.db.query(func.count(models.Feedback.id)).filter(
                models.Feedback.created_at >= now - timedelta(days=1)
            ).scalar(),
            "last_week": self.db.query(func.count(models.Feedback.id)).filter(
                models.Feedback.created_at >= last_week
            ).scalar(),
            "last_month": self.db.query(func.count(models.Feedback.id)).filter(
                models.Feedback.created_at >= last_month
            ).scalar(),
            "total": self.db.query(func.count(models.Feedback.id)).scalar()
        }

        return stats

    def get_trending_feedback(self, limit: int = 10) -> List[Dict[str, Any]]:
        """الحصول على التغذية الراجعة الأكثر شعبية"""
        # الحصول على التغذية الراجعة مع عدد التصويتات الإيجابية
        subquery = self.db.query(
            models.FeedbackVote.feedback_id,
            func.count(models.FeedbackVote.id).label("vote_count")
        ).filter(models.FeedbackVote.is_upvote).group_by(
            models.FeedbackVote.feedback_id
        ).subquery()

        # دمج مع جدول التغذية الراجعة وترتيب حسب عدد التصويتات
        query = self.db.query(models.Feedback).join(
            subquery,
            models.Feedback.id == subquery.c.feedback_id
        ).order_by(desc(subquery.c.vote_count))

        # الحصول على النتائج
        feedbacks = query.limit(limit).all()

        # تحويل إلى قواميس
        results = []
        for feedback in feedbacks:
            results.append(self._feedback_to_dict(feedback))

        return results

    def cleanup_old_feedback(self) -> Dict[str, int]:
        """تنظيف التغذية الراجعة القديمة"""
        now = datetime.now(timezone.utc)
        completed_cutoff = now - timedelta(days=config.FEEDBACK_SETTINGS["days_to_keep_completed_feedback"])
        rejected_cutoff = now - timedelta(days=config.FEEDBACK_SETTINGS["days_to_keep_rejected_feedback"])

        # حذف التغذية الراجعة المكتملة القديمة
        completed_deleted = self.db.query(models.Feedback).filter(
            models.Feedback.status == config.FeedbackStatus.COMPLETED,
            models.Feedback.updated_at < completed_cutoff
        ).delete(synchronize_session=False)

        # حذف التغذية الراجعة المرفوضة القديمة
        rejected_deleted = self.db.query(models.Feedback).filter(
            models.Feedback.status == config.FeedbackStatus.REJECTED,
            models.Feedback.updated_at < rejected_cutoff
        ).delete(synchronize_session=False)

        self.db.commit()

        return {
            "completed_deleted": completed_deleted,
            "rejected_deleted": rejected_deleted,
            "total_deleted": completed_deleted + rejected_deleted
        }

    def _feedback_to_dict(self, feedback: models.Feedback, include_details: bool = False) -> Dict[str, Any]:
        """تحويل كائن التغذية الراجعة إلى قاموس"""
        result = {
            "id": feedback.id,
            "title": feedback.title,
            "description": feedback.description,
            "feedback_type": str(feedback.feedback_type.value),
            "priority": str(feedback.priority.value),
            "status": str(feedback.status.value),
            "user_id": feedback.user_id,
            "module_name": feedback.module_name,
            "created_at": feedback.created_at,
            "updated_at": feedback.updated_at
        }

        # إضافة عدد التصويتات
        upvotes = self.db.query(func.count(models.FeedbackVote.id)).filter(
            models.FeedbackVote.feedback_id == feedback.id,
            models.FeedbackVote.is_upvote
        ).scalar()

        downvotes = self.db.query(func.count(models.FeedbackVote.id)).filter(
            models.FeedbackVote.feedback_id == feedback.id,
            models.FeedbackVote.is_upvote.is_(False)
        ).scalar()

        result["vote_count"] = upvotes - downvotes

        # إضافة التفاصيل إذا كان مطلوباً
        if include_details:
            # إضافة التعليقات
            comments = self.db.query(models.FeedbackComment).filter(
                models.FeedbackComment.feedback_id == feedback.id
            ).order_by(
                desc(models.FeedbackComment.created_at)
            ).all()

            result["comments"] = []
            for comment in comments:
                comment_dict = {
                    "id": comment.id,
                    "content": comment.content,
                    "user_id": comment.user_id,
                    "created_at": comment.created_at,
                    "updated_at": comment.updated_at
                }

                # إضافة اسم المستخدم إذا كان متاحاً
                if comment.user_id:
                    # هنا يمكن استدعاء خدمة المستخدمين للحصول على اسم المستخدم
                    # لكن لتبسيط الأمور، سنضيف اسماً افتراضياً
                    comment_dict["user_name"] = f"مستخدم {comment.user_id}"

                result["comments"].append(comment_dict)

            # إضافة المرفقات
            attachments = self.db.query(models.FeedbackAttachment).filter(
                models.FeedbackAttachment.feedback_id == feedback.id
            ).all()

            result["attachments"] = []
            for attachment in attachments:
                result["attachments"].append({
                    "id": attachment.id,
                    "file_name": attachment.file_name,
                    "file_path": attachment.file_path,
                    "file_type": attachment.file_type,
                    "file_size": attachment.file_size,
                    "created_at": attachment.created_at
                })

            # إضافة الوسوم
            tag_associations = self.db.query(models.FeedbackTagAssociation).filter(
                models.FeedbackTagAssociation.feedback_id == feedback.id
            ).all()

            tag_ids = [assoc.tag_id for assoc in tag_associations]

            if tag_ids:
                tags = self.db.query(models.FeedbackTag).filter(
                    models.FeedbackTag.id.in_(tag_ids)
                ).all()

                result["tags"] = []
                for tag in tags:
                    result["tags"].append({
                        "id": tag.id,
                        "name": tag.name,
                        "description": tag.description,
                        "color": tag.color
                    })
            else:
                result["tags"] = []

        return result

    def _notify_admins_new_feedback(self, feedback: models.Feedback):
        """إرسال إشعار للمسؤولين عن تغذية راجعة جديدة"""
        try:
            notification_service.send_notification_to_role(
                role_name="admin",
                title="تغذية راجعة جديدة",
                message=f"تم استلام تغذية راجعة جديدة: {feedback.title}",
                data={
                    "feedback_id": feedback.id,
                    "type": str(feedback.feedback_type.value),
                    "priority": str(feedback.priority.value)
                },
                notification_type="feedback"
            )
        except Exception as e:
            logger.error("خطأ في إرسال إشعار للمسؤولين: %s", str(e))

    def _notify_user_status_change(self, feedback: models.Feedback, old_status: config.FeedbackStatus, admin_id: int):
        """إرسال إشعار للمستخدم عن تغيير حالة التغذية الراجعة"""
        try:
            notification_service.send_notification_to_user(
                user_id=feedback.user_id,
                title="تحديث حالة التغذية الراجعة",
                message=f"تم تحديث حالة تغذيتك الراجعة '{feedback.title}' من {old_status.value} إلى {feedback.status.value}",
                data={
                    "feedback_id": feedback.id,
                    "old_status": str(old_status.value),
                    "new_status": str(feedback.status.value)
                },
                notification_type="feedback_update"
            )
        except Exception as e:
            logger.error("خطأ في إرسال إشعار للمستخدم: %s", str(e))

    def _notify_user_new_comment(self, feedback: models.Feedback, comment: models.FeedbackComment, commenter_id: int):
        """إرسال إشعار للمستخدم عن تعليق جديد على التغذية الراجعة"""
        try:
            notification_service.send_notification_to_user(
                user_id=feedback.user_id,
                title="تعليق جديد على تغذيتك الراجعة",
                message=f"تم إضافة تعليق جديد على تغذيتك الراجعة '{feedback.title}'",
                data={
                    "feedback_id": feedback.id,
                    "comment_id": comment.id,
                    "commenter_id": commenter_id
                },
                notification_type="feedback_comment"
            )
        except Exception as e:
            logger.error("خطأ في إرسال إشعار للمستخدم عن تعليق جديد: %s", str(e))


# إنشاء مثيل عام للخدمة
feedback_service = FeedbackService()
