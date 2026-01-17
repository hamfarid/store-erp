# 📋 Spec: نظام نقاط البيع | POS System

**Version:** 2.0.0
**Date:** 2026-01-16
**Role:** The Architect
**Status:** ✅ Approved
**Priority:** ⭐⭐⭐ Critical

---

## 1. نظرة عامة | Overview

نظام نقاط بيع (POS) احترافي وسريع مصمم للمبيعات السريعة في المحلات. يدعم مسح الباركود، اختيار تلقائي للوتات FIFO، إدارة الورديات، وطرق دفع متعددة.

---

## 2. المتطلبات الوظيفية | Functional Requirements

### 2.1 إدارة الورديات | Shift Management
- [ ] FR-001: فتح وردية جديدة مع رصيد افتتاحي
- [ ] FR-002: إغلاق الوردية مع تسوية الصندوق
- [ ] FR-003: تقرير الوردية (المبيعات، المرتجعات، الدفعات)
- [ ] FR-004: تعليق الوردية مؤقتاً
- [ ] FR-005: نقل الوردية لكاشير آخر

### 2.2 عمليات البيع | Sales Operations
- [ ] FR-006: إنشاء فاتورة بيع جديدة
- [ ] FR-007: إضافة منتجات بالباركود
- [ ] FR-008: إضافة منتجات بالبحث
- [ ] FR-009: تعديل الكمية في السلة
- [ ] FR-010: حذف منتج من السلة
- [ ] FR-011: تطبيق خصم على المنتج
- [ ] FR-012: تطبيق خصم على الفاتورة
- [ ] FR-013: إلغاء الفاتورة

### 2.3 اختيار اللوتات | Lot Selection
- [ ] FR-014: اختيار تلقائي FIFO
- [ ] FR-015: عرض اللوتات المتاحة
- [ ] FR-016: اختيار يدوي للوت
- [ ] FR-017: تحذير عند اللوتات قريبة الانتهاء
- [ ] FR-018: منع بيع اللوتات المنتهية

### 2.4 طرق الدفع | Payment Methods
- [ ] FR-019: الدفع نقداً (Cash)
- [ ] FR-020: الدفع بالبطاقة (Card)
- [ ] FR-021: الدفع الآجل (Credit)
- [ ] FR-022: التحويل البنكي (Transfer)
- [ ] FR-023: الدفع المختلط (Split Payment)
- [ ] FR-024: حساب الباقي تلقائياً

### 2.5 الفواتير | Invoices
- [ ] FR-025: طباعة فاتورة حرارية (80mm)
- [ ] FR-026: طباعة فاتورة A4
- [ ] FR-027: إرسال الفاتورة بالبريد
- [ ] FR-028: إرسال الفاتورة بواتساب
- [ ] FR-029: حفظ الفاتورة كمسودة

### 2.6 المرتجعات | Returns
- [ ] FR-030: استرجاع كامل للفاتورة
- [ ] FR-031: استرجاع جزئي
- [ ] FR-032: استبدال المنتج
- [ ] FR-033: إرجاع اللوت للمخزون
- [ ] FR-034: سبب الإرجاع (إلزامي)

### 2.7 العملاء | Customers
- [ ] FR-035: اختيار عميل موجود
- [ ] FR-036: إنشاء عميل سريع
- [ ] FR-037: عميل عابر (Walk-in)
- [ ] FR-038: عرض رصيد العميل
- [ ] FR-039: تطبيق حد ائتمان العميل

---

## 3. واجهة المستخدم | User Interface

