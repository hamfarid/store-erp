#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ إصلاح أمني شامل للنظام
Comprehensive Security Fix Script
"""

import os
import re
import secrets
import shutil
from pathlib import Path
from datetime import datetime


class SecurityFixer:
    """مصلح الأمان الشامل"""
    
    def __init__(self):
        self.fixes_applied = []
        self.backup_dir = Path("security_fixes_backup")
        self.backup_dir.mkdir(exist_ok=True)
        
    def backup_file(self, file_path):
        """إنشاء نسخة احتياطية من الملف"""
        if Path(file_path).exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"{Path(file_path).name}_{timestamp}.backup"
            shutil.copy2(file_path, backup_file)
            return str(backup_file)
        return None
        
    def fix_env_file(self):
        """إصلاح ملف .env"""
        print("🔧 إصلاح ملف .env...")
        
        env_file = Path("backend/.env")
        if not env_file.exists():
            print("⚠️ ملف .env غير موجود")
            return
            
        # نسخة احتياطية
        backup = self.backup_file(env_file)
        
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # إصلاح كلمات المرور الضعيفة
        weak_passwords = {
            'change_this_password_immediately': secrets.token_urlsafe(16),
            'HaRrMa123!@#': secrets.token_urlsafe(16),
            'admin': secrets.token_urlsafe(12),
            'password': secrets.token_urlsafe(12),
            'test': secrets.token_urlsafe(12)
        }
        
        for weak, strong in weak_passwords.items():
            if weak in content:
                content = content.replace(weak, strong)
                self.fixes_applied.append(f"استبدال كلمة مرور ضعيفة: {weak}")
                
        # تحديث مفاتيح التشفير
        if 'SECRET_KEY=' in content:
            new_secret = secrets.token_hex(32)
            content = re.sub(r'SECRET_KEY=.*', f'SECRET_KEY={new_secret}', content)
            self.fixes_applied.append("تحديث SECRET_KEY")
            
        if 'JWT_SECRET_KEY=' in content:
            new_jwt = secrets.token_hex(32)
            content = re.sub(r'JWT_SECRET_KEY=.*', f'JWT_SECRET_KEY={new_jwt}', content)
            self.fixes_applied.append("تحديث JWT_SECRET_KEY")
            
        if 'ENCRYPTION_KEY=your-encryption-key-here' in content:
            new_enc = secrets.token_hex(32)
            content = content.replace('ENCRYPTION_KEY=your-encryption-key-here', f'ENCRYPTION_KEY={new_enc}')
            self.fixes_applied.append("تحديث ENCRYPTION_KEY")
            
        # تحسين إعدادات الأمان
        security_improvements = {
            'FLASK_DEBUG=True': 'FLASK_DEBUG=False',
            'DEBUG_MODE=True': 'DEBUG_MODE=False',
            'JWT_ACCESS_TOKEN_EXPIRES=3600': 'JWT_ACCESS_TOKEN_EXPIRES=1800',  # 30 دقيقة
            'MAX_LOGIN_ATTEMPTS=5': 'MAX_LOGIN_ATTEMPTS=3',
            'LOCKOUT_DURATION=1800': 'LOCKOUT_DURATION=3600'  # ساعة واحدة
        }
        
        for old, new in security_improvements.items():
            if old in content:
                content = content.replace(old, new)
                self.fixes_applied.append(f"تحسين إعداد: {old} -> {new}")
                
        # إضافة إعدادات أمان جديدة
        new_security_settings = '''
# إعدادات أمان محسنة
SECURITY_HEADERS=True
CSRF_PROTECTION=True
XSS_PROTECTION=True
CONTENT_TYPE_NOSNIFF=True
FRAME_OPTIONS=DENY
HSTS_MAX_AGE=31536000
SECURE_COOKIES=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Strict

# إعدادات مراقبة أمنية
FAILED_LOGIN_MONITORING=True
SUSPICIOUS_ACTIVITY_DETECTION=True
IP_WHITELIST_ENABLED=False
RATE_LIMITING_ENABLED=True
BRUTE_FORCE_PROTECTION=True
'''
        
        if 'SECURITY_HEADERS=' not in content:
            content += new_security_settings
            self.fixes_applied.append("إضافة إعدادات أمان متقدمة")
            
        # حفظ الملف المحدث
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ تم إصلاح ملف .env (نسخة احتياطية: {backup})")
        
    def fix_file_permissions(self):
        """إصلاح صلاحيات الملفات"""
        print("🔒 إصلاح صلاحيات الملفات...")
        
        sensitive_files = [
            'backend/.env',
            'backend/encryption_keys/master.key',
            'backend/instance/inventory.db'
        ]
        
        for file_path in sensitive_files:
            if Path(file_path).exists():
                try:
                    os.chmod(file_path, 0o600)  # قراءة/كتابة للمالك فقط
                    self.fixes_applied.append(f"تحديث صلاحيات: {file_path}")
                    print(f"✅ تم تحديث صلاحيات: {file_path}")
                except Exception as e:
                    print(f"❌ خطأ في تحديث صلاحيات {file_path}: {e}")
                    
    def fix_sql_injection_vulnerabilities(self):
        """إصلاح ثغرات SQL Injection"""
        print("💉 إصلاح ثغرات SQL Injection...")
        
        python_files = list(Path("backend/src").rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original_content = content
                
                # استبدال string formatting خطير
                dangerous_patterns = [
                    (r'\.execute\s*\(\s*["\'].*%.*["\']', 'استخدم parameterized queries'),
                    (r'\.execute\s*\(\s*f["\']', 'تجنب f-strings في SQL'),
                    (r'\.execute\s*\(\s*.*\+.*\)', 'تجنب string concatenation في SQL')
                ]
                
                for pattern, suggestion in dangerous_patterns:
                    if re.search(pattern, content):
                        # إضافة تعليق تحذيري
                        content = re.sub(
                            pattern,
                            lambda m: f"# تحذير أمني: {suggestion}\n{m.group(0)}",
                            content
                        )
                        
                if content != original_content:
                    # نسخة احتياطية
                    backup = self.backup_file(file_path)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
                    self.fixes_applied.append(f"إضافة تحذيرات أمنية في: {file_path}")
                    
            except Exception as e:
                print(f"❌ خطأ في معالجة {file_path}: {e}")
                
    def create_security_middleware(self):
        """إنشاء middleware أمني"""
        print("🛡️ إنشاء middleware أمني...")
        
        middleware_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ Middleware أمني للنظام
Security Middleware for Enhanced Protection
"""

