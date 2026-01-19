# File: /home/ubuntu/ai_web_organized/src/modules/backup_restore/__init__.py
"""
from flask import g
وحدة النسخ الاحتياطي والاستعادة
توفر هذه الوحدة خدمات لإنشاء وإدارة النسخ الاحتياطية واستعادة البيانات
"""

from .api import router
from .backup_service import BackupService

__all__ = [
    'router',
    'BackupService'
]
