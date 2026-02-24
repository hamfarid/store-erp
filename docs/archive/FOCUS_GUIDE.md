# 🎯 FOCUS GUIDE - Never Get Lost Again

**One-Page Reference for Backend File Structure**

---

## 📊 THE SIMPLE RULE

```
Models (database)  = SINGULAR  → user.py, customer.py, supplier.py
Routes (endpoints) = PLURAL    → users.py, customers.py, suppliers.py
Unified (standard) = _unified  → users_unified.py, invoices_unified.py
```

---

## 🗂️ FILE DECISION MAP

### User Files
| File | Keep? | Why |
|------|-------|-----|
| `routes/users_unified.py` | ✅ YES | Main user endpoints |
| `routes/user_management_advanced.py` | ✅ YES | Admin features (rename later) |
| `routes/user.py` | ❌ NO | Old, replaced by users_unified |
| `routes/users.py` | ❌ NO | Old, replaced by users_unified |
| `models/user.py` | ✅ YES | User, UserSession, UserActivity models |

### Admin Files
| File | Keep? | Why |
|------|-------|-----|
| `routes/admin_panel.py` | ✅ YES | Descriptive name |
| `routes/admin.py` | 🔧 FIX | Has inline User class bug - fix then merge |

### Customer Files
| File | Keep? | Why |
|------|-------|-----|
| `routes/customers.py` | ✅ YES | Plural (correct) |
| `models/customer.py` | ✅ YES | Singular (correct) |

### Supplier Files
| File | Keep? | Why |
|------|-------|-----|
| `routes/suppliers.py` | ✅ YES | Plural (correct) |
| `models/supplier.py` | ✅ YES | Singular (correct) |

### Invoice Files
| File | Keep? | Why |
|------|-------|-----|
| `models/invoice_unified.py` | ✅ YES | Current production (table: invoices) |
| `models/unified_invoice.py` | ✅ YES | Future system (table: unified_invoices) |
| `models/invoice.py` | ❌ NO | Conflicts with invoice_unified |
| `models/invoices.py` | ❌ NO | Old support models |

### Product Files
| File | Keep? | Why |
|------|-------|-----|
| `models/inventory.py` | ✅ YES | Main Product model |
| `models/product_advanced.py` | ✅ YES | Agricultural features |
| `routes/products_unified.py` | ⚠️ CHECK | Verify vs products.py |
| `routes/products_advanced.py` | ✅ YES | Agricultural endpoints |

---

## 🚨 CRITICAL BUG FOUND

**File:** `backend/src/routes/admin.py` line 80

**Problem:** Inline `class User:` definition conflicts with `models/user.py`

**Fix:**
```python
# WRONG (current):
class User:
    """Mock User class"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        # ... rest of mock class

# CORRECT (change to):
from src.models.user import User
```

**Script Available:** `backend/scripts/fix_admin_user_conflict.py`

---

## ⚡ QUICK ACTIONS

### Fix Critical Bug Now
```bash
cd backend
python scripts/fix_admin_user_conflict.py
git commit -am "fix: Remove inline User class conflict in admin.py"
```

### Check What You Have Open
```bash
# If you have these open in editor, they're OLD:
- routes/user.py          → Close, use users_unified.py
- routes/users.py         → Close, use users_unified.py
- models/invoice.py       → Close, use invoice_unified.py
- models/invoices.py      → Close, use invoice_unified.py
```

### Find The Right File Fast
```bash
# User management:
code backend/src/routes/users_unified.py
code backend/src/models/user.py

# Admin panel:
code backend/src/routes/admin_panel.py

# Customers:
code backend/src/routes/customers.py
code backend/src/models/customer.py

# Products:
code backend/src/models/inventory.py
code backend/src/routes/products_unified.py
```

---

## 📈 CLEANUP PROGRESS

**Import Standardization:** ✅ DONE (93.7% already correct, 5 files fixed)

**Naming Consolidation:**
- User files: 🔄 IN PROGRESS (need to consolidate 4 → 2 route files)
- Admin files: 🔴 CRITICAL BUG (inline User class conflict)
- Customer files: ✅ CORRECT (no action needed)
- Supplier files: ✅ CORRECT (no action needed)
- Invoice files: 📋 DOCUMENTED (delete old files after testing)
- Product files: ⚠️ NEEDS INVESTIGATION

---

## 🎯 YOUR NEXT 3 ACTIONS

1. **Fix Critical Bug** (5 min)
   ```bash
   cd backend
   python scripts/fix_admin_user_conflict.py
   ```

2. **Test Backend Starts** (2 min)
   ```bash
   cd backend
   python app.py
   # Should see: ✅ All imports successful
   ```

3. **Read Full Analysis** (10 min)
   - Open: `NAMING_CONSOLIDATION_MAP.md`
   - Understand which files to delete
   - See detailed action plan

---

## 🧠 MENTAL MODEL

When you think: **"Is it user or users?"**

Ask yourself:
- **Am I looking at DATABASE?** → `models/user.py` (singular)
- **Am I looking at API ENDPOINTS?** → `routes/users.py` (plural)
- **Which is the CURRENT/STANDARD one?** → Look for `_unified` suffix

**Golden Files (Always Use These):**
- `models/user.py` - User model
- `routes/users_unified.py` - User endpoints
- `models/customer.py` - Customer model
- `routes/customers.py` - Customer endpoints
- `models/supplier.py` - Supplier model
- `routes/suppliers.py` - Supplier endpoints
- `models/invoice_unified.py` - Invoice model
- `models/inventory.py` - Product model

---

**Last Updated:** 2025-11-13  
**See Also:** NAMING_CONSOLIDATION_MAP.md, VISUAL_MAP.md, IMPORT_CLEANUP_PLAN.md
