#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة إدارة التكوين لنظام Gaara ERP
"""

import os
import logging
import json
import yaml
from dotenv import load_dotenv

# إعداد التسجيل
logger = logging.getLogger(__name__)

class ConfigManager:
    """مدير التكوين لنظام Gaara ERP"""
    
    _instance = None
    
    def __new__(cls):
        """تنفيذ نمط Singleton لضمان وجود نسخة واحدة فقط من مدير التكوين"""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """تهيئة مدير التكوين"""
        if self._initialized:
            return
            
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # تحديد مسار ملف التكوين
        self.config_dir = os.getenv('CONFIG_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'config'))
        self.config_file = os.getenv('CONFIG_FILE', 'config.yaml')
        self.config_path = os.path.join(self.config_dir, self.config_file)
        
        # تحميل التكوين
        self.config = {}
        self.load_config()
        
        # تحميل إعدادات قاعدة البيانات
        from .database.db_manager import DatabaseManager
        self.db_manager = DatabaseManager()
        
        self._initialized = True
        logger.info("تم تهيئة مدير التكوين بنجاح")
    
    def load_config(self):
        """تحميل التكوين من الملف"""
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"ملف التكوين غير موجود: {self.config_path}")
                self._create_default_config()
                return
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                    self.config = yaml.safe_load(f)
                elif self.config_file.endswith('.json'):
                    self.config = json.load(f)
                else:
                    logger.error(f"تنسيق ملف التكوين غير مدعوم: {self.config_file}")
                    self._create_default_config()
                    return
            
            logger.info(f"تم تحميل التكوين بنجاح من: {self.config_path}")
        except Exception as e:
            logger.error(f"فشل في تحميل التكوين: {str(e)}")
            self._create_default_config()
    
    def _create_default_config(self):
        """إنشاء ملف تكوين افتراضي"""
        try:
            # إنشاء دليل التكوين إذا لم يكن موجودًا
            os.makedirs(self.config_dir, exist_ok=True)
            
            # التكوين الافتراضي
            default_config = {
                'app': {
                    'name': 'Gaara ERP',
                    'version': '1.0.0',
                    'debug': True,
                    'log_level': 'INFO',
                    'secret_key': os.getenv('SECRET_KEY', 'gaara_erp_secret_key'),
                    'allowed_hosts': ['*'],
                    'timezone': 'Asia/Riyadh'
                },
                'database': {
                    'host': os.getenv('DB_HOST', 'localhost'),
                    'port': os.getenv('DB_PORT', '5432'),
                    'name': os.getenv('DB_NAME', 'gaara_erp'),
                    'user': os.getenv('DB_USER', 'postgres'),
                    'password': os.getenv('DB_PASSWORD', 'postgres'),
                    'min_connections': int(os.getenv('DB_MIN_CONNECTIONS', '1')),
                    'max_connections': int(os.getenv('DB_MAX_CONNECTIONS', '10'))
                },
                'auth': {
                    'jwt_secret': os.getenv('JWT_SECRET', 'gaara_erp_secret_key'),
                    'jwt_algorithm': os.getenv('JWT_ALGORITHM', 'HS256'),
                    'jwt_expiration': int(os.getenv('JWT_EXPIRATION', '86400'))
                },
                'integration': {
                    'agricultural_system': {
                        'enabled': True,
                        'api_url': os.getenv('AGRI_API_URL', 'http://localhost:8000/api'),
                        'api_key': os.getenv('AGRI_API_KEY', ''),
                        'sync_interval': int(os.getenv('AGRI_SYNC_INTERVAL', '3600'))
                    }
                },
                'i18n': {
                    'default_language': 'ar',
                    'available_languages': ['ar', 'en', 'tr', 'th'],
                    'rtl_languages': ['ar']
                },
                'currency': {
                    'default_currency': 'SAR',
                    'available_currencies': ['SAR', 'USD', 'EUR', 'TRY', 'AED', 'OMR', 'THB']
                },
                'email': {
                    'enabled': False,
                    'host': os.getenv('EMAIL_HOST', ''),
                    'port': int(os.getenv('EMAIL_PORT', '587')),
                    'username': os.getenv('EMAIL_USERNAME', ''),
                    'password': os.getenv('EMAIL_PASSWORD', ''),
                    'use_tls': True,
                    'from_email': os.getenv('EMAIL_FROM', 'noreply@gaaraerp.com')
                },
                'storage': {
                    'type': 'local',
                    'local_path': os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'storage'),
                    's3_bucket': os.getenv('S3_BUCKET', ''),
                    's3_region': os.getenv('S3_REGION', ''),
                    's3_access_key': os.getenv('S3_ACCESS_KEY', ''),
                    's3_secret_key': os.getenv('S3_SECRET_KEY', '')
                }
            }
            
            # حفظ التكوين الافتراضي
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                    yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
                elif self.config_file.endswith('.json'):
                    json.dump(default_config, f, ensure_ascii=False, indent=4)
                else:
                    yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            
            self.config = default_config
            logger.info(f"تم إنشاء ملف التكوين الافتراضي: {self.config_path}")
        except Exception as e:
            logger.error(f"فشل في إنشاء ملف التكوين الافتراضي: {str(e)}")
            self.config = {}
    
    def get(self, key, default=None):
        """الحصول على قيمة من التكوين"""
        try:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value.get(k)
                if value is None:
                    return default
            return value
        except Exception:
            return default
    
    def set(self, key, value):
        """تعيين قيمة في التكوين"""
        try:
            keys = key.split('.')
            config = self.config
            for i, k in enumerate(keys[:-1]):
                if k not in config:
                    config[k] = {}
                config = config[k]
            config[keys[-1]] = value
            self.save_config()
            return True
        except Exception as e:
            logger.error(f"فشل في تعيين قيمة التكوين: {str(e)}")
            return False
    
    def save_config(self):
        """حفظ التكوين إلى الملف"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                    yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
                elif self.config_file.endswith('.json'):
                    json.dump(self.config, f, ensure_ascii=False, indent=4)
                else:
                    yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"تم حفظ التكوين بنجاح إلى: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"فشل في حفظ التكوين: {str(e)}")
            return False
    
    def get_db_setting(self, key, default=None):
        """الحصول على إعداد من قاعدة البيانات"""
        try:
            query = """
                SELECT setting_value, setting_type
                FROM erp.settings
                WHERE setting_key = %s
            """
            result = self.db_manager.execute_query(query, (key,))
            
            if not result:
                return default
            
            setting = result[0]
            value = setting['setting_value']
            setting_type = setting['setting_type']
            
            # تحويل القيمة حسب النوع
            if setting_type == 'int':
                return int(value)
            elif setting_type == 'float':
                return float(value)
            elif setting_type == 'bool':
                return value.lower() in ('true', '1', 'yes')
            elif setting_type == 'json':
                return json.loads(value)
            else:
                return value
        except Exception as e:
            logger.error(f"فشل في الحصول على إعداد من قاعدة البيانات: {str(e)}")
            return default
    
    def set_db_setting(self, key, value, setting_type='string', description=None, is_system=False, is_editable=True):
        """تعيين إعداد في قاعدة البيانات"""
        try:
            # تحويل القيمة إلى نص
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, ensure_ascii=False)
                setting_type = 'json'
            else:
                value_str = str(value)
            
            # التحقق من وجود الإعداد
            query = """
                SELECT setting_id
                FROM erp.settings
                WHERE setting_key = %s
            """
            result = self.db_manager.execute_query(query, (key,))
            
            if result:
                # تحديث الإعداد الموجود
                update_query = """
                    UPDATE erp.settings
                    SET setting_value = %s, setting_type = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE setting_key = %s
                """
                self.db_manager.execute_query(update_query, (value_str, setting_type, key), fetch=False)
            else:
                # إنشاء إعداد جديد
                insert_query = """
                    INSERT INTO erp.settings
                    (setting_key, setting_value, setting_type, is_system, is_editable, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                self.db_manager.execute_query(insert_query, (key, value_str, setting_type, is_system, is_editable, description), fetch=False)
            
            logger.info(f"تم تعيين الإعداد في قاعدة البيانات: {key}")
            return True
        except Exception as e:
            logger.error(f"فشل في تعيين الإعداد في قاعدة البيانات: {str(e)}")
            return False
    
    def get_all_db_settings(self, is_system=None, is_editable=None):
        """الحصول على جميع الإعدادات من قاعدة البيانات"""
        try:
            query = """
                SELECT setting_id, setting_key, setting_value, setting_type, is_system, is_editable, description
                FROM erp.settings
            """
            params = []
            
            # إضافة شروط البحث
            conditions = []
            if is_system is not None:
                conditions.append("is_system = %s")
                params.append(is_system)
            if is_editable is not None:
                conditions.append("is_editable = %s")
                params.append(is_editable)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            return self.db_manager.execute_query(query, tuple(params))
        except Exception as e:
            logger.error(f"فشل في الحصول على الإعدادات من قاعدة البيانات: {str(e)}")
            return []

# نموذج استخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # تهيئة مدير التكوين
    config_manager = ConfigManager()
    
    # مثال على الحصول على قيمة من التكوين
    app_name = config_manager.get('app.name', 'Gaara ERP')
    print(f"اسم التطبيق: {app_name}")
    
    # مثال على تعيين قيمة في التكوين
    config_manager.set('app.debug', False)
    
    # مثال على الحصول على إعداد من قاعدة البيانات
    db_setting = config_manager.get_db_setting('system.maintenance_mode', False)
    print(f"وضع الصيانة: {db_setting}")
    
    # مثال على تعيين إعداد في قاعدة البيانات
    config_manager.set_db_setting('system.maintenance_mode', True, 'bool', 'وضع الصيانة للنظام', True, True)
