"""
/home/ubuntu/implemented_files/v3/src/integration/tests/test_frontend_backend_integration.py

ملف اختبار تكامل الواجهة الأمامية والخلفية في نظام Gaara ERP
يوفر هذا الملف اختبارات وحدة للتحقق من صحة تكامل الواجهة الأمامية مع الواجهة الخلفية
"""

import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
import pytest

# استيراد المديولات الداخلية
from src.modules.authentication.service import AuthenticationService
from src.modules.authentication.schemas import TokenData
from src.modules.user_management.service import UserManagementService


class MockResponse:
    """فئة استجابة وهمية لمحاكاة استجابات HTTP"""

    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data
        self._text = json.dumps(json_data)

    async def json(self):
        return self.json_data

    async def text(self):
        return self._text

    def __bool__(self):
        return 200 <= self.status_code < 300


@pytest.fixture
def mock_auth_service():
    """إنشاء نسخة وهمية من خدمة المصادقة للاختبار"""
    mock_service = AsyncMock(spec=AuthenticationService)

    # تهيئة سلوك الدوال الوهمية
    mock_service.login.return_value = TokenData(
        user_id="test_user_id",
        username="test_user",
        token_type="bearer",
        expires_at=datetime.now() + timedelta(hours=1)
    )

    return mock_service


@pytest.fixture
def mock_user_service():
    """إنشاء نسخة وهمية من خدمة إدارة المستخدمين للاختبار"""
    mock_service = AsyncMock(spec=UserManagementService)

    # تهيئة سلوك الدوال الوهمية
    mock_service.get_users.return_value = [
        {
            "id": "user1",
            "username": "user1",
            "email": "user1@example.com",
            "is_active": True
        },
        {
            "id": "user2",
            "username": "user2",
            "email": "user2@example.com",
            "is_active": True
        }
    ]

    return mock_service


@pytest.fixture
def mock_fetch():
    """إنشاء نسخة وهمية من دالة fetch للاختبار"""
    with patch("src.frontend.react_components.services.authService.fetch") as mock_fetch:
        # تهيئة سلوك الدالة الوهمية
        mock_fetch.return_value = MockResponse(200, {
            "token": "test_token",
            "user_id": "test_user_id",
            "username": "test_user",
            "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
        })

        yield mock_fetch


@pytest.mark.asyncio
async def test_login_frontend_backend_integration(mock_auth_service, mock_fetch):
    """اختبار تكامل تسجيل الدخول بين الواجهة الأمامية والخلفية"""
    # تهيئة بيانات الاختبار
    login_data = {
        "username": "test_user",
        "password": "password123"
    }

    # محاكاة استدعاء الواجهة الأمامية لخدمة المصادقة
    with patch("src.modules.authentication.api.AuthenticationService", return_value=mock_auth_service):
        # استدعاء خدمة المصادقة من الواجهة الأمامية
        from src.frontend.react_components.services.authService import login

        # تنفيذ الاختبار
        result = await login(login_data["username"], login_data["password"])

        # التحقق من النتائج
        assert result is not None
        assert "token" in result
        assert "user_id" in result
        assert result["username"] == "test_user"

        # التحقق من استدعاء الدوال المتوقعة
        mock_fetch.assert_called_once()
        assert "username" in str(mock_fetch.call_args)
        assert "password" in str(mock_fetch.call_args)


@pytest.mark.asyncio
async def test_get_users_frontend_backend_integration(mock_user_service, mock_fetch):
    """اختبار تكامل الحصول على المستخدمين بين الواجهة الأمامية والخلفية"""
    # تهيئة بيانات الاختبار
    mock_fetch.return_value = MockResponse(200, {
        "users": [
            {
                "id": "user1",
                "username": "user1",
                "email": "user1@example.com",
                "is_active": True
            },
            {
                "id": "user2",
                "username": "user2",
                "email": "user2@example.com",
                "is_active": True
            }
        ]
    })

    # محاكاة استدعاء الواجهة الأمامية لخدمة إدارة المستخدمين
    with patch("src.modules.user_management.api.UserManagementService", return_value=mock_user_service):
        # استدعاء خدمة إدارة المستخدمين من الواجهة الأمامية
        from src.frontend.react_components.services.userService import getUsers

        # تنفيذ الاختبار
        result = await getUsers("test_token")

        # التحقق من النتائج
        assert result is not None
        assert "users" in result
        assert len(result["users"]) == 2
        assert result["users"][0]["username"] == "user1"
        assert result["users"][1]["username"] == "user2"

        # التحقق من استدعاء الدوال المتوقعة
        mock_fetch.assert_called_once()
        assert "Authorization" in str(mock_fetch.call_args)
        assert "Bearer test_token" in str(mock_fetch.call_args)


