# -*- coding: utf-8 -*-
# FILE: backend/tests/test_performance_comprehensive.py | PURPOSE: Comprehensive Performance Tests | OWNER: Backend | RELATED: app.py | LAST-AUDITED: 2025-10-21

"""
اختبارات الأداء الشاملة لنظام إدارة المخزون العربي
Comprehensive Performance Tests for Arabic Inventory Management System

يتضمن:
- اختبارات أداء قاعدة البيانات
- اختبارات أداء API
- اختبارات الذاكرة والموارد
- اختبارات التحميل والضغط
- اختبارات Cache Performance
"""

import pytest
import time
import threading
psutil = pytest.importorskip("psutil")
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import patch

# استيراد التطبيق والنماذج
from app import create_app
from src.database import db
from src.models.product_unified import Product
from src.models.inventory import Category
from src.models.supplier import Supplier
from src.models.customer import Customer
from src.cache_manager import cache_manager


class TestDatabasePerformance:
    """اختبارات أداء قاعدة البيانات"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            self._create_test_data()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def _create_test_data(self):
        """إنشاء بيانات اختبار كبيرة"""
        # إنشاء تصنيفات
        categories = []
        for i in range(50):
            category = Category(
                name=f"Category {i}",
                name_ar=f"تصنيف {i}",
                description=f"Description for category {i}",
                description_ar=f"وصف التصنيف {i}",
            )
            categories.append(category)
            db.session.add(category)

        # إنشاء موردين
        suppliers = []
        for i in range(20):
            supplier = Supplier(
                name=f"Supplier {i}",
                name_ar=f"مورد {i}",
                email=f"supplier{i}@example.com",
                phone=f"123456789{i}",
                address=f"Address {i}",
                address_ar=f"عنوان {i}",
            )
            suppliers.append(supplier)
            db.session.add(supplier)

        db.session.commit()

        # إنشاء منتجات كثيرة
        products = []
        for i in range(1000):
            product = Product(
                name=f"Product {i}",
                name_ar=f"منتج {i}",
                description=f"Description for product {i}",
                description_ar=f"وصف المنتج {i}",
                barcode=f"BAR{i:06d}",
                sku=f"SKU{i:06d}",
                price=100 + (i % 500),
                cost=50 + (i % 250),
                category_id=categories[i % len(categories)].id,
                supplier_id=suppliers[i % len(suppliers)].id if i % 3 == 0 else None,
            )
            products.append(product)
            db.session.add(product)

            # إضافة للدفعة كل 100 منتج
            if i % 100 == 0:
                db.session.commit()

        db.session.commit()

        # إنشاء عملاء
        customers = []
        for i in range(200):
            customer = Customer(
                name=f"Customer {i}",
                name_ar=f"عميل {i}",
                email=f"customer{i}@example.com",
                phone=f"987654321{i}",
                address=f"Customer Address {i}",
                address_ar=f"عنوان العميل {i}",
            )
            customers.append(customer)
            db.session.add(customer)

        db.session.commit()

    def test_product_search_performance(self, app, client):
        """اختبار أداء البحث في المنتجات"""
        with app.app_context():
            start_time = time.time()

            # البحث النصي
            products = Product.search("Product 1").limit(50).all()

            search_time = time.time() - start_time

            # يجب أن يكون البحث سريعاً (أقل من 100ms)
            assert search_time < 0.1
            assert len(products) > 0

    def test_complex_query_performance(self, app):
        """اختبار أداء الاستعلامات المعقدة"""
        with app.app_context():
            start_time = time.time()

            # استعلام معقد مع joins متعددة
            query = (
                db.session.query(Product)
                .join(Category)
                .join(Supplier, Product.supplier_id == Supplier.id, isouter=True)
                .filter(Product.price > 200)
                .filter(Category.is_active.is_(True))
                .order_by(Product.created_at.desc())
                .limit(100)
            )

            products = query.all()

            query_time = time.time() - start_time

            # يجب أن يكون الاستعلام سريعاً (أقل من 200ms)
            assert query_time < 0.2
            assert len(products) > 0

    def test_bulk_insert_performance(self, app):
        """اختبار أداء الإدراج المجمع"""
        with app.app_context():
            start_time = time.time()

            # إدراج 500 منتج جديد
            new_products = []
            for i in range(500):
                product = Product(
                    name=f"Bulk Product {i}",
                    name_ar=f"منتج مجمع {i}",
                    barcode=f"BULK{i:06d}",
                    sku=f"BULKSKU{i:06d}",
                    price=150,
                    cost=75,
                    category_id=1,
                )
                new_products.append(product)

            db.session.bulk_save_objects(new_products)
            db.session.commit()

            insert_time = time.time() - start_time

            # يجب أن يكون الإدراج المجمع سريعاً (أقل من 1 ثانية)
            assert insert_time < 1.0

    def test_pagination_performance(self, app):
        """اختبار أداء التصفح"""
        with app.app_context():
            page_times = []

            # اختبار عدة صفحات
            for page in range(1, 11):
                start_time = time.time()

                products = Product.query.paginate(
                    page=page, per_page=50, error_out=False
                )

                # الوصول للبيانات لضمان تنفيذ الاستعلام
                _ = products.items

                page_time = time.time() - start_time
                page_times.append(page_time)

            # يجب أن تكون جميع الصفحات سريعة
            assert all(t < 0.1 for t in page_times)

            # يجب ألا يزداد الوقت كثيراً مع الصفحات المتأخرة
            assert max(page_times) / min(page_times) < 3


class TestAPIPerformance:
    """اختبارات أداء API"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            self._create_test_data()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def _create_test_data(self):
        """إنشاء بيانات اختبار"""
        # إنشاء تصنيف واحد للاختبار
        category = Category(name="Test Category", name_ar="تصنيف اختبار")
        db.session.add(category)
        db.session.commit()

        # إنشاء منتجات للاختبار
        for i in range(100):
            product = Product(
                name=f"API Test Product {i}",
                name_ar=f"منتج اختبار API {i}",
                barcode=f"API{i:06d}",
                sku=f"APISKU{i:06d}",
                price=100,
                cost=50,
                category_id=category.id,
            )
            db.session.add(product)

        db.session.commit()

    def test_api_response_time(self, client):
        """اختبار وقت استجابة API"""
        endpoints = [
            "/api/products",
            "/api/categories",
            "/api/suppliers",
            "/api/customers",
        ]

        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            response_time = time.time() - start_time

            # يجب أن يكون وقت الاستجابة أقل من 200ms
            assert response_time < 0.2
            assert response.status_code == 200

    def test_concurrent_requests_performance(self, client):
        """اختبار أداء الطلبات المتزامنة"""

        def make_request():
            start_time = time.time()
            response = client.get("/api/products")
            return time.time() - start_time, response.status_code

        # تشغيل 50 طلب متزامن
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [future.result() for future in as_completed(futures)]

        response_times = [result[0] for result in results]
        status_codes = [result[1] for result in results]

        # يجب أن تنجح جميع الطلبات
        assert all(code == 200 for code in status_codes)

        # يجب أن يكون متوسط وقت الاستجابة مقبولاً
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 0.5

    def test_large_payload_performance(self, client):
        """اختبار أداء البيانات الكبيرة"""
        # إنشاء بيانات كبيرة
        large_product_data = {
            "name": "Large Product",
            "name_ar": "منتج كبير",
            "description": "A" * 10000,  # وصف كبير
            "description_ar": "أ" * 10000,
            "barcode": "LARGE001",
            "sku": "LARGESKU001",
            "price": 100,
            "cost": 50,
            "category_id": 1,
        }

        start_time = time.time()
        response = client.post("/api/products", json=large_product_data)
        response_time = time.time() - start_time

        # يجب أن يتعامل مع البيانات الكبيرة بكفاءة
        assert response_time < 1.0
        assert response.status_code in [200, 201, 400, 422]


