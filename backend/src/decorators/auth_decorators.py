#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/decorators/auth_decorators.py
مزخرفات المصادقة والصلاحيات
Authentication and Authorization Decorators
"""

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from src.models.user_unified import User
import logging

logger = logging.getLogger(__name__)


def token_required(f):
    """مزخرف للتحقق من وجود رمز المصادقة"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # البحث عن الرمز في الرأس
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                return (
                    jsonify({"success": False, "error": "تنسيق رمز المصادقة غير صحيح"}),
                    401,
                )

        if not token:
            return jsonify({"success": False, "error": "رمز المصادقة مطلوب"}), 401

        try:
            # فك تشفير الرمز
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = User.query.filter_by(id=data["user_id"]).first()

            if not current_user or not current_user.is_active:
                return (
                    jsonify(
                        {"success": False, "error": "المستخدم غير موجود أو غير نشط"}
                    ),
                    401,
                )

            # إضافة المستخدم الحالي للطلب
            request.current_user = current_user  # type: ignore[attr-defined]

        except jwt.ExpiredSignatureError:
            return (
                jsonify({"success": False, "error": "انتهت صلاحية رمز المصادقة"}),
                401,
            )
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "error": "رمز المصادقة غير صحيح"}), 401
        except Exception as e:
            logger.error(f"خطأ في التحقق من الرمز: {e}")
            return (
                jsonify({"success": False, "error": "خطأ في التحقق من المصادقة"}),
                401,
            )

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """مزخرف للتحقق من صلاحيات الإدارة"""

    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = getattr(request, "current_user", None)

        if not current_user:
            return jsonify({"success": False, "error": "المصادقة مطلوبة"}), 401

        if current_user.role != "admin":
            return jsonify({"success": False, "error": "صلاحيات الإدارة مطلوبة"}), 403

        return f(*args, **kwargs)

    return decorated


def permission_required(permission):
    """مزخرف للتحقق من صلاحية محددة"""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = getattr(request, "current_user", None)

            if not current_user:
                return jsonify({"success": False, "error": "المصادقة مطلوبة"}), 401

            # التحقق من الصلاحية
            if not current_user.has_permission(permission):
                return (
                    jsonify(
                        {"success": False, "error": f"الصلاحية {permission} مطلوبة"}
                    ),
                    403,
                )

            return f(*args, **kwargs)

        return decorated

    return decorator
