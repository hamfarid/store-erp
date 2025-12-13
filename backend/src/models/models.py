from src.database import db
from datetime import datetime, timezone

# Role, User, UserSession, and UserActivity are defined in user.py - CANONICAL DEFINITIONS
# Import them when needed: from src.models.user import User, Role, UserSession, UserActivity


class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    current_stock = db.Column(db.Integer, default=0)
    cost_price = db.Column(db.Float, default=0.0)
    reorder_quantity = db.Column(db.Integer, default=0)
    barcode = db.Column(db.String(100))
    description = db.Column(db.Text)


# Category model imported from category.py to avoid duplicates
# from src.models.category import Category


class Warehouse(db.Model):
    __tablename__ = "warehouses"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class StockMovement(db.Model):
    __tablename__ = "stock_movements"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    movement_type = db.Column(db.String(50), nullable=False)
    movement_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"))
    product = db.relationship("Product", backref="stock_movements")
    warehouse = db.relationship("Warehouse", backref="stock_movements")
    customer = db.relationship("Customer", backref="stock_movements")
    supplier = db.relationship("Supplier", backref="stock_movements")


# Customer is defined below with full fields


class Supplier(db.Model):
    __tablename__ = "suppliers"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))


class ProductGroup(db.Model):
    __tablename__ = "product_groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Rank(db.Model):
    __tablename__ = "ranks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey("product_groups.id"))


class Customer(db.Model):
    __tablename__ = "customers"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(50), unique=True, nullable=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    company_name = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    credit_limit = db.Column(db.Numeric(15, 2), default=0.00)
    payment_terms = db.Column(db.String(50))
    currency = db.Column(db.String(3), default="USD")
    discount_rate = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(50), default="regular")
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    tags = db.Column(db.JSON)
    sales_engineer_id = db.Column(db.Integer, db.ForeignKey("sales_engineers.id"))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class SalesEngineer(db.Model):
    __tablename__ = "sales_engineers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    customers = db.relationship("Customer", backref="sales_engineer", lazy=True)
