# /home/ubuntu/image_search_integration/search_client.py
"""
وحدة عميل البحث للبحث عن صور الإصابات والآفات النباتية من الإنترنت
Search client for fetching plant disease and pest images from web search APIs.
"""

import logging
import os
import random
import time
from typing import List, Optional

import requests

# استيراد مدير الأسرار للحصول على مفاتيح API
try:
    from core.config import get_settings
    settings = get_settings()
except ImportError:
    logging.warning(
        "Core settings module not found. API keys must be handled manually or via environment variables.")
    settings = None

logger = logging.getLogger(__name__)

# --- التكوين الافتراضي ---
# استخدام متغيرات البيئة مباشرة إذا كان مدير الأسرار غير متوفر
# أو الحصول عليها باستخدام settings.get("SEARCH_API_KEY")
SEARCH_API_KEY = os.getenv("IMAGE_SEARCH_API_KEY", "YOUR_API_KEY_HERE")
SEARCH_ENGINE_ID = os.getenv(
    "IMAGE_SEARCH_ENGINE_ID",
    "YOUR_CX_OR_ENDPOINT_ID_HERE")  # مثال: معرف Google Custom Search CX
SEARCH_API_ENDPOINT = os.getenv(
    "IMAGE_SEARCH_API_ENDPOINT",
    "https://www.googleapis.com/customsearch/v1")  # مثال: نقطة نهاية Google Custom Search API

# استخدام المحاكاة إذا كان مفتاح API مفقود
USE_SIMULATION_FALLBACK = SEARCH_API_KEY == "YOUR_API_KEY_HERE"


