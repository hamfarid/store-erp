#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة ترقية وإصدارات قواعد البيانات
يوفر آليات لترقية هيكل قواعد البيانات وإدارة الإصدارات
"""

import os
import json
import logging
import datetime
import sqlite3
import re
import hashlib
from pathlib import Path
import yaml
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class DatabaseMigrationManager:
    """مدير ترقية وإصدارات قواعد البيانات"""
    
    def __init__(self, db_manager, migrations_dir=None):
        """تهيئة مدير الترقية"""
        self.logger = logging.getLogger(__name__)
        self.db_manager = db_manager
        self.migrations_dir = migrations_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'migrations')
        
        # إنشاء مجلد الترقيات إذا لم يكن موجودًا
        os.makedirs(self.migrations_dir, exist_ok=True)
        
        # إنشاء مجلدات لكل قاعدة بيانات
        for db_name in ['operational', 'employee_training', 'system_training', 'backup']:
            os.makedirs(os.path.join(self.migrations_dir, db_name), exist_ok=True)
        
        # التأكد من وجود جدول الترقيات في كل قاعدة بيانات
        self._ensure_migration_tables()
    
    def _ensure_migration_tables(self):
        """التأكد من وجود جدول الترقيات في كل قاعدة بيانات"""
        for db_name in ['operational', 'employee_training', 'system_training', 'backup']:
            try:
                # إنشاء جدول الترقيات إذا لم يكن موجودًا
                self.db_manager.execute(db_name, '''
                    CREATE TABLE IF NOT EXISTS migrations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        version TEXT NOT NULL,
                        name TEXT NOT NULL,
                        applied_at TIMESTAMP NOT NULL,
                        checksum TEXT NOT NULL,
                        success INTEGER NOT NULL,
                        error_message TEXT
                    )
                ''')
                
                self.logger.info(f"تم التأكد من وجود جدول الترقيات في قاعدة البيانات {db_name}")
            except Exception as e:
                self.logger.error(f"خطأ في إنشاء جدول الترقيات في قاعدة البيانات {db_name}: {e}")
                raise
    
    def _get_applied_migrations(self, db_name):
        """الحصول على قائمة الترقيات المطبقة"""
        try:
            migrations = self.db_manager.fetch_all(db_name, 'SELECT version, name, applied_at, checksum, success FROM migrations ORDER BY version')
            return {migration[0]: {'name': migration[1], 'applied_at': migration[2], 'checksum': migration[3], 'success': migration[4]} for migration in migrations}
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قائمة الترقيات المطبقة في قاعدة البيانات {db_name}: {e}")
            return {}
    
    def _get_available_migrations(self, db_name):
        """الحصول على قائمة الترقيات المتاحة"""
        migrations_path = os.path.join(self.migrations_dir, db_name)
        available_migrations = {}
        
        try:
            for filename in os.listdir(migrations_path):
                if filename.endswith('.sql'):
                    match = re.match(r'V(\d+)__(.+)\.sql', filename)
                    if match:
                        version = match.group(1)
                        name = match.group(2).replace('_', ' ')
                        
                        # حساب التشفير للملف
                        file_path = os.path.join(migrations_path, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            checksum = hashlib.md5(content.encode('utf-8')).hexdigest()
                        
                        available_migrations[version] = {
                            'name': name,
                            'path': file_path,
                            'checksum': checksum
                        }
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قائمة الترقيات المتاحة في قاعدة البيانات {db_name}: {e}")
        
        return available_migrations
    
    def _apply_migration(self, db_name, version, migration):
        """تطبيق ترقية محددة"""
        try:
            # قراءة محتوى ملف الترقية
            with open(migration['path'], 'r', encoding='utf-8') as f:
                sql = f.read()
            
            # تنفيذ الترقية
            self.db_manager.execute(db_name, sql)
            
            # تسجيل الترقية
            self.db_manager.insert(db_name, 'migrations', {
                'version': version,
                'name': migration['name'],
                'applied_at': datetime.datetime.now().isoformat(),
                'checksum': migration['checksum'],
                'success': 1,
                'error_message': None
            })
            
            self.logger.info(f"تم تطبيق الترقية {version} ({migration['name']}) في قاعدة البيانات {db_name}")
            return True, None
        except Exception as e:
            error_message = str(e)
            self.logger.error(f"خطأ في تطبيق الترقية {version} ({migration['name']}) في قاعدة البيانات {db_name}: {error_message}")
            
            # تسجيل الترقية مع الخطأ
            self.db_manager.insert(db_name, 'migrations', {
                'version': version,
                'name': migration['name'],
                'applied_at': datetime.datetime.now().isoformat(),
                'checksum': migration['checksum'],
                'success': 0,
                'error_message': error_message
            })
            
            return False, error_message
    
    def migrate(self, db_name=None, target_version=None):
        """تطبيق الترقيات المتاحة"""
        results = {}
        
        # تحديد قواعد البيانات المراد ترقيتها
        db_names = [db_name] if db_name else ['operational', 'employee_training', 'system_training', 'backup']
        
        for current_db in db_names:
            try:
                # الحصول على الترقيات المطبقة والمتاحة
                applied_migrations = self._get_applied_migrations(current_db)
                available_migrations = self._get_available_migrations(current_db)
                
                # تحديد الترقيات التي يجب تطبيقها
                migrations_to_apply = {}
                for version, migration in available_migrations.items():
                    # تخطي الترقيات المطبقة بنجاح
                    if version in applied_migrations and applied_migrations[version]['success']:
                        continue
                    
                    # تخطي الترقيات التي تتجاوز الإصدار المستهدف
                    if target_version and int(version) > int(target_version):
                        continue
                    
                    migrations_to_apply[version] = migration
                
                # ترتيب الترقيات حسب الإصدار
                sorted_versions = sorted(migrations_to_apply.keys(), key=int)
                
                # تطبيق الترقيات
                db_results = []
                for version in sorted_versions:
                    migration = migrations_to_apply[version]
                    success, error = self._apply_migration(current_db, version, migration)
                    db_results.append({
                        'version': version,
                        'name': migration['name'],
                        'success': success,
                        'error': error
                    })
                
                results[current_db] = db_results
                
                self.logger.info(f"تم الانتهاء من ترقية قاعدة البيانات {current_db}")
            except Exception as e:
                self.logger.error(f"خطأ في ترقية قاعدة البيانات {current_db}: {e}")
                results[current_db] = [{'error': str(e)}]
        
        return results
    
    def create_migration(self, db_name, name, sql_content):
        """إنشاء ملف ترقية جديد"""
        try:
            # التأكد من صحة اسم قاعدة البيانات
            if db_name not in ['operational', 'employee_training', 'system_training', 'backup']:
                return False, f"اسم قاعدة البيانات {db_name} غير صالح"
            
            # تنظيف الاسم
            clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
            
            # الحصول على آخر إصدار
            available_migrations = self._get_available_migrations(db_name)
            versions = [int(v) for v in available_migrations.keys()]
            next_version = str(max(versions) + 1 if versions else 1).zfill(3)
            
            # إنشاء اسم الملف
            filename = f"V{next_version}__{clean_name}.sql"
            file_path = os.path.join(self.migrations_dir, db_name, filename)
            
            # كتابة محتوى الملف
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sql_content)
            
            self.logger.info(f"تم إنشاء ملف الترقية {filename} في قاعدة البيانات {db_name}")
            return True, file_path
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء ملف الترقية: {e}")
            return False, str(e)
    
    def get_migration_status(self, db_name=None):
        """الحصول على حالة الترقيات"""
        results = {}
        
        # تحديد قواعد البيانات المراد فحصها
        db_names = [db_name] if db_name else ['operational', 'employee_training', 'system_training', 'backup']
        
        for current_db in db_names:
            try:
                # الحصول على الترقيات المطبقة والمتاحة
                applied_migrations = self._get_applied_migrations(current_db)
                available_migrations = self._get_available_migrations(current_db)
                
                # تجميع المعلومات
                migrations = []
                for version in sorted(set(list(applied_migrations.keys()) + list(available_migrations.keys())), key=int):
                    migration_info = {
                        'version': version,
                        'name': available_migrations.get(version, {}).get('name') or applied_migrations.get(version, {}).get('name'),
                        'status': 'PENDING'
                    }
                    
                    if version in applied_migrations:
                        if applied_migrations[version]['success']:
                            migration_info['status'] = 'SUCCESS'
                            migration_info['applied_at'] = applied_migrations[version]['applied_at']
                        else:
                            migration_info['status'] = 'FAILED'
                            migration_info['applied_at'] = applied_migrations[version]['applied_at']
                    
                    # التحقق من تغيير المحتوى
                    if version in applied_migrations and version in available_migrations:
                        if applied_migrations[version]['checksum'] != available_migrations[version]['checksum']:
                            migration_info['status'] = 'CHANGED'
                    
                    migrations.append(migration_info)
                
                results[current_db] = migrations
            except Exception as e:
                self.logger.error(f"خطأ في الحصول على حالة الترقيات في قاعدة البيانات {current_db}: {e}")
                results[current_db] = [{'error': str(e)}]
        
        return results
    
    def repair(self, db_name, version):
        """إصلاح ترقية فاشلة"""
        try:
            # التحقق من وجود الترقية
            applied_migrations = self._get_applied_migrations(db_name)
            available_migrations = self._get_available_migrations(db_name)
            
            if version not in applied_migrations:
                return False, f"الترقية {version} غير مطبقة في قاعدة البيانات {db_name}"
            
            if version not in available_migrations:
                return False, f"الترقية {version} غير موجودة في مجلد الترقيات"
            
            # حذف الترقية من جدول الترقيات
            self.db_manager.execute(db_name, 'DELETE FROM migrations WHERE version = ?', (version,))
            
            # إعادة تطبيق الترقية
            migration = available_migrations[version]
            success, error = self._apply_migration(db_name, version, migration)
            
            if success:
                self.logger.info(f"تم إصلاح الترقية {version} في قاعدة البيانات {db_name}")
                return True, "تم إصلاح الترقية بنجاح"
            else:
                self.logger.error(f"فشل إصلاح الترقية {version} في قاعدة البيانات {db_name}: {error}")
                return False, f"فشل إصلاح الترقية: {error}"
        except Exception as e:
            self.logger.error(f"خطأ في إصلاح الترقية {version} في قاعدة البيانات {db_name}: {e}")
            return False, str(e)
    
    def generate_schema(self, db_name):
        """توليد مخطط قاعدة البيانات"""
        try:
            # الحصول على اتصال قاعدة البيانات
            conn = self.db_manager.get_connection(db_name)
            
            # الحصول على قائمة الجداول
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = cursor.fetchall()
            
            schema = {}
            
            for table in tables:
                table_name = table[0]
                
                # الحصول على هيكل الجدول
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                table_schema = []
                for column in columns:
                    column_info = {
                        'name': column[1],
                        'type': column[2],
                        'notnull': column[3],
                        'default': column[4],
                        'pk': column[5]
                    }
                    table_schema.append(column_info)
                
                schema[table_name] = table_schema
            
            # إنشاء مجلد المخططات إذا لم يكن موجودًا
            schema_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'schemas')
            os.makedirs(schema_dir, exist_ok=True)
            
            # كتابة المخطط إلى ملف
            schema_path = os.path.join(schema_dir, f"{db_name}_schema.json")
            with open(schema_path, 'w', encoding='utf-8') as f:
                json.dump(schema, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"تم توليد مخطط قاعدة البيانات {db_name} وحفظه في {schema_path}")
            return True, schema_path
        except Exception as e:
            self.logger.error(f"خطأ في توليد مخطط قاعدة البيانات {db_name}: {e}")
            return False, str(e)
    
    def generate_initial_migration(self, db_name):
        """توليد ترقية أولية من قاعدة بيانات موجودة"""
        try:
            # الحصول على اتصال قاعدة البيانات
            conn = self.db_manager.get_connection(db_name)
            
            # الحصول على قائمة الجداول
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = cursor.fetchall()
            
            # توليد SQL لإنشاء الجداول
            sql_statements = []
            
            for table in tables:
                table_name = table[0]
                
                # الحصول على SQL لإنشاء الجدول
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                create_table_sql = cursor.fetchone()[0]
                
                sql_statements.append(create_table_sql + ";")
                
                # الحصول على الفهارس
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='{table_name}'")
                indexes = cursor.fetchall()
                
                for index in indexes:
                    if index[0]:  # بعض الفهارس قد تكون NULL
                        sql_statements.append(index[0] + ";")
            
            # إنشاء ملف الترقية
            sql_content = "\n\n".join(sql_statements)
            success, result = self.create_migration(db_name, "initial_schema", sql_content)
            
            if success:
                self.logger.info(f"تم توليد الترقية الأولية لقاعدة البيانات {db_name}")
                return True, result
            else:
                return False, result
        except Exception as e:
            self.logger.error(f"خطأ في توليد الترقية الأولية لقاعدة البيانات {db_name}: {e}")
            return False, str(e)
    
    def compare_schemas(self, db_name1, db_name2):
        """مقارنة مخططات قاعدتي بيانات"""
        try:
            # توليد مخططات قواعد البيانات
            success1, schema_path1 = self.generate_schema(db_name1)
            success2, schema_path2 = self.generate_schema(db_name2)
            
            if not success1 or not success2:
                return False, "فشل في توليد مخططات قواعد البيانات"
            
            # قراءة المخططات
            with open(schema_path1, 'r', encoding='utf-8') as f:
                schema1 = json.load(f)
            
            with open(schema_path2, 'r', encoding='utf-8') as f:
                schema2 = json.load(f)
            
            # مقارنة المخططات
            differences = {
                'tables_only_in_1': [],
                'tables_only_in_2': [],
                'different_tables': {}
            }
            
            # الجداول الموجودة في المخطط الأول فقط
            for table_name in schema1:
                if table_name not in schema2:
                    differences['tables_only_in_1'].append(table_name)
            
            # الجداول الموجودة في المخطط الثاني فقط
            for table_name in schema2:
                if table_name not in schema1:
                    differences['tables_only_in_2'].append(table_name)
            
            # الجداول المختلفة
            for table_name in schema1:
                if table_name in schema2:
                    table_diff = {
                        'columns_only_in_1': [],
                        'columns_only_in_2': [],
                        'different_columns': {}
                    }
                    
                    # تحويل الأعمدة إلى قاموس للمقارنة السهلة
                    columns1 = {col['name']: col for col in schema1[table_name]}
                    columns2 = {col['name']: col for col in schema2[table_name]}
                    
                    # الأعمدة الموجودة في الجدول الأول فقط
                    for col_name in columns1:
                        if col_name not in columns2:
                            table_diff['columns_only_in_1'].append(col_name)
                    
                    # الأعمدة الموجودة في الجدول الثاني فقط
                    for col_name in columns2:
                        if col_name not in columns1:
                            table_diff['columns_only_in_2'].append(col_name)
                    
                    # الأعمدة المختلفة
                    for col_name in columns1:
                        if col_name in columns2:
                            col1 = columns1[col_name]
                            col2 = columns2[col_name]
                            
                            if col1 != col2:
                                table_diff['different_columns'][col_name] = {
                                    'schema1': col1,
                                    'schema2': col2
                                }
                    
                    # إضافة الاختلافات إذا وجدت
                    if table_diff['columns_only_in_1'] or table_diff['columns_only_in_2'] or table_diff['different_columns']:
                        differences['different_tables'][table_name] = table_diff
            
            # حفظ نتائج المقارنة
            comparison_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'schemas')
            os.makedirs(comparison_dir, exist_ok=True)
            
            comparison_path = os.path.join(comparison_dir, f"comparison_{db_name1}_{db_name2}.json")
            with open(comparison_path, 'w', encoding='utf-8') as f:
                json.dump(differences, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"تم مقارنة مخططات قاعدتي البيانات {db_name1} و {db_name2} وحفظ النتائج في {comparison_path}")
            return True, comparison_path
        except Exception as e:
            self.logger.error(f"خطأ في مقارنة مخططات قاعدتي البيانات: {e}")
            return False, str(e)
    
    def generate_migration_from_comparison(self, db_name, comparison_path):
        """توليد ترقية من نتائج المقارنة"""
        try:
            # قراءة نتائج المقارنة
            with open(comparison_path, 'r', encoding='utf-8') as f:
                differences = json.load(f)
            
            # توليد SQL للترقية
            sql_statements = []
            
            # إنشاء الجداول الجديدة
            for table_name in differences['tables_only_in_2']:
                # الحصول على SQL لإنشاء الجدول من قاعدة البيانات الثانية
                db_name2 = comparison_path.split('_')[-1].split('.')[0]
                conn = self.db_manager.get_connection(db_name2)
                cursor = conn.cursor()
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                create_table_sql = cursor.fetchone()[0]
                
                sql_statements.append(create_table_sql + ";")
            
            # تعديل الجداول الموجودة
            for table_name, table_diff in differences['different_tables'].items():
                # إضافة الأعمدة الجديدة
                for col_name in table_diff['columns_only_in_2']:
                    # الحصول على معلومات العمود من قاعدة البيانات الثانية
                    db_name2 = comparison_path.split('_')[-1].split('.')[0]
                    conn = self.db_manager.get_connection(db_name2)
                    cursor = conn.cursor()
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    for column in columns:
                        if column[1] == col_name:
                            col_type = column[2]
                            col_notnull = "NOT NULL" if column[3] else ""
                            col_default = f"DEFAULT {column[4]}" if column[4] is not None else ""
                            
                            sql_statements.append(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type} {col_notnull} {col_default};")
                            break
            
            # إنشاء ملف الترقية
            sql_content = "\n".join(sql_statements)
            success, result = self.create_migration(db_name, "schema_update", sql_content)
            
            if success:
                self.logger.info(f"تم توليد ترقية لقاعدة البيانات {db_name} من نتائج المقارنة")
                return True, result
            else:
                return False, result
        except Exception as e:
            self.logger.error(f"خطأ في توليد ترقية من نتائج المقارنة: {e}")
            return False, str(e)


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
    
    # إنشاء مدير الترقية
    migration_manager = DatabaseMigrationManager(db_manager)
    
    # توليد ترقية أولية
    success, result = migration_manager.generate_initial_migration('operational')
    print(f"توليد الترقية الأولية: {success}, {result}")
    
    # تطبيق الترقيات
    results = migration_manager.migrate()
    print(f"نتائج تطبيق الترقيات: {results}")
    
    # الحصول على حالة الترقيات
    status = migration_manager.get_migration_status()
    print(f"حالة الترقيات: {status}")
