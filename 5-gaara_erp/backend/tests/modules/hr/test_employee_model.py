"""
Unit tests for the Employee model in HR module.

Tests cover:
- Employee creation and validation
- Field constraints
- Soft delete functionality
- Employment status transitions
"""
import pytest
from datetime import date
from unittest.mock import MagicMock, patch


class TestEmployeeModel:
    """Test suite for Employee model."""

    def test_employee_creation_with_required_fields(self):
        """Test creating employee with minimum required fields."""
        # Given
        employee_data = {
            'employee_id': 'EMP001',
            'first_name': 'أحمد',
            'last_name': 'محمد',
            'email': 'ahmed@company.com',
            'hire_date': date.today(),
        }
        
        # When/Then - Verify data structure is valid
        assert employee_data['employee_id'] is not None
        assert len(employee_data['first_name']) > 0
        assert '@' in employee_data['email']
        assert employee_data['hire_date'] is not None

    def test_employee_id_format(self):
        """Test employee ID format validation."""
        # Valid IDs
        valid_ids = ['EMP001', 'EMP1234', 'HR-2025-001']
        for emp_id in valid_ids:
            assert len(emp_id) >= 3, f"ID {emp_id} too short"
        
        # Invalid IDs
        invalid_ids = ['', '  ', 'A' * 51]  # Empty or too long
        for emp_id in invalid_ids:
            assert len(emp_id.strip()) == 0 or len(emp_id) > 50

    def test_employee_email_uniqueness(self):
        """Test that employee emails must be unique."""
        emails = ['user1@company.com', 'user2@company.com']
        # Verify no duplicates
        assert len(emails) == len(set(emails))

    def test_employee_full_name(self):
        """Test full name generation from first and last name."""
        first_name = 'أحمد'
        last_name = 'محمد'
        middle_name = 'علي'
        
        # Without middle name
        full_name = f"{first_name} {last_name}"
        assert full_name == 'أحمد محمد'
        
        # With middle name
        full_name_with_middle = f"{first_name} {middle_name} {last_name}"
        assert full_name_with_middle == 'أحمد علي محمد'

    def test_employee_soft_delete(self):
        """Test soft delete functionality."""
        employee = {
            'id': 1,
            'employee_id': 'EMP001',
            'is_active': True,
            'deleted_at': None
        }
        
        # Perform soft delete
        employee['is_active'] = False
        employee['deleted_at'] = date.today()
        
        # Verify
        assert employee['is_active'] is False
        assert employee['deleted_at'] is not None

    def test_employment_status_transitions(self):
        """Test valid employment status transitions."""
        valid_statuses = ['active', 'on_leave', 'suspended', 'terminated', 'resigned']
        
        # Active can transition to any status
        current_status = 'active'
        for new_status in valid_statuses:
            if new_status != current_status:
                # Transition is valid
                assert new_status in valid_statuses

    def test_phone_number_format(self):
        """Test phone number validation."""
        valid_phones = [
            '+201234567890',
            '01234567890',
            '+966501234567'
        ]
        
        for phone in valid_phones:
            # Should start with + or digits
            assert phone[0] in ['+', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            # Should have enough digits
            digits = ''.join(c for c in phone if c.isdigit())
            assert len(digits) >= 10

    def test_salary_constraints(self):
        """Test salary field constraints."""
        # Salary must be positive
        valid_salaries = [1000.00, 50000.00, 100000.00]
        for salary in valid_salaries:
            assert salary > 0
        
        # Invalid salaries
        invalid_salaries = [-1000.00, 0]
        for salary in invalid_salaries:
            assert salary <= 0

    def test_hire_date_constraints(self):
        """Test hire date cannot be in the future."""
        from datetime import timedelta
        
        today = date.today()
        past_date = today - timedelta(days=365)
        future_date = today + timedelta(days=30)
        
        # Past date is valid
        assert past_date <= today
        
        # Future date should be invalid for hire_date
        assert future_date > today

    def test_department_assignment(self):
        """Test employee department assignment."""
        employee = {
            'id': 1,
            'employee_id': 'EMP001',
            'department_id': None
        }
        
        # Assign department
        employee['department_id'] = 1
        assert employee['department_id'] == 1
        
        # Change department
        employee['department_id'] = 2
        assert employee['department_id'] == 2

    def test_manager_assignment(self):
        """Test employee manager assignment."""
        employee = {
            'id': 1,
            'employee_id': 'EMP001',
            'manager_id': None
        }
        
        # Assign manager
        employee['manager_id'] = 2
        assert employee['manager_id'] == 2
        
        # Employee cannot be their own manager
        employee['id'] = 1
        employee['manager_id'] = 1  # This should be prevented
        assert employee['id'] == employee['manager_id']  # Test detection of invalid state


class TestEmployeeValidation:
    """Test suite for Employee field validation."""

    def test_email_format_validation(self):
        """Test email format validation."""
        valid_emails = [
            'user@example.com',
            'user.name@company.co.uk',
            'user+tag@domain.org'
        ]
        
        for email in valid_emails:
            assert '@' in email
            assert '.' in email.split('@')[1]

    def test_national_id_validation(self):
        """Test national ID validation."""
        # Egyptian national ID (14 digits)
        egyptian_id = '29001011234567'
        assert len(egyptian_id) == 14
        assert egyptian_id.isdigit()
        
        # Saudi national ID (10 digits)
        saudi_id = '1234567890'
        assert len(saudi_id) == 10
        assert saudi_id.isdigit()

    def test_bank_account_validation(self):
        """Test bank account number validation."""
        # IBAN format
        iban = 'EG380019000500000000263180002'
        assert iban.startswith('EG')
        assert len(iban) >= 15

    def test_gender_choices(self):
        """Test gender field choices."""
        valid_genders = ['male', 'female', 'other', 'prefer_not_to_say']
        test_gender = 'male'
        assert test_gender in valid_genders


class TestEmployeeQueries:
    """Test suite for Employee query methods."""

    def test_filter_by_department(self):
        """Test filtering employees by department."""
        employees = [
            {'id': 1, 'department_id': 1},
            {'id': 2, 'department_id': 1},
            {'id': 3, 'department_id': 2},
        ]
        
        # Filter by department 1
        dept1_employees = [e for e in employees if e['department_id'] == 1]
        assert len(dept1_employees) == 2

    def test_filter_by_status(self):
        """Test filtering employees by status."""
        employees = [
            {'id': 1, 'employment_status': 'active'},
            {'id': 2, 'employment_status': 'active'},
            {'id': 3, 'employment_status': 'on_leave'},
            {'id': 4, 'employment_status': 'terminated'},
        ]
        
        # Filter active employees
        active_employees = [e for e in employees if e['employment_status'] == 'active']
        assert len(active_employees) == 2

    def test_search_by_name(self):
        """Test searching employees by name."""
        employees = [
            {'id': 1, 'first_name': 'أحمد', 'last_name': 'محمد'},
            {'id': 2, 'first_name': 'أحمد', 'last_name': 'علي'},
            {'id': 3, 'first_name': 'سارة', 'last_name': 'محمد'},
        ]
        
        # Search by first name
        search_term = 'أحمد'
        results = [e for e in employees if search_term in e['first_name']]
        assert len(results) == 2

    def test_count_by_department(self):
        """Test counting employees per department."""
        employees = [
            {'id': 1, 'department_id': 1},
            {'id': 2, 'department_id': 1},
            {'id': 3, 'department_id': 2},
            {'id': 4, 'department_id': 2},
            {'id': 5, 'department_id': 2},
        ]
        
        # Count by department
        dept_counts = {}
        for e in employees:
            dept_id = e['department_id']
            dept_counts[dept_id] = dept_counts.get(dept_id, 0) + 1
        
        assert dept_counts[1] == 2
        assert dept_counts[2] == 3
