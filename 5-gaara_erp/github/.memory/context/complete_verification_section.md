# القسم الكامل: فحص الصفحات، الأزرار، الربط، وقواعد البيانات

## 🔍 MANDATORY: COMPLETE SYSTEM VERIFICATION

### المبدأ الأساسي
**لا يمكن اعتبار أي مرحلة مكتملة إلا بعد التحقق من اكتمال جميع المكونات التالية:**

1. **جميع الصفحات المطلوبة موجودة وتعمل**
2. **جميع الأزرار موجودة ومربوطة بالـ Backend**
3. **جميع جداول قاعدة البيانات موجودة مع Migration**
4. **الربط الكامل بين Frontend ↔ Backend ↔ Database**

---

## 📄 PART 1: PAGES VERIFICATION (فحص الصفحات)

### القاعدة الصارمة
**Every entity in the system MUST have ALL of the following pages:**

#### 1.1 Authentication Pages (صفحات المصادقة)

| Page | Route | Backend API | Required |
|------|-------|-------------|----------|
| Login | `/login` | `POST /api/auth/login` | ✅ CRITICAL |
| Register | `/register` | `POST /api/auth/register` | ✅ CRITICAL |
| Forgot Password | `/forgot-password` | `POST /api/auth/forgot-password` | ✅ HIGH |
| Reset Password | `/reset-password/:token` | `POST /api/auth/reset-password` | ✅ HIGH |
| Email Verification | `/verify-email/:token` | `POST /api/auth/verify-email` | ✅ HIGH |
| Two-Factor Auth | `/2fa` | `POST /api/auth/verify-2fa` | ⚠️ MEDIUM |

#### 1.2 Dashboard Pages (صفحات لوحة التحكم)

| Page | Route | Backend API | Required |
|------|-------|-------------|----------|
| Main Dashboard | `/dashboard` | `GET /api/dashboard/stats` | ✅ CRITICAL |
| User Profile | `/profile` | `GET /api/users/profile` | ✅ CRITICAL |
| Edit Profile | `/profile/edit` | `PUT /api/users/profile` | ✅ HIGH |
| Settings | `/settings` | `GET /api/settings` | ✅ HIGH |
| Notifications | `/notifications` | `GET /api/notifications` | ✅ MEDIUM |

#### 1.3 CRUD Pages (لكل كيان في النظام)

**For EVERY entity (Users, Products, Orders, etc.), you MUST create:**

| Page Type | Route Pattern | Backend API | Purpose |
|-----------|---------------|-------------|---------|
| **List/Index** | `/{entity}` | `GET /api/{entity}` | عرض جميع السجلات مع بحث وفلترة |
| **Create** | `/{entity}/create` | `POST /api/{entity}` | إضافة سجل جديد |
| **Edit** | `/{entity}/edit/:id` | `PUT /api/{entity}/:id` | تعديل سجل موجود |
| **View/Details** | `/{entity}/view/:id` | `GET /api/{entity}/:id` | عرض تفاصيل سجل واحد |
| **Delete** | N/A (Modal) | `DELETE /api/{entity}/:id` | حذف سجل |

**مثال: إذا كان لديك كيان "Products"، يجب أن يكون لديك:**
- `/products` - قائمة المنتجات
- `/products/create` - إضافة منتج جديد
- `/products/edit/:id` - تعديل منتج
- `/products/view/:id` - عرض تفاصيل منتج
- Delete API endpoint

#### 1.4 Error Pages (صفحات الأخطاء)

| Page | Route | Purpose |
|------|-------|---------|
| 404 Not Found | `/404` | صفحة غير موجودة |
| 403 Forbidden | `/403` | غير مصرح |
| 500 Server Error | `/500` | خطأ في الخادم |
| Maintenance | `/maintenance` | صيانة |

---

## 🔘 PART 2: BUTTONS VERIFICATION (فحص الأزرار)

### القاعدة الصارمة
**Every page MUST have ALL required buttons, and every button MUST be fully functional and connected to the backend.**

#### 2.1 Buttons in List/Index Page

**REQUIRED buttons for EVERY list page:**

