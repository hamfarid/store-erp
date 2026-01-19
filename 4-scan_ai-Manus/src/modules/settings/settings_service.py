# File: /home/ubuntu/ai_web_organized/src/modules/settings/settings_service.py
"""
from flask import g
خدمة الإعدادات العامة
توفر هذه الوحدة خدمات لإدارة الإعدادات العامة للنظام
"""

import os
import json
import logging
import datetime

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("settings.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SettingsService:
    """خدمة الإعدادات العامة"""

    def __init__(self, config_dir=None):
        """
        تهيئة خدمة الإعدادات العامة

        Args:
            config_dir (str, optional): مجلد الإعدادات. Defaults to None.
        """
        # تحديد مجلد الإعدادات
        self.config_dir = config_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')

        # التأكد من وجود مجلد الإعدادات
        os.makedirs(self.config_dir, exist_ok=True)

        # مسار ملف الإعدادات العامة
        self.general_settings_file = os.path.join(self.config_dir, 'general_settings.json')

        # مسار ملف إعدادات الشركة
        self.company_settings_file = os.path.join(self.config_dir, 'company_settings.json')

        # مسار ملف إعدادات النظام
        self.system_settings_file = os.path.join(self.config_dir, 'system_settings.json')

        # مسار ملف إعدادات الاتصال
        self.connection_settings_file = os.path.join(self.config_dir, 'connection_settings.json')

        # تحميل الإعدادات
        self.general_settings = self._load_settings(self.general_settings_file, self._get_default_general_settings())
        self.company_settings = self._load_settings(self.company_settings_file, self._get_default_company_settings())
        self.system_settings = self._load_settings(self.system_settings_file, self._get_default_system_settings())
        self.connection_settings = self._load_settings(self.connection_settings_file, self._get_default_connection_settings())

    def _get_default_general_settings(self):
        """
        الحصول على الإعدادات العامة الافتراضية

        Returns:
            dict: الإعدادات العامة الافتراضية
        """
        return {
            "language": "ar",
            "timezone": "Africa/Cairo",
            "date_format": "YYYY-MM-DD",
            "time_format": "HH:mm:ss",
            "currency": "SAR",
            "decimal_separator": ".",
            "thousands_separator": ",",
            "default_page_size": 20,
            "theme": {
                "primary_color": "#1976d2",
                "secondary_color": "#dc004e",
                "dark_mode": False
            },
            "notifications": {
                "email": True,
                "sms": False,
                "push": True,
                "in_app": True
            },
            "last_updated": datetime.datetime.now().isoformat()
        }

    def _get_default_company_settings(self):
        """
        الحصول على إعدادات الشركة الافتراضية

        Returns:
            dict: إعدادات الشركة الافتراضية
        """
        return {
            "name": "شركة جعاره",
            "legal_name": "شركة جعاره للتقنية",
            "tax_id": "123456789",
            "registration_number": "987654321",
            "logo": "/assets/images/logo.png",
            "address": {
                "street": "شارع الملك فهد",
                "city": "الرياض",
                "state": "الرياض",
                "postal_code": "12345",
                "country": "جمهورية مصر العربية"
            },
            "contact": {
                "phone": "+20 100345 6789",
                "email": "info@gaaragroup.com",
                "website": "https://gaaragroup.com"
            },
            "social_media": {
                "facebook": "https://facebook.com/gaara",
                "twitter": "https://twitter.com/gaara",
                "linkedin": "https://linkedin.com/company/gaara",
                "instagram": "https://instagram.com/gaara"
            },
            "fiscal_year": {
                "start_month": 1,
                "start_day": 1,
                "end_month": 12,
                "end_day": 31
            },
            "last_updated": datetime.datetime.now().isoformat()
        }

    def _get_default_system_settings(self):
        """
        الحصول على إعدادات النظام الافتراضية

        Returns:
            dict: إعدادات النظام الافتراضية
        """
        return {
            "backup": {
                "auto_backup": True,
                "backup_frequency": "daily",
                "backup_time": "02:00",
                "backup_retention_days": 30,
                "backup_location": "/backups"
            },
            "security": {
                "password_expiry_days": 90,
                "min_password_length": 8,
                "require_special_chars": True,
                "require_numbers": True,
                "require_uppercase": True,
                "require_lowercase": True,
                "max_login_attempts": 5,
                "lockout_duration_minutes": 30,
                "session_timeout_minutes": 60,
                "two_factor_auth": False
            },
            "logging": {
                "log_level": "INFO",
                "log_retention_days": 90,
                "audit_trail": True
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl_seconds": 3600,
                "max_upload_size_mb": 10,
                "max_report_rows": 10000,
                "pagination_size": 50
            },
            "maintenance": {
                "maintenance_mode": False,
                "maintenance_message": "النظام قيد الصيانة حالياً. يرجى المحاولة لاحقاً.",
                "allowed_ips_during_maintenance": []
            },
            "last_updated": datetime.datetime.now().isoformat()
        }

    def _get_default_connection_settings(self):
        """
        الحصول على إعدادات الاتصال الافتراضية

        Returns:
            dict: إعدادات الاتصال الافتراضية
        """
        return {
            "database": {
                "type": "postgresql",
                "host": "localhost",
                "port": 5432,
                "name": "gaara_erp",
                "user": "postgres",
                "password": "postgres",
                "max_connections": 100,
                "timeout_seconds": 30
            },
            "redis": {
                "host": "localhost",
                "port": 6379,
                "password": "",
                "database": 0,
                "timeout_seconds": 5
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "use_tls": True,
                "from_email": "noreply@gaaragroup.com",
                "from_name": "نظام جعاره"
            },
            "sms": {
                "provider": "twilio",
                "account_sid": "",
                "auth_token": "",
                "from_number": ""
            },
            "storage": {
                "type": "local",
                "local_path": "/uploads",
                "aws_access_key": "",
                "aws_secret_key": "",
                "aws_bucket": "",
                "aws_region": "us-east-1"
            },
            "last_updated": datetime.datetime.now().isoformat()
        }

    def _load_settings(self, file_path, default_settings):
        """
        تحميل الإعدادات من ملف

        Args:
            file_path (str): مسار الملف
            default_settings (dict): الإعدادات الافتراضية

        Returns:
            dict: الإعدادات المحملة
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                # دمج الإعدادات المحملة مع الإعدادات الافتراضية
                merged_settings = default_settings.copy()
                self._deep_update(merged_settings, settings)

                return merged_settings

            # حفظ الإعدادات الافتراضية
            self._save_settings(file_path, default_settings)
            return default_settings

        except Exception as e:
            logger.exception("Error loading settings from %s: %s", file_path, str(e))

            # حفظ الإعدادات الافتراضية
            self._save_settings(file_path, default_settings)
            return default_settings

    def _save_settings(self, file_path, settings):
        """
        حفظ الإعدادات في ملف

        Args:
            file_path (str): مسار الملف
            settings (dict): الإعدادات

        Returns:
            bool: نجاح العملية
        """
        try:
            # تحديث تاريخ آخر تحديث
            if isinstance(settings, dict) and 'last_updated' in settings:
                settings['last_updated'] = datetime.datetime.now().isoformat()

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            logger.exception("Error saving settings to %s: %s", file_path, str(e))
            return False

    def _deep_update(self, target, source):
        """
        تحديث عميق للقاموس

        Args:
            target (dict): القاموس الهدف
            source (dict): القاموس المصدر
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def get_general_settings(self):
        """
        الحصول على الإعدادات العامة

        Returns:
            dict: الإعدادات العامة
        """
        return self.general_settings

    def update_general_settings(self, settings):
        """
        تحديث الإعدادات العامة

        Args:
            settings (dict): الإعدادات الجديدة

        Returns:
            dict: الإعدادات المحدثة
        """
        # دمج الإعدادات الجديدة مع الإعدادات الحالية
        self._deep_update(self.general_settings, settings)

        # حفظ الإعدادات
        self._save_settings(self.general_settings_file, self.general_settings)

        return self.general_settings

    def get_company_settings(self):
        """
        الحصول على إعدادات الشركة

        Returns:
            dict: إعدادات الشركة
        """
        return self.company_settings

    def update_company_settings(self, settings):
        """
        تحديث إعدادات الشركة

        Args:
            settings (dict): الإعدادات الجديدة

        Returns:
            dict: الإعدادات المحدثة
        """
        # دمج الإعدادات الجديدة مع الإعدادات الحالية
        self._deep_update(self.company_settings, settings)

        # حفظ الإعدادات
        self._save_settings(self.company_settings_file, self.company_settings)

        return self.company_settings

    def get_system_settings(self):
        """
        الحصول على إعدادات النظام

        Returns:
            dict: إعدادات النظام
        """
        return self.system_settings

    def update_system_settings(self, settings):
        """
        تحديث إعدادات النظام

        Args:
            settings (dict): الإعدادات الجديدة

        Returns:
            dict: الإعدادات المحدثة
        """
        # دمج الإعدادات الجديدة مع الإعدادات الحالية
        self._deep_update(self.system_settings, settings)

        # حفظ الإعدادات
        self._save_settings(self.system_settings_file, self.system_settings)

        return self.system_settings

    def get_connection_settings(self):
        """
        الحصول على إعدادات الاتصال

        Returns:
            dict: إعدادات الاتصال
        """
        return self.connection_settings

    def update_connection_settings(self, settings):
        """
        تحديث إعدادات الاتصال

        Args:
            settings (dict): الإعدادات الجديدة

        Returns:
            dict: الإعدادات المحدثة
        """
        # دمج الإعدادات الجديدة مع الإعدادات الحالية
        self._deep_update(self.connection_settings, settings)

        # حفظ الإعدادات
        self._save_settings(self.connection_settings_file, self.connection_settings)

        return self.connection_settings

    def get_all_settings(self):
        """
        الحصول على جميع الإعدادات

        Returns:
            dict: جميع الإعدادات
        """
        return {
            "general": self.general_settings,
            "company": self.company_settings,
            "system": self.system_settings,
            "connection": self.connection_settings
        }

    def reset_settings(self, settings_type):
        """
        إعادة تعيين الإعدادات إلى القيم الافتراضية

        Args:
            settings_type (str): نوع الإعدادات (general, company, system, connection, all)

        Returns:
            dict: الإعدادات المعاد تعيينها
        """
        if settings_type in ("general", "all"):
            self.general_settings = self._get_default_general_settings()
            self._save_settings(self.general_settings_file, self.general_settings)

        if settings_type in ("company", "all"):
            self.company_settings = self._get_default_company_settings()
            self._save_settings(self.company_settings_file, self.company_settings)

        if settings_type in ("system", "all"):
            self.system_settings = self._get_default_system_settings()
            self._save_settings(self.system_settings_file, self.system_settings)

        if settings_type in ("connection", "all"):
            self.connection_settings = self._get_default_connection_settings()
            self._save_settings(self.connection_settings_file, self.connection_settings)

        if settings_type == "general":
            return self.general_settings
        if settings_type == "company":
            return self.company_settings
        if settings_type == "system":
            return self.system_settings
        if settings_type == "connection":
            return self.connection_settings

        return self.get_all_settings()

    def export_settings(self, settings_type, file_path=None):
        """
        تصدير الإعدادات إلى ملف

        Args:
            settings_type (str): نوع الإعدادات (general, company, system, connection, all)
            file_path (str, optional): مسار الملف. Defaults to None.

        Returns:
            str: مسار الملف المصدر
        """
        try:
            if file_path is None:
                file_path = os.path.join(
                    self.config_dir,
                    f"export_{settings_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )

            if settings_type == "general":
                settings = self.general_settings
            elif settings_type == "company":
                settings = self.company_settings
            elif settings_type == "system":
                settings = self.system_settings
            elif settings_type == "connection":
                settings = self.connection_settings
            else:
                settings = self.get_all_settings()

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            return file_path
        except Exception as e:
            logger.exception("Error exporting settings to %s: %s", file_path, str(e))
            return None

    def import_settings(self, settings_type, file_path):
        """
        استيراد الإعدادات من ملف

        Args:
            settings_type (str): نوع الإعدادات (general, company, system, connection, all)
            file_path (str): مسار الملف

        Returns:
            bool: نجاح العملية
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)

            if settings_type == "general":
                self.update_general_settings(settings)
            elif settings_type == "company":
                self.update_company_settings(settings)
            elif settings_type == "system":
                self.update_system_settings(settings)
            elif settings_type == "connection":
                self.update_connection_settings(settings)
            else:
                # استيراد جميع الإعدادات
                if "general" in settings:
                    self.update_general_settings(settings["general"])
                if "company" in settings:
                    self.update_company_settings(settings["company"])
                if "system" in settings:
                    self.update_system_settings(settings["system"])
                if "connection" in settings:
                    self.update_connection_settings(settings["connection"])

            return True
        except Exception as e:
            logger.exception("Error importing settings from %s: %s", file_path, str(e))
            return False

    def validate_settings(self, settings_type, settings):
        """
        التحقق من صحة الإعدادات

        Args:
            settings_type (str): نوع الإعدادات (general, company, system, connection)
            settings (dict): الإعدادات

        Returns:
            tuple: (bool, str) نجاح التحقق ورسالة الخطأ
        """
        try:
            if settings_type not in ["general", "company", "system", "connection"]:
                return False, "Invalid settings type"

            if not isinstance(settings, dict):
                return False, "Settings must be a dictionary"

            # التحقق من الإعدادات العامة
            if settings_type == "general":
                if "language" in settings and not isinstance(settings["language"], str):
                    return False, "Language must be a string"

                if "timezone" in settings and not isinstance(settings["timezone"], str):
                    return False, "Timezone must be a string"

                if "currency" in settings and not isinstance(settings["currency"], str):
                    return False, "Currency must be a string"

                if "default_page_size" in settings and not isinstance(settings["default_page_size"], int):
                    return False, "Default page size must be an integer"

            # التحقق من إعدادات الشركة
            elif settings_type == "company":
                if "name" in settings and not isinstance(settings["name"], str):
                    return False, "Company name must be a string"

                if "tax_id" in settings and not isinstance(settings["tax_id"], str):
                    return False, "Tax ID must be a string"

                if "registration_number" in settings and not isinstance(settings["registration_number"], str):
                    return False, "Registration number must be a string"

            # التحقق من إعدادات النظام
            elif settings_type == "system":
                if "backup" in settings and not isinstance(settings["backup"], dict):
                    return False, "Backup settings must be a dictionary"

                if "security" in settings and not isinstance(settings["security"], dict):
                    return False, "Security settings must be a dictionary"

                if "logging" in settings and not isinstance(settings["logging"], dict):
                    return False, "Logging settings must be a dictionary"

            # التحقق من إعدادات الاتصال
            elif settings_type == "connection":
                if "database" in settings and not isinstance(settings["database"], dict):
                    return False, "Database settings must be a dictionary"

                if "redis" in settings and not isinstance(settings["redis"], dict):
                    return False, "Redis settings must be a dictionary"

                if "email" in settings and not isinstance(settings["email"], dict):
                    return False, "Email settings must be a dictionary"

            return True, "Settings are valid"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
