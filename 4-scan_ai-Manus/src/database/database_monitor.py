#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام مراقبة وتحسين أداء قواعد البيانات
يوفر أدوات لمراقبة أداء قواعد البيانات وتحسينها
"""

import os
import json
import logging
import datetime
import sqlite3
import time
import threading
import psutil
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class DatabaseMonitor:
    """مراقب أداء قواعد البيانات"""
    
    def __init__(self, db_manager, config_path=None):
        """تهيئة مراقب الأداء"""
        self.logger = logging.getLogger(__name__)
        self.db_manager = db_manager
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'monitoring.json')
        self.metrics_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'metrics')
        self.reports_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')
        
        # إنشاء المجلدات اللازمة
        os.makedirs(self.metrics_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # تحميل التكوين
        self.config = self._load_config()
        
        # إنشاء جداول المقاييس
        self._create_metrics_tables()
        
        # متغيرات للمراقبة المستمرة
        self.monitoring_thread = None
        self.stop_monitoring = threading.Event()
    
    def _load_config(self):
        """تحميل ملف التكوين"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # إنشاء ملف تكوين افتراضي
                config = {
                    'monitoring': {
                        'interval_seconds': 60,
                        'retention_days': 30,
                        'alert_thresholds': {
                            'query_time_ms': 1000,
                            'disk_usage_percent': 80,
                            'memory_usage_percent': 80,
                            'cpu_usage_percent': 80
                        }
                    },
                    'performance': {
                        'vacuum_threshold_mb': 100,
                        'index_analysis_threshold_ms': 500,
                        'auto_optimize': True
                    },
                    'reporting': {
                        'daily_report': True,
                        'weekly_report': True,
                        'monthly_report': True,
                        'report_recipients': []
                    }
                }
                
                # حفظ التكوين الافتراضي
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                return config
        except Exception as e:
            self.logger.error(f"خطأ في تحميل ملف التكوين: {e}")
            # إعداد تكوين افتراضي
            return {
                'monitoring': {
                    'interval_seconds': 60,
                    'retention_days': 30,
                    'alert_thresholds': {
                        'query_time_ms': 1000,
                        'disk_usage_percent': 80,
                        'memory_usage_percent': 80,
                        'cpu_usage_percent': 80
                    }
                },
                'performance': {
                    'vacuum_threshold_mb': 100,
                    'index_analysis_threshold_ms': 500,
                    'auto_optimize': True
                },
                'reporting': {
                    'daily_report': True,
                    'weekly_report': True,
                    'monthly_report': True,
                    'report_recipients': []
                }
            }
    
    def _create_metrics_tables(self):
        """إنشاء جداول المقاييس في قاعدة البيانات التشغيلية"""
        try:
            # جدول مقاييس الأداء
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    db_name TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    details TEXT
                )
            ''')
            
            # جدول سجل الاستعلامات البطيئة
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS slow_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    db_name TEXT NOT NULL,
                    query TEXT NOT NULL,
                    execution_time_ms REAL NOT NULL,
                    parameters TEXT
                )
            ''')
            
            # جدول تنبيهات الأداء
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS performance_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    db_name TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    alert_message TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    threshold REAL NOT NULL,
                    is_resolved INTEGER DEFAULT 0,
                    resolved_at TIMESTAMP
                )
            ''')
            
            # جدول توصيات تحسين الأداء
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS performance_recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    db_name TEXT NOT NULL,
                    recommendation_type TEXT NOT NULL,
                    recommendation TEXT NOT NULL,
                    expected_improvement TEXT,
                    is_applied INTEGER DEFAULT 0,
                    applied_at TIMESTAMP
                )
            ''')
            
            self.logger.info("تم إنشاء جداول المقاييس بنجاح")
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء جداول المقاييس: {e}")
            raise
    
    def record_query_execution(self, db_name, query, execution_time_ms, parameters=None):
        """تسجيل وقت تنفيذ الاستعلام"""
        try:
            # تسجيل الاستعلام إذا كان بطيئًا
            threshold = self.config['monitoring']['alert_thresholds']['query_time_ms']
            if execution_time_ms > threshold:
                self.db_manager.insert('operational', 'slow_queries', {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'db_name': db_name,
                    'query': query,
                    'execution_time_ms': execution_time_ms,
                    'parameters': json.dumps(parameters) if parameters else None
                })
                
                # إنشاء تنبيه للاستعلام البطيء
                self.create_alert(db_name, 'slow_query', f"استعلام بطيء في قاعدة البيانات {db_name}", execution_time_ms, threshold)
                
                self.logger.warning(f"استعلام بطيء في قاعدة البيانات {db_name}: {execution_time_ms} مللي ثانية")
            
            # تسجيل مقياس وقت التنفيذ
            self.record_metric(db_name, 'query_execution_time', execution_time_ms, {'query': query[:100]})
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل وقت تنفيذ الاستعلام: {e}")
            return False
    
    def record_metric(self, db_name, metric_type, metric_value, details=None):
        """تسجيل مقياس أداء"""
        try:
            self.db_manager.insert('operational', 'performance_metrics', {
                'timestamp': datetime.datetime.now().isoformat(),
                'db_name': db_name,
                'metric_type': metric_type,
                'metric_value': metric_value,
                'details': json.dumps(details) if details else None
            })
            
            # التحقق من تجاوز العتبة وإنشاء تنبيه إذا لزم الأمر
            if metric_type in self.config['monitoring']['alert_thresholds']:
                threshold = self.config['monitoring']['alert_thresholds'][metric_type]
                if metric_value > threshold:
                    self.create_alert(db_name, metric_type, f"تجاوز عتبة {metric_type} في قاعدة البيانات {db_name}", metric_value, threshold)
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل مقياس الأداء: {e}")
            return False
    
    def create_alert(self, db_name, alert_type, alert_message, metric_value, threshold):
        """إنشاء تنبيه أداء"""
        try:
            self.db_manager.insert('operational', 'performance_alerts', {
                'timestamp': datetime.datetime.now().isoformat(),
                'db_name': db_name,
                'alert_type': alert_type,
                'alert_message': alert_message,
                'metric_value': metric_value,
                'threshold': threshold,
                'is_resolved': 0,
                'resolved_at': None
            })
            
            self.logger.warning(f"تنبيه أداء: {alert_message} (القيمة: {metric_value}, العتبة: {threshold})")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تنبيه أداء: {e}")
            return False
    
    def resolve_alert(self, alert_id):
        """حل تنبيه أداء"""
        try:
            self.db_manager.update('operational', 'performance_alerts', {
                'is_resolved': 1,
                'resolved_at': datetime.datetime.now().isoformat()
            }, {'id': alert_id})
            
            self.logger.info(f"تم حل تنبيه الأداء رقم {alert_id}")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حل تنبيه الأداء: {e}")
            return False
    
    def create_recommendation(self, db_name, recommendation_type, recommendation, expected_improvement=None):
        """إنشاء توصية لتحسين الأداء"""
        try:
            self.db_manager.insert('operational', 'performance_recommendations', {
                'timestamp': datetime.datetime.now().isoformat(),
                'db_name': db_name,
                'recommendation_type': recommendation_type,
                'recommendation': recommendation,
                'expected_improvement': expected_improvement,
                'is_applied': 0,
                'applied_at': None
            })
            
            self.logger.info(f"توصية لتحسين الأداء: {recommendation}")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء توصية لتحسين الأداء: {e}")
            return False
    
    def apply_recommendation(self, recommendation_id):
        """تطبيق توصية تحسين الأداء"""
        try:
            self.db_manager.update('operational', 'performance_recommendations', {
                'is_applied': 1,
                'applied_at': datetime.datetime.now().isoformat()
            }, {'id': recommendation_id})
            
            self.logger.info(f"تم تطبيق توصية تحسين الأداء رقم {recommendation_id}")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تطبيق توصية تحسين الأداء: {e}")
            return False
    
    def collect_system_metrics(self):
        """جمع مقاييس النظام"""
        try:
            # استخدام مقاييس النظام
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # تسجيل مقاييس النظام
            self.record_metric('system', 'cpu_usage_percent', cpu_percent)
            self.record_metric('system', 'memory_usage_percent', memory.percent)
            self.record_metric('system', 'disk_usage_percent', disk.percent)
            
            # جمع مقاييس قواعد البيانات
            for db_name in ['operational', 'employee_training', 'system_training', 'backup']:
                try:
                    # حجم ملف قاعدة البيانات
                    db_path = self.db_manager.get_db_path(db_name)
                    if os.path.exists(db_path):
                        db_size_mb = os.path.getsize(db_path) / (1024 * 1024)
                        self.record_metric(db_name, 'db_size_mb', db_size_mb)
                        
                        # التحقق من الحاجة إلى تنظيف قاعدة البيانات
                        vacuum_threshold = self.config['performance']['vacuum_threshold_mb']
                        if db_size_mb > vacuum_threshold and self.config['performance']['auto_optimize']:
                            self.create_recommendation(db_name, 'vacuum', f"تنظيف قاعدة البيانات {db_name} لتقليل الحجم", f"تقليل الحجم من {db_size_mb:.2f} ميجابايت")
                    
                    # عدد الصفوف في الجداول الرئيسية
                    conn = self.db_manager.get_connection(db_name)
                    cursor = conn.cursor()
                    
                    # الحصول على قائمة الجداول
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                    tables = cursor.fetchall()
                    
                    for table in tables:
                        table_name = table[0]
                        try:
                            # عدد الصفوف في الجدول
                            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                            row_count = cursor.fetchone()[0]
                            self.record_metric(db_name, f"table_rows_{table_name}", row_count)
                        except Exception as table_error:
                            self.logger.error(f"خطأ في جمع مقاييس الجدول {table_name} في قاعدة البيانات {db_name}: {table_error}")
                except Exception as db_error:
                    self.logger.error(f"خطأ في جمع مقاييس قاعدة البيانات {db_name}: {db_error}")
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في جمع مقاييس النظام: {e}")
            return False
    
    def analyze_slow_queries(self):
        """تحليل الاستعلامات البطيئة وتقديم توصيات"""
        try:
            # الحصول على الاستعلامات البطيئة الأخيرة
            slow_queries = self.db_manager.fetch_all('operational', '''
                SELECT id, db_name, query, execution_time_ms, parameters
                FROM slow_queries
                WHERE timestamp > datetime('now', '-1 day')
                ORDER BY execution_time_ms DESC
                LIMIT 100
            ''')
            
            # تحليل الاستعلامات وتقديم توصيات
            for query_data in slow_queries:
                query_id, db_name, query, execution_time_ms, parameters = query_data
                
                # تحليل الاستعلام
                if 'SELECT' in query.upper():
                    # التحقق من وجود WHERE
                    if 'WHERE' not in query.upper():
                        self.create_recommendation(db_name, 'query_optimization', f"إضافة شرط WHERE للاستعلام: {query[:100]}...", "تقليل عدد الصفوف المسترجعة")
                    
                    # التحقق من استخدام LIKE مع بداية النص
                    if 'LIKE' in query.upper() and '%' in query and query.find('%') < query.find('LIKE'):
                        self.create_recommendation(db_name, 'query_optimization', f"تجنب استخدام LIKE مع بداية النص: {query[:100]}...", "تحسين استخدام الفهارس")
                    
                    # التحقق من استخدام الوظائف على الأعمدة
                    if any(func in query.upper() for func in ['UPPER(', 'LOWER(', 'SUBSTR(']):
                        self.create_recommendation(db_name, 'query_optimization', f"تجنب استخدام الوظائف على الأعمدة في شروط WHERE: {query[:100]}...", "تحسين استخدام الفهارس")
                
                # التحقق من الحاجة إلى فهارس
                if 'WHERE' in query.upper():
                    # استخراج الأعمدة المستخدمة في WHERE
                    where_clause = query.upper().split('WHERE')[1].split('ORDER BY')[0].split('GROUP BY')[0].split('HAVING')[0]
                    columns = re.findall(r'([a-zA-Z0-9_]+)\s*[=<>]', where_clause)
                    
                    for column in columns:
                        if column.lower() not in ['id', 'rowid']:
                            # التحقق من وجود فهرس للعمود
                            try:
                                # استخراج اسم الجدول
                                table_match = re.search(r'FROM\s+([a-zA-Z0-9_]+)', query.upper())
                                if table_match:
                                    table_name = table_match.group(1)
                                    
                                    conn = self.db_manager.get_connection(db_name)
                                    cursor = conn.cursor()
                                    cursor.execute(f"PRAGMA index_list({table_name})")
                                    indexes = cursor.fetchall()
                                    
                                    # التحقق من وجود فهرس يحتوي على العمود
                                    column_indexed = False
                                    for idx in indexes:
                                        index_name = idx[1]
                                        cursor.execute(f"PRAGMA index_info({index_name})")
                                        index_columns = cursor.fetchall()
                                        if any(col[2].lower() == column.lower() for col in index_columns):
                                            column_indexed = True
                                            break
                                    
                                    if not column_indexed:
                                        self.create_recommendation(db_name, 'index_creation', f"إنشاء فهرس للعمود {column} في الجدول {table_name}", f"تحسين أداء الاستعلامات التي تستخدم العمود {column}")
                            except Exception as index_error:
                                self.logger.error(f"خطأ في التحقق من فهارس العمود {column}: {index_error}")
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تحليل الاستعلامات البطيئة: {e}")
            return False
    
    def analyze_indexes(self, db_name):
        """تحليل الفهارس وتقديم توصيات"""
        try:
            conn = self.db_manager.get_connection(db_name)
            cursor = conn.cursor()
            
            # الحصول على قائمة الجداول
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                
                # الحصول على قائمة الفهارس للجدول
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()
                
                # الحصول على قائمة الأعمدة في الجدول
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                # تحليل استخدام الفهارس
                for column in columns:
                    column_name = column[1]
                    column_type = column[2].upper()
                    
                    # التحقق من وجود فهرس للعمود
                    column_indexed = False
                    for idx in indexes:
                        index_name = idx[1]
                        cursor.execute(f"PRAGMA index_info({index_name})")
                        index_columns = cursor.fetchall()
                        if any(col[2] == column_name for col in index_columns):
                            column_indexed = True
                            break
                    
                    # توصيات للفهارس
                    if not column_indexed:
                        # الأعمدة التي قد تحتاج إلى فهارس
                        if any(hint in column_name.lower() for hint in ['id', 'code', 'key', 'name', 'date', 'time', 'status']):
                            self.create_recommendation(db_name, 'index_creation', f"إنشاء فهرس للعمود {column_name} في الجدول {table_name}", f"تحسين أداء الاستعلامات التي تستخدم العمود {column_name}")
                        
                        # الأعمدة التي قد تستخدم في JOIN
                        if column_name.endswith('_id') or column_name == 'id':
                            self.create_recommendation(db_name, 'index_creation', f"إنشاء فهرس للعمود {column_name} في الجدول {table_name}", f"تحسين أداء عمليات JOIN التي تستخدم العمود {column_name}")
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تحليل الفهارس: {e}")
            return False
    
    def optimize_database(self, db_name):
        """تحسين أداء قاعدة البيانات"""
        try:
            conn = self.db_manager.get_connection(db_name)
            cursor = conn.cursor()
            
            # تنفيذ VACUUM لتقليل حجم قاعدة البيانات
            start_time = time.time()
            cursor.execute("VACUUM")
            vacuum_time = time.time() - start_time
            
            # تنفيذ ANALYZE لتحديث إحصائيات الفهارس
            start_time = time.time()
            cursor.execute("ANALYZE")
            analyze_time = time.time() - start_time
            
            # تسجيل مقاييس التحسين
            self.record_metric(db_name, 'vacuum_time_seconds', vacuum_time)
            self.record_metric(db_name, 'analyze_time_seconds', analyze_time)
            
            # حجم قاعدة البيانات بعد التحسين
            db_path = self.db_manager.get_db_path(db_name)
            db_size_mb = os.path.getsize(db_path) / (1024 * 1024)
            self.record_metric(db_name, 'db_size_after_optimization_mb', db_size_mb)
            
            self.logger.info(f"تم تحسين قاعدة البيانات {db_name} (VACUUM: {vacuum_time:.2f} ثانية, ANALYZE: {analyze_time:.2f} ثانية)")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تحسين قاعدة البيانات {db_name}: {e}")
            return False
    
    def cleanup_old_metrics(self):
        """تنظيف المقاييس القديمة"""
        try:
            retention_days = self.config['monitoring']['retention_days']
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
            cutoff_str = cutoff_date.isoformat()
            
            # حذف المقاييس القديمة
            self.db_manager.execute('operational', "DELETE FROM performance_metrics WHERE timestamp < ?", (cutoff_str,))
            self.db_manager.execute('operational', "DELETE FROM slow_queries WHERE timestamp < ?", (cutoff_str,))
            
            # حذف التنبيهات المحلولة القديمة
            self.db_manager.execute('operational', "DELETE FROM performance_alerts WHERE is_resolved = 1 AND resolved_at < ?", (cutoff_str,))
            
            # حذف التوصيات المطبقة القديمة
            self.db_manager.execute('operational', "DELETE FROM performance_recommendations WHERE is_applied = 1 AND applied_at < ?", (cutoff_str,))
            
            self.logger.info(f"تم تنظيف المقاييس القديمة (أقدم من {retention_days} يوم)")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تنظيف المقاييس القديمة: {e}")
            return False
    
    def generate_performance_report(self, report_type='daily', start_date=None, end_date=None):
        """توليد تقرير أداء"""
        try:
            # تحديد فترة التقرير
            if not end_date:
                end_date = datetime.datetime.now()
            
            if not start_date:
                if report_type == 'daily':
                    start_date = end_date - datetime.timedelta(days=1)
                elif report_type == 'weekly':
                    start_date = end_date - datetime.timedelta(days=7)
                elif report_type == 'monthly':
                    start_date = end_date - datetime.timedelta(days=30)
                else:
                    start_date = end_date - datetime.timedelta(days=1)
            
            start_str = start_date.isoformat()
            end_str = end_date.isoformat()
            
            report = {
                'report_type': report_type,
                'start_date': start_str,
                'end_date': end_str,
                'generated_at': datetime.datetime.now().isoformat(),
                'system_metrics': {},
                'database_metrics': {},
                'slow_queries': {},
                'alerts': {},
                'recommendations': {}
            }
            
            # جمع مقاييس النظام
            system_metrics = self.db_manager.fetch_all('operational', '''
                SELECT metric_type, AVG(metric_value) as avg_value, MAX(metric_value) as max_value, MIN(metric_value) as min_value
                FROM performance_metrics
                WHERE db_name = 'system' AND timestamp BETWEEN ? AND ?
                GROUP BY metric_type
            ''', (start_str, end_str))
            
            for metric in system_metrics:
                metric_type, avg_value, max_value, min_value = metric
                report['system_metrics'][metric_type] = {
                    'avg': avg_value,
                    'max': max_value,
                    'min': min_value
                }
            
            # جمع مقاييس قواعد البيانات
            for db_name in ['operational', 'employee_training', 'system_training', 'backup']:
                db_metrics = self.db_manager.fetch_all('operational', '''
                    SELECT metric_type, AVG(metric_value) as avg_value, MAX(metric_value) as max_value, MIN(metric_value) as min_value
                    FROM performance_metrics
                    WHERE db_name = ? AND timestamp BETWEEN ? AND ?
                    GROUP BY metric_type
                ''', (db_name, start_str, end_str))
                
                report['database_metrics'][db_name] = {}
                for metric in db_metrics:
                    metric_type, avg_value, max_value, min_value = metric
                    report['database_metrics'][db_name][metric_type] = {
                        'avg': avg_value,
                        'max': max_value,
                        'min': min_value
                    }
            
            # جمع الاستعلامات البطيئة
            for db_name in ['operational', 'employee_training', 'system_training', 'backup']:
                slow_queries = self.db_manager.fetch_all('operational', '''
                    SELECT query, AVG(execution_time_ms) as avg_time, COUNT(*) as count
                    FROM slow_queries
                    WHERE db_name = ? AND timestamp BETWEEN ? AND ?
                    GROUP BY query
                    ORDER BY avg_time DESC
                    LIMIT 10
                ''', (db_name, start_str, end_str))
                
                report['slow_queries'][db_name] = []
                for query_data in slow_queries:
                    query, avg_time, count = query_data
                    report['slow_queries'][db_name].append({
                        'query': query,
                        'avg_time_ms': avg_time,
                        'count': count
                    })
            
            # جمع التنبيهات
            alerts = self.db_manager.fetch_all('operational', '''
                SELECT db_name, alert_type, COUNT(*) as count
                FROM performance_alerts
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY db_name, alert_type
                ORDER BY count DESC
            ''', (start_str, end_str))
            
            for alert_data in alerts:
                db_name, alert_type, count = alert_data
                if db_name not in report['alerts']:
                    report['alerts'][db_name] = {}
                report['alerts'][db_name][alert_type] = count
            
            # جمع التوصيات
            recommendations = self.db_manager.fetch_all('operational', '''
                SELECT db_name, recommendation_type, recommendation, is_applied
                FROM performance_recommendations
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            ''', (start_str, end_str))
            
            for rec_data in recommendations:
                db_name, rec_type, recommendation, is_applied = rec_data
                if db_name not in report['recommendations']:
                    report['recommendations'][db_name] = []
                report['recommendations'][db_name].append({
                    'type': rec_type,
                    'recommendation': recommendation,
                    'is_applied': bool(is_applied)
                })
            
            # إنشاء رسوم بيانية
            self._create_performance_charts(report, report_type)
            
            # حفظ التقرير
            report_filename = f"{report_type}_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_path = os.path.join(self.reports_dir, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"تم توليد تقرير الأداء {report_type} وحفظه في {report_path}")
            return True, report_path
        except Exception as e:
            self.logger.error(f"خطأ في توليد تقرير الأداء: {e}")
            return False, str(e)
    
    def _create_performance_charts(self, report, report_type):
        """إنشاء رسوم بيانية للأداء"""
        try:
            # إنشاء مجلد للرسوم البيانية
            charts_dir = os.path.join(self.reports_dir, 'charts')
            os.makedirs(charts_dir, exist_ok=True)
            
            # تاريخ التقرير
            report_date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            # رسم بياني لمقاييس النظام
            if report['system_metrics']:
                plt.figure(figsize=(10, 6))
                metrics = []
                values = []
                
                for metric, data in report['system_metrics'].items():
                    metrics.append(metric)
                    values.append(data['avg'])
                
                plt.bar(metrics, values)
                plt.title(f"متوسط مقاييس النظام ({report_type})")
                plt.xlabel("المقياس")
                plt.ylabel("القيمة")
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                chart_path = os.path.join(charts_dir, f"system_metrics_{report_type}_{report_date}.png")
                plt.savefig(chart_path)
                plt.close()
            
            # رسم بياني لمقاييس قواعد البيانات
            if report['database_metrics']:
                # مقياس حجم قاعدة البيانات
                plt.figure(figsize=(10, 6))
                db_names = []
                db_sizes = []
                
                for db_name, metrics in report['database_metrics'].items():
                    if 'db_size_mb' in metrics:
                        db_names.append(db_name)
                        db_sizes.append(metrics['db_size_mb']['avg'])
                
                if db_names:
                    plt.bar(db_names, db_sizes)
                    plt.title(f"متوسط حجم قواعد البيانات ({report_type})")
                    plt.xlabel("قاعدة البيانات")
                    plt.ylabel("الحجم (ميجابايت)")
                    plt.tight_layout()
                    
                    chart_path = os.path.join(charts_dir, f"db_size_{report_type}_{report_date}.png")
                    plt.savefig(chart_path)
                    plt.close()
            
            # رسم بياني للاستعلامات البطيئة
            if report['slow_queries']:
                plt.figure(figsize=(10, 6))
                db_names = []
                query_counts = []
                
                for db_name, queries in report['slow_queries'].items():
                    db_names.append(db_name)
                    query_counts.append(len(queries))
                
                if db_names:
                    plt.bar(db_names, query_counts)
                    plt.title(f"عدد الاستعلامات البطيئة حسب قاعدة البيانات ({report_type})")
                    plt.xlabel("قاعدة البيانات")
                    plt.ylabel("عدد الاستعلامات البطيئة")
                    plt.tight_layout()
                    
                    chart_path = os.path.join(charts_dir, f"slow_queries_{report_type}_{report_date}.png")
                    plt.savefig(chart_path)
                    plt.close()
            
            # رسم بياني للتنبيهات
            if report['alerts']:
                plt.figure(figsize=(10, 6))
                alert_types = []
                alert_counts = []
                
                for db_name, alerts in report['alerts'].items():
                    for alert_type, count in alerts.items():
                        alert_types.append(f"{db_name}: {alert_type}")
                        alert_counts.append(count)
                
                if alert_types:
                    plt.bar(alert_types, alert_counts)
                    plt.title(f"عدد التنبيهات حسب النوع ({report_type})")
                    plt.xlabel("نوع التنبيه")
                    plt.ylabel("عدد التنبيهات")
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    chart_path = os.path.join(charts_dir, f"alerts_{report_type}_{report_date}.png")
                    plt.savefig(chart_path)
                    plt.close()
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الرسوم البيانية: {e}")
            return False
    
    def start_monitoring(self):
        """بدء المراقبة المستمرة"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.logger.warning("المراقبة المستمرة قيد التشغيل بالفعل")
            return False
        
        self.stop_monitoring.clear()
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        self.logger.info("تم بدء المراقبة المستمرة")
        return True
    
    def stop_monitoring(self):
        """إيقاف المراقبة المستمرة"""
        if not self.monitoring_thread or not self.monitoring_thread.is_alive():
            self.logger.warning("المراقبة المستمرة ليست قيد التشغيل")
            return False
        
        self.stop_monitoring.set()
        self.monitoring_thread.join(timeout=10)
        
        self.logger.info("تم إيقاف المراقبة المستمرة")
        return True
    
    def _monitoring_loop(self):
        """حلقة المراقبة المستمرة"""
        interval = self.config['monitoring']['interval_seconds']
        
        while not self.stop_monitoring.is_set():
            try:
                # جمع مقاييس النظام
                self.collect_system_metrics()
                
                # تحليل الاستعلامات البطيئة
                self.analyze_slow_queries()
                
                # تنظيف المقاييس القديمة
                self.cleanup_old_metrics()
                
                # توليد تقارير دورية
                now = datetime.datetime.now()
                
                # تقرير يومي
                if self.config['reporting']['daily_report'] and now.hour == 0 and now.minute < interval / 60:
                    self.generate_performance_report('daily')
                
                # تقرير أسبوعي
                if self.config['reporting']['weekly_report'] and now.weekday() == 0 and now.hour == 1 and now.minute < interval / 60:
                    self.generate_performance_report('weekly')
                
                # تقرير شهري
                if self.config['reporting']['monthly_report'] and now.day == 1 and now.hour == 2 and now.minute < interval / 60:
                    self.generate_performance_report('monthly')
                
                # تحسين قواعد البيانات
                if self.config['performance']['auto_optimize'] and now.hour == 3 and now.minute < interval / 60:
                    for db_name in ['operational', 'employee_training', 'system_training', 'backup']:
                        self.optimize_database(db_name)
            except Exception as e:
                self.logger.error(f"خطأ في حلقة المراقبة: {e}")
            
            # الانتظار حتى الفاصل الزمني التالي
            self.stop_monitoring.wait(interval)


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
    
    # إنشاء مراقب الأداء
    monitor = DatabaseMonitor(db_manager)
    
    # جمع مقاييس النظام
    monitor.collect_system_metrics()
    
    # تحليل الفهارس
    for db_name in ['operational', 'employee_training', 'system_training', 'backup']:
        monitor.analyze_indexes(db_name)
    
    # توليد تقرير أداء
    success, report_path = monitor.generate_performance_report('daily')
    print(f"توليد تقرير الأداء: {success}, {report_path}")
    
    # بدء المراقبة المستمرة
    monitor.start_monitoring()
    
    # يمكن إيقاف المراقبة لاحقًا
    # monitor.stop_monitoring()
