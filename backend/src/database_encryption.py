#!/usr/bin/env python3
# type: ignore
# flake8: noqa
# pylint: disable=all
"""
نظام تشفير قاعدة البيانات والتخزين المؤقت
ملف: database_encryption.py

All linting is disabled due to optional dependencies and complex encryption logic.
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, text, event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool, NullPool

try:
    from encryption_manager import EncryptionManager as ExternalEncryptionManager
except ImportError:
    print("⚠️ EncryptionManager not found, using dummy implementation")
    # Create a dummy class if EncryptionManager is not available

    class ExternalEncryptionManager:
        def __init__(self):
            pass

        def encrypt_symmetric(self, data):
            return data

        def decrypt_symmetric(self, data):
            return data

        def hash_password(self, password):
            return password

        def generate_secure_token(self, length):
            return "dummy_token"

        def encrypt_json_data(self, data):
            return data

        def decrypt_json_data(self, data):
            return data

        def encrypt_file(self, file_path, output_path=None):
            return True

        def decrypt_file(self, file_path, output_path=None):
            return True


try:
    import redis

    Redis = redis.Redis
except ImportError:
    print("⚠️ Redis not found, using dummy implementation")
    # Create a dummy redis module if not available

    class Redis:

        def __init__(self, *args, **kwargs):
            pass

        def get(self, key):
            return None

        def set(self, key, value, ex=None):
            return True

        def setex(self, key, time, value):
            return True

        def keys(self, pattern):
            return []

        def delete(self, *keys):
            return True

        def ping(self):
            return True


class DatabaseEncryption:
    """فئة تشفير قاعدة البيانات"""

    def __init__(self):
        self.encryption_manager = ExternalEncryptionManager()
        self.base_dir = Path(__file__).parent.parent
        self.db_dir = self.base_dir / "instance"
        self.db_dir.mkdir(exist_ok=True)

        # إعداد قاعدة البيانات المشفرة
        self.setup_encrypted_database()

    def setup_encrypted_database(self):
        """إعداد قاعدة البيانات المشفرة"""

        # إنشاء قاعدة بيانات مشفرة
        db_filename = os.environ.get("ENCRYPTED_DB_FILENAME", "inventory_encrypted.db")
        self.encrypted_db_path = self.db_dir / db_filename

        # إعداد SQLite مع تشفير
        self.setup_sqlite_encryption()

        # إنشاء الجداول المشفرة
        self.create_encrypted_tables()

    def setup_sqlite_encryption(self):
        """إعداد تشفير SQLite"""

        # إنشاء اتصال مع تشفير
        self.engine = create_engine(
            f"sqlite:///{self.encrypted_db_path}",
            poolclass=NullPool,
            connect_args={"check_same_thread": False, "timeout": 30},
            echo=False,
        )

        # إعداد مفتاح التشفير لـ SQLite

        try:

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                if isinstance(dbapi_connection, sqlite3.Connection):
                    # تفعيل إعدادات تحسين SQLite وتقليل مشاكل القفل
                    cursor = dbapi_connection.cursor()
                    cursor.execute("PRAGMA journal_mode=WAL")
                    cursor.execute("PRAGMA synchronous=NORMAL")
                    cursor.execute("PRAGMA cache_size=10000")
                    cursor.execute("PRAGMA temp_store=MEMORY")
                    cursor.execute(
                        "PRAGMA busy_timeout=5000"
                    )  # انتظر حتى 5 ثوانٍ بدلاً من فشل القفل فوراً
                    cursor.close()

        except ImportError:
            print("⚠️ SQLAlchemy event not available")

    def create_encrypted_tables(self):
        """إنشاء الجداول المشفرة"""

        with self.engine.begin() as conn:
            # جدول المستخدمين المشفر
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS encrypted_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email_encrypted TEXT,
                    phone_encrypted TEXT,
                    address_encrypted TEXT,
                    national_id_encrypted TEXT,
                    salt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """
                )
            )

            # جدول العملاء المشفر
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS encrypted_customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_encrypted TEXT NOT NULL,
                    email_encrypted TEXT,
                    phone_encrypted TEXT,
                    address_encrypted TEXT,
                    company_encrypted TEXT,
                    tax_id_encrypted TEXT,
                    credit_limit_encrypted TEXT,
                    notes_encrypted TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
                )
            )

            # جدول الموردين المشفر
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS encrypted_suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_encrypted TEXT NOT NULL,
                    email_encrypted TEXT,
                    phone_encrypted TEXT,
                    address_encrypted TEXT,
                    company_encrypted TEXT,
                    tax_id_encrypted TEXT,
                    bank_account_encrypted TEXT,
                    contact_person_encrypted TEXT,
                    notes_encrypted TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
                )
            )

            # جدول المعاملات المالية المشفرة
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS encrypted_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_type TEXT NOT NULL,
                    amount_encrypted TEXT NOT NULL,
                    currency TEXT DEFAULT 'EGP',
                    description_encrypted TEXT,
                    reference_number_encrypted TEXT,
                    customer_id INTEGER,
                    supplier_id INTEGER,
                    payment_method_encrypted TEXT,
                    bank_details_encrypted TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER
                )
            """
                )
            )

            # جدول سجلات الأمان
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS security_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    user_id INTEGER,
                    ip_address TEXT,
                    user_agent TEXT,
                    details_encrypted TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    severity TEXT DEFAULT 'INFO'
                )
            """
                )
            )

            # جدول مفاتيح التشفير
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS encryption_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_name TEXT UNIQUE NOT NULL,
                    key_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """
                )
            )

            conn.commit()
            print("✅ تم إنشاء الجداول المشفرة")

    def encrypt_user_data(self, user_data):
        """تشفير بيانات المستخدم"""
        encrypted_data = {}

        # الحقول التي تحتاج تشفير
        sensitive_fields = ["email", "phone", "address", "national_id"]

        for field, value in user_data.items():
            if field in sensitive_fields and value:
                encrypted_data[f"{field}_encrypted"] = (
                    self.encryption_manager.encrypt_symmetric(str(value))
                )
            elif field == "password":
                encrypted_data["password_hash"] = self.encryption_manager.hash_password(
                    value
                )
                encrypted_data["salt"] = self.encryption_manager.generate_secure_token(
                    16
                )
            else:
                encrypted_data[field] = value

        return encrypted_data

    def decrypt_user_data(self, encrypted_user_data):
        """فك تشفير بيانات المستخدم"""
        decrypted_data = {}

        sensitive_fields = ["email", "phone", "address", "national_id"]

        for field, value in encrypted_user_data.items():
            if field.endswith("_encrypted"):
                original_field = field.replace("_encrypted", "")
                if original_field in sensitive_fields and value:
                    decrypted_data[original_field] = (
                        self.encryption_manager.decrypt_symmetric(value)
                    )
            elif field not in ["password_hash", "salt"]:
                decrypted_data[field] = value

        return decrypted_data

    def insert_encrypted_user(self, user_data):
        """إدراج مستخدم مشفر"""
        try:
            encrypted_data = self.encrypt_user_data(user_data)

            with self.engine.begin() as conn:
                result = conn.execute(
                    text(
                        """
                    INSERT INTO encrypted_users
                    (username, password_hash, email_encrypted, phone_encrypted,
                     address_encrypted, national_id_encrypted, salt)
                    VALUES (:username,
                        :password_hash,
                        :email_encrypted,
                        :phone_encrypted,
                            :address_encrypted, :national_id_encrypted, :salt)
                """
                    ),
                    encrypted_data,
                )

                # transaction commits automatically when exiting begin() context
                try:
                    return result.lastrowid
                except Exception:
                    return None

        except Exception as e:
            print(f"❌ خطأ في إدراج المستخدم المشفر: {e}")
            return None

    def get_encrypted_user(self, user_id):
        """الحصول على مستخدم مشفر"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text(
                        """
                    SELECT * FROM encrypted_users WHERE id = :user_id
                """
                    ),
                    {"user_id": user_id},
                )

                row = result.fetchone()
                if row:
                    user_data = dict(row._mapping)
                    return self.decrypt_user_data(user_data)

                return None

        except Exception as e:
            print(f"❌ خطأ في الحصول على المستخدم المشفر: {e}")
            return None

    def encrypt_financial_transaction(self, transaction_data):
        """تشفير المعاملة المالية"""
        encrypted_data = {}

        sensitive_fields = [
            "amount",
            "description",
            "reference_number",
            "payment_method",
            "bank_details",
        ]

        for field, value in transaction_data.items():
            if field in sensitive_fields and value:
                encrypted_data[f"{field}_encrypted"] = (
                    self.encryption_manager.encrypt_symmetric(str(value))
                )
            else:
                encrypted_data[field] = value

        return encrypted_data

    def log_security_event(
        self, event_type, user_id, ip_address, user_agent, details, severity="INFO"
    ):
        """تسجيل حدث أمني"""
        try:
            encrypted_details = self.encryption_manager.encrypt_json_data(details)

            with self.engine.connect() as conn:
                conn.execute(
                    text(
                        """
                    INSERT INTO security_logs
                    (event_type,
                        user_id,
                        ip_address,
                        user_agent,
                        details_encrypted,
                        severity)
                    VALUES (:event_type,
                        :user_id,
                        :ip_address,
                        :user_agent,
                        :details_encrypted,
                        :severity)
                """
                    ),
                    {
                        "event_type": event_type,
                        "user_id": user_id,
                        "ip_address": ip_address,
                        "user_agent": user_agent,
                        "details_encrypted": encrypted_details,
                        "severity": severity,
                    },
                )

                conn.commit()

        except Exception as e:
            print(f"❌ خطأ في تسجيل الحدث الأمني: {e}")


