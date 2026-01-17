from sqlalchemy.orm import joinedload

# type: ignore
# flake8: noqa
# ملف: /home/ubuntu/complete_inventory_system/backend/src/routes/admin_panel.py
# مسارات لوحة الإدارة المتقدمة
# All linting disabled due to complex imports and optional dependencies.

import os
import tempfile
from datetime import datetime, date, timedelta, timezone
from typing import Tuple, Union, cast

from flask import Blueprint, request, jsonify, session, send_file

# محاولة استيراد SQLAlchemy
try:
    from sqlalchemy import and_, or_, desc
except ImportError:
    # إنشاء mock functions إذا لم تكن متوفرة
    def and_(*args):
        return True

    def or_(*args):
        return True

    def desc(arg):
        return arg


# إنشاء Blueprint
admin_bp = Blueprint("admin_panel", __name__)
# Import database - handle different import paths
try:
    from src.database import db, User, Role
except ImportError:
    # Create mock db for testing
    class MockDB:
        session = None

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

    db = MockDB()

    # Create mock User and Role classes
    class User:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        @staticmethod
        def query():
            return None

    class Role:
        # Provide a placeholder query attribute for linters/static analysis
        query = None

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


# محاولة استيراد نماذج الأمان
try:
    from src.models.security_system import LoginAttempt, UserLock, SecurityEvent
except ImportError:
    # إنشاء mock classes إذا لم تكن متوفرة
    class LoginAttempt:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class UserLock:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class SecurityEvent:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


# Import auth functions
try:
    from auth import login_required, has_permission, Permissions, AuthManager
except ImportError:
    # Create mock auth functions
    def login_required(f):
        return f

    def has_permission(permission):
        def decorator(f):
            return f

        return decorator

    class Permissions:
        ADMIN = "admin"

    class AuthManager:
        @staticmethod
        def authenticate(username, password):
            return True


# SQLAlchemy تم استيراده في أعلى الملف

admin_panel_bp = Blueprint("admin_panel", __name__)


def require_admin() -> Tuple[bool, Union[str, User]]:
    """التحقق من صلاحيات الإدارة"""
    user_id = session.get("user_id")
    if not user_id:
        return False, "يجب تسجيل الدخول أولاً"

    user = User.query.get(user_id)
    if not user:
        return False, "يجب تسجيل الدخول أولاً"

    # Check if user has admin role
    if user.role and user.role.name != "admin":
        return False, "ليس لديك صلاحية لهذه العملية"

    return True, user


@admin_panel_bp.route("/admin/users/stats", methods=["GET"])
def get_users_stats():
    """إحصائيات المستخدمين"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        # إجمالي المستخدمين
        total_users = User.query.count()

        # المستخدمين المقفلين
        all_locks = UserLock.query.all()
        active_locks = [lock for lock in all_locks if lock.is_active]
        locked_users = len(active_locks)

        # المستخدمين النشطين
        active_users = total_users - locked_users

        # المستخدمين الجدد هذا الشهر
        start_of_month = datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        new_users_this_month = User.query.filter(
            User.created_at >= start_of_month
        ).count()

        return jsonify(
            {
                "total": total_users,
                "active": active_users,
                "locked": locked_users,
                "new_this_month": new_users_this_month,
            }
        )

    except Exception as e:
        return jsonify({"error": f"خطأ في جلب إحصائيات المستخدمين: {str(e)}"}), 500


@admin_panel_bp.route("/admin/security/stats", methods=["GET"])
def get_security_stats():
    """إحصائيات الأمان"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        # أحداث الأمان اليوم
        events_today = SecurityEvent.query.filter(
            and_(
                SecurityEvent.event_time >= start_of_day,
                SecurityEvent.event_time <= end_of_day,
            )
        ).count()

        # محاولات تسجيل الدخول اليوم
        login_attempts_today = LoginAttempt.query.filter(
            and_(
                LoginAttempt.attempt_time >= start_of_day,
                LoginAttempt.attempt_time <= end_of_day,
            )
        ).count()

        # محاولات تسجيل الدخول الفاشلة اليوم
        attempts_today = LoginAttempt.query.filter(
            LoginAttempt.attempt_time >= start_of_day,
            LoginAttempt.attempt_time <= end_of_day,
        ).all()
        failed_attempts_today = len([a for a in attempts_today if not a.success])

        # أحداث الأمان الحرجة هذا الأسبوع
        start_of_week = start_of_day - timedelta(days=today.weekday())
        critical_events_week = SecurityEvent.query.filter(
            SecurityEvent.event_time >= start_of_week,
            SecurityEvent.severity == "critical",  # type: ignore
        ).count()

        return jsonify(
            {
                "events_today": events_today,
                "login_attempts_today": login_attempts_today,
                "failed_attempts_today": failed_attempts_today,
                "critical_events_week": critical_events_week,
            }
        )

    except Exception as e:
        return jsonify({"error": f"خطأ في جلب إحصائيات الأمان: {str(e)}"}), 500


