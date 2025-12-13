# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات - إصدار موحد ومحسن
Unified and Enhanced Database Models Package
"""

# استيراد قاعدة البيانات من database.py
try:
    from database import db
except ImportError:
    try:
        from ..database import db
    except ImportError:

        class MockDB:
            class Model:
                pass

            def __init__(self):
                """Mock initializer for testing without Flask app context."""
                pass

        db = MockDB()

# استيراد النماذج الأساسية
# NOTE: Models are NOT auto-imported here to avoid immediate DB creation
# Import them manually when needed or in database initialization routines
User = None
Role = None
Category = None
Warehouse = None
Product = None
Brand = None
ProductImage = None
StockMovement = None
Inventory = None
Customer = None
Supplier = None
UnifiedInvoice = None
UnifiedInvoiceItem = None
InvoicePayment = None
InvoiceType = None
InvoiceStatus = None
PaymentMethod = None
SalesInvoice = None
SalesInvoiceItem = None
CustomerPayment = None
Invoice = None
InvoiceItem = None
Payment = None


# التعدادات والثوابت الموحدة
class UserRole:
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class ProductType:
    SIMPLE = "simple"
    VARIABLE = "variable"
    SERVICE = "service"


class MovementType:
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"


# قائمة التصدير الموحدة
__all__ = [
    "db",
    "User",
    "Role",
    "Category",
    "Warehouse",
    "Product",
    "Brand",
    "ProductImage",
    "StockMovement",
    "Inventory",
    "Customer",
    "Supplier",
    # النماذج الموحدة الجديدة
    "UnifiedInvoice",
    "UnifiedInvoiceItem",
    "InvoicePayment",
    "InvoiceType",
    "InvoiceStatus",
    "PaymentMethod",
    # النماذج المتقدمة للمبيعات
    "SalesInvoice",
    "SalesInvoiceItem",
    "CustomerPayment",
    # النماذج القديمة (للتوافق)
    "Invoice",
    "InvoiceItem",
    "Payment",
    # الثوابت
    "UserRole",
    "ProductType",
    "MovementType",
]
