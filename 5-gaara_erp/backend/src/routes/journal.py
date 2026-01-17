#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مسارات سجل الأحداث (Journal Routes)
Journal/Audit Log API Routes
"""

import logging
from flask import Blueprint, jsonify, request
from src.database import db
from src.models.journal import JournalEntry, JournalConfig, JournalEventType
from src.services.journal_service import JournalService

logger = logging.getLogger(__name__)

journal_bp = Blueprint("journal", __name__, url_prefix="/api/journal")


@journal_bp.route("", methods=["GET"])
def get_journal_entries():
    """الحصول على سجل الأحداث"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        model_type = request.args.get("model_type")
        model_id = request.args.get("model_id", type=int)
        event_type = request.args.get("event_type")
        reference = request.args.get("reference")

        query = JournalEntry.query

        if model_type:
            query = query.filter(JournalEntry.model_type == model_type)
        if model_id:
            query = query.filter(JournalEntry.model_id == model_id)
        if event_type:
            query = query.filter(JournalEntry.event_type == event_type)
        if reference:
            query = query.filter(
                (JournalEntry.reference_number.ilike(f"%{reference}%"))
                | (JournalEntry.source_reference.ilike(f"%{reference}%"))
            )

        query = query.order_by(JournalEntry.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "success": True,
                "data": [e.to_dict() for e in pagination.items],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                },
            }
        )
    except Exception as e:
        logger.error(f"Error getting journal entries: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@journal_bp.route("/<int:entry_id>", methods=["GET"])
def get_journal_entry(entry_id):
    """الحصول على سجل حدث محدد"""
    entry = JournalEntry.query.get_or_404(entry_id)
    return jsonify({"success": True, "data": entry.to_dict()})


@journal_bp.route("/model/<model_type>/<int:model_id>", methods=["GET"])
def get_model_journal(model_type, model_id):
    """الحصول على سجل أحداث موديل محدد"""
    entries = (
        JournalEntry.query.filter_by(model_type=model_type, model_id=model_id)
        .order_by(JournalEntry.created_at.desc())
        .all()
    )

    return jsonify({"success": True, "data": [e.to_dict() for e in entries]})


@journal_bp.route("/config", methods=["GET"])
def get_journal_config():
    """الحصول على إعدادات السجل"""
    configs = JournalConfig.query.all()

    # إضافة الأحداث غير المُعدة
    existing = {c.event_type for c in configs}
    result = [c.to_dict() for c in configs]

    for event in JournalEventType:
        if event.value not in existing:
            result.append(
                {
                    "event_type": event.value,
                    "is_enabled": True,
                    "send_notification": False,
                    "send_email": False,
                    "retention_days": 365,
                }
            )

    return jsonify({"success": True, "data": result})


@journal_bp.route("/config", methods=["POST"])
def update_journal_config():
    """تحديث إعدادات السجل"""
    try:
        data = request.get_json()
        event_type = data.get("event_type")

        config = JournalConfig.query.filter_by(event_type=event_type).first()
        if not config:
            config = JournalConfig(event_type=event_type)
            db.session.add(config)

        config.is_enabled = data.get("is_enabled", True)
        config.send_notification = data.get("send_notification", False)
        config.notification_channels = data.get("notification_channels")
        config.send_email = data.get("send_email", False)
        config.email_template = data.get("email_template")
        config.email_recipients = data.get("email_recipients")
        config.retention_days = data.get("retention_days", 365)
        config.settings = data.get("settings")

        db.session.commit()

        return jsonify(
            {"success": True, "message": "تم تحديث الإعدادات", "data": config.to_dict()}
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating config: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@journal_bp.route("/event-types", methods=["GET"])
def get_event_types():
    """الحصول على أنواع الأحداث المتاحة"""
    return jsonify(
        {
            "success": True,
            "data": [{"value": e.value, "name": e.name} for e in JournalEventType],
        }
    )
