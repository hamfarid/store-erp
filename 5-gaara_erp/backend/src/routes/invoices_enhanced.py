#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مسارات الفواتير المحسنة مع Journal
Enhanced Invoice Routes with Journal Integration
"""

import logging
from flask import Blueprint, jsonify, request
from src.database import db
from src.models.invoice_unified import Invoice, InvoiceStatus
from src.models.journal import JournalEventType
from src.services.journal_service import JournalService
from src.services.invoice_email_service import InvoiceEmailService

logger = logging.getLogger(__name__)

invoices_enhanced_bp = Blueprint(
    "invoices_enhanced", __name__, url_prefix="/api/invoices"
)


@invoices_enhanced_bp.route("/<int:invoice_id>/validate", methods=["POST"])
def validate_invoice(invoice_id):
    """Validate and post invoice"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        service = InvoiceEmailService()
        result = service.validate_invoice(invoice)
        return jsonify(result), 200 if result["success"] else 400
    except Exception as e:
        logger.error(f"Error validating invoice: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@invoices_enhanced_bp.route("/<int:invoice_id>/send-email", methods=["POST"])
def send_invoice_email(invoice_id):
    """Send invoice via email with PDF"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json() or {}

        recipient_email = data.get("email")
        recipient_name = data.get("name")

        if not recipient_email:
            # Try to get from customer
            if invoice.customer:
                recipient_email = getattr(invoice.customer, "email", None)
                recipient_name = getattr(invoice.customer, "name", None)

        if not recipient_email:
            return jsonify({"success": False, "message": "Email address required"}), 400

        service = InvoiceEmailService()
        result = service.send_invoice_email(invoice, recipient_email, recipient_name)
        return jsonify(result), 200 if result["success"] else 400

    except Exception as e:
        logger.error(f"Error sending invoice email: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@invoices_enhanced_bp.route("/<int:invoice_id>/pdf", methods=["GET"])
def download_invoice_pdf(invoice_id):
    """Download invoice as PDF"""
    try:
        from flask import Response

        invoice = Invoice.query.get_or_404(invoice_id)
        service = InvoiceEmailService()
        pdf_bytes = service.generate_pdf(invoice.to_dict())

        filename = f"{invoice.invoice_number.replace('/', '_')}.pdf"
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@invoices_enhanced_bp.route("/<int:invoice_id>/journal", methods=["GET"])
def get_invoice_journal(invoice_id):
    """Get journal entries for invoice"""
    try:
        from src.models.journal import JournalEntry

        entries = (
            JournalEntry.query.filter_by(model_type="invoice", model_id=invoice_id)
            .order_by(JournalEntry.created_at.desc())
            .all()
        )

        return jsonify({"success": True, "data": [e.to_dict() for e in entries]})
    except Exception as e:
        logger.error(f"Error getting invoice journal: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@invoices_enhanced_bp.route("/<int:invoice_id>/status", methods=["PATCH"])
def update_invoice_status(invoice_id):
    """Update invoice status with journal logging"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()
        new_status = data.get("status")

        if not new_status:
            return jsonify({"success": False, "message": "Status required"}), 400

        old_status = invoice.status.value if invoice.status else "draft"

        # Map status string to enum
        status_map = {
            "draft": InvoiceStatus.DRAFT,
            "confirmed": InvoiceStatus.CONFIRMED,
            "paid": InvoiceStatus.PAID,
            "cancelled": InvoiceStatus.CANCELLED,
            "posted": InvoiceStatus.CONFIRMED,
        }

        if new_status.lower() not in status_map:
            return jsonify({"success": False, "message": "Invalid status"}), 400

        invoice.status = status_map[new_status.lower()]
        db.session.commit()

        # Determine event type
        event_map = {
            "confirmed": JournalEventType.INVOICE_VALIDATED,
            "posted": JournalEventType.INVOICE_POSTED,
            "paid": JournalEventType.INVOICE_PAID,
            "cancelled": JournalEventType.INVOICE_CANCELLED,
        }
        event_type = event_map.get(
            new_status.lower(), JournalEventType.INVOICE_VALIDATED
        )

        JournalService.log_invoice_event(
            invoice,
            event_type,
            old_values={"status": old_status},
            new_values={"status": new_status},
        )

        return jsonify(
            {
                "success": True,
                "message": f"Status updated to {new_status}",
                "data": invoice.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating status: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
