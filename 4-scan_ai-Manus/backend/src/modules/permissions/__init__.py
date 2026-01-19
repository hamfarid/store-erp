"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/permissions/__init__.py

ملف تهيئة وحدة الصلاحيات في نظام Gaara ERP
"""

from .api import router as permissions_router
from .models import Permission, Role, RolePermission, UserRole
from .service import PermissionService

__all__ = [
    'Permission',
    'Role',
    'UserRole',
    'RolePermission',
    'PermissionService',
    'permissions_router'
]
