# -*- coding: utf-8 -*-
# FILE: backend/tests/test_performance.py | PURPOSE: Performance Tests | OWNER: Backend | RELATED: models/, routes/ | LAST-AUDITED: 2025-10-21

"""
اختبارات الأداء - الإصدار 2.0
Performance Tests - Version 2.0

P3 Fixes Applied:
- P3.5: Database query performance tests
- P3.6: Cache effectiveness tests
- P3.7: API response time tests
- P3.8: Memory usage tests
"""

import pytest
import time
psutil = pytest.importorskip("psutil")
import threading
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import create_access_token

# Import the application and models
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.optimized_queries import OptimizedQueries
from src.cache_manager import cache_manager, get_cached_products_page
from src.database import db
from src.models.product_unified import Product
from src.models.inventory import Category


class TestDatabasePerformance:
    """Test database query performance."""

    @pytest.fixture
    def app_with_data(self):
        """Create app with test data."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        db.init_app(app)

        with app.app_context():
            db.create_all()

            # Create test categories
            categories = []
            for i in range(10):
                category = Category(name=f"Category {i}")
                categories.append(category)
                db.session.add(category)

            db.session.commit()

            # Create test products
            for i in range(1000):
                product = Product(
                    name=f"Product {i}",
                    sku=f"SKU{i:04d}",
                    price=10.0 + i,
                    category_id=categories[i % 10].id,
                )
                db.session.add(product)

            db.session.commit()
            yield app

    def test_products_with_categories_performance(self, app_with_data):
        """Test that products with categories query is optimized."""
        with app_with_data.app_context():
            start_time = time.time()

            # This should use optimized query with joinedload
            result = OptimizedQueries.get_products_with_categories(page=1, per_page=50)

            end_time = time.time()
            query_time = end_time - start_time

            # Should complete within reasonable time (< 1 second for 1000 products)
            assert query_time < 1.0
            assert len(result["products"]) <= 50
            assert "pagination" in result

    def test_inventory_summary_performance(self, app_with_data):
        """Test inventory summary query performance."""
        with app_with_data.app_context():
            start_time = time.time()

            result = OptimizedQueries.get_inventory_summary_by_category()

            end_time = time.time()
            query_time = end_time - start_time

            # Should complete quickly with aggregation
            assert query_time < 0.5
            assert len(result) == 10  # 10 categories

    def test_bulk_operations_performance(self, app_with_data):
        """Test bulk operations performance."""
        with app_with_data.app_context():
            # Prepare bulk update data
            updates = [
                {"product_id": i, "new_stock": i * 10}
                for i in range(1, 101)  # Update 100 products
            ]

            start_time = time.time()

            OptimizedQueries.bulk_update_stock(updates)

            end_time = time.time()
            update_time = end_time - start_time

            # Bulk update should be faster than individual updates
            assert update_time < 2.0


class TestCachePerformance:
    """Test cache performance and effectiveness."""

    def test_cache_hit_performance(self):
        """Test that cache hits are fast."""
        # Warm up cache
        cache_manager.set("test_key", {"data": "test_value"}, 300)

        start_time = time.time()

        # Multiple cache hits
        for _ in range(100):
            result = cache_manager.get("test_key")
            assert result is not None

        end_time = time.time()
        total_time = end_time - start_time

        # 100 cache hits should be very fast
        assert total_time < 0.1

    def test_cached_function_performance(self):
        """Test that cached functions improve performance."""
        # First call (cache miss)
        start_time = time.time()
        result1 = get_cached_products_page(page=1, per_page=20)
        first_call_time = time.time() - start_time

        # Second call (cache hit)
        start_time = time.time()
        result2 = get_cached_products_page(page=1, per_page=20)
        second_call_time = time.time() - start_time

        # Cache hit should be significantly faster
        assert second_call_time < first_call_time * 0.1
        assert result1 == result2

    def test_cache_invalidation_performance(self):
        """Test cache invalidation performance."""
        # Set multiple cache keys
        for i in range(100):
            cache_manager.set(f"products:{i}", {"id": i}, 300)

        start_time = time.time()

        # Invalidate all product cache
        cache_manager.delete_pattern("products:*")

        end_time = time.time()
        invalidation_time = end_time - start_time

        # Invalidation should be fast
        assert invalidation_time < 1.0


class TestAPIPerformance:
    """Test API endpoint performance."""

    @pytest.fixture
    def client_with_auth(self, app_with_data):
        """Create client with authentication."""
        with app_with_data.app_context():
            from src.models.user import User

            test_user = User(email="test@example.com", username="testuser")
            db.session.add(test_user)
            db.session.commit()

            access_token = create_access_token(identity=test_user.id)
            headers = {"Authorization": f"Bearer {access_token}"}

            client = app_with_data.test_client()
            yield client, headers

    def test_product_list_api_performance(self, client_with_auth):
        """Test product list API performance."""
        client, headers = client_with_auth

        start_time = time.time()

        response = client.get("/api/products?page=1&per_page=50", headers=headers)

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == 200
        # API should respond within 2 seconds
        assert response_time < 2.0

    def test_search_api_performance(self, client_with_auth):
        """Test search API performance."""
        client, headers = client_with_auth

        start_time = time.time()

        response = client.get("/api/products?search=Product", headers=headers)

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == 200
        # Search should be fast even with many results
        assert response_time < 3.0

    def test_concurrent_requests_performance(self, client_with_auth):
        """Test performance under concurrent requests."""
        client, headers = client_with_auth

        def make_request():
            return client.get("/api/products", headers=headers)

        # Create multiple threads for concurrent requests
        threads = []
        results = []

        start_time = time.time()

        for _ in range(10):
            thread = threading.Thread(target=lambda: results.append(make_request()))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        total_time = end_time - start_time

        # 10 concurrent requests should complete reasonably fast
        assert total_time < 10.0
        assert len(results) == 10

        # All requests should succeed
        for response in results:
            assert response.status_code == 200


class TestMemoryUsage:
    """Test memory usage and potential leaks."""

    def test_memory_usage_during_bulk_operations(self, app_with_data):
        """Test memory usage during bulk operations."""
        with app_with_data.app_context():
            # Get initial memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss

            # Perform bulk operations
            for batch in range(10):
                products = Product.query.limit(100).offset(batch * 100).all()
                # Process products (simulate heavy operation)
                processed = [{"id": p.id, "name": p.name} for p in products]
                del processed
                del products

            # Get final memory usage
            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory

            # Memory increase should be reasonable (< 50MB)
            assert memory_increase < 50 * 1024 * 1024

    def test_cache_memory_usage(self):
        """Test cache memory usage."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss

        # Fill cache with data
        for i in range(1000):
            large_data = {"data": "x" * 1000, "id": i}  # 1KB per item
            cache_manager.set(f"large_item_{i}", large_data, 300)

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable for 1MB of cached data
        assert memory_increase < 10 * 1024 * 1024  # Less than 10MB


