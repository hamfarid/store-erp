# File: /home/ubuntu/ai_web_organized/src/modules/setup_wizard/__init__.py
"""
from flask import g
حزمة معالج الإعداد التفاعلي
"""

from .api import router as setup_router
from .setup_wizard import SetupWizard

__all__ = ["SetupWizard", "setup_router"]
