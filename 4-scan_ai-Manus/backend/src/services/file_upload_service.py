"""
File Upload Service
====================

Purpose: Secure file upload handling with validation, storage, and cleanup.
Supports local storage and cloud storage (S3-compatible).

Features:
- File type validation
- Size limits
- Virus scanning (placeholder)
- Local and cloud storage
- Thumbnail generation
- Secure filename handling
- Cleanup of orphaned files

Usage:
    from src.services.file_upload_service import FileUploadService
    
    upload_service = FileUploadService()
    
    # Upload file
    result = await upload_service.upload(file, category="diagnosis")
    
    # Delete file
    await upload_service.delete(result["path"])

Author: Global System v35.0
Date: 2026-01-17
"""

import hashlib
import logging
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Tuple, Union

from fastapi import HTTPException, UploadFile, status

from ..core.config import get_settings

logger = logging.getLogger(__name__)


class FileUploadConfig:
    """Configuration for file uploads."""
    
    # Size limits (in bytes)
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024   # 5 MB for images
    
    # Allowed MIME types
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp"
    ]
    
    ALLOWED_DOCUMENT_TYPES: List[str] = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/csv",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ]
    
    # File extensions
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    ALLOWED_DOCUMENT_EXTENSIONS: List[str] = [".pdf", ".doc", ".docx", ".csv", ".xls", ".xlsx"]
    
    # Storage paths
    UPLOAD_DIR: str = "uploads"
    CATEGORIES: Dict[str, str] = {
        "diagnosis": "diagnosis",
        "profile": "profiles",
        "disease": "diseases",
        "report": "reports",
        "document": "documents",
        "temp": "temp"
    }
    
    # Thumbnail settings
    THUMBNAIL_SIZE: Tuple[int, int] = (200, 200)
    GENERATE_THUMBNAILS: bool = True


