"""
from flask import g
مديول معالجة الصور الزراعية
يوفر هذا المديول وظائف لمعالجة وتحليل الصور الزراعية
"""

from .api import router
from .image_processor import ImageProcessor

__all__ = ['router', 'ImageProcessor']
