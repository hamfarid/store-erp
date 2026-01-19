#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
قاعدة البيانات الرئيسية للنظام الزراعي
تدير هيكل قواعد البيانات الأربعة وتوفر واجهة موحدة للتعامل معها
"""

import os
import sqlite3
import json
import datetime
import shutil
import logging
from pathlib import Path
import yaml
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class DatabaseManager:
    """مدير قواعد البيانات الرئيسي للنظام الزراعي"""
    
    def __init__(self, config_path=None):
        """تهيئة مدير قواعد البيانات"""
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'database.yaml')
        self.config = self._load_config()
        self.db_connections = {}
        self.initialize_databases()
        
    def _load_config(self):
        """تحميل ملف التكوين الخاص بقواعد البيانات"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"خطأ في تحميل ملف التكوين: {e}")
            # إعداد تكوين افتراضي
            return {
                'databases': {
                    'operational': {
                        'path': os.path.join(os.path.dirname(__file__), 'operational', 'operational.db'),
                        'description': 'قاعدة البيانات التشغيلية الرئيسية',
                        'tables': self._get_default_tables()
                    },
                    'employee_training': {
                        'path': os.path.join(os.path.dirname(__file__), 'employee_training', 'employee_training.db'),
                        'description': 'قاعدة بيانات تدريب الموظفين',
                        'tables': self._get_default_tables()
                    },
                    'system_training': {
                        'path': os.path.join(os.path.dirname(__file__), 'system_training', 'system_training.db'),
                        'description': 'قاعدة بيانات تدريب النظام',
                        'tables': self._get_default_tables()
                    },
                    'backup': {
                        'path': os.path.join(os.path.dirname(__file__), 'backup', 'backup.db'),
                        'description': 'قاعدة بيانات النسخ الاحتياطي',
                        'tables': self._get_default_tables()
                    }
                },
                'backup': {
                    'schedule': 'daily',
                    'retention_days': 30,
                    'backup_dir': os.path.join(os.path.dirname(__file__), 'backup', 'history')
                }
            }
    
    def _get_default_tables(self):
        """الحصول على تعريف الجداول الافتراضية"""
        return {
            'users': '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE,
                    role TEXT NOT NULL,
                    country TEXT,
                    company TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active INTEGER DEFAULT 1
                )
            ''',
            'roles': '''
                CREATE TABLE IF NOT EXISTS roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    permissions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'countries': '''
                CREATE TABLE IF NOT EXISTS countries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    is_active INTEGER DEFAULT 1
                )
            ''',
            'companies': '''
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    country_id INTEGER,
                    description TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (country_id) REFERENCES countries (id)
                )
            ''',
            'plants': '''
                CREATE TABLE IF NOT EXISTS plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    scientific_name TEXT,
                    category TEXT,
                    description TEXT,
                    growing_conditions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'diseases': '''
                CREATE TABLE IF NOT EXISTS diseases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    scientific_name TEXT,
                    description TEXT,
                    symptoms TEXT,
                    causes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'treatments': '''
                CREATE TABLE IF NOT EXISTS treatments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    dosage TEXT,
                    application_method TEXT,
                    precautions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'disease_treatments': '''
                CREATE TABLE IF NOT EXISTS disease_treatments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disease_id INTEGER,
                    treatment_id INTEGER,
                    effectiveness REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (disease_id) REFERENCES diseases (id),
                    FOREIGN KEY (treatment_id) REFERENCES treatments (id)
                )
            ''',
            'varieties': '''
                CREATE TABLE IF NOT EXISTS varieties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plant_id INTEGER,
                    name TEXT NOT NULL,
                    description TEXT,
                    characteristics TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (plant_id) REFERENCES plants (id)
                )
            ''',
            'variety_comparisons': '''
                CREATE TABLE IF NOT EXISTS variety_comparisons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    variety_id INTEGER,
                    reference_variety_id INTEGER,
                    location TEXT,
                    planted_area REAL,
                    planting_date TIMESTAMP,
                    fruit_color TEXT,
                    fruit_size TEXT,
                    fruit_shape TEXT,
                    resistance TEXT,
                    tolerance TEXT,
                    productivity REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (variety_id) REFERENCES varieties (id),
                    FOREIGN KEY (reference_variety_id) REFERENCES varieties (id)
                )
            ''',
            'farms': '''
                CREATE TABLE IF NOT EXISTS farms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT,
                    area REAL,
                    owner TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'farm_plots': '''
                CREATE TABLE IF NOT EXISTS farm_plots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    farm_id INTEGER,
                    name TEXT NOT NULL,
                    area REAL,
                    plant_id INTEGER,
                    variety_id INTEGER,
                    planting_date TIMESTAMP,
                    plants_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (farm_id) REFERENCES farms (id),
                    FOREIGN KEY (plant_id) REFERENCES plants (id),
                    FOREIGN KEY (variety_id) REFERENCES varieties (id)
                )
            ''',
            'harvests': '''
                CREATE TABLE IF NOT EXISTS harvests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plot_id INTEGER,
                    harvest_date TIMESTAMP,
                    quantity REAL,
                    quality TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (plot_id) REFERENCES farm_plots (id)
                )
            ''',
            'irrigation_schedules': '''
                CREATE TABLE IF NOT EXISTS irrigation_schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plot_id INTEGER,
                    schedule_date TIMESTAMP,
                    duration INTEGER,
                    water_amount REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (plot_id) REFERENCES farm_plots (id)
                )
            ''',
            'fertilization_schedules': '''
                CREATE TABLE IF NOT EXISTS fertilization_schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plot_id INTEGER,
                    schedule_date TIMESTAMP,
                    fertilizer_id INTEGER,
                    amount REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (plot_id) REFERENCES farm_plots (id),
                    FOREIGN KEY (fertilizer_id) REFERENCES inventory_items (id)
                )
            ''',
            'inventory_items': '''
                CREATE TABLE IF NOT EXISTS inventory_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    description TEXT,
                    unit TEXT,
                    quantity REAL,
                    unit_cost REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'inventory_transactions': '''
                CREATE TABLE IF NOT EXISTS inventory_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER,
                    transaction_type TEXT,
                    quantity REAL,
                    transaction_date TIMESTAMP,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES inventory_items (id)
                )
            ''',
            'costs': '''
                CREATE TABLE IF NOT EXISTS costs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plot_id INTEGER,
                    cost_type TEXT,
                    amount REAL,
                    date TIMESTAMP,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (plot_id) REFERENCES farm_plots (id)
                )
            ''',
            'nurseries': '''
                CREATE TABLE IF NOT EXISTS nurseries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT,
                    capacity INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'seedlings': '''
                CREATE TABLE IF NOT EXISTS seedlings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nursery_id INTEGER,
                    plant_id INTEGER,
                    variety_id INTEGER,
                    quantity INTEGER,
                    seeding_date TIMESTAMP,
                    expected_ready_date TIMESTAMP,
                    season TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (nursery_id) REFERENCES nurseries (id),
                    FOREIGN KEY (plant_id) REFERENCES plants (id),
                    FOREIGN KEY (variety_id) REFERENCES varieties (id)
                )
            ''',
            'seedling_reservations': '''
                CREATE TABLE IF NOT EXISTS seedling_reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    seedling_id INTEGER,
                    customer_name TEXT,
                    quantity INTEGER,
                    reservation_date TIMESTAMP,
                    delivery_date TIMESTAMP,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (seedling_id) REFERENCES seedlings (id)
                )
            ''',
            'keywords': '''
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    keyword TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'trusted_sources': '''
                CREATE TABLE IF NOT EXISTS trusted_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT,
                    category TEXT,
                    reliability_score REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'audit_logs': '''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    entity_type TEXT,
                    entity_id INTEGER,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''',
            'learning_sessions': '''
                CREATE TABLE IF NOT EXISTS learning_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    model_type TEXT,
                    dataset_size INTEGER,
                    accuracy REAL,
                    distortion_rate REAL,
                    status TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'learning_results': '''
                CREATE TABLE IF NOT EXISTS learning_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    result_type TEXT,
                    result_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES learning_sessions (id)
                )
            '''
        }
    
    def initialize_databases(self):
        """تهيئة قواعد البيانات الأربعة"""
        for db_name, db_config in self.config['databases'].items():
            db_path = db_config['path']
            # التأكد من وجود المجلد
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # إنشاء الاتصال بقاعدة البيانات
            conn = sqlite3.connect(db_path)
            self.db_connections[db_name] = conn
            
            # إنشاء الجداول
            for table_name, table_schema in db_config['tables'].items():
                try:
                    conn.execute(table_schema)
                except Exception as e:
                    self.logger.error(f"خطأ في إنشاء جدول {table_name} في قاعدة بيانات {db_name}: {e}")
            
            conn.commit()
            self.logger.info(f"تم تهيئة قاعدة بيانات {db_name} بنجاح")
    
    def get_connection(self, db_name):
        """الحصول على اتصال بقاعدة بيانات محددة"""
        if db_name not in self.db_connections:
            raise ValueError(f"قاعدة البيانات {db_name} غير موجودة")
        return self.db_connections[db_name]
    
    def execute_query(self, db_name, query, params=None):
        """تنفيذ استعلام على قاعدة بيانات محددة"""
        conn = self.get_connection(db_name)
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            self.logger.error(f"خطأ في تنفيذ الاستعلام على قاعدة بيانات {db_name}: {e}")
            raise
    
    def fetch_all(self, db_name, query, params=None):
        """تنفيذ استعلام وإرجاع جميع النتائج"""
        cursor = self.execute_query(db_name, query, params)
        return cursor.fetchall()
    
    def fetch_one(self, db_name, query, params=None):
        """تنفيذ استعلام وإرجاع نتيجة واحدة"""
        cursor = self.execute_query(db_name, query, params)
        return cursor.fetchone()
    
    def insert(self, db_name, table, data):
        """إدراج بيانات في جدول محدد"""
        placeholders = ', '.join(['?'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute_query(db_name, query, values)
        return cursor.lastrowid
    
    def update(self, db_name, table, data, condition):
        """تحديث بيانات في جدول محدد"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in condition.keys()])
        values = tuple(list(data.values()) + list(condition.values()))
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        self.execute_query(db_name, query, values)
    
    def delete(self, db_name, table, condition):
        """حذف بيانات من جدول محدد"""
        where_clause = ' AND '.join([f"{key} = ?" for key in condition.keys()])
        values = tuple(condition.values())
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self.execute_query(db_name, query, values)
    
    def backup_database(self, db_name=None):
        """إنشاء نسخة احتياطية من قاعدة بيانات محددة أو جميع قواعد البيانات"""
        backup_dir = self.config['backup']['backup_dir']
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if db_name:
            if db_name not in self.config['databases']:
                raise ValueError(f"قاعدة البيانات {db_name} غير موجودة")
            
            db_path = self.config['databases'][db_name]['path']
            backup_path = os.path.join(backup_dir, f"{db_name}_{timestamp}.db")
            
            # إغلاق الاتصال مؤقتًا
            if db_name in self.db_connections:
                self.db_connections[db_name].close()
            
            # نسخ ملف قاعدة البيانات
            shutil.copy2(db_path, backup_path)
            
            # إعادة فتح الاتصال
            self.db_connections[db_name] = sqlite3.connect(db_path)
            
            self.logger.info(f"تم إنشاء نسخة احتياطية من قاعدة بيانات {db_name} في {backup_path}")
            return backup_path
        else:
            backup_paths = {}
            for db_name, db_config in self.config['databases'].items():
                db_path = db_config['path']
                backup_path = os.path.join(backup_dir, f"{db_name}_{timestamp}.db")
                
                # إغلاق الاتصال مؤقتًا
                if db_name in self.db_connections:
                    self.db_connections[db_name].close()
                
                # نسخ ملف قاعدة البيانات
                shutil.copy2(db_path, backup_path)
                
                # إعادة فتح الاتصال
                self.db_connections[db_name] = sqlite3.connect(db_path)
                
                backup_paths[db_name] = backup_path
                self.logger.info(f"تم إنشاء نسخة احتياطية من قاعدة بيانات {db_name} في {backup_path}")
            
            return backup_paths
    
    def restore_database(self, backup_path, db_name=None):
        """استعادة قاعدة بيانات من نسخة احتياطية"""
        if not os.path.exists(backup_path):
            raise ValueError(f"ملف النسخة الاحتياطية {backup_path} غير موجود")
        
        if db_name:
            if db_name not in self.config['databases']:
                raise ValueError(f"قاعدة البيانات {db_name} غير موجودة")
            
            db_path = self.config['databases'][db_name]['path']
            
            # إغلاق الاتصال مؤقتًا
            if db_name in self.db_connections:
                self.db_connections[db_name].close()
            
            # نسخ ملف النسخة الاحتياطية إلى قاعدة البيانات
            shutil.copy2(backup_path, db_path)
            
            # إعادة فتح الاتصال
            self.db_connections[db_name] = sqlite3.connect(db_path)
            
            self.logger.info(f"تم استعادة قاعدة بيانات {db_name} من {backup_path}")
        else:
            # استعادة جميع قواعد البيانات من مجلد النسخ الاحتياطية
            backup_dir = os.path.dirname(backup_path)
            for db_name, db_config in self.config['databases'].items():
                db_path = db_config['path']
                backup_files = [f for f in os.listdir(backup_dir) if f.startswith(f"{db_name}_")]
                
                if not backup_files:
                    self.logger.warning(f"لا توجد نسخ احتياطية لقاعدة بيانات {db_name}")
                    continue
                
                # اختيار أحدث نسخة احتياطية
                latest_backup = sorted(backup_files)[-1]
                latest_backup_path = os.path.join(backup_dir, latest_backup)
                
                # إغلاق الاتصال مؤقتًا
                if db_name in self.db_connections:
                    self.db_connections[db_name].close()
                
                # نسخ ملف النسخة الاحتياطية إلى قاعدة البيانات
                shutil.copy2(latest_backup_path, db_path)
                
                # إعادة فتح الاتصال
                self.db_connections[db_name] = sqlite3.connect(db_path)
                
                self.logger.info(f"تم استعادة قاعدة بيانات {db_name} من {latest_backup_path}")
    
    def cleanup_old_backups(self):
        """تنظيف النسخ الاحتياطية القديمة"""
        backup_dir = self.config['backup']['backup_dir']
        retention_days = self.config['backup']['retention_days']
        
        if not os.path.exists(backup_dir):
            return
        
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
        
        for filename in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, filename)
            
            # تخطي المجلدات
            if os.path.isdir(file_path):
                continue
            
            # الحصول على تاريخ إنشاء الملف
            file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            
            # حذف الملفات القديمة
            if file_creation_time < cutoff_date:
                os.remove(file_path)
                self.logger.info(f"تم حذف النسخة الاحتياطية القديمة: {filename}")
    
    def close_all_connections(self):
        """إغلاق جميع اتصالات قواعد البيانات"""
        for db_name, conn in self.db_connections.items():
            conn.close()
        self.db_connections = {}
        self.logger.info("تم إغلاق جميع اتصالات قواعد البيانات")
    
    def __del__(self):
        """تنظيف الموارد عند حذف الكائن"""
        self.close_all_connections()


# مثال على الاستخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # إنشاء مدير قواعد البيانات
    db_manager = DatabaseManager()
    
    # إدراج بيانات تجريبية في قاعدة البيانات التشغيلية
    user_id = db_manager.insert('operational', 'users', {
        'username': 'admin',
        'password_hash': 'hashed_password',
        'email': 'admin@example.com',
        'role': 'admin',
        'country': 'مصر',
        'company': 'شركة الزراعة المتقدمة'
    })
    
    print(f"تم إدراج مستخدم جديد بمعرف: {user_id}")
    
    # استعلام عن المستخدمين
    users = db_manager.fetch_all('operational', 'SELECT * FROM users')
    print("المستخدمون:")
    for user in users:
        print(user)
    
    # إنشاء نسخة احتياطية
    backup_path = db_manager.backup_database('operational')
    print(f"تم إنشاء نسخة احتياطية في: {backup_path}")
    
    # إغلاق الاتصالات
    db_manager.close_all_connections()
