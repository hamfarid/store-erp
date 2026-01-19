"""
Two-Factor Authentication Service - Gaara Scan AI v4.3.1
Implements TOTP-based 2FA for enhanced security
"""

import base64
import io
import logging
from typing import Dict

import pyotp
import qrcode

logger = logging.getLogger(__name__)


class TwoFactorAuthService:
    """Two-Factor Authentication service using TOTP"""

    def __init__(self, issuer_name: str = "Gaara Scan AI"):
        """
        Initialize 2FA service

        Args:
            issuer_name: Name of the application
        """
        self.issuer_name = issuer_name

    def generate_secret(self) -> str:
        """
        Generate a new TOTP secret

        Returns:
            Base32 encoded secret
        """
        return pyotp.random_base32()

    def get_totp_uri(self, secret: str, username: str) -> str:
        """
        Generate TOTP provisioning URI

        Args:
            secret: TOTP secret
            username: User's username or email

        Returns:
            TOTP URI for QR code generation
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=username,
            issuer_name=self.issuer_name
        )

    def generate_qr_code(self, secret: str, username: str) -> str:
        """
        Generate QR code for 2FA setup

        Args:
            secret: TOTP secret
            username: User's username or email

        Returns:
            Base64 encoded QR code image
        """
        try:
            # Get provisioning URI
            uri = self.get_totp_uri(secret, username)

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(uri)
            qr.make(fit=True)

            # Create image
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()

            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            logger.error(f"Failed to generate QR code: {str(e)}")
            raise

    def verify_token(
        self,
        secret: str,
        token: str,
        window: int = 1
    ) -> bool:
        """
        Verify TOTP token

        Args:
            secret: TOTP secret
            token: 6-digit token from authenticator app
            window: Time window for verification (default: 1 = ±30 seconds)

        Returns:
            True if token is valid, False otherwise
        """
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=window)
        except Exception as e:
            logger.error(f"Failed to verify token: {str(e)}")
            return False

    def get_current_token(self, secret: str) -> str:
        """
        Get current TOTP token (for testing)

        Args:
            secret: TOTP secret

        Returns:
            Current 6-digit token
        """
        totp = pyotp.TOTP(secret)
        return totp.now()

    def setup_2fa(self, username: str) -> Dict:
        """
        Setup 2FA for a user

        Args:
            username: User's username or email

        Returns:
            Dictionary with secret and QR code
        """
        try:
            # Generate secret
            secret = self.generate_secret()

            # Generate QR code
            qr_code = self.generate_qr_code(secret, username)

            return {
                "success": True,
                "secret": secret,
                "qr_code": qr_code,
                "issuer": self.issuer_name,
                "username": username,
                "message": "2FA setup initiated. Scan QR code with your authenticator app."
            }

        except Exception as e:
            logger.error(f"Failed to setup 2FA: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to setup 2FA"
            }

    def verify_and_enable_2fa(
        self,
        secret: str,
        token: str
    ) -> Dict:
        """
        Verify token and enable 2FA

        Args:
            secret: TOTP secret
            token: Verification token

        Returns:
            Verification result
        """
        try:
            is_valid = self.verify_token(secret, token)

            if is_valid:
                return {
                    "success": True,
                    "message": "2FA enabled successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Invalid verification code"
                }

        except Exception as e:
            logger.error(f"Failed to verify and enable 2FA: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to enable 2FA"
            }

    def generate_backup_codes(self, count: int = 10) -> list:
        """
        Generate backup codes for 2FA

        Args:
            count: Number of backup codes to generate

        Returns:
            List of backup codes
        """
        import secrets
        import string

        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            # Format as XXXX-XXXX
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)

        return codes


# Global instance
two_factor_auth = TwoFactorAuthService()