| Button | Function | API Call | Error Handling | Loading State |
|--------|----------|----------|----------------|---------------|
| **Add New** | Navigate to create page | N/A | N/A | N/A |
| **Search** | Filter results | `GET /api/{entity}?search=...` | ✅ | ✅ |
| **Filter** | Apply filters | `GET /api/{entity}?filter=...` | ✅ | ✅ |
| **Export** | Export to CSV/Excel | `GET /api/{entity}/export` | ✅ | ✅ |
| **Refresh** | Reload data | `GET /api/{entity}` | ✅ | ✅ |
| **Edit** (per row) | Navigate to edit page | N/A | N/A | N/A |
| **Delete** (per row) | Show delete confirmation | `DELETE /api/{entity}/:id` | ✅ | ✅ |
| **View** (per row) | Navigate to view page | N/A | N/A | N/A |
| **Bulk Actions** | Select multiple & delete/export | `POST /api/{entity}/bulk-delete` | ✅ | ✅ |

#### 2.2 Buttons in Create/Edit Page

**REQUIRED buttons for EVERY create/edit page:**

| Button | Function | API Call | Validation | Error Handling |
|--------|----------|----------|------------|----------------|
| **Save** | Submit form | `POST` or `PUT /api/{entity}` | ✅ Frontend + Backend | ✅ |
| **Cancel** | Go back without saving | N/A | N/A | N/A |
| **Save & Add Another** | Save and reset form | `POST /api/{entity}` | ✅ | ✅ |
| **Reset Form** | Clear all fields | N/A | N/A | N/A |

#### 2.3 Buttons in View/Details Page

**REQUIRED buttons for EVERY view page:**

| Button | Function | API Call |
|--------|----------|----------|
| **Edit** | Navigate to edit page | N/A |
| **Delete** | Show delete confirmation | `DELETE /api/{entity}/:id` |
| **Back to List** | Return to list page | N/A |
| **Print** | Print page | N/A |
| **Download PDF** | Generate PDF | `GET /api/{entity}/:id/pdf` |

#### 2.4 Global Navigation Buttons

**REQUIRED in EVERY authenticated page:**

| Button | Function | API Call |
|--------|----------|----------|
| **Logout** | End session | `POST /api/auth/logout` |
| **Profile** | Go to profile | N/A |
| **Notifications** | Show notifications | `GET /api/notifications` |
| **Settings** | Go to settings | N/A |
| **Help** | Show help | N/A |

---

## 🔗 PART 3: FRONTEND ↔ BACKEND CONNECTION (الربط الكامل)

### القاعدة الصارمة
**Every frontend action MUST have a complete connection chain to the backend.**

#### 3.1 Connection Chain Verification

**For EVERY page and button, verify this complete chain:**

```
[User Action] → [Frontend Event] → [API Call] → [Backend Route] → [Controller] → [Service] → [Database] → [Response] → [UI Update]
```

#### 3.2 Required Components for Each Connection

| Component | Location | Required Elements |
|-----------|----------|-------------------|
| **Frontend Route** | `routes/` or `App.jsx` | Route definition with path and component |
| **Page Component** | `pages/` or `views/` | React/Vue component file |
| **API Service** | `services/` or `api/` | Function to call backend endpoint |
| **Backend Route** | `routes/` | Express/FastAPI route definition |
| **Controller** | `controllers/` | Function to handle request |
| **Service/Logic** | `services/` | Business logic |
| **Model** | `models/` | Database model/schema |
| **Validation** | `validators/` or in controller | Input validation rules |
| **Error Handler** | `middleware/` | Error handling middleware |

#### 3.3 Verification Checklist (لكل صفحة)

```markdown
## Connection Verification: {Entity} - {Page Type}

### Frontend
- [ ] Route exists in router: `/{entity}/{action}`
- [ ] Page component exists: `pages/{Entity}{Action}.jsx`
- [ ] API service function exists: `api/{entity}Service.js`
- [ ] Loading state implemented
- [ ] Error handling implemented
- [ ] Success message implemented
- [ ] Form validation (if applicable)

### Backend
- [ ] Route exists: `{METHOD} /api/{entity}`
- [ ] Controller function exists: `{entity}Controller.{action}`
- [ ] Service function exists: `{entity}Service.{action}`
- [ ] Database model exists: `models/{Entity}.js`
- [ ] Input validation exists
- [ ] Error handling exists
- [ ] Response format correct

### Database
- [ ] Table exists in database
- [ ] Migration file exists
- [ ] All required columns exist
- [ ] Relationships defined
- [ ] Indexes created
```

