#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام التحقق من البيانات
Data Validation System

مجموعة من الدوال للتحقق من صحة البيانات
"""

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from functools import wraps
from flask import request
from .error_handlers import ValidationError


def validate_required_fields(data, required_fields):
    """
    التحقق من وجود الحقول المطلوبة
    Validate required fields

    Args:
        data: البيانات المراد التحقق منها
        required_fields: قائمة الحقول المطلوبة

    Raises:
        ValidationError: إذا كان هناك حقل مفقود
    """
    missing_fields = []

    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)

    if missing_fields:
        raise ValidationError(
            message=f'الحقول التالية مطلوبة: {", ".join(missing_fields)}',
            message_en=f'The following fields are required: {", ".join(missing_fields)}',
            errors={"missing_fields": missing_fields},
        )


def validate_email(email):
    """
    التحقق من صحة البريد الإلكتروني
    Validate email format
    """
    if not email:
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    التحقق من صحة رقم الهاتف
    Validate phone number
    """
    if not phone:
        return False

    # إزالة المسافات والرموز
    phone_clean = re.sub(r"[\s\-\(\)\+]", "", phone)

    # التحقق من أن الرقم يحتوي على أرقام فقط وطوله مناسب
    return phone_clean.isdigit() and 10 <= len(phone_clean) <= 15


def validate_date(date_string, format="%Y-%m-%d"):
    """
    التحقق من صحة التاريخ
    Validate date format
    """
    if not date_string:
        return False

    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False


def validate_number(value, min_value=None, max_value=None):
    """
    التحقق من صحة الرقم
    Validate number
    """
    try:
        num = Decimal(str(value))

        if min_value is not None and num < Decimal(str(min_value)):
            return False

        if max_value is not None and num > Decimal(str(max_value)):
            return False

        return True
    except (ValueError, InvalidOperation):
        return False


def validate_string_length(value, min_length=None, max_length=None):
    """
    التحقق من طول النص
    Validate string length
    """
    if not isinstance(value, str):
        return False

    length = len(value)

    if min_length is not None and length < min_length:
        return False

    if max_length is not None and length > max_length:
        return False

    return True


def validate_choice(value, choices):
    """
    التحقق من أن القيمة ضمن الخيارات المسموحة
    Validate value is in allowed choices
    """
    return value in choices


