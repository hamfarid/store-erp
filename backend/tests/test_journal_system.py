#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Journal/Audit Log System
اختبارات نظام السجلات والمراجعة
"""

import pytest
from datetime import datetime


class TestJournalModels:
    """Test Journal models and enums"""

    def test_journal_event_type_enum(self):
        """Test JournalEventType enum values"""
        from src.models.journal import JournalEventType

        # Test invoice events
        assert JournalEventType.INVOICE_CREATED.value == "invoice_created"
        assert JournalEventType.INVOICE_VALIDATED.value == "invoice_validated"
        assert JournalEventType.INVOICE_POSTED.value == "invoice_posted"
        assert JournalEventType.INVOICE_PAID.value == "invoice_paid"

        # Test payment events
        assert JournalEventType.PAYMENT_RECEIVED.value == "payment_received"
        assert JournalEventType.PAYMENT_SENT.value == "payment_sent"

        # Test stock events
        assert JournalEventType.STOCK_IN.value == "stock_in"
        assert JournalEventType.STOCK_OUT.value == "stock_out"

    def test_journal_entry_model_import(self):
        """Test JournalEntry model can be imported"""
        from src.models.journal import JournalEntry

        assert JournalEntry is not None
        assert hasattr(JournalEntry, "event_type")
        assert hasattr(JournalEntry, "reference_number")
        assert hasattr(JournalEntry, "model_type")
        assert hasattr(JournalEntry, "model_id")

    def test_journal_config_model_import(self):
        """Test JournalConfig model can be imported"""
        from src.models.journal import JournalConfig

        assert JournalConfig is not None
        assert hasattr(JournalConfig, "event_type")
        assert hasattr(JournalConfig, "is_enabled")
        assert hasattr(JournalConfig, "send_notification")
        assert hasattr(JournalConfig, "send_email")


class TestJournalService:
    """Test JournalService functionality"""

    def test_journal_service_import(self):
        """Test JournalService can be imported"""
        from src.services.journal_service import JournalService

        assert JournalService is not None
        assert hasattr(JournalService, "log")
        assert hasattr(JournalService, "log_invoice_event")
        assert hasattr(JournalService, "log_from_source")

    def test_get_all_event_types(self):
        """Test getting all event types"""
        from src.services.journal_service import JournalService

        event_types = JournalService.get_all_event_types()

        assert isinstance(event_types, list)
        assert len(event_types) > 0
        assert "invoice_created" in event_types
        assert "payment_received" in event_types


class TestJournalRoutes:
    """Test Journal API routes"""

    def test_journal_blueprint_import(self):
        """Test journal blueprint can be imported"""
        from src.routes.journal import journal_bp

        assert journal_bp is not None
        assert journal_bp.name == "journal"


class TestInvoiceEmailService:
    """Test InvoiceEmailService functionality"""

    def test_invoice_email_service_import(self):
        """Test InvoiceEmailService can be imported"""
        from src.services.invoice_email_service import InvoiceEmailService

        assert InvoiceEmailService is not None

    def test_generate_invoice_number_format(self):
        """Test invoice number generation format"""
        from src.services.invoice_email_service import InvoiceEmailService

        service = InvoiceEmailService()

        # Test with explicit parameters
        inv_num = service.generate_invoice_number(year=2025, sequence=2)
        assert inv_num == "INV/2025/00002"

        inv_num = service.generate_invoice_number(year=2025, sequence=123)
        assert inv_num == "INV/2025/00123"

    def test_generate_email_body(self):
        """Test email body generation"""
        from src.services.invoice_email_service import InvoiceEmailService

        service = InvoiceEmailService()

        body = service._generate_email_body(
            name="محمد ابراهيم",
            invoice_number="INV/2025/00002",
            reference="S00003",
            total=25000.00,
            currency="LE",
        )

        assert "Dear محمد ابراهيم" in body
        assert "INV/2025/00002" in body
        assert "S00003" in body
        assert "25,000.00 LE" in body


class TestInvoicesEnhancedRoutes:
    """Test enhanced invoice routes"""

    def test_invoices_enhanced_blueprint_import(self):
        """Test invoices_enhanced blueprint can be imported"""
        from src.routes.invoices_enhanced import invoices_enhanced_bp

        assert invoices_enhanced_bp is not None
        assert invoices_enhanced_bp.name == "invoices_enhanced"
