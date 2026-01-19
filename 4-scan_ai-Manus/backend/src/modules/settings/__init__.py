# File: /home/ubuntu/ai_web_organized/src/modules/settings/__init__.py
"""
وحدة الإعدادات العامة
توفر هذه الوحدة خدمات لإدارة الإعدادات العامة للنظام
"""

from .api import router as settings_router
from .settings_service import SettingsService

__all__ = ["SettingsService", "settings_router"]
