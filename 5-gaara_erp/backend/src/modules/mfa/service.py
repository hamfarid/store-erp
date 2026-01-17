# -*- coding: utf-8 -*-
"""
خدمة المصادقة الثنائية
MFA Service

منطق الأعمال للمصادقة الثنائية
Business logic for Multi-Factor Authentication
"""

from typing import List, Optional, Tuple
from datetime import datetime
import qrcode
import io
import base64
import logging

from .models import MFADevice, MFABackupCode

try:
    from src.database import db
except ImportError:
    db = None

logger = logging.getLogger(__name__)


class MFAService:
    """
    خدمة إدارة المصادقة الثنائية
    MFA Management Service
    """
    
    BACKUP_CODES_COUNT = 10
    
    @classmethod
    def setup_mfa(cls, user_id: int, device_name: str = 'Primary Device') -> Tuple[MFADevice, str]:
        """
        Setup MFA for a user.
        
        Args:
            user_id: User ID
            device_name: Name for the device
            
        Returns:
            Tuple of (MFADevice, qr_code_base64)
        """
        # Check if user already has active MFA
        existing = MFADevice.query.filter_by(
            user_id=user_id,
            is_active=True,
            is_verified=True
        ).first()
        
        if existing:
            raise ValueError("MFA already configured for this user")
        
        # Create new device
        device = MFADevice(user_id=user_id, name=device_name)
        db.session.add(device)
        db.session.flush()  # Get ID before commit
        
        logger.info(f"MFA device created for user {user_id}")
        
        return device, None  # QR generated in route with email
    
    @classmethod
    def generate_qr_code(cls, device: MFADevice, email: str) -> str:
        """
        Generate QR code for authenticator app.
        
        Args:
            device: MFADevice object
            email: User's email
            
        Returns:
            Base64 encoded PNG image
        """
        uri = device.get_provisioning_uri(email)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    @classmethod
    def verify_and_activate(cls, device_id: int, user_id: int, token: str) -> bool:
        """
        Verify TOTP token and activate MFA device.
        
        Args:
            device_id: MFA device ID
            user_id: User ID (for security check)
            token: 6-digit TOTP code
            
        Returns:
            True if verification successful
        """
        device = MFADevice.query.filter_by(
            id=device_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not device:
            raise ValueError("MFA device not found")
        
        if device.is_verified:
            raise ValueError("Device already verified")
        
        if device.verify_token(token):
            device.is_verified = True
            device.verified_at = datetime.utcnow()
            db.session.commit()
            
            # Generate backup codes
            cls._generate_backup_codes(user_id)
            
            logger.info(f"MFA activated for user {user_id}")
            return True
        
        db.session.commit()  # Save failed attempt count
        return False
    
    @classmethod
    def verify_token(cls, user_id: int, token: str) -> bool:
        """
        Verify TOTP token for login.
        
        Args:
            user_id: User ID
            token: 6-digit TOTP code
            
        Returns:
            True if token valid
        """
        device = MFADevice.query.filter_by(
            user_id=user_id,
            is_active=True,
            is_verified=True
        ).first()
        
        if not device:
            return False
        
        result = device.verify_token(token)
        db.session.commit()  # Save last_used_at and failed_attempts
        
        return result
    
    @classmethod
    def verify_backup_code(cls, user_id: int, code: str) -> bool:
        """
        Verify and consume a backup code.
        
        Args:
            user_id: User ID
            code: 8-character backup code
            
        Returns:
            True if code valid and consumed
        """
        backup_codes = MFABackupCode.query.filter_by(
            user_id=user_id,
            is_used=False
        ).all()
        
        for backup in backup_codes:
            if backup.verify(code):
                backup.mark_used()
                db.session.commit()
                
                logger.info(f"Backup code used for user {user_id}")
                return True
        
        return False
    
    @classmethod
    def disable_mfa(cls, user_id: int, token: str) -> bool:
        """
        Disable MFA for user.
        
        Args:
            user_id: User ID
            token: TOTP token for verification
            
        Returns:
            True if disabled successfully
        """
        # Verify token first
        if not cls.verify_token(user_id, token):
            return False
        
        # Deactivate all devices
        devices = MFADevice.query.filter_by(
            user_id=user_id,
            is_active=True
        ).all()
        
        for device in devices:
            device.is_active = False
        
        # Invalidate all backup codes
        backup_codes = MFABackupCode.query.filter_by(
            user_id=user_id,
            is_used=False
        ).all()
        
        for code in backup_codes:
            code.is_used = True
        
        db.session.commit()
        
        logger.info(f"MFA disabled for user {user_id}")
        return True
    
    @classmethod
    def is_mfa_enabled(cls, user_id: int) -> bool:
        """Check if user has MFA enabled."""
        return MFADevice.query.filter_by(
            user_id=user_id,
            is_active=True,
            is_verified=True
        ).first() is not None
    
    @classmethod
    def get_user_devices(cls, user_id: int) -> List[MFADevice]:
        """Get all MFA devices for user."""
        return MFADevice.query.filter_by(
            user_id=user_id,
            is_active=True
        ).all()
    
    @classmethod
    def get_backup_codes_count(cls, user_id: int) -> int:
        """Get count of remaining backup codes."""
        return MFABackupCode.query.filter_by(
            user_id=user_id,
            is_used=False
        ).count()
    
    @classmethod
    def regenerate_backup_codes(cls, user_id: int, token: str) -> Optional[List[str]]:
        """
        Regenerate backup codes (invalidates old ones).
        
        Args:
            user_id: User ID
            token: TOTP token for verification
            
        Returns:
            List of new backup codes (plain text, only shown once)
        """
        if not cls.verify_token(user_id, token):
            return None
        
        # Invalidate existing codes
        existing = MFABackupCode.query.filter_by(
            user_id=user_id,
            is_used=False
        ).all()
        
        for code in existing:
            code.is_used = True
        
        # Generate new codes
        return cls._generate_backup_codes(user_id)
    
    @classmethod
    def _generate_backup_codes(cls, user_id: int) -> List[str]:
        """
        Generate new backup codes.
        
        Returns:
            List of plain text codes (only shown once!)
        """
        codes = []
        
        for _ in range(cls.BACKUP_CODES_COUNT):
            plain_code = MFABackupCode.generate_code()
            codes.append(plain_code)
            
            backup = MFABackupCode(
                user_id=user_id,
                code_hash=MFABackupCode.hash_code(plain_code)
            )
            db.session.add(backup)
        
        db.session.commit()
        
        logger.info(f"Generated {cls.BACKUP_CODES_COUNT} backup codes for user {user_id}")
        
        return codes


__all__ = ['MFAService']
