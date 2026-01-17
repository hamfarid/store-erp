"""
File: examples/init_py_patterns/01_central_registry/__init__.py
Pattern: Central Registry for Definitions

Use Case:
- Centralized location for all type definitions
- Common in config packages
- Makes imports cleaner

Example from real project: config/definitions/
"""

# Import all definitions from submodules
from .status_types import Status, UserRole, Environment
from .response_types import APIResponse, ErrorResponse, PaginatedResponse
from .model_mixins import TimestampMixin, SoftDeleteMixin, AuditMixin

# Explicit __all__ - this is the public API
__all__ = [
    # Status Types
    'Status',
    'UserRole',
    'Environment',
    # Response Types
    'APIResponse',
    'ErrorResponse',
    'PaginatedResponse',
    # Model Mixins
    'TimestampMixin',
    'SoftDeleteMixin',
    'AuditMixin',
]

# Package metadata
__version__ = '1.0.0'

# Usage example in docstring
"""
Usage:
    from config.definitions import Status, UserRole, APIResponse
    
    class User:
        status: Status = Status.ACTIVE
        role: UserRole = UserRole.USER
"""

