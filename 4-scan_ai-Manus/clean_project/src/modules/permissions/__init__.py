"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/permissions/__init__.py

ملف تهيئة وحدة الصلاحيات في نظام Gaara ERP
"""

from .models import Permission, Role, UserRole, RolePermission
from .service import PermissionService
from .api import router as permissions_router

__all__ = [
    'Permission',
    'Role',
    'UserRole',
    'RolePermission',
    'PermissionService',
    'permissions_router'
]
