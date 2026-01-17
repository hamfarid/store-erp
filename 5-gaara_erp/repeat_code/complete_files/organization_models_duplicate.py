# organization/models.py
"""
Compatibility alias module for legacy imports.
Re-exports models from their current locations to maintain backward compatibility.
"""

# Re-export Company and Branch from their current location
from core_modules.core.models import Branch, Company

# Re-export other commonly imported models if they exist
try:
    from core_modules.core.models import Department
except ImportError:
    pass

try:
    from core_modules.system_settings.models import Country, Currency
except ImportError:
    pass

# Make all imports available at module level
__all__ = ["Company", "Branch"]

# Add Department, Country, Currency to __all__ if they were successfully imported
import sys

current_module = sys.modules[__name__]
if hasattr(current_module, "Department"):
    __all__.append("Department")
if hasattr(current_module, "Country"):
    __all__.append("Country")
if hasattr(current_module, "Currency"):
    __all__.append("Currency")
