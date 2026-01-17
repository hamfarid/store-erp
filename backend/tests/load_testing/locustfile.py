#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load Testing with Locust
=========================

Usage:
    # Install locust first:
    pip install locust

    # Run load test:
    locust -f backend/tests/load_testing/locustfile.py --host=http://localhost:5000

    # Run headless with specific users:
    locust -f backend/tests/load_testing/locustfile.py --host=http://localhost:5000 \
           --users 100 --spawn-rate 10 --run-time 60s --headless

    # Generate HTML report:
    locust -f backend/tests/load_testing/locustfile.py --host=http://localhost:5000 \
           --users 100 --spawn-rate 10 --run-time 60s --headless \
           --html=load_test_report.html
"""

from locust import HttpUser, task, between, TaskSet
import random
import json


class AuthTasks(TaskSet):
    """Authentication-related tasks"""

    @task(1)
    def login(self):
        """Test login endpoint"""
        self.client.post(
            "/api/auth/login", json={"username": "admin", "password": "password123"}
        )


class ProductTasks(TaskSet):
    """Product-related tasks"""

    @task(10)
    def list_products(self):
        """Test listing products"""
        page = random.randint(1, 5)
        per_page = random.choice([10, 20, 50])
        self.client.get(f"/api/products?page={page}&per_page={per_page}")

    @task(5)
    def search_products(self):
        """Test searching products"""
        search_terms = ["laptop", "phone", "tablet", "monitor", "keyboard"]
        search = random.choice(search_terms)
        self.client.get(f"/api/products?search={search}")

    @task(3)
    def filter_products_by_category(self):
        """Test filtering products by category"""
        category_id = random.randint(1, 10)
        self.client.get(f"/api/products?category_id={category_id}")

    @task(2)
    def get_product_detail(self):
        """Test getting product detail"""
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}")


class InventoryTasks(TaskSet):
    """Inventory-related tasks"""

    @task(5)
    def list_categories(self):
        """Test listing categories"""
        page = random.randint(1, 3)
        per_page = random.choice([10, 20])
        self.client.get(f"/api/inventory/categories?page={page}&per_page={per_page}")

    @task(5)
    def list_warehouses(self):
        """Test listing warehouses"""
        page = random.randint(1, 3)
        per_page = random.choice([10, 20])
        self.client.get(f"/api/inventory/warehouses?page={page}&per_page={per_page}")

    @task(3)
    def list_stock_movements(self):
        """Test listing stock movements"""
        page = random.randint(1, 5)
        per_page = random.choice([10, 20, 50])
        self.client.get(
            f"/api/inventory/stock-movements?page={page}&per_page={per_page}"
        )

    @task(2)
    def filter_stock_movements(self):
        """Test filtering stock movements"""
        movement_types = ["in", "out", "transfer", "adjustment"]
        movement_type = random.choice(movement_types)
        self.client.get(f"/api/inventory/stock-movements?movement_type={movement_type}")


class InvoiceTasks(TaskSet):
    """Invoice-related tasks"""

    @task(10)
    def list_invoices(self):
        """Test listing invoices"""
        page = random.randint(1, 5)
        per_page = random.choice([10, 20, 50])
        self.client.get(f"/api/invoices?page={page}&per_page={per_page}")

    @task(5)
    def filter_invoices_by_type(self):
        """Test filtering invoices by type"""
        invoice_types = ["sales", "purchase", "sales_return", "purchase_return"]
        invoice_type = random.choice(invoice_types)
        self.client.get(f"/api/invoices?invoice_type={invoice_type}")

    @task(5)
    def filter_invoices_by_status(self):
        """Test filtering invoices by status"""
        statuses = ["draft", "pending", "confirmed", "cancelled"]
        status = random.choice(statuses)
        self.client.get(f"/api/invoices?status={status}")

    @task(3)
    def search_invoices(self):
        """Test searching invoices"""
        search_terms = ["INV", "2025", "customer", "supplier"]
        search = random.choice(search_terms)
        self.client.get(f"/api/invoices?search={search}")

    @task(2)
    def get_invoice_detail(self):
        """Test getting invoice detail"""
        invoice_id = random.randint(1, 100)
        self.client.get(f"/api/invoices/{invoice_id}")


class SystemTasks(TaskSet):
    """System health and monitoring tasks"""

    @task(20)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/api/system/health")

    @task(5)
    def demo_ping(self):
        """Test demo ping endpoint"""
        self.client.get("/api/docs-demo/ping")

    @task(5)
    def external_health(self):
        """Test external health endpoint"""
        self.client.get("/api/docs-integration/external/health")


class ReadOnlyUser(HttpUser):
    """
    Simulates a read-only user (viewer, customer)
    Focuses on GET requests
    """

    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks

    tasks = {ProductTasks: 40, InventoryTasks: 30, InvoiceTasks: 20, SystemTasks: 10}


class RegularUser(HttpUser):
    """
    Simulates a regular user (employee, warehouse staff)
    Mix of read and write operations
    """

    wait_time = between(0.5, 2)  # Wait 0.5-2 seconds between tasks

    tasks = {ProductTasks: 35, InventoryTasks: 35, InvoiceTasks: 25, SystemTasks: 5}


class AdminUser(HttpUser):
    """
    Simulates an admin user
    All operations including auth
    """

    wait_time = between(0.5, 2)

    tasks = {
        AuthTasks: 5,
        ProductTasks: 30,
        InventoryTasks: 30,
        InvoiceTasks: 30,
        SystemTasks: 5,
    }


class StressTestUser(HttpUser):
    """
    Stress test user - rapid fire requests
    """

    wait_time = between(0.1, 0.5)  # Very short wait time

    tasks = {ProductTasks: 40, InventoryTasks: 30, InvoiceTasks: 20, SystemTasks: 10}


# Custom load shape for gradual ramp-up
from locust import LoadTestShape


class GradualRampUp(LoadTestShape):
    """
    Gradual ramp-up load shape
    - Start with 10 users
    - Ramp up to 100 users over 5 minutes
    - Hold at 100 users for 5 minutes
    - Ramp down to 0 over 2 minutes
    """

    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1},  # 1 min: 10 users
        {"duration": 180, "users": 50, "spawn_rate": 2},  # 3 min: 50 users
        {"duration": 300, "users": 100, "spawn_rate": 2},  # 5 min: 100 users
        {"duration": 600, "users": 100, "spawn_rate": 0},  # 10 min: hold at 100
        {"duration": 720, "users": 0, "spawn_rate": 10},  # 12 min: ramp down
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])

        return None


class SpikeTest(LoadTestShape):
    """
    Spike test load shape
    - Normal load: 20 users
    - Spike to 200 users for 1 minute
    - Back to normal
    """

    stages = [
        {"duration": 60, "users": 20, "spawn_rate": 2},  # 1 min: normal
        {"duration": 120, "users": 200, "spawn_rate": 20},  # 2 min: spike!
        {"duration": 180, "users": 20, "spawn_rate": 20},  # 3 min: back to normal
        {"duration": 240, "users": 20, "spawn_rate": 0},  # 4 min: hold
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])

        return None
