# /home/ubuntu/ai_web_organized/src/modules/data_validation/tests/test_validation_system.py

"""
from flask import g
اختبارات نظام التحقق من صحة البيانات

هذا الملف يحتوي على اختبارات شاملة لنظام التحقق من صحة البيانات،
بما في ذلك محقق النموذج، محقق قاعدة البيانات، ومعالج البيانات غير الصحيحة.
"""

import os
import sqlite3
import sys
import tempfile
import unittest

from modules.data_validation.database_validator import DatabaseValidator
from modules.data_validation.invalid_data_handler import InvalidDataHandler
from modules.data_validation.model_validator import ModelValidator

# إضافة المسار إلى وحدات التحقق
sys.path.append('/home/ubuntu/ai_web_organized/src')


class TestModelValidator(unittest.TestCase):
    """
    اختبارات محقق النموذج.
    """

    def setUp(self):
        """
        إعداد بيئة الاختبار.
        """
        self.validator = ModelValidator()

        # إضافة نموذج اختبار إذا لم يكن موجودًا
        if "test_model" not in self.validator.get_all_models():
            self.validator.add_model("test_model", {
                "fields": {
                    "id": {"type": "integer", "required": True},
                    "name": {"type": "string", "required": True, "min_length": 3, "max_length": 50},
                    "email": {"type": "email", "required": True},
                    "age": {"type": "integer", "required": False, "min": 18, "max": 100},
                    "active": {"type": "boolean", "required": True},
                    "role": {"type": "string", "required": True, "enum": ["admin", "user", "guest"]}
                }
            })

    def test_valid_data(self):
        """
        اختبار البيانات الصحيحة.
        """
        data = {
            "id": 1,
            "name": "أحمد محمد",
            "email": "ahmed@example.com",
            "age": 30,
            "active": True,
            "role": "admin"
        }

        is_valid, errors = self.validator.validate_data(data, "test_model")
        self.assertTrue(is_valid, "البيانات الصحيحة يجب أن تمر من التحقق")
        self.assertEqual(
            len(errors),
            0,
            "يجب ألا تكون هناك أخطاء للبيانات الصحيحة")

    def test_missing_required_field(self):
        """
        اختبار حقل مطلوب مفقود.
        """
        data = {
            "id": 1,
            "name": "أحمد محمد",
            "email": "ahmed@example.com",
            "active": True
            # حقل "role" مفقود
        }

        is_valid, errors = self.validator.validate_data(data, "test_model")
        self.assertFalse(
            is_valid,
            "البيانات مع حقل مطلوب مفقود يجب أن تفشل في التحقق")
        self.assertGreater(
            len(errors),
            0,
            "يجب أن تكون هناك أخطاء للبيانات مع حقل مطلوب مفقود")

        # التحقق من وجود خطأ للحقل المفقود
        error_fields = [error["field"] for error in errors]
        self.assertIn(
            "role",
            error_fields,
            "يجب أن يكون هناك خطأ للحقل المفقود 'role'")

    def test_invalid_type(self):
        """
        اختبار نوع غير صحيح.
        """
        data = {
            "id": "1",  # يجب أن يكون رقمًا
            "name": "أحمد محمد",
            "email": "ahmed@example.com",
            "age": "ثلاثون",  # يجب أن يكون رقمًا
            "active": "نعم",  # يجب أن يكون قيمة منطقية
            "role": "admin"
        }

        is_valid, errors = self.validator.validate_data(data, "test_model")
        self.assertFalse(
            is_valid,
            "البيانات مع أنواع غير صحيحة يجب أن تفشل في التحقق")
        self.assertGreater(
            len(errors),
            0,
            "يجب أن تكون هناك أخطاء للبيانات مع أنواع غير صحيحة")

    def test_invalid_value(self):
        """
        اختبار قيمة غير صحيحة.
        """
        data = {
            "id": 1,
            "name": "أ",  # أقل من الحد الأدنى
            "email": "invalid-email",  # بريد إلكتروني غير صالح
            "age": 15,  # أقل من الحد الأدنى
            "active": True,
            "role": "invalid-role"  # قيمة غير موجودة في القائمة
        }

        is_valid, errors = self.validator.validate_data(data, "test_model")
        self.assertFalse(
            is_valid,
            "البيانات مع قيم غير صحيحة يجب أن تفشل في التحقق")
        self.assertGreater(
            len(errors),
            0,
            "يجب أن تكون هناك أخطاء للبيانات مع قيم غير صحيحة")

    def test_unknown_field(self):
        """
        اختبار حقل غير معروف.
        """
        data = {
            "id": 1,
            "name": "أحمد محمد",
            "email": "ahmed@example.com",
            "age": 30,
            "active": True,
            "role": "admin",
            "unknown_field": "قيمة"  # حقل غير موجود في النموذج
        }

        is_valid, errors = self.validator.validate_data(data, "test_model")

        # في الوضع الصارم، يجب أن تفشل البيانات مع حقل غير معروف
        if self.validator.config.get("strict_mode", True):
            self.assertFalse(
                is_valid,
                "البيانات مع حقل غير معروف يجب أن تفشل في التحقق في الوضع الصارم")
            self.assertGreater(
                len(errors),
                0,
                "يجب أن تكون هناك أخطاء للبيانات مع حقل غير معروف في الوضع الصارم")

            # التحقق من وجود خطأ للحقل غير المعروف
            error_fields = [error["field"] for error in errors]
            self.assertIn(
                "unknown_field",
                error_fields,
                "يجب أن يكون هناك خطأ للحقل غير المعروف 'unknown_field'")

    def test_batch_validation(self):
        """
        اختبار التحقق من مجموعة من البيانات.
        """
        data_list = [
            {
                "id": 1,
                "name": "أحمد محمد",
                "email": "ahmed@example.com",
                "age": 30,
                "active": True,
                "role": "admin"
            },
            {
                "id": 2,
                "name": "محمد علي",
                "email": "mohamed@example.com",
                "active": True,
                "role": "user"
            },
            {
                "id": 3,
                "name": "س",  # أقل من الحد الأدنى
                "email": "invalid-email",  # بريد إلكتروني غير صالح
                "age": 15,  # أقل من الحد الأدنى
                "active": True,
                "role": "invalid-role"  # قيمة غير موجودة في القائمة
            }
        ]

        results = self.validator.validate_batch(data_list, "test_model")
        self.assertEqual(
            len(results),
            len(data_list),
            "يجب أن تكون هناك نتيجة لكل عنصر في القائمة")

        # التحقق من النتائج
        self.assertTrue(results[0][0], "العنصر الأول يجب أن يكون صحيحًا")
        self.assertTrue(results[1][0], "العنصر الثاني يجب أن يكون صحيحًا")
        self.assertFalse(results[2][0], "العنصر الثالث يجب أن يكون غير صحيح")
        self.assertGreater(len(results[2][1]), 0,
                           "يجب أن تكون هناك أخطاء للعنصر الثالث")

    def test_model_management(self):
        """
        اختبار إدارة النماذج (إضافة، تحديث، حذف).
        """
        # إضافة نموذج جديد
        new_model = {
            "fields": {
                "id": {"type": "integer", "required": True},
                "title": {"type": "string", "required": True, "min_length": 5, "max_length": 100},
                "content": {"type": "string", "required": True},
                "published": {"type": "boolean", "required": True}
            }
        }

        result = self.validator.add_model("article", new_model)
        self.assertTrue(result, "يجب أن تنجح إضافة النموذج")

        # التحقق من وجود النموذج
        model = self.validator.get_model("article")
        self.assertIsNotNone(model, "يجب أن يكون النموذج موجودًا بعد الإضافة")

        # تحديث النموذج
        updated_model = {
            "fields": {
                "id": {
                    "type": "integer", "required": True}, "title": {
                    "type": "string", "required": True, "min_length": 5, "max_length": 100}, "content": {
                    "type": "string", "required": True}, "published": {
                        "type": "boolean", "required": True}, "category": {
                            "type": "string", "required": False, "enum": [
                                "news", "article", "blog"]}}}

        result = self.validator.update_model("article", updated_model)
        self.assertTrue(result, "يجب أن ينجح تحديث النموذج")

        # التحقق من تحديث النموذج
        model = self.validator.get_model("article")
        self.assertIn(
            "category",
            model["fields"],
            "يجب أن يحتوي النموذج المحدث على الحقل الجديد")

        # حذف النموذج
        result = self.validator.delete_model("article")
        self.assertTrue(result, "يجب أن ينجح حذف النموذج")

        # التحقق من حذف النموذج
        model = self.validator.get_model("article")
        self.assertIsNone(model, "يجب ألا يكون النموذج موجودًا بعد الحذف")


