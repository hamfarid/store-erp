# -*- coding: utf-8 -*-
# FILE: backend/src/schemas/report_schemas.py | PURPOSE: Marshmallow
# schemas for Report validation | OWNER: Backend | RELATED:
# routes/reports_fixed.py | LAST-AUDITED: 2025-10-21

from marshmallow import Schema, fields, validate
from datetime import date


class StockValuationSchema(Schema):
    """Schema for stock valuation report parameters."""

    pass  # No parameters for now


class LowStockSchema(Schema):
    """Schema for low stock report parameters."""

    pass  # No parameters for now


class InventoryReportSchema(Schema):
    """Schema for inventory report parameters."""

    warehouse_id = fields.Int(required=False)
    category_id = fields.Int(required=False)
    include_zero_stock = fields.Bool(required=False, dump_default=False)
    low_stock_only = fields.Bool(required=False, dump_default=False)


class StockMovementsSchema(Schema):
    """Schema for stock movements report parameters."""

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    product_id = fields.Int(required=False)
    warehouse_id = fields.Int(required=False)
    movement_type = fields.Str(
        required=False, validate=validate.OneOf(["IN", "OUT", "ADJUSTMENT"])
    )
