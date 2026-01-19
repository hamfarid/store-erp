#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام التحليل المقارن لأنظمة تحليل الصور
=======================================

يوفر هذا المديول وظائف لتحليل ومقارنة أداء أنظمة تحليل الصور المختلفة (القياسي والأولي)
في مهام التعلم المختلفة، مما يساعد في تحديد النظام الأفضل لكل مهمة.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import logging
import time
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split

# إعداد السجل
logger = logging.getLogger("agricultural_ai.comparative_analysis")

class ImageSystemsComparativeAnalyzer:
    """فئة لتحليل ومقارنة أداء أنظمة تحليل الصور المختلفة"""
    
    def __init__(self, config: Dict, parallel_analyzer=None):
        """تهيئة محلل المقارنة
        
        المعاملات:
            config (Dict): تكوين المحلل
            parallel_analyzer: محلل الصور المتوازي (اختياري)
        """
        self.config = config.get("comparative_analysis", {})
        self.parallel_analyzer = parallel_analyzer
        
        # إعدادات التحليل
        self.results_dir = self.config.get("results_dir", "results/comparative_analysis")
        self.metrics_to_track = self.config.get("metrics_to_track", ["accuracy", "precision", "recall", "f1", "training_time", "inference_time"])
        self.generate_plots = self.config.get("generate_plots", True)
        
        # إنشاء مجلد النتائج إذا لم يكن موجودًا
        os.makedirs(self.results_dir, exist_ok=True)
        
        logger.info("تم تهيئة محلل المقارنة لأنظمة تحليل الصور")

    def compare_learning_performance(self, 
                                    dataset_path: str, 
                                    task_type: str = "disease_classification",
                                    test_size: float = 0.2,
                                    random_state: int = 42) -> Dict:
        """مقارنة أداء التعلم بين النظامين القياسي والأولي
        
        المعاملات:
            dataset_path (str): مسار مجموعة البيانات
            task_type (str): نوع المهمة ("disease_classification", "nutrient_deficiency", "plant_identification")
            test_size (float): نسبة بيانات الاختبار
            random_state (int): حالة العشوائية للتقسيم
            
        الإرجاع:
            Dict: نتائج المقارنة
        """
        logger.info(f"بدء مقارنة أداء التعلم للمهمة: {task_type}")
        
        # التحقق من وجود مجموعة البيانات
        if not os.path.exists(dataset_path):
            logger.error(f"مجموعة البيانات غير موجودة: {dataset_path}")
            return {"error": "مجموعة البيانات غير موجودة", "dataset_path": dataset_path}
            
        # تحميل البيانات
        try:
            dataset = self._load_dataset(dataset_path)
            logger.info(f"تم تحميل مجموعة البيانات: {len(dataset)} صور")
        except Exception as e:
            logger.error(f"فشل في تحميل مجموعة البيانات: {e}")
            return {"error": f"فشل في تحميل مجموعة البيانات: {e}", "dataset_path": dataset_path}
            
        # تقسيم البيانات إلى تدريب واختبار
        train_data, test_data = train_test_split(dataset, test_size=test_size, random_state=random_state)
        logger.info(f"تم تقسيم البيانات: {len(train_data)} للتدريب، {len(test_data)} للاختبار")
        
        # تحليل الصور باستخدام النظامين
        standard_features, standard_labels = self._extract_standard_features(train_data, task_type)
        primitive_features, primitive_labels = self._extract_primitive_features(train_data, task_type)
        
        # تدريب النماذج وتقييمها
        standard_results = self._train_and_evaluate_model(standard_features, standard_labels, test_data, task_type, "standard")
        primitive_results = self._train_and_evaluate_model(primitive_features, primitive_labels, test_data, task_type, "primitive")
        
        # مقارنة النتائج
        comparison_results = self._compare_results(standard_results, primitive_results)
        
        # إنشاء الرسوم البيانية إذا كان مطلوبًا
        if self.generate_plots:
            self._generate_comparison_plots(standard_results, primitive_results, task_type)
            
        # حفظ النتائج
        self._save_comparison_results(comparison_results, task_type)
        
        logger.info(f"اكتملت مقارنة أداء التعلم للمهمة: {task_type}")
        return comparison_results

    def _load_dataset(self, dataset_path: str) -> List[Dict]:
        """تحميل مجموعة البيانات
        
        المعاملات:
            dataset_path (str): مسار مجموعة البيانات
            
        الإرجاع:
            List[Dict]: قائمة بالصور ومعلوماتها
        """
        dataset = []
        
        # التحقق من نوع مجموعة البيانات (مجلد أو ملف JSON)
        if os.path.isdir(dataset_path):
            # مجموعة بيانات مجلدية (كل مجلد فرعي يمثل فئة)
            for class_name in os.listdir(dataset_path):
                class_dir = os.path.join(dataset_path, class_name)
                if os.path.isdir(class_dir):
                    for image_file in os.listdir(class_dir):
                        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            image_path = os.path.join(class_dir, image_file)
                            dataset.append({
                                "image_path": image_path,
                                "label": class_name
                            })
        elif dataset_path.endswith('.json'):
            # ملف JSON يحتوي على معلومات الصور
            with open(dataset_path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
        else:
            raise ValueError(f"نوع مجموعة البيانات غير مدعوم: {dataset_path}")
            
        return dataset

    def _extract_standard_features(self, data: List[Dict], task_type: str) -> Tuple[np.ndarray, np.ndarray]:
        """استخراج الميزات باستخدام النظام القياسي
        
        المعاملات:
            data (List[Dict]): بيانات الصور
            task_type (str): نوع المهمة
            
        الإرجاع:
            Tuple[np.ndarray, np.ndarray]: مصفوفة الميزات ومصفوفة التسميات
        """
        logger.info(f"استخراج الميزات باستخدام النظام القياسي لـ {len(data)} صور")
        
        features = []
        labels = []
        
        for item in data:
            image_path = item["image_path"]
            label = item["label"]
            
            # استخدام محلل الصور المتوازي إذا كان متاحًا
            if self.parallel_analyzer:
                analysis_results = self.parallel_analyzer.analyze_image(
                    image_path, 
                    analysis_mode="standard",
                    save_results=False
                )
                
                # استخراج الميزات المناسبة بناءً على نوع المهمة
                if task_type == "disease_classification":
                    # استخراج ميزات من تحليل الأمراض
                    disease_analysis = analysis_results.get("standard_analysis", {}).get("disease_analysis", {})
                    feature_vector = self._extract_disease_features(disease_analysis)
                elif task_type == "nutrient_deficiency":
                    # استخراج ميزات من تحليل نقص العناصر
                    nutrient_analysis = analysis_results.get("standard_analysis", {}).get("nutrient_analysis", {})
                    feature_vector = self._extract_nutrient_features(nutrient_analysis)
                else:
                    # استخراج ميزات عامة
                    feature_vector = self._extract_general_features(analysis_results.get("standard_analysis", {}))
            else:
                # محاكاة استخراج الميزات إذا لم يكن محلل الصور متاحًا
                feature_vector = np.random.rand(10)  # 10 ميزات عشوائية للمحاكاة
                
            features.append(feature_vector)
            labels.append(label)
            
        return np.array(features), np.array(labels)

    def _extract_primitive_features(self, data: List[Dict], task_type: str) -> Tuple[np.ndarray, np.ndarray]:
        """استخراج الميزات باستخدام النظام الأولي
        
        المعاملات:
            data (List[Dict]): بيانات الصور
            task_type (str): نوع المهمة
            
        الإرجاع:
            Tuple[np.ndarray, np.ndarray]: مصفوفة الميزات ومصفوفة التسميات
        """
        logger.info(f"استخراج الميزات باستخدام النظام الأولي لـ {len(data)} صور")
        
        features = []
        labels = []
        
        for item in data:
            image_path = item["image_path"]
            label = item["label"]
            
            # استخدام محلل الصور المتوازي إذا كان متاحًا
            if self.parallel_analyzer:
                analysis_results = self.parallel_analyzer.analyze_image(
                    image_path, 
                    analysis_mode="primitive",
                    save_results=False
                )
                
                # استخراج الميزات المناسبة بناءً على نوع المهمة
                if task_type == "disease_classification":
                    # استخراج ميزات من تحليل الأمراض
                    disease_analysis = analysis_results.get("primitive_analysis", {}).get("disease_analysis", {})
                    feature_vector = self._extract_disease_features(disease_analysis)
                elif task_type == "nutrient_deficiency":
                    # استخراج ميزات من تحليل نقص العناصر
                    nutrient_analysis = analysis_results.get("primitive_analysis", {}).get("nutrient_analysis", {})
                    feature_vector = self._extract_nutrient_features(nutrient_analysis)
                else:
                    # استخراج ميزات من نتائج التقسيم واستخراج الميزات الأولية
                    segmentation_results = analysis_results.get("primitive_analysis", {}).get("segmentation_results", {})
                    feature_extraction_results = analysis_results.get("primitive_analysis", {}).get("feature_extraction_results", [])
                    feature_vector = self._extract_primitive_system_features(segmentation_results, feature_extraction_results)
            else:
                # محاكاة استخراج الميزات إذا لم يكن محلل الصور متاحًا
                feature_vector = np.random.rand(15)  # 15 ميزات عشوائية للمحاكاة
                
            features.append(feature_vector)
            labels.append(label)
            
        return np.array(features), np.array(labels)

    def _extract_disease_features(self, disease_analysis: Dict) -> np.ndarray:
        """استخراج ميزات من تحليل الأمراض
        
        المعاملات:
            disease_analysis (Dict): نتائج تحليل الأمراض
            
        الإرجاع:
            np.ndarray: متجه الميزات
        """
        # هذه مجرد أمثلة للميزات التي يمكن استخراجها
        features = []
        
        # عدد الأمراض المكتشفة
        detected_diseases = disease_analysis.get("detected_diseases", [])
        features.append(len(detected_diseases))
        
        # متوسط الثقة
        if detected_diseases:
            avg_confidence = sum(d.get("confidence", 0) for d in detected_diseases) / len(detected_diseases)
            features.append(avg_confidence)
        else:
            features.append(0)
            
        # النسبة المئوية للمنطقة المتأثرة
        affected_area = disease_analysis.get("affected_area_percentage", 0)
        features.append(affected_area)
        
        # الثقة الإجمالية
        overall_confidence = disease_analysis.get("confidence", 0)
        features.append(overall_confidence)
        
        # ميزات إضافية (يمكن توسيعها)
        # ...
        
        return np.array(features)

    def _extract_nutrient_features(self, nutrient_analysis: Dict) -> np.ndarray:
        """استخراج ميزات من تحليل نقص العناصر
        
        المعاملات:
            nutrient_analysis (Dict): نتائج تحليل نقص العناصر
            
        الإرجاع:
            np.ndarray: متجه الميزات
        """
        # هذه مجرد أمثلة للميزات التي يمكن استخراجها
        features = []
        
        # عدد أوجه النقص المكتشفة
        deficiencies = nutrient_analysis.get("deficiencies", [])
        features.append(len(deficiencies))
        
        # متوسط الثقة
        if deficiencies:
            avg_confidence = sum(d.get("confidence", 0) for d in deficiencies) / len(deficiencies)
            features.append(avg_confidence)
        else:
            features.append(0)
            
        # النسبة المئوية للمنطقة المتأثرة
        affected_area = nutrient_analysis.get("affected_area_percentage", 0)
        features.append(affected_area)
        
        # الثقة الإجمالية
        overall_confidence = nutrient_analysis.get("confidence", 0)
        features.append(overall_confidence)
        
        # ميزات إضافية (يمكن توسيعها)
        # ...
        
        return np.array(features)

    def _extract_general_features(self, standard_analysis: Dict) -> np.ndarray:
        """استخراج ميزات عامة من التحليل القياسي
        
        المعاملات:
            standard_analysis (Dict): نتائج التحليل القياسي
            
        الإرجاع:
            np.ndarray: متجه الميزات
        """
        # هذه مجرد أمثلة للميزات التي يمكن استخراجها
        features = []
        
        # ميزات من تحليل الأمراض
        disease_analysis = standard_analysis.get("disease_analysis", {})
        features.append(len(disease_analysis.get("detected_diseases", [])))
        features.append(disease_analysis.get("confidence", 0))
        
        # ميزات من تحليل نقص العناصر
        nutrient_analysis = standard_analysis.get("nutrient_analysis", {})
        features.append(len(nutrient_analysis.get("deficiencies", [])))
        features.append(nutrient_analysis.get("confidence", 0))
        
        # ميزات إضافية (يمكن توسيعها)
        # ...
        
        return np.array(features)

    def _extract_primitive_system_features(self, segmentation_results: Dict, feature_extraction_results: List[Dict]) -> np.ndarray:
        """استخراج ميزات من نتائج التقسيم واستخراج الميزات الأولية
        
        المعاملات:
            segmentation_results (Dict): نتائج التقسيم
            feature_extraction_results (List[Dict]): نتائج استخراج الميزات الأولية
            
        الإرجاع:
            np.ndarray: متجه الميزات
        """
        # هذه مجرد أمثلة للميزات التي يمكن استخراجها
        features = []
        
        # عدد القطع
        num_segments = segmentation_results.get("num_segments", 0)
        features.append(num_segments)
        
        # عدد القطع المصابة بالأمراض
        segments = segmentation_results.get("segments", [])
        disease_segments = [s for s in segments if s.get("disease_detected", False)]
        features.append(len(disease_segments))
        
        # متوسط مساحة القطع
        if segments:
            avg_area = sum(s.get("area", 0) for s in segments) / len(segments)
            features.append(avg_area)
        else:
            features.append(0)
            
        # ميزات من نتائج استخراج الميزات الأولية
        if feature_extraction_results:
            # متوسط قيم بعض الميزات الأولية عبر جميع القطع
            avg_texture_contrast = 0
            avg_shape_circularity = 0
            count = 0
            
            for result in feature_extraction_results:
                features_dict = result.get("features", {})
                if "texture_contrast" in features_dict:
                    avg_texture_contrast += features_dict["texture_contrast"]
                    count += 1
                if "shape_circularity" in features_dict:
                    avg_shape_circularity += features_dict["shape_circularity"]
            
            if count > 0:
                avg_texture_contrast /= count
                avg_shape_circularity /= count
                
            features.append(avg_texture_contrast)
            features.append(avg_shape_circularity)
        else:
            features.append(0)
            features.append(0)
            
        # ميزات إضافية (يمكن توسيعها)
        # ...
        
        return np.array(features)

    def _train_and_evaluate_model(self, 
                                 features: np.ndarray, 
                                 labels: np.ndarray, 
                                 test_data: List[Dict], 
                                 task_type: str, 
                                 system_type: str) -> Dict:
        """تدريب وتقييم نموذج التعلم
        
        المعاملات:
            features (np.ndarray): ميزات التدريب
            labels (np.ndarray): تسميات التدريب
            test_data (List[Dict]): بيانات الاختبار
            task_type (str): نوع المهمة
            system_type (str): نوع النظام ("standard" أو "primitive")
            
        الإرجاع:
            Dict: نتائج التدريب والتقييم
        """
        logger.info(f"تدريب وتقييم نموذج {system_type} للمهمة {task_type}")
        
        # قياس وقت التدريب
        training_start_time = time.time()
        
        # اختيار وتدريب النموذج المناسب
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(features, labels)
        
        training_time = time.time() - training_start_time
        logger.debug(f"اكتمل تدريب نموذج {system_type} في {training_time:.2f} ثانية")
        
        # استخراج ميزات الاختبار
        if system_type == "standard":
            test_features, test_labels = self._extract_standard_features(test_data, task_type)
        else:
            test_features, test_labels = self._extract_primitive_features(test_data, task_type)
            
        # قياس وقت الاستدلال
        inference_start_time = time.time()
        predictions = model.predict(test_features)
        inference_time = time.time() - inference_start_time
        
        # حساب المقاييس
        accuracy = accuracy_score(test_labels, predictions)
        precision = precision_score(test_labels, predictions, average='weighted', zero_division=0)
        recall = recall_score(test_labels, predictions, average='weighted', zero_division=0)
        f1 = f1_score(test_labels, predictions, average='weighted', zero_division=0)
        
        # إنشاء مصفوفة الارتباك
        cm = confusion_matrix(test_labels, predictions)
        
        logger.info(f"نتائج تقييم نموذج {system_type}: دقة={accuracy:.4f}, F1={f1:.4f}")
        
        return {
            "system_type": system_type,
            "task_type": task_type,
            "model_type": "RandomForest",
            "num_features": features.shape[1],
            "num_samples": features.shape[0],
            "training_time": training_time,
            "inference_time": inference_time,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "confusion_matrix": cm.tolist(),
            "timestamp": datetime.now().isoformat()
        }

    def _compare_results(self, standard_results: Dict, primitive_results: Dict) -> Dict:
        """مقارنة نتائج النظامين
        
        المعاملات:
            standard_results (Dict): نتائج النظام القياسي
            primitive_results (Dict): نتائج النظام الأولي
            
        الإرجاع:
            Dict: نتائج المقارنة
        """
        logger.info("مقارنة نتائج النظامين")
        
        comparison = {
            "task_type": standard_results.get("task_type"),
            "metrics_comparison": {},
            "better_system": {},
            "overall_recommendation": None
        }
        
        # مقارنة المقاييس
        for metric in self.metrics_to_track:
            if metric in standard_results and metric in primitive_results:
                std_value = standard_results[metric]
                prim_value = primitive_results[metric]
                diff = prim_value - std_value
                
                comparison["metrics_comparison"][metric] = {
                    "standard": std_value,
                    "primitive": prim_value,
                    "difference": diff,
                    "percentage_difference": (diff / std_value) * 100 if std_value != 0 else float('inf')
                }
                
                # تحديد النظام الأفضل لهذا المقياس
                if metric in ["training_time", "inference_time"]:
                    # للأوقات، القيمة الأقل أفضل
                    comparison["better_system"][metric] = "standard" if std_value < prim_value else "primitive"
                else:
                    # للمقاييس الأخرى، القيمة الأعلى أفضل
                    comparison["better_system"][metric] = "standard" if std_value > prim_value else "primitive"
        
        # تحديد التوصية الإجمالية
        # نعطي وزنًا أكبر للدقة وF1 مقارنة بالأوقات
        better_count = {"standard": 0, "primitive": 0}
        
        # الأوزان للمقاييس المختلفة
        weights = {
            "accuracy": 3,
            "f1": 3,
            "precision": 2,
            "recall": 2,
            "training_time": 1,
            "inference_time": 1
        }
        
        for metric, better in comparison["better_system"].items():
            weight = weights.get(metric, 1)
            better_count[better] += weight
            
        # تحديد النظام الأفضل إجمالاً
        if better_count["standard"] > better_count["primitive"]:
            recommended_system = "standard"
            reason = "النظام القياسي يتفوق في المقاييس الأكثر أهمية"
        elif better_count["primitive"] > better_count["standard"]:
            recommended_system = "primitive"
            reason = "النظام الأولي يتفوق في المقاييس الأكثر أهمية"
        else:
            # في حالة التعادل، نفضل النظام الأسرع في الاستدلال
            if comparison["better_system"].get("inference_time") == "standard":
                recommended_system = "standard"
                reason = "النظام القياسي أسرع في الاستدلال مع أداء مماثل"
            else:
                recommended_system = "primitive"
                reason = "النظام الأولي أسرع في الاستدلال مع أداء مماثل"
                
        comparison["overall_recommendation"] = {
            "recommended_system": recommended_system,
            "reason": reason,
            "standard_points": better_count["standard"],
            "primitive_points": better_count["primitive"]
        }
        
        logger.info(f"النظام الموصى به: {recommended_system} ({reason})")
        return comparison

    def _generate_comparison_plots(self, standard_results: Dict, primitive_results: Dict, task_type: str) -> None:
        """إنشاء رسوم بيانية للمقارنة
        
        المعاملات:
            standard_results (Dict): نتائج النظام القياسي
            primitive_results (Dict): نتائج النظام الأولي
            task_type (str): نوع المهمة
        """
        logger.debug("إنشاء رسوم بيانية للمقارنة")
        
        # إنشاء مجلد للرسوم البيانية
        plots_dir = os.path.join(self.results_dir, "plots")
        os.makedirs(plots_dir, exist_ok=True)
        
        # 1. رسم بياني شريطي للمقاييس الرئيسية
        plt.figure(figsize=(12, 6))
        
        metrics = ["accuracy", "precision", "recall", "f1"]
        std_values = [standard_results.get(m, 0) for m in metrics]
        prim_values = [primitive_results.get(m, 0) for m in metrics]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        plt.bar(x - width/2, std_values, width, label='النظام القياسي')
        plt.bar(x + width/2, prim_values, width, label='النظام الأولي')
        
        plt.xlabel('المقاييس')
        plt.ylabel('القيمة')
        plt.title(f'مقارنة مقاييس الأداء للمهمة: {task_type}')
        plt.xticks(x, metrics)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # حفظ الرسم البياني
        plt.savefig(os.path.join(plots_dir, f"{task_type}_metrics_comparison.png"), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. رسم بياني للأوقات
        plt.figure(figsize=(10, 5))
        
        time_metrics = ["training_time", "inference_time"]
        std_times = [standard_results.get(m, 0) for m in time_metrics]
        prim_times = [primitive_results.get(m, 0) for m in time_metrics]
        
        x = np.arange(len(time_metrics))
        
        plt.bar(x - width/2, std_times, width, label='النظام القياسي')
        plt.bar(x + width/2, prim_times, width, label='النظام الأولي')
        
        plt.xlabel('نوع الوقت')
        plt.ylabel('الوقت (ثانية)')
        plt.title(f'مقارنة أوقات التدريب والاستدلال للمهمة: {task_type}')
        plt.xticks(x, ['وقت التدريب', 'وقت الاستدلال'])
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # حفظ الرسم البياني
        plt.savefig(os.path.join(plots_dir, f"{task_type}_time_comparison.png"), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. رسم مصفوفة الارتباك للنظامين
        if "confusion_matrix" in standard_results and "confusion_matrix" in primitive_results:
            # النظام القياسي
            plt.figure(figsize=(8, 6))
            cm = np.array(standard_results["confusion_matrix"])
            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title(f'مصفوفة الارتباك للنظام القياسي - {task_type}')
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(os.path.join(plots_dir, f"{task_type}_standard_confusion_matrix.png"), dpi=300, bbox_inches='tight')
            plt.close()
            
            # النظام الأولي
            plt.figure(figsize=(8, 6))
            cm = np.array(primitive_results["confusion_matrix"])
            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title(f'مصفوفة الارتباك للنظام الأولي - {task_type}')
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(os.path.join(plots_dir, f"{task_type}_primitive_confusion_matrix.png"), dpi=300, bbox_inches='tight')
            plt.close()
            
        logger.debug("اكتمل إنشاء الرسوم البيانية")

    def _save_comparison_results(self, comparison_results: Dict, task_type: str) -> None:
        """حفظ نتائج المقارنة
        
        المعاملات:
            comparison_results (Dict): نتائج المقارنة
            task_type (str): نوع المهمة
        """
        # إنشاء اسم ملف فريد
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{task_type}_comparison_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        # حفظ النتائج في ملف JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comparison_results, f, ensure_ascii=False, indent=2)
            
        logger.info(f"تم حفظ نتائج المقارنة في {filepath}")

    def analyze_learning_curve(self, 
                              dataset_path: str, 
                              task_type: str = "disease_classification",
                              train_sizes: List[float] = None,
                              n_splits: int = 5) -> Dict:
        """تحليل منحنى التعلم للنظامين
        
        المعاملات:
            dataset_path (str): مسار مجموعة البيانات
            task_type (str): نوع المهمة
            train_sizes (List[float]): أحجام مجموعات التدريب (نسب من إجمالي البيانات)
            n_splits (int): عدد التقسيمات للتحقق المتقاطع
            
        الإرجاع:
            Dict: نتائج تحليل منحنى التعلم
        """
        logger.info(f"بدء تحليل منحنى التعلم للمهمة: {task_type}")
        
        if train_sizes is None:
            train_sizes = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
            
        # التحقق من وجود مجموعة البيانات
        if not os.path.exists(dataset_path):
            logger.error(f"مجموعة البيانات غير موجودة: {dataset_path}")
            return {"error": "مجموعة البيانات غير موجودة", "dataset_path": dataset_path}
            
        # تحميل البيانات
        try:
            dataset = self._load_dataset(dataset_path)
            logger.info(f"تم تحميل مجموعة البيانات: {len(dataset)} صور")
        except Exception as e:
            logger.error(f"فشل في تحميل مجموعة البيانات: {e}")
            return {"error": f"فشل في تحميل مجموعة البيانات: {e}", "dataset_path": dataset_path}
            
        # تقسيم البيانات إلى تدريب واختبار
        train_data, test_data = train_test_split(dataset, test_size=0.2, random_state=42)
        
        # تحليل منحنى التعلم
        standard_learning_curve = self._analyze_system_learning_curve(train_data, test_data, task_type, "standard", train_sizes, n_splits)
        primitive_learning_curve = self._analyze_system_learning_curve(train_data, test_data, task_type, "primitive", train_sizes, n_splits)
        
        # مقارنة منحنيات التعلم
        comparison_results = {
            "task_type": task_type,
            "train_sizes": train_sizes,
            "standard_learning_curve": standard_learning_curve,
            "primitive_learning_curve": primitive_learning_curve,
            "comparison": self._compare_learning_curves(standard_learning_curve, primitive_learning_curve)
        }
        
        # إنشاء رسم بياني للمقارنة
        if self.generate_plots:
            self._generate_learning_curve_plot(comparison_results, task_type)
            
        # حفظ النتائج
        self._save_learning_curve_results(comparison_results, task_type)
        
        logger.info(f"اكتمل تحليل منحنى التعلم للمهمة: {task_type}")
        return comparison_results

    def _analyze_system_learning_curve(self, 
                                      train_data: List[Dict], 
                                      test_data: List[Dict], 
                                      task_type: str, 
                                      system_type: str,
                                      train_sizes: List[float],
                                      n_splits: int) -> Dict:
        """تحليل منحنى التعلم لنظام معين
        
        المعاملات:
            train_data (List[Dict]): بيانات التدريب
            test_data (List[Dict]): بيانات الاختبار
            task_type (str): نوع المهمة
            system_type (str): نوع النظام
            train_sizes (List[float]): أحجام مجموعات التدريب
            n_splits (int): عدد التقسيمات للتحقق المتقاطع
            
        الإرجاع:
            Dict: نتائج تحليل منحنى التعلم
        """
        logger.debug(f"تحليل منحنى التعلم للنظام {system_type}")
        
        # استخراج ميزات التدريب والاختبار
        if system_type == "standard":
            train_features, train_labels = self._extract_standard_features(train_data, task_type)
            test_features, test_labels = self._extract_standard_features(test_data, task_type)
        else:
            train_features, train_labels = self._extract_primitive_features(train_data, task_type)
            test_features, test_labels = self._extract_primitive_features(test_data, task_type)
            
        # تحليل منحنى التعلم
        from sklearn.model_selection import learning_curve
        from sklearn.ensemble import RandomForestClassifier
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # حساب أحجام التدريب الفعلية
        n_samples = len(train_data)
        train_sizes_abs = [int(ts * n_samples) for ts in train_sizes]
        
        # حساب منحنى التعلم
        train_sizes_abs, train_scores, test_scores = learning_curve(
            model, train_features, train_labels,
            train_sizes=train_sizes_abs,
            cv=n_splits,
            scoring='accuracy',
            n_jobs=-1
        )
        
        # حساب المتوسطات والانحرافات المعيارية
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        
        return {
            "system_type": system_type,
            "train_sizes_abs": train_sizes_abs.tolist(),
            "train_sizes_rel": [ts / n_samples for ts in train_sizes_abs],
            "train_scores_mean": train_scores_mean.tolist(),
            "train_scores_std": train_scores_std.tolist(),
            "test_scores_mean": test_scores_mean.tolist(),
            "test_scores_std": test_scores_std.tolist()
        }

    def _compare_learning_curves(self, standard_curve: Dict, primitive_curve: Dict) -> Dict:
        """مقارنة منحنيات التعلم
        
        المعاملات:
            standard_curve (Dict): منحنى التعلم للنظام القياسي
            primitive_curve (Dict): منحنى التعلم للنظام الأولي
            
        الإرجاع:
            Dict: نتائج المقارنة
        """
        # استخراج قيم الدقة على مجموعة الاختبار
        std_test_scores = standard_curve["test_scores_mean"]
        prim_test_scores = primitive_curve["test_scores_mean"]
        
        # مقارنة الدقة النهائية (عند أقصى حجم تدريب)
        final_std_score = std_test_scores[-1]
        final_prim_score = prim_test_scores[-1]
        
        # تحديد النظام الأفضل في الدقة النهائية
        if final_std_score > final_prim_score:
            better_final_system = "standard"
            final_diff = final_std_score - final_prim_score
        else:
            better_final_system = "primitive"
            final_diff = final_prim_score - final_std_score
            
        # تحليل معدل التحسن (الميل)
        std_improvement = std_test_scores[-1] - std_test_scores[0]
        prim_improvement = prim_test_scores[-1] - prim_test_scores[0]
        
        # تحديد النظام الأفضل في معدل التحسن
        if std_improvement > prim_improvement:
            better_improvement_system = "standard"
            improvement_diff = std_improvement - prim_improvement
        else:
            better_improvement_system = "primitive"
            improvement_diff = prim_improvement - std_improvement
            
        # تحليل الأداء مع بيانات تدريب قليلة
        early_std_score = std_test_scores[0]
        early_prim_score = prim_test_scores[0]
        
        # تحديد النظام الأفضل مع بيانات تدريب قليلة
        if early_std_score > early_prim_score:
            better_early_system = "standard"
            early_diff = early_std_score - early_prim_score
        else:
            better_early_system = "primitive"
            early_diff = early_prim_score - early_std_score
            
        # تحديد النظام الأفضل إجمالاً
        # نعطي وزنًا أكبر للدقة النهائية
        points = {"standard": 0, "primitive": 0}
        
        if better_final_system == "standard":
            points["standard"] += 3
        else:
            points["primitive"] += 3
            
        if better_improvement_system == "standard":
            points["standard"] += 1
        else:
            points["primitive"] += 1
            
        if better_early_system == "standard":
            points["standard"] += 1
        else:
            points["primitive"] += 1
            
        if points["standard"] > points["primitive"]:
            better_overall_system = "standard"
            if better_final_system == "standard" and better_improvement_system == "standard":
                reason = "النظام القياسي يحقق دقة أعلى ومعدل تحسن أفضل"
            elif better_final_system == "standard":
                reason = "النظام القياسي يحقق دقة نهائية أعلى"
            else:
                reason = "النظام القياسي يحقق معدل تحسن أفضل"
        else:
            better_overall_system = "primitive"
            if better_final_system == "primitive" and better_improvement_system == "primitive":
                reason = "النظام الأولي يحقق دقة أعلى ومعدل تحسن أفضل"
            elif better_final_system == "primitive":
                reason = "النظام الأولي يحقق دقة نهائية أعلى"
            else:
                reason = "النظام الأولي يحقق معدل تحسن أفضل"
                
        return {
            "final_accuracy": {
                "standard": final_std_score,
                "primitive": final_prim_score,
                "difference": final_diff,
                "better_system": better_final_system
            },
            "improvement_rate": {
                "standard": std_improvement,
                "primitive": prim_improvement,
                "difference": improvement_diff,
                "better_system": better_improvement_system
            },
            "early_performance": {
                "standard": early_std_score,
                "primitive": early_prim_score,
                "difference": early_diff,
                "better_system": better_early_system
            },
            "overall_recommendation": {
                "better_system": better_overall_system,
                "reason": reason,
                "standard_points": points["standard"],
                "primitive_points": points["primitive"]
            }
        }

    def _generate_learning_curve_plot(self, comparison_results: Dict, task_type: str) -> None:
        """إنشاء رسم بياني لمنحنى التعلم
        
        المعاملات:
            comparison_results (Dict): نتائج المقارنة
            task_type (str): نوع المهمة
        """
        # إنشاء مجلد للرسوم البيانية
        plots_dir = os.path.join(self.results_dir, "plots")
        os.makedirs(plots_dir, exist_ok=True)
        
        # استخراج البيانات
        std_curve = comparison_results["standard_learning_curve"]
        prim_curve = comparison_results["primitive_learning_curve"]
        
        train_sizes = std_curve["train_sizes_rel"]
        std_train_scores = std_curve["train_scores_mean"]
        std_test_scores = std_curve["test_scores_mean"]
        std_train_std = std_curve["train_scores_std"]
        std_test_std = std_curve["test_scores_std"]
        
        prim_train_scores = prim_curve["train_scores_mean"]
        prim_test_scores = prim_curve["test_scores_mean"]
        prim_train_std = prim_curve["train_scores_std"]
        prim_test_std = prim_curve["test_scores_std"]
        
        # إنشاء الرسم البياني
        plt.figure(figsize=(12, 8))
        
        # منحنى التعلم للنظام القياسي
        plt.plot(train_sizes, std_train_scores, 'o-', color='r', label='تدريب (قياسي)')
        plt.plot(train_sizes, std_test_scores, 'o-', color='g', label='اختبار (قياسي)')
        plt.fill_between(train_sizes, 
                         [a - b for a, b in zip(std_train_scores, std_train_std)],
                         [a + b for a, b in zip(std_train_scores, std_train_std)], 
                         alpha=0.1, color='r')
        plt.fill_between(train_sizes, 
                         [a - b for a, b in zip(std_test_scores, std_test_std)],
                         [a + b for a, b in zip(std_test_scores, std_test_std)], 
                         alpha=0.1, color='g')
        
        # منحنى التعلم للنظام الأولي
        plt.plot(train_sizes, prim_train_scores, 's--', color='b', label='تدريب (أولي)')
        plt.plot(train_sizes, prim_test_scores, 's--', color='m', label='اختبار (أولي)')
        plt.fill_between(train_sizes, 
                         [a - b for a, b in zip(prim_train_scores, prim_train_std)],
                         [a + b for a, b in zip(prim_train_scores, prim_train_std)], 
                         alpha=0.1, color='b')
        plt.fill_between(train_sizes, 
                         [a - b for a, b in zip(prim_test_scores, prim_test_std)],
                         [a + b for a, b in zip(prim_test_scores, prim_test_std)], 
                         alpha=0.1, color='m')
        
        # إضافة التفاصيل
        plt.title(f'مقارنة منحنى التعلم للمهمة: {task_type}')
        plt.xlabel('حجم مجموعة التدريب (نسبة)')
        plt.ylabel('الدقة')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='lower right')
        
        # إضافة التوصية
        recommendation = comparison_results["comparison"]["overall_recommendation"]
        better_system = "القياسي" if recommendation["better_system"] == "standard" else "الأولي"
        plt.figtext(0.5, 0.01, f'النظام الموصى به: {better_system} - {recommendation["reason"]}', 
                   ha='center', fontsize=12, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})
        
        # حفظ الرسم البياني
        plt.savefig(os.path.join(plots_dir, f"{task_type}_learning_curve_comparison.png"), dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.debug(f"تم إنشاء رسم بياني لمنحنى التعلم للمهمة: {task_type}")

    def _save_learning_curve_results(self, comparison_results: Dict, task_type: str) -> None:
        """حفظ نتائج تحليل منحنى التعلم
        
        المعاملات:
            comparison_results (Dict): نتائج المقارنة
            task_type (str): نوع المهمة
        """
        # إنشاء اسم ملف فريد
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{task_type}_learning_curve_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        # حفظ النتائج في ملف JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comparison_results, f, ensure_ascii=False, indent=2)
            
        logger.info(f"تم حفظ نتائج تحليل منحنى التعلم في {filepath}")

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "comparative_analysis": {
            "results_dir": "/tmp/comparative_analysis_results",
            "generate_plots": True
        }
    }
    
    # تهيئة المحلل
    comparative_analyzer = ImageSystemsComparativeAnalyzer(dummy_config)
    
    # محاكاة مجموعة بيانات
    import tempfile
    import shutil
    
    # إنشاء مجلد مؤقت لمجموعة البيانات
    dataset_dir = tempfile.mkdtemp()
    
    # إنشاء مجلدات للفئات
    os.makedirs(os.path.join(dataset_dir, "healthy"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "diseased"), exist_ok=True)
    
    # إنشاء صور وهمية
    for i in range(10):
        # صور سليمة
        img = np.ones((100, 100, 3), dtype=np.uint8) * np.array([0, 255, 0], dtype=np.uint8)  # صورة خضراء
        cv2.imwrite(os.path.join(dataset_dir, "healthy", f"healthy_{i}.jpg"), img)
        
        # صور مصابة
        img = np.ones((100, 100, 3), dtype=np.uint8) * np.array([0, 100, 0], dtype=np.uint8)  # صورة خضراء داكنة
        cv2.circle(img, (50, 50), 20, (0, 0, 255), -1)  # دائرة حمراء
        cv2.imwrite(os.path.join(dataset_dir, "diseased", f"diseased_{i}.jpg"), img)
    
    # اختبار المقارنة
    print("\n--- اختبار مقارنة أداء التعلم --- ")
    comparison_results = comparative_analyzer.compare_learning_performance(
        dataset_dir,
        task_type="disease_classification"
    )
    
    # عرض النتائج
    if "error" not in comparison_results:
        recommendation = comparison_results.get("overall_recommendation", {})
        print(f"\nالنظام الموصى به: {recommendation.get("recommended_system")}")
        print(f"السبب: {recommendation.get("reason")}")
        
        metrics = comparison_results.get("metrics_comparison", {})
        print("\nمقارنة المقاييس:")
        for metric, values in metrics.items():
            print(f"  {metric}: قياسي={values.get("standard", 0):.4f}, أولي={values.get("primitive", 0):.4f}, الفرق={values.get("difference", 0):.4f}")
    else:
        print(f"خطأ: {comparison_results.get("error")}")
    
    # اختبار تحليل منحنى التعلم
    print("\n--- اختبار تحليل منحنى التعلم --- ")
    learning_curve_results = comparative_analyzer.analyze_learning_curve(
        dataset_dir,
        task_type="disease_classification",
        train_sizes=[0.2, 0.4, 0.6, 0.8, 1.0]
    )
    
    # عرض النتائج
    if "error" not in learning_curve_results:
        recommendation = learning_curve_results.get("comparison", {}).get("overall_recommendation", {})
        print(f"\nالنظام الموصى به: {recommendation.get("better_system")}")
        print(f"السبب: {recommendation.get("reason")}")
        
        final_accuracy = learning_curve_results.get("comparison", {}).get("final_accuracy", {})
        print("\nالدقة النهائية:")
        print(f"  قياسي: {final_accuracy.get("standard", 0):.4f}")
        print(f"  أولي: {final_accuracy.get("primitive", 0):.4f}")
        print(f"  النظام الأفضل: {final_accuracy.get("better_system")}")
    else:
        print(f"خطأ: {learning_curve_results.get("error")}")
    
    # تنظيف
    shutil.rmtree(dataset_dir)
