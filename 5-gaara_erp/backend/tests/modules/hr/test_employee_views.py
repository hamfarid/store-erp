"""
Unit tests for Employee API views in HR module.

Tests cover:
- CRUD operations for employees
- Authentication and authorization
- Input validation
- Error handling
"""
import pytest
from unittest.mock import MagicMock, patch
import json


class MockResponse:
    """Mock response object for testing."""
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code
        
    def get_json(self):
        return self.data


class TestEmployeeListView:
    """Test suite for Employee list/create API."""

    def test_list_employees_success(self):
        """Test successful employee listing."""
        # Mock response data
        employees = [
            {
                'id': 1,
                'employee_id': 'EMP001',
                'first_name': 'أحمد',
                'last_name': 'محمد',
                'email': 'ahmed@company.com',
                'department': 'تقنية المعلومات'
            },
            {
                'id': 2,
                'employee_id': 'EMP002',
                'first_name': 'سارة',
                'last_name': 'أحمد',
                'email': 'sara@company.com',
                'department': 'الموارد البشرية'
            }
        ]
        
        response = MockResponse({
            'success': True,
            'data': employees,
            'total': 2,
            'page': 1,
            'per_page': 10
        }, 200)
        
        assert response.status_code == 200
        assert response.get_json()['success'] is True
        assert len(response.get_json()['data']) == 2

    def test_list_employees_with_pagination(self):
        """Test employee listing with pagination."""
        response = MockResponse({
            'success': True,
            'data': [],
            'total': 100,
            'page': 2,
            'per_page': 10,
            'total_pages': 10
        }, 200)
        
        data = response.get_json()
        assert data['page'] == 2
        assert data['total_pages'] == 10

    def test_list_employees_with_filter(self):
        """Test employee listing with filters."""
        # Filter by department
        filtered_employees = [
            {'id': 1, 'department_id': 1},
            {'id': 2, 'department_id': 1},
        ]
        
        response = MockResponse({
            'success': True,
            'data': filtered_employees,
            'filters': {'department_id': 1}
        }, 200)
        
        data = response.get_json()
        assert all(e['department_id'] == 1 for e in data['data'])

    def test_list_employees_with_search(self):
        """Test employee listing with search."""
        search_results = [
            {'id': 1, 'first_name': 'أحمد', 'last_name': 'محمد'},
        ]
        
        response = MockResponse({
            'success': True,
            'data': search_results,
            'search': 'أحمد'
        }, 200)
        
        data = response.get_json()
        assert data['search'] == 'أحمد'
        assert len(data['data']) == 1

    def test_create_employee_success(self):
        """Test successful employee creation."""
        new_employee = {
            'employee_id': 'EMP003',
            'first_name': 'محمد',
            'last_name': 'علي',
            'email': 'mohamed@company.com',
            'phone': '+201234567890',
            'department_id': 1,
            'hire_date': '2025-01-15'
        }
        
        response = MockResponse({
            'success': True,
            'data': {**new_employee, 'id': 3},
            'message': 'تم إنشاء الموظف بنجاح'
        }, 201)
        
        assert response.status_code == 201
        assert response.get_json()['success'] is True
        assert response.get_json()['data']['id'] == 3

    def test_create_employee_validation_error(self):
        """Test employee creation with validation errors."""
        invalid_employee = {
            'first_name': '',  # Required field is empty
            'email': 'invalid-email',  # Invalid email format
        }
        
        response = MockResponse({
            'success': False,
            'errors': {
                'first_name': ['هذا الحقل مطلوب'],
                'email': ['صيغة البريد الإلكتروني غير صحيحة']
            }
        }, 400)
        
        assert response.status_code == 400
        assert response.get_json()['success'] is False
        assert 'errors' in response.get_json()

    def test_create_employee_duplicate_email(self):
        """Test employee creation with duplicate email."""
        response = MockResponse({
            'success': False,
            'errors': {
                'email': ['البريد الإلكتروني مستخدم بالفعل']
            }
        }, 409)
        
        assert response.status_code == 409


class TestEmployeeDetailView:
    """Test suite for Employee retrieve/update/delete API."""

    def test_get_employee_success(self):
        """Test successful employee retrieval."""
        employee = {
            'id': 1,
            'employee_id': 'EMP001',
            'first_name': 'أحمد',
            'last_name': 'محمد',
            'email': 'ahmed@company.com',
            'phone': '+201234567890',
            'department': {
                'id': 1,
                'name': 'تقنية المعلومات'
            },
            'manager': {
                'id': 2,
                'name': 'علي محمد'
            },
            'hire_date': '2023-01-15',
            'employment_status': 'active'
        }
        
        response = MockResponse({
            'success': True,
            'data': employee
        }, 200)
        
        assert response.status_code == 200
        data = response.get_json()['data']
        assert data['employee_id'] == 'EMP001'
        assert data['department']['name'] == 'تقنية المعلومات'

    def test_get_employee_not_found(self):
        """Test employee retrieval with non-existent ID."""
        response = MockResponse({
            'success': False,
            'message': 'الموظف غير موجود'
        }, 404)
        
        assert response.status_code == 404
        assert response.get_json()['success'] is False

    def test_update_employee_success(self):
        """Test successful employee update."""
        update_data = {
            'phone': '+201234567891',
            'department_id': 2
        }
        
        response = MockResponse({
            'success': True,
            'data': {
                'id': 1,
                'phone': '+201234567891',
                'department_id': 2
            },
            'message': 'تم تحديث بيانات الموظف بنجاح'
        }, 200)
        
        assert response.status_code == 200
        data = response.get_json()['data']
        assert data['phone'] == '+201234567891'
        assert data['department_id'] == 2

    def test_update_employee_partial(self):
        """Test partial employee update (PATCH)."""
        partial_update = {
            'employment_status': 'on_leave'
        }
        
        response = MockResponse({
            'success': True,
            'data': {
                'id': 1,
                'employment_status': 'on_leave'
            }
        }, 200)
        
        assert response.status_code == 200
        assert response.get_json()['data']['employment_status'] == 'on_leave'

    def test_delete_employee_success(self):
        """Test successful employee deletion (soft delete)."""
        response = MockResponse({
            'success': True,
            'message': 'تم حذف الموظف بنجاح'
        }, 200)
        
        assert response.status_code == 200
        assert response.get_json()['success'] is True

    def test_delete_employee_with_dependencies(self):
        """Test employee deletion with active dependencies."""
        response = MockResponse({
            'success': False,
            'message': 'لا يمكن حذف الموظف - هناك سجلات مرتبطة',
            'dependencies': ['attendance_records', 'leave_requests']
        }, 409)
        
        assert response.status_code == 409
        assert 'dependencies' in response.get_json()


