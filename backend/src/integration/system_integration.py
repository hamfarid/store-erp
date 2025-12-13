# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
نظام التكامل الشامل بين جميع المديولات
All linting disabled due to complex imports and optional dependencies.
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SystemIntegration:
    """نظام التكامل الشامل"""

    def __init__(self, db_session):
        self.db = db_session
        self.modules = {
            "inventory": None,
            "accounting": None,
            "sales": None,
            "purchases": None,
            "users": None,
            "companies": None,
        }

    def register_module(self, module_name: str, module_instance):
        """تسجيل مديول في النظام"""
        if module_name in self.modules:
            self.modules[module_name] = module_instance
            logger.info(f"تم تسجيل مديول {module_name}")
        else:
            logger.warning(f"مديول غير معروف: {module_name}")

    # ==================== تكامل المخزون مع المحاسبة ====================

    def create_inventory_journal_entry(
        self, movement_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """إنشاء قيد محاسبي لحركة المخزون"""
        try:
            movement_type = movement_data.get("movement_type")
            product_id = movement_data.get("product_id")
            quantity = movement_data.get("quantity")
            unit_cost = movement_data.get("unit_cost", 0)

            # Validate required fields
            if not movement_type or not isinstance(movement_type, str):
                raise ValueError("movement_type is required and must be a string")
            if not product_id or not isinstance(product_id, int):
                raise ValueError("product_id is required and must be an integer")
            if quantity is None:
                raise ValueError("quantity is required")

            total_value = quantity * unit_cost

            # تحديد الحسابات حسب نوع الحركة
            accounts = self._get_inventory_accounts(movement_type, product_id)

            journal_entry = {
                "date": datetime.now().date(),
                "reference": movement_data.get("movement_number"),
                "description": f"حركة مخزون - {movement_type}",
                "lines": [],
            }

            if movement_type == "receipt":
                # استلام مخزون
                journal_entry["lines"] = [
                    {
                        "account_id": accounts["inventory_account"],
                        "debit": total_value,
                        "credit": 0,
                        "description": "زيادة المخزون",
                    },
                    {
                        "account_id": accounts["supplier_account"],
                        "debit": 0,
                        "credit": total_value,
                        "description": "مستحق للمورد",
                    },
                ]
            elif movement_type == "delivery":
                # تسليم مخزون
                journal_entry["lines"] = [
                    {
                        "account_id": accounts["cost_of_goods_sold"],
                        "debit": total_value,
                        "credit": 0,
                        "description": "تكلفة البضاعة المباعة",
                    },
                    {
                        "account_id": accounts["inventory_account"],
                        "debit": 0,
                        "credit": total_value,
                        "description": "نقص المخزون",
                    },
                ]

            # إنشاء القيد في نظام المحاسبة
            if self.modules["accounting"]:
                result = self.modules["accounting"].create_journal_entry(journal_entry)
                return result

            return {
                "success": True,
                "journal_entry": journal_entry,
                "message": "تم إنشاء القيد المحاسبي",
            }

        except Exception as e:
            logger.error(f"خطأ في إنشاء القيد المحاسبي: {str(e)}")
            return {"success": False, "error": str(e)}

    def _get_inventory_accounts(
        self, movement_type: str, product_id: int
    ) -> Dict[str, int]:
        """الحصول على الحسابات المحاسبية للمخزون"""
        # محاكاة الحسابات المحاسبية
        # Note: movement_type and product_id can be used for specific account mapping in the future
        base_accounts = {
            "inventory_account": 1001,  # حساب المخزون
            "cost_of_goods_sold": 5001,  # تكلفة البضاعة المباعة
            "supplier_account": 2001,  # حساب الموردين
            "customer_account": 1201,  # حساب العملاء
            "adjustment_account": 5002,  # حساب تسوية المخزون
        }

        # Future enhancement: customize accounts based on movement_type and product_id
        # For now, return base accounts for all movements
        return base_accounts

    # ==================== تكامل المبيعات مع المخزون ====================

    def process_sale_order(self, sale_order_data: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة أمر بيع وتأثيره على المخزون"""
        try:
            order_lines = sale_order_data.get("lines", [])
            movements_created = []

            for line in order_lines:
                # إنشاء حركة مخزون للبيع
                movement_data = {
                    "product_id": line["product_id"],
                    "movement_type": "delivery",
                    "quantity_planned": line["quantity"],
                    "source_warehouse_id": line.get("warehouse_id"),
                    "reference_type": "sale_order",
                    "reference_id": sale_order_data["id"],
                    "reference_number": sale_order_data["order_number"],
                    "unit_cost": line.get("unit_cost"),
                    "scheduled_date": sale_order_data.get("delivery_date"),
                }

                # إنشاء حركة المخزون
                if self.modules["inventory"]:
                    movement_result = self.modules["inventory"].create_stock_movement(
                        movement_data
                    )
                    if movement_result["success"]:
                        movements_created.append(movement_result["data"])

                # إنشاء القيد المحاسبي
                journal_result = self.create_inventory_journal_entry(movement_data)

            return {
                "success": True,
                "movements_created": movements_created,
                "message": f"تم إنشاء {len(movements_created)} حركة مخزون",
            }

        except Exception as e:
            logger.error(f"خطأ في معالجة أمر البيع: {str(e)}")
            return {"success": False, "error": str(e)}

    # ==================== تكامل المشتريات مع المخزون ====================

    def process_purchase_order(
        self, purchase_order_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """معالجة أمر شراء وتأثيره على المخزون"""
        try:
            order_lines = purchase_order_data.get("lines", [])
            movements_created = []

            for line in order_lines:
                # إنشاء حركة مخزون للشراء
                movement_data = {
                    "product_id": line["product_id"],
                    "movement_type": "receipt",
                    "quantity_planned": line["quantity"],
                    "destination_warehouse_id": line.get("warehouse_id"),
                    "reference_type": "purchase_order",
                    "reference_id": purchase_order_data["id"],
                    "reference_number": purchase_order_data["order_number"],
                    "unit_cost": line.get("unit_cost"),
                    "scheduled_date": purchase_order_data.get("delivery_date"),
                    "batch_data": line.get("batch_data"),  # معلومات اللوط
                }

                # إنشاء حركة المخزون
                if self.modules["inventory"]:
                    movement_result = self.modules["inventory"].create_stock_movement(
                        movement_data
                    )
                    if movement_result["success"]:
                        movements_created.append(movement_result["data"])

                # إنشاء القيد المحاسبي
                journal_result = self.create_inventory_journal_entry(movement_data)

            return {
                "success": True,
                "movements_created": movements_created,
                "message": f"تم إنشاء {len(movements_created)} حركة مخزون",
            }

        except Exception as e:
            logger.error(f"خطأ في معالجة أمر الشراء: {str(e)}")
            return {"success": False, "error": str(e)}

    # ==================== تكامل إدارة الشركات ====================

    def get_user_accessible_warehouses(self, user_id: int) -> List[Dict[str, Any]]:
        """الحصول على المخازن المتاحة للمستخدم"""
        try:
            # الحصول على شركات وفروع المستخدم
            if self.modules["companies"]:
                user_companies = self.modules["companies"].get_user_companies(user_id)
                user_branches = self.modules["companies"].get_user_branches(user_id)
            else:
                # محاكاة البيانات
                user_companies = [{"id": 1, "name": "الشركة الرئيسية"}]
                user_branches = [{"id": 1, "name": "الفرع الرئيسي"}]

            # الحصول على المخازن المرتبطة
            accessible_warehouses = []
            if self.modules["inventory"]:
                for company in user_companies:
                    warehouses = self.modules["inventory"].get_warehouses_by_company(
                        company["id"]
                    )
                    accessible_warehouses.extend(warehouses)

            return accessible_warehouses

        except Exception as e:
            logger.error(f"خطأ في الحصول على مخازن المستخدم: {str(e)}")
            return []

    # ==================== تقارير متكاملة ====================

    def generate_integrated_inventory_report(
        self, filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """تقرير مخزون متكامل مع المحاسبة"""
        try:
            # الحصول على بيانات المخزون
            inventory_data = {}
            if self.modules["inventory"]:
                inventory_data = self.modules["inventory"].get_stock_valuation_report(
                    filters
                )

            # الحصول على البيانات المحاسبية
            accounting_data = {}
            if self.modules["accounting"]:
                accounting_data = self.modules[
                    "accounting"
                ].get_inventory_accounts_balance()

            # دمج البيانات
            integrated_report = {
                "inventory_summary": inventory_data.get("data", {}),
                "accounting_summary": accounting_data.get("data", {}),
                "reconciliation": self._reconcile_inventory_accounting(
                    inventory_data, accounting_data
                ),
                "generated_at": datetime.now().isoformat(),
            }

            return {"success": True, "report": integrated_report}

        except Exception as e:
            logger.error(f"خطأ في تقرير المخزون المتكامل: {str(e)}")
            return {"success": False, "error": str(e)}

    def _reconcile_inventory_accounting(
        self, inventory_data: Dict, accounting_data: Dict
    ) -> Dict[str, Any]:
        """مطابقة بيانات المخزون مع المحاسبة"""
        try:
            inventory_value = inventory_data.get("data", {}).get("total_value", 0)
            accounting_balance = accounting_data.get("data", {}).get(
                "inventory_balance", 0
            )

            difference = inventory_value - accounting_balance

            return {
                "inventory_value": inventory_value,
                "accounting_balance": accounting_balance,
                "difference": difference,
                "is_balanced": abs(difference) < 0.01,
                "variance_percentage": (
                    (difference / inventory_value * 100) if inventory_value > 0 else 0
                ),
            }

        except Exception as e:
            logger.error(f"خطأ في مطابقة البيانات: {str(e)}")
            return {"error": str(e)}

    # ==================== إشعارات النظام ====================

    def send_low_stock_notifications(self) -> Dict[str, Any]:
        """إرسال إشعارات المخزون المنخفض"""
        try:
            notifications_sent = []

            # الحصول على المنتجات منخفضة المخزون
            if self.modules["inventory"]:
                low_stock_report = self.modules["inventory"].get_low_stock_report()
                low_stock_products = (
                    low_stock_report.get("data", []) if low_stock_report else []
                )

                for product in low_stock_products:
                    # إنشاء إشعار
                    notification = {
                        "type": "low_stock",
                        "title": "تنبيه: مخزون منخفض",
                        "message": f"المنتج {
                            product['product_name']} وصل لمستوى منخفض: {
                            product['current_quantity']}",
                        "product_id": product["product_id"],
                        "urgency": product.get("urgency_level", "medium"),
                        "created_at": datetime.now().isoformat(),
                    }

                    # إرسال الإشعار للمستخدمين المعنيين
                    if self.modules["users"]:
                        warehouse_id = product.get("warehouse_id")
                        user_module = self.modules["users"]
                        warehouse_managers = user_module.get_warehouse_managers(warehouse_id)  # type: ignore
                        # Type safety: ensure we have a valid iterable
                        if warehouse_managers is not None:
                            manager_list = (
                                warehouse_managers
                                if isinstance(warehouse_managers, list)
                                else []
                            )
                            for manager in manager_list:  # type: ignore
                                if isinstance(manager, dict) and "id" in manager:
                                    user_module.send_notification(
                                        manager["id"], notification
                                    )

                    notifications_sent.append(notification)

            return {
                "success": True,
                "notifications_sent": len(notifications_sent),
                "notifications": notifications_sent,
            }

        except Exception as e:
            logger.error(f"خطأ في إرسال الإشعارات: {str(e)}")
            return {"success": False, "error": str(e)}