class FileUploadService:
    """
    Service for handling file uploads securely.
    
    Provides file validation, storage, and management capabilities.
    
    Example:
        >>> service = FileUploadService()
        >>> result = await service.upload(file, category="diagnosis")
        >>> print(result["url"])
    """
    
    def __init__(self, config: Optional[FileUploadConfig] = None):
        """
        Initialize upload service.
        
        Args:
            config: Custom configuration, uses defaults if None
        """
        self.config = config or FileUploadConfig()
        self.settings = get_settings()
        self.base_path = Path(self.config.UPLOAD_DIR)
        
        # Ensure upload directories exist
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Create upload directories if they don't exist."""
        for category_dir in self.config.CATEGORIES.values():
            path = self.base_path / category_dir
            path.mkdir(parents=True, exist_ok=True)
            
            # Create thumbnails subdirectory
            (path / "thumbnails").mkdir(exist_ok=True)
        
        logger.info(f"Upload directories initialized at {self.base_path}")
    
    def _generate_filename(
        self, 
        original_filename: str, 
        prefix: Optional[str] = None
    ) -> str:
        """
        Generate secure unique filename.
        
        Args:
            original_filename: Original file name
            prefix: Optional prefix for filename
            
        Returns:
            str: Secure unique filename
        """
        # Get extension
        ext = Path(original_filename).suffix.lower()
        
        # Generate unique ID
        unique_id = uuid.uuid4().hex[:12]
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        if prefix:
            return f"{prefix}_{timestamp}_{unique_id}{ext}"
        return f"{timestamp}_{unique_id}{ext}"
    
    def _validate_file(
        self,
        file: UploadFile,
        allowed_types: List[str],
        allowed_extensions: List[str],
        max_size: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded file.
        
        Args:
            file: Uploaded file
            allowed_types: List of allowed MIME types
            allowed_extensions: List of allowed extensions
            max_size: Maximum file size in bytes
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # Check filename
        if not file.filename:
            return False, "No filename provided"
        
        # Check extension
        ext = Path(file.filename).suffix.lower()
        if ext not in allowed_extensions:
            return False, f"File type '{ext}' not allowed"
        
        # Check content type
        if file.content_type not in allowed_types:
            return False, f"Content type '{file.content_type}' not allowed"
        
        # Check file size (read and seek back)
        file.file.seek(0, 2)  # Seek to end
        size = file.file.tell()
        file.file.seek(0)  # Seek back to start
        
        if size > max_size:
            return False, f"File too large: {size} bytes (max: {max_size})"
        
        if size == 0:
            return False, "File is empty"
        
        return True, None
    
    async def upload(
        self,
        file: UploadFile,
        category: str = "temp",
        prefix: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Upload a file.
        
        Args:
            file: FastAPI UploadFile object
            category: Upload category (diagnosis, profile, etc.)
            prefix: Optional filename prefix
            user_id: Optional user ID for tracking
            
        Returns:
            Dict with file info (path, url, filename, etc.)
            
        Raises:
            HTTPException: If validation fails
        """
        # Determine file type
        ext = Path(file.filename).suffix.lower()
        is_image = ext in self.config.ALLOWED_IMAGE_EXTENSIONS
        
        # Select validation parameters
        if is_image:
            allowed_types = self.config.ALLOWED_IMAGE_TYPES
            allowed_extensions = self.config.ALLOWED_IMAGE_EXTENSIONS
            max_size = self.config.MAX_IMAGE_SIZE
        else:
            allowed_types = self.config.ALLOWED_DOCUMENT_TYPES
            allowed_extensions = self.config.ALLOWED_DOCUMENT_EXTENSIONS
            max_size = self.config.MAX_FILE_SIZE
        
        # Validate file
        is_valid, error = self._validate_file(
            file, allowed_types, allowed_extensions, max_size
        )
        
        if not is_valid:
            logger.warning(f"File validation failed: {error}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "INVALID_FILE",
                    "message": error,
                    "message_ar": "الملف غير صالح"
                }
            )
        
        # Get category directory
        category_dir = self.config.CATEGORIES.get(category, "temp")
        save_dir = self.base_path / category_dir
        
        # Generate unique filename
        filename = self._generate_filename(file.filename, prefix)
        file_path = save_dir / filename
        
        try:
            # Read file content
            content = await file.read()
            
            # Calculate hash
            file_hash = hashlib.sha256(content).hexdigest()
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(content)
            
            logger.info(f"File uploaded: {file_path}")
            
            # Generate thumbnail for images
            thumbnail_path = None
            if is_image and self.config.GENERATE_THUMBNAILS:
                thumbnail_path = await self._generate_thumbnail(
                    file_path, save_dir / "thumbnails"
                )
            
            # Build response
            result = {
                "success": True,
                "filename": filename,
                "original_filename": file.filename,
                "path": str(file_path),
                "relative_path": f"{category_dir}/{filename}",
                "url": f"/uploads/{category_dir}/{filename}",
                "content_type": file.content_type,
                "size": len(content),
                "hash": file_hash,
                "category": category,
                "is_image": is_image,
                "uploaded_at": datetime.utcnow().isoformat() + 'Z'
            }
            
            if thumbnail_path:
                result["thumbnail_url"] = f"/uploads/{category_dir}/thumbnails/{thumbnail_path.name}"
            
            if user_id:
                result["user_id"] = user_id
            
            return result
            
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            # Clean up partial upload
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "UPLOAD_FAILED",
                    "message": "Failed to save file",
                    "message_ar": "فشل في حفظ الملف"
                }
            )
    
    async def _generate_thumbnail(
        self,
        image_path: Path,
        thumbnail_dir: Path
    ) -> Optional[Path]:
        """
        Generate thumbnail for an image.
        
        Args:
            image_path: Path to original image
            thumbnail_dir: Directory for thumbnails
            
        Returns:
            Path to thumbnail or None if failed
        """
        try:
            from PIL import Image
            
            # Open image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Create thumbnail
                img.thumbnail(self.config.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                thumb_filename = f"thumb_{image_path.name}"
                thumb_path = thumbnail_dir / thumb_filename
                img.save(thumb_path, "JPEG", quality=85)
                
                logger.debug(f"Thumbnail generated: {thumb_path}")
                return thumb_path
                
        except ImportError:
            logger.warning("Pillow not installed, skipping thumbnail generation")
            return None
        except Exception as e:
            logger.warning(f"Thumbnail generation failed: {e}")
            return None
    
    async def delete(self, path: str) -> bool:
        """
        Delete an uploaded file.
        
        Args:
            path: File path (relative or absolute)
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            file_path = Path(path)
            
            # Handle relative paths
            if not file_path.is_absolute():
                file_path = self.base_path / path
            
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
                
                # Try to delete thumbnail
                thumb_path = file_path.parent / "thumbnails" / f"thumb_{file_path.name}"
                if thumb_path.exists():
                    thumb_path.unlink()
                
                return True
            else:
                logger.warning(f"File not found for deletion: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"File deletion failed: {e}")
            return False
    
    async def get_file_info(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an uploaded file.
        
        Args:
            path: File path
            
        Returns:
            Dict with file info or None if not found
        """
        try:
            file_path = Path(path)
            
            if not file_path.is_absolute():
                file_path = self.base_path / path
            
            if not file_path.exists():
                return None
            
            stat = file_path.stat()
            
            return {
                "filename": file_path.name,
                "path": str(file_path),
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "exists": True
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            return None
    
    async def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up temporary files older than max_age.
        
        Args:
            max_age_hours: Maximum age in hours
            
        Returns:
            int: Number of files deleted
        """
        temp_dir = self.base_path / self.config.CATEGORIES["temp"]
        deleted_count = 0
        
        try:
            cutoff_time = datetime.utcnow().timestamp() - (max_age_hours * 3600)
            
            for file_path in temp_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} temporary files")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Temp file cleanup failed: {e}")
            return deleted_count
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.
        
        Returns:
            Dict with storage stats per category
        """
        stats = {
            "total_files": 0,
            "total_size": 0,
            "categories": {}
        }
        
        for category, dirname in self.config.CATEGORIES.items():
            cat_path = self.base_path / dirname
            if cat_path.exists():
                files = list(cat_path.glob("*"))
                files = [f for f in files if f.is_file()]
                
                cat_size = sum(f.stat().st_size for f in files)
                
                stats["categories"][category] = {
                    "files": len(files),
                    "size": cat_size,
                    "size_mb": round(cat_size / (1024 * 1024), 2)
                }
                
                stats["total_files"] += len(files)
                stats["total_size"] += cat_size
        
        stats["total_size_mb"] = round(stats["total_size"] / (1024 * 1024), 2)
        
        return stats


# Singleton instance
_upload_service: Optional[FileUploadService] = None


def get_upload_service() -> FileUploadService:
    """Get or create upload service singleton."""
    global _upload_service
    
    if _upload_service is None:
        _upload_service = FileUploadService()
    
    return _upload_service
