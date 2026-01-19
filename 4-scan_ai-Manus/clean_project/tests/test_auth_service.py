# File: /home/ubuntu/clean_project/tests/test_auth_service.py
"""
مسار الملف: /home/ubuntu/clean_project/tests/test_auth_service.py

اختبارات شاملة لخدمة المصادقة والتفويض
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# إضافة مسار src إلى Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from auth_service import AuthService, hash_password, verify_password
from database_models import create_database, get_session, User

class TestAuthService(unittest.TestCase):
    """اختبارات خدمة المصادقة"""
    
    def setUp(self):
        """إعداد البيانات للاختبار"""
        self.auth_service = AuthService(secret_key="test_secret_key")
        self.engine = create_database("sqlite:///:memory:")  # قاعدة بيانات في الذاكرة للاختبار
        self.session = get_session(self.engine)
        
        # إنشاء مستخدم تجريبي
        self.test_user = User(
            username="test_user",
            email="test@example.com",
            password_hash=hash_password("test_password"),
            full_name="مستخدم تجريبي",
            is_active=True,
            is_admin=False
        )
        self.session.add(self.test_user)
        self.session.commit()
    
    def tearDown(self):
        """تنظيف البيانات بعد الاختبار"""
        self.session.close()
    
    def test_hash_password(self):
        """اختبار تشفير كلمة المرور"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(password, hashed)
        self.assertTrue(len(hashed) > 0)
    
    def test_verify_password(self):
        """اختبار التحقق من كلمة المرور"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        # كلمة مرور صحيحة
        self.assertTrue(verify_password(password, hashed))
        
        # كلمة مرور خاطئة
        self.assertFalse(verify_password("wrong_password", hashed))
    
    def test_create_token(self):
        """اختبار إنشاء الرمز المميز"""
        token = self.auth_service.create_token(1, "test_user", False)
        
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)
    
    def test_verify_token_valid(self):
        """اختبار التحقق من رمز صحيح"""
        token = self.auth_service.create_token(1, "test_user", False)
        result = self.auth_service.verify_token(token)
        
        self.assertTrue(result["valid"])
        self.assertEqual(result["user_id"], 1)
        self.assertEqual(result["username"], "test_user")
        self.assertFalse(result["is_admin"])
    
    def test_verify_token_invalid(self):
        """اختبار التحقق من رمز غير صحيح"""
        invalid_token = "invalid.token.here"
        result = self.auth_service.verify_token(invalid_token)
        
        self.assertFalse(result["valid"])
        self.assertIn("message", result)
    
    def test_verify_token_expired(self):
        """اختبار التحقق من رمز منتهي الصلاحية"""
        # إنشاء خدمة مصادقة برمز ينتهي فوراً
        short_auth = AuthService(secret_key="test_key", token_expiry_hours=-1)
        token = short_auth.create_token(1, "test_user", False)
        
        result = short_auth.verify_token(token)
        self.assertFalse(result["valid"])

class TestDatabaseModels(unittest.TestCase):
    """اختبارات نماذج قاعدة البيانات"""
    
    def setUp(self):
        """إعداد قاعدة البيانات للاختبار"""
        self.engine = create_database("sqlite:///:memory:")
        self.session = get_session(self.engine)
    
    def tearDown(self):
        """تنظيف البيانات"""
        self.session.close()
    
    def test_user_creation(self):
        """اختبار إنشاء مستخدم"""
        user = User(
            username="new_user",
            email="new@example.com",
            password_hash=hash_password("password123"),
            full_name="مستخدم جديد",
            is_active=True,
            is_admin=False
        )
        
        self.session.add(user)
        self.session.commit()
        
        # التحقق من الحفظ
        saved_user = self.session.query(User).filter(User.username == "new_user").first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, "new@example.com")
        self.assertEqual(saved_user.full_name, "مستخدم جديد")
    
    def test_user_unique_constraints(self):
        """اختبار قيود الفرادة للمستخدم"""
        # إنشاء مستخدم أول
        user1 = User(
            username="unique_user",
            email="unique@example.com",
            password_hash=hash_password("password123"),
            full_name="مستخدم فريد",
            is_active=True
        )
        self.session.add(user1)
        self.session.commit()
        
        # محاولة إنشاء مستخدم بنفس اسم المستخدم
        user2 = User(
            username="unique_user",  # نفس اسم المستخدم
            email="different@example.com",
            password_hash=hash_password("password123"),
            full_name="مستخدم آخر",
            is_active=True
        )
        self.session.add(user2)
        
        # يجب أن يفشل بسبب قيد الفرادة
        with self.assertRaises(Exception):
            self.session.commit()

if __name__ == '__main__':
    # تشغيل الاختبارات
    unittest.main(verbosity=2)

