"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/integration/tests/test_comprehensive_integration.py
الوصف: اختبار تكامل شامل للنظام
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import os
import sys
import unittest
from unittest.mock import Mock
import pytest

from src.integration.auth_permissions_integration import AuthPermissionsIntegration
from src.integration.memory_ai_integration import MemoryAIIntegration
from src.modules.notifications.service import NotificationService
from src.modules.notifications.schemas import NotificationCreateSchema
from src.modules.setup.service import SetupService
from src.modules.memory.service import MemoryService
from src.modules.ai_agent.service import AIAgentService
from src.modules.user_management.service import UserManagementService
from src.modules.authentication.service import AuthenticationService
from src.database import get_db
from src.modules.memory.schemas import MemoryCreate, MemoryTypeEnum, MemoryCategoryEnum, MemoryAccessEnum

# إضافة المسار الرئيسي للمشروع
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


class TestComprehensiveIntegration(unittest.TestCase):
    """اختبار تكامل شامل للنظام"""

    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار للفئة بأكملها"""
        cls.db = next(get_db())
        cls._setup_services()
        cls._setup_test_data()
        cls.test_user_id = None
        cls.client = None

    @classmethod
    def tearDownClass(cls):
        """تنظيف بعد انتهاء جميع الاختبارات"""
        cls._cleanup_test_data()
        cls.db.close()

    @classmethod
    def _setup_services(cls):
        """تهيئة الخدمات"""
        cls.auth_service = AuthenticationService(db=cls.db)
        cls.user_service = UserManagementService(db=cls.db)
        cls.ai_agent_service = AIAgentService(db=cls.db)
        cls.memory_service = MemoryService(db=cls.db)
        cls.setup_service = SetupService(db=cls.db)
        cls.notification_service = NotificationService(db=cls.db)

        # تهيئة التكاملات
        cls.memory_ai_integration = MemoryAIIntegration(
            memory_service=cls.memory_service,
            ai_agent_service=cls.ai_agent_service
        )
        cls.auth_permissions_integration = AuthPermissionsIntegration()

    @classmethod
    def _setup_test_data(cls):
        """تهيئة بيانات الاختبار"""
        cls.test_user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "Test@123",
            "first_name": "Test",
            "last_name": "User",
            "role": "user"
        }

        cls.test_agent_data = {
            "name": "Test Agent",
            "description": "Test agent for integration testing",
            "model": "gpt-4",
            "capabilities": ["text", "image"],
            "is_active": True
        }

        cls.test_memory_data = {
            "title": "Test Memory",
            "content": "This is a test memory for integration testing",
            "tags": ["test", "integration"],
            "is_private": False
        }

        cls.test_notification_data = {
            "title": "Test Notification",
            "content": "This is a test notification for integration testing",
            "type": "info",
            "priority": "medium",
            "channels": ["in_app"]
        }

    def setUp(self):
        """إعداد بيئة الاختبار لكل اختبار"""
        self._cleanup_test_data()

    def tearDown(self):
        """تنظيف بعد كل اختبار"""
        self._cleanup_test_data()

    @classmethod
    def _cleanup_test_data(cls):
        """تنظيف بيانات الاختبار"""
        try:
            user = cls.user_service.get_user_by_email(cls.test_user_data["email"])
            if user:
                cls.memory_service.delete_memories_by_user_id(user.id)
                cls.ai_agent_service.delete_agents_by_user_id(user.id)
                cls.notification_service.delete_notifications_by_user_id(user.id)
                cls.user_service.delete_user(user.id)
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def _create_test_user(self):
        """إنشاء مستخدم اختباري"""
        return self.user_service.create_user(
            username=self.test_user_data["username"],
            email=self.test_user_data["email"],
            password=self.test_user_data["password"],
            first_name=self.test_user_data["first_name"],
            last_name=self.test_user_data["last_name"],
            role=self.test_user_data["role"]
        )

    def test_001_system_initialization(self):
        """اختبار تهيئة النظام"""
        # التحقق من تهيئة الخدمات
        self.assertIsNotNone(self.auth_service)
        self.assertIsNotNone(self.user_service)
        self.assertIsNotNone(self.ai_agent_service)
        self.assertIsNotNone(self.memory_service)
        self.assertIsNotNone(self.setup_service)
        self.assertIsNotNone(self.notification_service)

        # التحقق من تهيئة التكاملات
        self.assertIsNotNone(self.memory_ai_integration)
        self.assertIsNotNone(self.auth_permissions_integration)

    def test_002_user_registration_and_authentication(self):
        """اختبار تسجيل المستخدم والمصادقة"""
        # تسجيل مستخدم جديد
        user = self._create_test_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.test_user_data["email"])

        # تسجيل الدخول
        token = self.auth_service.login(
            email=self.test_user_data["email"],
            password=self.test_user_data["password"]
        )
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)

        # التحقق من صلاحية التوكن
        user_info = self.auth_service.verify_token(token)
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info["email"], self.test_user_data["email"])

    def test_003_user_management(self):
        """اختبار إدارة المستخدمين"""
        # إنشاء مستخدم جديد
        user = self._create_test_user()
        self.assertIsNotNone(user)

        # تحديث بيانات المستخدم
        updated_user = self.user_service.update_user(
            user_id=user.id,
            first_name="Updated",
            last_name="User"
        )
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "User")

        # حذف المستخدم
        self.user_service.delete_user(user.id)
        deleted_user = self.user_service.get_user_by_id(user.id)
        self.assertIsNone(deleted_user)

    def test_004_ai_agent_management(self):
        """اختبار إدارة وكلاء الذكاء الاصطناعي"""
        # إنشاء مستخدم للاختبار
        user = self._create_test_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.test_user_data["email"])

        # إنشاء وكيل ذكاء اصطناعي
        agent = self.ai_agent_service.create_agent(
            user_id=user.id,
            name=self.test_agent_data["name"],
            description=self.test_agent_data["description"],
            model=self.test_agent_data["model"],
            capabilities=self.test_agent_data["capabilities"],
            is_active=self.test_agent_data["is_active"]
        )
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, self.test_agent_data["name"])

        # تحديث بيانات الوكيل
        updated_agent = self.ai_agent_service.update_agent(
            agent_id=agent.id,
            name="Updated Agent",
            description="Updated description"
        )
        self.assertIsNotNone(updated_agent)
        self.assertEqual(updated_agent.name, "Updated Agent")

        # حذف الوكيل
        self.ai_agent_service.delete_agent(agent.id)
        deleted_agent = self.ai_agent_service.get_agent_by_id(agent.id)
        self.assertIsNone(deleted_agent)

    def test_005_memory_management(self):
        """اختبار إدارة الذاكرة"""
        # إنشاء مستخدم للاختبار
        user = self._create_test_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.test_user_data["email"])

        # إنشاء ذاكرة جديدة
        memory_create = MemoryCreate(
            title=self.test_memory_data["title"],
            content=self.test_memory_data["content"],
            type=MemoryTypeEnum.TEXT,
            category=MemoryCategoryEnum.PERSONAL,
            access=MemoryAccessEnum.PUBLIC,
            tags=self.test_memory_data["tags"],
            is_private=self.test_memory_data["is_private"]
        )
        memory = self.memory_service.create_memory(user.id, memory_create)
        self.assertIsNotNone(memory)
        self.assertEqual(memory.title, self.test_memory_data["title"])

        # تحديث الذاكرة
        updated_memory = self.memory_service.update_memory(
            memory_id=memory.id,
            title="Updated Memory",
            content="Updated content"
        )
        self.assertIsNotNone(updated_memory)
        self.assertEqual(updated_memory.title, "Updated Memory")

        # حذف الذاكرة
        self.memory_service.delete_memory(memory.id)
        deleted_memory = self.memory_service.get_memory_by_id(memory.id)
        self.assertIsNone(deleted_memory)

    def test_006_notification_management(self):
        """اختبار إدارة الإشعارات"""
        # إنشاء مستخدم للاختبار
        user = self._create_test_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.test_user_data["email"])

        # إنشاء إشعار جديد
        notification_create = NotificationCreateSchema(
            title=self.test_notification_data["title"],
            content=self.test_notification_data["content"],
            type=self.test_notification_data["type"],
            priority=self.test_notification_data["priority"],
            channels=self.test_notification_data["channels"]
        )
        notification = self.notification_service.create_notification(
            user_id=user.id,
            notification=notification_create
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, self.test_notification_data["title"])

        # تحديث الإشعار
        updated_notification = self.notification_service.update_notification(
            notification_id=notification.id,
            title="Updated Notification",
            content="Updated content"
        )
        self.assertIsNotNone(updated_notification)
        self.assertEqual(updated_notification.title, "Updated Notification")

        # حذف الإشعار
        self.notification_service.delete_notification(notification.id)
        deleted_notification = self.notification_service.get_notification_by_id(notification.id)
        self.assertIsNone(deleted_notification)

    def test_007_memory_ai_integration(self):
        """اختبار تكامل الذاكرة مع الذكاء الاصطناعي"""
        # إنشاء مستخدم للاختبار
        user = self._create_test_user()

        # إنشاء وكيل ذكاء اصطناعي
        agent = self.ai_agent_service.create_agent(
            user_id=user.id,
            name=self.test_agent_data["name"],
            description=self.test_agent_data["description"],
            model=self.test_agent_data["model"],
            capabilities=self.test_agent_data["capabilities"],
            is_active=self.test_agent_data["is_active"]
        )
        self.assertIsNotNone(agent)

        # إنشاء ذاكرة جديدة
        memory_create = MemoryCreate(
            title=self.test_memory_data["title"],
            content=self.test_memory_data["content"],
            type=MemoryTypeEnum.TEXT,
            category=MemoryCategoryEnum.PERSONAL,
            access=MemoryAccessEnum.PUBLIC,
            tags=self.test_memory_data["tags"],
            is_private=self.test_memory_data["is_private"]
        )
        memory = self.memory_service.create_memory(user.id, memory_create)
        self.assertIsNotNone(memory)

        # اختبار تكامل الذاكرة مع الذكاء الاصطناعي
        result = self.memory_ai_integration.process_memory_with_ai(
            memory_id=memory.id,
            agent_id=agent.id,
            user_id=user.id
        )
        self.assertIsNotNone(result)
        self.assertTrue(result.get("success", False))

    def test_008_auth_permissions_integration(self):
        """اختبار تكامل المصادقة والصلاحيات"""
        # إنشاء مستخدم للاختبار
        user = self._create_test_user()

        # تسجيل الدخول
        token = self.auth_service.login(
            email=self.test_user_data["email"],
            password=self.test_user_data["password"]
        )
        self.assertIsNotNone(token)

        # اختبار التحقق من الصلاحيات
        has_permission = self.auth_permissions_integration.check_permission(
            user_id=user.id,
            permission="create_memory"
        )
        self.assertTrue(has_permission)

        # اختبار تحديث الصلاحيات
        updated_permissions = self.auth_permissions_integration.update_permissions(
            user_id=user.id,
            permissions=["create_memory", "read_memory", "update_memory"]
        )
        self.assertIsNotNone(updated_permissions)
        self.assertTrue(updated_permissions.get("success", False))

    def test_auth_flow(self):
        """Test the complete authentication flow."""
        # Test login
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        login_result = self.auth_service.login(login_data=login_data)
        self.assertIsNotNone(login_result)
        self.assertIn("access_token", login_result)

        # Test token validation
        token = login_result["access_token"]
        token_data = self.auth_service.validate_token(token=token, token_type="access")
        self.assertIsNotNone(token_data)

    def teardown_method(self):
        """Clean up test data after each test method."""
        if hasattr(self, 'test_user_id'):
            self._cleanup_test_data()

    @pytest.fixture
    def mock_memory_service(self):
        """Create a mock memory service."""
        service = Mock()
        service.delete_memories_by_user_id = Mock(return_value=True)
        service.get_memory_by_id = Mock(return_value=Mock())
        return service

    @pytest.fixture
    def mock_notification_service(self):
        """Create a mock notification service."""
        service = Mock()
        service.delete_notifications_by_user_id = Mock(return_value=True)
        service.update_notification = Mock(return_value=Mock())
        return service

    @pytest.fixture
    def mock_auth_permissions_service(self):
        """Create a mock auth permissions service."""
        service = Mock()
        service.check_permission = Mock(return_value=True)
        service.update_permissions = Mock(return_value={"success": True})
        return service

    def test_memory_creation(self):
        """Test memory creation flow"""
        # Create test user first
        user = self._create_test_user()
        self.assertIsNotNone(user)
        
        # Create test memory
        memory_data = {
            "title": "Test Memory",
            "content": "Test content",
            "type": "text",
            "category": "personal",
            "user_id": user.id
        }
        
        # Create memory using service instead of client
        memory_create = MemoryCreate(
            title=memory_data["title"],
            content=memory_data["content"],
            type=MemoryTypeEnum.TEXT,
            category=MemoryCategoryEnum.PERSONAL,
            access=MemoryAccessEnum.PUBLIC,
            tags=[],
            is_private=False
        )
        memory = self.memory_service.create_memory(user.id, memory_create)
        self.assertIsNotNone(memory)
        self.assertEqual(memory.title, memory_data["title"])


if __name__ == '__main__':
    unittest.main()
