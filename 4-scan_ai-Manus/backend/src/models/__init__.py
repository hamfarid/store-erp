"""
FILE: backend/src/models/__init__.py | PURPOSE: Database models
OWNER: Backend Team | LAST-AUDITED: 2026-01-31

SQLAlchemy database models - Multi-tenant Support

Version: 2.0.0 - Added Tenant model for multi-tenancy
"""

__version__ = "2.0.0"

from .breeding import BreedingProgram
from .company import Company
from .crop import Crop
from .diagnosis import Diagnosis
from .disease import Disease
from .equipment import Equipment
from .farm import Farm
from .inventory import Inventory
from .notification import Notification, NotificationType
from .report import Report
from .sensor import Sensor, SensorReading
from .tenant import Tenant

# Import all models
from .user import User

__all__ = [
    "BreedingProgram",
    "Company",
    "Crop",
    "Diagnosis",
    "Disease",
    "Equipment",
    "Farm",
    "Inventory",
    "Notification",
    "NotificationType",
    "Report",
    "Sensor",
    "SensorReading",
    "Tenant",
    "User",
]

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
    'Notification',
    'NotificationType',
]
