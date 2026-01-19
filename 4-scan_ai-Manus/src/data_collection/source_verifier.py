#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مدقق وموثق المصادر
==================

يوفر هذا المديول وظائف لتقييم موثوقية مصادر الويب وتوثيقها في قاعدة البيانات.
يستخدم قوائم المجالات المعروفة، وتحليل الروابط، وربما تقنيات أخرى لتقدير الموثوقية.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import logging
import re
from urllib.parse import urlparse
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# استيراد مدير قاعدة البيانات
from src.database.database_manager import DatabaseManager

# إعداد السجل
logger = logging.getLogger("agricultural_ai.source_verifier")

class SourceVerifier:
    """فئة لتقييم وتوثيق موثوقية مصادر الويب"""
    
    def __init__(self, config: Dict, db_manager: DatabaseManager):
        """تهيئة مدقق المصادر
        
        المعاملات:
            config (Dict): تكوين مدقق المصادر
            db_manager (DatabaseManager): كائن مدير قاعدة البيانات
        """
        self.config = config.get("source_verification", {})
        self.db_manager = db_manager
        
        # تحميل قوائم المجالات الموثوقة وغير الموثوقة
        self.trusted_domains = set(self.config.get("trusted_domains", [".edu", ".gov", ".org"]))
        self.high_trust_sites = set(self.config.get("high_trust_sites", [
            "wikipedia.org", "fao.org", "usda.gov", "cgiar.org", "plantvillage.psu.edu"
        ]))
        self.low_trust_indicators = set(self.config.get("low_trust_indicators", [
            "blogspot.com", "wordpress.com", "forum", "blog", "personal", "opinion"
        ]))
        
        # أوزان التقييم
        self.weights = {
            "domain_type": self.config.get("weight_domain_type", 0.4),
            "specific_site": self.config.get("weight_specific_site", 0.3),
            "url_path": self.config.get("weight_url_path", 0.1),
            "db_record": self.config.get("weight_db_record", 0.2)
        }
        
        logger.info("تم تهيئة مدقق وموثق المصادر")

    def verify_source(self, url: str, update_db: bool = True) -> Dict:
        """تقييم موثوقية مصدر ويب وتوثيقه في قاعدة البيانات
        
        المعاملات:
            url (str): رابط المصدر
            update_db (bool): تحديث قاعدة البيانات بمعلومات المصدر
            
        الإرجاع:
            Dict: قاموس يحتوي على الرابط، درجة الموثوقية، والملاحظات
        """
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower().replace("www.", "")
            path = parsed_url.path.lower()
            
            if not domain:
                return {"url": url, "reliability_score": 0.0, "notes": "رابط غير صالح أو بدون نطاق"}
                
            # التحقق من وجود المصدر في قاعدة البيانات
            existing_source = self.db_manager.get_trusted_source(url)
            if existing_source and existing_source.get("reliability_score") is not None:
                # إذا كان المصدر موجودًا وله درجة موثوقية، يمكن إرجاعها مباشرة أو إعادة تقييمها
                # هنا سنقوم بإعادة التقييم لتحديث المعلومات
                db_score = existing_source["reliability_score"]
                logger.debug(f"المصدر {url} موجود في قاعدة البيانات بدرجة {db_score}")
            else:
                db_score = None
                
            # حساب درجة الموثوقية بناءً على المؤشرات
            score = 0.0
            notes = []
            
            # 1. تقييم نوع النطاق
            domain_type_score = 0.5 # درجة أساسية
            matched_trusted = False
            for trusted_suffix in self.trusted_domains:
                if domain.endswith(trusted_suffix):
                    domain_type_score = 0.8
                    notes.append(f"نطاق موثوق ({trusted_suffix})")
                    matched_trusted = True
                    break
            if not matched_trusted:
                 notes.append("نطاق غير قياسي (مثل .com, .net)")
                 
            score += domain_type_score * self.weights["domain_type"]
            
            # 2. تقييم الموقع المحدد
            site_score = 0.0
            if domain in self.high_trust_sites:
                site_score = 1.0
                notes.append("موقع ذو ثقة عالية")
            # يمكن إضافة مواقع منخفضة الثقة هنا أيضًا
            # elif domain in self.low_trust_sites:
            #     site_score = 0.1
            #     notes.append("موقع ذو ثقة منخفضة")
            score += site_score * self.weights["specific_site"]
            
            # 3. تقييم مسار الرابط
            path_score = 0.5 # درجة أساسية
            low_trust_found = False
            for indicator in self.low_trust_indicators:
                if indicator in path or indicator in domain:
                    path_score = 0.2
                    notes.append(f"مؤشر ثقة منخفض في المسار/النطاق ({indicator})")
                    low_trust_found = True
                    break
            if not low_trust_found:
                 if "research" in path or "publication" in path or "article" in path:
                      path_score = 0.7
                      notes.append("مسار يشير إلى محتوى بحثي/مقالة")
                      
            score += path_score * self.weights["url_path"]
            
            # 4. دمج درجة قاعدة البيانات (إذا كانت موجودة)
            if db_score is not None:
                score += db_score * self.weights["db_record"]
                notes.append(f"تم الأخذ في الاعتبار درجة قاعدة البيانات السابقة ({db_score:.2f})")
            else:
                # إذا لم يكن المصدر في قاعدة البيانات، نزيد وزن المؤشرات الأخرى قليلاً
                adjustment_factor = 1 / (1 - self.weights["db_record"])
                score *= adjustment_factor
                
            # تطبيع النتيجة بين 0 و 1
            final_score = max(0.0, min(1.0, score))
            
            result = {
                "url": url,
                "domain": domain,
                "reliability_score": round(final_score, 3),
                "notes": ", ".join(notes),
                "verified_at": datetime.now().isoformat()
            }
            
            # تحديث قاعدة البيانات إذا طلب ذلك
            if update_db:
                self.db_manager.add_trusted_source(
                    url=url,
                    domain=domain,
                    reliability_score=result["reliability_score"],
                    notes=result["notes"]
                )
                logger.info(f"تم تقييم وتوثيق المصدر: {url} (الدرجة: {result["reliability_score"]})")
            else:
                logger.info(f"تم تقييم المصدر (بدون توثيق): {url} (الدرجة: {result["reliability_score"]})")
                
            return result
            
        except Exception as e:
            logger.error(f"فشل في تقييم المصدر {url}: {e}")
            return {"url": url, "reliability_score": None, "notes": f"خطأ في التقييم: {e}"}

    def get_reliability_score(self, url: str) -> Optional[float]:
        """الحصول على درجة الموثوقية لمصدر معين (قد يقوم بالتقييم إذا لم يكن موجودًا)"""
        result = self.verify_source(url, update_db=True) # التقييم والتحديث دائمًا عند الاستعلام المباشر
        return result.get("reliability_score")

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي لمدير قاعدة البيانات
    dummy_db_config = {
        "database": {
            "db_path": "../../data/test_agricultural_database_verifier.db",
            "schema_version": 1
        }
    }
    
    # حذف قاعدة البيانات القديمة إذا كانت موجودة للتجربة النظيفة
    if os.path.exists(dummy_db_config["database"]["db_path"]):
        os.remove(dummy_db_config["database"]["db_path"])
        print(f"تم حذف قاعدة البيانات القديمة: {dummy_db_config["database"]["db_path"]}")
        
    # تهيئة مدير قاعدة البيانات
    db_manager = DatabaseManager(dummy_db_config)
    
    # تكوين وهمي لمدقق المصادر
    dummy_verifier_config = {
        "source_verification": {
            "trusted_domains": [".edu", ".gov", ".org"],
            "high_trust_sites": ["wikipedia.org", "fao.org", "usda.gov"],
            "low_trust_indicators": ["blogspot.com", "forum", "blog"],
            "weight_domain_type": 0.4,
            "weight_specific_site": 0.3,
            "weight_url_path": 0.1,
            "weight_db_record": 0.2
        }
    }
    
    # تهيئة مدقق المصادر
    verifier = SourceVerifier(dummy_verifier_config, db_manager)
    
    # --- اختبار تقييم المصادر --- 
    print("\n--- اختبار تقييم المصادر --- ")
    
    urls_to_test = [
        "https://plantvillage.psu.edu/topics/tomato/infos",
        "http://www.fao.org/agriculture/crops/en/",
        "https://en.wikipedia.org/wiki/Tomato",
        "https://www.example-farmer-blog.com/my-tomato-tips",
        "http://gardeningforum.com/threads/help-with-tomatoes.1234/",
        "https://some-random-site.net/plants/info.html",
        "https://research.example.edu/publications/tomato_diseases.pdf"
    ]
    
    results = []
    for url in urls_to_test:
        result = verifier.verify_source(url, update_db=True)
        results.append(result)
        print(f"الرابط: {result["url"]}")
        print(f"  الدرجة: {result["reliability_score"]}")
        print(f"  الملاحظات: {result["notes"]}")
        
    # اختبار الحصول على درجة مصدر موجود
    print("\n--- اختبار الحصول على درجة مصدر موجود --- ")
    url_to_check = "https://en.wikipedia.org/wiki/Tomato"
    score = verifier.get_reliability_score(url_to_check)
    print(f"درجة الموثوقية للرابط {url_to_check}: {score}")
    
    # عرض المصادر الموثوقة من قاعدة البيانات
    print("\n--- المصادر الموثوقة في قاعدة البيانات --- ")
    trusted_sources_from_db = db_manager.list_trusted_sources(min_reliability=0.0)
    for source in trusted_sources_from_db:
        print(f"  - {source["url"]} (الدرجة: {source["reliability_score"]})")
        
    # إغلاق الاتصال بقاعدة البيانات
    db_manager.close_connection()
    
    # تنظيف الملفات الوهمية (اختياري)
    # if os.path.exists(dummy_db_config["database"]["db_path"]):
    #     os.remove(dummy_db_config["database"]["db_path"])
    #     print("\nتم حذف قاعدة بيانات الاختبار")
