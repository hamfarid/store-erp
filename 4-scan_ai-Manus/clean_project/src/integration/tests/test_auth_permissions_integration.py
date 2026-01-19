"""
/home/ubuntu/implemented_files/v3/src/integration/tests/test_auth_permissions_integration.py

ملف اختبار تكامل المصادقة والصلاحيات في نظام Gaara ERP
يوفر هذا الملف اختبارات وحدة للتحقق من صحة تكامل مديول المصادقة مع مديول الصلاحيات
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from src.integration.auth_permissions_integration import AuthPermissionsIntegration
from src.modules.authentication.service import AuthenticationService
from src.modules.authentication.schemas import TokenData
from src.modules.permissions.service import PermissionService
from src.modules.permissions.models import Role, Permission
from src.modules.user_management.service import UserManagementService
from src.modules.user_management.models import User


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

    mock_service.verify_token.return_value = TokenData(
        user_id="test_user_id",
        username="test_user",
        token_type="bearer",
        expires_at=datetime.now() + timedelta(hours=1)
    )

    mock_service.revoke_all_user_tokens.return_value = 3

    return mock_service


@pytest.fixture
def mock_permission_service():
    """إنشاء نسخة وهمية من خدمة الصلاحيات للاختبار"""
    mock_service = AsyncMock(spec=PermissionService)

    # تهيئة سلوك الدوال الوهمية
    test_permissions = [
        Permission(id="perm1", name="view_users", description="عرض المستخدمين", resource_type="user"),
        Permission(id="perm2", name="edit_users", description="تعديل المستخدمين", resource_type="user"),
        Permission(id="perm3", name="delete_users", description="حذف المستخدمين", resource_type="user")
    ]

    test_roles = [
        Role(id="role1", name="basic_user", description="مستخدم أساسي"),
        Role(id="role2", name="admin", description="مسؤول النظام")
    ]

    mock_service.get_user_permissions.return_value = test_permissions
    mock_service.get_user_roles.return_value = test_roles
    mock_service.check_permission.return_value = True
    mock_service.get_role_by_name.side_effect = lambda name: next((r for r in test_roles if r.name == name), None)
    mock_service.assign_role_to_user.return_value = True
    mock_service.get_organization_roles.return_value = test_roles

    return mock_service


@pytest.fixture
def mock_user_service():
    """إنشاء نسخة وهمية من خدمة إدارة المستخدمين للاختبار"""
    mock_service = AsyncMock(spec=UserManagementService)

    # تهيئة سلوك الدوال الوهمية
    test_user = User(
        id="test_user_id",
        username="test_user",
        email="test@example.com",
        is_active=True,
        is_verified=True
    )

    admin_user = User(
        id="admin_user_id",
        username="admin_user",
        email="admin@example.com",
        is_active=True,
        is_verified=True
    )

    def get_user_side_effect(user_id):
        if user_id == "test_user_id":
            return test_user
        elif user_id == "admin_user_id":
            return admin_user
        return None
    mock_service.get_user.side_effect = get_user_side_effect

    return mock_service


@pytest.fixture
def integration_service(mock_auth_service, mock_permission_service, mock_user_service):
    """إنشاء خدمة تكامل المصادقة والصلاحيات للاختبار"""
    return AuthPermissionsIntegration(
        auth_service=mock_auth_service,
        permission_service=mock_permission_service,
        user_service=mock_user_service
    )


@pytest.mark.asyncio
async def test_authenticate_and_get_permissions(integration_service, mock_auth_service, mock_permission_service):
    """اختبار مصادقة المستخدم والحصول على صلاحياته"""
    # تنفيذ الاختبار
    token_data, permissions = await integration_service.authenticate_and_get_permissions(
        username="test_user",
        password="password123",
        ip_address="127.0.0.1",
        user_agent="Mozilla/5.0"
    )

    # التحقق من النتائج
    assert token_data is not None
    assert token_data.user_id == "test_user_id"
    assert token_data.username == "test_user"

    assert permissions is not None
    assert len(permissions) == 3
    assert permissions[0].name == "view_users"
    assert permissions[1].name == "edit_users"
    assert permissions[2].name == "delete_users"

    # التحقق من استدعاء الدوال المتوقعة
    mock_auth_service.login.assert_called_once()
    mock_permission_service.get_user_permissions.assert_called_once_with("test_user_id")


@pytest.mark.asyncio
async def test_verify_token_and_permission(integration_service, mock_auth_service, mock_permission_service):
    """اختبار التحقق من صحة الرمز والصلاحية"""
    # تنفيذ الاختبار
    token_data, has_permission = await integration_service.verify_token_and_permission(
        token="valid_token",
        required_permission="view_users",
        resource_id="user123"
    )

    # التحقق من النتائج
    assert token_data is not None
    assert token_data.user_id == "test_user_id"
    assert has_permission is True

    # التحقق من استدعاء الدوال المتوقعة
    mock_auth_service.verify_token.assert_called_once_with("valid_token")
    mock_permission_service.check_permission.assert_called_once_with(
        user_id="test_user_id",
        permission="view_users",
        resource_id="user123"
    )


@pytest.mark.asyncio
async def test_assign_default_roles_to_new_user(integration_service, mock_permission_service, mock_user_service):
    """اختبار تعيين الأدوار الافتراضية للمستخدم الجديد"""
    # تنفيذ الاختبار
    assigned_roles = await integration_service.assign_default_roles_to_new_user(
        user_id="test_user_id",
        organization_id="org123",
        is_admin=True
    )

    # التحقق من النتائج
    assert assigned_roles is not None
    assert len(assigned_roles) == 2
    assert assigned_roles[0].name == "basic_user"
    assert assigned_roles[1].name == "admin"

    # التحقق من استدعاء الدوال المتوقعة
    mock_user_service.get_user.assert_called_once_with("test_user_id")
    assert mock_permission_service.get_role_by_name.call_count == 3
    assert mock_permission_service.assign_role_to_user.call_count == 2


@pytest.mark.asyncio
async def test_revoke_user_sessions_on_permission_change(integration_service, mock_auth_service, mock_user_service):
    """اختبار إلغاء جلسات المستخدم عند تغيير الصلاحيات"""
    # تنفيذ الاختبار
    revoked_count = await integration_service.revoke_user_sessions_on_permission_change(
        user_id="test_user_id",
        admin_user_id="admin_user_id"
    )

    # التحقق من النتائج
    assert revoked_count == 3

    # التحقق من استدعاء الدوال المتوقعة
    mock_user_service.get_user.assert_any_call("test_user_id")
    mock_user_service.get_user.assert_any_call("admin_user_id")
    mock_auth_service.revoke_all_user_tokens.assert_called_once_with("test_user_id")


@pytest.mark.asyncio
async def test_get_user_roles_and_permissions(integration_service, mock_permission_service, mock_user_service):
    """اختبار الحصول على أدوار وصلاحيات المستخدم"""
    # تنفيذ الاختبار
    result = await integration_service.get_user_roles_and_permissions(
        user_id="test_user_id"
    )

    # التحقق من النتائج
    assert result is not None
    assert result["user_id"] == "test_user_id"
    assert result["username"] == "test_user"
    assert len(result["roles"]) == 2
    assert len(result["permissions"]) == 3
    assert result["is_admin"] is True

    # التحقق من استدعاء الدوال المتوقعة
    mock_user_service.get_user.assert_called_once_with("test_user_id")
    mock_permission_service.get_user_roles.assert_called_once_with("test_user_id")
    mock_permission_service.get_user_permissions.assert_called_once_with("test_user_id")


@pytest.mark.asyncio
async def test_check_multi_level_permission(integration_service, mock_permission_service, mock_user_service):
    """اختبار التحقق من الصلاحية متعددة المستويات"""
    # تهيئة سلوك الدالة الوهمية
    mock_permission_service.check_permission.side_effect = [False, True, False]

    # تنفيذ الاختبار
    permission_hierarchy = [
        {"permission": "view_country", "resource_id": "country_123"},
        {"permission": "view_company", "resource_id": "company_456"},
        {"permission": "view_branch", "resource_id": "branch_789"}
    ]

    has_permission = await integration_service.check_multi_level_permission(
        user_id="test_user_id",
        permission_hierarchy=permission_hierarchy
    )

    # التحقق من النتائج
    assert has_permission is True

    # التحقق من استدعاء الدوال المتوقعة
    mock_user_service.get_user.assert_called_once_with("test_user_id")
    assert mock_permission_service.check_permission.call_count == 2


@pytest.mark.asyncio
async def test_create_audit_log_for_permission_change(integration_service, mock_user_service):
    """اختبار إنشاء سجل تدقيق لتغيير الصلاحية"""
    # تنفيذ الاختبار
    audit_log = await integration_service.create_audit_log_for_permission_change(
        user_id="test_user_id",
        admin_user_id="admin_user_id",
        action="add_role",
        role_id="role1",
        details={"reason": "تعيين دور جديد"}
    )

    # التحقق من النتائج
    assert audit_log is not None
    assert audit_log["action"] == "add_role"
    assert audit_log["affected_user"]["id"] == "test_user_id"
    assert audit_log["affected_user"]["username"] == "test_user"
    assert audit_log["admin_user"]["id"] == "admin_user_id"
    assert audit_log["admin_user"]["username"] == "admin_user"
    assert audit_log["details"]["reason"] == "تعيين دور جديد"

    # التحقق من استدعاء الدوال المتوقعة
    mock_user_service.get_user.assert_any_call("test_user_id")
    mock_user_service.get_user.assert_any_call("admin_user_id")


@pytest.mark.asyncio
async def test_sync_user_permissions_with_organization(integration_service, mock_permission_service, mock_user_service):
    """اختبار مزامنة صلاحيات المستخدم مع المؤسسة"""
    # تنفيذ الاختبار
    result = await integration_service.sync_user_permissions_with_organization(
        user_id="test_user_id",
        organization_id="org123",
        admin_user_id="admin_user_id"
    )

    # التحقق من النتائج
    assert result is not None
    assert result["user_id"] == "test_user_id"
    assert result["username"] == "test_user"
    assert result["organization_id"] == "org123"
    assert len(result["added_roles"]) == 2

    # التحقق من استدعاء الدوال المتوقعة
    mock_user_service.get_user.assert_called_once_with("test_user_id")
    mock_permission_service.get_organization_roles.assert_called_once_with("org123")
    mock_permission_service.get_user_roles.assert_called_once_with("test_user_id")
    assert mock_permission_service.assign_role_to_user.call_count == 2
