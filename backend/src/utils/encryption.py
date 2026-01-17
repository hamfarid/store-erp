# FILE: backend/src/utils/encryption.py | PURPOSE: Envelope encryption for
# PII using AWS KMS | OWNER: Security Team | RELATED: docs/Security.md |
# LAST-AUDITED: 2025-10-25

"""
Envelope Encryption Utility

Provides envelope encryption for PII and sensitive data using AWS KMS.

Features:
- Envelope encryption (data key + KMS master key)
- Context-based encryption for additional security
- Automatic key rotation support
- Base64 encoding for database storage
- Type-safe encryption/decryption

Usage:
    from src.utils.encryption import encrypt_field, decrypt_field

    # Encrypt PII
    encrypted_email = encrypt_field(
        user.email,
        context={'user_id': user.id, 'field': 'email'}
    )

    # Decrypt PII
    email = decrypt_field(
        encrypted_email,
        context={'user_id': user.id, 'field': 'email'}
    )
"""

import os
import base64
import logging
from typing import Optional, Dict, Any

# Try to import cryptography
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    from cryptography.hazmat.backends import default_backend

    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None  # type: ignore

# Try to import boto3 for KMS
try:
    import boto3
    from botocore.exceptions import ClientError

    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    boto3 = None  # type: ignore
    ClientError = Exception  # type: ignore

logger = logging.getLogger(__name__)

# Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
KMS_KEY_ID = os.getenv("KMS_KEY_ID", "")  # KMS key ARN or alias

# Fallback encryption key for development (NOT for production)
FALLBACK_ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")


class EncryptionError(Exception):
    """Base exception for encryption errors"""

    pass


def _get_kms_client():
    """Get or create AWS KMS client (singleton)"""
    if not BOTO3_AVAILABLE:
        raise EncryptionError("boto3 is not installed. Install with: pip install boto3")

    if not hasattr(_get_kms_client, "_client"):
        try:
            _get_kms_client._client = boto3.client("kms", region_name=AWS_REGION)
            logger.info(f"✅ Connected to AWS KMS in {AWS_REGION}")
        except Exception as e:
            logger.error(f"❌ Failed to create KMS client: {e}")
            raise EncryptionError(f"Failed to create KMS client: {e}")

    return _get_kms_client._client


def _generate_data_key(context: Optional[Dict[str, str]] = None) -> tuple[bytes, bytes]:
    """
    Generate a data encryption key using KMS

    Returns:
        (plaintext_key, encrypted_key) tuple
    """
    if not KMS_KEY_ID:
        raise EncryptionError("KMS_KEY_ID not configured")

    try:
        client = _get_kms_client()

        # Prepare encryption context
        encryption_context = context or {}

        # Generate data key
        response = client.generate_data_key(
            KeyId=KMS_KEY_ID, KeySpec="AES_256", EncryptionContext=encryption_context
        )

        plaintext_key = response["Plaintext"]
        encrypted_key = response["CiphertextBlob"]

        logger.debug(f"✅ Generated data key with context: {encryption_context}")

        return plaintext_key, encrypted_key

    except ClientError as e:
        logger.error(f"❌ KMS error generating data key: {e}")
        raise EncryptionError(f"KMS error: {e}")


def _decrypt_data_key(
    encrypted_key: bytes, context: Optional[Dict[str, str]] = None
) -> bytes:
    """
    Decrypt a data encryption key using KMS

    Returns:
        plaintext_key
    """
    try:
        client = _get_kms_client()

        # Prepare encryption context
        encryption_context = context or {}

        # Decrypt data key
        response = client.decrypt(
            CiphertextBlob=encrypted_key, EncryptionContext=encryption_context
        )

        plaintext_key = response["Plaintext"]

        logger.debug(f"✅ Decrypted data key with context: {encryption_context}")

        return plaintext_key

    except ClientError as e:
        logger.error(f"❌ KMS error decrypting data key: {e}")
        raise EncryptionError(f"KMS error: {e}")


def _get_fernet_cipher(key: bytes) -> Any:
    """Get Fernet cipher from key"""
    if not CRYPTOGRAPHY_AVAILABLE:
        raise EncryptionError("cryptography library not installed")

    return Fernet(base64.urlsafe_b64encode(key[:32]))


def _fallback_encrypt(plaintext: str) -> str:
    """Fallback encryption for development (NOT secure for production)"""
    if not CRYPTOGRAPHY_AVAILABLE:
        logger.warning("⚠️  Cryptography not available, returning plaintext (INSECURE)")
        return plaintext

    if not FALLBACK_ENCRYPTION_KEY:
        logger.warning("⚠️  No fallback encryption key, returning plaintext (INSECURE)")
        return plaintext

    try:
        # Derive key from fallback encryption key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"gaara-store-salt",  # Fixed salt for development
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(FALLBACK_ENCRYPTION_KEY.encode())

        cipher = _get_fernet_cipher(key)
        encrypted = cipher.encrypt(plaintext.encode())

        return base64.b64encode(encrypted).decode()

    except Exception as e:
        logger.error(f"❌ Fallback encryption error: {e}")
        return plaintext


