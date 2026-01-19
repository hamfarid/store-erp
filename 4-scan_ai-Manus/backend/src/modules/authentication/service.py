"""
/home/ubuntu/implemented_files/v3/src/modules/authentication/service.py

خدمة المصادقة

يوفر هذا الملف خدمة المصادقة لنظام Gaara ERP، بما في ذلك:
- تسجيل الدخول والخروج
- إدارة الرموز والجلسات
- المصادقة متعددة العوامل
- استعادة كلمات المرور
- التحقق من البريد الإلكتروني
- المصادقة باستخدام مزودي OAuth
"""

import hashlib
import logging
import os
import re
import secrets
import uuid

# Standard library imports
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

# Third-party imports
import jwt
import pyotp
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.modules.user_management.models import User
from src.modules.user_management.service import UserService

# Local application imports
from .config import default_config
from .models import (
    AuthLog,
    AuthProvider,
    LoginStatus,
    MFAConfiguration,
    MFAMethod,
    MFAMethodConfiguration,
    OAuthAccount,
    Token,
    TokenStatus,
    TokenType,
    UserSession,
)
from .schemas import (
    AuthLogCreate,
    EmailVerificationRequest,
    EmailVerificationResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    MFAConfigurationCreate,
    MFAConfigurationUpdate,
    MFAMethodConfigurationCreate,
    MFAMethodConfigurationUpdate,
    MFAVerifyRequest,
    MFAVerifyResponse,
    OAuthAccountCreate,
    OAuthAccountUpdate,
    PasswordResetConfirmRequest,
    PasswordResetConfirmResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    TokenCreate,
    TokenUpdate,
    UserSessionCreate,
    UserSessionUpdate,
)

# إعداد التسجيل
logger = logging.getLogger(__name__)

# تعريف الثوابت للرسائل المتكررة
INVALID_CREDENTIALS = "اسم المستخدم أو كلمة المرور غير صحيحة"
ACCOUNT_INACTIVE = "الحساب غير نشط"
USER_NOT_FOUND = "المستخدم غير موجود"


