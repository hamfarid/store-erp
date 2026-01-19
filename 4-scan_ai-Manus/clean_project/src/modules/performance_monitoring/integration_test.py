# /home/ubuntu/ai_web_organized/src/modules/performance_monitoring/integration_test.py

"""
from flask import g
اختبار تكامل نظام مراقبة الأداء (Performance Monitoring System Integration Test)

هذا الملف يحتوي على اختبارات تكامل لجميع مكونات نظام مراقبة الأداء،
للتأكد من توافقها مع التصميم وعملها بشكل صحيح معاً.
"""

from modules.performance_monitoring.monitoring_interface import PerformanceMonitoringInterface
from modules.performance_monitoring.report_generator import ReportGenerator
from modules.performance_monitoring.performance_analyzer import PerformanceAnalyzer
from modules.performance_monitoring.data_storage import FileBasedStorage, SQLiteStorage
from modules.performance_monitoring.data_collector import PerformanceDataCollector
from modules.performance_monitoring.performance_monitor import PerformanceMonitor
import os
import sys
import unittest
import logging
import json
import time
from datetime import datetime, timedelta
import tempfile
import shutil

# إعداد مسار النظام للوصول إلى الوحدات
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# استيراد مكونات نظام مراقبة الأداء

# تكوين نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PerformanceMonitoringIntegrationTest(unittest.TestCase):
    """اختبارات تكامل نظام مراقبة الأداء"""

    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار قبل تشغيل جميع الاختبارات"""
        # إنشاء دليل مؤقت للاختبارات
        cls.test_dir = tempfile.mkdtemp()
        cls.data_dir = os.path.join(cls.test_dir, 'data')
        cls.reports_dir = os.path.join(cls.test_dir, 'reports')
        os.makedirs(cls.data_dir, exist_ok=True)
        os.makedirs(cls.reports_dir, exist_ok=True)

        # إنشاء ملف تكوين للاختبارات
        cls.config_path = os.path.join(cls.test_dir, 'test_config.json')
        cls.config = {
            "data_dir": cls.data_dir,
            "reports_dir": cls.reports_dir,
            "collection_interval": 5,  # 5 seconds for testing
            "retention_period": 30,  # 30 days
            "storage_type": "file",  # file or sqlite
            "sqlite_db_path": os.path.join(cls.test_dir, 'performance_data.db'),
            "alert_thresholds": {
                "cpu_percent": {"warning": 70, "critical": 90},
                "memory_percent": {"warning": 70, "critical": 90},
                "disk_percent": {"warning": 70, "critical": 90},
                "error_rate": {"warning": 0.05, "critical": 0.1}
            }
        }

        with open(cls.config_path, 'w') as f:
            json.dump(cls.config, f, indent=4)

        # إنشاء بيانات اختبار
        cls._create_test_data()

    @classmethod
    def tearDownClass(cls):
        """تنظيف بيئة الاختبار بعد تشغيل جميع الاختبارات"""
        # حذف الدليل المؤقت
        shutil.rmtree(cls.test_dir)

    @classmethod
    def _create_test_data(cls):
        """إنشاء بيانات اختبار"""
        # إنشاء بيانات اختبار لمقاييس النظام
        system_metrics_file = os.path.join(cls.data_dir, 'system_metrics.json')
        system_metrics = []

        # إنشاء بيانات لآخر 24 ساعة
        now = datetime.now()
        for i in range(24):
            timestamp = (now - timedelta(hours=24 - i)).isoformat()

            # محاكاة زيادة استهلاك CPU والذاكرة خلال ساعات العمل
            hour = (now - timedelta(hours=24 - i)).hour
            if 8 <= hour <= 17:  # ساعات العمل
                cpu_percent = 50 + (i % 5) * 10  # 50-90%
                memory_percent = 60 + (i % 4) * 10  # 60-90%
            else:
                cpu_percent = 20 + (i % 3) * 5  # 20-30%
                memory_percent = 30 + (i % 3) * 5  # 30-40%

            # محاكاة استهلاك القرص الثابت
            disk_percent = 50 + (i // 8)  # زيادة تدريجية من 50% إلى 53%

            metrics = {
                "timestamp": timestamp,
                "cpu.total_percent": cpu_percent,
                "cpu.user_percent": cpu_percent * 0.7,
                "cpu.system_percent": cpu_percent * 0.3,
                "memory.total": 16 * 1024 * 1024 * 1024,  # 16 GB
                "memory.available": (16 * 1024 * 1024 * 1024) * (1 - memory_percent / 100),
                "memory.used": (16 * 1024 * 1024 * 1024) * (memory_percent / 100),
                "memory.percent": memory_percent,
                "disk.total": 500 * 1024 * 1024 * 1024,  # 500 GB
                "disk.used": (500 * 1024 * 1024 * 1024) * (disk_percent / 100),
                "disk.free": (500 * 1024 * 1024 * 1024) * (1 - disk_percent / 100),
                "disk.percent": disk_percent,
                "network.bytes_sent": 1024 * 1024 * (i + 1),
                "network.bytes_recv": 2048 * 1024 * (i + 1),
                "system.boot_time": (now - timedelta(days=7)).timestamp(),
                "system.uptime": 7 * 24 * 3600 - (24 - i) * 3600
            }

            system_metrics.append(metrics)

        with open(system_metrics_file, 'w') as f:
            json.dump(system_metrics, f, indent=4)

        # إنشاء بيانات اختبار لمقاييس المديولات
        modules = ['backup_module', 'data_validation', 'ai_module', 'user_management']

        for module in modules:
            module_metrics_file = os.path.join(cls.data_dir, f'module_{module}_metrics.json')
            module_metrics = []

            for i in range(24):
                timestamp = (now - timedelta(hours=24 - i)).isoformat()

                # محاكاة استهلاك الموارد
                hour = (now - timedelta(hours=24 - i)).hour
                if 8 <= hour <= 17:  # ساعات العمل
                    cpu_percent = 30 + (i % 5) * 10  # 30-70%
                    memory_mb = 200 + (i % 5) * 50  # 200-400 MB

                    # محاكاة مشكلة في مديول النسخ الاحتياطي
                    if module == 'backup_module' and 14 <= hour <= 15:
                        cpu_percent = 90  # استهلاك CPU مرتفع
                        error_rate = 0.15  # معدل أخطاء مرتفع
                    else:
                        error_rate = 0.01 + (i % 10) * 0.005  # 0.01-0.055
                else:
                    cpu_percent = 10 + (i % 3) * 5  # 10-20%
                    memory_mb = 100 + (i % 3) * 20  # 100-160 MB
                    error_rate = 0.005  # معدل أخطاء منخفض

                # محاكاة أداء المديول
                if module == 'ai_module':
                    response_time = 200 + (i % 5) * 50  # 200-400 ms
                    throughput = 50 - (i % 5) * 5  # 30-50 req/s
                elif module == 'data_validation':
                    response_time = 50 + (i % 3) * 10  # 50-70 ms
                    throughput = 200 - (i % 5) * 20  # 100-200 req/s
                elif module == 'backup_module':
                    response_time = 500 + (i % 5) * 100  # 500-900 ms
                    throughput = 10 - (i % 3)  # 8-10 req/s
                else:
                    response_time = 100 + (i % 4) * 25  # 100-175 ms
                    throughput = 100 - (i % 4) * 10  # 70-100 req/s

                metrics = {
                    "timestamp": timestamp,
                    "module_id": module,
                    "resources.cpu_percent": cpu_percent,
                    "resources.memory_mb": memory_mb,
                    "resources.thread_count": 5 + (i % 3),
                    "performance.response_time_ms": response_time,
                    "performance.throughput": throughput,
                    "performance.error_rate": error_rate,
                    "performance.request_count": 1000 + i * 100,
                    "performance.success_count": int((1000 + i * 100) * (1 - error_rate)),
                    "performance.error_count": int((1000 + i * 100) * error_rate)
                }

                module_metrics.append(metrics)

            with open(module_metrics_file, 'w') as f:
                json.dump(module_metrics, f, indent=4)

        # إنشاء بيانات اختبار لمقاييس الذكاء الصناعي
        ai_models = ['text_classification', 'image_recognition', 'recommendation_engine']

        for model in ai_models:
            ai_metrics_file = os.path.join(cls.data_dir, f'ai_{model}_metrics.json')
            ai_metrics = []

            for i in range(24):
                timestamp = (now - timedelta(hours=24 - i)).isoformat()

                # محاكاة استهلاك الموارد
                hour = (now - timedelta(hours=24 - i)).hour
                if 8 <= hour <= 17:  # ساعات العمل
                    gpu_percent = 60 + (i % 4) * 10  # 60-90%
                    memory_mb = 2000 + (i % 5) * 500  # 2000-4000 MB

                    # محاكاة مشكلة في نموذج التعرف على الصور
                    if model == 'image_recognition' and 10 <= hour <= 12:
                        gpu_percent = 95  # استهلاك GPU مرتفع
                        accuracy = 0.75  # دقة منخفضة
                    else:
                        accuracy = 0.90 + (i % 10) * 0.01  # 0.90-0.99
                else:
                    gpu_percent = 20 + (i % 3) * 10  # 20-40%
                    memory_mb = 1000 + (i % 3) * 200  # 1000-1400 MB
                    accuracy = 0.95  # دقة مرتفعة

                # محاكاة أداء النموذج
                if model == 'text_classification':
                    latency = 50 + (i % 5) * 10  # 50-90 ms
                    throughput = 100 - (i % 5) * 10  # 60-100 req/s
                elif model == 'image_recognition':
                    latency = 200 + (i % 5) * 50  # 200-400 ms
                    throughput = 20 - (i % 4) * 2  # 12-20 req/s
                else:
                    latency = 100 + (i % 4) * 25  # 100-175 ms
                    throughput = 50 - (i % 5) * 5  # 30-50 req/s

                metrics = {
                    "timestamp": timestamp,
                    "model_id": model,
                    "resources.gpu_percent": gpu_percent,
                    "resources.memory_mb": memory_mb,
                    "resources.cpu_percent": 30 + (i % 5) * 5,  # 30-50%
                    "performance.latency_ms": latency,
                    "performance.throughput": throughput,
                    "performance.accuracy": accuracy,
                    "performance.request_count": 1000 + i * 100,
                    "performance.cache_hit_ratio": 0.7 + (i % 6) * 0.05  # 0.7-0.95
                }

                ai_metrics.append(metrics)

            with open(ai_metrics_file, 'w') as f:
                json.dump(ai_metrics, f, indent=4)

    def setUp(self):
        """إعداد بيئة الاختبار قبل كل اختبار"""
        # إنشاء مكونات نظام مراقبة الأداء
        if self.config["storage_type"] == "file":
            self.storage = FileBasedStorage(self.data_dir)
        else:
            self.storage = SQLiteStorage(self.config["sqlite_db_path"])

        self.data_collector = PerformanceDataCollector(self.storage, self.config)
        self.performance_analyzer = PerformanceAnalyzer(self.data_collector, self.config)
        self.report_generator = ReportGenerator(self.performance_analyzer, self.config)

        self.performance_monitor = PerformanceMonitor(
            self.data_collector,
            self.performance_analyzer,
            self.report_generator,
            self.config
        )

    def test_data_collector_initialization(self):
        """اختبار تهيئة جامع البيانات"""
        self.assertIsNotNone(self.data_collector)
        self.assertEqual(self.data_collector.storage, self.storage)
        self.assertEqual(self.data_collector.config, self.config)

    def test_performance_analyzer_initialization(self):
        """اختبار تهيئة محلل الأداء"""
        self.assertIsNotNone(self.performance_analyzer)
        self.assertEqual(self.performance_analyzer.data_collector, self.data_collector)
        self.assertEqual(self.performance_analyzer.config, self.config)

    def test_report_generator_initialization(self):
        """اختبار تهيئة مولد التقارير"""
        self.assertIsNotNone(self.report_generator)
        self.assertEqual(self.report_generator.performance_analyzer, self.performance_analyzer)
        self.assertEqual(self.report_generator.config, self.config)

    def test_performance_monitor_initialization(self):
        """اختبار تهيئة نظام مراقبة الأداء"""
        self.assertIsNotNone(self.performance_monitor)
        self.assertEqual(self.performance_monitor.data_collector, self.data_collector)
        self.assertEqual(self.performance_monitor.performance_analyzer, self.performance_analyzer)
        self.assertEqual(self.performance_monitor.report_generator, self.report_generator)
        self.assertEqual(self.performance_monitor.config, self.config)

    def test_get_system_metrics(self):
        """اختبار الحصول على مقاييس النظام"""
        metrics = self.data_collector.get_system_metrics("1d")
        self.assertIsNotNone(metrics)
        self.assertGreater(len(metrics), 0)

        # التحقق من وجود الحقول المتوقعة
        expected_fields = [
            "timestamp", "cpu.total_percent", "memory.percent", "disk.percent"
        ]

        for field in expected_fields:
            self.assertIn(field, metrics[0])

    def test_get_module_metrics(self):
        """اختبار الحصول على مقاييس المديولات"""
        modules = self.data_collector.get_active_modules()
        self.assertIsNotNone(modules)
        self.assertGreater(len(modules), 0)

        for module in modules:
            metrics = self.data_collector.get_module_metrics(module, "1d")
            self.assertIsNotNone(metrics)
            self.assertGreater(len(metrics), 0)

            # التحقق من وجود الحقول المتوقعة
            expected_fields = [
                "timestamp", "module_id", "resources.cpu_percent",
                "resources.memory_mb", "performance.response_time_ms"
            ]

            for field in expected_fields:
                self.assertIn(field, metrics[0])

    def test_get_ai_metrics(self):
        """اختبار الحصول على مقاييس الذكاء الصناعي"""
        ai_models = self.data_collector.get_active_ai_models()
        self.assertIsNotNone(ai_models)
        self.assertGreater(len(ai_models), 0)

        for model in ai_models:
            metrics = self.data_collector.get_ai_metrics(model, "1d")
            self.assertIsNotNone(metrics)
            self.assertGreater(len(metrics), 0)

            # التحقق من وجود الحقول المتوقعة
            expected_fields = [
                "timestamp", "model_id", "resources.gpu_percent",
                "resources.memory_mb", "performance.accuracy"
            ]

            for field in expected_fields:
                self.assertIn(field, metrics[0])

    def test_analyze_performance_trend(self):
        """اختبار تحليل اتجاه الأداء"""
        # تحليل اتجاه أداء النظام
        trend = self.performance_analyzer.analyze_performance_trend("system", None, "1d")
        self.assertIsNotNone(trend)
        self.assertEqual(trend.entity_type, "system")

        # تحليل اتجاه أداء المديولات
        modules = self.data_collector.get_active_modules()
        for module in modules:
            trend = self.performance_analyzer.analyze_performance_trend("module", module, "1d")
            self.assertIsNotNone(trend)
            self.assertEqual(trend.entity_type, "module")
            self.assertEqual(trend.entity_id, module)

        # تحليل اتجاه أداء الذكاء الصناعي
        ai_models = self.data_collector.get_active_ai_models()
        for model in ai_models:
            trend = self.performance_analyzer.analyze_performance_trend("ai", model, "1d")
            self.assertIsNotNone(trend)
            self.assertEqual(trend.entity_type, "ai")
            self.assertEqual(trend.entity_id, model)

    def test_detect_performance_anomalies(self):
        """اختبار اكتشاف شذوذ الأداء"""
        # اكتشاف شذوذ أداء النظام
        anomalies = self.performance_analyzer.detect_performance_anomalies("system", None, "1d")
        self.assertIsNotNone(anomalies)

        # اكتشاف شذوذ أداء المديولات
        modules = self.data_collector.get_active_modules()
        for module in modules:
            anomalies = self.performance_analyzer.detect_performance_anomalies("module", module, "1d")
            self.assertIsNotNone(anomalies)

            # التحقق من وجود شذوذ في مديول النسخ الاحتياطي
            if module == 'backup_module':
                self.assertGreater(len(anomalies), 0)
                for anomaly in anomalies:
                    self.assertEqual(anomaly.entity_id, module)

        # اكتشاف شذوذ أداء الذكاء الصناعي
        ai_models = self.data_collector.get_active_ai_models()
        for model in ai_models:
            anomalies = self.performance_analyzer.detect_performance_anomalies("ai", model, "1d")
            self.assertIsNotNone(anomalies)

            # التحقق من وجود شذوذ في نموذج التعرف على الصور
            if model == 'image_recognition':
                self.assertGreater(len(anomalies), 0)
                for anomaly in anomalies:
                    self.assertEqual(anomaly.entity_id, model)

    def test_generate_performance_recommendations(self):
        """اختبار توليد توصيات تحسين الأداء"""
        # توليد توصيات لتحسين أداء النظام
        recommendations = self.performance_analyzer.generate_performance_recommendations("system")
        self.assertIsNotNone(recommendations)

        # توليد توصيات لتحسين أداء المديولات
        modules = self.data_collector.get_active_modules()
        for module in modules:
            recommendations = self.performance_analyzer.generate_performance_recommendations(module)
            self.assertIsNotNone(recommendations)

            # التحقق من وجود توصيات لمديول النسخ الاحتياطي
            if module == 'backup_module':
                self.assertGreater(len(recommendations), 0)
                for recommendation in recommendations:
                    self.assertEqual(recommendation.entity_id, module)

        # توليد توصيات لتحسين أداء الذكاء الصناعي
        ai_models = self.data_collector.get_active_ai_models()
        for model in ai_models:
            recommendations = self.performance_analyzer.generate_performance_recommendations(model)
            self.assertIsNotNone(recommendations)

            # التحقق من وجود توصيات لنموذج التعرف على الصور
            if model == 'image_recognition':
                self.assertGreater(len(recommendations), 0)
                for recommendation in recommendations:
                    self.assertEqual(recommendation.entity_id, model)

    def test_generate_system_performance_report(self):
        """اختبار إنشاء تقرير أداء النظام"""
        # إنشاء تكوين التقرير
        report_config = self.report_generator.ReportConfig(
            title="تقرير أداء النظام",
            description="تقرير اختبار أداء النظام",
            time_range="1d",
            include_charts=True,
            include_recommendations=True,
            include_anomalies=True,
            include_trends=True,
            output_format="html",
            output_dir=self.reports_dir
        )

        # إنشاء التقرير
        report_path = self.report_generator.generate_system_performance_report(report_config)
        self.assertIsNotNone(report_path)
        self.assertTrue(os.path.exists(report_path))

        # التحقق من محتوى التقرير
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("تقرير أداء النظام", content)
            self.assertIn("CPU", content)
            self.assertIn("الذاكرة", content)
            self.assertIn("القرص", content)

    def test_generate_module_performance_report(self):
        """اختبار إنشاء تقرير أداء المديول"""
        # إنشاء تكوين التقرير
        report_config = self.report_generator.ReportConfig(
            title="تقرير أداء المديول",
            description="تقرير اختبار أداء المديول",
            time_range="1d",
            include_charts=True,
            include_recommendations=True,
            include_anomalies=True,
            include_trends=True,
            output_format="html",
            output_dir=self.reports_dir
        )

        # إنشاء التقرير لمديول النسخ الاحتياطي
        module_id = "backup_module"
        report_path = self.report_generator.generate_module_performance_report(module_id, report_config)
        self.assertIsNotNone(report_path)
        self.assertTrue(os.path.exists(report_path))

        # التحقق من محتوى التقرير
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("تقرير أداء المديول", content)
            self.assertIn(module_id, content)
            self.assertIn("استهلاك CPU", content)
            self.assertIn("استهلاك الذاكرة", content)
            self.assertIn("معدل الأخطاء", content)

    def test_generate_ai_performance_report(self):
        """اختبار إنشاء تقرير أداء الذكاء الصناعي"""
        # إنشاء تكوين التقرير
        report_config = self.report_generator.ReportConfig(
            title="تقرير أداء الذكاء الصناعي",
            description="تقرير اختبار أداء الذكاء الصناعي",
            time_range="1d",
            include_charts=True,
            include_recommendations=True,
            include_anomalies=True,
            include_trends=True,
            output_format="html",
            output_dir=self.reports_dir
        )

        # إنشاء التقرير لنموذج التعرف على الصور
        model_id = "image_recognition"
        report_path = self.report_generator.generate_ai_performance_report(model_id, report_config)
        self.assertIsNotNone(report_path)
        self.assertTrue(os.path.exists(report_path))

        # التحقق من محتوى التقرير
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("تقرير أداء الذكاء الصناعي", content)
            self.assertIn(model_id, content)
            self.assertIn("استهلاك GPU", content)
            self.assertIn("الدقة", content)
            self.assertIn("زمن الاستجابة", content)

    def test_generate_comprehensive_report(self):
        """اختبار إنشاء تقرير شامل"""
        # إنشاء تكوين التقرير
        report_config = self.report_generator.ReportConfig(
            title="تقرير أداء شامل",
            description="تقرير اختبار أداء شامل للنظام والمديولات والذكاء الصناعي",
            time_range="1d",
            include_charts=True,
            include_recommendations=True,
            include_anomalies=True,
            include_trends=True,
            output_format="html",
            output_dir=self.reports_dir
        )

        # إنشاء التقرير الشامل
        report_path = self.report_generator.generate_comprehensive_report(report_config)
        self.assertIsNotNone(report_path)
        self.assertTrue(os.path.exists(report_path))

        # التحقق من محتوى التقرير
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("تقرير أداء شامل", content)
            self.assertIn("أداء النظام", content)
            self.assertIn("أداء المديولات", content)
            self.assertIn("أداء الذكاء الصناعي", content)
            self.assertIn("التوصيات", content)
            self.assertIn("الشذوذ", content)

    def test_monitoring_interface_initialization(self):
        """اختبار تهيئة واجهة مراقبة الأداء"""
        # إنشاء واجهة مراقبة الأداء
        interface = PerformanceMonitoringInterface(self.performance_monitor, self.config_path)
        self.assertIsNotNone(interface)
        self.assertEqual(interface.performance_monitor, self.performance_monitor)

        # التحقق من تهيئة التطبيق
        self.assertIsNotNone(interface.app)

        # التحقق من تحميل الإعدادات
        self.assertIsNotNone(interface.config)
        self.assertIn("host", interface.config)
        self.assertIn("port", interface.config)
        self.assertIn("alert_thresholds", interface.config)

    def test_monitoring_interface_routes(self):
        """اختبار مسارات واجهة مراقبة الأداء"""
        # إنشاء واجهة مراقبة الأداء
        interface = PerformanceMonitoringInterface(self.performance_monitor, self.config_path)

        # الحصول على قائمة المسارات
        routes = [str(rule) for rule in interface.app.url_map.iter_rules()]

        # التحقق من وجود المسارات المتوقعة
        expected_routes = [
            '/',
            '/login',
            '/api/system/metrics',
            '/api/modules/metrics',
            '/api/ai/metrics',
            '/api/database/metrics',
            '/api/system/analysis',
            '/api/modules/analysis',
            '/api/recommendations',
            '/api/reports/generate',
            '/api/reports/download',
            '/api/alerts',
            '/api/alerts/acknowledge',
            '/api/settings',
            '/api/modules/list',
            '/api/ai/list',
            '/api/database/list',
            '/api/modules/resource-intensive',
            '/api/modules/low-performing',
            '/dashboard',
            '/system',
            '/modules',
            '/ai',
            '/database',
            '/reports',
            '/alerts',
            '/settings'
        ]

        for route in expected_routes:
            self.assertIn(route, routes)

    def test_create_templates(self):
        """اختبار إنشاء قوالب واجهة المستخدم"""
        # إنشاء واجهة مراقبة الأداء
        interface = PerformanceMonitoringInterface(self.performance_monitor, self.config_path)

        # إنشاء القوالب
        interface.create_templates()

        # التحقق من وجود القوالب
        templates_dir = os.path.join(os.path.dirname(os.path.abspath(interface.__module__)), 'templates')
        dashboard_dir = os.path.join(templates_dir, 'admin_panel', 'performance_monitoring')

        self.assertTrue(os.path.exists(os.path.join(dashboard_dir, 'dashboard.html')))
        self.assertTrue(os.path.exists(os.path.join(dashboard_dir, 'login.html')))

    def test_integration_end_to_end(self):
        """اختبار تكامل نهاية إلى نهاية"""
        # إنشاء نظام مراقبة الأداء
        performance_monitor = PerformanceMonitor(
            self.data_collector,
            self.performance_analyzer,
            self.report_generator,
            self.config
        )

        # إنشاء واجهة مراقبة الأداء
        interface = PerformanceMonitoringInterface(performance_monitor, self.config_path)
        interface.create_templates()

        # محاكاة دورة جمع البيانات
        performance_monitor.collect_data()

        # محاكاة تحليل الأداء
        system_anomalies = performance_monitor.performance_analyzer.detect_performance_anomalies("system", None, "1d")
        self.assertIsNotNone(system_anomalies)

        # محاكاة إنشاء تقرير
        report_config = performance_monitor.report_generator.ReportConfig(
            title="تقرير أداء النظام",
            description="تقرير اختبار أداء النظام",
            time_range="1d",
            include_charts=True,
            include_recommendations=True,
            include_anomalies=True,
            include_trends=True,
            output_format="html",
            output_dir=self.reports_dir
        )

        report_path = performance_monitor.report_generator.generate_system_performance_report(report_config)
        self.assertIsNotNone(report_path)
        self.assertTrue(os.path.exists(report_path))

        # محاكاة فحص التنبيهات
        interface._check_alerts()

        # التحقق من وجود تنبيهات نشطة
        self.assertIsNotNone(interface.active_alerts)


if __name__ == '__main__':
    unittest.main()
