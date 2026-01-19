"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/notifications/__init__.py
الوصف: ملف التهيئة الأساسي لمديول الإشعارات
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from flask import Blueprint

notifications_blueprint = Blueprint('notifications', __name__, url_prefix='/api/notifications')

from src.modules.notifications.api import *  # noqa