class TestMemoryPerformance:
    """اختبارات أداء الذاكرة"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    def test_memory_usage_during_bulk_operations(self, app):
        """اختبار استخدام الذاكرة أثناء العمليات المجمعة"""
        with app.app_context():
            # قياس الذاكرة قبل العملية
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024  # MB

            # إنشاء بيانات كثيرة
            category = Category(name="Memory Test", name_ar="اختبار الذاكرة")
            db.session.add(category)
            db.session.commit()

            # إنشاء 1000 منتج
            products = []
            for i in range(1000):
                product = Product(
                    name=f"Memory Product {i}",
                    name_ar=f"منتج ذاكرة {i}",
                    barcode=f"MEM{i:06d}",
                    sku=f"MEMSKU{i:06d}",
                    price=100,
                    cost=50,
                    category_id=category.id,
                )
                products.append(product)

            db.session.bulk_save_objects(products)
            db.session.commit()

            # قياس الذاكرة بعد العملية
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = memory_after - memory_before

            # يجب ألا تزيد الذاكرة كثيراً (أقل من 100MB)
            assert memory_increase < 100

            # تنظيف الذاكرة
            gc.collect()

    def test_memory_leaks_detection(self, app):
        """اختبار كشف تسريب الذاكرة"""
        with app.app_context():
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024

            # تكرار عمليات قاعدة البيانات
            for iteration in range(10):
                # إنشاء وحذف بيانات
                category = Category(
                    name=f"Leak Test {iteration}", name_ar=f"اختبار تسريب {iteration}"
                )
                db.session.add(category)
                db.session.commit()

                # إنشاء منتجات
                for i in range(50):
                    product = Product(
                        name=f"Leak Product {iteration}-{i}",
                        name_ar=f"منتج تسريب {iteration}-{i}",
                        barcode=f"LEAK{iteration:02d}{i:03d}",
                        sku=f"LEAKSKU{iteration:02d}{i:03d}",
                        price=100,
                        cost=50,
                        category_id=category.id,
                    )
                    db.session.add(product)

                db.session.commit()

                # حذف البيانات
                Product.query.filter_by(category_id=category.id).delete()
                db.session.delete(category)
                db.session.commit()

                # تنظيف الذاكرة
                gc.collect()

                # قياس الذاكرة
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_growth = current_memory - initial_memory

                # يجب ألا تنمو الذاكرة كثيراً مع التكرار
                assert memory_growth < 50  # أقل من 50MB نمو


class TestCachePerformance:
    """اختبارات أداء التخزين المؤقت"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        app.config["CACHE_TYPE"] = "simple"
        with app.app_context():
            db.create_all()
            self._create_test_data()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def _create_test_data(self):
        """إنشاء بيانات اختبار"""
        category = Category(name="Cache Test", name_ar="اختبار التخزين المؤقت")
        db.session.add(category)
        db.session.commit()

        for i in range(100):
            product = Product(
                name=f"Cache Product {i}",
                name_ar=f"منتج تخزين مؤقت {i}",
                barcode=f"CACHE{i:06d}",
                sku=f"CACHESKU{i:06d}",
                price=100,
                cost=50,
                category_id=category.id,
            )
            db.session.add(product)

        db.session.commit()

    def test_cache_hit_performance(self, app):
        """اختبار أداء إصابة التخزين المؤقت"""
        with app.app_context():
            # الطلب الأول (cache miss)
            start_time = time.time()
            products_first = Product.query.limit(50).all()
            first_request_time = time.time() - start_time

            # تخزين في الكاش
            cache_key = "products_list_50"
            cache_manager.set(cache_key, products_first, timeout=300)

            # الطلب الثاني (cache hit)
            start_time = time.time()
            cached_products = cache_manager.get(cache_key)
            cache_hit_time = time.time() - start_time

            # يجب أن يكون الكاش أسرع بكثير
            assert cache_hit_time < first_request_time / 10
            assert cached_products is not None
            assert len(cached_products) == len(products_first)

    def test_cache_invalidation_performance(self, app):
        """اختبار أداء إبطال التخزين المؤقت"""
        with app.app_context():
            # تخزين بيانات في الكاش
            cache_keys = []
            for i in range(100):
                key = f"test_key_{i}"
                cache_manager.set(key, f"test_value_{i}", timeout=300)
                cache_keys.append(key)

            # قياس وقت إبطال الكاش
            start_time = time.time()
            for key in cache_keys:
                cache_manager.delete(key)
            invalidation_time = time.time() - start_time

            # يجب أن يكون إبطال الكاش سريعاً
            assert invalidation_time < 0.1

    def test_cache_memory_efficiency(self, app):
        """اختبار كفاءة ذاكرة التخزين المؤقت"""
        with app.app_context():
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024

            # تخزين بيانات كثيرة في الكاش
            large_data = "A" * 10000  # 10KB per item
            for i in range(1000):  # 10MB total
                cache_manager.set(f"large_data_{i}", large_data, timeout=300)

            memory_after = process.memory_info().rss / 1024 / 1024
            memory_increase = memory_after - memory_before

            # يجب أن تكون زيادة الذاكرة معقولة (أقل من 50MB)
            assert memory_increase < 50


