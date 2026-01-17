# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
نماذج المخزون - النسخة الموحدة
All linting disabled due to SQLAlchemy mock objects and optional dependencies.
"""

from datetime import datetime, timezone
from typing import Any

# إعداد المتغيرات الأساسية
db: Any = None
Column: Any = None
Integer: Any = None
String: Any = None
Text: Any = None
DateTime: Any = None
Boolean: Any = None
Float: Any = None
Date: Any = None
ForeignKey: Any = None
Numeric: Any = None
relationship: Any = None
synonym: Any = None
SQLALCHEMY_AVAILABLE = False

# محاولة استيراد قاعدة البيانات
try:
    from .user import db  # type: ignore
except ImportError:
    try:
        from user import db  # type: ignore
    except ImportError:
        try:
            from database import db  # type: ignore
        except ImportError:
            pass

# محاولة استيراد SQLAlchemy
try:
    from sqlalchemy import (
        Column as SQLColumn,
        Integer as SQLInteger,
        String as SQLString,
        Text as SQLText,
        DateTime as SQLDateTime,
        Boolean as SQLBoolean,
        Float as SQLFloat,
        Date as SQLDate,
        ForeignKey as SQLForeignKey,
        Numeric as SQLNumeric,
    )
    from sqlalchemy.orm import relationship as sql_relationship, synonym as sql_synonym

    # تعيين المتغيرات العامة
    Column = SQLColumn
    Integer = SQLInteger
    String = SQLString
    Text = SQLText
    DateTime = SQLDateTime
    Boolean = SQLBoolean
    Float = SQLFloat
    Date = SQLDate
    ForeignKey = SQLForeignKey
    Numeric = SQLNumeric
    relationship = sql_relationship
    synonym = sql_synonym
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    pass

# إنشاء mock components إذا لم تكن متوفرة
if not SQLALCHEMY_AVAILABLE or db is None:

    class MockQuery:
        def filter_by(self, **kwargs):
            return self

        def filter(self, *args):
            return self

        def all(self):
            return []

        def first(self):
            return None

        def count(self):
            return 0

        def order_by(self, *args):
            return self

        def limit(self, limit):
            return self

        def offset(self, offset):
            return self

        def get(self, id):
            return None

    class MockDB:
        class Model:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            def to_dict(self):
                return {}

            @classmethod
            def query(cls):
                return MockQuery()

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

        session = None

    # تعيين المتغيرات إذا لم تكن متوفرة
    if db is None:
        db = MockDB()

    if not SQLALCHEMY_AVAILABLE:

        def mock_column(*args, **kwargs):
            return None

        def mock_integer():
            return None

        def mock_string(length=None):
            return None

        def mock_text():
            return None

        def mock_datetime():
            return None

        def mock_boolean():
            return None

        def mock_float():
            return None

        def mock_date():
            return None

        def mock_foreign_key(*args, **kwargs):
            return None

        def mock_numeric(*args, **kwargs):
            return None

        def mock_relationship(*args, **kwargs):
            return None

        Column = mock_column
        Integer = mock_integer
        String = mock_string
        Text = mock_text
        DateTime = mock_datetime
        Boolean = mock_boolean
        Float = mock_float
        Date = mock_date
        ForeignKey = mock_foreign_key
        Numeric = mock_numeric
        relationship = mock_relationship


# Category model imported from category.py to avoid duplicates
# Import it where needed: from src.models.category import Category


class Product(db.Model):
    """نموذج المنتجات"""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    barcode = Column(String(50), unique=True)
    sku = Column(String(50), unique=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    # brand_id = Column(Integer, ForeignKey('brands.id'))  # Disabled: Brand model not loaded
    cost_price = Column(Numeric(10, 2), default=0)
    selling_price = Column(Numeric(10, 2), default=0)
    current_stock = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=0)
    max_stock_level = Column(Integer, default=0)
    description = Column(Text)
    specifications = Column(Text)
    is_active = Column(Boolean, default=True)
    is_trackable = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # العلاقات
    if SQLALCHEMY_AVAILABLE:
        batches = relationship(
            "Lot", backref="product", lazy="dynamic", foreign_keys="Lot.product_id"
        )

        # Compatibility aliases expected by tests / some routes
        unit_price = synonym("selling_price")
        stock_quantity = synonym("current_stock")

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "name": getattr(self, "name", ""),
            "name_ar": getattr(self, "name_ar", None),
            "barcode": getattr(self, "barcode", ""),
            "sku": getattr(self, "sku", ""),
            "category_id": getattr(self, "category_id", None),
            "cost_price": (
                float(self.cost_price)
                if hasattr(self, "cost_price") and self.cost_price
                else 0
            ),
            "unit_price": (
                float(getattr(self, "unit_price", None))
                if getattr(self, "unit_price", None) is not None
                else (
                    float(self.selling_price)
                    if hasattr(self, "selling_price") and self.selling_price
                    else 0
                )
            ),
            "selling_price": (
                float(self.selling_price)
                if hasattr(self, "selling_price") and self.selling_price
                else 0
            ),
            "current_stock": getattr(self, "current_stock", 0),
            "stock_quantity": getattr(self, "current_stock", 0),
            "min_stock_level": getattr(self, "min_stock_level", 0),
            "max_stock_level": getattr(self, "max_stock_level", 0),
            "description": getattr(self, "description", ""),
            "specifications": getattr(self, "specifications", ""),
            "is_active": getattr(self, "is_active", True),
            "is_trackable": getattr(self, "is_trackable", True),
            "created_at": (
                self.created_at.isoformat()
                if hasattr(self, "created_at") and self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if hasattr(self, "updated_at") and self.updated_at
                else None
            ),
        }


class Warehouse(db.Model):
    """نموذج المخازن"""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    name_ar = Column(String(100))
    code = Column(String(20), unique=True)
    location = Column(String(255))
    region = Column(String(100))
    address = Column(Text)
    manager_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "name": getattr(self, "name", ""),
            "name_ar": getattr(self, "name_ar", None),
            "code": getattr(self, "code", ""),
            "location": getattr(self, "location", ""),
            "region": getattr(self, "region", ""),
            "address": getattr(self, "address", ""),
            "manager_id": getattr(self, "manager_id", None),
            "is_active": getattr(self, "is_active", True),
            "created_at": (
                self.created_at.isoformat()
                if hasattr(self, "created_at") and self.created_at
                else None
            ),
        }


class Lot(db.Model):
    """نموذج اللوطات"""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True)
    lot_number = Column(String(50), unique=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    expiry_date = Column(Date)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "lot_number": getattr(self, "lot_number", ""),
            "product_id": getattr(self, "product_id", None),
            "quantity": getattr(self, "quantity", 0),
            "expiry_date": (
                self.expiry_date.isoformat()
                if hasattr(self, "expiry_date") and self.expiry_date
                else None
            ),
            "created_at": (
                self.created_at.isoformat()
                if hasattr(self, "created_at") and self.created_at
                else None
            ),
        }


class ProductGroup(db.Model):
    """نموذج مجموعات المنتجات"""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "product_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "name": getattr(self, "name", ""),
            "description": getattr(self, "description", ""),
            "category_id": getattr(self, "category_id", None),
            "is_active": getattr(self, "is_active", True),
            "created_at": (
                self.created_at.isoformat()
                if hasattr(self, "created_at") and self.created_at
                else None
            ),
        }


# إضافة aliases للتوافق مع الملفات الأخرى
Rank = ProductGroup
ProductRank = ProductGroup
Batch = Lot
InventoryMovement = Lot
StockMovement = Lot

# إضافة aliases إضافية للتوافق
Movement = Lot
Stock = Product
Item = Product

# Re-export Category from canonical source for backward compatibility
try:
    from src.models.category import Category
except ImportError:
    try:
        from .category import Category
    except ImportError:
        # Fallback mock Category if not available
        class Category(db.Model):
            """Fallback Category model"""

            __table_args__ = {"extend_existing": True}
            __tablename__ = "categories"
            id = Column(Integer, primary_key=True)
            name = Column(String(100), nullable=False)