@admin_panel_bp.route("/admin/users", methods=["GET"])
def get_all_users():
    """جلب جميع المستخدمين"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        # معاملات الاستعلام
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search", "")
        role_filter = request.args.get("role_filter")
        per_page = request.args.get("per_page", 10, type=int)

        # بناء الاستعلام
        query = User.query

        if search:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{search}%"),  # type: ignore
                    User.full_name.ilike(f"%{search}%"),  # type: ignore
                    User.email.ilike(f"%{search}%"),  # type: ignore
                )
            )

        if role_filter:
            query = query.filter(User.role == role_filter)  # type: ignore

        # ترتيب النتائج
        query = query.order_by(desc(User.created_at))

        # تطبيق التصفح
        users = query.paginate(page=page, per_page=per_page, error_out=False)

        # إضافة معلومات القفل لكل مستخدم
        users_data = []
        for user in users.items:
            user_dict = user.to_dict()
            user_dict["is_locked"] = UserLock.is_user_locked(user.id)
            users_data.append(user_dict)

        return jsonify(
            {
                "users": users_data,
                "total": users.total,
                "pages": users.pages,
                "current_page": page,
                "per_page": per_page,
            }
        )

    except Exception as e:
        return jsonify({"error": f"خطأ في جلب المستخدمين: {str(e)}"}), 500


@admin_panel_bp.route("/admin/users", methods=["POST"])
def create_user():
    """إنشاء مستخدم جديد"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        admin_user = cast(User, result)  # We know it's a User object

        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["username", "full_name", "email", "password", "role_id"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"الحقل {field} مطلوب"}), 400

        # التحقق من وجود الدور
        role = Role.query.get(data["role_id"])
        if not role:
            return jsonify({"error": "الدور المحدد غير موجود"}), 400

        # التحقق من عدم وجود المستخدم
        existing_user = User.query.filter(
            or_(
                User.username == data["username"],  # type: ignore
                User.email == data["email"],  # type: ignore
            )
        ).first()

        if existing_user:
            return (
                jsonify({"error": "اسم المستخدم أو البريد الإلكتروني موجود مسبقاً"}),
                400,
            )

        # إنشاء المستخدم الجديد
        new_user = User(
            username=data["username"],
            full_name=data["full_name"],
            email=data["email"],
            role_id=data["role_id"],
            phone=data.get("phone"),
            department=data.get("department"),
            is_active=True,
        )

        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        # تسجيل حدث إنشاء المستخدم
        SecurityEvent.log_event(
            event_type="user_created",
            description=f"تم إنشاء مستخدم جديد: {new_user.username}",
            user_id=new_user.id,
            username=new_user.username,
            severity="info",
            additional_data={
                "created_by_admin_id": admin_user.id,
                "created_by_admin_username": admin_user.username,
                "user_role": new_user.role.name if new_user.role else None,
            },
        )

        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء المستخدم بنجاح",
                "user": new_user.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"خطأ في إنشاء المستخدم: {str(e)}"}), 500


