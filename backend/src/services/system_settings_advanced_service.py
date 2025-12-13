#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/system_settings_advanced_service.py

خدمة إعدادات النظام المتقدمة
Advanced System Settings Service

يوفر هذا الملف خدمات شاملة لإدارة إعدادات النظام والتكوين
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import IntegrityError

# استيراد النماذج
from models.system_settings_advanced import (
    SystemConfiguration,
    CompanySettings,
    ModuleSettings,
    EmailSettings,
    NotificationSettings,
    SecuritySettings,
    BackupSettings,
    IntegrationSettings,
    UISettings,
    LocalizationSettings,
    PerformanceSettings,
    AuditSettings,
    MaintenanceSettings,
    LicenseSettings,
    CustomSettings,
)
from ..database import db

# إعداد السجلات
logger = logging.getLogger(__name__)


class SystemSettingsAdvancedService:
    """خدمة إعدادات النظام المتقدمة"""

    def __init__(self):
        """تهيئة الخدمة"""
        self.logger = logger
        self.default_settings = self._load_default_settings()

    # ==================== إدارة الإعدادات العامة ====================

    def get_system_configuration(self) -> Dict[str, Any]:
        """
        الحصول على تكوين النظام الحالي

        Returns:
            Dict: تكوين النظام
        """
        try:
            config = SystemConfiguration.query.first()

            if not config:
                # إنشاء تكوين افتراضي
                config = self._create_default_configuration()

            return {
                "success": True,
                "configuration": self._serialize_system_configuration(config),
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على تكوين النظام: {str(e)}")
            return {"success": False, "message": f"خطأ في الحصول على التكوين: {str(e)}"}

    def update_system_configuration(
        self, config_data: Dict[str, Any], updated_by: int
    ) -> Dict[str, Any]:
        """
        تحديث تكوين النظام

        Args:
            config_data: بيانات التكوين الجديدة
            updated_by: معرف المستخدم المحدث

        Returns:
            Dict: نتيجة العملية
        """
        try:
            config = SystemConfiguration.query.first()

            if not config:
                config = SystemConfiguration()
                db.session.add(config)

            # تحديث البيانات
            for key, value in config_data.items():
                if hasattr(config, key):
                    setattr(config, key, value)

            config.updated_by = updated_by
            config.updated_at = datetime.utcnow()

            db.session.commit()

            return {
                "success": True,
                "message": "تم تحديث تكوين النظام بنجاح",
                "configuration": self._serialize_system_configuration(config),
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في تحديث تكوين النظام: {str(e)}")
            return {"success": False, "message": f"خطأ في تحديث التكوين: {str(e)}"}

    # ==================== إعدادات الشركة ====================

    def get_company_settings(self) -> Dict[str, Any]:
        """
        الحصول على إعدادات الشركة

        Returns:
            Dict: إعدادات الشركة
        """
        try:
            settings = CompanySettings.query.first()

            if not settings:
                settings = self._create_default_company_settings()

            return {
                "success": True,
                "settings": self._serialize_company_settings(settings),
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على إعدادات الشركة: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على الإعدادات: {str(e)}",
            }

    def update_company_settings(
        self, settings_data: Dict[str, Any], updated_by: int
    ) -> Dict[str, Any]:
        """
        تحديث إعدادات الشركة

        Args:
            settings_data: بيانات الإعدادات الجديدة
            updated_by: معرف المستخدم المحدث

        Returns:
            Dict: نتيجة العملية
        """
        try:
            settings = CompanySettings.query.first()

            if not settings:
                settings = CompanySettings()
                db.session.add(settings)

            # تحديث البيانات
            for key, value in settings_data.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)

            settings.updated_by = updated_by
            settings.updated_at = datetime.utcnow()

            db.session.commit()

            return {
                "success": True,
                "message": "تم تحديث إعدادات الشركة بنجاح",
                "settings": self._serialize_company_settings(settings),
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في تحديث إعدادات الشركة: {str(e)}")
            return {"success": False, "message": f"خطأ في تحديث الإعدادات: {str(e)}"}

    # ==================== إعدادات الوحدات ====================

    def get_module_settings(self, module_name: str = None) -> Dict[str, Any]:
        """
        الحصول على إعدادات الوحدات

        Args:
            module_name: اسم الوحدة (اختياري)

        Returns:
            Dict: إعدادات الوحدات
        """
        try:
            query = ModuleSettings.query

            if module_name:
                query = query.filter_by(module_name=module_name)
                settings = query.first()

                if not settings:
                    return {
                        "success": False,
                        "message": f"إعدادات الوحدة {module_name} غير موجودة",
                    }

                return {
                    "success": True,
                    "settings": self._serialize_module_settings(settings),
                }
            else:
                settings_list = query.all()
                return {
                    "success": True,
                    "settings": [
                        self._serialize_module_settings(s) for s in settings_list
                    ],
                }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على إعدادات الوحدات: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على الإعدادات: {str(e)}",
            }

    def update_module_settings(
        self, module_name: str, settings_data: Dict[str, Any], updated_by: int
    ) -> Dict[str, Any]:
        """
        تحديث إعدادات وحدة

        Args:
            module_name: اسم الوحدة
            settings_data: بيانات الإعدادات الجديدة
            updated_by: معرف المستخدم المحدث

        Returns:
            Dict: نتيجة العملية
        """
        try:
            settings = ModuleSettings.query.filter_by(module_name=module_name).first()

            if not settings:
                settings = ModuleSettings(module_name=module_name)
                db.session.add(settings)

            # تحديث البيانات
            for key, value in settings_data.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)

            settings.updated_by = updated_by
            settings.updated_at = datetime.utcnow()

            db.session.commit()

            return {
                "success": True,
                "message": f"تم تحديث إعدادات وحدة {module_name} بنجاح",
                "settings": self._serialize_module_settings(settings),
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في تحديث إعدادات الوحدة: {str(e)}")
            return {"success": False, "message": f"خطأ في تحديث الإعدادات: {str(e)}"}

    # ==================== إعدادات البريد الإلكتروني ====================

    def get_email_settings(self) -> Dict[str, Any]:
        """
        الحصول على إعدادات البريد الإلكتروني

        Returns:
            Dict: إعدادات البريد الإلكتروني
        """
        try:
            settings = EmailSettings.query.first()

            if not settings:
                settings = self._create_default_email_settings()

            return {
                "success": True,
                "settings": self._serialize_email_settings(settings),
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على إعدادات البريد: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على الإعدادات: {str(e)}",
            }

    def test_email_connection(self, email_settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        اختبار اتصال البريد الإلكتروني

        Args:
            email_settings: إعدادات البريد الإلكتروني

        Returns:
            Dict: نتيجة الاختبار
        """
        try:
            import smtplib
            from email.mime.text import MIMEText

            # إنشاء اتصال SMTP
            server = smtplib.SMTP(
                email_settings.get("smtp_server"), email_settings.get("smtp_port", 587)
            )

            if email_settings.get("use_tls", True):
                server.starttls()

            if email_settings.get("username") and email_settings.get("password"):
                server.login(email_settings["username"], email_settings["password"])

            server.quit()

            return {
                "success": True,
                "message": "تم الاتصال بخادم البريد الإلكتروني بنجاح",
            }

        except Exception as e:
            self.logger.error(f"خطأ في اختبار اتصال البريد: {str(e)}")
            return {
                "success": False,
                "message": f"فشل في الاتصال بخادم البريد: {str(e)}",
            }

    # ==================== إعدادات الأمان ====================

    def get_security_settings(self) -> Dict[str, Any]:
        """
        الحصول على إعدادات الأمان

        Returns:
            Dict: إعدادات الأمان
        """
        try:
            settings = SecuritySettings.query.first()

            if not settings:
                settings = self._create_default_security_settings()

            return {
                "success": True,
                "settings": self._serialize_security_settings(settings),
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على إعدادات الأمان: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على الإعدادات: {str(e)}",
            }

    # ==================== معالج الإعداد ====================

    def run_setup_wizard(self, setup_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تشغيل معالج الإعداد الأولي

        Args:
            setup_data: بيانات الإعداد

        Returns:
            Dict: نتيجة الإعداد
        """
        try:
            results = []

            # الخطوة 1: إعدادات الشركة
            if setup_data.get("company_settings"):
                result = self.update_company_settings(
                    setup_data["company_settings"], setup_data.get("admin_user_id", 1)
                )
                results.append(
                    {
                        "step": "company_settings",
                        "success": result["success"],
                        "message": result["message"],
                    }
                )

            # الخطوة 2: إعدادات البريد الإلكتروني
            if setup_data.get("email_settings"):
                result = self.update_email_settings(
                    setup_data["email_settings"], setup_data.get("admin_user_id", 1)
                )
                results.append(
                    {
                        "step": "email_settings",
                        "success": result["success"],
                        "message": result["message"],
                    }
                )

            # الخطوة 3: إعدادات الأمان
            if setup_data.get("security_settings"):
                result = self.update_security_settings(
                    setup_data["security_settings"], setup_data.get("admin_user_id", 1)
                )
                results.append(
                    {
                        "step": "security_settings",
                        "success": result["success"],
                        "message": result["message"],
                    }
                )

            # الخطوة 4: إعدادات الوحدات
            if setup_data.get("module_settings"):
                for module_name, module_config in setup_data["module_settings"].items():
                    result = self.update_module_settings(
                        module_name, module_config, setup_data.get("admin_user_id", 1)
                    )
                    results.append(
                        {
                            "step": f"module_{module_name}",
                            "success": result["success"],
                            "message": result["message"],
                        }
                    )

            # تحديث حالة الإعداد
            config = SystemConfiguration.query.first()
            if config:
                config.is_setup_complete = True
                config.setup_completed_at = datetime.utcnow()
                db.session.commit()

            success_count = sum(1 for r in results if r["success"])
            total_count = len(results)

            return {
                "success": success_count == total_count,
                "message": f"تم إكمال {success_count} من {total_count} خطوات الإعداد",
                "results": results,
                "setup_complete": success_count == total_count,
            }

        except Exception as e:
            db.session.rollback()
            self.logger.error(f"خطأ في معالج الإعداد: {str(e)}")
            return {"success": False, "message": f"خطأ في معالج الإعداد: {str(e)}"}

    # ==================== الدوال المساعدة ====================

    def _load_default_settings(self) -> Dict[str, Any]:
        """تحميل الإعدادات الافتراضية"""
        return {
            "system": {
                "name": "نظام إدارة المخزون",
                "version": "1.0.0",
                "language": "ar",
                "timezone": "Asia/Riyadh",
                "currency": "SAR",
            },
            "company": {
                "name": "شركة جديدة",
                "country": "SA",
                "currency": "SAR",
                "language": "ar",
            },
            "security": {
                "password_min_length": 8,
                "password_require_uppercase": True,
                "password_require_lowercase": True,
                "password_require_numbers": True,
                "password_require_symbols": False,
                "session_timeout_minutes": 60,
                "max_login_attempts": 5,
            },
        }

    def _create_default_configuration(self) -> SystemConfiguration:
        """إنشاء تكوين افتراضي للنظام"""
        config = SystemConfiguration(
            system_name=self.default_settings["system"]["name"],
            system_version=self.default_settings["system"]["version"],
            default_language=self.default_settings["system"]["language"],
            default_timezone=self.default_settings["system"]["timezone"],
            default_currency=self.default_settings["system"]["currency"],
            is_setup_complete=False,
            maintenance_mode=False,
            debug_mode=False,
        )
        db.session.add(config)
        db.session.commit()
        return config

    def _create_default_company_settings(self) -> CompanySettings:
        """إنشاء إعدادات افتراضية للشركة"""
        settings = CompanySettings(
            company_name=self.default_settings["company"]["name"],
            country=self.default_settings["company"]["country"],
            currency=self.default_settings["company"]["currency"],
            language=self.default_settings["company"]["language"],
        )
        db.session.add(settings)
        db.session.commit()
        return settings

    def _create_default_email_settings(self) -> EmailSettings:
        """إنشاء إعدادات افتراضية للبريد الإلكتروني"""
        settings = EmailSettings(
            smtp_server="",
            smtp_port=587,
            use_tls=True,
            username="",
            password="",
            from_email="",
            from_name="نظام إدارة المخزون",
        )
        db.session.add(settings)
        db.session.commit()
        return settings

    def _create_default_security_settings(self) -> SecuritySettings:
        """إنشاء إعدادات افتراضية للأمان"""
        settings = SecuritySettings(
            password_min_length=self.default_settings["security"][
                "password_min_length"
            ],
            password_require_uppercase=self.default_settings["security"][
                "password_require_uppercase"
            ],
            password_require_lowercase=self.default_settings["security"][
                "password_require_lowercase"
            ],
            password_require_numbers=self.default_settings["security"][
                "password_require_numbers"
            ],
            password_require_symbols=self.default_settings["security"][
                "password_require_symbols"
            ],
            session_timeout_minutes=self.default_settings["security"][
                "session_timeout_minutes"
            ],
            max_login_attempts=self.default_settings["security"]["max_login_attempts"],
        )
        db.session.add(settings)
        db.session.commit()
        return settings

    def _serialize_system_configuration(
        self, config: SystemConfiguration
    ) -> Dict[str, Any]:
        """تحويل تكوين النظام إلى قاموس"""
        return {
            "id": config.id,
            "system_name": config.system_name,
            "system_version": config.system_version,
            "default_language": config.default_language,
            "default_timezone": config.default_timezone,
            "default_currency": config.default_currency,
            "is_setup_complete": config.is_setup_complete,
            "maintenance_mode": config.maintenance_mode,
            "debug_mode": config.debug_mode,
            "custom_settings": config.custom_settings,
            "created_at": config.created_at.isoformat() if config.created_at else None,
            "updated_at": config.updated_at.isoformat() if config.updated_at else None,
        }

    def _serialize_company_settings(self, settings: CompanySettings) -> Dict[str, Any]:
        """تحويل إعدادات الشركة إلى قاموس"""
        return {
            "id": settings.id,
            "company_name": settings.company_name,
            "company_name_en": settings.company_name_en,
            "legal_name": settings.legal_name,
            "tax_number": settings.tax_number,
            "commercial_register": settings.commercial_register,
            "address": settings.address,
            "city": settings.city,
            "state": settings.state,
            "country": settings.country,
            "postal_code": settings.postal_code,
            "phone": settings.phone,
            "fax": settings.fax,
            "email": settings.email,
            "website": settings.website,
            "logo_url": settings.logo_url,
            "currency": settings.currency,
            "language": settings.language,
            "fiscal_year_start": (
                settings.fiscal_year_start.isoformat()
                if settings.fiscal_year_start
                else None
            ),
            "business_type": settings.business_type,
            "industry": settings.industry,
            "employee_count": settings.employee_count,
            "established_date": (
                settings.established_date.isoformat()
                if settings.established_date
                else None
            ),
        }

    def _serialize_module_settings(self, settings: ModuleSettings) -> Dict[str, Any]:
        """تحويل إعدادات الوحدة إلى قاموس"""
        return {
            "id": settings.id,
            "module_name": settings.module_name,
            "is_enabled": settings.is_enabled,
            "version": settings.version,
            "configuration": settings.configuration,
            "permissions": settings.permissions,
            "dependencies": settings.dependencies,
            "auto_update": settings.auto_update,
            "license_key": settings.license_key,
        }

    def _serialize_email_settings(self, settings: EmailSettings) -> Dict[str, Any]:
        """تحويل إعدادات البريد الإلكتروني إلى قاموس"""
        return {
            "id": settings.id,
            "smtp_server": settings.smtp_server,
            "smtp_port": settings.smtp_port,
            "use_tls": settings.use_tls,
            "use_ssl": settings.use_ssl,
            "username": settings.username,
            "from_email": settings.from_email,
            "from_name": settings.from_name,
            "reply_to": settings.reply_to,
            "max_emails_per_hour": settings.max_emails_per_hour,
            "email_templates": settings.email_templates,
        }

    def _serialize_security_settings(
        self, settings: SecuritySettings
    ) -> Dict[str, Any]:
        """تحويل إعدادات الأمان إلى قاموس"""
        return {
            "id": settings.id,
            "password_min_length": settings.password_min_length,
            "password_max_length": settings.password_max_length,
            "password_require_uppercase": settings.password_require_uppercase,
            "password_require_lowercase": settings.password_require_lowercase,
            "password_require_numbers": settings.password_require_numbers,
            "password_require_symbols": settings.password_require_symbols,
            "password_expiry_days": settings.password_expiry_days,
            "password_history_count": settings.password_history_count,
            "session_timeout_minutes": settings.session_timeout_minutes,
            "max_login_attempts": settings.max_login_attempts,
            "lockout_duration_minutes": settings.lockout_duration_minutes,
            "two_factor_required": settings.two_factor_required,
            "ip_whitelist_enabled": settings.ip_whitelist_enabled,
            "allowed_ip_ranges": settings.allowed_ip_ranges,
            "security_headers_enabled": settings.security_headers_enabled,
            "audit_log_retention_days": settings.audit_log_retention_days,
        }


# إنشاء مثيل الخدمة
system_settings_service = SystemSettingsAdvancedService()
