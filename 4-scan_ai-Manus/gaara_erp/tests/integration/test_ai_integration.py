"""
اختبارات التكامل بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي
يحتوي هذا الملف على اختبارات للتحقق من صحة التكامل بين النظامين
"""

import os
import sys
import json
import unittest
import requests
from unittest import mock
from datetime import datetime
import tempfile
import shutil

# إضافة مسار المشروع إلى مسار النظام
sys.path.append('/home/ubuntu/agricultural_ai_system/gaara_erp/src')

# استيراد الوحدات المطلوبة
from core.config.config_manager import ConfigManager
from core.database.db_manager import DBManager
from core.integration.ai_system_integration import AISystemIntegration


class MockResponse:
    """فئة وهمية للاستجابة"""
    
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.text = json.dumps(json_data)
    
    def json(self):
        return self.json_data


class TestAISystemIntegration(unittest.TestCase):
    """اختبارات وحدة التكامل مع نظام الذكاء الاصطناعي"""
    
    def setUp(self):
        """إعداد الاختبار"""
        # إنشاء مجلدات مؤقتة للاختبار
        self.temp_dir = tempfile.mkdtemp()
        self.temp_images_dir = os.path.join(self.temp_dir, 'images')
        self.temp_shared_dir = os.path.join(self.temp_dir, 'shared')
        self.temp_docker_dir = os.path.join(self.temp_dir, 'docker')
        
        os.makedirs(self.temp_images_dir, exist_ok=True)
        os.makedirs(self.temp_shared_dir, exist_ok=True)
        os.makedirs(self.temp_docker_dir, exist_ok=True)
        
        # إنشاء مثيلات وهمية
        self.config_manager = mock.MagicMock(spec=ConfigManager)
        self.db_manager = mock.MagicMock(spec=DBManager)
        
        # تكوين مثيل ConfigManager الوهمي
        self.config_manager.get_config.return_value = {
            "api_base_url": "http://localhost:8000/api",
            "api_key": "test_api_key",
            "temp_images_dir": self.temp_images_dir,
            "shared_data_dir": self.temp_shared_dir,
            "docker_data_dir": self.temp_docker_dir,
            "poll_interval": 10
        }
        
        # إنشاء مثيل AISystemIntegration
        self.ai_integration = AISystemIntegration(self.config_manager, self.db_manager)
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        # حذف المجلدات المؤقتة
        shutil.rmtree(self.temp_dir)
    
    @mock.patch('requests.post')
    def test_send_diagnosis_request(self, mock_post):
        """اختبار إرسال طلب تشخيص"""
        # تكوين الاستجابة الوهمية
        mock_response = MockResponse({"success": True, "message": "تم استلام طلب التشخيص بنجاح"}, 200)
        mock_post.return_value = mock_response
        
        # إنشاء ملف صورة وهمي
        image_path = os.path.join(self.temp_images_dir, 'test_image.jpg')
        with open(image_path, 'w') as f:
            f.write('test image content')
        
        # استدعاء الدالة المراد اختبارها
        result = self.ai_integration._send_diagnosis_request(
            request_id="test_request_id",
            image_path=image_path,
            plant_type="tomato",
            description="اختبار تشخيص",
            metadata='{"source": "test"}'
        )
        
        # التحقق من النتائج
        self.assertTrue(result.get("success"))
        
        # التحقق من استدعاء requests.post بالمعلمات الصحيحة
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # التحقق من عنوان URL
        self.assertEqual(args[0], "http://localhost:8000/api/diagnosis/submit")
        
        # التحقق من البيانات
        self.assertEqual(kwargs['data']['request_id'], "test_request_id")
        self.assertEqual(kwargs['data']['plant_type'], "tomato")
        self.assertEqual(kwargs['data']['description'], "اختبار تشخيص")
        
        # التحقق من الرؤوس
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_api_key")
    
    @mock.patch('requests.get')
    def test_check_diagnosis_status(self, mock_get):
        """اختبار التحقق من حالة طلب التشخيص"""
        # تكوين الاستجابة الوهمية
        mock_response = MockResponse({
            "success": True,
            "status": "completed",
            "result": {
                "result_id": "test_result_id",
                "disease_name": "Late Blight",
                "confidence": 0.95,
                "details": {"symptoms": ["brown spots", "wilting"]},
                "treatment_recommendations": ["fungicide application", "remove infected plants"]
            }
        }, 200)
        mock_get.return_value = mock_response
        
        # استدعاء الدالة المراد اختبارها
        result = self.ai_integration._check_diagnosis_status("test_request_id")
        
        # التحقق من النتائج
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("status"), "completed")
        self.assertEqual(result.get("result").get("disease_name"), "Late Blight")
        
        # التحقق من استدعاء requests.get بالمعلمات الصحيحة
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        
        # التحقق من عنوان URL
        self.assertEqual(args[0], "http://localhost:8000/api/diagnosis/test_request_id/status")
        
        # التحقق من الرؤوس
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_api_key")
    
    def test_update_diagnosis_request_status(self):
        """اختبار تحديث حالة طلب التشخيص"""
        # استدعاء الدالة المراد اختبارها
        self.ai_integration._update_diagnosis_request_status(
            request_id="test_request_id",
            status="processing"
        )
        
        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        self.db_manager.execute_query.assert_called_once()
        args, kwargs = self.db_manager.execute_query.call_args
        
        # التحقق من الاستعلام
        self.assertIn("UPDATE ai_diagnosis_requests", args[0])
        self.assertIn("SET status = %s", args[0])
        self.assertIn("WHERE request_id = %s", args[0])
        
        # التحقق من المعلمات
        self.assertEqual(args[1][0], "processing")
        self.assertEqual(args[1][-1], "test_request_id")
    
    def test_update_diagnosis_request_status_with_error(self):
        """اختبار تحديث حالة طلب التشخيص مع رسالة خطأ"""
        # استدعاء الدالة المراد اختبارها
        self.ai_integration._update_diagnosis_request_status(
            request_id="test_request_id",
            status="failed",
            error_message="خطأ في معالجة الطلب"
        )
        
        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        self.db_manager.execute_query.assert_called_once()
        args, kwargs = self.db_manager.execute_query.call_args
        
        # التحقق من الاستعلام
        self.assertIn("UPDATE ai_diagnosis_requests", args[0])
        self.assertIn("SET status = %s", args[0])
        self.assertIn("error_message = %s", args[0])
        self.assertIn("WHERE request_id = %s", args[0])
        
        # التحقق من المعلمات
        self.assertEqual(args[1][0], "failed")
        self.assertEqual(args[1][2], "خطأ في معالجة الطلب")
        self.assertEqual(args[1][-1], "test_request_id")
    
    @mock.patch('requests.post')
    def test_send_breeding_request(self, mock_post):
        """اختبار إرسال طلب تهجين"""
        # تكوين الاستجابة الوهمية
        mock_response = MockResponse({"success": True, "message": "تم استلام طلب التهجين بنجاح"}, 200)
        mock_post.return_value = mock_response
        
        # بيانات التهجين
        breeding_data = {
            "request_id": "test_request_id",
            "parent_varieties": [
                {"variety_id": "var1", "name": "Roma"},
                {"variety_id": "var2", "name": "Cherry"}
            ],
            "breeding_goals": [
                {"trait": "yield", "target": "increase", "weight": 0.8},
                {"trait": "disease_resistance", "target": "increase", "weight": 0.6}
            ],
            "constraints": {
                "max_generations": 5,
                "population_size": 100
            },
            "parameters": {
                "selection_method": "tournament",
                "crossover_rate": 0.8,
                "mutation_rate": 0.1
            }
        }
        
        # استدعاء الدالة المراد اختبارها
        result = self.ai_integration._send_breeding_request(breeding_data)
        
        # التحقق من النتائج
        self.assertTrue(result.get("success"))
        
        # التحقق من استدعاء requests.post بالمعلمات الصحيحة
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # التحقق من عنوان URL
        self.assertEqual(args[0], "http://localhost:8000/api/breeding/submit")
        
        # التحقق من البيانات
        self.assertEqual(kwargs['json'], breeding_data)
        
        # التحقق من الرؤوس
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_api_key")
        self.assertEqual(kwargs['headers']['Content-Type'], "application/json")
    
    @mock.patch('requests.get')
    def test_check_breeding_status(self, mock_get):
        """اختبار التحقق من حالة طلب التهجين"""
        # تكوين الاستجابة الوهمية
        mock_response = MockResponse({
            "success": True,
            "status": "completed",
            "result": {
                "result_id": "test_result_id",
                "recommended_crosses": [
                    {"parent1": "var1", "parent2": "var2", "score": 0.85}
                ],
                "predicted_traits": {
                    "yield": {"mean": 4.2, "std": 0.3},
                    "disease_resistance": {"mean": 0.8, "std": 0.1}
                },
                "simulation_details": {
                    "generations": 5,
                    "final_population_size": 100
                }
            }
        }, 200)
        mock_get.return_value = mock_response
        
        # استدعاء الدالة المراد اختبارها
        result = self.ai_integration._check_breeding_status("test_request_id")
        
        # التحقق من النتائج
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("status"), "completed")
        self.assertEqual(result.get("result").get("result_id"), "test_result_id")
        
        # التحقق من استدعاء requests.get بالمعلمات الصحيحة
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        
        # التحقق من عنوان URL
        self.assertEqual(args[0], "http://localhost:8000/api/breeding/test_request_id/status")
        
        # التحقق من الرؤوس
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_api_key")
    
    def test_sync_nursery_data(self):
        """اختبار مزامنة بيانات المشاتل"""
        # تكوين استجابة قاعدة البيانات الوهمية
        nursery_data = [
            (
                "nursery1", "مشتل الأمل", "القاهرة", 1000, 500, "user1", "مشتل لإنتاج شتلات الخضروات",
                datetime(2023, 1, 1), datetime(2023, 6, 1),
                '[{"stock_id": "stock1", "variety_id": "var1", "quantity": 200, "status": "active", "planting_date": "2023-01-15", "expected_harvest_date": "2023-03-15"}]'
            )
        ]
        self.db_manager.execute_query.return_value = nursery_data
        
        # استدعاء الدالة المراد اختبارها
        self.ai_integration._sync_nursery_data()
        
        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        self.db_manager.execute_query.assert_called_once()
        args, kwargs = self.db_manager.execute_query.call_args
        
        # التحقق من الاستعلام
        self.assertIn("SELECT n.nursery_id, n.name, n.location", args[0])
        
        # التحقق من إنشاء ملف البيانات
        nursery_file = os.path.join(self.temp_shared_dir, "nursery_data.json")
        self.assertTrue(os.path.exists(nursery_file))
        
        # التحقق من محتوى ملف البيانات
        with open(nursery_file, "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["nursery_id"], "nursery1")
            self.assertEqual(data[0]["name"], "مشتل الأمل")
            self.assertEqual(len(data[0]["stocks"]), 1)
            self.assertEqual(data[0]["stocks"][0]["stock_id"], "stock1")
        
        # التحقق من نسخ الملف إلى مجلد Docker
        docker_nursery_file = os.path.join(self.temp_docker_dir, "nursery_data.json")
        self.assertTrue(os.path.exists(docker_nursery_file))
    
    @mock.patch('requests.get')
    def test_check_ai_system_status(self, mock_get):
        """اختبار التحقق من حالة نظام الذكاء الاصطناعي"""
        # تكوين الاستجابة الوهمية
        mock_response = MockResponse({
            "success": True,
            "status": "running",
            "version": "1.0.0",
            "uptime": "2 days, 3 hours",
            "services": {
                "api": "running",
                "diagnosis": "running",
                "breeding": "running",
                "database": "running"
            },
            "resources": {
                "cpu_usage": 35.2,
                "memory_usage": 42.8,
                "disk_usage": 68.5
            }
        }, 200)
        mock_get.return_value = mock_response
        
        # استدعاء الدالة المراد اختبارها
        result = self.ai_integration.check_ai_system_status()
        
        # التحقق من النتائج
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("status"), "running")
        self.assertEqual(result.get("version"), "1.0.0")
        
        # التحقق من استدعاء requests.get بالمعلمات الصحيحة
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        
        # التحقق من عنوان URL
        self.assertEqual(args[0], "http://localhost:8000/api/system/status")
        
        # التحقق من الرؤوس
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_api_key")


