# -*- coding: utf-8 -*-
"""
نموذج القسم
Department Model

يمثل قسماً في الهيكل التنظيمي
Represents a department in the organizational structure
"""

from datetime import datetime

try:
    from src.database import db
except ImportError:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()


class Department(db.Model):
    """
    القسم - يمثل قسماً في الهيكل التنظيمي
    
    Department - Represents a department in org structure.
    Supports hierarchical structure with parent department.
    
    Attributes:
        code: Unique department code
        name: Department name in English
        name_ar: Department name in Arabic
        parent_id: Parent department for hierarchy
        manager_id: Department manager
    """
    
    __tablename__ = 'hr_departments'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    # Hierarchy
    parent_id = db.Column(db.Integer, db.ForeignKey('hr_departments.id'), nullable=True)
    parent = db.relationship(
        'Department',
        remote_side=[id],
        backref=db.backref('children', lazy='dynamic')
    )
    
    # Manager (references Employee)
    manager_id = db.Column(db.Integer, nullable=True)
    
    # Budget
    budget = db.Column(db.Numeric(15, 2), nullable=True)
    budget_year = db.Column(db.Integer, nullable=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Department {self.code}: {self.name}>'
    
    @property
    def employee_count(self):
        """Get count of employees in this department."""
        return self.employees.count() if hasattr(self, 'employees') else 0
    
    @property
    def full_path(self):
        """Get full hierarchical path."""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name
    
    def to_dict(self, include_children=False):
        """
        Serialize department to dictionary.
        
        Args:
            include_children: Include child departments
        """
        data = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'name_ar': self.name_ar,
            'description': self.description,
            'parent_id': self.parent_id,
            'parent_name': self.parent.name if self.parent else None,
            'manager_id': self.manager_id,
            'employee_count': self.employee_count,
            'budget': float(self.budget) if self.budget else None,
            'budget_year': self.budget_year,
            'is_active': self.is_active,
            'full_path': self.full_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_children:
            data['children'] = [child.to_dict() for child in self.children]
        
        return data
    
    @classmethod
    def get_tree(cls):
        """Get department hierarchy as tree."""
        root_depts = cls.query.filter_by(parent_id=None, is_active=True).all()
        return [dept.to_dict(include_children=True) for dept in root_depts]


__all__ = ['Department']
