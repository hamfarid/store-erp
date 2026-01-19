"""
/home/ubuntu/implemented_files/v3/src/modules/user_management/service.py

خدمة إدارة المستخدمين

يوفر هذا الملف خدمة إدارة المستخدمين لنظام Gaara ERP، بما في ذلك:
- إنشاء وتعديل وحذف المستخدمين
- إدارة معلومات الملف الشخصي
- إدارة الأدوار والصلاحيات
- إدارة تفضيلات المستخدم
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta, timezone
import uuid
import secrets
import hashlib
import base64
import re
import logging
from fastapi import HTTPException, status, Depends
from pydantic import EmailStr, constr
import jwt
from passlib.context import CryptContext

from .models import (
    User, UserProfile, UserPreference, Role, UserRole, Organization, Gender,
    UserSession
)
from .schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserDetailResponse,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserPreferenceCreate,
    UserPreferenceUpdate,
    UserPreferenceResponse,
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationDetailResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    AssignRoleRequest,
    AssignRoleResponse,
    UserSearchRequest,
    UserSearchResponse,
    SessionCreate,
    SessionResponse
)
from .config import default_config
from ..permissions.service import PermissionService

# إعداد التسجيل
logger = logging.getLogger(__name__)

# ثوابت الرسائل
USER_NOT_FOUND_MESSAGE = "المستخدم غير موجود"
PASSWORD_COMPLEXITY_ERROR = "كلمة المرور يجب أن تحتوي على 8 أحرف على الأقل، وتتضمن حرف كبير وحرف صغير ورقم ورمز خاص"
SESSION_EXPIRED_MESSAGE = "انتهت صلاحية الجلسة"
INVALID_CREDENTIALS_MESSAGE = "بيانات الدخول غير صحيحة"
ACCOUNT_LOCKED_MESSAGE = "تم قفل الحساب بسبب محاولات تسجيل دخول فاشلة متكررة"

# إعداد تشفير كلمات المرور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# أنماط التحقق من كلمة المرور
PASSWORD_PATTERNS = {
    "length": r".{8,}",
    "uppercase": r"[A-Z]",
    "lowercase": r"[a-z]",
    "digit": r"\d",
    "special": r"[!@#$%^&*(),.?\":{}|<>]"
}

class UserService:
    """خدمة إدارة المستخدمين"""

    def __init__(self, db: Session):
        """
        تهيئة خدمة إدارة المستخدمين

        المعلمات:
            db (Session): جلسة قاعدة البيانات
        """
        self.db = db
        self.config = default_config

    def validate_password_complexity(self, password: str) -> bool:
        """
        التحقق من تعقيد كلمة المرور

        المعلمات:
            password (str): كلمة المرور للتحقق

        العوائد:
            bool: True إذا كانت كلمة المرور تفي بالمتطلبات، وإلا False
        """
        return all(
            re.search(pattern, password)
            for pattern in PASSWORD_PATTERNS.values()
        )

    def create_user(
            self,
            user_data: UserCreate,
            created_by: Optional[str] = None) -> User:
        """
        إنشاء مستخدم جديد

        المعلمات:
            user_data (UserCreate): بيانات المستخدم
            created_by (Optional[str]): معرف المستخدم الذي أنشأ المستخدم

        العوائد:
            User: المستخدم المنشأ

        يرفع:
            HTTPException: إذا كان اسم المستخدم أو البريد الإلكتروني موجوداً بالفعل
        """
        # التحقق من تعقيد كلمة المرور
        if not self.validate_password_complexity(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=PASSWORD_COMPLEXITY_ERROR
            )

        # التحقق من عدم وجود مستخدم بنفس اسم المستخدم
        existing_user = self.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="اسم المستخدم موجود بالفعل"
            )

        # التحقق من عدم وجود مستخدم بنفس البريد الإلكتروني
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="البريد الإلكتروني موجود بالفعل"
            )

        # تشفير كلمة المرور
        password_hash = pwd_context.hash(user_data.password)

        # إنشاء كائن المستخدم
        user = User(
            id=str(uuid.uuid4()),
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
            is_active=user_data.is_active,
            is_email_verified=user_data.is_email_verified,
            is_admin=user_data.is_admin,
            organization_id=user_data.organization_id,
            created_by=created_by,
            password_changed_at=datetime.now(timezone.utc),
            metadata=user_data.metadata,
            failed_login_attempts=0,
            last_failed_login=None,
            account_locked_until=None
        )

        # حفظ المستخدم في قاعدة البيانات
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # إنشاء الملف الشخصي والتفضيلات
        if self.config.user_config.auto_create_profile:
            self.create_user_profile(
                UserProfileCreate(
                    user_id=user.id), created_by)
            self.create_user_preference(
                UserPreferenceCreate(
                    user_id=user.id), created_by)

        # تعيين الدور الافتراضي
        default_role = self.get_role_by_name(
            self.config.user_config.default_role)
        if default_role:
            self.assign_role_to_user(user.id, default_role.id, created_by)

        return user

    def create_session(
            self,
            user_id: str,
            session_data: SessionCreate) -> UserSession:
        """
        إنشاء جلسة جديدة للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            session_data (SessionCreate): بيانات الجلسة

        العوائد:
            UserSession: الجلسة المنشأة

        يرفع:
            HTTPException: إذا كان المستخدم غير موجود أو غير نشط
        """
        user = self.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND_MESSAGE
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="الحساب غير نشط"
            )

        # إنشاء رمز JWT
        token_payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=self.config.session_config.expire_minutes),
            "jti": str(uuid.uuid4())
        }
        token = jwt.encode(
            token_payload,
            self.config.session_config.secret_key,
            algorithm=self.config.session_config.algorithm
        )

        # إنشاء كائن الجلسة
        session = UserSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            token=token,
            device_info=session_data.device_info,
            ip_address=session_data.ip_address,
            expires_at=datetime.utcnow() + timedelta(minutes=self.config.session_config.expire_minutes),
            is_active=True
        )

        # حفظ الجلسة في قاعدة البيانات
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def validate_session(self, token: str) -> Optional[UserSession]:
        """
        التحقق من صلاحية الجلسة

        المعلمات:
            token (str): رمز الجلسة

        العوائد:
            Optional[UserSession]: الجلسة إذا كانت صالحة، وإلا None
        """
        try:
            # فك تشفير الرمز
            payload = jwt.decode(
                token,
                self.config.session_config.secret_key,
                algorithms=[self.config.session_config.algorithm]
            )

            # البحث عن الجلسة في قاعدة البيانات
            session = self.db.query(UserSession).filter(
                UserSession.token == token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.utcnow()
            ).first()

            return session

        except jwt.InvalidTokenError:
            return None

    def invalidate_session(self, token: str) -> bool:
        """
        إبطال صلاحية الجلسة

        المعلمات:
            token (str): رمز الجلسة

        العوائد:
            bool: True إذا تم إبطال الجلسة بنجاح، وإلا False
        """
        session = self.db.query(UserSession).filter(
            UserSession.token == token,
            UserSession.is_active == True
        ).first()

        if session:
            session.is_active = False
            session.invalidated_at = datetime.utcnow()
            self.db.commit()
            return True

        return False

    def invalidate_all_user_sessions(self, user_id: str) -> bool:
        """
        إبطال جميع جلسات المستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            bool: True إذا تم إبطال الجلسات بنجاح، وإلا False
        """
        sessions = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).all()

        if sessions:
            for session in sessions:
                session.is_active = False
                session.invalidated_at = datetime.utcnow()
            self.db.commit()
            return True

        return False

    def get_active_sessions(self, user_id: str) -> List[UserSession]:
        """
        الحصول على الجلسات النشطة للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            List[UserSession]: قائمة الجلسات النشطة
        """
        return self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        ).all()

    # ==================== إدارة المستخدمين ====================

    def get_user(self, user_id: str) -> Optional[User]:
        """
        استرجاع مستخدم بواسطة المعرف

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[User]: المستخدم إذا وجد، وإلا None
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        استرجاع مستخدم بواسطة اسم المستخدم

        المعلمات:
            username (str): اسم المستخدم

        العوائد:
            Optional[User]: المستخدم إذا وجد، وإلا None
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        استرجاع مستخدم بواسطة البريد الإلكتروني

        المعلمات:
            email (str): البريد الإلكتروني

        العوائد:
            Optional[User]: المستخدم إذا وجد، وإلا None
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        استرجاع قائمة المستخدمين

        المعلمات:
            skip (int): عدد المستخدمين للتخطي
            limit (int): الحد الأقصى لعدد المستخدمين

        العوائد:
            List[User]: قائمة المستخدمين
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def search_users(
            self, search_data: UserSearchRequest) -> Tuple[List[User], int]:
        """
        البحث عن المستخدمين

        المعلمات:
            search_data (UserSearchRequest): بيانات البحث

        العوائد:
            Tuple[List[User], int]: قائمة المستخدمين وإجمالي عدد النتائج
        """
        # بناء استعلام البحث
        query = self.db.query(User)

        # تطبيق معايير البحث
        if search_data.query:
            search_term = f"%{search_data.query}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )

        if search_data.is_active is not None:
            query = query.filter(User.is_active == search_data.is_active)

        if search_data.is_admin is not None:
            query = query.filter(User.is_admin == search_data.is_admin)

        if search_data.organization_id:
            query = query.filter(
                User.organization_id == search_data.organization_id)

        if search_data.role_id:
            query = query.join(
                User.roles).filter(
                Role.id == search_data.role_id)

        # الحصول على إجمالي عدد النتائج
        total = query.count()

        # تطبيق الترتيب والتقسيم
        query = query.order_by(User.created_at.desc())
        query = query.offset(search_data.offset).limit(search_data.limit)

        # الحصول على النتائج
        users = query.all()

        return users, total

    def update_user(self, user_id: str, user_data: UserUpdate,
                    updated_by: Optional[str] = None) -> Optional[User]:
        """
        تحديث مستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            user_data (UserUpdate): بيانات التحديث
            updated_by (Optional[str]): معرف المستخدم الذي قام بالتحديث

        العوائد:
            Optional[User]: المستخدم المحدث إذا وجد، وإلا None

        يرفع:
            HTTPException: إذا كان البريد الإلكتروني موجوداً بالفعل
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return None

        # التحقق من عدم وجود مستخدم آخر بنفس البريد الإلكتروني
        if user_data.email and user_data.email != user.email:
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="البريد الإلكتروني موجود بالفعل"
                )

        # تحديث المستخدم
        if user_data.email is not None:
            user.email = user_data.email

        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        if user_data.is_admin is not None:
            user.is_admin = user_data.is_admin

        if user_data.is_email_verified is not None:
            user.is_email_verified = user_data.is_email_verified

        if user_data.organization_id is not None:
            user.organization_id = user_data.organization_id

        if user_data.metadata is not None:
            user.metadata = user_data.metadata

        # تحديث معلومات التحديث
        user.updated_at = datetime.now(timezone.utc)
        user.updated_by = updated_by

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(user)

        return user

    def update_user_email_verified(
            self,
            user_id: str,
            is_verified: bool) -> Optional[User]:
        """
        تحديث حالة التحقق من البريد الإلكتروني

        المعلمات:
            user_id (str): معرف المستخدم
            is_verified (bool): حالة التحقق

        العوائد:
            Optional[User]: المستخدم المحدث إذا وجد، وإلا None
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return None

        # تحديث حالة التحقق
        user.is_email_verified = is_verified

        # تحديث وقت التحديث
        user.updated_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(user)

        return user

    def update_user_last_login(self, user_id: str) -> Optional[User]:
        """
        تحديث وقت آخر تسجيل دخول

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[User]: المستخدم المحدث إذا وجد، وإلا None
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return None

        # تحديث وقت آخر تسجيل دخول
        user.last_login = datetime.now(timezone.utc)

        # إعادة تعيين عدد محاولات تسجيل الدخول الفاشلة
        user.failed_login_attempts = 0
        user.locked_until = None

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(user)

        return user

    def increment_failed_login_attempts(self, user_id: str) -> Optional[User]:
        """
        زيادة عدد محاولات تسجيل الدخول الفاشلة

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[User]: المستخدم المحدث إذا وجد، وإلا None
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return None

        # زيادة عدد محاولات تسجيل الدخول الفاشلة
        user.failed_login_attempts += 1

        # التحقق مما إذا كان يجب قفل الحساب
        if user.failed_login_attempts >= self.config.password_policy.lockout_threshold:
            user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=self.config.password_policy.lockout_duration_minutes)

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(self, user_id: str) -> bool:
        """
        حذف مستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            bool: True إذا تم الحذف بنجاح، وإلا False
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return False

        # حذف المستخدم
        self.db.delete(user)
        self.db.commit()

        return True

    def change_password(
            self,
            user_id: str,
            password_data: ChangePasswordRequest) -> bool:
        """
        تغيير كلمة المرور

        المعلمات:
            user_id (str): معرف المستخدم
            password_data (ChangePasswordRequest): بيانات تغيير كلمة المرور

        العوائد:
            bool: True إذا تم التغيير بنجاح، وإلا False

        يرفع:
            HTTPException: إذا كانت كلمة المرور الحالية غير صحيحة أو كلمة المرور الجديدة موجودة في سجل كلمات المرور
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return False

        # التحقق من كلمة المرور الحالية
        if not self.verify_password(
                password_data.current_password,
                user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="كلمة المرور الحالية غير صحيحة"
            )

        # التحقق من عدم وجود كلمة المرور الجديدة في سجل كلمات المرور
        if user.password_history:
            for old_password_hash in user.password_history:
                if self.verify_password(
                        password_data.new_password,
                        old_password_hash):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="لا يمكن استخدام كلمة مرور سبق استخدامها"
                    )

        # تشفير كلمة المرور الجديدة
        new_password_hash = self.hash_password(password_data.new_password)

        # تحديث سجل كلمات المرور
        if not user.password_history:
            user.password_history = []

        user.password_history.append(user.password_hash)

        # الاحتفاظ بعدد محدد من كلمات المرور في السجل
        if len(
                user.password_history) > self.config.password_policy.password_history_size:
            user.password_history = user.password_history[-self.config.password_policy.password_history_size:]

        # تحديث كلمة المرور
        user.password_hash = new_password_hash
        user.password_changed_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()

        return True

    def update_password(self, user_id: str, new_password: str) -> bool:
        """
        تحديث كلمة المرور

        المعلمات:
            user_id (str): معرف المستخدم
            new_password (str): كلمة المرور الجديدة

        العوائد:
            bool: True إذا تم التحديث بنجاح، وإلا False
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return False

        # تشفير كلمة المرور الجديدة
        new_password_hash = self.hash_password(new_password)

        # تحديث سجل كلمات المرور
        if not user.password_history:
            user.password_history = []

        user.password_history.append(user.password_hash)

        # الاحتفاظ بعدد محدد من كلمات المرور في السجل
        if len(
                user.password_history) > self.config.password_policy.password_history_size:
            user.password_history = user.password_history[-self.config.password_policy.password_history_size:]

        # تحديث كلمة المرور
        user.password_hash = new_password_hash
        user.password_changed_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()

        return True

    def hash_password(self, password: str) -> str:
        """
        تشفير كلمة المرور

        المعلمات:
            password (str): كلمة المرور

        العوائد:
            str: كلمة المرور المشفرة
        """
        # إنشاء ملح عشوائي
        salt = secrets.token_bytes(32)

        # تشفير كلمة المرور مع الملح
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        # تحويل الهاش إلى سلسلة
        password_hash_str = base64.b64encode(password_hash).decode('utf-8')

        # إرجاع الملح والهاش مفصولين بنقطتين
        return f"{salt}:{password_hash_str}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        التحقق من كلمة المرور

        المعلمات:
            password (str): كلمة المرور
            password_hash (str): كلمة المرور المشفرة

        العوائد:
            bool: True إذا كانت كلمة المرور صحيحة، وإلا False
        """
        # فصل الملح والهاش
        salt, stored_hash = password_hash.split(':')

        # تشفير كلمة المرور المدخلة مع الملح المخزن
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )

        # تحويل الهاش إلى سلسلة
        password_hash_str = base64.b64encode(password_hash).decode('utf-8')

        # مقارنة الهاش المحسوب مع الهاش المخزن
        return password_hash_str == stored_hash

    # ==================== إدارة الملف الشخصي ====================

    def create_user_profile(
            self,
            profile_data: UserProfileCreate,
            created_by: Optional[str] = None) -> UserProfile:
        """
        إنشاء ملف شخصي للمستخدم

        المعلمات:
            profile_data (UserProfileCreate): بيانات الملف الشخصي
            created_by (Optional[str]): معرف المستخدم الذي أنشأ الملف الشخصي

        العوائد:
            UserProfile: الملف الشخصي المنشأ

        يرفع:
            HTTPException: إذا كان المستخدم غير موجود أو كان لديه ملف شخصي بالفعل
        """
        # التحقق من وجود المستخدم
        user = self.get_user(profile_data.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND_MESSAGE
            )

        # التحقق من عدم وجود ملف شخصي للمستخدم
        existing_profile = self.get_user_profile(profile_data.user_id)

        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="المستخدم لديه ملف شخصي بالفعل"
            )

        # إنشاء كائن الملف الشخصي
        profile = UserProfile(
            id=str(uuid.uuid4()),
            user_id=profile_data.user_id,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            phone=profile_data.phone,
            address=profile_data.address,
            city=profile_data.city,
            country=profile_data.country,
            postal_code=profile_data.postal_code,
            bio=profile_data.bio,
            avatar=profile_data.avatar,
            birth_date=profile_data.birth_date,
            gender=profile_data.gender,
            created_by=created_by,
            metadata=profile_data.metadata
        )

        # حفظ الملف الشخصي في قاعدة البيانات
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        استرجاع الملف الشخصي للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[UserProfile]: الملف الشخصي إذا وجد، وإلا None
        """
        return self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id).first()

    def update_user_profile(
            self,
            user_id: str,
            profile_data: UserProfileUpdate,
            updated_by: Optional[str] = None) -> Optional[UserProfile]:
        """
        تحديث الملف الشخصي للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            profile_data (UserProfileUpdate): بيانات التحديث
            updated_by (Optional[str]): معرف المستخدم الذي قام بالتحديث

        العوائد:
            Optional[UserProfile]: الملف الشخصي المحدث إذا وجد، وإلا None
        """
        # البحث عن الملف الشخصي في قاعدة البيانات
        profile = self.get_user_profile(user_id)

        if not profile:
            return None

        # تحديث الملف الشخصي
        if profile_data.first_name is not None:
            profile.first_name = profile_data.first_name

        if profile_data.last_name is not None:
            profile.last_name = profile_data.last_name

        if profile_data.phone is not None:
            profile.phone = profile_data.phone

        if profile_data.address is not None:
            profile.address = profile_data.address

        if profile_data.city is not None:
            profile.city = profile_data.city

        if profile_data.country is not None:
            profile.country = profile_data.country

        if profile_data.postal_code is not None:
            profile.postal_code = profile_data.postal_code

        if profile_data.bio is not None:
            profile.bio = profile_data.bio

        if profile_data.avatar is not None:
            profile.avatar = profile_data.avatar

        if profile_data.birth_date is not None:
            profile.birth_date = profile_data.birth_date

        if profile_data.gender is not None:
            profile.gender = profile_data.gender

        if profile_data.metadata is not None:
            profile.metadata = profile_data.metadata

        # تحديث معلومات التحديث
        profile.updated_at = datetime.now(timezone.utc)
        profile.updated_by = updated_by

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(profile)

        return profile

    # ==================== إدارة التفضيلات ====================

    def create_user_preference(
            self,
            preference_data: UserPreferenceCreate,
            created_by: Optional[str] = None) -> UserPreference:
        """
        إنشاء تفضيلات للمستخدم

        المعلمات:
            preference_data (UserPreferenceCreate): بيانات التفضيلات
            created_by (Optional[str]): معرف المستخدم الذي أنشأ التفضيلات

        العوائد:
            UserPreference: التفضيلات المنشأة

        يرفع:
            HTTPException: إذا كان المستخدم غير موجود أو كان لديه تفضيلات بالفعل
        """
        # التحقق من وجود المستخدم
        user = self.get_user(preference_data.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND_MESSAGE
            )

        # التحقق من عدم وجود تفضيلات للمستخدم
        existing_preference = self.get_user_preference(preference_data.user_id)

        if existing_preference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="المستخدم لديه تفضيلات بالفعل"
            )

        # إنشاء كائن التفضيلات
        preference = UserPreference(
            id=str(
                uuid.uuid4()),
            user_id=preference_data.user_id,
            language=preference_data.language or self.config.user_config.default_language,
            timezone=preference_data.timezone or self.config.user_config.default_timezone,
            date_format=preference_data.date_format or self.config.user_config.default_date_format,
            time_format=preference_data.time_format or self.config.user_config.default_time_format,
            theme=preference_data.theme or self.config.user_config.default_theme,
            notifications_enabled=preference_data.notifications_enabled,
            email_notifications=preference_data.email_notifications,
            sms_notifications=preference_data.sms_notifications,
            push_notifications=preference_data.push_notifications,
            created_by=created_by,
            metadata=preference_data.metadata)

        # حفظ التفضيلات في قاعدة البيانات
        self.db.add(preference)
        self.db.commit()
        self.db.refresh(preference)

        return preference

    def get_user_preference(self, user_id: str) -> Optional[UserPreference]:
        """
        استرجاع تفضيلات المستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[UserPreference]: التفضيلات إذا وجدت، وإلا None
        """
        return self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id).first()

    def update_user_preference(
            self,
            user_id: str,
            preference_data: UserPreferenceUpdate,
            updated_by: Optional[str] = None) -> Optional[UserPreference]:
        """
        تحديث تفضيلات المستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            preference_data (UserPreferenceUpdate): بيانات التحديث
            updated_by (Optional[str]): معرف المستخدم الذي قام بالتحديث

        العوائد:
            Optional[UserPreference]: التفضيلات المحدثة إذا وجدت، وإلا None
        """
        # البحث عن التفضيلات في قاعدة البيانات
        preference = self.get_user_preference(user_id)

        if not preference:
            return None

        # تحديث التفضيلات
        if preference_data.language is not None:
            preference.language = preference_data.language

        if preference_data.timezone is not None:
            preference.timezone = preference_data.timezone

        if preference_data.date_format is not None:
            preference.date_format = preference_data.date_format

        if preference_data.time_format is not None:
            preference.time_format = preference_data.time_format

        if preference_data.theme is not None:
            preference.theme = preference_data.theme

        if preference_data.notifications_enabled is not None:
            preference.notifications_enabled = preference_data.notifications_enabled

        if preference_data.email_notifications is not None:
            preference.email_notifications = preference_data.email_notifications

        if preference_data.sms_notifications is not None:
            preference.sms_notifications = preference_data.sms_notifications

        if preference_data.push_notifications is not None:
            preference.push_notifications = preference_data.push_notifications

        if preference_data.metadata is not None:
            preference.metadata = preference_data.metadata

        # تحديث معلومات التحديث
        preference.updated_at = datetime.now(timezone.utc)
        preference.updated_by = updated_by

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(preference)

        return preference

    # ==================== إدارة الأدوار ====================

    def create_role(
            self,
            role_data: RoleCreate,
            created_by: Optional[str] = None) -> Role:
        """
        إنشاء دور جديد

        المعلمات:
            role_data (RoleCreate): بيانات الدور
            created_by (Optional[str]): معرف المستخدم الذي أنشأ الدور

        العوائد:
            Role: الدور المنشأ

        يرفع:
            HTTPException: إذا كان اسم الدور موجوداً بالفعل
        """
        # التحقق من عدم وجود دور بنفس الاسم
        existing_role = self.get_role_by_name(role_data.name)

        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="اسم الدور موجود بالفعل"
            )

        # إنشاء كائن الدور
        role = Role(
            id=str(uuid.uuid4()),
            name=role_data.name,
            description=role_data.description,
            is_system=role_data.is_system,
            is_default=role_data.is_default,
            created_by=created_by,
            metadata=role_data.metadata
        )

        # حفظ الدور في قاعدة البيانات
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        return role

    def get_role(self, role_id: str) -> Optional[Role]:
        """
        استرجاع دور بواسطة المعرف

        المعلمات:
            role_id (str): معرف الدور

        العوائد:
            Optional[Role]: الدور إذا وجد، وإلا None
        """
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """
        استرجاع دور بواسطة الاسم

        المعلمات:
            name (str): اسم الدور

        العوائد:
            Optional[Role]: الدور إذا وجد، وإلا None
        """
        return self.db.query(Role).filter(Role.name == name).first()

    def get_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """
        استرجاع قائمة الأدوار

        المعلمات:
            skip (int): عدد الأدوار للتخطي
            limit (int): الحد الأقصى لعدد الأدوار

        العوائد:
            List[Role]: قائمة الأدوار
        """
        return self.db.query(Role).offset(skip).limit(limit).all()

    def update_role(self, role_id: str, role_data: RoleUpdate,
                    updated_by: Optional[str] = None) -> Optional[Role]:
        """
        تحديث دور

        المعلمات:
            role_id (str): معرف الدور
            role_data (RoleUpdate): بيانات التحديث
            updated_by (Optional[str]): معرف المستخدم الذي قام بالتحديث

        العوائد:
            Optional[Role]: الدور المحدث إذا وجد، وإلا None

        يرفع:
            HTTPException: إذا كان اسم الدور موجوداً بالفعل
        """
        # البحث عن الدور في قاعدة البيانات
        role = self.get_role(role_id)

        if not role:
            return None

        # التحقق من عدم وجود دور آخر بنفس الاسم
        if role_data.name and role_data.name != role.name:
            existing_role = self.get_role_by_name(role_data.name)
            if existing_role and existing_role.id != role_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="اسم الدور موجود بالفعل"
                )

        # تحديث الدور
        if role_data.name is not None:
            role.name = role_data.name

        if role_data.description is not None:
            role.description = role_data.description

        if role_data.is_default is not None:
            role.is_default = role_data.is_default

        if role_data.metadata is not None:
            role.metadata = role_data.metadata

        # تحديث معلومات التحديث
        role.updated_at = datetime.now(timezone.utc)
        role.updated_by = updated_by

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(role)

        return role

    def delete_role(self, role_id: str) -> bool:
        """
        حذف دور

        المعلمات:
            role_id (str): معرف الدور

        العوائد:
            bool: True إذا تم الحذف بنجاح، وإلا False

        يرفع:
            HTTPException: إذا كان الدور نظامياً
        """
        # البحث عن الدور في قاعدة البيانات
        role = self.get_role(role_id)

        if not role:
            return False

        # التحقق من أن الدور ليس نظامياً
        if role.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="لا يمكن حذف الأدوار النظامية"
            )

        # حذف الدور
        self.db.delete(role)
        self.db.commit()

        return True

    def get_user_roles(self, user_id: str) -> List[Role]:
        """
        استرجاع أدوار المستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            List[Role]: قائمة الأدوار
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return []

        return user.roles

    def assign_role_to_user(
            self,
            user_id: str,
            role_id: str,
            assigned_by: Optional[str] = None) -> bool:
        """
        تعيين دور للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            role_id (str): معرف الدور
            assigned_by (Optional[str]): معرف المستخدم الذي قام بالتعيين

        العوائد:
            bool: True إذا تم التعيين بنجاح، وإلا False

        يرفع:
            HTTPException: إذا كان المستخدم أو الدور غير موجود
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المستخدم غير موجود"
            )

        # البحث عن الدور في قاعدة البيانات
        role = self.get_role(role_id)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="الدور غير موجود"
            )

        # التحقق مما إذا كان المستخدم لديه الدور بالفعل
        if role in user.roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="الدور معين بالفعل للمستخدم"
            )

        # تعيين الدور للمستخدم
        user.roles.append(role)

        # حفظ التغييرات
        self.db.commit()

        return True

    def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """
        إزالة دور من المستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            role_id (str): معرف الدور

        العوائد:
            bool: True إذا تمت الإزالة بنجاح، وإلا False
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user:
            return False

        # البحث عن الدور في قاعدة البيانات
        role = self.get_role(role_id)

        if not role:
            return False

        # التحقق مما إذا كان المستخدم لديه الدور
        if role not in user.roles:
            return True

        # إزالة الدور من المستخدم
        user.roles.remove(role)

        # حفظ التغييرات
        self.db.commit()

        return True

    # ==================== إدارة المؤسسات ====================

    def create_organization(
            self, org_data: OrganizationCreate, created_by: Optional[str] = None) -> Organization:
        """
        إنشاء مؤسسة جديدة

        المعلمات:
            org_data (OrganizationCreate): بيانات المؤسسة
            created_by (Optional[str]): معرف المستخدم الذي أنشأ المؤسسة

        العوائد:
            Organization: المؤسسة المنشأة
        """
        # إنشاء كائن المؤسسة
        organization = Organization(
            id=str(uuid.uuid4()),
            name=org_data.name,
            description=org_data.description,
            country=org_data.country,
            city=org_data.city,
            address=org_data.address,
            phone=org_data.phone,
            email=org_data.email,
            website=org_data.website,
            logo=org_data.logo,
            is_active=org_data.is_active,
            parent_id=org_data.parent_id,
            created_by=created_by,
            metadata=org_data.metadata
        )

        # حفظ المؤسسة في قاعدة البيانات
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def get_organization(self, org_id: str) -> Optional[Organization]:
        """
        استرجاع مؤسسة بواسطة المعرف

        المعلمات:
            org_id (str): معرف المؤسسة

        العوائد:
            Optional[Organization]: المؤسسة إذا وجدت، وإلا None
        """
        return self.db.query(Organization).filter(
            Organization.id == org_id).first()

    def get_organizations(
            self,
            skip: int = 0,
            limit: int = 100) -> List[Organization]:
        """
        استرجاع قائمة المؤسسات

        المعلمات:
            skip (int): عدد المؤسسات للتخطي
            limit (int): الحد الأقصى لعدد المؤسسات

        العوائد:
            List[Organization]: قائمة المؤسسات
        """
        return self.db.query(Organization).offset(skip).limit(limit).all()

    def get_organization_branches(self, org_id: str) -> List[Organization]:
        """
        استرجاع فروع المؤسسة

        المعلمات:
            org_id (str): معرف المؤسسة الأم

        العوائد:
            List[Organization]: قائمة الفروع
        """
        return (
            self.db.query(Organization)
            .filter(Organization.parent_id == org_id)
            .all()
        )

    def update_organization(
            self,
            org_id: str,
            org_data: OrganizationUpdate,
            updated_by: Optional[str] = None) -> Optional[Organization]:
        """
        تحديث مؤسسة

        المعلمات:
            org_id (str): معرف المؤسسة
            org_data (OrganizationUpdate): بيانات التحديث
            updated_by (Optional[str]): معرف المستخدم الذي قام بالتحديث

        العوائد:
            Optional[Organization]: المؤسسة المحدثة إذا وجدت، وإلا None
        """
        # البحث عن المؤسسة في قاعدة البيانات
        organization = self.get_organization(org_id)

        if not organization:
            return None

        # تحديث المؤسسة
        if org_data.name is not None:
            organization.name = org_data.name

        if org_data.description is not None:
            organization.description = org_data.description

        if org_data.country is not None:
            organization.country = org_data.country

        if org_data.city is not None:
            organization.city = org_data.city

        if org_data.address is not None:
            organization.address = org_data.address

        if org_data.phone is not None:
            organization.phone = org_data.phone

        if org_data.email is not None:
            organization.email = org_data.email

        if org_data.website is not None:
            organization.website = org_data.website

        if org_data.logo is not None:
            organization.logo = org_data.logo

        if org_data.is_active is not None:
            organization.is_active = org_data.is_active

        if org_data.parent_id is not None:
            organization.parent_id = org_data.parent_id

        if org_data.metadata is not None:
            organization.metadata = org_data.metadata

        # تحديث معلومات التحديث
        organization.updated_at = datetime.now(timezone.utc)
        organization.updated_by = updated_by

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(organization)

        return organization

    def delete_organization(self, org_id: str) -> bool:
        """
        حذف مؤسسة

        المعلمات:
            org_id (str): معرف المؤسسة

        العوائد:
            bool: True إذا تم الحذف بنجاح، وإلا False

        يرفع:
            HTTPException: إذا كان للمؤسسة فروع أو مستخدمين
        """
        # البحث عن المؤسسة في قاعدة البيانات
        organization = self.get_organization(org_id)

        if not organization:
            return False

        # التحقق من عدم وجود فروع للمؤسسة
        branches = self.get_organization_branches(org_id)

        if branches:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="لا يمكن حذف المؤسسة لأنها تحتوي على فروع"
            )

        # التحقق من عدم وجود مستخدمين في المؤسسة
        users = self.db.query(User).filter(
            User.organization_id == org_id).all()

        if users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="لا يمكن حذف المؤسسة لأنها تحتوي على مستخدمين"
            )

        # حذف المؤسسة
        self.db.delete(organization)
        self.db.commit()

        return True

    # ==================== وظائف مساعدة ====================

    def get_user_with_details(self, user_id: str) -> Optional[User]:
        """
        استرجاع المستخدم مع التفاصيل

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[User]: المستخدم مع التفاصيل إذا وجد، وإلا None
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        # تحميل العلاقات
        self.db.refresh(user)

        return user

    def is_password_expired(self, user_id: str) -> bool:
        """
        التحقق مما إذا كانت كلمة المرور منتهية الصلاحية

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            bool: True إذا كانت كلمة المرور منتهية الصلاحية، وإلا False
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user or not user.password_changed_at:
            return False

        # حساب الفترة منذ آخر تغيير لكلمة المرور
        days_since_change = (datetime.now(timezone.utc) - user.password_changed_at).days

        # التحقق مما إذا كانت الفترة تتجاوز الحد الأقصى
        return days_since_change > self.config.password_policy.max_age_days

    def is_account_locked(self, user_id: str) -> bool:
        """
        التحقق مما إذا كان الحساب مقفلاً

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            bool: True إذا كان الحساب مقفلاً، وإلا False
        """
        # البحث عن المستخدم في قاعدة البيانات
        user = self.get_user(user_id)

        if not user or not user.locked_until:
            return False

        # التحقق مما إذا كان وقت القفل لم ينته بعد
        return user.locked_until > datetime.now(timezone.utc)


# تصدير الدوال والكائنات
__all__ = ['UserService']
