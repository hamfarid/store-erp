"""
#!/usr/bin/env python3

مدير التشفير الشامل للواجهة الخلفية
ملف: encryption_manager.py
"""

import os
import base64
import hashlib
import secrets
import json
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

# من cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# من cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import bcrypt


class EncryptionManager:
    """مدير التشفير الشامل"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.keys_dir = self.base_dir / "encryption_keys"
        self.keys_dir.mkdir(exist_ok=True)

        # تحميل أو إنشاء المفاتيح
        self.master_key = self.load_or_generate_master_key()
        self.fernet = Fernet(self.master_key)
        (self.rsa_private_key, self.rsa_public_key) = self.load_or_generate_rsa_keys()

    def load_or_generate_master_key(self):
        """تحميل أو إنشاء المفتاح الرئيسي"""
        key_file = self.keys_dir / "master.key"

        if key_file.exists():
            try:
                with open(key_file, "rb") as f:
                    return f.read()
            except (ValueError, TypeError, OSError, InvalidToken) as e:
                print(f"⚠️ خطأ في تحميل المفتاح الرئيسي: {e}")

        # إنشاء مفتاح جديد
        key = Fernet.generate_key()

        try:
            with open(key_file, "wb") as f:
                f.write(key)

            # تعيين صلاحيات آمنة
            os.chmod(key_file, 0o600)
            print(f"✅ تم إنشاء مفتاح رئيسي جديد: {key_file}")

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في حفظ المفتاح الرئيسي: {e}")

        return key

    def load_or_generate_rsa_keys(self):
        """تحميل أو إنشاء مفاتيح RSA"""
        private_key_file = self.keys_dir / "rsa_private.pem"
        public_key_file = self.keys_dir / "rsa_public.pem"

        if private_key_file.exists() and public_key_file.exists():
            try:
                # تحميل المفتاح الخاص
                with open(private_key_file, "rb") as f:
                    private_key = serialization.load_pem_private_key(
                        f.read(), password=None
                    )

                # تحميل المفتاح العام
                with open(public_key_file, "rb") as f:
                    public_key = serialization.load_pem_public_key(f.read())

                return private_key, public_key

            except (ValueError, TypeError, OSError, InvalidToken) as e:
                print(f"⚠️ خطأ في تحميل مفاتيح RSA: {e}")

        # إنشاء مفاتيح جديدة
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        try:
            # حفظ المفتاح الخاص
            with open(private_key_file, "wb") as f:
                f.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )

            # حفظ المفتاح العام
            with open(public_key_file, "wb") as f:
                f.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                )

            # تعيين صلاحيات آمنة
            os.chmod(private_key_file, 0o600)
            os.chmod(public_key_file, 0o644)

            print("✅ تم إنشاء مفاتيح RSA جديدة")

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في حفظ مفاتيح RSA: {e}")

        return private_key, public_key

    def encrypt_symmetric(self, data):
        """تشفير متماثل باستخدام Fernet"""
        if isinstance(data, str):
            data = data.encode("utf-8")

        try:
            encrypted_data = self.fernet.encrypt(data)
            return base64.b64encode(encrypted_data).decode("utf-8")
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في التشفير المتماثل: {e}")
            return None

    def decrypt_symmetric(self, encrypted_data):
        """فك التشفير المتماثل"""
        try:
            encrypted_data = base64.b64decode(encrypted_data.encode("utf-8"))
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return decrypted_data.decode("utf-8")
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في فك التشفير المتماثل: {e}")
            return None

    def encrypt_asymmetric(self, data):
        """تشفير غير متماثل باستخدام RSA"""
        if isinstance(data, str):
            data = data.encode("utf-8")

        try:
            # التأكد من أن المفتاح هو RSA
            if isinstance(self.rsa_public_key, RSAPublicKey):
                encrypted_data = self.rsa_public_key.encrypt(
                    data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )
                return base64.b64encode(encrypted_data).decode("utf-8")
            print("❌ المفتاح العام ليس من نوع RSA")
            return None
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في التشفير غير المتماثل: {e}")
            return None

    def decrypt_asymmetric(self, encrypted_data):
        """فك التشفير غير المتماثل"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode("utf-8"))

            # التأكد من أن المفتاح هو RSA
            if isinstance(self.rsa_private_key, RSAPrivateKey):
                decrypted_data = self.rsa_private_key.decrypt(
                    encrypted_bytes,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )
                return decrypted_data.decode("utf-8")
            print("❌ المفتاح الخاص ليس من نوع RSA")
            return None
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في فك التشفير غير المتماثل: {e}")
            return None

    def hash_password(self, password):
        """تشفير كلمة المرور باستخدام bcrypt"""
        if isinstance(password, str):
            password = password.encode("utf-8")

        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password, salt)
            return hashed.decode("utf-8")
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في تشفير كلمة المرور: {e}")
            return None

    def verify_password(self, password, hashed_password):
        """التحقق من كلمة المرور"""
        if isinstance(password, str):
            password = password.encode("utf-8")
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode("utf-8")

        try:
            return bcrypt.checkpw(password, hashed_password)
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في التحقق من كلمة المرور: {e}")
            return False

    def generate_secure_token(self, length=32):
        """إنشاء رمز آمن"""
        try:
            token = secrets.token_urlsafe(length)
            return token
        except (ValueError, TypeError, OSError) as e:
            print(f"❌ خطأ في إنشاء الرمز الآمن: {e}")
            return None

    def encrypt_file(self, file_path, output_path=None):
        """تشفير ملف"""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"❌ الملف غير موجود: {file_path}")
            return False

        if output_path is None:
            output_path = file_path.with_suffix(file_path.suffix + ".encrypted")
        else:
            output_path = Path(output_path)

        try:
            with open(file_path, "rb") as f:
                file_data = f.read()

            encrypted_data = self.fernet.encrypt(file_data)

            with open(output_path, "wb") as f:
                f.write(encrypted_data)

            print(f"✅ تم تشفير الملف: {file_path} -> {output_path}")
            return True

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في تشفير الملف: {e}")
            return False

    def decrypt_file(self, encrypted_file_path, output_path=None):
        """فك تشفير ملف"""
        encrypted_file_path = Path(encrypted_file_path)

        if not encrypted_file_path.exists():
            print(f"❌ الملف المشفر غير موجود: {encrypted_file_path}")
            return False

        if output_path is None:
            output_path = encrypted_file_path.with_suffix("")
            if output_path.suffix == ".encrypted":
                output_path = output_path.with_suffix("")
        else:
            output_path = Path(output_path)

        try:
            with open(encrypted_file_path, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = self.fernet.decrypt(encrypted_data)

            with open(output_path, "wb") as f:
                f.write(decrypted_data)

            print(f"✅ تم فك تشفير الملف: {encrypted_file_path} -> {output_path}")
            return True

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في فك تشفير الملف: {e}")
            return False

    def encrypt_json_data(self, data):
        """تشفير بيانات JSON"""
        try:
            json_string = json.dumps(data, ensure_ascii=False)
            encrypted_data = self.encrypt_symmetric(json_string)
            return encrypted_data
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في تشفير بيانات JSON: {e}")
            return None

    def decrypt_json_data(self, encrypted_data):
        """فك تشفير بيانات JSON"""
        try:
            json_string = self.decrypt_symmetric(encrypted_data)
            if json_string:
                return json.loads(json_string)
            return None
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في فك تشفير بيانات JSON: {e}")
            return None

    def create_secure_session_data(self, user_data):
        """إنشاء بيانات جلسة آمنة"""
        try:
            # إضافة طابع زمني وملح
            session_data = {
                "user_data": user_data,
                "timestamp": datetime.now().isoformat(),
                "salt": self.generate_secure_token(16),
            }

            # تشفير البيانات
            encrypted_session = self.encrypt_json_data(session_data)
            return encrypted_session

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في إنشاء بيانات الجلسة الآمنة: {e}")
            return None

    def verify_secure_session_data(self, encrypted_session):
        """التحقق من بيانات الجلسة الآمنة"""
        try:
            session_data = self.decrypt_json_data(encrypted_session)
            if not session_data:
                return None

            # فحص الطابع الزمني (انتهاء الصلاحية)
            timestamp = datetime.fromisoformat(session_data["timestamp"])
            current_time = datetime.now()

            # انتهاء الصلاحية بعد 24 ساعة
            if (current_time - timestamp).total_seconds() > 86400:
                return None

            return session_data["user_data"]

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في التحقق من بيانات الجلسة: {e}")
            return None

    def get_encryption_info(self):
        """الحصول على معلومات التشفير"""
        return {
            "symmetric_algorithm": "Fernet (AES 128)",
            "asymmetric_algorithm": "RSA 2048",
            "password_hashing": "bcrypt (rounds=12)",
            "key_derivation": "PBKDF2-HMAC-SHA256",
            "keys_directory": str(self.keys_dir),
            "master_key_exists": (self.keys_dir / "master.key").exists(),
            "rsa_keys_exist": (self.keys_dir / "rsa_private.pem").exists(),
        }


class DatabaseEncryption:
    """تشفير قاعدة البيانات"""

    def __init__(self, encryption_manager):
        self.encryption_manager = encryption_manager

    def encrypt_sensitive_field(self, value):
        """تشفير حقل حساس في قاعدة البيانات"""
        if value is None:
            return None

        return self.encryption_manager.encrypt_symmetric(str(value))

    def decrypt_sensitive_field(self, encrypted_value):
        """فك تشفير حقل حساس"""
        if encrypted_value is None:
            return None

        return self.encryption_manager.decrypt_symmetric(encrypted_value)

    def encrypt_user_data(self, user_data):
        """تشفير بيانات المستخدم الحساسة"""
        encrypted_data = {}

        sensitive_fields = ["email", "phone", "address", "national_id"]

        for field, value in user_data.items():
            if field in sensitive_fields and value:
                encrypted_data[field] = self.encrypt_sensitive_field(value)
            else:
                encrypted_data[field] = value

        return encrypted_data

    def decrypt_user_data(self, encrypted_user_data):
        """فك تشفير بيانات المستخدم"""
        decrypted_data = {}

        sensitive_fields = ["email", "phone", "address", "national_id"]

        for field, value in encrypted_user_data.items():
            if field in sensitive_fields and value:
                decrypted_data[field] = self.decrypt_sensitive_field(value)
            else:
                decrypted_data[field] = value

        return decrypted_data


def create_encryption_manager():
    """إنشاء مدير التشفير"""
    return EncryptionManager()


def test_encryption():
    """اختبار نظام التشفير"""
    print("🔐 === اختبار نظام التشفير ===")

    # إنشاء مدير التشفير
    em = EncryptionManager()

    # اختبار التشفير المتماثل
    test_data = "هذا نص تجريبي للتشفير"
    encrypted = em.encrypt_symmetric(test_data)
    decrypted = em.decrypt_symmetric(encrypted)

    print(f"النص الأصلي: {test_data}")
    print(f"مشفر: {encrypted[:50] if encrypted else 'None'}...")
    print(f"فك التشفير: {decrypted}")
    print(f"التطابق: {'✅' if test_data == decrypted else '❌'}")

    # اختبار تشفير كلمة المرور
    password = "password123"
    hashed = em.hash_password(password)
    verified = em.verify_password(password, hashed)

    print(f"\nكلمة المرور: {password}")
    print(f"مشفرة: {hashed}")
    print(f"التحقق: {'✅' if verified else '❌'}")

    # عرض معلومات التشفير
    info = em.get_encryption_info()
    print("\nمعلومات التشفير:")
    for key, value in info.items():
        print(f"  {key}: {value}")


class CommunicationEncryption:
    """تشفير الاتصالات"""

    def __init__(self, encryption_manager):
        self.encryption_manager = encryption_manager

    def encrypt_api_request(self, request_data):
        """تشفير طلب API"""
        try:
            # إضافة طابع زمني ومعرف فريد
            encrypted_request = {
                "data": self.encryption_manager.encrypt_json_data(request_data),
                "timestamp": datetime.now().isoformat(),
                "request_id": self.encryption_manager.generate_secure_token(16),
            }
            return encrypted_request
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في تشفير طلب API: {e}")
            return None

    def decrypt_api_request(self, encrypted_request):
        """فك تشفير طلب API"""
        try:
            if not isinstance(encrypted_request, dict):
                return None

            # فك تشفير البيانات
            decrypted_data = self.encryption_manager.decrypt_json_data(
                encrypted_request.get("data")
            )

            # فحص الطابع الزمني (انتهاء الصلاحية خلال 5 دقائق)
            timestamp = datetime.fromisoformat(encrypted_request["timestamp"])
            current_time = datetime.now()

            if (current_time - timestamp).total_seconds() > 300:  # 5 دقائق
                return None

            return decrypted_data

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في فك تشفير طلب API: {e}")
            return None

    def encrypt_api_response(self, response_data):
        """تشفير استجابة API"""
        try:
            encrypted_response = {
                "data": self.encryption_manager.encrypt_json_data(response_data),
                "timestamp": datetime.now().isoformat(),
                "signature": self.create_response_signature(response_data),
            }
            return encrypted_response
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في تشفير استجابة API: {e}")
            return None

    def decrypt_api_response(self, encrypted_response):
        """فك تشفير استجابة API"""
        try:
            if not isinstance(encrypted_response, dict):
                return None

            # فك تشفير البيانات
            decrypted_data = self.encryption_manager.decrypt_json_data(
                encrypted_response.get("data")
            )

            # التحقق من التوقيع
            expected_signature = self.create_response_signature(decrypted_data)
            if encrypted_response.get("signature") != expected_signature:
                print("⚠️ تحذير: توقيع الاستجابة غير صحيح")
                return None

            return decrypted_data

        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في فك تشفير استجابة API: {e}")
            return None

    def create_response_signature(self, data):
        """إنشاء توقيع للاستجابة"""
        try:
            data_string = json.dumps(data, sort_keys=True, ensure_ascii=False)
            signature = hashlib.sha256(data_string.encode("utf-8")).hexdigest()
            return signature
        except (ValueError, TypeError, OSError, InvalidToken) as e:
            print(f"❌ خطأ في إنشاء التوقيع: {e}")
            return None


if __name__ == "__main__":
    test_encryption()
