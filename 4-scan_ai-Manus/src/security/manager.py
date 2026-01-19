#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة إدارة الأمن وحماية البيانات
===============================

توفر هذه الوحدة وظائف لتأمين النظام وحماية البيانات، بما في ذلك التحقق من صحة المدخلات،
تنقية البيانات، إدارة الوصول (مبسطة)، وتسجيل الأحداث الأمنية.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import re
import logging
import hashlib
import hmac
from typing import Dict, Any, Optional, List
from werkzeug.utils import secure_filename
import bleach # لمكافحة XSS

# إعداد السجل
logger = logging.getLogger("agricultural_ai.security_manager")

class SecurityManager:
    """فئة لإدارة الأمن وحماية البيانات"""
    
    def __init__(self, config: Dict):
        """تهيئة مدير الأمن
        
        المعاملات:
            config (Dict): تكوين مدير الأمن
        """
        self.config = config.get("security", {})
        self.secret_key = self.config.get("secret_key", os.urandom(24).hex()) # مفتاح سري للتوقيعات والتشفير
        self.allowed_image_extensions = set(self.config.get("allowed_image_extensions", [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff"]))
        self.max_image_size = self.config.get("max_image_size_mb", 10) * 1024 * 1024 # بالميغابايت
        self.input_length_limit = self.config.get("input_length_limit", 500)
        self.bleach_config = {
            "tags": self.config.get("bleach_allowed_tags", ["b", "i", "em", "strong", "p", "br"]),
            "attributes": self.config.get("bleach_allowed_attributes", {}),
            "strip": True # إزالة العلامات غير المسموح بها بدلاً من استبدالها
        }
        
        if not self.secret_key:
            logger.warning("لم يتم توفير مفتاح سري، تم إنشاء مفتاح عشوائي. قد يتغير هذا عند إعادة التشغيل.")
            self.secret_key = os.urandom(24).hex()
            
        logger.info("تم تهيئة مدير الأمن")

    def validate_image_upload(self, file_storage) -> Tuple[bool, str]:
        """التحقق من صحة ملف الصورة المرفوع (يتطلب كائن يشبه FileStorage من Flask/Werkzeug)
        
        المعاملات:
            file_storage: كائن يمثل الملف المرفوع (مثل request.files["image"] في Flask)
            
        الإرجاع:
            Tuple[bool, str]: (صالح أم لا، رسالة خطأ أو اسم ملف آمن)
        """
        if not file_storage:
            return False, "لم يتم تقديم أي ملف."
            
        if not file_storage.filename:
             return False, "اسم الملف فارغ."

        # التحقق من الامتداد
        _, ext = os.path.splitext(file_storage.filename.lower())
        if ext not in self.allowed_image_extensions:
            return False, f"امتداد الملف غير مسموح به. الامتدادات المسموح بها: {', '.join(self.allowed_image_extensions)}"
            
        # التحقق من حجم الملف (يتطلب دعمًا من الكائن file_storage أو قراءة المحتوى)
        try:
            # محاولة الحصول على الحجم دون قراءة الملف بالكامل إذا أمكن
            file_storage.seek(0, os.SEEK_END)
            file_length = file_storage.tell()
            file_storage.seek(0) # إعادة المؤشر إلى البداية
            
            if file_length > self.max_image_size:
                return False, f"حجم الملف يتجاوز الحد المسموح به ({self.max_image_size / (1024*1024)} ميجابايت)."
        except Exception as e:
            logger.warning(f"لم يتمكن من التحقق من حجم الملف مباشرة: {e}. قد يتم التحقق منه لاحقًا.")
            # يمكن إضافة تحقق إضافي هنا إذا لزم الأمر بقراءة جزء من الملف

        # تنقية اسم الملف
        safe_filename = secure_filename(file_storage.filename)
        if not safe_filename:
             return False, "اسم الملف غير صالح بعد التنقية."
             
        logger.debug(f"تم التحقق من صحة تحميل الصورة: {safe_filename}")
        return True, safe_filename

    def validate_text_input(self, text: str, field_name: str = "input") -> Tuple[bool, str]:
        """التحقق من صحة المدخلات النصية"""
        if not isinstance(text, str):
             return False, f"الإدخال للحقل ", {field_name}" يجب أن يكون نصيًا."
             
        if len(text) > self.input_length_limit:
            return False, f"طول الإدخال للحقل ", {field_name}" يتجاوز الحد المسموح به ({self.input_length_limit} حرفًا)."
            
        # يمكن إضافة فحوصات أخرى هنا (مثل التحقق من الأحرف المسموح بها)
        # مثال: التحقق من عدم وجود أحرف تحكم غير مرغوب فيها
        if re.search(r"[\x00-\x1F\x7F]", text):
            return False, f"الإدخال للحقل ", {field_name}" يحتوي على أحرف تحكم غير صالحة."
            
        logger.debug(f"تم التحقق من صحة الإدخال النصي للحقل: {field_name}")
        return True, "الإدخال صالح"

    def sanitize_html(self, html_content: str) -> str:
        """تنقية محتوى HTML لمنع هجمات XSS"""
        if not isinstance(html_content, str):
            return ""
        sanitized = bleach.clean(html_content, **self.bleach_config)
        if len(sanitized) < len(html_content):
             logger.warning("تمت إزالة بعض المحتوى أثناء تنقية HTML")
        return sanitized

    def generate_csrf_token(self, session_id: str) -> str:
        """إنشاء رمز CSRF مرتبط بجلسة المستخدم"""
        # استخدام HMAC لربط الرمز بالجلسة والمفتاح السري
        token_data = f"{session_id}-{time.time()}".encode("utf-8")
        token = hmac.new(self.secret_key.encode("utf-8"), token_data, hashlib.sha256).hexdigest()
        logger.debug(f"تم إنشاء رمز CSRF للجلسة: {session_id[:8]}...")
        return token

    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """التحقق من صحة رمز CSRF"""
        # إعادة إنشاء الرمز المتوقع بنفس الطريقة (قد يتطلب تخزين وقت الإنشاء أو استخدام نافذة زمنية)
        # هذا مثال مبسط، في التطبيق الحقيقي قد يكون التحقق أكثر تعقيدًا
        # للتحقق الدقيق، يجب مقارنة الرمز المقدم برمز مخزن في الجلسة
        # هنا نتحقق فقط من أن التوقيع صحيح باستخدام المفتاح السري (أقل أمانًا من المقارنة المباشرة)
        try:
            # لا يمكن إعادة إنشاء نفس الرمز بالضبط بدون الطابع الزمني الأصلي
            # لذلك، هذا التحقق هو مجرد مثال توضيحي لفكرة استخدام HMAC
            # في تطبيق حقيقي: قارن الرمز المقدم برمز مخزن في جلسة المستخدم
            # if stored_token and hmac.compare_digest(token, stored_token):
            #     return True
            # return False
            logger.warning("التحقق من صحة CSRF هو مثال توضيحي فقط في هذا الإصدار.")
            # تحقق مبدئي من الطول والشكل
            if len(token) == 64 and all(c in "0123456789abcdef" for c in token):
                 logger.debug(f"تم التحقق مبدئيًا من شكل رمز CSRF للجلسة: {session_id[:8]}...")
                 return True # افتراض الصحة في هذا المثال
        except Exception as e:
            logger.error(f"خطأ أثناء التحقق من رمز CSRF: {e}")
        return False

    def hash_password(self, password: str) -> str:
        """تجزئة كلمة المرور باستخدام دالة تجزئة آمنة مع ملح"""
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        # تخزين الملح مع الهاش
        stored_password = salt.hex() + ":" + pwd_hash.hex()
        logger.info("تم تجزئة كلمة المرور")
        return stored_password

    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        """التحقق من تطابق كلمة المرور المقدمة مع الهاش المخزن"""
        try:
            salt_hex, hash_hex = stored_password.split(":")
            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(hash_hex)
            
            # تجزئة كلمة المرور المقدمة بنفس الملح
            provided_hash = hashlib.pbkdf2_hmac("sha256", provided_password.encode("utf-8"), salt, 100000)
            
            # مقارنة آمنة
            is_valid = hmac.compare_digest(stored_hash, provided_hash)
            if is_valid:
                 logger.debug("تم التحقق من صحة كلمة المرور")
            else:
                 logger.warning("فشل التحقق من صحة كلمة المرور")
            return is_valid
        except Exception as e:
            logger.error(f"خطأ أثناء التحقق من كلمة المرور: {e}")
            return False

    def log_security_event(self, event_type: str, message: str, user_id: Optional[str] = None, ip_address: Optional[str] = None):
        """تسجيل حدث أمني"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message,
            "user_id": user_id,
            "ip_address": ip_address
        }
        # يمكن توجيه هذا السجل إلى ملف منفصل أو نظام مراقبة
        logger.warning(f"[SECURITY EVENT - {event_type}] {message} (User: {user_id or \'N/A\'}, IP: {ip_address or \'N/A\'})", extra=log_entry)

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    from datetime import datetime
    import io
    
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "security": {
            "secret_key": "my-super-secret-key-for-testing",
            "allowed_image_extensions": [".jpg", ".png"],
            "max_image_size_mb": 5,
            "input_length_limit": 100
        }
    }
    
    # تهيئة مدير الأمن
    security_manager = SecurityManager(dummy_config)
    
    # --- اختبار التحقق من صحة الصورة ---
    print("\n--- اختبار التحقق من صحة الصورة ---")
    # كائن وهمي يشبه FileStorage
    class MockFileStorage:
        def __init__(self, filename, content):
            self.filename = filename
            self.stream = io.BytesIO(content)
        def seek(self, offset, whence=0):
            self.stream.seek(offset, whence)
        def tell(self):
            return self.stream.tell()
            
    valid_image_content = b"dummy image content"
    large_image_content = b"a" * (6 * 1024 * 1024) # 6MB
    
    valid_file = MockFileStorage("plant.jpg", valid_image_content)
    invalid_ext_file = MockFileStorage("document.pdf", valid_image_content)
    large_file = MockFileStorage("large_image.png", large_image_content)
    unsafe_name_file = MockFileStorage("../secret/image.jpg", valid_image_content)
    
    print(f"Valid file: {security_manager.validate_image_upload(valid_file)}")
    print(f"Invalid extension: {security_manager.validate_image_upload(invalid_ext_file)}")
    print(f"Large file: {security_manager.validate_image_upload(large_file)}")
    print(f"Unsafe name: {security_manager.validate_image_upload(unsafe_name_file)}")
    
    # --- اختبار التحقق من صحة النص ---
    print("\n--- اختبار التحقق من صحة النص ---")
    valid_text = "هذا نص صالح"
    long_text = "أ" * 150
    control_char_text = "نص مع حرف تحكم \x08"
    
    print(f"Valid text: {security_manager.validate_text_input(valid_text)}")
    print(f"Long text: {security_manager.validate_text_input(long_text)}")
    print(f"Control char text: {security_manager.validate_text_input(control_char_text)}")
    
    # --- اختبار تنقية HTML ---
    print("\n--- اختبار تنقية HTML ---")
    dirty_html = "<p>نص عادي <script>alert(\'XSS\');</script> <b>وخط عريض</b></p><img src=\'invalid\' onerror=\'alert(\'error\')\'>"
    clean_html = security_manager.sanitize_html(dirty_html)
    print(f"Original HTML: {dirty_html}")
    print(f"Sanitized HTML: {clean_html}")
    
    # --- اختبار كلمات المرور ---
    print("\n--- اختبار كلمات المرور ---")
    password = "P@sswOrd123!"
    hashed_password = security_manager.hash_password(password)
    print(f"Hashed password: {hashed_password}")
    print(f"Verify correct password: {security_manager.verify_password(hashed_password, password)}")
    print(f"Verify incorrect password: {security_manager.verify_password(hashed_password, \"wrongpassword\")}")
    
    # --- اختبار تسجيل الأحداث ---
    print("\n--- اختبار تسجيل الأحداث ---")
    security_manager.log_security_event("LOGIN_FAILURE", "محاولة تسجيل دخول فاشلة للمستخدم testuser", user_id="testuser", ip_address="192.168.1.100")

