"""FILE: backend/src/api/v1/upload.py | PURPOSE: File upload API routes for integration workflow | OWNER: Backend Team | LAST-AUDITED: 2025-12-13

Upload API Routes (v1)

Implements minimal upload workflow required by integration tests:
- POST /api/v1/upload/image
- GET  /api/v1/upload/info/{file_id}
- DELETE /api/v1/upload/{file_id}

Storage is local (temp directory) with in-memory metadata registry.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from ...core.config import get_settings
from ...utils.security import sanitize_filename
from ...utils.image_validation import validate_image_file

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])


MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB (matches tests)


@dataclass(frozen=True)
class StoredFile:
    file_id: str
    filename: str
    content_type: str
    size: int
    path: str
    created_at: str


# In-memory registry (test-friendly)
_FILES: Dict[str, StoredFile] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _storage_dir() -> Path:
    base = Path(tempfile.gettempdir()) / "gaara_scan_uploads"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _error(message: str, code: str) -> HTTPException:
    # NOTE: Our global HTTPException handler wraps `exc.detail` into the
    # response's `message` field. Integration tests expect `message` to be a
    # string, so `detail` must be a string.
    _ = code  # reserved for future structured errors
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file and return a file_id."""

    if not file.content_type or not file.content_type.startswith("image/"):
        raise _error("نوع الملف غير مدعوم", "UPLOAD_UNSUPPORTED_TYPE")

    safe_name = sanitize_filename(file.filename or "image")
    file_id = str(uuid4())
    dest = _storage_dir() / f"{file_id}_{safe_name}"

    # Stream to disk while enforcing size limit
    size = 0
    try:
        with dest.open("wb") as f:
            while True:
                chunk = await file.read(1024 * 1024)  # 1MB
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_FILE_SIZE_BYTES:
                    try:
                        f.close()
                    finally:
                        if dest.exists():
                            dest.unlink(missing_ok=True)
                    raise _error("حجم الملف كبير جداً", "UPLOAD_FILE_TOO_LARGE")
                f.write(chunk)
    finally:
        await file.close()

    stored = StoredFile(
        file_id=file_id,
        filename=file.filename or safe_name,
        content_type=file.content_type,
        size=size,
        path=str(dest),
        created_at=_now_iso(),
    )

    # Validate file content after write (prevents content-type spoofing + decompression bombs)
    settings = get_settings()
    validation = validate_image_file(
        dest,
        allowed_exts=settings.ALLOWED_EXTENSIONS,
        max_pixels=settings.MAX_IMAGE_PIXELS,
    )
    if not validation.ok:
        # Cleanup file on failure
        try:
            dest.unlink(missing_ok=True)
        except Exception:
            pass
        raise _error(validation.message, "UPLOAD_INVALID_IMAGE")

    _FILES[file_id] = stored

    # Response shape expected by integration tests
    return {
        "file_id": stored.file_id,
        "filename": stored.filename,
        "content_type": stored.content_type,
        "size": stored.size,
        "created_at": stored.created_at,
    }


@router.get("/info/{file_id}")
async def get_file_info(file_id: str):
    stored: Optional[StoredFile] = _FILES.get(file_id)
    if not stored or not os.path.exists(stored.path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الملف غير موجود",
        )

    return {
        "file_id": stored.file_id,
        "filename": stored.filename,
        "content_type": stored.content_type,
        "size": stored.size,
        "created_at": stored.created_at,
    }


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    stored: Optional[StoredFile] = _FILES.pop(file_id, None)
    if not stored:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الملف غير موجود",
        )

    try:
        Path(stored.path).unlink(missing_ok=True)
    except Exception:
        # Best-effort cleanup; metadata removal is authoritative for API
        pass

    return {"success": True, "message": "تم حذف الملف"}


def _reset_in_memory_registry_for_tests() -> None:
    """Test helper to clear stored metadata."""
    _FILES.clear()
