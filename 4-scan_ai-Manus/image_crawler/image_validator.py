"""
Image Validator
================

Purpose: Validate and sanitize uploaded images before processing.
Prevents malicious file uploads and ensures image quality standards.

Security Features:
- File type validation (magic bytes)
- Size limits enforcement
- Metadata stripping
- Malware pattern detection
- Image dimension validation
- Content-type verification

Usage:
    from image_validator import ImageValidator
    
    validator = ImageValidator()
    is_valid, error = validator.validate(file_bytes, filename)

Author: Global System v35.0
Date: 2026-01-17
"""

import hashlib
import io
import logging
import struct
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Tuple, Union

# Configure logger
logger = logging.getLogger(__name__)


# ============================================
# Magic Bytes Signatures
# ============================================

MAGIC_SIGNATURES = {
    'jpeg': [
        b'\xff\xd8\xff\xe0',  # JFIF
        b'\xff\xd8\xff\xe1',  # EXIF
        b'\xff\xd8\xff\xe2',  # ICC
        b'\xff\xd8\xff\xdb',  # Define quantization table
        b'\xff\xd8\xff\xee',  # Adobe
    ],
    'png': [
        b'\x89PNG\r\n\x1a\n',
    ],
    'gif': [
        b'GIF87a',
        b'GIF89a',
    ],
    'webp': [
        b'RIFF',  # First 4 bytes, followed by size, then WEBP
    ],
    'bmp': [
        b'BM',
    ],
    'tiff': [
        b'II*\x00',  # Little-endian
        b'MM\x00*',  # Big-endian
    ],
}

# Known malicious patterns
MALICIOUS_PATTERNS = [
    b'<?php',
    b'<script',
    b'javascript:',
    b'eval(',
    b'base64_decode',
    b'system(',
    b'exec(',
    b'shell_exec',
    b'passthru(',
    b'<% ',
    b'<%=',
    b'<%@',
]


class ImageValidatorConfig:
    """
    Configuration for image validation.
    
    Attributes:
        MAX_FILE_SIZE: Maximum file size in bytes (default 10MB)
        MIN_FILE_SIZE: Minimum file size in bytes (default 1KB)
        MAX_DIMENSION: Maximum width/height in pixels
        MIN_DIMENSION: Minimum width/height in pixels
        ALLOWED_TYPES: List of allowed image types
        ALLOWED_EXTENSIONS: List of allowed file extensions
    """
    
    # Size limits
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    MIN_FILE_SIZE: int = 1024              # 1 KB
    
    # Dimension limits
    MAX_DIMENSION: int = 8192              # 8K resolution max
    MIN_DIMENSION: int = 32                # 32x32 minimum
    
    # Allowed types
    ALLOWED_TYPES: List[str] = ['jpeg', 'png', 'gif', 'webp']
    ALLOWED_EXTENSIONS: List[str] = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    # Content scanning
    SCAN_FOR_MALWARE: bool = True
    STRIP_METADATA: bool = True


class ValidationResult:
    """
    Result of image validation.
    
    Attributes:
        is_valid: Whether the image passed validation
        error: Error message if validation failed
        warnings: List of warnings (non-fatal issues)
        metadata: Extracted image metadata
    """
    
    def __init__(
        self,
        is_valid: bool = True,
        error: Optional[str] = None,
        warnings: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ):
        self.is_valid = is_valid
        self.error = error
        self.warnings = warnings or []
        self.metadata = metadata or {}
    
    def __bool__(self) -> bool:
        return self.is_valid
    
    def to_dict(self) -> Dict:
        return {
            "is_valid": self.is_valid,
            "error": self.error,
            "warnings": self.warnings,
            "metadata": self.metadata
        }


