# 🔄 المرحلة 2: الاختبارات والجودة
# Phase 2: Testing & Quality

**الأولوية / Priority:** 🔴 **P0 - حرج / CRITICAL**  
**الوقت المقدر / Estimated Time:** 5-7 أيام / days  
**الحالة / Status:** 🔄 **قيد التنفيذ / IN PROGRESS**  
**التاريخ / Date:** 2025-11-05

---

## 🎯 **الهدف / Objective**

رفع تغطية الاختبارات من **<15%** إلى **80%+** وإصلاح جميع مشاكل الجودة.

Increase test coverage from **<15%** to **80%+** and fix all quality issues.

---

## 📋 **المهام / Tasks**

### **Task 2.1: إصلاح أخطاء الاستيراد في الاختبارات**
**Fix Test Import Errors**

**المشكلة / Problem:**
```python
# ❌ Current (WRONG):
from backend.src.circuit_breaker import CircuitBreaker

# Error: ModuleNotFoundError: No module named 'backend'
```

**الحل / Solution:**
```python
# ✅ Correct:
from src.circuit_breaker import CircuitBreaker
```

**الملفات المتأثرة / Affected Files:**
- `backend/tests/test_circuit_breaker.py`
- أي ملفات اختبار أخرى بنفس المشكلة

**الوقت المقدر:** 1-2 ساعات

---

### **Task 2.2: إضافة اختبارات الوحدة**
**Add Unit Tests**

**الهدف / Target:**
- اختبار جميع الوحدات الأساسية
- تغطية >= 80% لكل ملف
- اختبار الحالات الطبيعية والاستثنائية

**الوحدات المطلوبة / Required Modules:**

#### 1. **Auth Module** (`src/auth.py`)
```python
# Tests needed:
- test_hash_password_with_argon2
- test_hash_password_with_bcrypt
- test_hash_password_empty_password
- test_hash_password_short_password
- test_verify_password_correct
- test_verify_password_incorrect
- test_verify_password_legacy_sha256
- test_create_access_token
- test_create_refresh_token
- test_decode_token_valid
- test_decode_token_expired
- test_decode_token_invalid
```

#### 2. **Security Middleware** (`src/security_middleware.py`)
```python
# Tests needed:
- test_require_role_valid
- test_require_role_invalid
- test_require_role_missing_token
- test_require_admin_valid
- test_require_admin_not_admin
- test_require_permission_valid
- test_require_permission_invalid
- test_rate_limiting
- test_csrf_protection
```

#### 3. **Config** (`src/config/`)
```python
# Tests needed:
- test_development_config
- test_production_config_with_secrets
- test_production_config_without_secrets
- test_testing_config
```

#### 4. **Database** (`src/database.py`)
```python
# Tests needed:
- test_db_connection
- test_db_initialization
- test_db_migration
- test_db_rollback
```

**الوقت المقدر:** 2-3 أيام

---

### **Task 2.3: إضافة اختبارات التكامل**
**Add Integration Tests**

**الهدف / Target:**
- اختبار جميع نقاط النهاية (API endpoints)
- اختبار التدفقات الكاملة
- اختبار التكامل بين الوحدات

**نقاط النهاية المطلوبة / Required Endpoints:**

#### 1. **Authentication Endpoints**
```python
# Tests needed:
- test_register_user_success
- test_register_user_duplicate
- test_login_success
- test_login_invalid_credentials
- test_refresh_token_success
- test_refresh_token_expired
- test_logout_success
```

#### 2. **User Management Endpoints**
```python
# Tests needed:
- test_get_users_as_admin
- test_get_users_as_regular_user
- test_create_user_as_admin
- test_update_user_as_admin
- test_delete_user_as_admin
- test_get_user_profile
- test_update_user_profile
```

#### 3. **Inventory Endpoints**
```python
# Tests needed:
- test_get_products
- test_create_product
- test_update_product
- test_delete_product
- test_search_products
- test_filter_products
```

#### 4. **Sales Endpoints**
```python
# Tests needed:
- test_create_sale
- test_get_sales
- test_get_sale_by_id
- test_update_sale
- test_cancel_sale
```

**الوقت المقدر:** 2-3 أيام

---

### **Task 2.4: تحقيق تغطية 80%+**
**Achieve 80%+ Coverage**

**الخطوات / Steps:**

1. **قياس التغطية الحالية**
   ```bash
   cd backend
   pytest --cov=src --cov-report=html --cov-report=term-missing
   ```

2. **تحديد الملفات ذات التغطية المنخفضة**
   ```bash
   # Check coverage report
   open htmlcov/index.html
   ```

3. **إضافة اختبارات للملفات المفقودة**
   - التركيز على الملفات ذات التغطية < 80%
   - إضافة اختبارات للحالات غير المغطاة

4. **التحقق من التغطية النهائية**
   ```bash
   pytest --cov=src --cov-report=term-missing
   # Target: TOTAL >= 80%
   ```

**معايير النجاح / Success Criteria:**
- ✅ التغطية الإجمالية >= 80%
- ✅ التغطية الحرجة >= 95%
- ✅ جميع الاختبارات تنجح

**الوقت المقدر:** 1-2 أيام

---

### **Task 2.5: إعداد CI/CD**
**Set Up CI/CD**

**الهدف / Target:**
- تشغيل الاختبارات تلقائياً عند كل commit
- تقرير التغطية تلقائياً
- منع الدمج إذا فشلت الاختبارات

**الخطوات / Steps:**

