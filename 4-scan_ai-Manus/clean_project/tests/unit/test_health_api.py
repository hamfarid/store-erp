"""
اختبارات وحدة API الصحة
Health API Unit Tests
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

from src.main import app

client = TestClient(app)

class TestHealthAPI:
    """اختبارات API الصحة"""
    
    def test_basic_health_check(self):
        """اختبار فحص الصحة الأساسي"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "Gaara Scan AI"
        assert data["version"] == "2.0.0"
        assert "timestamp" in data
    
    def test_ping_endpoint(self):
        """اختبار نقطة Ping"""
        response = client.get("/api/v1/ping")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "pong"
    
    @patch('src.core.database.check_db_health')
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_detailed_health_check_healthy(self, mock_disk, mock_memory, mock_cpu, mock_db):
        """اختبار فحص الصحة المفصل - حالة صحية"""
        # إعداد المحاكيات
        mock_db.return_value = True
        mock_cpu.return_value = 25.5
        
        mock_memory_obj = MagicMock()
        mock_memory_obj.percent = 60.0
        mock_memory_obj.available = 4 * 1024**3  # 4 GB
        mock_memory.return_value = mock_memory_obj
        
        mock_disk_obj = MagicMock()
        mock_disk_obj.percent = 45.0
        mock_disk_obj.free = 100 * 1024**3  # 100 GB
        mock_disk.return_value = mock_disk_obj
        
        response = client.get("/api/v1/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["components"]["database"]["status"] == "healthy"
        assert data["components"]["system"]["cpu_usage"] == "25.5%"
        assert data["components"]["system"]["memory_usage"] == "60.0%"
    
    @patch('src.core.database.check_db_health')
    def test_detailed_health_check_unhealthy(self, mock_db):
        """اختبار فحص الصحة المفصل - حالة غير صحية"""
        mock_db.return_value = False
        
        response = client.get("/api/v1/health/detailed")
        
        assert response.status_code == 503
        data = response.json()
        
        assert data["status"] == "unhealthy"
        assert data["components"]["database"]["status"] == "unhealthy"

class TestHealthAPIPerformance:
    """اختبارات أداء API الصحة"""
    
    def test_health_check_response_time(self):
        """اختبار وقت استجابة فحص الصحة"""
        import time
        
        start_time = time.time()
        response = client.get("/api/v1/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 0.1  # أقل من 100ms
    
    def test_concurrent_health_checks(self):
        """اختبار فحوصات الصحة المتزامنة"""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get("/api/v1/health")
        
        # تشغيل 10 طلبات متزامنة
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in futures]
        
        # التحقق من أن جميع الطلبات نجحت
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"

class TestHealthAPIHeaders:
    """اختبارات رؤوس HTTP"""
    
    def test_security_headers(self):
        """اختبار رؤوس الأمان"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        
        # فحص رؤوس الأمان
        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        
        assert "X-Frame-Options" in response.headers
        assert response.headers["X-Frame-Options"] == "DENY"
        
        assert "X-XSS-Protection" in response.headers
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
    
    def test_request_id_header(self):
        """اختبار رأس معرف الطلب"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) == 8  # UUID مقطوع
    
    def test_process_time_header(self):
        """اختبار رأس وقت المعالجة"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        assert "X-Process-Time" in response.headers
        
        process_time = float(response.headers["X-Process-Time"])
        assert process_time > 0
        assert process_time < 1.0  # أقل من ثانية واحدة

