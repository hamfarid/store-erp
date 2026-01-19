# /home/ubuntu/image_search_integration/image_collector.py
"""
وحدة جمع صور الإصابات والآفات النباتية من الإنترنت
Image collector for plant diseases and pests from the internet
"""

import logging
import os
import time
import random
import hashlib
import io
from urllib.parse import urlparse, unquote
from typing import List, Dict, Any
import requests
from PIL import Image

# استيراد عميل البحث
from src.modules.image_search.search_client import search_client

logger = logging.getLogger(__name__)


class ImageCollector:
    """جامع صور الإصابات والآفات النباتية من الإنترنت.

    يستخدم عميل البحث المكوّن (حقيقي أو محاكاة) للبحث عن الصور وتنزيلها.
    يتضمن خيارات لتأخير التنزيل، والتحقق من صحة الصور، وتنظيف أسماء الملفات.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """تهيئة جامع الصور.

        المعلمات:
            config: تكوين لجامع الصور.
        """
        self.config = config or {}
        self.download_path = self.config.get("download_path", "/tmp/images/web_search_collected")
        self.min_delay = self.config.get("min_download_delay_seconds", 0.5)
        self.max_delay = self.config.get("max_download_delay_seconds", 2.0)
        self.min_image_size = self.config.get("min_image_size_bytes", 10 * 1024)  # 10KB الحد الأدنى الافتراضي للحجم
        self.min_image_dim = self.config.get("min_image_dimension", 200)  # الحد الأدنى الافتراضي للعرض/الارتفاع
        self.search_api_params = self.config.get("search_api_params", {})

    def collect_images_by_keywords(self, keywords: List[str], max_images_per_keyword: int = 20) -> List[Dict[str, Any]]:
        """جمع الصور بناءً على الكلمات المفتاحية.

        المعلمات:
            keywords: قائمة الكلمات المفتاحية للبحث.
            max_images_per_keyword: الحد الأقصى لعدد الصور لكل كلمة مفتاحية.

        العائد:
            قائمة بالبيانات الوصفية للصور المجمعة.
        """
        if not keywords or not isinstance(keywords, list):
            logger.error("الكلمات المفتاحية مفقودة أو غير صالحة (يجب أن تكون قائمة)")
            return []

        logger.info("بدء جمع صور البحث للكلمات المفتاحية: %s", keywords)
        os.makedirs(self.download_path, exist_ok=True)
        collected_image_metadata = []

        for query in keywords:
            logger.info("البحث عن صور للاستعلام: '%s'", query)
            try:
                # استخدام عميل البحث المحتمل المحسّن، وتمرير المعلمات الإضافية
                image_urls = search_client.search_images(
                    query, count=max_images_per_keyword, **self.search_api_params)

                if not image_urls:
                    logger.warning("لم يتم العثور على عناوين URL للصور للاستعلام: '%s'", query)
                    continue

                # تنظيف الاستعلام للاستخدام في المسار
                safe_query_folder = "".join(c for c in query if c.isalnum() or c in ('_', '-')).rstrip()
                keyword_path = os.path.join(self.download_path, safe_query_folder)
                os.makedirs(keyword_path, exist_ok=True)
                download_count_for_query = 0

                for img_url in image_urls:
                    try:
                        # توليد اسم ملف أكثر قوة
                        save_path = self._generate_save_path(keyword_path, img_url)

                        # تجنب إعادة التنزيل إذا كان الملف موجودًا
                        if os.path.exists(save_path):
                            # logger.debug(f"تخطي الصورة التي تم تنزيلها بالفعل: {save_path}")
                            # اختياريًا إضافة المسارات الموجودة إلى البيانات الوصفية إذا لزم الأمر
                            # collected_image_metadata.append({...})
                            continue

                        # إضافة تأخير قبل التنزيل
                        delay = random.uniform(self.min_delay, self.max_delay)
                        logger.debug("الانتظار %.2fث قبل تنزيل %s", delay, img_url)
                        time.sleep(delay)

                        # تنزيل الصورة
                        img_response = requests.get(
                            img_url, stream=True, timeout=20, headers={
                                "User-Agent": "AgriculturalAIScraper/1.0"})
                        img_response.raise_for_status()

                        # التحقق الأساسي من نوع المحتوى
                        content_type = img_response.headers.get("content-type", "").lower()
                        if not content_type.startswith("image"):
                            logger.warning("تخطي نوع محتوى غير صورة ('%s') للعنوان: %s", content_type, img_url)
                            continue

                        # تنزيل المحتوى إلى الذاكرة أولاً للتحقق
                        img_data = img_response.content
                        if len(img_data) < self.min_image_size:
                            logger.warning("تخطي الصورة (صغيرة جدًا: %s بايت) من %s", len(img_data), img_url)
                            continue

                        # التحقق من أبعاد الصورة باستخدام Pillow
                        try:
                            with Image.open(io.BytesIO(img_data)) as img:
                                width, height = img.size
                                if width < self.min_image_dim or height < self.min_image_dim:
                                    logger.warning("تخطي الصورة (الأبعاد %sx%s صغيرة جدًا) من %s", width, height, img_url)
                                    continue
                                img_format = img.format or "UNKNOWN"  # الحصول على التنسيق
                        except Exception as img_val_e:
                            logger.warning("لا يمكن التحقق من بيانات الصورة من %s: %s", img_url, img_val_e)
                            continue  # تخطي إذا لم تتمكن Pillow من فتحها

                        # حفظ بيانات الصورة المتحقق منها
                        with open(save_path, "wb") as f:
                            f.write(img_data)

                        logger.info("تم تنزيل الصورة والتحقق منها بنجاح إلى: %s", save_path)
                        collected_image_metadata.append({
                            "file_path": save_path,
                            "source_url": img_url,
                            "query": query,
                            "timestamp": time.time(),
                            "size_bytes": len(img_data),
                            "dimensions": f"{width}x{height}",
                            "format": img_format
                        })
                        download_count_for_query += 1

                    except requests.exceptions.Timeout:
                        logger.warning("انتهت مهلة تنزيل الصورة %s", img_url)
                    except requests.exceptions.RequestException as img_e:
                        logger.warning("فشل تنزيل الصورة %s: %s", img_url, img_e)
                    except IOError as io_e:
                        logger.error("فشل حفظ الصورة %s إلى %s: %s", img_url, save_path, io_e)
                    except Exception as gen_e:
                        logger.error("خطأ غير متوقع أثناء تنزيل/حفظ %s: %s", img_url, gen_e, exc_info=True)

                logger.info("تم تنزيل %s صور جديدة للاستعلام '%s'.", download_count_for_query, query)

            except Exception as search_e:
                logger.error("خطأ أثناء عملية البحث/تنزيل الصور للاستعلام '%s': %s", query, search_e, exc_info=True)

        logger.info("اكتمل جمع صور البحث. إجمالي الصور الجديدة التي تم تنزيلها: %s", len(collected_image_metadata))
        # إرجاع قائمة قواميس البيانات الوصفية
        return collected_image_metadata

    def collect_images_by_disease(self, disease_name: str, max_images: int = 20) -> List[Dict[str, Any]]:
        """جمع صور لمرض نباتي محدد.

        المعلمات:
            disease_name: اسم المرض النباتي.
            max_images: الحد الأقصى لعدد الصور للجمع.

        العائد:
            قائمة بالبيانات الوصفية للصور المجمعة.
        """
        # تحسين الكلمات المفتاحية للبحث
        keywords = [
            f"plant disease {disease_name} symptoms",
            f"{disease_name} plant disease",
            f"{disease_name} crop infection"
        ]
        return self.collect_images_by_keywords(keywords, max_images // len(keywords))

    def collect_images_by_pest(self, pest_name: str, max_images: int = 20) -> List[Dict[str, Any]]:
        """جمع صور لآفة زراعية محددة.

        المعلمات:
            pest_name: اسم الآفة الزراعية.
            max_images: الحد الأقصى لعدد الصور للجمع.

        العائد:
            قائمة بالبيانات الوصفية للصور المجمعة.
        """
        # تحسين الكلمات المفتاحية للبحث
        keywords = [
            f"agricultural pest {pest_name}",
            f"{pest_name} crop pest",
            f"{pest_name} plant damage"
        ]
        return self.collect_images_by_keywords(keywords, max_images // len(keywords))

    def collect_images_by_crop(self, crop_name: str, condition: str = None, max_images: int = 20) -> List[Dict[str, Any]]:
        """جمع صور لمحصول زراعي محدد، اختيارياً مع حالة محددة.

        المعلمات:
            crop_name: اسم المحصول الزراعي.
            condition: حالة المحصول (مثل "صحي"، "مريض").
            max_images: الحد الأقصى لعدد الصور للجمع.

        العائد:
            قائمة بالبيانات الوصفية للصور المجمعة.
        """
        # تحسين الكلمات المفتاحية للبحث
        if condition:
            keywords = [
                f"{crop_name} plant {condition} condition",
                f"{crop_name} crop {condition}",
                f"{condition} {crop_name} agriculture"
            ]
        else:
            keywords = [
                f"{crop_name} plant",
                f"{crop_name} crop",
                f"{crop_name} agriculture"
            ]
        return self.collect_images_by_keywords(keywords, max_images // len(keywords))

    def _generate_save_path(self, base_dir: str, url: str) -> str:
        """توليد اسم ملف منظّف وفريد نسبيًا بناءً على عنوان URL.

        المعلمات:
            base_dir: المجلد الأساسي للحفظ.
            url: عنوان URL للصورة.

        العائد:
            مسار الحفظ الكامل للصورة.
        """
        try:
            parsed_url = urlparse(url)
            # الحصول على المسار، وإزالة الشرطات المائلة في البداية/النهاية، وفك ترميز URL
            path_part = unquote(parsed_url.path.strip('/'))
            if not path_part:
                # إذا كان المسار فارغًا، استخدم المجال + تجزئة عنوان URL الكامل
                base_name = parsed_url.netloc + "_" + hashlib.sha1(url.encode()).hexdigest()[:8]
            else:
                base_name = os.path.basename(path_part)

            filename_stem, ext = os.path.splitext(base_name)

            # تنظيف جذع اسم الملف
            safe_stem = "".join(c for c in filename_stem if c.isalnum() or c in ('_', '-')).rstrip()
            safe_stem = safe_stem[:80]  # تحديد الطول

            # التحقق من الامتداد أو استخدام الافتراضي
            ext = ext.lower()
            if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"]:
                ext = ".jpg"  # الافتراضي إلى jpg إذا كان غير معروف أو مفقود

            # إضافة جزء من تجزئة عنوان URL لتقليل التصادمات لأسماء الملفات المتشابهة من عناوين URL مختلفة
            url_hash_part = hashlib.sha1(url.encode()).hexdigest()[:6]
            final_filename = f"{safe_stem}_{url_hash_part}{ext}"

            return os.path.join(base_dir, final_filename)

        except Exception as e:
            # اسم ملف احتياطي إذا فشل التحليل/التجزئة
            logger.warning("خطأ في توليد اسم الملف لعنوان URL %s: %s. استخدام احتياطي عشوائي.", url, e)
            fallback_name = f"image_{random.randint(10000, 99999)}_{hashlib.sha1(url.encode()).hexdigest()[:6]}.jpg"
            return os.path.join(base_dir, fallback_name)