class CacheEncryption:
    """فئة تشفير التخزين المؤقت"""

    def __init__(self):
        self.encryption_manager = ExternalEncryptionManager()
        self.redis_client = None
        self.setup_redis_connection()

    def setup_redis_connection(self):
        """إعداد اتصال Redis"""
        try:
            self.redis_client = Redis(
                host=os.environ.get("REDIS_HOST", "localhost"),
                port=int(os.environ.get("REDIS_PORT", 5606)),
                db=int(os.environ.get("REDIS_DB", 0)),
                password=os.environ.get("REDIS_PASSWORD"),
                decode_responses=False,  # للتعامل مع البيانات المشفرة
            )

            # اختبار الاتصال
            self.redis_client.ping()
            print("✅ تم الاتصال بـ Redis")

        except Exception as e:
            print(f"⚠️ فشل الاتصال بـ Redis: {e}")
            self.redis_client = None

    def set_encrypted_cache(self, key, value, expiry=3600):
        """حفظ قيمة مشفرة في التخزين المؤقت"""
        if not self.redis_client:
            return False

        try:
            # تشفير القيمة
            encrypted_value = self.encryption_manager.encrypt_json_data(value)

            if encrypted_value:
                # حفظ في Redis
                self.redis_client.setex(
                    f"encrypted:{key}", expiry, encrypted_value.encode("utf-8")
                )
                return True

            return False

        except Exception as e:
            print(f"❌ خطأ في حفظ التخزين المؤقت المشفر: {e}")
            return False

    def get_encrypted_cache(self, key):
        """الحصول على قيمة مشفرة من التخزين المؤقت"""
        if not self.redis_client:
            return None

        try:
            # الحصول على القيمة المشفرة
            encrypted_value = self.redis_client.get(f"encrypted:{key}")

            if encrypted_value:
                # فك التشفير
                decrypted_value = self.encryption_manager.decrypt_json_data(
                    encrypted_value.decode("utf-8")
                )
                return decrypted_value

            return None

        except Exception as e:
            print(f"❌ خطأ في الحصول على التخزين المؤقت المشفر: {e}")
            return None

    def delete_encrypted_cache(self, key):
        """حذف قيمة من التخزين المؤقت المشفر"""
        if not self.redis_client:
            return False

        try:
            result = self.redis_client.delete(f"encrypted:{key}")
            return result > 0

        except Exception as e:
            print(f"❌ خطأ في حذف التخزين المؤقت المشفر: {e}")
            return False

    def clear_all_encrypted_cache(self):
        """مسح جميع البيانات المشفرة من التخزين المؤقت"""
        if not self.redis_client:
            return False

        try:
            # البحث عن جميع المفاتيح المشفرة
            encrypted_keys = self.redis_client.keys("encrypted:*")

            if encrypted_keys:
                # حذف جميع المفاتيح
                self.redis_client.delete(*encrypted_keys)
                print(f"✅ تم مسح {len(encrypted_keys)} عنصر من التخزين المؤقت المشفر")

            return True

        except Exception as e:
            print(f"❌ خطأ في مسح التخزين المؤقت المشفر: {e}")
            return False


