# File: /home/ubuntu/clean_project/tests/test_api_endpoints.py
"""
مسار الملف: /home/ubuntu/clean_project/tests/test_api_endpoints.py

اختبارات شاملة لواجهات برمجة التطبيقات
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# إضافة مسار src إلى Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi.testclient import TestClient
from main import app
from auth_service import AuthService

class TestAPIEndpoints(unittest.TestCase):
    """اختبارات واجهات برمجة التطبيقات"""
    
    def setUp(self):
        """إعداد عميل الاختبار"""
        self.client = TestClient(app)
        self.auth_service = AuthService(secret_key="test_secret")
        
        # إنشاء رمز مصادقة للاختبار
        self.test_token = self.auth_service.create_token(1, "test_user", False)
        self.admin_token = self.auth_service.create_token(2, "admin_user", True)
        
        self.headers = {"Authorization": f"Bearer {self.test_token}"}
        self.admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
    
    def test_health_check(self):
        """اختبار نقطة فحص صحة النظام"""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "healthy")
    
    def test_dashboard_stats_unauthorized(self):
        """اختبار الوصول غير المصرح به لإحصائيات لوحة التحكم"""
        response = self.client.get("/api/dashboard/stats")
        self.assertEqual(response.status_code, 401)
    
    def test_dashboard_stats_authorized(self):
        """اختبار الوصول المصرح به لإحصائيات لوحة التحكم"""
        with patch('modules.ai_management.api.get_ai_stats') as mock_stats:
            mock_stats.return_value = {
                "total_diagnoses": 100,
                "active_users": 25,
                "accuracy_rate": 0.95,
                "system_health": "good"
            }
            
            response = self.client.get("/api/dashboard/stats", headers=self.headers)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn("total_diagnoses", data)
            self.assertIn("active_users", data)
    
    def test_diagnosis_create_no_image(self):
        """اختبار إنشاء تشخيص بدون صورة"""
        response = self.client.post("/api/diagnosis/analyze", headers=self.headers)
        self.assertEqual(response.status_code, 400)
    
    def test_diagnosis_create_with_image(self):
        """اختبار إنشاء تشخيص مع صورة"""
        # محاكاة ملف صورة
        files = {
            "image": ("test.jpg", b"fake image data", "image/jpeg")
        }
        data = {
            "crop_type": "tomato"
        }
        
        with patch('modules.disease_diagnosis.api.analyze_image') as mock_analyze:
            mock_analyze.return_value = {
                "disease_name": "اللفحة المبكرة",
                "confidence": 0.92,
                "severity": "متوسط",
                "symptoms": "بقع بنية على الأوراق",
                "treatment": "استخدام مبيدات فطرية",
                "prevention": "تحسين التهوية"
            }
            
            response = self.client.post(
                "/api/diagnosis/analyze",
                headers=self.headers,
                files=files,
                data=data
            )
            
            self.assertEqual(response.status_code, 200)
            result = response.json()
            self.assertIn("disease_name", result)
            self.assertIn("confidence", result)
    
    def test_activity_log_get(self):
        """اختبار الحصول على سجل النشاط"""
        with patch('modules.activity_log.api.get_recent_activities') as mock_activities:
            mock_activities.return_value = [
                {
                    "id": 1,
                    "type": "diagnosis_created",
                    "message": "تم إنشاء تشخيص جديد",
                    "created_at": "2024-01-01T10:00:00"
                }
            ]
            
            response = self.client.get("/api/activity-log/recent", headers=self.headers)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn("type", data[0])
                self.assertIn("message", data[0])
    
    def test_ai_management_admin_only(self):
        """اختبار أن إدارة الذكاء الاصطناعي تتطلب صلاحيات إدارية"""
        # اختبار بمستخدم عادي
        response = self.client.get("/api/ai-management/models", headers=self.headers)
        self.assertEqual(response.status_code, 403)
        
        # اختبار بمستخدم إداري
        with patch('modules.ai_management.api.get_ai_models') as mock_models:
            mock_models.return_value = [
                {"id": 1, "name": "Disease Detection Model", "status": "active"}
            ]
            
            response = self.client.get("/api/ai-management/models", headers=self.admin_headers)
            self.assertEqual(response.status_code, 200)
    
    def test_ai_agents_list(self):
        """اختبار الحصول على قائمة الوكلاء الذكيين"""
        with patch('modules.ai_agent.api.get_user_agents') as mock_agents:
            mock_agents.return_value = [
                {
                    "id": 1,
                    "name": "مساعد التشخيص",
                    "type": "diagnosis_assistant",
                    "status": "active"
                }
            ]
            
            response = self.client.get("/api/ai-agents/", headers=self.headers)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIsInstance(data, list)
    
    def test_ai_agents_create(self):
        """اختبار إنشاء وكيل ذكي جديد"""
        agent_data = {
            "name": "وكيل تجريبي",
            "type": "general_assistant",
            "description": "وكيل للاختبار",
            "capabilities": ["text_analysis", "data_processing"]
        }
        
        with patch('modules.ai_agent.api.create_agent') as mock_create:
            mock_create.return_value = {
                "id": 2,
                "name": "وكيل تجريبي",
                "status": "created"
            }
            
            response = self.client.post(
                "/api/ai-agents/",
                headers=self.headers,
                json=agent_data
            )
            
            self.assertEqual(response.status_code, 201)
            result = response.json()
            self.assertIn("id", result)
            self.assertIn("status", result)
    
    def test_invalid_token(self):
        """اختبار رمز مصادقة غير صحيح"""
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        
        response = self.client.get("/api/dashboard/stats", headers=invalid_headers)
        self.assertEqual(response.status_code, 401)
    
    def test_missing_token(self):
        """اختبار طلب بدون رمز مصادقة"""
        response = self.client.get("/api/dashboard/stats")
        self.assertEqual(response.status_code, 401)
    
    def test_cors_headers(self):
        """اختبار وجود headers الـ CORS"""
        response = self.client.options("/api/health")
        self.assertEqual(response.status_code, 200)
        
        # التحقق من وجود CORS headers
        self.assertIn("access-control-allow-origin", response.headers)

class TestAPIValidation(unittest.TestCase):
    """اختبارات التحقق من صحة البيانات"""
    
    def setUp(self):
        """إعداد عميل الاختبار"""
        self.client = TestClient(app)
        self.auth_service = AuthService(secret_key="test_secret")
        self.test_token = self.auth_service.create_token(1, "test_user", False)
        self.headers = {"Authorization": f"Bearer {self.test_token}"}
    
    def test_diagnosis_invalid_crop_type(self):
        """اختبار تشخيص بنوع محصول غير صحيح"""
        files = {
            "image": ("test.jpg", b"fake image data", "image/jpeg")
        }
        data = {
            "crop_type": "invalid_crop"
        }
        
        response = self.client.post(
            "/api/diagnosis/analyze",
            headers=self.headers,
            files=files,
            data=data
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_agent_creation_missing_fields(self):
        """اختبار إنشاء وكيل بحقول ناقصة"""
        incomplete_data = {
            "name": "وكيل ناقص"
            # نوع الوكيل مفقود
        }
        
        response = self.client.post(
            "/api/ai-agents/",
            headers=self.headers,
            json=incomplete_data
        )
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    # تشغيل الاختبارات
    unittest.main(verbosity=2)

