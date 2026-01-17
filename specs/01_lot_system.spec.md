# 📋 Spec: نظام Lot المتقدم | Advanced Lot System

**Version:** 2.0.0
**Date:** 2026-01-16
**Role:** The Architect
**Status:** ✅ Approved
**Priority:** ⭐⭐⭐ Critical

---

## 1. نظرة عامة | Overview

نظام متقدم لتتبع اللوتات (Lots) مصمم خصيصاً لقطاع البذور والأسمدة والمنتجات الزراعية. يوفر تتبعاً شاملاً للجودة والكمية وتاريخ الانتهاء مع دعم كامل للمتطلبات الوزارية.

---

## 2. المتطلبات الوظيفية | Functional Requirements

### 2.1 إدارة اللوتات | Lot Management
- [ ] FR-001: إنشاء لوت جديد مع 50+ حقل متخصص
- [ ] FR-002: تحديث بيانات اللوت
- [ ] FR-003: حذف اللوت (soft delete)
- [ ] FR-004: عرض قائمة اللوتات مع فلترة وترتيب
- [ ] FR-005: البحث في اللوتات

### 2.2 تتبع الجودة | Quality Tracking
- [ ] FR-006: تسجيل معدل الإنبات (Germination Rate)
- [ ] FR-007: تسجيل نسبة النقاء (Purity Rate)
- [ ] FR-008: تسجيل نسبة الرطوبة (Moisture Content)
- [ ] FR-009: تاريخ فحص الجودة
- [ ] FR-010: ملاحظات فحص الجودة

### 2.3 اللوتات الوزارية | Ministry Lots
- [ ] FR-011: رقم الموافقة الوزارية
- [ ] FR-012: تاريخ الموافقة
- [ ] FR-013: تاريخ انتهاء الموافقة
- [ ] FR-014: نوع الموافقة (استيراد، محلي، تصدير)
- [ ] FR-015: مرفقات المستندات الوزارية

### 2.4 حالات اللوت | Lot States
- [ ] FR-016: متاح (AVAILABLE) - جاهز للبيع
- [ ] FR-017: محجوز (RESERVED) - محجوز لطلب معين
- [ ] FR-018: مباع (SOLD) - تم بيعه بالكامل
- [ ] FR-019: منتهي (EXPIRED) - انتهت صلاحيته
- [ ] FR-020: معطوب (DAMAGED) - تالف أو معيب
- [ ] FR-021: مرتجع (RETURNED) - تم إرجاعه
- [ ] FR-022: قيد المراجعة (IN_REVIEW) - قيد الفحص
- [ ] FR-023: محظور (BLOCKED) - محظور من البيع

### 2.5 اختيار FIFO/LIFO
- [ ] FR-024: اختيار تلقائي FIFO (الأقدم أولاً)
- [ ] FR-025: اختيار تلقائي LIFO (الأحدث أولاً)
- [ ] FR-026: اختيار يدوي للوت
- [ ] FR-027: تجاوز FIFO مع صلاحية خاصة

### 2.6 تتبع الانتهاء | Expiry Tracking
- [ ] FR-028: تنبيه قبل 30 يوم من الانتهاء
- [ ] FR-029: تنبيه قبل 7 أيام من الانتهاء
- [ ] FR-030: تنبيه عند الانتهاء
- [ ] FR-031: حظر تلقائي عند الانتهاء (قابل للتكوين)

### 2.7 متعدد المستودعات | Multi-Warehouse
- [ ] FR-032: تتبع اللوت حسب المستودع
- [ ] FR-033: نقل بين المستودعات
- [ ] FR-034: تقارير حسب المستودع

---

## 3. حقول اللوت (50+ حقل) | Lot Fields

### 3.1 المعلومات الأساسية | Basic Info
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| lot_number | String | ✅ | رقم اللوت الفريد |
| product_id | FK | ✅ | معرف المنتج |
| supplier_id | FK | ✅ | معرف المورد |
| warehouse_id | FK | ✅ | معرف المستودع |
| purchase_order_id | FK | ❌ | معرف أمر الشراء |

### 3.2 الكميات | Quantities
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| initial_quantity | Decimal | ✅ | الكمية الأولية |
| current_quantity | Decimal | ✅ | الكمية الحالية |
| reserved_quantity | Decimal | ✅ | الكمية المحجوزة |
| sold_quantity | Decimal | ✅ | الكمية المباعة |
| damaged_quantity | Decimal | ❌ | الكمية التالفة |
| unit_id | FK | ✅ | وحدة القياس |

### 3.3 التواريخ | Dates
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| manufacture_date | Date | ❌ | تاريخ التصنيع |
| expiry_date | Date | ✅ | تاريخ الانتهاء |
| received_date | Date | ✅ | تاريخ الاستلام |
| quality_check_date | Date | ❌ | تاريخ فحص الجودة |

### 3.4 الجودة | Quality
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| germination_rate | Decimal | ❌ | معدل الإنبات (%) |
| purity_rate | Decimal | ❌ | نسبة النقاء (%) |
| moisture_content | Decimal | ❌ | نسبة الرطوبة (%) |
| quality_grade | Enum | ❌ | درجة الجودة (A, B, C) |
| quality_notes | Text | ❌ | ملاحظات الجودة |

### 3.5 الوزارية | Ministry
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| is_ministry_lot | Boolean | ✅ | هل لوت وزاري |
| ministry_approval_number | String | ❌ | رقم الموافقة |
| ministry_approval_date | Date | ❌ | تاريخ الموافقة |
| ministry_expiry_date | Date | ❌ | انتهاء الموافقة |
| approval_type | Enum | ❌ | نوع الموافقة |

