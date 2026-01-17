# -*- coding: utf-8 -*-
"""
نموذج الموظف
Employee Model

يمثل موظفاً في المؤسسة
Represents an employee in the organization
"""

from datetime import date, datetime
from decimal import Decimal

try:
    from src.database import db
except ImportError:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()


class Employee(db.Model):
    """
    الموظف - يمثل موظفاً في المؤسسة
    
    Employee - Represents an employee in the organization.
    Links to User for authentication, Department for org structure.
    
    Attributes:
        employee_number: Unique employee identifier
        first_name: Employee's first name
        last_name: Employee's last name
        arabic_name: Full name in Arabic
        national_id: National ID number
        email: Email address
        department_id: Foreign key to department
        hire_date: Date of joining
        base_salary: Monthly salary
        status: active, on_leave, suspended, terminated
    """
    
    __tablename__ = 'hr_employees'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Link to User (for login)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Personal Information
    employee_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    arabic_name = db.Column(db.String(200), nullable=True)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # male, female
    marital_status = db.Column(db.String(20), nullable=True)
    nationality = db.Column(db.String(50), nullable=True)
    
    # Contact Information
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    
    # Employment Information
    department_id = db.Column(db.Integer, db.ForeignKey('hr_departments.id'), nullable=True)
    position_id = db.Column(db.Integer, nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('hr_employees.id'), nullable=True)
    hire_date = db.Column(db.Date, nullable=False, default=date.today)
    termination_date = db.Column(db.Date, nullable=True)
    employment_type = db.Column(db.String(20), default='full_time')
    # full_time, part_time, contract, intern
    
    # Compensation
    base_salary = db.Column(db.Numeric(12, 2), default=Decimal('0.00'))
    currency = db.Column(db.String(3), default='EGP')
    
    # Status
    status = db.Column(db.String(20), default='active', index=True)
    # active, on_leave, suspended, terminated
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship(
        'Department',
        backref=db.backref('employees', lazy='dynamic'),
        foreign_keys=[department_id]
    )
    manager = db.relationship(
        'Employee',
        remote_side=[id],
        backref=db.backref('subordinates', lazy='dynamic'),
        foreign_keys=[manager_id]
    )
    
    def __repr__(self):
        return f'<Employee {self.employee_number}: {self.full_name}>'
    
    @property
    def full_name(self):
        """Get full name in English."""
        return f'{self.first_name} {self.last_name}'
    
    @property
    def full_name_ar(self):
        """Get full name in Arabic."""
        return self.arabic_name or self.full_name
    
    @property
    def years_of_service(self):
        """Calculate years of service."""
        end_date = self.termination_date or date.today()
        delta = end_date - self.hire_date
        return delta.days // 365
    
    @property
    def is_active(self):
        """Check if employee is active."""
        return self.status == 'active'
    
    def to_dict(self, include_sensitive=False):
        """
        Serialize employee to dictionary.
        
        Args:
            include_sensitive: Include salary info (default: False)
        """
        data = {
            'id': self.id,
            'employee_number': self.employee_number,
            'full_name': self.full_name,
            'full_name_ar': self.full_name_ar,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'arabic_name': self.arabic_name,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'department_id': self.department_id,
            'department': self.department.name if self.department else None,
            'position_id': self.position_id,
            'manager_id': self.manager_id,
            'manager_name': self.manager.full_name if self.manager else None,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'employment_type': self.employment_type,
            'status': self.status,
            'years_of_service': self.years_of_service,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_sensitive:
            data.update({
                'national_id': self.national_id,
                'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
                'base_salary': float(self.base_salary) if self.base_salary else 0,
                'currency': self.currency,
                'address': self.address,
                'city': self.city,
            })
        
        return data


__all__ = ['Employee']