1. **إنشاء GitHub Actions Workflow**
   ```yaml
   # .github/workflows/tests.yml
   name: Tests
   
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - name: Install dependencies
           run: |
             cd backend
             pip install -r requirements.txt
         - name: Run tests
           run: |
             cd backend
             pytest --cov=src --cov-report=xml
         - name: Upload coverage
           uses: codecov/codecov-action@v3
   ```

2. **إضافة Badge إلى README**
   ```markdown
   ![Tests](https://github.com/hamfarid/store/workflows/Tests/badge.svg)
   ![Coverage](https://codecov.io/gh/hamfarid/store/branch/main/graph/badge.svg)
   ```

3. **إعداد Branch Protection**
   - Require status checks to pass
   - Require branches to be up to date
   - Require review before merging

**الوقت المقدر:** 4-6 ساعات

---

## 📊 **الجدول الزمني / Timeline**

| اليوم / Day | المهمة / Task | الوقت / Time |
|-------------|---------------|--------------|
| **Day 1** | Task 2.1: Fix Import Errors | 1-2 hours |
| **Day 1-2** | Task 2.2: Unit Tests (Part 1) | 1.5 days |
| **Day 3-4** | Task 2.2: Unit Tests (Part 2) | 1.5 days |
| **Day 4-5** | Task 2.3: Integration Tests (Part 1) | 1.5 days |
| **Day 5-6** | Task 2.3: Integration Tests (Part 2) | 1.5 days |
| **Day 6-7** | Task 2.4: Achieve 80%+ Coverage | 1-2 days |
| **Day 7** | Task 2.5: Set Up CI/CD | 4-6 hours |

**الإجمالي / Total:** 5-7 أيام

---

## ✅ **معايير النجاح / Success Criteria**

### **Phase 2 Complete When:**

- [ ] جميع أخطاء الاستيراد مصلحة
- [ ] اختبارات الوحدة >= 80% تغطية
- [ ] اختبارات التكامل لجميع نقاط النهاية
- [ ] التغطية الإجمالية >= 80%
- [ ] CI/CD يعمل تلقائياً
- [ ] جميع الاختبارات تنجح
- [ ] التوثيق محدث

---

## 🎯 **الأولويات / Priorities**

### **P0 - حرج / Critical:**
1. إصلاح أخطاء الاستيراد
2. اختبارات Auth & Security
3. اختبارات نقاط النهاية الحرجة
4. تحقيق 80%+ تغطية

### **P1 - مهم / Important:**
5. اختبارات التكامل الكاملة
6. إعداد CI/CD
7. تحديث التوثيق

---

## 📁 **الملفات المتوقعة / Expected Files**

### **ملفات الاختبار / Test Files:**
```
backend/tests/
├── test_auth.py                    # NEW
├── test_security_middleware.py     # NEW
├── test_config.py                  # NEW
├── test_database.py                # NEW
├── test_api_auth.py                # NEW
├── test_api_users.py               # NEW
├── test_api_inventory.py           # NEW
├── test_api_sales.py               # NEW
├── test_circuit_breaker.py         # UPDATED (fix imports)
└── test_security_fixes_p0.py       # EXISTS
```

### **ملفات CI/CD:**
```
.github/workflows/
└── tests.yml                       # NEW
```

### **ملفات التوثيق:**
```
PHASE_2_TESTING_COMPLETE.md         # NEW
PHASE_2_QUICK_REFERENCE.md          # NEW
save_phase2_to_memory.py            # NEW
```

---

## 💡 **أفضل الممارسات / Best Practices**

### **1. كتابة الاختبارات**
```python
# ✅ Good Test:
def test_hash_password_with_argon2():
    """Test password hashing with Argon2id"""
    password = "SecurePass123!"
    hashed = hash_password(password)
    
    # Assertions
    assert hashed is not None
    assert hashed != password
    assert hashed.startswith('$argon2id$')
    assert verify_password(password, hashed) is True
    assert verify_password('wrong', hashed) is False
```

### **2. اختبارات التكامل**
```python
# ✅ Good Integration Test:
def test_login_flow(client):
    """Test complete login flow"""
    # Register user
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'SecurePass123!',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'SecurePass123!'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
```

### **3. Fixtures**
```python
# ✅ Good Fixtures:
@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client):
    """Get authentication headers"""
    # Login and get token
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}
```

---

## 🚀 **البدء / Getting Started**

### **الخطوة 1: إعداد البيئة**
```bash
cd backend
pip install -r requirements.txt
pip install pytest pytest-cov pytest-mock
```

### **الخطوة 2: تشغيل الاختبارات الحالية**
```bash
pytest -v
```

### **الخطوة 3: قياس التغطية الحالية**
```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

### **الخطوة 4: البدء في Task 2.1**
```bash
# Fix import errors in test files
```

---

## 📞 **المساعدة / Help**

### **مشاكل شائعة / Common Issues:**

**1. Import Errors**
```python
# ❌ Wrong:
from backend.src.module import Class

# ✅ Correct:
from src.module import Class
```

**2. Test Discovery**
```bash
# If tests not found:
pytest --collect-only
```

**3. Coverage Not Working**
```bash
# Install coverage:
pip install pytest-cov
```

---

## ✅ **جاهز للبدء! / Ready to Start!**

**المرحلة 2 تبدأ الآن!**  
**Phase 2 starts now!**

**الخطوة الأولى:** Task 2.1 - إصلاح أخطاء الاستيراد

---

**آخر تحديث / Last Updated:** 2025-11-05  
**الحالة / Status:** 🔄 **قيد التنفيذ / IN PROGRESS**  
**المرحلة / Phase:** 2 من 5

