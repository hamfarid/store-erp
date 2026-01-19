# /home/ubuntu/image_search_integration/storage.py
"""
وحدة تخزين صور الإصابات والآفات النباتية
Storage module for plant disease and pest images
"""

import os
import shutil
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ImageStorage:
    """مدير تخزين الصور للإصابات والآفات النباتية."""

    def __init__(self, config: Dict[str, Any] = None):
        """تهيئة مدير تخزين الصور.

        المعلمات:
            config: تكوين لمدير تخزين الصور.
        """
        self.config = config or {}
        self.base_storage_path = self.config.get("base_storage_path", "/data/images/plant_images")

        # إنشاء المجلد الأساسي إذا لم يكن موجودًا
        os.makedirs(self.base_storage_path, exist_ok=True)

        # إنشاء المجلدات الفرعية
        self.disease_images_path = os.path.join(self.base_storage_path, "diseases")
        self.pest_images_path = os.path.join(self.base_storage_path, "pests")
        self.crop_images_path = os.path.join(self.base_storage_path, "crops")
        self.uploaded_images_path = os.path.join(self.base_storage_path, "uploads")

        os.makedirs(self.disease_images_path, exist_ok=True)
        os.makedirs(self.pest_images_path, exist_ok=True)
        os.makedirs(self.crop_images_path, exist_ok=True)
        os.makedirs(self.uploaded_images_path, exist_ok=True)

    def store_image(self, source_path: str, category: str = "uploads") -> str:
        """تخزين صورة في مخزن الصور.

        المعلمات:
            source_path: مسار الصورة المصدر.
            category: فئة الصورة (diseases, pests, crops, uploads).

        العائد:
            مسار الصورة المخزنة.
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"ملف الصورة المصدر غير موجود: {source_path}")

        # تحديد مجلد التخزين بناءً على الفئة
        if category == "diseases":
            storage_dir = self.disease_images_path
        elif category == "pests":
            storage_dir = self.pest_images_path
        elif category == "crops":
            storage_dir = self.crop_images_path
        else:
            storage_dir = self.uploaded_images_path

        # إنشاء مجلد فرعي بناءً على التاريخ
        date_subdir = datetime.now().strftime("%Y/%m/%d")
        storage_dir = os.path.join(storage_dir, date_subdir)
        os.makedirs(storage_dir, exist_ok=True)

        # توليد اسم ملف فريد
        file_ext = os.path.splitext(source_path)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"

        # مسار الوجهة النهائي
        dest_path = os.path.join(storage_dir, unique_filename)

        # نسخ الملف
        shutil.copy2(source_path, dest_path)

        logger.info(f"تم تخزين الصورة بنجاح: {dest_path}")
        return dest_path

    def delete_image(self, image_path: str) -> bool:
        """حذف صورة من مخزن الصور.

        المعلمات:
            image_path: مسار الصورة للحذف.

        العائد:
            True إذا تم الحذف بنجاح، False خلاف ذلك.
        """
        if not os.path.exists(image_path):
            logger.warning(f"ملف الصورة غير موجود للحذف: {image_path}")
            return False

        try:
            os.remove(image_path)
            logger.info(f"تم حذف الصورة بنجاح: {image_path}")
            return True
        except Exception as e:
            logger.error(f"فشل حذف الصورة {image_path}: {e}")
            return False

    def move_image(self, source_path: str, new_category: str, metadata: Dict[str, Any] = None) -> Optional[str]:
        """نقل صورة إلى فئة مختلفة.

        المعلمات:
            source_path: مسار الصورة المصدر.
            new_category: الفئة الجديدة (diseases, pests, crops, uploads).
            metadata: البيانات الوصفية للصورة.

        العائد:
            مسار الصورة الجديد، أو None إذا فشلت العملية.
        """
        if not os.path.exists(source_path):
            logger.warning(f"ملف الصورة غير موجود للنقل: {source_path}")
            return None

        try:
            # تخزين الصورة في الفئة الجديدة
            new_path = self.store_image(source_path, new_category)

            # حذف الصورة الأصلية
            os.remove(source_path)

            logger.info(f"تم نقل الصورة بنجاح من {source_path} إلى {new_path}")
            return new_path
        except Exception as e:
            logger.error(f"فشل نقل الصورة {source_path}: {e}")
            return None

    def get_image_url(self, image_path: str, base_url: str = None) -> str:
        """الحصول على عنوان URL للصورة.

        المعلمات:
            image_path: مسار الصورة.
            base_url: عنوان URL الأساسي للخادم.

        العائد:
            عنوان URL للصورة.
        """
        if not base_url:
            # استخدام عنوان URL افتراضي إذا لم يتم توفير عنوان URL أساسي
            base_url = self.config.get("base_url", "http://localhost:8000")

        # التحقق مما إذا كان المسار يبدأ بمسار التخزين الأساسي
        if image_path.startswith(self.base_storage_path):
            # استخراج المسار النسبي
            relative_path = os.path.relpath(image_path, self.base_storage_path)
            # بناء عنوان URL
            return f"{base_url}/images/{relative_path}"
        else:
            # إذا لم يكن المسار ضمن مسار التخزين الأساسي، إرجاع المسار كما هو
            return image_path