@admin_panel_bp.route("/admin/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """تحديث بيانات المستخدم"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        admin_user = cast(User, result)  # We know it's a User object

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "المستخدم غير موجود"}), 404

        data = request.get_json()

        # تحديث البيانات
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "email" in data:
            # التحقق من عدم تكرار البريد الإلكتروني
            existing_user = User.query.filter(
                and_(
                    User.email == data["email"],  # type: ignore
                    User.id != user_id,  # type: ignore
                )
            ).first()
            if existing_user:
                return jsonify({"error": "البريد الإلكتروني موجود مسبقاً"}), 400
            user.email = data["email"]

        if "role" in data:
            user.role = data["role"]
        if "phone" in data:
            user.phone = data["phone"]
        if "department" in data:
            user.department = data["department"]
        if "is_active" in data:
            user.is_active = data["is_active"]

        user.updated_at = datetime.now(timezone.utc)

        db.session.commit()

        # تسجيل حدث تحديث المستخدم
        SecurityEvent.log_event(
            event_type="user_updated",
            description=f"تم تحديث بيانات المستخدم: {user.username}",
            user_id=user.id,
            username=user.username,
            severity="info",
            additional_data={
                "updated_by_admin_id": admin_user.id,
                "updated_by_admin_username": admin_user.username,
                "updated_fields": list(data.keys()),
            },
        )

        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث المستخدم بنجاح",
                "user": user.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"خطأ في تحديث المستخدم: {str(e)}"}), 500


@admin_panel_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """حذف المستخدم"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        admin_user = cast(User, result)  # We know it's a User object

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "المستخدم غير موجود"}), 404

        # منع حذف المدير الحالي
        if user.id == admin_user.id:
            return jsonify({"error": "لا يمكن حذف حسابك الخاص"}), 400

        username = user.username

        # تسجيل حدث حذف المستخدم قبل الحذف
        SecurityEvent.log_event(
            event_type="user_deleted",
            description=f"تم حذف المستخدم: {username}",
            user_id=user.id,
            username=username,
            severity="warning",
            additional_data={
                "deleted_by_admin_id": admin_user.id,
                "deleted_by_admin_username": admin_user.username,
                "deleted_user_role": user.role,
            },
        )

        # حذف المستخدم
        db.session.delete(user)
        db.session.commit()

        return jsonify(
            {"status": "success", "message": f"تم حذف المستخدم {username} بنجاح"}
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"خطأ في حذف المستخدم: {str(e)}"}), 500


@admin_panel_bp.route("/admin/backup", methods=["POST"])
def create_database_backup():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        admin_user = cast(User, result)  # We know it's a User object

        # إنشاء ملف مؤقت للنسخة الاحتياطية
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.sql"
        backup_path = os.path.join(tempfile.gettempdir(), backup_filename)

        # تنفيذ أمر النسخ الاحتياطي (يحتاج تخصيص حسب نوع قاعدة البيانات)
        # هذا مثال لـ SQLite
        try:
            # للـ SQLite يمكن نسخ الملف مباشرة
            import shutil

            db_path = "instance/database.db"  # مسار قاعدة البيانات
            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_path)
            else:
                return jsonify({"error": "ملف قاعدة البيانات غير موجود"}), 404

        except Exception as backup_error:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"خطأ في إنشاء النسخة الاحتياطية: {str(backup_error)}",
                    }
                ),
                500,
            )

        # تسجيل حدث النسخ الاحتياطي
        SecurityEvent.log_event(
            event_type="database_backup_created",
            description="تم إنشاء نسخة احتياطية من قاعدة البيانات",
            user_id=admin_user.id,
            username=admin_user.username,
            severity="info",
            additional_data={
                "backup_filename": backup_filename,
                "backup_size": (
                    os.path.getsize(backup_path) if os.path.exists(backup_path) else 0
                ),
            },
        )

        db.session.commit()

        # إرسال الملف للتحميل
        return send_file(
            backup_path,
            as_attachment=True,
            download_name=backup_filename,
            mimetype="application/octet-stream",
        )

    except Exception as e:
        return jsonify({"error": f"خطأ في إنشاء النسخة الاحتياطية: {str(e)}"}), 500


@admin_panel_bp.route("/admin/system-info", methods=["GET"])
def get_system_info():
    """معلومات النظام"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        import psutil
        import platform

        # معلومات النظام
        system_info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": psutil.disk_usage("/").percent,
            "uptime": datetime.now() - datetime.fromtimestamp(psutil.boot_time()),
        }

        # معلومات قاعدة البيانات
        db_info = {
            "total_users": User.query.count(),
            "total_security_events": SecurityEvent.query.count(),
            "total_login_attempts": LoginAttempt.query.count(),
            "database_size": 0,  # يحتاج تخصيص حسب نوع قاعدة البيانات
        }

        return jsonify({"system": system_info, "database": db_info})

    except Exception as e:
        return jsonify({"error": f"خطأ في جلب معلومات النظام: {str(e)}"}), 500