### 3.6 التسعير | Pricing
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| cost_price | Decimal | ✅ | سعر التكلفة |
| selling_price | Decimal | ❌ | سعر البيع |
| currency_id | FK | ✅ | العملة |

### 3.7 الحالة | Status
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | Enum | ✅ | حالة اللوت |
| is_active | Boolean | ✅ | نشط |
| blocked_reason | Text | ❌ | سبب الحظر |

---

## 4. API Endpoints

### 4.1 CRUD Operations
```
GET    /api/v1/lots              # List lots (with pagination, filter, sort)
GET    /api/v1/lots/{id}         # Get lot details
POST   /api/v1/lots              # Create new lot
PUT    /api/v1/lots/{id}         # Update lot
DELETE /api/v1/lots/{id}         # Soft delete lot
```

### 4.2 Special Operations
```
GET    /api/v1/lots/expiring                    # Get expiring lots
GET    /api/v1/lots/by-product/{product_id}     # Get lots by product
GET    /api/v1/lots/by-warehouse/{warehouse_id} # Get lots by warehouse
POST   /api/v1/lots/{id}/reserve                # Reserve quantity
POST   /api/v1/lots/{id}/release                # Release reservation
POST   /api/v1/lots/{id}/transfer               # Transfer to warehouse
GET    /api/v1/lots/fifo/{product_id}           # Get FIFO selection
POST   /api/v1/lots/{id}/quality-check          # Record quality check
```

---

## 5. Database Schema

```sql
CREATE TABLE lots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lot_number VARCHAR(50) UNIQUE NOT NULL,
    product_id INTEGER NOT NULL REFERENCES products(id),
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    purchase_order_id INTEGER REFERENCES purchase_orders(id),
    
    -- Quantities
    initial_quantity DECIMAL(15,4) NOT NULL DEFAULT 0,
    current_quantity DECIMAL(15,4) NOT NULL DEFAULT 0,
    reserved_quantity DECIMAL(15,4) NOT NULL DEFAULT 0,
    sold_quantity DECIMAL(15,4) NOT NULL DEFAULT 0,
    damaged_quantity DECIMAL(15,4) DEFAULT 0,
    unit_id INTEGER NOT NULL REFERENCES units(id),
    
    -- Dates
    manufacture_date DATE,
    expiry_date DATE NOT NULL,
    received_date DATE NOT NULL DEFAULT CURRENT_DATE,
    quality_check_date DATE,
    
    -- Quality
    germination_rate DECIMAL(5,2),
    purity_rate DECIMAL(5,2),
    moisture_content DECIMAL(5,2),
    quality_grade VARCHAR(1) CHECK (quality_grade IN ('A', 'B', 'C')),
    quality_notes TEXT,
    
    -- Ministry
    is_ministry_lot BOOLEAN DEFAULT FALSE,
    ministry_approval_number VARCHAR(50),
    ministry_approval_date DATE,
    ministry_expiry_date DATE,
    approval_type VARCHAR(20) CHECK (approval_type IN ('import', 'local', 'export')),
    
    -- Pricing
    cost_price DECIMAL(15,4) NOT NULL,
    selling_price DECIMAL(15,4),
    currency_id INTEGER NOT NULL REFERENCES currencies(id),
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'available'
        CHECK (status IN ('available', 'reserved', 'sold', 'expired', 
                          'damaged', 'returned', 'in_review', 'blocked')),
    is_active BOOLEAN DEFAULT TRUE,
    blocked_reason TEXT,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_lots_product ON lots(product_id);
CREATE INDEX idx_lots_expiry ON lots(expiry_date);
CREATE INDEX idx_lots_status ON lots(status);
CREATE INDEX idx_lots_warehouse ON lots(warehouse_id);
CREATE INDEX idx_lots_fifo ON lots(product_id, expiry_date, received_date);
```

---

## 6. Business Rules

### 6.1 FIFO Selection
```python
def get_fifo_lots(product_id, quantity_needed):
    """
    Select lots using FIFO (First In First Out)
    Priority: expiry_date ASC, received_date ASC, id ASC
    """
    lots = Lot.query.filter(
        Lot.product_id == product_id,
        Lot.status == 'available',
        Lot.current_quantity > 0,
        Lot.expiry_date > datetime.now()
    ).order_by(
        Lot.expiry_date.asc(),
        Lot.received_date.asc(),
        Lot.id.asc()
    ).all()
    
    return select_lots_for_quantity(lots, quantity_needed)
```

### 6.2 Expiry Rules
- 30 days before: Warning notification
- 7 days before: Critical notification
- Expired: Auto-block (configurable)

---

## 7. Testing Requirements

### 7.1 Unit Tests
- [ ] Test lot creation with all fields
- [ ] Test lot status transitions
- [ ] Test FIFO selection algorithm
- [ ] Test quantity calculations
- [ ] Test expiry notifications

### 7.2 Integration Tests
- [ ] Test lot API endpoints
- [ ] Test lot-product relationship
- [ ] Test lot-warehouse transfer
- [ ] Test lot-POS integration

---

## 8. Security Considerations

### 8.1 Permissions Required
| Operation | Permission |
|-----------|------------|
| View lots | `lot.view` |
| Create lot | `lot.create` |
| Update lot | `lot.update` |
| Delete lot | `lot.delete` |
| Block lot | `lot.block` |
| Override FIFO | `lot.override_fifo` |

---

## 9. Related Files

- `backend/src/models/lot.py` - Lot model
- `backend/src/routes/lot_routes.py` - API routes
- `backend/src/services/lot_service.py` - Business logic
- `frontend/src/pages/lots/` - Lot pages
- `frontend/src/components/lots/` - Lot components

---

*Spec Status: ✅ Approved*
*Implementation: ✅ Complete*
