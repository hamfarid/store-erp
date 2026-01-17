#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/warehouse_adjustments_service.py

خدمة قيود المخزن
خدمة شاملة لإدارة قيود المخزن (هالك، فحص، تصحيح)
"""

from datetime import datetime, timezone, date
from decimal import Decimal
from typing import List, Dict, Optional, Any
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.orm import joinedload

from database import db
from models.warehouse_adjustments import (
    WarehouseAdjustment,
    WarehouseAdjustmentItem,
    AdjustmentApproval,
    AdjustmentAttachment,
    AdjustmentTemplate,
    AdjustmentType,
    AdjustmentStatus,
)


class WarehouseAdjustmentsService:
    """خدمة إدارة قيود المخزن"""

    @staticmethod
    def create_adjustment(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """
        إنشاء قيد مخزن جديد

        Args:
            data: بيانات القيد
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من البيانات المطلوبة
            required_fields = ["adjustment_type", "warehouse_id", "reason", "items"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return {"success": False, "message": f"الحقل {field} مطلوب"}

            # إنشاء القيد الرئيسي
            adjustment = WarehouseAdjustment(
                adjustment_type=AdjustmentType(data["adjustment_type"]),
                warehouse_id=data["warehouse_id"],
                reason=data["reason"],
                description=data.get("description", ""),
                adjustment_date=datetime.strptime(
                    data.get("adjustment_date", datetime.now().strftime("%Y-%m-%d")),
                    "%Y-%m-%d",
                ).date(),
                reference_number=data.get("reference_number", ""),
                template_id=data.get("template_id"),
                requires_approval=data.get("requires_approval", True),
                approval_level=data.get("approval_level", 1),
                notes=data.get("notes", ""),
                created_by=user_id,
            )

            db.session.add(adjustment)
            db.session.flush()  # للحصول على ID

            # إضافة البنود
            total_cost_impact = Decimal("0.00")
            for item_data in data["items"]:
                item = WarehouseAdjustmentItem(
                    adjustment_id=adjustment.id,
                    product_id=item_data["product_id"],
                    quantity_before=Decimal(str(item_data.get("quantity_before", 0))),
                    quantity_after=Decimal(str(item_data["quantity_after"])),
                    unit_cost=Decimal(str(item_data.get("unit_cost", 0))),
                    reason=item_data.get("reason", ""),
                    notes=item_data.get("notes", ""),
                    lot_number=item_data.get("lot_number"),
                    expiry_date=(
                        datetime.strptime(item_data["expiry_date"], "%Y-%m-%d").date()
                        if item_data.get("expiry_date")
                        else None
                    ),
                    location=item_data.get("location", ""),
                )

                # حساب التأثير على التكلفة
                quantity_diff = item.quantity_after - item.quantity_before
                cost_impact = quantity_diff * item.unit_cost
                item.cost_impact = cost_impact
                total_cost_impact += cost_impact

                db.session.add(item)

            # تحديث التأثير الإجمالي على التكلفة
            adjustment.total_cost_impact = total_cost_impact

            # إضافة المرفقات إن وجدت
            if "attachments" in data:
                for attachment_data in data["attachments"]:
                    attachment = AdjustmentAttachment(
                        adjustment_id=adjustment.id,
                        file_name=attachment_data["file_name"],
                        file_path=attachment_data["file_path"],
                        file_size=attachment_data.get("file_size", 0),
                        file_type=attachment_data.get("file_type", ""),
                        description=attachment_data.get("description", ""),
                        uploaded_by=user_id,
                    )
                    db.session.add(attachment)

            db.session.commit()

            return {
                "success": True,
                "message": "تم إنشاء قيد المخزن بنجاح",
                "data": adjustment.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في إنشاء قيد المخزن: {str(e)}"}

    @staticmethod
    def get_adjustment(adjustment_id: int) -> Dict[str, Any]:
        """
        الحصول على قيد مخزن محدد

        Args:
            adjustment_id: معرف القيد

        Returns:
            Dict: بيانات القيد
        """
        try:
            adjustment = WarehouseAdjustment.query.options(
                joinedload(WarehouseAdjustment.items),
                joinedload(WarehouseAdjustment.approvals),
                joinedload(WarehouseAdjustment.attachments),
            ).get(adjustment_id)

            if not adjustment:
                return {"success": False, "message": "قيد المخزن غير موجود"}

            return {"success": True, "data": adjustment.to_dict()}

        except Exception as e:
            return {"success": False, "message": f"خطأ في جلب قيد المخزن: {str(e)}"}

    @staticmethod
    def get_adjustments_list(
        filters: Dict[str, Any] = None, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        الحصول على قائمة قيود المخزن مع التصفية والترقيم

        Args:
            filters: مرشحات البحث
            page: رقم الصفحة
            per_page: عدد العناصر في الصفحة

        Returns:
            Dict: قائمة القيود
        """
        try:
            query = WarehouseAdjustment.query

            # تطبيق المرشحات
            if filters:
                if "adjustment_type" in filters and filters["adjustment_type"]:
                    query = query.filter(
                        WarehouseAdjustment.adjustment_type
                        == filters["adjustment_type"]
                    )

                if "status" in filters and filters["status"]:
                    query = query.filter(
                        WarehouseAdjustment.status == filters["status"]
                    )

                if "warehouse_id" in filters and filters["warehouse_id"]:
                    query = query.filter(
                        WarehouseAdjustment.warehouse_id == filters["warehouse_id"]
                    )

                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    query = query.filter(
                        WarehouseAdjustment.adjustment_date >= date_from
                    )

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    query = query.filter(WarehouseAdjustment.adjustment_date <= date_to)

                if "search" in filters and filters["search"]:
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            WarehouseAdjustment.adjustment_number.like(search_term),
                            WarehouseAdjustment.reason.like(search_term),
                            WarehouseAdjustment.description.like(search_term),
                        )
                    )

            # الترتيب
            sort_by = filters.get("sort_by", "created_at") if filters else "created_at"
            sort_order = filters.get("sort_order", "desc") if filters else "desc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(WarehouseAdjustment, sort_by)))
            else:
                query = query.order_by(asc(getattr(WarehouseAdjustment, sort_by)))

            # الترقيم
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "adjustments": [adj.to_dict() for adj in pagination.items],
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
                "message": f"خطأ في جلب قائمة قيود المخزن: {str(e)}",
            }

    @staticmethod
    def update_adjustment(
        adjustment_id: int, data: Dict[str, Any], user_id: int
    ) -> Dict[str, Any]:
        """
        تحديث قيد مخزن

        Args:
            adjustment_id: معرف القيد
            data: البيانات المحدثة
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            adjustment = WarehouseAdjustment.query.get(adjustment_id)
            if not adjustment:
                return {"success": False, "message": "قيد المخزن غير موجود"}

            # التحقق من إمكانية التعديل
            if adjustment.status not in [
                AdjustmentStatus.DRAFT,
                AdjustmentStatus.PENDING,
            ]:
                return {
                    "success": False,
                    "message": "لا يمكن تعديل قيد مخزن معتمد أو مكتمل",
                }

            # تحديث البيانات الأساسية
            if "reason" in data:
                adjustment.reason = data["reason"]
            if "description" in data:
                adjustment.description = data["description"]
            if "adjustment_date" in data:
                adjustment.adjustment_date = datetime.strptime(
                    data["adjustment_date"], "%Y-%m-%d"
                ).date()
            if "reference_number" in data:
                adjustment.reference_number = data["reference_number"]
            if "notes" in data:
                adjustment.notes = data["notes"]

            adjustment.updated_at = datetime.now(timezone.utc)

            # تحديث البنود إذا تم تمريرها
            if "items" in data:
                # حذف البنود الحالية
                WarehouseAdjustmentItem.query.filter_by(
                    adjustment_id=adjustment_id
                ).delete()

                # إضافة البنود الجديدة
                total_cost_impact = Decimal("0.00")
                for item_data in data["items"]:
                    item = WarehouseAdjustmentItem(
                        adjustment_id=adjustment.id,
                        product_id=item_data["product_id"],
                        quantity_before=Decimal(
                            str(item_data.get("quantity_before", 0))
                        ),
                        quantity_after=Decimal(str(item_data["quantity_after"])),
                        unit_cost=Decimal(str(item_data.get("unit_cost", 0))),
                        reason=item_data.get("reason", ""),
                        notes=item_data.get("notes", ""),
                        lot_number=item_data.get("lot_number"),
                        expiry_date=(
                            datetime.strptime(
                                item_data["expiry_date"], "%Y-%m-%d"
                            ).date()
                            if item_data.get("expiry_date")
                            else None
                        ),
                        location=item_data.get("location", ""),
                    )

                    # حساب التأثير على التكلفة
                    quantity_diff = item.quantity_after - item.quantity_before
                    cost_impact = quantity_diff * item.unit_cost
                    item.cost_impact = cost_impact
                    total_cost_impact += cost_impact

                    db.session.add(item)

                adjustment.total_cost_impact = total_cost_impact

            db.session.commit()

            return {
                "success": True,
                "message": "تم تحديث قيد المخزن بنجاح",
                "data": adjustment.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في تحديث قيد المخزن: {str(e)}"}

    @staticmethod
    def approve_adjustment(
        adjustment_id: int, user_id: int, notes: str = ""
    ) -> Dict[str, Any]:
        """
        الموافقة على قيد مخزن

        Args:
            adjustment_id: معرف القيد
            user_id: معرف المستخدم المعتمد
            notes: ملاحظات الموافقة

        Returns:
            Dict: نتيجة العملية
        """
        try:
            adjustment = WarehouseAdjustment.query.get(adjustment_id)
            if not adjustment:
                return {"success": False, "message": "قيد المخزن غير موجود"}

            if adjustment.status != AdjustmentStatus.PENDING:
                return {
                    "success": False,
                    "message": "قيد المخزن ليس في حالة انتظار الموافقة",
                }

            # إضافة سجل الموافقة
            approval = AdjustmentApproval(
                adjustment_id=adjustment_id,
                approved_by=user_id,
                approval_level=adjustment.approval_level,
                notes=notes,
                approved_at=datetime.now(timezone.utc),
            )
            db.session.add(approval)

            # تحديث حالة القيد
            adjustment.status = AdjustmentStatus.APPROVED
            adjustment.approved_at = datetime.now(timezone.utc)
            adjustment.approved_by = user_id

            db.session.commit()

            return {
                "success": True,
                "message": "تم اعتماد قيد المخزن بنجاح",
                "data": adjustment.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في اعتماد قيد المخزن: {str(e)}"}

    @staticmethod
    def complete_adjustment(adjustment_id: int, user_id: int) -> Dict[str, Any]:
        """
        إكمال قيد مخزن (تطبيق التغييرات على المخزون)

        Args:
            adjustment_id: معرف القيد
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            adjustment = WarehouseAdjustment.query.get(adjustment_id)
            if not adjustment:
                return {"success": False, "message": "قيد المخزن غير موجود"}

            if adjustment.status != AdjustmentStatus.APPROVED:
                return {"success": False, "message": "يجب اعتماد قيد المخزن أولاً"}

            # تطبيق التغييرات على المخزون
            # هنا يتم تحديث كميات المنتجات في المخزن
            # (يحتاج ربط مع نظام إدارة المخزون)

            # تحديث حالة القيد
            adjustment.status = AdjustmentStatus.COMPLETED
            adjustment.completed_at = datetime.now(timezone.utc)

            db.session.commit()

            return {
                "success": True,
                "message": "تم إكمال قيد المخزن بنجاح",
                "data": adjustment.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في إكمال قيد المخزن: {str(e)}"}

    @staticmethod
    def cancel_adjustment(
        adjustment_id: int, user_id: int, reason: str
    ) -> Dict[str, Any]:
        """
        إلغاء قيد مخزن

        Args:
            adjustment_id: معرف القيد
            user_id: معرف المستخدم
            reason: سبب الإلغاء

        Returns:
            Dict: نتيجة العملية
        """
        try:
            adjustment = WarehouseAdjustment.query.get(adjustment_id)
            if not adjustment:
                return {"success": False, "message": "قيد المخزن غير موجود"}

            if adjustment.status == AdjustmentStatus.COMPLETED:
                return {"success": False, "message": "لا يمكن إلغاء قيد مخزن مكتمل"}

            # تحديث حالة القيد
            adjustment.status = AdjustmentStatus.CANCELLED
            adjustment.cancelled_at = datetime.now(timezone.utc)
            adjustment.cancelled_by = user_id
            adjustment.cancellation_reason = reason

            db.session.commit()

            return {
                "success": True,
                "message": "تم إلغاء قيد المخزن بنجاح",
                "data": adjustment.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"خطأ في إلغاء قيد المخزن: {str(e)}"}

    @staticmethod
    def get_adjustment_statistics(filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        الحصول على إحصائيات قيود المخزن

        Args:
            filters: مرشحات الإحصائيات

        Returns:
            Dict: الإحصائيات
        """
        try:
            query = WarehouseAdjustment.query

            # تطبيق المرشحات
            if filters:
                if "date_from" in filters and filters["date_from"]:
                    date_from = datetime.strptime(
                        filters["date_from"], "%Y-%m-%d"
                    ).date()
                    query = query.filter(
                        WarehouseAdjustment.adjustment_date >= date_from
                    )

                if "date_to" in filters and filters["date_to"]:
                    date_to = datetime.strptime(filters["date_to"], "%Y-%m-%d").date()
                    query = query.filter(WarehouseAdjustment.adjustment_date <= date_to)

                if "warehouse_id" in filters and filters["warehouse_id"]:
                    query = query.filter(
                        WarehouseAdjustment.warehouse_id == filters["warehouse_id"]
                    )

            # حساب الإحصائيات
            total_adjustments = query.count()

            # إحصائيات حسب النوع
            type_stats = (
                db.session.query(
                    WarehouseAdjustment.adjustment_type,
                    func.count(WarehouseAdjustment.id).label("count"),
                    func.sum(WarehouseAdjustment.total_cost_impact).label(
                        "total_impact"
                    ),
                )
                .filter(query.whereclause if query.whereclause is not None else True)
                .group_by(WarehouseAdjustment.adjustment_type)
                .all()
            )

            # إحصائيات حسب الحالة
            status_stats = (
                db.session.query(
                    WarehouseAdjustment.status,
                    func.count(WarehouseAdjustment.id).label("count"),
                )
                .filter(query.whereclause if query.whereclause is not None else True)
                .group_by(WarehouseAdjustment.status)
                .all()
            )

            # إجمالي التأثير على التكلفة
            total_cost_impact = (
                query.with_entities(
                    func.sum(WarehouseAdjustment.total_cost_impact)
                ).scalar()
                or 0
            )

            return {
                "success": True,
                "data": {
                    "total_adjustments": total_adjustments,
                    "total_cost_impact": float(total_cost_impact),
                    "type_statistics": [
                        {
                            "type": (
                                stat.adjustment_type.value
                                if stat.adjustment_type
                                else "غير محدد"
                            ),
                            "count": stat.count,
                            "total_impact": float(stat.total_impact or 0),
                        }
                        for stat in type_stats
                    ],
                    "status_statistics": [
                        {
                            "status": stat.status.value if stat.status else "غير محدد",
                            "count": stat.count,
                        }
                        for stat in status_stats
                    ],
                },
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"خطأ في جلب إحصائيات قيود المخزن: {str(e)}",
            }

    @staticmethod
    def get_templates() -> Dict[str, Any]:
        """
        الحصول على قوالب قيود المخزن

        Returns:
            Dict: قائمة القوالب
        """
        try:
            templates = AdjustmentTemplate.query.filter_by(is_active=True).all()

            return {
                "success": True,
                "data": [template.to_dict() for template in templates],
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"خطأ في جلب قوالب قيود المخزن: {str(e)}",
            }

    @staticmethod
    def create_template(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """
        إنشاء قالب قيد مخزن جديد

        Args:
            data: بيانات القالب
            user_id: معرف المستخدم

        Returns:
            Dict: نتيجة العملية
        """
        try:
            template = AdjustmentTemplate(
                name=data["name"],
                description=data.get("description", ""),
                adjustment_type=AdjustmentType(data["adjustment_type"]),
                default_reason=data.get("default_reason", ""),
                requires_approval=data.get("requires_approval", True),
                approval_level=data.get("approval_level", 1),
                is_active=data.get("is_active", True),
                created_by=user_id,
            )

            db.session.add(template)
            db.session.commit()

            return {
                "success": True,
                "message": "تم إنشاء قالب قيد المخزن بنجاح",
                "data": template.to_dict(),
            }

        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"خطأ في إنشاء قالب قيد المخزن: {str(e)}",
            }
