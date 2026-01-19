# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/feedback/schemas.py
"""
مخططات البيانات لوحدة التغذية الراجعة
توفر هذه الوحدة مخططات Pydantic للتحقق من صحة البيانات وتحويلها في وحدة التغذية الراجعة
"""

import re
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator

from .config import FEEDBACK_SETTINGS, FeedbackPriority, FeedbackStatus, FeedbackType


class FeedbackBase(BaseModel):
    """النموذج الأساسي للتغذية الراجعة"""
    title: str = Field(..., min_length=3,
                       max_length=FEEDBACK_SETTINGS["max_feedback_title_length"])
    description: str = Field(...,
                             min_length=10,
                             max_length=FEEDBACK_SETTINGS["max_feedback_description_length"])
    feedback_type: FeedbackType
    priority: Optional[FeedbackPriority] = FEEDBACK_SETTINGS["default_feedback_priority"]
    module_name: Optional[str] = None

    @validator('title')
    def title_must_be_valid(cls, v):
        if not re.match(r'^[\u0600-\u06FFa-zA-Z0-9\s\-_.,!?()]+$', v):
            raise ValueError(
                'العنوان يجب أن يحتوي على أحرف وأرقام وعلامات ترقيم فقط')
        return v


class FeedbackCreate(FeedbackBase):
    """نموذج إنشاء تغذية راجعة جديدة"""


class FeedbackUpdate(BaseModel):
    """نموذج تحديث التغذية الراجعة"""
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=FEEDBACK_SETTINGS["max_feedback_title_length"])
    description: Optional[str] = Field(
        None,
        min_length=10,
        max_length=FEEDBACK_SETTINGS["max_feedback_description_length"])
    feedback_type: Optional[FeedbackType] = None
    priority: Optional[FeedbackPriority] = None
    status: Optional[FeedbackStatus] = None
    module_name: Optional[str] = None

    @validator('title')
    def title_must_be_valid(cls, v):
        if v is not None and not re.match(
                r'^[\u0600-\u06FFa-zA-Z0-9\s\-_.,!?()]+$', v):
            raise ValueError(
                'العنوان يجب أن يحتوي على أحرف وأرقام وعلامات ترقيم فقط')
        return v


class FeedbackInDB(FeedbackBase):
    """نموذج التغذية الراجعة في قاعدة البيانات"""
    id: int
    status: FeedbackStatus
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FeedbackWithDetails(FeedbackInDB):
    """نموذج التغذية الراجعة مع التفاصيل"""
    comments: List['CommentInDB'] = []
    attachments: List['AttachmentInDB'] = []
    vote_count: int = 0
    user_vote: Optional[bool] = None
    tags: List['TagInDB'] = []

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    """النموذج الأساسي للتعليق"""
    content: str = Field(..., min_length=1,
                         max_length=FEEDBACK_SETTINGS["max_comment_length"])


class CommentCreate(CommentBase):
    """نموذج إنشاء تعليق جديد"""
    feedback_id: int


class CommentInDB(CommentBase):
    """نموذج التعليق في قاعدة البيانات"""
    id: int
    feedback_id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    user_name: Optional[str] = None  # اسم المستخدم (يتم ملؤه من الخدمة)

    class Config:
        orm_mode = True


class AttachmentBase(BaseModel):
    """النموذج الأساسي للمرفق"""
    file_name: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class AttachmentCreate(AttachmentBase):
    """نموذج إنشاء مرفق جديد"""
    feedback_id: int
    file_path: str


class AttachmentInDB(AttachmentBase):
    """نموذج المرفق في قاعدة البيانات"""
    id: int
    feedback_id: int
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    """نموذج إنشاء تصويت جديد"""
    feedback_id: int
    is_upvote: bool = True


class VoteInDB(VoteCreate):
    """نموذج التصويت في قاعدة البيانات"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    """النموذج الأساسي للوسم"""
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    color: Optional[str] = Field(
        None, regex=r'^#[0-9A-Fa-f]{6}$')  # لون بصيغة HEX (#RRGGBB)


class TagCreate(TagBase):
    """نموذج إنشاء وسم جديد"""


class TagInDB(TagBase):
    """نموذج الوسم في قاعدة البيانات"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class FeedbackStatistics(BaseModel):
    """نموذج إحصائيات التغذية الراجعة"""
    by_type: Dict[str, int]
    by_status: Dict[str, int]
    by_priority: Dict[str, int]
    by_module: Dict[str, int]
    time_periods: Dict[str, int]


class FeedbackFilter(BaseModel):
    """نموذج تصفية التغذية الراجعة"""
    status: Optional[FeedbackStatus] = None
    feedback_type: Optional[FeedbackType] = None
    priority: Optional[FeedbackPriority] = None
    module_name: Optional[str] = None
    user_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search_query: Optional[str] = None
    tags: Optional[List[int]] = None
    skip: int = 0
    limit: int = 100
    sort_by: str = "created_at"
    sort_desc: bool = True


# تحديث الإشارات الدائرية
FeedbackWithDetails.update_forward_refs()