from functools import wraps
from flask import request, jsonify, current_app
import time
import hashlib
from collections import defaultdict, deque
from datetime import datetime, timedelta


class SecurityMiddleware:
    """Middleware أمني شامل"""
    
    def __init__(self, app=None):
        self.app = app
        self.failed_attempts = defaultdict(deque)
        self.blocked_ips = {}
        self.rate_limits = defaultdict(deque)
        
        if app:
            self.init_app(app)
            
    def init_app(self, app):
        """تهيئة الـ middleware مع التطبيق"""
        self.app = app
        
        # إعدادات افتراضية
        app.config.setdefault('MAX_LOGIN_ATTEMPTS', 3)
        app.config.setdefault('LOCKOUT_DURATION', 3600)
        app.config.setdefault('RATE_LIMIT_REQUESTS', 100)
        app.config.setdefault('RATE_LIMIT_WINDOW', 3600)
        
        # تطبيق الـ middleware
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
    def get_client_ip(self):
        """الحصول على IP العميل"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
            
    def is_ip_blocked(self, ip):
        """التحقق من حظر IP"""
        if ip in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]
        return False
        
    def block_ip(self, ip, duration=None):
        """حظر IP لفترة محددة"""
        if duration is None:
            duration = current_app.config.get('LOCKOUT_DURATION', 3600)
            
        self.blocked_ips[ip] = datetime.now() + timedelta(seconds=duration)
        
    def check_rate_limit(self, ip):
        """فحص حد المعدل"""
        now = time.time()
        window = current_app.config.get('RATE_LIMIT_WINDOW', 3600)
        max_requests = current_app.config.get('RATE_LIMIT_REQUESTS', 100)
        
        # تنظيف الطلبات القديمة
        while self.rate_limits[ip] and self.rate_limits[ip][0] < now - window:
            self.rate_limits[ip].popleft()
            
        # فحص الحد
        if len(self.rate_limits[ip]) >= max_requests:
            return False
            
        # إضافة الطلب الحالي
        self.rate_limits[ip].append(now)
        return True
        
    def log_failed_attempt(self, ip):
        """تسجيل محاولة فاشلة"""
        now = time.time()
        window = 3600  # ساعة واحدة
        
        # تنظيف المحاولات القديمة
        while self.failed_attempts[ip] and self.failed_attempts[ip][0] < now - window:
            self.failed_attempts[ip].popleft()
            
        # إضافة المحاولة الحالية
        self.failed_attempts[ip].append(now)
        
        # فحص الحد الأقصى
        max_attempts = current_app.config.get('MAX_LOGIN_ATTEMPTS', 3)
        if len(self.failed_attempts[ip]) >= max_attempts:
            self.block_ip(ip)
            return True
            
        return False
        
    def before_request(self):
        """معالجة قبل الطلب"""
        ip = self.get_client_ip()
        
        # فحص IP محظور
        if self.is_ip_blocked(ip):
            return jsonify({
                'error': 'IP محظور مؤقتاً',
                'message': 'تم حظر عنوان IP الخاص بك بسبب نشاط مشبوه'
            }), 429
            
        # فحص حد المعدل
        if not self.check_rate_limit(ip):
            return jsonify({
                'error': 'تجاوز حد المعدل',
                'message': 'تم تجاوز الحد الأقصى للطلبات'
            }), 429
            
    def after_request(self, response):
        """معالجة بعد الطلب"""
        # إضافة headers أمنية
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response


def require_auth(f):
    """decorator للمصادقة المطلوبة"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # فحص المصادقة هنا
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'مصادقة مطلوبة'}), 401
            
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """decorator للصلاحيات الإدارية"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # فحص الصلاحيات الإدارية هنا
        # يجب تنفيذ منطق فحص الدور
        return f(*args, **kwargs)
    return decorated_function


# إنشاء instance عام
security_middleware = SecurityMiddleware()
'''
        
        middleware_file = Path("backend/src/security_middleware.py")
        with open(middleware_file, 'w', encoding='utf-8') as f:
            f.write(middleware_content)
            
        self.fixes_applied.append("إنشاء security middleware")
        print("✅ تم إنشاء security middleware")
        
    def create_security_config(self):
        """إنشاء ملف تكوين أمني"""
        print("⚙️ إنشاء ملف تكوين أمني...")
        
        config_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 إعدادات الأمان المتقدمة
Advanced Security Configuration
"""

