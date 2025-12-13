#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/users.py
مسارات إدارة المستخدمين
Users Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.user import User
from src.decorators.auth_decorators import token_required, admin_required
from werkzeug.security import generate_password_hash
import logging

logger = logging.getLogger(__name__)

users_bp = Blueprint("users", __name__)


@users_bp.route("/api/users", methods=["GET"])
@token_required
@admin_required
def get_users():
    """الحصول على قائمة المستخدمين"""
    try:
        users = User.query.all()
        return jsonify(
            {
                "success": True,
                "data": [user.to_dict() for user in users],
                "total": len(users),
            }
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدمين: {e}")
        return jsonify({"success": False, "error": "فشل في الحصول على المستخدمين"}), 500


@users_bp.route("/api/users", methods=["POST"])
@token_required
@admin_required
def create_user():
    """إنشاء مستخدم جديد"""
    try:
        data = request.get_json()

        if not data or not data.get("username") or not data.get("password"):
            return (
                jsonify(
                    {"success": False, "error": "اسم المستخدم وكلمة المرور مطلوبان"}
                ),
                400,
            )

        # التحقق من عدم وجود المستخدم
        if User.query.filter_by(username=data["username"]).first():
            return (
                jsonify({"success": False, "error": "اسم المستخدم موجود بالفعل"}),
                400,
            )

        user = User(
            username=data["username"],
            email=data.get("email", ""),
            full_name=data.get("full_name", ""),
            password_hash=generate_password_hash(data["password"]),
            role=data.get("role", "user"),
            is_active=data.get("is_active", True),
        )

        db.session.add(user)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "data": user.to_dict(),
                    "message": "تم إنشاء المستخدم بنجاح",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء المستخدم: {e}")
        return jsonify({"success": False, "error": "فشل في إنشاء المستخدم"}), 500


@users_bp.route("/api/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    """الحصول على مستخدم محدد"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({"success": True, "data": user.to_dict()})
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدم: {e}")
        return jsonify({"success": False, "error": "فشل في الحصول على المستخدم"}), 500


@users_bp.route("/api/users/<int:user_id>", methods=["PUT"])
@token_required
@admin_required
def update_user(user_id):
    """تحديث مستخدم"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if data.get("username"):
            user.username = data["username"]
        if data.get("email"):
            user.email = data["email"]
        if data.get("full_name"):
            user.full_name = data["full_name"]
        if data.get("password"):
            user.password_hash = generate_password_hash(data["password"])
        if "role" in data:
            user.role = data["role"]
        if "is_active" in data:
            user.is_active = data["is_active"]

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "data": user.to_dict(),
                "message": "تم تحديث المستخدم بنجاح",
            }
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث المستخدم: {e}")
        return jsonify({"success": False, "error": "فشل في تحديث المستخدم"}), 500


@users_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(user_id):
    """حذف مستخدم"""
    try:
        user = User.query.get_or_404(user_id)

        # منع حذف المستخدم الحالي
        current_user = getattr(request, "current_user", None)
        if current_user and current_user.id == user_id:
            return (
                jsonify({"success": False, "error": "لا يمكن حذف المستخدم الحالي"}),
                400,
            )

        db.session.delete(user)
        db.session.commit()

        return jsonify({"success": True, "message": "تم حذف المستخدم بنجاح"})

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف المستخدم: {e}")
        return jsonify({"success": False, "error": "فشل في حذف المستخدم"}), 500
