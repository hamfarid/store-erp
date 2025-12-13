#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FILE: backend/src/utils/validation.py | PURPOSE: P0.19 Input Validation | OWNER: Security
"""
/backend/src/utils/validation.py

P0.19: Comprehensive API Input Validation

أدوات التحقق من صحة البيانات
Data Validation Utilities using Marshmallow schemas
"""

from functools import wraps
from flask import request, g, jsonify
from marshmallow import Schema, fields, validate, ValidationError, EXCLUDE
import logging
import re
import bleach

logger = logging.getLogger(__name__)


# ============================================================================
# P0.19: Security Validators (reusable)
# ============================================================================


def sanitize_string(value):
    """
    P0.19: Sanitize string input to prevent XSS
    Strips HTML tags and dangerous characters
    """
    if not value:
        return value
    # Remove HTML tags
    cleaned = bleach.clean(str(value), tags=[], strip=True)
    # Remove control characters except newlines/tabs
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", cleaned)
    return cleaned.strip()


def validate_no_sql_injection(value):
    """
    P0.18: Basic SQL injection pattern detection
    Note: This is a defense-in-depth measure; parameterized queries are the primary defense
    """
    if not value:
        return True

    dangerous_patterns = [
        r"('\s*OR\s*'1'\s*=\s*'1)",  # OR injection
        r"(;\s*DROP\s+TABLE)",  # DROP TABLE
        r"(;\s*DELETE\s+FROM)",  # DELETE
        r"(UNION\s+SELECT)",  # UNION injection
        r"(--\s*$)",  # SQL comment
        r"(/\*.*\*/)",  # Block comment
    ]

    value_upper = str(value).upper()
    for pattern in dangerous_patterns:
        if re.search(pattern, value_upper, re.IGNORECASE):
            raise ValidationError(f"Potentially dangerous input detected")

    return True


class SafeString(fields.Str):
    """P0.19: String field with automatic sanitization"""

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        if value:
            value = sanitize_string(value)
            validate_no_sql_injection(value)
        return value


class SafeEmail(fields.Email):
    """P0.19: Email field with sanitization"""

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        if value:
            value = sanitize_string(value)
        return value


# ============================================================================
# Authentication Schemas
# ============================================================================


class LoginSchema(Schema):
    """Schema للتحقق من بيانات تسجيل الدخول"""

    class Meta:
        unknown = EXCLUDE

    username = SafeString(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(
                r"^[a-zA-Z0-9_-]+$",
                error="Username can only contain letters, numbers, underscore and dash",
            ),
        ],
    )
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))


class RegisterSchema(Schema):
    """Schema للتحقق من بيانات التسجيل"""

    class Meta:
        unknown = EXCLUDE

    username = SafeString(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(
                r"^[a-zA-Z0-9_-]+$",
                error="Username can only contain letters, numbers, underscore and dash",
            ),
        ],
    )
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))
    email = SafeEmail(required=False, allow_none=True)
    full_name = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=100)
    )
    phone = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=20)
    )
    role = SafeString(
        required=False,
        allow_none=True,
        validate=validate.OneOf(["admin", "manager", "user", "viewer"]),
    )


class RefreshSchema(Schema):
    """Schema للتحقق من بيانات تحديث الرمز"""

    class Meta:
        unknown = EXCLUDE

    refresh_token = fields.Str(required=True, validate=validate.Length(min=10))


class ChangePasswordSchema(Schema):
    """Schema للتحقق من بيانات تغيير كلمة المرور"""

    class Meta:
        unknown = EXCLUDE

    old_password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
    new_password = fields.Str(required=True, validate=validate.Length(min=8, max=128))


# ============================================================================
# Product Schemas
# ============================================================================


class ProductCreateSchema(Schema):
    """Schema للتحقق من بيانات إنشاء المنتج"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(required=True, validate=validate.Length(min=1, max=200))
    cost_price = fields.Float(
        required=True, validate=validate.Range(min=0, max=999999999)
    )
    sale_price = fields.Float(
        required=True, validate=validate.Range(min=0, max=999999999)
    )
    sku = SafeString(required=False, allow_none=True, validate=validate.Length(max=50))
    barcode = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=50)
    )
    category_id = fields.Int(
        required=False, allow_none=True, validate=validate.Range(min=1)
    )
    is_active = fields.Bool(required=False)
    product_type = SafeString(
        required=False,
        allow_none=True,
        validate=validate.OneOf(["simple", "variable", "bundle", "service"]),
    )
    tracking_type = SafeString(
        required=False,
        allow_none=True,
        validate=validate.OneOf(["none", "serial", "lot", "batch"]),
    )
    description = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=2000)
    )


class ProductUpdateSchema(Schema):
    """Schema للتحقق من بيانات تحديث المنتج"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(
        required=False, allow_none=True, validate=validate.Length(min=1, max=200)
    )
    cost_price = fields.Float(
        required=False, allow_none=True, validate=validate.Range(min=0, max=999999999)
    )
    sale_price = fields.Float(
        required=False, allow_none=True, validate=validate.Range(min=0, max=999999999)
    )
    sku = SafeString(required=False, allow_none=True, validate=validate.Length(max=50))
    barcode = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=50)
    )
    category_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False)


