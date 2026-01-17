"""
Admin Roles & Permissions Models

This module defines the database models for role-based access control (RBAC).
"""

from datetime import datetime
from src.database import db


# Association table for Role-Permission many-to-many relationship
role_permissions = db.Table(
    "role_permissions",
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column("created_at", db.DateTime, default=datetime.utcnow),
)

# Association table for User-Role many-to-many relationship
user_roles = db.Table(
    "user_roles",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column("assigned_at", db.DateTime, default=datetime.utcnow),
    db.Column("assigned_by", db.Integer, db.ForeignKey("users.id")),
)


class Permission(db.Model):
    """
    Permission model representing a specific action that can be performed.

    Permissions are organized by module (e.g., products.view, products.create)
    """

    __tablename__ = "permissions"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    name_ar = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    module = db.Column(db.String(50), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "name_ar": self.name_ar,
            "description": self.description,
            "description_ar": self.description_ar,
            "module": self.module,
            "is_active": self.is_active,
        }


class Role(db.Model):
    """
    Role model representing a collection of permissions.

    Roles can be assigned to users to grant them access to specific features.
    """

    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    color = db.Column(db.String(20), default="blue")
    icon = db.Column(db.String(50), default="shield")
    is_system = db.Column(db.Boolean, default=False)  # System roles cannot be deleted
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=0)  # Higher = more important
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationships - use different name to avoid conflict with 'permissions'
    # column in other Role models
    permission_objects = db.relationship(
        "Permission",
        secondary=role_permissions,
        backref=db.backref("role_objects", lazy="dynamic"),
        lazy="dynamic",
    )

    def to_dict(self, include_permissions=False):
        data = {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "name_ar": self.name_ar,
            "description": self.description,
            "description_ar": self.description_ar,
            "color": self.color,
            "icon": self.icon,
            "is_system": self.is_system,
            "is_active": self.is_active,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "users_count": len(self.users) if hasattr(self, "users") else 0,
        }
        if include_permissions:
            data["permissions"] = [p.to_dict() for p in self.permission_objects]
        return data

    def has_permission(self, permission_code):
        """Check if role has a specific permission."""
        return any(p.code == permission_code for p in self.permission_objects)


class SystemSetup(db.Model):
    """
    System setup configuration model.

    Stores initial setup status and configuration.
    """

    __tablename__ = "system_setup"

    id = db.Column(db.Integer, primary_key=True)
    is_completed = db.Column(db.Boolean, default=False)
    setup_step = db.Column(db.Integer, default=0)
    company_name = db.Column(db.String(200))
    company_name_ar = db.Column(db.String(200))
    company_email = db.Column(db.String(200))
    company_phone = db.Column(db.String(50))
    company_address = db.Column(db.Text)
    company_logo = db.Column(db.String(500))
    tax_number = db.Column(db.String(50))
    commercial_register = db.Column(db.String(50))
    currency = db.Column(db.String(10), default="EGP")
    timezone = db.Column(db.String(50), default="Asia/Riyadh")
    language = db.Column(db.String(10), default="ar")
    fiscal_year_start = db.Column(db.Integer, default=1)  # Month (1-12)
    admin_created = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "is_completed": self.is_completed,
            "setup_step": self.setup_step,
            "company_name": self.company_name,
            "company_name_ar": self.company_name_ar,
            "company_email": self.company_email,
            "company_phone": self.company_phone,
            "company_address": self.company_address,
            "company_logo": self.company_logo,
            "tax_number": self.tax_number,
            "commercial_register": self.commercial_register,
            "currency": self.currency,
            "timezone": self.timezone,
            "language": self.language,
            "fiscal_year_start": self.fiscal_year_start,
            "admin_created": self.admin_created,
        }


# AuditLog is now defined in audit_log.py - import it when needed:
# from src.models.audit_log import AuditLog


