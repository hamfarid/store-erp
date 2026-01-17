# قسم فحص الصفحات والأزرار - مسودة

## المشكلة المحددة
عند تطبيق البرومبت، تظهر المشاكل التالية:
1. صفحات كثيرة غير موجودة
2. أزرار كثيرة غير موجودة
3. لا يوجد ربط بين الواجهة الأمامية والخلفية
4. صفحات بدون وظائف

## الحل المقترح

### 1. إضافة قسم إلزامي في البرومبت الأساسي
قسم جديد بعنوان: **MANDATORY: COMPLETE PAGES & BUTTONS VERIFICATION**

### 2. محتوى القسم

#### A. فحص الصفحات الإلزامية
قائمة بجميع الصفحات التي يجب أن تكون موجودة في أي مشروع:

**صفحات المصادقة:**
- Login Page (تسجيل الدخول)
- Register Page (التسجيل)
- Forgot Password Page (نسيت كلمة المرور)
- Reset Password Page (إعادة تعيين كلمة المرور)
- Email Verification Page (تأكيد البريد الإلكتروني)

**صفحات Dashboard:**
- Main Dashboard (لوحة التحكم الرئيسية)
- User Profile (الملف الشخصي)
- Settings (الإعدادات)
- Notifications (الإشعارات)

**صفحات CRUD لكل كيان:**
- List/Index Page (صفحة القائمة)
- Create/Add Page (صفحة الإضافة)
- Edit/Update Page (صفحة التعديل)
- View/Detail Page (صفحة التفاصيل)
- Delete Confirmation Modal (نافذة تأكيد الحذف)

**صفحات النظام:**
- 404 Not Found
- 403 Forbidden
- 500 Server Error
- Maintenance Mode

#### B. فحص الأزرار الإلزامية
قائمة بجميع الأزرار التي يجب أن تكون موجودة:

**في صفحة القائمة (List):**
- Add New / Create (إضافة جديد)
- Search / Filter (بحث / تصفية)
- Export (تصدير)
- Refresh (تحديث)
- Edit (تعديل) - لكل صف
- Delete (حذف) - لكل صف
- View Details (عرض التفاصيل) - لكل صف

**في صفحة الإضافة/التعديل (Create/Edit):**
- Save (حفظ)
- Cancel (إلغاء)
- Save & Add Another (حفظ وإضافة آخر)
- Reset Form (إعادة تعيين النموذج)

**في صفحة التفاصيل (View):**
- Edit (تعديل)
- Delete (حذف)
- Back to List (العودة للقائمة)
- Print (طباعة)

**أزرار عامة:**
- Logout (تسجيل الخروج)
- Profile (الملف الشخصي)
- Notifications (الإشعارات)
- Help (مساعدة)

#### C. فحص الربط بين Frontend و Backend

**لكل صفحة:**
1. ✅ الصفحة موجودة في Frontend
2. ✅ Route موجود في Frontend Router
3. ✅ API Endpoint موجود في Backend
4. ✅ Controller موجود في Backend
5. ✅ Service/Logic موجود في Backend
6. ✅ Database Model موجود
7. ✅ Validation موجود
8. ✅ Error Handling موجود

**لكل زر:**
1. ✅ الزر موجود في UI
2. ✅ Event Handler موجود
3. ✅ API Call موجود
4. ✅ Backend Endpoint موجود
5. ✅ Response Handling موجود
6. ✅ Error Handling موجود
7. ✅ Loading State موجود
8. ✅ Success/Error Messages موجودة

#### D. Checklist Template