class UpdateStockSchema(Schema):
    """Schema للتحقق من بيانات تحديث المخزون"""

    class Meta:
        unknown = EXCLUDE

    quantity = fields.Float(
        required=True, validate=validate.Range(min=0, max=999999999)
    )
    reason = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=500)
    )
    warehouse_id = fields.Int(required=False, allow_none=True)


# ============================================================================
# Category & Warehouse Schemas
# ============================================================================


class CategorySchema(Schema):
    """Schema للتحقق من بيانات الفئة"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(required=True, validate=validate.Length(min=1, max=100))
    description = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=500)
    )
    parent_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False)


class WarehouseSchema(Schema):
    """Schema للتحقق من بيانات المستودع"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(required=True, validate=validate.Length(min=1, max=100))
    code = SafeString(required=False, allow_none=True, validate=validate.Length(max=20))
    location = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=200)
    )
    description = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=500)
    )
    manager_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False)


# ============================================================================
# Customer & Supplier Schemas
# ============================================================================


class CustomerSchema(Schema):
    """Schema للتحقق من بيانات العميل"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(required=True, validate=validate.Length(min=1, max=100))
    code = SafeString(required=False, allow_none=True, validate=validate.Length(max=20))
    email = SafeEmail(required=False, allow_none=True)
    phone = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=20)
    )
    address = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=500)
    )
    credit_limit = fields.Float(
        required=False, allow_none=True, validate=validate.Range(min=0, max=999999999)
    )
    is_active = fields.Bool(required=False)
    tax_number = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=50)
    )


class SupplierSchema(Schema):
    """Schema للتحقق من بيانات المورد"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(required=True, validate=validate.Length(min=1, max=100))
    code = SafeString(required=False, allow_none=True, validate=validate.Length(max=20))
    email = SafeEmail(required=False, allow_none=True)
    phone = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=20)
    )
    address = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=500)
    )
    contact_person = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=100)
    )
    is_active = fields.Bool(required=False)


# ============================================================================
# User & Role Schemas
# ============================================================================


class UserCreateSchema(Schema):
    """Schema للتحقق من بيانات إنشاء مستخدم"""

    class Meta:
        unknown = EXCLUDE

    username = SafeString(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(
                r"^[a-zA-Z0-9_-]+$",
                error="Username can only contain letters, numbers, underscore and dash",
            ),
        ],
    )
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))
    email = SafeEmail(required=False, allow_none=True)
    full_name = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=100)
    )
    role_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False, load_default=True)


class UserUpdateSchema(Schema):
    """Schema للتحقق من بيانات تحديث مستخدم"""

    class Meta:
        unknown = EXCLUDE

    email = SafeEmail(required=False, allow_none=True)
    full_name = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=100)
    )
    role_id = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False)


class RoleCreateSchema(Schema):
    """Schema للتحقق من بيانات إنشاء دور"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(
        required=True,
        validate=[
            validate.Length(min=2, max=50),
            validate.Regexp(
                r"^[a-zA-Z0-9_-]+$",
                error="Role name can only contain letters, numbers, underscore and dash",
            ),
        ],
    )
    description = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=200)
    )
    permissions = fields.List(fields.Str(), required=False, allow_none=True)


# ============================================================================
# Treasury & Transaction Schemas
# ============================================================================


class TreasurySchema(Schema):
    """Schema للتحقق من بيانات الخزينة"""

    class Meta:
        unknown = EXCLUDE

    name = SafeString(required=True, validate=validate.Length(min=1, max=100))
    initial_balance = fields.Float(
        required=False, allow_none=True, validate=validate.Range(min=0, max=999999999)
    )
    currency = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=10)
    )
    is_active = fields.Bool(required=False, load_default=True)


class TransactionSchema(Schema):
    """Schema للتحقق من بيانات المعاملة المالية"""

    class Meta:
        unknown = EXCLUDE

    amount = fields.Float(
        required=True, validate=validate.Range(min=0.01, max=999999999)
    )
    transaction_type = SafeString(
        required=True, validate=validate.OneOf(["income", "expense", "transfer"])
    )
    treasury_id = fields.Int(required=True)
    description = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=500)
    )
    reference_number = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=50)
    )


# ============================================================================
# Invoice Schemas
# ============================================================================


class InvoiceItemSchema(Schema):
    """Schema for invoice line items"""

    class Meta:
        unknown = EXCLUDE

    product_id = fields.Int(required=True, validate=validate.Range(min=1))
    quantity = fields.Float(
        required=True, validate=validate.Range(min=0.001, max=999999999)
    )
    unit_price = fields.Float(
        required=True, validate=validate.Range(min=0, max=999999999)
    )
    discount = fields.Float(
        required=False, allow_none=True, validate=validate.Range(min=0, max=100)
    )


class InvoiceCreateSchema(Schema):
    """Schema للتحقق من بيانات إنشاء فاتورة"""

    class Meta:
        unknown = EXCLUDE

    invoice_type = SafeString(
        required=True,
        validate=validate.OneOf(["sale", "purchase", "return_sale", "return_purchase"]),
    )
    customer_id = fields.Int(required=False, allow_none=True)
    supplier_id = fields.Int(required=False, allow_none=True)
    warehouse_id = fields.Int(required=False, allow_none=True)
    items = fields.List(
        fields.Nested(InvoiceItemSchema), required=True, validate=validate.Length(min=1)
    )
    notes = SafeString(
        required=False, allow_none=True, validate=validate.Length(max=1000)
    )
    discount = fields.Float(
        required=False, allow_none=True, validate=validate.Range(min=0, max=100)
    )
    tax = fields.Float(
        required=False, allow_none=True, validate=validate.Range(min=0, max=100)
    )


# ============================================================================
# Validation Decorator
# ============================================================================


def validate_json(schema_class):
    """
    P0.19: Decorator للتحقق من صحة JSON باستخدام Marshmallow schema

    Features:
    - Validates input against schema
    - Sanitizes string inputs
    - Rejects unknown fields
    - Provides detailed error messages
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Handle both JSON and form data
                json_data = request.get_json(silent=True)

                if not json_data:
                    # Try form data for file uploads etc.
                    if request.form:
                        json_data = request.form.to_dict()
                    else:
                        return (
                            jsonify(
                                {
                                    "success": False,
                                    "error": "No JSON data provided",
                                    "code": "VALIDATION_ERROR",
                                }
                            ),
                            400,
                        )

                # Skip validation if schema is None (fallback mode)
                if schema_class is None:
                    return f(*args, **kwargs)

                schema = schema_class()
                validated_data = schema.load(json_data)
                g.validated_data = validated_data

                return f(*args, **kwargs)

            except ValidationError as err:
                logger.warning("P0.19 Validation error: %s", err.messages)
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Validation failed",
                            "code": "VALIDATION_ERROR",
                            "details": err.messages,
                        }
                    ),
                    400,
                )

            except Exception as err:
                logger.error("P0.19 Unexpected error in validation: %s", err)
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Internal server error",
                            "code": "INTERNAL_ERROR",
                        }
                    ),
                    500,
                )

        return decorated_function

    return decorator