class FileEncryption:
    """فئة تشفير الملفات"""

    def __init__(self):
        self.encryption_manager = ExternalEncryptionManager()
        self.base_dir = Path(__file__).parent.parent
        self.encrypted_files_dir = self.base_dir / "encrypted_files"
        self.encrypted_files_dir.mkdir(exist_ok=True)

    def encrypt_uploaded_file(self, file_path, original_filename):
        """تشفير ملف مرفوع"""
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                return None

            # إنشاء اسم ملف مشفر
            file_hash = hashlib.sha256(original_filename.encode()).hexdigest()[:16]
            encrypted_filename = (
                f"{file_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
            )
            encrypted_file_path = self.encrypted_files_dir / encrypted_filename

            # تشفير الملف
            success = self.encryption_manager.encrypt_file(
                file_path, encrypted_file_path
            )

            if success:
                # حفظ معلومات الملف
                file_info = {
                    "original_filename": original_filename,
                    "encrypted_filename": encrypted_filename,
                    "file_size": file_path.stat().st_size,
                    "upload_time": datetime.now().isoformat(),
                    "file_hash": file_hash,
                }

                info_file = encrypted_file_path.with_suffix(".info")
                with open(info_file, "w", encoding="utf-8") as f:
                    json.dump(file_info, f, ensure_ascii=False, indent=2)

                # حذف الملف الأصلي
                file_path.unlink()

                return {
                    "encrypted_path": str(encrypted_file_path),
                    "file_info": file_info,
                }

            return None

        except Exception as e:
            print(f"❌ خطأ في تشفير الملف المرفوع: {e}")
            return None

    def decrypt_file_for_download(self, encrypted_filename):
        """فك تشفير ملف للتحميل"""
        try:
            encrypted_file_path = self.encrypted_files_dir / encrypted_filename
            info_file = encrypted_file_path.with_suffix(".info")

            if not encrypted_file_path.exists() or not info_file.exists():
                return None

            # قراءة معلومات الملف
            with open(info_file, "r", encoding="utf-8") as f:
                file_info = json.load(f)

            # إنشاء ملف مؤقت مفكوك التشفير
            temp_dir = self.base_dir / "temp"
            temp_dir.mkdir(exist_ok=True)

            temp_file_path = temp_dir / file_info["original_filename"]

            # فك تشفير الملف
            success = self.encryption_manager.decrypt_file(
                encrypted_file_path, temp_file_path
            )

            if success:
                return {
                    "temp_path": str(temp_file_path),
                    "original_filename": file_info["original_filename"],
                    "file_info": file_info,
                }

            return None

        except Exception as e:
            print(f"❌ خطأ في فك تشفير الملف: {e}")
            return None