# Default permissions to seed
DEFAULT_PERMISSIONS = [
    # Dashboard
    {
        "code": "dashboard.view",
        "name": "View Dashboard",
        "name_ar": "عرض لوحة التحكم",
        "module": "dashboard",
    },
    {
        "code": "dashboard.widgets",
        "name": "Manage Widgets",
        "name_ar": "إدارة الودجات",
        "module": "dashboard",
    },
    # Products
    {
        "code": "products.view",
        "name": "View Products",
        "name_ar": "عرض المنتجات",
        "module": "products",
    },
    {
        "code": "products.create",
        "name": "Create Products",
        "name_ar": "إنشاء المنتجات",
        "module": "products",
    },
    {
        "code": "products.edit",
        "name": "Edit Products",
        "name_ar": "تعديل المنتجات",
        "module": "products",
    },
    {
        "code": "products.delete",
        "name": "Delete Products",
        "name_ar": "حذف المنتجات",
        "module": "products",
    },
    {
        "code": "products.import",
        "name": "Import Products",
        "name_ar": "استيراد المنتجات",
        "module": "products",
    },
    {
        "code": "products.export",
        "name": "Export Products",
        "name_ar": "تصدير المنتجات",
        "module": "products",
    },
    # Categories
    {
        "code": "categories.view",
        "name": "View Categories",
        "name_ar": "عرض الفئات",
        "module": "categories",
    },
    {
        "code": "categories.create",
        "name": "Create Categories",
        "name_ar": "إنشاء الفئات",
        "module": "categories",
    },
    {
        "code": "categories.edit",
        "name": "Edit Categories",
        "name_ar": "تعديل الفئات",
        "module": "categories",
    },
    {
        "code": "categories.delete",
        "name": "Delete Categories",
        "name_ar": "حذف الفئات",
        "module": "categories",
    },
    # Inventory
    {
        "code": "inventory.view",
        "name": "View Inventory",
        "name_ar": "عرض المخزون",
        "module": "inventory",
    },
    {
        "code": "inventory.adjust",
        "name": "Adjust Inventory",
        "name_ar": "تعديل المخزون",
        "module": "inventory",
    },
    {
        "code": "inventory.transfer",
        "name": "Transfer Stock",
        "name_ar": "تحويل المخزون",
        "module": "inventory",
    },
    # Warehouses
    {
        "code": "warehouses.view",
        "name": "View Warehouses",
        "name_ar": "عرض المستودعات",
        "module": "warehouses",
    },
    {
        "code": "warehouses.create",
        "name": "Create Warehouses",
        "name_ar": "إنشاء المستودعات",
        "module": "warehouses",
    },
    {
        "code": "warehouses.edit",
        "name": "Edit Warehouses",
        "name_ar": "تعديل المستودعات",
        "module": "warehouses",
    },
    {
        "code": "warehouses.delete",
        "name": "Delete Warehouses",
        "name_ar": "حذف المستودعات",
        "module": "warehouses",
    },
    # Stock Movements
    {
        "code": "stock_movements.view",
        "name": "View Stock Movements",
        "name_ar": "عرض حركة المخزون",
        "module": "stock_movements",
    },
    {
        "code": "stock_movements.create",
        "name": "Create Stock Movements",
        "name_ar": "إنشاء حركة المخزون",
        "module": "stock_movements",
    },
    # Customers
    {
        "code": "customers.view",
        "name": "View Customers",
        "name_ar": "عرض العملاء",
        "module": "customers",
    },
    {
        "code": "customers.create",
        "name": "Create Customers",
        "name_ar": "إنشاء العملاء",
        "module": "customers",
    },
    {
        "code": "customers.edit",
        "name": "Edit Customers",
        "name_ar": "تعديل العملاء",
        "module": "customers",
    },
    {
        "code": "customers.delete",
        "name": "Delete Customers",
        "name_ar": "حذف العملاء",
        "module": "customers",
    },
    # Suppliers
    {
        "code": "suppliers.view",
        "name": "View Suppliers",
        "name_ar": "عرض الموردين",
        "module": "suppliers",
    },
    {
        "code": "suppliers.create",
        "name": "Create Suppliers",
        "name_ar": "إنشاء الموردين",
        "module": "suppliers",
    },
    {
        "code": "suppliers.edit",
        "name": "Edit Suppliers",
        "name_ar": "تعديل الموردين",
        "module": "suppliers",
    },
    {
        "code": "suppliers.delete",
        "name": "Delete Suppliers",
        "name_ar": "حذف الموردين",
        "module": "suppliers",
    },
    # Invoices
    {
        "code": "invoices.view",
        "name": "View Invoices",
        "name_ar": "عرض الفواتير",
        "module": "invoices",
    },
    {
        "code": "invoices.create",
        "name": "Create Invoices",
        "name_ar": "إنشاء الفواتير",
        "module": "invoices",
    },
    {
        "code": "invoices.edit",
        "name": "Edit Invoices",
        "name_ar": "تعديل الفواتير",
        "module": "invoices",
    },
    {
        "code": "invoices.delete",
        "name": "Delete Invoices",
        "name_ar": "حذف الفواتير",
        "module": "invoices",
    },
    {
        "code": "invoices.void",
        "name": "Void Invoices",
        "name_ar": "إلغاء الفواتير",
        "module": "invoices",
    },
    # Payments
    {
        "code": "payments.view",
        "name": "View Payments",
        "name_ar": "عرض المدفوعات",
        "module": "payments",
    },
    {
        "code": "payments.create",
        "name": "Create Payments",
        "name_ar": "إنشاء المدفوعات",
        "module": "payments",
    },
    {
        "code": "payments.edit",
        "name": "Edit Payments",
        "name_ar": "تعديل المدفوعات",
        "module": "payments",
    },
    {
        "code": "payments.delete",
        "name": "Delete Payments",
        "name_ar": "حذف المدفوعات",
        "module": "payments",
    },
    # Returns
    {
        "code": "returns.view",
        "name": "View Returns",
        "name_ar": "عرض المرتجعات",
        "module": "returns",
    },
    {
        "code": "returns.create",
        "name": "Create Returns",
        "name_ar": "إنشاء المرتجعات",
        "module": "returns",
    },
    {
        "code": "returns.approve",
        "name": "Approve Returns",
        "name_ar": "الموافقة على المرتجعات",
        "module": "returns",
    },
    # Reports
    {
        "code": "reports.view",
        "name": "View Reports",
        "name_ar": "عرض التقارير",
        "module": "reports",
    },
    {
        "code": "reports.export",
        "name": "Export Reports",
        "name_ar": "تصدير التقارير",
        "module": "reports",
    },
    {
        "code": "reports.financial",
        "name": "Financial Reports",
        "name_ar": "التقارير المالية",
        "module": "reports",
    },
    # Users
    {
        "code": "users.view",
        "name": "View Users",
        "name_ar": "عرض المستخدمين",
        "module": "users",
    },
    {
        "code": "users.create",
        "name": "Create Users",
        "name_ar": "إنشاء المستخدمين",
        "module": "users",
    },
    {
        "code": "users.edit",
        "name": "Edit Users",
        "name_ar": "تعديل المستخدمين",
        "module": "users",
    },
    {
        "code": "users.delete",
        "name": "Delete Users",
        "name_ar": "حذف المستخدمين",
        "module": "users",
    },
    # Roles
    {
        "code": "roles.view",
        "name": "View Roles",
        "name_ar": "عرض الأدوار",
        "module": "roles",
    },
    {
        "code": "roles.create",
        "name": "Create Roles",
        "name_ar": "إنشاء الأدوار",
        "module": "roles",
    },
    {
        "code": "roles.edit",
        "name": "Edit Roles",
        "name_ar": "تعديل الأدوار",
        "module": "roles",
    },
    {
        "code": "roles.delete",
        "name": "Delete Roles",
        "name_ar": "حذف الأدوار",
        "module": "roles",
    },
    {
        "code": "roles.assign",
        "name": "Assign Roles",
        "name_ar": "تعيين الأدوار",
        "module": "roles",
    },
    # Settings
    {
        "code": "settings.view",
        "name": "View Settings",
        "name_ar": "عرض الإعدادات",
        "module": "settings",
    },
    {
        "code": "settings.edit",
        "name": "Edit Settings",
        "name_ar": "تعديل الإعدادات",
        "module": "settings",
    },
    # Company
    {
        "code": "company.view",
        "name": "View Company",
        "name_ar": "عرض الشركة",
        "module": "company",
    },
    {
        "code": "company.edit",
        "name": "Edit Company",
        "name_ar": "تعديل الشركة",
        "module": "company",
    },
    # Admin
    {
        "code": "admin.view",
        "name": "Admin Access",
        "name_ar": "وصول المدير",
        "module": "admin",
    },
    {
        "code": "admin.audit",
        "name": "View Audit Logs",
        "name_ar": "عرض سجلات التدقيق",
        "module": "admin",
    },
    {
        "code": "admin.backup",
        "name": "Backup System",
        "name_ar": "النسخ الاحتياطي",
        "module": "admin",
    },
    # Tools
    {
        "code": "tools.use",
        "name": "Use Tools",
        "name_ar": "استخدام الأدوات",
        "module": "tools",
    },
    {
        "code": "tools.import",
        "name": "Import Data",
        "name_ar": "استيراد البيانات",
        "module": "tools",
    },
    {
        "code": "tools.export",
        "name": "Export Data",
        "name_ar": "تصدير البيانات",
        "module": "tools",
    },
]