class TestDatabaseValidator(unittest.TestCase):
    """
    اختبارات محقق قاعدة البيانات.
    """

    def setUp(self):
        """
        إعداد بيئة الاختبار.
        """
        # إنشاء قاعدة بيانات مؤقتة للاختبار
        self.db_fd, self.db_path = tempfile.mkstemp()

        # إنشاء محقق قاعدة البيانات مع قاعدة البيانات المؤقتة
        self.validator = DatabaseValidator()
        self.validator.config["db_type"] = "sqlite"
        self.validator.config["db_path"] = self.db_path

        # إنشاء جداول الاختبار
        self._create_test_tables()

    def tearDown(self):
        """
        تنظيف بيئة الاختبار.
        """
        # قطع الاتصال بقاعدة البيانات
        if self.validator.connection:
            self.validator.disconnect()

        # إغلاق وحذف قاعدة البيانات المؤقتة
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _create_test_tables(self):
        """
        إنشاء جداول الاختبار.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # إنشاء جدول المستخدمين
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin', 'user', 'guest')),
                created_at TEXT
            )
        ''')

        # إنشاء جدول المنتجات
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL CHECK (price >= 0),
                category TEXT NOT NULL,
                in_stock INTEGER NOT NULL,
                created_at TEXT
            )
        ''')

        # إنشاء جدول الطلبات
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                total REAL NOT NULL CHECK (total >= 0),
                status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # إنشاء جدول عناصر الطلب
        cursor.execute('''
            CREATE TABLE order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 1),
                price REAL NOT NULL CHECK (price >= 0),
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # إدخال بيانات اختبار
        cursor.execute('''
            INSERT INTO users (id, username, email, password, role, created_at)
            VALUES (1, 'admin', 'admin@example.com', 'password123', 'admin', '2023-01-01 12:00:00')
        ''')

        cursor.execute('''
            INSERT INTO users (id, username, email, password, role, created_at)
            VALUES (2, 'user1', 'user1@example.com', 'password123', 'user', '2023-01-02 12:00:00')
        ''')

        cursor.execute('''
            INSERT INTO products (id, name, price, category, in_stock, created_at)
            VALUES (1, 'Product 1', 10.99, 'Category 1', 1, '2023-01-01 12:00:00')
        ''')

        cursor.execute('''
            INSERT INTO products (id, name, price, category, in_stock, created_at)
            VALUES (2, 'Product 2', 20.99, 'Category 2', 1, '2023-01-02 12:00:00')
        ''')

        cursor.execute('''
            INSERT INTO orders (id, user_id, total, status, created_at)
            VALUES (1, 1, 10.99, 'pending', '2023-01-03 12:00:00')
        ''')

        cursor.execute('''
            INSERT INTO order_items (id, order_id, product_id, quantity, price)
            VALUES (1, 1, 1, 1, 10.99)
        ''')

        conn.commit()
        conn.close()

        # تحديث قيود قاعدة البيانات
        self.validator.constraints = {
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

    def test_connection(self):
        """
        اختبار الاتصال بقاعدة البيانات.
        """
        result = self.validator.connect()
        self.assertTrue(result, "يجب أن ينجح الاتصال بقاعدة البيانات")
        self.assertIsNotNone(
            self.validator.connection,
            "يجب أن يكون هناك اتصال بقاعدة البيانات")

        result = self.validator.disconnect()
        self.assertTrue(result, "يجب أن ينجح قطع الاتصال بقاعدة البيانات")
        self.assertIsNone(
            self.validator.connection,
            "يجب ألا يكون هناك اتصال بقاعدة البيانات بعد قطع الاتصال")

    def test_get_table_schema(self):
        """
        اختبار الحصول على مخطط الجدول.
        """
        self.validator.connect()

        schema = self.validator.get_table_schema("users")
        self.assertIsNotNone(schema, "يجب أن يكون هناك مخطط للجدول")
        self.assertIn(
            "columns",
            schema,
            "يجب أن يحتوي المخطط على معلومات الأعمدة")
        self.assertIn(
            "primary_key",
            schema,
            "يجب أن يحتوي المخطط على معلومات المفتاح الرئيسي")

        # التحقق من وجود الأعمدة المتوقعة
        self.assertIn(
            "id",
            schema["columns"],
            "يجب أن يحتوي المخطط على عمود 'id'")
        self.assertIn(
            "username",
            schema["columns"],
            "يجب أن يحتوي المخطط على عمود 'username'")
        self.assertIn(
            "email",
            schema["columns"],
            "يجب أن يحتوي المخطط على عمود 'email'")
        self.assertIn(
            "password",
            schema["columns"],
            "يجب أن يحتوي المخطط على عمود 'password'")
        self.assertIn(
            "role",
            schema["columns"],
            "يجب أن يحتوي المخطط على عمود 'role'")

        # التحقق من المفتاح الرئيسي
        self.assertEqual(
            schema["primary_key"],
            "id",
            "يجب أن يكون المفتاح الرئيسي هو 'id'")

    def test_validate_table_schema(self):
        """
        اختبار التحقق من صحة مخطط الجدول.
        """
        self.validator.connect()

        # التحقق من صحة مخطط جدول المستخدمين
        is_valid, errors = self.validator.validate_table_schema("users")
        self.assertTrue(is_valid, "يجب أن يكون مخطط جدول المستخدمين صحيحًا")
        self.assertEqual(
            len(errors),
            0,
            "يجب ألا تكون هناك أخطاء في مخطط جدول المستخدمين")

        # تغيير قيود الجدول لإنشاء خطأ
        original_primary_key = self.validator.constraints["users"]["primary_key"]
        self.validator.constraints["users"]["primary_key"] = "non_existent_column"

        # التحقق من صحة مخطط الجدول مع القيود المتغيرة
        is_valid, errors = self.validator.validate_table_schema("users")
        self.assertFalse(
            is_valid,
            "يجب أن يكون مخطط جدول المستخدمين غير صحيح مع القيود المتغيرة")
        self.assertGreater(
            len(errors),
            0,
            "يجب أن تكون هناك أخطاء في مخطط جدول المستخدمين مع القيود المتغيرة")

        # إعادة القيود الأصلية
        self.validator.constraints["users"]["primary_key"] = original_primary_key

    def test_validate_data_integrity(self):
        """
        اختبار التحقق من تكامل البيانات.
        """
        self.validator.connect()

        # التحقق من تكامل بيانات جدول المستخدمين
        is_valid, errors = self.validator.validate_data_integrity("users")
        self.assertTrue(is_valid, "يجب أن تكون بيانات جدول المستخدمين متكاملة")
        self.assertEqual(
            len(errors),
            0,
            "يجب ألا تكون هناك أخطاء في تكامل بيانات جدول المستخدمين")

        # إدخال بيانات غير صحيحة
        cursor = self.validator.connection.cursor()
        cursor.execute('''
            INSERT INTO users (id, username, email, password, role, created_at)
            VALUES (3, 'user2', 'user2@example.com', 'password123', 'invalid_role', '2023-01-03 12:00:00')
        ''')
        self.validator.connection.commit()

        # التحقق من تكامل البيانات مع البيانات غير الصحيحة
        is_valid, errors = self.validator.validate_data_integrity("users")
        self.assertFalse(
            is_valid,
            "يجب أن تكون بيانات جدول المستخدمين غير متكاملة مع البيانات غير الصحيحة")
        self.assertGreater(
            len(errors),
            0,
            "يجب أن تكون هناك أخطاء في تكامل بيانات جدول المستخدمين مع البيانات غير الصحيحة")

    def test_validate_all_tables(self):
        """
        اختبار التحقق من صحة جميع الجداول.
        """
        self.validator.connect()

        # التحقق من صحة جميع الجداول
        results = self.validator.validate_all_tables()
        self.assertIsInstance(results, dict, "يجب أن تكون النتائج قاموسًا")
        self.assertEqual(len(results),
                         len(self.validator.constraints),
                         "يجب أن تكون هناك نتيجة لكل جدول")

        # التحقق من نتائج كل جدول
        for table_name, (is_valid, errors) in results.items():
            self.assertIsInstance(
                is_valid, bool, "يجب أن تكون النتيجة قيمة منطقية")
            self.assertIsInstance(errors, list, "يجب أن تكون الأخطاء قائمة")

    def test_repair_data_integrity(self):
        """
        اختبار إصلاح تكامل البيانات.
        """
        self.validator.connect()

        # إدخال بيانات غير صحيحة
        cursor = self.validator.connection.cursor()
        cursor.execute('''
            INSERT INTO users (id, username, email, password, role, created_at)
            VALUES (4, 'user3', 'user3@example.com', 'password123', 'invalid_role', '2023-01-04 12:00:00')
        ''')
        self.validator.connection.commit()

        # التحقق من تكامل البيانات قبل الإصلاح
        is_valid, errors = self.validator.validate_data_integrity("users")
        self.assertFalse(
            is_valid,
            "يجب أن تكون بيانات جدول المستخدمين غير متكاملة قبل الإصلاح")

        # إصلاح تكامل البيانات
        is_fixed, actions = self.validator.repair_data_integrity(
            "users", auto_fix=True)
        self.assertTrue(is_fixed, "يجب أن ينجح إصلاح تكامل البيانات")
        self.assertGreater(len(actions), 0, "يجب أن تكون هناك إجراءات للإصلاح")

        # التحقق من تكامل البيانات بعد الإصلاح
        is_valid, errors = self.validator.validate_data_integrity("users")
        self.assertTrue(
            is_valid,
            "يجب أن تكون بيانات جدول المستخدمين متكاملة بعد الإصلاح")
        self.assertEqual(
            len(errors),
            0,
            "يجب ألا تكون هناك أخطاء في تكامل بيانات جدول المستخدمين بعد الإصلاح")

    def test_constraint_management(self):
        """
        اختبار إدارة القيود (إضافة، إزالة).
        """
        # إضافة قيد جديد
        result = self.validator.add_constraint("users", "check_constraints", {
                                               "username": {"min_length": 3}})
        self.assertTrue(result, "يجب أن تنجح إضافة القيد")

        # التحقق من إضافة القيد
        constraints = self.validator.get_constraints("users")
        self.assertIn(
            "username",
            constraints["check_constraints"],
            "يجب أن يحتوي القيود على القيد الجديد")

        # إزالة القيد
        result = self.validator.remove_constraint(
            "users", "check_constraints", "username")
        self.assertTrue(result, "يجب أن تنجح إزالة القيد")

        # التحقق من إزالة القيد
        constraints = self.validator.get_constraints("users")
        self.assertNotIn(
            "username",
            constraints["check_constraints"],
            "يجب ألا يحتوي القيود على القيد المحذوف")


class TestInvalidDataHandler(unittest.TestCase):
    """
    اختبارات معالج البيانات غير الصحيحة.
    """

    def setUp(self):
        """
        إعداد بيئة الاختبار.
        """
        self.handler = InvalidDataHandler()

        # إضافة نموذج اختبار إذا لم يكن موجودًا
        if "test_model" not in self.handler.model_validator.get_all_models():
            self.handler.model_validator.add_model("test_model", {
                "fields": {
                    "id": {"type": "integer", "required": True},
                    "name": {"type": "string", "required": True, "min_length": 3, "max_length": 50},
                    "email": {"type": "email", "required": True},
                    "age": {"type": "integer", "required": False, "min": 18, "max": 100},
                    "active": {"type": "boolean", "required": True},
                    "role": {"type": "string", "required": True, "enum": ["admin", "user", "guest"]}
                }
            })

    def test_handle_invalid_model_data(self):
        """
        اختبار معالجة البيانات غير الصحيحة وفقًا لنموذج محدد.
        """
        # بيانات غير صحيحة
        data = {
            "id": "1",  # يجب أن يكون رقمًا
            "name": "أ",  # أقل من الحد الأدنى
            "email": "invalid-email",  # بريد إلكتروني غير صالح
            "age": 15,  # أقل من الحد الأدنى
            "active": "نعم",  # يجب أن يكون قيمة منطقية
            "role": "invalid-role",  # قيمة غير موجودة في القائمة
            "unknown_field": "قيمة"  # حقل غير موجود في النموذج
        }

        # معالجة البيانات بدون إصلاح تلقائي
        is_valid, fixed_data, actions = self.handler.handle_invalid_model_data(
            data, "test_model", auto_fix=False)
        self.assertFalse(
            is_valid,
            "يجب أن تكون البيانات غير صحيحة بدون إصلاح تلقائي")
        self.assertEqual(
            len(actions),
            0,
            "يجب ألا تكون هناك إجراءات بدون إصلاح تلقائي")

        # معالجة البيانات مع إصلاح تلقائي
        is_valid, fixed_data, actions = self.handler.handle_invalid_model_data(
            data, "test_model", auto_fix=True)

        # قد لا يتم إصلاح جميع المشكلات، لكن يجب أن تكون هناك إجراءات
        self.assertGreater(
            len(actions),
            0,
            "يجب أن تكون هناك إجراءات مع الإصلاح التلقائي")

        # التحقق من الإجراءات
        action_fields = [action["field"]
                         for action in actions if "field" in action]

        # يجب أن تكون هناك إجراءات لبعض الحقول على الأقل
        expected_fields = [
            "id",
            "name",
            "email",
            "age",
            "active",
            "role",
            "unknown_field"]
        self.assertTrue(any(field in action_fields for field in expected_fields),
                        "يجب أن تكون هناك إجراءات لبعض الحقول المتوقعة")

    def test_handle_batch_model_data(self):
        """
        اختبار معالجة مجموعة من البيانات غير الصحيحة.
        """
        # مجموعة من البيانات
        data_list = [
            {
                "id": 1,
                "name": "أحمد محمد",
                "email": "ahmed@example.com",
                "age": 30,
                "active": True,
                "role": "admin"
            },
            {
                "id": "2",  # يجب أن يكون رقمًا
                "name": "محمد علي",
                "email": "invalid-email",  # بريد إلكتروني غير صالح
                "active": "نعم",  # يجب أن يكون قيمة منطقية
                "role": "user"
            },
            {
                "id": 3,
                "name": "س",  # أقل من الحد الأدنى
                "email": "sara@example.com",
                "age": 15,  # أقل من الحد الأدنى
                "active": True,
                "role": "invalid-role"  # قيمة غير موجودة في القائمة
            }
        ]

        # معالجة البيانات مع إصلاح تلقائي
        is_valid, fixed_data_list, actions = self.handler.handle_batch_model_data(
            data_list, "test_model", auto_fix=True)

        # قد لا يتم إصلاح جميع المشكلات، لكن يجب أن تكون هناك إجراءات
        self.assertGreater(
            len(actions),
            0,
            "يجب أن تكون هناك إجراءات مع الإصلاح التلقائي")
        self.assertEqual(
            len(fixed_data_list),
            len(data_list),
            "يجب أن تكون هناك بيانات مصححة لكل عنصر في القائمة")

        # التحقق من الإجراءات
        indices = [action["index"] for action in actions if "index" in action]

        # يجب أن تكون هناك إجراءات للعناصر الثاني والثالث على الأقل
        self.assertTrue(1 in indices or 2 in indices,
                        "يجب أن تكون هناك إجراءات للعناصر غير الصحيحة")


if __name__ == "__main__":
    unittest.main()
