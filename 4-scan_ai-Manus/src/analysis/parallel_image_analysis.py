#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام تحليل الصور المتوازي
========================

يوفر هذا المديول نظامًا متوازيًا لتحليل الصور باستخدام طريقتين:
1. نظام التحليل القياسي (Standard Analysis)
2. نظام التحليل الأولي (Primitive Analysis) المعتمد على تقسيم الصور واستخراج الميزات

يتيح للمستخدم اختيار النظام المفضل أو استخدام كليهما معًا مع مقارنة النتائج.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import logging
import time
import uuid
import numpy as np
import cv2
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# إعداد السجل
logger = logging.getLogger("agricultural_ai.parallel_image_analysis")

class ParallelImageAnalysisSystem:
    """فئة لإدارة أنظمة تحليل الصور المتوازية"""
    
    def __init__(self, config: Dict, 
                 disease_detector=None, 
                 nutrient_analyzer=None, 
                 segmentation_analyzer=None, 
                 feature_extractor=None):
        """تهيئة نظام التحليل المتوازي
        
        المعاملات:
            config (Dict): تكوين النظام
            disease_detector: كاشف الأمراض القياسي
            nutrient_analyzer: محلل نقص العناصر القياسي
            segmentation_analyzer: محلل تقسيم الصور
            feature_extractor: مستخرج الميزات الأولية
        """
        self.config = config.get("parallel_image_analysis", {})
        self.disease_detector = disease_detector
        self.nutrient_analyzer = nutrient_analyzer
        self.segmentation_analyzer = segmentation_analyzer
        self.feature_extractor = feature_extractor
        
        # إعدادات النظام
        self.results_dir = self.config.get("results_dir", "results/parallel_analysis")
        self.save_intermediate_results = self.config.get("save_intermediate_results", True)
        self.default_analysis_mode = self.config.get("default_analysis_mode", "both")  # "standard", "primitive", "both"
        
        # إنشاء مجلد النتائج إذا لم يكن موجودًا
        os.makedirs(self.results_dir, exist_ok=True)
        
        logger.info("تم تهيئة نظام تحليل الصور المتوازي")

    def analyze_image(self, 
                      image_path: str, 
                      analysis_mode: str = None, 
                      plant_type: str = None,
                      save_results: bool = True) -> Dict:
        """تحليل صورة باستخدام النظام المحدد أو كلا النظامين
        
        المعاملات:
            image_path (str): مسار الصورة المراد تحليلها
            analysis_mode (str): وضع التحليل ("standard", "primitive", "both")
            plant_type (str): نوع النبات (اختياري)
            save_results (bool): حفظ النتائج في ملفات
            
        الإرجاع:
            Dict: نتائج التحليل
        """
        if not os.path.exists(image_path):
            logger.error(f"الصورة غير موجودة: {image_path}")
            return {"error": "الصورة غير موجودة", "image_path": image_path}
            
        # استخدام الوضع الافتراضي إذا لم يتم تحديد وضع
        if analysis_mode is None:
            analysis_mode = self.default_analysis_mode
            
        logger.info(f"بدء تحليل الصورة {image_path} باستخدام الوضع: {analysis_mode}")
        
        # إنشاء معرف فريد للتحليل
        analysis_id = str(uuid.uuid4())
        
        # قراءة الصورة
        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"فشل في قراءة الصورة: {image_path}")
                return {"error": "فشل في قراءة الصورة", "image_path": image_path}
        except Exception as e:
            logger.error(f"خطأ أثناء قراءة الصورة {image_path}: {e}")
            return {"error": f"خطأ أثناء قراءة الصورة: {e}", "image_path": image_path}
            
        # تحضير قاموس النتائج
        results = {
            "analysis_id": analysis_id,
            "image_path": image_path,
            "analysis_mode": analysis_mode,
            "plant_type": plant_type,
            "timestamp": datetime.now().isoformat(),
            "standard_analysis": None,
            "primitive_analysis": None,
            "comparative_results": None
        }
        
        # إجراء التحليل القياسي إذا كان مطلوبًا
        if analysis_mode in ["standard", "both"]:
            standard_results = self._perform_standard_analysis(image, image_path, plant_type)
            results["standard_analysis"] = standard_results
            
        # إجراء التحليل الأولي إذا كان مطلوبًا
        if analysis_mode in ["primitive", "both"]:
            primitive_results = self._perform_primitive_analysis(image, image_path, plant_type)
            results["primitive_analysis"] = primitive_results
            
        # إجراء تحليل مقارن إذا تم استخدام كلا النظامين
        if analysis_mode == "both" and results["standard_analysis"] and results["primitive_analysis"]:
            comparative_results = self._compare_analysis_results(
                results["standard_analysis"], 
                results["primitive_analysis"]
            )
            results["comparative_results"] = comparative_results
            
        # حفظ النتائج إذا كان مطلوبًا
        if save_results:
            self._save_analysis_results(results)
            
        logger.info(f"اكتمل تحليل الصورة {image_path} (معرف التحليل: {analysis_id})")
        return results

    def _perform_standard_analysis(self, image: np.ndarray, image_path: str, plant_type: str = None) -> Dict:
        """إجراء التحليل القياسي للصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            image_path (str): مسار الصورة
            plant_type (str): نوع النبات (اختياري)
            
        الإرجاع:
            Dict: نتائج التحليل القياسي
        """
        logger.debug(f"بدء التحليل القياسي للصورة {image_path}")
        start_time = time.time()
        
        standard_results = {
            "disease_analysis": None,
            "nutrient_analysis": None,
            "processing_time": None
        }
        
        # تحليل الأمراض إذا كان كاشف الأمراض متاحًا
        if self.disease_detector:
            try:
                disease_results = self.disease_detector.detect(image_path, plant_type=plant_type)
                standard_results["disease_analysis"] = disease_results
                logger.debug(f"اكتمل تحليل الأمراض: {len(disease_results.get('detected_diseases', []))} أمراض تم اكتشافها")
            except Exception as e:
                logger.error(f"فشل في تحليل الأمراض: {e}")
                standard_results["disease_analysis"] = {"error": str(e)}
                
        # تحليل نقص العناصر إذا كان محلل نقص العناصر متاحًا
        if self.nutrient_analyzer:
            try:
                nutrient_results = self.nutrient_analyzer.analyze(image_path, plant_type=plant_type)
                standard_results["nutrient_analysis"] = nutrient_results
                logger.debug(f"اكتمل تحليل نقص العناصر: {len(nutrient_results.get('deficiencies', []))} أوجه نقص تم اكتشافها")
            except Exception as e:
                logger.error(f"فشل في تحليل نقص العناصر: {e}")
                standard_results["nutrient_analysis"] = {"error": str(e)}
                
        # حساب وقت المعالجة
        standard_results["processing_time"] = time.time() - start_time
        
        logger.debug(f"اكتمل التحليل القياسي في {standard_results['processing_time']:.2f} ثانية")
        return standard_results

    def _perform_primitive_analysis(self, image: np.ndarray, image_path: str, plant_type: str = None) -> Dict:
        """إجراء التحليل الأولي للصورة (تقسيم + استخراج ميزات)
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            image_path (str): مسار الصورة
            plant_type (str): نوع النبات (اختياري)
            
        الإرجاع:
            Dict: نتائج التحليل الأولي
        """
        logger.debug(f"بدء التحليل الأولي للصورة {image_path}")
        start_time = time.time()
        
        primitive_results = {
            "segmentation_results": None,
            "feature_extraction_results": None,
            "disease_analysis": None,
            "nutrient_analysis": None,
            "processing_time": None
        }
        
        # التحقق من توفر محلل التقسيم ومستخرج الميزات
        if not self.segmentation_analyzer:
            logger.error("محلل تقسيم الصور غير متاح")
            primitive_results["error"] = "محلل تقسيم الصور غير متاح"
            return primitive_results
            
        if not self.feature_extractor:
            logger.warning("مستخرج الميزات الأولية غير متاح، سيتم استخدام التقسيم فقط")
            
        # تقسيم الصورة
        try:
            segmentation_results = self.segmentation_analyzer.analyze(image_path, plant_type=plant_type)
            primitive_results["segmentation_results"] = segmentation_results
            logger.debug(f"اكتمل تقسيم الصورة: {segmentation_results.get('num_segments', 0)} قطع تم اكتشافها")
            
            # استخراج الميزات الأولية لكل قطعة إذا كان مستخرج الميزات متاحًا
            if self.feature_extractor and "segments" in segmentation_results:
                feature_extraction_results = []
                
                for segment in segmentation_results["segments"]:
                    segment_id = segment.get("segment_id")
                    segment_mask = segment.get("mask")
                    segment_bbox = segment.get("bbox")
                    
                    if segment_mask is not None and segment_bbox is not None:
                        # استخراج منطقة الاهتمام (ROI) من الصورة الأصلية
                        x, y, w, h = segment_bbox
                        roi = image[y:y+h, x:x+w]
                        
                        # استخراج الميزات الأولية
                        try:
                            features = self.feature_extractor.extract_features(roi, segment_mask)
                            feature_extraction_results.append({
                                "segment_id": segment_id,
                                "features": features
                            })
                        except Exception as e:
                            logger.error(f"فشل في استخراج الميزات للقطعة {segment_id}: {e}")
                            feature_extraction_results.append({
                                "segment_id": segment_id,
                                "error": str(e)
                            })
                
                primitive_results["feature_extraction_results"] = feature_extraction_results
                logger.debug(f"اكتمل استخراج الميزات الأولية لـ {len(feature_extraction_results)} قطع")
                
            # تحليل الأمراض ونقص العناصر بناءً على نتائج التقسيم
            primitive_results["disease_analysis"] = self._analyze_diseases_from_segments(segmentation_results)
            primitive_results["nutrient_analysis"] = self._analyze_nutrients_from_segments(segmentation_results)
            
        except Exception as e:
            logger.error(f"فشل في التحليل الأولي: {e}")
            primitive_results["error"] = str(e)
            
        # حساب وقت المعالجة
        primitive_results["processing_time"] = time.time() - start_time
        
        logger.debug(f"اكتمل التحليل الأولي في {primitive_results['processing_time']:.2f} ثانية")
        return primitive_results

    def _analyze_diseases_from_segments(self, segmentation_results: Dict) -> Dict:
        """تحليل الأمراض بناءً على نتائج التقسيم
        
        المعاملات:
            segmentation_results (Dict): نتائج التقسيم
            
        الإرجاع:
            Dict: نتائج تحليل الأمراض
        """
        disease_analysis = {
            "detected_diseases": [],
            "affected_area_percentage": 0.0,
            "confidence": 0.0
        }
        
        # استخراج معلومات الأمراض من القطع
        if "segments" in segmentation_results:
            disease_segments = [s for s in segmentation_results["segments"] if s.get("disease_detected", False)]
            
            if disease_segments:
                # تجميع الأمراض المكتشفة
                diseases = {}
                total_disease_area = 0
                
                for segment in disease_segments:
                    disease_name = segment.get("disease_name", "غير معروف")
                    confidence = segment.get("disease_confidence", 0.0)
                    area = segment.get("area", 0)
                    
                    total_disease_area += area
                    
                    if disease_name in diseases:
                        diseases[disease_name]["segments"].append(segment.get("segment_id"))
                        diseases[disease_name]["total_area"] += area
                        diseases[disease_name]["confidence"] = max(diseases[disease_name]["confidence"], confidence)
                    else:
                        diseases[disease_name] = {
                            "name": disease_name,
                            "segments": [segment.get("segment_id")],
                            "total_area": area,
                            "confidence": confidence
                        }
                
                # حساب النسبة المئوية للمنطقة المتأثرة
                total_image_area = sum(s.get("area", 0) for s in segmentation_results["segments"])
                if total_image_area > 0:
                    disease_analysis["affected_area_percentage"] = (total_disease_area / total_image_area) * 100
                
                # تحويل قاموس الأمراض إلى قائمة
                disease_analysis["detected_diseases"] = list(diseases.values())
                
                # حساب متوسط الثقة
                if disease_analysis["detected_diseases"]:
                    disease_analysis["confidence"] = sum(d["confidence"] for d in disease_analysis["detected_diseases"]) / len(disease_analysis["detected_diseases"])
        
        return disease_analysis

    def _analyze_nutrients_from_segments(self, segmentation_results: Dict) -> Dict:
        """تحليل نقص العناصر بناءً على نتائج التقسيم
        
        المعاملات:
            segmentation_results (Dict): نتائج التقسيم
            
        الإرجاع:
            Dict: نتائج تحليل نقص العناصر
        """
        nutrient_analysis = {
            "deficiencies": [],
            "affected_area_percentage": 0.0,
            "confidence": 0.0
        }
        
        # استخراج معلومات نقص العناصر من القطع
        # هذا تنفيذ مبسط، يمكن توسيعه بناءً على كيفية تخزين معلومات نقص العناصر في القطع
        if "segments" in segmentation_results:
            # نفترض أن القطع قد تحتوي على حقل "nutrient_deficiency" يشير إلى وجود نقص
            deficiency_segments = [s for s in segmentation_results["segments"] if s.get("nutrient_deficiency", False)]
            
            if deficiency_segments:
                # تجميع أوجه النقص المكتشفة
                deficiencies = {}
                total_deficiency_area = 0
                
                for segment in deficiency_segments:
                    deficiency_type = segment.get("deficiency_type", "غير معروف")
                    confidence = segment.get("deficiency_confidence", 0.0)
                    area = segment.get("area", 0)
                    
                    total_deficiency_area += area
                    
                    if deficiency_type in deficiencies:
                        deficiencies[deficiency_type]["segments"].append(segment.get("segment_id"))
                        deficiencies[deficiency_type]["total_area"] += area
                        deficiencies[deficiency_type]["confidence"] = max(deficiencies[deficiency_type]["confidence"], confidence)
                    else:
                        deficiencies[deficiency_type] = {
                            "type": deficiency_type,
                            "segments": [segment.get("segment_id")],
                            "total_area": area,
                            "confidence": confidence
                        }
                
                # حساب النسبة المئوية للمنطقة المتأثرة
                total_image_area = sum(s.get("area", 0) for s in segmentation_results["segments"])
                if total_image_area > 0:
                    nutrient_analysis["affected_area_percentage"] = (total_deficiency_area / total_image_area) * 100
                
                # تحويل قاموس أوجه النقص إلى قائمة
                nutrient_analysis["deficiencies"] = list(deficiencies.values())
                
                # حساب متوسط الثقة
                if nutrient_analysis["deficiencies"]:
                    nutrient_analysis["confidence"] = sum(d["confidence"] for d in nutrient_analysis["deficiencies"]) / len(nutrient_analysis["deficiencies"])
        
        return nutrient_analysis

    def _compare_analysis_results(self, standard_results: Dict, primitive_results: Dict) -> Dict:
        """مقارنة نتائج التحليل القياسي والأولي
        
        المعاملات:
            standard_results (Dict): نتائج التحليل القياسي
            primitive_results (Dict): نتائج التحليل الأولي
            
        الإرجاع:
            Dict: نتائج المقارنة
        """
        logger.debug("مقارنة نتائج التحليل القياسي والأولي")
        
        comparative_results = {
            "disease_detection_comparison": None,
            "nutrient_analysis_comparison": None,
            "processing_time_comparison": None,
            "recommended_system": None
        }
        
        # مقارنة تحليل الأمراض
        std_diseases = standard_results.get("disease_analysis", {}).get("detected_diseases", [])
        prim_diseases = primitive_results.get("disease_analysis", {}).get("detected_diseases", [])
        
        disease_comparison = {
            "standard_count": len(std_diseases),
            "primitive_count": len(prim_diseases),
            "common_diseases": [],
            "unique_to_standard": [],
            "unique_to_primitive": [],
            "confidence_comparison": {}
        }
        
        # تحديد الأمراض المشتركة والفريدة
        std_disease_names = [d.get("name", "") for d in std_diseases]
        prim_disease_names = [d.get("name", "") for d in prim_diseases]
        
        for disease in std_diseases:
            name = disease.get("name", "")
            if name in prim_disease_names:
                disease_comparison["common_diseases"].append(name)
                
                # مقارنة الثقة للأمراض المشتركة
                std_confidence = disease.get("confidence", 0.0)
                prim_disease = next((d for d in prim_diseases if d.get("name", "") == name), None)
                prim_confidence = prim_disease.get("confidence", 0.0) if prim_disease else 0.0
                
                disease_comparison["confidence_comparison"][name] = {
                    "standard": std_confidence,
                    "primitive": prim_confidence,
                    "difference": abs(std_confidence - prim_confidence)
                }
            else:
                disease_comparison["unique_to_standard"].append(name)
                
        for disease in prim_diseases:
            name = disease.get("name", "")
            if name not in std_disease_names:
                disease_comparison["unique_to_primitive"].append(name)
                
        comparative_results["disease_detection_comparison"] = disease_comparison
        
        # مقارنة تحليل نقص العناصر (مشابهة لمقارنة الأمراض)
        std_deficiencies = standard_results.get("nutrient_analysis", {}).get("deficiencies", [])
        prim_deficiencies = primitive_results.get("nutrient_analysis", {}).get("deficiencies", [])
        
        nutrient_comparison = {
            "standard_count": len(std_deficiencies),
            "primitive_count": len(prim_deficiencies),
            "common_deficiencies": [],
            "unique_to_standard": [],
            "unique_to_primitive": [],
            "confidence_comparison": {}
        }
        
        # تحديد أوجه النقص المشتركة والفريدة
        std_deficiency_types = [d.get("type", "") for d in std_deficiencies]
        prim_deficiency_types = [d.get("type", "") for d in prim_deficiencies]
        
        for deficiency in std_deficiencies:
            deficiency_type = deficiency.get("type", "")
            if deficiency_type in prim_deficiency_types:
                nutrient_comparison["common_deficiencies"].append(deficiency_type)
                
                # مقارنة الثقة لأوجه النقص المشتركة
                std_confidence = deficiency.get("confidence", 0.0)
                prim_deficiency = next((d for d in prim_deficiencies if d.get("type", "") == deficiency_type), None)
                prim_confidence = prim_deficiency.get("confidence", 0.0) if prim_deficiency else 0.0
                
                nutrient_comparison["confidence_comparison"][deficiency_type] = {
                    "standard": std_confidence,
                    "primitive": prim_confidence,
                    "difference": abs(std_confidence - prim_confidence)
                }
            else:
                nutrient_comparison["unique_to_standard"].append(deficiency_type)
                
        for deficiency in prim_deficiencies:
            deficiency_type = deficiency.get("type", "")
            if deficiency_type not in std_deficiency_types:
                nutrient_comparison["unique_to_primitive"].append(deficiency_type)
                
        comparative_results["nutrient_analysis_comparison"] = nutrient_comparison
        
        # مقارنة وقت المعالجة
        std_time = standard_results.get("processing_time", 0.0)
        prim_time = primitive_results.get("processing_time", 0.0)
        
        comparative_results["processing_time_comparison"] = {
            "standard": std_time,
            "primitive": prim_time,
            "difference": abs(std_time - prim_time),
            "faster_system": "standard" if std_time < prim_time else "primitive"
        }
        
        # تحديد النظام الموصى به
        # هذه مجرد مقاربة بسيطة، يمكن تحسينها بناءً على معايير أكثر تعقيدًا
        recommended_system = self._determine_recommended_system(
            disease_comparison, 
            nutrient_comparison, 
            comparative_results["processing_time_comparison"]
        )
        comparative_results["recommended_system"] = recommended_system
        
        logger.debug(f"اكتملت المقارنة، النظام الموصى به: {recommended_system}")
        return comparative_results

    def _determine_recommended_system(self, 
                                     disease_comparison: Dict, 
                                     nutrient_comparison: Dict, 
                                     time_comparison: Dict) -> Dict:
        """تحديد النظام الموصى به بناءً على المقارنات
        
        المعاملات:
            disease_comparison (Dict): مقارنة تحليل الأمراض
            nutrient_comparison (Dict): مقارنة تحليل نقص العناصر
            time_comparison (Dict): مقارنة وقت المعالجة
            
        الإرجاع:
            Dict: توصية النظام
        """
        # حساب النقاط لكل نظام
        standard_points = 0
        primitive_points = 0
        
        # نقاط اكتشاف الأمراض
        if disease_comparison["standard_count"] > disease_comparison["primitive_count"]:
            standard_points += 1
        elif disease_comparison["primitive_count"] > disease_comparison["standard_count"]:
            primitive_points += 1
            
        # نقاط اكتشاف نقص العناصر
        if nutrient_comparison["standard_count"] > nutrient_comparison["primitive_count"]:
            standard_points += 1
        elif nutrient_comparison["primitive_count"] > nutrient_comparison["standard_count"]:
            primitive_points += 1
            
        # نقاط وقت المعالجة
        if time_comparison["faster_system"] == "standard":
            standard_points += 1
        else:
            primitive_points += 1
            
        # تحديد النظام الموصى به
        recommended_system = {
            "system": "standard" if standard_points > primitive_points else "primitive",
            "reason": "",
            "standard_points": standard_points,
            "primitive_points": primitive_points
        }
        
        # تحديد سبب التوصية
        if standard_points > primitive_points:
            if disease_comparison["standard_count"] > disease_comparison["primitive_count"]:
                recommended_system["reason"] = "النظام القياسي اكتشف أمراضًا أكثر"
            elif nutrient_comparison["standard_count"] > nutrient_comparison["primitive_count"]:
                recommended_system["reason"] = "النظام القياسي اكتشف أوجه نقص أكثر"
            else:
                recommended_system["reason"] = "النظام القياسي أسرع في المعالجة"
        else:
            if disease_comparison["primitive_count"] > disease_comparison["standard_count"]:
                recommended_system["reason"] = "النظام الأولي اكتشف أمراضًا أكثر"
            elif nutrient_comparison["primitive_count"] > nutrient_comparison["standard_count"]:
                recommended_system["reason"] = "النظام الأولي اكتشف أوجه نقص أكثر"
            else:
                recommended_system["reason"] = "النظام الأولي أسرع في المعالجة"
                
        return recommended_system

    def _save_analysis_results(self, results: Dict) -> None:
        """حفظ نتائج التحليل في ملفات
        
        المعاملات:
            results (Dict): نتائج التحليل
        """
        if not self.save_intermediate_results:
            return
            
        analysis_id = results.get("analysis_id", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # إنشاء مجلد للنتائج
        results_subdir = os.path.join(self.results_dir, f"{timestamp}_{analysis_id}")
        os.makedirs(results_subdir, exist_ok=True)
        
        # حفظ ملخص النتائج في ملف JSON
        import json
        
        # إنشاء نسخة من النتائج قابلة للتسلسل (بدون مصفوفات NumPy)
        serializable_results = self._make_serializable(results)
        
        with open(os.path.join(results_subdir, "analysis_results.json"), "w", encoding="utf-8") as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)
            
        logger.debug(f"تم حفظ نتائج التحليل في {results_subdir}")

    def _make_serializable(self, obj):
        """تحويل الكائن إلى كائن قابل للتسلسل (JSON)"""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        else:
            return obj

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # --- محاكاة للمكونات الأخرى --- 
    class MockDiseaseDetector:
        def detect(self, image_path, plant_type=None):
            print(f"[Mock] Detecting diseases in {image_path}, plant_type={plant_type}")
            return {
                "detected_diseases": [
                    {"name": "البقع البنية", "confidence": 0.85, "affected_area": 0.15},
                    {"name": "البياض الدقيقي", "confidence": 0.65, "affected_area": 0.05}
                ],
                "overall_health": "متوسط",
                "confidence": 0.75
            }
            
    class MockNutrientAnalyzer:
        def analyze(self, image_path, plant_type=None):
            print(f"[Mock] Analyzing nutrients in {image_path}, plant_type={plant_type}")
            return {
                "deficiencies": [
                    {"type": "نقص النيتروجين", "confidence": 0.70, "severity": "متوسط"},
                    {"type": "نقص الحديد", "confidence": 0.60, "severity": "خفيف"}
                ],
                "overall_status": "نقص متعدد",
                "confidence": 0.65
            }
            
    class MockSegmentationAnalyzer:
        def analyze(self, image_path, plant_type=None):
            print(f"[Mock] Segmenting image {image_path}, plant_type={plant_type}")
            # محاكاة تقسيم الصورة إلى 3 قطع
            return {
                "num_segments": 3,
                "segments": [
                    {
                        "segment_id": 0,
                        "bbox": (10, 10, 100, 100),
                        "area": 10000,
                        "mask": np.ones((100, 100), dtype=np.uint8),
                        "disease_detected": True,
                        "disease_name": "البقع البنية",
                        "disease_confidence": 0.90
                    },
                    {
                        "segment_id": 1,
                        "bbox": (120, 10, 100, 100),
                        "area": 10000,
                        "mask": np.ones((100, 100), dtype=np.uint8),
                        "disease_detected": False
                    },
                    {
                        "segment_id": 2,
                        "bbox": (10, 120, 100, 100),
                        "area": 10000,
                        "mask": np.ones((100, 100), dtype=np.uint8),
                        "disease_detected": True,
                        "disease_name": "البياض الدقيقي",
                        "disease_confidence": 0.75,
                        "nutrient_deficiency": True,
                        "deficiency_type": "نقص النيتروجين",
                        "deficiency_confidence": 0.80
                    }
                ]
            }
            
    class MockFeatureExtractor:
        def extract_features(self, roi, mask):
            print(f"[Mock] Extracting features from ROI shape {roi.shape}")
            # محاكاة استخراج الميزات الأولية
            return {
                "dominant_color_rgb": [120, 180, 30],
                "color_histogram": {"green": 0.7, "brown": 0.2, "yellow": 0.1},
                "texture_contrast": 12.5,
                "texture_homogeneity": 0.8,
                "shape_circularity": 0.75
            }
    # --- نهاية المحاكاة --- 
    
    # تكوين وهمي
    dummy_config = {
        "parallel_image_analysis": {
            "results_dir": "/tmp/parallel_analysis_results",
            "save_intermediate_results": True,
            "default_analysis_mode": "both"
        }
    }
    
    # تهيئة النظام مع المحاكاة
    parallel_system = ParallelImageAnalysisSystem(
        dummy_config,
        disease_detector=MockDiseaseDetector(),
        nutrient_analyzer=MockNutrientAnalyzer(),
        segmentation_analyzer=MockSegmentationAnalyzer(),
        feature_extractor=MockFeatureExtractor()
    )
    
    # اختبار التحليل
    print("\n--- اختبار التحليل القياسي --- ")
    # نفترض وجود صورة اختبار (يمكن إنشاء صورة وهمية للاختبار)
    test_image_path = "/tmp/test_plant.jpg"
    
    # إنشاء صورة وهمية للاختبار
    test_image = np.ones((300, 300, 3), dtype=np.uint8) * 255
    cv2.circle(test_image, (150, 150), 50, (0, 255, 0), -1)  # دائرة خضراء
    cv2.circle(test_image, (180, 120), 20, (0, 0, 255), -1)  # دائرة حمراء (تمثل مرضًا)
    cv2.imwrite(test_image_path, test_image)
    
    # تحليل الصورة باستخدام النظام القياسي
    standard_results = parallel_system.analyze_image(test_image_path, analysis_mode="standard", plant_type="tomato")
    print(f"\nنتائج التحليل القياسي:")
    print(f"  الأمراض المكتشفة: {len(standard_results.get("standard_analysis", {}).get("disease_analysis", {}).get("detected_diseases", []))}")
    print(f"  أوجه النقص المكتشفة: {len(standard_results.get("standard_analysis", {}).get("nutrient_analysis", {}).get("deficiencies", []))}")
    print(f"  وقت المعالجة: {standard_results.get("standard_analysis", {}).get("processing_time", 0):.2f} ثانية")
    
    # تحليل الصورة باستخدام النظام الأولي
    print("\n--- اختبار التحليل الأولي --- ")
    primitive_results = parallel_system.analyze_image(test_image_path, analysis_mode="primitive", plant_type="tomato")
    print(f"\nنتائج التحليل الأولي:")
    print(f"  عدد القطع: {primitive_results.get("primitive_analysis", {}).get("segmentation_results", {}).get("num_segments", 0)}")
    print(f"  الأمراض المكتشفة: {len(primitive_results.get("primitive_analysis", {}).get("disease_analysis", {}).get("detected_diseases", []))}")
    print(f"  أوجه النقص المكتشفة: {len(primitive_results.get("primitive_analysis", {}).get("nutrient_analysis", {}).get("deficiencies", []))}")
    print(f"  وقت المعالجة: {primitive_results.get("primitive_analysis", {}).get("processing_time", 0):.2f} ثانية")
    
    # تحليل الصورة باستخدام كلا النظامين
    print("\n--- اختبار التحليل المزدوج والمقارنة --- ")
    both_results = parallel_system.analyze_image(test_image_path, analysis_mode="both", plant_type="tomato")
    print(f"\nنتائج المقارنة:")
    comparative = both_results.get("comparative_results", {})
    if comparative:
        print(f"  النظام الموصى به: {comparative.get("recommended_system", {}).get("system", "غير معروف")}")
        print(f"  سبب التوصية: {comparative.get("recommended_system", {}).get("reason", "غير معروف")}")
        print(f"  مقارنة وقت المعالجة: القياسي={comparative.get("processing_time_comparison", {}).get("standard", 0):.2f}s, الأولي={comparative.get("processing_time_comparison", {}).get("primitive", 0):.2f}s")
    
    # تنظيف
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
