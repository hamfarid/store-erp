# FILE: backend/src/routes/automation.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# type: ignore
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/routes/automation.py

API endpoints للأتمتة
Automation API Endpoints

يوفر هذا الملف واجهات برمجة التطبيقات لإدارة الأتمتة والمهام المجدولة
All linting disabled due to complex imports and optional dependencies.
"""

from flask import Blueprint, request, jsonify, current_app

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime
from typing import Dict, List, Any

# محاولة استيراد الخدمات
try:
    from services.automation_service import automation_service
except ImportError:
    # إنشاء mock service إذا لم تكن متوفرة
    class MockAutomationService:
        def get_all_tasks(self):
            return []

        def create_task(self, task_data):
            return {"id": 1, "status": "created", **task_data}

        def update_task(self, task_id, task_data):
            return {"id": task_id, "status": "updated", **task_data}

        def delete_task(self, task_id):
            return {"id": task_id, "status": "deleted"}

        def execute_task(self, task_id):
            return {"id": task_id, "status": "executed"}

    automation_service = MockAutomationService()

try:
    from decorators.permission_decorators import require_permission
except ImportError:
    # إنشاء mock permission decorator
    def require_permission(permission):
        """Mock permission decorator"""

        def decorator(func):
            return func

        return decorator


automation_bp = Blueprint("automation", __name__, url_prefix="/api/automation")

# إعداد السجلات
logger = logging.getLogger(__name__)

# ==================== إدارة المهام المجدولة ====================


@automation_bp.route("/scheduled-tasks", methods=["GET"])
@jwt_required()
@require_permission("automation_read")
def get_scheduled_tasks():
    """الحصول على قائمة المهام المجدولة"""
    try:
        tasks = automation_service.get_scheduled_tasks()

        return jsonify({"status": "success", "tasks": tasks, "total": len(tasks)}), 200

    except Exception as e:
        logger.error(f"خطأ في الحصول على المهام المجدولة: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على المهام: {str(e)}"}
            ),
            500,
        )


@automation_bp.route("/scheduled-tasks", methods=["POST"])
@jwt_required()
@require_permission("automation_create")
def create_scheduled_task():
    """إنشاء مهمة مجدولة جديدة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["name", "schedule_type", "action"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"الحقل {field} مطلوب"}),
                    400,
                )

        # إنشاء معرف فريد للمهمة
        task_id = f"task_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # إضافة المهمة
        result = automation_service.add_scheduled_task(task_id, data)

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"خطأ في إنشاء المهمة المجدولة: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في إنشاء المهمة: {str(e)}"}),
            500,
        )


@automation_bp.route("/scheduled-tasks/<task_id>", methods=["PUT"])
@jwt_required()
@require_permission("automation_update")
def update_scheduled_task(task_id):
    """تحديث مهمة مجدولة"""
    try:
        data = request.get_json()

        # حذف المهمة القديمة
        automation_service.remove_scheduled_task(task_id)

        # إضافة المهمة المحدثة
        result = automation_service.add_scheduled_task(task_id, data)

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"خطأ في تحديث المهمة المجدولة: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث المهمة: {str(e)}"}),
            500,
        )


@automation_bp.route("/scheduled-tasks/<task_id>", methods=["DELETE"])
@jwt_required()
@require_permission("automation_delete")
def delete_scheduled_task(task_id):
    """حذف مهمة مجدولة"""
    try:
        success = automation_service.remove_scheduled_task(task_id)

        if success:
            return jsonify({"status": "success", "message": "تم حذف المهمة بنجاح"}), 200
        else:
            return jsonify({"status": "error", "message": "المهمة غير موجودة"}), 404

    except Exception as e:
        logger.error(f"خطأ في حذف المهمة المجدولة: {str(e)}")
        return (
            jsonify({"success": False, "message": f"خطأ في حذف المهمة: {str(e)}"}),
            500,
        )


# ==================== إدارة قواعد الأتمتة ====================


@automation_bp.route("/rules", methods=["GET"])
@jwt_required()
@require_permission("automation_read")
def get_automation_rules():
    """الحصول على قائمة قواعد الأتمتة"""
    try:
        rules = automation_service.get_automation_rules()

        return jsonify({"status": "success", "rules": rules, "total": len(rules)}), 200

    except Exception as e:
        logger.error(f"خطأ في الحصول على قواعد الأتمتة: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على القواعد: {str(e)}"}
            ),
            500,
        )


