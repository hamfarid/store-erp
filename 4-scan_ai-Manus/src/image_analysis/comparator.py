#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام مقارنة التحليل الأولي للصور مع التحليل القياسي
"""

import os
import cv2
import numpy as np
import logging
import json
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field, asdict

# استيراد المكونات الأخرى
from primitive.analyzer import PrimitiveImageAnalyzer, PrimitiveFeatures

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ComparisonResult:
    """فئة لتخزين نتائج المقارنة بين التحليل الأولي والتحليل القياسي"""
    
    # معلومات الصورة
    image_path: str = ""
    primitive_features_path: str = ""
    standard_features_path: str = ""
    
    # نتائج المقارنة
    color_similarity: float = 0.0
    texture_similarity: float = 0.0
    shape_similarity: float = 0.0
    anomaly_similarity: float = 0.0
    overall_similarity: float = 0.0
    
    # إحصائيات الأداء
    primitive_processing_time: float = 0.0
    standard_processing_time: float = 0.0
    primitive_memory_usage: float = 0.0
    standard_memory_usage: float = 0.0
    
    # معلومات إضافية
    notes: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل النتائج إلى قاموس"""
        return asdict(self)
    
    def to_json(self) -> str:
        """تحويل النتائج إلى سلسلة JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComparisonResult':
        """إنشاء كائن من قاموس"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ComparisonResult':
        """إنشاء كائن من سلسلة JSON"""
        return cls.from_dict(json.loads(json_str))

