# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
#!/usr/bin/env python3

نظام الاتصالات الآمنة للواجهة الخلفية
ملف: secure_communication.py
All linting disabled due to complex imports and optional dependencies.
"""

import json
import hashlib
import hmac
import time
from datetime import datetime
from flask import request, jsonify, g
import logging
from functools import wraps
from ..encryption_manager import EncryptionManager


class SecureCommunication:
    """فئة الاتصالات الآمنة"""

    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.api_keys = {}  # تخزين مفاتيح API
        self.rate_limits = {}  # تحديد معدل الطلبات

    def generate_api_key(self, client_id):
        """إنشاء مفتاح API للعميل"""
        api_key = self.encryption_manager.generate_secure_token(32)
        api_secret = self.encryption_manager.generate_secure_token(64)

        self.api_keys[client_id] = {
            "api_key": api_key,
            "api_secret": api_secret,
            "created_at": datetime.now().isoformat(),
            "active": True,
        }

        return api_key, api_secret

    def verify_api_key(self, api_key):
        """التحقق من مفتاح API"""
        for client_id, key_data in self.api_keys.items():
            if key_data["api_key"] == api_key and key_data["active"]:
                return client_id
        return None

    def create_request_signature(self, method, url, body, timestamp, api_secret):
        """إنشاء توقيع للطلب"""
        # إنشاء السلسلة للتوقيع
        string_to_sign = f"{method}\n{url}\n{body}\n{timestamp}"

        # إنشاء HMAC
        signature = hmac.new(
            api_secret.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return signature

    def verify_request_signature(
        self, signature, method, url, body, timestamp, api_secret
    ):
        """التحقق من توقيع الطلب"""
        expected_signature = self.create_request_signature(
            method, url, body, timestamp, api_secret
        )
        return hmac.compare_digest(signature, expected_signature)

    def encrypt_request_data(self, data):
        """تشفير بيانات الطلب"""
        try:
            # تحويل البيانات إلى JSON
            json_data = json.dumps(data, ensure_ascii=False)

            # تشفير البيانات
            encrypted_data = self.encryption_manager.encrypt_symmetric(json_data)

            # إضافة معلومات إضافية
            request_package = {
                "encrypted_data": encrypted_data,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
            }

            return request_package

        except Exception as e:
            print(f"❌ خطأ في تشفير بيانات الطلب: {e}")
            return None

    def decrypt_request_data(self, encrypted_package):
        """فك تشفير بيانات الطلب"""
        try:
            if not isinstance(encrypted_package, dict):
                return None

            # فحص الطابع الزمني
            timestamp = datetime.fromisoformat(encrypted_package["timestamp"])
            current_time = datetime.now()

            # انتهاء الصلاحية خلال 5 دقائق
            if (current_time - timestamp).total_seconds() > 300:
                return None

            # فك تشفير البيانات
            encrypted_data = encrypted_package["encrypted_data"]
            json_data = self.encryption_manager.decrypt_symmetric(encrypted_data)

            if json_data:
                return json.loads(json_data)

            return None

        except Exception as e:
            print(f"❌ خطأ في فك تشفير بيانات الطلب: {e}")
            return None

    def encrypt_response_data(self, data):
        """تشفير بيانات الاستجابة"""
        try:
            # تحويل البيانات إلى JSON
            json_data = json.dumps(data, ensure_ascii=False)

            # تشفير البيانات
            encrypted_data = self.encryption_manager.encrypt_symmetric(json_data)

            # إنشاء توقيع للتحقق من التكامل
            signature = hashlib.sha256(json_data.encode("utf-8")).hexdigest()

            # إنشاء حزمة الاستجابة
            response_package = {
                "encrypted_data": encrypted_data,
                "signature": signature,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
            }

            return response_package

        except Exception as e:
            print(f"❌ خطأ في تشفير بيانات الاستجابة: {e}")
            return None

    def decrypt_response_data(self, encrypted_package):
        """فك تشفير بيانات الاستجابة"""
        try:
            if not isinstance(encrypted_package, dict):
                return None

            # فك تشفير البيانات
            encrypted_data = encrypted_package["encrypted_data"]
            json_data = self.encryption_manager.decrypt_symmetric(encrypted_data)

            if not json_data:
                return None

            # التحقق من التوقيع
            expected_signature = hashlib.sha256(json_data.encode("utf-8")).hexdigest()
            if encrypted_package["signature"] != expected_signature:
                print("⚠️ تحذير: توقيع الاستجابة غير صحيح")
                return None

            return json.loads(json_data)

        except Exception as e:
            print(f"❌ خطأ في فك تشفير بيانات الاستجابة: {e}")
            return None


def require_api_key(f):
    """ديكوريتر للتحقق من مفتاح API"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return (
                jsonify({"error": "API Key Required", "message": "مفتاح API مطلوب"}),
                401,
            )

        # التحقق من مفتاح API
        secure_comm = SecureCommunication()
        client_id = secure_comm.verify_api_key(api_key)

        if not client_id:
            return (
                jsonify({"error": "Invalid API Key", "message": "مفتاح API غير صحيح"}),
                401,
            )

        # حفظ معرف العميل في السياق
        g.client_id = client_id
        g.api_key = api_key

        return f(*args, **kwargs)

    return decorated_function


