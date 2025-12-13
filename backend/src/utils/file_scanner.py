#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.33: File Upload Security Scanner

Provides comprehensive file upload security scanning including:
- File type validation (magic bytes)
- Malware signature detection
- File size limits
- Filename sanitization
- MIME type verification
"""

import os
import re
import hashlib
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

MAX_FILE_SIZE = int(os.environ.get("MAX_UPLOAD_SIZE", 16 * 1024 * 1024))  # 16MB default
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

# Allowed file extensions by category
ALLOWED_EXTENSIONS = {
    "images": {"png", "jpg", "jpeg", "gif", "webp", "bmp", "ico", "svg"},
    "documents": {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "csv"},
    "archives": {"zip", "rar", "7z", "tar", "gz"},
    "data": {"json", "xml", "yaml", "yml"},
}

# File magic bytes signatures
MAGIC_SIGNATURES = {
    # Images
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpg",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
    b"RIFF": "webp",  # RIFF....WEBP
    b"BM": "bmp",
    # Documents
    b"%PDF": "pdf",
    b"PK\x03\x04": "zip",  # Also docx, xlsx, pptx
    b"\xd0\xcf\x11\xe0": "doc",  # MS Office
    # Archives
    b"Rar!\x1a\x07": "rar",
    b"7z\xbc\xaf\x27\x1c": "7z",
    b"\x1f\x8b\x08": "gz",
}

# Dangerous file patterns to block
DANGEROUS_PATTERNS = [
    # Executable files
    b"MZ",  # Windows executable
    b"\x7fELF",  # Linux executable
    b"#!/",  # Shell scripts
    b"<?php",  # PHP files
    b"<%",  # ASP/JSP
    # Malware signatures (common patterns)
    b"<script",  # Embedded scripts
    b"javascript:",
    b"vbscript:",
    b"data:text/html",
    # Office macro indicators
    b"vbaProject",
    b"_VBA_PROJECT",
]

# Known malware hashes (example - would be updated regularly in production)
MALWARE_HASHES = set(
    [
        # Add known malware MD5/SHA256 hashes here
    ]
)


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ScanResult:
    """Result of a file security scan."""

    is_safe: bool
    file_type: Optional[str]
    detected_extension: Optional[str]
    file_size: int
    threats: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "file_type": self.file_type,
            "detected_extension": self.detected_extension,
            "file_size": self.file_size,
            "threats": self.threats,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


# =============================================================================
# Scanner Class
# =============================================================================


class FileScanner:
    """
    P1.33: Comprehensive file security scanner.

    Usage:
        scanner = FileScanner()
        result = scanner.scan_file(file_path)
        if not result.is_safe:
            raise SecurityError(result.threats)
    """

    def __init__(
        self,
        max_size: int = MAX_FILE_SIZE,
        allowed_categories: Optional[List[str]] = None,
    ):
        self.max_size = max_size
        self.allowed_categories = allowed_categories or ["images", "documents", "data"]
        self._build_allowed_extensions()

    def _build_allowed_extensions(self):
        """Build set of allowed extensions from categories."""
        self.allowed_extensions = set()
        for category in self.allowed_categories:
            if category in ALLOWED_EXTENSIONS:
                self.allowed_extensions.update(ALLOWED_EXTENSIONS[category])

    def scan_file(self, file_path: str) -> ScanResult:
        """
        Perform comprehensive security scan on a file.

        Args:
            file_path: Path to the file to scan

        Returns:
            ScanResult with scan findings
        """
        threats = []
        warnings = []
        metadata = {}

        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            return ScanResult(
                is_safe=False,
                file_type=None,
                detected_extension=None,
                file_size=0,
                threats=["File not found"],
                warnings=[],
                metadata={},
            )

        # Get file size
        file_size = path.stat().st_size
        metadata["file_size"] = file_size

        # Check file size
        if file_size > self.max_size:
            threats.append(
                f"File size ({file_size} bytes) exceeds maximum ({self.max_size} bytes)"
            )

        if file_size == 0:
            warnings.append("File is empty")

        # Get file extension
        extension = path.suffix.lower().lstrip(".")
        metadata["declared_extension"] = extension

        # Check extension
        if extension and extension not in self.allowed_extensions:
            threats.append(f"File extension .{extension} is not allowed")

        # Read file header for magic byte analysis
        try:
            with open(file_path, "rb") as f:
                header = f.read(8192)  # Read first 8KB for analysis
        except Exception as e:
            return ScanResult(
                is_safe=False,
                file_type=None,
                detected_extension=extension,
                file_size=file_size,
                threats=[f"Cannot read file: {str(e)}"],
                warnings=warnings,
                metadata=metadata,
            )

        # Detect file type from magic bytes
        detected_type = self._detect_file_type(header)
        metadata["detected_type"] = detected_type

        # Verify extension matches content
        if detected_type and extension:
            if not self._extension_matches_type(extension, detected_type):
                threats.append(
                    f"Extension mismatch: declared .{extension}, detected {detected_type}"
                )

        # Scan for dangerous patterns
        dangerous_findings = self._scan_for_dangerous_patterns(header)
        threats.extend(dangerous_findings)

        # Check for malware signatures
        file_hash = self._calculate_hash(file_path)
        metadata["sha256"] = file_hash

        if file_hash in MALWARE_HASHES:
            threats.append("Known malware signature detected")

        # Determine if file is safe
        is_safe = len(threats) == 0

        return ScanResult(
            is_safe=is_safe,
            file_type=detected_type,
            detected_extension=extension,
            file_size=file_size,
            threats=threats,
            warnings=warnings,
            metadata=metadata,
        )

    def scan_bytes(self, content: bytes, filename: str) -> ScanResult:
        """
        Scan file content from bytes (for in-memory files).

        Args:
            content: File content as bytes
            filename: Original filename

        Returns:
            ScanResult with scan findings
        """
        threats = []
        warnings = []
        metadata = {}

        file_size = len(content)
        metadata["file_size"] = file_size

        # Check file size
        if file_size > self.max_size:
            threats.append(
                f"File size ({file_size} bytes) exceeds maximum ({self.max_size} bytes)"
            )

        if file_size == 0:
            warnings.append("File is empty")

        # Get extension from filename
        extension = Path(filename).suffix.lower().lstrip(".")
        metadata["declared_extension"] = extension

        # Check extension
        if extension and extension not in self.allowed_extensions:
            threats.append(f"File extension .{extension} is not allowed")

        # Detect file type
        header = content[:8192]
        detected_type = self._detect_file_type(header)
        metadata["detected_type"] = detected_type

        # Verify extension matches content
        if detected_type and extension:
            if not self._extension_matches_type(extension, detected_type):
                threats.append(
                    f"Extension mismatch: declared .{extension}, detected {detected_type}"
                )

        # Scan for dangerous patterns
        dangerous_findings = self._scan_for_dangerous_patterns(header)
        threats.extend(dangerous_findings)

        # Calculate hash
        file_hash = hashlib.sha256(content).hexdigest()
        metadata["sha256"] = file_hash

        if file_hash in MALWARE_HASHES:
            threats.append("Known malware signature detected")

        is_safe = len(threats) == 0

        return ScanResult(
            is_safe=is_safe,
            file_type=detected_type,
            detected_extension=extension,
            file_size=file_size,
            threats=threats,
            warnings=warnings,
            metadata=metadata,
        )

    def _detect_file_type(self, header: bytes) -> Optional[str]:
        """Detect file type from magic bytes."""
        for signature, file_type in MAGIC_SIGNATURES.items():
            if header.startswith(signature):
                return file_type
        return None

    def _extension_matches_type(self, extension: str, detected_type: str) -> bool:
        """Check if file extension matches detected type."""
        type_extensions = {
            "png": ["png"],
            "jpg": ["jpg", "jpeg"],
            "gif": ["gif"],
            "webp": ["webp"],
            "bmp": ["bmp"],
            "pdf": ["pdf"],
            "zip": ["zip", "docx", "xlsx", "pptx"],  # Office files are zips
            "doc": ["doc"],
            "rar": ["rar"],
            "7z": ["7z"],
            "gz": ["gz", "tar.gz", "tgz"],
        }

        allowed = type_extensions.get(detected_type, [detected_type])
        return extension in allowed

    def _scan_for_dangerous_patterns(self, content: bytes) -> List[str]:
        """Scan content for dangerous patterns."""
        findings = []

        for pattern in DANGEROUS_PATTERNS:
            if (
                pattern in content.lower()
                if isinstance(pattern, bytes)
                else pattern.encode() in content.lower()
            ):
                findings.append(f"Dangerous pattern detected: {pattern[:20]}...")

        return findings

    def _calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file."""
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)

        return sha256.hexdigest()