---

## 🗄️ PART 4: DATABASE & MIGRATIONS (قواعد البيانات)

### القاعدة الصارمة
**Every entity MUST have a complete database table with proper migration files.**

#### 4.1 Database Table Requirements

**For EVERY entity, create a table with:**

| Requirement | Description | Example |
|-------------|-------------|---------|
| **Primary Key** | Unique identifier | `id` (UUID or Auto-increment) |
| **Timestamps** | Creation and update time | `created_at`, `updated_at` |
| **Soft Delete** | Deletion timestamp | `deleted_at` (nullable) |
| **All Fields** | All entity properties | Based on requirements |
| **Foreign Keys** | Relationships | `user_id`, `category_id`, etc. |
| **Indexes** | Performance optimization | On frequently queried columns |
| **Constraints** | Data integrity | `UNIQUE`, `NOT NULL`, `CHECK` |

#### 4.2 Migration File Structure

**REQUIRED for EVERY table:**

**Migration File Naming:**
```
{timestamp}_{action}_{table_name}.js
```

**Examples:**
```
20250114_create_users_table.js
20250114_create_products_table.js
20250114_add_email_to_users.js
20250114_create_orders_table.js
```

**Migration File Content (Example for Node.js/Sequelize):**

```javascript
// migrations/20250114_create_products_table.js

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('products', {
      id: {
        type: Sequelize.UUID,
        defaultValue: Sequelize.UUIDV4,
        primaryKey: true,
      },
      name: {
        type: Sequelize.STRING(255),
        allowNull: false,
      },
      description: {
        type: Sequelize.TEXT,
        allowNull: true,
      },
      price: {
        type: Sequelize.DECIMAL(10, 2),
        allowNull: false,
      },
      stock: {
        type: Sequelize.INTEGER,
        defaultValue: 0,
      },
      category_id: {
        type: Sequelize.UUID,
        allowNull: true,
        references: {
          model: 'categories',
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'SET NULL',
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.NOW,
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.NOW,
      },
      deleted_at: {
        type: Sequelize.DATE,
        allowNull: true,
      },
    });

    // Add indexes
    await queryInterface.addIndex('products', ['name']);
    await queryInterface.addIndex('products', ['category_id']);
    await queryInterface.addIndex('products', ['created_at']);
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('products');
  },
};
```

**Migration File Content (Example for Python/Django):**

```python
# migrations/0001_create_products.py

from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(
                    'Category',
                    on_delete=models.SET_NULL,
                    null=True,
                    related_name='products'
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='product_name_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='product_category_idx'),
        ),
    ]
```

#### 4.3 Database Seeder (Optional but Recommended)

**Create seed data for testing:**

```javascript
// seeders/20250114_seed_products.js

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.bulkInsert('products', [
      {
        id: Sequelize.literal('UUID()'),
        name: 'Product 1',
        description: 'Description for product 1',
        price: 99.99,
        stock: 100,
        created_at: new Date(),
        updated_at: new Date(),
      },
      // Add more seed data...
    ]);
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.bulkDelete('products', null, {});
  },
};
```

#### 4.4 Migration Commands

**MUST document these commands in README.md:**

```bash
# Create new migration
npm run migration:create -- --name create_products_table

# Run all pending migrations
npm run migration:up

# Rollback last migration
npm run migration:down

# Rollback all migrations
npm run migration:reset

# Run seeders
npm run seed:all

# Check migration status
npm run migration:status
```

---

## ✅ PART 5: COMPLETE VERIFICATION PROCESS

### 5.1 Pre-Implementation Checklist

**Before starting ANY implementation, create this document:**

**File:** `docs/COMPLETE_SYSTEM_CHECKLIST.md`

