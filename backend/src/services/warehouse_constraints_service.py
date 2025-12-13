#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/warehouse_constraints_service.py

خدمة إدارة قيود المخازن (صادر/وارد)
تدير جميع العمليات المتعلقة بقيود المخازن والتقارير
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import logging
from models.warehouse_constraints import (
    WarehouseConstraint,
    WarehouseConstraintLine,
    WarehouseConstraintTemplate,
    WarehouseConstraintApproval,
    ConstraintType,
    ConstraintStatus,
)
from models.inventory import Product, Warehouse
from models.user import User

logger = logging.getLogger(__name__)


class WarehouseConstraintsService:
    """خدمة إدارة قيود المخازن الشاملة"""

    def __init__(self, db_session: Session):
        self.db = db_session

    # ==================== إدارة القيود ====================

    def create_constraint(
        self, constraint_data: Dict[str, Any], user_id: int
    ) -> WarehouseConstraint:
        """
        إنشاء قيد مخزن جديد

        Args:
            constraint_data: بيانات القيد
            user_id: معرف المستخدم المنشئ

        Returns:
            WarehouseConstraint: القيد المنشأ
        """
        try:
            # إنشاء رقم القيد
            constraint_number = self._generate_constraint_number(
                constraint_data.get("constraint_type")
            )

            # إنشاء القيد الرئيسي
            constraint = WarehouseConstraint(
                constraint_number=constraint_number,
                constraint_type=ConstraintType(constraint_data["constraint_type"]),
                constraint_date=constraint_data.get(
                    "constraint_date", datetime.utcnow()
                ),
                source_warehouse_id=constraint_data.get("source_warehouse_id"),
                destination_warehouse_id=constraint_data.get(
                    "destination_warehouse_id"
                ),
                customer_id=constraint_data.get("customer_id"),
                supplier_id=constraint_data.get("supplier_id"),
                reference=constraint_data.get("reference"),
                description=constraint_data.get("description"),
                notes=constraint_data.get("notes"),
                currency=constraint_data.get("currency", "USD"),
                exchange_rate=constraint_data.get("exchange_rate", 1.0),
                batch_number=constraint_data.get("batch_number"),
                lot_number=constraint_data.get("lot_number"),
                created_by=user_id,
            )

            self.db.add(constraint)
            self.db.flush()  # للحصول على ID

            # إضافة البنود
            if "lines" in constraint_data:
                for line_data in constraint_data["lines"]:
                    line = WarehouseConstraintLine(
                        constraint_id=constraint.id,
                        product_id=line_data["product_id"],
                        product_variant_id=line_data.get("product_variant_id"),
                        quantity=line_data["quantity"],
                        unit_of_measure_id=line_data["unit_of_measure_id"],
                        unit_cost=line_data.get("unit_cost", 0.0),
                        unit_price=line_data.get("unit_price", 0.0),
                        lot_number=line_data.get("lot_number"),
                        batch_number=line_data.get("batch_number"),
                        serial_number=line_data.get("serial_number"),
                        expiry_date=line_data.get("expiry_date"),
                        description=line_data.get("description"),
                        notes=line_data.get("notes"),
                    )
                    line.calculate_total_value()
                    constraint.constraint_lines.append(line)

            # حساب القيمة الإجمالية
            constraint.calculate_total_value()

            self.db.commit()
            logger.info(f"تم إنشاء قيد مخزن جديد: {constraint.constraint_number}")
            return constraint

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء قيد المخزن: {str(e)}")
            raise

    def update_constraint(
        self, constraint_id: int, update_data: Dict[str, Any], user_id: int
    ) -> WarehouseConstraint:
        """
        تحديث قيد مخزن

        Args:
            constraint_id: معرف القيد
            update_data: البيانات المحدثة
            user_id: معرف المستخدم

        Returns:
            WarehouseConstraint: القيد المحدث
        """
        try:
            constraint = (
                self.db.query(WarehouseConstraint).filter_by(id=constraint_id).first()
            )
            if not constraint:
                raise ValueError("القيد غير موجود")

            # التحقق من إمكانية التعديل
            if constraint.status not in [
                ConstraintStatus.DRAFT,
                ConstraintStatus.CONFIRMED,
            ]:
                raise ValueError("لا يمكن تعديل قيد مرحل أو ملغي")

            # تحديث البيانات الأساسية
            for field, value in update_data.items():
                if field not in ["lines"] and hasattr(constraint, field):
                    setattr(constraint, field, value)

            # تحديث البنود إذا كانت موجودة
            if "lines" in update_data:
                # حذف البنود القديمة
                for line in constraint.constraint_lines:
                    self.db.delete(line)

                # إضافة البنود الجديدة
                for line_data in update_data["lines"]:
                    line = WarehouseConstraintLine(
                        constraint_id=constraint.id, **line_data
                    )
                    line.calculate_total_value()
                    constraint.constraint_lines.append(line)

            # إعادة حساب القيمة الإجمالية
            constraint.calculate_total_value()
            constraint.updated_at = datetime.utcnow()

            self.db.commit()
            logger.info(f"تم تحديث قيد المخزن: {constraint.constraint_number}")
            return constraint

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في تحديث قيد المخزن: {str(e)}")
            raise

    def confirm_constraint(self, constraint_id: int, user_id: int) -> bool:
        """تأكيد قيد المخزن"""
        try:
            constraint = (
                self.db.query(WarehouseConstraint).filter_by(id=constraint_id).first()
            )
            if not constraint:
                raise ValueError("القيد غير موجود")

            if constraint.confirm():
                constraint.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"تم تأكيد قيد المخزن: {constraint.constraint_number}")
                return True
            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في تأكيد قيد المخزن: {str(e)}")
            raise

    def post_constraint(self, constraint_id: int, user_id: int) -> bool:
        """ترحيل قيد المخزن"""
        try:
            constraint = (
                self.db.query(WarehouseConstraint).filter_by(id=constraint_id).first()
            )
            if not constraint:
                raise ValueError("القيد غير موجود")

            # التحقق من الموافقات المطلوبة
            if not self._check_approvals(constraint_id):
                raise ValueError("القيد يحتاج موافقات إضافية")

            if constraint.post(user_id):
                # تطبيق تأثير القيد على المخزون
                self._apply_constraint_to_inventory(constraint)

                constraint.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"تم ترحيل قيد المخزن: {constraint.constraint_number}")
                return True
            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في ترحيل قيد المخزن: {str(e)}")
            raise

    def cancel_constraint(
        self, constraint_id: int, user_id: int, reason: str = None
    ) -> bool:
        """إلغاء قيد المخزن"""
        try:
            constraint = (
                self.db.query(WarehouseConstraint).filter_by(id=constraint_id).first()
            )
            if not constraint:
                raise ValueError("القيد غير موجود")

            if constraint.cancel():
                if reason:
                    constraint.notes = (
                        f"{constraint.notes or ''}\nسبب الإلغاء: {reason}"
                    )
                constraint.updated_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"تم إلغاء قيد المخزن: {constraint.constraint_number}")
                return True
            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إلغاء قيد المخزن: {str(e)}")
            raise

    # ==================== التقارير ====================

    def get_constraints_report(
        self, filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        تقرير قيود المخازن

        Args:
            filters: فلاتر التقرير

        Returns:
            List[Dict]: قائمة القيود مع التفاصيل
        """
        try:
            query = self.db.query(WarehouseConstraint)

            # تطبيق الفلاتر
            if filters:
                if "constraint_type" in filters:
                    query = query.filter(
                        WarehouseConstraint.constraint_type
                        == filters["constraint_type"]
                    )

                if "status" in filters:
                    query = query.filter(
                        WarehouseConstraint.status == filters["status"]
                    )

                if "warehouse_id" in filters:
                    query = query.filter(
                        or_(
                            WarehouseConstraint.source_warehouse_id
                            == filters["warehouse_id"],
                            WarehouseConstraint.destination_warehouse_id
                            == filters["warehouse_id"],
                        )
                    )

                if "date_from" in filters:
                    query = query.filter(
                        WarehouseConstraint.constraint_date >= filters["date_from"]
                    )

                if "date_to" in filters:
                    query = query.filter(
                        WarehouseConstraint.constraint_date <= filters["date_to"]
                    )

                if "customer_id" in filters:
                    query = query.filter(
                        WarehouseConstraint.customer_id == filters["customer_id"]
                    )

                if "supplier_id" in filters:
                    query = query.filter(
                        WarehouseConstraint.supplier_id == filters["supplier_id"]
                    )

            # ترتيب النتائج
            order_by = (
                filters.get("order_by", "constraint_date")
                if filters
                else "constraint_date"
            )
            order_dir = filters.get("order_dir", "desc") if filters else "desc"

            if order_dir == "desc":
                query = query.order_by(desc(getattr(WarehouseConstraint, order_by)))
            else:
                query = query.order_by(asc(getattr(WarehouseConstraint, order_by)))

            constraints = query.all()

            # تحويل النتائج
            result = []
            for constraint in constraints:
                constraint_data = {
                    "id": constraint.id,
                    "constraint_number": constraint.constraint_number,
                    "constraint_type": constraint.constraint_type.value,
                    "status": constraint.status.value,
                    "constraint_date": (
                        constraint.constraint_date.isoformat()
                        if constraint.constraint_date
                        else None
                    ),
                    "posting_date": (
                        constraint.posting_date.isoformat()
                        if constraint.posting_date
                        else None
                    ),
                    "source_warehouse": (
                        constraint.source_warehouse.name
                        if constraint.source_warehouse
                        else None
                    ),
                    "destination_warehouse": (
                        constraint.destination_warehouse.name
                        if constraint.destination_warehouse
                        else None
                    ),
                    "customer": (
                        constraint.customer.name if constraint.customer else None
                    ),
                    "supplier": (
                        constraint.supplier.name if constraint.supplier else None
                    ),
                    "reference": constraint.reference,
                    "description": constraint.description,
                    "total_value": constraint.total_value,
                    "currency": constraint.currency,
                    "created_by": (
                        constraint.creator.username if constraint.creator else None
                    ),
                    "lines_count": len(constraint.constraint_lines),
                }
                result.append(constraint_data)

            return result

        except Exception as e:
            logger.error(f"خطأ في تقرير قيود المخازن: {str(e)}")
            raise

    def get_incoming_outgoing_summary(
        self, filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        تقرير ملخص الوارد والصادر

        Args:
            filters: فلاتر التقرير

        Returns:
            Dict: ملخص الوارد والصادر
        """
        try:
            base_query = self.db.query(WarehouseConstraint).filter(
                WarehouseConstraint.status == ConstraintStatus.POSTED
            )

            # تطبيق فلاتر التاريخ
            if filters:
                if "date_from" in filters:
                    base_query = base_query.filter(
                        WarehouseConstraint.posting_date >= filters["date_from"]
                    )
                if "date_to" in filters:
                    base_query = base_query.filter(
                        WarehouseConstraint.posting_date <= filters["date_to"]
                    )
                if "warehouse_id" in filters:
                    base_query = base_query.filter(
                        or_(
                            WarehouseConstraint.source_warehouse_id
                            == filters["warehouse_id"],
                            WarehouseConstraint.destination_warehouse_id
                            == filters["warehouse_id"],
                        )
                    )

            # حساب الوارد
            incoming_query = base_query.filter(
                WarehouseConstraint.constraint_type.in_(
                    [ConstraintType.INCOMING, ConstraintType.TRANSFER]
                )
            )
            incoming_total = (
                incoming_query.with_entities(
                    func.sum(WarehouseConstraint.total_value)
                ).scalar()
                or 0
            )
            incoming_count = incoming_query.count()

            # حساب الصادر
            outgoing_query = base_query.filter(
                WarehouseConstraint.constraint_type.in_(
                    [ConstraintType.OUTGOING, ConstraintType.TRANSFER]
                )
            )
            outgoing_total = (
                outgoing_query.with_entities(
                    func.sum(WarehouseConstraint.total_value)
                ).scalar()
                or 0
            )
            outgoing_count = outgoing_query.count()

            # حساب التسويات
            adjustment_query = base_query.filter(
                WarehouseConstraint.constraint_type == ConstraintType.ADJUSTMENT
            )
            adjustment_total = (
                adjustment_query.with_entities(
                    func.sum(WarehouseConstraint.total_value)
                ).scalar()
                or 0
            )
            adjustment_count = adjustment_query.count()

            # حساب المرتجعات
            return_query = base_query.filter(
                WarehouseConstraint.constraint_type == ConstraintType.RETURN
            )
            return_total = (
                return_query.with_entities(
                    func.sum(WarehouseConstraint.total_value)
                ).scalar()
                or 0
            )
            return_count = return_query.count()

            return {
                "incoming": {"total_value": incoming_total, "count": incoming_count},
                "outgoing": {"total_value": outgoing_total, "count": outgoing_count},
                "adjustments": {
                    "total_value": adjustment_total,
                    "count": adjustment_count,
                },
                "returns": {"total_value": return_total, "count": return_count},
                "net_movement": incoming_total - outgoing_total,
                "total_transactions": incoming_count
                + outgoing_count
                + adjustment_count
                + return_count,
            }

        except Exception as e:
            logger.error(f"خطأ في تقرير ملخص الوارد والصادر: {str(e)}")
            raise

    def get_warehouse_movement_report(
        self, warehouse_id: int, filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        تقرير حركة مخزن محدد

        Args:
            warehouse_id: معرف المخزن
            filters: فلاتر إضافية

        Returns:
            Dict: تقرير حركة المخزن
        """
        try:
            query = self.db.query(WarehouseConstraint).filter(
                and_(
                    or_(
                        WarehouseConstraint.source_warehouse_id == warehouse_id,
                        WarehouseConstraint.destination_warehouse_id == warehouse_id,
                    ),
                    WarehouseConstraint.status == ConstraintStatus.POSTED,
                )
            )

            # تطبيق فلاتر التاريخ
            if filters:
                if "date_from" in filters:
                    query = query.filter(
                        WarehouseConstraint.posting_date >= filters["date_from"]
                    )
                if "date_to" in filters:
                    query = query.filter(
                        WarehouseConstraint.posting_date <= filters["date_to"]
                    )

            constraints = query.order_by(desc(WarehouseConstraint.posting_date)).all()

            # تحليل الحركات
            incoming_movements = []
            outgoing_movements = []

            for constraint in constraints:
                movement_data = {
                    "constraint_number": constraint.constraint_number,
                    "constraint_type": constraint.constraint_type.value,
                    "posting_date": (
                        constraint.posting_date.isoformat()
                        if constraint.posting_date
                        else None
                    ),
                    "reference": constraint.reference,
                    "description": constraint.description,
                    "total_value": constraint.total_value,
                    "partner": (
                        constraint.customer.name
                        if constraint.customer
                        else (constraint.supplier.name if constraint.supplier else None)
                    ),
                }

                # تحديد نوع الحركة بالنسبة للمخزن
                if constraint.destination_warehouse_id == warehouse_id:
                    incoming_movements.append(movement_data)
                elif constraint.source_warehouse_id == warehouse_id:
                    outgoing_movements.append(movement_data)

            # حساب الإجماليات
            incoming_total = sum(m["total_value"] for m in incoming_movements)
            outgoing_total = sum(m["total_value"] for m in outgoing_movements)

            return {
                "warehouse_id": warehouse_id,
                "incoming_movements": incoming_movements,
                "outgoing_movements": outgoing_movements,
                "summary": {
                    "incoming_total": incoming_total,
                    "outgoing_total": outgoing_total,
                    "net_movement": incoming_total - outgoing_total,
                    "incoming_count": len(incoming_movements),
                    "outgoing_count": len(outgoing_movements),
                },
            }

        except Exception as e:
            logger.error(f"خطأ في تقرير حركة المخزن: {str(e)}")
            raise

    # ==================== الدوال المساعدة ====================

    def _generate_constraint_number(self, constraint_type: str) -> str:
        """توليد رقم قيد جديد"""
        try:
            # البحث عن آخر رقم
            last_constraint = (
                self.db.query(WarehouseConstraint)
                .filter(
                    WarehouseConstraint.constraint_type
                    == ConstraintType(constraint_type)
                )
                .order_by(desc(WarehouseConstraint.id))
                .first()
            )

            # تحديد البادئة حسب النوع
            prefixes = {
                "incoming": "IN",
                "outgoing": "OUT",
                "transfer": "TRF",
                "adjustment": "ADJ",
                "return": "RET",
            }

            prefix = prefixes.get(constraint_type, "CON")

            if last_constraint:
                # استخراج الرقم من آخر قيد
                last_number = last_constraint.constraint_number.split("-")[-1]
                try:
                    next_number = int(last_number) + 1
                except ValueError:
                    next_number = 1
            else:
                next_number = 1

            # تكوين الرقم الجديد
            today = datetime.now()
            return f"{prefix}-{today.year}{today.month:02d}-{next_number:06d}"

        except Exception as e:
            logger.error(f"خطأ في توليد رقم القيد: {str(e)}")
            # رقم احتياطي
            return f"CON-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def _check_approvals(self, constraint_id: int) -> bool:
        """التحقق من الموافقات المطلوبة"""
        try:
            pending_approvals = (
                self.db.query(WarehouseConstraintApproval)
                .filter(
                    and_(
                        WarehouseConstraintApproval.constraint_id == constraint_id,
                        WarehouseConstraintApproval.approval_status == "pending",
                    )
                )
                .count()
            )

            return pending_approvals == 0

        except Exception as e:
            logger.error(f"خطأ في التحقق من الموافقات: {str(e)}")
            return False

    def _apply_constraint_to_inventory(self, constraint: WarehouseConstraint):
        """تطبيق تأثير القيد على المخزون"""
        try:
            # هذه الدالة ستحتاج للتكامل مع نظام إدارة المخزون
            # لتطبيق التغييرات الفعلية على أرصدة المنتجات

            for line in constraint.constraint_lines:
                # تطبيق التغيير حسب نوع القيد
                if constraint.constraint_type == ConstraintType.INCOMING:
                    # زيادة المخزون في المخزن المستهدف
                    self._update_product_stock(
                        line.product_id,
                        constraint.destination_warehouse_id,
                        line.quantity,
                        "increase",
                    )
                elif constraint.constraint_type == ConstraintType.OUTGOING:
                    # تقليل المخزون من المخزن المصدر
                    self._update_product_stock(
                        line.product_id,
                        constraint.source_warehouse_id,
                        line.quantity,
                        "decrease",
                    )
                elif constraint.constraint_type == ConstraintType.TRANSFER:
                    # تقليل من المصدر وزيادة في المستهدف
                    self._update_product_stock(
                        line.product_id,
                        constraint.source_warehouse_id,
                        line.quantity,
                        "decrease",
                    )
                    self._update_product_stock(
                        line.product_id,
                        constraint.destination_warehouse_id,
                        line.quantity,
                        "increase",
                    )

            logger.info(
                f"تم تطبيق قيد المخزن على المخزون: {constraint.constraint_number}"
            )

        except Exception as e:
            logger.error(f"خطأ في تطبيق قيد المخزن على المخزون: {str(e)}")
            raise

    def _update_product_stock(
        self, product_id: int, warehouse_id: int, quantity: float, operation: str
    ):
        """تحديث رصيد منتج في مخزن محدد"""
        try:
            # هذه الدالة ستحتاج للتكامل مع نموذج أرصدة المنتجات
            # ProductStock أو ما يشابهه

            # مثال على التنفيذ (يحتاج للتعديل حسب النموذج الفعلي)
            """
            stock = self.db.query(ProductStock).filter(
                and_(
                    ProductStock.product_id == product_id,
                    ProductStock.warehouse_id == warehouse_id
                )
            ).first()

            if not stock:
                stock = ProductStock(
                    product_id=product_id,
                    warehouse_id=warehouse_id,
                    quantity=0
                )
                self.db.add(stock)

            if operation == 'increase':
                stock.quantity += quantity
            elif operation == 'decrease':
                stock.quantity -= quantity

            stock.last_updated = datetime.utcnow()
            """

            logger.info(
                f"تم تحديث رصيد المنتج {product_id} في المخزن {warehouse_id}: {operation} {quantity}"
            )

        except Exception as e:
            logger.error(f"خطأ في تحديث رصيد المنتج: {str(e)}")
            raise