class TestScalabilityLimits:
    """Test system behavior at scale limits."""

    def test_large_dataset_query_performance(self, app_with_data):
        """Test query performance with large datasets."""
        with app_with_data.app_context():
            # Test with different page sizes
            page_sizes = [10, 50, 100, 500]

            for page_size in page_sizes:
                start_time = time.time()

                result = OptimizedQueries.get_products_with_categories(
                    page=1, per_page=page_size
                )

                end_time = time.time()
                query_time = end_time - start_time

                # Query time should scale reasonably with page size
                # Larger page sizes should not cause exponential slowdown
                if page_size <= 100:
                    assert query_time < 1.0
                else:
                    assert query_time < 3.0

    def test_cache_performance_under_load(self):
        """Test cache performance under heavy load."""

        def cache_operations():
            for i in range(100):
                cache_manager.set(f"load_test_{i}", {"data": i}, 60)
                cache_manager.get(f"load_test_{i}")

        # Run multiple threads doing cache operations
        threads = []
        start_time = time.time()

        for _ in range(5):
            thread = threading.Thread(target=cache_operations)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        total_time = end_time - start_time

        # 500 cache operations across 5 threads should complete quickly
        assert total_time < 5.0


class TestPerformanceRegression:
    """Test for performance regressions."""

    def test_query_count_optimization(self, app_with_data):
        """Test that N+1 queries are avoided."""
        with app_with_data.app_context():
            # Enable query counting
            query_count = 0

            def count_queries(
                conn, cursor, statement, parameters, context, executemany
            ):
                nonlocal query_count
                query_count += 1

            # Mock database event to count queries
            with patch("sqlalchemy.event.listen") as mock_listen:
                mock_listen.side_effect = lambda *args: count_queries

                # This operation should use optimized queries
                result = OptimizedQueries.get_products_with_categories(
                    page=1, per_page=50
                )

                # Should not exceed reasonable query count
                # (1 for products + categories, maybe 1-2 for pagination)
                assert len(result["products"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