# =============================================================================
# Helper Functions
# =============================================================================


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe storage.

    Removes potentially dangerous characters and patterns.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed_file"

    # Get base name (remove directory components)
    filename = os.path.basename(filename)

    # Remove null bytes and control characters
    filename = re.sub(r"[\x00-\x1f\x7f]", "", filename)

    # Replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")

    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]

    # Ensure we have a valid filename
    if not name:
        name = "unnamed_file"

    return name + ext


def get_safe_extension(filename: str) -> Optional[str]:
    """
    Get the file extension if it's in the allowed list.

    Args:
        filename: Filename to check

    Returns:
        Extension if allowed, None otherwise
    """
    ext = Path(filename).suffix.lower().lstrip(".")

    all_allowed = set()
    for exts in ALLOWED_EXTENSIONS.values():
        all_allowed.update(exts)

    return ext if ext in all_allowed else None


def validate_upload(
    file_storage,
    allowed_categories: Optional[List[str]] = None,
    max_size: Optional[int] = None,
) -> Tuple[bool, ScanResult]:
    """
    Validate a Flask file upload.

    Args:
        file_storage: Flask FileStorage object
        allowed_categories: List of allowed file categories
        max_size: Maximum file size in bytes

    Returns:
        Tuple of (is_valid, scan_result)
    """
    scanner = FileScanner(
        max_size=max_size or MAX_FILE_SIZE, allowed_categories=allowed_categories
    )

    # Read file content
    content = file_storage.read()
    file_storage.seek(0)  # Reset for later use

    # Scan the file
    result = scanner.scan_bytes(content, file_storage.filename or "")

    return result.is_safe, result


# =============================================================================
# Flask Integration
# =============================================================================


def init_file_scanner(app):
    """
    Initialize file scanner for Flask app.

    Adds a before_request hook to scan file uploads.

    Args:
        app: Flask application instance
    """
    from flask import request, jsonify

    @app.before_request
    def _scan_uploads():
        """Scan all file uploads before processing."""
        if request.files:
            for key, file in request.files.items():
                if file and file.filename:
                    is_safe, result = validate_upload(file)

                    if not is_safe:
                        logger.warning(
                            f"P1.33: Blocked unsafe file upload: {file.filename} - "
                            f"Threats: {result.threats}"
                        )
                        return (
                            jsonify(
                                {
                                    "success": False,
                                    "error": {
                                        "code": "FILE_SECURITY_ERROR",
                                        "message": "File failed security scan",
                                        "details": result.threats,
                                    },
                                }
                            ),
                            400,
                        )

    logger.info("P1.33: File upload scanner initialized")


__all__ = [
    "FileScanner",
    "ScanResult",
    "sanitize_filename",
    "get_safe_extension",
    "validate_upload",
    "init_file_scanner",
    "ALLOWED_EXTENSIONS",
    "MAX_FILE_SIZE",
]
