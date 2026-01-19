"""
FILE: backend/src/core/__init__.py
PURPOSE: Core module initialization
OWNER: Backend Team
LAST-AUDITED: 2025-11-18

Core application modules
"""

from .app_factory import create_app
from .config import get_settings
from .logging_config import setup_logging

__all__ = ["create_app", "get_settings", "setup_logging"]
