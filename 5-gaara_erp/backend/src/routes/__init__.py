"""
Routes Package - حزمة المسارات
Gaara ERP v12

Central export for all API blueprints.

Author: Global v35.0 Singularity
Version: 1.0.0
"""

from __future__ import annotations

# Import all blueprints
from .tenant_api import tenant_bp
from .sales_api import sales_api
from .inventory_api import inventory_api
from .purchasing_api import purchasing_api
from .customers_api import customers_api
from .agricultural_api import agricultural_api

# Alias for consistency
tenant_api = tenant_bp

# List of all blueprints for registration
ALL_BLUEPRINTS = [
    tenant_bp,
    sales_api,
    inventory_api,
    purchasing_api,
    customers_api,
    agricultural_api,
]

__all__ = [
    'tenant_bp',
    'tenant_api',
    'sales_api',
    'inventory_api',
    'purchasing_api',
    'customers_api',
    'agricultural_api',
    'ALL_BLUEPRINTS',
]
