"""
Unit Tests for Database Models
"""

import pytest
from datetime import datetime
from decimal import Decimal
from src.models.user_unified import User, Role
from src.models.product_unified import Product
from src.models.warehouse_unified import Warehouse
from src.models.invoice_unified import Invoice, InvoiceItem
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.category import Category  # ensure categories table exists
from src.models.invoice_unified import InvoiceType
from src.database import db


# NOTE: app and client fixtures are now in conftest.py for better test isolation


class TestUserModel:
    """Test User model"""

    def test_create_user(self, app):
        """Test creating a new user"""
        with app.app_context():
            user = User(
                username="testuser", email="test@example.com", full_name="Test User"
            )
            user.set_password("password123")

            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.username == "testuser"
            assert user.email == "test@example.com"
            assert user.check_password("password123")

    def test_password_hashing(self, app):
        """Test password hashing"""
        with app.app_context():
            user = User(username="testuser")
            user.set_password("secret")

            assert user.password_hash != "secret"
            assert user.check_password("secret")
            assert not user.check_password("wrong")

    def test_user_to_dict(self, app):
        """Test user to_dict method"""
        with app.app_context():
            user = User(
                username="testuser",
                email="test@example.com",
                full_name="Test User",
                role="admin",
            )
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

            user_dict = user.to_dict()

            assert user_dict["username"] == "testuser"
            assert user_dict["email"] == "test@example.com"
            assert "password_hash" not in user_dict


class TestProductModel:
    """Test Product model"""

    def test_create_product(self, app):
        """Test creating a new product"""
        with app.app_context():
            product = Product(
                name="Test Product",
                sku="TEST-001",
                barcode="1234567890",
                cost_price=Decimal("10.00"),
                sale_price=Decimal("15.00"),
                current_stock=100,
            )

            db.session.add(product)
            db.session.commit()

            assert product.id is not None
            assert product.name == "Test Product"
            assert product.sku == "TEST-001"
            assert product.current_stock == 100

    def test_product_profit_margin(self, app):
        """Test product profit margin calculation"""
        with app.app_context():
            product = Product(
                name="Test Product",
                cost_price=Decimal("10.00"),
                sale_price=Decimal("15.00"),
            )

            # Profit margin should be 33.33%
            expected_margin = (
                (Decimal("15.00") - Decimal("10.00")) / Decimal("10.00")
            ) * 100
            assert abs(
                Decimal(str(product.calculate_profit_margin())) - expected_margin
            ) < Decimal("0.01")

    def test_low_stock_detection(self, app):
        """Test low stock detection"""
        with app.app_context():
            product = Product(name="Test Product", current_stock=5, min_quantity=10)

            assert product.is_low_stock()

            product.current_stock = 15
            assert not product.is_low_stock()


class TestWarehouseModel:
    """Test Warehouse model"""

    def test_create_warehouse(self, app):
        """Test creating a new warehouse"""
        with app.app_context():
            warehouse = Warehouse(
                name="Main Warehouse",
                code="WH-001",
                location="City Center",
                storage_capacity=Decimal("10000.00"),
            )

            db.session.add(warehouse)
            db.session.commit()

            assert warehouse.id is not None
            assert warehouse.name == "Main Warehouse"
            assert warehouse.code == "WH-001"


class TestInvoiceModel:
    """Test Invoice model"""

    def test_create_invoice(self, app):
        """Test creating a new invoice"""
        with app.app_context():
            # Create customer first
            customer = Customer(name="Test Customer", email="customer@example.com")
            db.session.add(customer)
            db.session.commit()
            # Create a user (creator)
            user = User(
                username="creator1", email="creator1@example.com", password_hash="x"
            )
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            # Create invoice
            invoice = Invoice(
                invoice_number="INV-001",
                customer_id=customer.id,
                created_by=user.id,
                invoice_type=InvoiceType.SALES,
                total_amount=Decimal("100.00"),
            )

            db.session.add(invoice)
            db.session.commit()

            assert invoice.id is not None
            assert invoice.invoice_number == "INV-001"
            assert invoice.total_amount == Decimal("100.00")

    def test_invoice_with_items(self, app):
        """Test invoice with items"""
        with app.app_context():
            # Create dependencies
            customer = Customer(name="Test Customer", email="customer@example.com")
            product = Product(
                name="Test Product", sale_price=Decimal("10.00"), sku="SKU-001"
            )

            db.session.add_all([customer, product])
            db.session.commit()

            # Create a user (creator)
            user = User(
                username="creator2", email="creator2@example.com", password_hash="x"
            )
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            # Create invoice with items
            invoice = Invoice(
                invoice_number="INV-002",
                customer_id=customer.id,
                created_by=user.id,
                invoice_type=InvoiceType.SALES,
            )

            item = InvoiceItem(
                product_id=product.id,
                quantity=5,
                price=Decimal("10.00"),
                total=Decimal("50.00"),
            )

            invoice.items.append(item)
            db.session.add(invoice)
            db.session.commit()

            assert len(invoice.items) == 1
            assert invoice.items[0].quantity == 5


class TestPartnerModel:
    """Test Partner model"""

    def test_create_customer(self, app):
        """Test creating a customer"""
        with app.app_context():
            customer = Customer(
                name="Test Customer", email="customer@example.com", phone="1234567890"
            )

            db.session.add(customer)
            db.session.commit()

            assert customer.id is not None
            assert customer.email == "customer@example.com"

    def test_create_supplier(self, app):
        """Test creating a supplier"""
        with app.app_context():
            supplier = Supplier(name="Test Supplier", email="supplier@example.com")

            db.session.add(supplier)
            db.session.commit()

            assert supplier.id is not None


class TestModelRelationships:
    """Test model relationships"""

    def test_invoice_warehouse_relationship(self, app):
        """Test invoice-warehouse relationship"""
        with app.app_context():
            warehouse = Warehouse(name="Test Warehouse", code="WH-001")
            db.session.add(warehouse)
            db.session.commit()

            user = User(
                username="creator3", email="creator3@example.com", password_hash="x"
            )
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            invoice = Invoice(
                invoice_number="INV-004",
                warehouse_id=warehouse.id,
                created_by=user.id,
                invoice_type=InvoiceType.SALES,
            )
            db.session.add(invoice)
            db.session.commit()

            assert invoice.warehouse_id == warehouse.id

    def test_invoice_partner_relationship(self, app):
        """Test invoice-customer relationship"""
        with app.app_context():
            customer = Customer(name="Test Partner", email="partner@example.com")
            db.session.add(customer)
            db.session.commit()

            user = User(
                username="creator4", email="creator4@example.com", password_hash="x"
            )
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            invoice = Invoice(
                invoice_number="INV-003",
                customer_id=customer.id,
                created_by=user.id,
                invoice_type=InvoiceType.SALES,
            )
            db.session.add(invoice)
            db.session.commit()

            assert invoice.customer_id == customer.id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
