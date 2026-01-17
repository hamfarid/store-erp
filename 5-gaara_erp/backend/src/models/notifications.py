"""
Notifications System
نظام الإشعارات - إدارة التنبيهات لتواريخ الانتهاء والمواعيد المهمة
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json


class NotificationSystem:
    """
    نظام الإشعارات
    يدير التنبيهات لـ:
    - تواريخ انتهاء فحص الوزارة
    - تواريخ انتهاء التسجيل والحماية
    - تواريخ انتهاء البطاقات والجوازات
    - تواريخ انتهاء رخص الأشخاص والعربيات
    - تواريخ انتهاء أوراق الشركة
    """

    def __init__(self, db_connection=None):
        """تهيئة نظام الإشعارات"""
        self.db = db_connection
        self._create_tables()

    def _create_tables(self):
        """إنشاء جداول نظام الإشعارات"""
        if not self.db:
            return

        cursor = self.db.cursor()

        # جدول إعدادات الإشعارات
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notification_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_type TEXT NOT NULL UNIQUE,
                days_before_expiry INTEGER NOT NULL DEFAULT 30,
                enabled BOOLEAN DEFAULT 1,
                send_email BOOLEAN DEFAULT 1,
                send_sms BOOLEAN DEFAULT 0,
                send_system_notification BOOLEAN DEFAULT 1,
                recipients TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول تواريخ انتهاء المنتجات (التسجيل والحماية)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS product_expiry_dates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                expiry_type TEXT NOT NULL,
                registration_number TEXT,
                protection_number TEXT,
                registration_date DATE,
                expiry_date DATE NOT NULL,
                renewal_cost REAL,
                document_image_path TEXT,
                alert_days_before INTEGER DEFAULT 30,
                status TEXT DEFAULT 'active',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """
        )

        # جدول تواريخ انتهاء وثائق الموظفين
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employee_document_expiry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                employee_name TEXT NOT NULL,
                document_type TEXT NOT NULL,
                document_number TEXT,
                issue_date DATE,
                expiry_date DATE NOT NULL,
                issuing_authority TEXT,
                document_image_path TEXT,
                alert_days_before INTEGER DEFAULT 30,
                status TEXT DEFAULT 'active',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول تواريخ انتهاء رخص المركبات
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vehicle_license_expiry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                vehicle_number TEXT NOT NULL,
                license_type TEXT NOT NULL,
                license_number TEXT,
                issue_date DATE,
                expiry_date DATE NOT NULL,
                renewal_cost REAL,
                document_image_path TEXT,
                alert_days_before INTEGER DEFAULT 30,
                status TEXT DEFAULT 'active',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول تواريخ انتهاء وثائق الشركة
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS company_document_expiry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_type TEXT NOT NULL,
                document_number TEXT,
                issue_date DATE,
                expiry_date DATE NOT NULL,
                issuing_authority TEXT,
                renewal_cost REAL,
                document_image_path TEXT,
                alert_days_before INTEGER DEFAULT 30,
                status TEXT DEFAULT 'active',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول الإشعارات المرسلة
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sent_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_type TEXT NOT NULL,
                reference_type TEXT NOT NULL,
                reference_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT DEFAULT 'info',
                sent_to TEXT,
                sent_via TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP,
                acknowledged_at TIMESTAMP,
                acknowledged_by INTEGER,
                status TEXT DEFAULT 'sent'
            )
        """
        )

        # إنشاء فهارس
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_product_expiry_date
            ON product_expiry_dates(expiry_date)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_employee_doc_expiry_date
            ON employee_document_expiry(expiry_date)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_vehicle_license_expiry_date
            ON vehicle_license_expiry(expiry_date)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_company_doc_expiry_date
            ON company_document_expiry(expiry_date)
        """
        )

        # إدراج إعدادات افتراضية
        cursor.execute(
            """
            INSERT OR IGNORE INTO notification_settings
            (notification_type, days_before_expiry) VALUES
            ('product_registration', 30),
            ('product_protection', 30),
            ('ministry_inspection', 15),
            ('employee_passport', 60),
            ('employee_id_card', 30),
            ('employee_license', 30),
            ('vehicle_license', 30),
            ('vehicle_insurance', 15),
            ('company_commercial_register', 60),
            ('company_tax_card', 60),
            ('company_vat_certificate', 60),
            ('company_activity_license', 60)
        """
        )

        self.db.commit()

    def add_product_expiry(
        self,
        product_id: int,
        product_name: str,
        expiry_type: str,
        expiry_date: datetime,
        registration_number: Optional[str] = None,
        protection_number: Optional[str] = None,
        registration_date: Optional[datetime] = None,
        renewal_cost: Optional[float] = None,
        document_image_path: Optional[str] = None,
        alert_days_before: int = 30,
        notes: Optional[str] = None,
    ) -> int:
        """إضافة تاريخ انتهاء منتج"""
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO product_expiry_dates (
                product_id, product_name, expiry_type, registration_number,
                protection_number, registration_date, expiry_date, renewal_cost,
                document_image_path, alert_days_before, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                product_id,
                product_name,
                expiry_type,
                registration_number,
                protection_number,
                registration_date.date() if registration_date else None,
                expiry_date.date(),
                renewal_cost,
                document_image_path,
                alert_days_before,
                notes,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def add_employee_document_expiry(
        self,
        employee_id: int,
        employee_name: str,
        document_type: str,
        expiry_date: datetime,
        document_number: Optional[str] = None,
        issue_date: Optional[datetime] = None,
        issuing_authority: Optional[str] = None,
        document_image_path: Optional[str] = None,
        alert_days_before: int = 30,
        notes: Optional[str] = None,
    ) -> int:
        """إضافة تاريخ انتهاء وثيقة موظف"""
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO employee_document_expiry (
                employee_id, employee_name, document_type, document_number,
                issue_date, expiry_date, issuing_authority, document_image_path,
                alert_days_before, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                employee_id,
                employee_name,
                document_type,
                document_number,
                issue_date.date() if issue_date else None,
                expiry_date.date(),
                issuing_authority,
                document_image_path,
                alert_days_before,
                notes,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def add_company_document_expiry(
        self,
        document_type: str,
        expiry_date: datetime,
        document_number: Optional[str] = None,
        issue_date: Optional[datetime] = None,
        issuing_authority: Optional[str] = None,
        renewal_cost: Optional[float] = None,
        document_image_path: Optional[str] = None,
        alert_days_before: int = 60,
        notes: Optional[str] = None,
    ) -> int:
        """إضافة تاريخ انتهاء وثيقة شركة"""
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO company_document_expiry (
                document_type, document_number, issue_date, expiry_date,
                issuing_authority, renewal_cost, document_image_path,
                alert_days_before, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                document_type,
                document_number,
                issue_date.date() if issue_date else None,
                expiry_date.date(),
                issuing_authority,
                renewal_cost,
                document_image_path,
                alert_days_before,
                notes,
            ),
        )
        self.db.commit()
        return cursor.lastrowid
