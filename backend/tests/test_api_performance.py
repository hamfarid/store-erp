#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T14: API Performance Tests
Tests for response time assertions and pagination performance
"""

import pytest
import time
import statistics
from typing import List


@pytest.fixture
def client():
    """Create test client"""
    import sys
    import os

    backend_path = os.path.dirname(os.path.dirname(__file__))
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    from src.main import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestResponseTimeAssertions:
    """Test that API endpoints meet response time SLAs"""

    # SLA definitions (in seconds)
    SLA_GET_SIMPLE = 0.2  # 200ms for simple GET requests
    SLA_GET_LIST = 0.5  # 500ms for list endpoints
    SLA_POST = 0.5  # 500ms for POST requests
    SLA_PUT = 0.5  # 500ms for PUT requests
    SLA_DELETE = 0.3  # 300ms for DELETE requests

    def measure_response_time(self, client, method: str, url: str, **kwargs) -> float:
        """Measure response time for a request"""
        start = time.time()

        if method.upper() == "GET":
            response = client.get(url, **kwargs)
        elif method.upper() == "POST":
            response = client.post(url, **kwargs)
        elif method.upper() == "PUT":
            response = client.put(url, **kwargs)
        elif method.upper() == "DELETE":
            response = client.delete(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

        duration = time.time() - start
        return duration, response

    def test_auth_login_response_time(self, client):
        """Test that /api/auth/login responds within SLA"""
        duration, response = self.measure_response_time(
            client,
            "POST",
            "/api/auth/login",
            json={"username": "admin", "password": "password"},
        )

        # Should respond within SLA (even if auth fails)
        assert (
            duration < self.SLA_POST
        ), f"Login endpoint took {duration:.3f}s, expected < {self.SLA_POST}s"

        # Response should be received (even if 401)
        assert response.status_code in [
            200,
            401,
            500,
        ], f"Unexpected status code: {response.status_code}"

    def test_products_list_response_time(self, client):
        """Test that /api/products responds within SLA"""
        duration, response = self.measure_response_time(client, "GET", "/api/products")

        # Should respond within SLA
        assert (
            duration < self.SLA_GET_LIST
        ), f"Products list took {duration:.3f}s, expected < {self.SLA_GET_LIST}s"

        # Response should be received
        assert response.status_code in [
            200,
            500,
        ], f"Unexpected status code: {response.status_code}"

    def test_inventory_categories_response_time(self, client):
        """Test that /api/inventory/categories responds within SLA"""
        duration, response = self.measure_response_time(
            client, "GET", "/api/inventory/categories"
        )

        # Should respond within SLA
        assert (
            duration < self.SLA_GET_LIST
        ), f"Categories list took {duration:.3f}s, expected < {self.SLA_GET_LIST}s"

        # Response should be received
        assert response.status_code in [
            200,
            500,
        ], f"Unexpected status code: {response.status_code}"

    def test_inventory_warehouses_response_time(self, client):
        """Test that /api/inventory/warehouses responds within SLA"""
        duration, response = self.measure_response_time(
            client, "GET", "/api/inventory/warehouses"
        )

        # Should respond within SLA
        assert (
            duration < self.SLA_GET_LIST
        ), f"Warehouses list took {duration:.3f}s, expected < {self.SLA_GET_LIST}s"

        # Response should be received
        assert response.status_code in [
            200,
            500,
        ], f"Unexpected status code: {response.status_code}"

    def test_invoices_list_response_time(self, client):
        """Test that /api/invoices responds within SLA"""
        duration, response = self.measure_response_time(client, "GET", "/api/invoices")

        # Should respond within SLA
        assert (
            duration < self.SLA_GET_LIST
        ), f"Invoices list took {duration:.3f}s, expected < {self.SLA_GET_LIST}s"

        # Response should be received
        assert response.status_code in [
            200,
            500,
        ], f"Unexpected status code: {response.status_code}"

    def test_average_response_time_across_endpoints(self, client):
        """Test average response time across all endpoints"""
        endpoints = [
            ("GET", "/api/products"),
            ("GET", "/api/inventory/categories"),
            ("GET", "/api/inventory/warehouses"),
            ("GET", "/api/invoices"),
        ]

        durations = []

        for method, url in endpoints:
            duration, response = self.measure_response_time(client, method, url)
            durations.append(duration)

        avg_duration = statistics.mean(durations)
        max_duration = max(durations)

        # Average should be reasonable
        assert (
            avg_duration < 0.3
        ), f"Average response time {avg_duration:.3f}s is too high"

        # No endpoint should be extremely slow
        assert (
            max_duration < 1.0
        ), f"Slowest endpoint took {max_duration:.3f}s, which is too slow"


class TestPaginationPerformance:
    """Test pagination performance across different page sizes"""

    def test_products_pagination_first_page(self, client):
        """Test first page performance"""
        start = time.time()
        response = client.get("/api/products?page=1&per_page=20")
        duration = time.time() - start

        # First page should be fast
        assert duration < 0.5, f"First page took {duration:.3f}s, expected < 0.5s"

        # Should return data (or error if DB not available)
        assert response.status_code in [200, 500]

    def test_products_pagination_different_page_sizes(self, client):
        """Test performance with different page sizes"""
        page_sizes = [10, 20, 50, 100]
        durations = []

        for page_size in page_sizes:
            start = time.time()
            response = client.get(f"/api/products?page=1&per_page={page_size}")
            duration = time.time() - start
            durations.append(duration)

            # Each request should complete reasonably fast
            assert (
                duration < 1.0
            ), f"Page size {page_size} took {duration:.3f}s, expected < 1.0s"

        # Performance should scale reasonably
        # Larger page sizes may take longer, but not exponentially
        if len(durations) >= 2:
            # Last duration shouldn't be more than 3x the first
            assert (
                durations[-1] < durations[0] * 3
            ), "Performance degrades too much with larger page sizes"

    def test_inventory_categories_pagination(self, client):
        """Test inventory categories pagination performance"""
        start = time.time()
        response = client.get("/api/inventory/categories?page=1&per_page=20")
        duration = time.time() - start

        # Should be fast
        assert duration < 0.5, f"Categories pagination took {duration:.3f}s"
        assert response.status_code in [200, 500]

    def test_inventory_warehouses_pagination(self, client):
        """Test inventory warehouses pagination performance"""
        start = time.time()
        response = client.get("/api/inventory/warehouses?page=1&per_page=20")
        duration = time.time() - start

        # Should be fast
        assert duration < 0.5, f"Warehouses pagination took {duration:.3f}s"
        assert response.status_code in [200, 500]

    def test_invoices_pagination_with_filters(self, client):
        """Test invoices pagination with filters performance"""
        # Test with various filters
        filters = [
            "?page=1&per_page=20",
            "?page=1&per_page=20&invoice_type=sales",
            "?page=1&per_page=20&status=draft",
            "?page=1&per_page=20&invoice_type=sales&status=confirmed",
        ]

        durations = []

        for filter_str in filters:
            start = time.time()
            response = client.get(f"/api/invoices{filter_str}")
            duration = time.time() - start
            durations.append(duration)

            # Each request should be reasonably fast
            assert (
                duration < 1.0
            ), f"Invoices with filter '{filter_str}' took {duration:.3f}s"

        # Filters shouldn't significantly degrade performance
        avg_duration = statistics.mean(durations)
        assert (
            avg_duration < 0.6
        ), f"Average filtered query took {avg_duration:.3f}s, expected < 0.6s"

    def test_pagination_consistency(self, client):
        """Test that pagination performance is consistent across multiple requests"""
        durations = []

        # Make 5 requests to the same endpoint
        for _ in range(5):
            start = time.time()
            response = client.get("/api/products?page=1&per_page=20")
            duration = time.time() - start
            durations.append(duration)

        # Calculate standard deviation
        if len(durations) > 1:
            std_dev = statistics.stdev(durations)
            avg = statistics.mean(durations)

            # Standard deviation should be small (consistent performance)
            # Allow up to 50% variation
            assert (
                std_dev < avg * 0.5
            ), f"Performance is inconsistent: avg={avg:.3f}s, std={std_dev:.3f}s"


class TestConcurrentRequests:
    """Test performance under concurrent load (basic)"""

    def test_sequential_requests_baseline(self, client):
        """Establish baseline for sequential requests"""
        num_requests = 10
        start = time.time()

        for _ in range(num_requests):
            response = client.get("/api/products")
            assert response.status_code in [200, 500]

        total_duration = time.time() - start
        avg_duration = total_duration / num_requests

        # Average should be reasonable
        assert (
            avg_duration < 0.5
        ), f"Average request time {avg_duration:.3f}s is too high"

        return avg_duration