class TestAIIntegrationControllers(unittest.TestCase):
    """اختبارات وحدات التحكم في التكامل مع نظام الذكاء الاصطناعي"""
    
    def setUp(self):
        """إعداد الاختبار"""
        # إنشاء مثيلات وهمية
        self.ai_integration = mock.MagicMock(spec=AISystemIntegration)
        self.db_manager = mock.MagicMock(spec=DBManager)
        self.config_manager = mock.MagicMock(spec=ConfigManager)
        
        # تكوين مثيل AISystemIntegration الوهمي
        self.ai_integration.temp_images_dir = "/tmp/ai_images"
        
        # تكوين المستخدم الحالي
        self.current_user = {
            "user_id": "user1",
            "username": "testuser",
            "permissions": ["ai.diagnosis.create", "ai.diagnosis.view", "ai.breeding.create", "ai.breeding.view", "ai.sync.manage", "ai.system.view"]
        }
    
    @mock.patch('fastapi.UploadFile')
    @mock.patch('fastapi.BackgroundTasks')
    async def test_create_diagnosis_request(self, mock_background_tasks, mock_upload_file):
        """اختبار إنشاء طلب تشخيص"""
        # تكوين ملف التحميل الوهمي
        mock_upload_file.filename = "test_image.jpg"
        mock_upload_file.read = mock.AsyncMock(return_value=b"test image content")
        
        # استيراد وحدة التحكم
        from ai.controllers.ai_integration_controllers import create_diagnosis_request
        
        # استدعاء الدالة المراد اختبارها
        result = await create_diagnosis_request(
            background_tasks=mock_background_tasks,
            plant_type="tomato",
            description="اختبار تشخيص",
            metadata='{"source": "test"}',
            image=mock_upload_file,
            current_user=self.current_user,
            db_manager=self.db_manager,
            ai_integration=self.ai_integration
        )
        
        # التحقق من النتائج
        self.assertEqual(result["status"], "success")
        self.assertIn("request_id", result["data"])
        self.assertEqual(result["data"]["status"], "pending")
        
        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        self.db_manager.execute_query.assert_called_once()
        args, kwargs = self.db_manager.execute_query.call_args
        
        # التحقق من الاستعلام
        self.assertIn("INSERT INTO ai_diagnosis_requests", args[0])
        
        # التحقق من إضافة مهمة المزامنة في الخلفية
        mock_background_tasks.add_task.assert_called_once_with(self.ai_integration._sync_diagnosis_requests)
    
    async def test_get_diagnosis_request(self):
        """اختبار الحصول على طلب تشخيص"""
        # تكوين استجابة قاعدة البيانات الوهمية
        request_data = (
            "req1", "user1", "/tmp/ai_images/req1.jpg", "tomato", "اختبار تشخيص",
            '{"source": "test"}', "completed", None, datetime(2023, 1, 1), datetime(2023, 1, 2),
            "testuser"
        )
        self.db_manager.execute_query.side_effect = [
            [request_data],  # استجابة الاستعلام الأول
            [("res1", "Late Blight", 0.95, '{"symptoms": ["brown spots", "wilting"]}', '["fungicide application", "remove infected plants"]', '[]', datetime(2023, 1, 2))]  # استجابة الاستعلام الثاني
        ]
        
        # استيراد وحدة التحكم
        from ai.controllers.ai_integration_controllers import get_diagnosis_request
        
        # استدعاء الدالة المراد اختبارها
        result = await get_diagnosis_request(
            request_id="req1",
            current_user=self.current_user,
            db_manager=self.db_manager
        )
        
        # التحقق من النتائج
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["request_id"], "req1")
        self.assertEqual(result["data"]["status"], "completed")
        self.assertIn("result", result["data"])
        self.assertEqual(result["data"]["result"]["disease_name"], "Late Blight")
        
        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        self.assertEqual(self.db_manager.execute_query.call_count, 2)
    
    async def test_get_all_diagnosis_requests(self):
        """اختبار الحصول على جميع طلبات التشخيص"""
        # تكوين استجابة قاعدة البيانات الوهمية
        request_data = [
            ("req1", "user1", "/tmp/ai_images/req1.jpg", "tomato", "اختبار تشخيص 1", "completed", datetime(2023, 1, 1), "testuser"),
            ("req2", "user1", "/tmp/ai_images/req2.jpg", "potato", "اختبار تشخيص 2", "processing", datetime(2023, 1, 2), "testuser")
        ]
        self.db_manager.execute_query.side_effect = [
            request_data,  # استجابة الاستعلام الأول
            [(2,)]  # استجابة الاستعلام الثاني (العدد الإجمالي)
        ]
        
        # استيراد وحدة التحكم
        from ai.controllers.ai_integration_controllers import get_all_diagnosis_requests
        
        # استدعاء الدالة المراد اختبارها
        result = await get_all_diagnosis_requests(
            status=None,
            plant_type=None,
            limit=10,
            offset=0,
            current_user=self.current_user,
            db_manager=self.db_manager
        )
        
        # التحقق من النتائج
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]["requests"]), 2)
        self.assertEqual(result["data"]["total"], 2)
        self.assertEqual(result["data"]["requests"][0]["request_id"], "req1")
        self.assertEqual(result["data"]["requests"][1]["request_id"], "req2")
        
        # التحقق من استدعاء execute_query بالمعلمات الصحيحة
        self.assertEqual(self.db_manager.execute_query.call_count, 2)
    
    async def test_start_sync_service(self):
        """اختبار بدء خدمة المزامنة"""
        # تكوين استجابة AISystemIntegration الوهمية
        self.ai_integration.start_sync_service.return_value = True
        
        # استيراد وحدة التحكم
        from ai.controllers.ai_integration_controllers import start_sync_service
        
        # استدعاء الدالة المراد اختبارها
        result = await start_sync_service(
            current_user=self.current_user,
            ai_integration=self.ai_integration
        )
        
        # التحقق من النتائج
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "تم بدء خدمة المزامنة بنجاح")
        
        # التحقق من استدعاء start_sync_service
        self.ai_integration.start_sync_service.assert_called_once()
    
    async def test_get_ai_system_status(self):
        """اختبار الحصول على حالة نظام الذكاء الاصطناعي"""
        # تكوين استجابة AISystemIntegration الوهمية
        self.ai_integration.check_ai_system_status.return_value = {
            "success": True,
            "status": "running",
            "version": "1.0.0",
            "uptime": "2 days, 3 hours",
            "services": {
                "api": "running",
                "diagnosis": "running",
                "breeding": "running",
                "database": "running"
            },
            "resources": {
                "cpu_usage": 35.2,
                "memory_usage": 42.8,
                "disk_usage": 68.5
            }
        }
        
        # استيراد وحدة التحكم
        from ai.controllers.ai_integration_controllers import get_ai_system_status
        
        # استدعاء الدالة المراد اختبارها
        result = await get_ai_system_status(
            current_user=self.current_user,
            ai_integration=self.ai_integration
        )
        
        # التحقق من النتائج
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["status"], "running")
        self.assertEqual(result["data"]["version"], "1.0.0")
        
        # التحقق من استدعاء check_ai_system_status
        self.ai_integration.check_ai_system_status.assert_called_once()


if __name__ == '__main__':
    unittest.main()
