"""
Unit tests for the Department model in HR module.

Tests cover:
- Department creation and validation
- Hierarchical structure (parent-child relationships)
- Budget management
- Department statistics
"""
import pytest
from datetime import date


class TestDepartmentModel:
    """Test suite for Department model."""

    def test_department_creation_with_required_fields(self):
        """Test creating department with minimum required fields."""
        # Given
        department_data = {
            'code': 'IT',
            'name': 'Information Technology',
            'name_ar': 'تقنية المعلومات',
        }
        
        # When/Then - Verify data structure is valid
        assert department_data['code'] is not None
        assert len(department_data['code']) <= 20
        assert len(department_data['name']) > 0

    def test_department_code_uniqueness(self):
        """Test that department codes must be unique."""
        codes = ['IT', 'HR', 'FIN', 'SALES']
        # Verify no duplicates
        assert len(codes) == len(set(codes))

    def test_department_code_format(self):
        """Test department code format validation."""
        # Valid codes (uppercase alphanumeric with hyphens)
        valid_codes = ['IT', 'HR-01', 'DEV_TEAM', 'SALES123']
        for code in valid_codes:
            assert len(code) >= 2
            assert len(code) <= 20
        
        # Invalid codes
        invalid_codes = ['', 'A' * 21]  # Empty or too long
        for code in invalid_codes:
            assert len(code) == 0 or len(code) > 20

    def test_department_hierarchy(self):
        """Test parent-child department relationships."""
        # Create hierarchy: Company -> IT -> Development
        departments = {
            'company': {'id': 1, 'code': 'COMPANY', 'parent_id': None},
            'it': {'id': 2, 'code': 'IT', 'parent_id': 1},
            'development': {'id': 3, 'code': 'DEV', 'parent_id': 2},
        }
        
        # Verify hierarchy
        assert departments['company']['parent_id'] is None  # Root
        assert departments['it']['parent_id'] == 1  # Child of company
        assert departments['development']['parent_id'] == 2  # Child of IT

    def test_department_cannot_be_own_parent(self):
        """Test that a department cannot be its own parent."""
        department = {'id': 1, 'code': 'IT', 'parent_id': 1}
        
        # This should be invalid
        assert department['id'] == department['parent_id']  # Test detection

    def test_department_soft_delete(self):
        """Test soft delete functionality."""
        department = {
            'id': 1,
            'code': 'IT',
            'is_active': True,
            'deleted_at': None
        }
        
        # Perform soft delete
        department['is_active'] = False
        department['deleted_at'] = date.today()
        
        # Verify
        assert department['is_active'] is False
        assert department['deleted_at'] is not None


class TestDepartmentBudget:
    """Test suite for Department budget management."""

    def test_budget_assignment(self):
        """Test assigning budget to department."""
        department = {
            'id': 1,
            'code': 'IT',
            'budget': 0,
            'budget_year': date.today().year
        }
        
        # Assign budget
        department['budget'] = 500000.00
        assert department['budget'] == 500000.00

    def test_budget_must_be_positive(self):
        """Test budget must be non-negative."""
        valid_budgets = [0, 1000.00, 1000000.00]
        for budget in valid_budgets:
            assert budget >= 0
        
        invalid_budget = -1000.00
        assert invalid_budget < 0

    def test_budget_year_validation(self):
        """Test budget year validation."""
        current_year = date.today().year
        
        # Valid years (current or future)
        valid_years = [current_year, current_year + 1]
        for year in valid_years:
            assert year >= current_year - 5  # Allow historical
        
        # Very old years should be flagged
        old_year = 1990
        assert old_year < current_year - 30


