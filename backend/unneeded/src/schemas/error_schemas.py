# -*- coding: utf-8 -*-
"""
Error Response Schemas for OpenAPI Documentation
=================================================

Comprehensive error schemas for all API endpoints.
Part of T23: API Documentation Enhancement

Error Codes:
- 400: Bad Request (validation errors)
- 401: Unauthorized (authentication required)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 409: Conflict (duplicate resource)
- 422: Unprocessable Entity (business logic error)
- 429: Too Many Requests (rate limit exceeded)
- 500: Internal Server Error
- 503: Service Unavailable
"""

from marshmallow import Schema, fields


class ValidationErrorDetailSchema(Schema):
    """Single validation error detail."""

    field = fields.String(
        required=True,
        metadata={
            "description": "Field name that failed validation",
            "example": "email",
        },
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Validation error message",
            "example": "Not a valid email address",
        },
    )
    value = fields.Raw(
        allow_none=True,
        metadata={"description": "Invalid value provided", "example": "invalid-email"},
    )


class ErrorResponseSchema(Schema):
    """Standard error response format."""

    error = fields.String(
        required=True,
        metadata={"description": "Error type/code", "example": "VALIDATION_ERROR"},
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Human-readable error message",
            "example": "Validation failed for one or more fields",
        },
    )
    status_code = fields.Integer(
        required=True, metadata={"description": "HTTP status code", "example": 400}
    )
    timestamp = fields.DateTime(
        required=True,
        metadata={
            "description": "Error timestamp (ISO 8601)",
            "example": "2025-11-07T10:30:00Z",
        },
    )
    path = fields.String(
        metadata={
            "description": "Request path that caused the error",
            "example": "/api/auth/login",
        }
    )
    details = fields.List(
        fields.Nested(ValidationErrorDetailSchema),
        allow_none=True,
        metadata={"description": "Detailed validation errors (for 400/422 responses)"},
    )


class BadRequestErrorSchema(ErrorResponseSchema):
    """400 Bad Request - Validation errors."""

    class Meta:
        description = "Request validation failed"
        example = {
            "error": "VALIDATION_ERROR",
            "message": "Validation failed for one or more fields",
            "status_code": 400,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/auth/login",
            "details": [
                {"field": "username", "message": "Field is required", "value": None},
                {
                    "field": "password",
                    "message": "Must be at least 8 characters",
                    "value": "short",
                },
            ],
        }


class UnauthorizedErrorSchema(ErrorResponseSchema):
    """401 Unauthorized - Authentication required."""

    class Meta:
        description = "Authentication required or token invalid/expired"
        example = {
            "error": "UNAUTHORIZED",
            "message": "Authentication required. Please provide a valid access token.",
            "status_code": 401,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/products",
        }


class ForbiddenErrorSchema(ErrorResponseSchema):
    """403 Forbidden - Insufficient permissions."""

    class Meta:
        description = "User doesn't have permission to access this resource"
        example = {
            "error": "FORBIDDEN",
            "message": "You don't have permission to perform this action",
            "status_code": 403,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/products/1",
            "details": [
                {
                    "field": "permission",
                    "message": "Requires 'products:delete' permission",
                    "value": "user",
                }
            ],
        }


class NotFoundErrorSchema(ErrorResponseSchema):
    """404 Not Found - Resource doesn't exist."""

    class Meta:
        description = "Requested resource was not found"
        example = {
            "error": "NOT_FOUND",
            "message": "Product with ID 999 not found",
            "status_code": 404,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/products/999",
        }


class ConflictErrorSchema(ErrorResponseSchema):
    """409 Conflict - Duplicate resource."""

    class Meta:
        description = "Resource already exists (duplicate)"
        example = {
            "error": "CONFLICT",
            "message": "Product with barcode '1234567890' already exists",
            "status_code": 409,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/products",
            "details": [
                {"field": "barcode", "message": "Must be unique", "value": "1234567890"}
            ],
        }