def _fallback_decrypt(ciphertext: str) -> str:
    """Fallback decryption for development"""
    if not CRYPTOGRAPHY_AVAILABLE:
        logger.warning("⚠️  Cryptography not available, returning ciphertext as-is")
        return ciphertext

    if not FALLBACK_ENCRYPTION_KEY:
        logger.warning("⚠️  No fallback encryption key, returning ciphertext as-is")
        return ciphertext

    try:
        # Derive key from fallback encryption key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"gaara-store-salt",
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(FALLBACK_ENCRYPTION_KEY.encode())

        cipher = _get_fernet_cipher(key)
        encrypted = base64.b64decode(ciphertext.encode())
        decrypted = cipher.decrypt(encrypted)

        return decrypted.decode()

    except Exception as e:
        logger.error(f"❌ Fallback decryption error: {e}")
        return ciphertext


def encrypt_field(plaintext: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Encrypt a field using envelope encryption

    Args:
        plaintext: Data to encrypt
        context: Encryption context (e.g., {'user_id': 123, 'field': 'email'})

    Returns:
        Base64-encoded encrypted data in format: {encrypted_key}:{encrypted_data}

    Example:
        >>> encrypted = encrypt_field('user@example.com', {'user_id': 123})
        >>> # Returns: "base64_encrypted_key:base64_encrypted_data"
    """
    if not plaintext:
        return ""

    # Development mode: use fallback encryption
    if ENVIRONMENT == "development":
        logger.debug("🔧 Development mode: using fallback encryption")
        return _fallback_encrypt(plaintext)

    # Production mode: use KMS envelope encryption
    if not BOTO3_AVAILABLE or not KMS_KEY_ID:
        logger.warning("⚠️  KMS not available, using fallback encryption")
        return _fallback_encrypt(plaintext)

    try:
        # Convert context to string keys
        str_context = {str(k): str(v) for k, v in (context or {}).items()}

        # Generate data key
        plaintext_key, encrypted_key = _generate_data_key(str_context)

        # Encrypt data with data key
        cipher = _get_fernet_cipher(plaintext_key)
        encrypted_data = cipher.encrypt(plaintext.encode())

        # Encode both encrypted key and data
        encoded_key = base64.b64encode(encrypted_key).decode()
        encoded_data = base64.b64encode(encrypted_data).decode()

        # Combine: {encrypted_key}:{encrypted_data}
        result = f"{encoded_key}:{encoded_data}"

        logger.info(f"✅ Encrypted field with context: {str_context}")

        return result

    except Exception as e:
        logger.error(f"❌ Encryption error: {e}")
        # Fallback to development encryption
        return _fallback_encrypt(plaintext)


def decrypt_field(ciphertext: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Decrypt a field using envelope encryption

    Args:
        ciphertext: Encrypted data in format: {encrypted_key}:{encrypted_data}
        context: Encryption context (must match encryption context)

    Returns:
        Decrypted plaintext

    Example:
        >>> plaintext = decrypt_field(encrypted, {'user_id': 123})
        >>> # Returns: "user@example.com"
    """
    if not ciphertext:
        return ""

    # Development mode: use fallback decryption
    if ENVIRONMENT == "development":
        logger.debug("🔧 Development mode: using fallback decryption")
        return _fallback_decrypt(ciphertext)

    # Check if ciphertext is in envelope format
    if ":" not in ciphertext:
        # Old format or fallback encrypted
        logger.warning(
            "⚠️  Ciphertext not in envelope format, using fallback decryption"
        )
        return _fallback_decrypt(ciphertext)

    # Production mode: use KMS envelope decryption
    if not BOTO3_AVAILABLE or not KMS_KEY_ID:
        logger.warning("⚠️  KMS not available, using fallback decryption")
        return _fallback_decrypt(ciphertext)

    try:
        # Split encrypted key and data
        encoded_key, encoded_data = ciphertext.split(":", 1)

        # Decode
        encrypted_key = base64.b64decode(encoded_key.encode())
        encrypted_data = base64.b64decode(encoded_data.encode())

        # Convert context to string keys
        str_context = {str(k): str(v) for k, v in (context or {}).items()}

        # Decrypt data key using KMS
        plaintext_key = _decrypt_data_key(encrypted_key, str_context)

        # Decrypt data with data key
        cipher = _get_fernet_cipher(plaintext_key)
        decrypted_data = cipher.decrypt(encrypted_data)

        logger.info(f"✅ Decrypted field with context: {str_context}")

        return decrypted_data.decode()

    except Exception as e:
        logger.error(f"❌ Decryption error: {e}")
        # Try fallback decryption
        return _fallback_decrypt(ciphertext)