### 3.1 Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  [🔍 بحث المنتج]  [📷 مسح الباركود]    [👤 العميل] [⚙️ الإعدادات]│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────┐  ┌──────────────────────────┐│
│  │                              │  │   سلة المشتريات          ││
│  │      منتجات سريعة           │  │                          ││
│  │      (Quick Products)       │  │   🌾 بذور طماطم (2 كجم)  ││
│  │                              │  │      Lot: L2024-001      ││
│  │  [منتج 1] [منتج 2] [منتج 3] │  │      15.00 × 2 = 30.00   ││
│  │  [منتج 4] [منتج 5] [منتج 6] │  │   ─────────────────────  ││
│  │  [منتج 7] [منتج 8] [منتج 9] │  │   🧪 سماد NPK (5 كجم)    ││
│  │                              │  │      Lot: L2024-015      ││
│  │                              │  │      45.00 × 1 = 45.00   ││
│  │                              │  │                          ││
│  └──────────────────────────────┘  │   ─────────────────────  ││
│                                    │   المجموع: 75.00 ج.م     ││
│                                    │   الخصم: 0.00            ││
│                                    │   الضريبة: 11.25         ││
│                                    │   ─────────────────────  ││
│                                    │   الإجمالي: 86.25 ج.م    ││
│                                    └──────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│  [💵 نقد]  [💳 بطاقة]  [📝 آجل]  [🔄 تحويل]      [✅ إتمام البيع]│
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Quick Keys
| Key | Action |
|-----|--------|
| F1 | فتح البحث |
| F2 | مسح الباركود |
| F3 | اختيار عميل |
| F4 | تطبيق خصم |
| F5 | إتمام البيع |
| F8 | إلغاء الفاتورة |
| F10 | تعليق الفاتورة |
| Esc | العودة |

---

## 4. API Endpoints

### 4.1 Shift Management
```
POST   /api/v1/pos/shift/open          # Open new shift
POST   /api/v1/pos/shift/close         # Close current shift
GET    /api/v1/pos/shift/current       # Get current shift
GET    /api/v1/pos/shift/{id}/report   # Get shift report
POST   /api/v1/pos/shift/suspend       # Suspend shift
```

### 4.2 Sales Operations
```
POST   /api/v1/pos/sale                # Create sale
GET    /api/v1/pos/sale/{id}           # Get sale details
PUT    /api/v1/pos/sale/{id}           # Update sale (draft)
DELETE /api/v1/pos/sale/{id}           # Cancel sale
POST   /api/v1/pos/sale/{id}/complete  # Complete sale
POST   /api/v1/pos/sale/{id}/suspend   # Suspend sale
```

### 4.3 Product Search
```
GET    /api/v1/pos/products/search?q=  # Search products
GET    /api/v1/pos/products/barcode/{code}  # Get by barcode
GET    /api/v1/pos/products/quick      # Get quick products
```

### 4.4 Returns
```
POST   /api/v1/pos/sale/{id}/return    # Process return
GET    /api/v1/pos/returns             # List returns
GET    /api/v1/pos/return/{id}         # Get return details
```

### 4.5 Reports
```
GET    /api/v1/pos/daily-summary       # Daily summary
GET    /api/v1/pos/shift-report        # Shift report
GET    /api/v1/pos/sales-by-product    # Sales by product
GET    /api/v1/pos/sales-by-cashier    # Sales by cashier
```

---

## 5. Database Schema