class UnprocessableEntityErrorSchema(ErrorResponseSchema):
    """422 Unprocessable Entity - Business logic error."""

    class Meta:
        description = "Request is valid but business logic prevents processing"
        example = {
            "error": "BUSINESS_LOGIC_ERROR",
            "message": "Insufficient stock for this operation",
            "status_code": 422,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/inventory/stock-movements",
            "details": [
                {
                    "field": "quantity",
                    "message": "Requested 100 but only 50 available",
                    "value": 100,
                }
            ],
        }


class RateLimitErrorSchema(ErrorResponseSchema):
    """429 Too Many Requests - Rate limit exceeded."""

    retry_after = fields.Integer(
        required=True,
        metadata={"description": "Seconds to wait before retrying", "example": 60},
    )

    class Meta:
        description = "Rate limit exceeded"
        example = {
            "error": "RATE_LIMIT_EXCEEDED",
            "message": "Too many requests. Please try again later.",
            "status_code": 429,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/auth/login",
            "retry_after": 60,
        }


class InternalServerErrorSchema(ErrorResponseSchema):
    """500 Internal Server Error."""

    error_id = fields.String(
        metadata={
            "description": "Unique error ID for tracking",
            "example": "err_abc123xyz",
        }
    )

    class Meta:
        description = "Internal server error occurred"
        example = {
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please contact support.",
            "status_code": 500,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/products",
            "error_id": "err_abc123xyz",
        }


class ServiceUnavailableErrorSchema(ErrorResponseSchema):
    """503 Service Unavailable."""

    retry_after = fields.Integer(
        allow_none=True,
        metadata={"description": "Seconds to wait before retrying", "example": 300},
    )

    class Meta:
        description = "Service temporarily unavailable"
        example = {
            "error": "SERVICE_UNAVAILABLE",
            "message": "Service is temporarily unavailable. Please try again later.",
            "status_code": 503,
            "timestamp": "2025-11-07T10:30:00Z",
            "path": "/api/products",
            "retry_after": 300,
        }


# Common error responses for reuse in endpoints
COMMON_ERROR_RESPONSES = {
    400: {
        "description": "Bad Request - Validation errors",
        "content": {
            "application/json": {
                "schema": BadRequestErrorSchema,
                "example": BadRequestErrorSchema.Meta.example,
            }
        },
    },
    401: {
        "description": "Unauthorized - Authentication required",
        "content": {
            "application/json": {
                "schema": UnauthorizedErrorSchema,
                "example": UnauthorizedErrorSchema.Meta.example,
            }
        },
    },
    403: {
        "description": "Forbidden - Insufficient permissions",
        "content": {
            "application/json": {
                "schema": ForbiddenErrorSchema,
                "example": ForbiddenErrorSchema.Meta.example,
            }
        },
    },
    404: {
        "description": "Not Found - Resource doesn't exist",
        "content": {
            "application/json": {
                "schema": NotFoundErrorSchema,
                "example": NotFoundErrorSchema.Meta.example,
            }
        },
    },
    409: {
        "description": "Conflict - Duplicate resource",
        "content": {
            "application/json": {
                "schema": ConflictErrorSchema,
                "example": ConflictErrorSchema.Meta.example,
            }
        },
    },
    422: {
        "description": "Unprocessable Entity - Business logic error",
        "content": {
            "application/json": {
                "schema": UnprocessableEntityErrorSchema,
                "example": UnprocessableEntityErrorSchema.Meta.example,
            }
        },
    },
    429: {
        "description": "Too Many Requests - Rate limit exceeded",
        "content": {
            "application/json": {
                "schema": RateLimitErrorSchema,
                "example": RateLimitErrorSchema.Meta.example,
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "schema": InternalServerErrorSchema,
                "example": InternalServerErrorSchema.Meta.example,
            }
        },
    },
    503: {
        "description": "Service Unavailable",
        "content": {
            "application/json": {
                "schema": ServiceUnavailableErrorSchema,
                "example": ServiceUnavailableErrorSchema.Meta.example,
            }
        },
    },
}
