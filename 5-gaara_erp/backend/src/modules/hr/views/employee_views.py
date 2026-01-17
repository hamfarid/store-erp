# -*- coding: utf-8 -*-
"""
عروض الموظفين
Employee Views - API endpoints for employee management

Provides CRUD operations for employees and departments
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from datetime import date
import logging

try:
    from flask_jwt_extended import jwt_required, get_jwt_identity
except ImportError:
    def jwt_required():
        def decorator(f):
            return f
        return decorator
    
    def get_jwt_identity():
        return 1

try:
    from src.database import db
    from ..models.employee import Employee
    from ..models.department import Department
except ImportError:
    db = None
    Employee = None
    Department = None

logger = logging.getLogger(__name__)

hr_bp = Blueprint('hr', __name__, url_prefix='/api/hr')


# =============================================================================
# Employee Endpoints
# =============================================================================

@hr_bp.route('/employees', methods=['GET'])
@jwt_required()
def list_employees():
    """
    قائمة الموظفين
    List all employees with filtering and pagination.
    
    Query params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    - search: Search by name, email, employee_number
    - department_id: Filter by department
    - status: Filter by status
    - employment_type: Filter by employment type
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search', '')
        department_id = request.args.get('department_id', type=int)
        status = request.args.get('status', '')
        employment_type = request.args.get('employment_type', '')
        
        query = Employee.query
        
        # Search filter
        if search:
            search_filter = or_(
                Employee.first_name.ilike(f'%{search}%'),
                Employee.last_name.ilike(f'%{search}%'),
                Employee.arabic_name.ilike(f'%{search}%'),
                Employee.email.ilike(f'%{search}%'),
                Employee.employee_number.ilike(f'%{search}%'),
            )
            query = query.filter(search_filter)
        
        # Department filter
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        
        # Status filter
        if status:
            query = query.filter(Employee.status == status)
        
        # Employment type filter
        if employment_type:
            query = query.filter(Employee.employment_type == employment_type)
        
        # Pagination
        pagination = query.order_by(
            Employee.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'items': [emp.to_dict() for emp in pagination.items],
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages,
            }
        })
        
    except Exception as e:
        logger.error(f"List employees error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء جلب قائمة الموظفين'
        }), 500


