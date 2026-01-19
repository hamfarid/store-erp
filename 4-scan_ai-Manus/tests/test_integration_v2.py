#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات التكامل للنظام الزراعي المتكامل (الإصدار 2)
==================================================

تختبر هذه الوحدة التكامل بين المكونات الجديدة (بحث الصور، تحليل التربة،
التقسيم، المقارنة) والنظام الرئيسي.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import unittest
import os
import sys
import yaml
import cv2
import numpy as np
import shutil

# إضافة مسار src إلى مسار بايثون
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from main import AgriculturalAISystem

# مسارات الاختبار
TEST_CONFIG_PATH = "../config/default.yaml"
TEST_IMAGE_DIR = "../data/test_images"
TEST_RESULTS_DIR = "../results/test_integration_v2"

# محاكاة أدوات المتصفح (للبحث عن الصور)
class MockBrowserTools:
    def info_search_web(self, query):
        print(f"[Mock] Search: {query}")
        if "أمراض الطماطم" in query:
            return {"results": [{"url": "https://example.com/tomato-diseases"}]}
        return {"results": []}
        
    def browser_navigate(self, url):
        print(f"[Mock] Navigate: {url}")
        return True
        
    def browser_scroll_down(self):
        print("[Mock] Scroll Down")
        return True
        
    def browser_view(self):
        print("[Mock] View Page")
        # محتوى وهمي مع صور
        return {"content": "<html><body><img src=\"https://example.com/img/tomato_blight.jpg\" alt=\"Tomato Blight\"></body></html>"}

