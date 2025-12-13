# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Product model - Alias to ProductAdvanced
All linting disabled due to SQLAlchemy.
"""

from src.models.product_advanced import (
    ProductAdvanced,
    ProductTypeEnum,
    TrackingTypeEnum,
    QualityGradeEnum,
)

# Create alias for backward compatibility
Product = ProductAdvanced
ProductType = ProductTypeEnum
TrackingType = TrackingTypeEnum

__all__ = [
    "Product",
    "ProductAdvanced",
    "ProductType",
    "ProductTypeEnum",
    "TrackingType",
    "TrackingTypeEnum",
    "QualityGradeEnum",
]
