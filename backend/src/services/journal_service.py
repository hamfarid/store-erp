#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
خدمة سجل الأحداث (Journal Service)
Comprehensive Journal/Audit Service

خدمة مركزية لتسجيل جميع الأحداث في النظام
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from flask import request, g
from src.database import db
from src.models.journal import JournalEntry, JournalEventType, JournalConfig

logger = logging.getLogger(__name__)


class JournalService:
    """خدمة إدارة سجل الأحداث"""

    # قاموس الرسائل للأحداث
    EVENT_MESSAGES = {
        JournalEventType.INVOICE_CREATED: "Invoice Created",
        JournalEventType.INVOICE_VALIDATED: "Invoice validated",
        JournalEventType.INVOICE_POSTED: "Invoice posted",
        JournalEventType.INVOICE_PAID: "Invoice paid",
        JournalEventType.INVOICE_CANCELLED: "Invoice cancelled",
        JournalEventType.INVOICE_SENT: "Invoice sent to customer",
        JournalEventType.PAYMENT_RECEIVED: "Payment received",
        JournalEventType.PAYMENT_SENT: "Payment sent",
        JournalEventType.STOCK_IN: "Stock received",
        JournalEventType.STOCK_OUT: "Stock dispatched",
        JournalEventType.STOCK_ADJUSTED: "Stock adjusted",
        JournalEventType.PRODUCT_CREATED: "Product created",
        JournalEventType.PRODUCT_UPDATED: "Product updated",
        JournalEventType.JOURNAL_ENTRY_CREATED: "Journal entry created",
    }

    @classmethod
    def log(
        cls,
        event_type: JournalEventType,
        model_type: str = None,
        model_id: int = None,
        reference_number: str = None,
        source_reference: str = None,
        title: str = None,
        description: str = None,
        old_values: Dict = None,
        new_values: Dict = None,
        changes: Dict = None,
        metadata: Dict = None,
        user_id: int = None,
        user_name: str = None,
    ) -> Optional[JournalEntry]:
        """تسجيل حدث في السجل"""
        try:
            # التحقق من تفعيل تسجيل هذا الحدث
            if not cls._is_event_enabled(event_type):
                return None

            # الحصول على معلومات المستخدم
            if not user_id:
                user_id = getattr(g, "user_id", None) or getattr(
                    g, "current_user_id", None
                )
            if not user_name:
                user_name = getattr(g, "user_name", None) or "System"

            # إنشاء العنوان الافتراضي
            if not title:
                title = cls.EVENT_MESSAGES.get(event_type, event_type.value)

            # إنشاء سجل الحدث
            entry = JournalEntry(
                event_type=event_type,
                model_type=model_type,
                model_id=model_id,
                reference_number=reference_number,
                source_reference=source_reference,
                title=title,
                description=description,
                old_values=old_values,
                new_values=new_values,
                changes=changes,
                user_id=user_id,
                user_name=user_name,
                extra_data=metadata,
            )

            # إضافة معلومات الطلب
            try:
                entry.ip_address = request.remote_addr
                entry.user_agent = request.headers.get("User-Agent", "")[:500]
            except RuntimeError:
                pass  # خارج سياق الطلب

            db.session.add(entry)
            db.session.commit()

            # إرسال الإشعارات إذا كانت مفعلة
            cls._send_notifications(event_type, entry)

            logger.info(f"Journal: {event_type.value} - {reference_number or model_id}")
            return entry

        except Exception as e:
            logger.error(f"Failed to log journal entry: {e}")
            db.session.rollback()
            return None

    @classmethod
    def log_invoice_event(
        cls,
        invoice,
        event_type: JournalEventType,
        description: str = None,
        old_values: Dict = None,
        new_values: Dict = None,
    ) -> Optional[JournalEntry]:
        """تسجيل حدث فاتورة"""
        changes = None
        if old_values and new_values:
            changes = cls._calculate_changes(old_values, new_values)

        return cls.log(
            event_type=event_type,
            model_type="invoice",
            model_id=invoice.id,
            reference_number=invoice.invoice_number,
            source_reference=invoice.reference_number or invoice.po_number,
            description=description,
            old_values=old_values,
            new_values=new_values,
            changes=changes,
            metadata={
                "invoice_type": (
                    invoice.invoice_type.value if invoice.invoice_type else None
                ),
                "total_amount": (
                    float(invoice.total_amount) if invoice.total_amount else 0
                ),
                "customer_id": invoice.customer_id,
                "supplier_id": invoice.supplier_id,
            },
        )

    @classmethod
    def log_from_source(
        cls,
        source_reference: str,
        event_type: JournalEventType,
        title: str,
        description: str = None,
        metadata: Dict = None,
    ) -> Optional[JournalEntry]:
        """تسجيل حدث من مصدر (مثل S00003)"""
        return cls.log(
            event_type=event_type,
            source_reference=source_reference,
            title=title,
            description=description,
            metadata=metadata,
        )

    @classmethod
    def _is_event_enabled(cls, event_type: JournalEventType) -> bool:
        """التحقق من تفعيل تسجيل هذا الحدث"""
        try:
            config = JournalConfig.query.filter_by(event_type=event_type.value).first()
            return config.is_enabled if config else True
        except Exception:
            return True

    @classmethod
    def _send_notifications(cls, event_type: JournalEventType, entry: JournalEntry):
        """إرسال الإشعارات"""
        try:
            config = JournalConfig.query.filter_by(event_type=event_type.value).first()
            if not config:
                return
            # يمكن إضافة منطق الإشعارات هنا
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    @staticmethod
    def _calculate_changes(old: Dict, new: Dict) -> Dict:
        """حساب التغييرات بين القيم القديمة والجديدة"""
        changes = {}
        all_keys = set(old.keys()) | set(new.keys())
        for key in all_keys:
            old_val = old.get(key)
            new_val = new.get(key)
            if old_val != new_val:
                changes[key] = {"from": old_val, "to": new_val}
        return changes

    @classmethod
    def get_all_event_types(cls) -> List[str]:
        """الحصول على جميع أنواع الأحداث"""
        return [e.value for e in JournalEventType]

    @classmethod
    def get_event_type_info(cls) -> List[Dict[str, str]]:
        """الحصول على معلومات أنواع الأحداث"""
        return [
            {
                "value": e.value,
                "name": e.name,
                "message": cls.EVENT_MESSAGES.get(e, e.value),
            }
            for e in JournalEventType
        ]