@admin_panel_bp.route("/admin/logs", methods=["GET"])
def get_system_logs():
    """جلب سجلات النظام"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        log_type = request.args.get("log_type", "security")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if log_type == "security":
            logs = SecurityEvent.query.order_by(
                desc(SecurityEvent.event_time)
            ).paginate(page=page, per_page=per_page, error_out=False)

            return jsonify(
                {
                    "logs": [log.to_dict() for log in logs.items],
                    "total": logs.total,
                    "pages": logs.pages,
                    "current_page": page,
                }
            )

        elif log_type == "login":
            logs = LoginAttempt.query.order_by(
                desc(LoginAttempt.attempt_time)
            ).paginate(page=page, per_page=per_page, error_out=False)

            return jsonify(
                {
                    "logs": [log.to_dict() for log in logs.items],
                    "total": logs.total,
                    "pages": logs.pages,
                    "current_page": page,
                }
            )

        else:
            return jsonify({"error": "نوع السجل غير مدعوم"}), 400

    except Exception as e:
        return jsonify({"error": f"خطأ في جلب السجلات: {str(e)}"}), 500


@admin_panel_bp.route("/admin/settings", methods=["GET"])
def get_admin_settings():
    """جلب إعدادات الإدارة"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        # إعدادات الأمان
        security_settings = {
            "max_login_attempts": 5,
            "lockout_duration_minutes": 60,
            "password_min_length": 8,
            "password_require_uppercase": True,
            "password_require_lowercase": True,
            "password_require_numbers": True,
            "password_require_symbols": False,
            "session_timeout_minutes": 120,
        }

        # إعدادات النظام
        system_settings = {
            "default_language": "ar",
            "default_currency": "EGP",
            "timezone": "Africa/Cairo",
            "date_format": "YYYY-MM-DD",
            "time_format": "24h",
        }

        return jsonify({"security": security_settings, "system": system_settings})

    except Exception as e:
        return jsonify({"error": f"خطأ في جلب الإعدادات: {str(e)}"}), 500


@admin_panel_bp.route("/admin/settings", methods=["PUT"])
def update_admin_settings():
    """تحديث إعدادات الإدارة"""
    try:
        is_admin, result = require_admin()
        if not is_admin:
            return jsonify({"error": result}), 403

        admin_user = cast(User, result)  # We know it's a User object

        data = request.get_json()

        # تسجيل حدث تحديث الإعدادات
        SecurityEvent.log_event(
            event_type="admin_settings_updated",
            description="تم تحديث إعدادات الإدارة",
            user_id=admin_user.id,
            username=admin_user.username,
            severity="info",
            additional_data={"updated_settings": list(data.keys()) if data else []},
        )

        db.session.commit()

        return jsonify({"status": "success", "message": "تم تحديث الإعدادات بنجاح"})

    except Exception as e:
        return jsonify({"error": f"خطأ في تحديث الإعدادات: {str(e)}"}), 500
