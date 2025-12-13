#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FILE: backend/src/permissions.py | PURPOSE: P0.9 RBAC Permission System | OWNER: Security
"""
/backend/src/permissions.py

P0.9: Role-Based Access Control (RBAC) Permission System

Provides:
- Permission constants
- Role-to-permission mapping
- JWT-compatible permission decorator
- Permission checking utilities
"""

from functools import wraps
from flask import request, jsonify, g
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Permission Constants
# ============================================================================


class Permissions:
    """
    P0.9: Comprehensive permission constants

    Naming convention: {RESOURCE}_{ACTION}
    """

    # System Administration
    ADMIN_FULL = "admin_full"  # Full admin access
    USER_MANAGEMENT = "user_management"  # Manage users
    ROLE_MANAGEMENT = "role_management"  # Manage roles
    SYSTEM_SETTINGS = "system_settings"  # System configuration
    MANAGE_SECURITY = "manage_security"  # Security settings
    VIEW_SECURITY = "view_security"  # View security logs
    VIEW_AUDIT_LOG = "view_audit_log"  # View audit logs

    # User Profile
    PROFILE_VIEW = "profile_view"  # View own profile
    PROFILE_EDIT = "profile_edit"  # Edit own profile

    # Inventory/Products
    INVENTORY_VIEW = "inventory_view"
    INVENTORY_ADD = "inventory_add"
    INVENTORY_EDIT = "inventory_edit"
    INVENTORY_DELETE = "inventory_delete"
    INVENTORY_EXPORT = "inventory_export"

    # Categories
    CATEGORY_VIEW = "category_view"
    CATEGORY_ADD = "category_add"
    CATEGORY_EDIT = "category_edit"
    CATEGORY_DELETE = "category_delete"

    # Warehouses
    WAREHOUSE_VIEW = "warehouse_view"
    WAREHOUSE_ADD = "warehouse_add"
    WAREHOUSE_EDIT = "warehouse_edit"
    WAREHOUSE_DELETE = "warehouse_delete"
    WAREHOUSE_TRANSFER = "warehouse_transfer"

    # Sales
    SALES_VIEW = "sales_view"
    SALES_ADD = "sales_add"
    SALES_EDIT = "sales_edit"
    SALES_DELETE = "sales_delete"
    SALES_APPROVE = "sales_approve"

    # Purchases
    PURCHASES_VIEW = "purchases_view"
    PURCHASES_ADD = "purchases_add"
    PURCHASES_EDIT = "purchases_edit"
    PURCHASES_DELETE = "purchases_delete"
    PURCHASES_APPROVE = "purchases_approve"

    # Customers
    CUSTOMER_VIEW = "customer_view"
    CUSTOMER_ADD = "customer_add"
    CUSTOMER_EDIT = "customer_edit"
    CUSTOMER_DELETE = "customer_delete"

    # Suppliers
    SUPPLIER_VIEW = "supplier_view"
    SUPPLIER_ADD = "supplier_add"
    SUPPLIER_EDIT = "supplier_edit"
    SUPPLIER_DELETE = "supplier_delete"

    # Invoices
    INVOICE_VIEW = "invoice_view"
    INVOICE_ADD = "invoice_add"
    INVOICE_EDIT = "invoice_edit"
    INVOICE_DELETE = "invoice_delete"
    INVOICE_APPROVE = "invoice_approve"
    INVOICE_VOID = "invoice_void"

    # Reports
    REPORTS_VIEW = "reports_view"
    REPORTS_EXPORT = "reports_export"
    REPORTS_ADVANCED = "reports_advanced"
    REPORTS_FINANCIAL = "reports_financial"

    # Dashboard
    DASHBOARD_VIEW = "dashboard_view"
    DASHBOARD_ADMIN = "dashboard_admin"

    # Treasury
    TREASURY_VIEW = "treasury_view"
    TREASURY_ADD = "treasury_add"
    TREASURY_EDIT = "treasury_edit"
    TREASURY_DELETE = "treasury_delete"
    TREASURY_TRANSFER = "treasury_transfer"

    # Excel Operations
    EXCEL_IMPORT = "excel_import"
    EXCEL_EXPORT = "excel_export"

    # Settings
    SYSTEM_SETTINGS_EDIT = "system_settings_edit"
    SYSTEM_SETTINGS_VIEW = "system_settings_view"

    # Partners (Customers/Suppliers)
    PARTNERS_VIEW = "partners_view"
    PARTNERS_ADD = "partners_add"
    PARTNERS_EDIT = "partners_edit"
    PARTNERS_DELETE = "partners_delete"


