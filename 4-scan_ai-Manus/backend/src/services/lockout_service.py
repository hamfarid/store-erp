"""
Account Lockout Service
========================

Purpose: Implement account lockout protection against brute force attacks.
This service tracks failed login attempts and locks accounts after
exceeding the maximum allowed attempts.

Security Features:
- Configurable max attempts (default: 5)
- Configurable lockout duration (default: 15 minutes)
- Automatic reset on successful login
- Audit logging for security events

Usage:
    from src.services.lockout_service import LockoutService
    
    # Check if account is locked
    if LockoutService.is_locked(user):
        raise HTTPException(status_code=423, detail="Account locked")
    
    # Record failed attempt
    is_now_locked = LockoutService.record_failed_attempt(db, user)
    
    # Reset on successful login
    LockoutService.reset_attempts(db, user)

Author: Global System v35.0
Date: 2026-01-17
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

# Configure logger
logger = logging.getLogger(__name__)


class LockoutConfig:
    """
    Configuration for account lockout policy.
    
    Attributes:
        MAX_ATTEMPTS: Maximum failed attempts before lockout
        LOCKOUT_DURATION: How long the account remains locked
        PROGRESSIVE_LOCKOUT: Enable increasing lockout duration
    """
    
    MAX_ATTEMPTS: int = 5
    LOCKOUT_DURATION: timedelta = timedelta(minutes=15)
    PROGRESSIVE_LOCKOUT: bool = True
    
    # Progressive lockout multipliers (attempts -> duration multiplier)
    LOCKOUT_MULTIPLIERS = {
        5: 1,    # 15 minutes
        10: 2,   # 30 minutes
        15: 4,   # 1 hour
        20: 8,   # 2 hours
    }


class LockoutService:
    """
    Service for managing account lockout due to failed login attempts.
    
    This service provides protection against brute force attacks by:
    1. Tracking failed login attempts per user
    2. Locking accounts after exceeding max attempts
    3. Automatically unlocking after lockout duration
    4. Resetting attempts on successful login
    
    All methods are static for easy use without instantiation.
    """
    
    @staticmethod
    def is_locked(user) -> bool:
        """
        Check if a user account is currently locked.
        
        Args:
            user: User model instance with locked_until field
            
        Returns:
            bool: True if account is locked, False otherwise
            
        Example:
            >>> if LockoutService.is_locked(user):
            ...     raise HTTPException(423, "Account locked")
        """
        if user is None:
            return False
            
        if not hasattr(user, 'locked_until') or user.locked_until is None:
            return False
            
        is_locked = datetime.utcnow() < user.locked_until
        
        if is_locked:
            remaining = user.locked_until - datetime.utcnow()
            logger.warning(
                f"Account locked: user_id={user.id}, "
                f"remaining={remaining.total_seconds():.0f}s"
            )
            
        return is_locked
    
    @staticmethod
    def get_lockout_remaining(user) -> Optional[int]:
        """
        Get remaining lockout time in seconds.
        
        Args:
            user: User model instance
            
        Returns:
            int or None: Seconds remaining, or None if not locked
        """
        if not LockoutService.is_locked(user):
            return None
            
        remaining = user.locked_until - datetime.utcnow()
        return max(0, int(remaining.total_seconds()))
    
    @staticmethod
    def record_failed_attempt(db: Session, user) -> bool:
        """
        Record a failed login attempt for a user.
        
        Increments the failed attempt counter and locks the account
        if max attempts is exceeded.
        
        Args:
            db: SQLAlchemy database session
            user: User model instance
            
        Returns:
            bool: True if account is now locked, False otherwise
            
        Example:
            >>> is_locked = LockoutService.record_failed_attempt(db, user)
            >>> if is_locked:
            ...     logger.warning(f"Account {user.email} has been locked")
        """
        if user is None:
            return False
            
        # Increment failed attempts
        if not hasattr(user, 'failed_login_attempts'):
            logger.error(f"User model missing failed_login_attempts field")
            return False
            
        user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
        
        logger.info(
            f"Failed login attempt: user_id={user.id}, "
            f"attempts={user.failed_login_attempts}/{LockoutConfig.MAX_ATTEMPTS}"
        )
        
        # Check if should lock
        if user.failed_login_attempts >= LockoutConfig.MAX_ATTEMPTS:
            # Calculate lockout duration (progressive if enabled)
            duration = LockoutService._calculate_lockout_duration(
                user.failed_login_attempts
            )
            
            user.locked_until = datetime.utcnow() + duration
            
            logger.warning(
                f"Account locked: user_id={user.id}, "
                f"duration={duration.total_seconds():.0f}s, "
                f"until={user.locked_until.isoformat()}"
            )
            
            db.commit()
            return True
        
        db.commit()
        return False
    
    @staticmethod
    def _calculate_lockout_duration(attempts: int) -> timedelta:
        """
        Calculate lockout duration based on number of attempts.
        
        Uses progressive lockout if enabled, where duration increases
        with more failed attempts.
        
        Args:
            attempts: Number of failed attempts
            
        Returns:
            timedelta: Lockout duration
        """
        if not LockoutConfig.PROGRESSIVE_LOCKOUT:
            return LockoutConfig.LOCKOUT_DURATION
        
        # Find the appropriate multiplier
        multiplier = 1
        for threshold, mult in sorted(LockoutConfig.LOCKOUT_MULTIPLIERS.items()):
            if attempts >= threshold:
                multiplier = mult
        
        return LockoutConfig.LOCKOUT_DURATION * multiplier
    
    @staticmethod
    def reset_attempts(db: Session, user) -> None:
        """
        Reset failed login attempts after successful login.
        
        This should be called after a successful authentication to
        clear the failed attempt counter and any lockout.
        
        Args:
            db: SQLAlchemy database session
            user: User model instance
            
        Example:
            >>> # After successful password verification
            >>> LockoutService.reset_attempts(db, user)
            >>> # User can now login normally
        """
        if user is None:
            return
            
        previous_attempts = getattr(user, 'failed_login_attempts', 0) or 0
        was_locked = LockoutService.is_locked(user)
        
        # Reset counters
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.utcnow()
        
        if previous_attempts > 0 or was_locked:
            logger.info(
                f"Login attempts reset: user_id={user.id}, "
                f"previous_attempts={previous_attempts}, "
                f"was_locked={was_locked}"
            )
        
        db.commit()
    
    @staticmethod
    def get_attempts_remaining(user) -> int:
        """
        Get number of login attempts remaining before lockout.
        
        Args:
            user: User model instance
            
        Returns:
            int: Number of attempts remaining (0 if locked)
        """
        if LockoutService.is_locked(user):
            return 0
            
        attempts = getattr(user, 'failed_login_attempts', 0) or 0
        return max(0, LockoutConfig.MAX_ATTEMPTS - attempts)
    
    @staticmethod
    def unlock_account(db: Session, user) -> bool:
        """
        Manually unlock a user account (admin function).
        
        This allows administrators to unlock accounts before the
        lockout duration expires.
        
        Args:
            db: SQLAlchemy database session
            user: User model instance
            
        Returns:
            bool: True if account was unlocked, False if wasn't locked
            
        Example:
            >>> # Admin unlocking a user
            >>> if LockoutService.unlock_account(db, user):
            ...     logger.info(f"Admin unlocked account {user.email}")
        """
        if user is None:
            return False
            
        was_locked = LockoutService.is_locked(user)
        
        user.failed_login_attempts = 0
        user.locked_until = None
        
        if was_locked:
            logger.info(
                f"Account manually unlocked: user_id={user.id}"
            )
        
        db.commit()
        return was_locked


# Convenience functions for simpler imports
is_account_locked = LockoutService.is_locked
record_failed_login = LockoutService.record_failed_attempt
reset_login_attempts = LockoutService.reset_attempts
unlock_account = LockoutService.unlock_account
