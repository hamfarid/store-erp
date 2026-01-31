#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة جمع البيانات من الويب (Web Scraping)
=======================================

توفر هذه الوحدة وظائف لجمع البيانات من صفحات الويب وتحليلها.
تتضمن التعامل مع طلبات HTTP، تحليل HTML، واحترام قواعد robots.txt.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import time
import logging
import random
import hashlib
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup

# إعداد السجل
logger = logging.getLogger("agricultural_ai.web_scraper")


class WebScraper:  # pylint: disable=too-many-instance-attributes
    """فئة لجمع البيانات من الويب"""

    def __init__(self, config: Dict):
        """تهيئة جامع البيانات

        المعاملات:
            config (Dict): تكوين جامع البيانات
        """
        self.config = config.get("web_scraping", {})
        self.user_agent = self.config.get(
            "user_agent", "AgriculturalAI Research Bot/1.0"
        )
        self.request_delay = self.config.get("request_delay", 2)  # ثواني
        self.max_retries = self.config.get("max_retries", 3)
        self.timeout = self.config.get("timeout", 30)  # ثواني
        self.respect_robots = self.config.get("respect_robots_txt", True)
        self.proxy_config = self.config.get("proxy", {})
        self.cache_dir = self.config.get("cache_dir", "cache/web")
        self.cache_enabled = self.config.get("cache_results", True)
        self.cache_expiry = self.config.get("cache_expiry", 604800)  # 7 days

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

        # إعداد الوكيل (Proxy) إذا تم تفعيله
        if self.proxy_config.get("enable") and self.proxy_config.get("list"):
            # اختيار وكيل عشوائي من القائمة
            proxy_url = random.choice(self.proxy_config["list"])
            self.session.proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }
            logger.info("استخدام الوكيل: %s", proxy_url)

        # تهيئة محلل robots.txt
        self.robot_parsers = {}

        # إنشاء مجلد التخزين المؤقت
        if self.cache_enabled:
            os.makedirs(self.cache_dir, exist_ok=True)

        logger.info("تم تهيئة جامع البيانات من الويب")

    def _get_robot_parser(
        self, url: str
    ) -> Optional[robotparser.RobotFileParser]:
        """الحصول على محلل robots.txt لموقع معين"""
        if not self.respect_robots:
            return None

        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = urljoin(base_url, "/robots.txt")

        if base_url in self.robot_parsers:
            return self.robot_parsers[base_url]

        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
            self.robot_parsers[base_url] = rp
            logger.debug("تم تحميل وقراءة robots.txt لـ %s", base_url)
            return rp
        except (OSError, IOError, ValueError) as e:
            logger.warning("فشل في قراءة robots.txt لـ %s: %s", base_url, e)
            # افتراض السماح بالوصول في حالة الفشل
            self.robot_parsers[base_url] = None
            return None

    def _can_fetch(self, url: str) -> bool:
        """التحقق مما إذا كان مسموحًا بجلب عنوان URL بناءً على robots.txt"""
        rp = self._get_robot_parser(url)
        if rp:
            try:
                return rp.can_fetch(self.user_agent, url)
            except (AttributeError, ValueError) as e:
                logger.warning("خطأ أثناء التحقق من robots.txt لـ %s: %s", url, e)
                return True  # السماح افتراضيًا عند حدوث خطأ
        return True  # السماح إذا لم يتم العثور على robots.txt

    def _get_cache_path(self, url: str) -> str:
        """الحصول على مسار ملف التخزين المؤقت لعنوان URL"""
        url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.json")

    def _read_cache(self, url: str) -> Optional[Dict]:
        """قراءة البيانات من التخزين المؤقت"""
        if not self.cache_enabled:
            return None

        cache_path = self._get_cache_path(url)
        if os.path.exists(cache_path):
            try:
                # التحقق من عمر الملف المؤقت
                file_mod_time = os.path.getmtime(cache_path)
                if time.time() - file_mod_time < self.cache_expiry:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        cached_data = json.load(f)
                    logger.info(
                        "تم العثور على بيانات في التخزين المؤقت لـ %s", url
                    )
                    return cached_data
                logger.info("انتهت صلاحية التخزين المؤقت لـ %s", url)
                os.remove(cache_path)  # حذف الملف منتهي الصلاحية
            except (OSError, IOError, json.JSONDecodeError) as e:
                logger.error("فشل في قراءة التخزين المؤقت لـ %s: %s", url, e)
        return None

    def _write_cache(self, url: str, data: Dict):
        """كتابة البيانات إلى التخزين المؤقت"""
        if not self.cache_enabled:
            return

        cache_path = self._get_cache_path(url)
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info("تم حفظ بيانات %s في التخزين المؤقت", url)
        except (OSError, IOError, TypeError) as e:
            logger.error("فشل في كتابة التخزين المؤقت لـ %s: %s", url, e)

    def fetch_page(self, url: str) -> Optional[str]:
        """جلب محتوى صفحة ويب

        المعاملات:
            url (str): عنوان URL للصفحة

        الإرجاع:
            Optional[str]: محتوى HTML للصفحة أو None في حالة الفشل
        """
        # التحقق من التخزين المؤقت أولاً
        cached_data = self._read_cache(url)
        if cached_data:
            return cached_data.get("content")

        # التحقق من robots.txt
        if not self._can_fetch(url):
            logger.warning("تم حظر جلب %s بواسطة robots.txt", url)
            return None

        # انتظار التأخير المطلوب
        time.sleep(self.request_delay)

        # محاولة جلب الصفحة مع إعادة المحاولة
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()  # إثارة خطأ لحالات HTTP غير الناجحة

                # التحقق من نوع المحتوى
                content_type = response.headers.get("Content-Type", "").lower()
                if "text/html" not in content_type:
                    logger.warning(
                        "نوع محتوى غير متوقع لـ %s: %s", url, content_type
                    )
                    return None  # أو التعامل مع أنواع أخرى إذا لزم الأمر

                # الحصول على المحتوى
                content = response.text
                logger.info(
                    "تم جلب الصفحة بنجاح: %s (الحجم: %d بايت)", url, len(content)
                )

                # حفظ في التخزين المؤقت
                cache_data = {
                    "url": url,
                    "content": content,
                    "timestamp": time.time()
                }
                self._write_cache(url, cache_data)

                return content

            except requests.exceptions.RequestException as e:
                retry_info = f"{attempt + 1}/{self.max_retries}"
                logger.warning(
                    "فشل في جلب %s (المحاولة %s): %s", url, retry_info, e
                )
                if attempt < self.max_retries - 1:
                    # زيادة التأخير بين المحاولات
                    time.sleep(self.request_delay * (attempt + 1))
                else:
                    logger.error(
                        "فشل في جلب %s بعد %d محاولات", url, self.max_retries
                    )
                    return None
        return None  # يجب ألا يتم الوصول إليه

    def parse_html(
        self, html_content: str, url: str
    ) -> Optional[BeautifulSoup]:
        """تحليل محتوى HTML باستخدام BeautifulSoup

        المعاملات:
            html_content (str): محتوى HTML
            url (str): عنوان URL الأصلي (لحل الروابط النسبية)

        الإرجاع:
            Optional[BeautifulSoup]: كائن BeautifulSoup أو None في حالة الفشل
        """
        if not html_content:
            return None
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            # حل الروابط النسبية
            soup.url = url  # إضافة خاصية url إلى الكائن
            for tag in soup.find_all(href=True):
                tag["href"] = urljoin(url, tag["href"])
            for tag in soup.find_all(src=True):
                tag["src"] = urljoin(url, tag["src"])

            return soup
        except (ValueError, TypeError, AttributeError) as e:
            logger.error("فشل في تحليل HTML لـ %s: %s", url, e)
            return None

    def extract_text(self, soup: BeautifulSoup) -> str:
        """استخراج النص النظيف من كائن BeautifulSoup"""
        if not soup:
            return ""

        # إزالة عناصر الـ script والـ style
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # الحصول على النص
        text = soup.get_text()

        # تنظيف النص (إزالة الأسطر الفارغة الزائدة والمسافات البيضاء)
        lines = (line.strip() for line in text.splitlines())
        chunks = (
            phrase.strip() for line in lines for phrase in line.split("  ")
        )
        text = "\n".join(chunk for chunk in chunks if chunk)

        return text

    def extract_links(
        self, soup: BeautifulSoup, same_domain: bool = True
    ) -> List[str]:
        """استخراج الروابط من كائن BeautifulSoup"""
        if not soup or not hasattr(soup, "url"):
            return []

        links = set()
        base_domain = urlparse(soup.url).netloc

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            parsed_href = urlparse(href)

            # تجاهل الروابط غير الصالحة أو التي تشير إلى نفس الصفحة
            valid_schemes = ["http", "https"]
            if not parsed_href.scheme or parsed_href.scheme not in valid_schemes:
                continue
            if href == soup.url or href.endswith("#"):
                continue

            # التحقق من النطاق إذا كان مطلوبًا
            if same_domain and parsed_href.netloc != base_domain:
                continue

            links.add(href)

        return list(links)

    def extract_specific_data(
        self, soup: BeautifulSoup, selectors: Dict[str, str]
    ) -> Dict[str, Optional[str]]:
        """استخراج بيانات محددة باستخدام محددات CSS

        المعاملات:
            soup (BeautifulSoup): كائن BeautifulSoup
            selectors (Dict[str, str]): قاموس يربط بين اسم الحقل ومحدد CSS

        الإرجاع:
            Dict[str, Optional[str]]: قاموس بالبيانات المستخرجة
        """
        if not soup:
            return {key: None for key in selectors}

        extracted_data = {}
        for field_name, selector in selectors.items():
            element = soup.select_one(selector)
            if element:
                # محاولة الحصول على النص أو خاصية معينة (مثل src للصورة)
                if element.name == "img" and element.has_attr("src"):
                    extracted_data[field_name] = element["src"]
                elif element.has_attr("content"):
                    extracted_data[field_name] = element["content"].strip()
                else:
                    extracted_data[field_name] = element.get_text(strip=True)
            else:
                extracted_data[field_name] = None
                logger.debug("لم يتم العثور على العنصر للمحدد: %s", selector)

        return extracted_data

    def scrape_url(
        self,
        url: str,
        extract_text_content: bool = True,
        extract_links_list: bool = False,
        specific_selectors: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """جلب وتحليل واستخراج بيانات من عنوان URL واحد

        المعاملات:
            url (str): عنوان URL للصفحة
            extract_text_content (bool): استخراج النص النظيف
            extract_links_list (bool): استخراج قائمة الروابط
            specific_selectors (Dict, optional): محددات CSS لاستخراج بيانات محددة

        الإرجاع:
            Dict[str, Any]: قاموس يحتوي على البيانات المستخرجة
        """
        result = {
            "url": url,
            "status": "failure",
            "error_message": None,
            "content": None,
            "text": None,
            "links": None,
            "specific_data": None
        }

        html_content = self.fetch_page(url)
        if not html_content:
            result["error_message"] = (
                "Failed to fetch page content or blocked by robots.txt"
            )
            return result

        result["content"] = html_content  # تضمين المحتوى الخام إذا لزم الأمر

        soup = self.parse_html(html_content, url)
        if not soup:
            result["error_message"] = "Failed to parse HTML content"
            return result

        result["status"] = "success"

        if extract_text_content:
            result["text"] = self.extract_text(soup)

        if extract_links_list:
            result["links"] = self.extract_links(soup)

        if specific_selectors:
            result["specific_data"] = self.extract_specific_data(
                soup, specific_selectors
            )

        return result


# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # تكوين وهمي
    dummy_config = {
        "web_scraping": {
            "user_agent": "Manus Test Scraper/1.0",
            "request_delay": 1,
            "max_retries": 2,
            "timeout": 10,
            "respect_robots_txt": True,
            "cache_enabled": True,
            "cache_dir": "../../cache/web",  # مسار نسبي
            "cache_expiry": 3600  # ساعة واحدة
        }
    }

    # تهيئة الجامع
    scraper = WebScraper(dummy_config)

    # مثال لجلب وتحليل صفحة
    TEST_URL = "https://httpbin.org/html"  # صفحة اختبار بسيطة

    print(f"\nجاري جلب وتحليل: {TEST_URL}")
    scrape_result = scraper.scrape_url(
        TEST_URL,
        extract_text_content=True,
        extract_links_list=True,
        specific_selectors={"title": "h1", "first_paragraph": "p"}
    )

    if scrape_result["status"] == "success":
        print("تم الجلب والتحليل بنجاح!")
        specific_data = scrape_result.get('specific_data', {})
        print(f"العنوان المستخرج: {specific_data.get('title')}")
        text_preview = scrape_result.get('text', '')[:100]
        print(f"النص المستخرج (أول 100 حرف): {text_preview}...")
        links_count = len(scrape_result.get('links', []))
        print(f"عدد الروابط المستخرجة: {links_count}")
    else:
        print(f"فشل في الجلب أو التحليل: {scrape_result['error_message']}")

    # مثال آخر مع التخزين المؤقت
    print(f"\nجاري جلب وتحليل نفس الصفحة مرة أخرى: {TEST_URL}")
    scrape_result_cached = scraper.scrape_url(TEST_URL)
    if scrape_result_cached["status"] == "success":
        print("تم الجلب بنجاح (من التخزين المؤقت أو جديد)")
    else:
        print("فشل")
