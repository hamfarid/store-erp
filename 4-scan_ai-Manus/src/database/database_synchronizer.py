#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام مزامنة قواعد البيانات والنسخ الاحتياطي
يوفر آليات لمزامنة البيانات بين قواعد البيانات المختلفة وإدارة النسخ الاحتياطية
"""

import os
import sqlite3
import json
import datetime
import shutil
import logging
import time
import threading
import schedule
from pathlib import Path
import yaml
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class DatabaseSynchronizer:
    """مزامن قواعد البيانات ومدير النسخ الاحتياطية"""
    
    def __init__(self, db_manager, config_path=None):
        """تهيئة مزامن قواعد البيانات"""
        self.logger = logging.getLogger(__name__)
        self.db_manager = db_manager
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'sync.yaml')
        self.config = self._load_config()
        self.sync_lock = threading.Lock()
        self.backup_lock = threading.Lock()
        self.scheduler_thread = None
        self.is_running = False
        
    def _load_config(self):
        """تحميل ملف التكوين الخاص بالمزامنة"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"خطأ في تحميل ملف التكوين: {e}")
            # إعداد تكوين افتراضي
            return {
                'sync': {
                    'enabled': True,
                    'interval': {
                        'operational_to_backup': 'daily',
                        'system_training_to_operational': 'hourly',
                        'employee_training_to_operational': 'daily'
                    },
                    'tables': {
                        'all': True,
                        'exclude': ['audit_logs', 'learning_sessions', 'learning_results']
                    }
                },
                'backup': {
                    'enabled': True,
                    'schedule': 'daily',
                    'time': '00:00',
                    'retention_days': 30,
                    'compress': True,
                    'backup_dir': os.path.join(os.path.dirname(__file__), 'backup', 'history')
                },
                'notifications': {
                    'enabled': True,
                    'on_sync_success': True,
                    'on_sync_failure': True,
                    'on_backup_success': True,
                    'on_backup_failure': True
                }
            }
    
    def start_scheduler(self):
        """بدء جدولة المزامنة والنسخ الاحتياطي"""
        if self.is_running:
            self.logger.warning("المجدول قيد التشغيل بالفعل")
            return
        
        self.is_running = True
        
        # جدولة المزامنة
        if self.config['sync']['enabled']:
            # مزامنة من التشغيلية إلى النسخ الاحتياطي
            if self.config['sync']['interval']['operational_to_backup'] == 'hourly':
                schedule.every().hour.do(self.sync_databases, 'operational', 'backup')
            elif self.config['sync']['interval']['operational_to_backup'] == 'daily':
                schedule.every().day.at("22:00").do(self.sync_databases, 'operational', 'backup')
            elif self.config['sync']['interval']['operational_to_backup'] == 'weekly':
                schedule.every().week.do(self.sync_databases, 'operational', 'backup')
            
            # مزامنة من تدريب النظام إلى التشغيلية
            if self.config['sync']['interval']['system_training_to_operational'] == 'hourly':
                schedule.every().hour.do(self.sync_databases, 'system_training', 'operational')
            elif self.config['sync']['interval']['system_training_to_operational'] == 'daily':
                schedule.every().day.at("02:00").do(self.sync_databases, 'system_training', 'operational')
            
            # مزامنة من تدريب الموظفين إلى التشغيلية
            if self.config['sync']['interval']['employee_training_to_operational'] == 'hourly':
                schedule.every().hour.do(self.sync_databases, 'employee_training', 'operational')
            elif self.config['sync']['interval']['employee_training_to_operational'] == 'daily':
                schedule.every().day.at("03:00").do(self.sync_databases, 'employee_training', 'operational')
        
        # جدولة النسخ الاحتياطي
        if self.config['backup']['enabled']:
            backup_time = self.config['backup']['time']
            if self.config['backup']['schedule'] == 'daily':
                schedule.every().day.at(backup_time).do(self.create_full_backup)
            elif self.config['backup']['schedule'] == 'weekly':
                schedule.every().week.at(backup_time).do(self.create_full_backup)
            elif self.config['backup']['schedule'] == 'monthly':
                schedule.every(30).days.at(backup_time).do(self.create_full_backup)
        
        # جدولة تنظيف النسخ الاحتياطية القديمة
        schedule.every().week.do(self.cleanup_old_backups)
        
        # بدء خيط المجدول
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info("تم بدء جدولة المزامنة والنسخ الاحتياطي")
    
    def _run_scheduler(self):
        """تشغيل المجدول في خيط منفصل"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # التحقق كل دقيقة
    
    def stop_scheduler(self):
        """إيقاف جدولة المزامنة والنسخ الاحتياطي"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
            self.scheduler_thread = None
        
        self.logger.info("تم إيقاف جدولة المزامنة والنسخ الاحتياطي")
    
    def sync_databases(self, source_db, target_db):
        """مزامنة البيانات من قاعدة بيانات المصدر إلى قاعدة بيانات الهدف"""
        with self.sync_lock:
            try:
                self.logger.info(f"بدء مزامنة البيانات من {source_db} إلى {target_db}")
                
                # الحصول على اتصالات قواعد البيانات
                source_conn = self.db_manager.get_connection(source_db)
                target_conn = self.db_manager.get_connection(target_db)
                
                # الحصول على قائمة الجداول في قاعدة بيانات المصدر
                source_cursor = source_conn.cursor()
                source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = [row[0] for row in source_cursor.fetchall()]
                
                # استبعاد الجداول المحددة في التكوين
                if not self.config['sync']['tables']['all']:
                    # إذا كانت قائمة الجداول محددة، استخدم فقط الجداول المحددة
                    tables = [table for table in tables if table in self.config['sync']['tables']['include']]
                else:
                    # استبعاد الجداول المحددة في قائمة الاستبعاد
                    tables = [table for table in tables if table not in self.config['sync']['tables']['exclude']]
                
                # مزامنة كل جدول
                for table in tables:
                    self._sync_table(source_conn, target_conn, table)
                
                self.logger.info(f"تمت مزامنة البيانات من {source_db} إلى {target_db} بنجاح")
                
                # إرسال إشعار بنجاح المزامنة
                if self.config['notifications']['enabled'] and self.config['notifications']['on_sync_success']:
                    self._send_notification(f"تمت مزامنة البيانات من {source_db} إلى {target_db} بنجاح")
                
                return True
            except Exception as e:
                self.logger.error(f"خطأ في مزامنة البيانات من {source_db} إلى {target_db}: {e}")
                
                # إرسال إشعار بفشل المزامنة
                if self.config['notifications']['enabled'] and self.config['notifications']['on_sync_failure']:
                    self._send_notification(f"فشل في مزامنة البيانات من {source_db} إلى {target_db}: {e}")
                
                return False
    
    def _sync_table(self, source_conn, target_conn, table):
        """مزامنة جدول محدد من قاعدة بيانات المصدر إلى قاعدة بيانات الهدف"""
        try:
            self.logger.info(f"مزامنة جدول {table}")
            
            # الحصول على هيكل الجدول
            source_cursor = source_conn.cursor()
            source_cursor.execute(f"PRAGMA table_info({table})")
            columns_info = source_cursor.fetchall()
            
            # التحقق من وجود الجدول في قاعدة بيانات الهدف
            target_cursor = target_conn.cursor()
            target_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            table_exists = target_cursor.fetchone() is not None
            
            if not table_exists:
                # إنشاء الجدول في قاعدة بيانات الهدف
                source_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'")
                create_table_sql = source_cursor.fetchone()[0]
                target_cursor.execute(create_table_sql)
                target_conn.commit()
            
            # الحصول على أسماء الأعمدة
            columns = [column[1] for column in columns_info]
            columns_str = ', '.join(columns)
            
            # الحصول على البيانات من جدول المصدر
            source_cursor.execute(f"SELECT {columns_str} FROM {table}")
            rows = source_cursor.fetchall()
            
            if not rows:
                self.logger.info(f"لا توجد بيانات للمزامنة في جدول {table}")
                return
            
            # حذف البيانات الموجودة في جدول الهدف (اختياري، يمكن تعديله حسب الحاجة)
            # target_cursor.execute(f"DELETE FROM {table}")
            
            # إدراج البيانات في جدول الهدف
            placeholders = ', '.join(['?'] * len(columns))
            insert_sql = f"INSERT OR REPLACE INTO {table} ({columns_str}) VALUES ({placeholders})"
            
            target_conn.executemany(insert_sql, rows)
            target_conn.commit()
            
            self.logger.info(f"تمت مزامنة {len(rows)} صف في جدول {table}")
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة جدول {table}: {e}")
            raise
    
    def create_full_backup(self):
        """إنشاء نسخة احتياطية كاملة لجميع قواعد البيانات"""
        with self.backup_lock:
            try:
                self.logger.info("بدء إنشاء نسخة احتياطية كاملة")
                
                # إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجودًا
                backup_dir = self.config['backup']['backup_dir']
                os.makedirs(backup_dir, exist_ok=True)
                
                # إنشاء مجلد فرعي للنسخة الاحتياطية الحالية
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_subdir = os.path.join(backup_dir, f"backup_{timestamp}")
                os.makedirs(backup_subdir, exist_ok=True)
                
                # إنشاء نسخة احتياطية لكل قاعدة بيانات
                backup_paths = {}
                for db_name in self.db_manager.db_connections.keys():
                    backup_path = self._backup_database(db_name, backup_subdir)
                    backup_paths[db_name] = backup_path
                
                # إنشاء ملف وصفي للنسخة الاحتياطية
                metadata = {
                    'timestamp': timestamp,
                    'databases': backup_paths,
                    'created_by': os.environ.get('USER', 'system'),
                    'version': '1.0'
                }
                
                metadata_path = os.path.join(backup_subdir, 'metadata.json')
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=4)
                
                # ضغط مجلد النسخة الاحتياطية إذا كان مطلوبًا
                if self.config['backup']['compress']:
                    self._compress_backup(backup_subdir)
                
                self.logger.info(f"تم إنشاء نسخة احتياطية كاملة في {backup_subdir}")
                
                # إرسال إشعار بنجاح النسخ الاحتياطي
                if self.config['notifications']['enabled'] and self.config['notifications']['on_backup_success']:
                    self._send_notification(f"تم إنشاء نسخة احتياطية كاملة في {backup_subdir}")
                
                return backup_subdir
            except Exception as e:
                self.logger.error(f"خطأ في إنشاء نسخة احتياطية كاملة: {e}")
                
                # إرسال إشعار بفشل النسخ الاحتياطي
                if self.config['notifications']['enabled'] and self.config['notifications']['on_backup_failure']:
                    self._send_notification(f"فشل في إنشاء نسخة احتياطية كاملة: {e}")
                
                return None
    
    def _backup_database(self, db_name, backup_dir):
        """إنشاء نسخة احتياطية من قاعدة بيانات محددة"""
        try:
            self.logger.info(f"إنشاء نسخة احتياطية من قاعدة بيانات {db_name}")
            
            # الحصول على مسار قاعدة البيانات
            db_path = self.db_manager.config['databases'][db_name]['path']
            
            # إنشاء مسار النسخة الاحتياطية
            backup_path = os.path.join(backup_dir, f"{db_name}.db")
            
            # إغلاق الاتصال مؤقتًا
            conn = self.db_manager.db_connections[db_name]
            conn.close()
            
            # نسخ ملف قاعدة البيانات
            shutil.copy2(db_path, backup_path)
            
            # إعادة فتح الاتصال
            self.db_manager.db_connections[db_name] = sqlite3.connect(db_path)
            
            self.logger.info(f"تم إنشاء نسخة احتياطية من قاعدة بيانات {db_name} في {backup_path}")
            
            return backup_path
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء نسخة احتياطية من قاعدة بيانات {db_name}: {e}")
            
            # إعادة فتح الاتصال في حالة الخطأ
            if db_name not in self.db_manager.db_connections or self.db_manager.db_connections[db_name] is None:
                self.db_manager.db_connections[db_name] = sqlite3.connect(db_path)
            
            raise
    
    def _compress_backup(self, backup_dir):
        """ضغط مجلد النسخة الاحتياطية"""
        try:
            self.logger.info(f"ضغط مجلد النسخة الاحتياطية {backup_dir}")
            
            # إنشاء ملف الضغط
            shutil.make_archive(backup_dir, 'zip', backup_dir)
            
            # حذف المجلد الأصلي بعد الضغط
            shutil.rmtree(backup_dir)
            
            self.logger.info(f"تم ضغط مجلد النسخة الاحتياطية إلى {backup_dir}.zip")
            
            return f"{backup_dir}.zip"
        except Exception as e:
            self.logger.error(f"خطأ في ضغط مجلد النسخة الاحتياطية: {e}")
            raise
    
    def restore_backup(self, backup_path):
        """استعادة النسخة الاحتياطية"""
        with self.backup_lock:
            try:
                self.logger.info(f"بدء استعادة النسخة الاحتياطية من {backup_path}")
                
                # التحقق من وجود ملف الضغط
                if backup_path.endswith('.zip'):
                    # فك ضغط الملف
                    backup_dir = backup_path[:-4]  # إزالة امتداد .zip
                    shutil.unpack_archive(backup_path, backup_dir, 'zip')
                else:
                    backup_dir = backup_path
                
                # التحقق من وجود ملف البيانات الوصفية
                metadata_path = os.path.join(backup_dir, 'metadata.json')
                if not os.path.exists(metadata_path):
                    raise ValueError(f"ملف البيانات الوصفية غير موجود في {backup_dir}")
                
                # قراءة ملف البيانات الوصفية
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # استعادة كل قاعدة بيانات
                for db_name, db_backup_path in metadata['databases'].items():
                    self._restore_database(db_name, os.path.join(backup_dir, os.path.basename(db_backup_path)))
                
                self.logger.info(f"تمت استعادة النسخة الاحتياطية من {backup_path} بنجاح")
                
                # إرسال إشعار بنجاح الاستعادة
                if self.config['notifications']['enabled']:
                    self._send_notification(f"تمت استعادة النسخة الاحتياطية من {backup_path} بنجاح")
                
                # تنظيف المجلد المؤقت إذا كان ملف ضغط
                if backup_path.endswith('.zip') and os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                
                return True
            except Exception as e:
                self.logger.error(f"خطأ في استعادة النسخة الاحتياطية: {e}")
                
                # إرسال إشعار بفشل الاستعادة
                if self.config['notifications']['enabled']:
                    self._send_notification(f"فشل في استعادة النسخة الاحتياطية: {e}")
                
                return False
    
    def _restore_database(self, db_name, backup_path):
        """استعادة قاعدة بيانات محددة من نسخة احتياطية"""
        try:
            self.logger.info(f"استعادة قاعدة بيانات {db_name} من {backup_path}")
            
            # التحقق من وجود ملف النسخة الاحتياطية
            if not os.path.exists(backup_path):
                raise ValueError(f"ملف النسخة الاحتياطية {backup_path} غير موجود")
            
            # الحصول على مسار قاعدة البيانات
            db_path = self.db_manager.config['databases'][db_name]['path']
            
            # إغلاق الاتصال مؤقتًا
            conn = self.db_manager.db_connections[db_name]
            conn.close()
            
            # نسخ ملف النسخة الاحتياطية إلى قاعدة البيانات
            shutil.copy2(backup_path, db_path)
            
            # إعادة فتح الاتصال
            self.db_manager.db_connections[db_name] = sqlite3.connect(db_path)
            
            self.logger.info(f"تمت استعادة قاعدة بيانات {db_name} من {backup_path}")
        except Exception as e:
            self.logger.error(f"خطأ في استعادة قاعدة بيانات {db_name}: {e}")
            
            # إعادة فتح الاتصال في حالة الخطأ
            if db_name not in self.db_manager.db_connections or self.db_manager.db_connections[db_name] is None:
                self.db_manager.db_connections[db_name] = sqlite3.connect(db_path)
            
            raise
    
    def cleanup_old_backups(self):
        """تنظيف النسخ الاحتياطية القديمة"""
        try:
            self.logger.info("بدء تنظيف النسخ الاحتياطية القديمة")
            
            backup_dir = self.config['backup']['backup_dir']
            retention_days = self.config['backup']['retention_days']
            
            if not os.path.exists(backup_dir):
                self.logger.warning(f"مجلد النسخ الاحتياطية {backup_dir} غير موجود")
                return
            
            # حساب تاريخ القطع
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
            
            # الحصول على قائمة النسخ الاحتياطية
            backup_items = []
            for item in os.listdir(backup_dir):
                item_path = os.path.join(backup_dir, item)
                
                # تخطي الملفات غير ذات الصلة
                if not (item.startswith('backup_') or item.endswith('.zip')):
                    continue
                
                # الحصول على تاريخ إنشاء العنصر
                try:
                    if item.startswith('backup_'):
                        # استخراج الطابع الزمني من اسم المجلد
                        timestamp_str = item.replace('backup_', '')
                        timestamp = datetime.datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    else:
                        # استخدام تاريخ إنشاء الملف
                        timestamp = datetime.datetime.fromtimestamp(os.path.getctime(item_path))
                    
                    backup_items.append((item_path, timestamp))
                except Exception as e:
                    self.logger.warning(f"تعذر تحديد تاريخ إنشاء {item_path}: {e}")
                    continue
            
            # فرز العناصر حسب التاريخ (الأقدم أولاً)
            backup_items.sort(key=lambda x: x[1])
            
            # حذف النسخ الاحتياطية القديمة
            deleted_count = 0
            for item_path, timestamp in backup_items:
                if timestamp < cutoff_date:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    
                    self.logger.info(f"تم حذف النسخة الاحتياطية القديمة: {item_path}")
                    deleted_count += 1
            
            self.logger.info(f"تم حذف {deleted_count} نسخة احتياطية قديمة")
        except Exception as e:
            self.logger.error(f"خطأ في تنظيف النسخ الاحتياطية القديمة: {e}")
    
    def _send_notification(self, message):
        """إرسال إشعار"""
        # يمكن تنفيذ آلية الإشعارات حسب احتياجات النظام
        # مثال: إرسال بريد إلكتروني، إشعار في النظام، إلخ.
        self.logger.info(f"إشعار: {message}")
        
        # هنا يمكن إضافة رمز لإرسال الإشعارات عبر وسائل مختلفة
        # مثال: إرسال بريد إلكتروني
        # self._send_email(message)
        
        # مثال: إرسال إشعار في النظام
        # self._send_system_notification(message)
        
        pass


# مثال على الاستخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # استيراد مدير قواعد البيانات
    from database_manager import DatabaseManager
    
    # إنشاء مدير قواعد البيانات
    db_manager = DatabaseManager()
    
    # إنشاء مزامن قواعد البيانات
    db_sync = DatabaseSynchronizer(db_manager)
    
    # مزامنة قواعد البيانات
    db_sync.sync_databases('operational', 'backup')
    
    # إنشاء نسخة احتياطية كاملة
    backup_path = db_sync.create_full_backup()
    print(f"تم إنشاء نسخة احتياطية كاملة في: {backup_path}")
    
    # بدء جدولة المزامنة والنسخ الاحتياطي
    db_sync.start_scheduler()
    
    # الانتظار لفترة للسماح بتنفيذ المهام المجدولة
    try:
        print("جاري تشغيل المجدول. اضغط Ctrl+C للخروج.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("إيقاف المجدول...")
        db_sync.stop_scheduler()
        print("تم إيقاف المجدول.")
