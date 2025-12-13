# -*- coding: utf-8 -*-
# FILE: backend/src/schemas/auth_schemas.py | PURPOSE: Marshmallow schemas
# for Auth validation | OWNER: Backend | RELATED: auth_fixed.py |
# LAST-AUDITED: 2025-10-21

from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    """Schema for user registration."""

    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))


class LoginSchema(Schema):
    """Schema for user login."""

    email = fields.Email(required=True)
    password = fields.Str(required=True)
