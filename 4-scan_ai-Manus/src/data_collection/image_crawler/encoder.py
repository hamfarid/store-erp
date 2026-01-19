#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام تسمية وترميز صور الأمراض النباتية بشكل آلي
"""

import os
import re
import uuid
import time
import hashlib
import logging
import datetime
from pathlib import Path
from dotenv import load_dotenv

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlantDiseaseImageEncoder:
    """فئة لتسمية وترميز صور الأمراض النباتية بشكل آلي"""
    
    def __init__(self, config=None):
        """
        تهيئة مرمز صور الأمراض النباتية
        
        المعلمات:
            config (dict): تكوين المرمز
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'input_base_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'categories': ['vegetables', 'fruits', 'crops'],
            'naming_pattern': '{category}_{disease_type}_{plant_type}_{date}_{hash}',
            'date_format': '%Y%m%d',
            'hash_length': 8,
            'metadata_file': os.getenv('IMAGE_METADATA_FILE', 'data/images/metadata.csv'),
            'disease_types': {
                'bacterial': ['spot', 'canker', 'wilt', 'rot'],
                'viral': ['mosaic', 'yellowing', 'curl', 'mottling'],
                'fungal': ['mildew', 'rust', 'blight', 'anthracnose', 'scab']
            },
            'plant_types': {
                'vegetables': ['tomato', 'potato', 'pepper', 'cucumber', 'eggplant', 'lettuce', 'cabbage', 'carrot'],
                'fruits': ['apple', 'grape', 'strawberry', 'citrus', 'peach', 'banana', 'mango'],
                'crops': ['wheat', 'corn', 'rice', 'barley', 'soybean', 'cotton']
            }
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
            
        # إنشاء ملف البيانات الوصفية إذا لم يكن موجودًا
        self._initialize_metadata_file()
    
    def _initialize_metadata_file(self):
        """إنشاء ملف البيانات الوصفية إذا لم يكن موجودًا"""
        if not os.path.exists(self.config['metadata_file']):
            # إنشاء المجلد إذا لم يكن موجودًا
            os.makedirs(os.path.dirname(self.config['metadata_file']), exist_ok=True)
            
            # إنشاء ملف البيانات الوصفية مع الرأس
            with open(self.config['metadata_file'], 'w', encoding='utf-8') as f:
                f.write('file_path,original_name,category,disease_type,plant_type,date_added,hash\n')
            
            logger.info(f"تم إنشاء ملف البيانات الوصفية: {self.config['metadata_file']}")
    
    def _detect_disease_type(self, filename):
        """
        اكتشاف نوع المرض من اسم الملف
        
        المعلمات:
            filename (str): اسم الملف
            
        العوائد:
            str: نوع المرض المكتشف أو 'unknown'
        """
        filename_lower = filename.lower()
        
        # البحث عن أنواع الأمراض في اسم الملف
        for disease_category, disease_list in self.config['disease_types'].items():
            for disease in disease_list:
                if disease in filename_lower:
                    return f"{disease_category}_{disease}"
        
        # إذا لم يتم العثور على نوع المرض، استخدم الفئة الرئيسية
        for disease_category in self.config['disease_types'].keys():
            if disease_category in filename_lower:
                return f"{disease_category}_unknown"
        
        return 'unknown'
    
    def _detect_plant_type(self, filename, category):
        """
        اكتشاف نوع النبات من اسم الملف والفئة
        
        المعلمات:
            filename (str): اسم الملف
            category (str): فئة الصورة
            
        العوائد:
            str: نوع النبات المكتشف أو 'unknown'
        """
        filename_lower = filename.lower()
        
        # البحث عن أنواع النباتات في اسم الملف
        if category in self.config['plant_types']:
            for plant in self.config['plant_types'][category]:
                if plant in filename_lower:
                    return plant
        
        # البحث في جميع الفئات إذا لم يتم العثور على نوع النبات
        for plant_category, plant_list in self.config['plant_types'].items():
            for plant in plant_list:
                if plant in filename_lower:
                    return plant
        
        return 'unknown'
    
    def _generate_hash(self, file_path):
        """
        توليد هاش للملف
        
        المعلمات:
            file_path (str): مسار الملف
            
        العوائد:
            str: هاش الملف
        """
        # استخدام اسم الملف والوقت الحالي لتوليد هاش فريد
        unique_string = f"{file_path}_{time.time()}_{uuid.uuid4()}"
        hash_obj = hashlib.md5(unique_string.encode())
        return hash_obj.hexdigest()[:self.config['hash_length']]
    
    def _generate_new_filename(self, original_filename, category, disease_type, plant_type):
        """
        توليد اسم ملف جديد بناءً على نمط التسمية
        
        المعلمات:
            original_filename (str): اسم الملف الأصلي
            category (str): فئة الصورة
            disease_type (str): نوع المرض
            plant_type (str): نوع النبات
            
        العوائد:
            str: اسم الملف الجديد
        """
        # الحصول على امتداد الملف
        _, ext = os.path.splitext(original_filename)
        
        # توليد هاش
        file_hash = self._generate_hash(original_filename)
        
        # الحصول على التاريخ الحالي
        current_date = datetime.datetime.now().strftime(self.config['date_format'])
        
        # توليد اسم الملف الجديد
        new_filename = self.config['naming_pattern'].format(
            category=category,
            disease_type=disease_type,
            plant_type=plant_type,
            date=current_date,
            hash=file_hash
        )
        
        # إضافة امتداد الملف
        new_filename += ext.lower()
        
        # استبدال الأحرف غير الصالحة
        new_filename = re.sub(r'[^\w\-\.]', '_', new_filename)
        
        return new_filename
    
    def _add_metadata_entry(self, file_path, original_name, category, disease_type, plant_type, file_hash):
        """
        إضافة إدخال إلى ملف البيانات الوصفية
        
        المعلمات:
            file_path (str): مسار الملف
            original_name (str): اسم الملف الأصلي
            category (str): فئة الصورة
            disease_type (str): نوع المرض
            plant_type (str): نوع النبات
            file_hash (str): هاش الملف
        """
        # الحصول على التاريخ الحالي
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # إضافة إدخال إلى ملف البيانات الوصفية
        with open(self.config['metadata_file'], 'a', encoding='utf-8') as f:
            f.write(f'{file_path},{original_name},{category},{disease_type},{plant_type},{current_date},{file_hash}\n')
    
    def encode_image(self, image_path):
        """
        تسمية وترميز صورة واحدة
        
        المعلمات:
            image_path (str): مسار ملف الصورة
            
        العوائد:
            str: مسار الملف الجديد
        """
        try:
            # التحقق من وجود الملف
            if not os.path.exists(image_path):
                logger.error(f"الملف غير موجود: {image_path}")
                return None
            
            # استخراج اسم الملف والمجلد
            file_dir = os.path.dirname(image_path)
            filename = os.path.basename(image_path)
            
            # استخراج الفئة من مسار الملف
            path_parts = file_dir.split(os.sep)
            category = path_parts[-1]
            
            # التحقق من أن الفئة صالحة
            if category not in self.config['categories']:
                logger.warning(f"فئة غير صالحة: {category}")
                category = 'unknown'
            
            # اكتشاف نوع المرض ونوع النبات
            disease_type = self._detect_disease_type(filename)
            plant_type = self._detect_plant_type(filename, category)
            
            # توليد اسم ملف جديد
            new_filename = self._generate_new_filename(filename, category, disease_type, plant_type)
            new_path = os.path.join(file_dir, new_filename)
            
            # إعادة تسمية الملف
            os.rename(image_path, new_path)
            
            # استخراج هاش من اسم الملف الجديد
            file_hash = new_filename.split('_')[-1].split('.')[0]
            
            # إضافة إدخال إلى ملف البيانات الوصفية
            self._add_metadata_entry(new_path, filename, category, disease_type, plant_type, file_hash)
            
            logger.info(f"تم ترميز الصورة: {image_path} -> {new_path}")
            return new_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء ترميز الصورة {image_path}: {str(e)}")
            return None
    
    def encode_category(self, category):
        """
        تسمية وترميز جميع الصور في فئة معينة
        
        المعلمات:
            category (str): اسم الفئة
            
        العوائد:
            dict: إحصائيات الترميز
        """
        # تحديد مجلد الفئة
        category_dir = os.path.join(self.config['input_base_dir'], category)
        
        # التحقق من وجود المجلد
        if not os.path.exists(category_dir):
            logger.error(f"مجلد الفئة غير موجود: {category_dir}")
            return {
                'total_images': 0,
                'encoded_images': 0,
                'failed_images': 0
            }
        
        # الحصول على قائمة ملفات الصور
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = [
            os.path.join(category_dir, f) for f in os.listdir(category_dir)
            if os.path.isfile(os.path.join(category_dir, f)) and
            os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        # إحصائيات الترميز
        stats = {
            'total_images': len(image_files),
            'encoded_images': 0,
            'failed_images': 0
        }
        
        # ترميز الصور
        for image_path in image_files:
            # ترميز الصورة
            new_path = self.encode_image(image_path)
            
            if new_path:
                stats['encoded_images'] += 1
            else:
                stats['failed_images'] += 1
        
        logger.info(f"اكتمل ترميز الصور في الفئة {category}: {stats}")
        return stats
    
    def encode_all_categories(self):
        """
        تسمية وترميز جميع الصور في جميع الفئات
        
        العوائد:
            dict: إحصائيات الترميز
        """
        logger.info(f"بدء ترميز الصور في جميع الفئات")
        
        # إحصائيات الترميز
        stats = {
            'total_images': 0,
            'encoded_images': 0,
            'failed_images': 0,
            'categories': {}
        }
        
        # ترميز كل فئة
        for category in self.config['categories']:
            category_stats = self.encode_category(category)
            
            # تحديث الإحصائيات الإجمالية
            stats['total_images'] += category_stats['total_images']
            stats['encoded_images'] += category_stats['encoded_images']
            stats['failed_images'] += category_stats['failed_images']
            
            # إضافة إحصائيات الفئة
            stats['categories'][category] = category_stats
        
        logger.info(f"اكتمل ترميز الصور في جميع الفئات: {stats}")
        return stats


# نموذج استخدام
if __name__ == "__main__":
    # تكوين المرمز
    config = {
        'input_base_dir': 'data/images',
        'naming_pattern': '{category}_{disease_type}_{plant_type}_{date}_{hash}',
        'date_format': '%Y%m%d'
    }
    
    # إنشاء كائن المرمز
    encoder = PlantDiseaseImageEncoder(config)
    
    # ترميز جميع الصور
    stats = encoder.encode_all_categories()
    print(f"إحصائيات الترميز: {stats}")
