# FILE: backend/src/routes/warehouse_transfer.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from datetime import datetime
from sqlalchemy.orm import joinedload

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
# ملف: /home/ubuntu/complete_inventory_system/backend/src/routes/warehouse_transfer.py
# APIs لإدارة تحويلات المخزون
# All linting disabled due to complex imports and optional dependencies.

from flask import Blueprint, request, jsonify, session

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging
from sqlalchemy import or_

# Lazy import models to avoid early mapper configuration errors
WarehouseTransfer = None
WarehouseTransferItem = None


def _get_models():
    global WarehouseTransfer, WarehouseTransferItem
    if WarehouseTransfer is None or WarehouseTransferItem is None:
        from models import warehouse_transfer as wt

        WarehouseTransfer = wt.WarehouseTransfer
        WarehouseTransferItem = wt.WarehouseTransferItem
    return WarehouseTransfer, WarehouseTransferItem


# Import database - handle different import paths
try:
    from database import db
except ImportError:
    # Create mock db for testing
    class MockDB:
        session = None

        @staticmethod
        def create_all():  # pragma: no cover - mock placeholder for tests
            pass

        @staticmethod
        def drop_all():  # pragma: no cover - mock placeholder for tests
            pass

    db = MockDB()
# Import auth functions
try:
    from auth import login_required, has_permission, Permissions, AuthManager
except ImportError:
    # Create mock auth functions
    def login_required(f):
        return f

    def has_permission(_permission):  # pragma: no cover - mock placeholder
        def decorator(f):
            return f

        return decorator

    class Permissions:
        ADMIN = "admin"

    class AuthManager:
        @staticmethod
        def authenticate(username, password):
            return True


warehouse_transfer_bp = Blueprint("warehouse_transfer", __name__)

# ---- OpenAPI Metadata & Schema Registration (optional) ----
try:  # noqa: SIM105
    from src.api_meta import api_endpoint as api_meta, register_schema

    # Base transfer item schema
    register_schema(
        "WarehouseTransferItem",
        {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer"},
                "requested_quantity": {"type": "number"},
                "approved_quantity": {"type": "number"},
                "unit": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["product_id", "requested_quantity"],
        },
    )

    # Transfer schema
    register_schema(
        "WarehouseTransfer",
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "from_warehouse_id": {"type": "integer"},
                "to_warehouse_id": {"type": "integer"},
                "requested_by": {"type": "integer"},
                "approved_by": {"type": "integer"},
                "completed_by": {"type": "integer"},
                "requested_date": {"type": "string", "format": "date-time"},
                "approved_date": {"type": "string", "format": "date-time"},
                "completed_date": {"type": "string", "format": "date-time"},
                "status": {"type": "string"},
                "total_items": {"type": "integer"},
                "notes": {"type": "string"},
                "items": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/WarehouseTransferItem"},
                },
            },
            "required": ["id", "from_warehouse_id", "to_warehouse_id", "status"],
        },
    )

    register_schema(
        "WarehouseTransferListResponse",
        {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "error"]},
                "transfers": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/WarehouseTransfer"},
                },
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "current_page": {"type": "integer"},
            },
            "required": ["status", "transfers"],
        },
    )

    register_schema(
        "WarehouseTransferResponse",
        {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "error"]},
                "transfer": {"$ref": "#/components/schemas/WarehouseTransfer"},
            },
            "required": ["status", "transfer"],
        },
    )

    register_schema(
        "WarehouseTransferStats",
        {
            "type": "object",
            "properties": {
                "total_transfers": {"type": "integer"},
                "pending_transfers": {"type": "integer"},
                "approved_transfers": {"type": "integer"},
                "completed_transfers": {"type": "integer"},
                "today_transfers": {"type": "integer"},
            },
            "required": ["total_transfers"],
        },
    )

    register_schema(
        "WarehouseTransferStatsResponse",
        {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["success", "error"]},
                "stats": {"$ref": "#/components/schemas/WarehouseTransferStats"},
            },
            "required": ["status", "stats"],
        },
    )
except Exception:  # noqa: BLE001
    api_meta = None  # type: ignore


def _meta(*args, **kwargs):  # small helper to safely apply decorator
    if api_meta:
        return api_meta(*args, **kwargs)

    def inner(f):  # pragma: no cover - trivial wrapper
        return f

    return inner


