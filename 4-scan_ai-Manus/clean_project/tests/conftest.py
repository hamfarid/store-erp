"""
تكوين pytest والاختبارات
Pytest Configuration and Test Settings
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path

# إضافة مسار المشروع
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def pytest_configure(config):
    """تكوين pytest"""
    # إضافة علامات مخصصة
    config.addinivalue_line(
        "markers", "unit: اختبارات الوحدة"
    )
    config.addinivalue_line(
        "markers", "integration: اختبارات التكامل"
    )
    config.addinivalue_line(
        "markers", "e2e: اختبارات النهاية إلى النهاية"
    )
    config.addinivalue_line(
        "markers", "slow: اختبارات بطيئة"
    )
    config.addinivalue_line(
        "markers", "auth: اختبارات المصادقة"
    )
    config.addinivalue_line(
        "markers", "api: اختبارات API"
    )
    config.addinivalue_line(
        "markers", "database: اختبارات قاعدة البيانات"
    )

def pytest_collection_modifyitems(config, items):
    """تعديل عناصر الجمع"""
    # إضافة علامة slow للاختبارات البطيئة
    for item in items:
        if "e2e" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        if "selenium" in item.nodeid:
            item.add_marker(pytest.mark.slow)

@pytest.fixture(scope="session")
def event_loop():
    """إنشاء حلقة أحداث للجلسة"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_settings():
    """إعدادات الاختبار"""
    return {
        "base_url": "http://localhost:8000",
        "test_username": "admin",
        "test_password": "admin123",
        "timeout": 30,
        "max_file_size": 50 * 1024 * 1024,  # 50 MB
    }

@pytest.fixture
def test_client():
    """عميل اختبار FastAPI"""
    from fastapi.testclient import TestClient
    from src.main import app
    
    return TestClient(app)

@pytest.fixture
def auth_headers(test_client, test_settings):
    """رؤوس المصادقة للاختبارات"""
    login_data = {
        "username": test_settings["test_username"],
        "password": test_settings["test_password"]
    }
    
    response = test_client.post("/api/v1/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        pytest.skip("فشل في تسجيل الدخول للاختبار")

@pytest.fixture
def sample_image():
    """صورة عينة للاختبارات"""
    from PIL import Image
    import io
    
    # إنشاء صورة RGB بسيطة
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

@pytest.fixture
def uploaded_file(test_client, sample_image):
    """ملف مرفوع للاختبارات"""
    files = {"file": ("test_image.jpg", sample_image, "image/jpeg")}
    response = test_client.post("/api/v1/upload/image", files=files)
    
    if response.status_code == 200:
        file_data = response.json()
        yield file_data
        
        # تنظيف - حذف الملف بعد الاختبار
        try:
            test_client.delete(f"/api/v1/upload/{file_data['file_id']}")
        except:
            pass  # تجاهل أخطاء التنظيف
    else:
        pytest.skip("فشل في رفع الملف للاختبار")

@pytest.fixture(scope="session")
def docker_compose_file():
    """ملف docker-compose للاختبارات"""
    return project_root / "docker-compose.test.yml"

@pytest.fixture(scope="session")
def database_url():
    """رابط قاعدة البيانات للاختبارات"""
    return "sqlite:///./test.db"

def pytest_runtest_setup(item):
    """إعداد قبل تشغيل كل اختبار"""
    # تخطي اختبارات e2e إذا لم يكن Selenium متاحاً
    if "e2e" in item.keywords:
        try:
            from selenium import webdriver
        except ImportError:
            pytest.skip("Selenium غير متاح لاختبارات e2e")

def pytest_runtest_teardown(item):
    """تنظيف بعد تشغيل كل اختبار"""
    # تنظيف ملفات الاختبار المؤقتة
    test_files = Path(".").glob("test_*.jpg")
    for file in test_files:
        try:
            file.unlink()
        except:
            pass

# إعدادات pytest في ملف pytest.ini
pytest_ini_content = """
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: اختبارات الوحدة
    integration: اختبارات التكامل
    e2e: اختبارات النهاية إلى النهاية
    slow: اختبارات بطيئة
    auth: اختبارات المصادقة
    api: اختبارات API
    database: اختبارات قاعدة البيانات
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
"""

