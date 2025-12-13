/**
 * P2.63: Print Templates System
 * 
 * Provides reusable print templates for invoices, receipts, reports, etc.
 */

// =============================================================================
// Types
// =============================================================================

export interface PrintOptions {
  title?: string;
  pageSize?: 'A4' | 'A5' | 'Letter' | 'Receipt';
  orientation?: 'portrait' | 'landscape';
  margins?: { top: number; right: number; bottom: number; left: number };
  showHeader?: boolean;
  showFooter?: boolean;
  copies?: number;
}

export interface CompanyInfo {
  name: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  logo?: string;
  taxId?: string;
}

export interface InvoiceData {
  invoiceNumber: string;
  date: string;
  dueDate?: string;
  customer: {
    name: string;
    address?: string;
    phone?: string;
    email?: string;
  };
  items: {
    name: string;
    quantity: number;
    unitPrice: number;
    discount?: number;
    tax?: number;
    total: number;
  }[];
  subtotal: number;
  discount?: number;
  tax?: number;
  total: number;
  notes?: string;
  terms?: string;
  status?: string;
  paymentMethod?: string;
}

// =============================================================================
// CSS Styles
// =============================================================================

const printStyles = `
  @media print {
    @page {
      margin: 10mm;
    }
    body {
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
  }
  
  .print-container {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #333;
    line-height: 1.5;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .print-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #4F46E5;
  }
  
  .company-info {
    flex: 1;
  }
  
  .company-logo {
    max-height: 60px;
    margin-bottom: 10px;
  }
  
  .company-name {
    font-size: 24px;
    font-weight: bold;
    color: #4F46E5;
    margin: 0 0 5px 0;
  }
  
  .company-details {
    font-size: 12px;
    color: #666;
  }
  
  .invoice-info {
    text-align: right;
  }
  
  .invoice-title {
    font-size: 28px;
    font-weight: bold;
    color: #333;
    margin: 0 0 10px 0;
  }
  
  .invoice-number {
    font-size: 14px;
    color: #666;
  }
  
  .invoice-date {
    font-size: 14px;
    color: #666;
  }
  
  .customer-section {
    margin-bottom: 30px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
  }
  
  .section-title {
    font-size: 12px;
    font-weight: 600;
    color: #666;
    text-transform: uppercase;
    margin-bottom: 10px;
  }
  
  .customer-name {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin-bottom: 5px;
  }
  
  .customer-details {
    font-size: 13px;
    color: #666;
  }
  
  .items-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 30px;
  }
  
  .items-table th {
    background: #4F46E5;
    color: white;
    padding: 12px;
    text-align: left;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
  }
  
  .items-table th:last-child {
    text-align: right;
  }
  
  .items-table td {
    padding: 12px;
    border-bottom: 1px solid #eee;
    font-size: 13px;
  }
  
  .items-table td:last-child {
    text-align: right;
    font-weight: 500;
  }
  
  .items-table tbody tr:hover {
    background: #f8f9fa;
  }
  
  .totals-section {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 30px;
  }
  
  .totals-table {
    width: 300px;
  }
  
  .totals-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #eee;
  }
  
  .totals-row.total {
    font-size: 18px;
    font-weight: bold;
    color: #4F46E5;
    border-top: 2px solid #4F46E5;
    border-bottom: none;
    padding-top: 15px;
  }
  
  .notes-section {
    margin-top: 30px;
    padding: 15px;
    background: #fffbeb;
    border-radius: 8px;
    border-left: 4px solid #f59e0b;
  }
  
  .notes-title {
    font-size: 12px;
    font-weight: 600;
    color: #92400e;
    margin-bottom: 5px;
  }
  
  .notes-content {
    font-size: 13px;
    color: #78350f;
  }
  
  .print-footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    text-align: center;
    font-size: 12px;
    color: #999;
  }
  
  .status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
  }
  
  .status-paid {
    background: #d1fae5;
    color: #065f46;
  }
  
  .status-pending {
    background: #fef3c7;
    color: #92400e;
  }
  
  .status-overdue {
    background: #fee2e2;
    color: #991b1b;
  }
  
  /* Receipt styles */
  .receipt {
    width: 80mm;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    padding: 10px;
  }
  
  .receipt-header {
    text-align: center;
    border-bottom: 1px dashed #000;
    padding-bottom: 10px;
    margin-bottom: 10px;
  }
  
  .receipt-items {
    border-bottom: 1px dashed #000;
    padding-bottom: 10px;
    margin-bottom: 10px;
  }
  
  .receipt-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
  }
  
  .receipt-total {
    font-weight: bold;
    font-size: 14px;
    text-align: right;
  }
  
  .receipt-footer {
    text-align: center;
    margin-top: 15px;
    font-size: 11px;
  }
`;