@pytest.mark.asyncio
async def test_ai_agent_frontend_backend_integration(mock_fetch):
    """اختبار تكامل وكلاء الذكاء الاصطناعي بين الواجهة الأمامية والخلفية"""
    # تهيئة بيانات الاختبار
    mock_fetch.return_value = MockResponse(200, {
        "agents": [
            {
                "id": "agent1",
                "name": "وكيل الزراعة",
                "agent_type": "SYSTEM",
                "capabilities": ["MEMORY_ACCESS", "KNOWLEDGE_QUERY"],
                "created_by": "system"
            },
            {
                "id": "agent2",
                "name": "وكيل المستخدم",
                "agent_type": "USER",
                "capabilities": ["MEMORY_ACCESS"],
                "created_by": "user1"
            }
        ]
    })

    # محاكاة استدعاء الواجهة الأمامية لخدمة وكلاء الذكاء الاصطناعي
    # استدعاء خدمة وكلاء الذكاء الاصطناعي من الواجهة الأمامية
    from src.frontend.react_components.services.aiAgentService import getAgents

    # تنفيذ الاختبار
    result = await getAgents("test_token")

    # التحقق من النتائج
    assert result is not None
    assert "agents" in result
    assert len(result["agents"]) == 2
    assert result["agents"][0]["name"] == "وكيل الزراعة"
    assert result["agents"][1]["name"] == "وكيل المستخدم"

    # التحقق من استدعاء الدوال المتوقعة
    mock_fetch.assert_called_once()
    assert "Authorization" in str(mock_fetch.call_args)
    assert "Bearer test_token" in str(mock_fetch.call_args)


@pytest.mark.asyncio
async def test_memory_frontend_backend_integration(mock_fetch):
    """اختبار تكامل الذاكرة بين الواجهة الأمامية والخلفية"""
    # تهيئة بيانات الاختبار
    mock_fetch.return_value = MockResponse(200, {
        "memories": [
            {
                "id": "mem1",
                "content": "معلومات عن المحاصيل الزراعية",
                "memory_type": "LONG_TERM",
                "created_by": "user1",
                "tags": ["زراعة", "محاصيل"]
            },
            {
                "id": "mem2",
                "content": "بيانات الطقس للأسبوع الماضي",
                "memory_type": "SHORT_TERM",
                "created_by": "user1",
                "tags": ["طقس", "بيانات"]
            }
        ]
    })

    # محاكاة استدعاء الواجهة الأمامية لخدمة الذاكرة
    # استدعاء خدمة الذاكرة من الواجهة الأمامية
    from src.frontend.react_components.services.memoryService import getMemories

    # تنفيذ الاختبار
    result = await getMemories("test_token")

    # التحقق من النتائج
    assert result is not None
    assert "memories" in result
    assert len(result["memories"]) == 2
    assert result["memories"][0]["content"] == "معلومات عن المحاصيل الزراعية"
    assert result["memories"][1]["content"] == "بيانات الطقس للأسبوع الماضي"

    # التحقق من استدعاء الدوال المتوقعة
    mock_fetch.assert_called_once()
    assert "Authorization" in str(mock_fetch.call_args)
    assert "Bearer test_token" in str(mock_fetch.call_args)


@pytest.mark.asyncio
async def test_settings_frontend_backend_integration(mock_fetch):
    """اختبار تكامل الإعدادات بين الواجهة الأمامية والخلفية"""
    # تهيئة بيانات الاختبار
    mock_fetch.return_value = MockResponse(200, {
        "settings": {
            "general": {
                "language": "ar",
                "theme": "light",
                "timezone": "Africa/Cairo"
            },
            "notifications": {
                "email": True,
                "push": True,
                "sms": False
            },
            "security": {
                "two_factor_auth": True,
                "session_timeout": 30
            }
        }
    })

    # محاكاة استدعاء الواجهة الأمامية لخدمة الإعدادات
    # استدعاء خدمة الإعدادات من الواجهة الأمامية
    from src.frontend.react_components.services.settingsService import getSettings

    # تنفيذ الاختبار
    result = await getSettings("test_token")

    # التحقق من النتائج
    assert result is not None
    assert "settings" in result
    assert "general" in result["settings"]
    assert "notifications" in result["settings"]
    assert "security" in result["settings"]
    assert result["settings"]["general"]["language"] == "ar"
    assert result["settings"]["security"]["two_factor_auth"] is True

    # التحقق من استدعاء الدوال المتوقعة
    mock_fetch.assert_called_once()
    assert "Authorization" in str(mock_fetch.call_args)
    assert "Bearer test_token" in str(mock_fetch.call_args)


@pytest.mark.asyncio
async def test_backup_restore_frontend_backend_integration(mock_fetch):
    """اختبار تكامل النسخ الاحتياطي والاستعادة بين الواجهة الأمامية والخلفية"""
    # تهيئة بيانات الاختبار
    mock_fetch.return_value = MockResponse(200, {
        "backups": [
            {
                "id": "backup1",
                "name": "نسخة احتياطية كاملة",
                "created_at": "2025-05-20T10:00:00Z",
                "size": 1024000,
                "type": "FULL"
            },
            {
                "id": "backup2",
                "name": "نسخة احتياطية تزايدية",
                "created_at": "2025-05-25T10:00:00Z",
                "size": 512000,
                "type": "INCREMENTAL"
            }
        ]
    })

    # محاكاة استدعاء الواجهة الأمامية لخدمة النسخ الاحتياطي والاستعادة
    # استدعاء خدمة النسخ الاحتياطي والاستعادة من الواجهة الأمامية
    from src.frontend.react_components.services.backupRestoreService import getBackups

    # تنفيذ الاختبار
    result = await getBackups("test_token")

    # التحقق من النتائج
    assert result is not None
    assert "backups" in result
    assert len(result["backups"]) == 2
    assert result["backups"][0]["name"] == "نسخة احتياطية كاملة"
    assert result["backups"][1]["name"] == "نسخة احتياطية تزايدية"

    # التحقق من استدعاء الدوال المتوقعة
    mock_fetch.assert_called_once()
    assert "Authorization" in str(mock_fetch.call_args)
    assert "Bearer test_token" in str(mock_fetch.call_args)
