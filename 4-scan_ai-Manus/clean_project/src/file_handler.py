# File: /home/ubuntu/clean_project/src/file_handler.py
"""
مسار الملف: /home/ubuntu/clean_project/src/file_handler.py

معالج الملفات والصور الفعلي
يتضمن تحميل، معالجة، وحفظ الصور للتشخيص
"""

import os
import uuid
import shutil
from datetime import datetime
from typing import Dict, Any, Optional, List
from PIL import Image, ImageEnhance, ImageFilter
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FileHandler:
    """معالج الملفات والصور"""
    
    def __init__(self, upload_dir: str = "uploads", max_file_size: int = 10 * 1024 * 1024):
        self.upload_dir = Path(upload_dir)
        self.max_file_size = max_file_size
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        
        # إنشاء مجلدات التحميل
        self.setup_directories()
    
    def setup_directories(self):
        """إنشاء مجلدات التحميل المطلوبة"""
        directories = [
            self.upload_dir,
            self.upload_dir / "images",
            self.upload_dir / "processed",
            self.upload_dir / "thumbnails",
            self.upload_dir / "temp"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"تم إنشاء المجلد: {directory}")
    
    def validate_file(self, file_path: str, file_size: int) -> Dict[str, Any]:
        """التحقق من صحة الملف"""
        try:
            # التحقق من حجم الملف
            if file_size > self.max_file_size:
                return {
                    "valid": False,
                    "message": f"حجم الملف كبير جداً. الحد الأقصى {self.max_file_size / (1024*1024):.1f} ميجابايت"
                }
            
            # التحقق من امتداد الملف
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.allowed_extensions:
                return {
                    "valid": False,
                    "message": f"نوع الملف غير مدعوم. الأنواع المدعومة: {', '.join(self.allowed_extensions)}"
                }
            
            # التحقق من كون الملف صورة صالحة
            try:
                with Image.open(file_path) as img:
                    img.verify()
            except Exception:
                return {
                    "valid": False,
                    "message": "الملف ليس صورة صالحة"
                }
            
            return {
                "valid": True,
                "message": "الملف صالح"
            }
            
        except Exception as e:
            logger.error(f"خطأ في التحقق من الملف: {e}")
            return {
                "valid": False,
                "message": "خطأ في التحقق من الملف"
            }
    
    def save_uploaded_file(self, file_content: bytes, original_filename: str, 
                          user_id: int) -> Dict[str, Any]:
        """حفظ الملف المرفوع"""
        try:
            # إنشاء اسم ملف فريد
            file_extension = Path(original_filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # مسار الحفظ
            save_path = self.upload_dir / "images" / unique_filename
            
            # حفظ الملف
            with open(save_path, 'wb') as f:
                f.write(file_content)
            
            # التحقق من صحة الملف
            validation = self.validate_file(str(save_path), len(file_content))
            if not validation["valid"]:
                # حذف الملف إذا كان غير صالح
                os.remove(save_path)
                return validation
            
            # الحصول على معلومات الصورة
            image_info = self.get_image_info(str(save_path))
            
            logger.info(f"تم حفظ الملف: {unique_filename} للمستخدم {user_id}")
            
            return {
                "success": True,
                "message": "تم رفع الملف بنجاح",
                "file_path": str(save_path),
                "filename": unique_filename,
                "original_filename": original_filename,
                "file_size": len(file_content),
                "image_info": image_info
            }
            
        except Exception as e:
            logger.error(f"خطأ في حفظ الملف: {e}")
            return {
                "success": False,
                "message": "خطأ في حفظ الملف"
            }
    
    def get_image_info(self, file_path: str) -> Dict[str, Any]:
        """الحصول على معلومات الصورة"""
        try:
            with Image.open(file_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                    "size_mb": os.path.getsize(file_path) / (1024 * 1024)
                }
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات الصورة: {e}")
            return {}
    
    def create_thumbnail(self, image_path: str, size: tuple = (300, 300)) -> str:
        """إنشاء صورة مصغرة"""
        try:
            # مسار الصورة المصغرة
            filename = Path(image_path).stem
            thumbnail_path = self.upload_dir / "thumbnails" / f"{filename}_thumb.jpg"
            
            with Image.open(image_path) as img:
                # تحويل إلى RGB إذا لزم الأمر
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # إنشاء الصورة المصغرة
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(thumbnail_path, 'JPEG', quality=85)
            
            logger.info(f"تم إنشاء صورة مصغرة: {thumbnail_path}")
            return str(thumbnail_path)
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء الصورة المصغرة: {e}")
            return ""
    
    def preprocess_image(self, image_path: str, enhance: bool = True) -> str:
        """معالجة الصورة للتشخيص"""
        try:
            # مسار الصورة المعالجة
            filename = Path(image_path).stem
            processed_path = self.upload_dir / "processed" / f"{filename}_processed.jpg"
            
            with Image.open(image_path) as img:
                # تحويل إلى RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                if enhance:
                    # تحسين الصورة
                    img = self.enhance_image(img)
                
                # تغيير حجم الصورة للمعالجة (اختياري)
                max_size = (1024, 1024)
                if img.width > max_size[0] or img.height > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # حفظ الصورة المعالجة
                img.save(processed_path, 'JPEG', quality=95)
            
            logger.info(f"تم معالجة الصورة: {processed_path}")
            return str(processed_path)
            
        except Exception as e:
            logger.error(f"خطأ في معالجة الصورة: {e}")
            return image_path  # إرجاع المسار الأصلي في حالة الخطأ
    
    def enhance_image(self, img: Image.Image) -> Image.Image:
        """تحسين جودة الصورة"""
        try:
            # تحسين الحدة
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.2)
            
            # تحسين التباين
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
            # تحسين السطوع
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.05)
            
            # تطبيق مرشح لتقليل الضوضاء
            img = img.filter(ImageFilter.SMOOTH_MORE)
            
            return img
            
        except Exception as e:
            logger.error(f"خطأ في تحسين الصورة: {e}")
            return img
    
    def delete_file(self, file_path: str) -> bool:
        """حذف ملف"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"تم حذف الملف: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"خطأ في حذف الملف: {e}")
            return False
    
    def cleanup_temp_files(self, older_than_hours: int = 24):
        """تنظيف الملفات المؤقتة القديمة"""
        try:
            temp_dir = self.upload_dir / "temp"
            current_time = datetime.now()
            deleted_count = 0
            
            for file_path in temp_dir.glob("*"):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    age_hours = (current_time - file_time).total_seconds() / 3600
                    
                    if age_hours > older_than_hours:
                        file_path.unlink()
                        deleted_count += 1
            
            logger.info(f"تم حذف {deleted_count} ملف مؤقت قديم")
            return deleted_count
            
        except Exception as e:
            logger.error(f"خطأ في تنظيف الملفات المؤقتة: {e}")
            return 0
    
    def get_file_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الملفات"""
        try:
            stats = {
                "total_files": 0,
                "total_size_mb": 0,
                "images_count": 0,
                "thumbnails_count": 0,
                "processed_count": 0
            }
            
            # عد الملفات في كل مجلد
            for subdir in ["images", "thumbnails", "processed"]:
                dir_path = self.upload_dir / subdir
                if dir_path.exists():
                    files = list(dir_path.glob("*"))
                    count = len([f for f in files if f.is_file()])
                    size = sum(f.stat().st_size for f in files if f.is_file())
                    
                    stats[f"{subdir}_count"] = count
                    stats["total_files"] += count
                    stats["total_size_mb"] += size / (1024 * 1024)
            
            return stats
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على إحصائيات الملفات: {e}")
            return {}

# إنشاء مثيل معالج الملفات العام
file_handler = FileHandler()

def save_uploaded_image(file_content: bytes, filename: str, user_id: int) -> Dict[str, Any]:
    """دالة مساعدة لحفظ الصور المرفوعة"""
    return file_handler.save_uploaded_file(file_content, filename, user_id)

def process_image_for_diagnosis(image_path: str) -> str:
    """دالة مساعدة لمعالجة الصور للتشخيص"""
    return file_handler.preprocess_image(image_path)