// =============================================================================
// Template Functions
// =============================================================================

export function generateInvoiceHTML(
  invoice: InvoiceData,
  company: CompanyInfo,
  options: PrintOptions = {}
): string {
  const statusClass = invoice.status === 'paid' ? 'status-paid' :
                      invoice.status === 'pending' ? 'status-pending' :
                      invoice.status === 'overdue' ? 'status-overdue' : '';

  return `
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
  <meta charset="UTF-8">
  <title>${options.title || `Invoice #${invoice.invoiceNumber}`}</title>
  <style>${printStyles}</style>
</head>
<body>
  <div class="print-container">
    <div class="print-header">
      <div class="company-info">
        ${company.logo ? `<img src="${company.logo}" alt="${company.name}" class="company-logo">` : ''}
        <h1 class="company-name">${company.name}</h1>
        <div class="company-details">
          ${company.address ? `<div>${company.address}</div>` : ''}
          ${company.phone ? `<div>Tel: ${company.phone}</div>` : ''}
          ${company.email ? `<div>Email: ${company.email}</div>` : ''}
          ${company.taxId ? `<div>Tax ID: ${company.taxId}</div>` : ''}
        </div>
      </div>
      <div class="invoice-info">
        <h2 class="invoice-title">INVOICE</h2>
        <div class="invoice-number">#${invoice.invoiceNumber}</div>
        <div class="invoice-date">Date: ${invoice.date}</div>
        ${invoice.dueDate ? `<div class="invoice-date">Due: ${invoice.dueDate}</div>` : ''}
        ${invoice.status ? `<span class="status-badge ${statusClass}">${invoice.status.toUpperCase()}</span>` : ''}
      </div>
    </div>
    
    <div class="customer-section">
      <div class="section-title">Bill To</div>
      <div class="customer-name">${invoice.customer.name}</div>
      <div class="customer-details">
        ${invoice.customer.address ? `<div>${invoice.customer.address}</div>` : ''}
        ${invoice.customer.phone ? `<div>${invoice.customer.phone}</div>` : ''}
        ${invoice.customer.email ? `<div>${invoice.customer.email}</div>` : ''}
      </div>
    </div>
    
    <table class="items-table">
      <thead>
        <tr>
          <th>Item</th>
          <th>Qty</th>
          <th>Unit Price</th>
          ${invoice.items.some(i => i.discount) ? '<th>Discount</th>' : ''}
          ${invoice.items.some(i => i.tax) ? '<th>Tax</th>' : ''}
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        ${invoice.items.map(item => `
          <tr>
            <td>${item.name}</td>
            <td>${item.quantity}</td>
            <td>$${item.unitPrice.toFixed(2)}</td>
            ${invoice.items.some(i => i.discount) ? `<td>${item.discount ? `$${item.discount.toFixed(2)}` : '-'}</td>` : ''}
            ${invoice.items.some(i => i.tax) ? `<td>${item.tax ? `$${item.tax.toFixed(2)}` : '-'}</td>` : ''}
            <td>$${item.total.toFixed(2)}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    
    <div class="totals-section">
      <div class="totals-table">
        <div class="totals-row">
          <span>Subtotal</span>
          <span>$${invoice.subtotal.toFixed(2)}</span>
        </div>
        ${invoice.discount ? `
          <div class="totals-row">
            <span>Discount</span>
            <span>-$${invoice.discount.toFixed(2)}</span>
          </div>
        ` : ''}
        ${invoice.tax ? `
          <div class="totals-row">
            <span>Tax</span>
            <span>$${invoice.tax.toFixed(2)}</span>
          </div>
        ` : ''}
        <div class="totals-row total">
          <span>Total</span>
          <span>$${invoice.total.toFixed(2)}</span>
        </div>
      </div>
    </div>
    
    ${invoice.notes ? `
      <div class="notes-section">
        <div class="notes-title">Notes</div>
        <div class="notes-content">${invoice.notes}</div>
      </div>
    ` : ''}
    
    ${invoice.terms ? `
      <div class="notes-section" style="background: #f0f9ff; border-color: #0ea5e9;">
        <div class="notes-title" style="color: #0369a1;">Terms & Conditions</div>
        <div class="notes-content" style="color: #075985;">${invoice.terms}</div>
      </div>
    ` : ''}
    
    <div class="print-footer">
      <p>Thank you for your business!</p>
      ${company.website ? `<p>${company.website}</p>` : ''}
    </div>
  </div>
</body>
</html>
`;
}

export function generateReceiptHTML(
  invoice: InvoiceData,
  company: CompanyInfo
): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Receipt #${invoice.invoiceNumber}</title>
  <style>${printStyles}</style>
</head>
<body>
  <div class="receipt">
    <div class="receipt-header">
      <strong>${company.name}</strong><br>
      ${company.address || ''}<br>
      ${company.phone ? `Tel: ${company.phone}` : ''}
    </div>
    
    <div style="text-align: center; margin-bottom: 10px;">
      <strong>RECEIPT</strong><br>
      #${invoice.invoiceNumber}<br>
      ${invoice.date}
    </div>
    
    <div class="receipt-items">
      ${invoice.items.map(item => `
        <div class="receipt-item">
          <span>${item.name} x${item.quantity}</span>
          <span>$${item.total.toFixed(2)}</span>
        </div>
      `).join('')}
    </div>
    
    <div style="margin-bottom: 10px;">
      <div class="receipt-item">
        <span>Subtotal:</span>
        <span>$${invoice.subtotal.toFixed(2)}</span>
      </div>
      ${invoice.discount ? `
        <div class="receipt-item">
          <span>Discount:</span>
          <span>-$${invoice.discount.toFixed(2)}</span>
        </div>
      ` : ''}
      ${invoice.tax ? `
        <div class="receipt-item">
          <span>Tax:</span>
          <span>$${invoice.tax.toFixed(2)}</span>
        </div>
      ` : ''}
    </div>
    
    <div class="receipt-total">
      TOTAL: $${invoice.total.toFixed(2)}
    </div>
    
    ${invoice.paymentMethod ? `
      <div style="margin-top: 10px; text-align: center;">
        Payment: ${invoice.paymentMethod}
      </div>
    ` : ''}
    
    <div class="receipt-footer">
      Thank you!<br>
      Please come again
    </div>
  </div>
</body>
</html>
`;
}

export function generateReportHTML(
  title: string,
  headers: string[],
  rows: (string | number)[][],
  company: CompanyInfo,
  options: {
    summary?: { label: string; value: string | number }[];
    dateRange?: { from: string; to: string };
  } = {}
): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
  <style>${printStyles}</style>
</head>
<body>
  <div class="print-container">
    <div class="print-header">
      <div class="company-info">
        <h1 class="company-name">${company.name}</h1>
      </div>
      <div class="invoice-info">
        <h2 class="invoice-title">${title}</h2>
        <div class="invoice-date">Generated: ${new Date().toLocaleDateString()}</div>
        ${options.dateRange ? `
          <div class="invoice-date">Period: ${options.dateRange.from} - ${options.dateRange.to}</div>
        ` : ''}
      </div>
    </div>
    
    <table class="items-table">
      <thead>
        <tr>
          ${headers.map(h => `<th>${h}</th>`).join('')}
        </tr>
      </thead>
      <tbody>
        ${rows.map(row => `
          <tr>
            ${row.map(cell => `<td>${cell}</td>`).join('')}
          </tr>
        `).join('')}
      </tbody>
    </table>
    
    ${options.summary ? `
      <div class="totals-section">
        <div class="totals-table">
          ${options.summary.map(s => `
            <div class="totals-row">
              <span>${s.label}</span>
              <span>${s.value}</span>
            </div>
          `).join('')}
        </div>
      </div>
    ` : ''}
    
    <div class="print-footer">
      <p>${company.name} - Confidential Report</p>
    </div>
  </div>
</body>
</html>
`;
}

// =============================================================================
// Print Functions
// =============================================================================

export function printHTML(html: string, options: PrintOptions = {}): void {
  const printWindow = window.open('', '_blank');
  
  if (!printWindow) {
    console.error('Could not open print window');
    return;
  }
  
  printWindow.document.write(html);
  printWindow.document.close();
  
  // Wait for content to load then print
  printWindow.onload = () => {
    setTimeout(() => {
      printWindow.print();
      printWindow.close();
    }, 250);
  };
}

export function printInvoice(
  invoice: InvoiceData,
  company: CompanyInfo,
  options: PrintOptions = {}
): void {
  const html = generateInvoiceHTML(invoice, company, options);
  printHTML(html, options);
}

export function printReceipt(
  invoice: InvoiceData,
  company: CompanyInfo
): void {
  const html = generateReceiptHTML(invoice, company);
  printHTML(html);
}

export function printReport(
  title: string,
  headers: string[],
  rows: (string | number)[][],
  company: CompanyInfo,
  options?: {
    summary?: { label: string; value: string | number }[];
    dateRange?: { from: string; to: string };
  }
): void {
  const html = generateReportHTML(title, headers, rows, company, options);
  printHTML(html);
}

// =============================================================================
// Export
// =============================================================================

export default {
  generateInvoiceHTML,
  generateReceiptHTML,
  generateReportHTML,
  printHTML,
  printInvoice,
  printReceipt,
  printReport,
};