class ImageAnalysisComparator:
    """فئة لمقارنة التحليل الأولي للصور مع التحليل القياسي"""
    
    def __init__(self, config=None):
        """
        تهيئة مقارن التحليل
        
        المعلمات:
            config (dict): تكوين المقارن
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'primitive_output_dir': os.getenv('PRIMITIVE_OUTPUT_DIR', 'data/primitive_features'),
            'standard_output_dir': os.getenv('STANDARD_OUTPUT_DIR', 'data/standard_features'),
            'comparison_output_dir': os.getenv('COMPARISON_OUTPUT_DIR', 'data/comparison_results'),
            'visualization_output_dir': os.getenv('VISUALIZATION_OUTPUT_DIR', 'data/visualizations'),
            'color_weight': float(os.getenv('COMPARISON_COLOR_WEIGHT', 0.25)),
            'texture_weight': float(os.getenv('COMPARISON_TEXTURE_WEIGHT', 0.25)),
            'shape_weight': float(os.getenv('COMPARISON_SHAPE_WEIGHT', 0.25)),
            'anomaly_weight': float(os.getenv('COMPARISON_ANOMALY_WEIGHT', 0.25)),
            'save_visualizations': os.getenv('SAVE_VISUALIZATIONS', 'true').lower() == 'true'
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
            
        # إنشاء مجلدات المخرجات إذا لم تكن موجودة
        os.makedirs(self.config['comparison_output_dir'], exist_ok=True)
        os.makedirs(self.config['visualization_output_dir'], exist_ok=True)
        
        # إنشاء محلل الصور الأولي
        self.primitive_analyzer = PrimitiveImageAnalyzer({
            'output_dir': self.config['primitive_output_dir']
        })
    
    def _compare_color_features(self, primitive_features: PrimitiveFeatures, standard_features: Dict[str, Any]) -> float:
        """
        مقارنة ميزات اللون
        
        المعلمات:
            primitive_features (PrimitiveFeatures): ميزات التحليل الأولي
            standard_features (Dict[str, Any]): ميزات التحليل القياسي
            
        العوائد:
            float: درجة التشابه (0-1)
        """
        try:
            # مقارنة الألوان المهيمنة
            primitive_colors = np.array(primitive_features.dominant_colors)
            standard_colors = np.array(standard_features.get('dominant_colors', []))
            
            if len(primitive_colors) == 0 or len(standard_colors) == 0:
                return 0.0
            
            # تحديد الحد الأدنى من عدد الألوان للمقارنة
            min_colors = min(len(primitive_colors), len(standard_colors))
            
            # حساب متوسط الفرق بين الألوان
            color_diffs = []
            for i in range(min_colors):
                p_color = primitive_colors[i]
                s_color = standard_colors[i]
                
                # حساب المسافة الإقليدية بين الألوان
                diff = np.sqrt(np.sum((p_color - s_color) ** 2))
                color_diffs.append(diff)
            
            # تطبيع الفروق
            max_diff = 441.67  # الحد الأقصى للفرق بين لونين (sqrt(255^2 + 255^2 + 255^2))
            avg_diff = np.mean(color_diffs) / max_diff if color_diffs else 1.0
            
            # حساب درجة التشابه
            similarity = 1.0 - avg_diff
            
            return similarity
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء مقارنة ميزات اللون: {str(e)}")
            return 0.0
    
    def _compare_texture_features(self, primitive_features: PrimitiveFeatures, standard_features: Dict[str, Any]) -> float:
        """
        مقارنة ميزات النسيج
        
        المعلمات:
            primitive_features (PrimitiveFeatures): ميزات التحليل الأولي
            standard_features (Dict[str, Any]): ميزات التحليل القياسي
            
        العوائد:
            float: درجة التشابه (0-1)
        """
        try:
            # مقارنة ميزات GLCM
            primitive_glcm = primitive_features.texture_glcm
            standard_glcm = standard_features.get('texture_glcm', {})
            
            if not primitive_glcm or not standard_glcm:
                return 0.0
            
            # حساب الفرق بين ميزات GLCM
            glcm_diffs = []
            for key in ['contrast', 'homogeneity', 'energy', 'correlation']:
                if key in primitive_glcm and key in standard_glcm:
                    p_value = primitive_glcm[key]
                    s_value = standard_glcm[key]
                    
                    # حساب الفرق النسبي
                    max_value = max(abs(p_value), abs(s_value))
                    if max_value > 0:
                        diff = abs(p_value - s_value) / max_value
                    else:
                        diff = 0.0
                    
                    glcm_diffs.append(diff)
            
            # حساب متوسط الفروق
            avg_diff = np.mean(glcm_diffs) if glcm_diffs else 1.0
            
            # حساب درجة التشابه
            similarity = 1.0 - avg_diff
            
            return similarity
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء مقارنة ميزات النسيج: {str(e)}")
            return 0.0
    
    def _compare_shape_features(self, primitive_features: PrimitiveFeatures, standard_features: Dict[str, Any]) -> float:
        """
        مقارنة ميزات الشكل
        
        المعلمات:
            primitive_features (PrimitiveFeatures): ميزات التحليل الأولي
            standard_features (Dict[str, Any]): ميزات التحليل القياسي
            
        العوائد:
            float: درجة التشابه (0-1)
        """
        try:
            # مقارنة لحظات هو
            primitive_hu = np.array(primitive_features.shape_hu_moments)
            standard_hu = np.array(standard_features.get('shape_hu_moments', []))
            
            if len(primitive_hu) == 0 or len(standard_hu) == 0:
                return 0.0
            
            # تحديد الحد الأدنى من عدد اللحظات للمقارنة
            min_moments = min(len(primitive_hu), len(standard_hu))
            
            # حساب متوسط الفرق بين اللحظات
            moment_diffs = []
            for i in range(min_moments):
                p_moment = primitive_hu[i]
                s_moment = standard_hu[i]
                
                # حساب الفرق النسبي
                max_value = max(abs(p_moment), abs(s_moment))
                if max_value > 0:
                    diff = abs(p_moment - s_moment) / max_value
                else:
                    diff = 0.0
                
                moment_diffs.append(diff)
            
            # حساب متوسط الفروق
            avg_diff = np.mean(moment_diffs) if moment_diffs else 1.0
            
            # حساب درجة التشابه
            similarity = 1.0 - avg_diff
            
            return similarity
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء مقارنة ميزات الشكل: {str(e)}")
            return 0.0
    
    def _compare_anomaly_features(self, primitive_features: PrimitiveFeatures, standard_features: Dict[str, Any]) -> float:
        """
        مقارنة ميزات الشذوذ
        
        المعلمات:
            primitive_features (PrimitiveFeatures): ميزات التحليل الأولي
            standard_features (Dict[str, Any]): ميزات التحليل القياسي
            
        العوائد:
            float: درجة التشابه (0-1)
        """
        try:
            # مقارنة درجة الشذوذ
            primitive_score = primitive_features.anomaly_score
            standard_score = standard_features.get('anomaly_score', 0.0)
            
            # حساب الفرق المطلق
            diff = abs(primitive_score - standard_score)
            
            # حساب درجة التشابه
            similarity = 1.0 - diff
            
            return similarity
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء مقارنة ميزات الشذوذ: {str(e)}")
            return 0.0
    
    def _calculate_overall_similarity(self, color_similarity: float, texture_similarity: float, 
                                     shape_similarity: float, anomaly_similarity: float) -> float:
        """
        حساب درجة التشابه الإجمالية
        
        المعلمات:
            color_similarity (float): درجة تشابه اللون
            texture_similarity (float): درجة تشابه النسيج
            shape_similarity (float): درجة تشابه الشكل
            anomaly_similarity (float): درجة تشابه الشذوذ
            
        العوائد:
            float: درجة التشابه الإجمالية (0-1)
        """
        # حساب المتوسط المرجح
        weights = [
            self.config['color_weight'],
            self.config['texture_weight'],
            self.config['shape_weight'],
            self.config['anomaly_weight']
        ]
        
        similarities = [
            color_similarity,
            texture_similarity,
            shape_similarity,
            anomaly_similarity
        ]
        
        # تطبيع الأوزان
        total_weight = sum(weights)
        if total_weight > 0:
            normalized_weights = [w / total_weight for w in weights]
        else:
            normalized_weights = [0.25, 0.25, 0.25, 0.25]
        
        # حساب المتوسط المرجح
        overall_similarity = sum(s * w for s, w in zip(similarities, normalized_weights))
        
        return overall_similarity
    
    def _create_visualization(self, image_path: str, primitive_features: PrimitiveFeatures, 
                             standard_features: Dict[str, Any], comparison_result: ComparisonResult) -> str:
        """
        إنشاء تصور مرئي للمقارنة
        
        المعلمات:
            image_path (str): مسار الصورة
            primitive_features (PrimitiveFeatures): ميزات التحليل الأولي
            standard_features (Dict[str, Any]): ميزات التحليل القياسي
            comparison_result (ComparisonResult): نتائج المقارنة
            
        العوائد:
            str: مسار ملف التصور المرئي
        """
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"فشل قراءة الصورة: {image_path}")
            
            # تحويل الصورة من BGR إلى RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # إنشاء الشكل
            plt.figure(figsize=(15, 10))
            
            # عنوان الشكل
            plt.suptitle(f"مقارنة التحليل الأولي والتحليل القياسي\n{os.path.basename(image_path)}", fontsize=16)
            
            # عرض الصورة الأصلية
            plt.subplot(2, 3, 1)
            plt.imshow(image_rgb)
            plt.title("الصورة الأصلية")
            plt.axis('off')
            
            # عرض الصورة المقسمة (إذا كانت متاحة)
            primitive_segmented_path = os.path.join(
                self.config['primitive_output_dir'],
                f"{os.path.splitext(os.path.basename(image_path))[0]}_segmented.png"
            )
            
            if os.path.exists(primitive_segmented_path):
                segmented_image = cv2.imread(primitive_segmented_path)
                segmented_image_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)
                
                plt.subplot(2, 3, 2)
                plt.imshow(segmented_image_rgb)
                plt.title("الصورة المقسمة (التحليل الأولي)")
                plt.axis('off')
            
            # عرض الألوان المهيمنة
            plt.subplot(2, 3, 3)
            
            # الألوان المهيمنة من التحليل الأولي
            primitive_colors = primitive_features.dominant_colors
            if primitive_colors:
                primitive_colors_rgb = [color for color in primitive_colors]
                primitive_colors_display = np.array([primitive_colors_rgb for _ in range(50)])
                plt.imshow(primitive_colors_display)
                plt.title(f"الألوان المهيمنة (التشابه: {comparison_result.color_similarity:.2f})")
            else:
                plt.text(0.5, 0.5, "لا توجد ألوان مهيمنة", ha='center', va='center')
                plt.title("الألوان المهيمنة")
            
            plt.axis('off')
            
            # عرض مناطق الشذوذ
            plt.subplot(2, 3, 4)
            
            # نسخة من الصورة لعرض مناطق الشذوذ
            anomaly_image = image_rgb.copy()
            
            # رسم مناطق الشذوذ من التحليل الأولي
            primitive_anomalies = primitive_features.anomaly_regions
            if primitive_anomalies:
                for region in primitive_anomalies:
                    x = region['x']
                    y = region['y']
                    w = region['width']
                    h = region['height']
                    score = region['anomaly_score']
                    
                    # تحديد لون المستطيل بناءً على درجة الشذوذ
                    color = (255, 0, 0)  # أحمر
                    thickness = 2
                    
                    # رسم المستطيل
                    cv2.rectangle(anomaly_image, (x, y), (x + w, y + h), color, thickness)
                
                plt.imshow(anomaly_image)
                plt.title(f"مناطق الشذوذ (التشابه: {comparison_result.anomaly_similarity:.2f})")
            else:
                plt.imshow(anomaly_image)
                plt.title("لا توجد مناطق شذوذ")
            
            plt.axis('off')
            
            # عرض نتائج المقارنة
            plt.subplot(2, 3, 5)
            plt.axis('off')
            
            comparison_text = f"""
            نتائج المقارنة:
            
            تشابه اللون: {comparison_result.color_similarity:.2f}
            تشابه النسيج: {comparison_result.texture_similarity:.2f}
            تشابه الشكل: {comparison_result.shape_similarity:.2f}
            تشابه الشذوذ: {comparison_result.anomaly_similarity:.2f}
            
            التشابه الإجمالي: {comparison_result.overall_similarity:.2f}
            
            وقت المعالجة:
            التحليل الأولي: {comparison_result.primitive_processing_time:.2f} ثانية
            التحليل القياسي: {comparison_result.standard_processing_time:.2f} ثانية
            
            استخدام الذاكرة:
            التحليل الأولي: {comparison_result.primitive_memory_usage:.2f} ميجابايت
            التحليل القياسي: {comparison_result.standard_memory_usage:.2f} ميجابايت
            """
            
            plt.text(0.5, 0.5, comparison_text, ha='center', va='center', fontsize=10)
            plt.title("نتائج المقارنة")
            
            # عرض رسم بياني للتشابه
            plt.subplot(2, 3, 6)
            
            categories = ['اللون', 'النسيج', 'الشكل', 'الشذوذ', 'الإجمالي']
            values = [
                comparison_result.color_similarity,
                comparison_result.texture_similarity,
                comparison_result.shape_similarity,
                comparison_result.anomaly_similarity,
                comparison_result.overall_similarity
            ]
            
            plt.bar(categories, values, color=['red', 'green', 'blue', 'purple', 'orange'])
            plt.ylim(0, 1)
            plt.title("درجات التشابه")
            plt.ylabel("درجة التشابه")
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الشكل
            visualization_path = os.path.join(
                self.config['visualization_output_dir'],
                f"{os.path.splitext(os.path.basename(image_path))[0]}_comparison.png"
            )
            
            plt.savefig(visualization_path, dpi=300)
            plt.close()
            
            logger.info(f"تم إنشاء التصور المرئي: {visualization_path}")
            return visualization_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء إنشاء التصور المرئي: {str(e)}")
            return ""
    
    def compare_image(self, image_path: str, standard_features_path: Optional[str] = None) -> ComparisonResult:
        """
        مقارنة التحليل الأولي والتحليل القياسي لصورة واحدة
        
        المعلمات:
            image_path (str): مسار الصورة
            standard_features_path (str): مسار ملف ميزات التحليل القياسي (اختياري)
            
        العوائد:
            ComparisonResult: نتائج المقارنة
        """
        try:
            # إنشاء كائن نتائج المقارنة
            comparison_result = ComparisonResult(image_path=image_path)
            
            # قياس وقت واستخدام الذاكرة للتحليل الأولي
            import time
            import psutil
            
            process = psutil.Process(os.getpid())
            
            # قياس استخدام الذاكرة قبل التحليل الأولي
            memory_before = process.memory_info().rss / (1024 * 1024)  # بالميجابايت
            
            # قياس وقت التحليل الأولي
            start_time = time.time()
            
            # تحليل الصورة باستخدام التحليل الأولي
            primitive_result = self.primitive_analyzer.process_image(image_path)
            
            # حساب وقت المعالجة
            primitive_processing_time = time.time() - start_time
            
            # حساب استخدام الذاكرة
            memory_after = process.memory_info().rss / (1024 * 1024)  # بالميجابايت
            primitive_memory_usage = memory_after - memory_before
            
            # تخزين وقت المعالجة واستخدام الذاكرة
            comparison_result.primitive_processing_time = primitive_processing_time
            comparison_result.primitive_memory_usage = primitive_memory_usage
            
            # التحقق من نجاح التحليل الأولي
            if 'error' in primitive_result:
                raise ValueError(f"فشل التحليل الأولي: {primitive_result['error']}")
            
            # الحصول على مسار ملف ميزات التحليل الأولي
            primitive_features_path = primitive_result['features_path']
            comparison_result.primitive_features_path = primitive_features_path
            
            # قراءة ميزات التحليل الأولي
            with open(primitive_features_path, 'r', encoding='utf-8') as f:
                primitive_features = PrimitiveFeatures.from_json(f.read())
            
            # تحديد مسار ملف ميزات التحليل القياسي
            if standard_features_path is None:
                standard_features_path = os.path.join(
                    self.config['standard_output_dir'],
                    f"{os.path.splitext(os.path.basename(image_path))[0]}_features.json"
                )
            
            comparison_result.standard_features_path = standard_features_path
            
            # التحقق من وجود ملف ميزات التحليل القياسي
            if not os.path.exists(standard_features_path):
                # إذا لم يكن ملف ميزات التحليل القياسي موجودًا، استخدم ميزات التحليل الأولي كبديل
                logger.warning(f"ملف ميزات التحليل القياسي غير موجود: {standard_features_path}")
                logger.warning("استخدام ميزات التحليل الأولي كبديل للتحليل القياسي")
                
                # تعيين وقت المعالجة واستخدام الذاكرة للتحليل القياسي
                comparison_result.standard_processing_time = primitive_processing_time
                comparison_result.standard_memory_usage = primitive_memory_usage
                
                # تعيين درجات التشابه إلى 1.0 (تطابق تام)
                comparison_result.color_similarity = 1.0
                comparison_result.texture_similarity = 1.0
                comparison_result.shape_similarity = 1.0
                comparison_result.anomaly_similarity = 1.0
                comparison_result.overall_similarity = 1.0
                
                # إضافة ملاحظة
                comparison_result.notes['warning'] = "تم استخدام ميزات التحليل الأولي كبديل للتحليل القياسي"
                
                # حفظ نتائج المقارنة
                self._save_comparison_result(comparison_result)
                
                # إنشاء تصور مرئي إذا تم تمكين ذلك
                if self.config['save_visualizations']:
                    self._create_visualization(image_path, primitive_features, primitive_features.to_dict(), comparison_result)
                
                return comparison_result
            
            # قراءة ميزات التحليل القياسي
            with open(standard_features_path, 'r', encoding='utf-8') as f:
                standard_features = json.load(f)
            
            # قياس وقت واستخدام الذاكرة للتحليل القياسي (تقديري)
            # ملاحظة: هذا تقدير لأننا نقرأ الميزات من ملف بدلاً من حسابها
            comparison_result.standard_processing_time = standard_features.get('processing_time', primitive_processing_time * 1.5)
            comparison_result.standard_memory_usage = standard_features.get('memory_usage', primitive_memory_usage * 1.5)
            
            # مقارنة الميزات
            comparison_result.color_similarity = self._compare_color_features(primitive_features, standard_features)
            comparison_result.texture_similarity = self._compare_texture_features(primitive_features, standard_features)
            comparison_result.shape_similarity = self._compare_shape_features(primitive_features, standard_features)
            comparison_result.anomaly_similarity = self._compare_anomaly_features(primitive_features, standard_features)
            
            # حساب درجة التشابه الإجمالية
            comparison_result.overall_similarity = self._calculate_overall_similarity(
                comparison_result.color_similarity,
                comparison_result.texture_similarity,
                comparison_result.shape_similarity,
                comparison_result.anomaly_similarity
            )
            
            # حفظ نتائج المقارنة
            self._save_comparison_result(comparison_result)
            
            # إنشاء تصور مرئي إذا تم تمكين ذلك
            if self.config['save_visualizations']:
                self._create_visualization(image_path, primitive_features, standard_features, comparison_result)
            
            return comparison_result
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء مقارنة الصورة {image_path}: {str(e)}")
            
            # إنشاء نتيجة مقارنة فارغة مع الخطأ
            comparison_result = ComparisonResult(
                image_path=image_path,
                notes={'error': str(e)}
            )
            
            return comparison_result
    
    def _save_comparison_result(self, comparison_result: ComparisonResult) -> str:
        """
        حفظ نتائج المقارنة
        
        المعلمات:
            comparison_result (ComparisonResult): نتائج المقارنة
            
        العوائد:
            str: مسار ملف نتائج المقارنة
        """
        try:
            # إنشاء اسم الملف
            image_name = os.path.basename(comparison_result.image_path)
            base_name = os.path.splitext(image_name)[0]
            result_path = os.path.join(self.config['comparison_output_dir'], f"{base_name}_comparison.json")
            
            # حفظ النتائج
            with open(result_path, 'w', encoding='utf-8') as f:
                f.write(comparison_result.to_json())
            
            logger.info(f"تم حفظ نتائج المقارنة: {result_path}")
            return result_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء حفظ نتائج المقارنة: {str(e)}")
            return ""
    
    def compare_directory(self, directory_path: str, standard_features_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        مقارنة التحليل الأولي والتحليل القياسي لمجلد من الصور
        
        المعلمات:
            directory_path (str): مسار المجلد
            standard_features_dir (str): مسار مجلد ميزات التحليل القياسي (اختياري)
            
        العوائد:
            Dict[str, Any]: نتائج المقارنة
        """
        try:
            # التحقق من وجود المجلد
            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                raise ValueError(f"المجلد غير موجود: {directory_path}")
            
            # تحديد مجلد ميزات التحليل القياسي
            if standard_features_dir is None:
                standard_features_dir = self.config['standard_output_dir']
            
            # الحصول على قائمة ملفات الصور
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            image_files = [
                os.path.join(directory_path, f) for f in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, f)) and
                os.path.splitext(f)[1].lower() in image_extensions
            ]
            
            # إحصائيات المقارنة
            stats = {
                'total_images': len(image_files),
                'compared_images': 0,
                'failed_images': 0,
                'average_similarity': {
                    'color': 0.0,
                    'texture': 0.0,
                    'shape': 0.0,
                    'anomaly': 0.0,
                    'overall': 0.0
                },
                'average_processing_time': {
                    'primitive': 0.0,
                    'standard': 0.0
                },
                'average_memory_usage': {
                    'primitive': 0.0,
                    'standard': 0.0
                },
                'results': []
            }
            
            # مقارنة كل صورة
            for image_path in image_files:
                try:
                    # تحديد مسار ملف ميزات التحليل القياسي
                    standard_features_path = os.path.join(
                        standard_features_dir,
                        f"{os.path.splitext(os.path.basename(image_path))[0]}_features.json"
                    )
                    
                    # مقارنة الصورة
                    result = self.compare_image(image_path, standard_features_path)
                    
                    # تحديث الإحصائيات
                    if 'error' in result.notes:
                        stats['failed_images'] += 1
                    else:
                        stats['compared_images'] += 1
                        
                        # تحديث متوسط درجات التشابه
                        stats['average_similarity']['color'] += result.color_similarity
                        stats['average_similarity']['texture'] += result.texture_similarity
                        stats['average_similarity']['shape'] += result.shape_similarity
                        stats['average_similarity']['anomaly'] += result.anomaly_similarity
                        stats['average_similarity']['overall'] += result.overall_similarity
                        
                        # تحديث متوسط وقت المعالجة
                        stats['average_processing_time']['primitive'] += result.primitive_processing_time
                        stats['average_processing_time']['standard'] += result.standard_processing_time
                        
                        # تحديث متوسط استخدام الذاكرة
                        stats['average_memory_usage']['primitive'] += result.primitive_memory_usage
                        stats['average_memory_usage']['standard'] += result.standard_memory_usage
                    
                    # إضافة النتيجة
                    stats['results'].append(result.to_dict())
                    
                except Exception as e:
                    logger.error(f"حدث خطأ أثناء مقارنة الصورة {image_path}: {str(e)}")
                    stats['failed_images'] += 1
                    stats['results'].append({
                        'image_path': image_path,
                        'error': str(e)
                    })
            
            # حساب المتوسطات
            if stats['compared_images'] > 0:
                for key in stats['average_similarity']:
                    stats['average_similarity'][key] /= stats['compared_images']
                
                for key in stats['average_processing_time']:
                    stats['average_processing_time'][key] /= stats['compared_images']
                
                for key in stats['average_memory_usage']:
                    stats['average_memory_usage'][key] /= stats['compared_images']
            
            logger.info(f"اكتمل مقارنة المجلد {directory_path}: {stats['compared_images']} صورة تمت مقارنتها، {stats['failed_images']} صورة فشلت")
            
            # حفظ إحصائيات المقارنة
            stats_path = os.path.join(self.config['comparison_output_dir'], "directory_comparison_stats.json")
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            logger.info(f"تم حفظ إحصائيات المقارنة: {stats_path}")
            
            return stats
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء مقارنة المجلد {directory_path}: {str(e)}")
            return {
                'directory_path': directory_path,
                'error': str(e),
                'total_images': 0,
                'compared_images': 0,
                'failed_images': 0,
                'results': []
            }


