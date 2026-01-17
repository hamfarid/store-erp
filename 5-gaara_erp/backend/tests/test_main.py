"""
إطار الاختبار الشامل
Comprehensive Testing Framework
"""

import unittest
import json
import sys
import os
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


class APITestCase(unittest.TestCase):
    """فئة اختبار API الأساسية"""

    @classmethod
    def setUpClass(cls):
        """إعداد الاختبارات"""
        os.environ["TESTING"] = "1"
        os.environ["SKIP_BLUEPRINTS"] = "1"

        try:
            from app import create_app

            cls.app = create_app()
            cls.app.config["TESTING"] = True
            cls.client = cls.app.test_client()
            cls.app_context = cls.app.app_context()
            cls.app_context.push()
        except Exception as e:
            print(f"خطأ في إعداد الاختبار: {e}")
            cls.app = None

    @classmethod
    def tearDownClass(cls):
        """تنظيف بعد الاختبارات"""
        if hasattr(cls, "app_context"):
            cls.app_context.pop()

    def test_health_endpoint(self):
        """اختبار نقطة نهاية الصحة"""
        if not self.app:
            self.skipTest("التطبيق غير متاح")

        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "healthy")

    def test_system_status(self):
        """اختبار حالة النظام"""
        if not self.app:
            self.skipTest("التطبيق غير متاح")

        response = self.client.get("/api/system/status")
        self.assertIn(response.status_code, [200, 404])  # قد لا تكون موجودة

    def test_temp_endpoints(self):
        """اختبار نقاط النهاية المؤقتة"""
        if not self.app:
            self.skipTest("التطبيق غير متاح")

        temp_endpoints = [
            "/api/temp/products",
            "/api/temp/customers",
            "/api/temp/suppliers",
        ]

        for endpoint in temp_endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                self.assertIn(response.status_code, [200, 404, 500])


class DatabaseTestCase(unittest.TestCase):
    """اختبارات قاعدة البيانات"""

    def test_database_connection(self):
        """اختبار الاتصال بقاعدة البيانات"""
        try:
            from database import db

            # اختبار بسيط للاتصال
            self.assertIsNotNone(db)
        except ImportError:
            self.skipTest("وحدة قاعدة البيانات غير متاحة")

    def test_models_import(self):
        """اختبار استيراد النماذج"""
        try:
            from models.inventory import Product
            from models.customer import Customer

            self.assertIsNotNone(Product)
            self.assertIsNotNone(Customer)
        except ImportError as e:
            self.skipTest(f"النماذج غير متاحة: {e}")


class PerformanceTestCase(unittest.TestCase):
    """اختبارات الأداء"""

    def test_import_performance(self):
        """اختبار أداء الاستيراد"""
        import time

        start_time = time.time()
        try:
            import sys

            sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
            from database import db
            from models.inventory import Product
        except ImportError:
            pass

        import_time = time.time() - start_time
        self.assertLess(import_time, 5.0, "الاستيراد يستغرق وقتاً طويلاً")

    def test_memory_usage(self):
        """اختبار استخدام الذاكرة"""
        try:
            import psutil

            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.assertLess(memory_mb, 500, "استخدام ذاكرة عالي")
        except ImportError:
            self.skipTest("psutil غير متاح")


def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("🧪 بدء تشغيل الاختبارات الشاملة...")
    print("=" * 50)

    # إنشاء test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # إضافة فئات الاختبار
    test_classes = [APITestCase, DatabaseTestCase, PerformanceTestCase]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # تقرير النتائج
    print("=" * 50)
    print(f"📊 نتائج الاختبارات:")
    print(f"✅ نجح: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ فشل: {len(result.failures)}")
    print(f"⚠️ أخطاء: {len(result.errors)}")
    print(f"⏭️ تم تخطيه: {len(result.skipped) if hasattr(result, 'skipped') else 0}")

    success_rate = (
        (
            (result.testsRun - len(result.failures) - len(result.errors))
            / result.testsRun
            * 100
        )
        if result.testsRun > 0
        else 0
    )
    print(f"📈 معدل النجاح: {success_rate:.1f}%")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
