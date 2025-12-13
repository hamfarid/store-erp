# type: ignore
# flake8: noqa
"""
warehouse.py - Warehouse Model Export
Exports the Warehouse model for backward compatibility.
"""

try:
    from src.models.inventory import Warehouse
except ImportError:
    try:
        from src.models.warehouse_unified import Warehouse
    except ImportError:
        # Create a mock Warehouse class if no models are available
        class Warehouse:
            """Mock Warehouse class for compatibility"""

            __tablename__ = "warehouses"
            pass


__all__ = ["Warehouse"]