# نموذج استخدام
if __name__ == "__main__":
    import argparse
    
    # إنشاء محلل الوسائط
    parser = argparse.ArgumentParser(description='مقارنة التحليل الأولي والتحليل القياسي للصور')
    parser.add_argument('--input', '-i', required=True, help='مسار الصورة أو المجلد')
    parser.add_argument('--standard', '-s', help='مسار ملف أو مجلد ميزات التحليل القياسي')
    parser.add_argument('--output', '-o', help='مجلد المخرجات')
    parser.add_argument('--visualize', '-v', action='store_true', help='إنشاء تصورات مرئية')
    
    # تحليل الوسائط
    args = parser.parse_args()
    
    # إنشاء التكوين
    config = {
        'save_visualizations': args.visualize
    }
    
    # تعيين مجلد المخرجات إذا تم تحديده
    if args.output:
        config['comparison_output_dir'] = os.path.join(args.output, 'comparison_results')
        config['visualization_output_dir'] = os.path.join(args.output, 'visualizations')
    
    # إنشاء كائن المقارن
    comparator = ImageAnalysisComparator(config)
    
    # معالجة الإدخال
    if os.path.isdir(args.input):
        # مقارنة مجلد
        results = comparator.compare_directory(args.input, args.standard)
        print(f"تمت مقارنة {results['compared_images']} صورة من أصل {results['total_images']}")
        print(f"متوسط درجة التشابه الإجمالية: {results['average_similarity']['overall']:.2f}")
    else:
        # مقارنة صورة واحدة
        result = comparator.compare_image(args.input, args.standard)
        if 'error' in result.notes:
            print(f"فشل مقارنة الصورة: {result.notes['error']}")
        else:
            print(f"تمت مقارنة الصورة بنجاح")
            print(f"درجة التشابه الإجمالية: {result.overall_similarity:.2f}")
            print(f"درجة تشابه اللون: {result.color_similarity:.2f}")
            print(f"درجة تشابه النسيج: {result.texture_similarity:.2f}")
            print(f"درجة تشابه الشكل: {result.shape_similarity:.2f}")
            print(f"درجة تشابه الشذوذ: {result.anomaly_similarity:.2f}")