# ============================================================================
# Role Definitions
# ============================================================================

# Standard role names
ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_WAREHOUSE_MANAGER = "warehouse_manager"
ROLE_SALES = "sales"
ROLE_PURCHASE = "purchase"
ROLE_ACCOUNTANT = "accountant"
ROLE_VIEWER = "viewer"

# Arabic role names (for compatibility)
ROLE_ADMIN_AR = "مدير النظام"
ROLE_WAREHOUSE_MANAGER_AR = "مدير المخزون"
ROLE_SALES_AR = "موظف المبيعات"
ROLE_PURCHASE_AR = "موظف المشتريات"
ROLE_ACCOUNTANT_AR = "محاسب"


# ============================================================================
# Role-Permission Mapping
# ============================================================================

ROLE_PERMISSIONS = {
    # Admin - Full access
    ROLE_ADMIN: [
        Permissions.ADMIN_FULL,
        Permissions.USER_MANAGEMENT,
        Permissions.ROLE_MANAGEMENT,
        Permissions.SYSTEM_SETTINGS,
        Permissions.MANAGE_SECURITY,
        Permissions.VIEW_SECURITY,
        Permissions.VIEW_AUDIT_LOG,
        Permissions.PROFILE_VIEW,
        Permissions.PROFILE_EDIT,
        # All inventory permissions
        Permissions.INVENTORY_VIEW,
        Permissions.INVENTORY_ADD,
        Permissions.INVENTORY_EDIT,
        Permissions.INVENTORY_DELETE,
        Permissions.INVENTORY_EXPORT,
        Permissions.CATEGORY_VIEW,
        Permissions.CATEGORY_ADD,
        Permissions.CATEGORY_EDIT,
        Permissions.CATEGORY_DELETE,
        Permissions.WAREHOUSE_VIEW,
        Permissions.WAREHOUSE_ADD,
        Permissions.WAREHOUSE_EDIT,
        Permissions.WAREHOUSE_DELETE,
        Permissions.WAREHOUSE_TRANSFER,
        # All sales permissions
        Permissions.SALES_VIEW,
        Permissions.SALES_ADD,
        Permissions.SALES_EDIT,
        Permissions.SALES_DELETE,
        Permissions.SALES_APPROVE,
        # All purchase permissions
        Permissions.PURCHASES_VIEW,
        Permissions.PURCHASES_ADD,
        Permissions.PURCHASES_EDIT,
        Permissions.PURCHASES_DELETE,
        Permissions.PURCHASES_APPROVE,
        # All partner permissions
        Permissions.CUSTOMER_VIEW,
        Permissions.CUSTOMER_ADD,
        Permissions.CUSTOMER_EDIT,
        Permissions.CUSTOMER_DELETE,
        Permissions.SUPPLIER_VIEW,
        Permissions.SUPPLIER_ADD,
        Permissions.SUPPLIER_EDIT,
        Permissions.SUPPLIER_DELETE,
        # All invoice permissions
        Permissions.INVOICE_VIEW,
        Permissions.INVOICE_ADD,
        Permissions.INVOICE_EDIT,
        Permissions.INVOICE_DELETE,
        Permissions.INVOICE_APPROVE,
        Permissions.INVOICE_VOID,
        # All report permissions
        Permissions.REPORTS_VIEW,
        Permissions.REPORTS_EXPORT,
        Permissions.REPORTS_ADVANCED,
        Permissions.REPORTS_FINANCIAL,
        Permissions.DASHBOARD_VIEW,
        Permissions.DASHBOARD_ADMIN,
        # Treasury
        Permissions.TREASURY_VIEW,
        Permissions.TREASURY_ADD,
        Permissions.TREASURY_EDIT,
        Permissions.TREASURY_DELETE,
        Permissions.TREASURY_TRANSFER,
        # Excel
        Permissions.EXCEL_IMPORT,
        Permissions.EXCEL_EXPORT,
        # Settings
        Permissions.SYSTEM_SETTINGS_EDIT,
        Permissions.SYSTEM_SETTINGS_VIEW,
        # Partners
        Permissions.PARTNERS_VIEW,
        Permissions.PARTNERS_ADD,
        Permissions.PARTNERS_EDIT,
        Permissions.PARTNERS_DELETE,
    ],
    # Arabic admin alias
    ROLE_ADMIN_AR: None,  # Will be set to same as ROLE_ADMIN
    # Manager - Most permissions except security management
    ROLE_MANAGER: [
        Permissions.USER_MANAGEMENT,
        Permissions.VIEW_SECURITY,
        Permissions.VIEW_AUDIT_LOG,
        Permissions.PROFILE_VIEW,
        Permissions.PROFILE_EDIT,
        Permissions.INVENTORY_VIEW,
        Permissions.INVENTORY_ADD,
        Permissions.INVENTORY_EDIT,
        Permissions.INVENTORY_DELETE,
        Permissions.INVENTORY_EXPORT,
        Permissions.CATEGORY_VIEW,
        Permissions.CATEGORY_ADD,
        Permissions.CATEGORY_EDIT,
        Permissions.WAREHOUSE_VIEW,
        Permissions.WAREHOUSE_ADD,
        Permissions.WAREHOUSE_EDIT,
        Permissions.WAREHOUSE_TRANSFER,
        Permissions.SALES_VIEW,
        Permissions.SALES_ADD,
        Permissions.SALES_EDIT,
        Permissions.SALES_DELETE,
        Permissions.SALES_APPROVE,
        Permissions.PURCHASES_VIEW,
        Permissions.PURCHASES_ADD,
        Permissions.PURCHASES_EDIT,
        Permissions.PURCHASES_DELETE,
        Permissions.PURCHASES_APPROVE,
        Permissions.CUSTOMER_VIEW,
        Permissions.CUSTOMER_ADD,
        Permissions.CUSTOMER_EDIT,
        Permissions.CUSTOMER_DELETE,
        Permissions.SUPPLIER_VIEW,
        Permissions.SUPPLIER_ADD,
        Permissions.SUPPLIER_EDIT,
        Permissions.SUPPLIER_DELETE,
        Permissions.INVOICE_VIEW,
        Permissions.INVOICE_ADD,
        Permissions.INVOICE_EDIT,
        Permissions.INVOICE_APPROVE,
        Permissions.REPORTS_VIEW,
        Permissions.REPORTS_EXPORT,
        Permissions.REPORTS_ADVANCED,
        Permissions.REPORTS_FINANCIAL,
        Permissions.DASHBOARD_VIEW,
        Permissions.DASHBOARD_ADMIN,
        Permissions.TREASURY_VIEW,
        Permissions.TREASURY_ADD,
        Permissions.TREASURY_EDIT,
        Permissions.TREASURY_TRANSFER,
        Permissions.EXCEL_IMPORT,
        Permissions.EXCEL_EXPORT,
    ],
    # Warehouse Manager - Inventory focused
    ROLE_WAREHOUSE_MANAGER: [
        Permissions.PROFILE_VIEW,
        Permissions.PROFILE_EDIT,
        Permissions.INVENTORY_VIEW,
        Permissions.INVENTORY_ADD,
        Permissions.INVENTORY_EDIT,
        Permissions.INVENTORY_DELETE,
        Permissions.INVENTORY_EXPORT,
        Permissions.CATEGORY_VIEW,
        Permissions.CATEGORY_ADD,
        Permissions.CATEGORY_EDIT,
        Permissions.WAREHOUSE_VIEW,
        Permissions.WAREHOUSE_ADD,
        Permissions.WAREHOUSE_EDIT,
        Permissions.WAREHOUSE_TRANSFER,
        Permissions.SUPPLIER_VIEW,
        Permissions.REPORTS_VIEW,
        Permissions.REPORTS_EXPORT,
        Permissions.DASHBOARD_VIEW,
        Permissions.EXCEL_IMPORT,
        Permissions.EXCEL_EXPORT,
    ],
    # Arabic warehouse manager alias
    ROLE_WAREHOUSE_MANAGER_AR: None,  # Will be set to same as ROLE_WAREHOUSE_MANAGER
    # Sales - Sales focused
    ROLE_SALES: [
        Permissions.PROFILE_VIEW,
        Permissions.PROFILE_EDIT,
        Permissions.INVENTORY_VIEW,
        Permissions.SALES_VIEW,
        Permissions.SALES_ADD,
        Permissions.SALES_EDIT,
        Permissions.CUSTOMER_VIEW,
        Permissions.CUSTOMER_ADD,
        Permissions.CUSTOMER_EDIT,
        Permissions.INVOICE_VIEW,
        Permissions.INVOICE_ADD,
        Permissions.REPORTS_VIEW,
        Permissions.DASHBOARD_VIEW,
        Permissions.EXCEL_EXPORT,
    ],
    # Arabic sales alias
    ROLE_SALES_AR: None,
    # Purchase - Purchase focused
    ROLE_PURCHASE: [
        Permissions.PROFILE_VIEW,
        Permissions.PROFILE_EDIT,
        Permissions.INVENTORY_VIEW,
        Permissions.PURCHASES_VIEW,
        Permissions.PURCHASES_ADD,
        Permissions.PURCHASES_EDIT,
        Permissions.SUPPLIER_VIEW,
        Permissions.SUPPLIER_ADD,
        Permissions.SUPPLIER_EDIT,
        Permissions.INVOICE_VIEW,
        Permissions.INVOICE_ADD,
        Permissions.REPORTS_VIEW,
        Permissions.DASHBOARD_VIEW,
        Permissions.EXCEL_EXPORT,
    ],
    # Arabic purchase alias
    ROLE_PURCHASE_AR: None,
    # Accountant - Financial focused
    ROLE_ACCOUNTANT: [
        Permissions.PROFILE_VIEW,
        Permissions.PROFILE_EDIT,
        Permissions.INVENTORY_VIEW,
        Permissions.SALES_VIEW,
        Permissions.PURCHASES_VIEW,
        Permissions.CUSTOMER_VIEW,
        Permissions.SUPPLIER_VIEW,
        Permissions.INVOICE_VIEW,
        Permissions.REPORTS_VIEW,
        Permissions.REPORTS_EXPORT,
        Permissions.REPORTS_FINANCIAL,
        Permissions.DASHBOARD_VIEW,
        Permissions.TREASURY_VIEW,
        Permissions.EXCEL_EXPORT,
    ],
    # Arabic accountant alias
    ROLE_ACCOUNTANT_AR: None,
    # Viewer - Read only
    ROLE_VIEWER: [
        Permissions.PROFILE_VIEW,
        Permissions.INVENTORY_VIEW,
        Permissions.CATEGORY_VIEW,
        Permissions.WAREHOUSE_VIEW,
        Permissions.SALES_VIEW,
        Permissions.PURCHASES_VIEW,
        Permissions.CUSTOMER_VIEW,
        Permissions.SUPPLIER_VIEW,
        Permissions.INVOICE_VIEW,
        Permissions.REPORTS_VIEW,
        Permissions.DASHBOARD_VIEW,
    ],
    # Default user role
    "user": [
        Permissions.PROFILE_VIEW,
        Permissions.PROFILE_EDIT,
        Permissions.INVENTORY_VIEW,
        Permissions.DASHBOARD_VIEW,
    ],
}

