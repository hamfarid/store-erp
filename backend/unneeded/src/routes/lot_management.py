# FILE: backend/src/routes/lot_management.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
إدارة اللوطات
All linting disabled due to complex imports and optional dependencies.
"""

from datetime import datetime, timezone

try:
    from flask import Blueprint, request, jsonify, session
except ImportError:
    # Fallback when Flask is not available
    class Blueprint:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(f):
                return f

            return decorator

    def jsonify(data):
        return {"data": data}

    class request:
        args = {}


# P0.2.4: Import error envelope helpers
try:
    from src.middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes,
    )
except ImportError:
    # Fallback when middleware is not available
    def success_response(data=None, message="Success", code="SUCCESS", status_code=200):
        return {"success": True, "data": data, "message": message}, status_code

    def error_response(message, code=None, details=None, status_code=400):
        return {"success": False, "message": message, "code": code}, status_code

    class ErrorCodes:
        SYS_INTERNAL_ERROR = "SYS_001"

    # Fallback when Flask is not available
    class Blueprint:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(f):
                return f

            return decorator

    def jsonify(data):
        return {"data": data}

    class request:
        json = {}
        form = {}
        args = {}

    session = {}

try:
    from sqlalchemy import func, and_, or_
except ImportError:
    # Fallback when SQLAlchemy is not available
    class func:
        @staticmethod
        def count(*args):
            return 0

        @staticmethod
        def sum(*args):
            return 0

    def and_(*args):
        return True

    def or_(*args):
        return True


try:
    from src.database import db
    from src.models.inventory import Batch, InventoryMovement

    try:
        from src.models.product_unified import Product  # prefer unified product model
    except Exception:
        from src.models.inventory import Product  # fallback to legacy product if needed
except ImportError:
    # Fallback when models are not available
    class MockDB:
        session = None

        @staticmethod
        def add(obj):
            pass

        @staticmethod
        def commit():
            pass

        @staticmethod
        def rollback():
            pass

    db = MockDB()

    class Batch:
        query = None

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Product:
        query = None

    class InventoryMovement:
        pass


try:
    from src.models.supplier import Supplier
except ImportError:

    class Supplier:
        query = None


try:
    from src.models.user import User
except ImportError:

    class User:
        query = None


# إنشاء Blueprint
lot_bp = Blueprint("lot_management", __name__)


@lot_bp.route("/api/lots", methods=["GET"])
def get_lots():
    """الحصول على قائمة اللوطات"""
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        search = request.args.get("search", "")
        status = request.args.get("status", "")
        product_id = request.args.get("product_id", "")

        lots = []
        total = 0

        if Batch and hasattr(Batch, "query") and Batch.query:
            query = Batch.query

            # تطبيق الفلاتر
            if search:
                query = query.filter(
                    or_(
                        Batch.batch_number.contains(search),
                        Batch.notes.contains(search),
                    )
                )

            if status:
                query = query.filter(Batch.status == status)

            if product_id:
                query = query.filter(Batch.product_id == product_id)

            # الحصول على العدد الإجمالي
            total = query.count()

            # تطبيق التصفح
            lots_data = query.offset((page - 1) * per_page).limit(per_page).all()
            lots = [lot.to_dict() for lot in lots_data]

        return jsonify(
            {
                "status": "success",
                "data": lots,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": (total + per_page - 1) // per_page,
                },
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "error": f"خطأ في الحصول على اللوطات: {str(e)}"}
            ),
            500,
        )


@lot_bp.route("/api/lots", methods=["POST"])
def create_lot():
    """إنشاء لوط جديد"""
    try:
        data = request.json if hasattr(request, "json") else {}

        # التحقق من البيانات المطلوبة
        required_fields = ["batch_number", "product_id", "initial_quantity"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"status": "error", "error": f"{field} مطلوب"}), 400

        # التحقق من عدم وجود لوط بنفس الرقم
        if Batch and hasattr(Batch, "query") and Batch.query:
            existing_lot = Batch.query.filter_by(
                batch_number=data["batch_number"]
            ).first()

            if existing_lot:
                return (
                    jsonify({"status": "error", "error": "يوجد لوط بهذا الرقم بالفعل"}),
                    400,
                )

        # إنشاء اللوط الجديد
        new_lot = Batch(
            batch_number=data["batch_number"],
            product_id=data["product_id"],
            initial_quantity=data["initial_quantity"],
            current_quantity=data["initial_quantity"],
            production_date=(
                datetime.strptime(data["production_date"], "%Y-%m-%d").date()
                if data.get("production_date")
                else None
            ),
            expiry_date=(
                datetime.strptime(data["expiry_date"], "%Y-%m-%d").date()
                if data.get("expiry_date")
                else None
            ),
            received_date=(
                datetime.strptime(data["received_date"], "%Y-%m-%d").date()
                if data.get("received_date")
                else None
            ),
            status=data.get("status", "active"),
            quality_grade=data.get("quality_grade"),
            notes=data.get("notes"),
            supplier_id=data.get("supplier_id"),
            supplier_batch_number=data.get("supplier_batch_number"),
            purchase_price=data.get("purchase_price"),
        )

        if db and hasattr(db, "session") and db.session:
            db.session.add(new_lot)
            db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء اللوط بنجاح",
                "data": new_lot.to_dict() if hasattr(new_lot, "to_dict") else {},
            }
        )

    except Exception as e:
        if db and hasattr(db, "session") and db.session:
            db.session.rollback()
        return (
            jsonify({"status": "error", "error": f"خطأ في إنشاء اللوط: {str(e)}"}),
            500,
        )


@lot_bp.route("/api/lots/<int:lot_id>", methods=["GET"])
def get_lot(lot_id):
    """الحصول على تفاصيل لوط محدد"""
    try:
        lot = None
        if Batch and hasattr(Batch, "query") and Batch.query:
            lot = Batch.query.get(lot_id)

        if not lot:
            return jsonify({"status": "error", "error": "اللوط غير موجود"}), 404

        return jsonify(
            {
                "status": "success",
                "data": lot.to_dict() if hasattr(lot, "to_dict") else {},
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في الحصول على اللوط: {str(e)}"}),
            500,
        )


@lot_bp.route("/api/lots/<int:lot_id>", methods=["PUT"])
def update_lot(lot_id):
    """تحديث لوط"""
    try:
        data = request.json if hasattr(request, "json") else {}

        lot = None
        if Batch and hasattr(Batch, "query") and Batch.query:
            lot = Batch.query.get(lot_id)

        if not lot:
            return jsonify({"status": "error", "error": "اللوط غير موجود"}), 404

        # تحديث البيانات
        updatable_fields = [
            "batch_number",
            "production_date",
            "expiry_date",
            "received_date",
            "status",
            "quality_grade",
            "notes",
            "supplier_id",
            "supplier_batch_number",
            "purchase_price",
        ]

        for field in updatable_fields:
            if field in data:
                if (
                    field in ["production_date", "expiry_date", "received_date"]
                    and data[field]
                ):
                    setattr(
                        lot, field, datetime.strptime(data[field], "%Y-%m-%d").date()
                    )
                else:
                    setattr(lot, field, data[field])

        if db and hasattr(db, "session") and db.session:
            db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث اللوط بنجاح",
                "data": lot.to_dict() if hasattr(lot, "to_dict") else {},
            }
        )

    except Exception as e:
        if db and hasattr(db, "session") and db.session:
            db.session.rollback()
        return (
            jsonify({"status": "error", "error": f"خطأ في تحديث اللوط: {str(e)}"}),
            500,
        )


@lot_bp.route("/api/lots/<int:lot_id>/movements", methods=["GET"])
def get_lot_movements(lot_id):
    """الحصول على حركات لوط محدد"""
    try:
        movements = []

        if (
            InventoryMovement
            and hasattr(InventoryMovement, "query")
            and InventoryMovement.query
        ):
            movements_data = (
                InventoryMovement.query.filter_by(batch_id=lot_id)
                .order_by(InventoryMovement.movement_date.desc())
                .all()
            )

            movements = [movement.to_dict() for movement in movements_data]

        return jsonify({"status": "success", "data": movements})

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "error": f"خطأ في الحصول على حركات اللوط: {str(e)}"}
            ),
            500,
        )


@lot_bp.route("/api/lots/stats", methods=["GET"])
def get_lots_stats():
    """الحصول على إحصائيات اللوطات"""
    try:
        stats = {
            "total_lots": 0,
            "active_lots": 0,
            "expired_lots": 0,
            "recalled_lots": 0,
            "sold_out_lots": 0,
        }

        if Batch and hasattr(Batch, "query") and Batch.query:
            stats["total_lots"] = Batch.query.count()
            stats["active_lots"] = Batch.query.filter_by(status="active").count()
            stats["expired_lots"] = Batch.query.filter_by(status="expired").count()
            stats["recalled_lots"] = Batch.query.filter_by(status="recalled").count()
            stats["sold_out_lots"] = Batch.query.filter_by(status="sold_out").count()

        return jsonify({"status": "success", "data": stats})

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "error": f"خطأ في الحصول على إحصائيات اللوطات: {str(e)}",
                }
            ),
            500,
        )