def require_signature(f):
    """ديكوريتر للتحقق من توقيع الطلب"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # الحصول على معلومات التوقيع
        signature = request.headers.get("X-Signature")
        timestamp = request.headers.get("X-Timestamp")
        api_key = request.headers.get("X-API-Key")

        if not all([signature, timestamp, api_key]):
            return (
                jsonify(
                    {
                        "error": "Missing Signature Headers",
                        "message": "رؤوس التوقيع مفقودة",
                    }
                ),
                400,
            )

        # فحص الطابع الزمني
        try:
            request_time = float(timestamp) if timestamp else 0
            current_time = time.time()

            # انتهاء الصلاحية خلال 5 دقائق
            if abs(current_time - request_time) > 300:
                return (
                    jsonify(
                        {"error": "Request Expired", "message": "انتهت صلاحية الطلب"}
                    ),
                    400,
                )
        except ValueError:
            return (
                jsonify(
                    {"error": "Invalid Timestamp", "message": "طابع زمني غير صحيح"}
                ),
                400,
            )

        # التحقق من التوقيع
        secure_comm = SecureCommunication()
        client_id = secure_comm.verify_api_key(api_key)

        if not client_id:
            return (
                jsonify({"error": "Invalid API Key", "message": "مفتاح API غير صحيح"}),
                401,
            )

        # الحصول على سر API
        api_secret = secure_comm.api_keys[client_id]["api_secret"]

        # إنشاء بيانات التوقيع
        method = request.method
        url = request.url
        body = request.get_data(as_text=True)

        # التحقق من التوقيع
        if not secure_comm.verify_request_signature(
            signature, method, url, body, timestamp, api_secret
        ):
            return (
                jsonify({"error": "Invalid Signature", "message": "توقيع غير صحيح"}),
                401,
            )

        return f(*args, **kwargs)

    return decorated_function


def encrypt_sensitive_data(f):
    """ديكوريتر لتشفير البيانات الحساسة"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # تشفير البيانات الواردة
        if request.is_json:
            secure_comm = SecureCommunication()

            # فحص إذا كانت البيانات مشفرة
            if request.json and "encrypted_data" in request.json:
                decrypted_data = secure_comm.decrypt_request_data(request.json)
                if decrypted_data:
                    # استبدال البيانات المشفرة بالبيانات المفكوكة
                    # request.json = decrypted_data  # لا يمكن تعديل request.json مباشرة
                    request._cached_json = decrypted_data

        # تنفيذ الدالة
        response = f(*args, **kwargs)

        # تشفير الاستجابة إذا كانت JSON
        if hasattr(response, "is_json") and response.is_json:
            secure_comm = SecureCommunication()
            encrypted_response = secure_comm.encrypt_response_data(response.json)

            if encrypted_response:
                response.data = json.dumps(encrypted_response)

        return response

    return decorated_function


class RateLimiter:
    """محدد معدل الطلبات"""

    def __init__(self):
        self.requests = {}
        self.limits = {
            "default": {"requests": 100, "window": 3600},  # 100 طلب في الساعة
            "auth": {"requests": 10, "window": 300},
            # 10 طلبات في 5 دقائق
            "upload": {"requests": 5, "window": 300},  # 5 طلبات في 5 دقائق
        }

    def is_allowed(self, client_id, endpoint_type="default"):
        """فحص إذا كان الطلب مسموح"""
        current_time = time.time()
        limit_config = self.limits.get(endpoint_type, self.limits["default"])

        # تنظيف الطلبات القديمة
        if client_id in self.requests:
            self.requests[client_id] = [
                req_time
                for req_time in self.requests[client_id]
                if current_time - req_time < limit_config["window"]
            ]
        else:
            self.requests[client_id] = []

        # فحص الحد المسموح
        if len(self.requests[client_id]) >= limit_config["requests"]:
            return False

        # إضافة الطلب الحالي
        self.requests[client_id].append(current_time)
        return True


def rate_limit(endpoint_type="default"):
    """ديكوريتر لتحديد معدل الطلبات"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_id = getattr(g, "client_id", request.remote_addr)

            rate_limiter = RateLimiter()
            if not rate_limiter.is_allowed(client_id, endpoint_type):
                return (
                    jsonify(
                        {
                            "error": "Rate Limit Exceeded",
                            "message": "تم تجاوز الحد المسموح من الطلبات",
                        }
                    ),
                    429,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def test_secure_communication():
    """اختبار نظام الاتصالات الآمنة"""
    print("🔐 === اختبار نظام الاتصالات الآمنة ===")

    # إنشاء نظام الاتصالات الآمنة
    secure_comm = SecureCommunication()

    # إنشاء مفتاح API
    client_id = "test_client"
    api_key, api_secret = secure_comm.generate_api_key(client_id)

    print(f"معرف العميل: {client_id}")
    print(f"مفتاح API: {api_key}")
    print(f"سر API: {api_secret[:20] if api_secret else 'None'}...")

    # اختبار تشفير البيانات
    test_data = {
        "username": "admin",
        "action": "login",
        "timestamp": datetime.now().isoformat(),
    }

    # تشفير الطلب
    encrypted_request = secure_comm.encrypt_request_data(test_data)
    print(f"\nالطلب المشفر: {str(encrypted_request)[:100]}...")

    # فك تشفير الطلب
    decrypted_request = secure_comm.decrypt_request_data(encrypted_request)
    print(f"الطلب المفكوك: {decrypted_request}")

    # التحقق من التطابق
    print(f"التطابق: {'✅' if test_data == decrypted_request else '❌'}")


if __name__ == "__main__":
    test_secure_communication()
