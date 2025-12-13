#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.85: Tax Calculation System

Flexible tax calculation service supporting multiple tax types.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from src.database import db
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# Tax Configuration
# =============================================================================


@dataclass
class TaxRate:
    """Tax rate configuration."""

    code: str
    name: str
    name_ar: str
    rate: float
    is_inclusive: bool = False
    is_compound: bool = False
    apply_to: str = "all"  # all, products, services


# Default VAT rates (Saudi Arabia)
DEFAULT_TAX_RATES = {
    "VAT": TaxRate(
        code="VAT",
        name="Value Added Tax",
        name_ar="ضريبة القيمة المضافة",
        rate=15.0,
        is_inclusive=False,
    ),
    "VAT_ZERO": TaxRate(
        code="VAT_ZERO",
        name="Zero-rated VAT",
        name_ar="ضريبة صفرية",
        rate=0.0,
        is_inclusive=False,
    ),
    "EXEMPT": TaxRate(
        code="EXEMPT",
        name="Tax Exempt",
        name_ar="معفى من الضريبة",
        rate=0.0,
        is_inclusive=False,
    ),
}


class TaxConfiguration(db.Model):
    """Database-stored tax configuration."""

    __tablename__ = "tax_configurations"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100))
    rate = db.Column(db.Float, nullable=False)
    is_inclusive = db.Column(db.Boolean, default=False)
    is_compound = db.Column(db.Boolean, default=False)
    apply_to = db.Column(db.String(50), default="all")
    is_active = db.Column(db.Boolean, default=True)

    # Validity period
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "name_ar": self.name_ar,
            "rate": self.rate,
            "is_inclusive": self.is_inclusive,
            "is_compound": self.is_compound,
            "apply_to": self.apply_to,
            "is_active": self.is_active,
        }


# =============================================================================
# Tax Calculation Service
# =============================================================================


@dataclass
class TaxBreakdown:
    """Breakdown of tax calculation."""

    tax_code: str
    tax_name: str
    rate: float
    taxable_amount: float
    tax_amount: float
    is_inclusive: bool


@dataclass
class TaxResult:
    """Result of tax calculation."""

    subtotal: float
    total_tax: float
    total: float
    breakdown: List[TaxBreakdown]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subtotal": round(self.subtotal, 2),
            "total_tax": round(self.total_tax, 2),
            "total": round(self.total, 2),
            "breakdown": [
                {
                    "tax_code": b.tax_code,
                    "tax_name": b.tax_name,
                    "rate": b.rate,
                    "taxable_amount": round(b.taxable_amount, 2),
                    "tax_amount": round(b.tax_amount, 2),
                    "is_inclusive": b.is_inclusive,
                }
                for b in self.breakdown
            ],
        }


