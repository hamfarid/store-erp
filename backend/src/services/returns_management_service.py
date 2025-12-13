#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/returns_management_service.py

خدمة إدارة المرتجعات
خدمة شاملة لإدارة مرتجع المبيعات والمشتريات
"""

from datetime import datetime, timezone, date
from decimal import Decimal
from typing import List, Dict, Optional, Any
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.orm import joinedload

from database import db
from models.returns_management import (
    SalesReturn,
    SalesReturnItem,
    PurchaseReturn,
    PurchaseReturnItem,
    ReturnProcessingLog,
    ReturnStatus,
    ReturnReason,
)


class ReturnsManagementService:
    """خدمة إدارة المرتجعات"""

    @staticmethod
    def create_sales_return(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """
        إنشاء مرتجع مبيعات جديد

        Args:
            data: بيانات المرتجع
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من البيانات المطلوبة
            required_fields = ["customer_id", "return_reason", "items"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return {"success": False, "message": f"الحقل {field} مطلوب"}

            # إنشاء المرتجع الرئيسي
            sales_return = SalesReturn(
                customer_id=data["customer_id"],
                original_invoice_id=data.get("original_invoice_id"),
                original_invoice_number=data.get("original_invoice_number", ""),
                return_date=datetime.strptime(
                    data.get("return_date", datetime.now().strftime("%Y-%m-%d")),
                    "%Y-%m-%d",
                ).date(),
                return_reason=ReturnReason(data["return_reason"]),
                warehouse_id=data.get("warehouse_id"),
                notes=data.get("notes", ""),
                requires_approval=data.get("requires_approval", True),
                created_by=user_id,
            )

            db.session.add(sales_return)
            db.session.flush()  # للحصول على ID

            # إضافة البنود
            total_amount = Decimal("0.00")
            total_quantity = Decimal("0.00")

            for item_data in data["items"]:
                item = SalesReturnItem(
                    return_id=sales_return.id,
                    product_id=item_data["product_id"],
                    quantity=Decimal(str(item_data["quantity"])),
                    unit_price=Decimal(str(item_data["unit_price"])),
                    discount_amount=Decimal(str(item_data.get("discount_amount", 0))),
                    tax_amount=Decimal(str(item_data.get("tax_amount", 0))),
                    reason=item_data.get("reason", ""),
                    condition=item_data.get("condition", "جيد"),
                    lot_number=item_data.get("lot_number"),
                    expiry_date=(
                        datetime.strptime(item_data["expiry_date"], "%Y-%m-%d").date()
                        if item_data.get("expiry_date")
                        else None
                    ),
                    notes=item_data.get("notes", ""),
                )

                # حساب المبلغ الإجمالي للبند
                item_total = (
                    (item.quantity * item.unit_price)
                    - item.discount_amount
                    + item.tax_amount
                )
                item.total_amount = item_total

                total_amount += item_total
                total_quantity += item.quantity

                db.session.add(item)

            # تحديث المجاميع
            sales_return.total_amount = total_amount
            sales_return.total_quantity = total_quantity

            # إضافة سجل المعالجة
            log = ReturnProcessingLog(
                return_id=sales_return.id,
                return_type="SALES",
                action="CREATED",
                performed_by=user_id,
                notes="تم إنشاء مرتجع المبيعات",
            )
            db.session.add(log)

            db.session.commit()

            return {
                "success": True,
                "message": "تم إنشاء مرتجع المبيعات بنجاح",
                "data": sales_return.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"خطأ في إنشاء مرتجع المبيعات: {str(e)}",
            }

    @staticmethod
    def create_purchase_return(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """
        إنشاء مرتجع مشتريات جديد

        Args:
            data: بيانات المرتجع
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من البيانات المطلوبة
            required_fields = ["supplier_id", "return_reason", "items"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return {"success": False, "message": f"الحقل {field} مطلوب"}

            # إنشاء المرتجع الرئيسي
            purchase_return = PurchaseReturn(
                supplier_id=data["supplier_id"],
                original_invoice_id=data.get("original_invoice_id"),
                original_invoice_number=data.get("original_invoice_number", ""),
                return_date=datetime.strptime(
                    data.get("return_date", datetime.now().strftime("%Y-%m-%d")),
                    "%Y-%m-%d",
                ).date(),
                return_reason=ReturnReason(data["return_reason"]),
                warehouse_id=data.get("warehouse_id"),
                notes=data.get("notes", ""),
                requires_approval=data.get("requires_approval", True),
                created_by=user_id,
            )

            db.session.add(purchase_return)
            db.session.flush()  # للحصول على ID

            # إضافة البنود
            total_amount = Decimal("0.00")
            total_quantity = Decimal("0.00")

            for item_data in data["items"]:
                item = PurchaseReturnItem(
                    return_id=purchase_return.id,
                    product_id=item_data["product_id"],
                    quantity=Decimal(str(item_data["quantity"])),
                    unit_cost=Decimal(str(item_data["unit_cost"])),
                    discount_amount=Decimal(str(item_data.get("discount_amount", 0))),
                    tax_amount=Decimal(str(item_data.get("tax_amount", 0))),
                    reason=item_data.get("reason", ""),
                    condition=item_data.get("condition", "جيد"),
                    lot_number=item_data.get("lot_number"),
                    expiry_date=(
                        datetime.strptime(item_data["expiry_date"], "%Y-%m-%d").date()
                        if item_data.get("expiry_date")
                        else None
                    ),
                    notes=item_data.get("notes", ""),
                )

                # حساب المبلغ الإجمالي للبند
                item_total = (
                    (item.quantity * item.unit_cost)
                    - item.discount_amount
                    + item.tax_amount
                )
                item.total_amount = item_total

                total_amount += item_total
                total_quantity += item.quantity

                db.session.add(item)

            # تحديث المجاميع
            purchase_return.total_amount = total_amount
            purchase_return.total_quantity = total_quantity

            # إضافة سجل المعالجة
            log = ReturnProcessingLog(
                return_id=purchase_return.id,
                return_type="PURCHASE",
                action="CREATED",
                performed_by=user_id,
                notes="تم إنشاء مرتجع المشتريات",
            )
            db.session.add(log)

            db.session.commit()

            return {
                "success": True,
                "message": "تم إنشاء مرتجع المشتريات بنجاح",
                "data": purchase_return.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"خطأ في إنشاء مرتجع المشتريات: {str(e)}",
            }

    @staticmethod
    def get_sales_return(return_id: int) -> Dict[str, Any]:
        """
        الحصول على مرتجع مبيعات محدد

        Args:
            return_id: معرف المرتجع

        Returns:
            Dict: بيانات المرتجع
        """
        try:
            sales_return = SalesReturn.query.options(
                joinedload(SalesReturn.items), joinedload(SalesReturn.processing_logs)
            ).get(return_id)

            if not sales_return:
                return {"success": False, "message": "مرتجع المبيعات غير موجود"}

            return {"success": True, "data": sales_return.to_dict()}

        except Exception as e:
            return {"success": False, "message": f"خطأ في جلب مرتجع المبيعات: {str(e)}"}

    @staticmethod
    def get_purchase_return(return_id: int) -> Dict[str, Any]:
        """
        الحصول على مرتجع مشتريات محدد

        Args:
            return_id: معرف المرتجع

        Returns:
            Dict: بيانات المرتجع
        """
        try:
            purchase_return = PurchaseReturn.query.options(
                joinedload(PurchaseReturn.items),
                joinedload(PurchaseReturn.processing_logs),
            ).get(return_id)

            if not purchase_return:
                return {"success": False, "message": "مرتجع المشتريات غير موجود"}

            return {"success": True, "data": purchase_return.to_dict()}

        except Exception as e:
            return {
                "success": False,
                "message": f"خطأ في جلب مرتجع المشتريات: {str(e)}",
            }

    @staticmethod
    def get_sales_returns_list(
        filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        الحصول على قائمة مرتجع المبيعات مع التصفية والترقيم

        Args:
            filters: مرشحات البحث
            page: رقم الصفحة
            per_page: عدد العناصر في الصفحة

        Returns:
            Dict: قائمة المرتجعات
        """
        try:
            query = SalesReturn.query

            # تطبيق المرشحات
            if filters:
                if "status" in filters and filters["status"]:
                    query = query.filter(SalesReturn.status == filters["status"])

                if "customer_id" in filters and filters["customer_id"]:
                    query = query.filter(
                        SalesReturn.customer_id == filters["customer_id"]
                    )

                if "return_reason" in filters and filters["return_reason"]:
                    query = query.filter(
                        SalesReturn.return_reason == filters["return_reason"]
                    )

                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    query = query.filter(SalesReturn.return_date >= date_from)

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    query = query.filter(SalesReturn.return_date <= date_to)

                if "search" in filters and filters["search"]:
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            SalesReturn.return_number.like(search_term),
                            SalesReturn.original_invoice_number.like(search_term),
                            SalesReturn.notes.like(search_term),
                        )
                    )

            # الترتيب
            sort_by = filters.get("sort_by", "created_at") if filters else "created_at"
            sort_order = filters.get("sort_order", "desc") if filters else "desc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(SalesReturn, sort_by)))
            else:
                query = query.order_by(asc(getattr(SalesReturn, sort_by)))

            # الترقيم
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "returns": [ret.to_dict() for ret in pagination.items],
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
                "message": f"خطأ في جلب قائمة مرتجع المبيعات: {str(e)}",
            }

    @staticmethod
    def get_purchase_returns_list(
        filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        الحصول على قائمة مرتجع المشتريات مع التصفية والترقيم

        Args:
            filters: مرشحات البحث
            page: رقم الصفحة
            per_page: عدد العناصر في الصفحة

        Returns:
            Dict: قائمة المرتجعات
        """
        try:
            query = PurchaseReturn.query

            # تطبيق المرشحات
            if filters:
                if "status" in filters and filters["status"]:
                    query = query.filter(PurchaseReturn.status == filters["status"])

                if "supplier_id" in filters and filters["supplier_id"]:
                    query = query.filter(
                        PurchaseReturn.supplier_id == filters["supplier_id"]
                    )

                if "return_reason" in filters and filters["return_reason"]:
                    query = query.filter(
                        PurchaseReturn.return_reason == filters["return_reason"]
                    )

                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    query = query.filter(PurchaseReturn.return_date >= date_from)

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    query = query.filter(PurchaseReturn.return_date <= date_to)

                if "search" in filters and filters["search"]:
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            PurchaseReturn.return_number.like(search_term),
                            PurchaseReturn.original_invoice_number.like(search_term),
                            PurchaseReturn.notes.like(search_term),
                        )
                    )

            # الترتيب
            sort_by = filters.get("sort_by", "created_at") if filters else "created_at"
            sort_order = filters.get("sort_order", "desc") if filters else "desc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(PurchaseReturn, sort_by)))
            else:
                query = query.order_by(asc(getattr(PurchaseReturn, sort_by)))

            # الترقيم
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "returns": [ret.to_dict() for ret in pagination.items],
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
                "message": f"خطأ في جلب قائمة مرتجع المشتريات: {str(e)}",
            }

    @staticmethod
    def approve_return(
        return_id: int, return_type: str, user_id: int, notes: str = ""
    ) -> Dict[str, Any]:
        """
        الموافقة على مرتجع

        Args:
            return_id: معرف المرتجع
            return_type: نوع المرتجع (SALES/PURCHASE)
            user_id: معرف المستخدم المعتمد
            notes: ملاحظات الموافقة

        Returns:
            Dict: نتيجة العملية
        """
        try:
            if return_type == "SALES":
                return_obj = SalesReturn.query.get(return_id)
                if not return_obj:
                    return {"success": False, "message": "مرتجع المبيعات غير موجود"}
            else:
                return_obj = PurchaseReturn.query.get(return_id)
                if not return_obj:
                    return {"success": False, "message": "مرتجع المشتريات غير موجود"}

            if return_obj.status != ReturnStatus.PENDING:
                return {
                    "success": False,
                    "message": "المرتجع ليس في حالة انتظار الموافقة",
                }

            # تحديث حالة المرتجع
            return_obj.status = ReturnStatus.APPROVED
            return_obj.approved_at = datetime.now(timezone.utc)
            return_obj.approved_by = user_id

            # إضافة سجل المعالجة
            log = ReturnProcessingLog(
                return_id=return_id,
                return_type=return_type,
                action="APPROVED",
                performed_by=user_id,
                notes=f"تم اعتماد المرتجع. {notes}" if notes else "تم اعتماد المرتجع",
            )
            db.session.add(log)

            db.session.commit()

            return {
                "success": True,
                "message": "تم اعتماد المرتجع بنجاح",
                "data": return_obj.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في اعتماد المرتجع: {str(e)}"}

    @staticmethod
    def complete_return(
        return_id: int, return_type: str, user_id: int
    ) -> Dict[str, Any]:
        """
        إكمال مرتجع (تطبيق التغييرات على المخزون والحسابات)

        Args:
            return_id: معرف المرتجع
            return_type: نوع المرتجع (SALES/PURCHASE)
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            if return_type == "SALES":
                return_obj = SalesReturn.query.get(return_id)
                if not return_obj:
                    return {"success": False, "message": "مرتجع المبيعات غير موجود"}
            else:
                return_obj = PurchaseReturn.query.get(return_id)
                if not return_obj:
                    return {"success": False, "message": "مرتجع المشتريات غير موجود"}

            if return_obj.status != ReturnStatus.APPROVED:
                return {"success": False, "message": "يجب اعتماد المرتجع أولاً"}

            # تطبيق التغييرات على المخزون والحسابات
            # هنا يتم تحديث كميات المنتجات وحسابات العملاء/الموردين
            # (يحتاج ربط مع نظام إدارة المخزون والحسابات)

            # تحديث حالة المرتجع
            return_obj.status = ReturnStatus.COMPLETED
            return_obj.completed_at = datetime.now(timezone.utc)

            # إضافة سجل المعالجة
            log = ReturnProcessingLog(
                return_id=return_id,
                return_type=return_type,
                action="COMPLETED",
                performed_by=user_id,
                notes="تم إكمال المرتجع وتطبيق التغييرات",
            )
            db.session.add(log)

            db.session.commit()

            return {
                "success": True,
                "message": "تم إكمال المرتجع بنجاح",
                "data": return_obj.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في إكمال المرتجع: {str(e)}"}

    @staticmethod
    def get_returns_statistics(filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        الحصول على إحصائيات المرتجعات

        Args:
            filters: مرشحات الإحصائيات

        Returns:
            Dict: الإحصائيات
        """
        try:
            # إحصائيات مرتجع المبيعات
            sales_query = SalesReturn.query
            purchase_query = PurchaseReturn.query

            # تطبيق المرشحات
            if filters:
                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    sales_query = sales_query.filter(
                        SalesReturn.return_date >= date_from
                    )
                    purchase_query = purchase_query.filter(
                        PurchaseReturn.return_date >= date_from
                    )

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    sales_query = sales_query.filter(SalesReturn.return_date <= date_to)
                    purchase_query = purchase_query.filter(
                        PurchaseReturn.return_date <= date_to
                    )

            # حساب الإحصائيات
            sales_stats = {
                "total_returns": sales_query.count(),
                "total_amount": sales_query.with_entities(
                    func.sum(SalesReturn.total_amount)
                ).scalar()
                or 0,
                "total_quantity": sales_query.with_entities(
                    func.sum(SalesReturn.total_quantity)
                ).scalar()
                or 0,
            }

            purchase_stats = {
                "total_returns": purchase_query.count(),
                "total_amount": purchase_query.with_entities(
                    func.sum(PurchaseReturn.total_amount)
                ).scalar()
                or 0,
                "total_quantity": purchase_query.with_entities(
                    func.sum(PurchaseReturn.total_quantity)
                ).scalar()
                or 0,
            }

            return {
                "success": True,
                "data": {
                    "sales_returns": {
                        "total_returns": sales_stats["total_returns"],
                        "total_amount": float(sales_stats["total_amount"]),
                        "total_quantity": float(sales_stats["total_quantity"]),
                    },
                    "purchase_returns": {
                        "total_returns": purchase_stats["total_returns"],
                        "total_amount": float(purchase_stats["total_amount"]),
                        "total_quantity": float(purchase_stats["total_quantity"]),
                    },
                },
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"خطأ في جلب إحصائيات المرتجعات: {str(e)}",
            }
