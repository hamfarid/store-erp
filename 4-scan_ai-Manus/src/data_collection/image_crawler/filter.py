#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام تنقية صور الأمراض النباتية وإزالة الصور غير المناسبة
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

class PlantDiseaseImageFilter:
    """فئة لتنقية صور الأمراض النباتية وإزالة الصور غير المناسبة"""
    
    def __init__(self, config=None):
        """
        تهيئة مرشح صور الأمراض النباتية
        
        المعلمات:
            config (dict): تكوين المرشح
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'input_base_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'rejected_dir': os.getenv('REJECTED_IMAGES_DIR', 'data/images/rejected'),
            'categories': ['vegetables', 'fruits', 'crops'],
            'min_resolution': (224, 224),  # الحد الأدنى للدقة (العرض، الارتفاع)
            'max_resolution': (4096, 4096),  # الحد الأقصى للدقة (العرض، الارتفاع)
            'min_file_size': 10 * 1024,  # الحد الأدنى لحجم الملف (10 كيلوبايت)
            'max_file_size': 10 * 1024 * 1024,  # الحد الأقصى لحجم الملف (10 ميجابايت)
            'blur_threshold': 100,  # عتبة التشويش (قيمة Laplacian)
            'min_contrast': 40,  # الحد الأدنى للتباين
            'min_brightness': 30,  # الحد الأدنى للسطوع
            'max_brightness': 220,  # الحد الأقصى للسطوع
            'max_threads': int(os.getenv('MAX_FILTER_THREADS', 4))
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
            
        # إنشاء مجلد الصور المرفوضة إذا لم يكن موجودًا
        os.makedirs(self.config['rejected_dir'], exist_ok=True)
    
    def _check_resolution(self, image):
        """
        التحقق من دقة الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            
        العوائد:
            bool: True إذا كانت الدقة مقبولة، False خلاف ذلك
        """
        height, width = image.shape[:2]
        min_width, min_height = self.config['min_resolution']
        max_width, max_height = self.config['max_resolution']
        
        return (width >= min_width and height >= min_height and 
                width <= max_width and height <= max_height)
    
    def _check_file_size(self, file_path):
        """
        التحقق من حجم ملف الصورة
        
        المعلمات:
            file_path (str): مسار ملف الصورة
            
        العوائد:
            bool: True إذا كان حجم الملف مقبولًا، False خلاف ذلك
        """
        file_size = os.path.getsize(file_path)
        return (file_size >= self.config['min_file_size'] and 
                file_size <= self.config['max_file_size'])
    
    def _check_blur(self, image):
        """
        التحقق من تشويش الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            
        العوائد:
            bool: True إذا كانت الصورة غير مشوشة، False خلاف ذلك
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب قيمة Laplacian
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        return laplacian_var >= self.config['blur_threshold']
    
    def _check_contrast(self, image):
        """
        التحقق من تباين الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            
        العوائد:
            bool: True إذا كان التباين مقبولًا، False خلاف ذلك
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب التباين
        contrast = gray.std()
        
        return contrast >= self.config['min_contrast']
    
    def _check_brightness(self, image):
        """
        التحقق من سطوع الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            
        العوائد:
            bool: True إذا كان السطوع مقبولًا، False خلاف ذلك
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب متوسط السطوع
        brightness = gray.mean()
        
        return (brightness >= self.config['min_brightness'] and 
                brightness <= self.config['max_brightness'])
    
    def _check_duplicate(self, image, image_path, category):
        """
        التحقق من تكرار الصورة
        
        المعلمات:
            image (numpy.ndarray): صورة OpenCV
            image_path (str): مسار ملف الصورة
            category (str): فئة الصورة
            
        العوائد:
            bool: True إذا كانت الصورة غير مكررة، False خلاف ذلك
        """
        # هذه وظيفة مبسطة للتحقق من التكرار
        # في التطبيق الفعلي، يمكن استخدام تقنيات أكثر تقدمًا مثل perceptual hashing
        
        # تصغير الصورة لتسريع المقارنة
        small_image = cv2.resize(image, (32, 32))
        
        # تحويل الصورة إلى تدرج الرمادي
        gray_small = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)
        
        # الحصول على قائمة الصور في نفس الفئة
        category_dir = os.path.dirname(image_path)
        image_files = [
            os.path.join(category_dir, f) for f in os.listdir(category_dir)
            if os.path.isfile(os.path.join(category_dir, f)) and
            f != os.path.basename(image_path)
        ]
        
        # مقارنة الصورة مع الصور الأخرى
        for other_image_path in image_files:
            try:
                # قراءة الصورة الأخرى
                other_image = cv2.imread(other_image_path)
                
                # التحقق من قراءة الصورة بنجاح
                if other_image is None:
                    continue
                
                # تصغير الصورة الأخرى
                other_small = cv2.resize(other_image, (32, 32))
                
                # تحويل الصورة الأخرى إلى تدرج الرمادي
                other_gray_small = cv2.cvtColor(other_small, cv2.COLOR_BGR2GRAY)
                
                # حساب معامل الارتباط
                correlation = cv2.matchTemplate(gray_small, other_gray_small, cv2.TM_CCOEFF_NORMED)
                
                # إذا كان معامل الارتباط مرتفعًا، فالصورة مكررة
                if correlation.max() > 0.9:
                    return False
                    
            except Exception as e:
                logger.error(f"حدث خطأ أثناء مقارنة الصورة {image_path} مع {other_image_path}: {str(e)}")
        
        return True
    
    def filter_image(self, image_path):
        """
        تنقية صورة واحدة
        
        المعلمات:
            image_path (str): مسار ملف الصورة
            
        العوائد:
            tuple: (نتيجة التنقية، سبب الرفض إذا تم رفض الصورة)
        """
        try:
            # التحقق من وجود الملف
            if not os.path.exists(image_path):
                return False, "الملف غير موجود"
            
            # التحقق من حجم الملف
            if not self._check_file_size(image_path):
                return False, "حجم الملف غير مقبول"
            
            # قراءة الصورة
            image = cv2.imread(image_path)
            
            # التحقق من قراءة الصورة بنجاح
            if image is None:
                return False, "فشل قراءة الصورة"
            
            # التحقق من دقة الصورة
            if not self._check_resolution(image):
                return False, "دقة الصورة غير مقبولة"
            
            # التحقق من تشويش الصورة
            if not self._check_blur(image):
                return False, "الصورة مشوشة"
            
            # التحقق من تباين الصورة
            if not self._check_contrast(image):
                return False, "تباين الصورة منخفض"
            
            # التحقق من سطوع الصورة
            if not self._check_brightness(image):
                return False, "سطوع الصورة غير مقبول"
            
            # استخراج الفئة من مسار الملف
            path_parts = image_path.split(os.sep)
            category_index = -2  # الفئة هي المجلد قبل اسم الملف
            
            if len(path_parts) >= abs(category_index):
                category = path_parts[category_index]
                
                # التحقق من تكرار الصورة
                if not self._check_duplicate(image, image_path, category):
                    return False, "الصورة مكررة"
            
            return True, None
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تنقية الصورة {image_path}: {str(e)}")
            return False, str(e)
    
    def move_to_rejected(self, image_path, reason):
        """
        نقل صورة مرفوضة إلى مجلد الصور المرفوضة
        
        المعلمات:
            image_path (str): مسار ملف الصورة
            reason (str): سبب الرفض
            
        العوائد:
            str: مسار الملف الجديد
        """
        try:
            # إنشاء اسم الملف الجديد
            filename = os.path.basename(image_path)
            reason_slug = reason.replace(" ", "_").lower()
            new_filename = f"{reason_slug}_{filename}"
            new_path = os.path.join(self.config['rejected_dir'], new_filename)
            
            # نقل الملف
            os.rename(image_path, new_path)
            
            logger.info(f"تم نقل الصورة المرفوضة من {image_path} إلى {new_path} (السبب: {reason})")
            return new_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء نقل الصورة المرفوضة {image_path}: {str(e)}")
            return None
    
    def filter_category(self, category):
        """
        تنقية جميع الصور في فئة معينة
        
        المعلمات:
            category (str): اسم الفئة
            
        العوائد:
            dict: إحصائيات التنقية
        """
        # تحديد مجلد الفئة
        category_dir = os.path.join(self.config['input_base_dir'], category)
        
        # التحقق من وجود المجلد
        if not os.path.exists(category_dir):
            logger.error(f"مجلد الفئة غير موجود: {category_dir}")
            return {
                'total_images': 0,
                'accepted_images': 0,
                'rejected_images': 0,
                'rejection_reasons': {}
            }
        
        # الحصول على قائمة ملفات الصور
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = [
            os.path.join(category_dir, f) for f in os.listdir(category_dir)
            if os.path.isfile(os.path.join(category_dir, f)) and
            os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        # إحصائيات التنقية
        stats = {
            'total_images': len(image_files),
            'accepted_images': 0,
            'rejected_images': 0,
            'rejection_reasons': {}
        }
        
        # تنقية الصور
        for image_path in image_files:
            # تنقية الصورة
            is_accepted, reason = self.filter_image(image_path)
            
            if is_accepted:
                stats['accepted_images'] += 1
            else:
                stats['rejected_images'] += 1
                
                # إضافة سبب الرفض إلى الإحصائيات
                if reason not in stats['rejection_reasons']:
                    stats['rejection_reasons'][reason] = 0
                stats['rejection_reasons'][reason] += 1
                
                # نقل الصورة إلى مجلد الصور المرفوضة
                self.move_to_rejected(image_path, reason)
        
        logger.info(f"اكتمل تنقية الصور في الفئة {category}: {stats}")
        return stats
    
    def filter_all_categories(self):
        """
        تنقية جميع الصور في جميع الفئات
        
        العوائد:
            dict: إحصائيات التنقية
        """
        logger.info(f"بدء تنقية الصور في جميع الفئات")
        
        # إحصائيات التنقية
        stats = {
            'total_images': 0,
            'accepted_images': 0,
            'rejected_images': 0,
            'rejection_reasons': {},
            'categories': {}
        }
        
        # تنقية كل فئة
        for category in self.config['categories']:
            category_stats = self.filter_category(category)
            
            # تحديث الإحصائيات الإجمالية
            stats['total_images'] += category_stats['total_images']
            stats['accepted_images'] += category_stats['accepted_images']
            stats['rejected_images'] += category_stats['rejected_images']
            
            # تحديث أسباب الرفض
            for reason, count in category_stats['rejection_reasons'].items():
                if reason not in stats['rejection_reasons']:
                    stats['rejection_reasons'][reason] = 0
                stats['rejection_reasons'][reason] += count
            
            # إضافة إحصائيات الفئة
            stats['categories'][category] = category_stats
        
        logger.info(f"اكتمل تنقية الصور في جميع الفئات: {stats}")
        return stats


# نموذج استخدام
if __name__ == "__main__":
    # تكوين المرشح
    config = {
        'input_base_dir': 'data/images',
        'rejected_dir': 'data/images/rejected',
        'blur_threshold': 80,
        'min_contrast': 30,
        'max_threads': 4
    }
    
    # إنشاء كائن المرشح
    image_filter = PlantDiseaseImageFilter(config)
    
    # تنقية جميع الصور
    stats = image_filter.filter_all_categories()
    print(f"إحصائيات التنقية: {stats}")
