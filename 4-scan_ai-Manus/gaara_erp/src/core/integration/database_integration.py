"""
وحدة تكامل قواعد البيانات بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي

هذه الوحدة مسؤولة عن:
1. إنشاء وإدارة الاتصال بقواعد بيانات النظامين
2. مزامنة البيانات بين النظامين
3. التحقق من سلامة البيانات أثناء عمليات النقل
4. إدارة التحديثات والتغييرات في هيكل البيانات
"""

import os
import json
import logging
import sqlite3
import psycopg2
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("database_integration")

class DatabaseIntegration:
    """فئة تكامل قواعد البيانات بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي"""
    
    def __init__(self, config_path=None):
        """
        تهيئة وحدة تكامل قواعد البيانات
        
        المعلمات:
            config_path (str): مسار ملف التكوين (اختياري)
        """
        self.config = self._load_config(config_path)
        self.erp_engine = self._create_erp_db_engine()
        self.ai_engine = self._create_ai_db_engine()
        self.sync_tables = self.config.get('sync_tables', {})
        self.last_sync = {}
        
        # تحميل سجل آخر مزامنة إذا كان موجوداً
        self._load_last_sync()
        
        logger.info("تم تهيئة وحدة تكامل قواعد البيانات بنجاح")
    
    def _load_config(self, config_path):
        """
        تحميل ملف التكوين
        
        المعلمات:
            config_path (str): مسار ملف التكوين
            
        العوائد:
            dict: بيانات التكوين
        """
        default_config = {
            'erp_db': {
                'type': 'postgresql',
                'host': 'localhost',
                'port': 5432,
                'database': 'gaara_erp',
                'user': 'postgres',
                'password': 'postgres'
            },
            'ai_db': {
                'type': 'postgresql',
                'host': 'localhost',
                'port': 5432,
                'database': 'agricultural_ai',
                'user': 'postgres',
                'password': 'postgres'
            },
            'sync_interval': 3600,  # بالثواني
            'sync_tables': {
                'nurseries': {
                    'erp_table': 'nursery',
                    'ai_table': 'nurseries',
                    'primary_key': 'id',
                    'direction': 'erp_to_ai',
                    'fields_mapping': {
                        'id': 'id',
                        'name': 'name',
                        'location': 'location',
                        'capacity': 'capacity',
                        'status': 'status'
                    }
                },
                'plants': {
                    'erp_table': 'plant',
                    'ai_table': 'plants',
                    'primary_key': 'id',
                    'direction': 'bidirectional',
                    'fields_mapping': {
                        'id': 'id',
                        'name': 'name',
                        'variety': 'variety',
                        'planting_date': 'planting_date',
                        'nursery_id': 'nursery_id'
                    }
                },
                'diseases': {
                    'erp_table': 'disease',
                    'ai_table': 'diseases',
                    'primary_key': 'id',
                    'direction': 'ai_to_erp',
                    'fields_mapping': {
                        'id': 'id',
                        'name': 'name',
                        'description': 'description',
                        'symptoms': 'symptoms',
                        'treatment': 'treatment'
                    }
                },
                'disease_detections': {
                    'erp_table': 'disease_detection',
                    'ai_table': 'disease_detections',
                    'primary_key': 'id',
                    'direction': 'ai_to_erp',
                    'fields_mapping': {
                        'id': 'id',
                        'plant_id': 'plant_id',
                        'disease_id': 'disease_id',
                        'detection_date': 'detection_date',
                        'confidence': 'confidence',
                        'status': 'status'
                    }
                },
                'breeding_requests': {
                    'erp_table': 'breeding_request',
                    'ai_table': 'breeding_requests',
                    'primary_key': 'id',
                    'direction': 'erp_to_ai',
                    'fields_mapping': {
                        'id': 'id',
                        'parent1_id': 'parent1_id',
                        'parent2_id': 'parent2_id',
                        'target_traits': 'target_traits',
                        'request_date': 'request_date',
                        'status': 'status'
                    }
                },
                'breeding_results': {
                    'erp_table': 'breeding_result',
                    'ai_table': 'breeding_results',
                    'primary_key': 'id',
                    'direction': 'ai_to_erp',
                    'fields_mapping': {
                        'id': 'id',
                        'request_id': 'request_id',
                        'result_date': 'result_date',
                        'predicted_traits': 'predicted_traits',
                        'success_probability': 'success_probability',
                        'recommendations': 'recommendations'
                    }
                }
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # دمج التكوين المخصص مع التكوين الافتراضي
                    for key, value in config.items():
                        if isinstance(value, dict) and key in default_config and isinstance(default_config[key], dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
                logger.info(f"تم تحميل ملف التكوين من {config_path}")
            except Exception as e:
                logger.error(f"خطأ في تحميل ملف التكوين: {str(e)}")
        else:
            logger.warning("لم يتم تحديد ملف تكوين، استخدام الإعدادات الافتراضية")
        
        return default_config
    
    def _create_erp_db_engine(self):
        """
        إنشاء محرك اتصال بقاعدة بيانات نظام ERP
        
        العوائد:
            sqlalchemy.engine.Engine: محرك الاتصال بقاعدة البيانات
        """
        db_config = self.config['erp_db']
        db_type = db_config['type']
        
        if db_type == 'postgresql':
            connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        elif db_type == 'mysql':
            connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        elif db_type == 'sqlite':
            connection_string = f"sqlite:///{db_config['database']}"
        else:
            raise ValueError(f"نوع قاعدة البيانات غير مدعوم: {db_type}")
        
        try:
            engine = create_engine(connection_string)
            # اختبار الاتصال
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"تم الاتصال بنجاح بقاعدة بيانات نظام ERP ({db_type})")
            return engine
        except Exception as e:
            logger.error(f"فشل الاتصال بقاعدة بيانات نظام ERP: {str(e)}")
            raise
    
    def _create_ai_db_engine(self):
        """
        إنشاء محرك اتصال بقاعدة بيانات نظام الذكاء الاصطناعي
        
        العوائد:
            sqlalchemy.engine.Engine: محرك الاتصال بقاعدة البيانات
        """
        db_config = self.config['ai_db']
        db_type = db_config['type']
        
        if db_type == 'postgresql':
            connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        elif db_type == 'mysql':
            connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        elif db_type == 'sqlite':
            connection_string = f"sqlite:///{db_config['database']}"
        else:
            raise ValueError(f"نوع قاعدة البيانات غير مدعوم: {db_type}")
        
        try:
            engine = create_engine(connection_string)
            # اختبار الاتصال
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"تم الاتصال بنجاح بقاعدة بيانات نظام الذكاء الاصطناعي ({db_type})")
            return engine
        except Exception as e:
            logger.error(f"فشل الاتصال بقاعدة بيانات نظام الذكاء الاصطناعي: {str(e)}")
            raise
    
    def _load_last_sync(self):
        """تحميل سجل آخر مزامنة من الملف"""
        sync_file = "last_sync.json"
        if os.path.exists(sync_file):
            try:
                with open(sync_file, 'r') as f:
                    self.last_sync = json.load(f)
                logger.info("تم تحميل سجل آخر مزامنة بنجاح")
            except Exception as e:
                logger.error(f"خطأ في تحميل سجل آخر مزامنة: {str(e)}")
                self.last_sync = {}
        else:
            logger.info("لم يتم العثور على سجل آخر مزامنة، سيتم إنشاء سجل جديد")
            self.last_sync = {}
    
    def _save_last_sync(self):
        """حفظ سجل آخر مزامنة إلى الملف"""
        sync_file = "last_sync.json"
        try:
            with open(sync_file, 'w') as f:
                json.dump(self.last_sync, f, indent=4)
            logger.info("تم حفظ سجل آخر مزامنة بنجاح")
        except Exception as e:
            logger.error(f"خطأ في حفظ سجل آخر مزامنة: {str(e)}")
    
    def sync_all_tables(self):
        """مزامنة جميع الجداول المحددة في التكوين"""
        logger.info("بدء مزامنة جميع الجداول...")
        
        for table_name, table_config in self.sync_tables.items():
            try:
                logger.info(f"مزامنة جدول {table_name}...")
                
                direction = table_config.get('direction', 'bidirectional')
                
                if direction in ['erp_to_ai', 'bidirectional']:
                    self.sync_table_from_erp_to_ai(table_name)
                
                if direction in ['ai_to_erp', 'bidirectional']:
                    self.sync_table_from_ai_to_erp(table_name)
                
                # تحديث وقت آخر مزامنة
                self.last_sync[table_name] = datetime.now().isoformat()
                
                logger.info(f"تمت مزامنة جدول {table_name} بنجاح")
            except Exception as e:
                logger.error(f"خطأ في مزامنة جدول {table_name}: {str(e)}")
        
        # حفظ سجل آخر مزامنة
        self._save_last_sync()
        
        logger.info("اكتملت مزامنة جميع الجداول")
    
    def sync_table_from_erp_to_ai(self, table_name):
        """
        مزامنة جدول من نظام ERP إلى نظام الذكاء الاصطناعي
        
        المعلمات:
            table_name (str): اسم الجدول في التكوين
        """
        if table_name not in self.sync_tables:
            raise ValueError(f"الجدول {table_name} غير موجود في التكوين")
        
        table_config = self.sync_tables[table_name]
        erp_table = table_config['erp_table']
        ai_table = table_config['ai_table']
        primary_key = table_config['primary_key']
        fields_mapping = table_config['fields_mapping']
        
        # تحديد وقت آخر مزامنة
        last_sync_time = self.last_sync.get(table_name, None)
        
        # استعلام البيانات من نظام ERP
        query = f"SELECT * FROM {erp_table}"
        if last_sync_time:
            query += f" WHERE updated_at >= '{last_sync_time}'"
        
        try:
            # قراءة البيانات من نظام ERP
            erp_data = pd.read_sql(query, self.erp_engine)
            
            if erp_data.empty:
                logger.info(f"لا توجد بيانات جديدة في جدول {erp_table} لمزامنتها")
                return
            
            # إعادة تسمية الأعمدة وفقاً لتعيين الحقول
            erp_data_mapped = erp_data.rename(columns={v: k for k, v in fields_mapping.items()})
            
            # اختيار الأعمدة المطلوبة فقط
            columns_to_sync = list(fields_mapping.keys())
            erp_data_mapped = erp_data_mapped[columns_to_sync]
            
            # مزامنة البيانات مع نظام الذكاء الاصطناعي
            for _, row in erp_data_mapped.iterrows():
                # التحقق مما إذا كان السجل موجوداً بالفعل في نظام الذكاء الاصطناعي
                pk_value = row[primary_key]
                check_query = f"SELECT COUNT(*) FROM {ai_table} WHERE {primary_key} = {pk_value}"
                
                with self.ai_engine.connect() as conn:
                    result = conn.execute(text(check_query)).scalar()
                    
                    if result > 0:
                        # تحديث السجل الموجود
                        update_parts = []
                        params = {}
                        
                        for col in columns_to_sync:
                            if col != primary_key:
                                update_parts.append(f"{col} = :{col}")
                                params[col] = row[col]
                        
                        params[primary_key] = pk_value
                        
                        update_query = f"UPDATE {ai_table} SET {', '.join(update_parts)} WHERE {primary_key} = :{primary_key}"
                        conn.execute(text(update_query), params)
                        logger.debug(f"تم تحديث السجل {pk_value} في جدول {ai_table}")
                    else:
                        # إدراج سجل جديد
                        columns = ', '.join(columns_to_sync)
                        placeholders = ', '.join([f":{col}" for col in columns_to_sync])
                        
                        params = {col: row[col] for col in columns_to_sync}
                        
                        insert_query = f"INSERT INTO {ai_table} ({columns}) VALUES ({placeholders})"
                        conn.execute(text(insert_query), params)
                        logger.debug(f"تم إدراج سجل جديد {pk_value} في جدول {ai_table}")
                    
                    conn.commit()
            
            logger.info(f"تمت مزامنة {len(erp_data)} سجل من {erp_table} إلى {ai_table}")
        
        except Exception as e:
            logger.error(f"خطأ في مزامنة جدول {erp_table} إلى {ai_table}: {str(e)}")
            raise
    
    def sync_table_from_ai_to_erp(self, table_name):
        """
        مزامنة جدول من نظام الذكاء الاصطناعي إلى نظام ERP
        
        المعلمات:
            table_name (str): اسم الجدول في التكوين
        """
        if table_name not in self.sync_tables:
            raise ValueError(f"الجدول {table_name} غير موجود في التكوين")
        
        table_config = self.sync_tables[table_name]
        erp_table = table_config['erp_table']
        ai_table = table_config['ai_table']
        primary_key = table_config['primary_key']
        fields_mapping = table_config['fields_mapping']
        
        # تحديد وقت آخر مزامنة
        last_sync_time = self.last_sync.get(table_name, None)
        
        # استعلام البيانات من نظام الذكاء الاصطناعي
        query = f"SELECT * FROM {ai_table}"
        if last_sync_time:
            query += f" WHERE updated_at >= '{last_sync_time}'"
        
        try:
            # قراءة البيانات من نظام الذكاء الاصطناعي
            ai_data = pd.read_sql(query, self.ai_engine)
            
            if ai_data.empty:
                logger.info(f"لا توجد بيانات جديدة في جدول {ai_table} لمزامنتها")
                return
            
            # إعادة تسمية الأعمدة وفقاً لتعيين الحقول
            ai_data_mapped = ai_data.rename(columns={k: v for k, v in fields_mapping.items()})
            
            # اختيار الأعمدة المطلوبة فقط
            columns_to_sync = [fields_mapping[k] for k in fields_mapping.keys()]
            ai_data_mapped = ai_data_mapped[columns_to_sync]
            
            # مزامنة البيانات مع نظام ERP
            for _, row in ai_data_mapped.iterrows():
                # التحقق مما إذا كان السجل موجوداً بالفعل في نظام ERP
                pk_field = fields_mapping[primary_key]
                pk_value = row[pk_field]
                check_query = f"SELECT COUNT(*) FROM {erp_table} WHERE {pk_field} = {pk_value}"
                
                with self.erp_engine.connect() as conn:
                    result = conn.execute(text(check_query)).scalar()
                    
                    if result > 0:
                        # تحديث السجل الموجود
                        update_parts = []
                        params = {}
                        
                        for ai_col, erp_col in fields_mapping.items():
                            if ai_col != primary_key:
                                update_parts.append(f"{erp_col} = :{erp_col}")
                                params[erp_col] = row[erp_col]
                        
                        params[pk_field] = pk_value
                        
                        update_query = f"UPDATE {erp_table} SET {', '.join(update_parts)} WHERE {pk_field} = :{pk_field}"
                        conn.execute(text(update_query), params)
                        logger.debug(f"تم تحديث السجل {pk_value} في جدول {erp_table}")
                    else:
                        # إدراج سجل جديد
                        columns = ', '.join(columns_to_sync)
                        placeholders = ', '.join([f":{col}" for col in columns_to_sync])
                        
                        params = {col: row[col] for col in columns_to_sync}
                        
                        insert_query = f"INSERT INTO {erp_table} ({columns}) VALUES ({placeholders})"
                        conn.execute(text(insert_query), params)
                        logger.debug(f"تم إدراج سجل جديد {pk_value} في جدول {erp_table}")
                    
                    conn.commit()
            
            logger.info(f"تمت مزامنة {len(ai_data)} سجل من {ai_table} إلى {erp_table}")
        
        except Exception as e:
            logger.error(f"خطأ في مزامنة جدول {ai_table} إلى {erp_table}: {str(e)}")
            raise
    
    def verify_data_integrity(self, table_name):
        """
        التحقق من سلامة البيانات بين النظامين
        
        المعلمات:
            table_name (str): اسم الجدول في التكوين
            
        العوائد:
            dict: نتائج التحقق من سلامة البيانات
        """
        if table_name not in self.sync_tables:
            raise ValueError(f"الجدول {table_name} غير موجود في التكوين")
        
        table_config = self.sync_tables[table_name]
        erp_table = table_config['erp_table']
        ai_table = table_config['ai_table']
        primary_key = table_config['primary_key']
        fields_mapping = table_config['fields_mapping']
        
        try:
            # استعلام البيانات من كلا النظامين
            erp_data = pd.read_sql(f"SELECT * FROM {erp_table}", self.erp_engine)
            ai_data = pd.read_sql(f"SELECT * FROM {ai_table}", self.ai_engine)
            
            # إعادة تسمية الأعمدة في بيانات نظام الذكاء الاصطناعي
            ai_data_mapped = ai_data.rename(columns={k: v for k, v in fields_mapping.items()})
            
            # اختيار الأعمدة المشتركة فقط
            common_columns = [fields_mapping[k] for k in fields_mapping.keys()]
            erp_data = erp_data[common_columns]
            ai_data_mapped = ai_data_mapped[common_columns]
            
            # تحويل الأعمدة إلى مجموعات للمقارنة
            erp_pks = set(erp_data[fields_mapping[primary_key]])
            ai_pks = set(ai_data_mapped[fields_mapping[primary_key]])
            
            # تحديد السجلات المفقودة في كل نظام
            missing_in_ai = erp_pks - ai_pks
            missing_in_erp = ai_pks - erp_pks
            common_pks = erp_pks.intersection(ai_pks)
            
            # التحقق من تطابق البيانات للسجلات المشتركة
            mismatched_records = []
            
            for pk in common_pks:
                erp_record = erp_data[erp_data[fields_mapping[primary_key]] == pk].iloc[0]
                ai_record = ai_data_mapped[ai_data_mapped[fields_mapping[primary_key]] == pk].iloc[0]
                
                # مقارنة القيم في كل عمود
                mismatched_fields = []
                
                for col in common_columns:
                    if erp_record[col] != ai_record[col]:
                        mismatched_fields.append({
                            'field': col,
                            'erp_value': erp_record[col],
                            'ai_value': ai_record[col]
                        })
                
                if mismatched_fields:
                    mismatched_records.append({
                        'primary_key': pk,
                        'mismatched_fields': mismatched_fields
                    })
            
            # إعداد تقرير النتائج
            results = {
                'table_name': table_name,
                'erp_table': erp_table,
                'ai_table': ai_table,
                'total_records_erp': len(erp_data),
                'total_records_ai': len(ai_data),
                'common_records': len(common_pks),
                'missing_in_ai': list(missing_in_ai),
                'missing_in_erp': list(missing_in_erp),
                'mismatched_records': mismatched_records,
                'integrity_score': (len(common_pks) - len(mismatched_records)) / max(len(erp_pks), len(ai_pks)) if max(len(erp_pks), len(ai_pks)) > 0 else 1.0
            }
            
            logger.info(f"تم التحقق من سلامة البيانات لجدول {table_name} (درجة السلامة: {results['integrity_score']:.2f})")
            
            return results
        
        except Exception as e:
            logger.error(f"خطأ في التحقق من سلامة البيانات لجدول {table_name}: {str(e)}")
            raise
    
    def verify_all_tables_integrity(self):
        """
        التحقق من سلامة البيانات لجميع الجداول
        
        العوائد:
            dict: نتائج التحقق من سلامة البيانات لجميع الجداول
        """
        logger.info("بدء التحقق من سلامة البيانات لجميع الجداول...")
        
        results = {}
        
        for table_name in self.sync_tables:
            try:
                table_results = self.verify_data_integrity(table_name)
                results[table_name] = table_results
            except Exception as e:
                logger.error(f"خطأ في التحقق من سلامة البيانات لجدول {table_name}: {str(e)}")
                results[table_name] = {'error': str(e)}
        
        # حساب متوسط درجة السلامة
        integrity_scores = [r['integrity_score'] for r in results.values() if 'integrity_score' in r]
        avg_integrity_score = sum(integrity_scores) / len(integrity_scores) if integrity_scores else 0
        
        results['summary'] = {
            'total_tables': len(self.sync_tables),
            'tables_checked': len(integrity_scores),
            'avg_integrity_score': avg_integrity_score
        }
        
        logger.info(f"اكتمل التحقق من سلامة البيانات لجميع الجداول (متوسط درجة السلامة: {avg_integrity_score:.2f})")
        
        return results
    
    def repair_data_integrity(self, table_name, direction='bidirectional'):
        """
        إصلاح مشاكل سلامة البيانات
        
        المعلمات:
            table_name (str): اسم الجدول في التكوين
            direction (str): اتجاه الإصلاح (erp_to_ai, ai_to_erp, bidirectional)
            
        العوائد:
            dict: نتائج عملية الإصلاح
        """
        if table_name not in self.sync_tables:
            raise ValueError(f"الجدول {table_name} غير موجود في التكوين")
        
        # التحقق من سلامة البيانات أولاً
        integrity_results = self.verify_data_integrity(table_name)
        
        repair_results = {
            'table_name': table_name,
            'direction': direction,
            'records_added_to_ai': 0,
            'records_added_to_erp': 0,
            'records_updated_in_ai': 0,
            'records_updated_in_erp': 0
        }
        
        try:
            # إصلاح السجلات المفقودة
            if direction in ['erp_to_ai', 'bidirectional'] and integrity_results['missing_in_ai']:
                # إضافة السجلات المفقودة في نظام الذكاء الاصطناعي
                for pk in integrity_results['missing_in_ai']:
                    self._add_missing_record(table_name, pk, 'erp_to_ai')
                    repair_results['records_added_to_ai'] += 1
            
            if direction in ['ai_to_erp', 'bidirectional'] and integrity_results['missing_in_erp']:
                # إضافة السجلات المفقودة في نظام ERP
                for pk in integrity_results['missing_in_erp']:
                    self._add_missing_record(table_name, pk, 'ai_to_erp')
                    repair_results['records_added_to_erp'] += 1
            
            # إصلاح السجلات غير المتطابقة
            if integrity_results['mismatched_records']:
                for record in integrity_results['mismatched_records']:
                    pk = record['primary_key']
                    
                    if direction in ['erp_to_ai', 'bidirectional']:
                        # تحديث السجل في نظام الذكاء الاصطناعي
                        self._update_mismatched_record(table_name, pk, 'erp_to_ai')
                        repair_results['records_updated_in_ai'] += 1
                    
                    if direction in ['ai_to_erp', 'bidirectional']:
                        # تحديث السجل في نظام ERP
                        self._update_mismatched_record(table_name, pk, 'ai_to_erp')
                        repair_results['records_updated_in_erp'] += 1
            
            logger.info(f"تم إصلاح مشاكل سلامة البيانات لجدول {table_name} (الاتجاه: {direction})")
            
            # التحقق من سلامة البيانات بعد الإصلاح
            post_repair_integrity = self.verify_data_integrity(table_name)
            repair_results['post_repair_integrity_score'] = post_repair_integrity['integrity_score']
            
            return repair_results
        
        except Exception as e:
            logger.error(f"خطأ في إصلاح مشاكل سلامة البيانات لجدول {table_name}: {str(e)}")
            raise
    
    def _add_missing_record(self, table_name, pk_value, direction):
        """
        إضافة سجل مفقود
        
        المعلمات:
            table_name (str): اسم الجدول في التكوين
            pk_value: قيمة المفتاح الأساسي
            direction (str): اتجاه الإضافة (erp_to_ai, ai_to_erp)
        """
        table_config = self.sync_tables[table_name]
        erp_table = table_config['erp_table']
        ai_table = table_config['ai_table']
        primary_key = table_config['primary_key']
        fields_mapping = table_config['fields_mapping']
        
        if direction == 'erp_to_ai':
            # استعلام البيانات من نظام ERP
            source_engine = self.erp_engine
            source_table = erp_table
            target_engine = self.ai_engine
            target_table = ai_table
            pk_field = fields_mapping[primary_key]
            
            # قراءة السجل من نظام ERP
            query = f"SELECT * FROM {source_table} WHERE {pk_field} = {pk_value}"
            source_data = pd.read_sql(query, source_engine)
            
            if source_data.empty:
                logger.warning(f"لم يتم العثور على السجل {pk_value} في جدول {source_table}")
                return
            
            # إعادة تسمية الأعمدة وفقاً لتعيين الحقول
            source_data_mapped = source_data.rename(columns={v: k for k, v in fields_mapping.items()})
            
            # اختيار الأعمدة المطلوبة فقط
            columns_to_sync = list(fields_mapping.keys())
            source_data_mapped = source_data_mapped[columns_to_sync]
            
            # إدراج السجل في نظام الذكاء الاصطناعي
            row = source_data_mapped.iloc[0]
            
            columns = ', '.join(columns_to_sync)
            placeholders = ', '.join([f":{col}" for col in columns_to_sync])
            
            params = {col: row[col] for col in columns_to_sync}
            
            with target_engine.connect() as conn:
                insert_query = f"INSERT INTO {target_table} ({columns}) VALUES ({placeholders})"
                conn.execute(text(insert_query), params)
                conn.commit()
            
            logger.info(f"تم إضافة السجل {pk_value} إلى جدول {target_table}")
        
        elif direction == 'ai_to_erp':
            # استعلام البيانات من نظام الذكاء الاصطناعي
            source_engine = self.ai_engine
            source_table = ai_table
            target_engine = self.erp_engine
            target_table = erp_table
            
            # قراءة السجل من نظام الذكاء الاصطناعي
            query = f"SELECT * FROM {source_table} WHERE {primary_key} = {pk_value}"
            source_data = pd.read_sql(query, source_engine)
            
            if source_data.empty:
                logger.warning(f"لم يتم العثور على السجل {pk_value} في جدول {source_table}")
                return
            
            # إعادة تسمية الأعمدة وفقاً لتعيين الحقول
            source_data_mapped = source_data.rename(columns={k: v for k, v in fields_mapping.items()})
            
            # اختيار الأعمدة المطلوبة فقط
            columns_to_sync = [fields_mapping[k] for k in fields_mapping.keys()]
            source_data_mapped = source_data_mapped[columns_to_sync]
            
            # إدراج السجل في نظام ERP
            row = source_data_mapped.iloc[0]
            
            columns = ', '.join(columns_to_sync)
            placeholders = ', '.join([f":{col}" for col in columns_to_sync])
            
            params = {col: row[col] for col in columns_to_sync}
            
            with target_engine.connect() as conn:
                insert_query = f"INSERT INTO {target_table} ({columns}) VALUES ({placeholders})"
                conn.execute(text(insert_query), params)
                conn.commit()
            
            logger.info(f"تم إضافة السجل {pk_value} إلى جدول {target_table}")
    
    def _update_mismatched_record(self, table_name, pk_value, direction):
        """
        تحديث سجل غير متطابق
        
        المعلمات:
            table_name (str): اسم الجدول في التكوين
            pk_value: قيمة المفتاح الأساسي
            direction (str): اتجاه التحديث (erp_to_ai, ai_to_erp)
        """
        table_config = self.sync_tables[table_name]
        erp_table = table_config['erp_table']
        ai_table = table_config['ai_table']
        primary_key = table_config['primary_key']
        fields_mapping = table_config['fields_mapping']
        
        if direction == 'erp_to_ai':
            # استعلام البيانات من نظام ERP
            source_engine = self.erp_engine
            source_table = erp_table
            target_engine = self.ai_engine
            target_table = ai_table
            pk_field = fields_mapping[primary_key]
            
            # قراءة السجل من نظام ERP
            query = f"SELECT * FROM {source_table} WHERE {pk_field} = {pk_value}"
            source_data = pd.read_sql(query, source_engine)
            
            if source_data.empty:
                logger.warning(f"لم يتم العثور على السجل {pk_value} في جدول {source_table}")
                return
            
            # إعادة تسمية الأعمدة وفقاً لتعيين الحقول
            source_data_mapped = source_data.rename(columns={v: k for k, v in fields_mapping.items()})
            
            # اختيار الأعمدة المطلوبة فقط
            columns_to_sync = list(fields_mapping.keys())
            source_data_mapped = source_data_mapped[columns_to_sync]
            
            # تحديث السجل في نظام الذكاء الاصطناعي
            row = source_data_mapped.iloc[0]
            
            update_parts = []
            params = {}
            
            for col in columns_to_sync:
                if col != primary_key:
                    update_parts.append(f"{col} = :{col}")
                    params[col] = row[col]
            
            params[primary_key] = pk_value
            
            with target_engine.connect() as conn:
                update_query = f"UPDATE {target_table} SET {', '.join(update_parts)} WHERE {primary_key} = :{primary_key}"
                conn.execute(text(update_query), params)
                conn.commit()
            
            logger.info(f"تم تحديث السجل {pk_value} في جدول {target_table}")
        
        elif direction == 'ai_to_erp':
            # استعلام البيانات من نظام الذكاء الاصطناعي
            source_engine = self.ai_engine
            source_table = ai_table
            target_engine = self.erp_engine
            target_table = erp_table
            
            # قراءة السجل من نظام الذكاء الاصطناعي
            query = f"SELECT * FROM {source_table} WHERE {primary_key} = {pk_value}"
            source_data = pd.read_sql(query, source_engine)
            
            if source_data.empty:
                logger.warning(f"لم يتم العثور على السجل {pk_value} في جدول {source_table}")
                return
            
            # إعادة تسمية الأعمدة وفقاً لتعيين الحقول
            source_data_mapped = source_data.rename(columns={k: v for k, v in fields_mapping.items()})
            
            # اختيار الأعمدة المطلوبة فقط
            columns_to_sync = [fields_mapping[k] for k in fields_mapping.keys()]
            source_data_mapped = source_data_mapped[columns_to_sync]
            
            # تحديث السجل في نظام ERP
            row = source_data_mapped.iloc[0]
            
            update_parts = []
            params = {}
            
            for ai_col, erp_col in fields_mapping.items():
                if ai_col != primary_key:
                    update_parts.append(f"{erp_col} = :{erp_col}")
                    params[erp_col] = row[erp_col]
            
            pk_field = fields_mapping[primary_key]
            params[pk_field] = pk_value
            
            with target_engine.connect() as conn:
                update_query = f"UPDATE {target_table} SET {', '.join(update_parts)} WHERE {pk_field} = :{pk_field}"
                conn.execute(text(update_query), params)
                conn.commit()
            
            logger.info(f"تم تحديث السجل {pk_value} في جدول {target_table}")
    
    def run_scheduled_sync(self):
        """تشغيل المزامنة المجدولة"""
        sync_interval = self.config.get('sync_interval', 3600)  # الفاصل الزمني بالثواني
        
        logger.info(f"بدء المزامنة المجدولة (الفاصل الزمني: {sync_interval} ثانية)")
        
        import time
        import threading
        
        def sync_job():
            while True:
                try:
                    logger.info("تشغيل المزامنة المجدولة...")
                    self.sync_all_tables()
                    logger.info(f"اكتملت المزامنة المجدولة، انتظار {sync_interval} ثانية للمزامنة التالية")
                except Exception as e:
                    logger.error(f"خطأ في المزامنة المجدولة: {str(e)}")
                
                time.sleep(sync_interval)
        
        # تشغيل المزامنة في خيط منفصل
        sync_thread = threading.Thread(target=sync_job, daemon=True)
        sync_thread.start()
        
        return sync_thread
    
    def generate_sync_report(self):
        """
        إنشاء تقرير عن حالة المزامنة
        
        العوائد:
            dict: تقرير المزامنة
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'tables': {},
            'last_sync': self.last_sync,
            'integrity': {}
        }
        
        # التحقق من سلامة البيانات لجميع الجداول
        integrity_results = self.verify_all_tables_integrity()
        report['integrity'] = integrity_results
        
        # جمع إحصائيات عن كل جدول
        for table_name, table_config in self.sync_tables.items():
            erp_table = table_config['erp_table']
            ai_table = table_config['ai_table']
            
            try:
                # عدد السجلات في كل نظام
                erp_count_query = f"SELECT COUNT(*) FROM {erp_table}"
                ai_count_query = f"SELECT COUNT(*) FROM {ai_table}"
                
                with self.erp_engine.connect() as conn:
                    erp_count = conn.execute(text(erp_count_query)).scalar()
                
                with self.ai_engine.connect() as conn:
                    ai_count = conn.execute(text(ai_count_query)).scalar()
                
                # آخر تحديث في كل نظام
                erp_last_update_query = f"SELECT MAX(updated_at) FROM {erp_table}"
                ai_last_update_query = f"SELECT MAX(updated_at) FROM {ai_table}"
                
                try:
                    with self.erp_engine.connect() as conn:
                        erp_last_update = conn.execute(text(erp_last_update_query)).scalar()
                except:
                    erp_last_update = None
                
                try:
                    with self.ai_engine.connect() as conn:
                        ai_last_update = conn.execute(text(ai_last_update_query)).scalar()
                except:
                    ai_last_update = None
                
                report['tables'][table_name] = {
                    'erp_table': erp_table,
                    'ai_table': ai_table,
                    'erp_record_count': erp_count,
                    'ai_record_count': ai_count,
                    'erp_last_update': erp_last_update.isoformat() if erp_last_update else None,
                    'ai_last_update': ai_last_update.isoformat() if ai_last_update else None,
                    'last_sync': self.last_sync.get(table_name, None),
                    'integrity_score': integrity_results.get(table_name, {}).get('integrity_score', None)
                }
            
            except Exception as e:
                logger.error(f"خطأ في جمع إحصائيات الجدول {table_name}: {str(e)}")
                report['tables'][table_name] = {
                    'erp_table': erp_table,
                    'ai_table': ai_table,
                    'error': str(e)
                }
        
        # حساب متوسط درجة السلامة
        integrity_scores = [t['integrity_score'] for t in report['tables'].values() if t.get('integrity_score') is not None]
        avg_integrity_score = sum(integrity_scores) / len(integrity_scores) if integrity_scores else 0
        
        report['summary'] = {
            'total_tables': len(self.sync_tables),
            'tables_checked': len(integrity_scores),
            'avg_integrity_score': avg_integrity_score,
            'last_full_sync': max(self.last_sync.values()) if self.last_sync else None
        }
        
        logger.info("تم إنشاء تقرير المزامنة")
        
        return report
    
    def export_sync_report(self, format='json', output_path=None):
        """
        تصدير تقرير المزامنة
        
        المعلمات:
            format (str): صيغة التقرير (json, csv, html)
            output_path (str): مسار ملف الإخراج (اختياري)
            
        العوائد:
            str: مسار ملف التقرير
        """
        report = self.generate_sync_report()
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"sync_report_{timestamp}.{format}"
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=4)
        
        elif format == 'csv':
            # تحويل التقرير إلى DataFrame
            tables_data = []
            
            for table_name, table_info in report['tables'].items():
                row = {
                    'table_name': table_name,
                    'erp_table': table_info.get('erp_table'),
                    'ai_table': table_info.get('ai_table'),
                    'erp_record_count': table_info.get('erp_record_count'),
                    'ai_record_count': table_info.get('ai_record_count'),
                    'erp_last_update': table_info.get('erp_last_update'),
                    'ai_last_update': table_info.get('ai_last_update'),
                    'last_sync': table_info.get('last_sync'),
                    'integrity_score': table_info.get('integrity_score')
                }
                tables_data.append(row)
            
            df = pd.DataFrame(tables_data)
            df.to_csv(output_path, index=False)
        
        elif format == 'html':
            # إنشاء تقرير HTML
            html_content = f"""
            <!DOCTYPE html>
            <html dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>تقرير مزامنة قواعد البيانات</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; direction: rtl; }}
                    h1, h2 {{ color: #333; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: right; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    .good {{ color: green; }}
                    .warning {{ color: orange; }}
                    .error {{ color: red; }}
                </style>
            </head>
            <body>
                <h1>تقرير مزامنة قواعد البيانات</h1>
                <p>تاريخ التقرير: {report['timestamp']}</p>
                
                <h2>ملخص</h2>
                <table>
                    <tr>
                        <th>عدد الجداول الكلي</th>
                        <td>{report['summary']['total_tables']}</td>
                    </tr>
                    <tr>
                        <th>عدد الجداول التي تم فحصها</th>
                        <td>{report['summary']['tables_checked']}</td>
                    </tr>
                    <tr>
                        <th>متوسط درجة سلامة البيانات</th>
                        <td class="{self._get_integrity_class(report['summary']['avg_integrity_score'])}">
                            {report['summary']['avg_integrity_score']:.2f}
                        </td>
                    </tr>
                    <tr>
                        <th>آخر مزامنة كاملة</th>
                        <td>{report['summary']['last_full_sync'] or 'لم تتم مزامنة بعد'}</td>
                    </tr>
                </table>
                
                <h2>تفاصيل الجداول</h2>
                <table>
                    <tr>
                        <th>اسم الجدول</th>
                        <th>جدول ERP</th>
                        <th>جدول AI</th>
                        <th>عدد سجلات ERP</th>
                        <th>عدد سجلات AI</th>
                        <th>آخر تحديث ERP</th>
                        <th>آخر تحديث AI</th>
                        <th>آخر مزامنة</th>
                        <th>درجة سلامة البيانات</th>
                    </tr>
            """
            
            for table_name, table_info in report['tables'].items():
                integrity_score = table_info.get('integrity_score')
                integrity_class = self._get_integrity_class(integrity_score) if integrity_score is not None else ''
                
                html_content += f"""
                    <tr>
                        <td>{table_name}</td>
                        <td>{table_info.get('erp_table')}</td>
                        <td>{table_info.get('ai_table')}</td>
                        <td>{table_info.get('erp_record_count')}</td>
                        <td>{table_info.get('ai_record_count')}</td>
                        <td>{table_info.get('erp_last_update') or 'غير متوفر'}</td>
                        <td>{table_info.get('ai_last_update') or 'غير متوفر'}</td>
                        <td>{table_info.get('last_sync') or 'لم تتم مزامنة بعد'}</td>
                        <td class="{integrity_class}">{integrity_score:.2f if integrity_score is not None else 'غير متوفر'}</td>
                    </tr>
                """
            
            html_content += """
                </table>
                
                <h2>تفاصيل سلامة البيانات</h2>
            """
            
            for table_name, integrity_info in report['integrity'].items():
                if table_name == 'summary':
                    continue
                
                html_content += f"""
                <h3>جدول {table_name}</h3>
                <table>
                    <tr>
                        <th>عدد السجلات في ERP</th>
                        <td>{integrity_info.get('total_records_erp')}</td>
                    </tr>
                    <tr>
                        <th>عدد السجلات في AI</th>
                        <td>{integrity_info.get('total_records_ai')}</td>
                    </tr>
                    <tr>
                        <th>عدد السجلات المشتركة</th>
                        <td>{integrity_info.get('common_records')}</td>
                    </tr>
                    <tr>
                        <th>عدد السجلات المفقودة في AI</th>
                        <td>{len(integrity_info.get('missing_in_ai', []))}</td>
                    </tr>
                    <tr>
                        <th>عدد السجلات المفقودة في ERP</th>
                        <td>{len(integrity_info.get('missing_in_erp', []))}</td>
                    </tr>
                    <tr>
                        <th>عدد السجلات غير المتطابقة</th>
                        <td>{len(integrity_info.get('mismatched_records', []))}</td>
                    </tr>
                    <tr>
                        <th>درجة سلامة البيانات</th>
                        <td class="{self._get_integrity_class(integrity_info.get('integrity_score'))}">{integrity_info.get('integrity_score', 0):.2f}</td>
                    </tr>
                </table>
                """
                
                if integrity_info.get('missing_in_ai'):
                    html_content += f"""
                    <h4>السجلات المفقودة في AI</h4>
                    <p>{', '.join(map(str, integrity_info.get('missing_in_ai')))}</p>
                    """
                
                if integrity_info.get('missing_in_erp'):
                    html_content += f"""
                    <h4>السجلات المفقودة في ERP</h4>
                    <p>{', '.join(map(str, integrity_info.get('missing_in_erp')))}</p>
                    """
                
                if integrity_info.get('mismatched_records'):
                    html_content += f"""
                    <h4>السجلات غير المتطابقة</h4>
                    <table>
                        <tr>
                            <th>المفتاح الأساسي</th>
                            <th>الحقل</th>
                            <th>قيمة ERP</th>
                            <th>قيمة AI</th>
                        </tr>
                    """
                    
                    for record in integrity_info.get('mismatched_records', []):
                        pk = record['primary_key']
                        
                        for field in record.get('mismatched_fields', []):
                            html_content += f"""
                            <tr>
                                <td>{pk}</td>
                                <td>{field['field']}</td>
                                <td>{field['erp_value']}</td>
                                <td>{field['ai_value']}</td>
                            </tr>
                            """
                    
                    html_content += """
                    </table>
                    """
            
            html_content += """
            </body>
            </html>
            """
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        else:
            raise ValueError(f"صيغة التقرير غير مدعومة: {format}")
        
        logger.info(f"تم تصدير تقرير المزامنة إلى {output_path}")
        
        return output_path
    
    def _get_integrity_class(self, score):
        """
        تحديد فئة درجة سلامة البيانات
        
        المعلمات:
            score (float): درجة سلامة البيانات
            
        العوائد:
            str: فئة درجة سلامة البيانات
        """
        if score is None:
            return ''
        
        if score >= 0.9:
            return 'good'
        elif score >= 0.7:
            return 'warning'
        else:
            return 'error'


# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء كائن تكامل قواعد البيانات
    db_integration = DatabaseIntegration()
    
    # مزامنة جميع الجداول
    db_integration.sync_all_tables()
    
    # التحقق من سلامة البيانات
    integrity_results = db_integration.verify_all_tables_integrity()
    
    # إصلاح مشاكل سلامة البيانات
    for table_name in db_integration.sync_tables:
        db_integration.repair_data_integrity(table_name)
    
    # إنشاء وتصدير تقرير المزامنة
    db_integration.export_sync_report(format='html', output_path='database_sync_report.html')
    
    # تشغيل المزامنة المجدولة
    sync_thread = db_integration.run_scheduled_sync()
    
    # انتظار انتهاء المزامنة المجدولة (لن يحدث في هذا المثال)
    sync_thread.join()
