# FILE: backend/src/validators/mfa_validators.py | PURPOSE: Pydantic
# schemas for MFA endpoints | OWNER: Backend | RELATED:
# contracts/openapi.yaml | LAST-AUDITED: 2025-10-27

"""
MFA Pydantic Validators

Provides schemas for MFA (Multi-Factor Authentication) endpoints:
- MFASetupResponseSchema: MFA setup response with QR code
- MFAVerifyRequestSchema: MFA code verification request
- MFADisableRequestSchema: MFA disable request
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class MFASetupDataSchema(BaseModel):
    """MFA setup data schema"""

    qr_code: str = Field(..., description="Base64-encoded QR code image")
    secret: str = Field(..., description="TOTP secret (for manual entry)")

    class Config:
        json_schema_extra = {
            "example": {
                "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
                "secret": "JBSWY3DPEHPK3PXP",
            }
        }


class MFASetupResponseSchema(BaseModel):
    """
    MFA setup response schema

    Aligned with OpenAPI spec: #/components/schemas/MFASetupResponse
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    traceId: str = Field(..., description="Request trace ID")
    data: MFASetupDataSchema = Field(..., description="MFA setup data")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "MFA setup initiated",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "data": {
                    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
                    "secret": "JBSWY3DPEHPK3PXP",
                },
            }
        }


class MFAVerifyRequestSchema(BaseModel):
    """
    MFA code verification request schema

    Aligned with OpenAPI spec: #/components/schemas/MFAVerifyRequest
    """

    code: str = Field(..., min_length=6, max_length=6, description="6-digit TOTP code")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Validate that code is exactly 6 digits"""
        if not re.match(r"^\d{6}$", v):
            raise ValueError("Code must be exactly 6 digits")
        return v

    class Config:
        json_schema_extra = {"example": {"code": "123456"}}


class MFADisableRequestSchema(BaseModel):
    """
    MFA disable request schema

    Aligned with OpenAPI spec: #/components/schemas/MFADisableRequest
    """

    password: str = Field(
        ..., min_length=1, description="User password for confirmation"
    )

    class Config:
        json_schema_extra = {"example": {"password": "admin123"}}