# Default roles to seed
DEFAULT_ROLES = [
    {
        "code": "super_admin",
        "name": "Super Admin",
        "name_ar": "مدير النظام",
        "description": "Full access to all system features",
        "description_ar": "وصول كامل لجميع ميزات النظام",
        "color": "rose",
        "icon": "crown",
        "is_system": True,
        "priority": 100,
        "permissions": "*",  # All permissions
    },
    {
        "code": "admin",
        "name": "Admin",
        "name_ar": "مدير",
        "description": "Administrative access with some restrictions",
        "description_ar": "وصول إداري مع بعض القيود",
        "color": "purple",
        "icon": "shield",
        "is_system": True,
        "priority": 90,
        "permissions": [
            "dashboard.*",
            "products.*",
            "categories.*",
            "inventory.*",
            "warehouses.*",
            "customers.*",
            "suppliers.*",
            "invoices.*",
            "payments.*",
            "returns.*",
            "reports.*",
            "users.view",
            "settings.view",
            "company.view",
        ],
    },
    {
        "code": "manager",
        "name": "Manager",
        "name_ar": "مدير فرع",
        "description": "Branch manager with operational access",
        "description_ar": "مدير فرع مع وصول تشغيلي",
        "color": "blue",
        "icon": "briefcase",
        "is_system": False,
        "priority": 70,
        "permissions": [
            "dashboard.view",
            "products.*",
            "categories.view",
            "inventory.*",
            "warehouses.view",
            "customers.*",
            "suppliers.view",
            "invoices.*",
            "payments.*",
            "returns.*",
            "reports.view",
            "stock_movements.*",
        ],
    },
    {
        "code": "sales",
        "name": "Sales",
        "name_ar": "مبيعات",
        "description": "Sales staff with limited access",
        "description_ar": "موظف مبيعات مع وصول محدود",
        "color": "teal",
        "icon": "shopping-cart",
        "is_system": False,
        "priority": 50,
        "permissions": [
            "dashboard.view",
            "products.view",
            "customers.*",
            "invoices.view",
            "invoices.create",
            "payments.view",
            "payments.create",
            "returns.view",
            "returns.create",
        ],
    },
    {
        "code": "accountant",
        "name": "Accountant",
        "name_ar": "محاسب",
        "description": "Financial and accounting access",
        "description_ar": "وصول مالي ومحاسبي",
        "color": "emerald",
        "icon": "calculator",
        "is_system": False,
        "priority": 60,
        "permissions": [
            "dashboard.view",
            "invoices.*",
            "payments.*",
            "reports.*",
            "customers.view",
            "suppliers.view",
        ],
    },
    {
        "code": "warehouse",
        "name": "Warehouse Staff",
        "name_ar": "أمين مستودع",
        "description": "Warehouse and inventory management",
        "description_ar": "إدارة المستودع والمخزون",
        "color": "amber",
        "icon": "warehouse",
        "is_system": False,
        "priority": 40,
        "permissions": [
            "dashboard.view",
            "products.view",
            "inventory.*",
            "warehouses.view",
            "stock_movements.*",
            "lots.view",
        ],
    },
    {
        "code": "viewer",
        "name": "Viewer",
        "name_ar": "مشاهد",
        "description": "Read-only access",
        "description_ar": "وصول للقراءة فقط",
        "color": "gray",
        "icon": "eye",
        "is_system": False,
        "priority": 10,
        "permissions": [
            "dashboard.view",
            "products.view",
            "categories.view",
            "inventory.view",
            "customers.view",
            "suppliers.view",
            "invoices.view",
            "reports.view",
        ],
    },
]


def seed_permissions_and_roles():
    """Seed default permissions and roles into the database."""
    # Seed permissions
    for perm_data in DEFAULT_PERMISSIONS:
        existing = Permission.query.filter_by(code=perm_data["code"]).first()
        if not existing:
            permission = Permission(**perm_data)
            db.session.add(permission)

    db.session.commit()

    # Seed roles
    for role_data in DEFAULT_ROLES:
        existing = Role.query.filter_by(code=role_data["code"]).first()
        if not existing:
            perms = role_data.pop("permissions")
            role = Role(**role_data)

            # Assign permissions
            if perms == "*":
                role.permissions = Permission.query.all()
            else:
                for perm_pattern in perms:
                    if perm_pattern.endswith(".*"):
                        module = perm_pattern.replace(".*", "")
                        role.permissions.extend(
                            Permission.query.filter_by(module=module).all()
                        )
                    else:
                        perm = Permission.query.filter_by(code=perm_pattern).first()
                        if perm:
                            role.permissions.append(perm)

            db.session.add(role)

    db.session.commit()

    return True
