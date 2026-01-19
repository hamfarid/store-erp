#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام تحديث قاعدة البيانات تلقائيًا بصور الأمراض النباتية
"""

import os
import sys
import json
import logging
import datetime
import sqlite3
import csv
import shutil
from pathlib import Path
from dotenv import load_dotenv

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlantDiseaseDatabaseUpdater:
    """فئة لتحديث قاعدة البيانات تلقائيًا بصور الأمراض النباتية"""
    
    def __init__(self, config=None):
        """
        تهيئة محدث قاعدة البيانات
        
        المعلمات:
            config (dict): تكوين المحدث
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'images_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'archive_dir': os.getenv('ARCHIVE_DIR', 'data/archives'),
            'database_path': os.getenv('DATABASE_PATH', 'data/database/plant_diseases.db'),
            'metadata_file': os.getenv('IMAGE_METADATA_FILE', 'data/images/metadata.csv'),
            'categories': ['vegetables', 'fruits', 'crops'],
            'backup_database': True,
            'max_batch_size': 1000,
            'integrity_check': True,
            'auto_vacuum': True
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
            
        # إنشاء مجلد قاعدة البيانات إذا لم يكن موجودًا
        os.makedirs(os.path.dirname(self.config['database_path']), exist_ok=True)
        
        # إنشاء قاعدة البيانات إذا لم تكن موجودة
        self._initialize_database()
    
    def _initialize_database(self):
        """إنشاء قاعدة البيانات وجداولها إذا لم تكن موجودة"""
        try:
            # الاتصال بقاعدة البيانات
            conn = sqlite3.connect(self.config['database_path'])
            cursor = conn.cursor()
            
            # إنشاء جدول الفئات
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # إنشاء جدول أنواع النباتات
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS plant_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category_id INTEGER,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
            ''')
            
            # إنشاء جدول أنواع الأمراض
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS disease_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                symptoms TEXT,
                causes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # إنشاء جدول الصور
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                original_name TEXT,
                file_path TEXT,
                archive_path TEXT,
                category_id INTEGER,
                plant_type_id INTEGER,
                disease_type_id INTEGER,
                width INTEGER,
                height INTEGER,
                file_size INTEGER,
                hash TEXT,
                metadata TEXT,
                is_archived INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id),
                FOREIGN KEY (plant_type_id) REFERENCES plant_types (id),
                FOREIGN KEY (disease_type_id) REFERENCES disease_types (id)
            )
            ''')
            
            # إنشاء فهارس للبحث السريع
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_category ON images (category_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_plant_type ON images (plant_type_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_disease_type ON images (disease_type_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_hash ON images (hash)')
            
            # إدخال الفئات الافتراضية
            for category in self.config['categories']:
                cursor.execute(
                    'INSERT OR IGNORE INTO categories (name) VALUES (?)',
                    (category,)
                )
            
            # حفظ التغييرات
            conn.commit()
            
            # إغلاق الاتصال
            conn.close()
            
            logger.info(f"تم تهيئة قاعدة البيانات بنجاح: {self.config['database_path']}")
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تهيئة قاعدة البيانات: {str(e)}")
            raise
    
    def _backup_database(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            # الحصول على مسار النسخة الاحتياطية
            backup_dir = os.path.join(os.path.dirname(self.config['database_path']), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # توليد اسم ملف النسخة الاحتياطية
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f"plant_diseases_{timestamp}.db")
            
            # نسخ ملف قاعدة البيانات
            shutil.copy2(self.config['database_path'], backup_path)
            
            logger.info(f"تم إنشاء نسخة احتياطية من قاعدة البيانات: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء إنشاء نسخة احتياطية من قاعدة البيانات: {str(e)}")
            return None
    
    def _get_category_id(self, conn, category_name):
        """
        الحصول على معرف الفئة
        
        المعلمات:
            conn (sqlite3.Connection): اتصال قاعدة البيانات
            category_name (str): اسم الفئة
            
        العوائد:
            int: معرف الفئة
        """
        cursor = conn.cursor()
        
        # البحث عن الفئة
        cursor.execute(
            'SELECT id FROM categories WHERE name = ?',
            (category_name,)
        )
        
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # إنشاء الفئة إذا لم تكن موجودة
            cursor.execute(
                'INSERT INTO categories (name) VALUES (?)',
                (category_name,)
            )
            conn.commit()
            
            return cursor.lastrowid
    
    def _get_plant_type_id(self, conn, plant_type_name, category_id):
        """
        الحصول على معرف نوع النبات
        
        المعلمات:
            conn (sqlite3.Connection): اتصال قاعدة البيانات
            plant_type_name (str): اسم نوع النبات
            category_id (int): معرف الفئة
            
        العوائد:
            int: معرف نوع النبات
        """
        cursor = conn.cursor()
        
        # البحث عن نوع النبات
        cursor.execute(
            'SELECT id FROM plant_types WHERE name = ?',
            (plant_type_name,)
        )
        
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # إنشاء نوع النبات إذا لم يكن موجودًا
            cursor.execute(
                'INSERT INTO plant_types (name, category_id) VALUES (?, ?)',
                (plant_type_name, category_id)
            )
            conn.commit()
            
            return cursor.lastrowid
    
    def _get_disease_type_id(self, conn, disease_type_name, disease_category):
        """
        الحصول على معرف نوع المرض
        
        المعلمات:
            conn (sqlite3.Connection): اتصال قاعدة البيانات
            disease_type_name (str): اسم نوع المرض
            disease_category (str): فئة المرض
            
        العوائد:
            int: معرف نوع المرض
        """
        cursor = conn.cursor()
        
        # البحث عن نوع المرض
        cursor.execute(
            'SELECT id FROM disease_types WHERE name = ?',
            (disease_type_name,)
        )
        
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # إنشاء نوع المرض إذا لم يكن موجودًا
            cursor.execute(
                'INSERT INTO disease_types (name, category) VALUES (?, ?)',
                (disease_type_name, disease_category)
            )
            conn.commit()
            
            return cursor.lastrowid
    
    def _check_image_exists(self, conn, file_hash):
        """
        التحقق من وجود الصورة في قاعدة البيانات
        
        المعلمات:
            conn (sqlite3.Connection): اتصال قاعدة البيانات
            file_hash (str): هاش الملف
            
        العوائد:
            bool: True إذا كانت الصورة موجودة، False خلاف ذلك
        """
        cursor = conn.cursor()
        
        # البحث عن الصورة
        cursor.execute(
            'SELECT id FROM images WHERE hash = ?',
            (file_hash,)
        )
        
        result = cursor.fetchone()
        
        return result is not None
    
    def _get_image_dimensions(self, image_path):
        """
        الحصول على أبعاد الصورة
        
        المعلمات:
            image_path (str): مسار الصورة
            
        العوائد:
            tuple: (العرض، الارتفاع)
        """
        try:
            from PIL import Image
            
            # فتح الصورة
            with Image.open(image_path) as img:
                return img.size
                
        except Exception as e:
            logger.error(f"حدث خطأ أثناء الحصول على أبعاد الصورة {image_path}: {str(e)}")
            return (0, 0)
    
    def _parse_metadata_from_filename(self, filename):
        """
        استخراج البيانات الوصفية من اسم الملف
        
        المعلمات:
            filename (str): اسم الملف
            
        العوائد:
            dict: البيانات الوصفية
        """
        # نمط اسم الملف: {category}_{disease_type}_{plant_type}_{date}_{hash}
        parts = filename.split('_')
        
        if len(parts) < 5:
            return {
                'disease_type': 'unknown',
                'plant_type': 'unknown',
                'hash': ''
            }
        
        # استخراج هاش الملف
        file_hash = parts[-1].split('.')[0]
        
        # استخراج نوع المرض
        disease_parts = []
        for i in range(1, min(3, len(parts) - 2)):
            disease_parts.append(parts[i])
        
        disease_type = '_'.join(disease_parts)
        
        # استخراج نوع النبات
        plant_type = parts[min(3, len(parts) - 2)]
        
        return {
            'disease_type': disease_type,
            'plant_type': plant_type,
            'hash': file_hash
        }
    
    def _update_database_from_metadata_file(self):
        """تحديث قاعدة البيانات من ملف البيانات الوصفية"""
        try:
            # التحقق من وجود ملف البيانات الوصفية
            if not os.path.exists(self.config['metadata_file']):
                logger.warning(f"ملف البيانات الوصفية غير موجود: {self.config['metadata_file']}")
                return {
                    'total_images': 0,
                    'added_images': 0,
                    'skipped_images': 0,
                    'failed_images': 0
                }
            
            # الاتصال بقاعدة البيانات
            conn = sqlite3.connect(self.config['database_path'])
            
            # إنشاء نسخة احتياطية إذا تم تمكين ذلك
            if self.config['backup_database']:
                self._backup_database()
            
            # قراءة ملف البيانات الوصفية
            with open(self.config['metadata_file'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # إحصائيات التحديث
                stats = {
                    'total_images': 0,
                    'added_images': 0,
                    'skipped_images': 0,
                    'failed_images': 0
                }
                
                # معالجة كل صورة
                batch_count = 0
                for row in reader:
                    stats['total_images'] += 1
                    
                    try:
                        # التحقق من وجود الصورة
                        file_path = row['file_path']
                        file_hash = row['hash']
                        
                        # التحقق من وجود الصورة في قاعدة البيانات
                        if self._check_image_exists(conn, file_hash):
                            stats['skipped_images'] += 1
                            continue
                        
                        # الحصول على معرفات الفئات
                        category_id = self._get_category_id(conn, row['category'])
                        plant_type_id = self._get_plant_type_id(conn, row['plant_type'], category_id)
                        
                        # استخراج فئة المرض ونوع المرض
                        disease_parts = row['disease_type'].split('_')
                        disease_category = disease_parts[0] if len(disease_parts) > 0 else 'unknown'
                        disease_name = '_'.join(disease_parts[1:]) if len(disease_parts) > 1 else disease_parts[0]
                        
                        disease_type_id = self._get_disease_type_id(conn, disease_name, disease_category)
                        
                        # الحصول على أبعاد الصورة
                        width, height = self._get_image_dimensions(file_path) if os.path.exists(file_path) else (0, 0)
                        
                        # الحصول على حجم الملف
                        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                        
                        # إدخال الصورة في قاعدة البيانات
                        cursor = conn.cursor()
                        cursor.execute('''
                        INSERT INTO images (
                            file_name, original_name, file_path, category_id, plant_type_id,
                            disease_type_id, width, height, file_size, hash, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            os.path.basename(file_path),
                            row['original_name'],
                            file_path,
                            category_id,
                            plant_type_id,
                            disease_type_id,
                            width,
                            height,
                            file_size,
                            file_hash,
                            row['date_added']
                        ))
                        
                        stats['added_images'] += 1
                        batch_count += 1
                        
                        # حفظ التغييرات كل حجم دفعة
                        if batch_count >= self.config['max_batch_size']:
                            conn.commit()
                            batch_count = 0
                            
                    except Exception as e:
                        logger.error(f"حدث خطأ أثناء إضافة الصورة {row.get('file_path', 'unknown')}: {str(e)}")
                        stats['failed_images'] += 1
                
                # حفظ التغييرات المتبقية
                conn.commit()
                
                # إجراء فحص سلامة قاعدة البيانات إذا تم تمكين ذلك
                if self.config['integrity_check']:
                    cursor = conn.cursor()
                    cursor.execute('PRAGMA integrity_check')
                    integrity_result = cursor.fetchone()
                    logger.info(f"نتيجة فحص سلامة قاعدة البيانات: {integrity_result[0]}")
                
                # إجراء تفريغ تلقائي لقاعدة البيانات إذا تم تمكين ذلك
                if self.config['auto_vacuum']:
                    cursor = conn.cursor()
                    cursor.execute('VACUUM')
                    logger.info("تم إجراء تفريغ تلقائي لقاعدة البيانات")
                
                # إغلاق الاتصال
                conn.close()
                
                logger.info(f"اكتمل تحديث قاعدة البيانات من ملف البيانات الوصفية: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تحديث قاعدة البيانات من ملف البيانات الوصفية: {str(e)}")
            return {
                'total_images': 0,
                'added_images': 0,
                'skipped_images': 0,
                'failed_images': 0,
                'error': str(e)
            }
    
    def _update_database_from_directory(self, category):
        """
        تحديث قاعدة البيانات من مجلد
        
        المعلمات:
            category (str): اسم الفئة
            
        العوائد:
            dict: إحصائيات التحديث
        """
        try:
            # تحديد مجلد الفئة
            category_dir = os.path.join(self.config['images_dir'], category)
            
            # التحقق من وجود المجلد
            if not os.path.exists(category_dir):
                logger.warning(f"مجلد الفئة غير موجود: {category_dir}")
                return {
                    'total_images': 0,
                    'added_images': 0,
                    'skipped_images': 0,
                    'failed_images': 0
                }
            
            # الاتصال بقاعدة البيانات
            conn = sqlite3.connect(self.config['database_path'])
            
            # الحصول على معرف الفئة
            category_id = self._get_category_id(conn, category)
            
            # الحصول على قائمة ملفات الصور
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            image_files = [
                os.path.join(category_dir, f) for f in os.listdir(category_dir)
                if os.path.isfile(os.path.join(category_dir, f)) and
                os.path.splitext(f)[1].lower() in image_extensions
            ]
            
            # إحصائيات التحديث
            stats = {
                'total_images': len(image_files),
                'added_images': 0,
                'skipped_images': 0,
                'failed_images': 0
            }
            
            # معالجة كل صورة
            batch_count = 0
            for image_path in image_files:
                try:
                    # استخراج اسم الملف
                    filename = os.path.basename(image_path)
                    
                    # استخراج البيانات الوصفية من اسم الملف
                    metadata = self._parse_metadata_from_filename(filename)
                    
                    # التحقق من وجود الصورة في قاعدة البيانات
                    if self._check_image_exists(conn, metadata['hash']):
                        stats['skipped_images'] += 1
                        continue
                    
                    # الحصول على معرفات الفئات
                    plant_type_id = self._get_plant_type_id(conn, metadata['plant_type'], category_id)
                    
                    # استخراج فئة المرض ونوع المرض
                    disease_parts = metadata['disease_type'].split('_')
                    disease_category = disease_parts[0] if len(disease_parts) > 0 else 'unknown'
                    disease_name = '_'.join(disease_parts[1:]) if len(disease_parts) > 1 else disease_parts[0]
                    
                    disease_type_id = self._get_disease_type_id(conn, disease_name, disease_category)
                    
                    # الحصول على أبعاد الصورة
                    width, height = self._get_image_dimensions(image_path)
                    
                    # الحصول على حجم الملف
                    file_size = os.path.getsize(image_path)
                    
                    # إدخال الصورة في قاعدة البيانات
                    cursor = conn.cursor()
                    cursor.execute('''
                    INSERT INTO images (
                        file_name, file_path, category_id, plant_type_id,
                        disease_type_id, width, height, file_size, hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        filename,
                        image_path,
                        category_id,
                        plant_type_id,
                        disease_type_id,
                        width,
                        height,
                        file_size,
                        metadata['hash']
                    ))
                    
                    stats['added_images'] += 1
                    batch_count += 1
                    
                    # حفظ التغييرات كل حجم دفعة
                    if batch_count >= self.config['max_batch_size']:
                        conn.commit()
                        batch_count = 0
                        
                except Exception as e:
                    logger.error(f"حدث خطأ أثناء إضافة الصورة {image_path}: {str(e)}")
                    stats['failed_images'] += 1
            
            # حفظ التغييرات المتبقية
            conn.commit()
            
            # إغلاق الاتصال
            conn.close()
            
            logger.info(f"اكتمل تحديث قاعدة البيانات من مجلد {category}: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تحديث قاعدة البيانات من مجلد {category}: {str(e)}")
            return {
                'total_images': 0,
                'added_images': 0,
                'skipped_images': 0,
                'failed_images': 0,
                'error': str(e)
            }
    
    def _update_database_from_archives(self):
        """
        تحديث قاعدة البيانات من الأرشيفات
        
        العوائد:
            dict: إحصائيات التحديث
        """
        try:
            # التحقق من وجود مجلد الأرشيف
            if not os.path.exists(self.config['archive_dir']):
                logger.warning(f"مجلد الأرشيف غير موجود: {self.config['archive_dir']}")
                return {
                    'total_archives': 0,
                    'processed_archives': 0,
                    'failed_archives': 0,
                    'total_images': 0,
                    'added_images': 0,
                    'skipped_images': 0,
                    'failed_images': 0
                }
            
            # الحصول على قائمة ملفات الأرشيف
            archive_extensions = ['.zip']
            archive_files = [
                os.path.join(self.config['archive_dir'], f) for f in os.listdir(self.config['archive_dir'])
                if os.path.isfile(os.path.join(self.config['archive_dir'], f)) and
                os.path.splitext(f)[1].lower() in archive_extensions
            ]
            
            # إحصائيات التحديث
            stats = {
                'total_archives': len(archive_files),
                'processed_archives': 0,
                'failed_archives': 0,
                'total_images': 0,
                'added_images': 0,
                'skipped_images': 0,
                'failed_images': 0
            }
            
            # الاتصال بقاعدة البيانات
            conn = sqlite3.connect(self.config['database_path'])
            
            # معالجة كل أرشيف
            for archive_path in archive_files:
                try:
                    # استخراج اسم الأرشيف
                    archive_name = os.path.basename(archive_path)
                    
                    logger.info(f"معالجة الأرشيف: {archive_name}")
                    
                    # استخراج البيانات الوصفية من الأرشيف
                    import zipfile
                    
                    with zipfile.ZipFile(archive_path, 'r') as zipf:
                        # البحث عن ملف البيانات الوصفية
                        metadata_file = self.config['archive_metadata_file']
                        
                        if metadata_file in zipf.namelist():
                            # قراءة ملف البيانات الوصفية
                            with zipf.open(metadata_file) as f:
                                metadata = json.load(f)
                                
                                # معالجة كل صورة
                                batch_count = 0
                                for file_path, image_metadata in metadata.items():
                                    stats['total_images'] += 1
                                    
                                    try:
                                        # التحقق من وجود الصورة في قاعدة البيانات
                                        file_hash = image_metadata['hash']
                                        
                                        if self._check_image_exists(conn, file_hash):
                                            stats['skipped_images'] += 1
                                            continue
                                        
                                        # الحصول على معرفات الفئات
                                        category_id = self._get_category_id(conn, image_metadata['category'])
                                        plant_type_id = self._get_plant_type_id(conn, image_metadata['plant_type'], category_id)
                                        
                                        # استخراج فئة المرض ونوع المرض
                                        disease_parts = image_metadata['disease_type'].split('_')
                                        disease_category = disease_parts[0] if len(disease_parts) > 0 else 'unknown'
                                        disease_name = '_'.join(disease_parts[1:]) if len(disease_parts) > 1 else disease_parts[0]
                                        
                                        disease_type_id = self._get_disease_type_id(conn, disease_name, disease_category)
                                        
                                        # استخراج اسم الملف
                                        filename = os.path.basename(file_path)
                                        
                                        # إدخال الصورة في قاعدة البيانات
                                        cursor = conn.cursor()
                                        cursor.execute('''
                                        INSERT INTO images (
                                            file_name, original_name, archive_path, category_id, plant_type_id,
                                            disease_type_id, hash, is_archived, created_at
                                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                        ''', (
                                            filename,
                                            image_metadata['original_name'],
                                            archive_path,
                                            category_id,
                                            plant_type_id,
                                            disease_type_id,
                                            file_hash,
                                            1,
                                            image_metadata['date_added']
                                        ))
                                        
                                        stats['added_images'] += 1
                                        batch_count += 1
                                        
                                        # حفظ التغييرات كل حجم دفعة
                                        if batch_count >= self.config['max_batch_size']:
                                            conn.commit()
                                            batch_count = 0
                                            
                                    except Exception as e:
                                        logger.error(f"حدث خطأ أثناء إضافة الصورة {file_path} من الأرشيف {archive_name}: {str(e)}")
                                        stats['failed_images'] += 1
                                
                                # حفظ التغييرات المتبقية
                                conn.commit()
                        else:
                            logger.warning(f"ملف البيانات الوصفية غير موجود في الأرشيف: {archive_name}")
                    
                    stats['processed_archives'] += 1
                    
                except Exception as e:
                    logger.error(f"حدث خطأ أثناء معالجة الأرشيف {archive_path}: {str(e)}")
                    stats['failed_archives'] += 1
            
            # إغلاق الاتصال
            conn.close()
            
            logger.info(f"اكتمل تحديث قاعدة البيانات من الأرشيفات: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تحديث قاعدة البيانات من الأرشيفات: {str(e)}")
            return {
                'total_archives': 0,
                'processed_archives': 0,
                'failed_archives': 0,
                'total_images': 0,
                'added_images': 0,
                'skipped_images': 0,
                'failed_images': 0,
                'error': str(e)
            }
    
    def update_database(self):
        """
        تحديث قاعدة البيانات من جميع المصادر
        
        العوائد:
            dict: إحصائيات التحديث
        """
        logger.info("بدء تحديث قاعدة البيانات")
        
        # إنشاء نسخة احتياطية إذا تم تمكين ذلك
        if self.config['backup_database']:
            self._backup_database()
        
        # إحصائيات التحديث
        stats = {
            'total_images': 0,
            'added_images': 0,
            'skipped_images': 0,
            'failed_images': 0,
            'sources': {}
        }
        
        # تحديث قاعدة البيانات من ملف البيانات الوصفية
        metadata_stats = self._update_database_from_metadata_file()
        stats['sources']['metadata'] = metadata_stats
        stats['total_images'] += metadata_stats['total_images']
        stats['added_images'] += metadata_stats['added_images']
        stats['skipped_images'] += metadata_stats['skipped_images']
        stats['failed_images'] += metadata_stats['failed_images']
        
        # تحديث قاعدة البيانات من المجلدات
        for category in self.config['categories']:
            category_stats = self._update_database_from_directory(category)
            stats['sources'][category] = category_stats
            stats['total_images'] += category_stats['total_images']
            stats['added_images'] += category_stats['added_images']
            stats['skipped_images'] += category_stats['skipped_images']
            stats['failed_images'] += category_stats['failed_images']
        
        # تحديث قاعدة البيانات من الأرشيفات
        archive_stats = self._update_database_from_archives()
        stats['sources']['archives'] = archive_stats
        stats['total_images'] += archive_stats['total_images']
        stats['added_images'] += archive_stats['added_images']
        stats['skipped_images'] += archive_stats['skipped_images']
        stats['failed_images'] += archive_stats['failed_images']
        
        logger.info(f"اكتمل تحديث قاعدة البيانات: {stats}")
        return stats


# نموذج استخدام
if __name__ == "__main__":
    # تكوين المحدث
    config = {
        'images_dir': 'data/images',
        'archive_dir': 'data/archives',
        'database_path': 'data/database/plant_diseases.db',
        'backup_database': True,
        'integrity_check': True
    }
    
    # إنشاء كائن المحدث
    updater = PlantDiseaseDatabaseUpdater(config)
    
    # تحديث قاعدة البيانات
    stats = updater.update_database()
    print(f"إحصائيات تحديث قاعدة البيانات: {stats}")