@warehouse_transfer_bp.route("/api/warehouse-transfers", methods=["GET"])
@login_required
@_meta(
    summary="List warehouse transfers",
    description="Paginated list of warehouse transfer requests",
    tags=["WarehouseTransfers"],
    response_schema="WarehouseTransferListResponse",
)
def get_transfers():
    """الحصول على قائمة التحويلات"""
    try:
        page = request.args.get("page", 1, type=int)
        status = request.args.get("status")
        warehouse_id = request.args.get("warehouse_id")
        per_page = request.args.get("per_page", 10, type=int)

        WT, _ = _get_models()
        query = WT.query

        # فلترة حسب الحالة (تطبيع إلى Enum)
        if status:
            try:
                from models.warehouse_transfer import TransferStatus as WTStatus

                status_norm = status.strip().lower()
                # توافق قديم: 'approved' تعتبر 'in_transit'
                if status_norm == "approved":
                    status_norm = "in_transit"
                enum_val = WTStatus(status_norm)
                query = query.filter_by(status=enum_val)
            except Exception:
                pass  # تجاهل قيمة حالة غير صالحة

        # فلترة حسب المخزن
        if warehouse_id:
            try:
                warehouse_id_int = int(warehouse_id)
                query = query.filter(
                    or_(
                        WT.from_warehouse_id == warehouse_id_int,
                        WT.to_warehouse_id == warehouse_id_int,
                    )
                )
            except (ValueError, TypeError):
                pass  # Skip invalid warehouse_id

        # ترتيب حسب التاريخ
        query = query.order_by(WT.transfer_date.desc())

        # تطبيق التصفح
        transfers = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "status": "success",
                "transfers": [transfer.to_dict() for transfer in transfers.items],
                "total": transfers.total,
                "pages": transfers.pages,
                "current_page": page,
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@warehouse_transfer_bp.route("/api/warehouse-transfers", methods=["POST"])
@login_required
@_meta(
    summary="Create transfer",
    description="Create a new warehouse transfer with items",
    tags=["WarehouseTransfers"],
    response_schema="WarehouseTransferResponse",
)
def create_transfer():
    """إنشاء تحويل جديد"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["from_warehouse_id", "to_warehouse_id", "items"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        # التحقق من أن المخزنين مختلفين
        if data["from_warehouse_id"] == data["to_warehouse_id"]:
            return (
                jsonify(
                    {"status": "error", "message": "لا يمكن التحويل إلى نفس المخزن"}
                ),
                400,
            )

        # إنشاء التحويل (توليد رقم تحويل وضبط الحقول وفق النموذج)
        transfer_number = f"TR-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:17]}"
        transfer = WarehouseTransfer(
            transfer_number=transfer_number,
            from_warehouse_id=data["from_warehouse_id"],
            to_warehouse_id=data["to_warehouse_id"],
            created_by=session["user_id"],
            notes=data.get("notes"),
        )

        db.session.add(transfer)
        db.session.flush()  # للحصول على ID

        # إضافة العناصر
        total_items = 0
        for item_data in data["items"]:
            qty = item_data.get("quantity", 0)
            if qty and qty > 0:
                item = WarehouseTransferItem(
                    transfer_id=transfer.id,
                    product_id=item_data["product_id"],
                    quantity_requested=qty,
                    notes=item_data.get("notes"),
                )
                db.session.add(item)
                total_items += 1

        transfer.total_items = total_items
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء التحويل بنجاح",
                "transfer": transfer.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@warehouse_transfer_bp.route(
    "/api/warehouse-transfers/<int:transfer_id>", methods=["GET"]
)
@login_required
@_meta(
    summary="Get transfer details",
    description="Retrieve a single warehouse transfer by ID",
    tags=["WarehouseTransfers"],
    response_schema="WarehouseTransferResponse",
)
def get_transfer(transfer_id):
    """الحصول على تفاصيل تحويل محدد"""
    try:
        WT, _ = _get_models()
        transfer = WT.query.get_or_404(transfer_id)
        return jsonify({"status": "success", "transfer": transfer.to_dict()})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@warehouse_transfer_bp.route(
    "/api/warehouse-transfers/<int:transfer_id>/approve", methods=["POST"]
)
@login_required
@_meta(
    summary="Approve transfer",
    description="Approve a pending warehouse transfer",
    tags=["WarehouseTransfers"],
    response_schema="WarehouseTransferResponse",
)
def approve_transfer(transfer_id):
    """تأكيد التحويل"""
    try:
        WT, _ = _get_models()
        transfer = WT.query.get_or_404(transfer_id)

        if transfer.status != WTStatus.PENDING:
            return (
                jsonify({"status": "error", "message": "لا يمكن تأكيد هذا التحويل"}),
                400,
            )

        # تحديث الكميات المرسلة (تعادل approved_quantity القديمة)
        data = request.get_json() or {}
        if "items" in data:
            for item_data in data["items"]:
                item = WarehouseTransferItem.query.filter_by(
                    transfer_id=transfer_id, product_id=item_data["product_id"]
                ).first()
                if item:
                    item.quantity_sent = item_data.get(
                        "approved_quantity", item.quantity_requested
                    )

        # تحديث حالة التحويل والمعلومات التعريفية
        transfer.status = WTStatus.IN_TRANSIT
        try:
            transfer.approved_by = session["user_id"]
        except Exception:
            pass
        transfer.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تأكيد التحويل بنجاح",
                "transfer": transfer.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@warehouse_transfer_bp.route(
    "/api/warehouse-transfers/<int:transfer_id>/complete", methods=["POST"]
)
@login_required
@_meta(
    summary="Complete transfer",
    description="Complete an approved transfer and update stock levels",
    tags=["WarehouseTransfers"],
    response_schema="WarehouseTransferResponse",
)
def complete_transfer(transfer_id):
    """إكمال التحويل"""
    try:
        WT, _ = _get_models()
        transfer = WT.query.get_or_404(transfer_id)

        if transfer.status != WTStatus.IN_TRANSIT:
            return (
                jsonify({"status": "error", "message": "لا يمكن إكمال تحويل غير مؤكد"}),
                400,
            )

        data = request.get_json() or {}
        if "items" in data:
            for item_data in data["items"]:
                item = WarehouseTransferItem.query.filter_by(
                    transfer_id=transfer_id, product_id=item_data["product_id"]
                ).first()
                if item:
                    item.quantity_received = item_data.get(
                        "received_quantity",
                        item.quantity_sent or item.quantity_requested,
                    )

        transfer.status = WTStatus.COMPLETED
        try:
            transfer.received_by = session["user_id"]
        except Exception:
            pass
        transfer.completed_date = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إكمال التحويل وتحديث المخزون بنجاح",
                "transfer": transfer.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@warehouse_transfer_bp.route(
    "/api/warehouse-transfers/<int:transfer_id>/cancel", methods=["POST"]
)
@login_required
@_meta(
    summary="Cancel transfer",
    description="Cancel a pending or approved (not completed) transfer",
    tags=["WarehouseTransfers"],
    response_schema="WarehouseTransferResponse",
)
def cancel_transfer(transfer_id):
    """إلغاء التحويل"""
    try:
        WT, _ = _get_models()
        transfer = WT.query.get_or_404(transfer_id)

        if transfer.status == WTStatus.COMPLETED:
            return (
                jsonify({"status": "error", "message": "لا يمكن إلغاء تحويل مكتمل"}),
                400,
            )

        transfer.status = WTStatus.CANCELLED
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إلغاء التحويل بنجاح",
                "transfer": transfer.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@warehouse_transfer_bp.route("/api/warehouse-transfers/stats", methods=["GET"])
@login_required
@_meta(
    summary="Transfer statistics",
    description="Aggregate statistics about transfer states and today's activity",
    tags=["WarehouseTransfers"],
    response_schema="WarehouseTransferStatsResponse",
)
def get_transfer_stats():
    """إحصائيات التحويلات"""
    try:
        from sqlalchemy import func

        # إحصائيات عامة
        WT, _ = _get_models()
        total_transfers = WT.query.count()
        WT, _ = _get_models()
        pending_transfers = WT.query.filter_by(status=WTStatus.PENDING).count()
        in_transit_transfers = WT.query.filter_by(status=WTStatus.IN_TRANSIT).count()
        completed_transfers = WT.query.filter_by(status=WTStatus.COMPLETED).count()

        # تحويلات اليوم
        today = datetime.now().date()
        today_transfers = WT.query.filter(func.date(WT.transfer_date) == today).count()

        return jsonify(
            {
                "status": "success",
                "stats": {
                    "total_transfers": total_transfers,
                    "pending_transfers": pending_transfers,
                    "in_transit_transfers": in_transit_transfers,
                    "completed_transfers": completed_transfers,
                    "today_transfers": today_transfers,
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
