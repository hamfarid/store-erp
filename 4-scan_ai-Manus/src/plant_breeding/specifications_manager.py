#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مدير مواصفات الأصناف والبحث عن المقالات
=======================================

يوفر هذا المديول وظائف لإدارة مواصفات الأصناف النباتية والبحث عن معلومات
ومقالات علمية ذات صلة عبر الإنترنت.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# استيراد مكونات أخرى (نفترض أنها موجودة في المسار)
# from database.database_manager import DatabaseManager
# from data_collection.comprehensive_search import ComprehensiveInternetSearcher

# إعداد السجل
logger = logging.getLogger("agricultural_ai.specifications_manager")

class SpecificationsManager:
    """فئة لإدارة مواصفات الأصناف والبحث عن المعلومات المتعلقة بها"""
    
    def __init__(self, db_manager, comprehensive_searcher):
        """تهيئة مدير المواصفات
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
            comprehensive_searcher: باحث الإنترنت الشامل
        """
        self.db_manager = db_manager
        self.searcher = comprehensive_searcher
        logger.info("تم تهيئة مدير مواصفات الأصناف")

    def get_specification(self, variety_name_or_id: str) -> Optional[Dict]:
        """استرجاع مواصفات صنف معين من قاعدة البيانات
        
        المعاملات:
            variety_name_or_id (str): اسم الصنف أو معرفه
            
        الإرجاع:
            Optional[Dict]: قاموس يحتوي على مواصفات الصنف، أو None إذا لم يتم العثور عليه
        """
        logger.debug(f"محاولة استرجاع مواصفات الصنف: {variety_name_or_id}")
        try:
            # نفترض وجود طريقة في db_manager للبحث عن المواصفات
            if hasattr(self.db_manager, "find_variety_specification"):
                spec = self.db_manager.find_variety_specification(variety_name_or_id)
                if spec:
                    logger.info(f"تم العثور على مواصفات الصنف: {variety_name_or_id}")
                    return spec
                else:
                    logger.warning(f"لم يتم العثور على مواصفات الصنف في قاعدة البيانات: {variety_name_or_id}")
                    return None
            else:
                logger.error("طريقة find_variety_specification غير موجودة في DatabaseManager")
                return None
        except Exception as e:
            logger.error(f"فشل في استرجاع مواصفات الصنف {variety_name_or_id}: {e}")
            return None

    def search_specifications(self, query_params: Dict) -> List[Dict]:
        """البحث في قاعدة البيانات عن أصناف تطابق معايير معينة
        
        المعاملات:
            query_params (Dict): قاموس بمعايير البحث (مثل {"disease_resistance": "Late Blight"})
            
        الإرجاع:
            List[Dict]: قائمة بالأصناف المطابقة
        """
        logger.debug(f"البحث عن مواصفات أصناف بالمعايير: {query_params}")
        try:
            # نفترض وجود طريقة في db_manager للبحث المتقدم
            if hasattr(self.db_manager, "search_variety_specifications"):
                results = self.db_manager.search_variety_specifications(query_params)
                logger.info(f"تم العثور على {len(results)} أصناف مطابقة للمعايير")
                return results
            else:
                logger.error("طريقة search_variety_specifications غير موجودة في DatabaseManager")
                return []
        except Exception as e:
            logger.error(f"فشل في البحث عن مواصفات الأصناف: {e}")
            return []

    def find_related_articles(self, variety_name: str, max_results: int = 5) -> List[Dict]:
        """البحث عن مقالات ومعلومات عبر الإنترنت حول صنف معين
        
        المعاملات:
            variety_name (str): اسم الصنف للبحث عنه
            max_results (int): الحد الأقصى لعدد النتائج
            
        الإرجاع:
            List[Dict]: قائمة بنتائج البحث من الإنترنت
        """
        logger.debug(f"البحث عن مقالات متعلقة بالصنف: {variety_name}")
        if not self.searcher:
            logger.error("باحث الإنترنت الشامل غير متاح")
            return []
            
        try:
            # صياغة استعلامات بحث متنوعة
            queries = [
                f"مقالات علمية عن صنف {variety_name}",
                f"مواصفات صنف {variety_name}",
                f"{variety_name} disease resistance",
                f"{variety_name} yield trials"
            ]
            
            all_articles = []
            processed_urls = set()
            
            for query in queries:
                if len(all_articles) >= max_results:
                    break
                # استخدام فئات لتحسين البحث
                results = self.searcher.search(query, categories=["article", "specification"], max_total_results=max_results)
                
                for res in results:
                    url = res.get("url")
                    if url and url not in processed_urls:
                        all_articles.append(res)
                        processed_urls.add(url)
                        if len(all_articles) >= max_results:
                            break
                            
            logger.info(f"تم العثور على {len(all_articles)} مقالات/مصادر متعلقة بـ {variety_name}")
            return all_articles
            
        except Exception as e:
            logger.error(f"فشل في البحث عن مقالات متعلقة بـ {variety_name}: {e}")
            return []

    def add_specification(self, spec_data: Dict) -> Optional[str]:
        """إضافة مواصفات صنف جديد إلى قاعدة البيانات
        
        المعاملات:
            spec_data (Dict): قاموس يحتوي على بيانات المواصفات
            
        الإرجاع:
            Optional[str]: معرف الصنف الجديد إذا تمت الإضافة بنجاح، وإلا None
        """
        logger.debug(f"محاولة إضافة مواصفات صنف جديد: {spec_data.get("name")}")
        try:
            # نفترض وجود طريقة في db_manager للإضافة
            if hasattr(self.db_manager, "add_variety_specification"):
                variety_id = self.db_manager.add_variety_specification(spec_data)
                if variety_id:
                    logger.info(f"تمت إضافة مواصفات الصنف بنجاح (المعرف: {variety_id})")
                    return variety_id
                else:
                    logger.error("فشل في إضافة مواصفات الصنف إلى قاعدة البيانات")
                    return None
            else:
                logger.error("طريقة add_variety_specification غير موجودة في DatabaseManager")
                return None
        except Exception as e:
            logger.error(f"فشل في إضافة مواصفات الصنف: {e}")
            return None

    def update_specification(self, variety_id: str, update_data: Dict) -> bool:
        """تحديث مواصفات صنف موجود
        
        المعاملات:
            variety_id (str): معرف الصنف المراد تحديثه
            update_data (Dict): قاموس يحتوي على البيانات المحدثة
            
        الإرجاع:
            bool: True إذا تم التحديث بنجاح، وإلا False
        """
        logger.debug(f"محاولة تحديث مواصفات الصنف (المعرف: {variety_id})")
        try:
            # نفترض وجود طريقة في db_manager للتحديث
            if hasattr(self.db_manager, "update_variety_specification"):
                success = self.db_manager.update_variety_specification(variety_id, update_data)
                if success:
                    logger.info(f"تم تحديث مواصفات الصنف (المعرف: {variety_id}) بنجاح")
                    return True
                else:
                    logger.error(f"فشل في تحديث مواصفات الصنف (المعرف: {variety_id}) في قاعدة البيانات")
                    return False
            else:
                logger.error("طريقة update_variety_specification غير موجودة في DatabaseManager")
                return False
        except Exception as e:
            logger.error(f"فشل في تحديث مواصفات الصنف (المعرف: {variety_id}): {e}")
            return False

    def get_variety_info_package(self, variety_name_or_id: str) -> Dict:
        """الحصول على حزمة معلومات كاملة لصنف معين (مواصفات + مقالات)"""
        logger.info(f"الحصول على حزمة معلومات الصنف: {variety_name_or_id}")
        specification = self.get_specification(variety_name_or_id)
        articles = []
        
        # استخدام الاسم من المواصفات للبحث عن المقالات إذا تم العثور عليها
        variety_name_for_search = variety_name_or_id
        if specification and "name" in specification:
            # قد يكون هناك أسماء متعددة، نختار الأول كمثال
            if isinstance(specification["name"], list) and specification["name"]:
                variety_name_for_search = specification["name"][0]
            elif isinstance(specification["name"], str):
                 variety_name_for_search = specification["name"]
                 
        articles = self.find_related_articles(variety_name_for_search)
        
        return {
            "query": variety_name_or_id,
            "specification": specification,
            "related_articles": articles,
            "retrieved_at": datetime.now().isoformat()
        }

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # --- محاكاة للمكونات الأخرى --- 
    class MockDatabaseManager:
        def __init__(self):
            self.specs = {
                "tomato_v1": {"variety_id": "tomato_v1", "name": "Tomato Variety 1", "disease_resistance": ["Fusarium Wilt"], "yield_potential": "High"},
                "potato_x": {"variety_id": "potato_x", "name": "Potato X", "disease_resistance": ["Late Blight"], "yield_potential": "Medium"}
            }
        def find_variety_specification(self, name_or_id):
            if name_or_id in self.specs:
                return self.specs[name_or_id]
            for spec in self.specs.values():
                if isinstance(spec["name"], str) and spec["name"] == name_or_id:
                    return spec
                elif isinstance(spec["name"], list) and name_or_id in spec["name"]:
                    return spec
            return None
        def search_variety_specifications(self, params):
            results = []
            for spec in self.specs.values():
                match = True
                for key, value in params.items():
                    if key not in spec or spec[key] != value:
                         # تبسيط: البحث عن القيمة ضمن قائمة إذا كانت قائمة
                         if isinstance(spec.get(key), list) and value not in spec[key]:
                             match = False
                             break
                         elif not isinstance(spec.get(key), list) and spec.get(key) != value:
                             match = False
                             break
                if match:
                    results.append(spec)
            return results
        def add_variety_specification(self, data):
            new_id = data.get("variety_id", data.get("name", "unknown").lower().replace(" ", "_"))
            data["variety_id"] = new_id
            self.specs[new_id] = data
            return new_id
        def update_variety_specification(self, variety_id, data):
            if variety_id in self.specs:
                self.specs[variety_id].update(data)
                return True
            return False
            
    class MockComprehensiveSearcher:
        def search(self, query, categories=None, max_total_results=5):
            print(f"[Mock Searcher] Query: {query}, Categories: {categories}")
            results = []
            if "Tomato Variety 1" in query:
                results.append({"url": "https://example.com/tomato_v1_study", "title": "Study on Tomato Variety 1", "snippet": "...", "copyright_info": {"status": "potentially_protected"}})
            if "Potato X" in query:
                 results.append({"url": "https://wikipedia.org/wiki/Potato_X", "title": "Potato X - Wikipedia", "snippet": "...", "copyright_info": {"status": "likely_clear_or_unspecified"}})
            return results[:max_total_results]
    # --- نهاية المحاكاة --- 

    # تهيئة المدير مع المحاكاة
    mock_db = MockDatabaseManager()
    mock_searcher = MockComprehensiveSearcher()
    spec_manager = SpecificationsManager(mock_db, mock_searcher)

    # --- اختبار الوظائف --- 
    print("\n--- اختبار استرجاع مواصفات --- ")
    spec_v1 = spec_manager.get_specification("Tomato Variety 1")
    if spec_v1:
        print(f"تم العثور على مواصفات Tomato Variety 1: {spec_v1}")
    else:
        print("لم يتم العثور على مواصفات Tomato Variety 1")
        
    spec_unknown = spec_manager.get_specification("Unknown Variety")
    if not spec_unknown:
        print("تم التحقق من عدم العثور على صنف غير موجود")

    print("\n--- اختبار البحث عن مواصفات --- ")
    resistant_specs = spec_manager.search_specifications({"disease_resistance": "Late Blight"})
    print(f"أصناف مقاومة لـ Late Blight: {resistant_specs}")

    print("\n--- اختبار البحث عن مقالات --- ")
    articles_v1 = spec_manager.find_related_articles("Tomato Variety 1")
    print(f"مقالات متعلقة بـ Tomato Variety 1: {articles_v1}")

    print("\n--- اختبار إضافة مواصفات --- ")
    new_spec_data = {"name": "Tomato Variety 2", "disease_resistance": ["Verticillium Wilt"], "yield_potential": "Medium"}
    new_id = spec_manager.add_specification(new_spec_data)
    if new_id:
        print(f"تمت إضافة صنف جديد بالمعرف: {new_id}")
        spec_v2 = spec_manager.get_specification(new_id)
        print(f"المواصفات المضافة: {spec_v2}")

    print("\n--- اختبار تحديث مواصفات --- ")
    update_success = spec_manager.update_specification("tomato_v1", {"yield_potential": "Very High"})
    if update_success:
        spec_v1_updated = spec_manager.get_specification("tomato_v1")
        print(f"تم تحديث مواصفات tomato_v1: {spec_v1_updated}")

    print("\n--- اختبار الحصول على حزمة معلومات --- ")
    info_package = spec_manager.get_variety_info_package("Potato X")
    print(f"حزمة معلومات Potato X:")
    print(f"  المواصفات: {info_package.get("specification")}")
    print(f"  المقالات المتعلقة: {info_package.get("related_articles")}")

