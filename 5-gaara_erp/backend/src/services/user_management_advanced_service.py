#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/user_management_advanced_service.py

خدمة إدارة المستخدمين والمجموعات المتقدمة
Advanced User and Group Management Service

يوفر هذا الملف خدمات شاملة لإدارة المستخدمين والمجموعات والصلاحيات
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.exc import IntegrityError
import secrets
import string

# استيراد النماذج
from models.user_management_advanced import (
    UserGroup,
    UserGroupMembership,
    UserSession,
    UserActivity,
    UserPreferences,
    UserNotification,
    UserSecuritySettings,
    PasswordHistory,
    TwoFactorAuth,
    UserRole,
    RolePermission,
    UserAuditLog,
    UserProfile,
    UserDepartment,
    UserBranch,
)
from models.user import User
from models.advanced_permissions import Permission
from ..database import db

# إعداد السجلات
logger = logging.getLogger(__name__)


class UserManagementAdvancedService:
    """خدمة إدارة المستخدمين والمجموعات المتقدمة"""

    def __init__(self):
        """تهيئة الخدمة"""
        self.logger = logger

    # ==================== إدارة المجموعات ====================

    def create_user_group(
        self, group_data: Dict[str, Any], created_by: int
    ) -> Dict[str, Any]:
        """
        إنشاء مجموعة مستخدمين جديدة

        Args:
            group_data: بيانات المجموعة
            created_by: معرف المستخدم المنشئ

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من عدم وجود مجموعة بنفس الاسم
            existing_group = UserGroup.query.filter_by(
                name=group_data.get("name")
            ).first()

            if existing_group:
                return {"success": False, "message": "مجموعة بهذا الاسم موجودة بالفعل"}

            # إنشاء المجموعة الجديدة
            new_group = UserGroup(
                name=group_data.get("name"),
                description=group_data.get("description", ""),
                group_type=group_data.get("group_type", "custom"),
                is_active=group_data.get("is_active", True),
                permissions=group_data.get("permissions", {}),
                settings=group_data.get("settings", {}),
                created_by=created_by,
            )

            db.session.add(new_group)
            db.session.commit()

            # تسجيل النشاط
            self._log_user_activity(
                user_id=created_by,
                action="create_user_group",
                details=f"تم إنشاء مجموعة: {new_group.name}",
                resource_type="user_group",
                resource_id=new_group.id,
            )

            return {
                "success": True,
                "message": "تم إنشاء المجموعة بنجاح",
                "group_id": new_group.id,
                "group": self._serialize_user_group(new_group),
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في إنشاء مجموعة المستخدمين: {str(e)}")
            return {"success": False, "message": f"خطأ في إنشاء المجموعة: {str(e)}"}

    def get_user_groups(
        self, filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        الحصول على قائمة مجموعات المستخدمين

        Args:
            filters: مرشحات البحث
            page: رقم الصفحة
            per_page: عدد العناصر في الصفحة

        Returns:
            Dict: قائمة المجموعات
        """
        try:
            query = UserGroup.query

            # تطبيق المرشحات
            if filters:
                if filters.get("name"):
                    query = query.filter(UserGroup.name.ilike(f"%{filters['name']}%"))

                if filters.get("group_type"):
                    query = query.filter(UserGroup.group_type == filters["group_type"])

                if filters.get("is_active") is not None:
                    query = query.filter(UserGroup.is_active == filters["is_active"])

            # ترتيب النتائج
            query = query.order_by(UserGroup.created_at.desc())

            # تطبيق التصفح
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            groups = [self._serialize_user_group(group) for group in pagination.items]

            return {
                "success": True,
                "groups": groups,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                },
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على مجموعات المستخدمين: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على المجموعات: {str(e)}",
            }

    def add_user_to_group(
        self, user_id: int, group_id: int, added_by: int, role: str = "member"
    ) -> Dict[str, Any]:
        """
        إضافة مستخدم إلى مجموعة

        Args:
            user_id: معرف المستخدم
            group_id: معرف المجموعة
            added_by: معرف المستخدم المضيف
            role: دور المستخدم في المجموعة

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من وجود المستخدم والمجموعة
            user = User.query.get(user_id)
            group = UserGroup.query.get(group_id)

            if not user:
                return {"success": False, "message": "المستخدم غير موجود"}

            if not group:
                return {"success": False, "message": "المجموعة غير موجودة"}

            # التحقق من عدم وجود عضوية سابقة
            existing_membership = UserGroupMembership.query.filter_by(
                user_id=user_id, group_id=group_id
            ).first()

            if existing_membership:
                return {"success": False, "message": "المستخدم عضو في المجموعة بالفعل"}

            # إنشاء العضوية الجديدة
            membership = UserGroupMembership(
                user_id=user_id, group_id=group_id, role=role, added_by=added_by
            )

            db.session.add(membership)
            db.session.commit()

            # تسجيل النشاط
            self._log_user_activity(
                user_id=added_by,
                action="add_user_to_group",
                details=f"تم إضافة المستخدم {user.username} إلى مجموعة {group.name}",
                resource_type="user_group_membership",
                resource_id=membership.id,
            )

            return {
                "success": True,
                "message": "تم إضافة المستخدم إلى المجموعة بنجاح",
                "membership_id": membership.id,
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في إضافة المستخدم إلى المجموعة: {str(e)}")
            return {"success": False, "message": f"خطأ في إضافة المستخدم: {str(e)}"}

    # ==================== إدارة المستخدمين ====================

    def create_user_advanced(
        self, user_data: Dict[str, Any], created_by: int
    ) -> Dict[str, Any]:
        """
        إنشاء مستخدم جديد مع إعدادات متقدمة

        Args:
            user_data: بيانات المستخدم
            created_by: معرف المستخدم المنشئ

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من عدم وجود مستخدم بنفس البيانات
            existing_user = User.query.filter(
                or_(
                    User.username == user_data.get("username"),
                    User.email == user_data.get("email"),
                )
            ).first()

            if existing_user:
                return {
                    "success": False,
                    "message": "مستخدم بهذا الاسم أو البريد الإلكتروني موجود بالفعل",
                }

            # إنشاء كلمة مرور عشوائية إذا لم تُحدد
            password = user_data.get("password")
            if not password:
                password = self._generate_random_password()

            # إنشاء المستخدم الجديد
            new_user = User(
                username=user_data.get("username"),
                email=user_data.get("email"),
                password_hash=generate_password_hash(password),
                first_name=user_data.get("first_name", ""),
                last_name=user_data.get("last_name", ""),
                phone=user_data.get("phone", ""),
                is_active=user_data.get("is_active", True),
                created_by=created_by,
            )

            db.session.add(new_user)
            db.session.flush()  # للحصول على معرف المستخدم

            # إنشاء ملف المستخدم
            user_profile = UserProfile(
                user_id=new_user.id,
                department_id=user_data.get("department_id"),
                branch_id=user_data.get("branch_id"),
                position=user_data.get("position", ""),
                hire_date=user_data.get("hire_date"),
                employee_id=user_data.get("employee_id", ""),
                manager_id=user_data.get("manager_id"),
                bio=user_data.get("bio", ""),
                avatar_url=user_data.get("avatar_url", ""),
                social_links=user_data.get("social_links", {}),
                emergency_contact=user_data.get("emergency_contact", {}),
                skills=user_data.get("skills", []),
                certifications=user_data.get("certifications", []),
            )

            db.session.add(user_profile)

            # إنشاء إعدادات المستخدم
            user_preferences = UserPreferences(
                user_id=new_user.id,
                language=user_data.get("language", "ar"),
                timezone=user_data.get("timezone", "Asia/Riyadh"),
                theme=user_data.get("theme", "light"),
                notifications_enabled=user_data.get("notifications_enabled", True),
                email_notifications=user_data.get("email_notifications", True),
                sms_notifications=user_data.get("sms_notifications", False),
                dashboard_layout=user_data.get("dashboard_layout", {}),
                display_settings=user_data.get("display_settings", {}),
            )

            db.session.add(user_preferences)

            # إنشاء إعدادات الأمان
            security_settings = UserSecuritySettings(
                user_id=new_user.id,
                password_expiry_days=user_data.get("password_expiry_days", 90),
                require_password_change=user_data.get("require_password_change", True),
                two_factor_enabled=user_data.get("two_factor_enabled", False),
                login_attempts_limit=user_data.get("login_attempts_limit", 5),
                session_timeout_minutes=user_data.get("session_timeout_minutes", 60),
                ip_whitelist=user_data.get("ip_whitelist", []),
                allowed_login_hours=user_data.get("allowed_login_hours", {}),
                security_questions=user_data.get("security_questions", []),
            )

            db.session.add(security_settings)

            # إضافة المستخدم إلى المجموعات المحددة
            if user_data.get("group_ids"):
                for group_id in user_data["group_ids"]:
                    membership = UserGroupMembership(
                        user_id=new_user.id,
                        group_id=group_id,
                        role="member",
                        added_by=created_by,
                    )
                    db.session.add(membership)

            # إضافة الأدوار المحددة
            if user_data.get("role_ids"):
                for role_id in user_data["role_ids"]:
                    new_user.roles.append(UserRole.query.get(role_id))

            db.session.commit()

            # تسجيل النشاط
            self._log_user_activity(
                user_id=created_by,
                action="create_user",
                details=f"تم إنشاء مستخدم جديد: {new_user.username}",
                resource_type="user",
                resource_id=new_user.id,
            )

            return {
                "success": True,
                "message": "تم إنشاء المستخدم بنجاح",
                "user_id": new_user.id,
                "username": new_user.username,
                "temporary_password": (
                    password if not user_data.get("password") else None
                ),
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في إنشاء المستخدم: {str(e)}")
            return {"success": False, "message": f"خطأ في إنشاء المستخدم: {str(e)}"}

    def get_users_advanced(
        self, filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        الحصول على قائمة المستخدمين مع معلومات متقدمة

        Args:
            filters: مرشحات البحث
            page: رقم الصفحة
            per_page: عدد العناصر في الصفحة

        Returns:
            Dict: قائمة المستخدمين
        """
        try:
            query = db.session.query(User).join(UserProfile, isouter=True)

            # تطبيق المرشحات
            if filters:
                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            User.username.ilike(search_term),
                            User.email.ilike(search_term),
                            User.first_name.ilike(search_term),
                            User.last_name.ilike(search_term),
                        )
                    )

                if filters.get("is_active") is not None:
                    query = query.filter(User.is_active == filters["is_active"])

                if filters.get("department_id"):
                    query = query.filter(
                        UserProfile.department_id == filters["department_id"]
                    )

                if filters.get("branch_id"):
                    query = query.filter(UserProfile.branch_id == filters["branch_id"])

                if filters.get("group_id"):
                    query = query.join(UserGroupMembership).filter(
                        UserGroupMembership.group_id == filters["group_id"]
                    )

            # ترتيب النتائج
            sort_by = filters.get("sort_by", "created_at") if filters else "created_at"
            sort_order = filters.get("sort_order", "desc") if filters else "desc"

            if hasattr(User, sort_by):
                if sort_order == "asc":
                    query = query.order_by(asc(getattr(User, sort_by)))
                else:
                    query = query.order_by(desc(getattr(User, sort_by)))

            # تطبيق التصفح
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            users = [self._serialize_user_advanced(user) for user in pagination.items]

            return {
                "success": True,
                "users": users,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                },
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على المستخدمين: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على المستخدمين: {str(e)}",
            }

    # ==================== إدارة الجلسات ====================

    def create_user_session(
        self, user_id: int, session_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        إنشاء جلسة مستخدم جديدة

        Args:
            user_id: معرف المستخدم
            session_data: بيانات الجلسة

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # إنهاء الجلسات القديمة إذا لزم الأمر
            if session_data.get("end_other_sessions", False):
                UserSession.query.filter_by(user_id=user_id, is_active=True).update(
                    {"is_active": False, "ended_at": datetime.utcnow()}
                )

            # إنشاء الجلسة الجديدة
            session = UserSession(
                user_id=user_id,
                session_token=secrets.token_urlsafe(32),
                ip_address=session_data.get("ip_address", ""),
                user_agent=session_data.get("user_agent", ""),
                device_info=session_data.get("device_info", {}),
                location_info=session_data.get("location_info", {}),
                expires_at=datetime.utcnow()
                + timedelta(minutes=session_data.get("timeout_minutes", 60)),
            )

            db.session.add(session)
            db.session.commit()

            # تسجيل النشاط
            self._log_user_activity(
                user_id=user_id,
                action="login",
                details=f"تسجيل دخول من {session_data.get('ip_address', 'غير معروف')}",
                resource_type="user_session",
                resource_id=session.id,
            )

            return {
                "success": True,
                "session_token": session.session_token,
                "expires_at": session.expires_at.isoformat(),
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في إنشاء جلسة المستخدم: {str(e)}")
            return {"success": False, "message": f"خطأ في إنشاء الجلسة: {str(e)}"}

    # ==================== الدوال المساعدة ====================

    def _serialize_user_group(self, group: UserGroup) -> Dict[str, Any]:
        """تحويل مجموعة المستخدمين إلى قاموس"""
        return {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "group_type": group.group_type,
            "is_active": group.is_active,
            "permissions": group.permissions,
            "settings": group.settings,
            "member_count": len(group.memberships),
            "created_at": group.created_at.isoformat() if group.created_at else None,
            "updated_at": group.updated_at.isoformat() if group.updated_at else None,
        }

    def _serialize_user_advanced(self, user: User) -> Dict[str, Any]:
        """تحويل المستخدم إلى قاموس مع معلومات متقدمة"""
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        }

        # إضافة معلومات الملف الشخصي
        if hasattr(user, "profile") and user.profile:
            user_dict["profile"] = {
                "position": user.profile.position,
                "department_id": user.profile.department_id,
                "branch_id": user.profile.branch_id,
                "hire_date": (
                    user.profile.hire_date.isoformat()
                    if user.profile.hire_date
                    else None
                ),
                "employee_id": user.profile.employee_id,
                "avatar_url": user.profile.avatar_url,
            }

        # إضافة معلومات المجموعات
        if hasattr(user, "group_memberships"):
            user_dict["groups"] = [
                {
                    "id": membership.group.id,
                    "name": membership.group.name,
                    "role": membership.role,
                }
                for membership in user.group_memberships
                if membership.group.is_active
            ]

        return user_dict

    def _generate_random_password(self, length: int = 12) -> str:
        """توليد كلمة مرور عشوائية"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(secrets.choice(characters) for _ in range(length))

    def _log_user_activity(
        self,
        user_id: int,
        action: str,
        details: str,
        resource_type: str = None,
        resource_id: int = None,
    ):
        """تسجيل نشاط المستخدم"""
        try:
            activity = UserActivity(
                user_id=user_id,
                action=action,
                details=details,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address="",  # يمكن الحصول عليه من الطلب
                user_agent="",  # يمكن الحصول عليه من الطلب
            )
            db.session.add(activity)
            db.session.commit()
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل نشاط المستخدم: {str(e)}")

    # ==================== إدارة الصلاحيات ====================

    def assign_role_to_user(
        self, user_id: int, role_id: int, assigned_by: int
    ) -> Dict[str, Any]:
        """
        تعيين دور للمستخدم

        Args:
            user_id: معرف المستخدم
            role_id: معرف الدور
            assigned_by: معرف المستخدم المعين

        Returns:
            Dict: نتيجة العملية
        """
        try:
            user = User.query.get(user_id)
            role = UserRole.query.get(role_id)

            if not user:
                return {"success": False, "message": "المستخدم غير موجود"}

            if not role:
                return {"success": False, "message": "الدور غير موجود"}

            # التحقق من عدم وجود الدور مسبقاً
            if role in user.roles:
                return {"success": False, "message": "المستخدم لديه هذا الدور بالفعل"}

            user.roles.append(role)
            db.session.commit()

            # تسجيل النشاط
            self._log_user_activity(
                user_id=assigned_by,
                action="assign_role",
                details=f"تم تعيين دور {role.name} للمستخدم {user.username}",
                resource_type="user_role",
                resource_id=role.id,
            )

            return {"success": True, "message": "تم تعيين الدور بنجاح"}

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في تعيين الدور: {str(e)}")
            return {"success": False, "message": f"خطأ في تعيين الدور: {str(e)}"}

    def get_user_permissions(self, user_id: int) -> Dict[str, Any]:
        """
        الحصول على صلاحيات المستخدم

        Args:
            user_id: معرف المستخدم

        Returns:
            Dict: صلاحيات المستخدم
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "المستخدم غير موجود"}

            permissions = set()

            # صلاحيات من الأدوار
            for role in user.roles:
                for permission in role.permissions:
                    permissions.add(permission.name)

            # صلاحيات من المجموعات
            for membership in user.group_memberships:
                if membership.group.is_active:
                    group_permissions = membership.group.permissions or {}
                    permissions.update(group_permissions.keys())

            return {"success": True, "permissions": list(permissions)}

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على صلاحيات المستخدم: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على الصلاحيات: {str(e)}",
            }


# إنشاء مثيل الخدمة
user_management_service = UserManagementAdvancedService()
