/**
 * PDF Export Utility for Reports
 * تصدير التقارير بصيغة PDF
 * 
 * @file frontend/src/utils/pdfExport.js
 * @author Store ERP v2.0.0
 */

import { toast } from 'react-hot-toast';
import { logActivity } from './activityLogger';

/**
 * Generate and download a PDF report
 * @param {Object} options - PDF options
 * @param {string} options.title - Report title
 * @param {string} options.subtitle - Report subtitle
 * @param {Array<Object>} options.data - Data rows
 * @param {Array<Object>} options.columns - Column definitions [{key, header, width}]
 * @param {Object} [options.summary] - Summary data to display
 * @param {string} [options.filename] - Output filename
 * @param {string} [options.orientation] - 'portrait' or 'landscape'
 */
export async function exportToPDF(options) {
  const {
    title = 'تقرير',
    subtitle = '',
    data = [],
    columns = [],
    summary = null,
    filename = 'report',
    orientation = 'portrait',
    companyName = 'Store ERP',
    logo = null
  } = options;

  const startedAt = performance.now?.() || Date.now();

  try {
    if (!data.length && !summary) {
      toast.error('لا توجد بيانات للتصدير');
      return;
    }

    // Dynamically import jsPDF for code splitting
    const { default: jsPDF } = await import('jspdf');
    await import('jspdf-autotable');

    const doc = new jsPDF({
      orientation,
      unit: 'mm',
      format: 'a4'
    });

    // Set RTL font (Arabic support)
    doc.setFont('helvetica');
    doc.setLanguage('ar');

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 15;

    let yPos = margin;

    // === Header ===
    // Company name
    doc.setFontSize(18);
    doc.setTextColor(51, 51, 51);
    doc.text(companyName, pageWidth / 2, yPos, { align: 'center' });
    yPos += 10;

    // Report title
    doc.setFontSize(16);
    doc.setTextColor(33, 150, 243); // Blue
    doc.text(title, pageWidth / 2, yPos, { align: 'center' });
    yPos += 8;

    // Subtitle
    if (subtitle) {
      doc.setFontSize(10);
      doc.setTextColor(128, 128, 128);
      doc.text(subtitle, pageWidth / 2, yPos, { align: 'center' });
      yPos += 6;
    }

    // Date
    const dateStr = new Date().toLocaleDateString('ar-SA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    doc.setFontSize(9);
    doc.setTextColor(100, 100, 100);
    doc.text(`تاريخ التقرير: ${dateStr}`, pageWidth - margin, yPos, { align: 'right' });
    yPos += 10;

    // === Summary Section ===
    if (summary) {
      doc.setFillColor(245, 245, 245);
      doc.roundedRect(margin, yPos, pageWidth - 2 * margin, 30, 3, 3, 'F');
      
      const summaryKeys = Object.keys(summary);
      const colWidth = (pageWidth - 2 * margin) / summaryKeys.length;
      
      summaryKeys.forEach((key, index) => {
        const x = margin + colWidth * index + colWidth / 2;
        doc.setFontSize(9);
        doc.setTextColor(128, 128, 128);
        doc.text(key, x, yPos + 8, { align: 'center' });
        
        doc.setFontSize(14);
        doc.setTextColor(33, 33, 33);
        doc.text(String(summary[key]), x, yPos + 20, { align: 'center' });
      });
      
      yPos += 40;
    }

    // === Data Table ===
    if (data.length > 0 && columns.length > 0) {
      const tableHeaders = columns.map(col => col.header || col.key);
      const tableBody = data.map(row => 
        columns.map(col => formatCellValue(row[col.key]))
      );

      doc.autoTable({
        head: [tableHeaders],
        body: tableBody,
        startY: yPos,
        margin: { left: margin, right: margin },
        styles: {
          font: 'helvetica',
          fontSize: 9,
          cellPadding: 4,
          overflow: 'linebreak',
          halign: 'right' // RTL alignment
        },
        headStyles: {
          fillColor: [33, 150, 243],
          textColor: [255, 255, 255],
          fontStyle: 'bold',
          halign: 'center'
        },
        alternateRowStyles: {
          fillColor: [245, 245, 245]
        },
        columnStyles: columns.reduce((acc, col, index) => {
          if (col.width) {
            acc[index] = { cellWidth: col.width };
          }
          return acc;
        }, {}),
        didDrawPage: (data) => {
          // Footer on each page
          const pageCount = doc.internal.getNumberOfPages();
          doc.setFontSize(8);
          doc.setTextColor(150, 150, 150);
          doc.text(
            `صفحة ${data.pageNumber} من ${pageCount}`,
            pageWidth / 2,
            pageHeight - 10,
            { align: 'center' }
          );
          doc.text(
            'Store ERP v2.0.0',
            margin,
            pageHeight - 10
          );
        }
      });
    }

    // Save PDF
    doc.save(`${filename}.pdf`);

    const ms = (performance.now?.() || Date.now()) - startedAt;
    toast.success(`تم تصدير التقرير بصيغة PDF`);
    logActivity({
      action: 'EXPORT',
      entityType: filename,
      format: 'PDF',
      recordCount: data.length,
      outcome: 'success',
      timed_ms: Math.round(ms)
    });

  } catch (err) {
    const ms = (performance.now?.() || Date.now()) - startedAt;
    toast.error('فشل تصدير PDF');
    logActivity({
      action: 'EXPORT',
      entityType: filename,
      format: 'PDF',
      recordCount: data.length,
      outcome: 'error',
      timed_ms: Math.round(ms)
    });
    console.error('exportToPDF failed:', err);
  }
}

/**
 * Format cell value for PDF
 */
function formatCellValue(value) {
  if (value == null) return '';
  if (typeof value === 'number') {
    return new Intl.NumberFormat('ar-SA').format(value);
  }
  if (value instanceof Date) {
    return value.toLocaleDateString('ar-SA');
  }
  return String(value);
}

/**
 * Generate profit report PDF
 */
export async function exportProfitReportPDF(reportData, dateRange) {
  const columns = [
    { key: 'month', header: 'الشهر', width: 30 },
    { key: 'revenue', header: 'الإيرادات', width: 35 },
    { key: 'costs', header: 'التكاليف', width: 35 },
    { key: 'profit', header: 'الربح', width: 35 },
    { key: 'margin', header: 'الهامش %', width: 25 }
  ];

  const data = (reportData.monthlyTrend || []).map(item => ({
    month: item.month,
    revenue: formatCurrency(item.revenue),
    costs: formatCurrency(item.costs),
    profit: formatCurrency(item.profit),
    margin: `${((item.profit / item.revenue) * 100).toFixed(1)}%`
  }));

  const summary = {
    'إجمالي الإيرادات': formatCurrency(reportData.summary?.totalRevenue || 0),
    'إجمالي التكاليف': formatCurrency(reportData.summary?.totalCosts || 0),
    'صافي الربح': formatCurrency(reportData.summary?.netProfit || 0),
    'هامش الربح': `${reportData.summary?.profitMargin || 0}%`
  };

  await exportToPDF({
    title: 'تقرير الأرباح والخسائر',
    subtitle: `من ${dateRange.from} إلى ${dateRange.to}`,
    data,
    columns,
    summary,
    filename: `profit-loss-report-${Date.now()}`,
    orientation: 'landscape'
  });
}

/**
 * Generate lot expiry report PDF
 */
export async function exportLotExpiryPDF(lots, daysFilter) {
  const columns = [
    { key: 'lotNumber', header: 'رقم اللوت', width: 30 },
    { key: 'productName', header: 'المنتج', width: 40 },
    { key: 'quantity', header: 'الكمية', width: 25 },
    { key: 'expiryDate', header: 'تاريخ الانتهاء', width: 30 },
    { key: 'daysRemaining', header: 'أيام متبقية', width: 25 },
    { key: 'status', header: 'الحالة', width: 25 }
  ];

  const data = lots.map(lot => ({
    lotNumber: lot.lotNumber || lot.lot_number,
    productName: lot.productName || lot.product_name,
    quantity: lot.quantity,
    expiryDate: lot.expiryDate || lot.expiry_date,
    daysRemaining: lot.daysRemaining || lot.days_remaining,
    status: lot.status === 'expired' ? 'منتهي' : 
            lot.status === 'warning' ? 'قريب الانتهاء' : 'نشط'
  }));

  const summary = {
    'إجمالي اللوتات': lots.length,
    'منتهية الصلاحية': lots.filter(l => l.status === 'expired').length,
    'قريبة الانتهاء': lots.filter(l => l.status === 'warning').length,
    'نشطة': lots.filter(l => l.status === 'active').length
  };

  await exportToPDF({
    title: 'تقرير انتهاء صلاحية اللوتات',
    subtitle: `خلال ${daysFilter} يوم`,
    data,
    columns,
    summary,
    filename: `lot-expiry-report-${Date.now()}`,
    orientation: 'landscape'
  });
}

/**
 * Format currency for Arabic
 */
function formatCurrency(amount) {
  return new Intl.NumberFormat('ar-SA', {
    style: 'currency',
    currency: 'EGP',
    minimumFractionDigits: 0
  }).format(amount);
}

export default {
  exportToPDF,
  exportProfitReportPDF,
  exportLotExpiryPDF
};
