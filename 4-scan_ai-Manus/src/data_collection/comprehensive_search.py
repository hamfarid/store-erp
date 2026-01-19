#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام البحث الشامل عبر الإنترنت
=============================

يوفر هذا المديول وظائف للبحث الشامل عبر الإنترنت عن معلومات زراعية متنوعة
(أمراض، تشوهات، تربة، نقص عناصر، مواصفات، مقالات) باستخدام كلمات مفتاحية.
يتضمن التحقق من موثوقية المصادر ومحاولة تحديد معلومات حقوق النشر.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import logging
import time
import re
from urllib.parse import urlparse
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# استيراد مكونات أخرى
# from src.data_collection.source_verifier import SourceVerifier

# إعداد السجل
logger = logging.getLogger("agricultural_ai.comprehensive_search")

# تعابير منتظمة للبحث عن إشعارات حقوق النشر
COPYRIGHT_PATTERNS = [
    re.compile(r"copyright|©|&copy;", re.IGNORECASE),
    re.compile(r"all rights reserved", re.IGNORECASE),
    re.compile(r"rights reserved", re.IGNORECASE)
]

class ComprehensiveInternetSearcher:
    """فئة للبحث الشامل عبر الإنترنت"""
    
    def __init__(self, config: Dict, source_verifier=None, browser_tools=None, info_search_tool=None):
        """تهيئة الباحث الشامل
        
        المعاملات:
            config (Dict): تكوين الباحث
            source_verifier: كائن للتحقق من موثوقية المصادر
            browser_tools: أدوات المتصفح (للتصفح والتحليل)
            info_search_tool: أداة البحث على الويب (مثل info_search_web)
        """
        self.config = config.get("comprehensive_search", {})
        self.source_verifier = source_verifier
        self.browser_tools = browser_tools
        self.info_search_tool = info_search_tool
        
        # إعدادات البحث
        self.max_results_per_query = self.config.get("max_results_per_query", 10)
        self.search_timeout = self.config.get("search_timeout_seconds", 10)
        self.page_analysis_depth = self.config.get("page_analysis_depth", 1) # 0: لا تحليل, 1: تحليل أساسي, 2: تحليل متعمق (تصفح)
        self.min_reliability_threshold = self.config.get("min_reliability_threshold", 0.3)
        
        logger.info("تم تهيئة الباحث الشامل عبر الإنترنت")

    def search(self, keywords: Union[str, List[str]], 
               categories: Optional[List[str]] = None, 
               max_total_results: int = 20) -> List[Dict]:
        """إجراء بحث شامل عبر الإنترنت
        
        المعاملات:
            keywords (Union[str, List[str]]): الكلمات المفتاحية (نص واحد أو قائمة)
            categories (Optional[List[str]]): الفئات المستهدفة (مثل ["disease", "soil", "article"])
            max_total_results (int): الحد الأقصى لإجمالي النتائج المراد إرجاعها
            
        الإرجاع:
            List[Dict]: قائمة بالنتائج التي تم العثور عليها
        """
        start_time = time.time()
        logger.info(f"بدء البحث الشامل عن: {keywords}, الفئات: {categories}")
        
        if isinstance(keywords, str):
            keywords_list = [keywords]
        else:
            keywords_list = keywords
            
        all_results = []
        processed_urls = set()
        
        for keyword in keywords_list:
            if len(all_results) >= max_total_results:
                break
                
            # صياغة استعلام البحث
            search_query = self._build_search_query(keyword, categories)
            
            # إجراء البحث باستخدام الأداة المتاحة
            try:
                if not self.info_search_tool:
                    logger.error("أداة البحث على الويب غير متاحة")
                    continue
                    
                search_response = self.info_search_tool(query=search_query)
                raw_results = search_response.get("results", []) if search_response else []
                logger.debug(f"تم العثور على {len(raw_results)} نتائج أولية للاستعلام: {search_query}")
                
                # معالجة النتائج الأولية
                for result in raw_results:
                    if len(all_results) >= max_total_results:
                        break
                        
                    url = result.get("url")
                    if not url or url in processed_urls:
                        continue
                        
                    processed_urls.add(url)
                    
                    # تحليل النتيجة الفردية
                    analyzed_result = self._analyze_search_result(result, keyword, categories)
                    if analyzed_result:
                        all_results.append(analyzed_result)
                        
            except Exception as e:
                logger.error(f"فشل في البحث عن الكلمة المفتاحية ", {keyword}": {e}")
                
        logger.info(f"اكتمل البحث الشامل. تم العثور على {len(all_results)} نتائج في {time.time() - start_time:.2f} ثانية")
        
        # يمكن إضافة خطوة لترتيب النتائج النهائية هنا
        return all_results

    def _build_search_query(self, keyword: str, categories: Optional[List[str]]) -> str:
        """بناء استعلام البحث بناءً على الكلمات المفتاحية والفئات"""
        query = keyword
        if categories:
            # إضافة مصطلحات متعلقة بالفئات لتحسين دقة البحث
            category_terms = []
            for cat in categories:
                if cat == "disease": category_terms.append("مرض نبات")
                elif cat == "soil": category_terms.append("نوع تربة")
                elif cat == "nutrient": category_terms.append("نقص عناصر غذائية")
                elif cat == "specification" or cat == "variety": category_terms.append("صنف نبات")
                elif cat == "article": category_terms.append("مقالة علمية")
            if category_terms:
                query += " " + " OR ".join(category_terms)
        return query

    def _analyze_search_result(self, result: Dict, keyword: str, categories: Optional[List[str]]) -> Optional[Dict]:
        """تحليل نتيجة بحث فردية (تحقق من المصدر، تحليل الصفحة)"""
        url = result.get("url")
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        
        # 1. التحقق من موثوقية المصدر
        reliability_score = 0.5 # افتراضي
        verification_notes = "لم يتم التحقق"
        if self.source_verifier:
            try:
                verification = self.source_verifier.verify_source(url, update_db=False) # لا نحدث قاعدة البيانات هنا
                reliability_score = verification.get("reliability_score", 0)
                verification_notes = verification.get("notes", "")
            except Exception as e:
                logger.warning(f"فشل في التحقق من مصدر الرابط {url}: {e}")
                
        # تجاهل المصادر ذات الموثوقية المنخفضة جدًا
        if reliability_score < self.min_reliability_threshold:
            logger.debug(f"تم تجاهل نتيجة من مصدر منخفض الموثوقية: {url} (الموثوقية: {reliability_score})")
            return None
            
        # 2. تحليل محتوى الصفحة (إذا تم التكوين لذلك)
        copyright_info = {"status": "unknown", "mentions": []}
        page_content_summary = snippet # استخدام المقتطف كملخص افتراضي
        
        if self.page_analysis_depth > 0 and self.browser_tools:
            try:
                # التنقل إلى الصفحة باستخدام المتصفح
                if hasattr(self.browser_tools, "browser_navigate"):
                    self.browser_tools.browser_navigate(url=url)
                    time.sleep(2) # انتظار تحميل الصفحة
                    
                    # الحصول على محتوى الصفحة المرئي
                    if hasattr(self.browser_tools, "browser_view"):
                        page_view = self.browser_tools.browser_view()
                        page_text_content = page_view.get("markdown", "") # استخدام المحتوى المستخرج إن وجد
                        if not page_text_content:
                             page_text_content = page_view.get("content", "") # استخدام HTML إذا لم يتوفر markdown
                             
                        if page_text_content:
                            # تحديث ملخص المحتوى (أول 500 حرف مثلاً)
                            page_content_summary = page_text_content[:500].strip() + ("..." if len(page_text_content) > 500 else "")
                            
                            # البحث عن إشارات حقوق النشر
                            copyright_mentions = []
                            for pattern in COPYRIGHT_PATTERNS:
                                matches = pattern.findall(page_text_content)
                                if matches:
                                    copyright_mentions.extend(matches)
                                    
                            if copyright_mentions:
                                copyright_info["status"] = "potentially_protected"
                                copyright_info["mentions"] = list(set(m.lower() for m in copyright_mentions))
                            else:
                                copyright_info["status"] = "likely_clear_or_unspecified"
                                
            except Exception as e:
                logger.warning(f"فشل في تحليل محتوى الصفحة {url} باستخدام المتصفح: {e}")
                # الاستمرار بالمعلومات الأساسية
                
        # 3. تجميع النتيجة النهائية
        analyzed_result = {
            "url": url,
            "title": title,
            "snippet": snippet,
            "content_summary": page_content_summary, # ملخص أطول إذا تم تحليل الصفحة
            "search_keyword": keyword,
            "matched_categories": categories, # الفئات التي تم البحث عنها
            "source_reliability": reliability_score,
            "source_verification_notes": verification_notes,
            "copyright_info": copyright_info,
            "retrieved_at": datetime.now().isoformat()
        }
        
        return analyzed_result

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "comprehensive_search": {
            "max_results_per_query": 5,
            "page_analysis_depth": 1, # تحليل أساسي للصفحة
            "min_reliability_threshold": 0.2
        }
    }
    
    # محاكاة مدقق المصادر
    class MockSourceVerifier:
        def verify_source(self, url, update_db=False):
            if "wikipedia.org" in url:
                return {"reliability_score": 0.8, "notes": "ويكيبيديا (موثوقية عالية نسبيًا)"}
            elif "example.com" in url:
                 return {"reliability_score": 0.5, "notes": "موقع مثال (موثوقية متوسطة)"}
            else:
                return {"reliability_score": 0.1, "notes": "مصدر غير معروف (موثوقية منخفضة)"}
                
    # محاكاة أداة البحث
    class MockInfoSearchTool:
        def __call__(self, query):
            print(f"[Mock] Search Tool Query: {query}")
            results = []
            if "مرض نبات" in query:
                results.append({"url": "https://ar.wikipedia.org/wiki/Late_blight", "title": "اللفحة المتأخرة - ويكيبيديا", "snippet": "اللفحة المتأخرة مرض فطري يصيب البطاطس والطماطم..."})
                results.append({"url": "https://example.com/plant-diseases/blight", "title": "Plant Disease Guide: Blight", "snippet": "Learn about blight symptoms and treatment..."})
                results.append({"url": "https://unreliable-source.net/blight-cure", "title": "Amazing Blight Cure!", "snippet": "Click here for the secret cure..."})
            elif "نوع تربة" in query:
                 results.append({"url": "https://example.com/soil-types/clay", "title": "Clay Soil Characteristics", "snippet": "Clay soil is heavy and retains water..."})
            return {"results": results}
            
    # محاكاة أدوات المتصفح
    class MockBrowserTools:
        def browser_navigate(self, url):
            print(f"[Mock] Navigate: {url}")
            return True
        def browser_view(self):
            print("[Mock] View Page")
            # محتوى وهمي مع إشارة حقوق نشر
            return {"markdown": "هذا محتوى الصفحة. © 2025 Example Inc. All rights reserved.", "content": "<html><body>هذا محتوى الصفحة. © 2025 Example Inc. All rights reserved.</body></html>"}
            
    # تهيئة الباحث مع المحاكاة
    searcher = ComprehensiveInternetSearcher(
        dummy_config,
        source_verifier=MockSourceVerifier(),
        browser_tools=MockBrowserTools(),
        info_search_tool=MockInfoSearchTool()
    )
    
    # اختبار البحث
    print("\n--- اختبار البحث الشامل --- ")
    keywords_to_search = "اللفحة المتأخرة في الطماطم"
    categories_to_search = ["disease", "article"]
    search_results = searcher.search(keywords_to_search, categories=categories_to_search, max_total_results=10)
    
    print(f"\nتم العثور على {len(search_results)} نتائج:")
    for i, res in enumerate(search_results):
        print(f"  {i+1}. {res.get("title", "N/A")}")
        print(f"     الرابط: {res.get("url", "N/A")}")
        print(f"     الموثوقية: {res.get("source_reliability", 0):.2f}")
        print(f"     حقوق النشر: {res.get("copyright_info", {}).get("status", "unknown")}")
        if res.get("copyright_info", {}).get("mentions"):
             print(f"       إشارات: {res["copyright_info"]["mentions"]}")
        print(f"     ملخص المحتوى: {res.get("content_summary", "N/A")[:100]}...")
        
    # اختبار بحث آخر
    print("\n--- اختبار بحث عن نوع تربة --- ")
    keywords_to_search = "التربة الطينية"
    categories_to_search = ["soil"]
    search_results_soil = searcher.search(keywords_to_search, categories=categories_to_search, max_total_results=5)
    print(f"\nتم العثور على {len(search_results_soil)} نتائج:")
    for i, res in enumerate(search_results_soil):
        print(f"  {i+1}. {res.get("title", "N/A")}")
        print(f"     الرابط: {res.get("url", "N/A")}")
        print(f"     الموثوقية: {res.get("source_reliability", 0):.2f}")

