# FILE: backend/src/models/refresh_token.py | PURPOSE: Refresh token model
# for JWT token rotation (P0.2) | OWNER: security | RELATED:
# backend/src/auth.py,backend/src/routes/user.py | LAST-AUDITED:
# 2025-11-04

"""
Refresh Token Model
Stores refresh tokens for JWT token rotation with revocation support

P0.2: JWT token rotation with 15min access + 7d refresh
"""

from datetime import datetime, timezone
from sqlalchemy import Index
from database import db


class RefreshToken(db.Model):
    """
    Refresh Token Model

    Stores refresh tokens with:
    - jti (JWT ID) for unique identification
    - User association
    - Expiration tracking
    - Revocation support
    - Device/IP tracking for security
    """

    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    # JWT ID (unique identifier for this token)
    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)

    # User association
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Token metadata
    token_hash = db.Column(db.String(128), nullable=False)  # SHA-256 hash of the token

    # Expiration
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)

    # Revocation
    is_revoked = db.Column(db.Boolean, default=False, nullable=False, index=True)
    revoked_at = db.Column(db.DateTime(timezone=True), nullable=True)
    revocation_reason = db.Column(db.String(255), nullable=True)

    # Security tracking
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 max length
    user_agent = db.Column(db.String(512), nullable=True)
    device_fingerprint = db.Column(db.String(128), nullable=True)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_used_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user = db.relationship(
        "src.models.user.User",
        backref=db.backref(
            "refresh_tokens", lazy="dynamic", cascade="all, delete-orphan"
        ),
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_refresh_token_user_active", "user_id", "is_revoked", "expires_at"),
        Index("idx_refresh_token_jti_active", "jti", "is_revoked"),
    )

    def __repr__(self):
        return f"<RefreshToken {self.jti} for User {self.user_id}>"

    def is_valid(self):
        """
        Check if token is valid (not expired and not revoked)

        Returns:
            bool: True if token is valid
        """
        now = datetime.now(timezone.utc)
        return not self.is_revoked and self.expires_at > now

    def revoke(self, reason=None):
        """
        Revoke this refresh token

        Args:
            reason: Optional reason for revocation
        """
        self.is_revoked = True
        self.revoked_at = datetime.now(timezone.utc)
        self.revocation_reason = reason

    def update_last_used(self):
        """Update last used timestamp"""
        self.last_used_at = datetime.now(timezone.utc)

    @classmethod
    def create_token(
        cls,
        user_id,
        jti,
        token_hash,
        expires_at,
        ip_address=None,
        user_agent=None,
        device_fingerprint=None,
    ):
        """
        Create a new refresh token

        Args:
            user_id: User ID
            jti: JWT ID (unique identifier)
            token_hash: SHA-256 hash of the token
            expires_at: Expiration datetime
            ip_address: Client IP address
            user_agent: Client user agent
            device_fingerprint: Device fingerprint

        Returns:
            RefreshToken: Created token instance
        """
        token = cls(
            jti=jti,
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
            device_fingerprint=device_fingerprint,
        )
        db.session.add(token)
        return token

    @classmethod
    def find_by_jti(cls, jti):
        """
        Find token by JTI

        Args:
            jti: JWT ID

        Returns:
            RefreshToken or None
        """
        return cls.query.filter_by(jti=jti).first()

    @classmethod
    def revoke_all_for_user(cls, user_id, reason=None):
        """
        Revoke all refresh tokens for a user

        Args:
            user_id: User ID
            reason: Optional reason for revocation

        Returns:
            int: Number of tokens revoked
        """
        now = datetime.now(timezone.utc)
        count = cls.query.filter_by(user_id=user_id, is_revoked=False).update(
            {
                "is_revoked": True,
                "revoked_at": now,
                "revocation_reason": reason or "Revoked all tokens",
            }
        )
        return count

    @classmethod
    def cleanup_expired(cls):
        """
        Delete expired tokens (cleanup job)

        Returns:
            int: Number of tokens deleted
        """
        now = datetime.now(timezone.utc)
        count = cls.query.filter(cls.expires_at < now).delete()
        return count

    @classmethod
    def cleanup_revoked(cls, days=30):
        """
        Delete old revoked tokens (cleanup job)

        Args:
            days: Delete revoked tokens older than this many days

        Returns:
            int: Number of tokens deleted
        """
        from datetime import timedelta

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        count = (
            cls.query.filter_by(is_revoked=True)
            .filter(cls.revoked_at < cutoff)
            .delete()
        )
        return count

    @classmethod
    def get_active_tokens_for_user(cls, user_id):
        """
        Get all active (valid) tokens for a user

        Args:
            user_id: User ID

        Returns:
            list: List of active RefreshToken instances
        """
        now = datetime.now(timezone.utc)
        return (
            cls.query.filter_by(user_id=user_id, is_revoked=False)
            .filter(cls.expires_at > now)
            .order_by(cls.created_at.desc())
            .all()
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "jti": self.jti,
            "user_id": self.user_id,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_revoked": self.is_revoked,
            "revoked_at": self.revoked_at.isoformat() if self.revoked_at else None,
            "revocation_reason": self.revocation_reason,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_used_at": (
                self.last_used_at.isoformat() if self.last_used_at else None
            ),
            "is_valid": self.is_valid(),
        }