class TaxService:
    """
    P2.85: Tax calculation service.

    Features:
    - Multiple tax rates
    - Inclusive/Exclusive tax
    - Compound taxes
    - Product-specific tax rates
    """

    @staticmethod
    def get_tax_rate(tax_code: str) -> Optional[TaxRate]:
        """Get tax rate by code."""
        # First check database
        config = TaxConfiguration.query.filter_by(code=tax_code, is_active=True).first()

        if config:
            return TaxRate(
                code=config.code,
                name=config.name,
                name_ar=config.name_ar,
                rate=config.rate,
                is_inclusive=config.is_inclusive,
                is_compound=config.is_compound,
                apply_to=config.apply_to,
            )

        # Fall back to defaults
        return DEFAULT_TAX_RATES.get(tax_code)

    @staticmethod
    def calculate_tax(
        amount: float, tax_code: str = "VAT", quantity: int = 1
    ) -> TaxResult:
        """
        Calculate tax for an amount.

        Args:
            amount: Unit price or total amount
            tax_code: Tax rate code to apply
            quantity: Quantity (for unit price calculation)

        Returns:
            TaxResult with breakdown
        """
        tax_rate = TaxService.get_tax_rate(tax_code)

        if not tax_rate or tax_rate.rate == 0:
            return TaxResult(
                subtotal=amount * quantity,
                total_tax=0,
                total=amount * quantity,
                breakdown=[],
            )

        base_amount = amount * quantity

        if tax_rate.is_inclusive:
            # Price includes tax
            tax_amount = base_amount - (base_amount / (1 + tax_rate.rate / 100))
            subtotal = base_amount - tax_amount
        else:
            # Tax on top
            subtotal = base_amount
            tax_amount = base_amount * (tax_rate.rate / 100)

        # Round to 2 decimal places
        tax_amount = float(
            Decimal(str(tax_amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )
        subtotal = float(
            Decimal(str(subtotal)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )

        breakdown = [
            TaxBreakdown(
                tax_code=tax_rate.code,
                tax_name=tax_rate.name_ar or tax_rate.name,
                rate=tax_rate.rate,
                taxable_amount=subtotal,
                tax_amount=tax_amount,
                is_inclusive=tax_rate.is_inclusive,
            )
        ]

        return TaxResult(
            subtotal=subtotal,
            total_tax=tax_amount,
            total=subtotal + tax_amount,
            breakdown=breakdown,
        )

    @staticmethod
    def calculate_line_items(
        items: List[Dict[str, Any]], default_tax_code: str = "VAT"
    ) -> Dict[str, Any]:
        """
        Calculate taxes for multiple line items.

        Args:
            items: List of items with 'amount', 'quantity', 'tax_code' (optional)
            default_tax_code: Default tax code if not specified

        Returns:
            Combined tax calculation result
        """
        total_subtotal = 0
        total_tax = 0
        all_breakdowns = []

        for item in items:
            amount = item.get("amount", 0)
            quantity = item.get("quantity", 1)
            tax_code = item.get("tax_code", default_tax_code)

            result = TaxService.calculate_tax(amount, tax_code, quantity)

            total_subtotal += result.subtotal
            total_tax += result.total_tax
            all_breakdowns.extend(result.breakdown)

        # Consolidate breakdowns by tax code
        consolidated = {}
        for bd in all_breakdowns:
            if bd.tax_code not in consolidated:
                consolidated[bd.tax_code] = TaxBreakdown(
                    tax_code=bd.tax_code,
                    tax_name=bd.tax_name,
                    rate=bd.rate,
                    taxable_amount=0,
                    tax_amount=0,
                    is_inclusive=bd.is_inclusive,
                )
            consolidated[bd.tax_code].taxable_amount += bd.taxable_amount
            consolidated[bd.tax_code].tax_amount += bd.tax_amount

        return TaxResult(
            subtotal=total_subtotal,
            total_tax=total_tax,
            total=total_subtotal + total_tax,
            breakdown=list(consolidated.values()),
        )

    @staticmethod
    def extract_tax_from_inclusive(
        total_with_tax: float, tax_rate: float
    ) -> Dict[str, float]:
        """Extract tax amount from an inclusive price."""
        tax_amount = total_with_tax - (total_with_tax / (1 + tax_rate / 100))
        subtotal = total_with_tax - tax_amount

        return {
            "subtotal": round(subtotal, 2),
            "tax_amount": round(tax_amount, 2),
            "total": round(total_with_tax, 2),
            "tax_rate": tax_rate,
        }

    @staticmethod
    def add_tax_to_price(price_without_tax: float, tax_rate: float) -> Dict[str, float]:
        """Add tax to a price."""
        tax_amount = price_without_tax * (tax_rate / 100)
        total = price_without_tax + tax_amount

        return {
            "subtotal": round(price_without_tax, 2),
            "tax_amount": round(tax_amount, 2),
            "total": round(total, 2),
            "tax_rate": tax_rate,
        }


__all__ = [
    "TaxService",
    "TaxConfiguration",
    "TaxRate",
    "TaxResult",
    "TaxBreakdown",
    "DEFAULT_TAX_RATES",
]
