#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام تقسيم الصور للكشف عن الأمراض
================================

يوفر هذا المديول وظائف متقدمة لتقسيم صور النباتات والبحث عن التشوهات والأمراض
باستخدام تقنيات معالجة الصور والتعلم العميق.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import cv2
import numpy as np
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import uuid

# إعداد السجل
logger = logging.getLogger("agricultural_ai.image_segmentation")

class ImageSegmentationAnalyzer:
    """فئة لتقسيم الصور والكشف عن الأمراض والتشوهات"""
    
    def __init__(self, config: Dict, models_dir: str = "models"):
        """تهيئة محلل تقسيم الصور
        
        المعاملات:
            config (Dict): تكوين محلل تقسيم الصور
            models_dir (str): مسار مجلد النماذج
        """
        self.config = config.get("image_segmentation", {})
        self.models_dir = models_dir
        self.results_dir = self.config.get("results_dir", "results/segmentation")
        
        # إنشاء مجلد النتائج إذا لم يكن موجودًا
        os.makedirs(self.results_dir, exist_ok=True)
        
        # تحميل النماذج
        self.segmentation_model = self._load_segmentation_model()
        self.disease_detection_model = self._load_disease_detection_model()
        
        # إعدادات التقسيم
        self.min_segment_size = self.config.get("min_segment_size", 100) # الحد الأدنى لحجم القطعة بالبكسل
        self.disease_confidence_threshold = self.config.get("disease_confidence_threshold", 0.7) # حد الثقة للكشف عن المرض
        
        logger.info("تم تهيئة محلل تقسيم الصور")

    def _load_segmentation_model(self):
        """تحميل نموذج تقسيم الصور"""
        try:
            # هنا يمكن تحميل نموذج حقيقي مثل U-Net أو Mask R-CNN
            # لأغراض هذا المثال، سنستخدم محاكاة بسيطة
            logger.info("تحميل نموذج تقسيم الصور")
            return "segmentation_model_mock"
        except Exception as e:
            logger.error(f"فشل في تحميل نموذج تقسيم الصور: {e}")
            return None

    def _load_disease_detection_model(self):
        """تحميل نموذج الكشف عن الأمراض"""
        try:
            # هنا يمكن تحميل نموذج حقيقي مثل CNN مدرب على تصنيف أمراض النبات
            # لأغراض هذا المثال، سنستخدم محاكاة بسيطة
            logger.info("تحميل نموذج الكشف عن الأمراض")
            return "disease_detection_model_mock"
        except Exception as e:
            logger.error(f"فشل في تحميل نموذج الكشف عن الأمراض: {e}")
            return None

    def analyze_image(self, image_path: str, save_visualization: bool = True) -> Dict:
        """تحليل صورة النبات لتقسيمها والكشف عن الأمراض
        
        المعاملات:
            image_path (str): مسار صورة النبات
            save_visualization (bool): حفظ صورة توضيحية للنتائج
            
        الإرجاع:
            Dict: نتائج التحليل (القطع، الأمراض المكتشفة)
        """
        start_time = time.time()
        analysis_id = str(uuid.uuid4())[:8]
        logger.info(f"بدء تحليل تقسيم الصورة: {image_path} (معرف: {analysis_id})")
        
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
            max_dim = 800
            if height > max_dim or width > max_dim:
                scale = max_dim / max(height, width)
                image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                height, width, _ = image.shape
                
            # تحويل الصورة إلى مساحة ألوان RGB (OpenCV يقرأ BGR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # 1. تقسيم الصورة
            segments = self._segment_image(image_rgb)
            
            # 2. تحليل كل قطعة للكشف عن الأمراض
            segments_analysis = []
            disease_regions = []
            
            for i, segment in enumerate(segments):
                segment_analysis = self._analyze_segment(image_rgb, segment, i)
                segments_analysis.append(segment_analysis)
                
                # إذا تم اكتشاف مرض في هذه القطعة، أضفها إلى قائمة مناطق المرض
                if segment_analysis.get("disease_detected", False):
                    disease_regions.append({
                        "segment_id": i,
                        "disease": segment_analysis["disease_name"],
                        "confidence": segment_analysis["disease_confidence"],
                        "bbox": segment_analysis["bbox"],
                        "area_percentage": segment_analysis["area_percentage"]
                    })
            
            # 3. إنشاء صورة توضيحية (اختياري)
            visualization_path = None
            if save_visualization:
                visualization_path = os.path.join(self.results_dir, f"segmentation_{analysis_id}.jpg")
                self._create_visualization(image_rgb, segments, disease_regions, visualization_path)
            
            # 4. تجميع النتائج
            analysis_result = {
                "analysis_id": analysis_id,
                "timestamp": datetime.now().isoformat(),
                "image_path": image_path,
                "image_dimensions": {"width": width, "height": height},
                "num_segments": len(segments),
                "segments_analysis": segments_analysis,
                "disease_regions": disease_regions,
                "visualization_path": visualization_path,
                "processing_time": time.time() - start_time
            }
            
            logger.info(f"اكتمل تحليل تقسيم الصورة. تم اكتشاف {len(disease_regions)} مناطق مرض.")
            return analysis_result
            
        except Exception as e:
            logger.exception(f"فشل في تحليل تقسيم الصورة {image_path}: {e}")
            return {"error": f"Failed to analyze image: {str(e)}"}

    def _segment_image(self, image: np.ndarray) -> List[Dict]:
        """تقسيم الصورة إلى مناطق
        
        في التنفيذ الحقيقي، يمكن استخدام خوارزميات مثل:
        - تقسيم المياه (Watershed)
        - K-means للألوان
        - نماذج التعلم العميق مثل U-Net
        
        هنا نستخدم تقسيم بسيط باستخدام تحويل الألوان وعتبة التقسيم
        """
        segments = []
        
        try:
            # تحويل الصورة إلى مساحة ألوان HSV (أفضل للتقسيم)
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # استخدام قناة التشبع للمساعدة في تمييز النبات عن الخلفية
            saturation = hsv[:, :, 1]
            
            # تطبيق عتبة التقسيم البسيطة
            _, thresh = cv2.threshold(saturation, 30, 255, cv2.THRESH_BINARY)
            
            # تطبيق عمليات مورفولوجية لتحسين التقسيم
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            
            # العثور على المكونات المتصلة
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening, connectivity=8)
            
            # تجاهل الخلفية (المكون 0)
            for i in range(1, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                
                # تجاهل المكونات الصغيرة جدًا
                if area < self.min_segment_size:
                    continue
                    
                # إنشاء قناع للمكون الحالي
                component_mask = np.zeros_like(labels, dtype=np.uint8)
                component_mask[labels == i] = 255
                
                # الحصول على المستطيل المحيط
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                
                # إضافة معلومات القطعة
                segment = {
                    "mask": component_mask,
                    "bbox": (x, y, w, h),
                    "area": area,
                    "centroid": (centroids[i, 0], centroids[i, 1])
                }
                segments.append(segment)
                
            logger.debug(f"تم تقسيم الصورة إلى {len(segments)} قطعة")
            return segments
            
        except Exception as e:
            logger.error(f"فشل في تقسيم الصورة: {e}")
            # إرجاع قطعة واحدة تغطي الصورة بأكملها كحل بديل
            h, w, _ = image.shape
            fallback_segment = {
                "mask": np.ones((h, w), dtype=np.uint8) * 255,
                "bbox": (0, 0, w, h),
                "area": w * h,
                "centroid": (w/2, h/2)
            }
            return [fallback_segment]

    def _analyze_segment(self, image: np.ndarray, segment: Dict, segment_id: int) -> Dict:
        """تحليل قطعة للكشف عن الأمراض والتشوهات"""
        h, w, _ = image.shape
        x, y, width, height = segment["bbox"]
        area = segment["area"]
        area_percentage = (area / (h * w)) * 100
        
        # استخراج منطقة الاهتمام (ROI)
        mask = segment["mask"]
        roi = cv2.bitwise_and(image, image, mask=mask)
        
        # في التنفيذ الحقيقي، هنا يتم تمرير ROI إلى نموذج الكشف عن الأمراض
        # لأغراض هذا المثال، سنستخدم محاكاة بسيطة
        
        # محاكاة الكشف عن المرض باستخدام تحليل اللون البسيط
        # نفترض أن المناطق ذات اللون الأصفر أو البني قد تكون مصابة
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        
        # نطاق اللون الأصفر في HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)
        
        # نطاق اللون البني في HSV
        lower_brown = np.array([10, 100, 20])
        upper_brown = np.array([20, 255, 200])
        brown_mask = cv2.inRange(hsv_roi, lower_brown, upper_brown)
        
        # دمج الأقنعة
        disease_mask = cv2.bitwise_or(yellow_mask, brown_mask)
        
        # حساب نسبة البكسلات المصابة
        disease_pixels = cv2.countNonZero(disease_mask)
        if area > 0:
            disease_ratio = disease_pixels / area
        else:
            disease_ratio = 0
            
        # تحديد ما إذا كان هناك مرض
        disease_detected = disease_ratio > 0.1 # نسبة عتبة بسيطة
        disease_confidence = min(disease_ratio * 5, 1.0) # تحويل النسبة إلى درجة ثقة
        
        # تحديد نوع المرض (محاكاة)
        disease_name = None
        if disease_detected:
            if cv2.countNonZero(yellow_mask) > cv2.countNonZero(brown_mask):
                disease_name = "اللفحة الصفراء"
            else:
                disease_name = "البقع البنية"
        
        # تجميع نتائج تحليل القطعة
        segment_analysis = {
            "segment_id": segment_id,
            "bbox": segment["bbox"],
            "area": area,
            "area_percentage": area_percentage,
            "centroid": segment["centroid"],
            "disease_detected": disease_detected,
            "disease_confidence": disease_confidence if disease_detected else 0.0,
            "disease_name": disease_name,
            "disease_ratio": disease_ratio
        }
        
        return segment_analysis

    def _create_visualization(self, image: np.ndarray, segments: List[Dict], 
                             disease_regions: List[Dict], output_path: str):
        """إنشاء صورة توضيحية للنتائج"""
        # نسخة من الصورة الأصلية
        visualization = image.copy()
        
        # رسم حدود جميع القطع
        for i, segment in enumerate(segments):
            x, y, w, h = segment["bbox"]
            cv2.rectangle(visualization, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(visualization, f"S{i}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
        # رسم مناطق المرض بلون مختلف
        for region in disease_regions:
            x, y, w, h = region["bbox"]
            confidence = region["confidence"]
            disease = region["disease"]
            
            # استخدام اللون الأحمر للمناطق المصابة
            cv2.rectangle(visualization, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # إضافة نص المرض والثقة
            text = f"{disease} ({confidence:.2f})"
            cv2.putText(visualization, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            
        # حفظ الصورة التوضيحية
        cv2.imwrite(output_path, cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))
        logger.info(f"تم حفظ الصورة التوضيحية في: {output_path}")

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "image_segmentation": {
            "results_dir": "../../results/segmentation_test",
            "min_segment_size": 100,
            "disease_confidence_threshold": 0.7
        }
    }
    
    # تهيئة المحلل
    analyzer = ImageSegmentationAnalyzer(dummy_config)
    
    # إنشاء صورة نبات وهمية مع مناطق مصابة
    test_image_path = "test_plant_disease_image.png"
    
    # إنشاء صورة خضراء (نبات سليم) مع بقع صفراء وبنية (مناطق مصابة)
    image = np.ones((400, 600, 3), dtype=np.uint8) * np.array([0, 150, 0], dtype=np.uint8) # خلفية خضراء
    
    # إضافة بقعة صفراء (مرض)
    cv2.circle(image, (200, 150), 50, (255, 255, 0), -1)
    
    # إضافة بقعة بنية (مرض آخر)
    cv2.circle(image, (400, 250), 70, (150, 75, 0), -1)
    
    # إضافة بعض التشويش
    noise = np.random.randint(-20, 20, image.shape, dtype=np.int16)
    image = np.clip(image + noise, 0, 255).astype(np.uint8)
    
    # حفظ الصورة
    cv2.imwrite(test_image_path, image)
    print(f"تم إنشاء صورة نبات اختبار وهمية: {test_image_path}")
    
    # تحليل الصورة
    print("\n--- تحليل تقسيم الصورة --- ")
    result = analyzer.analyze_image(test_image_path)
    
    if "error" not in result:
        print(f"معرف التحليل: {result["analysis_id"]}")
        print(f"عدد القطع: {result["num_segments"]}")
        print(f"عدد مناطق المرض المكتشفة: {len(result["disease_regions"])}")
        
        # عرض معلومات مناطق المرض
        for i, region in enumerate(result["disease_regions"]):
            print(f"  منطقة المرض {i+1}:")
            print(f"    المرض: {region["disease"]}")
            print(f"    الثقة: {region["confidence"]:.2f}")
            print(f"    النسبة المئوية من الصورة: {region["area_percentage"]:.2f}%")
            
        # عرض مسار الصورة التوضيحية
        if result["visualization_path"]:
            print(f"\nتم حفظ الصورة التوضيحية في: {result["visualization_path"]}")
    else:
        print(f"فشل التحليل: {result["error"]}")
        
    # تنظيف الملف الوهمي
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
        print(f"\nتم حذف صورة الاختبار: {test_image_path}")