def validate_json_schema(data, schema):
    """
    التحقق من البيانات حسب Schema محدد
    Validate data against a schema

    Args:
        data: البيانات المراد التحقق منها
        schema: Schema التحقق
            {
                'field_name': {
                    'type': 'string|number|email|phone|date|choice',
                    'required': True|False,
                    'min': value,
                    'max': value,
                    'choices': [list],
                    'min_length': value,
                    'max_length': value
                }
            }

    Raises:
        ValidationError: إذا كانت البيانات غير صحيحة
    """
    errors = {}

    for field_name, rules in schema.items():
        value = data.get(field_name)

        # التحقق من الحقول المطلوبة
        if rules.get("required", False):
            if value is None or value == "":
                errors[field_name] = "هذا الحقل مطلوب | This field is required"
                continue

        # إذا كانت القيمة فارغة وليست مطلوبة، تخطي باقي التحققات
        if value is None or value == "":
            continue

        field_type = rules.get("type", "string")

        # التحقق حسب النوع
        if field_type == "email":
            if not validate_email(value):
                errors[field_name] = "البريد الإلكتروني غير صحيح | Invalid email"

        elif field_type == "phone":
            if not validate_phone(value):
                errors[field_name] = "رقم الهاتف غير صحيح | Invalid phone number"

        elif field_type == "date":
            if not validate_date(value):
                errors[field_name] = "التاريخ غير صحيح | Invalid date"

        elif field_type == "number":
            min_val = rules.get("min")
            max_val = rules.get("max")
            if not validate_number(value, min_val, max_val):
                if min_val is not None and max_val is not None:
                    errors[field_name] = (
                        f"يجب أن يكون الرقم بين {min_val} و {max_val} | Number must be between {min_val} and {max_val}"
                    )
                elif min_val is not None:
                    errors[field_name] = (
                        f"يجب أن يكون الرقم أكبر من أو يساوي {min_val} | Number must be >= {min_val}"
                    )
                elif max_val is not None:
                    errors[field_name] = (
                        f"يجب أن يكون الرقم أصغر من أو يساوي {max_val} | Number must be <= {max_val}"
                    )
                else:
                    errors[field_name] = "الرقم غير صحيح | Invalid number"

        elif field_type == "string":
            min_len = rules.get("min_length")
            max_len = rules.get("max_length")
            if not validate_string_length(value, min_len, max_len):
                if min_len is not None and max_len is not None:
                    errors[field_name] = (
                        f"يجب أن يكون الطول بين {min_len} و {max_len} حرف | Length must be between {min_len} and {max_len} characters"
                    )
                elif min_len is not None:
                    errors[field_name] = (
                        f"يجب أن يكون الطول {min_len} حرف على الأقل | Minimum length is {min_len} characters"
                    )
                elif max_len is not None:
                    errors[field_name] = (
                        f"يجب أن لا يتجاوز الطول {max_len} حرف | Maximum length is {max_len} characters"
                    )

        elif field_type == "choice":
            choices = rules.get("choices", [])
            if not validate_choice(value, choices):
                choices_str = ", ".join(map(str, choices))
                errors[field_name] = (
                    f"القيمة يجب أن تكون من: {choices_str} | Value must be one of: {choices_str}"
                )

    if errors:
        raise ValidationError(
            message="البيانات المدخلة غير صحيحة",
            message_en="Invalid input data",
            errors=errors,
        )


def validate_request(schema):
    """
    Decorator للتحقق من بيانات الطلب
    Decorator to validate request data

    Usage:
        @validate_request({
            'name': {'type': 'string', 'required': True, 'min_length': 3},
            'email': {'type': 'email', 'required': True},
            'age': {'type': 'number', 'min': 18, 'max': 100}
        })
        def create_user():
            data = request.get_json()
            # البيانات تم التحقق منها بالفعل
            ...
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            validate_json_schema(data, schema)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Schemas جاهزة للاستخدام
USER_SCHEMA = {
    "username": {"type": "string", "required": True, "min_length": 3, "max_length": 50},
    "email": {"type": "email", "required": True},
    "password": {"type": "string", "required": True, "min_length": 6},
    "full_name": {
        "type": "string",
        "required": True,
        "min_length": 3,
        "max_length": 100,
    },
    "phone": {"type": "phone", "required": False},
}

PRODUCT_SCHEMA = {
    "name": {"type": "string", "required": True, "min_length": 3, "max_length": 200},
    "sku": {"type": "string", "required": True, "min_length": 3, "max_length": 100},
    "price": {"type": "number", "required": True, "min": 0},
    "cost": {"type": "number", "required": False, "min": 0},
    "quantity": {"type": "number", "required": False, "min": 0},
    "category_id": {"type": "number", "required": False, "min": 1},
}

INVOICE_SCHEMA = {
    "invoice_type": {
        "type": "choice",
        "required": True,
        "choices": ["sales", "purchase", "sales_return", "purchase_return"],
    },
    "invoice_date": {"type": "date", "required": True},
    "customer_id": {"type": "number", "required": False, "min": 1},
    "supplier_id": {"type": "number", "required": False, "min": 1},
    "warehouse_id": {"type": "number", "required": False, "min": 1},
}

CUSTOMER_SCHEMA = {
    "name": {"type": "string", "required": True, "min_length": 3, "max_length": 200},
    "email": {"type": "email", "required": False},
    "phone": {"type": "phone", "required": False},
    "address": {"type": "string", "required": False, "max_length": 500},
}
