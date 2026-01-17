# FILE: backend/src/validators/common_validators.py | PURPOSE: Common
# Pydantic schemas for API responses | OWNER: Backend | RELATED:
# contracts/openapi.yaml | LAST-AUDITED: 2025-10-27

"""
Common Pydantic Validators

Provides common schemas used across all API endpoints:
- SuccessResponseSchema: Standard success response
- ErrorResponseSchema: Standard error response
- PaginationSchema: Pagination metadata
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class SuccessResponseSchema(BaseModel):
    """
    Standard success response schema

    Aligned with OpenAPI spec: #/components/schemas/SuccessResponse
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    traceId: UUID = Field(..., description="Request trace ID for debugging")
    data: Optional[Dict[str, Any]] = Field(None, description="Optional response data")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "data": {},
            }
        }


class ErrorResponseSchema(BaseModel):
    """
    Standard error response schema

    Aligned with OpenAPI spec: #/components/schemas/ErrorEnvelope
    """

    success: bool = Field(False, description="Operation success status")
    code: str = Field(..., description="Error code for client handling")
    message: str = Field(..., description="Error message")
    traceId: UUID = Field(..., description="Request trace ID for debugging")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Optional error details"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "code": "AUTH_001",
                "message": "Invalid credentials",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "details": None,
            }
        }


class PaginationSchema(BaseModel):
    """
    Pagination metadata schema

    Used in list responses to provide pagination information
    """

    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, le=100, description="Items per page")
    pages: int = Field(..., ge=0, description="Total number of pages")

    class Config:
        json_schema_extra = {
            "example": {"total": 100, "page": 1, "per_page": 20, "pages": 5}
        }
