"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/setup/__init__.py
الوصف: ملف التهيئة الأساسي لمديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from flask import Blueprint

setup_blueprint = Blueprint('setup', __name__, url_prefix='/api/setup')

from src.modules.setup.api import *  # noqa
