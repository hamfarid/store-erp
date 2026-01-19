# File: /home/ubuntu/ai_web_organized/src/modules/setup_wizard/__init__.py
"""
from flask import g
حزمة معالج الإعداد التفاعلي
"""

from .setup_wizard import SetupWizard
from .api import router as setup_router

__all__ = ["SetupWizard", "setup_router"]
