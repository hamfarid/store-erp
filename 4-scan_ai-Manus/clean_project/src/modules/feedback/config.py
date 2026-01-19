# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/feedback/config.py
"""
ملف إعدادات وحدة التغذية الراجعة
يحتوي على الإعدادات والثوابت الخاصة بوحدة التغذية الراجعة
"""

from enum import Enum

# أنواع التغذية الراجعة


class FeedbackType(str, Enum):
    BUG = "bug"  # تقرير خطأ
    FEATURE_REQUEST = "feature_request"  # طلب ميزة جديدة
    IMPROVEMENT = "improvement"  # اقتراح تحسين
    QUESTION = "question"  # سؤال
    OTHER = "other"  # أخرى

# أولويات التغذية الراجعة


class FeedbackPriority(str, Enum):
    LOW = "low"  # منخفضة
    MEDIUM = "medium"  # متوسطة
    HIGH = "high"  # عالية
    CRITICAL = "critical"  # حرجة

# حالات التغذية الراجعة


class FeedbackStatus(str, Enum):
    NEW = "new"  # جديدة
    UNDER_REVIEW = "under_review"  # قيد المراجعة
    PLANNED = "planned"  # مخطط لها
    IN_PROGRESS = "in_progress"  # قيد التنفيذ
    COMPLETED = "completed"  # مكتملة
    REJECTED = "rejected"  # مرفوضة

# صلاحيات التغذية الراجعة


class FeedbackPermissions:
    VIEW_FEEDBACK = "view_feedback"  # عرض التغذية الراجعة
    VIEW_FEEDBACK_DETAILS = "view_feedback_details"  # عرض تفاصيل التغذية الراجعة
    ADD_FEEDBACK = "add_feedback"  # إضافة تغذية راجعة
    EDIT_FEEDBACK = "edit_feedback"  # تعديل التغذية الراجعة
    DELETE_FEEDBACK = "delete_feedback"  # حذف التغذية الراجعة
    MANAGE_FEEDBACK = "manage_feedback"  # إدارة التغذية الراجعة (تغيير الحالة، الأولوية، إلخ)
    APPROVE_FEEDBACK = "approve_feedback"  # الموافقة على التغذية الراجعة


# إعدادات عامة
FEEDBACK_SETTINGS = {
    "max_attachments_per_feedback": 5,  # الحد الأقصى لعدد المرفقات لكل تغذية راجعة
    "max_attachment_size_mb": 10,  # الحد الأقصى لحجم المرفق بالميجابايت
    "allowed_attachment_types": ["image/jpeg", "image/png", "image/gif", "application/pdf", "text/plain"],  # أنواع الملفات المسموح بها
    "max_feedback_title_length": 100,  # الحد الأقصى لطول عنوان التغذية الراجعة
    "max_feedback_description_length": 5000,  # الحد الأقصى لطول وصف التغذية الراجعة
    "max_comment_length": 1000,  # الحد الأقصى لطول التعليق
    "default_feedback_priority": FeedbackPriority.MEDIUM,  # أولوية التغذية الراجعة الافتراضية
    "default_feedback_status": FeedbackStatus.NEW,  # حالة التغذية الراجعة الافتراضية
    "notify_admins_on_new_feedback": True,  # إشعار المسؤولين عند إضافة تغذية راجعة جديدة
    "notify_user_on_status_change": True,  # إشعار المستخدم عند تغيير حالة التغذية الراجعة
    "enable_voting": True,  # تمكين التصويت على التغذية الراجعة
    "enable_comments": True,  # تمكين التعليقات على التغذية الراجعة
    "enable_attachments": True,  # تمكين المرفقات في التغذية الراجعة
    "days_to_keep_completed_feedback": 365,  # عدد الأيام للاحتفاظ بالتغذية الراجعة المكتملة
    "days_to_keep_rejected_feedback": 180,  # عدد الأيام للاحتفاظ بالتغذية الراجعة المرفوضة
}
