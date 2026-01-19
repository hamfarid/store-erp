# /home/ubuntu/ai_web_organized/src/modules/data_validation/database_validator.py

"""
وحدة محقق قاعدة البيانات (Database Validator)

هذه الوحدة مسؤولة عن التحقق من صحة البيانات في قاعدة البيانات،
والتأكد من تكامل البيانات والعلاقات بين الجداول.
"""

import json
import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Optional MySQL connector import
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    mysql = None

# Constants
DB_NOT_CONNECTED = 'قاعدة البيانات غير متصلة'

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('database_validator')


class DatabaseValidator:
    """
    فئة محقق قاعدة البيانات المسؤولة عن التحقق من صحة البيانات في قاعدة البيانات.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        تهيئة محقق قاعدة البيانات.

        Args:
            config_path (str, optional): مسار ملف التكوين. إذا لم يتم تحديده، يتم استخدام الإعدادات الافتراضية.
        """
        self.config = self._load_config(config_path)
        self.connection = None
        self.constraints = self._load_constraints()
        logger.info("تم تهيئة محقق قاعدة البيانات بنجاح")

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        تحميل ملف التكوين.

        Args:
            config_path (str, optional): مسار ملف التكوين.

        Returns:
            Dict[str, Any]: بيانات التكوين.
        """
        default_config = {
            "db_type": "sqlite",
            "db_path": "/home/ubuntu/ai_web_organized/src/database/app.db",
            "db_host": "localhost",
            "db_port": 3306,
            "db_name": "app_db",
            "db_user": "app_user",
            "db_password": "app_password",
            "constraints_path": "/home/ubuntu/ai_web_organized/src/modules/data_validation/constraints",
            "log_level": "INFO"}

        if config_path:
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                logger.error(f"خطأ في تحميل ملف التكوين: {str(e)}")
                return default_config
        return default_config

    def _load_constraints(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل قيود قاعدة البيانات.

        Returns:
            Dict[str, Dict[str, Any]]: قيود قاعدة البيانات المحملة.
        """
        constraints = {}
        try:
            # في الإنتاج، يمكن تحميل القيود من ملفات JSON أو قاعدة بيانات
            # هنا نستخدم قيود افتراضية للتوضيح
            constraints = {
                "users": {
                    "primary_key": "id",
                    "unique_keys": ["username", "email"],
                    "foreign_keys": {},
                    "not_null": ["id", "username", "email", "password", "role"],
                    "check_constraints": {
                        "role": ["admin", "user", "guest"]
                    }
                },
                "products": {
                    "primary_key": "id",
                    "unique_keys": ["name"],
                    "foreign_keys": {},
                    "not_null": ["id", "name", "price", "category", "in_stock"],
                    "check_constraints": {
                        "price": {"min": 0}
                    }
                },
                "orders": {
                    "primary_key": "id",
                    "unique_keys": [],
                    "foreign_keys": {
                        "user_id": {"table": "users", "field": "id"}
                    },
                    "not_null": ["id", "user_id", "total", "status"],
                    "check_constraints": {
                        "total": {"min": 0},
                        "status": ["pending", "processing", "shipped", "delivered", "cancelled"]
                    }
                },
                "order_items": {
                    "primary_key": "id",
                    "unique_keys": [],
                    "foreign_keys": {
                        "order_id": {"table": "orders", "field": "id"},
                        "product_id": {"table": "products", "field": "id"}
                    },
                    "not_null": ["id", "order_id", "product_id", "quantity", "price"],
                    "check_constraints": {
                        "quantity": {"min": 1},
                        "price": {"min": 0}
                    }
                }
            }
            logger.info(f"تم تحميل قيود لـ {len(constraints)} جدول بنجاح")
        except Exception as e:
            logger.error(f"خطأ في تحميل قيود قاعدة البيانات: {str(e)}")
        return constraints

    def connect(self) -> bool:
        """
        الاتصال بقاعدة البيانات.

        Returns:
            bool: True إذا تم الاتصال بنجاح، False خلاف ذلك.
        """
        try:
            db_type = self.config.get("db_type", "sqlite")

            if db_type == "sqlite":
                db_path = self.config.get("db_path")
                self.connection = sqlite3.connect(db_path)
                self.connection.row_factory = sqlite3.Row
            elif db_type == "mysql":
                if not MYSQL_AVAILABLE:
                    logger.error(
                        "MySQL connector غير متوفر. يرجى تثبيت mysql-connector-python")
                    return False
                self.connection = mysql.connector.connect(
                    host=self.config.get("db_host"),
                    port=self.config.get("db_port"),
                    database=self.config.get("db_name"),
                    user=self.config.get("db_user"),
                    password=self.config.get("db_password")
                )
            else:
                logger.error(f"نوع قاعدة البيانات غير مدعوم: {db_type}")
                return False

            logger.info(f"تم الاتصال بقاعدة البيانات {db_type} بنجاح")
            return True
        except Exception as e:
            logger.error(f"خطأ في الاتصال بقاعدة البيانات: {str(e)}")
            return False

    def disconnect(self) -> bool:
        """
        قطع الاتصال بقاعدة البيانات.

        Returns:
            bool: True إذا تم قطع الاتصال بنجاح، False خلاف ذلك.
        """
        try:
            if self.connection is not None:
                self.connection.close()
                self.connection = None
                logger.info("تم قطع الاتصال بقاعدة البيانات بنجاح")
                return True
            return False
        except Exception as e:
            logger.error(f"خطأ في قطع الاتصال بقاعدة البيانات: {str(e)}")
            return False

    def get_table_schema(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على مخطط الجدول.

        Args:
            table_name (str): اسم الجدول.

        Returns:
            Optional[Dict[str, Any]]: مخطط الجدول إذا كان موجودًا، None خلاف ذلك.
        """
        if not self.connection:
            logger.error(DB_NOT_CONNECTED)
            return None

        try:
            db_type = self.config.get("db_type", "sqlite")
            cursor = self.connection.cursor()

            if db_type == "sqlite":
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                schema = {
                    "columns": {},
                    "primary_key": None
                }

                for column in columns:
                    column_name = column["name"]
                    column_type = column["type"]
                    not_null = column["notnull"] == 1
                    primary_key = column["pk"] == 1

                    schema["columns"][column_name] = {
                        "type": column_type,
                        "not_null": not_null
                    }

                    if primary_key:
                        schema["primary_key"] = column_name

                # الحصول على المفاتيح الفريدة
                cursor.execute(f"PRAGMA index_list({table_name})")
                indices = cursor.fetchall()

                unique_keys = []
                for index in indices:
                    if index["unique"] == 1:
                        cursor.execute(f"PRAGMA index_info({index['name']})")
                        index_columns = cursor.fetchall()
                        unique_key = [column["name"]
                                      for column in index_columns]
                        if len(unique_key) == 1:
                            unique_keys.append(unique_key[0])
                        else:
                            unique_keys.append(tuple(unique_key))

                schema["unique_keys"] = unique_keys

                # الحصول على المفاتيح الأجنبية
                cursor.execute(f"PRAGMA foreign_key_list({table_name})")
                foreign_keys = cursor.fetchall()

                schema["foreign_keys"] = {}
                for fk in foreign_keys:
                    from_column = fk["from"]
                    to_table = fk["table"]
                    to_column = fk["to"]

                    schema["foreign_keys"][from_column] = {
                        "table": to_table,
                        "column": to_column
                    }

                return schema
            elif db_type == "mysql":
                # الحصول على معلومات الأعمدة
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()

                schema = {
                    "columns": {},
                    "primary_key": None,
                    "unique_keys": [],
                    "foreign_keys": {}
                }

                for column in columns:
                    column_name = column[0]
                    column_type = column[1]
                    not_null = column[2] == "NO"
                    primary_key = column[3] == "PRI"

                    schema["columns"][column_name] = {
                        "type": column_type,
                        "not_null": not_null
                    }

                    if primary_key:
                        schema["primary_key"] = column_name

                    if column[3] == "UNI":
                        schema["unique_keys"].append(column_name)

                # الحصول على المفاتيح الأجنبية
                cursor.execute(f"""
                    SELECT
                        COLUMN_NAME,
                        REFERENCED_TABLE_NAME,
                        REFERENCED_COLUMN_NAME
                    FROM
                        INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                    WHERE
                        TABLE_NAME = '{table_name}'
                        AND REFERENCED_TABLE_NAME IS NOT NULL
                """)
                foreign_keys = cursor.fetchall()

                for fk in foreign_keys:
                    from_column = fk[0]
                    to_table = fk[1]
                    to_column = fk[2]

                    schema["foreign_keys"][from_column] = {
                        "table": to_table,
                        "column": to_column
                    }

                return schema
            else:
                logger.error(f"نوع قاعدة البيانات غير مدعوم: {db_type}")
                return None
        except Exception as e:
            logger.error(f"خطأ في الحصول على مخطط الجدول: {str(e)}")
            return None

    def validate_table_schema(
            self, table_name: str) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        التحقق من صحة مخطط الجدول.

        Args:
            table_name (str): اسم الجدول.

        Returns:
            Tuple[bool, List[Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) وقائمة بالأخطاء.
        """
        if table_name not in self.constraints:
            logger.error(
                f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات")
            return False, [
                {"table": table_name, "error": f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات"}]

        schema = self.get_table_schema(table_name)
        if not schema:
            logger.error(f"لم يتم العثور على مخطط الجدول '{table_name}'")
            return False, [
                {"table": table_name, "error": f"لم يتم العثور على مخطط الجدول '{table_name}'"}]

        constraints = self.constraints[table_name]
        errors = []

        # التحقق من المفتاح الرئيسي
        if constraints.get("primary_key") != schema.get("primary_key"):
            errors.append({
                "table": table_name,
                "error": f"المفتاح الرئيسي غير متطابق. المتوقع: {constraints.get('primary_key')}, الفعلي: {schema.get('primary_key')}"
            })

        # التحقق من المفاتيح الفريدة
        expected_unique_keys = set(constraints.get("unique_keys", []))
        actual_unique_keys = set(schema.get("unique_keys", []))

        if expected_unique_keys != actual_unique_keys:
            errors.append({
                "table": table_name,
                "error": f"المفاتيح الفريدة غير متطابقة. المتوقع: {expected_unique_keys}, الفعلي: {actual_unique_keys}"
            })

        # التحقق من المفاتيح الأجنبية
        expected_foreign_keys = constraints.get("foreign_keys", {})
        actual_foreign_keys = schema.get("foreign_keys", {})

        for fk_column, fk_details in expected_foreign_keys.items():
            if fk_column not in actual_foreign_keys:
                errors.append({
                    "table": table_name,
                    "error": f"المفتاح الأجنبي '{fk_column}' غير موجود"
                })
            else:
                expected_table = fk_details.get("table")
                expected_column = fk_details.get("field")
                actual_table = actual_foreign_keys[fk_column].get("table")
                actual_column = actual_foreign_keys[fk_column].get("column")

                if expected_table != actual_table or expected_column != actual_column:
                    errors.append({
                        "table": table_name,
                        "error": f"المفتاح الأجنبي '{fk_column}' غير متطابق. المتوقع: {expected_table}.{expected_column}, الفعلي: {actual_table}.{actual_column}"
                    })

        # التحقق من الأعمدة غير الفارغة
        expected_not_null = set(constraints.get("not_null", []))
        actual_not_null = {
            column for column,
            details in schema.get(
                "columns",
                {}).items() if details.get("not_null")}

        if expected_not_null != actual_not_null:
            errors.append({
                "table": table_name,
                "error": f"الأعمدة غير الفارغة غير متطابقة. المتوقع: {expected_not_null}, الفعلي: {actual_not_null}"
            })

        is_valid = len(errors) == 0
        return is_valid, errors

    def validate_data_integrity(
            self, table_name: str) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        التحقق من تكامل البيانات في الجدول.

        Args:
            table_name (str): اسم الجدول.

        Returns:
            Tuple[bool, List[Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) وقائمة بالأخطاء.
        """
        if not self.connection:
            logger.error(DB_NOT_CONNECTED)
            return False, [{"table": table_name, "error": DB_NOT_CONNECTED}]

        if table_name not in self.constraints:
            logger.error(
                f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات")
            return False, [
                {"table": table_name, "error": f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات"}]

        constraints = self.constraints[table_name]
        errors = []

        try:
            cursor = self.connection.cursor()

            # التحقق من القيم الفارغة
            for column in constraints.get("not_null", []):
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE {column} IS NULL")
                count = cursor.fetchone()[0]

                if count > 0:
                    errors.append({
                        "table": table_name,
                        "column": column,
                        "error": f"يوجد {count} صف به قيمة فارغة في العمود '{column}'"
                    })

            # التحقق من قيود التحقق
            check_constraints = constraints.get("check_constraints", {})
            for column, check in check_constraints.items():
                if isinstance(check, list):
                    # التحقق من القيم المحددة (enum)
                    placeholders = ", ".join(["?"] * len(check))
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table_name} WHERE {column} NOT IN ({placeholders})",
                        check)
                    count = cursor.fetchone()[0]

                    if count > 0:
                        errors.append({
                            "table": table_name,
                            "column": column,
                            "error": f"يوجد {count} صف به قيمة غير صالحة في العمود '{column}'. القيم المسموح بها: {check}"
                        })
                elif isinstance(check, dict):
                    # التحقق من القيم الرقمية
                    if "min" in check:
                        cursor.execute(
                            f"SELECT COUNT(*) FROM {table_name} WHERE {column} < ?", (check["min"],))
                        count = cursor.fetchone()[0]

                        if count > 0:
                            errors.append({
                                "table": table_name,
                                "column": column,
                                "error": f"يوجد {count} صف به قيمة أقل من {check['min']} في العمود '{column}'"
                            })

                    if "max" in check:
                        cursor.execute(
                            f"SELECT COUNT(*) FROM {table_name} WHERE {column} > ?", (check["max"],))
                        count = cursor.fetchone()[0]

                        if count > 0:
                            errors.append({
                                "table": table_name,
                                "column": column,
                                "error": f"يوجد {count} صف به قيمة أكبر من {check['max']} في العمود '{column}'"
                            })

            # التحقق من تكامل المفاتيح الأجنبية
            foreign_keys = constraints.get("foreign_keys", {})
            for column, fk in foreign_keys.items():
                ref_table = fk.get("table")
                ref_column = fk.get("field")

                cursor.execute(f"""
                    SELECT COUNT(*)
                    FROM {table_name} t
                    LEFT JOIN {ref_table} r ON t.{column} = r.{ref_column}
                    WHERE t.{column} IS NOT NULL AND r.{ref_column} IS NULL
                """)
                count = cursor.fetchone()[0]

                if count > 0:
                    errors.append({
                        "table": table_name,
                        "column": column,
                        "error": f"يوجد {count} صف به قيمة غير موجودة في الجدول المرجعي '{ref_table}.{ref_column}'"
                    })

            is_valid = len(errors) == 0
            return is_valid, errors
        except Exception as e:
            logger.error(f"خطأ في التحقق من تكامل البيانات: {str(e)}")
            return False, [
                {"table": table_name, "error": f"خطأ في التحقق من تكامل البيانات: {str(e)}"}]

    def validate_all_tables(
            self) -> Dict[str, Tuple[bool, List[Dict[str, Any]]]]:
        """
        التحقق من صحة جميع الجداول.

        Returns:
            Dict[str, Tuple[bool, List[Dict[str, Any]]]]: نتائج التحقق لكل جدول.
        """
        results = {}

        for table_name in self.constraints.keys():
            # التحقق من صحة مخطط الجدول
            schema_valid, schema_errors = self.validate_table_schema(
                table_name)

            # التحقق من تكامل البيانات
            data_valid, data_errors = self.validate_data_integrity(table_name)

            is_valid = schema_valid and data_valid
            errors = schema_errors + data_errors

            results[table_name] = (is_valid, errors)

        return results

    def repair_data_integrity(
            self, table_name: str, auto_fix: bool = False) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        إصلاح مشكلات تكامل البيانات في الجدول.

        Args:
            table_name (str): اسم الجدول.
            auto_fix (bool, optional): ما إذا كان يجب إصلاح المشكلات تلقائيًا. الافتراضي هو False.

        Returns:
            Tuple[bool, List[Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) وقائمة بالإجراءات المتخذة.
        """
        if not self.connection:
            logger.error(DB_NOT_CONNECTED)
            return False, [{"table": table_name, "error": DB_NOT_CONNECTED}]

        if table_name not in self.constraints:
            logger.error(
                f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات")
            return False, [
                {"table": table_name, "error": f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات"}]

        # التحقق من تكامل البيانات أولاً
        is_valid, errors = self.validate_data_integrity(table_name)

        if is_valid:
            logger.info(
                f"لا توجد مشكلات في تكامل البيانات في الجدول '{table_name}'")
            return True, []

        if not auto_fix:
            logger.info(
                f"تم العثور على {len(errors)} مشكلة في تكامل البيانات في الجدول '{table_name}'، لكن لم يتم تفعيل الإصلاح التلقائي")
            return False, errors

        # إصلاح المشكلات
        actions = []
        constraints = self.constraints[table_name]

        try:
            cursor = self.connection.cursor()

            # إصلاح القيم الفارغة
            for column in constraints.get("not_null", []):
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE {column} IS NULL")
                count = cursor.fetchone()[0]

                if count > 0:
                    # تحديد القيمة الافتراضية بناءً على نوع العمود
                    schema = self.get_table_schema(table_name)
                    column_type = schema["columns"][column]["type"].lower()

                    default_value = None
                    if "int" in column_type:
                        default_value = 0
                    elif "float" in column_type or "double" in column_type or "decimal" in column_type:
                        default_value = 0.0
                    elif "char" in column_type or "text" in column_type:
                        default_value = ""
                    elif "date" in column_type:
                        default_value = datetime.now().strftime("%Y-%m-%d")
                    elif "time" in column_type:
                        default_value = datetime.now().strftime("%H:%M:%S")
                    elif "datetime" in column_type:
                        default_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    elif "bool" in column_type:
                        default_value = False

                    if default_value is not None:
                        cursor.execute(
                            f"UPDATE {table_name} SET {column} = ? WHERE {column} IS NULL", (default_value,))
                        self.connection.commit()

                        actions.append({
                            "table": table_name,
                            "column": column,
                            "action": f"تم تحديث {count} صف بقيمة افتراضية '{default_value}' في العمود '{column}'"
                        })

            # إصلاح قيود التحقق
            check_constraints = constraints.get("check_constraints", {})
            for column, check in check_constraints.items():
                if isinstance(check, list) and len(check) > 0:
                    # إصلاح القيم المحددة (enum)
                    default_value = check[0]
                    placeholders = ", ".join(["?"] * len(check))

                    cursor.execute(
                        f"SELECT id FROM {table_name} WHERE {column} NOT IN ({placeholders})", check)
                    invalid_ids = [row[0] for row in cursor.fetchall()]

                    if invalid_ids:
                        id_placeholders = ", ".join(["?"] * len(invalid_ids))
                        cursor.execute(
                            f"UPDATE {table_name} SET {column} = ? WHERE id IN ({id_placeholders})",
                            [default_value] + invalid_ids)
                        self.connection.commit()

                        actions.append({
                            "table": table_name,
                            "column": column,
                            "action": f"تم تحديث {len(invalid_ids)} صف بقيمة افتراضية '{default_value}' في العمود '{column}'"
                        })
                elif isinstance(check, dict):
                    # إصلاح القيم الرقمية
                    if "min" in check:
                        min_value = check["min"]
                        cursor.execute(
                            f"SELECT id FROM {table_name} WHERE {column} < ?", (min_value,))
                        invalid_ids = [row[0] for row in cursor.fetchall()]

                        if invalid_ids:
                            id_placeholders = ", ".join(
                                ["?"] * len(invalid_ids))
                            cursor.execute(
                                f"UPDATE {table_name} SET {column} = ? WHERE id IN ({id_placeholders})",
                                [min_value] + invalid_ids)
                            self.connection.commit()

                            actions.append({
                                "table": table_name,
                                "column": column,
                                "action": f"تم تحديث {len(invalid_ids)} صف بقيمة الحد الأدنى '{min_value}' في العمود '{column}'"
                            })

                    if "max" in check:
                        max_value = check["max"]
                        cursor.execute(
                            f"SELECT id FROM {table_name} WHERE {column} > ?", (max_value,))
                        invalid_ids = [row[0] for row in cursor.fetchall()]

                        if invalid_ids:
                            id_placeholders = ", ".join(
                                ["?"] * len(invalid_ids))
                            cursor.execute(
                                f"UPDATE {table_name} SET {column} = ? WHERE id IN ({id_placeholders})",
                                [max_value] + invalid_ids)
                            self.connection.commit()

                            actions.append({
                                "table": table_name,
                                "column": column,
                                "action": f"تم تحديث {len(invalid_ids)} صف بقيمة الحد الأقصى '{max_value}' في العمود '{column}'"
                            })

            # إصلاح تكامل المفاتيح الأجنبية
            foreign_keys = constraints.get("foreign_keys", {})
            for column, fk in foreign_keys.items():
                ref_table = fk.get("table")
                ref_column = fk.get("field")

                cursor.execute(f"""
                    SELECT t.id
                    FROM {table_name} t
                    LEFT JOIN {ref_table} r ON t.{column} = r.{ref_column}
                    WHERE t.{column} IS NOT NULL AND r.{ref_column} IS NULL
                """)
                invalid_ids = [row[0] for row in cursor.fetchall()]

                if invalid_ids:
                    # الحصول على قيمة صالحة من الجدول المرجعي
                    cursor.execute(
                        f"SELECT {ref_column} FROM {ref_table} LIMIT 1")
                    result = cursor.fetchone()

                    if result:
                        valid_value = result[0]
                        id_placeholders = ", ".join(["?"] * len(invalid_ids))
                        cursor.execute(
                            f"UPDATE {table_name} SET {column} = ? WHERE id IN ({id_placeholders})",
                            [valid_value] + invalid_ids)
                        self.connection.commit()

                        actions.append({
                            "table": table_name,
                            "column": column,
                            "action": f"تم تحديث {len(invalid_ids)} صف بقيمة صالحة '{valid_value}' في العمود '{column}'"
                        })
                    else:
                        # إذا لم يكن هناك قيمة صالحة، يتم تعيين القيمة إلى NULL
                        id_placeholders = ", ".join(["?"] * len(invalid_ids))
                        cursor.execute(
                            f"UPDATE {table_name} SET {column} = NULL WHERE id IN ({id_placeholders})",
                            invalid_ids)
                        self.connection.commit()

                        actions.append({
                            "table": table_name,
                            "column": column,
                            "action": f"تم تحديث {len(invalid_ids)} صف بقيمة NULL في العمود '{column}'"
                        })

            # التحقق مرة أخرى بعد الإصلاح
            is_valid, remaining_errors = self.validate_data_integrity(
                table_name)

            if is_valid:
                logger.info(
                    f"تم إصلاح جميع مشكلات تكامل البيانات في الجدول '{table_name}'")
                return True, actions
            else:
                logger.warning(
                    f"تم إصلاح بعض مشكلات تكامل البيانات في الجدول '{table_name}'، لكن لا تزال هناك {len(remaining_errors)} مشكلة")
                return False, actions + \
                    [{"table": table_name, "error": "مشكلات متبقية", "details": remaining_errors}]
        except Exception as e:
            logger.error(f"خطأ في إصلاح تكامل البيانات: {str(e)}")
            return False, [{"table": table_name,
                            "error": f"خطأ في إصلاح تكامل البيانات: {str(e)}"}]

    def add_constraint(
            self,
            table_name: str,
            constraint_type: str,
            constraint_details: Any) -> bool:
        """
        إضافة قيد جديد.

        Args:
            table_name (str): اسم الجدول.
            constraint_type (str): نوع القيد (primary_key, unique_keys, foreign_keys, not_null, check_constraints).
            constraint_details (Any): تفاصيل القيد.

        Returns:
            bool: True إذا تمت الإضافة بنجاح، False خلاف ذلك.
        """
        if table_name not in self.constraints:
            self.constraints[table_name] = {
                "primary_key": None,
                "unique_keys": [],
                "foreign_keys": {},
                "not_null": [],
                "check_constraints": {}
            }

        try:
            if constraint_type == "primary_key":
                self.constraints[table_name]["primary_key"] = constraint_details
            elif constraint_type == "unique_keys":
                if isinstance(constraint_details, list):
                    self.constraints[table_name]["unique_keys"] = constraint_details
                else:
                    self.constraints[table_name]["unique_keys"].append(
                        constraint_details)
            elif constraint_type == "foreign_keys":
                if isinstance(constraint_details, dict):
                    self.constraints[table_name]["foreign_keys"].update(
                        constraint_details)
                else:
                    logger.error("تفاصيل المفتاح الأجنبي يجب أن تكون قاموسًا")
                    return False
            elif constraint_type == "not_null":
                if isinstance(constraint_details, list):
                    self.constraints[table_name]["not_null"] = constraint_details
                else:
                    self.constraints[table_name]["not_null"].append(
                        constraint_details)
            elif constraint_type == "check_constraints":
                if isinstance(constraint_details, dict):
                    self.constraints[table_name]["check_constraints"].update(
                        constraint_details)
                else:
                    logger.error("تفاصيل قيد التحقق يجب أن تكون قاموسًا")
                    return False
            else:
                logger.error(f"نوع القيد غير معروف: {constraint_type}")
                return False

            logger.info(
                f"تمت إضافة القيد '{constraint_type}' للجدول '{table_name}' بنجاح")
            return True
        except Exception as e:
            logger.error(f"خطأ في إضافة القيد: {str(e)}")
            return False

    def remove_constraint(
            self,
            table_name: str,
            constraint_type: str,
            constraint_key: Optional[str] = None) -> bool:
        """
        إزالة قيد.

        Args:
            table_name (str): اسم الجدول.
            constraint_type (str): نوع القيد (primary_key, unique_keys, foreign_keys, not_null, check_constraints).
            constraint_key (str, optional): مفتاح القيد (للمفاتيح الأجنبية وقيود التحقق).

        Returns:
            bool: True إذا تمت الإزالة بنجاح، False خلاف ذلك.
        """
        if table_name not in self.constraints:
            logger.error(
                f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات")
            return False

        try:
            if constraint_type == "primary_key":
                self.constraints[table_name]["primary_key"] = None
            elif constraint_type == "unique_keys":
                if constraint_key:
                    if constraint_key in self.constraints[table_name]["unique_keys"]:
                        self.constraints[table_name]["unique_keys"].remove(
                            constraint_key)
                    else:
                        logger.warning(
                            f"المفتاح الفريد '{constraint_key}' غير موجود في الجدول '{table_name}'")
                else:
                    self.constraints[table_name]["unique_keys"] = []
            elif constraint_type == "foreign_keys":
                if constraint_key:
                    if constraint_key in self.constraints[table_name]["foreign_keys"]:
                        del self.constraints[table_name]["foreign_keys"][constraint_key]
                    else:
                        logger.warning(
                            f"المفتاح الأجنبي '{constraint_key}' غير موجود في الجدول '{table_name}'")
                else:
                    self.constraints[table_name]["foreign_keys"] = {}
            elif constraint_type == "not_null":
                if constraint_key:
                    if constraint_key in self.constraints[table_name]["not_null"]:
                        self.constraints[table_name]["not_null"].remove(
                            constraint_key)
                    else:
                        logger.warning(
                            f"قيد عدم الفراغ '{constraint_key}' غير موجود في الجدول '{table_name}'")
                else:
                    self.constraints[table_name]["not_null"] = []
            elif constraint_type == "check_constraints":
                if constraint_key:
                    if constraint_key in self.constraints[table_name]["check_constraints"]:
                        del self.constraints[table_name]["check_constraints"][constraint_key]
                    else:
                        logger.warning(
                            f"قيد التحقق '{constraint_key}' غير موجود في الجدول '{table_name}'")
                else:
                    self.constraints[table_name]["check_constraints"] = {}
            else:
                logger.error(f"نوع القيد غير معروف: {constraint_type}")
                return False

            logger.info(
                f"تمت إزالة القيد '{constraint_type}' من الجدول '{table_name}' بنجاح")
            return True
        except Exception as e:
            logger.error(f"خطأ في إزالة القيد: {str(e)}")
            return False

    def get_constraints(
            self, table_name: Optional[str] = None) -> Dict[str, Any]:
        """
        الحصول على قيود قاعدة البيانات.

        Args:
            table_name (str, optional): اسم الجدول. إذا لم يتم تحديده، يتم إرجاع جميع القيود.

        Returns:
            Dict[str, Any]: قيود قاعدة البيانات.
        """
        if table_name:
            if table_name not in self.constraints:
                logger.warning(
                    f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات")
                return {}
            return self.constraints[table_name]
        return self.constraints


# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء كائن محقق قاعدة البيانات
    validator = DatabaseValidator()

    # الاتصال بقاعدة البيانات
    if validator.connect():
        # التحقق من صحة مخطط الجدول
        is_valid, errors = validator.validate_table_schema("users")

        if is_valid:
            print("مخطط الجدول صحيح")
        else:
            print("مخطط الجدول غير صحيح:")
            for error in errors:
                print(f"- {error['error']}")

        # التحقق من تكامل البيانات
        is_valid, errors = validator.validate_data_integrity("users")

        if is_valid:
            print("تكامل البيانات صحيح")
        else:
            print("تكامل البيانات غير صحيح:")
            for error in errors:
                print(f"- {error['error']}")

        # قطع الاتصال بقاعدة البيانات
        validator.disconnect()
