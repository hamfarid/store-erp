"""
PDF Generator Module
@file backend/src/utils/pdf_generator.py

مولد تقارير PDF مع دعم العربية
"""

import os
import io
from typing import List, Dict, Any, Optional
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
import logging

logger = logging.getLogger(__name__)


class ArabicPDFGenerator:
    """PDF generator with Arabic support"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_arabic_fonts()
        self._setup_styles()
    
    def _setup_arabic_fonts(self):
        """Setup Arabic fonts"""
        # Try to register Arabic font
        font_paths = [
            'fonts/arabic/NotoSansArabic-Regular.ttf',
            'static/fonts/NotoSansArabic-Regular.ttf',
            '/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf',
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('Arabic', font_path))
                    logger.info(f"Arabic font registered from {font_path}")
                    return
                except Exception as e:
                    logger.warning(f"Failed to register font from {font_path}: {e}")
        
        logger.warning("Arabic font not found, using default font")
    
    def _setup_styles(self):
        """Setup custom styles"""
        # Arabic title style
        self.styles.add(ParagraphStyle(
            name='ArabicTitle',
            fontName='Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#1e3a8a')
        ))
        
        # Arabic subtitle style
        self.styles.add(ParagraphStyle(
            name='ArabicSubtitle',
            fontName='Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            fontSize=14,
            alignment=TA_RIGHT,
            spaceAfter=12,
            textColor=colors.HexColor('#374151')
        ))
        
        # Arabic normal style
        self.styles.add(ParagraphStyle(
            name='ArabicNormal',
            fontName='Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            fontSize=11,
            alignment=TA_RIGHT,
            spaceAfter=8
        ))
    
    def _reverse_arabic(self, text: str) -> str:
        """Reverse Arabic text for proper display in PDF"""
        # Simple reversal for RTL display
        # In production, use arabic_reshaper and bidi libraries
        return text[::-1] if any('\u0600' <= c <= '\u06FF' for c in text) else text
    
    def generate_invoice_pdf(self, invoice_data: Dict[str, Any]) -> bytes:
        """
        Generate invoice PDF
        
        Args:
            invoice_data: Invoice details including items, customer info, totals
        
        Returns:
            PDF content as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        elements = []
        
        # Header
        elements.append(Paragraph(
            self._reverse_arabic("فاتورة مبيعات"),
            self.styles['ArabicTitle']
        ))
        
        # Invoice info
        info_data = [
            [self._reverse_arabic(f"التاريخ: {invoice_data.get('date', '')}"),
             self._reverse_arabic(f"رقم الفاتورة: {invoice_data.get('number', '')}")],
            [self._reverse_arabic(f"العميل: {invoice_data.get('customer_name', '')}"),
             self._reverse_arabic(f"الهاتف: {invoice_data.get('customer_phone', '')}")]
        ]
        
        info_table = Table(info_data, colWidths=[doc.width/2]*2)
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Items table
        headers = [
            self._reverse_arabic('الإجمالي'),
            self._reverse_arabic('السعر'),
            self._reverse_arabic('الكمية'),
            self._reverse_arabic('المنتج'),
            '#'
        ]
        
        items_data = [headers]
        for idx, item in enumerate(invoice_data.get('items', []), 1):
            items_data.append([
                f"{item.get('total', 0):.2f}",
                f"{item.get('price', 0):.2f}",
                str(item.get('quantity', 0)),
                self._reverse_arabic(item.get('name', '')),
                str(idx)
            ])
        
        # Totals
        items_data.append(['', '', '', self._reverse_arabic('المجموع الفرعي'), f"{invoice_data.get('subtotal', 0):.2f}"])
        if invoice_data.get('discount', 0) > 0:
            items_data.append(['', '', '', self._reverse_arabic('الخصم'), f"-{invoice_data.get('discount', 0):.2f}"])
        if invoice_data.get('tax', 0) > 0:
            items_data.append(['', '', '', self._reverse_arabic('الضريبة'), f"{invoice_data.get('tax', 0):.2f}"])
        items_data.append(['', '', '', self._reverse_arabic('الإجمالي'), f"{invoice_data.get('total', 0):.2f}"])
        
        items_table = Table(items_data, colWidths=[2*cm, 2.5*cm, 2*cm, 8*cm, 1*cm])
        items_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -5), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -5), colors.HexColor('#f9fafb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -5), [colors.white, colors.HexColor('#f3f4f6')]),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(items_table)
        
        # Footer
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            self._reverse_arabic("شكراً لتعاملكم معنا"),
            self.styles['ArabicNormal']
        ))
        
        doc.build(elements)
        return buffer.getvalue()
    
    def generate_report_pdf(
        self,
        title: str,
        data: List[Dict[str, Any]],
        columns: List[Dict[str, str]],
        summary: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Generate a generic report PDF
        
        Args:
            title: Report title
            data: List of data rows
            columns: Column definitions [{'key': str, 'label': str, 'width': float}]
            summary: Optional summary data
        
        Returns:
            PDF content as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        elements = []
        
        # Title
        elements.append(Paragraph(
            self._reverse_arabic(title),
            self.styles['ArabicTitle']
        ))
        
        # Date
        elements.append(Paragraph(
            self._reverse_arabic(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
            self.styles['ArabicNormal']
        ))
        elements.append(Spacer(1, 20))
        
        # Headers
        headers = [self._reverse_arabic(col['label']) for col in reversed(columns)]
        col_widths = [col.get('width', 3)*cm for col in reversed(columns)]
        
        # Data rows
        table_data = [headers]
        for row in data:
            row_data = []
            for col in reversed(columns):
                value = row.get(col['key'], '')
                if isinstance(value, (int, float)):
                    row_data.append(f"{value:,.2f}" if isinstance(value, float) else str(value))
                else:
                    row_data.append(self._reverse_arabic(str(value)))
            table_data.append(row_data)
        
        # Create table
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        elements.append(table)
        
        # Summary
        if summary:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(
                self._reverse_arabic("ملخص التقرير"),
                self.styles['ArabicSubtitle']
            ))
            
            for key, value in summary.items():
                elements.append(Paragraph(
                    self._reverse_arabic(f"{key}: {value}"),
                    self.styles['ArabicNormal']
                ))
        
        doc.build(elements)
        return buffer.getvalue()
    
    def generate_lot_expiry_report(
        self,
        lots: List[Dict[str, Any]],
        warehouse_name: str = ''
    ) -> bytes:
        """Generate lot expiry report PDF"""
        columns = [
            {'key': 'lot_number', 'label': 'رقم اللوط', 'width': 3},
            {'key': 'product_name', 'label': 'المنتج', 'width': 5},
            {'key': 'quantity', 'label': 'الكمية', 'width': 2},
            {'key': 'expiry_date', 'label': 'تاريخ الانتهاء', 'width': 3},
            {'key': 'days_until_expiry', 'label': 'الأيام المتبقية', 'width': 2},
            {'key': 'status', 'label': 'الحالة', 'width': 2}
        ]
        
        title = f"تقرير صلاحية اللوتات - {warehouse_name}" if warehouse_name else "تقرير صلاحية اللوتات"
        
        # Calculate summary
        total_lots = len(lots)
        expired = sum(1 for l in lots if l.get('days_until_expiry', 0) < 0)
        expiring_soon = sum(1 for l in lots if 0 <= l.get('days_until_expiry', 0) <= 30)
        
        summary = {
            'إجمالي اللوتات': total_lots,
            'منتهية الصلاحية': expired,
            'تنتهي خلال 30 يوم': expiring_soon
        }
        
        return self.generate_report_pdf(title, lots, columns, summary)
    
    def generate_profit_report(
        self,
        profit_data: Dict[str, Any],
        period: str = ''
    ) -> bytes:
        """Generate profit/loss report PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        elements = []
        
        # Title
        elements.append(Paragraph(
            self._reverse_arabic(f"تقرير الأرباح والخسائر - {period}"),
            self.styles['ArabicTitle']
        ))
        elements.append(Spacer(1, 20))
        
        # Revenue section
        elements.append(Paragraph(
            self._reverse_arabic("الإيرادات"),
            self.styles['ArabicSubtitle']
        ))
        
        revenue_data = [
            [self._reverse_arabic('إجمالي المبيعات'), f"{profit_data.get('total_sales', 0):,.2f}"],
            [self._reverse_arabic('المرتجعات'), f"-{profit_data.get('returns', 0):,.2f}"],
            [self._reverse_arabic('صافي الإيرادات'), f"{profit_data.get('net_revenue', 0):,.2f}"],
        ]
        
        revenue_table = Table(revenue_data, colWidths=[10*cm, 5*cm])
        revenue_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecfdf5')),
        ]))
        elements.append(revenue_table)
        elements.append(Spacer(1, 15))
        
        # Expenses section
        elements.append(Paragraph(
            self._reverse_arabic("المصروفات"),
            self.styles['ArabicSubtitle']
        ))
        
        expenses_data = [
            [self._reverse_arabic('تكلفة البضاعة المباعة'), f"{profit_data.get('cogs', 0):,.2f}"],
            [self._reverse_arabic('مصاريف التشغيل'), f"{profit_data.get('operating_expenses', 0):,.2f}"],
            [self._reverse_arabic('إجمالي المصروفات'), f"{profit_data.get('total_expenses', 0):,.2f}"],
        ]
        
        expenses_table = Table(expenses_data, colWidths=[10*cm, 5*cm])
        expenses_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arabic' if 'Arabic' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fef2f2')),
        ]))
        elements.append(expenses_table)
        elements.append(Spacer(1, 20))
        
        # Net profit
        net_profit = profit_data.get('net_profit', 0)
        profit_color = colors.HexColor('#16a34a') if net_profit >= 0 else colors.HexColor('#dc2626')
        
        profit_table = Table([
            [self._reverse_arabic('صافي الربح'), f"{net_profit:,.2f}"]
        ], colWidths=[10*cm, 5*cm])
        profit_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('TEXTCOLOR', (1, 0), (1, 0), profit_color),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(profit_table)
        
        doc.build(elements)
        return buffer.getvalue()


# Singleton instance
pdf_generator = ArabicPDFGenerator()