```markdown
# Complete System Verification Checklist

## Entities List
- [ ] Users
- [ ] Products
- [ ] Categories
- [ ] Orders
- [ ] ... (list all entities)

## For Each Entity: {Entity Name}

### Pages
- [ ] List Page (`/{entity}`)
  - [ ] Frontend route exists
  - [ ] Backend API exists: `GET /api/{entity}`
  - [ ] Pagination implemented
  - [ ] Search implemented
  - [ ] Filter implemented
  
- [ ] Create Page (`/{entity}/create`)
  - [ ] Frontend route exists
  - [ ] Backend API exists: `POST /api/{entity}`
  - [ ] Form validation (frontend)
  - [ ] Form validation (backend)
  
- [ ] Edit Page (`/{entity}/edit/:id`)
  - [ ] Frontend route exists
  - [ ] Backend API exists: `PUT /api/{entity}/:id`
  - [ ] Data loading works
  - [ ] Form validation works
  
- [ ] View Page (`/{entity}/view/:id`)
  - [ ] Frontend route exists
  - [ ] Backend API exists: `GET /api/{entity}/:id`
  - [ ] All fields displayed

### Buttons (List Page)
- [ ] Add New button → navigates to create page
- [ ] Search button → calls API with search params
- [ ] Filter button → calls API with filters
- [ ] Export button → calls export API
- [ ] Refresh button → reloads data
- [ ] Edit button (per row) → navigates to edit page
- [ ] Delete button (per row) → shows confirmation → calls delete API
- [ ] View button (per row) → navigates to view page

### Buttons (Create/Edit Page)
- [ ] Save button → submits form → calls API → shows success/error
- [ ] Cancel button → goes back
- [ ] Save & Add Another → saves → resets form
- [ ] Reset Form → clears all fields

### Buttons (View Page)
- [ ] Edit button → navigates to edit page
- [ ] Delete button → shows confirmation → calls delete API
- [ ] Back button → returns to list

### Backend
- [ ] Controller exists: `controllers/{Entity}Controller.js`
- [ ] Service exists: `services/{Entity}Service.js`
- [ ] Model exists: `models/{Entity}.js`
- [ ] Routes exist: `routes/{entity}.js`
- [ ] Validation exists: `validators/{entity}.js`
- [ ] All CRUD operations implemented:
  - [ ] GET /api/{entity} (list)
  - [ ] GET /api/{entity}/:id (get one)
  - [ ] POST /api/{entity} (create)
  - [ ] PUT /api/{entity}/:id (update)
  - [ ] DELETE /api/{entity}/:id (delete)

### Database
- [ ] Migration file exists: `migrations/xxx_create_{entity}_table.js`
- [ ] Table created in database
- [ ] All columns exist
- [ ] Primary key defined
- [ ] Foreign keys defined
- [ ] Indexes created
- [ ] Timestamps added (created_at, updated_at)
- [ ] Soft delete column added (deleted_at)

### Testing
- [ ] Unit tests for service
- [ ] Integration tests for API
- [ ] E2E tests for UI
```

### 5.2 Automated Verification Script

**Create this tool:** `.global/tools/complete_system_checker.py`

