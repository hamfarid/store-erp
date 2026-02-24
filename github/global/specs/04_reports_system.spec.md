# Reports System Specification

**Version:** 2.0.0  
**Status:** Implemented  
**Last Updated:** 2026-01-16

---

## Overview

نظام التقارير المتكامل لـ Store ERP يوفر 8+ أنواع من التقارير مع دعم كامل للتصدير.

---

## Report Types

### 1. Sales Reports
- Daily/Weekly/Monthly/Yearly sales
- Sales by product/category
- Sales by customer
- Sales by payment method

### 2. Inventory Reports
- Current stock levels
- Low stock alerts
- Stock valuation
- Stock movements

### 3. Profit/Loss Reports
- Revenue analysis
- Cost breakdown
- Gross/Net profit
- Margin analysis

### 4. Lot Expiry Reports
- Expiring lots by date range
- Expired lots
- Quality metrics report

### 5. Customer Reports
- Customer transactions
- Credit/Debit balances
- Top customers

### 6. Supplier Reports
- Purchase history
- Payment status
- Supplier performance

### 7. POS Reports
- Shift summaries
- Cash flow
- Transaction logs

### 8. Audit Reports
- User activity logs
- Security events
- System changes

---

## Export Formats

| Format | Library | Features |
|--------|---------|----------|
| PDF | jsPDF + jspdf-autotable | Arabic RTL support |
| Excel | xlsx | Multi-sheet, styling |
| CSV | Native | Universal compatibility |

---

## API Endpoints

```
GET /api/reports/sales
GET /api/reports/inventory
GET /api/reports/profit-loss
GET /api/reports/lot-expiry
GET /api/reports/customers
GET /api/reports/suppliers
GET /api/reports/pos
GET /api/reports/audit
GET /api/reports/{type}/export
```

---

## Frontend Pages

- `ReportsSystem.jsx` - Reports hub
- `ProfitLossReports.jsx` - P&L analysis
- `LotExpiryReport.jsx` - Expiry tracking
- `AdvancedReports.jsx` - Custom reports

---

## Implementation Status

- ✅ Sales Reports
- ✅ Inventory Reports
- ✅ Profit/Loss Reports
- ✅ Lot Expiry Reports
- ✅ PDF Export
- ✅ Excel Export
- ✅ CSV Export
- ✅ Date Filtering
- ✅ Interactive Charts
