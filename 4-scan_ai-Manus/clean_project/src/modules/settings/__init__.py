# File: /home/ubuntu/ai_web_organized/src/modules/settings/__init__.py
"""
from flask import g
وحدة الإعدادات العامة
توفر هذه الوحدة خدمات لإدارة الإعدادات العامة للنظام
"""

from .settings_service import SettingsService
from .api import router as settings_router