# Set Arabic aliases
ROLE_PERMISSIONS[ROLE_ADMIN_AR] = ROLE_PERMISSIONS[ROLE_ADMIN]
ROLE_PERMISSIONS[ROLE_WAREHOUSE_MANAGER_AR] = ROLE_PERMISSIONS[ROLE_WAREHOUSE_MANAGER]
ROLE_PERMISSIONS[ROLE_SALES_AR] = ROLE_PERMISSIONS[ROLE_SALES]
ROLE_PERMISSIONS[ROLE_PURCHASE_AR] = ROLE_PERMISSIONS[ROLE_PURCHASE]
ROLE_PERMISSIONS[ROLE_ACCOUNTANT_AR] = ROLE_PERMISSIONS[ROLE_ACCOUNTANT]


# ============================================================================
# Permission Checking Functions
# ============================================================================


def get_user_permissions(role: str) -> list:
    """
    Get list of permissions for a role

    Args:
        role: Role name (English or Arabic)

    Returns:
        List of permission strings
    """
    return ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS.get("user", []))


def check_permission(role: str, permission: str) -> bool:
    """
    Check if a role has a specific permission

    Args:
        role: Role name
        permission: Permission string

    Returns:
        True if role has permission
    """
    permissions = get_user_permissions(role)

    # Admin has all permissions
    if Permissions.ADMIN_FULL in permissions:
        return True

    return permission in permissions


