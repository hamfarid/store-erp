# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Unified Warehouse Model
Exports the Warehouse model from inventory.py for use in routes
"""

from src.models.inventory import Warehouse

__all__ = ["Warehouse"]
