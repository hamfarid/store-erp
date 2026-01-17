#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/payment_debt_management_service.py

خدمة إدارة المدفوعات والمديونات
خدمة شاملة لإدارة أوامر الدفع والاستلام والمديونات
"""

from datetime import datetime, timezone, date, timedelta
from decimal import Decimal
from typing import List, Dict, Optional, Any
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.orm import joinedload

from database import db
from models.payment_management import (
    PaymentOrder,
    DebtRecord,
    DebtPayment,
    DebtFollowUp,
    PaymentProcessingLog,
    PaymentAttachment,
    BankAccount,
    PaymentType,
    PaymentStatus,
    DebtStatus,
    PaymentMethod,
)


class PaymentDebtManagementService:
    """خدمة إدارة المدفوعات والمديونات"""

    @staticmethod
    def create_payment_order(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """
        إنشاء أمر دفع أو استلام جديد

        Args:
            data: بيانات الأمر
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من البيانات المطلوبة
            required_fields = ["payment_type", "amount", "payment_method"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return {"success": False, "message": f"الحقل {field} مطلوب"}

            # إنشاء أمر الدفع
            payment_order = PaymentOrder(
                payment_type=PaymentType(data["payment_type"]),
                amount=Decimal(str(data["amount"])),
                currency=data.get("currency", "EGP"),
                payment_method=PaymentMethod(data["payment_method"]),
                order_date=datetime.strptime(
                    data.get("order_date", datetime.now().strftime("%Y-%m-%d")),
                    "%Y-%m-%d",
                ).date(),
                due_date=(
                    datetime.strptime(data["due_date"], "%Y-%m-%d").date()
                    if data.get("due_date")
                    else None
                ),
                counterpart_type=data.get("counterpart_type"),
                counterpart_id=data.get("counterpart_id"),
                counterpart_name=data.get("counterpart_name", ""),
                reference_type=data.get("reference_type"),
                reference_id=data.get("reference_id"),
                reference_number=data.get("reference_number", ""),
                description=data.get("description", ""),
                notes=data.get("notes", ""),
                bank_account_id=data.get("bank_account_id"),
                requires_approval=data.get("requires_approval", True),
                approval_level=data.get("approval_level", 1),
                created_by=user_id,
            )

            db.session.add(payment_order)
            db.session.flush()  # للحصول على ID

            # إضافة المرفقات إن وجدت
            if "attachments" in data:
                for attachment_data in data["attachments"]:
                    attachment = PaymentAttachment(
                        payment_order_id=payment_order.id,
                        file_name=attachment_data["file_name"],
                        file_path=attachment_data["file_path"],
                        file_size=attachment_data.get("file_size", 0),
                        file_type=attachment_data.get("file_type", ""),
                        description=attachment_data.get("description", ""),
                        uploaded_by=user_id,
                    )
                    db.session.add(attachment)

            # إضافة سجل المعالجة
            log = PaymentProcessingLog(
                payment_order_id=payment_order.id,
                action="CREATED",
                performed_by=user_id,
                notes="تم إنشاء أمر الدفع",
            )
            db.session.add(log)

            db.session.commit()

            return {
                "success": True,
                "message": "تم إنشاء أمر الدفع بنجاح",
                "data": payment_order.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في إنشاء أمر الدفع: {str(e)}"}

    @staticmethod
    def create_debt_record(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """
        إنشاء سجل مديونية جديد

        Args:
            data: بيانات المديونية
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من البيانات المطلوبة
            required_fields = ["debtor_type", "debtor_id", "original_amount"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return {"success": False, "message": f"الحقل {field} مطلوب"}

            # إنشاء سجل المديونية
            debt_record = DebtRecord(
                debtor_type=data["debtor_type"],
                debtor_id=data["debtor_id"],
                debtor_name=data.get("debtor_name", ""),
                original_amount=Decimal(str(data["original_amount"])),
                remaining_amount=Decimal(str(data["original_amount"])),
                # في البداية المبلغ المتبقي = المبلغ الأصلي
                currency=data.get("currency", "EGP"),
                debt_date=datetime.strptime(
                    data.get("debt_date", datetime.now().strftime("%Y-%m-%d")),
                    "%Y-%m-%d",
                ).date(),
                due_date=(
                    datetime.strptime(data["due_date"], "%Y-%m-%d").date()
                    if data.get("due_date")
                    else None
                ),
                reference_type=data.get("reference_type"),
                reference_id=data.get("reference_id"),
                reference_number=data.get("reference_number", ""),
                description=data.get("description", ""),
                notes=data.get("notes", ""),
                interest_rate=Decimal(str(data.get("interest_rate", 0))),
                late_fee_rate=Decimal(str(data.get("late_fee_rate", 0))),
                created_by=user_id,
            )

            db.session.add(debt_record)
            db.session.commit()

            return {
                "success": True,
                "message": "تم إنشاء سجل المديونية بنجاح",
                "data": debt_record.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"خطأ في إنشاء سجل المديونية: {str(e)}",
            }

    @staticmethod
    def create_debt_payment(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """
        إنشاء دفعة مديونية جديدة

        Args:
            data: بيانات الدفعة
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من البيانات المطلوبة
            required_fields = ["debt_record_id", "payment_amount", "payment_method"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return {"success": False, "message": f"الحقل {field} مطلوب"}

            # التحقق من وجود سجل المديونية
            debt_record = DebtRecord.query.get(data["debt_record_id"])
            if not debt_record:
                return {"success": False, "message": "سجل المديونية غير موجود"}

            payment_amount = Decimal(str(data["payment_amount"]))

            # التحقق من أن مبلغ الدفعة لا يتجاوز المبلغ المتبقي
            if payment_amount > debt_record.remaining_amount:
                return {
                    "success": False,
                    "message": "مبلغ الدفعة يتجاوز المبلغ المتبقي",
                }

            # إنشاء دفعة المديونية
            debt_payment = DebtPayment(
                debt_record_id=data["debt_record_id"],
                payment_amount=payment_amount,
                payment_method=PaymentMethod(data["payment_method"]),
                payment_date=datetime.strptime(
                    data.get("payment_date", datetime.now().strftime("%Y-%m-%d")),
                    "%Y-%m-%d",
                ).date(),
                reference_number=data.get("reference_number", ""),
                notes=data.get("notes", ""),
                bank_account_id=data.get("bank_account_id"),
                processed_by=user_id,
            )

            db.session.add(debt_payment)

            # تحديث المبلغ المتبقي في سجل المديونية
            debt_record.remaining_amount -= payment_amount
            debt_record.last_payment_date = debt_payment.payment_date

            # تحديث حالة المديونية
            if debt_record.remaining_amount <= 0:
                debt_record.status = DebtStatus.PAID
                debt_record.paid_at = datetime.now(timezone.utc)
            elif debt_record.remaining_amount < debt_record.original_amount:
                debt_record.status = DebtStatus.PARTIALLY_PAID

            db.session.commit()

            return {
                "success": True,
                "message": "تم إنشاء دفعة المديونية بنجاح",
                "data": {
                    "payment": debt_payment.to_dict(),
                    "debt_record": debt_record.to_dict(),
                },
            }

        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"خطأ في إنشاء دفعة المديونية: {str(e)}",
            }

    @staticmethod
    def get_payment_orders_list(
        filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        الحصول على قائمة أوامر الدفع مع التصفية والترقيم

        Args:
            filters: مرشحات البحث
            page: رقم الصفحة
            per_page: عدد العناصر في الصفحة

        Returns:
            Dict: قائمة الأوامر
        """
        try:
            query = PaymentOrder.query

            # تطبيق المرشحات
            if filters:
                if "payment_type" in filters and filters["payment_type"]:
                    query = query.filter(
                        PaymentOrder.payment_type == filters["payment_type"]
                    )

                if "status" in filters and filters["status"]:
                    query = query.filter(PaymentOrder.status == filters["status"])

                if "payment_method" in filters and filters["payment_method"]:
                    query = query.filter(
                        PaymentOrder.payment_method == filters["payment_method"]
                    )

                if "counterpart_type" in filters and filters["counterpart_type"]:
                    query = query.filter(
                        PaymentOrder.counterpart_type == filters["counterpart_type"]
                    )

                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    query = query.filter(PaymentOrder.order_date >= date_from)

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    query = query.filter(PaymentOrder.order_date <= date_to)

                if "search" in filters and filters["search"]:
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            PaymentOrder.order_number.like(search_term),
                            PaymentOrder.counterpart_name.like(search_term),
                            PaymentOrder.description.like(search_term),
                        )
                    )

            # الترتيب
            sort_by = filters.get("sort_by", "created_at") if filters else "created_at"
            sort_order = filters.get("sort_order", "desc") if filters else "desc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(PaymentOrder, sort_by)))
            else:
                query = query.order_by(asc(getattr(PaymentOrder, sort_by)))

            # الترقيم
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "payment_orders": [order.to_dict() for order in pagination.items],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": pagination.total,
                        "pages": pagination.pages,
                        "has_next": pagination.has_next,
                        "has_prev": pagination.has_prev,
                    },
                },
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"خطأ في جلب قائمة أوامر الدفع: {str(e)}",
            }

    @staticmethod
    def get_debt_records_list(
        filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        الحصول على قائمة سجلات المديونيات مع التصفية والترقيم

        Args:
            filters: مرشحات البحث
            page: رقم الصفحة
            per_page: عدد العناصر في الصفحة

        Returns:
            Dict: قائمة المديونيات
        """
        try:
            query = DebtRecord.query

            # تطبيق المرشحات
            if filters:
                if "status" in filters and filters["status"]:
                    query = query.filter(DebtRecord.status == filters["status"])

                if "debtor_type" in filters and filters["debtor_type"]:
                    query = query.filter(
                        DebtRecord.debtor_type == filters["debtor_type"]
                    )

                if "debtor_id" in filters and filters["debtor_id"]:
                    query = query.filter(DebtRecord.debtor_id == filters["debtor_id"])

                if "overdue_only" in filters and filters["overdue_only"]:
                    today = date.today()
                    query = query.filter(
                        and_(
                            DebtRecord.due_date < today,
                            DebtRecord.status != DebtStatus.PAID,
                        )
                    )

                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    query = query.filter(DebtRecord.debt_date >= date_from)

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    query = query.filter(DebtRecord.debt_date <= date_to)

                if "search" in filters and filters["search"]:
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            DebtRecord.debt_number.like(search_term),
                            DebtRecord.debtor_name.like(search_term),
                            DebtRecord.description.like(search_term),
                        )
                    )

            # الترتيب
            sort_by = filters.get("sort_by", "created_at") if filters else "created_at"
            sort_order = filters.get("sort_order", "desc") if filters else "desc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(DebtRecord, sort_by)))
            else:
                query = query.order_by(asc(getattr(DebtRecord, sort_by)))

            # الترقيم
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "debt_records": [debt.to_dict() for debt in pagination.items],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": pagination.total,
                        "pages": pagination.pages,
                        "has_next": pagination.has_next,
                        "has_prev": pagination.has_prev,
                    },
                },
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"خطأ في جلب قائمة المديونيات: {str(e)}",
            }

    @staticmethod
    def approve_payment_order(
        order_id: int, user_id: int, notes: str = ""
    ) -> Dict[str, Any]:
        """
        الموافقة على أمر دفع

        Args:
            order_id: معرف الأمر
            user_id: معرف المستخدم المعتمد
            notes: ملاحظات الموافقة

        Returns:
            Dict: نتيجة العملية
        """
        try:
            payment_order = PaymentOrder.query.get(order_id)
            if not payment_order:
                return {"success": False, "message": "أمر الدفع غير موجود"}

            if payment_order.status != PaymentStatus.PENDING:
                return {
                    "success": False,
                    "message": "أمر الدفع ليس في حالة انتظار الموافقة",
                }

            # تحديث حالة الأمر
            payment_order.status = PaymentStatus.APPROVED
            payment_order.approved_at = datetime.now(timezone.utc)
            payment_order.approved_by = user_id

            # إضافة سجل المعالجة
            log = PaymentProcessingLog(
                payment_order_id=order_id,
                action="APPROVED",
                performed_by=user_id,
                notes=(
                    f"تم اعتماد أمر الدفع. {notes}" if notes else "تم اعتماد أمر الدفع"
                ),
            )
            db.session.add(log)

            db.session.commit()

            return {
                "success": True,
                "message": "تم اعتماد أمر الدفع بنجاح",
                "data": payment_order.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في اعتماد أمر الدفع: {str(e)}"}

    @staticmethod
    def get_debt_statistics(filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        الحصول على إحصائيات المديونيات

        Args:
            filters: مرشحات الإحصائيات

        Returns:
            Dict: الإحصائيات
        """
        try:
            query = DebtRecord.query

            # تطبيق المرشحات
            if filters:
                if "debtor_type" in filters and filters["debtor_type"]:
                    query = query.filter(
                        DebtRecord.debtor_type == filters["debtor_type"]
                    )

                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    query = query.filter(DebtRecord.debt_date >= date_from)

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    query = query.filter(DebtRecord.debt_date <= date_to)

            # حساب الإحصائيات
            total_debts = query.count()
            total_original_amount = (
                query.with_entities(func.sum(DebtRecord.original_amount)).scalar() or 0
            )
            total_remaining_amount = (
                query.with_entities(func.sum(DebtRecord.remaining_amount)).scalar() or 0
            )
            total_paid_amount = total_original_amount - total_remaining_amount

            # المديونيات المتأخرة
            today = date.today()
            overdue_debts = query.filter(
                and_(DebtRecord.due_date < today, DebtRecord.status != DebtStatus.PAID)
            ).count()

            overdue_amount = (
                query.filter(
                    and_(
                        DebtRecord.due_date < today,
                        DebtRecord.status != DebtStatus.PAID,
                    )
                )
                .with_entities(func.sum(DebtRecord.remaining_amount))
                .scalar()
                or 0
            )

            # إحصائيات حسب الحالة
            status_stats = (
                db.session.query(
                    DebtRecord.status,
                    func.count(DebtRecord.id).label("count"),
                    func.sum(DebtRecord.remaining_amount).label("total_amount"),
                )
                .filter(query.whereclause if query.whereclause is not None else True)
                .group_by(DebtRecord.status)
                .all()
            )

            return {
                "success": True,
                "data": {
                    "total_debts": total_debts,
                    "total_original_amount": float(total_original_amount),
                    "total_remaining_amount": float(total_remaining_amount),
                    "total_paid_amount": float(total_paid_amount),
                    "overdue_debts": overdue_debts,
                    "overdue_amount": float(overdue_amount),
                    "payment_rate": float(
                        (total_paid_amount / total_original_amount * 100)
                        if total_original_amount > 0
                        else 0
                    ),
                    "status_statistics": [
                        {
                            "status": stat.status.value if stat.status else "غير محدد",
                            "count": stat.count,
                            "total_amount": float(stat.total_amount or 0),
                        }
                        for stat in status_stats
                    ],
                },
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"خطأ في جلب إحصائيات المديونيات: {str(e)}",
            }
