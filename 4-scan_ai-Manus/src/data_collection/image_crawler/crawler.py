#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة زحف الويب لجمع صور الأمراض النباتية
"""

import os
import time
import random
import logging
import requests
import hashlib
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlantDiseaseImageCrawler:
    """فئة لزحف الويب وجمع صور الأمراض النباتية"""
    
    def __init__(self, config=None):
        """
        تهيئة زاحف صور الأمراض النباتية
        
        المعلمات:
            config (dict): تكوين الزاحف
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'output_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'max_images_per_source': int(os.getenv('MAX_IMAGES_PER_SOURCE', 100)),
            'delay_between_requests': float(os.getenv('DELAY_BETWEEN_REQUESTS', 1.0)),
            'user_agents': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
            ],
            'allowed_extensions': ['.jpg', '.jpeg', '.png', '.webp'],
            'min_image_size': 10 * 1024,  # 10 KB
            'max_threads': int(os.getenv('MAX_CRAWLER_THREADS', 5)),
            'trusted_domains': []
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
            
        # إنشاء مجلدات الإخراج إذا لم تكن موجودة
        self._create_output_directories()
        
        # قائمة الروابط التي تمت زيارتها
        self.visited_urls = set()
        
        # قائمة الصور التي تم تنزيلها
        self.downloaded_images = set()
        
    def _create_output_directories(self):
        """إنشاء مجلدات الإخراج للصور المصنفة"""
        base_dir = self.config['output_dir']
        
        # إنشاء المجلدات الرئيسية للتصنيف
        categories = ['vegetables', 'fruits', 'crops', 'unclassified']
        
        for category in categories:
            category_dir = os.path.join(base_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            logger.info(f"تم إنشاء مجلد الإخراج: {category_dir}")
    
    def _get_random_user_agent(self):
        """الحصول على وكيل مستخدم عشوائي من القائمة"""
        return random.choice(self.config['user_agents'])
    
    def _is_valid_image_url(self, url):
        """التحقق مما إذا كان عنوان URL صالحًا للصورة"""
        parsed_url = urlparse(url)
        
        # التحقق من امتداد الملف
        _, ext = os.path.splitext(parsed_url.path.lower())
        if ext not in self.config['allowed_extensions']:
            return False
            
        # التحقق من النطاق إذا كانت قائمة النطاقات الموثوقة غير فارغة
        if self.config['trusted_domains']:
            domain = parsed_url.netloc
            if domain not in self.config['trusted_domains']:
                return False
                
        return True
    
    def _generate_filename(self, url, category):
        """توليد اسم ملف فريد للصورة"""
        # إنشاء هاش من عنوان URL
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        # استخراج امتداد الملف
        parsed_url = urlparse(url)
        _, ext = os.path.splitext(parsed_url.path.lower())
        
        # إنشاء اسم الملف
        filename = f"{category}_{url_hash}{ext}"
        
        return filename
    
    def download_image(self, url, category='unclassified'):
        """
        تنزيل صورة من عنوان URL وحفظها في المجلد المناسب
        
        المعلمات:
            url (str): عنوان URL للصورة
            category (str): فئة الصورة (vegetables, fruits, crops, unclassified)
            
        العوائد:
            str: مسار الملف المحلي إذا نجح التنزيل، وإلا None
        """
        # التحقق مما إذا كانت الصورة قد تم تنزيلها بالفعل
        if url in self.downloaded_images:
            logger.debug(f"تم تنزيل الصورة مسبقًا: {url}")
            return None
            
        # التحقق من صحة عنوان URL
        if not self._is_valid_image_url(url):
            logger.debug(f"عنوان URL غير صالح للصورة: {url}")
            return None
            
        try:
            # إنشاء جلسة HTTP مع وكيل مستخدم عشوائي
            headers = {'User-Agent': self._get_random_user_agent()}
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            
            # التحقق من نجاح الاستجابة
            if response.status_code != 200:
                logger.warning(f"فشل تنزيل الصورة من {url}: رمز الحالة {response.status_code}")
                return None
                
            # التحقق من نوع المحتوى
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                logger.warning(f"نوع المحتوى غير صالح للصورة: {content_type}")
                return None
                
            # التحقق من حجم الصورة
            content_length = int(response.headers.get('Content-Length', 0))
            if content_length < self.config['min_image_size']:
                logger.debug(f"حجم الصورة صغير جدًا: {content_length} بايت")
                return None
                
            # إنشاء اسم الملف ومسار الحفظ
            filename = self._generate_filename(url, category)
            save_path = os.path.join(self.config['output_dir'], category, filename)
            
            # حفظ الصورة
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # إضافة عنوان URL إلى قائمة الصور التي تم تنزيلها
            self.downloaded_images.add(url)
            
            logger.info(f"تم تنزيل الصورة بنجاح: {url} -> {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تنزيل الصورة من {url}: {str(e)}")
            return None
    
    def extract_image_urls(self, page_url):
        """
        استخراج عناوين URL للصور من صفحة ويب
        
        المعلمات:
            page_url (str): عنوان URL للصفحة
            
        العوائد:
            list: قائمة بعناوين URL للصور
        """
        # التحقق مما إذا كانت الصفحة قد تمت زيارتها بالفعل
        if page_url in self.visited_urls:
            logger.debug(f"تمت زيارة الصفحة مسبقًا: {page_url}")
            return []
            
        # إضافة عنوان URL إلى قائمة الصفحات التي تمت زيارتها
        self.visited_urls.add(page_url)
        
        try:
            # إنشاء جلسة HTTP مع وكيل مستخدم عشوائي
            headers = {'User-Agent': self._get_random_user_agent()}
            response = requests.get(page_url, headers=headers, timeout=10)
            
            # التحقق من نجاح الاستجابة
            if response.status_code != 200:
                logger.warning(f"فشل الوصول إلى الصفحة {page_url}: رمز الحالة {response.status_code}")
                return []
                
            # تحليل محتوى الصفحة
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # استخراج عناوين URL للصور
            image_urls = []
            
            # البحث عن علامات img
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    # تحويل المسار النسبي إلى مسار مطلق
                    img_url = urljoin(page_url, src)
                    if self._is_valid_image_url(img_url):
                        image_urls.append(img_url)
            
            # البحث عن علامات a التي تشير إلى صور
            for a in soup.find_all('a'):
                href = a.get('href')
                if href:
                    # تحويل المسار النسبي إلى مسار مطلق
                    link_url = urljoin(page_url, href)
                    if self._is_valid_image_url(link_url):
                        image_urls.append(link_url)
            
            logger.info(f"تم استخراج {len(image_urls)} عنوان URL للصور من {page_url}")
            return image_urls
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء استخراج عناوين URL للصور من {page_url}: {str(e)}")
            return []
    
    def crawl_website(self, start_url, category='unclassified', max_depth=2):
        """
        زحف موقع ويب لجمع صور الأمراض النباتية
        
        المعلمات:
            start_url (str): عنوان URL البداية
            category (str): فئة الصور (vegetables, fruits, crops, unclassified)
            max_depth (int): الحد الأقصى لعمق الزحف
            
        العوائد:
            list: قائمة بمسارات الملفات المحلية للصور التي تم تنزيلها
        """
        logger.info(f"بدء زحف الموقع: {start_url} (الفئة: {category}, العمق الأقصى: {max_depth})")
        
        # قائمة الصفحات التي سيتم زحفها
        pages_to_crawl = [(start_url, 0)]  # (url, depth)
        
        # قائمة الصور التي تم تنزيلها
        downloaded_files = []
        
        # عدد الصور التي تم تنزيلها
        image_count = 0
        
        # زحف الصفحات
        while pages_to_crawl and image_count < self.config['max_images_per_source']:
            # الحصول على الصفحة التالية
            current_url, current_depth = pages_to_crawl.pop(0)
            
            # استخراج عناوين URL للصور
            image_urls = self.extract_image_urls(current_url)
            
            # تنزيل الصور
            with ThreadPoolExecutor(max_workers=self.config['max_threads']) as executor:
                futures = [executor.submit(self.download_image, img_url, category) for img_url in image_urls]
                
                for future in futures:
                    result = future.result()
                    if result:
                        downloaded_files.append(result)
                        image_count += 1
                        
                        # التحقق من الوصول إلى الحد الأقصى
                        if image_count >= self.config['max_images_per_source']:
                            break
            
            # إذا لم نصل إلى الحد الأقصى للعمق، استخراج الروابط للصفحات التالية
            if current_depth < max_depth:
                try:
                    # إنشاء جلسة HTTP مع وكيل مستخدم عشوائي
                    headers = {'User-Agent': self._get_random_user_agent()}
                    response = requests.get(current_url, headers=headers, timeout=10)
                    
                    # التحقق من نجاح الاستجابة
                    if response.status_code == 200:
                        # تحليل محتوى الصفحة
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # استخراج الروابط
                        for a in soup.find_all('a'):
                            href = a.get('href')
                            if href:
                                # تحويل المسار النسبي إلى مسار مطلق
                                next_url = urljoin(current_url, href)
                                
                                # التحقق من النطاق
                                if urlparse(next_url).netloc == urlparse(current_url).netloc:
                                    # إضافة الصفحة إلى قائمة الصفحات التي سيتم زحفها
                                    if next_url not in self.visited_urls:
                                        pages_to_crawl.append((next_url, current_depth + 1))
                
                except Exception as e:
                    logger.error(f"حدث خطأ أثناء استخراج الروابط من {current_url}: {str(e)}")
            
            # تأخير بين الطلبات
            time.sleep(self.config['delay_between_requests'])
        
        logger.info(f"اكتمل زحف الموقع: {start_url} (تم تنزيل {len(downloaded_files)} صورة)")
        return downloaded_files
    
    def crawl_multiple_sources(self, sources):
        """
        زحف مصادر متعددة لجمع صور الأمراض النباتية
        
        المعلمات:
            sources (list): قائمة بالمصادر، كل مصدر هو قاموس يحتوي على:
                - url: عنوان URL للمصدر
                - category: فئة الصور (vegetables, fruits, crops)
                - max_depth: الحد الأقصى لعمق الزحف
                
        العوائد:
            dict: قاموس بالإحصائيات
        """
        logger.info(f"بدء زحف {len(sources)} مصدر")
        
        # إحصائيات
        stats = {
            'total_sources': len(sources),
            'successful_sources': 0,
            'failed_sources': 0,
            'total_images': 0,
            'images_by_category': {
                'vegetables': 0,
                'fruits': 0,
                'crops': 0,
                'unclassified': 0
            }
        }
        
        # زحف كل مصدر
        for source in sources:
            url = source.get('url')
            category = source.get('category', 'unclassified')
            max_depth = source.get('max_depth', 2)
            
            try:
                # زحف الموقع
                downloaded_files = self.crawl_website(url, category, max_depth)
                
                # تحديث الإحصائيات
                if downloaded_files:
                    stats['successful_sources'] += 1
                    stats['total_images'] += len(downloaded_files)
                    stats['images_by_category'][category] += len(downloaded_files)
                else:
                    stats['failed_sources'] += 1
                    
            except Exception as e:
                logger.error(f"حدث خطأ أثناء زحف المصدر {url}: {str(e)}")
                stats['failed_sources'] += 1
        
        logger.info(f"اكتمل زحف المصادر: {stats}")
        return stats


# نموذج استخدام
if __name__ == "__main__":
    # تكوين الزاحف
    config = {
        'output_dir': 'data/images',
        'max_images_per_source': 50,
        'delay_between_requests': 1.5,
        'min_image_size': 20 * 1024,  # 20 KB
        'max_threads': 3
    }
    
    # إنشاء كائن الزاحف
    crawler = PlantDiseaseImageCrawler(config)
    
    # قائمة المصادر
    sources = [
        {
            'url': 'https://plantvillage.psu.edu/topics/tomato/infos',
            'category': 'vegetables',
            'max_depth': 2
        },
        {
            'url': 'https://www.apsnet.org/edcenter/disandpath/viral/pdlessons/Pages/TomatoSpottedWilt.aspx',
            'category': 'vegetables',
            'max_depth': 1
        },
        {
            'url': 'https://www.canr.msu.edu/resources/apple_scab',
            'category': 'fruits',
            'max_depth': 1
        }
    ]
    
    # زحف المصادر
    stats = crawler.crawl_multiple_sources(sources)
    print(f"إحصائيات الزحف: {stats}")
