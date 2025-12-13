#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Integration Tests with Database
====================================

These tests require a real database connection and test the full stack:
- Database operations
- API endpoints
- Business logic
- Data validation
"""

import pytest
import os
import sys

# Add backend to path
backend_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app import app
from src.database import db
from src.models.user import User
from src.models.inventory import Category, Warehouse, Product
from src.models.invoice_unified import Invoice, InvoiceItem


@pytest.fixture
def sample_role(db_session):
    """Create a sample role"""
    from src.models.user import Role

    role = Role(
        name="admin",
        description="Administrator role",
        permissions=["create", "read", "update", "delete"],
        is_active=True,
    )
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture
def sample_user(db_session, sample_role):
    """Create a sample user"""
    user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        role_id=sample_role.id,
    )
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_category(db_session):
    """Create a sample category"""
    category = Category(
        name="Electronics", name_ar="إلكترونيات", description="Electronic products"
    )
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def sample_warehouse(db_session):
    """Create a sample warehouse"""
    warehouse = Warehouse(
        name="Main Warehouse",
        name_ar="المخزن الرئيسي",
        location="Riyadh",
        is_active=True,
    )
    db_session.add(warehouse)
    db_session.commit()
    return warehouse


@pytest.fixture
def sample_product(db_session, sample_category):
    """Create a sample product"""
    product = Product(
        name="Laptop",
        name_ar="لابتوب",
        sku="LAPTOP-001",
        barcode="1234567890123",
        category_id=sample_category.id,
        unit_price=3000.00,
        cost_price=2500.00,
        stock_quantity=10,
        min_stock_level=5,
        is_active=True,
    )
    db_session.add(product)
    db_session.commit()
    return product


class TestAuthIntegration:
    """Integration tests for authentication"""

    def test_login_with_valid_credentials(self, client, sample_user):
        """Test login with valid credentials"""
        response = client.post(
            "/api/auth/login", json={"username": "testuser", "password": "password123"}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert data["user"]["username"] == "testuser"

    def test_login_with_invalid_credentials(self, client, sample_user):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "wrongpassword"},
        )

        assert response.status_code == 401

    def test_login_with_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 401


class TestProductsIntegration:
    """Integration tests for products"""

    def test_list_products(self, client, sample_product):
        """Test listing products"""
        response = client.get("/api/products")

        assert response.status_code == 200
        data = response.get_json()
        assert "items" in data
        assert len(data["items"]) > 0
        assert data["items"][0]["name"] == "Laptop"

    def test_list_products_with_pagination(self, client, db_session, sample_category):
        """Test listing products with pagination"""
        # Create multiple products
        for i in range(25):
            product = Product(
                name=f"Product {i}",
                name_ar=f"منتج {i}",
                sku=f"PROD-{i:03d}",
                category_id=sample_category.id,
                unit_price=100.00,
                is_active=True,
            )
            db_session.add(product)
        db_session.commit()

        # Test first page
        response = client.get("/api/products?page=1&per_page=10")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]) == 10
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["total"] >= 25

        # Test second page
        response = client.get("/api/products?page=2&per_page=10")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]) == 10
        assert data["pagination"]["page"] == 2

    def test_search_products(self, client, sample_product):
        """Test searching products"""
        response = client.get("/api/products?search=Laptop")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]) > 0
        assert "Laptop" in data["items"][0]["name"]

    def test_filter_products_by_category(self, client, sample_product, sample_category):
        """Test filtering products by category"""
        response = client.get(f"/api/products?category_id={sample_category.id}")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]) > 0
        assert data["items"][0]["category_id"] == sample_category.id


class TestInventoryIntegration:
    """Integration tests for inventory"""

    def test_list_categories(self, client, sample_category):
        """Test listing categories"""
        response = client.get("/api/inventory/categories")

        assert response.status_code == 200
        data = response.get_json()
        assert "items" in data
        assert len(data["items"]) > 0
        assert data["items"][0]["name"] == "Electronics"

    def test_create_category(self, client, db_session):
        """Test creating a category"""
        response = client.post(
            "/api/inventory/categories",
            json={
                "name": "Furniture",
                "name_ar": "أثاث",
                "description": "Furniture products",
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Furniture"
        assert data["name_ar"] == "أثاث"

        # Verify in database
        category = db_session.query(Category).filter_by(name="Furniture").first()
        assert category is not None
        assert category.name_ar == "أثاث"

    def test_list_warehouses(self, client, sample_warehouse):
        """Test listing warehouses"""
        response = client.get("/api/inventory/warehouses")

        assert response.status_code == 200
        data = response.get_json()
        assert "items" in data
        assert len(data["items"]) > 0
        assert data["items"][0]["name"] == "Main Warehouse"

    def test_create_warehouse(self, client, db_session):
        """Test creating a warehouse"""
        response = client.post(
            "/api/inventory/warehouses",
            json={
                "name": "Branch Warehouse",
                "name_ar": "مخزن الفرع",
                "location": "Jeddah",
                "is_active": True,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Branch Warehouse"
        assert data["location"] == "Jeddah"

        # Verify in database
        warehouse = (
            db_session.query(Warehouse).filter_by(name="Branch Warehouse").first()
        )
        assert warehouse is not None
        assert warehouse.location == "Jeddah"


class TestInvoicesIntegration:
    """Integration tests for invoices"""

    def test_list_invoices(self, client, db_session, sample_product, sample_user):
        """Test listing invoices"""
        # Create a sample invoice
        invoice = Invoice(
            invoice_number="TEST-SLS-0001",
            invoice_type="sales",
            status="draft",
            total_amount=3000.00,
            created_by=sample_user.id,
        )
        db_session.add(invoice)
        db_session.commit()

        response = client.get("/api/invoices")

        assert response.status_code == 200
        data = response.get_json()
        assert "items" in data
        assert len(data["items"]) > 0

    def test_filter_invoices_by_type(self, client, db_session, sample_user):
        """Test filtering invoices by type"""
        # Create invoices of different types
        for invoice_type in ["sales", "purchase"]:
            invoice = Invoice(
                invoice_number=f"TEST-{invoice_type.upper()}-0001",
                invoice_type=invoice_type,
                status="draft",
                total_amount=1000.00,
                created_by=sample_user.id,
            )
            db_session.add(invoice)
        db_session.commit()

        response = client.get("/api/invoices?invoice_type=sales")

        assert response.status_code == 200
        data = response.get_json()
        assert all(item["invoice_type"] == "sales" for item in data["items"])

    def test_filter_invoices_by_status(self, client, db_session, sample_user):
        """Test filtering invoices by status"""
        # Create invoices with different statuses
        for status in ["draft", "confirmed"]:
            invoice = Invoice(invoice_type="sales", status=status, total_amount=1000.00)
            invoice.invoice_number = f"TEST-SLS-{status.upper()}-0001"
            invoice.created_by = sample_user.id
            db_session.add(invoice)
        db_session.commit()

        response = client.get("/api/invoices?status=draft")

        assert response.status_code == 200
        data = response.get_json()
        assert all(item["status"] == "draft" for item in data["items"])