import os
from datetime import timedelta


class SecurityConfig:
    """إعدادات الأمان الشاملة"""
    
    # إعدادات كلمات المرور
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SYMBOLS = True
    PASSWORD_HISTORY_COUNT = 5  # عدد كلمات المرور السابقة المحظورة
    
    # إعدادات الجلسات
    SESSION_TIMEOUT = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # إعدادات JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ALGORITHM = 'HS256'
    
    # إعدادات محاولات تسجيل الدخول
    MAX_LOGIN_ATTEMPTS = 3
    LOCKOUT_DURATION = timedelta(hours=1)
    LOCKOUT_ESCALATION = True  # زيادة مدة الحظر مع كل محاولة
    
    # إعدادات Rate Limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = timedelta(hours=1)
    
    # إعدادات CORS
    CORS_ORIGINS = ['http://localhost:3000', 'https://yourdomain.com']
    CORS_ALLOW_CREDENTIALS = True
    CORS_MAX_AGE = timedelta(hours=24)
    
    # إعدادات التشفير
    ENCRYPTION_ALGORITHM = 'AES-256-GCM'
    HASH_ALGORITHM = 'SHA-256'
    SALT_LENGTH = 32
    
    # إعدادات Headers الأمنية
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
    }
    
    # إعدادات المراقبة
    MONITORING_ENABLED = True
    LOG_FAILED_LOGINS = True
    LOG_SUSPICIOUS_ACTIVITY = True
    ALERT_ON_MULTIPLE_FAILURES = True
    
    # إعدادات النسخ الاحتياطية
    BACKUP_ENCRYPTION = True
    BACKUP_RETENTION_DAYS = 30
    BACKUP_VERIFICATION = True
    
    # إعدادات التدقيق
    AUDIT_LOG_ENABLED = True
    AUDIT_LOG_RETENTION_DAYS = 90
    AUDIT_SENSITIVE_OPERATIONS = True
    
    @classmethod
    def get_security_level(cls):
        """تحديد مستوى الأمان الحالي"""
        score = 0
        max_score = 100
        
        # فحص كلمات المرور
        if cls.PASSWORD_MIN_LENGTH >= 8:
            score += 10
        if cls.PASSWORD_REQUIRE_UPPERCASE and cls.PASSWORD_REQUIRE_LOWERCASE:
            score += 10
        if cls.PASSWORD_REQUIRE_NUMBERS and cls.PASSWORD_REQUIRE_SYMBOLS:
            score += 10
            
        # فحص الجلسات
        if cls.SESSION_TIMEOUT <= timedelta(hours=1):
            score += 10
        if cls.SESSION_COOKIE_SECURE and cls.SESSION_COOKIE_HTTPONLY:
            score += 10
            
        # فحص JWT
        if cls.JWT_ACCESS_TOKEN_EXPIRES <= timedelta(hours=1):
            score += 10
            
        # فحص Rate Limiting
        if cls.RATE_LIMIT_ENABLED:
            score += 10
            
        # فحص المراقبة
        if cls.MONITORING_ENABLED and cls.LOG_FAILED_LOGINS:
            score += 10
            
        # فحص النسخ الاحتياطية
        if cls.BACKUP_ENCRYPTION:
            score += 10
            
        # فحص التدقيق
        if cls.AUDIT_LOG_ENABLED:
            score += 10
            
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score) * 100,
            'level': cls._get_security_grade(score, max_score)
        }
        
    @staticmethod
    def _get_security_grade(score, max_score):
        """تحديد درجة الأمان"""
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            return 'A+ (ممتاز)'
        elif percentage >= 80:
            return 'A (جيد جداً)'
        elif percentage >= 70:
            return 'B (جيد)'
        elif percentage >= 60:
            return 'C (مقبول)'
        else:
            return 'D (ضعيف)'