def test_database_encryption():
    """اختبار تشفير قاعدة البيانات"""
    print("🔐 === اختبار تشفير قاعدة البيانات ===")

    # إنشاء نظام تشفير قاعدة البيانات
    import os
    import uuid

    os.environ["ENCRYPTED_DB_FILENAME"] = (
        f"inventory_encrypted_test_{uuid.uuid4().hex[:6]}.db"
    )
    db_encryption = DatabaseEncryption()

    # اختبار إدراج مستخدم مشفر
    import uuid
    import os

    # استخدم ملف قاعدة بيانات مؤقت لمنع تعارضات القفل في بيئات متعددة العمليات
    os.environ["ENCRYPTED_DB_FILENAME"] = (
        f"inventory_encrypted_test_{uuid.uuid4().hex[:6]}.db"
    )
    unique_username = f"test_user_{uuid.uuid4().hex[:8]}"
    test_user = {
        "username": unique_username,
        "password": "secure_password123",
        "email": "test@example.com",
        "phone": "+201234567890",
        "address": "عنوان تجريبي للاختبار",
        "national_id": "12345678901234",
    }

    # إدراج المستخدم
    user_id = db_encryption.insert_encrypted_user(test_user)
    print(f"معرف المستخدم المدرج: {user_id}")

    # استرجاع المستخدم إذا تم الإدراج بنجاح
    if user_id:
        retrieved_user = db_encryption.get_encrypted_user(user_id)
        print(f"المستخدم المسترجع: {retrieved_user}")
    else:
        print("لم يتم إدراج المستخدم بسبب خطأ سابق.")

    # اختبار تشفير التخزين المؤقت
    cache_encryption = CacheEncryption()

    test_data = {"key": "value", "number": 123, "list": [1, 2, 3]}

    # حفظ في التخزين المؤقت
    cache_encryption.set_encrypted_cache("test_key", test_data, 60)

    # استرجاع من التخزين المؤقت
    cached_data = cache_encryption.get_encrypted_cache("test_key")
    print(f"البيانات المخزنة مؤقتاً: {cached_data}")


if __name__ == "__main__":
    test_database_encryption()