```python
#!/usr/bin/env python3
"""
Complete System Verification Tool
Checks pages, buttons, connections, and database migrations
"""

import os
import json
import re
from pathlib import Path

class CompleteSystemChecker:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.frontend_path = self.project_path / 'frontend'
        self.backend_path = self.project_path / 'backend'
        self.report = {
            'entities': [],
            'missing_pages': [],
            'missing_buttons': [],
            'missing_endpoints': [],
            'missing_migrations': [],
            'missing_connections': [],
            'score': 0
        }
    
    def find_entities(self):
        """استخراج جميع الكيانات من المشروع"""
        entities = set()
        
        # من Models
        models_path = self.backend_path / 'models'
        if models_path.exists():
            for file in models_path.glob('*.js'):
                if file.stem not in ['index', 'base']:
                    entities.add(file.stem)
        
        return list(entities)
    
    def check_pages(self, entity):
        """فحص وجود جميع الصفحات المطلوبة"""
        required_pages = ['index', 'create', 'edit', 'view']
        missing = []
        
        for page in required_pages:
            page_file = self.frontend_path / 'pages' / entity / f'{page}.jsx'
            if not page_file.exists():
                missing.append(f'{entity}/{page}')
        
        return missing
    
    def check_buttons(self, entity):
        """فحص وجود الأزرار المطلوبة"""
        # تنفيذ فحص الأزرار
        pass
    
    def check_endpoints(self, entity):
        """فحص وجود جميع Endpoints المطلوبة"""
        required_endpoints = ['index', 'show', 'store', 'update', 'destroy']
        missing = []
        
        routes_file = self.backend_path / 'routes' / f'{entity}.js'
        if not routes_file.exists():
            return required_endpoints
        
        content = routes_file.read_text()
        for endpoint in required_endpoints:
            if endpoint not in content:
                missing.append(f'{entity}.{endpoint}')
        
        return missing
    
    def check_migrations(self, entity):
        """فحص وجود Migration للكيان"""
        migrations_path = self.backend_path / 'migrations'
        if not migrations_path.exists():
            return [f'{entity} - no migrations folder']
        
        pattern = f'*create_{entity}_table*'
        migrations = list(migrations_path.glob(pattern))
        
        if not migrations:
            return [f'{entity} - no migration file']
        
        return []
    
    def check_database_connection(self, entity):
        """فحص الربط مع قاعدة البيانات"""
        # تنفيذ فحص الربط
        pass
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        entities = self.find_entities()
        
        for entity in entities:
            self.report['entities'].append(entity)
            self.report['missing_pages'].extend(self.check_pages(entity))
            self.report['missing_endpoints'].extend(self.check_endpoints(entity))
            self.report['missing_migrations'].extend(self.check_migrations(entity))
        
        # حساب النتيجة
        total_required = len(entities) * 10  # 10 items per entity
        total_missing = (
            len(self.report['missing_pages']) +
            len(self.report['missing_endpoints']) +
            len(self.report['missing_migrations'])
        )
        self.report['score'] = ((total_required - total_missing) / total_required) * 100
        
        return self.report
    
    def print_report(self):
        """طباعة التقرير"""
        report = self.generate_report()
        
        print("=" * 80)
        print("COMPLETE SYSTEM VERIFICATION REPORT")
        print("=" * 80)
        print(f"\nEntities Found: {len(report['entities'])}")
        print(f"Completion Score: {report['score']:.2f}%\n")
        
        if report['missing_pages']:
            print("❌ Missing Pages:")
            for page in report['missing_pages']:
                print(f"   - {page}")
        
        if report['missing_endpoints']:
            print("\n❌ Missing Endpoints:")
            for endpoint in report['missing_endpoints']:
                print(f"   - {endpoint}")
        
        if report['missing_migrations']:
            print("\n❌ Missing Migrations:")
            for migration in report['missing_migrations']:
                print(f"   - {migration}")
        
        if report['score'] == 100:
            print("\n✅ ALL CHECKS PASSED!")
        else:
            print(f"\n⚠️  INCOMPLETE: {100 - report['score']:.2f}% missing")
        
        print("=" * 80)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python complete_system_checker.py /path/to/project")
        sys.exit(1)
    
    checker = CompleteSystemChecker(sys.argv[1])
    checker.print_report()
```

---

## 🚨 PART 6: ENFORCEMENT RULES

### 6.1 Phase Completion Rules

**You CANNOT mark a phase as complete unless:**

1. ✅ All required pages exist
2. ✅ All required buttons exist and work
3. ✅ All backend endpoints exist
4. ✅ All database migrations exist
5. ✅ Complete verification script passes with 100% score

### 6.2 Mandatory Verification Command

**Before completing Phase 3 (Implementation), you MUST run:**

```bash
python .global/tools/complete_system_checker.py /path/to/project
```

**If score < 100%, you MUST:**
1. Log all missing items in `errors/high/incomplete_system.md`
2. Fix all missing items
3. Re-run the checker
4. Only proceed when score = 100%

---

## 📝 SUMMARY

This verification system ensures:

1. **Complete Pages:** Every entity has all CRUD pages
2. **Complete Buttons:** Every page has all required buttons
3. **Complete Connections:** Every button is connected to backend
4. **Complete Database:** Every entity has proper migration
5. **Complete Testing:** Automated verification before completion

**This is a ZERO-TOLERANCE requirement. No exceptions.**

