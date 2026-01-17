# -*- coding: utf-8 -*-
"""
نماذج المصادقة الثنائية
MFA Models

تخزين أجهزة المصادقة ورموز النسخ الاحتياطي
Stores authentication devices and backup codes
"""

from datetime import datetime
import pyotp
import secrets

try:
    from src.database import db
except ImportError:
    # Fallback for testing
    class MockDB:
        @staticmethod
        def Column(*args, **kwargs):
            return None

        Integer = int
        String = str
        Boolean = bool
        DateTime = datetime

        @staticmethod
        def ForeignKey(x):
            return x

        @staticmethod
        def relationship(*args, **kwargs):
            return None

        Model = object

    db = MockDB()


class MFADevice(db.Model):
    """
    جهاز المصادقة الثنائية
    MFA Device - Stores TOTP secrets for each user
    
    Each user can have multiple MFA devices (e.g., phone, hardware token)
    """
    
    __tablename__ = 'mfa_devices'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Device identification
    name = db.Column(db.String(100), default='Primary Device')
    device_type = db.Column(db.String(20), default='totp')  # totp, hardware
    
    # TOTP Secret (encrypted in production)
    secret = db.Column(db.String(32), nullable=False)
    
    # Status
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime, nullable=True)
    last_used_at = db.Column(db.DateTime, nullable=True)
    
    # Security
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, user_id: int, name: str = 'Primary Device'):
        self.user_id = user_id
        self.name = name
        self.secret = pyotp.random_base32()
    
    def __repr__(self):
        return f'<MFADevice {self.id}: user={self.user_id}, verified={self.is_verified}>'
    
    def get_totp(self) -> pyotp.TOTP:
        """Get TOTP object for this device."""
        return pyotp.TOTP(self.secret)
    
    def verify_token(self, token: str) -> bool:
        """
        Verify a TOTP token.
        
        Args:
            token: 6-digit TOTP code
            
        Returns:
            True if token is valid
        """
        if self.is_locked():
            return False
        
        totp = self.get_totp()
        is_valid = totp.verify(token, valid_window=1)  # Allow 30s window
        
        if is_valid:
            self.failed_attempts = 0
            self.last_used_at = datetime.utcnow()
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 5:
                from datetime import timedelta
                self.locked_until = datetime.utcnow() + timedelta(minutes=15)
        
        return is_valid
    
    def is_locked(self) -> bool:
        """Check if device is locked due to failed attempts."""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    def get_provisioning_uri(self, email: str, issuer: str = 'Gaara ERP') -> str:
        """
        Get provisioning URI for QR code.
        
        Args:
            email: User's email address
            issuer: Application name
            
        Returns:
            otpauth:// URI for authenticator apps
        """
        totp = self.get_totp()
        return totp.provisioning_uri(name=email, issuer_name=issuer)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary (excludes secret)."""
        return {
            'id': self.id,
            'name': self.name,
            'device_type': self.device_type,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
        }


class MFABackupCode(db.Model):
    """
    رموز النسخ الاحتياطي
    MFA Backup Codes - One-time use codes for account recovery
    
    Each user gets 10 backup codes when enabling MFA
    """
    
    __tablename__ = 'mfa_backup_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Hashed code (never store plain text)
    code_hash = db.Column(db.String(128), nullable=False)
    
    # Status
    is_used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def generate_code() -> str:
        """Generate a random 8-character backup code."""
        return secrets.token_hex(4).upper()
    
    @staticmethod
    def hash_code(code: str) -> str:
        """Hash a backup code for storage."""
        import hashlib
        return hashlib.sha256(code.encode()).hexdigest()
    
    def verify(self, code: str) -> bool:
        """
        Verify a backup code.
        
        Args:
            code: Plain text backup code
            
        Returns:
            True if code is valid and not yet used
        """
        if self.is_used:
            return False
        
        return self.code_hash == self.hash_code(code)
    
    def mark_used(self):
        """Mark this backup code as used."""
        self.is_used = True
        self.used_at = datetime.utcnow()


__all__ = ['MFADevice', 'MFABackupCode']