class WebSearchClient:
    """عميل للتفاعل مع API بحث الويب للعثور على عناوين URL للصور."""

    def __init__(
            self,
            api_key: Optional[str] = None,
            engine_id: Optional[str] = None,
            endpoint: Optional[str] = None):
        """تهيئة عميل البحث.

        المعلمات:
            api_key: مفتاح API لخدمة البحث.
            engine_id: معرف محرك البحث المحدد أو السياق (مثل Google CX).
            endpoint: عنوان URL الأساسي لنقطة نهاية API البحث.
        """
        # محاولة الحصول على المفاتيح من إعدادات النظام أولاً
        if settings:
            self.api_key = api_key or settings.get(
                "SEARCH_API_KEY", SEARCH_API_KEY)
            self.engine_id = engine_id or settings.get(
                "SEARCH_ENGINE_ID", SEARCH_ENGINE_ID)
            self.endpoint = endpoint or settings.get(
                "SEARCH_API_ENDPOINT", SEARCH_API_ENDPOINT)
        else:
            self.api_key = api_key or SEARCH_API_KEY
            self.engine_id = engine_id or SEARCH_ENGINE_ID
            self.endpoint = endpoint or SEARCH_API_ENDPOINT

        if self.api_key == "YOUR_API_KEY_HERE":
            logger.warning(
                "مفتاح API البحث غير مكوّن. ستكون وظائف البحث محدودة أو محاكاة.")
            # إجبار المحاكاة إذا كان المفتاح مفقودًا
            global USE_SIMULATION_FALLBACK
            USE_SIMULATION_FALLBACK = True

    def search_images(
            self,
            query: str,
            count: int = 10,
            start_index: int = 1,
            **kwargs) -> List[str]:
        """إجراء بحث عن الصور باستخدام API المكوّن.

        المعلمات:
            query: سلسلة استعلام البحث.
            count: العدد المطلوب من الصور (قد تنطبق حدود API لكل طلب).
            start_index: فهرس البداية للنتائج (للتصفح).
            **kwargs: معلمات إضافية خاصة بـ API البحث (مثل safeSearch، imageSize).

        العائد:
            قائمة بعناوين URL للصور التي تم العثور عليها، أو قائمة فارغة إذا فشل البحث أو لم تكن هناك نتائج.
        """
        if USE_SIMULATION_FALLBACK:
            logger.warning("مفتاح API مفقود، الرجوع إلى البحث المحاكى.")
            return self._simulate_search_images(query, count)

        logger.info(
            f"إجراء بحث صور حقيقي عن: '{query}' (العدد={count}، البداية={start_index})")
        results = []
        num_fetched = 0
        current_start = start_index

        # غالبًا ما تعيد واجهات API بحد أقصى 10 نتائج لكل صفحة، لذا قم بالتكرار
        # إذا كان هناك حاجة إلى المزيد
        while num_fetched < count:
            # بحد أقصى 10 لكل صفحة Google CSE
            results_per_page = min(10, count - num_fetched)
            params = {
                "key": self.api_key,
                "cx": self.engine_id,
                "q": query,
                "searchType": "image",
                "num": results_per_page,
                "start": current_start,
                # إضافة معلمات شائعة أخرى (اختياري)
                "safe": kwargs.get("safeSearch", "medium"),
                "imgSize": kwargs.get("imageSize", "medium"),
                "imgType": kwargs.get("imageType", "photo"),
                "fileType": kwargs.get("fileType", "jpg,png,gif,webp"),
                # "rights": kwargs.get("rights", None)  # مثال: "cc_publicdomain"
            }
            # إضافة أي kwargs إضافية تم تمريرها
            params.update(kwargs)

            try:
                response = requests.get(
                    self.endpoint, params=params, timeout=15)
                response.raise_for_status()  # رفع HTTPError للاستجابات السيئة (4xx أو 5xx)
                data = response.json()

                if "items" in data:
                    page_results = [
                        item.get("link") for item in data["items"] if item.get("link")]
                    results.extend(page_results)
                    num_fetched += len(page_results)
                    logger.debug(
                        f"تم جلب {len(page_results)} عناوين URL للصور من الصفحة التي تبدأ عند {current_start}.")

                    # التحقق مما إذا كانت هناك المزيد من النتائج المتاحة (خاص
                    # بهيكل استجابة API)
                    if "queries" in data and "nextPage" in data["queries"]:
                        current_start = data["queries"]["nextPage"][0]["startIndex"]
                    else:
                        logger.info(
                            "لا توجد المزيد من الصفحات المتاحة وفقًا لاستجابة API.")
                        break  # لا مزيد من الصفحات
                else:
                    logger.info(
                        f"لم يتم العثور على نتائج صور للاستعلام '{query}' بدءًا من الفهرس {current_start}.")
                    break  # لم يتم العثور على عناصر في هذه الصفحة

                # تأخير اختياري بين الصفحات
                if num_fetched < count:
                    time.sleep(random.uniform(0.2, 0.8))

            except requests.exceptions.Timeout:
                logger.error(
                    f"حدث مهلة أثناء البحث عن الصور للاستعلام: {query}")
                break
            except requests.exceptions.RequestException as e:
                logger.error(
                    f"خطأ أثناء طلب البحث عن الصور للاستعلام '{query}': {e}")
                # تسجيل نص الاستجابة إذا كان مفيدًا وليس كبيرًا جدًا
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(
                        f"حالة الاستجابة: {e.response.status_code}, النص: {e.response.text[:500]}")
                break
            except Exception as e:
                logger.error(
                    f"خطأ غير متوقع أثناء تحليل نتائج البحث للاستعلام '{query}': {e}",
                    exc_info=True)
                break

        logger.info(
            f"انتهى البحث عن '{query}'. تم العثور على {len(results)} إجمالي عناوين URL للصور.")
        return results[:count]  # إرجاع فقط حتى العدد المطلوب

    def _simulate_search_images(
            self,
            query: str,
            count: int = 10) -> List[str]:
        """محاكاة العثور على عناوين URL للصور للاختبار عندما يكون API غير متوفر."""
        logger.info(f"محاكاة البحث عن الصور لـ: '{query}' (العدد={count})")
        results = []
        for i in range(count):
            domain = random.choice([
                f"farm{random.randint(1,9)}.staticflickr.com",
                "plantsdb.org",
                "agriimages.net",
                "example-source.org"
            ])
            # تنسيق سلسلة f المصححة
            safe_query = query.replace(
                ' ', '_').replace(
                '/', '_')  # تنظيف أساسي
            path = f"/images/{safe_query}/{random.randint(1000, 9999)}_{i}.jpg"
            results.append(f"https://{domain}{path}")
        logger.info(f"أعادت المحاكاة {len(results)} عناوين URL للصور.")
        return results

    def search_images_by_disease(
            self,
            disease_name: str,
            count: int = 10,
            **kwargs) -> List[str]:
        """البحث عن صور مرض نباتي محدد.

        المعلمات:
            disease_name: اسم المرض النباتي.
            count: عدد الصور المطلوبة.
            **kwargs: معلمات إضافية للبحث.

        العائد:
            قائمة بعناوين URL للصور.
        """
        # تحسين استعلام البحث للحصول على نتائج أفضل
        query = f"plant disease {disease_name} symptoms"
        return self.search_images(query, count, **kwargs)

    def search_images_by_pest(
            self,
            pest_name: str,
            count: int = 10,
            **kwargs) -> List[str]:
        """البحث عن صور آفة زراعية محددة.

        المعلمات:
            pest_name: اسم الآفة الزراعية.
            count: عدد الصور المطلوبة.
            **kwargs: معلمات إضافية للبحث.

        العائد:
            قائمة بعناوين URL للصور.
        """
        # تحسين استعلام البحث للحصول على نتائج أفضل
        query = f"agricultural pest {pest_name}"
        return self.search_images(query, count, **kwargs)

    def search_images_by_crop(
            self,
            crop_name: str,
            condition: str = None,
            count: int = 10,
            **kwargs) -> List[str]:
        """البحث عن صور محصول زراعي محدد، اختيارياً مع حالة محددة.

        المعلمات:
            crop_name: اسم المحصول الزراعي.
            condition: حالة المحصول (مثل "صحي"، "مريض").
            count: عدد الصور المطلوبة.
            **kwargs: معلمات إضافية للبحث.

        العائد:
            قائمة بعناوين URL للصور.
        """
        # تحسين استعلام البحث للحصول على نتائج أفضل
        if condition:
            query = f"{crop_name} plant {condition} condition"
        else:
            query = f"{crop_name} plant"
        return self.search_images(query, count, **kwargs)


# إنشاء نسخة من العميل للاستخدام المباشر المحتمل
# فكر في إدارة الإنشاء ضمن سياق التطبيق إذا كان ذلك مناسبًا
search_client = WebSearchClient()
