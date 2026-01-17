#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج سجل الأحداث (Journal) الشامل
Comprehensive Journal/Audit Log Model

يسجل جميع العمليات في النظام مع إمكانية التكوين
"""

import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    JSON,
)
from src.database import db


class JournalEventType(enum.Enum):
    """أنواع الأحداث"""

    # الفواتير
    INVOICE_CREATED = "invoice_created"
    INVOICE_VALIDATED = "invoice_validated"
    INVOICE_POSTED = "invoice_posted"
    INVOICE_PAID = "invoice_paid"
    INVOICE_CANCELLED = "invoice_cancelled"
    INVOICE_SENT = "invoice_sent"

    # المدفوعات
    PAYMENT_RECEIVED = "payment_received"
    PAYMENT_SENT = "payment_sent"
    PAYMENT_CANCELLED = "payment_cancelled"

    # المخزون
    STOCK_IN = "stock_in"
    STOCK_OUT = "stock_out"
    STOCK_ADJUSTED = "stock_adjusted"
    STOCK_TRANSFERRED = "stock_transferred"

    # المنتجات
    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"

    # العملاء والموردين
    CUSTOMER_CREATED = "customer_created"
    CUSTOMER_UPDATED = "customer_updated"
    SUPPLIER_CREATED = "supplier_created"
    SUPPLIER_UPDATED = "supplier_updated"

    # المحاسبة
    JOURNAL_ENTRY_CREATED = "journal_entry_created"
    JOURNAL_ENTRY_POSTED = "journal_entry_posted"

    # النظام
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    SETTINGS_CHANGED = "settings_changed"

    # عام
    CUSTOM = "custom"


class JournalEntry(db.Model):
    """سجل الأحداث - Journal Entry"""

    __tablename__ = "journal_entries"
    __table_args__ = (
        Index("idx_journal_event_type", "event_type"),
        Index("idx_journal_model", "model_type", "model_id"),
        Index("idx_journal_user", "user_id"),
        Index("idx_journal_created", "created_at"),
        Index("idx_journal_reference", "reference_number"),
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True)

    # نوع الحدث
    event_type = Column(Enum(JournalEventType), nullable=False)

    # الموديل المرتبط (polymorphic)
    model_type = Column(String(50))  # invoice, payment, product, etc.
    model_id = Column(Integer)

    # رقم مرجعي (مثل INV/2025/00002 أو S00003)
    reference_number = Column(String(100))
    source_reference = Column(String(100))  # المرجع المصدر (مثل S00003)

    # الوصف
    title = Column(String(200), nullable=False)
    description = Column(Text)

    # التغييرات (قبل وبعد)
    old_values = Column(JSON)  # القيم القديمة
    new_values = Column(JSON)  # القيم الجديدة
    changes = Column(JSON)  # ملخص التغييرات

    # معلومات المستخدم
    user_id = Column(Integer, ForeignKey("users.id"))
    user_name = Column(String(100))

    # معلومات الطلب
    ip_address = Column(String(45))
    user_agent = Column(String(500))

    # بيانات إضافية
    extra_data = Column(JSON)

    # التواريخ
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # العلاقات
    user = db.relationship("src.models.user.User", foreign_keys=[user_id])

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "event_type": self.event_type.value if self.event_type else None,
            "model_type": self.model_type,
            "model_id": self.model_id,
            "reference_number": self.reference_number,
            "source_reference": self.source_reference,
            "title": self.title,
            "description": self.description,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "changes": self.changes,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "extra_data": self.extra_data,
        }

    def __repr__(self):
        return f'<JournalEntry {self.id} - {self.event_type.value if self.event_type else "unknown"}>'


class JournalConfig(db.Model):
    """إعدادات تكوين سجل الأحداث"""

    __tablename__ = "journal_config"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)

    # نوع الحدث
    event_type = Column(String(50), unique=True, nullable=False)

    # هل يتم تسجيل هذا الحدث؟
    is_enabled = Column(Boolean, default=True)

    # هل يتم إرسال إشعار؟
    send_notification = Column(Boolean, default=False)
    notification_channels = Column(JSON)  # ['email', 'sms', 'push']

    # هل يتم إرسال بريد إلكتروني؟
    send_email = Column(Boolean, default=False)
    email_template = Column(String(100))
    email_recipients = Column(JSON)  # قائمة المستلمين

    # الاحتفاظ بالسجلات (بالأيام)
    retention_days = Column(Integer, default=365)

    # إعدادات إضافية
    settings = Column(JSON)

    # التواريخ
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "is_enabled": self.is_enabled,
            "send_notification": self.send_notification,
            "notification_channels": self.notification_channels,
            "send_email": self.send_email,
            "email_template": self.email_template,
            "email_recipients": self.email_recipients,
            "retention_days": self.retention_days,
            "settings": self.settings,
        }