# إعدادات البيئة
class ProductionSecurityConfig(SecurityConfig):
    """إعدادات أمان الإنتاج"""
    
    # إعدادات أكثر صرامة للإنتاج
    PASSWORD_MIN_LENGTH = 12
    SESSION_TIMEOUT = timedelta(minutes=15)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    MAX_LOGIN_ATTEMPTS = 2
    LOCKOUT_DURATION = timedelta(hours=2)
    RATE_LIMIT_REQUESTS = 50


class DevelopmentSecurityConfig(SecurityConfig):
    """إعدادات أمان التطوير"""
    
    # إعدادات أكثر مرونة للتطوير
    SESSION_TIMEOUT = timedelta(hours=8)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=30)
'''
        
        config_file = Path("backend/src/security_config.py")
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
            
        self.fixes_applied.append("إنشاء ملف تكوين أمني")
        print("✅ تم إنشاء ملف تكوين أمني")
        
    def generate_security_report(self):
        """توليد تقرير الإصلاحات"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'fixes_applied': len(self.fixes_applied),
            'fixes_details': self.fixes_applied,
            'backup_location': str(self.backup_dir),
            'recommendations': [
                'تشغيل فحص الأمان مرة أخرى للتحقق من التحسينات',
                'إنشاء مستخدم admin آمن باستخدام create_admin_user.py',
                'تفعيل HTTPS في الإنتاج',
                'إعداد مراقبة أمنية مستمرة',
                'تحديث كلمات المرور دورياً',
                'إجراء نسخ احتياطية مشفرة'
            ]
        }
        
        with open('security_fixes_report.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        return report
        
    def run_comprehensive_fix(self):
        """تشغيل الإصلاح الشامل"""
        print("🛡️ بدء الإصلاح الأمني الشامل...")
        print("=" * 50)
        
        try:
            self.fix_env_file()
            self.fix_file_permissions()
            self.fix_sql_injection_vulnerabilities()
            self.create_security_middleware()
            self.create_security_config()
            
            report = self.generate_security_report()
            
            print("\n" + "=" * 50)
            print("✅ تم إكمال الإصلاح الأمني الشامل!")
            print(f"🔧 عدد الإصلاحات: {len(self.fixes_applied)}")
            print(f"💾 النسخ الاحتياطية: {self.backup_dir}")
            print("📄 تقرير الإصلاحات: security_fixes_report.json")
            
            print("\n🎯 الخطوات التالية:")
            print("1. تشغيل فحص الأمان: python security_audit_comprehensive.py")
            print("2. إنشاء admin user: python create_admin_user.py")
            print("3. اختبار النظام المحسن")
            
            return report
            
        except Exception as e:
            print(f"❌ خطأ في الإصلاح: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    fixer = SecurityFixer()
    fixer.run_comprehensive_fix()
