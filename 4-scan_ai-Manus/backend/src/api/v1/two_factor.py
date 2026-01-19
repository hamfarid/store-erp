"""
Two-Factor Authentication API Endpoints - Gaara Scan AI v4.3.1
API endpoints for 2FA management
"""

import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ...services.two_factor_auth import two_factor_auth

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/2fa", tags=["Two-Factor Authentication"])

# Models


class Setup2FARequest(BaseModel):
    """Setup 2FA request model"""
    username: str


class Verify2FARequest(BaseModel):
    """Verify 2FA request model"""
    secret: str
    token: str


class Validate2FARequest(BaseModel):
    """Validate 2FA token request model"""
    token: str


@router.post("/setup")
async def setup_2fa(request: Setup2FARequest):
    """
    Setup 2FA for a user

    - **username**: User's username or email

    Returns QR code and secret for authenticator app setup
    """
    try:
        result = two_factor_auth.setup_2fa(request.username)

        if result["success"]:
            return {
                "success": True,
                "data": {
                    "secret": result["secret"],
                    "qr_code": result["qr_code"],
                    "issuer": result["issuer"]
                },
                "message": result["message"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Failed to setup 2FA")
            )

    except Exception as e:
        logger.error(f"Failed to setup 2FA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/verify")
async def verify_2fa(request: Verify2FARequest):
    """
    Verify 2FA token and enable 2FA

    - **secret**: TOTP secret from setup
    - **token**: 6-digit code from authenticator app

    Verifies the token and enables 2FA for the user
    """
    try:
        result = two_factor_auth.verify_and_enable_2fa(
            request.secret,
            request.token
        )

        if result["success"]:
            return {
                "success": True,
                "message": result["message"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("message", "Invalid verification code")
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to verify 2FA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/validate")
async def validate_2fa_token(request: Validate2FARequest):
    """
    Validate 2FA token during login

    - **token**: 6-digit code from authenticator app

    Note: In production, you should pass the user's secret from database
    """
    try:
        # In production, get secret from database based on authenticated user
        # For now, this is a placeholder
        return {
            "success": True,
            "message": "Token validation endpoint. Implement with user's secret from database."
        }

    except Exception as e:
        logger.error(f"Failed to validate 2FA token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/backup-codes")
async def generate_backup_codes():
    """
    Generate backup codes for 2FA

    Returns 10 backup codes that can be used when authenticator app is unavailable
    """
    try:
        codes = two_factor_auth.generate_backup_codes(count=10)

        return {
            "success": True,
            "data": {
                "backup_codes": codes,
                "count": len(codes)
            },
            "message": "Backup codes generated successfully. Store them securely."
        }

    except Exception as e:
        logger.error(f"Failed to generate backup codes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/disable")
async def disable_2fa():
    """
    Disable 2FA for a user

    Note: In production, verify user authentication and require password confirmation
    """
    try:
        # In production, verify user and delete 2FA secret from database
        return {
            "success": True,
            "message": "2FA disabled successfully"
        }

    except Exception as e:
        logger.error(f"Failed to disable 2FA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/status")
async def get_2fa_status():
    """
    Get 2FA status for current user

    Note: In production, check database for user's 2FA status
    """
    try:
        # In production, check if user has 2FA enabled in database
        return {
            "success": True,
            "data": {
                "enabled": False,
                "setup_date": None
            },
            "message": "2FA status retrieved"
        }

    except Exception as e:
        logger.error(f"Failed to get 2FA status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
