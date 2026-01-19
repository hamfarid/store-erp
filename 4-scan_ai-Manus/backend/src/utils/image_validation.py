"""
FILE: backend/src/utils/image_validation.py | PURPOSE: Validate uploaded image bytes safely | OWNER: Security Team

Security goals:
- Prevent content-type spoofing (e.g., executable renamed to .png)
- Prevent decompression bombs / excessive memory usage (Pillow MAX_IMAGE_PIXELS)
- Ensure uploads are a supported image type before any downstream processing
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import filetype
from PIL import Image
from PIL import UnidentifiedImageError
from PIL.Image import DecompressionBombError


@dataclass(frozen=True)
class ImageValidationResult:
    ok: bool
    message: str
    detected_mime: Optional[str] = None
    detected_ext: Optional[str] = None
    size: Optional[Tuple[int, int]] = None
    format: Optional[str] = None


def _normalize_ext(ext: str) -> str:
    e = (ext or "").lower().lstrip(".")
    if e == "jpeg":
        return "jpg"
    return e


def validate_image_file(
    path: str | Path,
    *,
    allowed_exts: list[str],
    max_pixels: int,
) -> ImageValidationResult:
    """
    Validate an image file on disk.

    This uses:
    - filetype.guess() for magic-byte sniffing
    - Pillow Image.verify() to ensure the file is parseable as an image
    - MAX_IMAGE_PIXELS to mitigate decompression bombs
    """
    p = Path(path)
    if not p.exists() or not p.is_file():
        return ImageValidationResult(ok=False, message="الملف غير موجود")

    allowed = {_normalize_ext(x) for x in (allowed_exts or [])}
    if not allowed:
        # safe default if config is empty
        allowed = {"jpg", "png", "gif", "bmp", "tiff"}

    # Magic-byte sniffing (content-based)
    header = p.read_bytes()[:4096]
    kind = filetype.guess(header)
    detected_mime = getattr(kind, "mime", None)
    detected_ext = _normalize_ext(getattr(kind, "extension", None) or "")

    if not detected_mime or not detected_ext:
        return ImageValidationResult(ok=False, message="نوع الملف غير مدعوم")

    if detected_ext not in allowed:
        return ImageValidationResult(
            ok=False,
            message="نوع الملف غير مدعوم",
            detected_mime=detected_mime,
            detected_ext=detected_ext,
        )

    # Pillow safety limit
    Image.MAX_IMAGE_PIXELS = int(max_pixels) if max_pixels else None

    try:
        with Image.open(p) as img:
            fmt = (img.format or "").upper()
            size = img.size
            # verify() checks file integrity; must be called before using the image further
            img.verify()

        # Re-open to read metadata safely after verify()
        with Image.open(p) as img2:
            size2 = img2.size

        return ImageValidationResult(
            ok=True,
            message="OK",
            detected_mime=detected_mime,
            detected_ext=detected_ext,
            size=size2 or size,
            format=fmt,
        )
    except DecompressionBombError:
        return ImageValidationResult(
            ok=False,
            message="الصورة كبيرة جداً أو غير آمنة",
            detected_mime=detected_mime,
            detected_ext=detected_ext,
        )
    except UnidentifiedImageError:
        return ImageValidationResult(
            ok=False,
            message="ملف صورة غير صالح",
            detected_mime=detected_mime,
            detected_ext=detected_ext,
        )
    except Exception:
        return ImageValidationResult(
            ok=False,
            message="فشل التحقق من الصورة",
            detected_mime=detected_mime,
            detected_ext=detected_ext,
        )