@automation_bp.route("/rules", methods=["POST"])
@jwt_required()
@require_permission("automation_create")
def create_automation_rule():
    """إنشاء قاعدة أتمتة جديدة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["name", "trigger", "conditions", "actions"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"الحقل {field} مطلوب"}),
                    400,
                )

        # إنشاء معرف فريد للقاعدة
        rule_id = f"rule_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # إضافة القاعدة
        result = automation_service.add_automation_rule(rule_id, data)

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"خطأ في إنشاء قاعدة الأتمتة: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في إنشاء القاعدة: {str(e)}"}),
            500,
        )


@automation_bp.route("/rules/<rule_id>", methods=["PUT"])
@jwt_required()
@require_permission("automation_update")
def update_automation_rule(rule_id):
    """تحديث قاعدة أتمتة"""
    try:
        data = request.get_json()

        # حذف القاعدة القديمة
        automation_service.remove_automation_rule(rule_id)

        # إضافة القاعدة المحدثة
        result = automation_service.add_automation_rule(rule_id, data)

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"خطأ في تحديث قاعدة الأتمتة: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث القاعدة: {str(e)}"}),
            500,
        )


@automation_bp.route("/rules/<rule_id>", methods=["DELETE"])
@jwt_required()
@require_permission("automation_delete")
def delete_automation_rule(rule_id):
    """حذف قاعدة أتمتة"""
    try:
        success = automation_service.remove_automation_rule(rule_id)

        if success:
            return (
                jsonify({"status": "success", "message": "تم حذف القاعدة بنجاح"}),
                200,
            )
        else:
            return jsonify({"status": "error", "message": "القاعدة غير موجودة"}), 404

    except Exception as e:
        logger.error(f"خطأ في حذف قاعدة الأتمتة: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في حذف القاعدة: {str(e)}"}),
            500,
        )


# ==================== إدارة المجدول ====================


@automation_bp.route("/scheduler/start", methods=["POST"])
@jwt_required()
@require_permission("automation_admin")
def start_scheduler():
    """بدء مجدول المهام"""
    try:
        success = automation_service.start_scheduler()

        if success:
            return (
                jsonify({"status": "success", "message": "تم بدء مجدول المهام بنجاح"}),
                200,
            )
        else:
            return jsonify({"status": "error", "message": "المجدول يعمل بالفعل"}), 400

    except Exception as e:
        logger.error(f"خطأ في بدء المجدول: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في بدء المجدول: {str(e)}"}),
            500,
        )


@automation_bp.route("/scheduler/stop", methods=["POST"])
@jwt_required()
@require_permission("automation_admin")
def stop_scheduler():
    """إيقاف مجدول المهام"""
    try:
        success = automation_service.stop_scheduler()

        if success:
            return (
                jsonify(
                    {"status": "success", "message": "تم إيقاف مجدول المهام بنجاح"}
                ),
                200,
            )
        else:
            return jsonify({"status": "error", "message": "خطأ في إيقاف المجدول"}), 400

    except Exception as e:
        logger.error(f"خطأ في إيقاف المجدول: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في إيقاف المجدول: {str(e)}"}),
            500,
        )


@automation_bp.route("/scheduler/status", methods=["GET"])
@jwt_required()
@require_permission("automation_read")
def get_scheduler_status():
    """الحصول على حالة المجدول"""
    try:
        status = {
            "is_running": automation_service.is_running,
            "total_tasks": len(automation_service.scheduled_tasks),
            "total_rules": len(automation_service.automation_rules),
        }

        return jsonify({"status": "success", "scheduler": status}), 200

    except Exception as e:
        logger.error(f"خطأ في الحصول على حالة المجدول: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على الحالة: {str(e)}"}
            ),
            500,
        )


# ==================== تشغيل الأحداث ====================


@automation_bp.route("/trigger-event", methods=["POST"])
@jwt_required()
@require_permission("automation_execute")
def trigger_event():
    """تشغيل حدث لتفعيل قواعد الأتمتة"""
    try:
        data = request.get_json()

        event_type = data.get("event_type")
        event_data = data.get("event_data", {})

        if not event_type:
            return jsonify({"status": "error", "message": "نوع الحدث مطلوب"}), 400

        # تشغيل قواعد الأتمتة
        automation_service.trigger_automation_rules(event_type, event_data)

        return jsonify({"status": "success", "message": "تم تشغيل الحدث بنجاح"}), 200

    except Exception as e:
        logger.error(f"خطأ في تشغيل الحدث: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في تشغيل الحدث: {str(e)}"}),
            500,
        )


# ==================== قوالب الأتمتة ====================


@automation_bp.route("/templates", methods=["GET"])
@jwt_required()
@require_permission("automation_read")
def get_automation_templates():
    """الحصول على قوالب الأتمتة المتاحة"""
    try:
        templates = [
            {
                "id": "low_stock_alert",
                "name": "تنبيه المخزون المنخفض",
                "description": "إرسال تنبيه عند انخفاض مستوى المخزون",
                "trigger": "event_based",
                "conditions": {"event_type": "low_stock_alert"},
                "actions": [
                    {
                        "type": "send_notification",
                        "parameters": {
                            "message": "تنبيه: المنتج {product_name} منخفض المخزون",
                            "recipient": "inventory_manager",
                        },
                    }
                ],
            },
            {
                "id": "payment_reminder",
                "name": "تذكير الدفع",
                "description": "إرسال تذكير للعملاء بالفواتير المستحقة",
                "trigger": "event_based",
                "conditions": {"event_type": "payment_reminder"},
                "actions": [
                    {
                        "type": "send_email",
                        "parameters": {
                            "to_email": "{customer_email}",
                            "subject": "تذكير: فاتورة مستحقة رقم {invoice_number}",
                            "body": "عزيزي {customer_name}، لديك فاتورة مستحقة بمبلغ {amount}",
                        },
                    }
                ],
            },
            {
                "id": "daily_backup",
                "name": "النسخ الاحتياطي اليومي",
                "description": "إنشاء نسخة احتياطية يومية للبيانات",
                "schedule_type": "daily",
                "schedule_time": "02:00",
                "action": "backup_data",
                "parameters": {"backup_type": "incremental"},
            },
            {
                "id": "weekly_report",
                "name": "التقرير الأسبوعي",
                "description": "توليد تقرير أسبوعي للمبيعات",
                "schedule_type": "weekly",
                "schedule_time": "08:00",
                "day_of_week": "monday",
                "action": "generate_report",
                "parameters": {"report_type": "sales", "period": "weekly"},
            },
        ]

        return jsonify({"status": "success", "templates": templates}), 200

    except Exception as e:
        logger.error(f"خطأ في الحصول على قوالب الأتمتة: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على القوالب: {str(e)}"}
            ),
            500,
        )


@automation_bp.route("/templates/<template_id>/apply", methods=["POST"])
@jwt_required()
@require_permission("automation_create")
def apply_automation_template(template_id):
    """تطبيق قالب أتمتة"""
    try:
        data = request.get_json()
        customizations = data.get("customizations", {})

        # الحصول على القالب
        templates = {
            "low_stock_alert": {
                "name": "تنبيه المخزون المنخفض",
                "trigger": "event_based",
                "conditions": {"event_type": "low_stock_alert"},
                "actions": [
                    {
                        "type": "send_notification",
                        "parameters": {"message": "تنبيه مخزون منخفض"},
                    }
                ],
            },
            "payment_reminder": {
                "name": "تذكير الدفع",
                "trigger": "event_based",
                "conditions": {"event_type": "payment_reminder"},
                "actions": [
                    {"type": "send_email", "parameters": {"subject": "تذكير دفع"}}
                ],
            },
        }

        if template_id not in templates:
            return jsonify({"status": "error", "message": "القالب غير موجود"}), 404

        template = templates[template_id].copy()

        # تطبيق التخصيصات
        template.update(customizations)

        # إنشاء معرف فريد
        rule_id = f"{template_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # إضافة القاعدة
        result = automation_service.add_automation_rule(rule_id, template)

        if result.get("status") == "success" or result.get("success") is True:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"خطأ في تطبيق قالب الأتمتة: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"خطأ في تطبيق القالب: {str(e)}"}),
            500,
        )


# ==================== إحصائيات الأتمتة ====================


@automation_bp.route("/statistics", methods=["GET"])
@jwt_required()
@require_permission("automation_read")
def get_automation_statistics():
    """الحصول على إحصائيات الأتمتة"""
    try:
        tasks = automation_service.get_scheduled_tasks()
        rules = automation_service.get_automation_rules()

        # حساب الإحصائيات
        active_tasks = len([t for t in tasks if t.get("is_active", True)])
        active_rules = len([r for r in rules if r.get("is_active", True)])
        total_executions = sum(t.get("run_count", 0) for t in tasks)
        total_rule_executions = sum(r.get("execution_count", 0) for r in rules)

        statistics = {
            "total_tasks": len(tasks),
            "active_tasks": active_tasks,
            "total_rules": len(rules),
            "active_rules": active_rules,
            "total_executions": total_executions,
            "total_rule_executions": total_rule_executions,
            "scheduler_status": automation_service.is_running,
        }

        return jsonify({"status": "success", "statistics": statistics}), 200

    except Exception as e:
        logger.error(f"خطأ في الحصول على إحصائيات الأتمتة: {str(e)}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"خطأ في الحصول على الإحصائيات: {str(e)}",
                }
            ),
            500,
        )


# معالج الأخطاء
@automation_bp.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "المورد غير موجود"}), 404


@automation_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "خطأ داخلي في الخادم"}), 500
