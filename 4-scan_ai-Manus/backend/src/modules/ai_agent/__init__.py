"""
/home/ubuntu/implemented_files/v3/src/modules/ai_agent/__init__.py

مديول وكلاء الذكاء الاصطناعي لنظام Gaara ERP

يوفر هذا المديول وظائف إدارة وكلاء الذكاء الاصطناعي، بما في ذلك:
- إنشاء وتكوين وإدارة وكلاء الذكاء الاصطناعي
- تنفيذ المهام باستخدام وكلاء الذكاء الاصطناعي
- تكامل الوكلاء مع مديولات النظام الأخرى
- مراقبة أداء الوكلاء وتحسينه
"""

from .config import default_config
from .models import AgentRole, AgentStatus, AgentType

__version__ = "1.0.0"
__author__ = "Gaara ERP Team"

# تصدير الدوال والكائنات
__all__ = [
    'default_config',
    'AgentType',
    'AgentStatus',
    'AgentRole'
]