class ImageValidator:
    """
    Validator for uploaded images.
    
    Performs comprehensive validation including:
    - File type verification (magic bytes)
    - Size limit enforcement
    - Dimension validation
    - Malware pattern scanning
    - Extension verification
    
    Example:
        >>> validator = ImageValidator()
        >>> with open('plant.jpg', 'rb') as f:
        ...     result = validator.validate(f.read(), 'plant.jpg')
        >>> if result.is_valid:
        ...     print("Image is safe to process")
        ... else:
        ...     print(f"Validation failed: {result.error}")
    """
    
    def __init__(self, config: Optional[ImageValidatorConfig] = None):
        """
        Initialize validator with optional config.
        
        Args:
            config: Custom configuration, uses defaults if None
        """
        self.config = config or ImageValidatorConfig()
    
    def validate(
        self,
        data: Union[bytes, BinaryIO],
        filename: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate an image.
        
        Args:
            data: Image data as bytes or file-like object
            filename: Original filename (optional, used for extension check)
            
        Returns:
            ValidationResult: Validation result with details
        """
        warnings = []
        metadata = {}
        
        # Convert file-like to bytes
        if hasattr(data, 'read'):
            data = data.read()
        
        # 1. Check file size
        file_size = len(data)
        metadata['file_size'] = file_size
        
        if file_size < self.config.MIN_FILE_SIZE:
            return ValidationResult(
                is_valid=False,
                error=f"File too small: {file_size} bytes (minimum: {self.config.MIN_FILE_SIZE})"
            )
        
        if file_size > self.config.MAX_FILE_SIZE:
            return ValidationResult(
                is_valid=False,
                error=f"File too large: {file_size} bytes (maximum: {self.config.MAX_FILE_SIZE})"
            )
        
        # 2. Detect file type from magic bytes
        detected_type = self._detect_type(data)
        metadata['detected_type'] = detected_type
        
        if not detected_type:
            return ValidationResult(
                is_valid=False,
                error="Could not determine file type from magic bytes"
            )
        
        if detected_type not in self.config.ALLOWED_TYPES:
            return ValidationResult(
                is_valid=False,
                error=f"File type '{detected_type}' not allowed"
            )
        
        # 3. Check filename extension (if provided)
        if filename:
            ext = Path(filename).suffix.lower()
            metadata['extension'] = ext
            
            if ext not in self.config.ALLOWED_EXTENSIONS:
                return ValidationResult(
                    is_valid=False,
                    error=f"File extension '{ext}' not allowed"
                )
            
            # Check extension matches detected type
            expected_exts = self._get_expected_extensions(detected_type)
            if ext not in expected_exts:
                warnings.append(
                    f"Extension '{ext}' doesn't match detected type '{detected_type}'"
                )
        
        # 4. Scan for malicious content
        if self.config.SCAN_FOR_MALWARE:
            is_safe, malware_error = self._scan_for_malware(data)
            if not is_safe:
                logger.warning(f"[SECURITY] Malicious content detected: {malware_error}")
                return ValidationResult(
                    is_valid=False,
                    error=f"Malicious content detected: {malware_error}"
                )
        
        # 5. Validate image dimensions
        dimensions = self._get_dimensions(data, detected_type)
        if dimensions:
            width, height = dimensions
            metadata['width'] = width
            metadata['height'] = height
            
            if width < self.config.MIN_DIMENSION or height < self.config.MIN_DIMENSION:
                return ValidationResult(
                    is_valid=False,
                    error=f"Image too small: {width}x{height} (minimum: {self.config.MIN_DIMENSION}x{self.config.MIN_DIMENSION})"
                )
            
            if width > self.config.MAX_DIMENSION or height > self.config.MAX_DIMENSION:
                return ValidationResult(
                    is_valid=False,
                    error=f"Image too large: {width}x{height} (maximum: {self.config.MAX_DIMENSION}x{self.config.MAX_DIMENSION})"
                )
        else:
            warnings.append("Could not determine image dimensions")
        
        # 6. Calculate hash for deduplication
        metadata['sha256'] = hashlib.sha256(data).hexdigest()
        metadata['md5'] = hashlib.md5(data).hexdigest()
        
        logger.info(f"Image validated successfully: type={detected_type}, size={file_size}")
        
        return ValidationResult(
            is_valid=True,
            warnings=warnings,
            metadata=metadata
        )
    
    def _detect_type(self, data: bytes) -> Optional[str]:
        """
        Detect image type from magic bytes.
        
        Args:
            data: Raw file bytes
            
        Returns:
            str: Detected type or None
        """
        for image_type, signatures in MAGIC_SIGNATURES.items():
            for sig in signatures:
                if data.startswith(sig):
                    # Special handling for WEBP
                    if image_type == 'webp':
                        # WEBP format: RIFF....WEBP
                        if len(data) >= 12 and data[8:12] == b'WEBP':
                            return 'webp'
                        continue
                    return image_type
        
        return None
    
    def _get_expected_extensions(self, image_type: str) -> List[str]:
        """Get expected extensions for an image type."""
        mapping = {
            'jpeg': ['.jpg', '.jpeg'],
            'png': ['.png'],
            'gif': ['.gif'],
            'webp': ['.webp'],
            'bmp': ['.bmp'],
            'tiff': ['.tif', '.tiff'],
        }
        return mapping.get(image_type, [])
    
    def _scan_for_malware(self, data: bytes) -> Tuple[bool, Optional[str]]:
        """
        Scan for malicious content patterns.
        
        Args:
            data: Raw file bytes
            
        Returns:
            Tuple[bool, Optional[str]]: (is_safe, error_message)
        """
        # Convert to lowercase for case-insensitive matching
        data_lower = data.lower()
        
        for pattern in MALICIOUS_PATTERNS:
            if pattern.lower() in data_lower:
                return False, f"Suspicious pattern: {pattern.decode('utf-8', errors='ignore')}"
        
        # Check for null bytes in unusual places (potential polyglot)
        # Allow null bytes in binary image data, but not in suspicious contexts
        # This is a heuristic check
        null_count = data[:100].count(b'\x00')
        if null_count > 20:
            # Too many null bytes at start could indicate padding/hiding
            pass  # Allow for now, image formats can have null bytes
        
        return True, None
    
    def _get_dimensions(
        self, 
        data: bytes, 
        image_type: str
    ) -> Optional[Tuple[int, int]]:
        """
        Extract image dimensions without full decode.
        
        Args:
            data: Raw file bytes
            image_type: Detected image type
            
        Returns:
            Tuple[int, int]: (width, height) or None
        """
        try:
            if image_type == 'png':
                return self._get_png_dimensions(data)
            elif image_type == 'jpeg':
                return self._get_jpeg_dimensions(data)
            elif image_type == 'gif':
                return self._get_gif_dimensions(data)
            elif image_type == 'webp':
                return self._get_webp_dimensions(data)
        except Exception as e:
            logger.warning(f"Could not extract dimensions: {e}")
        
        return None
    
    def _get_png_dimensions(self, data: bytes) -> Optional[Tuple[int, int]]:
        """Extract dimensions from PNG header."""
        # PNG IHDR chunk starts at byte 8, width at byte 16, height at byte 20
        if len(data) < 24:
            return None
        
        # Check for IHDR chunk
        if data[12:16] != b'IHDR':
            return None
        
        width = struct.unpack('>I', data[16:20])[0]
        height = struct.unpack('>I', data[20:24])[0]
        return (width, height)
    
    def _get_jpeg_dimensions(self, data: bytes) -> Optional[Tuple[int, int]]:
        """Extract dimensions from JPEG markers."""
        # JPEG dimensions are in SOFx markers
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            
            marker = data[i + 1]
            
            # SOF0-SOF3 and SOF5-SOF15 contain dimensions
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height = struct.unpack('>H', data[i + 5:i + 7])[0]
                width = struct.unpack('>H', data[i + 7:i + 9])[0]
                return (width, height)
            
            # Skip to next marker
            if marker in (0xD8, 0xD9, 0x01):  # Start/End/TEM
                i += 2
            else:
                length = struct.unpack('>H', data[i + 2:i + 4])[0]
                i += 2 + length
        
        return None
    
    def _get_gif_dimensions(self, data: bytes) -> Optional[Tuple[int, int]]:
        """Extract dimensions from GIF header."""
        if len(data) < 10:
            return None
        
        width = struct.unpack('<H', data[6:8])[0]
        height = struct.unpack('<H', data[8:10])[0]
        return (width, height)
    
    def _get_webp_dimensions(self, data: bytes) -> Optional[Tuple[int, int]]:
        """Extract dimensions from WebP header."""
        if len(data) < 30:
            return None
        
        # Check for VP8 chunk (lossy)
        if data[12:16] == b'VP8 ':
            # Width and height at bytes 26-27 and 28-29
            if len(data) < 30:
                return None
            width = struct.unpack('<H', data[26:28])[0] & 0x3FFF
            height = struct.unpack('<H', data[28:30])[0] & 0x3FFF
            return (width, height)
        
        # Check for VP8L chunk (lossless)
        if data[12:16] == b'VP8L':
            if len(data) < 25:
                return None
            # Dimensions are packed in 4 bytes starting at byte 21
            b = struct.unpack('<I', data[21:25])[0]
            width = (b & 0x3FFF) + 1
            height = ((b >> 14) & 0x3FFF) + 1
            return (width, height)
        
        return None
    
    def sanitize(self, data: bytes) -> bytes:
        """
        Sanitize image by stripping metadata.
        
        Note: This is a basic implementation. For production,
        use Pillow or wand for proper re-encoding.
        
        Args:
            data: Raw image bytes
            
        Returns:
            bytes: Sanitized image bytes
        """
        if not self.config.STRIP_METADATA:
            return data
        
        try:
            # Try to use Pillow for proper sanitization
            from PIL import Image
            
            img = Image.open(io.BytesIO(data))
            
            # Create new image without EXIF
            output = io.BytesIO()
            
            # Save without EXIF
            if img.format == 'JPEG':
                img.save(output, format='JPEG', quality=95)
            elif img.format == 'PNG':
                img.save(output, format='PNG')
            else:
                img.save(output, format=img.format)
            
            return output.getvalue()
            
        except ImportError:
            logger.warning("Pillow not available, returning original image")
            return data
        except Exception as e:
            logger.warning(f"Could not sanitize image: {e}")
            return data


# ============================================
# Convenience Functions
# ============================================

def validate_image(
    data: Union[bytes, BinaryIO],
    filename: Optional[str] = None
) -> ValidationResult:
    """
    Convenience function to validate an image.
    
    Args:
        data: Image data
        filename: Original filename
        
    Returns:
        ValidationResult: Validation result
    """
    validator = ImageValidator()
    return validator.validate(data, filename)


def is_valid_image(
    data: Union[bytes, BinaryIO],
    filename: Optional[str] = None
) -> bool:
    """
    Quick check if image is valid.
    
    Args:
        data: Image data
        filename: Original filename
        
    Returns:
        bool: True if valid
    """
    result = validate_image(data, filename)
    return result.is_valid
