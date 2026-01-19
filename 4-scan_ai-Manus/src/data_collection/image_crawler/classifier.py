#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام تصنيف صور الأمراض النباتية حسب نوع المحصول
"""

import os
import cv2
import logging
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlantDiseaseImageClassifier:
    """فئة لتصنيف صور الأمراض النباتية حسب نوع المحصول"""
    
    def __init__(self, config=None):
        """
        تهيئة مصنف صور الأمراض النباتية
        
        المعلمات:
            config (dict): تكوين المصنف
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'input_dir': os.getenv('IMAGE_INPUT_DIR', 'data/images/unclassified'),
            'output_base_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'categories': ['vegetables', 'fruits', 'crops'],
            'color_features': {
                'vegetables': {
                    'green_range': [(30, 50, 20), (80, 255, 255)],  # نطاق اللون الأخضر في HSV
                    'min_green_ratio': 0.3  # الحد الأدنى لنسبة اللون الأخضر
                },
                'fruits': {
                    'color_ranges': [
                        [(0, 50, 50), (10, 255, 255)],  # نطاق اللون الأحمر في HSV (الجزء الأول)
                        [(170, 50, 50), (180, 255, 255)],  # نطاق اللون الأحمر في HSV (الجزء الثاني)
                        [(20, 100, 100), (30, 255, 255)]  # نطاق اللون الأصفر في HSV
                    ],
                    'min_color_ratio': 0.2  # الحد الأدنى لنسبة الألوان المميزة
                }
            },
            'texture_features': {
                'crops': {
                    'min_texture_variance': 500  # الحد الأدنى لتباين الملمس
                }
            },
            'max_threads': int(os.getenv('MAX_CLASSIFIER_THREADS', 4)),
            'confidence_threshold': 0.6  # عتبة الثقة للتصنيف
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
    
    def _extract_color_features(self, image):
        """
        استخراج ميزات اللون من الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            
        العوائد:
            dict: قاموس بميزات اللون
        """
        # تحويل الصورة إلى فضاء اللون HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # حساب نسبة اللون الأخضر (للخضروات)
        green_mask = cv2.inRange(
            hsv_image,
            np.array(self.config['color_features']['vegetables']['green_range'][0]),
            np.array(self.config['color_features']['vegetables']['green_range'][1])
        )
        green_ratio = np.count_nonzero(green_mask) / (image.shape[0] * image.shape[1])
        
        # حساب نسبة الألوان المميزة للفواكه
        fruit_color_ratio = 0
        for color_range in self.config['color_features']['fruits']['color_ranges']:
            color_mask = cv2.inRange(
                hsv_image,
                np.array(color_range[0]),
                np.array(color_range[1])
            )
            fruit_color_ratio += np.count_nonzero(color_mask) / (image.shape[0] * image.shape[1])
        
        return {
            'green_ratio': green_ratio,
            'fruit_color_ratio': fruit_color_ratio
        }
    
    def _extract_texture_features(self, image):
        """
        استخراج ميزات الملمس من الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            
        العوائد:
            dict: قاموس بميزات الملمس
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب تباين الملمس
        texture_variance = np.var(gray_image)
        
        # حساب مصفوفة التواجد المشترك للمستوى الرمادي (GLCM)
        # هذا مبسط، يمكن استخدام مكتبات مثل scikit-image للحصول على GLCM كامل
        texture_entropy = -np.sum(np.multiply(gray_image / 255.0, np.log2(gray_image / 255.0 + 1e-10)))
        
        return {
            'texture_variance': texture_variance,
            'texture_entropy': texture_entropy
        }
    
    def _extract_shape_features(self, image):
        """
        استخراج ميزات الشكل من الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            
        العوائد:
            dict: قاموس بميزات الشكل
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # تطبيق عتبة ثنائية
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        
        # العثور على الحدود
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # حساب ميزات الشكل
        if contours:
            # اختيار أكبر محيط
            largest_contour = max(contours, key=cv2.contourArea)
            
            # حساب المساحة والمحيط
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # حساب الاستدارة
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # حساب المستطيل المحيط
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / h if h > 0 else 0
            
            return {
                'area': area,
                'perimeter': perimeter,
                'circularity': circularity,
                'aspect_ratio': aspect_ratio
            }
        else:
            return {
                'area': 0,
                'perimeter': 0,
                'circularity': 0,
                'aspect_ratio': 0
            }
    
    def _classify_image(self, image_features):
        """
        تصنيف الصورة بناءً على الميزات المستخرجة
        
        المعلمات:
            image_features (dict): ميزات الصورة
            
        العوائد:
            tuple: (الفئة المتوقعة، درجة الثقة)
        """
        # حساب درجات الثقة لكل فئة
        confidence_scores = {
            'vegetables': 0.0,
            'fruits': 0.0,
            'crops': 0.0
        }
        
        # تصنيف الخضروات بناءً على نسبة اللون الأخضر
        if image_features['color']['green_ratio'] >= self.config['color_features']['vegetables']['min_green_ratio']:
            confidence_scores['vegetables'] += 0.6
        
        # تصنيف الفواكه بناءً على نسبة الألوان المميزة
        if image_features['color']['fruit_color_ratio'] >= self.config['color_features']['fruits']['min_color_ratio']:
            confidence_scores['fruits'] += 0.6
        
        # تصنيف المحاصيل بناءً على تباين الملمس
        if image_features['texture']['texture_variance'] >= self.config['texture_features']['crops']['min_texture_variance']:
            confidence_scores['crops'] += 0.6
        
        # تعديل درجات الثقة بناءً على ميزات الشكل
        if image_features['shape']['circularity'] > 0.7:
            confidence_scores['fruits'] += 0.2
        elif image_features['shape']['aspect_ratio'] > 2.0:
            confidence_scores['crops'] += 0.2
        
        # تحديد الفئة المتوقعة
        predicted_category = max(confidence_scores, key=confidence_scores.get)
        confidence = confidence_scores[predicted_category]
        
        return predicted_category, confidence
    
    def classify_image(self, image_path):
        """
        تصنيف صورة بناءً على مسار الملف
        
        المعلمات:
            image_path (str): مسار ملف الصورة
            
        العوائد:
            tuple: (الفئة المتوقعة، درجة الثقة)
        """
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            
            # التحقق من قراءة الصورة بنجاح
            if image is None:
                logger.error(f"فشل قراءة الصورة: {image_path}")
                return None, 0.0
            
            # استخراج الميزات
            color_features = self._extract_color_features(image)
            texture_features = self._extract_texture_features(image)
            shape_features = self._extract_shape_features(image)
            
            # تجميع الميزات
            image_features = {
                'color': color_features,
                'texture': texture_features,
                'shape': shape_features
            }
            
            # تصنيف الصورة
            predicted_category, confidence = self._classify_image(image_features)
            
            logger.debug(f"تم تصنيف الصورة {image_path}: {predicted_category} (الثقة: {confidence:.2f})")
            return predicted_category, confidence
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تصنيف الصورة {image_path}: {str(e)}")
            return None, 0.0
    
    def classify_and_move_image(self, image_path):
        """
        تصنيف صورة ونقلها إلى المجلد المناسب
        
        المعلمات:
            image_path (str): مسار ملف الصورة
            
        العوائد:
            tuple: (مسار الملف الجديد، الفئة المتوقعة، درجة الثقة)
        """
        # تصنيف الصورة
        predicted_category, confidence = self.classify_image(image_path)
        
        # التحقق من نجاح التصنيف ودرجة الثقة
        if predicted_category is None or confidence < self.config['confidence_threshold']:
            logger.warning(f"فشل تصنيف الصورة {image_path} أو درجة الثقة منخفضة: {confidence:.2f}")
            return None, None, confidence
        
        try:
            # إنشاء مسار الملف الجديد
            image_filename = os.path.basename(image_path)
            new_image_path = os.path.join(self.config['output_base_dir'], predicted_category, image_filename)
            
            # التأكد من وجود المجلد
            os.makedirs(os.path.dirname(new_image_path), exist_ok=True)
            
            # نقل الصورة
            os.rename(image_path, new_image_path)
            
            logger.info(f"تم نقل الصورة من {image_path} إلى {new_image_path} (الفئة: {predicted_category}, الثقة: {confidence:.2f})")
            return new_image_path, predicted_category, confidence
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء نقل الصورة {image_path}: {str(e)}")
            return None, predicted_category, confidence
    
    def classify_directory(self, input_dir=None):
        """
        تصنيف جميع الصور في مجلد
        
        المعلمات:
            input_dir (str): مسار المجلد المدخل (إذا كان None، يتم استخدام المجلد الافتراضي)
            
        العوائد:
            dict: إحصائيات التصنيف
        """
        # تحديد مجلد المدخلات
        input_directory = input_dir if input_dir else self.config['input_dir']
        logger.info(f"بدء تصنيف الصور في المجلد: {input_directory}")
        
        # التحقق من وجود المجلد
        if not os.path.exists(input_directory):
            logger.error(f"المجلد غير موجود: {input_directory}")
            return {
                'total_images': 0,
                'classified_images': 0,
                'failed_images': 0,
                'classification_by_category': {}
            }
        
        # الحصول على قائمة ملفات الصور
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = [
            os.path.join(input_directory, f) for f in os.listdir(input_directory)
            if os.path.isfile(os.path.join(input_directory, f)) and
            os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        # إحصائيات التصنيف
        stats = {
            'total_images': len(image_files),
            'classified_images': 0,
            'failed_images': 0,
            'classification_by_category': {category: 0 for category in self.config['categories']}
        }
        
        # تصنيف الصور باستخدام مجموعة من الخيوط
        with ThreadPoolExecutor(max_workers=self.config['max_threads']) as executor:
            results = list(executor.map(self.classify_and_move_image, image_files))
        
        # تحليل النتائج
        for new_path, category, confidence in results:
            if new_path and category:
                stats['classified_images'] += 1
                stats['classification_by_category'][category] += 1
            else:
                stats['failed_images'] += 1
        
        logger.info(f"اكتمل تصنيف الصور: {stats}")
        return stats


# نموذج استخدام
if __name__ == "__main__":
    # تكوين المصنف
    config = {
        'input_dir': 'data/images/unclassified',
        'output_base_dir': 'data/images',
        'confidence_threshold': 0.5,
        'max_threads': 4
    }
    
    # إنشاء كائن المصنف
    classifier = PlantDiseaseImageClassifier(config)
    
    # تصنيف الصور
    stats = classifier.classify_directory()
    print(f"إحصائيات التصنيف: {stats}")
