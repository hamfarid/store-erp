"""
FILE: backend/src/models/__init__.py | PURPOSE: Database models initialization | OWNER: Backend Team | LAST-AUDITED: 2025-11-18

SQLAlchemy database models
"""

__version__ = "1.0.0"

from .breeding import BreedingProgram
from .company import Company
from .crop import Crop
from .diagnosis import Diagnosis
from .disease import Disease
from .equipment import Equipment
from .farm import Farm
from .inventory import Inventory
from .report import Report
from .sensor import Sensor, SensorReading

# Import all models
from .user import User

__all__ = [
    'User',
    'Farm',
    'Diagnosis',
    'Report',
    'Crop',
    'Disease',
    'Sensor',
    'SensorReading',
    'Equipment',
    'Inventory',
    'Company',
    'BreedingProgram',
]