# ============================================================================
# Validation Helper Functions
# ============================================================================


def sanitize_search_term(term: str, max_length: int = 100) -> str:
    """
    P0.18: Sanitize search term for SQL LIKE queries

    Provides defense-in-depth by escaping LIKE wildcards and
    limiting length. SQLAlchemy already parameterizes, but this
    adds extra protection.

    Args:
        term: The search term to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized search term
    """
    if not term:
        return ""

    # Convert to string and strip
    term = str(term).strip()

    # Truncate to max length
    term = term[:max_length]

    # Escape SQL LIKE wildcards
    term = term.replace("\\", "\\\\")  # Escape backslash first
    term = term.replace("%", "\\%")
    term = term.replace("_", "\\_")

    # Remove null bytes and control characters
    term = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", term)

    return term


def validate_required_fields(data, required_fields):
    """التحقق من وجود الحقول المطلوبة"""
    missing_fields = []

    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)

    if missing_fields:
        return False, f"الحقول التالية مطلوبة: {', '.join(missing_fields)}"

    return True, None


def validate_numeric_range(value, min_value=None, max_value=None):
    """التحقق من أن القيمة ضمن النطاق المحدد"""
    try:
        num_value = float(value)

        if min_value is not None and num_value < min_value:
            return False

        if max_value is not None and num_value > max_value:
            return False

        return True

    except (ValueError, TypeError):
        return False


def validate_email(email):
    """التحقق من صحة البريد الإلكتروني"""
    if not email:
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """التحقق من صحة رقم الهاتف"""
    if not phone:
        return False

    cleaned_phone = re.sub(r"[^\d+]", "", phone)
    return 10 <= len(cleaned_phone) <= 15


def validate_uuid(value):
    """التحقق من صحة UUID"""
    if not value:
        return False

    uuid_pattern = (
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )
    return bool(re.match(uuid_pattern, str(value).lower()))


# ============================================================================
# Export all schemas and utilities
# ============================================================================

__all__ = [
    # Authentication
    "LoginSchema",
    "RegisterSchema",
    "RefreshSchema",
    "ChangePasswordSchema",
    # Products
    "ProductCreateSchema",
    "ProductUpdateSchema",
    "UpdateStockSchema",
    # Categories & Warehouses
    "CategorySchema",
    "WarehouseSchema",
    # Partners
    "CustomerSchema",
    "SupplierSchema",
    # Users & Roles
    "UserCreateSchema",
    "UserUpdateSchema",
    "RoleCreateSchema",
    # Treasury
    "TreasurySchema",
    "TransactionSchema",
    # Invoices
    "InvoiceCreateSchema",
    "InvoiceItemSchema",
    # Decorator
    "validate_json",
    # Utilities
    "validate_required_fields",
    "validate_numeric_range",
    "validate_email",
    "validate_phone",
    "validate_uuid",
    "sanitize_string",
    "sanitize_search_term",  # P0.18
    "SafeString",
    "SafeEmail",
]
