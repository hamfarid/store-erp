# T34 Model & Schema Definitions Map

## Missing Models to Create

### 1. Brand Model
**Location:** `backend/src/models/enhanced_models.py`
**Purpose:** Product brand/manufacturer management
**Fields:**
- id (Integer, PK)
- name (String, 100, indexed)
- name_ar (String, 100, indexed)
- description (Text, optional)
- description_ar (Text, optional)
- logo_url (String, 255, optional)
- website (String, 255, optional)
- is_active (Boolean, default=True, indexed)
- created_at (DateTime, indexed)
- updated_at (DateTime)

**Relationships:**
- products: One-to-Many with Product

**Used In:**
- `backend/src/routes/products_enhanced.py` (lines 32, 350, 473, 759, 795, 833-839, 865)

---

### 2. ProductImage Model
**Location:** `backend/src/models/enhanced_models.py`
**Purpose:** Product image management with multiple sizes
**Fields:**
- id (Integer, PK)
- product_id (Integer, FK -> products.id, indexed)
- image_url (String, 255)
- thumbnail_url (String, 255, optional)
- medium_url (String, 255, optional)
- large_url (String, 255, optional)
- is_primary (Boolean, default=False)
- sort_order (Integer, default=0)
- alt_text (String, 255, optional)
- alt_text_ar (String, 255, optional)
- created_at (DateTime, indexed)

**Relationships:**
- product: Many-to-One with Product

**Used In:**
- `backend/src/routes/products_enhanced.py` (lines 32, 673)

---

### 3. StockMovement Model
**Location:** `backend/src/models/enhanced_models.py`
**Purpose:** Track all stock movements for audit trail
**Fields:**
- id (Integer, PK)
- product_id (Integer, FK -> products.id, indexed)
- warehouse_id (Integer, FK -> warehouses.id, indexed)
- movement_type (String, 20, indexed) # 'in', 'out', 'adjustment', 'transfer'
- quantity (Integer)
- quantity_before (Integer)
- quantity_after (Integer)
- reference_type (String, 50, optional) # 'sale', 'purchase', 'return', 'adjustment'
- reference_id (Integer, optional)
- notes (Text, optional)
- notes_ar (Text, optional)
- user_id (Integer, FK -> users.id, indexed)
- created_at (DateTime, indexed)

**Relationships:**
- product: Many-to-One with Product
- warehouse: Many-to-One with Warehouse
- user: Many-to-One with User

**Used In:**
- `backend/src/routes/products_enhanced.py` (lines 32, 287-295, 392)

---

## Missing Schemas to Create

### 1. CategorySchema
**Location:** `backend/src/schemas/product_schema.py`
**Purpose:** Validate category data
**Fields:**
- id (Int, dump_only)
- name (Str, required, 2-100 chars)
- name_ar (Str, required, 2-100 chars)
- description (Str, optional)
- description_ar (Str, optional)
- parent_id (Int, optional)
- is_active (Bool, default=True)
- sort_order (Int, default=0)

---

### 2. BrandSchema
**Location:** `backend/src/schemas/product_schema.py`
**Purpose:** Validate brand data
**Fields:**
- id (Int, dump_only)
- name (Str, required, 2-100 chars)
- name_ar (Str, required, 2-100 chars)
- description (Str, optional)
- description_ar (Str, optional)
- logo_url (Str, optional)
- website (Str, optional)
- is_active (Bool, default=True)

---

### 3. ProductImageSchema
**Location:** `backend/src/schemas/product_schema.py`
**Purpose:** Validate product image data
**Fields:**
- id (Int, dump_only)
- product_id (Int, required)
- image_url (Str, required)
- thumbnail_url (Str, optional)
- medium_url (Str, optional)
- large_url (Str, optional)
- is_primary (Bool, default=False)
- sort_order (Int, default=0)
- alt_text (Str, optional)
- alt_text_ar (Str, optional)

---

### 4. ProductCreateSchema, ProductUpdateSchema, ProductSearchSchema
**Status:** Already exist in product_schema.py - may need enhancement

---

## Model Export Configuration

### Update `backend/src/models/__init__.py`
Add exports:
```python
Brand = None
ProductImage = None
StockMovement = None

__all__ = [
    # ... existing exports ...
    'Brand', 'ProductImage', 'StockMovement'
]
```

---

## Implementation Order

1. ✅ Create Brand model
2. ✅ Create ProductImage model
3. ✅ Create StockMovement model
4. ✅ Update Product model relationships
5. ✅ Create CategorySchema
6. ✅ Create BrandSchema
7. ✅ Create ProductImageSchema
8. ✅ Update __init__.py exports
9. ✅ Re-enable imports in products_enhanced.py
10. ✅ Re-enable schema instantiations
11. ✅ Test all routes

---

## Logger System Requirements

### Backend Logger
**Location:** `backend/src/utils/logger.py`
**Features:**
- Structured logging (JSON format)
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Request/response logging
- Database query logging
- Performance metrics
- Error stack traces
- User action tracking

### Frontend Logger
**Location:** `frontend/src/utils/logger.ts`
**Features:**
- Console logging with levels
- Error boundary integration
- API error logging
- User action tracking
- Performance monitoring

### Database Logger
**Features:**
- Query logging
- Slow query detection
- Connection pool monitoring
- Migration tracking

---

## Status
- Models: ⏳ To be created
- Schemas: ⏳ To be created
- Exports: ⏳ To be updated
- Logger: ⏳ To be implemented
