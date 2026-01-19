#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
جامع البيانات المتقدم (صور ومقالات)
===================================

يوفر هذا المديول وظائف متقدمة لجمع البيانات من الويب، مع التركيز على استخراج الصور
والمقالات الكاملة من صفحات الويب وتوثيق مصادرها.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import requests
import logging
import time
import hashlib
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional, Union, Tuple

# استيراد مكونات أخرى (إذا لزم الأمر)
# from src.database.database_manager import DatabaseManager

# إعداد السجل
logger = logging.getLogger("agricultural_ai.advanced_scraper")

class AdvancedScraper:
    """فئة لجمع الصور والمقالات من الويب"""
    
    def __init__(self, config: Dict):
        """تهيئة جامع البيانات المتقدم
        
        المعاملات:
            config (Dict): تكوين جامع البيانات
        """
        self.config = config.get("advanced_scraping", {})
        self.request_headers = self.config.get("request_headers", {
            "User-Agent": "Mozilla/5.0 (compatible; ManusAgriculturalAI/1.0; +http://example.com/bot)"
        })
        self.request_timeout = self.config.get("request_timeout_seconds", 15)
        self.image_save_dir = self.config.get("image_save_dir", "data/scraped_images")
        self.article_save_dir = self.config.get("article_save_dir", "data/scraped_articles")
        self.min_image_size = self.config.get("min_image_size_bytes", 5000) # 5KB
        self.allowed_image_formats = self.config.get("allowed_image_formats", [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"])
        
        # إنشاء مجلدات الحفظ إذا لم تكن موجودة
        os.makedirs(self.image_save_dir, exist_ok=True)
        os.makedirs(self.article_save_dir, exist_ok=True)
        
        # يمكن تهيئة مدير قاعدة البيانات هنا إذا لزم الأمر لتوثيق المصادر مباشرة
        # self.db_manager = DatabaseManager(config)
        
        logger.info("تم تهيئة جامع البيانات المتقدم")

    def _make_request(self, url: str) -> Optional[requests.Response]:
        """إجراء طلب HTTP للحصول على محتوى الصفحة"""
        try:
            response = requests.get(url, headers=self.request_headers, timeout=self.request_timeout, allow_redirects=True)
            response.raise_for_status() # رفع استثناء لأخطاء HTTP
            logger.debug(f"تم جلب الصفحة بنجاح: {url} (الحالة: {response.status_code})")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"فشل في جلب الصفحة {url}: {e}")
            return None

    def scrape_article(self, url: str, save_content: bool = True) -> Optional[Dict]:
        """استخراج محتوى المقالة الرئيسي من صفحة ويب
        
        المعاملات:
            url (str): رابط الصفحة
            save_content (bool): حفظ محتوى المقالة في ملف
            
        الإرجاع:
            Optional[Dict]: قاموس يحتوي على عنوان المقالة، النص، والمصدر، أو None عند الفشل
        """
        response = self._make_request(url)
        if not response or "text/html" not in response.headers.get("Content-Type", "").lower():
            logger.warning(f"الصفحة ليست HTML أو فشل الجلب: {url}")
            return None
            
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # محاولة استخراج العنوان
            title = soup.find("h1")
            if not title:
                title = soup.find("title")
            title_text = title.get_text(strip=True) if title else "عنوان غير متاح"
            
            # محاولة استخراج محتوى المقالة الرئيسي
            # هذا الجزء يعتمد بشكل كبير على هيكل الصفحة وقد يحتاج إلى تخصيص
            article_body = soup.find("article")
            if not article_body:
                # محاولة البحث عن عناصر شائعة أخرى
                article_body = soup.find("div", class_=re.compile(r"content|article|post|main", re.I))
            if not article_body:
                 article_body = soup.find("main")
            if not article_body:
                 article_body = soup.body # كحل أخير
                 
            # تنظيف النص واستخراجه
            if article_body:
                # إزالة العناصر غير المرغوب فيها (مثل الإعلانات، القوائم الجانبية، التذييلات)
                for element in article_body.find_all(["script", "style", "nav", "aside", "footer", "header", "form"]):
                    element.decompose()
                
                # الحصول على النص مع الحفاظ على الفقرات
                paragraphs = article_body.find_all("p")
                if paragraphs:
                    article_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                else:
                    article_text = article_body.get_text(separator="\n\n", strip=True)
            else:
                article_text = "فشل في استخراج محتوى المقالة"
                
            # التحقق من طول النص المستخرج
            if len(article_text) < self.config.get("min_article_length", 100):
                 logger.warning(f"المحتوى المستخرج قصير جدًا، قد لا يكون مقالة: {url}")
                 # قد لا نرغب في حفظ المقالات القصيرة جدًا
                 # return None

            article_data = {
                "url": url,
                "title": title_text,
                "text": article_text,
                "scraped_at": datetime.now().isoformat()
            }
            
            # حفظ المحتوى إذا طلب ذلك
            if save_content:
                try:
                    # إنشاء اسم ملف آمن من الرابط
                    parsed_url = urlparse(url)
                    filename_base = f"{parsed_url.netloc}_{hashlib.md5(url.encode()).hexdigest()[:8]}"
                    filepath = os.path.join(self.article_save_dir, f"{filename_base}.txt")
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"URL: {url}\n")
                        f.write(f"Title: {title_text}\n")
                        f.write(f"Scraped At: {article_data["scraped_at"]}\n\n")
                        f.write(article_text)
                        
                    article_data["saved_path"] = filepath
                    logger.info(f"تم حفظ المقالة من {url} في {filepath}")
                except Exception as e:
                    logger.error(f"فشل في حفظ المقالة من {url}: {e}")
            
            return article_data
            
        except Exception as e:
            logger.error(f"فشل في تحليل المقالة من {url}: {e}")
            return None

    def scrape_images(self, url: str, save_images: bool = True, 
                      min_width: int = 100, min_height: int = 100) -> List[Dict]:
        """استخراج الصور من صفحة ويب
        
        المعاملات:
            url (str): رابط الصفحة
            save_images (bool): حفظ الصور المستخرجة محليًا
            min_width (int): الحد الأدنى لعرض الصورة بالبكسل (تقديري)
            min_height (int): الحد الأدنى لارتفاع الصورة بالبكسل (تقديري)
            
        الإرجاع:
            List[Dict]: قائمة بالصور المستخرجة (معلومات وروابط، ومسارات محلية إذا تم الحفظ)
        """
        response = self._make_request(url)
        if not response or "text/html" not in response.headers.get("Content-Type", "").lower():
            logger.warning(f"الصفحة ليست HTML أو فشل الجلب: {url}")
            return []
            
        scraped_images = []
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            base_url = response.url # استخدام الرابط النهائي بعد عمليات إعادة التوجيه
            
            for img_tag in soup.find_all("img"):
                src = img_tag.get("src")
                if not src:
                    continue
                    
                # تخطي الصور المضمنة (base64)
                if src.startswith("data:image"):
                    continue
                    
                # إنشاء رابط مطلق للصورة
                img_url = urljoin(base_url, src)
                
                # التحقق من امتداد الملف (إذا كان متاحًا في الرابط)
                img_ext = os.path.splitext(urlparse(img_url).path)[1].lower()
                if img_ext not in self.allowed_image_formats:
                    # قد تكون الصورة بدون امتداد، سنحاول جلبها لاحقًا
                    pass
                    
                # محاولة الحصول على أبعاد الصورة من السمات (إذا كانت موجودة)
                width = img_tag.get("width")
                height = img_tag.get("height")
                try:
                    img_width = int(str(width).replace("px", "")) if width else 0
                    img_height = int(str(height).replace("px", "")) if height else 0
                except ValueError:
                    img_width, img_height = 0, 0
                    
                # التحقق المبدئي من الأبعاد
                if (width and img_width < min_width) or (height and img_height < min_height):
                    logger.debug(f"تخطي صورة صغيرة بناءً على السمات: {img_url}")
                    continue
                    
                # الحصول على النص البديل والوصف
                alt_text = img_tag.get("alt", "")
                title_text = img_tag.get("title", "")
                
                image_info = {
                    "url": img_url,
                    "alt": alt_text,
                    "title": title_text,
                    "source_page": url,
                    "width": img_width, # قد تكون 0 إذا لم تكن السمة موجودة
                    "height": img_height # قد تكون 0 إذا لم تكن السمة موجودة
                }
                
                # حفظ الصورة إذا طلب ذلك
                if save_images:
                    saved_path = self._download_and_save_image(img_url, min_width, min_height)
                    if saved_path:
                        image_info["saved_path"] = saved_path
                        scraped_images.append(image_info)
                    else:
                        # إذا فشل التنزيل أو كانت الصورة صغيرة جدًا، لا تضفها
                        pass
                else:
                    # إذا لم نقم بالحفظ، أضف المعلومات على أي حال (قد نرغب في فلترة لاحقًا)
                    scraped_images.append(image_info)
                    
            logger.info(f"تم العثور على {len(scraped_images)} صور (بعد الفلترة الأولية) في الصفحة: {url}")
            return scraped_images
            
        except Exception as e:
            logger.error(f"فشل في استخراج الصور من {url}: {e}")
            return []

    def _download_and_save_image(self, img_url: str, min_width: int, min_height: int) -> Optional[str]:
        """تنزيل صورة وحفظها والتحقق من حجمها وأبعادها"""
        try:
            # إجراء طلب للحصول على الصورة
            img_response = requests.get(img_url, headers=self.request_headers, timeout=self.request_timeout, stream=True)
            img_response.raise_for_status()
            
            # التحقق من نوع المحتوى
            content_type = img_response.headers.get("Content-Type", "").lower()
            if not content_type.startswith("image/"):
                logger.warning(f"المحتوى ليس صورة: {img_url} (النوع: {content_type})")
                return None
                
            # التحقق من حجم المحتوى
            content_length = img_response.headers.get("Content-Length")
            if content_length and int(content_length) < self.min_image_size:
                logger.debug(f"تخطي صورة صغيرة بناءً على حجم المحتوى: {img_url} ({content_length} بايت)")
                return None
                
            # قراءة محتوى الصورة
            img_content = img_response.content
            
            # التحقق مرة أخرى من الحجم الفعلي
            if len(img_content) < self.min_image_size:
                logger.debug(f"تخطي صورة صغيرة بناءً على الحجم الفعلي: {img_url} ({len(img_content)} بايت)")
                return None
                
            # محاولة التحقق من الأبعاد باستخدام مكتبة خارجية (مثل Pillow)
            try:
                from PIL import Image
                import io
                
                img = Image.open(io.BytesIO(img_content))
                actual_width, actual_height = img.size
                img_format = img.format.lower()
                img.close()
                
                if actual_width < min_width or actual_height < min_height:
                    logger.debug(f"تخطي صورة صغيرة بناءً على الأبعاد الفعلية: {img_url} ({actual_width}x{actual_height})")
                    return None
                    
                # التحقق من الصيغة المسموح بها
                if f".{img_format}" not in self.allowed_image_formats:
                     logger.warning(f"تنسيق الصورة غير مسموح به: {img_url} (التنسيق: {img_format})")
                     return None
                     
            except ImportError:
                logger.warning("مكتبة Pillow غير مثبتة، لا يمكن التحقق من أبعاد الصورة الفعلية.")
                img_format = content_type.split("/")[-1] # استخدام نوع المحتوى كصيغة
            except Exception as e:
                logger.warning(f"فشل في التحقق من أبعاد الصورة {img_url}: {e}")
                img_format = content_type.split("/")[-1]
                
            # إنشاء اسم ملف فريد وآمن
            parsed_url = urlparse(img_url)
            filename_base = f"{parsed_url.netloc}_{hashlib.md5(img_url.encode()).hexdigest()[:12]}"
            filepath = os.path.join(self.image_save_dir, f"{filename_base}.{img_format}")
            
            # حفظ الصورة
            with open(filepath, "wb") as f:
                f.write(img_content)
                
            logger.info(f"تم تنزيل وحفظ الصورة: {img_url} -> {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            logger.error(f"فشل في تنزيل الصورة {img_url}: {e}")
            return None
        except Exception as e:
            logger.error(f"فشل في معالجة أو حفظ الصورة {img_url}: {e}")
            return None

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "advanced_scraping": {
            "image_save_dir": "../../data/scraped_images_test",
            "article_save_dir": "../../data/scraped_articles_test",
            "min_image_size_bytes": 10000, # 10KB
            "min_article_length": 50
        }
    }
    
    # تهيئة جامع البيانات
    scraper = AdvancedScraper(dummy_config)
    
    # رابط صفحة ويكيبيديا كمثال
    test_url = "https://ar.wikipedia.org/wiki/%D8%B7%D9%85%D8%A7%D8%B7%D9%85"
    
    # --- اختبار استخراج المقالة --- 
    print(f"\n--- اختبار استخراج المقالة من: {test_url} ---")
    article_data = scraper.scrape_article(test_url, save_content=True)
    
    if article_data:
        print(f"العنوان: {article_data["title"]}")
        print(f"بداية النص: {article_data["text"][:200]}...")
        if "saved_path" in article_data:
            print(f"تم حفظ المقالة في: {article_data["saved_path"]}")
    else:
        print("فشل في استخراج المقالة")
        
    # --- اختبار استخراج الصور --- 
    print(f"\n--- اختبار استخراج الصور من: {test_url} ---")
    # تأكد من تثبيت Pillow: pip install Pillow
    try:
        import PIL
        print("(Pillow مثبتة، سيتم التحقق من أبعاد الصور)")
    except ImportError:
        print("(Pillow غير مثبتة، لن يتم التحقق من أبعاد الصور الفعلية)")
        
    images_data = scraper.scrape_images(test_url, save_images=True, min_width=150, min_height=150)
    
    if images_data:
        print(f"تم العثور على {len(images_data)} صور وحفظها:")
        for i, img_info in enumerate(images_data[:3]): # عرض أول 3 صور
            print(f"  {i+1}. الرابط: {img_info["url"]}")
            print(f"     النص البديل: {img_info["alt"]}")
            if "saved_path" in img_info:
                print(f"     المسار المحفوظ: {img_info["saved_path"]}")
    else:
        print("لم يتم العثور على صور مطابقة للمعايير أو فشل الاستخراج")
        
    # تنظيف الملفات الوهمية (اختياري)
    # import shutil
    # if os.path.exists(dummy_config["advanced_scraping"]["image_save_dir"]):
    #     shutil.rmtree(dummy_config["advanced_scraping"]["image_save_dir"])
    # if os.path.exists(dummy_config["advanced_scraping"]["article_save_dir"]):
    #     shutil.rmtree(dummy_config["advanced_scraping"]["article_save_dir"])
    # print("\nتم حذف مجلدات الاختبار")
