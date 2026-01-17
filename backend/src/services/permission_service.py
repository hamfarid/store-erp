# type: ignore
# pylint: disable=all
# flake8: noqa
"""
خدمة إدارة الصلاحيات المتقدمة
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/permission_service.py
"""

from typing import List, Dict, Optional
from datetime import timezone
from flask import session
from src.database import db
from src.models.user import User
from src.models.inventory import Warehouse, StockMovement
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.advanced_permissions_enhanced import (
    UserWarehousePermission,
    UserCustomerPermission,
    PermissionTemplate,
    UserPermissionLog,
)


class PermissionService:
    """خدمة شاملة لإدارة الصلاحيات المتقدمة"""

    @staticmethod
    def get_current_user_id() -> Optional[int]:
        """الحصول على معرف المستخدم الحالي"""
        return session.get("user_id")

    @staticmethod
    def is_admin(user_id: Optional[int] = None) -> bool:
        """فحص ما إذا كان المستخدم أدمن"""
        if not user_id:
            user_id = PermissionService.get_current_user_id()

        if not user_id:
            return False

        user = User.query.get(user_id)
        if not user or not user.role:
            return False

        return user.role.name in ["admin", "super_admin"]

    # ==================== صلاحيات المخازن ====================

    @staticmethod
    def user_can_access_warehouse(
        user_id: int, warehouse_id: int, permission_type: str = "view"
    ) -> bool:
        """فحص صلاحية المستخدم على مخزن معين"""
        # الأدمن له صلاحية على كل شيء
        if PermissionService.is_admin(user_id):
            return True

        permission = UserWarehousePermission.query.filter_by(
            user_id=user_id, warehouse_id=warehouse_id, is_active=True
        ).first()

        if not permission:
            return False

        permission_map = {
            "view": permission.can_view,
            "edit": permission.can_edit,
            "create": permission.can_create,
            "delete": permission.can_delete,
            "reports": permission.can_view_reports,
            "financial": permission.can_view_financial,
            "approve": permission.can_approve,
            "manage_stock": permission.can_manage_stock,
            "view_cost_prices": permission.can_view_cost_prices,
            "edit_prices": permission.can_edit_prices,
            "view_profit_margins": permission.can_view_profit_margins,
            "access_analytics": permission.can_access_analytics,
        }

        return permission_map.get(permission_type, False)

    @staticmethod
    def get_user_warehouses(
        user_id: int, permission_type: str = "view"
    ) -> List[Warehouse]:
        """الحصول على المخازن المصرح للمستخدم بالوصول إليها"""
        # الأدمن له صلاحية على جميع المخازن
        if PermissionService.is_admin(user_id):
            return Warehouse.query.filter_by(is_active=True).all()

        query = (
            db.session.query(Warehouse)
            .join(
                UserWarehousePermission,
                Warehouse.id == UserWarehousePermission.warehouse_id,
            )
            .filter(
                UserWarehousePermission.user_id == user_id,
                UserWarehousePermission.is_active,
                Warehouse.is_active,
            )
        )

        # تطبيق فلتر نوع الصلاحية
        if permission_type == "view":
            query = query.filter(UserWarehousePermission.can_view)
        elif permission_type == "edit":
            query = query.filter(UserWarehousePermission.can_edit)
        elif permission_type == "create":
            query = query.filter(UserWarehousePermission.can_create)
        elif permission_type == "delete":
            query = query.filter(UserWarehousePermission.can_delete)
        elif permission_type == "reports":
            query = query.filter(UserWarehousePermission.can_view_reports)
        elif permission_type == "financial":
            query = query.filter(UserWarehousePermission.can_view_financial)

        return query.all()

    @staticmethod
    def get_warehouse_ids_for_user(
        user_id: int, permission_type: str = "view"
    ) -> List[int]:
        """الحصول على معرفات المخازن المصرح للمستخدم بالوصول إليها"""
        warehouses = PermissionService.get_user_warehouses(user_id, permission_type)
        return [w.id for w in warehouses]

    # ==================== صلاحيات العملاء ====================

    @staticmethod
    def user_can_access_customer(
        user_id: int, customer_id: int, permission_type: str = "view"
    ) -> bool:
        """فحص صلاحية المستخدم على عميل معين"""
        # الأدمن له صلاحية على كل شيء
        if PermissionService.is_admin(user_id):
            return True

        # فحص الربط المباشر (مهندس المبيعات)
        customer = Customer.query.filter_by(
            id=customer_id, sales_engineer_id=user_id, is_active=True
        ).first()

        if customer:
            return True

        # فحص الصلاحيات المخصصة
        permission = UserCustomerPermission.query.filter_by(
            user_id=user_id, customer_id=customer_id, is_active=True
        ).first()

        if not permission:
            return False

        permission_map = {
            "view": permission.can_view,
            "edit": permission.can_edit,
            "create_invoices": permission.can_create_invoices,
            "financial": permission.can_view_financial,
            "approve_credit": permission.can_approve_credit,
            "modify_prices": permission.can_modify_prices,
        }

        return permission_map.get(permission_type, False)

    @staticmethod
    def get_sales_engineer_customers(user_id: int) -> List[Customer]:
        """الحصول على عملاء مهندس المبيعات"""
        # الأدمن له صلاحية على جميع العملاء
        if PermissionService.is_admin(user_id):
            return Customer.query.filter_by(is_active=True).all()

        # العملاء المربوطين مباشرة
        direct_customers = Customer.query.filter_by(
            sales_engineer_id=user_id, is_active=True
        ).all()

        # العملاء من خلال الصلاحيات المخصصة
        permission_customers = (
            db.session.query(Customer)
            .join(
                UserCustomerPermission,
                Customer.id == UserCustomerPermission.customer_id,
            )
            .filter(
                UserCustomerPermission.user_id == user_id,
                UserCustomerPermission.is_active,
                UserCustomerPermission.can_view,
                Customer.is_active,
            )
            .all()
        )

        # دمج القوائم وإزالة التكرار
        all_customers = {c.id: c for c in direct_customers + permission_customers}
        return list(all_customers.values())

    @staticmethod
    def get_customer_ids_for_user(user_id: int) -> List[int]:
        """الحصول على معرفات العملاء المصرح للمستخدم بالوصول إليها"""
        customers = PermissionService.get_sales_engineer_customers(user_id)
        return [c.id for c in customers]

    # ==================== صلاحيات الفواتير ====================

    @staticmethod
    def get_sales_engineer_invoices(user_id: int):
        """الحصول على فواتير مهندس المبيعات"""
        customer_ids = PermissionService.get_customer_ids_for_user(user_id)

        if not customer_ids:
            return []

        # استيراد Invoice هنا لتجنب circular import
        try:
            from src.models.invoices import Invoice

            return Invoice.query.filter(Invoice.customer_id.in_(customer_ids)).all()
        except ImportError:
            # إذا لم يكن نموذج Invoice موجود، نستخدم StockMovement
            return StockMovement.query.filter(
                StockMovement.customer_id.in_(customer_ids),
                StockMovement.movement_type.in_(["فاتورة_مبيعات", "عرض_سعر"]),
            ).all()

    # ==================== إدارة الصلاحيات ====================

    @staticmethod
    def grant_warehouse_permission(
        user_id: int,
        warehouse_id: int,
        permissions: Dict[str, bool],
        granted_by: int,
        reason: str = None,
    ) -> bool:
        """منح صلاحيات مخزن لمستخدم"""
        try:
            # حذف الصلاحية الموجودة إن وجدت
            existing = UserWarehousePermission.query.filter_by(
                user_id=user_id, warehouse_id=warehouse_id
            ).first()

            old_values = existing.to_dict() if existing else None

            if existing:
                db.session.delete(existing)

            # إنشاء صلاحية جديدة
            new_permission = UserWarehousePermission(
                user_id=user_id,
                warehouse_id=warehouse_id,
                can_view=permissions.get("can_view", False),
                can_edit=permissions.get("can_edit", False),
                can_create=permissions.get("can_create", False),
                can_delete=permissions.get("can_delete", False),
                can_view_reports=permissions.get("can_view_reports", False),
                can_view_financial=permissions.get("can_view_financial", False),
                can_approve=permissions.get("can_approve", False),
                can_manage_stock=permissions.get("can_manage_stock", False),
                can_view_cost_prices=permissions.get("can_view_cost_prices", False),
                can_edit_prices=permissions.get("can_edit_prices", False),
                can_view_profit_margins=permissions.get(
                    "can_view_profit_margins", False
                ),
                can_access_analytics=permissions.get("can_access_analytics", False),
                created_by=granted_by,
            )

            db.session.add(new_permission)

            # تسجيل التغيير
            log_entry = UserPermissionLog(
                user_id=user_id,
                permission_type="warehouse",
                permission_id=new_permission.id,
                action="create" if not existing else "update",
                old_values=old_values,
                new_values=new_permission.to_dict(),
                reason=reason,
                created_by=granted_by,
            )

            db.session.add(log_entry)
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error granting warehouse permission: {e}")
            return False

    @staticmethod
    def grant_customer_permission(
        user_id: int,
        customer_id: int,
        permissions: Dict[str, bool],
        granted_by: int,
        reason: str = None,
    ) -> bool:
        """منح صلاحيات عميل لمستخدم"""
        try:
            # حذف الصلاحية الموجودة إن وجدت
            existing = UserCustomerPermission.query.filter_by(
                user_id=user_id, customer_id=customer_id
            ).first()

            old_values = existing.to_dict() if existing else None

            if existing:
                db.session.delete(existing)

            # إنشاء صلاحية جديدة
            new_permission = UserCustomerPermission(
                user_id=user_id,
                customer_id=customer_id,
                can_view=permissions.get("can_view", False),
                can_edit=permissions.get("can_edit", False),
                can_create_invoices=permissions.get("can_create_invoices", False),
                can_view_financial=permissions.get("can_view_financial", False),
                can_approve_credit=permissions.get("can_approve_credit", False),
                can_modify_prices=permissions.get("can_modify_prices", False),
                created_by=granted_by,
            )

            db.session.add(new_permission)

            # تسجيل التغيير
            log_entry = UserPermissionLog(
                user_id=user_id,
                permission_type="customer",
                permission_id=new_permission.id,
                action="create" if not existing else "update",
                old_values=old_values,
                new_values=new_permission.to_dict(),
                reason=reason,
                created_by=granted_by,
            )

            db.session.add(log_entry)
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error granting customer permission: {e}")
            return False

    @staticmethod
    def assign_customer_to_sales_engineer(
        customer_id: int, sales_engineer_id: int, assigned_by: int, reason: str = None
    ) -> bool:
        """ربط عميل بمهندس مبيعات"""
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                return False

            old_engineer_id = customer.sales_engineer_id
            customer.sales_engineer_id = sales_engineer_id

            # تسجيل التغيير
            log_entry = UserPermissionLog(
                user_id=sales_engineer_id,
                permission_type="customer_assignment",
                permission_id=customer_id,
                action="assign",
                old_values={"sales_engineer_id": old_engineer_id},
                new_values={"sales_engineer_id": sales_engineer_id},
                reason=reason,
                created_by=assigned_by,
            )

            db.session.add(log_entry)
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error assigning customer to sales engineer: {e}")
            return False

    # ==================== قوالب الصلاحيات ====================

    @staticmethod
    def create_permission_template(
        name: str,
        description: str,
        template_type: str,
        permissions: Dict,
        created_by: int,
    ) -> Optional[PermissionTemplate]:
        """إنشاء قالب صلاحيات"""
        try:
            template = PermissionTemplate(
                name=name,
                description=description,
                template_type=template_type,
                permissions=permissions,
                created_by=created_by,
            )

            db.session.add(template)
            db.session.commit()

            return template

        except Exception as e:
            db.session.rollback()
            print(f"Error creating permission template: {e}")
            return None

    @staticmethod
    def apply_permission_template(
        template_id: int,
        user_id: int,
        target_ids: List[int],
        applied_by: int,
        reason: str = None,
    ) -> bool:
        """تطبيق قالب صلاحيات على مستخدم"""
        try:
            template = PermissionTemplate.query.get(template_id)
            if not template:
                return False

            success_count = 0

            for target_id in target_ids:
                if template.template_type == "warehouse":
                    success = PermissionService.grant_warehouse_permission(
                        user_id, target_id, template.permissions, applied_by, reason
                    )
                elif template.template_type == "customer":
                    success = PermissionService.grant_customer_permission(
                        user_id, target_id, template.permissions, applied_by, reason
                    )
                else:
                    continue

                if success:
                    success_count += 1

            return success_count > 0

        except Exception as e:
            print(f"Error applying permission template: {e}")
            return False

    # ==================== تقارير الصلاحيات ====================

    @staticmethod
    def get_user_permission_summary(user_id: int) -> Dict:
        """الحصول على ملخص صلاحيات المستخدم"""
        user = User.query.get(user_id)
        if not user:
            return {}

        warehouse_permissions = UserWarehousePermission.query.filter_by(
            user_id=user_id, is_active=True
        ).all()

        customer_permissions = UserCustomerPermission.query.filter_by(
            user_id=user_id, is_active=True
        ).all()

        assigned_customers = Customer.query.filter_by(
            sales_engineer_id=user_id, is_active=True
        ).all()

        return {
            "user": user.to_dict(),
            "warehouse_permissions": [p.to_dict() for p in warehouse_permissions],
            "customer_permissions": [p.to_dict() for p in customer_permissions],
            "assigned_customers": [c.to_dict() for c in assigned_customers],
            "is_admin": PermissionService.is_admin(user_id),
        }

    @staticmethod
    def get_permission_audit_log(
        user_id: Optional[int] = None, days: int = 30
    ) -> List[Dict]:
        """الحصول على سجل تدقيق الصلاحيات"""
        from datetime import datetime, timedelta

        query = UserPermissionLog.query

        if user_id:
            query = query.filter(UserPermissionLog.user_id == user_id)

        # آخر 30 يوم افتراضياً
        since_date = datetime.now(timezone.utc) - timedelta(days=days)
        query = query.filter(UserPermissionLog.created_at >= since_date)

        query = query.order_by(UserPermissionLog.created_at.desc())

        logs = query.all()
        return [log.to_dict() for log in logs]
