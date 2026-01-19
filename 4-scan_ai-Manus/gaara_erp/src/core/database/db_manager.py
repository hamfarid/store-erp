#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة إدارة قاعدة البيانات الأساسية لنظام Gaara ERP
"""

import os
import logging
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# إعداد التسجيل
logger = logging.getLogger(__name__)

class DatabaseManager:
    """مدير قاعدة البيانات لنظام Gaara ERP"""
    
    _instance = None
    
    def __new__(cls):
        """تنفيذ نمط Singleton لضمان وجود نسخة واحدة فقط من مدير قاعدة البيانات"""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """تهيئة مدير قاعدة البيانات"""
        if self._initialized:
            return
            
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # إعدادات قاعدة البيانات
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME', 'gaara_erp')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', 'postgres')
        self.min_connections = int(os.getenv('DB_MIN_CONNECTIONS', '1'))
        self.max_connections = int(os.getenv('DB_MAX_CONNECTIONS', '10'))
        
        # إنشاء تجمع الاتصالات
        self._connection_pool = None
        self._create_connection_pool()
        
        self._initialized = True
        logger.info("تم تهيئة مدير قاعدة البيانات بنجاح")
    
    def _create_connection_pool(self):
        """إنشاء تجمع اتصالات قاعدة البيانات"""
        try:
            self._connection_pool = pool.ThreadedConnectionPool(
                self.min_connections,
                self.max_connections,
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            logger.info("تم إنشاء تجمع اتصالات قاعدة البيانات بنجاح")
        except Exception as e:
            logger.error(f"فشل في إنشاء تجمع اتصالات قاعدة البيانات: {str(e)}")
            raise
    
    def get_connection(self):
        """الحصول على اتصال من تجمع الاتصالات"""
        if not self._connection_pool:
            self._create_connection_pool()
        
        try:
            connection = self._connection_pool.getconn()
            return connection
        except Exception as e:
            logger.error(f"فشل في الحصول على اتصال من تجمع الاتصالات: {str(e)}")
            raise
    
    def release_connection(self, connection):
        """إعادة اتصال إلى تجمع الاتصالات"""
        if self._connection_pool:
            self._connection_pool.putconn(connection)
    
    def execute_query(self, query, params=None, fetch=True, dict_cursor=True):
        """تنفيذ استعلام SQL وإرجاع النتائج"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            
            if dict_cursor:
                cursor = connection.cursor(cursor_factory=RealDictCursor)
            else:
                cursor = connection.cursor()
                
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.rowcount
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"فشل في تنفيذ الاستعلام: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.release_connection(connection)
    
    def execute_script(self, script_path):
        """تنفيذ ملف نصي SQL"""
        connection = None
        cursor = None
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            connection = self.get_connection()
            cursor = connection.cursor()
            
            cursor.execute(sql_script)
            connection.commit()
            
            logger.info(f"تم تنفيذ النص البرمجي SQL بنجاح: {script_path}")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"فشل في تنفيذ النص البرمجي SQL: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.release_connection(connection)
    
    def close_all_connections(self):
        """إغلاق جميع الاتصالات في تجمع الاتصالات"""
        if self._connection_pool:
            self._connection_pool.closeall()
            logger.info("تم إغلاق جميع اتصالات قاعدة البيانات")
    
    def create_database(self):
        """إنشاء قاعدة البيانات إذا لم تكن موجودة"""
        # الاتصال بقاعدة بيانات postgres الافتراضية
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname="postgres",
                user=self.db_user,
                password=self.db_password
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # التحقق من وجود قاعدة البيانات
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'")
            exists = cursor.fetchone()
            
            if not exists:
                # إنشاء قاعدة البيانات
                cursor.execute(f"CREATE DATABASE {self.db_name}")
                logger.info(f"تم إنشاء قاعدة البيانات {self.db_name} بنجاح")
            else:
                logger.info(f"قاعدة البيانات {self.db_name} موجودة بالفعل")
                
            return True
        except Exception as e:
            logger.error(f"فشل في إنشاء قاعدة البيانات: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def initialize_database(self, script_path):
        """تهيئة قاعدة البيانات باستخدام النص البرمجي المحدد"""
        try:
            # إنشاء قاعدة البيانات إذا لم تكن موجودة
            self.create_database()
            
            # تنفيذ النص البرمجي لإنشاء الجداول
            self.execute_script(script_path)
            
            logger.info("تم تهيئة قاعدة البيانات بنجاح")
            return True
        except Exception as e:
            logger.error(f"فشل في تهيئة قاعدة البيانات: {str(e)}")
            raise

# نموذج استخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # تهيئة قاعدة البيانات
    db_manager = DatabaseManager()
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'database_init.sql')
    db_manager.initialize_database(script_path)
