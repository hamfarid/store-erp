"""
API رفع الملفات - رفع ومعالجة الصور
File Upload API - Image upload and processing
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from pathlib import Path
import logging
from PIL import Image
import aiofiles

from src.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    content_type: str
    upload_path: str

class FileInfo(BaseModel):
    file_id: str
    filename: str
    size: int
    content_type: str
    upload_date: str
    status: str

def validate_file(file: UploadFile) -> bool:
    """
    التحقق من صحة الملف
    Validate uploaded file
    """
    # فحص امتداد الملف
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        return False
    
    # فحص نوع المحتوى
    allowed_content_types = [
        'image/jpeg', 'image/jpg', 'image/png', 
        'image/gif', 'image/bmp', 'image/tiff'
    ]
    if file.content_type not in allowed_content_types:
        return False
    
    return True

@router.post("/image", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    رفع صورة
    Upload image
    """
    try:
        # التحقق من صحة الملف
        if not validate_file(file):
            raise HTTPException(
                status_code=400,
                detail="نوع الملف غير مدعوم. الأنواع المدعومة: " + ", ".join(settings.ALLOWED_EXTENSIONS)
            )
        
        # فحص حجم الملف
        file_content = await file.read()
        if len(file_content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"حجم الملف كبير جداً. الحد الأقصى: {settings.MAX_FILE_SIZE}"
            )
        
        # إنشاء معرف فريد للملف
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1].lower()
        new_filename = f"{file_id}.{file_extension}"
        
        # إنشاء مجلد الرفع إذا لم يكن موجوداً
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # مسار الملف الكامل
        file_path = upload_dir / new_filename
        
        # حفظ الملف
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # التحقق من أن الملف صورة صالحة
        try:
            with Image.open(file_path) as img:
                img.verify()
        except Exception:
            # حذف الملف إذا لم يكن صورة صالحة
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail="الملف المرفوع ليس صورة صالحة"
            )
        
        logger.info(f"تم رفع الملف بنجاح: {file.filename} -> {new_filename}")
        
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            size=len(file_content),
            content_type=file.content_type,
            upload_path=str(file_path)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في رفع الملف: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطأ في رفع الملف"
        )

@router.post("/batch", response_model=List[UploadResponse])
async def upload_multiple_images(files: List[UploadFile] = File(...)):
    """
    رفع عدة صور
    Upload multiple images
    """
    if len(files) > 10:  # حد أقصى 10 ملفات
        raise HTTPException(
            status_code=400,
            detail="عدد الملفات كبير جداً. الحد الأقصى: 10 ملفات"
        )
    
    results = []
    errors = []
    
    for file in files:
        try:
            result = await upload_image(file)
            results.append(result)
        except HTTPException as e:
            errors.append(f"{file.filename}: {e.detail}")
        except Exception as e:
            errors.append(f"{file.filename}: خطأ غير متوقع")
    
    if errors and not results:
        raise HTTPException(
            status_code=400,
            detail=f"فشل في رفع جميع الملفات: {'; '.join(errors)}"
        )
    
    return results

@router.get("/info/{file_id}", response_model=FileInfo)
async def get_file_info(file_id: str):
    """
    الحصول على معلومات الملف
    Get file information
    """
    try:
        # البحث عن الملف
        upload_dir = Path(settings.UPLOAD_DIR)
        file_pattern = f"{file_id}.*"
        
        matching_files = list(upload_dir.glob(file_pattern))
        
        if not matching_files:
            raise HTTPException(
                status_code=404,
                detail="الملف غير موجود"
            )
        
        file_path = matching_files[0]
        file_stat = file_path.stat()
        
        return FileInfo(
            file_id=file_id,
            filename=file_path.name,
            size=file_stat.st_size,
            content_type="image/jpeg",  # يمكن تحسينه لاحقاً
            upload_date=str(file_stat.st_mtime),
            status="uploaded"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في الحصول على معلومات الملف: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطأ في الحصول على معلومات الملف"
        )

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """
    حذف ملف
    Delete file
    """
    try:
        # البحث عن الملف
        upload_dir = Path(settings.UPLOAD_DIR)
        file_pattern = f"{file_id}.*"
        
        matching_files = list(upload_dir.glob(file_pattern))
        
        if not matching_files:
            raise HTTPException(
                status_code=404,
                detail="الملف غير موجود"
            )
        
        # حذف الملف
        file_path = matching_files[0]
        os.remove(file_path)
        
        logger.info(f"تم حذف الملف: {file_path}")
        
        return {"message": "تم حذف الملف بنجاح"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في حذف الملف: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطأ في حذف الملف"
        )