### 5.1 POS Shifts Table
```sql
CREATE TABLE pos_shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cashier_id INTEGER NOT NULL REFERENCES users(id),
    terminal_id VARCHAR(50) NOT NULL,
    
    -- Timing
    opened_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP,
    
    -- Cash
    opening_cash DECIMAL(15,2) NOT NULL DEFAULT 0,
    closing_cash DECIMAL(15,2),
    expected_cash DECIMAL(15,2),
    cash_difference DECIMAL(15,2),
    
    -- Totals
    total_sales DECIMAL(15,2) DEFAULT 0,
    total_returns DECIMAL(15,2) DEFAULT 0,
    total_cash_payments DECIMAL(15,2) DEFAULT 0,
    total_card_payments DECIMAL(15,2) DEFAULT 0,
    total_credit_payments DECIMAL(15,2) DEFAULT 0,
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'suspended', 'closed')),
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 POS Sales Table
```sql
CREATE TABLE pos_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_number VARCHAR(50) UNIQUE NOT NULL,
    shift_id INTEGER NOT NULL REFERENCES pos_shifts(id),
    customer_id INTEGER REFERENCES customers(id),
    
    -- Amounts
    subtotal DECIMAL(15,2) NOT NULL DEFAULT 0,
    discount_amount DECIMAL(15,2) DEFAULT 0,
    tax_amount DECIMAL(15,2) DEFAULT 0,
    total_amount DECIMAL(15,2) NOT NULL DEFAULT 0,
    
    -- Payment
    payment_method VARCHAR(20) NOT NULL
        CHECK (payment_method IN ('cash', 'card', 'credit', 'transfer', 'split')),
    amount_paid DECIMAL(15,2) DEFAULT 0,
    change_amount DECIMAL(15,2) DEFAULT 0,
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'completed', 'cancelled', 'suspended', 'returned')),
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    created_by INTEGER REFERENCES users(id)
);
```

### 5.3 POS Sale Items Table
```sql
CREATE TABLE pos_sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL REFERENCES pos_sales(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    lot_id INTEGER REFERENCES lots(id),
    
    -- Quantities
    quantity DECIMAL(15,4) NOT NULL,
    unit_price DECIMAL(15,4) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    discount_amount DECIMAL(15,2) DEFAULT 0,
    tax_percent DECIMAL(5,2) DEFAULT 0,
    tax_amount DECIMAL(15,2) DEFAULT 0,
    total_amount DECIMAL(15,2) NOT NULL,
    
    -- Lot Info
    lot_number VARCHAR(50),
    lot_expiry_date DATE,
    
    -- Status
    is_returned BOOLEAN DEFAULT FALSE,
    returned_quantity DECIMAL(15,4) DEFAULT 0
);
```

---

## 6. Business Rules

### 6.1 Shift Rules
- Only one open shift per cashier
- Cannot process sales without open shift
- Must close shift at end of day
- Cash difference must be documented

### 6.2 Sale Rules
- At least one item required
- Quantity must be positive
- Cannot exceed available lot quantity
- Payment amount must equal or exceed total (except credit)

### 6.3 Return Rules
- Can only return completed sales
- Return within 30 days (configurable)
- Reason required
- Manager approval for large returns

### 6.4 FIFO Rules
```python
def auto_select_lot(product_id, quantity):
    """Auto-select lot using FIFO"""
    available_lots = Lot.query.filter(
        Lot.product_id == product_id,
        Lot.status == 'available',
        Lot.current_quantity > 0,
        Lot.expiry_date > datetime.now()
    ).order_by(
        Lot.expiry_date.asc(),
        Lot.received_date.asc()
    ).all()
    
    selected = []
    remaining = quantity
    
    for lot in available_lots:
        if remaining <= 0:
            break
        take = min(lot.current_quantity, remaining)
        selected.append({
            'lot_id': lot.id,
            'lot_number': lot.lot_number,
            'quantity': take,
            'expiry_date': lot.expiry_date
        })
        remaining -= take
    
    return selected, remaining
```

---

## 7. Testing Requirements

### 7.1 Unit Tests
- [ ] Test shift open/close
- [ ] Test sale creation
- [ ] Test FIFO lot selection
- [ ] Test payment calculations
- [ ] Test return processing

### 7.2 Integration Tests
- [ ] Test full sale workflow
- [ ] Test POS-Lot integration
- [ ] Test POS-Inventory sync
- [ ] Test receipt printing

### 7.3 E2E Tests
- [ ] Complete sale scenario
- [ ] Return scenario
- [ ] Shift reconciliation

---

## 8. Security Considerations

### 8.1 Permissions Required
| Operation | Permission |
|-----------|------------|
| Open shift | `pos.shift.open` |
| Close shift | `pos.shift.close` |
| Create sale | `pos.sale.create` |
| Process return | `pos.return.create` |
| Override FIFO | `pos.override_fifo` |
| Apply discount | `pos.discount.apply` |
| Cancel sale | `pos.sale.cancel` |
| View reports | `pos.reports.view` |

---

## 9. Related Files

- `backend/src/models/pos_*.py` - POS models
- `backend/src/routes/pos_routes.py` - API routes
- `backend/src/services/pos_service.py` - Business logic
- `frontend/src/pages/pos/` - POS interface
- `frontend/src/components/pos/` - POS components

---

*Spec Status: ✅ Approved*
*Implementation: ✅ Complete*