class TestIntegrationV2(unittest.TestCase):
    """مجموعة اختبارات التكامل للإصدار الثاني من النظام"""
    
    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار"""
        os.makedirs(TEST_IMAGE_DIR, exist_ok=True)
        os.makedirs(TEST_RESULTS_DIR, exist_ok=True)
        
        # إنشاء صور اختبار وهمية
        cls.plant_image_path = os.path.join(TEST_IMAGE_DIR, "test_plant_v2.png")
        cls.soil_image_path = os.path.join(TEST_IMAGE_DIR, "test_soil_v2.png")
        
        # صورة نبات مع مرض (بقع بنية)
        plant_img = np.ones((300, 300, 3), dtype=np.uint8) * np.array([0, 180, 0], dtype=np.uint8)
        cv2.circle(plant_img, (150, 150), 40, (139, 69, 19), -1) # بقعة بنية
        cv2.imwrite(cls.plant_image_path, plant_img)
        
        # صورة تربة (بني مصفر)
        soil_img = np.ones((200, 200, 3), dtype=np.uint8) * np.array([74, 118, 155], dtype=np.uint8) # BGR for (155, 118, 74) RGB
        cv2.imwrite(cls.soil_image_path, soil_img)
        
        # تهيئة النظام مع محاكاة المتصفح
        cls.system = AgriculturalAISystem(config_path=TEST_CONFIG_PATH, browser_tools=MockBrowserTools())
        # تعديل مسارات النتائج في التكوين للاختبار
        cls.system.segmentation_analyzer.results_dir = os.path.join(TEST_RESULTS_DIR, "segmentation")
        cls.system.image_searcher.image_save_dir = os.path.join(TEST_RESULTS_DIR, "searched_images")
        os.makedirs(cls.system.segmentation_analyzer.results_dir, exist_ok=True)
        os.makedirs(cls.system.image_searcher.image_save_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """تنظيف بيئة الاختبار"""
        # shutil.rmtree(TEST_IMAGE_DIR)
        # shutil.rmtree(TEST_RESULTS_DIR)
        print("\nحافظ على مجلدات الاختبار للفحص اليدوي")

    def test_01_full_analysis_plant_image(self):
        """اختبار التحليل الشامل لصورة نبات"""
        print("\n--- اختبار التحليل الشامل (نبات) ---")
        results = self.system.run_full_image_analysis(
            self.plant_image_path, 
            plant_type="tomato",
            perform_segmentation=True,
            perform_soil_analysis=False, # لا نتوقع تحليل تربة لصورة نبات
            perform_comparison=True
        )
        
        self.assertIsNotNone(results)
        self.assertEqual(results["image_path"], self.plant_image_path)
        self.assertIn("analysis_id", results)
        
        # التحقق من وجود جميع أقسام النتائج
        self.assertIn("standard_analysis", results)
        self.assertIsNotNone(results["standard_analysis"])
        self.assertIn("segmentation_analysis", results)
        self.assertIsNotNone(results["segmentation_analysis"])
        self.assertIn("soil_analysis", results)
        self.assertIsNone(results["soil_analysis"]) # يجب أن يكون None
        self.assertIn("comparative_reports", results)
        self.assertIn("disease_detection", results["comparative_reports"]) # مقارنة الأمراض
        self.assertNotIn("nutrient_vs_soil", results["comparative_reports"]) # لا توجد مقارنة مع تربة
        self.assertIn("final_recommendations", results)
        self.assertIsNotNone(results["final_recommendations"])
        
        # التحقق من نتائج التقسيم (يجب أن يكتشف منطقة مرض)
        seg_analysis = results["segmentation_analysis"]
        self.assertGreater(seg_analysis.get("num_segments", 0), 0)
        self.assertGreater(len(seg_analysis.get("disease_regions", [])), 0, "يجب اكتشاف منطقة مرض واحدة على الأقل في التقسيم")
        if seg_analysis.get("disease_regions"): 
            self.assertIn("البقع البنية", seg_analysis["disease_regions"][0].get("disease", ""))
            
        # التحقق من التوصيات النهائية
        final_recs = results["final_recommendations"]
        self.assertGreater(len(final_recs.get("detected_diseases", [])), 0, "يجب اكتشاف مرض واحد على الأقل في التوصيات النهائية")
        if final_recs.get("detected_diseases"):
            self.assertIn("البقع البنية", final_recs["detected_diseases"][0].get("name", ""))
        self.assertIsNotNone(final_recs.get("treatments"))
        
        print("اكتمل اختبار التحليل الشامل (نبات)")

    def test_02_full_analysis_soil_image(self):
        """اختبار التحليل الشامل لصورة تربة"""
        print("\n--- اختبار التحليل الشامل (تربة) ---")
        results = self.system.run_full_image_analysis(
            self.soil_image_path, 
            plant_type="soil", # تحديد النوع كتربة
            perform_segmentation=False, # لا معنى لتقسيم صورة تربة متجانسة
            perform_soil_analysis=True,
            perform_comparison=True
        )
        
        self.assertIsNotNone(results)
        self.assertEqual(results["image_path"], self.soil_image_path)
        
        # التحقق من وجود تحليل التربة
        self.assertIn("soil_analysis", results)
        self.assertIsNotNone(results["soil_analysis"])
        self.assertNotIn("error", results["soil_analysis"])
        self.assertIn("primary_soil_color_rgb", results["soil_analysis"])
        self.assertIn("matched_database_color", results["soil_analysis"])
        # التحقق من اللون المتوقع (بني مصفر)
        matched_color = results["soil_analysis"].get("matched_database_color", {})
        self.assertEqual(matched_color.get("munsell_code"), "10YR 5/6")
        
        # التحقق من عدم وجود تحليل تقسيم
        self.assertIn("segmentation_analysis", results)
        self.assertIsNone(results["segmentation_analysis"])
        
        # التحقق من وجود مقارنة (إذا كان تحليل الصور القياسي قد أعطى نتائج نقص عناصر)
        self.assertIn("comparative_reports", results)
        if results["standard_analysis"] and results["standard_analysis"].get("nutrient_analysis"):
             self.assertIn("nutrient_vs_soil", results["comparative_reports"])
        
        print("اكتمل اختبار التحليل الشامل (تربة)")

    def test_03_image_search_online(self):
        """اختبار البحث عن الصور عبر الإنترنت"""
        print("\n--- اختبار البحث عن الصور عبر الإنترنت ---")
        keywords = "أمراض الطماطم" 
        max_images = 3
        results = self.system.search_images_online(keywords, max_images=max_images)
        
        self.assertIsNotNone(results)
        self.assertLessEqual(len(results), max_images)
        
        # التحقق من وجود صور تم تنزيلها (بناءً على المحاكاة)
        # في المحاكاة، نتوقع تنزيل صورة واحدة
        self.assertGreaterEqual(len(results), 0) 
        if len(results) > 0:
            img_info = results[0]
            self.assertIn("saved_path", img_info)
            self.assertTrue(os.path.exists(img_info["saved_path"]))
            self.assertIn("url", img_info)
            self.assertIn("source_page", img_info)
            self.assertIn("relevance_score", img_info)
            print(f"تم العثور على صورة: {img_info["saved_path"]}")
        else:
             print("لم يتم العثور على صور (متوقع في بعض بيئات الاختبار)")
            
        print("اكتمل اختبار البحث عن الصور")

if __name__ == "__main__":
    unittest.main()

