# -*- coding: utf-8 -*-
# FILE: backend/src/schemas/inventory_schemas.py | PURPOSE: Marshmallow
# schemas for Inventory validation | OWNER: Backend | RELATED:
# routes/inventory_fixed.py | LAST-AUDITED: 2025-10-21

from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    """Schema for Category validation."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(required=False, allow_none=True)


class ProductGroupSchema(Schema):
    """Schema for ProductGroup validation."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category_id = fields.Int(required=True)
    description = fields.Str(required=False, allow_none=True)


class RankSchema(Schema):
    """Schema for Rank validation."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    group_id = fields.Int(required=True)
    description = fields.Str(required=False, allow_none=True)
