"""
نظام معالجة وتحسين صور الأمراض
Image Processing and Enhancement System
"""

import hashlib
import logging
from io import BytesIO
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PIL.Image import DecompressionBombError

logger = logging.getLogger(__name__)


class ImageProcessor:
    """معالج الصور"""

    def __init__(self, storage_path: str = "/app/data/processed_images"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def process_disease_image(
        self,
        image_data: bytes,
        enhance: bool = True,
        remove_background: bool = False,
        target_size: Tuple[int, int] = (512, 512)
    ) -> Tuple[bytes, dict]:
        """
        معالجة صورة المرض

        Args:
            image_data: بيانات الصورة
            enhance: تحسين الصورة
            remove_background: إزالة الخلفية
            target_size: الحجم المستهدف

        Returns:
            (processed_image_data, metadata)
        """
        try:
            # Pillow decompression bomb protection (limit total pixels)
            try:
                from ..core.config import get_settings

                settings = get_settings()
                Image.MAX_IMAGE_PIXELS = int(settings.MAX_IMAGE_PIXELS) if settings.MAX_IMAGE_PIXELS else None
            except Exception:
                # Best-effort; do not fail if settings cannot be loaded
                pass

            # فتح الصورة
            image = Image.open(BytesIO(image_data))
            original_size = image.size
            original_format = image.format

            # تحويل إلى RGB إذا لزم الأمر
            if image.mode != 'RGB':
                image = image.convert('RGB')

            metadata = {
                "original_size": original_size,
                "original_format": original_format,
                "processed": []
            }

            # 1. تصحيح التوجيه (EXIF orientation)
            image = ImageOps.exif_transpose(image)
            metadata["processed"].append("orientation_corrected")

            # 2. تحسين الصورة
            if enhance:
                image = self._enhance_image(image)
                metadata["processed"].append("enhanced")

            # 3. إزالة الضوضاء
            image = self._denoise_image(image)
            metadata["processed"].append("denoised")

            # 4. إزالة الخلفية (اختياري)
            if remove_background:
                image = self._remove_background(image)
                metadata["processed"].append("background_removed")

            # 5. تغيير الحجم
            image = self._resize_image(image, target_size)
            metadata["processed"].append(f"resized_to_{target_size}")

            # 6. شحذ الصورة
            image = image.filter(ImageFilter.SHARPEN)
            metadata["processed"].append("sharpened")

            # حفظ الصورة المعالجة
            output = BytesIO()
            image.save(output, format='JPEG', quality=95, optimize=True)
            processed_data = output.getvalue()

            metadata["final_size"] = image.size
            metadata["file_size_bytes"] = len(processed_data)

            logger.info(f"Image processed successfully: {metadata}")
            return processed_data, metadata

        except DecompressionBombError:
            logger.warning("Rejected image: decompression bomb detected")
            raise
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise

    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """تحسين جودة الصورة"""
        try:
            # تحسين السطوع
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)

            # تحسين التباين
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)

            # تحسين الألوان
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.15)

            # تحسين الحدة
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.3)

            return image

        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return image

    def _denoise_image(self, image: Image.Image) -> Image.Image:
        """إزالة الضوضاء من الصورة"""
        try:
            # تحويل إلى numpy array
            img_array = np.array(image)

            # استخدام Non-local Means Denoising
            denoised = cv2.fastNlMeansDenoisingColored(
                img_array,
                None,
                h=10,
                hColor=10,
                templateWindowSize=7,
                searchWindowSize=21
            )

            # تحويل مرة أخرى إلى PIL Image
            return Image.fromarray(denoised)

        except Exception as e:
            logger.error(f"Error denoising image: {e}")
            return image

    def _remove_background(self, image: Image.Image) -> Image.Image:
        """إزالة خلفية الصورة"""
        try:
            # تحويل إلى numpy array
            img_array = np.array(image)

            # تحويل إلى HSV
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

            # تحديد نطاق اللون الأخضر (للنباتات)
            lower_green = np.array([25, 40, 40])
            upper_green = np.array([90, 255, 255])

            # إنشاء mask
            mask = cv2.inRange(hsv, lower_green, upper_green)

            # تحسين الـ mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # تطبيق الـ mask
            result = cv2.bitwise_and(img_array, img_array, mask=mask)

            # إضافة خلفية بيضاء
            white_bg = np.ones_like(img_array) * 255
            mask_inv = cv2.bitwise_not(mask)
            background = cv2.bitwise_and(white_bg, white_bg, mask=mask_inv)
            final = cv2.add(result, background)

            return Image.fromarray(final)

        except Exception as e:
            logger.error(f"Error removing background: {e}")
            return image

    def _resize_image(
        self,
        image: Image.Image,
        target_size: Tuple[int, int],
        maintain_aspect: bool = True
    ) -> Image.Image:
        """تغيير حجم الصورة"""
        try:
            if maintain_aspect:
                # الحفاظ على نسبة العرض إلى الارتفاع
                image.thumbnail(target_size, Image.Resampling.LANCZOS)

                # إنشاء صورة جديدة بالحجم المطلوب مع خلفية بيضاء
                new_image = Image.new('RGB', target_size, (255, 255, 255))

                # لصق الصورة في المنتصف
                paste_pos = (
                    (target_size[0] - image.size[0]) // 2,
                    (target_size[1] - image.size[1]) // 2
                )
                new_image.paste(image, paste_pos)

                return new_image
            else:
                return image.resize(target_size, Image.Resampling.LANCZOS)

        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            return image

    def create_thumbnail(
        self,
        image_data: bytes,
        size: Tuple[int, int] = (128, 128)
    ) -> bytes:
        """إنشاء صورة مصغرة"""
        try:
            try:
                from ..core.config import get_settings

                settings = get_settings()
                Image.MAX_IMAGE_PIXELS = int(settings.MAX_IMAGE_PIXELS) if settings.MAX_IMAGE_PIXELS else None
            except Exception:
                pass
            image = Image.open(BytesIO(image_data))
            image.thumbnail(size, Image.Resampling.LANCZOS)

            output = BytesIO()
            image.save(output, format='JPEG', quality=85)
            return output.getvalue()

        except DecompressionBombError:
            logger.warning("Rejected thumbnail: decompression bomb detected")
            raise
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            raise

    def extract_features(self, image_data: bytes) -> dict:
        """استخراج ميزات الصورة للتحليل"""
        try:
            try:
                from ..core.config import get_settings

                settings = get_settings()
                Image.MAX_IMAGE_PIXELS = int(settings.MAX_IMAGE_PIXELS) if settings.MAX_IMAGE_PIXELS else None
            except Exception:
                pass
            image = Image.open(BytesIO(image_data))
            img_array = np.array(image)

            # حساب الإحصائيات
            features = {
                "mean_rgb": img_array.mean(axis=(0, 1)).tolist(),
                "std_rgb": img_array.std(axis=(0, 1)).tolist(),
                "brightness": img_array.mean(),
                "contrast": img_array.std(),
            }

            # تحليل الألوان
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            features["mean_hsv"] = hsv.mean(axis=(0, 1)).tolist()

            # كشف الحواف
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            features["edge_density"] = (edges > 0).sum() / edges.size

            return features

        except DecompressionBombError:
            logger.warning("Rejected feature extraction: decompression bomb detected")
            return {}
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return {}

    def save_processed_image(
        self,
        image_data: bytes,
        disease_name: str,
        image_id: str
    ) -> str:
        """حفظ الصورة المعالجة"""
        try:
            # إنشاء مجلد للمرض
            disease_folder = self.storage_path / disease_name.replace(" ", "_")
            disease_folder.mkdir(parents=True, exist_ok=True)

            # حفظ الصورة
            filename = f"{image_id}.jpg"
            filepath = disease_folder / filename

            with open(filepath, 'wb') as f:
                f.write(image_data)

            logger.info(f"Image saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving image: {e}")
            raise

    def batch_process_images(
        self,
        images: List[bytes],
        **kwargs
    ) -> List[Tuple[bytes, dict]]:
        """معالجة دفعة من الصور"""
        results = []

        for i, image_data in enumerate(images):
            try:
                processed, metadata = self.process_disease_image(image_data, **kwargs)
                results.append((processed, metadata))
                logger.info(f"Processed image {i+1}/{len(images)}")
            except Exception as e:
                logger.error(f"Error processing image {i+1}: {e}")
                results.append((None, {"error": str(e)}))

        return results

    def compare_images(
        self,
        image1_data: bytes,
        image2_data: bytes
    ) -> float:
        """مقارنة صورتين وإرجاع نسبة التشابه"""
        try:
            # فتح الصور
            img1 = Image.open(BytesIO(image1_data)).convert('RGB')
            img2 = Image.open(BytesIO(image2_data)).convert('RGB')

            # تغيير الحجم لنفس الأبعاد
            size = (256, 256)
            img1 = img1.resize(size)
            img2 = img2.resize(size)

            # تحويل إلى numpy arrays
            arr1 = np.array(img1)
            arr2 = np.array(img2)

            # حساب MSE (Mean Squared Error)
            mse = np.mean((arr1 - arr2) ** 2)

            # تحويل إلى نسبة تشابه (0-1)
            max_mse = 255 ** 2
            similarity = 1 - (mse / max_mse)

            return float(similarity)

        except Exception as e:
            logger.error(f"Error comparing images: {e}")
            return 0.0

    def generate_image_hash(self, image_data: bytes) -> str:
        """توليد hash للصورة للتحقق من التكرار"""
        # Using MD5 for non-security purposes (deduplication only)
        return hashlib.md5(image_data, usedforsecurity=False).hexdigest()


# دالة مساعدة
def get_image_processor() -> ImageProcessor:
    """الحصول على معالج الصور"""
    return ImageProcessor()