```markdown
## Pages & Buttons Verification Checklist

### Authentication Pages
- [ ] Login Page
  - [ ] Frontend: /login route exists
  - [ ] Backend: POST /api/auth/login exists
  - [ ] Login button works
  - [ ] Forgot password link works
  - [ ] Register link works
  
- [ ] Register Page
  - [ ] Frontend: /register route exists
  - [ ] Backend: POST /api/auth/register exists
  - [ ] Register button works
  - [ ] Back to login link works

### Dashboard Pages
- [ ] Main Dashboard
  - [ ] Frontend: /dashboard route exists
  - [ ] Backend: GET /api/dashboard/stats exists
  - [ ] All widgets load data
  - [ ] Refresh button works

### CRUD Pages (for each entity)
- [ ] List Page
  - [ ] Frontend: /{entity} route exists
  - [ ] Backend: GET /api/{entity} exists
  - [ ] Add New button exists and works
  - [ ] Edit button exists for each row
  - [ ] Delete button exists for each row
  - [ ] View button exists for each row
  - [ ] Search/Filter works
  - [ ] Pagination works

- [ ] Create Page
  - [ ] Frontend: /{entity}/create route exists
  - [ ] Backend: POST /api/{entity} exists
  - [ ] Save button works
  - [ ] Cancel button works
  - [ ] Form validation works
  - [ ] Success message shows
  - [ ] Redirects after save

- [ ] Edit Page
  - [ ] Frontend: /{entity}/edit/:id route exists
  - [ ] Backend: PUT /api/{entity}/:id exists
  - [ ] Backend: GET /api/{entity}/:id exists (to load data)
  - [ ] Update button works
  - [ ] Cancel button works
  - [ ] Form validation works
  - [ ] Success message shows

- [ ] View Page
  - [ ] Frontend: /{entity}/view/:id route exists
  - [ ] Backend: GET /api/{entity}/:id exists
  - [ ] Edit button works
  - [ ] Delete button works
  - [ ] Back button works

- [ ] Delete Functionality
  - [ ] Backend: DELETE /api/{entity}/:id exists
  - [ ] Confirmation modal shows
  - [ ] Confirm button works
  - [ ] Cancel button works
  - [ ] Success message shows
  - [ ] List refreshes after delete
```

### 3. أداة فحص تلقائية

إنشاء سكريبت Python لفحص المشروع:

```python
# .global/tools/pages_buttons_checker.py

import os
import re
import json

class PagesButtonsChecker:
    def __init__(self, project_path):
        self.project_path = project_path
        self.frontend_path = os.path.join(project_path, 'frontend')
        self.backend_path = os.path.join(project_path, 'backend')
        self.report = {
            'missing_pages': [],
            'missing_buttons': [],
            'missing_endpoints': [],
            'missing_connections': []
        }
    
    def check_frontend_routes(self):
        """فحص Routes في Frontend"""
        pass
    
    def check_backend_endpoints(self):
        """فحص Endpoints في Backend"""
        pass
    
    def check_buttons(self):
        """فحص الأزرار في الصفحات"""
        pass
    
    def check_connections(self):
        """فحص الربط بين Frontend و Backend"""
        pass
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        pass
```

### 4. إضافة إلى مراحل العمل

في **Phase 2: Planning & Architecture**:
- إنشاء قائمة كاملة بجميع الصفحات المطلوبة
- إنشاء قائمة كاملة بجميع الأزرار المطلوبة
- رسم خريطة الربط بين Frontend و Backend

في **Phase 3: Implementation**:
- تنفيذ جميع الصفحات المطلوبة
- تنفيذ جميع الأزرار المطلوبة
- تنفيذ جميع الروابط

في **Phase 4: Testing**:
- فحص وجود جميع الصفحات
- فحص عمل جميع الأزرار
- فحص الربط الكامل

### 5. قاعدة صارمة جديدة

**Rule: Complete Pages & Buttons Coverage**

```markdown
# Rule: Complete Pages & Buttons Coverage

## Principle
Every page MUST have all required buttons, and every button MUST be fully connected to the backend.

## Requirements

### 1. Page Completeness
- Every entity MUST have all CRUD pages (List, Create, Edit, View)
- Every page MUST be accessible via a route
- Every page MUST load data from the backend
- Every page MUST handle errors properly

### 2. Button Completeness
- Every page MUST have all required buttons
- Every button MUST have a working event handler
- Every button MUST call the correct API endpoint
- Every button MUST handle success and error states

### 3. Connection Completeness
- Every frontend route MUST have a corresponding backend endpoint
- Every API call MUST have proper error handling
- Every form MUST have validation (frontend + backend)
- Every action MUST have user feedback (loading, success, error)

## Verification
Run the Pages & Buttons Checker before marking any phase as complete:
\`\`\`bash
python .global/tools/pages_buttons_checker.py /path/to/project
\`\`\`

## Penalties
- Missing page: CRITICAL error - Phase cannot be marked complete
- Missing button: HIGH error - Phase cannot be marked complete
- Missing connection: HIGH error - Phase cannot be marked complete
```

---

## الخلاصة

هذا القسم سيضمن:
1. ✅ جميع الصفحات المطلوبة موجودة
2. ✅ جميع الأزرار المطلوبة موجودة وتعمل
3. ✅ الربط الكامل بين Frontend و Backend
4. ✅ فحص تلقائي قبل إكمال أي مرحلة
5. ✅ تقرير شامل بالصفحات والأزرار المفقودة

