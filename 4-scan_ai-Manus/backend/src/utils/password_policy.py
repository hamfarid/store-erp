"""
FILE: backend/src/utils/password_policy.py | PURPOSE: Enhanced password security policies | OWNER: Security Team | LAST-AUDITED: 2025-11-18

Password Policy Module

Implements comprehensive password security policies:
- Complexity requirements
- Password strength validation
- Password history tracking
- Common password detection
- Password expiry
- Account lockout

Version: 1.0.0
"""

import re
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from passlib.context import CryptContext

# Password hashing context (bcrypt with cost factor 12)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12)


class PasswordPolicy:
    """
    Password Policy Enforcement

    Defines and enforces password security requirements.
    """

    # Minimum password length
    MIN_LENGTH = 12

    # Maximum password length
    MAX_LENGTH = 128

    # Password expiry (days)
    EXPIRY_DAYS = 90

    # Password history (number of previous passwords to check)
    HISTORY_COUNT = 5

    # Account lockout threshold (failed attempts)
    LOCKOUT_THRESHOLD = 5

    # Lockout duration (minutes)
    LOCKOUT_DURATION = 30

    # Common passwords (top 100 most common)
    COMMON_PASSWORDS = {
        "password", "123456", "123456789", "12345678", "12345", "1234567",
        "password1", "123123", "1234567890", "000000", "abc123", "qwerty",
        "admin", "letmein", "welcome", "monkey", "dragon", "master", "sunshine",
        "princess", "football", "shadow", "michael", "jennifer", "computer",
        # Add more common passwords as needed
    }

    @staticmethod
    def _normalize_for_common_password_check(password: str) -> str:
        # Remove separators/symbols so patterns like "Password123!" normalize to "password123"
        return re.sub(r"[^a-z0-9]", "", (password or "").lower())

    @staticmethod
    def _has_sequential_run(password: str, min_run: int = 4) -> bool:
        """Detect sequential runs like 1234 / abcd (length >= min_run).

        We intentionally ignore shorter sequences (e.g., "456") to reduce false
        positives while still catching obvious patterns like "123456".
        """
        s = (password or "").lower()
        if not s:
            return False

        def has_run(chars: str) -> bool:
            for i in range(0, len(chars) - min_run + 1):
                window = chars[i: i + min_run]
                if window in s:
                    return True
            return False

        digits = "0123456789"
        letters = "abcdefghijklmnopqrstuvwxyz"
        return has_run(digits) or has_run(letters)

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, List[str]]:
        """
        Validate password against policy requirements

        Args:
            password: Password to validate

        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []

        # Check length
        if len(password) < PasswordPolicy.MIN_LENGTH:
            errors.append(
                f"Password must be at least {PasswordPolicy.MIN_LENGTH} characters long")

        if len(password) > PasswordPolicy.MAX_LENGTH:
            errors.append(
                f"Password must not exceed {PasswordPolicy.MAX_LENGTH} characters")

        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append(
                "Password must contain at least one uppercase letter")

        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            errors.append(
                "Password must contain at least one lowercase letter")

        # Check for digit
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")

        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(
                "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)")

        # Check for common passwords (including common base words with digits/symbols)
        normalized = PasswordPolicy._normalize_for_common_password_check(password)
        if (
            normalized in PasswordPolicy.COMMON_PASSWORDS
            or any(normalized.startswith(common) for common in PasswordPolicy.COMMON_PASSWORDS)
        ):
            errors.append("Password is too common. Please choose a more unique password")

        # Check for sequential characters
        if PasswordPolicy._has_sequential_run(password, min_run=4):
            errors.append("Password should not contain sequential characters")

        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            errors.append(
                "Password should not contain more than 2 repeated characters")

        is_valid = len(errors) == 0
        return is_valid, errors

    @staticmethod
    def calculate_strength(password: str) -> Tuple[int, str]:
        """
        Calculate password strength score

        Args:
            password: Password to evaluate

        Returns:
            Tuple[int, str]: (score 0-100, strength_label)
        """
        score = 0

        # Length score (up to 30 points)
        length_score = min(len(password) * 2, 30)
        score += length_score

        # Character variety (up to 40 points)
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 10

        # Complexity bonus (up to 15 points)
        # No sequential characters
        if not PasswordPolicy._has_sequential_run(password, min_run=4):
            score += 5

        # No repeated characters
        if not re.search(r'(.)\1{2,}', password):
            score += 5

        # Not a common password
        normalized = PasswordPolicy._normalize_for_common_password_check(password)
        if (
            normalized not in PasswordPolicy.COMMON_PASSWORDS
            and not any(normalized.startswith(common) for common in PasswordPolicy.COMMON_PASSWORDS)
        ):
            score += 5

        # Determine strength label
        if score < 40:
            strength = "Weak"
        elif score < 60:
            strength = "Fair"
        elif score < 80:
            strength = "Good"
        else:
            strength = "Strong"

        return score, strength

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt

        Args:
            password: Plain text password

        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def check_password_history(
        new_password: str,
        password_history: List[str]
    ) -> bool:
        """
        Check if password was used before

        Args:
            new_password: New password to check
            password_history: List of previous password hashes

        Returns:
            bool: True if password is new, False if it was used before
        """
        for old_hash in password_history[-PasswordPolicy.HISTORY_COUNT:]:
            if pwd_context.verify(new_password, old_hash):
                return False
        return True

    @staticmethod
    def is_password_expired(last_changed: datetime) -> bool:
        """
        Check if password has expired

        Args:
            last_changed: Date when password was last changed

        Returns:
            bool: True if expired, False otherwise
        """
        expiry_date = last_changed + timedelta(days=PasswordPolicy.EXPIRY_DAYS)
        return datetime.now() > expiry_date

    @staticmethod
    def should_lockout_account(
            failed_attempts: int,
            last_attempt: Optional[datetime] = None) -> bool:
        """
        Determine if account should be locked out

        Args:
            failed_attempts: Number of failed login attempts
            last_attempt: Time of last failed attempt

        Returns:
            bool: True if account should be locked, False otherwise
        """
        if failed_attempts < PasswordPolicy.LOCKOUT_THRESHOLD:
            return False

        if last_attempt:
            lockout_end = last_attempt + \
                timedelta(minutes=PasswordPolicy.LOCKOUT_DURATION)
            if datetime.now() < lockout_end:
                return True

        return False


# Convenience functions
def validate_password(password: str) -> Tuple[bool, List[str]]:
    """Validate password"""
    return PasswordPolicy.validate_password(password)


def hash_password(password: str) -> str:
    """Hash password"""
    return PasswordPolicy.hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return PasswordPolicy.verify_password(plain_password, hashed_password)


def calculate_password_strength(password: str) -> Tuple[int, str]:
    """Calculate password strength"""
    return PasswordPolicy.calculate_strength(password)
