"""
FILE: backend/src/modules/mfa/mfa_service.py | PURPOSE: Multi-Factor Authentication service | OWNER: Security Team | LAST-AUDITED: 2025-11-18

Multi-Factor Authentication (MFA) Service

Provides TOTP-based (Time-based One-Time Password) MFA functionality.
Supports Google Authenticator, Authy, and other TOTP apps.

Features:
- TOTP generation and validation
- QR code generation for easy setup
- Backup codes generation
- MFA enforcement policies

Version: 1.0.0
"""

import base64
import io
import secrets
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import pyotp
import qrcode


class MFAService:
    """
    Multi-Factor Authentication Service

    Handles TOTP-based MFA for user accounts.
    """

    def __init__(self, issuer_name: str = "Gaara AI"):
        """
        Initialize MFA service

        Args:
            issuer_name: Name of the application (shown in authenticator apps)
        """
        self.issuer_name = issuer_name

    def generate_secret(self) -> str:
        """
        Generate a new TOTP secret key

        Returns:
            str: Base32-encoded secret key
        """
        return pyotp.random_base32()

    def generate_qr_code(self, secret: str, user_email: str) -> str:
        """
        Generate QR code for TOTP setup

        Args:
            secret: TOTP secret key
            user_email: User's email address

        Returns:
            str: Base64-encoded QR code image
        """
        # Create TOTP URI
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(
            name=user_email,
            issuer_name=self.issuer_name
        )

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

    def verify_token(self, secret: str, token: str, window: int = 1) -> bool:
        """
        Verify TOTP token

        Args:
            secret: TOTP secret key
            token: 6-digit TOTP token from user
            window: Number of time windows to check (default: 1 = ±30 seconds)

        Returns:
            bool: True if token is valid, False otherwise
        """
        if not token or not secret:
            return False

        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=window)
        except Exception:
            return False

    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """
        Generate backup codes for account recovery

        Args:
            count: Number of backup codes to generate

        Returns:
            List[str]: List of backup codes
        """
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = secrets.token_hex(4).upper()
            # Format as XXXX-XXXX
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)

        return codes

    def get_current_token(self, secret: str) -> str:
        """
        Get current TOTP token (for testing/debugging only)

        Args:
            secret: TOTP secret key

        Returns:
            str: Current 6-digit TOTP token
        """
        totp = pyotp.TOTP(secret)
        return totp.now()

    def get_time_remaining(self) -> int:
        """
        Get seconds remaining until next TOTP token

        Returns:
            int: Seconds remaining
        """
        # Secret doesn't matter for time calculation
        return 30 - (int(datetime.now().timestamp()) % 30)


class MFAPolicy:
    """
    MFA Policy Enforcement

    Defines when MFA is required.
    """

    @staticmethod
    def is_mfa_required(
        user_role: str,
        action: str,
        ip_address: Optional[str] = None,
        last_mfa_time: Optional[datetime] = None
    ) -> bool:
        """
        Determine if MFA is required for an action

        Args:
            user_role: User's role (ADMIN, MANAGER, USER, GUEST)
            action: Action being performed
            ip_address: User's IP address
            last_mfa_time: Last time user completed MFA

        Returns:
            bool: True if MFA is required, False otherwise
        """
        # Always require MFA for admins
        if user_role == "ADMIN":
            return True

        # Require MFA for sensitive actions
        sensitive_actions = [
            "delete_user",
            "change_permissions",
            "export_data",
            "modify_settings",
            "access_admin_panel"
        ]
        if action in sensitive_actions:
            return True

        # Require MFA if last MFA was more than 1 hour ago
        if last_mfa_time:
            time_since_mfa = datetime.now() - last_mfa_time
            if time_since_mfa > timedelta(hours=1):
                return True

        # Require MFA for new IP addresses (optional - requires IP tracking)
        # This would need to be implemented with IP history tracking

        return False


# Convenience functions
def setup_mfa(user_email: str) -> Tuple[str, str, List[str]]:
    """
    Setup MFA for a user

    Args:
        user_email: User's email address

    Returns:
        Tuple[str, str, List[str]]: (secret, qr_code, backup_codes)
    """
    service = MFAService()
    secret = service.generate_secret()
    qr_code = service.generate_qr_code(secret, user_email)
    backup_codes = service.generate_backup_codes()

    return secret, qr_code, backup_codes


def verify_mfa_token(secret: str, token: str) -> bool:
    """
    Verify MFA token

    Args:
        secret: TOTP secret key
        token: 6-digit TOTP token

    Returns:
        bool: True if valid, False otherwise
    """
    service = MFAService()
    return service.verify_token(secret, token)
