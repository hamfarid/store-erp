#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.72: Image Upload and Management

Utilities for handling image uploads, resizing, and optimization.
"""

import os
import uuid
import logging
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


# =============================================================================
# Configuration
# =============================================================================

UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
MAX_IMAGE_SIZE = int(os.environ.get("MAX_IMAGE_SIZE", 5 * 1024 * 1024))  # 5MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
THUMBNAIL_SIZES = {
    "small": (150, 150),
    "medium": (400, 400),
    "large": (800, 800),
}


@dataclass
class ImageInfo:
    """Information about an uploaded image."""

    original_filename: str
    filename: str
    filepath: str
    url: str
    size: int
    width: int
    height: int
    format: str
    thumbnails: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_filename": self.original_filename,
            "filename": self.filename,
            "url": self.url,
            "size": self.size,
            "width": self.width,
            "height": self.height,
            "format": self.format,
            "thumbnails": self.thumbnails,
        }


class ImageManager:
    """
    P2.72: Image upload and management service.

    Features:
    - Image upload with validation
    - Automatic resizing and thumbnail generation
    - Image optimization
    - Multiple storage backends (local, S3)
    """

    def __init__(self, upload_folder: str = None, url_prefix: str = "/uploads"):
        self.upload_folder = Path(upload_folder or UPLOAD_FOLDER)
        self.url_prefix = url_prefix
        self._ensure_folders()

    def _ensure_folders(self):
        """Create upload folders if they don't exist."""
        for folder in ["products", "users", "categories", "temp", "thumbnails"]:
            (self.upload_folder / folder).mkdir(parents=True, exist_ok=True)

    def _allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed."""
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    def _generate_filename(self, original: str) -> str:
        """Generate unique filename."""
        ext = original.rsplit(".", 1)[1].lower() if "." in original else "jpg"
        return f"{uuid.uuid4().hex}.{ext}"

    def upload(
        self,
        file,
        folder: str = "products",
        resize: Tuple[int, int] = None,
        generate_thumbnails: bool = True,
        optimize: bool = True,
    ) -> Optional[ImageInfo]:
        """
        Upload and process an image.

        Args:
            file: File object (from Flask request.files)
            folder: Subfolder to store the image
            resize: Optional (width, height) to resize to
            generate_thumbnails: Whether to generate thumbnails
            optimize: Whether to optimize the image

        Returns:
            ImageInfo or None if upload failed
        """
        try:
            from PIL import Image
        except ImportError:
            logger.error("P2.72: Pillow not installed")
            return None

        if not file or not file.filename:
            logger.warning("P2.72: No file provided")
            return None

        original_filename = secure_filename(file.filename)

        if not self._allowed_file(original_filename):
            logger.warning(f"P2.72: File type not allowed: {original_filename}")
            return None

        # Generate unique filename
        filename = self._generate_filename(original_filename)
        target_folder = self.upload_folder / folder
        filepath = target_folder / filename

        try:
            # Open and validate image
            img = Image.open(file)
            img.verify()  # Verify it's a valid image
            file.seek(0)  # Reset file pointer
            img = Image.open(file)

            original_width, original_height = img.size
            img_format = img.format or "JPEG"

            # Convert RGBA to RGB for JPEG
            if img.mode == "RGBA" and img_format.upper() == "JPEG":
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background

            # Resize if specified
            if resize:
                img = self._resize_image(img, resize)

            # Optimize
            if optimize:
                img = self._optimize_image(img)

            # Save main image
            save_kwargs = {"quality": 85, "optimize": True}
            if img_format.upper() == "JPEG":
                save_kwargs["progressive"] = True

            img.save(filepath, format=img_format, **save_kwargs)

            # Generate thumbnails
            thumbnails = {}
            if generate_thumbnails:
                thumbnails = self._generate_thumbnails(img, folder, filename)

            # Get file size
            file_size = filepath.stat().st_size

            logger.info(f"P2.72: Uploaded image: {filename}")

            return ImageInfo(
                original_filename=original_filename,
                filename=filename,
                filepath=str(filepath),
                url=f"{self.url_prefix}/{folder}/{filename}",
                size=file_size,
                width=img.size[0],
                height=img.size[1],
                format=img_format,
                thumbnails=thumbnails,
            )

        except Exception as e:
            logger.error(f"P2.72: Image upload failed: {e}")
            return None

    def _resize_image(self, img, size: Tuple[int, int]):
        """Resize image maintaining aspect ratio."""
        from PIL import Image

        img.thumbnail(size, Image.Resampling.LANCZOS)
        return img

    def _optimize_image(self, img):
        """Optimize image for web."""
        # For now, just return the image
        # Could add more optimization like color reduction, etc.
        return img

    def _generate_thumbnails(self, img, folder: str, filename: str) -> Dict[str, str]:
        """Generate thumbnail versions of the image."""
        from PIL import Image

        thumbnails = {}
        thumb_folder = self.upload_folder / "thumbnails" / folder
        thumb_folder.mkdir(parents=True, exist_ok=True)

        name, ext = filename.rsplit(".", 1)

        for size_name, size in THUMBNAIL_SIZES.items():
            thumb = img.copy()
            thumb.thumbnail(size, Image.Resampling.LANCZOS)

            thumb_filename = f"{name}_{size_name}.{ext}"
            thumb_path = thumb_folder / thumb_filename

            thumb.save(thumb_path, quality=80, optimize=True)
            thumbnails[size_name] = (
                f"{self.url_prefix}/thumbnails/{folder}/{thumb_filename}"
            )

        return thumbnails

    def delete(self, url: str) -> bool:
        """Delete an image and its thumbnails."""
        try:
            # Extract path from URL
            relative_path = url.replace(self.url_prefix, "").lstrip("/")
            filepath = self.upload_folder / relative_path

            if filepath.exists():
                filepath.unlink()

                # Delete thumbnails
                parts = relative_path.split("/")
                if len(parts) >= 2:
                    folder = parts[0]
                    filename = parts[1]
                    name, ext = filename.rsplit(".", 1)

                    for size_name in THUMBNAIL_SIZES.keys():
                        thumb_path = (
                            self.upload_folder
                            / "thumbnails"
                            / folder
                            / f"{name}_{size_name}.{ext}"
                        )
                        if thumb_path.exists():
                            thumb_path.unlink()

                logger.info(f"P2.72: Deleted image: {url}")
                return True

            return False

        except Exception as e:
            logger.error(f"P2.72: Image delete failed: {e}")
            return False

    def get_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get information about an uploaded image."""
        try:
            from PIL import Image

            relative_path = url.replace(self.url_prefix, "").lstrip("/")
            filepath = self.upload_folder / relative_path

            if not filepath.exists():
                return None

            img = Image.open(filepath)

            return {
                "url": url,
                "size": filepath.stat().st_size,
                "width": img.size[0],
                "height": img.size[1],
                "format": img.format,
            }

        except Exception as e:
            logger.error(f"P2.72: Get image info failed: {e}")
            return None

    def list_images(self, folder: str = "products") -> List[Dict[str, Any]]:
        """List all images in a folder."""
        images = []
        target_folder = self.upload_folder / folder

        if not target_folder.exists():
            return images

        for filepath in target_folder.glob("*"):
            if filepath.is_file() and self._allowed_file(filepath.name):
                images.append(
                    {
                        "filename": filepath.name,
                        "url": f"{self.url_prefix}/{folder}/{filepath.name}",
                        "size": filepath.stat().st_size,
                        "modified": filepath.stat().st_mtime,
                    }
                )

        return sorted(images, key=lambda x: x["modified"], reverse=True)


# Global instance
image_manager = ImageManager()


__all__ = ["ImageManager", "ImageInfo", "image_manager"]