@hr_bp.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    """
    إنشاء موظف جديد
    Create a new employee.
    
    Request Body:
        employee_number: Unique identifier (required)
        first_name: First name (required)
        last_name: Last name (required)
        national_id: National ID (required)
        email: Email address (required)
        ... other optional fields
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'البيانات مطلوبة'
            }), 400
        
        # Required fields
        required = ['employee_number', 'first_name', 'last_name', 'national_id', 'email']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({
                'success': False,
                'message': f'الحقول التالية مطلوبة: {", ".join(missing)}'
            }), 400
        
        # Check for duplicate employee number
        existing = Employee.query.filter_by(
            employee_number=data['employee_number']
        ).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'رقم الموظف موجود بالفعل'
            }), 409
        
        # Check for duplicate email
        existing_email = Employee.query.filter_by(email=data['email']).first()
        if existing_email:
            return jsonify({
                'success': False,
                'message': 'البريد الإلكتروني موجود بالفعل'
            }), 409
        
        # Create employee
        employee = Employee(
            employee_number=data['employee_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            arabic_name=data.get('arabic_name'),
            national_id=data['national_id'],
            email=data['email'],
            phone=data.get('phone'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            city=data.get('city'),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            marital_status=data.get('marital_status'),
            nationality=data.get('nationality'),
            department_id=data.get('department_id'),
            position_id=data.get('position_id'),
            manager_id=data.get('manager_id'),
            hire_date=data.get('hire_date', date.today()),
            employment_type=data.get('employment_type', 'full_time'),
            base_salary=data.get('base_salary', 0),
            currency=data.get('currency', 'EGP'),
        )
        
        db.session.add(employee)
        db.session.commit()
        
        logger.info(f"Created employee: {employee.employee_number}")
        
        return jsonify({
            'success': True,
            'data': employee.to_dict(),
            'message': 'تم إنشاء الموظف بنجاح'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Create employee error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء إنشاء الموظف'
        }), 500


@hr_bp.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    """
    عرض تفاصيل موظف
    Get employee details by ID.
    """
    try:
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
        
        # Include sensitive info for authorized users
        include_sensitive = True  # TODO: Check permission
        
        return jsonify({
            'success': True,
            'data': employee.to_dict(include_sensitive=include_sensitive)
        })
        
    except Exception as e:
        logger.error(f"Get employee error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء جلب بيانات الموظف'
        }), 500


@hr_bp.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    """
    تحديث بيانات موظف
    Update employee data.
    """
    try:
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'البيانات مطلوبة'
            }), 400
        
        # Update fields
        updatable = [
            'first_name', 'last_name', 'arabic_name', 'email', 'phone', 'mobile',
            'address', 'city', 'date_of_birth', 'gender', 'marital_status',
            'nationality', 'department_id', 'position_id', 'manager_id',
            'employment_type', 'base_salary', 'currency', 'status'
        ]
        
        for field in updatable:
            if field in data:
                setattr(employee, field, data[field])
        
        db.session.commit()
        
        logger.info(f"Updated employee: {employee.employee_number}")
        
        return jsonify({
            'success': True,
            'data': employee.to_dict(),
            'message': 'تم تحديث بيانات الموظف بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update employee error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء تحديث بيانات الموظف'
        }), 500


@hr_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    """
    حذف موظف
    Delete (soft) employee - marks as terminated.
    """
    try:
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
        
        # Soft delete - change status
        employee.status = 'terminated'
        employee.termination_date = date.today()
        db.session.commit()
        
        logger.info(f"Deleted employee: {employee.employee_number}")
        
        return jsonify({
            'success': True,
            'message': 'تم حذف الموظف بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete employee error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء حذف الموظف'
        }), 500


# =============================================================================
# Department Endpoints
# =============================================================================

@hr_bp.route('/departments', methods=['GET'])
@jwt_required()
def list_departments():
    """
    قائمة الأقسام
    List all departments.
    """
    try:
        tree = request.args.get('tree', 'false').lower() == 'true'
        
        if tree:
            data = Department.get_tree()
        else:
            departments = Department.query.filter_by(is_active=True).all()
            data = [dept.to_dict() for dept in departments]
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        logger.error(f"List departments error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء جلب قائمة الأقسام'
        }), 500


@hr_bp.route('/departments', methods=['POST'])
@jwt_required()
def create_department():
    """
    إنشاء قسم جديد
    Create a new department.
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('code') or not data.get('name'):
            return jsonify({
                'success': False,
                'message': 'رمز واسم القسم مطلوبان'
            }), 400
        
        # Check for duplicate code
        existing = Department.query.filter_by(code=data['code']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'رمز القسم موجود بالفعل'
            }), 409
        
        department = Department(
            code=data['code'],
            name=data['name'],
            name_ar=data.get('name_ar'),
            description=data.get('description'),
            parent_id=data.get('parent_id'),
            manager_id=data.get('manager_id'),
            budget=data.get('budget'),
            budget_year=data.get('budget_year'),
        )
        
        db.session.add(department)
        db.session.commit()
        
        logger.info(f"Created department: {department.code}")
        
        return jsonify({
            'success': True,
            'data': department.to_dict(),
            'message': 'تم إنشاء القسم بنجاح'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Create department error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء إنشاء القسم'
        }), 500


@hr_bp.route('/departments/<int:dept_id>', methods=['GET'])
@jwt_required()
def get_department(dept_id):
    """Get department by ID."""
    try:
        department = Department.query.get(dept_id)
        
        if not department:
            return jsonify({
                'success': False,
                'message': 'القسم غير موجود'
            }), 404
        
        return jsonify({
            'success': True,
            'data': department.to_dict(include_children=True)
        })
        
    except Exception as e:
        logger.error(f"Get department error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء جلب بيانات القسم'
        }), 500


@hr_bp.route('/departments/<int:dept_id>', methods=['PUT'])
@jwt_required()
def update_department(dept_id):
    """Update department."""
    try:
        department = Department.query.get(dept_id)
        
        if not department:
            return jsonify({
                'success': False,
                'message': 'القسم غير موجود'
            }), 404
        
        data = request.get_json()
        
        updatable = ['name', 'name_ar', 'description', 'parent_id', 
                     'manager_id', 'budget', 'budget_year', 'is_active']
        
        for field in updatable:
            if field in data:
                setattr(department, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': department.to_dict(),
            'message': 'تم تحديث القسم بنجاح'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update department error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء تحديث القسم'
        }), 500


__all__ = ['hr_bp']
