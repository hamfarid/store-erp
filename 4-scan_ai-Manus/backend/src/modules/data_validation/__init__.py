# File: /home/ubuntu/ai_web_organized/src/modules/data_validation/__init__.py
"""
وحدة التحقق من صحة البيانات
توفر هذه الوحدة خدمات للتحقق من صحة البيانات وتنظيفها وإصلاحها
"""

from .api import router as validation_router
from .validation_service import ValidationService

__all__ = ['ValidationService', 'validation_router']
