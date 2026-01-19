"""
مديول محاكاة التهجين النباتي
يوفر هذا المديول وظائف لمحاكاة عمليات التهجين النباتي وإعطاء توصيات للهجائن الجديدة
"""

from .api import router
from .hybridization_simulator import HybridizationSimulator

__all__ = ['router', 'HybridizationSimulator']
