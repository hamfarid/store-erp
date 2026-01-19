#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام البحث المتقدم عن الصور
==========================

يوفر هذا المديول وظائف للبحث عن الصور الزراعية عبر الإنترنت باستخدام كلمات مفتاحية،
مع التحقق من موثوقية المصادر وتصفية النتائج.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import logging
import time
import hashlib
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# استيراد مكونات أخرى (إذا لزم الأمر)
# from src.data_collection.source_verifier import SourceVerifier

# إعداد السجل
logger = logging.getLogger("agricultural_ai.image_search")

class ImageSearcher:
    """فئة للبحث عن الصور الزراعية عبر الإنترنت باستخدام كلمات مفتاحية"""
    
    def __init__(self, config: Dict, source_verifier=None, browser_tools=None):
        """تهيئة باحث الصور
        
        المعاملات:
            config (Dict): تكوين باحث الصور
            source_verifier: كائن للتحقق من موثوقية المصادر
            browser_tools: أدوات المتصفح (للاختبار والمحاكاة)
        """
        self.config = config.get("image_search", {})
        self.source_verifier = source_verifier
        self.browser_tools = browser_tools
        
        # إعدادات البحث
        self.search_engines = self.config.get("search_engines", ["google", "bing"])
        self.max_pages_per_engine = self.config.get("max_pages_per_engine", 2)
        self.max_scroll_per_page = self.config.get("max_scroll_per_page", 5)
        
        # إعدادات الصور
        self.image_save_dir = self.config.get("image_save_dir", "data/searched_images")
        self.min_image_size = self.config.get("min_image_size_bytes", 10000) # 10KB
        self.min_image_width = self.config.get("min_image_width", 200)
        self.min_image_height = self.config.get("min_image_height", 200)
        self.allowed_image_formats = self.config.get("allowed_image_formats", [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"])
        
        # إنشاء مجلد الحفظ إذا لم يكن موجودًا
        os.makedirs(self.image_save_dir, exist_ok=True)
        
        logger.info("تم تهيئة باحث الصور المتقدم")

    def search(self, keywords: str, max_images: int = 10, min_reliability: float = 0.4) -> List[Dict]:
        """البحث عن صور باستخدام كلمات مفتاحية
        
        المعاملات:
            keywords (str): الكلمات المفتاحية للبحث
            max_images (int): الحد الأقصى لعدد الصور المراد إرجاعها
            min_reliability (float): الحد الأدنى لموثوقية المصدر
            
        الإرجاع:
            List[Dict]: قائمة بالصور التي تم العثور عليها (معلومات ومسارات محلية)
        """
        start_time = time.time()
        logger.info(f"بدء البحث عن صور باستخدام الكلمات المفتاحية: {keywords}")
        
        # تنظيف الكلمات المفتاحية
        clean_keywords = self._sanitize_keywords(keywords)
        keywords_list = [kw.strip() for kw in clean_keywords.split() if len(kw.strip()) > 2]
        
        # الحصول على روابط محتملة من البحث
        potential_urls = self._perform_web_search(clean_keywords)
        logger.info(f"تم العثور على {len(potential_urls)} روابط محتملة")
        
        # تصفية الروابط بناءً على الموثوقية
        verified_urls = []
        for url in potential_urls:
            if len(verified_urls) >= self.max_pages_per_engine * len(self.search_engines):
                break
                
            # التحقق من موثوقية المصدر (إذا كان متاحًا)
            if self.source_verifier:
                verification = self.source_verifier.verify_source(url, update_db=True)
                reliability = verification.get("reliability_score", 0)
                
                if reliability >= min_reliability:
                    verified_urls.append({"url": url, "reliability": reliability, "verification": verification})
                    logger.debug(f"تمت إضافة رابط موثوق: {url} (الموثوقية: {reliability})")
                else:
                    logger.debug(f"تم تجاهل رابط غير موثوق: {url} (الموثوقية: {reliability})")
            else:
                # إذا لم يكن هناك مدقق مصادر، نفترض أن جميع الروابط موثوقة
                verified_urls.append({"url": url, "reliability": 0.5, "verification": {"notes": "لم يتم التحقق"}})
                
        # جمع الصور من الروابط الموثوقة
        all_images = []
        for url_info in verified_urls:
            if len(all_images) >= max_images:
                break
                
            url = url_info["url"]
            try:
                # استخراج الصور من الرابط
                page_images = self._scrape_images_from_url(url, keywords_list)
                
                # إضافة معلومات المصدر
                for img in page_images:
                    img["source_page"] = url
                    img["source_reliability"] = url_info["reliability"]
                    img["source_verification"] = url_info["verification"]
                
                all_images.extend(page_images)
                logger.info(f"تم استخراج {len(page_images)} صور من {url}")
            except Exception as e:
                logger.error(f"فشل في استخراج الصور من {url}: {e}")
                
        # تصفية وترتيب النتائج
        filtered_images = self._filter_and_rank_images(all_images, keywords_list)
        result_images = filtered_images[:max_images]
        
        logger.info(f"اكتمل البحث عن الصور. تم العثور على {len(result_images)} صور (من أصل {len(all_images)}) في {time.time() - start_time:.2f} ثانية")
        return result_images

    def _sanitize_keywords(self, keywords: str) -> str:
        """تنظيف الكلمات المفتاحية"""
        # إزالة الأحرف الخاصة غير المرغوب فيها
        clean = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', keywords)
        # استبدال المسافات المتعددة بمسافة واحدة
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    def _perform_web_search(self, keywords: str) -> List[str]:
        """إجراء بحث على الويب للحصول على روابط محتملة
        
        المعاملات:
            keywords (str): الكلمات المفتاحية للبحث
            
        الإرجاع:
            List[str]: قائمة بالروابط المحتملة
        """
        urls = []
        
        # استخدام أداة البحث العامة (info_search_web)
        try:
            # تعديل الاستعلام ليشمل "صور" أو "images"
            for search_engine in self.search_engines:
                if search_engine == "google":
                    search_query = f"images {keywords}"
                    if self.browser_tools and hasattr(self.browser_tools, "info_search_web"):
                        search_results = self.browser_tools.info_search_web(query=search_query)
                        if search_results and "results" in search_results:
                            for result in search_results["results"]:
                                if "url" in result and result["url"] not in urls:
                                    urls.append(result["url"])
                elif search_engine == "bing":
                    search_query = f"bing images {keywords}"
                    if self.browser_tools and hasattr(self.browser_tools, "info_search_web"):
                        search_results = self.browser_tools.info_search_web(query=search_query)
                        if search_results and "results" in search_results:
                            for result in search_results["results"]:
                                if "url" in result and result["url"] not in urls:
                                    urls.append(result["url"])
        except Exception as e:
            logger.error(f"فشل في إجراء البحث على الويب: {e}")
            
        return urls

    def _scrape_images_from_url(self, url: str, keywords_list: List[str]) -> List[Dict]:
        """استخراج الصور من رابط
        
        المعاملات:
            url (str): رابط الصفحة
            keywords_list (List[str]): قائمة الكلمات المفتاحية للتصفية
            
        الإرجاع:
            List[Dict]: قائمة بالصور المستخرجة
        """
        images = []
        
        if not self.browser_tools:
            logger.error("أدوات المتصفح غير متاحة")
            return images
            
        try:
            # التنقل إلى الرابط
            if hasattr(self.browser_tools, "browser_navigate"):
                self.browser_tools.browser_navigate(url=url)
                logger.debug(f"تم الانتقال إلى {url}")
                
                # التمرير لأسفل لتحميل المزيد من الصور
                for _ in range(self.max_scroll_per_page):
                    if hasattr(self.browser_tools, "browser_scroll_down"):
                        self.browser_tools.browser_scroll_down()
                        time.sleep(1) # انتظار تحميل المحتوى
                
                # استخراج محتوى الصفحة
                if hasattr(self.browser_tools, "browser_view"):
                    page_content = self.browser_tools.browser_view()
                    
                    # تحليل محتوى الصفحة للعثور على الصور
                    if page_content and "content" in page_content:
                        # استخدام BeautifulSoup أو تعبيرات منتظمة لاستخراج الصور
                        # هنا نستخدم تعبير منتظم بسيط للتوضيح
                        img_tags = re.findall(r'<img[^>]+src="([^"]+)"[^>]*>', page_content["content"])
                        
                        for img_src in img_tags:
                            # تحويل الرابط النسبي إلى مطلق
                            img_url = urljoin(url, img_src)
                            
                            # استخراج النص البديل (إذا وجد)
                            alt_match = re.search(r'<img[^>]+alt="([^"]*)"[^>]*src="' + re.escape(img_src) + r'"[^>]*>', page_content["content"])
                            alt_text = alt_match.group(1) if alt_match else ""
                            
                            # التحقق من صلة الصورة بالكلمات المفتاحية
                            if self._is_relevant_image(img_url, alt_text, keywords_list):
                                # تنزيل وحفظ الصورة
                                saved_info = self._filter_and_save_image(img_url, url, alt_text)
                                if saved_info:
                                    images.append(saved_info)
        except Exception as e:
            logger.error(f"فشل في استخراج الصور من {url}: {e}")
            
        return images

    def _is_relevant_image(self, img_url: str, alt_text: str, keywords_list: List[str]) -> bool:
        """التحقق من صلة الصورة بالكلمات المفتاحية
        
        المعاملات:
            img_url (str): رابط الصورة
            alt_text (str): النص البديل للصورة
            keywords_list (List[str]): قائمة الكلمات المفتاحية
            
        الإرجاع:
            bool: ما إذا كانت الصورة ذات صلة
        """
        # التحقق من النص البديل
        if alt_text:
            alt_text_lower = alt_text.lower()
            for keyword in keywords_list:
                if keyword.lower() in alt_text_lower:
                    return True
                    
        # التحقق من اسم الملف في الرابط
        filename = os.path.basename(urlparse(img_url).path).lower()
        for keyword in keywords_list:
            if keyword.lower() in filename:
                return True
                
        # يمكن إضافة المزيد من طرق التحقق هنا
        
        # إذا لم نتمكن من التحقق، نفترض أنها ذات صلة (سيتم تصفيتها لاحقًا)
        return True

    def _filter_and_save_image(self, img_url: str, source_page_url: str, alt_text: str) -> Optional[Dict]:
        """تنزيل وحفظ الصورة إذا كانت تلبي المعايير
        
        المعاملات:
            img_url (str): رابط الصورة
            source_page_url (str): رابط الصفحة المصدر
            alt_text (str): النص البديل للصورة
            
        الإرجاع:
            Optional[Dict]: معلومات الصورة المحفوظة، أو None إذا فشلت
        """
        try:
            # تنزيل الصورة
            import requests
            response = requests.get(img_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # التحقق من نوع المحتوى
            content_type = response.headers.get("Content-Type", "").lower()
            if not content_type.startswith("image/"):
                logger.debug(f"تم تجاهل محتوى غير صورة: {img_url} (النوع: {content_type})")
                return None
                
            # التحقق من حجم المحتوى
            content_length = int(response.headers.get("Content-Length", 0))
            if content_length > 0 and content_length < self.min_image_size:
                logger.debug(f"تم تجاهل صورة صغيرة: {img_url} (الحجم: {content_length} بايت)")
                return None
                
            # قراءة محتوى الصورة
            img_content = response.content
            
            # التحقق من الحجم الفعلي
            if len(img_content) < self.min_image_size:
                logger.debug(f"تم تجاهل صورة صغيرة: {img_url} (الحجم الفعلي: {len(img_content)} بايت)")
                return None
                
            # التحقق من الأبعاد (إذا كانت مكتبة PIL متاحة)
            try:
                from PIL import Image
                import io
                
                img = Image.open(io.BytesIO(img_content))
                width, height = img.size
                img_format = img.format.lower() if img.format else ""
                
                if width < self.min_image_width or height < self.min_image_height:
                    logger.debug(f"تم تجاهل صورة صغيرة الأبعاد: {img_url} ({width}x{height})")
                    return None
                    
                # التحقق من الصيغة
                if img_format and f".{img_format}" not in self.allowed_image_formats:
                    logger.debug(f"تم تجاهل صورة بصيغة غير مدعومة: {img_url} (الصيغة: {img_format})")
                    return None
            except ImportError:
                logger.warning("مكتبة PIL غير متاحة، لا يمكن التحقق من أبعاد الصورة")
                img_format = content_type.split("/")[-1]
            except Exception as e:
                logger.warning(f"فشل في التحقق من أبعاد الصورة {img_url}: {e}")
                img_format = content_type.split("/")[-1]
                
            # إنشاء اسم ملف فريد
            parsed_url = urlparse(img_url)
            filename_base = f"{parsed_url.netloc}_{hashlib.md5(img_url.encode()).hexdigest()[:12]}"
            filepath = os.path.join(self.image_save_dir, f"{filename_base}.{img_format}")
            
            # حفظ الصورة
            with open(filepath, "wb") as f:
                f.write(img_content)
                
            logger.info(f"تم تنزيل وحفظ الصورة: {img_url} -> {filepath}")
            
            # إرجاع معلومات الصورة
            return {
                "url": img_url,
                "saved_path": filepath,
                "alt_text": alt_text,
                "source_page": source_page_url,
                "width": width if 'width' in locals() else None,
                "height": height if 'height' in locals() else None,
                "format": img_format,
                "size_bytes": len(img_content),
                "downloaded_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"فشل في تنزيل أو حفظ الصورة {img_url}: {e}")
            return None

    def _filter_and_rank_images(self, images: List[Dict], keywords_list: List[str]) -> List[Dict]:
        """تصفية وترتيب الصور بناءً على الصلة والجودة
        
        المعاملات:
            images (List[Dict]): قائمة الصور
            keywords_list (List[str]): قائمة الكلمات المفتاحية
            
        الإرجاع:
            List[Dict]: قائمة الصور المصفاة والمرتبة
        """
        # إزالة التكرارات (بناءً على المسار المحفوظ)
        unique_images = {}
        for img in images:
            if "saved_path" in img and img["saved_path"] not in unique_images:
                unique_images[img["saved_path"]] = img
                
        # حساب درجة الصلة لكل صورة
        scored_images = []
        for img in unique_images.values():
            relevance_score = 0
            
            # زيادة الدرجة إذا كانت الكلمات المفتاحية موجودة في النص البديل
            if "alt_text" in img and img["alt_text"]:
                alt_text_lower = img["alt_text"].lower()
                for keyword in keywords_list:
                    if keyword.lower() in alt_text_lower:
                        relevance_score += 2
                        
            # زيادة الدرجة إذا كانت الكلمات المفتاحية موجودة في اسم الملف
            if "url" in img:
                filename = os.path.basename(urlparse(img["url"]).path).lower()
                for keyword in keywords_list:
                    if keyword.lower() in filename:
                        relevance_score += 1
                        
            # زيادة الدرجة بناءً على موثوقية المصدر
            if "source_reliability" in img:
                relevance_score += img["source_reliability"] * 3
                
            # زيادة الدرجة بناءً على حجم الصورة (الأبعاد)
            if "width" in img and "height" in img and img["width"] and img["height"]:
                size_factor = min(1.0, (img["width"] * img["height"]) / (1000 * 1000))
                relevance_score += size_factor * 2
                
            # إضافة الدرجة إلى الصورة
            img["relevance_score"] = relevance_score
            scored_images.append(img)
            
        # ترتيب الصور بناءً على درجة الصلة (تنازليًا)
        sorted_images = sorted(scored_images, key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return sorted_images

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "image_search": {
            "image_save_dir": "../../data/searched_images_test",
            "min_image_size_bytes": 10000,
            "min_image_width": 200,
            "min_image_height": 200,
            "allowed_image_formats": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
            "search_engines": ["google", "bing"],
            "max_pages_per_engine": 2,
            "max_scroll_per_page": 5
        }
    }
    
    # محاكاة أدوات المتصفح (للتجربة فقط)
    class MockBrowserTools:
        def info_search_web(self, query):
            print(f"محاكاة البحث عن: {query}")
            # إرجاع نتائج وهمية
            return {
                "results": [
                    {"url": "https://example.com/images/tomato-diseases"},
                    {"url": "https://example.org/plant-gallery/tomato"}
                ]
            }
            
        def browser_navigate(self, url):
            print(f"محاكاة الانتقال إلى: {url}")
            return True
            
        def browser_scroll_down(self):
            print("محاكاة التمرير لأسفل")
            return True
            
        def browser_view(self):
            print("محاكاة عرض محتوى الصفحة")
            # إرجاع محتوى HTML وهمي
            return {
                "content": """
                <html>
                <body>
                    <img src="https://example.com/images/tomato_blight.jpg" alt="Tomato Late Blight Disease">
                    <img src="https://example.com/images/healthy_tomato.jpg" alt="Healthy Tomato Plant">
                </body>
                </html>
                """
            }
    
    # محاكاة مدقق المصادر (للتجربة فقط)
    class MockSourceVerifier:
        def verify_source(self, url, update_db=True):
            print(f"محاكاة التحقق من المصدر: {url}")
            # إرجاع نتيجة وهمية
            if "example.org" in url:
                return {"reliability_score": 0.8, "notes": "مصدر موثوق (وهمي)"}
            return {"reliability_score": 0.5, "notes": "مصدر متوسط الموثوقية (وهمي)"}
    
    # تهيئة باحث الصور مع المحاكاة
    image_searcher = ImageSearcher(
        dummy_config,
        source_verifier=MockSourceVerifier(),
        browser_tools=MockBrowserTools()
    )
    
    # اختبار البحث
    print("\n--- اختبار البحث عن الصور ---")
    keywords = "أمراض الطماطم اللفحة المتأخرة"
    results = image_searcher.search(keywords, max_images=5)
    
    print(f"\nتم العثور على {len(results)} صور:")
    for i, img in enumerate(results):
        print(f"  {i+1}. {img.get('alt_text', 'بدون وصف')}")
        print(f"     الرابط: {img.get('url', 'N/A')}")
        print(f"     درجة الصلة: {img.get('relevance_score', 0)}")
        if "saved_path" in img:
            print(f"     المسار المحفوظ: {img['saved_path']}")
            
    # تنظيف الملفات الوهمية (اختياري)
    # import shutil
    # if os.path.exists(dummy_config["image_search"]["image_save_dir"]):
    #     shutil.rmtree(dummy_config["image_search"]["image_save_dir"])
    # print("\nتم حذف مجلد الاختبار")
