"""
Two-Factor Authentication (2FA) Module

Implements TOTP (Time-based One-Time Password) authentication
using the pyotp library.

Features:
- Generate QR codes for authenticator apps
- Verify TOTP codes
- Backup codes generation
- Recovery codes

Author: Store ERP Team
Version: 2.0
Last Updated: 2025-12-13
"""

import pyotp
import qrcode
import io
import base64
import secrets
import hashlib
from datetime import datetime
from typing import Tuple, List, Optional
from src.utils.logger import info, warning, error, log_security_event


class TwoFactorAuth:
    """Two-Factor Authentication handler."""
    
    def __init__(self, issuer_name: str = "Store ERP"):
        """
        Initialize 2FA handler.
        
        Args:
            issuer_name: Name of the application (appears in authenticator app)
        """
        self.issuer_name = issuer_name
    
    def generate_secret(self) -> str:
        """
        Generate a new secret key for TOTP.
        
        Returns:
            Base32-encoded secret key
        """
        secret = pyotp.random_base32()
        info("Generated new 2FA secret", secret_length=len(secret))
        return secret
    
    def get_provisioning_uri(self, secret: str, username: str) -> str:
        """
        Generate provisioning URI for QR code.
        
        Args:
            secret: TOTP secret key
            username: User's username or email
            
        Returns:
            Provisioning URI string
        """
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(
            name=username,
            issuer_name=self.issuer_name
        )
        return uri
    
    def generate_qr_code(self, secret: str, username: str) -> str:
        """
        Generate QR code as base64-encoded image.
        
        Args:
            secret: TOTP secret key
            username: User's username or email
            
        Returns:
            Base64-encoded PNG image
        """
        try:
            # Get provisioning URI
            uri = self.get_provisioning_uri(secret, username)
            
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
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            info("Generated QR code for 2FA", username=username)
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            error(f"Failed to generate QR code: {str(e)}", username=username)
            raise
    
    def verify_code(self, secret: str, code: str, username: str = None) -> bool:
        """
        Verify TOTP code.
        
        Args:
            secret: TOTP secret key
            code: 6-digit code from authenticator app
            username: User's username (for logging)
            
        Returns:
            True if code is valid, False otherwise
        """
        try:
            totp = pyotp.TOTP(secret)
            is_valid = totp.verify(code, valid_window=1)  # Allow 1 time step before/after
            
            if is_valid:
                info("2FA code verified successfully", username=username)
                log_security_event(
                    event_type="2fa_success",
                    user_id=username,
                    details={"timestamp": datetime.utcnow().isoformat()}
                )
            else:
                warning("2FA code verification failed", username=username, code_length=len(code))
                log_security_event(
                    event_type="2fa_failed",
                    user_id=username,
                    details={"timestamp": datetime.utcnow().isoformat()}
                )
            
            return is_valid
            
        except Exception as e:
            error(f"Error verifying 2FA code: {str(e)}", username=username)
            return False
    
    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """
        Generate backup codes for account recovery.
        
        Args:
            count: Number of backup codes to generate
            
        Returns:
            List of backup codes
        """
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = secrets.token_hex(4).upper()
            # Format as XXXX-XXXX
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)
        
        info(f"Generated {count} backup codes")
        return codes
    
    def hash_backup_code(self, code: str) -> str:
        """
        Hash backup code for secure storage.
        
        Args:
            code: Backup code to hash
            
        Returns:
            SHA-256 hash of the code
        """
        return hashlib.sha256(code.encode()).hexdigest()
    
    def verify_backup_code(self, code: str, hashed_codes: List[str]) -> bool:
        """
        Verify backup code against list of hashed codes.
        
        Args:
            code: Backup code to verify
            hashed_codes: List of hashed backup codes
            
        Returns:
            True if code is valid, False otherwise
        """
        code_hash = self.hash_backup_code(code)
        return code_hash in hashed_codes
    
    def get_current_code(self, secret: str) -> str:
        """
        Get current TOTP code (for testing/debugging only).
        
        Args:
            secret: TOTP secret key
            
        Returns:
            Current 6-digit code
        """
        totp = pyotp.TOTP(secret)
        return totp.now()


