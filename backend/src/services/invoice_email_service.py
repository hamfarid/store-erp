#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
خدمة البريد الإلكتروني للفواتير
Invoice Email Service

Features:
- Send invoice emails with PDF attachment
- Generate professional invoice PDFs
- Journal/Audit log for invoice actions
- Support for Arabic and English
"""

import os
import io
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

from flask import current_app
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.database import db

logger = logging.getLogger(__name__)


class InvoiceEmailService:
    """خدمة إرسال البريد الإلكتروني للفواتير"""

    def __init__(self):
        self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
        self.smtp_user = os.environ.get("SMTP_USER", "")
        self.smtp_password = os.environ.get("SMTP_PASSWORD", "")
        self.from_email = os.environ.get("FROM_EMAIL", "noreply@store.com")
        self.company_name = os.environ.get("COMPANY_NAME", "Seeds")

    def generate_invoice_number(self, year: int = None, sequence: int = None) -> str:
        """
        توليد رقم فاتورة بتنسيق INV/YYYY/NNNNN
        Generate invoice number in format INV/YYYY/NNNNN
        """
        if year is None:
            year = datetime.now().year

        if sequence is None:
            # الحصول على آخر رقم تسلسلي
            from src.models.invoice_unified import Invoice

            last_invoice = (
                Invoice.query.filter(Invoice.invoice_number.like(f"INV/{year}/%"))
                .order_by(Invoice.id.desc())
                .first()
            )

            if last_invoice:
                try:
                    last_seq = int(last_invoice.invoice_number.split("/")[-1])
                    sequence = last_seq + 1
                except (ValueError, IndexError):
                    sequence = 1
            else:
                sequence = 1

        return f"INV/{year}/{sequence:05d}"

    def generate_pdf(self, invoice_data: Dict[str, Any]) -> bytes:
        """
        إنشاء ملف PDF للفاتورة
        Generate PDF file for invoice
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()
        story = []

        # العنوان
        title_style = ParagraphStyle(
            "Title", parent=styles["Heading1"], fontSize=18, alignment=1, spaceAfter=20
        )
        story.append(
            Paragraph(f"Invoice {invoice_data.get('invoice_number', '')}", title_style)
        )
        story.append(Spacer(1, 0.5 * cm))

        # معلومات الفاتورة
        info_data = [
            ["Invoice Number:", invoice_data.get("invoice_number", "")],
            ["Reference:", invoice_data.get("reference_number", "")],
            ["Date:", invoice_data.get("invoice_date", "")],
            ["Due Date:", invoice_data.get("due_date", "")],
            ["Customer:", invoice_data.get("customer_name", "")],
            ["Status:", invoice_data.get("status", "Draft")],
        ]

        info_table = Table(info_data, colWidths=[4 * cm, 10 * cm])
        info_table.setStyle(
            TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ]
            )
        )
        story.append(info_table)
        story.append(Spacer(1, 1 * cm))

        # جدول العناصر
        items = invoice_data.get("items", [])
        if items:
            item_data = [["#", "Description", "Qty", "Unit Price", "Total"]]
            for i, item in enumerate(items, 1):
                item_data.append(
                    [
                        str(i),
                        item.get("product_name", ""),
                        str(item.get("quantity", 0)),
                        f"{item.get('price', 0):.2f}",
                        f"{item.get('total', 0):.2f}",
                    ]
                )

            item_table = Table(
                item_data, colWidths=[1 * cm, 8 * cm, 2 * cm, 3 * cm, 3 * cm]
            )
            item_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            story.append(item_table)

        story.append(Spacer(1, 1 * cm))

        # الإجمالي
        total_data = [
            ["Subtotal:", f"{invoice_data.get('subtotal', 0):.2f}"],
            ["Tax:", f"{invoice_data.get('tax_amount', 0):.2f}"],
            [
                "Total:",
                f"{invoice_data.get('total_amount', 0):.2f} {invoice_data.get('currency', 'LE')}",
            ],
        ]
        total_table = Table(total_data, colWidths=[12 * cm, 5 * cm])
        total_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(total_table)

        doc.build(story)
        return buffer.getvalue()

    def send_invoice_email(
        self, invoice, recipient_email: str, recipient_name: str = None
    ) -> Dict[str, Any]:
        """
        إرسال فاتورة بالبريد الإلكتروني مع ملف PDF
        Send invoice email with PDF attachment
        """
        try:
            # تحضير بيانات الفاتورة
            invoice_data = invoice.to_dict() if hasattr(invoice, "to_dict") else invoice
            invoice_number = invoice_data.get("invoice_number", "Unknown")
            reference = invoice_data.get("reference_number", "")
            total = invoice_data.get("total_amount", 0)
            currency = invoice_data.get("currency", "LE")

            # إنشاء PDF
            pdf_bytes = self.generate_pdf(invoice_data)
            pdf_filename = f"{invoice_number.replace('/', '_')}.pdf"

            # إنشاء رسالة البريد
            msg = MIMEMultipart()
            msg["From"] = f"{self.company_name} <{self.from_email}>"
            msg["To"] = recipient_email
            msg["Subject"] = f"Invoice {invoice_number} from {self.company_name}"

            # نص البريد
            body = self._generate_email_body(
                recipient_name or "Customer", invoice_number, reference, total, currency
            )
            msg.attach(MIMEText(body, "html", "utf-8"))

            # إرفاق PDF
            pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
            pdf_attachment.add_header(
                "Content-Disposition", "attachment", filename=pdf_filename
            )
            msg.attach(pdf_attachment)

            # إرسال البريد
            if self.smtp_user and self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)

                # تسجيل في Journal
                from src.services.journal_service import JournalService
                from src.models.journal import JournalEventType

                JournalService.log(
                    event_type=JournalEventType.INVOICE_SENT,
                    model_type="invoice",
                    model_id=invoice_data.get("id"),
                    reference_number=invoice_number,
                    title=f"Invoice sent to {recipient_email}",
                    description=f"Invoice {invoice_number} sent to {recipient_name}",
                )

                return {"success": True, "message": "تم إرسال الفاتورة بنجاح"}
            else:
                return {"success": False, "message": "SMTP not configured"}

        except Exception as e:
            logger.error(f"Failed to send invoice email: {e}")
            return {"success": False, "message": str(e)}

    def _generate_email_body(
        self,
        name: str,
        invoice_number: str,
        reference: str,
        total: float,
        currency: str,
    ) -> str:
        """Generate HTML email body"""
        ref_text = f" (with reference: {reference})" if reference else ""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <p>Dear {name},</p>

            <p>Here is your invoice <strong>{invoice_number}</strong>{ref_text}
            amounting in <strong>{total:,.2f} {currency}</strong> from {self.company_name}.
            Please remit payment at your earliest convenience.</p>

            <p>Please use the following communication for your payment:
            <strong>{invoice_number}</strong></p>

            <p>Do not hesitate to contact us if you have any questions.</p>

            <hr style="border: 1px solid #eee;">
            <p style="color: #666; font-size: 12px;">
                This email was sent automatically by {self.company_name}
            </p>
        </body>
        </html>
        """

    def validate_invoice(self, invoice) -> Dict[str, Any]:
        """Validate and post invoice with journal logging"""
        try:
            from src.models.invoice_unified import InvoiceStatus
            from src.services.journal_service import JournalService
            from src.models.journal import JournalEventType

            old_status = invoice.status.value if invoice.status else "draft"

            # Update status to confirmed/posted
            invoice.status = InvoiceStatus.CONFIRMED
            db.session.commit()

            # Log validation
            JournalService.log_invoice_event(
                invoice,
                JournalEventType.INVOICE_VALIDATED,
                description="Invoice validated and reviewed",
                old_values={"status": old_status},
                new_values={"status": "confirmed"},
            )

            # Log posting
            JournalService.log_invoice_event(
                invoice,
                JournalEventType.INVOICE_POSTED,
                description="Invoice posted to accounting",
            )

            # Log journal entry creation
            JournalService.log(
                event_type=JournalEventType.JOURNAL_ENTRY_CREATED,
                model_type="invoice",
                model_id=invoice.id,
                reference_number=invoice.invoice_number,
                source_reference=invoice.reference_number,
                title="This journal entry has been created from: "
                + (invoice.reference_number or invoice.invoice_number),
            )

            return {
                "success": True,
                "message": "Invoice validated and posted",
                "changes": [
                    {"field": "Reviewed", "old": "No", "new": "Yes"},
                    {"field": "Number", "old": "None", "new": invoice.invoice_number},
                    {
                        "field": "Payment Reference",
                        "old": "None",
                        "new": invoice.invoice_number,
                    },
                    {"field": "Status", "old": "Draft", "new": "Posted"},
                ],
            }
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to validate invoice: {e}")
            return {"success": False, "message": str(e)}