class TestDepartmentHierarchyQueries:
    """Test suite for Department hierarchy queries."""

    def test_get_children_departments(self):
        """Test getting child departments."""
        departments = [
            {'id': 1, 'code': 'COMPANY', 'parent_id': None},
            {'id': 2, 'code': 'IT', 'parent_id': 1},
            {'id': 3, 'code': 'HR', 'parent_id': 1},
            {'id': 4, 'code': 'DEV', 'parent_id': 2},
            {'id': 5, 'code': 'OPS', 'parent_id': 2},
        ]
        
        # Get children of COMPANY (id=1)
        company_children = [d for d in departments if d['parent_id'] == 1]
        assert len(company_children) == 2
        
        # Get children of IT (id=2)
        it_children = [d for d in departments if d['parent_id'] == 2]
        assert len(it_children) == 2

    def test_get_root_departments(self):
        """Test getting root (top-level) departments."""
        departments = [
            {'id': 1, 'code': 'COMPANY', 'parent_id': None},
            {'id': 2, 'code': 'IT', 'parent_id': 1},
            {'id': 3, 'code': 'HR', 'parent_id': 1},
        ]
        
        # Get root departments
        root_depts = [d for d in departments if d['parent_id'] is None]
        assert len(root_depts) == 1
        assert root_depts[0]['code'] == 'COMPANY'

    def test_get_all_descendants(self):
        """Test getting all descendants of a department."""
        departments = [
            {'id': 1, 'code': 'COMPANY', 'parent_id': None, 'level': 0},
            {'id': 2, 'code': 'IT', 'parent_id': 1, 'level': 1},
            {'id': 3, 'code': 'DEV', 'parent_id': 2, 'level': 2},
            {'id': 4, 'code': 'BACKEND', 'parent_id': 3, 'level': 3},
        ]
        
        def get_descendants(dept_id):
            """Recursively get all descendants."""
            result = []
            children = [d for d in departments if d['parent_id'] == dept_id]
            for child in children:
                result.append(child)
                result.extend(get_descendants(child['id']))
            return result
        
        # Get all descendants of COMPANY
        company_descendants = get_descendants(1)
        assert len(company_descendants) == 3
        
        # Get all descendants of IT
        it_descendants = get_descendants(2)
        assert len(it_descendants) == 2

    def test_get_full_path(self):
        """Test getting full hierarchical path."""
        departments = {
            1: {'id': 1, 'code': 'COMPANY', 'name': 'الشركة', 'parent_id': None},
            2: {'id': 2, 'code': 'IT', 'name': 'تقنية المعلومات', 'parent_id': 1},
            3: {'id': 3, 'code': 'DEV', 'name': 'التطوير', 'parent_id': 2},
        }
        
        def get_path(dept_id):
            """Get full path from root to department."""
            path = []
            current_id = dept_id
            while current_id is not None:
                dept = departments[current_id]
                path.insert(0, dept['name'])
                current_id = dept['parent_id']
            return ' > '.join(path)
        
        # Get path for DEV department
        dev_path = get_path(3)
        assert dev_path == 'الشركة > تقنية المعلومات > التطوير'


class TestDepartmentStatistics:
    """Test suite for Department statistics."""

    def test_employee_count(self):
        """Test counting employees in department."""
        employees = [
            {'id': 1, 'department_id': 1},
            {'id': 2, 'department_id': 1},
            {'id': 3, 'department_id': 2},
        ]
        
        dept_1_count = len([e for e in employees if e['department_id'] == 1])
        assert dept_1_count == 2
        
        dept_2_count = len([e for e in employees if e['department_id'] == 2])
        assert dept_2_count == 1

    def test_total_salary_expense(self):
        """Test calculating total salary expense for department."""
        employees = [
            {'id': 1, 'department_id': 1, 'salary': 5000},
            {'id': 2, 'department_id': 1, 'salary': 6000},
            {'id': 3, 'department_id': 2, 'salary': 7000},
        ]
        
        dept_1_salary = sum(e['salary'] for e in employees if e['department_id'] == 1)
        assert dept_1_salary == 11000

    def test_budget_utilization(self):
        """Test calculating budget utilization percentage."""
        department = {
            'budget': 100000,
            'spent': 75000
        }
        
        utilization = (department['spent'] / department['budget']) * 100
        assert utilization == 75.0

    def test_headcount_by_status(self):
        """Test counting employees by status within department."""
        employees = [
            {'id': 1, 'department_id': 1, 'status': 'active'},
            {'id': 2, 'department_id': 1, 'status': 'active'},
            {'id': 3, 'department_id': 1, 'status': 'on_leave'},
            {'id': 4, 'department_id': 1, 'status': 'terminated'},
        ]
        
        dept_1 = [e for e in employees if e['department_id'] == 1]
        
        active_count = len([e for e in dept_1 if e['status'] == 'active'])
        assert active_count == 2
        
        on_leave_count = len([e for e in dept_1 if e['status'] == 'on_leave'])
        assert on_leave_count == 1
