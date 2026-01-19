"""
Database Seeds Package
حزمة بذور قاعدة البيانات

Contains seed scripts for initializing database with default data.
"""

from .tenant_plans_seed import seed_plans, get_plan_by_code

__all__ = ['seed_plans', 'get_plan_by_code']
