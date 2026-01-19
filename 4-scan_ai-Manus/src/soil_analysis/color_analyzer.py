#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
محلل لون التربة
===============

يوفر هذا المديول وظائف لتحليل لون التربة من الصور لتقدير بعض خصائصها.
يستخدم تقنيات معالجة الصور لاستخراج الألوان السائدة ومقارنتها بمعايير معروفة.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import cv2
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from sklearn.cluster import KMeans

# إعداد السجل
logger = logging.getLogger("agricultural_ai.soil_color_analyzer")

class SoilColorAnalyzer:
    """فئة لتحليل لون التربة من الصور"""
    
    def __init__(self, config: Dict):
        """تهيئة محلل لون التربة
        
        المعاملات:
            config (Dict): تكوين محلل لون التربة
        """
        self.config = config.get("soil_analysis", {})
        self.num_dominant_colors = self.config.get("num_dominant_colors", 5)
        self.min_soil_area_ratio = self.config.get("min_soil_area_ratio", 0.1) # الحد الأدنى لنسبة مساحة التربة المفترضة
        
        # تحميل قاعدة بيانات ألوان التربة (مثال بسيط، يمكن توسيعه)
        # يستخدم نظام Munsell كمثال، لكن يتطلب بيانات حقيقية
        self.soil_color_database = self._load_soil_color_database()
        
        logger.info("تم تهيئة محلل لون التربة")

    def _load_soil_color_database(self) -> Dict:
        """تحميل قاعدة بيانات مرجعية لألوان التربة وخصائصها (مثال)"""
        # هذا مثال مبسط جدًا. قاعدة بيانات حقيقية ستكون أكثر تعقيدًا
        # وتعتمد على نظام Munsell أو أنظمة أخرى.
        # القيم هنا هي قيم RGB تقريبية للمثال فقط.
        return {
            "10YR 3/2": {"rgb": (85, 68, 53), "description": "بني داكن جداً", "properties": "عالي المادة العضوية، رطوبة جيدة"},
            "10YR 5/6": {"rgb": (155, 118, 74), "description": "بني مصفر", "properties": "مادة عضوية متوسطة، تصريف جيد"},
            "7.5YR 6/8": {"rgb": (190, 115, 60), "description": "بني محمر قوي", "properties": "محتوى حديد عالي، قد يكون تصريف جيد"},
            "5Y 7/1": {"rgb": (180, 180, 170), "description": "رمادي فاتح", "properties": "مادة عضوية منخفضة، قد يكون تصريف سيء أو تشبع بالماء"},
            "N 2/0": {"rgb": (50, 50, 50), "description": "أسود", "properties": "مادة عضوية عالية جداً، غالبًا تربة مستنقعات"}
            # ... يجب إضافة المزيد من الإدخالات بناءً على بيانات حقيقية
        }

    def analyze_soil_image(self, image_path: str) -> Dict:
        """تحليل صورة التربة لاستخراج اللون السائد وتقدير الخصائص
        
        المعاملات:
            image_path (str): مسار صورة التربة
            
        الإرجاع:
            Dict: نتائج التحليل (اللون السائد، الخصائص المقدرة)
        """
        start_time = time.time()
        logger.info(f"بدء تحليل لون التربة للصورة: {image_path}")
        
        if not os.path.exists(image_path):
            logger.error(f"الصورة غير موجودة: {image_path}")
            return {"error": "Image not found"}
            
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"فشل في قراءة الصورة: {image_path}")
                return {"error": "Failed to read image"}
                
            # تغيير حجم الصورة لتسريع المعالجة (اختياري)
            height, width, _ = image.shape
            max_dim = 600
            if height > max_dim or width > max_dim:
                scale = max_dim / max(height, width)
                image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                
            # تحويل الصورة إلى مساحة ألوان RGB (OpenCV يقرأ BGR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # إعادة تشكيل الصورة إلى قائمة بكسلات
            pixels = image_rgb.reshape((-1, 3))
            
            # استخدام K-Means للعثور على الألوان السائدة
            kmeans = KMeans(n_clusters=self.num_dominant_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # الحصول على الألوان السائدة ونسبها
            unique_labels, counts = np.unique(kmeans.labels_, return_counts=True)
            total_pixels = pixels.shape[0]
            dominant_colors = []
            for i, count in enumerate(counts):
                color_rgb = tuple(map(int, kmeans.cluster_centers_[i]))
                percentage = (count / total_pixels) * 100
                dominant_colors.append({"rgb": color_rgb, "percentage": percentage})
                
            # فرز الألوان حسب النسبة المئوية (تنازليًا)
            dominant_colors.sort(key=lambda x: x["percentage"], reverse=True)
            
            # افتراض أن اللون الأكثر سيطرة هو لون التربة (يمكن تحسين هذا الافتراض)
            primary_soil_color = dominant_colors[0]
            
            # البحث عن أقرب لون في قاعدة البيانات
            matched_color_info = self._find_closest_color(primary_soil_color["rgb"])
            
            # تجميع النتائج
            analysis_result = {
                "dominant_colors": dominant_colors,
                "primary_soil_color_rgb": primary_soil_color["rgb"],
                "primary_soil_color_percentage": primary_soil_color["percentage"],
                "matched_database_color": matched_color_info,
                "estimated_properties": matched_color_info.get("properties", "غير قادر على التقدير") if matched_color_info else "غير قادر على التقدير",
                "processing_time": time.time() - start_time
            }
            
            logger.info(f"اكتمل تحليل لون التربة. اللون السائد: {primary_soil_color["rgb"]}")
            return analysis_result
            
        except Exception as e:
            logger.exception(f"فشل في تحليل لون التربة للصورة {image_path}: {e}")
            return {"error": f"Failed to analyze soil color: {str(e)}"}

    def _find_closest_color(self, target_rgb: Tuple[int, int, int]) -> Optional[Dict]:
        """البحث عن أقرب لون في قاعدة البيانات باستخدام المسافة الإقليدية"""
        min_distance = float("inf")
        closest_match = None
        
        target_np = np.array(target_rgb)
        
        for munsell_code, data in self.soil_color_database.items():
            db_rgb_np = np.array(data["rgb"])
            distance = np.linalg.norm(target_np - db_rgb_np)
            
            if distance < min_distance:
                min_distance = distance
                closest_match = {
                    "munsell_code": munsell_code,
                    "description": data["description"],
                    "properties": data["properties"],
                    "database_rgb": data["rgb"],
                    "distance": distance
                }
                
        # يمكن إضافة حد أقصى للمسافة لاعتبار المطابقة صالحة
        if closest_match and closest_match["distance"] > self.config.get("max_color_distance_threshold", 100):
             logger.warning(f"المسافة إلى أقرب لون في قاعدة البيانات كبيرة ({closest_match["distance"]}), قد تكون المطابقة غير دقيقة")
             # قد نختار عدم إرجاع أي تطابق إذا كانت المسافة كبيرة جدًا
             # return None
             
        return closest_match

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "soil_analysis": {
            "num_dominant_colors": 5,
            "max_color_distance_threshold": 100
        }
    }
    
    # تهيئة المحلل
    analyzer = SoilColorAnalyzer(dummy_config)
    
    # إنشاء صورة تربة وهمية (بني مصفر)
    test_image_path = "test_soil_image.png"
    soil_color = (155, 118, 74) # بني مصفر (قريب من 10YR 5/6)
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    # ملء الصورة باللون مع بعض التشويش
    noise = np.random.randint(-10, 10, image.shape, dtype=np.int16)
    image = np.clip(image + soil_color + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(test_image_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    print(f"تم إنشاء صورة تربة اختبار وهمية: {test_image_path}")
    
    # تحليل الصورة
    print("\n--- تحليل صورة التربة --- ")
    result = analyzer.analyze_soil_image(test_image_path)
    
    if "error" not in result:
        print(f"اللون السائد (RGB): {result["primary_soil_color_rgb"]}")
        print(f"النسبة المئوية: {result["primary_soil_color_percentage"]:.2f}%")
        if result["matched_database_color"]:
            match = result["matched_database_color"]
            print(f"أقرب لون في قاعدة البيانات: {match["munsell_code"]} ({match["description"]})")
            print(f"  المسافة: {match["distance"]:.2f}")
            print(f"الخصائص المقدرة: {result["estimated_properties"]}")
        else:
            print("لم يتم العثور على لون مطابق في قاعدة البيانات")
    else:
        print(f"فشل التحليل: {result["error"]}")
        
    # تنظيف الملف الوهمي
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
        print(f"\nتم حذف صورة الاختبار: {test_image_path}")

