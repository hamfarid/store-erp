"""
Integration module for Gaara ERP system.
This module handles integration between different components of the system.
"""

# Remove problematic Pylint options
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=unused-argument
# pylint: disable=unused-import
# pylint: disable=unused-variable
# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position

from .memory_ai_integration import MemoryAIIntegration
from .auth_permissions_integration import AuthPermissionsIntegration
from .frontend_backend_integration import FrontendBackendIntegration

__all__ = [
    'MemoryAIIntegration',
    'AuthPermissionsIntegration',
    'FrontendBackendIntegration'
]
