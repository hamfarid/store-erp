#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام تخزين وأرشفة صور الأمراض النباتية
"""

import os
import shutil
import logging
import datetime
import zipfile
import json
import csv
from pathlib import Path
from dotenv import load_dotenv

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlantDiseaseImageArchiver:
    """فئة لتخزين وأرشفة صور الأمراض النباتية"""
    
    def __init__(self, config=None):
        """
        تهيئة مؤرشف صور الأمراض النباتية
        
        المعلمات:
            config (dict): تكوين المؤرشف
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'input_base_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'archive_dir': os.getenv('ARCHIVE_DIR', 'data/archives'),
            'categories': ['vegetables', 'fruits', 'crops'],
            'archive_format': 'zip',  # 'zip' أو 'tar'
            'compression_level': 9,  # مستوى الضغط (1-9)
            'archive_naming_pattern': '{category}_images_{date}',
            'date_format': '%Y%m%d_%H%M%S',
            'metadata_file': os.getenv('IMAGE_METADATA_FILE', 'data/images/metadata.csv'),
            'archive_metadata_file': 'metadata.json',
            'backup_original': True,  # نسخ احتياطي للصور الأصلية
            'max_archive_size': 500 * 1024 * 1024,  # الحد الأقصى لحجم الأرشيف (500 ميجابايت)
            'auto_archive_threshold': 1000  # عدد الصور الذي يؤدي إلى الأرشفة التلقائية
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
            
        # إنشاء مجلد الأرشيف إذا لم يكن موجودًا
        os.makedirs(self.config['archive_dir'], exist_ok=True)
    
    def _generate_archive_name(self, category):
        """
        توليد اسم ملف الأرشيف
        
        المعلمات:
            category (str): فئة الصور
            
        العوائد:
            str: اسم ملف الأرشيف
        """
        # الحصول على التاريخ والوقت الحاليين
        current_datetime = datetime.datetime.now().strftime(self.config['date_format'])
        
        # توليد اسم الأرشيف
        archive_name = self.config['archive_naming_pattern'].format(
            category=category,
            date=current_datetime
        )
        
        # إضافة امتداد الملف
        if self.config['archive_format'] == 'zip':
            archive_name += '.zip'
        elif self.config['archive_format'] == 'tar':
            archive_name += '.tar.gz'
        
        return archive_name
    
    def _extract_metadata_from_csv(self, image_paths):
        """
        استخراج البيانات الوصفية من ملف CSV
        
        المعلمات:
            image_paths (list): قائمة بمسارات الصور
            
        العوائد:
            dict: البيانات الوصفية للصور
        """
        metadata = {}
        
        # التحقق من وجود ملف البيانات الوصفية
        if not os.path.exists(self.config['metadata_file']):
            logger.warning(f"ملف البيانات الوصفية غير موجود: {self.config['metadata_file']}")
            return metadata
        
        try:
            # قراءة ملف البيانات الوصفية
            with open(self.config['metadata_file'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # استخراج البيانات الوصفية للصور المحددة
                for row in reader:
                    file_path = row['file_path']
                    
                    # التحقق من أن الصورة في قائمة الصور المطلوبة
                    if file_path in image_paths:
                        metadata[file_path] = {
                            'original_name': row['original_name'],
                            'category': row['category'],
                            'disease_type': row['disease_type'],
                            'plant_type': row['plant_type'],
                            'date_added': row['date_added'],
                            'hash': row['hash']
                        }
            
            return metadata
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء قراءة ملف البيانات الوصفية: {str(e)}")
            return metadata
    
    def _create_zip_archive(self, archive_path, image_paths, metadata):
        """
        إنشاء أرشيف ZIP
        
        المعلمات:
            archive_path (str): مسار ملف الأرشيف
            image_paths (list): قائمة بمسارات الصور
            metadata (dict): البيانات الوصفية للصور
            
        العوائد:
            bool: True إذا نجح إنشاء الأرشيف، False خلاف ذلك
        """
        try:
            # إنشاء أرشيف ZIP
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=self.config['compression_level']) as zipf:
                # إضافة الصور إلى الأرشيف
                for image_path in image_paths:
                    # استخراج اسم الملف
                    filename = os.path.basename(image_path)
                    
                    # إضافة الصورة إلى الأرشيف
                    zipf.write(image_path, filename)
                
                # إضافة ملف البيانات الوصفية إلى الأرشيف
                metadata_json = json.dumps(metadata, indent=4, ensure_ascii=False)
                zipf.writestr(self.config['archive_metadata_file'], metadata_json)
            
            return True
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء إنشاء أرشيف ZIP: {str(e)}")
            return False
    
    def _create_tar_archive(self, archive_path, image_paths, metadata):
        """
        إنشاء أرشيف TAR
        
        المعلمات:
            archive_path (str): مسار ملف الأرشيف
            image_paths (list): قائمة بمسارات الصور
            metadata (dict): البيانات الوصفية للصور
            
        العوائد:
            bool: True إذا نجح إنشاء الأرشيف، False خلاف ذلك
        """
        try:
            import tarfile
            
            # إنشاء أرشيف TAR
            with tarfile.open(archive_path, 'w:gz') as tarf:
                # إضافة الصور إلى الأرشيف
                for image_path in image_paths:
                    # استخراج اسم الملف
                    filename = os.path.basename(image_path)
                    
                    # إضافة الصورة إلى الأرشيف
                    tarf.add(image_path, arcname=filename)
                
                # إضافة ملف البيانات الوصفية إلى الأرشيف
                metadata_json = json.dumps(metadata, indent=4, ensure_ascii=False)
                
                # إنشاء ملف مؤقت للبيانات الوصفية
                temp_metadata_file = os.path.join(os.path.dirname(archive_path), 'temp_metadata.json')
                with open(temp_metadata_file, 'w', encoding='utf-8') as f:
                    f.write(metadata_json)
                
                # إضافة ملف البيانات الوصفية إلى الأرشيف
                tarf.add(temp_metadata_file, arcname=self.config['archive_metadata_file'])
                
                # حذف الملف المؤقت
                os.remove(temp_metadata_file)
            
            return True
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء إنشاء أرشيف TAR: {str(e)}")
            return False
    
    def archive_category(self, category, delete_originals=False):
        """
        أرشفة جميع الصور في فئة معينة
        
        المعلمات:
            category (str): اسم الفئة
            delete_originals (bool): حذف الصور الأصلية بعد الأرشفة
            
        العوائد:
            tuple: (مسار الأرشيف، إحصائيات الأرشفة)
        """
        # تحديد مجلد الفئة
        category_dir = os.path.join(self.config['input_base_dir'], category)
        
        # التحقق من وجود المجلد
        if not os.path.exists(category_dir):
            logger.error(f"مجلد الفئة غير موجود: {category_dir}")
            return None, {
                'total_images': 0,
                'archived_images': 0,
                'failed_images': 0,
                'archive_size': 0
            }
        
        # الحصول على قائمة ملفات الصور
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = [
            os.path.join(category_dir, f) for f in os.listdir(category_dir)
            if os.path.isfile(os.path.join(category_dir, f)) and
            os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        # التحقق من وجود صور
        if not image_files:
            logger.warning(f"لا توجد صور في الفئة: {category}")
            return None, {
                'total_images': 0,
                'archived_images': 0,
                'failed_images': 0,
                'archive_size': 0
            }
        
        # استخراج البيانات الوصفية
        metadata = self._extract_metadata_from_csv(image_files)
        
        # توليد اسم الأرشيف
        archive_name = self._generate_archive_name(category)
        archive_path = os.path.join(self.config['archive_dir'], archive_name)
        
        # إنشاء الأرشيف
        success = False
        if self.config['archive_format'] == 'zip':
            success = self._create_zip_archive(archive_path, image_files, metadata)
        elif self.config['archive_format'] == 'tar':
            success = self._create_tar_archive(archive_path, image_files, metadata)
        
        # إحصائيات الأرشفة
        stats = {
            'total_images': len(image_files),
            'archived_images': len(image_files) if success else 0,
            'failed_images': 0 if success else len(image_files),
            'archive_size': os.path.getsize(archive_path) if success and os.path.exists(archive_path) else 0
        }
        
        # حذف الصور الأصلية إذا تم طلب ذلك
        if success and delete_originals:
            for image_path in image_files:
                try:
                    os.remove(image_path)
                except Exception as e:
                    logger.error(f"حدث خطأ أثناء حذف الصورة الأصلية {image_path}: {str(e)}")
                    stats['failed_images'] += 1
        
        logger.info(f"اكتمل أرشفة الصور في الفئة {category}: {stats}")
        return archive_path if success else None, stats
    
    def archive_all_categories(self, delete_originals=False):
        """
        أرشفة جميع الصور في جميع الفئات
        
        المعلمات:
            delete_originals (bool): حذف الصور الأصلية بعد الأرشفة
            
        العوائد:
            dict: إحصائيات الأرشفة
        """
        logger.info(f"بدء أرشفة الصور في جميع الفئات")
        
        # إحصائيات الأرشفة
        stats = {
            'total_images': 0,
            'archived_images': 0,
            'failed_images': 0,
            'total_archives': 0,
            'total_archive_size': 0,
            'categories': {}
        }
        
        # أرشفة كل فئة
        for category in self.config['categories']:
            archive_path, category_stats = self.archive_category(category, delete_originals)
            
            # تحديث الإحصائيات الإجمالية
            stats['total_images'] += category_stats['total_images']
            stats['archived_images'] += category_stats['archived_images']
            stats['failed_images'] += category_stats['failed_images']
            
            if archive_path:
                stats['total_archives'] += 1
                stats['total_archive_size'] += category_stats['archive_size']
            
            # إضافة إحصائيات الفئة
            stats['categories'][category] = category_stats
        
        logger.info(f"اكتمل أرشفة الصور في جميع الفئات: {stats}")
        return stats
    
    def check_auto_archive_threshold(self):
        """
        التحقق من عتبة الأرشفة التلقائية
        
        العوائد:
            dict: قائمة بالفئات التي تجاوزت العتبة
        """
        categories_to_archive = {}
        
        # التحقق من كل فئة
        for category in self.config['categories']:
            category_dir = os.path.join(self.config['input_base_dir'], category)
            
            # التحقق من وجود المجلد
            if not os.path.exists(category_dir):
                continue
            
            # الحصول على قائمة ملفات الصور
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            image_files = [
                f for f in os.listdir(category_dir)
                if os.path.isfile(os.path.join(category_dir, f)) and
                os.path.splitext(f)[1].lower() in image_extensions
            ]
            
            # التحقق من تجاوز العتبة
            if len(image_files) >= self.config['auto_archive_threshold']:
                categories_to_archive[category] = len(image_files)
        
        return categories_to_archive
    
    def auto_archive(self):
        """
        أرشفة تلقائية للفئات التي تجاوزت العتبة
        
        العوائد:
            dict: إحصائيات الأرشفة
        """
        # التحقق من الفئات التي تجاوزت العتبة
        categories_to_archive = self.check_auto_archive_threshold()
        
        if not categories_to_archive:
            logger.info("لا توجد فئات تجاوزت عتبة الأرشفة التلقائية")
            return {
                'total_images': 0,
                'archived_images': 0,
                'failed_images': 0,
                'total_archives': 0,
                'total_archive_size': 0,
                'categories': {}
            }
        
        logger.info(f"بدء الأرشفة التلقائية للفئات: {categories_to_archive}")
        
        # إحصائيات الأرشفة
        stats = {
            'total_images': 0,
            'archived_images': 0,
            'failed_images': 0,
            'total_archives': 0,
            'total_archive_size': 0,
            'categories': {}
        }
        
        # أرشفة كل فئة
        for category in categories_to_archive.keys():
            archive_path, category_stats = self.archive_category(category, True)
            
            # تحديث الإحصائيات الإجمالية
            stats['total_images'] += category_stats['total_images']
            stats['archived_images'] += category_stats['archived_images']
            stats['failed_images'] += category_stats['failed_images']
            
            if archive_path:
                stats['total_archives'] += 1
                stats['total_archive_size'] += category_stats['archive_size']
            
            # إضافة إحصائيات الفئة
            stats['categories'][category] = category_stats
        
        logger.info(f"اكتمل الأرشفة التلقائية: {stats}")
        return stats


# نموذج استخدام
if __name__ == "__main__":
    # تكوين المؤرشف
    config = {
        'input_base_dir': 'data/images',
        'archive_dir': 'data/archives',
        'archive_format': 'zip',
        'compression_level': 9,
        'auto_archive_threshold': 1000
    }
    
    # إنشاء كائن المؤرشف
    archiver = PlantDiseaseImageArchiver(config)
    
    # أرشفة تلقائية
    stats = archiver.auto_archive()
    print(f"إحصائيات الأرشفة التلقائية: {stats}")
