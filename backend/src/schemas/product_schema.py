# -*- coding: utf-8 -*-
# FILE: backend/src/schemas/product_schema.py | PURPOSE: Marshmallow
# schema for Product validation | OWNER: Backend | RELATED:
# routes/products_fixed.py | LAST-AUDITED: 2025-10-21

from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    """Marshmallow schema for validating product data."""

    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=150),
        error_messages={
            "required": "اسم المنتج مطلوب.",
            "length": "يجب أن يكون اسم المنتج بين 2 و 150 حرفًا.",
        },
    )
    description = fields.Str(required=False, allow_none=True)
    sku = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={"required": "SKU مطلوب."},
    )
    barcode = fields.Str(required=False, allow_none=True)
    price = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        error_messages={
            "required": "السعر مطلوب.",
            "validator_failed": "يجب أن يكون السعر رقمًا موجبًا.",
        },
    )
    cost = fields.Float(required=False, allow_none=True, validate=validate.Range(min=0))
    quantity = fields.Int(
        required=False, allow_none=True, validate=validate.Range(min=0)
    )
    min_quantity = fields.Int(
        required=False, allow_none=True, validate=validate.Range(min=0)
    )
    category_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False, default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
