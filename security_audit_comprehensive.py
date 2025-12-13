#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 فحص أمان النظام الشامل
Comprehensive Security Audit Script
"""

import os
import re
import json
import hashlib
import secrets
from datetime import datetime
from pathlib import Path


class SecurityAuditor:
    """فاحص الأمان الشامل"""
    
    def __init__(self):
        self.vulnerabilities = []
        self.recommendations = []
        self.security_score = 0
        self.max_score = 100
        
    def audit_passwords(self):
        """فحص كلمات المرور والمفاتيح"""
        print("🔍 فحص كلمات المرور والمفاتيح...")
        
        # فحص ملف .env
        env_file = Path("backend/.env")
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # فحص كلمات مرور ضعيفة
            weak_passwords = [
                'password', '123456', 'admin', 'root', 'test',
                'change_this_password_immediately'
            ]
            
            for weak in weak_passwords:
                if weak.lower() in content.lower():
                    self.vulnerabilities.append({
                        'type': 'weak_password',
                        'severity': 'high',
                        'description': f'كلمة مرور ضعيفة موجودة: {weak}',
                        'file': str(env_file)
                    })
                    
            # فحص مفاتيح التشفير
            if 'SECRET_KEY=' in content:
                secret_match = re.search(r'SECRET_KEY=(.+)', content)
                if secret_match:
                    secret = secret_match.group(1).strip()
                    if len(secret) < 32:
                        self.vulnerabilities.append({
                            'type': 'weak_secret',
                            'severity': 'high',
                            'description': 'مفتاح التشفير قصير جداً (أقل من 32 حرف)',
                            'file': str(env_file)
                        })
                        
        self.security_score += 15
        
    def audit_file_permissions(self):
        """فحص صلاحيات الملفات"""
        print("📁 فحص صلاحيات الملفات...")
        
        sensitive_files = [
            'backend/.env',
            'backend/encryption_keys/master.key',
            'backend/instance/inventory.db'
        ]
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                permissions = oct(stat.st_mode)[-3:]
                
                # يجب أن تكون الملفات الحساسة 600 (قراءة/كتابة للمالك فقط)
                if permissions != '600':
                    self.vulnerabilities.append({
                        'type': 'file_permissions',
                        'severity': 'medium',
                        'description': f'صلاحيات غير آمنة للملف: {file_path} ({permissions})',
                        'recommendation': 'chmod 600 ' + file_path
                    })
                    
        self.security_score += 10
        
    def audit_sql_injection(self):
        """فحص ثغرات SQL Injection"""
        print("💉 فحص ثغرات SQL Injection...")
        
        python_files = list(Path("backend/src").rglob("*.py"))
        
        dangerous_patterns = [
            r'\.execute\s*\(\s*["\'].*%.*["\']',  # String formatting in SQL
            r'\.execute\s*\(\s*f["\']',  # f-strings in SQL
            r'\.execute\s*\(\s*.*\+.*\)',  # String concatenation
        ]
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in dangerous_patterns:
                    if re.search(pattern, content):
                        self.vulnerabilities.append({
                            'type': 'sql_injection',
                            'severity': 'critical',
                            'description': f'احتمالية SQL Injection في: {file_path}',
                            'pattern': pattern
                        })
            except Exception:
                continue
                
        self.security_score += 20
        
    def audit_xss_vulnerabilities(self):
        """فحص ثغرات XSS"""
        print("🌐 فحص ثغرات XSS...")
        
        # فحص ملفات React
        jsx_files = list(Path("frontend/src").rglob("*.jsx"))
        
        dangerous_patterns = [
            r'dangerouslySetInnerHTML',
            r'innerHTML\s*=',
            r'eval\s*\(',
        ]
        
        for file_path in jsx_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in dangerous_patterns:
                    if re.search(pattern, content):
                        self.vulnerabilities.append({
                            'type': 'xss_vulnerability',
                            'severity': 'high',
                            'description': f'احتمالية XSS في: {file_path}',
                            'pattern': pattern
                        })
            except Exception:
                continue
                
        self.security_score += 15
        
    def audit_authentication(self):
        """فحص نظام المصادقة"""
        print("🔐 فحص نظام المصادقة...")
        
        # فحص إعدادات JWT
        env_file = Path("backend/.env")
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # فحص انتهاء صلاحية JWT
            if 'JWT_ACCESS_TOKEN_EXPIRES=' in content:
                expires_match = re.search(r'JWT_ACCESS_TOKEN_EXPIRES=(\d+)', content)
                if expires_match:
                    expires = int(expires_match.group(1))
                    if expires > 86400:  # أكثر من 24 ساعة
                        self.vulnerabilities.append({
                            'type': 'jwt_long_expiry',
                            'severity': 'medium',
                            'description': f'انتهاء صلاحية JWT طويل جداً: {expires} ثانية',
                            'recommendation': 'تقليل مدة انتهاء الصلاحية إلى 3600 ثانية (ساعة واحدة)'
                        })
                        
        self.security_score += 15
        
    def audit_cors_settings(self):
        """فحص إعدادات CORS"""
        print("🌍 فحص إعدادات CORS...")
        
        # فحص ملفات Flask
        python_files = list(Path("backend").rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # فحص CORS مفتوح للجميع
                if re.search(r'CORS.*origins.*\*', content):
                    self.vulnerabilities.append({
                        'type': 'open_cors',
                        'severity': 'medium',
                        'description': f'CORS مفتوح للجميع في: {file_path}',
                        'recommendation': 'تحديد domains محددة بدلاً من *'
                    })
            except Exception:
                continue
                
        self.security_score += 10
        
    def audit_error_handling(self):
        """فحص معالجة الأخطاء"""
        print("⚠️ فحص معالجة الأخطاء...")
        
        python_files = list(Path("backend/src").rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # فحص except عام بدون تحديد
                if re.search(r'except\s*:', content):
                    self.vulnerabilities.append({
                        'type': 'generic_exception',
                        'severity': 'low',
                        'description': f'معالجة أخطاء عامة في: {file_path}',
                        'recommendation': 'تحديد نوع الاستثناء المطلوب'
                    })
                    
                # فحص طباعة معلومات حساسة في الأخطاء
                if re.search(r'print.*password|print.*secret|print.*key', content, re.IGNORECASE):
                    self.vulnerabilities.append({
                        'type': 'sensitive_info_leak',
                        'severity': 'high',
                        'description': f'تسريب معلومات حساسة في: {file_path}',
                        'recommendation': 'إزالة طباعة المعلومات الحساسة'
                    })
            except Exception:
                continue
                
        self.security_score += 10
        
    def audit_dependencies(self):
        """فحص التبعيات الأمنية"""
        print("📦 فحص التبعيات الأمنية...")
        
        # فحص requirements.txt
        req_file = Path("backend/requirements.txt")
        if req_file.exists():
            with open(req_file, 'r', encoding='utf-8') as f:
                requirements = f.read()
                
            # مكتبات معروفة بثغرات أمنية
            vulnerable_packages = [
                'flask==0.12',  # إصدارات قديمة
                'requests==2.6',
                'urllib3==1.24',
                'jinja2==2.10'
            ]
            
            for package in vulnerable_packages:
                if package in requirements:
                    self.vulnerabilities.append({
                        'type': 'vulnerable_dependency',
                        'severity': 'high',
                        'description': f'مكتبة بثغرة أمنية: {package}',
                        'recommendation': 'تحديث إلى أحدث إصدار آمن'
                    })
                    
        self.security_score += 15
        
    def generate_recommendations(self):
        """توليد التوصيات الأمنية"""
        print("💡 توليد التوصيات الأمنية...")
        
        self.recommendations = [
            {
                'category': 'كلمات المرور',
                'items': [
                    'استخدام كلمات مرور قوية (12+ حرف)',
                    'تفعيل المصادقة الثنائية',
                    'تغيير كلمات المرور دورياً',
                    'استخدام مدير كلمات مرور'
                ]
            },
            {
                'category': 'التشفير',
                'items': [
                    'استخدام HTTPS في الإنتاج',
                    'تشفير قاعدة البيانات',
                    'استخدام مفاتيح تشفير قوية',
                    'تدوير المفاتيح دورياً'
                ]
            },
            {
                'category': 'المراقبة',
                'items': [
                    'تسجيل جميع محاولات تسجيل الدخول',
                    'مراقبة الأنشطة المشبوهة',
                    'إعداد تنبيهات أمنية',
                    'مراجعة السجلات دورياً'
                ]
            },
            {
                'category': 'النسخ الاحتياطية',
                'items': [
                    'نسخ احتياطية مشفرة',
                    'اختبار استعادة البيانات',
                    'تخزين النسخ في مواقع متعددة',
                    'جدولة النسخ الاحتياطية'
                ]
            }
        ]
        
    def calculate_final_score(self):
        """حساب النقاط النهائية"""
        # خصم نقاط حسب شدة الثغرات
        deductions = 0
        for vuln in self.vulnerabilities:
            if vuln['severity'] == 'critical':
                deductions += 20
            elif vuln['severity'] == 'high':
                deductions += 10
            elif vuln['severity'] == 'medium':
                deductions += 5
            elif vuln['severity'] == 'low':
                deductions += 2
                
        self.security_score = max(0, self.security_score - deductions)
        
    def generate_report(self):
        """توليد تقرير الأمان"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'security_score': self.security_score,
            'max_score': self.max_score,
            'grade': self.get_security_grade(),
            'vulnerabilities_count': len(self.vulnerabilities),
            'vulnerabilities': self.vulnerabilities,
            'recommendations': self.recommendations,
            'summary': {
                'critical': len([v for v in self.vulnerabilities if v['severity'] == 'critical']),
                'high': len([v for v in self.vulnerabilities if v['severity'] == 'high']),
                'medium': len([v for v in self.vulnerabilities if v['severity'] == 'medium']),
                'low': len([v for v in self.vulnerabilities if v['severity'] == 'low'])
            }
        }
        
        # حفظ التقرير
        with open('security_audit_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        return report
        
    def get_security_grade(self):
        """تحديد درجة الأمان"""
        if self.security_score >= 90:
            return 'A+ (ممتاز)'
        elif self.security_score >= 80:
            return 'A (جيد جداً)'
        elif self.security_score >= 70:
            return 'B (جيد)'
        elif self.security_score >= 60:
            return 'C (مقبول)'
        elif self.security_score >= 50:
            return 'D (ضعيف)'
        else:
            return 'F (فاشل)'
            
    def run_full_audit(self):
        """تشغيل الفحص الشامل"""
        print("🔒 بدء فحص الأمان الشامل...")
        print("=" * 50)
        
        self.audit_passwords()
        self.audit_file_permissions()
        self.audit_sql_injection()
        self.audit_xss_vulnerabilities()
        self.audit_authentication()
        self.audit_cors_settings()
        self.audit_error_handling()
        self.audit_dependencies()
        self.generate_recommendations()
        self.calculate_final_score()
        
        report = self.generate_report()
        
        print("\n" + "=" * 50)
        print("📊 نتائج فحص الأمان:")
        print(f"🎯 النقاط: {self.security_score}/{self.max_score}")
        print(f"📈 الدرجة: {self.get_security_grade()}")
        print(f"⚠️ الثغرات: {len(self.vulnerabilities)}")
        print(f"🔴 حرجة: {report['summary']['critical']}")
        print(f"🟠 عالية: {report['summary']['high']}")
        print(f"🟡 متوسطة: {report['summary']['medium']}")
        print(f"🟢 منخفضة: {report['summary']['low']}")
        print("\n📄 تم حفظ التقرير في: security_audit_report.json")
        
        return report


if __name__ == "__main__":
    auditor = SecurityAuditor()
    auditor.run_full_audit()