class TwoFactorAuthManager:
    """Manager for user 2FA settings."""
    
    def __init__(self, db_session):
        """
        Initialize 2FA manager.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        self.tfa = TwoFactorAuth()
    
    def enable_2fa(self, user_id: int, username: str) -> Tuple[str, str, List[str]]:
        """
        Enable 2FA for a user.
        
        Args:
            user_id: User ID
            username: Username
            
        Returns:
            Tuple of (secret, qr_code_base64, backup_codes)
        """
        try:
            # Generate secret
            secret = self.tfa.generate_secret()
            
            # Generate QR code
            qr_code = self.tfa.generate_qr_code(secret, username)
            
            # Generate backup codes
            backup_codes = self.tfa.generate_backup_codes()
            
            # Hash backup codes for storage
            hashed_codes = [self.tfa.hash_backup_code(code) for code in backup_codes]
            
            # Update user in database
            from src.models.user import User
            user = self.db.query(User).filter_by(id=user_id).first()
            if user:
                user.two_factor_secret = secret
                user.two_factor_enabled = True
                user.two_factor_backup_codes = ','.join(hashed_codes)
                self.db.commit()
                
                info("2FA enabled for user", user_id=user_id, username=username)
                log_security_event(
                    event_type="2fa_enabled",
                    user_id=str(user_id),
                    details={"username": username}
                )
            
            return secret, qr_code, backup_codes
            
        except Exception as e:
            self.db.rollback()
            error(f"Failed to enable 2FA: {str(e)}", user_id=user_id)
            raise
    
    def disable_2fa(self, user_id: int, username: str) -> bool:
        """
        Disable 2FA for a user.
        
        Args:
            user_id: User ID
            username: Username
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from src.models.user import User
            user = self.db.query(User).filter_by(id=user_id).first()
            if user:
                user.two_factor_secret = None
                user.two_factor_enabled = False
                user.two_factor_backup_codes = None
                self.db.commit()
                
                info("2FA disabled for user", user_id=user_id, username=username)
                log_security_event(
                    event_type="2fa_disabled",
                    user_id=str(user_id),
                    details={"username": username}
                )
                return True
            return False
            
        except Exception as e:
            self.db.rollback()
            error(f"Failed to disable 2FA: {str(e)}", user_id=user_id)
            return False
    
    def verify_user_code(self, user_id: int, code: str) -> bool:
        """
        Verify 2FA code for a user.
        
        Args:
            user_id: User ID
            code: 6-digit TOTP code or backup code
            
        Returns:
            True if code is valid, False otherwise
        """
        try:
            from src.models.user import User
            user = self.db.query(User).filter_by(id=user_id).first()
            
            if not user or not user.two_factor_enabled:
                return False
            
            # Try TOTP code first
            if self.tfa.verify_code(user.two_factor_secret, code, user.username):
                return True
            
            # Try backup code
            if user.two_factor_backup_codes:
                hashed_codes = user.two_factor_backup_codes.split(',')
                if self.tfa.verify_backup_code(code, hashed_codes):
                    # Remove used backup code
                    code_hash = self.tfa.hash_backup_code(code)
                    hashed_codes.remove(code_hash)
                    user.two_factor_backup_codes = ','.join(hashed_codes)
                    self.db.commit()
                    
                    info("Backup code used", user_id=user_id)
                    log_security_event(
                        event_type="2fa_backup_code_used",
                        user_id=str(user_id),
                        details={"remaining_codes": len(hashed_codes)}
                    )
                    return True
            
            return False
            
        except Exception as e:
            error(f"Error verifying user 2FA code: {str(e)}", user_id=user_id)
            return False
    
    def regenerate_backup_codes(self, user_id: int, username: str) -> Optional[List[str]]:
        """
        Regenerate backup codes for a user.
        
        Args:
            user_id: User ID
            username: Username
            
        Returns:
            New backup codes or None if failed
        """
        try:
            from src.models.user import User
            user = self.db.query(User).filter_by(id=user_id).first()
            
            if not user or not user.two_factor_enabled:
                return None
            
            # Generate new backup codes
            backup_codes = self.tfa.generate_backup_codes()
            hashed_codes = [self.tfa.hash_backup_code(code) for code in backup_codes]
            
            # Update user
            user.two_factor_backup_codes = ','.join(hashed_codes)
            self.db.commit()
            
            info("Backup codes regenerated", user_id=user_id, username=username)
            log_security_event(
                event_type="2fa_backup_codes_regenerated",
                user_id=str(user_id),
                details={"username": username}
            )
            
            return backup_codes
            
        except Exception as e:
            self.db.rollback()
            error(f"Failed to regenerate backup codes: {str(e)}", user_id=user_id)
            return None


# Convenience functions
def enable_2fa_for_user(db_session, user_id: int, username: str) -> Tuple[str, str, List[str]]:
    """Enable 2FA for a user."""
    manager = TwoFactorAuthManager(db_session)
    return manager.enable_2fa(user_id, username)


def disable_2fa_for_user(db_session, user_id: int, username: str) -> bool:
    """Disable 2FA for a user."""
    manager = TwoFactorAuthManager(db_session)
    return manager.disable_2fa(user_id, username)


def verify_2fa_code(db_session, user_id: int, code: str) -> bool:
    """Verify 2FA code for a user."""
    manager = TwoFactorAuthManager(db_session)
    return manager.verify_user_code(user_id, code)


def regenerate_backup_codes(db_session, user_id: int, username: str) -> Optional[List[str]]:
    """Regenerate backup codes for a user."""
    manager = TwoFactorAuthManager(db_session)
    return manager.regenerate_backup_codes(user_id, username)