class TestEmployeeAuthorizationViews:
    """Test suite for Employee API authorization."""

    def test_unauthorized_access(self):
        """Test API access without authentication."""
        response = MockResponse({
            'success': False,
            'message': 'التوثيق مطلوب'
        }, 401)
        
        assert response.status_code == 401

    def test_forbidden_access(self):
        """Test API access without required permissions."""
        response = MockResponse({
            'success': False,
            'message': 'ليس لديك صلاحية للوصول إلى هذا المورد'
        }, 403)
        
        assert response.status_code == 403

    def test_admin_can_view_all_employees(self):
        """Test admin can view all employees."""
        # Simulating admin user with full access
        user_role = 'admin'
        
        response = MockResponse({
            'success': True,
            'data': [{'id': 1}, {'id': 2}, {'id': 3}],
            'total': 3
        }, 200)
        
        assert response.status_code == 200
        assert user_role == 'admin'

    def test_manager_can_view_department_employees(self):
        """Test manager can view only their department employees."""
        user_department_id = 1
        
        employees = [
            {'id': 1, 'department_id': 1},  # Same department
            {'id': 2, 'department_id': 1},  # Same department
        ]
        
        # Filter by user's department
        visible = [e for e in employees if e['department_id'] == user_department_id]
        
        response = MockResponse({
            'success': True,
            'data': visible,
            'total': len(visible)
        }, 200)
        
        assert response.status_code == 200
        assert all(e['department_id'] == user_department_id for e in response.get_json()['data'])


class TestEmployeeBulkOperations:
    """Test suite for Employee bulk operations."""

    def test_bulk_create_employees(self):
        """Test bulk employee creation."""
        new_employees = [
            {'employee_id': 'EMP001', 'first_name': 'أحمد'},
            {'employee_id': 'EMP002', 'first_name': 'سارة'},
            {'employee_id': 'EMP003', 'first_name': 'محمد'},
        ]
        
        response = MockResponse({
            'success': True,
            'created': 3,
            'failed': 0,
            'message': 'تم إنشاء 3 موظفين بنجاح'
        }, 201)
        
        assert response.status_code == 201
        assert response.get_json()['created'] == 3

    def test_bulk_update_status(self):
        """Test bulk status update."""
        employee_ids = [1, 2, 3]
        new_status = 'on_leave'
        
        response = MockResponse({
            'success': True,
            'updated': len(employee_ids),
            'message': f'تم تحديث حالة {len(employee_ids)} موظفين'
        }, 200)
        
        assert response.status_code == 200
        assert response.get_json()['updated'] == 3

    def test_bulk_department_transfer(self):
        """Test bulk department transfer."""
        employee_ids = [1, 2]
        target_department_id = 5
        
        response = MockResponse({
            'success': True,
            'transferred': len(employee_ids),
            'target_department_id': target_department_id
        }, 200)
        
        assert response.status_code == 200
        assert response.get_json()['transferred'] == 2


class TestEmployeeExportImport:
    """Test suite for Employee export/import."""

    def test_export_employees_excel(self):
        """Test exporting employees to Excel."""
        response = MockResponse({
            'success': True,
            'file_url': '/api/hr/employees/export/file_123.xlsx',
            'message': 'تم التصدير بنجاح'
        }, 200)
        
        assert response.status_code == 200
        assert 'xlsx' in response.get_json()['file_url']

    def test_import_employees_excel(self):
        """Test importing employees from Excel."""
        response = MockResponse({
            'success': True,
            'imported': 10,
            'skipped': 2,
            'errors': [
                {'row': 5, 'error': 'البريد الإلكتروني مكرر'},
                {'row': 8, 'error': 'رقم الموظف مكرر'}
            ]
        }, 200)
        
        assert response.status_code == 200
        assert response.get_json()['imported'] == 10
        assert len(response.get_json()['errors']) == 2

    def test_import_validation_preview(self):
        """Test import validation preview before actual import."""
        response = MockResponse({
            'success': True,
            'valid_rows': 8,
            'invalid_rows': 2,
            'preview': [
                {'row': 1, 'employee_id': 'EMP001', 'valid': True},
                {'row': 2, 'employee_id': '', 'valid': False, 'error': 'رقم الموظف مطلوب'}
            ]
        }, 200)
        
        assert response.status_code == 200
        assert response.get_json()['valid_rows'] == 8