def get_current_user_role() -> str:
    """
    Get current user's role from JWT token context

    Returns:
        Role name or 'user' as default
    """
    # Try to get role from request context (set by token_required)
    if hasattr(request, "current_user_role"):
        return request.current_user_role

    # Try to get from g object
    if hasattr(g, "current_user_role"):
        return g.current_user_role

    # Try to get user from database
    user_id = getattr(request, "current_user_id", None)
    if user_id:
        try:
            from src.models.user import User, Role

            user = User.query.get(user_id)
            if user:
                # Try unified model first
                if hasattr(user, "role_obj") and user.role_obj:
                    return user.role_obj.name
                # Fallback to role_id
                if hasattr(user, "role_id") and user.role_id:
                    role = Role.query.get(user.role_id)
                    if role:
                        return role.name
                # Fallback to role string
                if hasattr(user, "role") and user.role:
                    return user.role
        except Exception as e:
            logger.warning(f"Error getting user role: {e}")

    return "user"


# ============================================================================
# Permission Decorator
# ============================================================================


def require_permission(*required_permissions, any_of=False):
    """
    P0.9: JWT-compatible permission decorator

    Args:
        *required_permissions: One or more permission strings required
        any_of: If True, user needs ANY of the permissions. If False (default), needs ALL.

    Usage:
        @require_permission(Permissions.INVENTORY_VIEW)
        def get_products():
            ...

        @require_permission(Permissions.INVENTORY_ADD, Permissions.INVENTORY_EDIT, any_of=True)
        def manage_product():
            ...
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get current user role
            role = get_current_user_role()
            user_permissions = get_user_permissions(role)

            # Admin bypass - admin_full grants all permissions
            if Permissions.ADMIN_FULL in user_permissions:
                return f(*args, **kwargs)

            # Check permissions
            if any_of:
                # User needs at least one of the permissions
                has_any = any(perm in user_permissions for perm in required_permissions)
                if not has_any:
                    logger.warning(
                        f"P0.9 Permission denied: User role '{role}' lacks any of {required_permissions}"
                    )
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": "permission_denied",
                                "message": "ليس لديك صلاحية للوصول إلى هذه الوظيفة",
                                "required_permissions": list(required_permissions),
                                "code": "INSUFFICIENT_PERMISSIONS",
                            }
                        ),
                        403,
                    )
            else:
                # User needs all permissions
                missing = [
                    perm
                    for perm in required_permissions
                    if perm not in user_permissions
                ]
                if missing:
                    logger.warning(
                        f"P0.9 Permission denied: User role '{role}' missing {missing}"
                    )
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": "permission_denied",
                                "message": "ليس لديك صلاحية للوصول إلى هذه الوظيفة",
                                "missing_permissions": missing,
                                "code": "INSUFFICIENT_PERMISSIONS",
                            }
                        ),
                        403,
                    )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_any_permission(*permissions):
    """Shortcut for require_permission with any_of=True"""
    return require_permission(*permissions, any_of=True)


def require_admin(f):
    """Decorator requiring admin role"""
    return require_permission(Permissions.ADMIN_FULL)(f)


def require_manager(f):
    """Decorator requiring manager or admin"""
    return require_permission(Permissions.USER_MANAGEMENT)(f)


# ============================================================================
# Export
# ============================================================================

__all__ = [
    "Permissions",
    "ROLE_PERMISSIONS",
    "ROLE_ADMIN",
    "ROLE_MANAGER",
    "ROLE_WAREHOUSE_MANAGER",
    "ROLE_SALES",
    "ROLE_PURCHASE",
    "ROLE_ACCOUNTANT",
    "ROLE_VIEWER",
    "get_user_permissions",
    "check_permission",
    "get_current_user_role",
    "require_permission",
    "require_any_permission",
    "require_admin",
    "require_manager",
]
