# -*- coding: utf-8 -*-
"""
مديول الموارد البشرية
Human Resources Module

إدارة الموظفين والأقسام والرواتب والحضور
Manages employees, departments, payroll, and attendance
"""

from .models.employee import Employee
from .models.department import Department
from .views.employee_views import hr_bp

__all__ = [
    "Employee",
    "Department",
    "hr_bp",
]
