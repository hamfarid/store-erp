# FILE: backend/src/password_hasher.py | PURPOSE: Secure password hashing
# with Argon2id (OWASP recommended) | OWNER: security | RELATED:
# backend/src/auth.py,backend/src/encryption_manager.py | LAST-AUDITED:
# 2025-11-04

"""
Secure Password Hashing Module
Uses Argon2id (OWASP recommended) with fallback to bcrypt for legacy support
"""

from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Try to import Argon2id (preferred)
try:
    from argon2 import PasswordHasher
    from argon2.exceptions import (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError,
    )

    ARGON2_AVAILABLE = True
    logger.info("✅ Argon2id available (OWASP recommended)")
except ImportError:
    ARGON2_AVAILABLE = False
    PasswordHasher = None
    VerifyMismatchError = None
    VerificationError = None
    InvalidHashError = None
    logger.warning("⚠️ argon2-cffi not available, falling back to bcrypt")

# Try to import bcrypt (legacy fallback)
try:
    import bcrypt

    BCRYPT_AVAILABLE = True
    logger.info("✅ bcrypt available (legacy support)")
except ImportError:
    BCRYPT_AVAILABLE = False
    bcrypt = None
    logger.warning("⚠️ bcrypt not available")


class SecurePasswordHasher:
    """
    Secure password hasher using Argon2id (OWASP recommended)

    Argon2id parameters (OWASP recommendations 2024):
    - time_cost: 2 iterations (minimum)
    - memory_cost: 19456 KiB (~19 MB) for interactive systems
    - parallelism: 1 thread (can be increased for server-side)
    - hash_len: 32 bytes
    - salt_len: 16 bytes

    Fallback to bcrypt for legacy password verification.
    """

    def __init__(self):
        if ARGON2_AVAILABLE:
            # OWASP recommended parameters for interactive systems
            self.ph = PasswordHasher(
                time_cost=2,  # iterations
                memory_cost=19456,  # 19 MB
                parallelism=1,  # threads
                hash_len=32,  # output length
                salt_len=16,  # salt length
            )
            self.algorithm = "argon2id"
        else:
            self.ph = None
            self.algorithm = "bcrypt" if BCRYPT_AVAILABLE else "sha256"

    def hash_password(self, password: str) -> Optional[str]:
        """
        Hash a password using Argon2id (preferred) or bcrypt (fallback)

        Args:
            password: Plain text password

        Returns:
            Hashed password string or None on error
        """
        if not password:
            logger.error("Cannot hash empty password")
            return None

        try:
            if ARGON2_AVAILABLE and self.ph:
                # Argon2id hashing (OWASP recommended)
                hashed = self.ph.hash(password)
                logger.debug("Password hashed with Argon2id")
                return hashed

            elif BCRYPT_AVAILABLE and bcrypt:
                # Bcrypt fallback (legacy)
                salt = bcrypt.gensalt(rounds=12)
                hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
                logger.warning(
                    "Password hashed with bcrypt (legacy) - consider upgrading to Argon2id"
                )
                return hashed.decode("utf-8")

            else:
                # SHA-256 fallback (INSECURE - development only)
                import hashlib

                hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
                logger.error(
                    "⚠️ INSECURE: Password hashed with SHA-256 (development only)"
                )
                return hashed

        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            return None

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against a hash

        Supports:
        - Argon2id hashes (current)
        - bcrypt hashes (legacy)
        - SHA-256 hashes (insecure fallback)

        Args:
            password: Plain text password
            hashed: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        if not password or not hashed:
            logger.error("Cannot verify empty password or hash")
            return False

        try:
            # Try Argon2id first (current standard)
            if ARGON2_AVAILABLE and self.ph and hashed.startswith("$argon2"):
                try:
                    self.ph.verify(hashed, password)

                    # Check if rehashing is needed (parameters changed)
                    if self.ph.check_needs_rehash(hashed):
                        logger.info(
                            "Password hash needs rehashing with updated parameters"
                        )

                    return True
                except Exception as e:
                    if type(e).__name__ in (
                        "VerifyMismatchError",
                        "VerificationError",
                        "InvalidHashError",
                    ):
                        return False
                    raise

            # Try bcrypt (legacy)
            elif (
                BCRYPT_AVAILABLE
                and bcrypt
                and (
                    hashed.startswith("$2a$")
                    or hashed.startswith("$2b$")
                    or hashed.startswith("$2y$")
                )
            ):
                try:
                    result = bcrypt.checkpw(
                        password.encode("utf-8"), hashed.encode("utf-8")
                    )
                    if result:
                        logger.info(
                            "Password verified with bcrypt (legacy) - consider rehashing with Argon2id"
                        )
                    return result
                except Exception as e:
                    logger.error(f"bcrypt verification failed: {e}")
                    return False

            # Try SHA-256 (insecure fallback)
            else:
                import hashlib

                computed = hashlib.sha256(password.encode("utf-8")).hexdigest()
                result = computed == hashed
                if result:
                    logger.warning(
                        "⚠️ INSECURE: Password verified with SHA-256 - MUST rehash with Argon2id"
                    )
                return result

        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False

    def needs_rehash(self, hashed: str) -> bool:
        """
        Check if a password hash needs to be rehashed

        Returns True if:
        - Hash is not Argon2id
        - Hash uses outdated Argon2id parameters

        Args:
            hashed: Hashed password

        Returns:
            True if rehashing is recommended
        """
        if not hashed:
            return False

        # Not Argon2id - needs rehash
        if not hashed.startswith("$argon2"):
            return True

        # Check Argon2id parameters
        if ARGON2_AVAILABLE and self.ph:
            try:
                return self.ph.check_needs_rehash(hashed)
            except Exception:
                return True

        return False

    def get_algorithm(self) -> str:
        """Get the current hashing algorithm"""
        return self.algorithm


# Global instance
_hasher = SecurePasswordHasher()


def hash_password(password: str) -> Optional[str]:
    """
    Hash a password using Argon2id (preferred) or bcrypt (fallback)

    Args:
        password: Plain text password

    Returns:
        Hashed password string or None on error
    """
    return _hasher.hash_password(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a hash

    Args:
        password: Plain text password
        hashed: Hashed password

    Returns:
        True if password matches, False otherwise
    """
    return _hasher.verify_password(password, hashed)


def needs_rehash(hashed: str) -> bool:
    """
    Check if a password hash needs to be rehashed

    Args:
        hashed: Hashed password

    Returns:
        True if rehashing is recommended
    """
    return _hasher.needs_rehash(hashed)


def get_algorithm() -> str:
    """Get the current hashing algorithm"""
    return _hasher.get_algorithm()


# Example usage and tests
if __name__ == "__main__":
    import sys

    # Test password hashing
    test_password = "SecureP@ssw0rd123"

    print(f"Current algorithm: {get_algorithm()}")
    print(f"Argon2id available: {ARGON2_AVAILABLE}")
    print(f"bcrypt available: {BCRYPT_AVAILABLE}")
    print()

    # Hash password
    hashed = hash_password(test_password)
    if hashed:
        print("✅ Password hashed successfully")
        print(f"Hash: {hashed[:50]}...")
        print(f"Needs rehash: {needs_rehash(hashed)}")
        print()

        # Verify correct password
        if verify_password(test_password, hashed):
            print("✅ Correct password verified")
        else:
            print("❌ Correct password verification failed")

        # Verify incorrect password
        if not verify_password("WrongPassword", hashed):
            print("✅ Incorrect password rejected")
        else:
            print("❌ Incorrect password accepted (SECURITY ISSUE)")
    else:
        print("❌ Password hashing failed")
        sys.exit(1)
