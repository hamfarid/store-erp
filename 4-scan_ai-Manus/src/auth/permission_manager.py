#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة صلاحيات المستخدمين وقواعد البيانات
يوفر آليات للتحكم في وصول المستخدمين إلى قواعد البيانات والوظائف المختلفة
"""

import os
import json
import logging
import datetime
import hashlib
import secrets
import re
import jwt
from pathlib import Path
import yaml
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class PermissionManager:
    """مدير صلاحيات المستخدمين وقواعد البيانات"""
    
    # تعريف مستويات الصلاحيات
    PERMISSION_LEVELS = {
        'admin': 100,  # المدير العام
        'department_manager': 80,  # مدير قسم الدعم والتطوير
        'support_engineer': 60,  # مهندس الدعم الفني
        'development_engineer': 50,  # مهندس التطوير
        'user': 10,  # مستخدم عادي
        'guest': 1  # ضيف
    }
    
    # تعريف الصلاحيات المتاحة
    AVAILABLE_PERMISSIONS = {
        # صلاحيات قواعد البيانات
        'db_operational_read': 'قراءة قاعدة البيانات التشغيلية',
        'db_operational_write': 'كتابة قاعدة البيانات التشغيلية',
        'db_employee_training_read': 'قراءة قاعدة بيانات تدريب الموظفين',
        'db_employee_training_write': 'كتابة قاعدة بيانات تدريب الموظفين',
        'db_system_training_read': 'قراءة قاعدة بيانات تدريب النظام',
        'db_system_training_write': 'كتابة قاعدة بيانات تدريب النظام',
        'db_backup_read': 'قراءة قاعدة بيانات النسخ الاحتياطي',
        'db_backup_write': 'كتابة قاعدة بيانات النسخ الاحتياطي',
        
        # صلاحيات وحدات النظام
        'disease_detection_access': 'الوصول إلى وحدة الكشف عن الأمراض',
        'disease_detection_admin': 'إدارة وحدة الكشف عن الأمراض',
        'nutrient_analysis_access': 'الوصول إلى وحدة تحليل نقص العناصر',
        'nutrient_analysis_admin': 'إدارة وحدة تحليل نقص العناصر',
        'plant_breeding_access': 'الوصول إلى وحدة التهجين',
        'plant_breeding_admin': 'إدارة وحدة التهجين',
        'treatment_recommendation_access': 'الوصول إلى وحدة توصيات العلاج',
        'treatment_recommendation_admin': 'إدارة وحدة توصيات العلاج',
        'farm_management_access': 'الوصول إلى وحدة إدارة المزارع',
        'farm_management_admin': 'إدارة وحدة إدارة المزارع',
        'nursery_management_access': 'الوصول إلى وحدة إدارة المشاتل',
        'nursery_management_admin': 'إدارة وحدة إدارة المشاتل',
        'cost_management_access': 'الوصول إلى وحدة إدارة التكاليف',
        'cost_management_admin': 'إدارة وحدة إدارة التكاليف',
        'variety_comparison_access': 'الوصول إلى وحدة مقارنة الأصناف',
        'variety_comparison_admin': 'إدارة وحدة مقارنة الأصناف',
        
        # صلاحيات إدارة النظام
        'user_management': 'إدارة المستخدمين',
        'role_management': 'إدارة الأدوار',
        'system_configuration': 'تكوين النظام',
        'backup_management': 'إدارة النسخ الاحتياطي',
        'audit_log_view': 'عرض سجلات التدقيق',
        'ai_agent_premium': 'استخدام وكيل الذكاء الاصطناعي المدفوع',
        'ai_agent_free': 'استخدام وكيل الذكاء الاصطناعي المجاني',
        'learning_management': 'إدارة التعلم',
        'trusted_sources_management': 'إدارة المصادر الموثوقة',
        'keyword_management': 'إدارة الكلمات المفتاحية',
        'reporting_access': 'الوصول إلى التقارير',
        'reporting_admin': 'إدارة التقارير'
    }
    
    # تعريف الأدوار الافتراضية وصلاحياتها
    DEFAULT_ROLES = {
        'admin': {
            'description': 'المدير العام مع كامل الصلاحيات',
            'permissions': list(AVAILABLE_PERMISSIONS.keys())
        },
        'department_manager': {
            'description': 'مدير قسم الدعم والتطوير',
            'permissions': [
                'db_operational_read', 'db_employee_training_read', 'db_employee_training_write',
                'db_system_training_read', 'db_backup_read',
                'disease_detection_access', 'disease_detection_admin',
                'nutrient_analysis_access', 'nutrient_analysis_admin',
                'plant_breeding_access', 'plant_breeding_admin',
                'treatment_recommendation_access', 'treatment_recommendation_admin',
                'farm_management_access', 'farm_management_admin',
                'nursery_management_access', 'nursery_management_admin',
                'cost_management_access', 'cost_management_admin',
                'variety_comparison_access', 'variety_comparison_admin',
                'user_management', 'role_management',
                'audit_log_view', 'ai_agent_premium', 'ai_agent_free',
                'learning_management', 'trusted_sources_management',
                'keyword_management', 'reporting_access', 'reporting_admin'
            ]
        },
        'support_engineer': {
            'description': 'مهندس الدعم الفني',
            'permissions': [
                'db_operational_read', 'db_employee_training_read',
                'disease_detection_access', 'nutrient_analysis_access',
                'plant_breeding_access', 'treatment_recommendation_access',
                'farm_management_access', 'nursery_management_access',
                'cost_management_access', 'variety_comparison_access',
                'ai_agent_premium', 'ai_agent_free',
                'reporting_access'
            ]
        },
        'development_engineer': {
            'description': 'مهندس التطوير',
            'permissions': [
                'db_operational_read', 'db_system_training_read', 'db_system_training_write',
                'disease_detection_access', 'nutrient_analysis_access',
                'plant_breeding_access', 'treatment_recommendation_access',
                'farm_management_access', 'nursery_management_access',
                'cost_management_access', 'variety_comparison_access',
                'ai_agent_premium', 'ai_agent_free',
                'learning_management', 'trusted_sources_management',
                'keyword_management', 'reporting_access'
            ]
        },
        'user': {
            'description': 'مستخدم عادي',
            'permissions': [
                'disease_detection_access', 'nutrient_analysis_access',
                'plant_breeding_access', 'treatment_recommendation_access',
                'farm_management_access', 'nursery_management_access',
                'cost_management_access', 'variety_comparison_access',
                'ai_agent_free', 'reporting_access'
            ]
        },
        'guest': {
            'description': 'ضيف',
            'permissions': [
                'disease_detection_access', 'nutrient_analysis_access',
                'ai_agent_free'
            ]
        }
    }
    
    def __init__(self, db_manager, config_path=None):
        """تهيئة مدير الصلاحيات"""
        self.logger = logging.getLogger(__name__)
        self.db_manager = db_manager
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'permissions.yaml')
        self.config = self._load_config()
        self.jwt_secret = os.environ.get('JWT_SECRET', secrets.token_hex(32))
        self.jwt_expiry = int(os.environ.get('JWT_EXPIRY', 86400))  # 24 ساعة افتراضيًا
        self.initialize_roles()
    
    def _load_config(self):
        """تحميل ملف التكوين الخاص بالصلاحيات"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"خطأ في تحميل ملف التكوين: {e}")
            # إعداد تكوين افتراضي
            return {
                'roles': self.DEFAULT_ROLES,
                'countries': {
                    'مصر': {
                        'code': 'EG',
                        'companies': ['شركة الزراعة المتقدمة', 'شركة الإنتاج الزراعي', 'شركة البذور المحسنة']
                    },
                    'السعودية': {
                        'code': 'SA',
                        'companies': ['شركة الزراعة السعودية', 'شركة الواحات الزراعية', 'شركة الخيرات الزراعية']
                    },
                    'الإمارات': {
                        'code': 'AE',
                        'companies': ['شركة الزراعة الإماراتية', 'شركة الخليج للزراعة', 'شركة الإمارات للإنتاج الزراعي']
                    }
                },
                'password_policy': {
                    'min_length': 8,
                    'require_uppercase': True,
                    'require_lowercase': True,
                    'require_numbers': True,
                    'require_special_chars': True,
                    'max_age_days': 90,
                    'history_count': 5
                },
                'session': {
                    'timeout_minutes': 30,
                    'max_concurrent_sessions': 3
                }
            }
    
    def initialize_roles(self):
        """تهيئة الأدوار في قاعدة البيانات"""
        try:
            # التحقق من وجود الأدوار في قاعدة البيانات
            roles = self.db_manager.fetch_all('operational', 'SELECT name FROM roles')
            existing_roles = [role[0] for role in roles]
            
            # إضافة الأدوار الافتراضية إذا لم تكن موجودة
            for role_name, role_data in self.config['roles'].items():
                if role_name not in existing_roles:
                    self.db_manager.insert('operational', 'roles', {
                        'name': role_name,
                        'description': role_data['description'],
                        'permissions': json.dumps(role_data['permissions'])
                    })
                    self.logger.info(f"تم إضافة الدور {role_name} إلى قاعدة البيانات")
            
            # إضافة الدول والشركات إذا لم تكن موجودة
            for country_name, country_data in self.config['countries'].items():
                # التحقق من وجود الدولة
                country = self.db_manager.fetch_one('operational', 'SELECT id FROM countries WHERE name = ?', (country_name,))
                
                if country:
                    country_id = country[0]
                else:
                    country_id = self.db_manager.insert('operational', 'countries', {
                        'name': country_name,
                        'code': country_data['code'],
                        'is_active': 1
                    })
                    self.logger.info(f"تم إضافة الدولة {country_name} إلى قاعدة البيانات")
                
                # إضافة الشركات
                for company_name in country_data['companies']:
                    company = self.db_manager.fetch_one('operational', 'SELECT id FROM companies WHERE name = ? AND country_id = ?', (company_name, country_id))
                    
                    if not company:
                        self.db_manager.insert('operational', 'companies', {
                            'name': company_name,
                            'country_id': country_id,
                            'description': f"شركة في {country_name}",
                            'is_active': 1
                        })
                        self.logger.info(f"تم إضافة الشركة {company_name} إلى قاعدة البيانات")
            
            # إضافة مستخدم المدير الافتراضي إذا لم يكن موجودًا
            admin_user = self.db_manager.fetch_one('operational', 'SELECT id FROM users WHERE username = ?', ('admin',))
            
            if not admin_user:
                # إنشاء كلمة مرور عشوائية آمنة للمدير
                admin_password = secrets.token_urlsafe(12)
                admin_password_hash = self._hash_password(admin_password)
                
                self.db_manager.insert('operational', 'users', {
                    'username': 'admin',
                    'password_hash': admin_password_hash,
                    'email': 'admin@example.com',
                    'role': 'admin',
                    'is_active': 1
                })
                
                self.logger.info(f"تم إنشاء مستخدم المدير الافتراضي. كلمة المرور: {admin_password}")
                print(f"تم إنشاء مستخدم المدير الافتراضي. كلمة المرور: {admin_password}")
            
            self.logger.info("تم تهيئة الأدوار والدول والشركات بنجاح")
        except Exception as e:
            self.logger.error(f"خطأ في تهيئة الأدوار: {e}")
            raise
    
    def _hash_password(self, password):
        """تشفير كلمة المرور باستخدام خوارزمية آمنة"""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        password_hash = salt + password_hash
        return password_hash.hex()
    
    def _verify_password(self, stored_password, provided_password):
        """التحقق من صحة كلمة المرور"""
        stored_password = bytes.fromhex(stored_password)
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        password_hash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt, 100000)
        return password_hash == stored_password
    
    def _validate_password_policy(self, password):
        """التحقق من توافق كلمة المرور مع سياسة كلمات المرور"""
        policy = self.config['password_policy']
        
        if len(password) < policy['min_length']:
            return False, f"كلمة المرور يجب أن تكون على الأقل {policy['min_length']} أحرف"
        
        if policy['require_uppercase'] and not any(c.isupper() for c in password):
            return False, "كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل"
        
        if policy['require_lowercase'] and not any(c.islower() for c in password):
            return False, "كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل"
        
        if policy['require_numbers'] and not any(c.isdigit() for c in password):
            return False, "كلمة المرور يجب أن تحتوي على رقم واحد على الأقل"
        
        if policy['require_special_chars'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "كلمة المرور يجب أن تحتوي على حرف خاص واحد على الأقل"
        
        return True, "كلمة المرور صالحة"
    
    def authenticate_user(self, username, password, country=None, company=None):
        """مصادقة المستخدم والتحقق من صلاحياته"""
        try:
            # البحث عن المستخدم في قاعدة البيانات
            user = self.db_manager.fetch_one('operational', 'SELECT id, username, password_hash, email, role, country, company, is_active FROM users WHERE username = ?', (username,))
            
            if not user:
                return False, "اسم المستخدم غير موجود"
            
            user_id, db_username, password_hash, email, role, user_country, user_company, is_active = user
            
            # التحقق من حالة المستخدم
            if not is_active:
                return False, "الحساب غير نشط"
            
            # التحقق من كلمة المرور
            if not self._verify_password(password_hash, password):
                return False, "كلمة المرور غير صحيحة"
            
            # التحقق من الدولة والشركة إذا تم تحديدهما
            if country and company:
                # التحقق من وجود الدولة
                country_record = self.db_manager.fetch_one('operational', 'SELECT id FROM countries WHERE name = ? AND is_active = 1', (country,))
                if not country_record:
                    return False, "الدولة غير موجودة أو غير نشطة"
                
                country_id = country_record[0]
                
                # التحقق من وجود الشركة
                company_record = self.db_manager.fetch_one('operational', 'SELECT id FROM companies WHERE name = ? AND country_id = ? AND is_active = 1', (company, country_id))
                if not company_record:
                    return False, "الشركة غير موجودة أو غير نشطة"
                
                # تحديث بيانات المستخدم بالدولة والشركة المحددة
                self.db_manager.update('operational', 'users', {'country': country, 'company': company, 'last_login': datetime.datetime.now().isoformat()}, {'id': user_id})
            else:
                # تحديث وقت آخر تسجيل دخول
                self.db_manager.update('operational', 'users', {'last_login': datetime.datetime.now().isoformat()}, {'id': user_id})
            
            # الحصول على صلاحيات الدور
            role_record = self.db_manager.fetch_one('operational', 'SELECT permissions FROM roles WHERE name = ?', (role,))
            if not role_record:
                return False, "الدور غير موجود"
            
            permissions = json.loads(role_record[0])
            
            # إنشاء رمز JWT
            token_data = {
                'user_id': user_id,
                'username': username,
                'email': email,
                'role': role,
                'country': country or user_country,
                'company': company or user_company,
                'permissions': permissions,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.jwt_expiry)
            }
            
            token = jwt.encode(token_data, self.jwt_secret, algorithm='HS256')
            
            # تسجيل عملية تسجيل الدخول
            self.db_manager.insert('operational', 'audit_logs', {
                'user_id': user_id,
                'action': 'login',
                'entity_type': 'user',
                'entity_id': user_id,
                'details': json.dumps({
                    'country': country or user_country,
                    'company': company or user_company,
                    'timestamp': datetime.datetime.now().isoformat()
                })
            })
            
            return True, {
                'token': token,
                'user_id': user_id,
                'username': username,
                'email': email,
                'role': role,
                'country': country or user_country,
                'company': company or user_company,
                'permissions': permissions
            }
        except Exception as e:
            self.logger.error(f"خطأ في مصادقة المستخدم: {e}")
            return False, f"خطأ في المصادقة: {str(e)}"
    
    def verify_token(self, token):
        """التحقق من صحة رمز JWT"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, "انتهت صلاحية الرمز"
        except jwt.InvalidTokenError:
            return False, "الرمز غير صالح"
    
    def check_permission(self, token, permission):
        """التحقق من امتلاك المستخدم لصلاحية محددة"""
        success, result = self.verify_token(token)
        if not success:
            return False, result
        
        user_permissions = result.get('permissions', [])
        
        # التحقق من وجود الصلاحية المطلوبة
        if permission in user_permissions:
            return True, "المستخدم يملك الصلاحية المطلوبة"
        
        # التحقق من وجود صلاحية المدير العام
        if 'admin' in user_permissions:
            return True, "المستخدم مدير عام ويملك جميع الصلاحيات"
        
        return False, "المستخدم لا يملك الصلاحية المطلوبة"
    
    def get_user_permissions(self, user_id):
        """الحصول على صلاحيات المستخدم"""
        try:
            # الحصول على دور المستخدم
            user = self.db_manager.fetch_one('operational', 'SELECT role FROM users WHERE id = ?', (user_id,))
            if not user:
                return False, "المستخدم غير موجود"
            
            role = user[0]
            
            # الحصول على صلاحيات الدور
            role_record = self.db_manager.fetch_one('operational', 'SELECT permissions FROM roles WHERE name = ?', (role,))
            if not role_record:
                return False, "الدور غير موجود"
            
            permissions = json.loads(role_record[0])
            
            return True, permissions
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على صلاحيات المستخدم: {e}")
            return False, f"خطأ: {str(e)}"
    
    def create_user(self, username, password, email, role, country=None, company=None, created_by=None):
        """إنشاء مستخدم جديد"""
        try:
            # التحقق من عدم وجود مستخدم بنفس اسم المستخدم
            existing_user = self.db_manager.fetch_one('operational', 'SELECT id FROM users WHERE username = ?', (username,))
            if existing_user:
                return False, "اسم المستخدم موجود بالفعل"
            
            # التحقق من عدم وجود مستخدم بنفس البريد الإلكتروني
            if email:
                existing_email = self.db_manager.fetch_one('operational', 'SELECT id FROM users WHERE email = ?', (email,))
                if existing_email:
                    return False, "البريد الإلكتروني موجود بالفعل"
            
            # التحقق من وجود الدور
            role_record = self.db_manager.fetch_one('operational', 'SELECT id FROM roles WHERE name = ?', (role,))
            if not role_record:
                return False, "الدور غير موجود"
            
            # التحقق من سياسة كلمة المرور
            valid, message = self._validate_password_policy(password)
            if not valid:
                return False, message
            
            # تشفير كلمة المرور
            password_hash = self._hash_password(password)
            
            # إنشاء المستخدم
            user_id = self.db_manager.insert('operational', 'users', {
                'username': username,
                'password_hash': password_hash,
                'email': email,
                'role': role,
                'country': country,
                'company': company,
                'is_active': 1
            })
            
            # تسجيل عملية إنشاء المستخدم
            if created_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': created_by,
                    'action': 'create_user',
                    'entity_type': 'user',
                    'entity_id': user_id,
                    'details': json.dumps({
                        'username': username,
                        'email': email,
                        'role': role,
                        'country': country,
                        'company': company,
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, user_id
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء المستخدم: {e}")
            return False, f"خطأ: {str(e)}"
    
    def update_user(self, user_id, data, updated_by=None):
        """تحديث بيانات المستخدم"""
        try:
            # التحقق من وجود المستخدم
            user = self.db_manager.fetch_one('operational', 'SELECT id FROM users WHERE id = ?', (user_id,))
            if not user:
                return False, "المستخدم غير موجود"
            
            # التحقق من عدم وجود مستخدم آخر بنفس اسم المستخدم
            if 'username' in data:
                existing_user = self.db_manager.fetch_one('operational', 'SELECT id FROM users WHERE username = ? AND id != ?', (data['username'], user_id))
                if existing_user:
                    return False, "اسم المستخدم موجود بالفعل"
            
            # التحقق من عدم وجود مستخدم آخر بنفس البريد الإلكتروني
            if 'email' in data and data['email']:
                existing_email = self.db_manager.fetch_one('operational', 'SELECT id FROM users WHERE email = ? AND id != ?', (data['email'], user_id))
                if existing_email:
                    return False, "البريد الإلكتروني موجود بالفعل"
            
            # التحقق من وجود الدور
            if 'role' in data:
                role_record = self.db_manager.fetch_one('operational', 'SELECT id FROM roles WHERE name = ?', (data['role'],))
                if not role_record:
                    return False, "الدور غير موجود"
            
            # التحقق من سياسة كلمة المرور
            if 'password' in data:
                valid, message = self._validate_password_policy(data['password'])
                if not valid:
                    return False, message
                
                # تشفير كلمة المرور
                data['password_hash'] = self._hash_password(data['password'])
                del data['password']
            
            # تحديث بيانات المستخدم
            self.db_manager.update('operational', 'users', data, {'id': user_id})
            
            # تسجيل عملية تحديث المستخدم
            if updated_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': updated_by,
                    'action': 'update_user',
                    'entity_type': 'user',
                    'entity_id': user_id,
                    'details': json.dumps({
                        'updated_fields': list(data.keys()),
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, "تم تحديث بيانات المستخدم بنجاح"
        except Exception as e:
            self.logger.error(f"خطأ في تحديث بيانات المستخدم: {e}")
            return False, f"خطأ: {str(e)}"
    
    def delete_user(self, user_id, deleted_by=None):
        """حذف المستخدم"""
        try:
            # التحقق من وجود المستخدم
            user = self.db_manager.fetch_one('operational', 'SELECT username FROM users WHERE id = ?', (user_id,))
            if not user:
                return False, "المستخدم غير موجود"
            
            username = user[0]
            
            # حذف المستخدم (تعطيل بدلاً من الحذف الفعلي)
            self.db_manager.update('operational', 'users', {'is_active': 0}, {'id': user_id})
            
            # تسجيل عملية حذف المستخدم
            if deleted_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': deleted_by,
                    'action': 'delete_user',
                    'entity_type': 'user',
                    'entity_id': user_id,
                    'details': json.dumps({
                        'username': username,
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, "تم حذف المستخدم بنجاح"
        except Exception as e:
            self.logger.error(f"خطأ في حذف المستخدم: {e}")
            return False, f"خطأ: {str(e)}"
    
    def create_role(self, name, description, permissions, created_by=None):
        """إنشاء دور جديد"""
        try:
            # التحقق من عدم وجود دور بنفس الاسم
            existing_role = self.db_manager.fetch_one('operational', 'SELECT id FROM roles WHERE name = ?', (name,))
            if existing_role:
                return False, "الدور موجود بالفعل"
            
            # التحقق من صحة الصلاحيات
            for permission in permissions:
                if permission not in self.AVAILABLE_PERMISSIONS:
                    return False, f"الصلاحية {permission} غير موجودة"
            
            # إنشاء الدور
            role_id = self.db_manager.insert('operational', 'roles', {
                'name': name,
                'description': description,
                'permissions': json.dumps(permissions)
            })
            
            # تسجيل عملية إنشاء الدور
            if created_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': created_by,
                    'action': 'create_role',
                    'entity_type': 'role',
                    'entity_id': role_id,
                    'details': json.dumps({
                        'name': name,
                        'description': description,
                        'permissions': permissions,
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, role_id
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الدور: {e}")
            return False, f"خطأ: {str(e)}"
    
    def update_role(self, role_id, data, updated_by=None):
        """تحديث بيانات الدور"""
        try:
            # التحقق من وجود الدور
            role = self.db_manager.fetch_one('operational', 'SELECT name FROM roles WHERE id = ?', (role_id,))
            if not role:
                return False, "الدور غير موجود"
            
            role_name = role[0]
            
            # التحقق من عدم وجود دور آخر بنفس الاسم
            if 'name' in data:
                existing_role = self.db_manager.fetch_one('operational', 'SELECT id FROM roles WHERE name = ? AND id != ?', (data['name'], role_id))
                if existing_role:
                    return False, "الدور موجود بالفعل"
            
            # التحقق من صحة الصلاحيات
            if 'permissions' in data:
                for permission in data['permissions']:
                    if permission not in self.AVAILABLE_PERMISSIONS:
                        return False, f"الصلاحية {permission} غير موجودة"
                
                # تحويل الصلاحيات إلى JSON
                data['permissions'] = json.dumps(data['permissions'])
            
            # تحديث بيانات الدور
            self.db_manager.update('operational', 'roles', data, {'id': role_id})
            
            # تسجيل عملية تحديث الدور
            if updated_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': updated_by,
                    'action': 'update_role',
                    'entity_type': 'role',
                    'entity_id': role_id,
                    'details': json.dumps({
                        'name': role_name,
                        'updated_fields': list(data.keys()),
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, "تم تحديث بيانات الدور بنجاح"
        except Exception as e:
            self.logger.error(f"خطأ في تحديث بيانات الدور: {e}")
            return False, f"خطأ: {str(e)}"
    
    def delete_role(self, role_id, deleted_by=None):
        """حذف الدور"""
        try:
            # التحقق من وجود الدور
            role = self.db_manager.fetch_one('operational', 'SELECT name FROM roles WHERE id = ?', (role_id,))
            if not role:
                return False, "الدور غير موجود"
            
            role_name = role[0]
            
            # التحقق من عدم وجود مستخدمين يستخدمون هذا الدور
            users = self.db_manager.fetch_all('operational', 'SELECT id FROM users WHERE role = ?', (role_name,))
            if users:
                return False, "لا يمكن حذف الدور لأنه مستخدم من قبل مستخدمين"
            
            # حذف الدور
            self.db_manager.delete('operational', 'roles', {'id': role_id})
            
            # تسجيل عملية حذف الدور
            if deleted_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': deleted_by,
                    'action': 'delete_role',
                    'entity_type': 'role',
                    'entity_id': role_id,
                    'details': json.dumps({
                        'name': role_name,
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, "تم حذف الدور بنجاح"
        except Exception as e:
            self.logger.error(f"خطأ في حذف الدور: {e}")
            return False, f"خطأ: {str(e)}"
    
    def get_countries(self):
        """الحصول على قائمة الدول"""
        try:
            countries = self.db_manager.fetch_all('operational', 'SELECT id, name, code, is_active FROM countries')
            return True, countries
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قائمة الدول: {e}")
            return False, f"خطأ: {str(e)}"
    
    def get_companies(self, country_id=None):
        """الحصول على قائمة الشركات"""
        try:
            if country_id:
                companies = self.db_manager.fetch_all('operational', 'SELECT id, name, country_id, description, is_active FROM companies WHERE country_id = ?', (country_id,))
            else:
                companies = self.db_manager.fetch_all('operational', 'SELECT id, name, country_id, description, is_active FROM companies')
            
            return True, companies
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قائمة الشركات: {e}")
            return False, f"خطأ: {str(e)}"
    
    def create_country(self, name, code, created_by=None):
        """إنشاء دولة جديدة"""
        try:
            # التحقق من عدم وجود دولة بنفس الاسم
            existing_country = self.db_manager.fetch_one('operational', 'SELECT id FROM countries WHERE name = ?', (name,))
            if existing_country:
                return False, "الدولة موجودة بالفعل"
            
            # التحقق من عدم وجود دولة بنفس الرمز
            existing_code = self.db_manager.fetch_one('operational', 'SELECT id FROM countries WHERE code = ?', (code,))
            if existing_code:
                return False, "رمز الدولة موجود بالفعل"
            
            # إنشاء الدولة
            country_id = self.db_manager.insert('operational', 'countries', {
                'name': name,
                'code': code,
                'is_active': 1
            })
            
            # تسجيل عملية إنشاء الدولة
            if created_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': created_by,
                    'action': 'create_country',
                    'entity_type': 'country',
                    'entity_id': country_id,
                    'details': json.dumps({
                        'name': name,
                        'code': code,
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, country_id
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الدولة: {e}")
            return False, f"خطأ: {str(e)}"
    
    def create_company(self, name, country_id, description=None, created_by=None):
        """إنشاء شركة جديدة"""
        try:
            # التحقق من وجود الدولة
            country = self.db_manager.fetch_one('operational', 'SELECT id FROM countries WHERE id = ?', (country_id,))
            if not country:
                return False, "الدولة غير موجودة"
            
            # التحقق من عدم وجود شركة بنفس الاسم في نفس الدولة
            existing_company = self.db_manager.fetch_one('operational', 'SELECT id FROM companies WHERE name = ? AND country_id = ?', (name, country_id))
            if existing_company:
                return False, "الشركة موجودة بالفعل في هذه الدولة"
            
            # إنشاء الشركة
            company_id = self.db_manager.insert('operational', 'companies', {
                'name': name,
                'country_id': country_id,
                'description': description,
                'is_active': 1
            })
            
            # تسجيل عملية إنشاء الشركة
            if created_by:
                self.db_manager.insert('operational', 'audit_logs', {
                    'user_id': created_by,
                    'action': 'create_company',
                    'entity_type': 'company',
                    'entity_id': company_id,
                    'details': json.dumps({
                        'name': name,
                        'country_id': country_id,
                        'description': description,
                        'timestamp': datetime.datetime.now().isoformat()
                    })
                })
            
            return True, company_id
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الشركة: {e}")
            return False, f"خطأ: {str(e)}"
    
    def get_audit_logs(self, filters=None, limit=100, offset=0):
        """الحصول على سجلات التدقيق"""
        try:
            query = '''
                SELECT al.id, al.user_id, u.username, al.action, al.entity_type, al.entity_id, al.details, al.timestamp
                FROM audit_logs al
                LEFT JOIN users u ON al.user_id = u.id
            '''
            
            params = []
            
            if filters:
                where_clauses = []
                
                if 'user_id' in filters:
                    where_clauses.append('al.user_id = ?')
                    params.append(filters['user_id'])
                
                if 'action' in filters:
                    where_clauses.append('al.action = ?')
                    params.append(filters['action'])
                
                if 'entity_type' in filters:
                    where_clauses.append('al.entity_type = ?')
                    params.append(filters['entity_type'])
                
                if 'entity_id' in filters:
                    where_clauses.append('al.entity_id = ?')
                    params.append(filters['entity_id'])
                
                if 'start_date' in filters:
                    where_clauses.append('al.timestamp >= ?')
                    params.append(filters['start_date'])
                
                if 'end_date' in filters:
                    where_clauses.append('al.timestamp <= ?')
                    params.append(filters['end_date'])
                
                if where_clauses:
                    query += ' WHERE ' + ' AND '.join(where_clauses)
            
            query += ' ORDER BY al.timestamp DESC LIMIT ? OFFSET ?'
            params.extend([limit, offset])
            
            logs = self.db_manager.fetch_all('operational', query, tuple(params))
            
            return True, logs
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على سجلات التدقيق: {e}")
            return False, f"خطأ: {str(e)}"


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
    
    # إنشاء مدير الصلاحيات
    permission_manager = PermissionManager(db_manager)
    
    # تهيئة الأدوار والدول والشركات
    permission_manager.initialize_roles()
    
    # مصادقة المستخدم
    success, result = permission_manager.authenticate_user('admin', 'admin_password', 'مصر', 'شركة الزراعة المتقدمة')
    
    if success:
        print(f"تم تسجيل الدخول بنجاح. الرمز: {result['token']}")
        
        # التحقق من صلاحية
        success, message = permission_manager.check_permission(result['token'], 'user_management')
        print(f"التحقق من صلاحية إدارة المستخدمين: {success}, {message}")
    else:
        print(f"فشل تسجيل الدخول: {result}")