class AuthenticationService:
    """خدمة المصادقة"""

    def __init__(self, db: Session):
        """
        تهيئة خدمة المصادقة

        المعلمات:
            db (Session): جلسة قاعدة البيانات
        """
        self.db = db
        self.config = default_config
        self.user_service = UserService(db)

    # ==================== إدارة الرموز ====================

    def create_token(self, token_data: TokenCreate) -> Token:
        """
        إنشاء رمز جديد

        المعلمات:
            token_data (TokenCreate): بيانات الرمز

        العوائد:
            Token: الرمز المنشأ
        """
        # إنشاء رمز عشوائي
        raw_token = secrets.token_urlsafe(32)

        # حساب هاش الرمز
        token_hash = self._hash_token(raw_token)

        # تحديد مدة صلاحية الرمز
        expires_in_seconds = token_data.expires_in_seconds
        if not expires_in_seconds:
            if token_data.token_type == TokenType.ACCESS:
                expires_in_seconds = self.config.jwt.access_token_expire_minutes * \
                    60  # pylint: disable=no-member
            elif token_data.token_type == TokenType.REFRESH:
                expires_in_seconds = self.config.jwt.refresh_token_expire_days * \
                    24 * 60 * 60  # pylint: disable=no-member
            elif token_data.token_type == TokenType.PASSWORD_RESET:
                expires_in_seconds = self.config.password.password_reset_token_expire_minutes * \
                    60  # pylint: disable=no-member
            elif token_data.token_type == TokenType.EMAIL_VERIFICATION:
                expires_in_seconds = self.config.email_verification_token_expire_hours * 60 * 60
            else:
                expires_in_seconds = 3600  # ساعة واحدة افتراضياً

        # إنشاء كائن الرمز
        token = Token(
            id=str(
                uuid.uuid4()),
            user_id=token_data.user_id,
            token_type=token_data.token_type,
            token_hash=token_hash,
            status=TokenStatus.ACTIVE,
            expires_at=datetime.now(
                timezone.utc) +
            timedelta(
                seconds=expires_in_seconds),
            metadata=token_data.metadata)

        # حفظ الرمز في قاعدة البيانات
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)

        # إرجاع الرمز مع الرمز الخام
        token.raw_token = raw_token

        return token

    def get_token(self, token_id: str) -> Optional[Token]:
        """
        استرجاع رمز بواسطة المعرف

        المعلمات:
            token_id (str): معرف الرمز

        العوائد:
            Optional[Token]: الرمز إذا وجد، وإلا None
        """
        return self.db.query(Token).filter(Token.id == token_id).first()

    def get_token_by_hash(self, token_hash: str) -> Optional[Token]:
        """
        استرجاع رمز بواسطة هاش الرمز

        المعلمات:
            token_hash (str): هاش الرمز

        العوائد:
            Optional[Token]: الرمز إذا وجد، وإلا None
        """
        return self.db.query(Token).filter(
            Token.token_hash == token_hash).first()

    def verify_token(
            self,
            raw_token: str,
            token_type: TokenType) -> Optional[Token]:
        """
        التحقق من صحة الرمز

        المعلمات:
            raw_token (str): الرمز الخام
            token_type (TokenType): نوع الرمز

        العوائد:
            Optional[Token]: الرمز إذا كان صالحاً، وإلا None
        """
        # حساب هاش الرمز
        token_hash = self._hash_token(raw_token)

        # البحث عن الرمز في قاعدة البيانات
        token = self.db.query(Token).filter(
            Token.token_hash == token_hash,
            Token.token_type == token_type,
            Token.status == TokenStatus.ACTIVE,
            Token.expires_at > datetime.now(timezone.utc)
        ).first()

        return token

    def update_token(
            self,
            token_id: str,
            token_data: TokenUpdate) -> Optional[Token]:
        """
        تحديث رمز

        المعلمات:
            token_id (str): معرف الرمز
            token_data (TokenUpdate): بيانات التحديث

        العوائد:
            Optional[Token]: الرمز المحدث إذا وجد، وإلا None
        """
        # البحث عن الرمز في قاعدة البيانات
        token = self.get_token(token_id)

        if not token:
            return None

        # تحديث الرمز
        if token_data.status is not None:
            token.status = token_data.status

        if token_data.revoked_at is not None:
            token.revoked_at = token_data.revoked_at

        if token_data.used_at is not None:
            token.used_at = token_data.used_at

        if token_data.metadata is not None:
            token.metadata = token_data.metadata

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(token)

        return token

    def revoke_token(self, token_id: str) -> bool:
        """
        إلغاء رمز

        المعلمات:
            token_id (str): معرف الرمز

        العوائد:
            bool: True إذا تم الإلغاء بنجاح، وإلا False
        """
        # البحث عن الرمز في قاعدة البيانات
        token = self.get_token(token_id)

        if not token:
            return False

        # إلغاء الرمز
        token.status = TokenStatus.REVOKED
        token.revoked_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()

        return True

    def revoke_user_tokens(
            self,
            user_id: str,
            token_type: Optional[TokenType] = None) -> int:
        """
        إلغاء جميع رموز المستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            token_type (Optional[TokenType]): نوع الرمز (اختياري)

        العوائد:
            int: عدد الرموز الملغاة
        """
        # بناء استعلام البحث
        query = self.db.query(Token).filter(
            Token.user_id == user_id,
            Token.status == TokenStatus.ACTIVE
        )

        if token_type:
            query = query.filter(Token.token_type == token_type)

        # الحصول على الرموز
        tokens = query.all()

        # إلغاء الرموز
        for token in tokens:
            token.status = TokenStatus.REVOKED
            token.revoked_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()

        return len(tokens)

    def clean_expired_tokens(self) -> int:
        """
        تنظيف الرموز منتهية الصلاحية

        العوائد:
            int: عدد الرموز المنظفة
        """
        # البحث عن الرموز منتهية الصلاحية
        tokens = self.db.query(Token).filter(
            Token.status == TokenStatus.ACTIVE,
            Token.expires_at <= datetime.now(timezone.utc)
        ).all()

        # تحديث حالة الرموز
        for token in tokens:
            token.status = TokenStatus.EXPIRED

        # حفظ التغييرات
        self.db.commit()

        return len(tokens)

    # ==================== إدارة الجلسات ====================

    def create_session(self, session_data: UserSessionCreate) -> UserSession:
        """
        إنشاء جلسة مستخدم جديدة

        المعلمات:
            session_data (UserSessionCreate): بيانات الجلسة

        العوائد:
            UserSession: الجلسة المنشأة
        """
        # إنشاء رمز جلسة عشوائي
        raw_session_token = secrets.token_urlsafe(32)

        # حساب هاش رمز الجلسة
        session_token_hash = self._hash_token(raw_session_token)

        # تحديد مدة صلاحية الجلسة
        expires_in_seconds = session_data.expires_in_seconds
        if not expires_in_seconds:
            if session_data.metadata and session_data.metadata.get(
                    "remember_me"):
                expires_in_seconds = self.config.remember_me_days * 24 * 60 * 60
            else:
                expires_in_seconds = self.config.session.session_expire_minutes * \
                    60  # pylint: disable=no-member

        # إنشاء كائن الجلسة
        session = UserSession(
            id=str(
                uuid.uuid4()),
            user_id=session_data.user_id,
            session_token_hash=session_token_hash,
            ip_address=session_data.ip_address,
            user_agent=session_data.user_agent,
            expires_at=datetime.now(
                timezone.utc) +
            timedelta(
                seconds=expires_in_seconds),
            is_active=True,
            metadata=session_data.metadata)

        # التحقق من الحد الأقصى لعدد الجلسات النشطة
        if self.config.session.max_active_sessions_per_user > 0:  # pylint: disable=no-member
            active_sessions_count = self.db.query(UserSession).filter(
                UserSession.user_id == session_data.user_id,
                UserSession.is_active,
                UserSession.expires_at > datetime.now(timezone.utc)
            ).count()

            if active_sessions_count >= self.config.session.max_active_sessions_per_user:  # pylint: disable=no-member
                # إلغاء أقدم جلسة
                oldest_session = self.db.query(UserSession).filter(
                    UserSession.user_id == session_data.user_id,
                    UserSession.is_active,
                    UserSession.expires_at > datetime.now(timezone.utc)
                ).order_by(UserSession.created_at).first()

                if oldest_session:
                    oldest_session.is_active = False
                    oldest_session.revoked_at = datetime.now(timezone.utc)

        # حفظ الجلسة في قاعدة البيانات
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        # إرجاع الجلسة مع رمز الجلسة الخام
        session.raw_session_token = raw_session_token

        return session

    def get_session(self, session_id: str) -> Optional[UserSession]:
        """
        استرجاع جلسة بواسطة المعرف

        المعلمات:
            session_id (str): معرف الجلسة

        العوائد:
            Optional[UserSession]: الجلسة إذا وجدت، وإلا None
        """
        return self.db.query(UserSession).filter(
            UserSession.id == session_id).first()

    def get_session_by_token(
            self,
            raw_session_token: str) -> Optional[UserSession]:
        """
        استرجاع جلسة بواسطة رمز الجلسة

        المعلمات:
            raw_session_token (str): رمز الجلسة الخام

        العوائد:
            Optional[UserSession]: الجلسة إذا وجدت، وإلا None
        """
        # حساب هاش رمز الجلسة
        session_token_hash = self._hash_token(raw_session_token)

        # البحث عن الجلسة في قاعدة البيانات
        session = self.db.query(UserSession).filter(
            UserSession.session_token_hash == session_token_hash,
            UserSession.is_active,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).first()

        return session

    def update_session(
            self,
            session_id: str,
            session_data: UserSessionUpdate) -> Optional[UserSession]:
        """
        تحديث جلسة

        المعلمات:
            session_id (str): معرف الجلسة
            session_data (UserSessionUpdate): بيانات التحديث

        العوائد:
            Optional[UserSession]: الجلسة المحدثة إذا وجدت، وإلا None
        """
        # البحث عن الجلسة في قاعدة البيانات
        session = self.get_session(session_id)

        if not session:
            return None

        # تحديث الجلسة
        if session_data.last_activity_at is not None:
            session.last_activity_at = session_data.last_activity_at

        if session_data.expires_at is not None:
            session.expires_at = session_data.expires_at

        if session_data.revoked_at is not None:
            session.revoked_at = session_data.revoked_at

        if session_data.is_active is not None:
            session.is_active = session_data.is_active

        if session_data.metadata is not None:
            session.metadata = session_data.metadata

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(session)

        return session

    def revoke_session(self, session_id: str) -> bool:
        """
        إلغاء جلسة

        المعلمات:
            session_id (str): معرف الجلسة

        العوائد:
            bool: True إذا تم الإلغاء بنجاح، وإلا False
        """
        current_session = self.get_session(session_id)
        if not current_session:
            return False

        current_session.status = "revoked"
        current_session.revoked_at = datetime.now(timezone.utc)
        self.db.commit()
        return True

    def revoke_user_sessions(
            self,
            user_id: str,
            exclude_session_id: Optional[str] = None) -> int:
        """
        إلغاء جميع جلسات المستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            exclude_session_id (Optional[str]): معرف الجلسة المستثناة

        العوائد:
            int: عدد الجلسات الملغاة
        """
        query = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.status == "active"
        )
        if exclude_session_id:
            query = query.filter(UserSession.id != exclude_session_id)
        user_sessions = query.all()
        count = len(user_sessions)
        for current_session in user_sessions:
            current_session.status = "revoked"
            current_session.revoked_at = datetime.now(timezone.utc)
        self.db.commit()
        return count

    def clean_expired_sessions(self) -> int:
        """
        تنظيف الجلسات منتهية الصلاحية

        العوائد:
            int: عدد الجلسات المنظفة
        """
        # البحث عن الجلسات منتهية الصلاحية
        sessions = self.db.query(UserSession).filter(
            UserSession.is_active,
            UserSession.expires_at <= datetime.now(timezone.utc)
        ).all()

        # تحديث حالة الجلسات
        for session in sessions:
            session.is_active = False

        # حفظ التغييرات
        self.db.commit()

        return len(sessions)

    # ==================== المصادقة متعددة العوامل ====================

    def get_mfa_config(self, user_id: str) -> Optional[MFAConfiguration]:
        """
        استرجاع تكوين المصادقة متعددة العوامل للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[MFAConfiguration]: تكوين المصادقة متعددة العوامل إذا وجد، وإلا None
        """
        return self.db.query(MFAConfiguration).filter(
            MFAConfiguration.user_id == user_id).first()

    def create_mfa_config(
            self,
            mfa_config_data: MFAConfigurationCreate) -> MFAConfiguration:
        """
        إنشاء تكوين المصادقة متعددة العوامل للمستخدم

        المعلمات:
            mfa_config_data (MFAConfigurationCreate): بيانات التكوين

        العوائد:
            MFAConfiguration: تكوين المصادقة متعددة العوامل المنشأ
        """
        # التحقق من عدم وجود تكوين سابق
        existing_config = self.get_mfa_config(mfa_config_data.user_id)

        if existing_config:
            raise ValueError(
                "يوجد تكوين مصادقة متعددة العوامل للمستخدم بالفعل")

        # إنشاء كائن التكوين
        mfa_config = MFAConfiguration(
            id=str(uuid.uuid4()),
            user_id=mfa_config_data.user_id,
            preferred_method=mfa_config_data.preferred_method,
            is_mfa_enabled=mfa_config_data.is_mfa_enabled
        )

        # حفظ التكوين في قاعدة البيانات
        self.db.add(mfa_config)
        self.db.commit()
        self.db.refresh(mfa_config)

        return mfa_config

    def update_mfa_config(
            self,
            user_id: str,
            mfa_config_data: MFAConfigurationUpdate) -> Optional[MFAConfiguration]:
        """
        تحديث تكوين المصادقة متعددة العوامل للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            mfa_config_data (MFAConfigurationUpdate): بيانات التحديث

        العوائد:
            Optional[MFAConfiguration]: تكوين المصادقة متعددة العوامل المحدث إذا وجد، وإلا None
        """
        # البحث عن التكوين في قاعدة البيانات
        mfa_config = self.get_mfa_config(user_id)

        if not mfa_config:
            return None

        # تحديث التكوين
        if mfa_config_data.preferred_method is not None:
            mfa_config.preferred_method = mfa_config_data.preferred_method

        if mfa_config_data.is_mfa_enabled is not None:
            mfa_config.is_mfa_enabled = mfa_config_data.is_mfa_enabled

        # تحديث وقت التحديث
        mfa_config.updated_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(mfa_config)

        return mfa_config

    def get_mfa_method(
            self,
            method_id: str) -> Optional[MFAMethodConfiguration]:
        """
        استرجاع تكوين طريقة المصادقة متعددة العوامل

        المعلمات:
            method_id (str): معرف الطريقة

        العوائد:
            Optional[MFAMethodConfiguration]: تكوين الطريقة إذا وجد، وإلا None
        """
        return self.db.query(MFAMethodConfiguration).filter(
            MFAMethodConfiguration.id == method_id).first()

    def get_mfa_methods(
            self,
            mfa_config_id: str) -> List[MFAMethodConfiguration]:
        """
        استرجاع طرق المصادقة متعددة العوامل لتكوين معين

        المعلمات:
            mfa_config_id (str): معرف تكوين المصادقة متعددة العوامل

        العوائد:
            List[MFAMethodConfiguration]: قائمة طرق المصادقة متعددة العوامل
        """
        return self.db.query(MFAMethodConfiguration).filter(
            MFAMethodConfiguration.mfa_config_id == mfa_config_id
        ).all()

    def get_user_mfa_methods(
            self,
            user_id: str) -> List[MFAMethodConfiguration]:
        """
        استرجاع طرق المصادقة متعددة العوامل للمستخدم

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            List[MFAMethodConfiguration]: قائمة طرق المصادقة متعددة العوامل
        """
        # البحث عن تكوين المصادقة متعددة العوامل للمستخدم
        mfa_config = self.get_mfa_config(user_id)

        if not mfa_config:
            return []

        # استرجاع طرق المصادقة متعددة العوامل
        return self.get_mfa_methods(mfa_config.id)

    def create_mfa_method(
            self,
            method_data: MFAMethodConfigurationCreate) -> MFAMethodConfiguration:
        """
        إنشاء طريقة مصادقة متعددة العوامل

        المعلمات:
            method_data (MFAMethodConfigurationCreate): بيانات الطريقة

        العوائد:
            MFAMethodConfiguration: طريقة المصادقة متعددة العوامل المنشأة
        """
        # إنشاء كائن الطريقة
        mfa_method = MFAMethodConfiguration(
            id=str(uuid.uuid4()),
            mfa_config_id=method_data.mfa_config_id,
            method_type=method_data.method_type,
            secret=method_data.secret,
            phone_number=method_data.phone_number,
            email=method_data.email,
            backup_codes_hashed=method_data.backup_codes_hashed,
            security_key_credential_id=method_data.security_key_credential_id,
            is_verified=method_data.is_verified,
            is_enabled=method_data.is_enabled
        )

        # حفظ الطريقة في قاعدة البيانات
        self.db.add(mfa_method)
        self.db.commit()
        self.db.refresh(mfa_method)

        return mfa_method

    def update_mfa_method(
            self,
            method_id: str,
            method_data: MFAMethodConfigurationUpdate) -> Optional[MFAMethodConfiguration]:
        """
        تحديث طريقة مصادقة متعددة العوامل

        المعلمات:
            method_id (str): معرف الطريقة
            method_data (MFAMethodConfigurationUpdate): بيانات التحديث

        العوائد:
            Optional[MFAMethodConfiguration]: طريقة المصادقة متعددة العوامل المحدثة إذا وجدت، وإلا None
        """
        # البحث عن الطريقة في قاعدة البيانات
        mfa_method = self.get_mfa_method(method_id)

        if not mfa_method:
            return None

        # تحديث الطريقة
        if method_data.secret is not None:
            mfa_method.secret = method_data.secret

        if method_data.phone_number is not None:
            mfa_method.phone_number = method_data.phone_number

        if method_data.email is not None:
            mfa_method.email = method_data.email

        if method_data.backup_codes_hashed is not None:
            mfa_method.backup_codes_hashed = method_data.backup_codes_hashed

        if method_data.security_key_credential_id is not None:
            mfa_method.security_key_credential_id = method_data.security_key_credential_id

        if method_data.is_verified is not None:
            mfa_method.is_verified = method_data.is_verified

        if method_data.is_enabled is not None:
            mfa_method.is_enabled = method_data.is_enabled

        # تحديث وقت التحديث
        mfa_method.updated_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(mfa_method)

        return mfa_method

    def delete_mfa_method(self, method_id: str) -> bool:
        """
        حذف طريقة مصادقة متعددة العوامل

        المعلمات:
            method_id (str): معرف الطريقة

        العوائد:
            bool: True إذا تم الحذف بنجاح، وإلا False
        """
        # البحث عن الطريقة في قاعدة البيانات
        mfa_method = self.get_mfa_method(method_id)

        if not mfa_method:
            return False

        # حذف الطريقة
        self.db.delete(mfa_method)
        self.db.commit()

        return True

    def generate_totp_secret(self) -> str:
        """
        إنشاء سر TOTP

        العوائد:
            str: سر TOTP
        """
        return pyotp.random_base32()

    def generate_totp_uri(self, secret: str, user_email: str) -> str:
        """
        إنشاء URI TOTP

        المعلمات:
            secret (str): سر TOTP
            user_email (str): بريد المستخدم الإلكتروني

        العوائد:
            str: URI TOTP
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=user_email,
            issuer_name=self.config.mfa.totp_issuer)  # pylint: disable=no-member  # pylint: disable=no-member

    def verify_totp(self, secret: str, code: str) -> bool:
        """
        التحقق من رمز TOTP

        المعلمات:
            secret (str): سر TOTP
            code (str): رمز TOTP

        العوائد:
            bool: True إذا كان الرمز صحيحاً، وإلا False
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(code)

    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """
        إنشاء رموز النسخ الاحتياطي

        المعلمات:
            count (int): عدد الرموز

        العوائد:
            List[str]: قائمة رموز النسخ الاحتياطي
        """
        codes = []
        for _ in range(count):
            code = secrets.token_hex(5)  # 10 أحرف
            codes.append(code)

        return codes

    def hash_backup_codes(self, codes: List[str]) -> List[str]:
        """
        تشفير رموز النسخ الاحتياطي

        المعلمات:
            codes (List[str]): قائمة رموز النسخ الاحتياطي

        العوائد:
            List[str]: قائمة رموز النسخ الاحتياطي المشفرة
        """
        hashed_codes = []
        for code in codes:
            hashed_code = self._hash_token(code)
            hashed_codes.append(hashed_code)

        return hashed_codes

    def verify_backup_code(self, hashed_codes: List[str], code: str) -> bool:
        """
        التحقق من رمز النسخ الاحتياطي

        المعلمات:
            hashed_codes (List[str]): قائمة رموز النسخ الاحتياطي المشفرة
            code (str): رمز النسخ الاحتياطي

        العوائد:
            bool: True إذا كان الرمز صحيحاً، وإلا False
        """
        # حساب هاش الرمز
        hashed_code = self._hash_token(code)

        # التحقق من وجود الرمز في القائمة
        return hashed_code in hashed_codes

    def use_backup_code(self, mfa_method_id: str, code: str) -> bool:
        """
        استخدام رمز النسخ الاحتياطي

        المعلمات:
            mfa_method_id (str): معرف طريقة المصادقة متعددة العوامل
            code (str): رمز النسخ الاحتياطي

        العوائد:
            bool: True إذا تم استخدام الرمز بنجاح، وإلا False
        """
        # البحث عن الطريقة في قاعدة البيانات
        mfa_method = self.get_mfa_method(mfa_method_id)

        if not mfa_method or mfa_method.method_type != MFAMethod.BACKUP_CODE:
            return False

        # التحقق من وجود رموز النسخ الاحتياطي
        if not mfa_method.backup_codes_hashed:
            return False

        # حساب هاش الرمز
        hashed_code = self._hash_token(code)

        # التحقق من وجود الرمز في القائمة
        if hashed_code not in mfa_method.backup_codes_hashed:
            return False

        # إزالة الرمز من القائمة
        mfa_method.backup_codes_hashed.remove(hashed_code)

        # حفظ التغييرات
        self.db.commit()

        return True

    # ==================== سجلات المصادقة ====================

    def create_auth_log(self, log_data: AuthLogCreate) -> AuthLog:
        """
        إنشاء سجل مصادقة

        المعلمات:
            log_data (AuthLogCreate): بيانات السجل

        العوائد:
            AuthLog: سجل المصادقة المنشأ
        """
        # إنشاء كائن السجل
        auth_log = AuthLog(
            id=str(uuid.uuid4()),
            user_id=log_data.user_id,
            username_attempt=log_data.username_attempt,
            timestamp=datetime.now(timezone.utc),
            action=log_data.action,
            status=log_data.status,
            ip_address=log_data.ip_address,
            user_agent=log_data.user_agent,
            provider=log_data.provider,
            error_message=log_data.error_message,
            metadata=log_data.metadata
        )

        # حفظ السجل في قاعدة البيانات
        self.db.add(auth_log)
        self.db.commit()
        self.db.refresh(auth_log)

        return auth_log

    def get_auth_logs(
            self,
            user_id: Optional[str] = None,
            limit: int = 100) -> List[AuthLog]:
        """
        استرجاع سجلات المصادقة

        المعلمات:
            user_id (Optional[str]): معرف المستخدم (اختياري)
            limit (int): الحد الأقصى لعدد السجلات

        العوائد:
            List[AuthLog]: قائمة سجلات المصادقة
        """
        # بناء استعلام البحث
        query = self.db.query(AuthLog)

        if user_id:
            query = query.filter(AuthLog.user_id == user_id)

        # ترتيب السجلات حسب الوقت تنازلياً
        query = query.order_by(AuthLog.timestamp.desc())

        # تحديد عدد السجلات
        query = query.limit(limit)

        return query.all()

    def get_failed_login_attempts(
            self,
            username: str,
            minutes: int = 15) -> int:
        """
        استرجاع عدد محاولات تسجيل الدخول الفاشلة

        المعلمات:
            username (str): اسم المستخدم
            minutes (int): عدد الدقائق السابقة

        العوائد:
            int: عدد محاولات تسجيل الدخول الفاشلة
        """
        # حساب الوقت السابق
        time_ago = datetime.now(timezone.utc) - timedelta(minutes=minutes)

        # بناء استعلام البحث
        count = self.db.query(AuthLog).filter(
            AuthLog.username_attempt == username,
            AuthLog.action == "login",
            AuthLog.status == LoginStatus.FAILURE,
            AuthLog.timestamp >= time_ago
        ).count()

        return count

    def is_account_locked(self, username: str) -> bool:
        """
        التحقق مما إذا كان الحساب مقفلاً

        المعلمات:
            username (str): اسم المستخدم

        العوائد:
            bool: True إذا كان الحساب مقفلاً، وإلا False
        """
        # الحصول على عدد محاولات تسجيل الدخول الفاشلة
        failed_attempts = self.get_failed_login_attempts(
            username,
            self.config.password.lockout_duration_minutes  # pylint: disable=no-member  # pylint: disable=no-member
        )

        # التحقق مما إذا كان عدد المحاولات الفاشلة يتجاوز الحد
        return failed_attempts >= self.config.password.lockout_threshold  # pylint: disable=no-member  # pylint: disable=no-member

    # ==================== حسابات OAuth ====================

    def get_oauth_account(self, id: str) -> Optional[OAuthAccount]:
        """
        استرجاع حساب OAuth بواسطة المعرف

        المعلمات:
            id (str): معرف الحساب

        العوائد:
            Optional[OAuthAccount]: حساب OAuth إذا وجد، وإلا None
        """
        return self.db.query(OAuthAccount).filter(
            OAuthAccount.id == id).first()

    def get_oauth_account_by_provider(
            self,
            user_id: str,
            provider: AuthProvider) -> Optional[OAuthAccount]:
        """
        استرجاع حساب OAuth بواسطة المزود

        المعلمات:
            user_id (str): معرف المستخدم
            provider (AuthProvider): مزود المصادقة

        العوائد:
            Optional[OAuthAccount]: حساب OAuth إذا وجد، وإلا None
        """
        return self.db.query(OAuthAccount).filter(
            OAuthAccount.user_id == user_id,
            OAuthAccount.provider == provider
        ).first()

    def get_oauth_account_by_provider_user_id(
            self,
            provider: AuthProvider,
            provider_user_id: str) -> Optional[OAuthAccount]:
        """
        استرجاع حساب OAuth بواسطة معرف المستخدم لدى المزود

        المعلمات:
            provider (AuthProvider): مزود المصادقة
            provider_user_id (str): معرف المستخدم لدى المزود

        العوائد:
            Optional[OAuthAccount]: حساب OAuth إذا وجد، وإلا None
        """
        return self.db.query(OAuthAccount).filter(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_user_id == provider_user_id
        ).first()

    def create_oauth_account(
            self,
            oauth_data: OAuthAccountCreate) -> OAuthAccount:
        """
        إنشاء حساب OAuth

        المعلمات:
            oauth_data (OAuthAccountCreate): بيانات الحساب

        العوائد:
            OAuthAccount: حساب OAuth المنشأ
        """
        # إنشاء كائن الحساب
        oauth_account = OAuthAccount(
            id=str(uuid.uuid4()),
            user_id=oauth_data.user_id,
            provider=oauth_data.provider,
            provider_user_id=oauth_data.provider_user_id,
            access_token=oauth_data.access_token,
            refresh_token=oauth_data.refresh_token,
            expires_at=oauth_data.expires_at,
            scope=oauth_data.scope
        )

        # حفظ الحساب في قاعدة البيانات
        self.db.add(oauth_account)
        self.db.commit()
        self.db.refresh(oauth_account)

        return oauth_account

    def update_oauth_account(
            self,
            id: str,
            oauth_data: OAuthAccountUpdate) -> Optional[OAuthAccount]:
        """
        تحديث حساب OAuth

        المعلمات:
            id (str): معرف الحساب
            oauth_data (OAuthAccountUpdate): بيانات التحديث

        العوائد:
            Optional[OAuthAccount]: حساب OAuth المحدث إذا وجد، وإلا None
        """
        # البحث عن الحساب في قاعدة البيانات
        oauth_account = self.get_oauth_account(id)

        if not oauth_account:
            return None

        # تحديث الحساب
        if oauth_data.access_token is not None:
            oauth_account.access_token = oauth_data.access_token

        if oauth_data.refresh_token is not None:
            oauth_account.refresh_token = oauth_data.refresh_token

        if oauth_data.expires_at is not None:
            oauth_account.expires_at = oauth_data.expires_at

        if oauth_data.scope is not None:
            oauth_account.scope = oauth_data.scope

        # تحديث وقت التحديث
        oauth_account.updated_at = datetime.now(timezone.utc)

        # حفظ التغييرات
        self.db.commit()
        self.db.refresh(oauth_account)

        return oauth_account

    def delete_oauth_account(self, id: str) -> bool:
        """
        حذف حساب OAuth

        المعلمات:
            id (str): معرف الحساب

        العوائد:
            bool: True إذا تم الحذف بنجاح، وإلا False
        """
        # البحث عن الحساب في قاعدة البيانات
        oauth_account = self.get_oauth_account(id)

        if not oauth_account:
            return False

        # حذف الحساب
        self.db.delete(oauth_account)
        self.db.commit()

        return True

    # ==================== عمليات المصادقة ====================

    def login(
            self,
            login_data: LoginRequest,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None) -> LoginResponse:
        """
        تسجيل الدخول

        المعلمات:
            login_data (LoginRequest): بيانات تسجيل الدخول
            ip_address (Optional[str]): عنوان IP
            user_agent (Optional[str]): وكيل المستخدم

        العوائد:
            LoginResponse: استجابة تسجيل الدخول

        يرفع:
            HTTPException: إذا فشل تسجيل الدخول
        """
        # التحقق مما إذا كان الحساب مقفلاً
        if self.is_account_locked(login_data.username):
            # تسجيل محاولة تسجيل الدخول
            self.create_auth_log(
                AuthLogCreate(
                    username_attempt=login_data.username,
                    action="login",
                    status=LoginStatus.LOCKED_OUT,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    provider=AuthProvider.LOCAL,
                    error_message="الحساب مقفل بسبب عدد كبير من محاولات تسجيل الدخول الفاشلة"))

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="الحساب مقفل بسبب عدد كبير من محاولات تسجيل الدخول الفاشلة")

        # البحث عن المستخدم
        user = self.user_service.get_user_by_username(login_data.username)

        if not user:
            # تسجيل محاولة تسجيل الدخول
            self.create_auth_log(AuthLogCreate(
                username_attempt=login_data.username,
                action="login",
                status=LoginStatus.FAILURE,
                ip_address=ip_address,
                user_agent=user_agent,
                provider=AuthProvider.LOCAL,
                error_message=INVALID_CREDENTIALS
            ))

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS
            )

        # التحقق من كلمة المرور
        if not self.user_service.verify_password(
                login_data.password, user.password_hash):
            # تسجيل محاولة تسجيل الدخول
            self.create_auth_log(AuthLogCreate(
                user_id=user.id,
                username_attempt=login_data.username,
                action="login",
                status=LoginStatus.FAILURE,
                ip_address=ip_address,
                user_agent=user_agent,
                provider=AuthProvider.LOCAL,
                error_message=INVALID_CREDENTIALS
            ))

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS
            )

        # التحقق من حالة المستخدم
        if not user.is_active:
            # تسجيل محاولة تسجيل الدخول
            self.create_auth_log(AuthLogCreate(
                user_id=user.id,
                username_attempt=login_data.username,
                action="login",
                status=LoginStatus.FAILURE,
                ip_address=ip_address,
                user_agent=user_agent,
                provider=AuthProvider.LOCAL,
                error_message=ACCOUNT_INACTIVE
            ))

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ACCOUNT_INACTIVE
            )

        # التحقق من المصادقة متعددة العوامل
        mfa_config = self.get_mfa_config(user.id)
        requires_mfa = False
        mfa_token = None
        available_mfa_methods = None

        if mfa_config and mfa_config.is_mfa_enabled:
            # الحصول على طرق المصادقة متعددة العوامل المتاحة
            mfa_methods = self.get_mfa_methods(mfa_config.id)
            verified_methods = [
                m for m in mfa_methods if m.is_verified and m.is_enabled]

            if verified_methods:
                requires_mfa = True
                available_mfa_methods = [
                    m.method_type for m in verified_methods]

                # إنشاء رمز MFA
                mfa_token_obj = self.create_token(TokenCreate(
                    user_id=user.id,
                    token_type=TokenType.MFA_SETUP,
                    expires_in_seconds=300,  # 5 دقائق
                    metadata={"username": user.username}
                ))

                mfa_token = mfa_token_obj.raw_token

        if requires_mfa:
            # تسجيل محاولة تسجيل الدخول
            self.create_auth_log(AuthLogCreate(
                user_id=user.id,
                username_attempt=login_data.username,
                action="login",
                status=LoginStatus.MFA_REQUIRED,
                ip_address=ip_address,
                user_agent=user_agent,
                provider=AuthProvider.LOCAL
            ))

            return LoginResponse(
                access_token="",
                token_type="bearer",
                expires_in=0,
                refresh_token="",
                user_id=user.id,
                requires_mfa=True,
                mfa_token=mfa_token,
                available_mfa_methods=available_mfa_methods
            )

        # إنشاء رمز الوصول
        access_token_obj = self.create_token(TokenCreate(
            user_id=user.id,
            token_type=TokenType.ACCESS,
            metadata={"username": user.username}
        ))

        # إنشاء رمز التحديث
        refresh_token_obj = self.create_token(TokenCreate(
            user_id=user.id,
            token_type=TokenType.REFRESH,
            metadata={"username": user.username}
        ))

        # إنشاء جلسة المستخدم
        session = self.create_session(UserSessionCreate(
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={"remember_me": login_data.remember_me}
        ))

        # تسجيل محاولة تسجيل الدخول
        self.create_auth_log(AuthLogCreate(
            user_id=user.id,
            username_attempt=login_data.username,
            action="login",
            status=LoginStatus.SUCCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            provider=AuthProvider.LOCAL
        ))

        # حساب مدة صلاحية رمز الوصول بالثواني
        expires_in = int(
            (access_token_obj.expires_at -
             datetime.now(
                 timezone.utc)).total_seconds())

        return LoginResponse(
            access_token=access_token_obj.raw_token,
            token_type="bearer",
            expires_in=expires_in,
            refresh_token=refresh_token_obj.raw_token,
            user_id=user.id,
            requires_mfa=False,
            session_id=session.id
        )

    def verify_mfa(
            self,
            verify_data: MFAVerifyRequest,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None) -> MFAVerifyResponse:
        """
        التحقق من المصادقة متعددة العوامل

        المعلمات:
            verify_data (MFAVerifyRequest): بيانات التحقق
            ip_address (Optional[str]): عنوان IP
            user_agent (Optional[str]): وكيل المستخدم

        العوائد:
            MFAVerifyResponse: استجابة التحقق

        يرفع:
            HTTPException: إذا فشل التحقق
        """
        # التحقق من رمز MFA
        mfa_token = self.verify_token(
            verify_data.mfa_token, TokenType.MFA_SETUP)

        if not mfa_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="رمز MFA غير صالح أو منتهي الصلاحية"
            )

        # الحصول على المستخدم
        user_id = mfa_token.user_id
        user = self.user_service.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_FOUND
            )

        # الحصول على تكوين المصادقة متعددة العوامل
        mfa_config = self.get_mfa_config(user_id)

        if not mfa_config:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="المصادقة متعددة العوامل غير مكونة"
            )

        # الحصول على طرق المصادقة متعددة العوامل
        mfa_methods = self.get_mfa_methods(mfa_config.id)

        # البحث عن الطريقة المطلوبة
        method = None
        for m in mfa_methods:
            if m.method_type == verify_data.method_type and m.is_verified and m.is_enabled:
                method = m
                break

        if not method:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="طريقة المصادقة متعددة العوامل غير متاحة"
            )

        # التحقق من الرمز
        is_valid = False

        if method.method_type == MFAMethod.TOTP:
            is_valid = self.verify_totp(method.secret, verify_data.mfa_code)
        elif method.method_type == MFAMethod.BACKUP_CODE:
            is_valid = self.use_backup_code(method.id, verify_data.mfa_code)
        else:
            # طرق أخرى غير مدعومة حالياً
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="طريقة المصادقة متعددة العوامل غير مدعومة"
            )

        if not is_valid:
            # تسجيل محاولة التحقق
            self.create_auth_log(AuthLogCreate(
                user_id=user_id,
                username_attempt=user.username,
                action="mfa_verify",
                status=LoginStatus.FAILURE,
                ip_address=ip_address,
                user_agent=user_agent,
                provider=AuthProvider.LOCAL,
                error_message="رمز المصادقة متعددة العوامل غير صحيح"
            ))

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="رمز المصادقة متعددة العوامل غير صحيح"
            )

        # تحديث حالة رمز MFA
        self.update_token(mfa_token.id, TokenUpdate(
            status=TokenStatus.USED,
            used_at=datetime.now(timezone.utc)
        ))

        # إنشاء رمز الوصول
        access_token_obj = self.create_token(TokenCreate(
            user_id=user_id,
            token_type=TokenType.ACCESS,
            metadata={"username": user.username}
        ))

        # إنشاء رمز التحديث
        refresh_token_obj = self.create_token(TokenCreate(
            user_id=user_id,
            token_type=TokenType.REFRESH,
            metadata={"username": user.username}
        ))

        # إنشاء جلسة المستخدم
        session = self.create_session(UserSessionCreate(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        ))

        # تسجيل محاولة التحقق
        self.create_auth_log(AuthLogCreate(
            user_id=user_id,
            username_attempt=user.username,
            action="mfa_verify",
            status=LoginStatus.SUCCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            provider=AuthProvider.LOCAL
        ))

        # حساب مدة صلاحية رمز الوصول بالثواني
        expires_in = int(
            (access_token_obj.expires_at -
             datetime.now(
                 timezone.utc)).total_seconds())

        return MFAVerifyResponse(
            access_token=access_token_obj.raw_token,
            token_type="bearer",
            expires_in=expires_in,
            refresh_token=refresh_token_obj.raw_token,
            user_id=user_id,
            session_id=session.id
        )

    def refresh_token(
            self,
            refresh_data: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        تحديث الرمز

        المعلمات:
            refresh_data (RefreshTokenRequest): بيانات التحديث

        العوائد:
            RefreshTokenResponse: استجابة التحديث

        يرفع:
            HTTPException: إذا فشل التحديث
        """
        # التحقق من رمز التحديث
        refresh_token = self.verify_token(
            refresh_data.refresh_token, TokenType.REFRESH)

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="رمز التحديث غير صالح أو منتهي الصلاحية"
            )

        # الحصول على المستخدم
        user_id = refresh_token.user_id
        user = self.user_service.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_FOUND
            )

        # التحقق من حالة المستخدم
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="الحساب غير نشط"
            )

        # تحديث حالة رمز التحديث
        self.update_token(refresh_token.id, TokenUpdate(
            status=TokenStatus.USED,
            used_at=datetime.now(timezone.utc)
        ))

        # إنشاء رمز الوصول الجديد
        access_token_obj = self.create_token(TokenCreate(
            user_id=user_id,
            token_type=TokenType.ACCESS,
            metadata={"username": user.username}
        ))

        # إنشاء رمز التحديث الجديد
        refresh_token_obj = self.create_token(TokenCreate(
            user_id=user_id,
            token_type=TokenType.REFRESH,
            metadata={"username": user.username}
        ))

        # حساب مدة صلاحية رمز الوصول بالثواني
        expires_in = int(
            (access_token_obj.expires_at -
             datetime.now(
                 timezone.utc)).total_seconds())

        return RefreshTokenResponse(
            access_token=access_token_obj.raw_token,
            token_type="bearer",
            expires_in=expires_in,
            refresh_token=refresh_token_obj.raw_token
        )

    def logout(self, user_id: str, logout_data: LogoutRequest,
               session_id: Optional[str] = None) -> LogoutResponse:
        """
        تسجيل الخروج

        المعلمات:
            user_id (str): معرف المستخدم
            logout_data (LogoutRequest): بيانات تسجيل الخروج
            session_id (Optional[str]): معرف الجلسة الحالية

        العوائد:
            LogoutResponse: استجابة تسجيل الخروج
        """
        if logout_data.all_sessions:
            # إلغاء جميع جلسات المستخدم
            revoked_count = self.revoke_user_sessions(user_id)

            # إلغاء جميع رموز المستخدم
            self.revoke_user_tokens(user_id)

            return LogoutResponse(
                message=f"تم تسجيل الخروج من {revoked_count} جلسة",
                success=True
            )
        else:
            # إلغاء الجلسة الحالية فقط
            if session_id:
                self.revoke_session(session_id)

            return LogoutResponse(
                message="تم تسجيل الخروج بنجاح",
                success=True
            )

    def request_password_reset(
            self,
            reset_data: PasswordResetRequest,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None) -> PasswordResetResponse:
        """
        طلب إعادة تعيين كلمة المرور

        المعلمات:
            reset_data (PasswordResetRequest): بيانات الطلب
            ip_address (Optional[str]): عنوان IP
            user_agent (Optional[str]): معلومات المتصفح

        العوائد:
            PasswordResetResponse: استجابة الطلب
        """
        user = self.user_service.get_user_by_email(reset_data.email)
        if not user:
            return PasswordResetResponse(
                success=False,
                message="البريد الإلكتروني غير مسجل"
            )

        # إنشاء رمز إعادة التعيين
        reset_token = self.create_token(TokenCreate(
            user_id=user.id,
            token_type=TokenType.PASSWORD_RESET,
            expires_in_seconds=self.config.password.password_reset_token_expire_minutes *
            60  # pylint: disable=no-member
        ))

        # تسجيل محاولة إعادة التعيين
        self.create_auth_log(AuthLogCreate(
            user_id=user.id,
            event_type="password_reset_request",
            ip_address=ip_address,
            user_agent=user_agent,
            status="success"
        ))

        return PasswordResetResponse(
            success=True,
            message="تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني",
            reset_token=reset_token.raw_token)

    def confirm_password_reset(
            self,
            confirm_data: PasswordResetConfirmRequest,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None) -> PasswordResetConfirmResponse:
        """
        تأكيد إعادة تعيين كلمة المرور

        المعلمات:
            confirm_data (PasswordResetConfirmRequest): بيانات تأكيد إعادة التعيين
            ip_address (Optional[str]): عنوان IP
            user_agent (Optional[str]): وكيل المستخدم

        العوائد:
            PasswordResetConfirmResponse: استجابة تأكيد إعادة التعيين

        يرفع:
            HTTPException: إذا فشل تأكيد إعادة التعيين
        """
        # التحقق من رمز إعادة تعيين كلمة المرور
        reset_token = self.verify_token(
            confirm_data.token, TokenType.PASSWORD_RESET)

        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="رمز إعادة تعيين كلمة المرور غير صالح أو منتهي الصلاحية"
            )

        # الحصول على المستخدم
        user_id = reset_token.user_id
        user = self.user_service.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_FOUND
            )

        # التحقق من تطابق كلمات المرور
        if confirm_data.new_password != confirm_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="كلمات المرور غير متطابقة"
            )

        # التحقق من قوة كلمة المرور
        if len(
                confirm_data.new_password) < self.config.password.min_length:  # pylint: disable=no-member
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"يجب أن تكون كلمة المرور {self.config.password.min_length} أحرف على الأقل"  # pylint: disable=no-member
            )

        if self.config.password.require_uppercase and not re.search(
                r'[A-Z]', confirm_data.new_password):  # pylint: disable=no-member
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل"
            )

        if self.config.password.require_lowercase and not re.search(
                r'[a-z]', confirm_data.new_password):  # pylint: disable=no-member
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل"
            )

        if self.config.password.require_digit and not re.search(
                r'\d', confirm_data.new_password):  # pylint: disable=no-member
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="يجب أن تحتوي كلمة المرور على رقم واحد على الأقل"
            )

        if self.config.password.require_special_char and not re.search(
                r'[!@#$%^&*(),.?":{}|<>]', confirm_data.new_password):  # pylint: disable=no-member
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="يجب أن تحتوي كلمة المرور على حرف خاص واحد على الأقل"
            )

        # تحديث كلمة المرور
        self.user_service.update_password(user_id, confirm_data.new_password)

        # تحديث حالة رمز إعادة تعيين كلمة المرور
        self.update_token(reset_token.id, TokenUpdate(
            status=TokenStatus.USED,
            used_at=datetime.now(timezone.utc)
        ))

        # إلغاء جميع جلسات المستخدم
        self.revoke_user_sessions(user_id)

        # إلغاء جميع رموز المستخدم
        self.revoke_user_tokens(user_id)

        # تسجيل محاولة تأكيد إعادة تعيين كلمة المرور
        self.create_auth_log(AuthLogCreate(
            user_id=user_id,
            action="password_reset_confirm",
            status=LoginStatus.SUCCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            provider=AuthProvider.LOCAL
        ))

        return PasswordResetConfirmResponse(
            message="تم إعادة تعيين كلمة المرور بنجاح",
            success=True
        )

    def verify_email(
            self,
            verify_data: EmailVerificationRequest) -> EmailVerificationResponse:
        """
        التحقق من البريد الإلكتروني

        المعلمات:
            verify_data (EmailVerificationRequest): بيانات التحقق

        العوائد:
            EmailVerificationResponse: استجابة التحقق

        يرفع:
            HTTPException: إذا فشل التحقق
        """
        # التحقق من رمز التحقق من البريد الإلكتروني
        verify_token = self.verify_token(
            verify_data.token, TokenType.EMAIL_VERIFICATION)

        if not verify_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="رمز التحقق من البريد الإلكتروني غير صالح أو منتهي الصلاحية")

        # الحصول على المستخدم
        user_id = verify_token.user_id
        user = self.user_service.get_user(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_FOUND
            )

        # تحديث حالة التحقق من البريد الإلكتروني
        self.user_service.update_user_email_verified(user_id, True)

        # تحديث حالة رمز التحقق من البريد الإلكتروني
        self.update_token(verify_token.id, TokenUpdate(
            status=TokenStatus.USED,
            used_at=datetime.now(timezone.utc)
        ))

        # تسجيل محاولة التحقق من البريد الإلكتروني
        self.create_auth_log(AuthLogCreate(
            user_id=user_id,
            action="email_verification",
            status=LoginStatus.SUCCESS,
            provider=AuthProvider.LOCAL
        ))

        return EmailVerificationResponse(
            message="تم التحقق من البريد الإلكتروني بنجاح",
            success=True
        )

    # ==================== وظائف مساعدة ====================

    def _hash_token(self, token: str) -> str:
        """
        حساب هاش الرمز

        المعلمات:
            token (str): الرمز

        العوائد:
            str: هاش الرمز
        """
        return hashlib.sha256(token.encode()).hexdigest()

    def create_jwt_token(
            self,
            user_id: str,
            expires_delta: Optional[timedelta] = None) -> str:
        # تحديد وقت انتهاء الصلاحية
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(
                timezone.utc) + timedelta(
                minutes=self.config.jwt.access_token_expire_minutes)  # pylint: disable=no-member

        # إنشاء البيانات
        to_encode = {"sub": user_id, "exp": expire}

        # الحصول على المفتاح السري
        secret_key = os.environ.get(
            self.config.jwt.secret_key_env_var,
            "")  # pylint: disable=no-member

        if not secret_key:
            # استخدام مفتاح افتراضي للتطوير
            secret_key = "development_secret_key"
            logger.warning(
                "استخدام مفتاح سري افتراضي للتطوير. يرجى تعيين متغير البيئة %s",
                self.config.jwt.secret_key_env_var)  # pylint: disable=no-member  # pylint: disable=no-member

        # تشفير الرمز
        encoded_jwt = jwt.encode(
            to_encode,
            secret_key,
            algorithm=self.config.jwt.algorithm)  # pylint: disable=no-member  # pylint: disable=no-member

        return encoded_jwt

    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        # الحصول على المفتاح السري
        secret_key = os.environ.get(
            self.config.jwt.secret_key_env_var,
            "")  # pylint: disable=no-member

        if not secret_key:
            # استخدام مفتاح افتراضي للتطوير
            secret_key = "development_secret_key"
            logger.warning(
                "استخدام مفتاح سري افتراضي للتطوير. يرجى تعيين متغير البيئة %s",
                self.config.jwt.secret_key_env_var)  # pylint: disable=no-member  # pylint: disable=no-member

        try:
            # فك تشفير الرمز
            payload = jwt.decode(
                token, secret_key, algorithms=[
                    self.config.jwt.algorithm])  # pylint: disable=no-member
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="انتهت صلاحية الرمز"
            )
        except jwt.JWTError:  # pylint: disable=no-member
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="رمز غير صالح"
            )

    def create_otp_secret(self) -> str:
        """إنشاء سر OTP جديد"""
        return pyotp.random_base32()

    def verify_otp(self, secret: str, token: str) -> bool:
        """التحقق من رمز OTP"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)

    def generate_otp(self, secret: str) -> str:
        """إنشاء رمز OTP"""
        totp = pyotp.TOTP(secret)
        return totp.now()

    def get_otp_uri(
            self,
            secret: str,
            username: str,
            issuer: str = "MyApp") -> str:
        """الحصول على رابط OTP"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(username, issuer_name=issuer)

    def _validate_password(self, password: str) -> bool:
        """التحقق من قوة كلمة المرور"""
        if len(password) < self.config.password.min_length:  # pylint: disable=no-member
            return False

        if not re.search(r"[A-Z]", password):
            return False

        if not re.search(r"[a-z]", password):
            return False

        if not re.search(r"\d", password):
            return False

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False

        return True

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        البحث عن مستخدم بواسطة اسم المستخدم

        المعلمات:
            username (str): اسم المستخدم

        العوائد:
            Optional[User]: كائن المستخدم إذا وجد، وإلا None
        """
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND
            )
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        البحث عن مستخدم بواسطة البريد الإلكتروني

        المعلمات:
            email (str): البريد الإلكتروني

        العوائد:
            Optional[User]: كائن المستخدم إذا وجد، وإلا None
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND
            )
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        البحث عن مستخدم بواسطة المعرف

        المعلمات:
            user_id (str): معرف المستخدم

        العوائد:
            Optional[User]: كائن المستخدم إذا وجد، وإلا None
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND
            )
        return user

    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """
        البحث عن مستخدم بواسطة رقم الهاتف

        المعلمات:
            phone (str): رقم الهاتف

        العوائد:
            Optional[User]: كائن المستخدم إذا وجد، وإلا None
        """
        user = self.db.query(User).filter(User.phone == phone).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND
            )
        return user

    def get_user_by_reset_token(self, token: str) -> Optional[User]:
        """
        البحث عن مستخدم بواسطة رمز إعادة تعيين كلمة المرور

        المعلمات:
            token (str): رمز إعادة تعيين كلمة المرور

        العوائد:
            Optional[User]: كائن المستخدم إذا وجد، وإلا None
        """
        user = self.db.query(User).filter(User.reset_token == token).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND
            )
        return user

    def validate_phone_number(self, phone: str) -> bool:
        """
        التحقق من صحة رقم الهاتف

        المعلمات:
            phone (str): رقم الهاتف

        العوائد:
            bool: True إذا كان الرقم صحيحاً، وإلا False
        """
        # التحقق من تنسيق رقم الهاتف
        if not re.match(r'^\+?[1-9]\d{1,14}$', phone):
            return False
        return True


# تصدير الدوال والكائنات
__all__ = ['AuthenticationService']
