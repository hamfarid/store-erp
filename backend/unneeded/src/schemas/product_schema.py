# -*- coding: utf-8 -*-
# FILE: backend/src/schemas/product_schema.py | PURPOSE: Marshmallow schema for Product validation | OWNER: Backend | RELATED: routes/products_fixed.py | LAST-AUDITED: 2025-10-21

from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    """Marshmallow schema for validating category data."""

    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "اسم الفئة مطلوب."},
    )
    name_ar = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "الاسم العربي مطلوب."},
    )
    description = fields.Str(required=False, allow_none=True)
    description_ar = fields.Str(required=False, allow_none=True)
    parent_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False, dump_default=True)
    sort_order = fields.Int(required=False, dump_default=0)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class BrandSchema(Schema):
    """Marshmallow schema for validating brand data."""

    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "اسم العلامة التجارية مطلوب."},
    )
    name_ar = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "الاسم العربي مطلوب."},
    )
    description = fields.Str(required=False, allow_none=True)
    description_ar = fields.Str(required=False, allow_none=True)
    logo_url = fields.Str(required=False, allow_none=True)
    website = fields.Str(required=False, allow_none=True)
    is_active = fields.Bool(required=False, dump_default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProductImageSchema(Schema):
    """Marshmallow schema for validating product image data."""

    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    image_url = fields.Str(required=True)
    thumbnail_url = fields.Str(required=False, allow_none=True)
    medium_url = fields.Str(required=False, allow_none=True)
    large_url = fields.Str(required=False, allow_none=True)
    is_primary = fields.Bool(required=False, dump_default=False)
    sort_order = fields.Int(required=False, dump_default=0)
    alt_text = fields.Str(required=False, allow_none=True)
    alt_text_ar = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class ProductCreateSchema(Schema):
    """Schema for creating new products."""

    name = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    name_ar = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    sku = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    barcode = fields.Str(required=False, allow_none=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    cost = fields.Float(required=False, allow_none=True)
    category_id = fields.Int(required=True)
    supplier_id = fields.Int(required=False, allow_none=True)
    brand_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False, dump_default=True)


class ProductUpdateSchema(Schema):
    """Schema for updating products."""

    name = fields.Str(required=False, validate=validate.Length(min=2, max=150))
    name_ar = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    sku = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    barcode = fields.Str(required=False, allow_none=True)
    price = fields.Float(required=False, validate=validate.Range(min=0))
    cost = fields.Float(required=False, allow_none=True)
    category_id = fields.Int(required=False)
    supplier_id = fields.Int(required=False, allow_none=True)
    brand_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False)


class ProductSearchSchema(Schema):
    """Schema for product search parameters."""

    query = fields.Str(required=False, allow_none=True)
    category_id = fields.Int(required=False, allow_none=True)
    supplier_id = fields.Int(required=False, allow_none=True)
    brand_id = fields.Int(required=False, allow_none=True)
    min_price = fields.Float(required=False, allow_none=True)
    max_price = fields.Float(required=False, allow_none=True)
    is_active = fields.Bool(required=False, allow_none=True)
    page = fields.Int(required=False, dump_default=1)
    per_page = fields.Int(required=False, dump_default=20)
    sort_by = fields.Str(required=False, allow_none=True)
    sort_order = fields.Str(required=False, allow_none=True)


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
    is_active = fields.Bool(required=False, dump_default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
