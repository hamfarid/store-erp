# File: /home/ubuntu/ai_web_organized/src/modules/disease_diagnosis/__init__.py
"""
from flask import g
مديول تشخيص الأمراض النباتية
يوفر هذا المديول وظائف لتشخيص الأمراض النباتية وتقديم توصيات العلاج
"""

from .api import router
from .diagnosis_engine import DiagnosisEngine
from .disease_knowledge_base import DiseaseKnowledgeBase

__all__ = ['router', 'DiseaseKnowledgeBase', 'DiagnosisEngine']
