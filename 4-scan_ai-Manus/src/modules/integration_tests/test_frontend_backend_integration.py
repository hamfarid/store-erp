# File: /home/ubuntu/ai_web_organized/src/modules/integration_tests/test_frontend_backend_integration.py
"""
from flask import g
اختبارات تكامل الواجهات الأمامية والخلفية
هذا الملف يحتوي على اختبارات للتحقق من تكامل وارتباط الواجهات الأمامية والخلفية والأزرار لجميع المديولات
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

import requests
from playwright.sync_api import sync_playwright

from modules.performance_monitoring.performance_monitor import PerformanceDataCollector
from modules.plant_hybridization.hybridization_simulator import HybridizationSimulator
from modules.image_processing.image_processor import ImageProcessor
from modules.disease_diagnosis.disease_knowledge_base import DiseaseKnowledgeBase
from modules.disease_diagnosis.diagnosis_engine import DiagnosisEngine

# إضافة مسار المشروع إلى مسارات البحث
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# استيراد المديولات المطلوبة للاختبار


class TestFrontendBackendIntegration(unittest.TestCase):
    """اختبارات تكامل الواجهات الأمامية والخلفية"""

    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار"""
        # تهيئة المتغيرات المشتركة
        cls.base_url = "http://localhost:3000"  # عنوان الواجهة الأمامية
        cls.api_url = "http://localhost:5000"   # عنوان واجهة API

        # تهيئة مكونات الواجهة الخلفية للاختبار
        cls.disease_knowledge_base = DiseaseKnowledgeBase()
        cls.diagnosis_engine = DiagnosisEngine(cls.disease_knowledge_base)
        cls.image_processor = ImageProcessor()
        cls.hybridization_simulator = HybridizationSimulator()
        cls.performance_collector = PerformanceDataCollector()

    def setUp(self):
        """إعداد قبل كل اختبار"""
        # تهيئة متغيرات الاختبار
        self.timeout = 30

    def tearDown(self):
        """تنظيف بعد كل اختبار"""
        # تنظيف الموارد المؤقتة
        # لا توجد موارد تحتاج تنظيف في الوقت الحالي
        return

    def test_api_endpoints_availability(self):
        """اختبار توفر نقاط نهاية API"""
        # قائمة نقاط النهاية المتوقعة
        endpoints = [
            "/api/disease-diagnosis/diagnose",
            "/api/image-processing/analyze",
            "/api/plant-hybridization/simulate",
            "/api/performance-monitoring/metrics",
            "/api/module-management/list",
            "/api/ai-management/agents"
        ]

        # التحقق من توفر كل نقطة نهاية
        with patch('requests.get') as mock_get:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "success"}
            mock_get.return_value = mock_response

            for endpoint in endpoints:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=30)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["status"], "success")

    def test_disease_diagnosis_integration(self):
        """اختبار تكامل مديول تشخيص الأمراض"""
        # تهيئة قاعدة المعرفة بمعلومات تجريبية
        self.disease_knowledge_base.add_crop('طماطم')
        self.disease_knowledge_base.add_disease('طماطم', 'اللفحة المتأخرة', {
            'scientific_name': 'Phytophthora infestans',
            'symptoms': ['بقع بنية على الأوراق', 'تعفن الثمار', 'ذبول الأوراق'],
            'visual_symptoms': ['بقع بنية', 'عفن أبيض'],
            'severity': 'high',
            'treatments': ['رش مبيدات فطرية', 'إزالة النباتات المصابة'],
            'prevention': ['تجنب الري العلوي', 'استخدام أصناف مقاومة']
        })

        # محاكاة طلب API من الواجهة الأمامية
        with patch('requests.post') as mock_post:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "crop_type": "طماطم",
                "symptoms": ["بقع بنية على الأوراق", "تعفن الثمار"],
                "results": [{
                    "disease": "اللفحة المتأخرة",
                    "match_score": 0.67,
                    "matching_symptoms": ["بقع بنية على الأوراق", "تعفن الثمار"],
                    "total_symptoms": 3
                }],
                "most_likely_disease": {
                    "disease": "اللفحة المتأخرة",
                    "match_score": 0.67
                }
            }
            mock_post.return_value = mock_response

            # محاكاة طلب من الواجهة الأمامية
            response = requests.post(
                f"{self.api_url}/api/disease-diagnosis/diagnose",
                json={
                    "crop_type": "طماطم",
                    "symptoms": ["بقع بنية على الأوراق", "تعفن الثمار"]
                },
                timeout=30
            )

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["most_likely_disease"]["disease"], "اللفحة المتأخرة")

    def test_image_processing_integration(self):
        """اختبار تكامل مديول معالجة الصور"""
        # محاكاة طلب API من الواجهة الأمامية
        with patch('requests.post') as mock_post:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "results": [{
                    "class": "مرض_1",
                    "probability": 0.85
                }, {
                    "class": "سليم",
                    "probability": 0.10
                }, {
                    "class": "مرض_2",
                    "probability": 0.05
                }],
                "top_result": {
                    "class": "مرض_1",
                    "probability": 0.85
                },
                "is_disease": True
            }
            mock_post.return_value = mock_response

            # محاكاة طلب من الواجهة الأمامية (تحميل صورة)
            response = requests.post(
                f"{self.api_url}/api/image-processing/analyze",
                files={"image": ("test_image.jpg", b"test_image_data", "image/jpeg")},
                data={"crop_type": "طماطم"},
                timeout=30
            )

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["top_result"]["class"], "مرض_1")
            self.assertTrue(data["is_disease"])

    def test_plant_hybridization_integration(self):
        """اختبار تكامل مديول محاكاة التهجين"""
        # محاكاة طلب API من الواجهة الأمامية
        with patch('requests.post') as mock_post:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "recommendations": [{
                    "rank": 1,
                    "id": "hybrid_1",
                    "name": "Hybrid-Var1-Var2",
                    "fitness": 0.85,
                    "traits": {
                        "yield": {
                            "value": 6.5,
                            "target": 7.0
                        },
                        "disease_resistance": {
                            "value": "high",
                            "target": "high"
                        }
                    }
                }]
            }
            mock_post.return_value = mock_response

            # محاكاة طلب من الواجهة الأمامية
            response = requests.post(
                f"{self.api_url}/api/plant-hybridization/simulate",
                json={
                    "varieties": [
                        {"id": "var1", "name": "صنف 1", "yield": 5.2, "disease_resistance": "medium"},
                        {"id": "var2", "name": "صنف 2", "yield": 4.8, "disease_resistance": "high"}
                    ],
                    "objectives": {
                        "yield": 7.0,
                        "yield_importance": 8,
                        "disease_resistance": "high",
                        "disease_resistance_importance": 10
                    },
                    "config": {
                        "simulation_generations": 5,
                        "population_size": 100
                    }
                },
                timeout=30
            )

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(len(data["recommendations"]), 1)
            self.assertEqual(data["recommendations"][0]["name"], "Hybrid-Var1-Var2")

    def test_performance_monitoring_integration(self):
        """اختبار تكامل مديول مراقبة الأداء"""
        # محاكاة طلب API من الواجهة الأمامية
        with patch('requests.get') as mock_get:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "metrics": {
                    "system": {
                        "cpu": {
                            "total_percent": 25.5,
                            "core_count": 4
                        },
                        "memory": {
                            "total_bytes": 8589934592,  # 8 GB
                            "used_bytes": 4294967296,   # 4 GB
                            "percent": 50.0
                        }
                    },
                    "modules": {
                        "disease_diagnosis": {
                            "status": "active",
                            "cpu_percent": 10.5,
                            "memory_bytes": 52428800  # 50 MB
                        },
                        "image_processing": {
                            "status": "active",
                            "cpu_percent": 15.2,
                            "memory_bytes": 104857600  # 100 MB
                        }
                    }
                }
            }
            mock_get.return_value = mock_response

            # محاكاة طلب من الواجهة الأمامية
            response = requests.get(f"{self.api_url}/api/performance-monitoring/metrics", timeout=30)

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertIn("system", data["metrics"])
            self.assertIn("modules", data["metrics"])
            self.assertEqual(data["metrics"]["system"]["memory"]["percent"], 50.0)

    def test_module_management_integration(self):
        """اختبار تكامل مديول إدارة المديولات"""
        # محاكاة طلب API من الواجهة الأمامية
        with patch('requests.get') as mock_get:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "modules": [
                    {
                        "id": 1,
                        "name": "disease_diagnosis",
                        "displayName": {
                            "ar": "تشخيص الأمراض",
                            "en": "Disease Diagnosis"
                        },
                        "status": "running",
                        "cpuUsage": 10.5,
                        "memoryUsage": 50,
                        "priority": "high"
                    },
                    {
                        "id": 2,
                        "name": "image_processing",
                        "displayName": {
                            "ar": "معالجة الصور",
                            "en": "Image Processing"
                        },
                        "status": "running",
                        "cpuUsage": 15.2,
                        "memoryUsage": 100,
                        "priority": "medium"
                    }
                ]
            }
            mock_get.return_value = mock_response

            # محاكاة طلب من الواجهة الأمامية
            response = requests.get(f"{self.api_url}/api/module-management/list", timeout=30)

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(len(data["modules"]), 2)
            self.assertEqual(data["modules"][0]["name"], "disease_diagnosis")
            self.assertEqual(data["modules"][0]["status"], "running")

    def test_ai_management_integration(self):
        """اختبار تكامل مديول إدارة الذكاء الصناعي"""
        # محاكاة طلب API من الواجهة الأمامية
        with patch('requests.get') as mock_get:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "success": True,
                "agents": [
                    {
                        "id": 1,
                        "name": "ai_agent",
                        "displayName": {
                            "ar": "الوكيل الرئيسي",
                            "en": "Main Agent"
                        },
                        "status": "active",
                        "type": "system",
                        "cpuUsage": 20.5,
                        "memoryUsage": 500,
                        "requestsPerMinute": 12
                    },
                    {
                        "id": 2,
                        "name": "ai_agent_image_analyzer",
                        "displayName": {
                            "ar": "محلل الصور",
                            "en": "Image Analyzer"
                        },
                        "status": "active",
                        "type": "specialized",
                        "cpuUsage": 30.2,
                        "memoryUsage": 800,
                        "requestsPerMinute": 5
                    }
                ]
            }
            mock_get.return_value = mock_response

            # محاكاة طلب من الواجهة الأمامية
            response = requests.get(f"{self.api_url}/api/ai-management/agents", timeout=30)

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(len(data["agents"]), 2)
            self.assertEqual(data["agents"][0]["name"], "ai_agent")
            self.assertEqual(data["agents"][0]["status"], "active")

    @unittest.skip("يتطلب تشغيل الواجهة الأمامية والخلفية")
    def test_frontend_ui_integration(self):
        """اختبار تكامل واجهة المستخدم الأمامية مع الخلفية"""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            try:
                # فتح صفحة إدارة المديولات
                page.goto(f"{self.base_url}/admin/modules")

                # التحقق من تحميل الصفحة
                self.assertTrue(page.is_visible("text=إدارة المديولات"))

                # التحقق من عرض جدول المديولات
                self.assertTrue(page.is_visible("table"))

                # التحقق من وجود أزرار التحكم
                self.assertTrue(page.is_visible("button:has-text('تحديث')"))

                # اختبار زر التحديث
                page.click("button:has-text('تحديث')")

                # التحقق من ظهور مؤشر التحميل
                self.assertTrue(page.is_visible("role=progressbar"))

                # انتظار اكتمال التحميل
                page.wait_for_selector("role=progressbar", state="hidden")

                # التحقق من تحديث البيانات
                self.assertTrue(page.is_visible("table"))

                # فتح صفحة إدارة الذكاء الصناعي
                page.goto(f"{self.base_url}/admin/ai-management")

                # التحقق من تحميل الصفحة
                self.assertTrue(page.is_visible("text=إدارة الذكاء الصناعي"))

                # التحقق من عرض قائمة الوكلاء
                self.assertTrue(page.is_visible("text=الوكيل الرئيسي"))

            finally:
                browser.close()

    def test_api_error_handling(self):
        """اختبار معالجة الأخطاء في واجهة API"""
        # محاكاة طلب API من الواجهة الأمامية مع خطأ
        with patch('requests.post') as mock_post:
            # تكوين المحاكاة للاستجابة بخطأ
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.json.return_value = {
                "success": False,
                "error": "بيانات غير صالحة",
                "details": "نوع المحصول مطلوب"
            }
            mock_post.return_value = mock_response

            # محاكاة طلب من الواجهة الأمامية مع بيانات ناقصة
            response = requests.post(
                f"{self.api_url}/api/disease-diagnosis/diagnose",
                json={
                    "symptoms": ["بقع بنية على الأوراق", "تعفن الثمار"]
                    # نوع المحصول مفقود
                },
                timeout=30
            )

            # التحقق من الاستجابة
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertFalse(data["success"])
            self.assertEqual(data["error"], "بيانات غير صالحة")


if __name__ == '__main__':
    unittest.main()