class TestLoadTesting:
    """اختبارات التحميل والضغط"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    def test_sustained_load(self, app):
        """اختبار التحميل المستمر"""
        with app.test_client() as client:
            # تشغيل طلبات مستمرة لمدة 30 ثانية
            end_time = time.time() + 30
            request_count = 0
            response_times = []

            while time.time() < end_time:
                start_time = time.time()
                client.get("/api/products")
                response_time = time.time() - start_time

                response_times.append(response_time)
                request_count += 1

                # توقف قصير لمحاكاة الاستخدام الطبيعي
                time.sleep(0.1)

            # تحليل النتائج
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)

            # يجب أن يحافظ على الأداء تحت التحميل
            assert avg_response_time < 0.5
            assert max_response_time < 2.0
            assert request_count > 100  # معدل طلبات معقول

    def test_spike_load(self, app):
        """اختبار التحميل المفاجئ"""
        with app.test_client() as client:

            def burst_requests():
                """إرسال دفعة من الطلبات"""
                times = []
                for _ in range(20):
                    start = time.time()
                    client.get("/api/products")
                    times.append(time.time() - start)
                return times

            # إرسال عدة دفعات متزامنة
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(burst_requests) for _ in range(5)]
                all_times = []
                for future in as_completed(futures):
                    all_times.extend(future.result())

            # تحليل النتائج
            avg_time = sum(all_times) / len(all_times)
            percentile_95 = sorted(all_times)[int(len(all_times) * 0.95)]

            # يجب أن يتعامل مع الذروات بكفاءة
            assert avg_time < 1.0
            assert percentile_95 < 3.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
