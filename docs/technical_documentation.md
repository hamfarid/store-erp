# التوثيق التقني الشامل - نظام إدارة المخزون

**إعداد:** Manus AI  
**التاريخ:** 16 يونيو 2025  
**الإصدار:** 1.0

---

## المحتويات

1. [نظرة عامة على النظام](#نظرة-عامة-على-النظام)
2. [معمارية النظام](#معمارية-النظام)
3. [قاعدة البيانات](#قاعدة-البيانات)
4. [واجهات برمجة التطبيقات](#واجهات-برمجة-التطبيقات)
5. [الواجهة الأمامية](#الواجهة-الأمامية)
6. [الأمان والصلاحيات](#الأمان-والصلاحيات)
7. [التثبيت والنشر](#التثبيت-والنشر)
8. [الصيانة والمراقبة](#الصيانة-والمراقبة)

---

## نظرة عامة على النظام

### الهدف والنطاق

نظام إدارة المخزون هو تطبيق ويب شامل مطور باستخدام تقنيات حديثة لتوفير حل متكامل لإدارة المخازن والمنتجات. النظام مصمم ليكون بديلاً متطوراً لأنظمة Excel التقليدية، مع توفير واجهة مستخدم حديثة وقاعدة بيانات قوية وإمكانيات تحليلية متقدمة.

### المتطلبات الوظيفية الرئيسية

النظام يلبي المتطلبات الوظيفية التالية:

**إدارة المنتجات الشاملة**: يوفر النظام إمكانيات كاملة لإدارة المنتجات تشمل إضافة وتعديل وحذف المنتجات، مع دعم لمعلومات مفصلة لكل منتج مثل الاسم، رمز المنتج (SKU)، الفئة، الوحدة، أسعار التكلفة والبيع، الكميات المتاحة، والحد الأدنى للمخزون. النظام يدعم أيضاً تصنيف المنتجات في فئات مختلفة وربطها بالموردين.

**تتبع حركات المخزون**: النظام يسجل جميع حركات المخزون بدقة، سواء كانت وارد أو صادر، مع تسجيل التاريخ والوقت والمستخدم المسؤول عن كل حركة. هذا يوفر تتبعاً كاملاً لتاريخ كل منتج ويساعد في المحاسبة والتدقيق.

**إدارة العملاء والموردين**: قاعدة بيانات شاملة للعملاء والموردين تتضمن معلومات الاتصال، التخصصات، تاريخ التعاملات، والتقييمات. هذا يساعد في بناء علاقات قوية مع الشركاء التجاريين وتحسين عمليات الشراء والبيع.

**التقارير والتحليلات**: مجموعة شاملة من التقارير التفاعلية والرسوم البيانية التي تساعد في فهم أداء المخزون واتخاذ قرارات مدروسة. التقارير تشمل تقارير المخزون الحالي، حركات المخزون، تحليل المبيعات، والمنتجات الأكثر والأقل مبيعاً.

**نظام التنبيهات**: تنبيهات تلقائية للمخزون المنخفض، المنتجات منتهية الصلاحية، والأحداث المهمة الأخرى. هذا يساعد في منع نفاد المخزون والحفاظ على استمرارية العمل.

**الاستيراد والتصدير**: إمكانيات شاملة لاستيراد البيانات من ملفات Excel وتصدير التقارير والبيانات إلى تنسيقات مختلفة مثل Excel وPDF. هذا يسهل الانتقال من الأنظمة القديمة والتكامل مع الأنظمة الأخرى.

### التقنيات المستخدمة

**الواجهة الخلفية (Backend)**:
- **Python 3.11**: لغة البرمجة الرئيسية للخادم
- **Flask**: إطار عمل ويب خفيف ومرن لبناء واجهات برمجة التطبيقات
- **SQLAlchemy**: مكتبة ORM لإدارة قاعدة البيانات
- **SQLite/PostgreSQL**: قواعد بيانات مدعومة
- **Flask-CORS**: لدعم طلبات CORS من الواجهة الأمامية
- **Pandas**: لمعالجة البيانات والتحليلات
- **OpenPyXL**: لقراءة وكتابة ملفات Excel

**الواجهة الأمامية (Frontend)**:
- **React 18**: مكتبة JavaScript لبناء واجهات المستخدم
- **Vite**: أداة بناء سريعة ومحسنة للتطوير
- **Tailwind CSS**: إطار عمل CSS للتصميم السريع والمتجاوب
- **Lucide React**: مكتبة أيقونات حديثة
- **React Hot Toast**: لعرض التنبيهات والرسائل
- **Recharts**: لإنشاء الرسوم البيانية التفاعلية

**أدوات التطوير والنشر**:
- **Git**: نظام إدارة الإصدارات
- **npm/pnpm**: مدير الحزم لـ Node.js
- **pip**: مدير الحزم لـ Python
- **Docker**: للحاويات والنشر (اختياري)
- **Nginx**: خادم ويب للإنتاج

### خصائص النظام

**الأداء**: النظام محسن للأداء السريع مع تحميل البيانات بشكل تدريجي وذاكرة تخزين مؤقت ذكية. الواجهة الأمامية تستخدم تقنيات React الحديثة لضمان استجابة سريعة للمستخدم.

**القابلية للتوسع**: معمارية النظام تسمح بالتوسع الأفقي والعمودي. يمكن إضافة خوادم إضافية أو ترقية الأجهزة الموجودة حسب الحاجة.

**الأمان**: النظام يطبق أفضل ممارسات الأمان مع تشفير البيانات، نظام صلاحيات متعدد المستويات، وحماية من الهجمات الشائعة مثل SQL Injection وXSS.

**سهولة الاستخدام**: واجهة مستخدم بديهية باللغة العربية مع دعم كامل لاتجاه RTL ومصممة لتكون سهلة التعلم والاستخدام.

**التوافق**: النظام يعمل على جميع المتصفحات الحديثة وجميع أنظمة التشغيل الرئيسية، مع دعم كامل للأجهزة المحمولة والأجهزة اللوحية.

---

## معمارية النظام

### النمط المعماري

النظام يتبع نمط **Client-Server Architecture** مع فصل واضح بين الواجهة الأمامية والخلفية. هذا النمط يوفر مرونة في التطوير والصيانة ويسمح بتطوير كل جزء بشكل مستقل.

### مكونات النظام

**طبقة العرض (Presentation Layer)**:
هذه الطبقة تتكون من تطبيق React الذي يعمل في متصفح المستخدم. هي المسؤولة عن عرض البيانات وتلقي مدخلات المستخدم وإرسالها للطبقات الأخرى. الطبقة تتضمن:

- مكونات React للواجهات المختلفة
- إدارة الحالة المحلية للتطبيق
- التحقق من صحة البيانات في الواجهة الأمامية
- التفاعل مع واجهات برمجة التطبيقات

**طبقة الخدمات (Service Layer)**:
طبقة وسطية تحتوي على منطق الأعمال وتتعامل مع طلبات HTTP من الواجهة الأمامية. هذه الطبقة مبنية باستخدام Flask وتتضمن:

- واجهات برمجة التطبيقات (REST APIs)
- منطق الأعمال والتحقق من صحة البيانات
- إدارة الجلسات والمصادقة
- معالجة الأخطاء والاستثناءات

**طبقة البيانات (Data Layer)**:
هذه الطبقة مسؤولة عن تخزين واسترجاع البيانات. تتضمن:

- قاعدة البيانات (SQLite أو PostgreSQL)
- نماذج البيانات (Data Models)
- طبقة الوصول للبيانات (Data Access Layer)
- إدارة المعاملات (Transactions)

### تدفق البيانات

**من المستخدم إلى قاعدة البيانات**:
1. المستخدم يتفاعل مع الواجهة الأمامية (React)
2. الواجهة الأمامية تتحقق من صحة البيانات محلياً
3. إرسال طلب HTTP إلى الواجهة الخلفية (Flask)
4. الواجهة الخلفية تتحقق من الصلاحيات والبيانات
5. تنفيذ منطق الأعمال المطلوب
6. التفاعل مع قاعدة البيانات عبر SQLAlchemy
7. إرجاع النتيجة للواجهة الأمامية
8. عرض النتيجة للمستخدم

**من قاعدة البيانات إلى المستخدم**:
1. طلب البيانات من الواجهة الأمامية
2. الواجهة الخلفية تستعلم قاعدة البيانات
3. معالجة وتنسيق البيانات
4. إرسال البيانات للواجهة الأمامية
5. عرض البيانات في الواجهة المناسبة

### الاتصال بين المكونات

**HTTP/HTTPS**: جميع الاتصالات بين الواجهة الأمامية والخلفية تتم عبر بروتوكول HTTP/HTTPS باستخدام تنسيق JSON لتبادل البيانات.

**RESTful APIs**: النظام يتبع مبادئ REST في تصميم واجهات برمجة التطبيقات، مما يجعلها سهلة الفهم والاستخدام والتطوير.

**CORS**: تم تكوين CORS بشكل صحيح للسماح للواجهة الأمامية بالوصول للواجهة الخلفية من نطاقات مختلفة.

### إدارة الحالة

**الواجهة الأمامية**: تستخدم React Hooks لإدارة الحالة المحلية، مع استخدام useEffect لتحميل البيانات وuseState لإدارة حالة المكونات.

**الواجهة الخلفية**: تستخدم Flask Sessions لإدارة جلسات المستخدمين وSQLAlchemy لإدارة حالة قاعدة البيانات.

### التعامل مع الأخطاء

النظام يطبق استراتيجية شاملة للتعامل مع الأخطاء:

**في الواجهة الأمامية**:
- التحقق من صحة البيانات قبل الإرسال
- معالجة أخطاء الشبكة والخادم
- عرض رسائل خطأ واضحة للمستخدم
- نظام fallback للبيانات التجريبية

**في الواجهة الخلفية**:
- التحقق من صحة البيانات الواردة
- معالجة استثناءات قاعدة البيانات
- تسجيل الأخطاء للمراجعة اللاحقة
- إرجاع رسائل خطأ مفيدة ومفهومة

---

## قاعدة البيانات

### تصميم قاعدة البيانات

قاعدة البيانات مصممة باستخدام نمط **Relational Database** مع تطبيق مبادئ التطبيع (Normalization) لضمان سلامة البيانات وتجنب التكرار.

### الجداول الرئيسية

**جدول المستخدمين (Users)**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

هذا الجدول يخزن معلومات المستخدمين الأساسية مع تشفير كلمات المرور وتحديد الأدوار والصلاحيات. الحقل `role` يحدد نوع المستخدم (admin, manager, user) والذي يؤثر على الصلاحيات المتاحة.

**جدول المنتجات (Products)**:
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    min_quantity INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    supplier_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
);
```

جدول المنتجات هو قلب النظام ويحتوي على جميع المعلومات المتعلقة بالمنتجات. الحقل `sku` فريد لكل منتج ويستخدم للتتبع السريع. الأسعار مخزنة بدقة عشرية لضمان دقة الحسابات المالية.

**جدول العملاء (Customers)**:
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    address TEXT,
    notes TEXT,
    total_purchases DECIMAL(12,2) DEFAULT 0,
    last_purchase_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**جدول الموردين (Suppliers)**:
```sql
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    specialization VARCHAR(100),
    rating INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**جدول حركات المخزون (Stock Movements)**:
```sql
CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    movement_type VARCHAR(20) NOT NULL, -- 'in' or 'out'
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2),
    total_value DECIMAL(12,2),
    reference_number VARCHAR(100),
    notes TEXT,
    user_id INTEGER NOT NULL,
    customer_id INTEGER, -- for 'out' movements
    supplier_id INTEGER, -- for 'in' movements
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
);
```

هذا الجدول يسجل جميع حركات المخزون مع ربطها بالمنتجات والمستخدمين والعملاء أو الموردين حسب نوع الحركة. هذا يوفر تتبعاً كاملاً لتاريخ كل منتج.

### العلاقات بين الجداول

**علاقة واحد إلى متعدد (One-to-Many)**:
- مورد واحد يمكن أن يوفر عدة منتجات
- منتج واحد يمكن أن يكون له عدة حركات مخزون
- مستخدم واحد يمكن أن ينفذ عدة حركات مخزون
- عميل واحد يمكن أن يكون له عدة عمليات شراء

**المفاتيح الخارجية (Foreign Keys)**:
جميع العلاقات محمية بمفاتيح خارجية لضمان سلامة البيانات ومنع حذف السجلات المرتبطة بسجلات أخرى.

### الفهارس (Indexes)

لتحسين الأداء، تم إنشاء فهارس على الحقول الأكثر استخداماً في الاستعلامات:

```sql
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_stock_movements_product_id ON stock_movements(product_id);
CREATE INDEX idx_stock_movements_created_at ON stock_movements(created_at);
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_users_username ON users(username);
```

### إدارة البيانات

**التحقق من سلامة البيانات**: النظام يطبق قيود صارمة على البيانات لضمان سلامتها:
- قيود الفرادة (Unique Constraints) على الحقول المهمة
- قيود عدم القبول بالقيم الفارغة (NOT NULL) على الحقول المطلوبة
- قيود التحقق (Check Constraints) على القيم المنطقية
- المفاتيح الخارجية لضمان العلاقات الصحيحة

**النسخ الاحتياطي**: النظام يدعم عدة طرق للنسخ الاحتياطي:
- نسخ احتياطية تلقائية دورية
- نسخ احتياطية يدوية عند الطلب
- تصدير البيانات إلى ملفات SQL أو CSV
- استعادة البيانات من النسخ الاحتياطية

**الأداء**: لضمان الأداء الأمثل:
- استخدام الفهارس المناسبة
- تحسين الاستعلامات المعقدة
- تنظيف البيانات القديمة دورياً
- مراقبة أداء قاعدة البيانات

---

## واجهات برمجة التطبيقات

### تصميم API

النظام يتبع مبادئ **RESTful API Design** مع استخدام HTTP methods المناسبة وتنظيم منطقي للمسارات.

### مسارات API الرئيسية

**مصادقة المستخدمين**:
```
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/register
GET /api/auth/profile
PUT /api/auth/profile
POST /api/auth/change-password
```

**إدارة المنتجات**:
```
GET /api/products              # جلب جميع المنتجات
POST /api/products             # إضافة منتج جديد
GET /api/products/{id}         # جلب منتج محدد
PUT /api/products/{id}         # تحديث منتج
DELETE /api/products/{id}      # حذف منتج
GET /api/products/low-stock    # المنتجات منخفضة المخزون
GET /api/products/categories   # جلب الفئات
```

**إدارة العملاء**:
```
GET /api/customers             # جلب جميع العملاء
POST /api/customers            # إضافة عميل جديد
GET /api/customers/{id}        # جلب عميل محدد
PUT /api/customers/{id}        # تحديث عميل
DELETE /api/customers/{id}     # حذف عميل
```

**إدارة الموردين**:
```
GET /api/suppliers             # جلب جميع الموردين
POST /api/suppliers            # إضافة مورد جديد
GET /api/suppliers/{id}        # جلب مورد محدد
PUT /api/suppliers/{id}        # تحديث مورد
DELETE /api/suppliers/{id}     # حذف مورد
```

**حركات المخزون**:
```
GET /api/movements             # جلب حركات المخزون
POST /api/movements            # تسجيل حركة جديدة
GET /api/movements/{id}        # جلب حركة محددة
GET /api/movements/recent      # الحركات الأخيرة
```

**الإحصائيات والتقارير**:
```
GET /api/stats/overview        # إحصائيات عامة
GET /api/stats/products        # إحصائيات المنتجات
GET /api/stats/movements       # إحصائيات الحركات
GET /api/reports/inventory     # تقرير المخزون
GET /api/reports/sales         # تقرير المبيعات
```

**الاستيراد والتصدير**:
```
POST /api/import/products      # استيراد منتجات من Excel
POST /api/import/customers     # استيراد عملاء من Excel
GET /api/export/products       # تصدير المنتجات
GET /api/export/inventory      # تصدير تقرير المخزون
```

### تنسيق الاستجابات

جميع استجابات API تتبع تنسيقاً موحداً:

**استجابة ناجحة**:
```json
{
    "success": true,
    "data": {
        // البيانات المطلوبة
    },
    "message": "تم تنفيذ العملية بنجاح",
    "timestamp": "2025-06-16T08:30:00Z"
}
```

**استجابة خطأ**:
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "البيانات المدخلة غير صحيحة",
        "details": {
            "field": "اسم الحقل",
            "issue": "وصف المشكلة"
        }
    },
    "timestamp": "2025-06-16T08:30:00Z"
}
```

### التحقق من صحة البيانات

كل API endpoint يتضمن تحققاً شاملاً من صحة البيانات:

**تحقق من نوع البيانات**: التأكد من أن البيانات من النوع المطلوب (رقم، نص، تاريخ، إلخ)

**تحقق من النطاقات**: التأكد من أن القيم ضمن النطاقات المقبولة

**تحقق من الفرادة**: التأكد من عدم تكرار القيم الفريدة

**تحقق من العلاقات**: التأكد من وجود السجلات المرتبطة

### معالجة الأخطاء

النظام يطبق استراتيجية شاملة لمعالجة الأخطاء:

**أخطاء التحقق من صحة البيانات**: رسائل واضحة تحدد المشكلة بالضبط

**أخطاء قاعدة البيانات**: معالجة أخطاء الاتصال والاستعلامات

**أخطاء الصلاحيات**: رسائل واضحة عند عدم وجود صلاحيات كافية

**أخطاء النظام**: معالجة الأخطاء غير المتوقعة مع تسجيلها للمراجعة

### الأمان في APIs

**المصادقة**: جميع APIs المحمية تتطلب مصادقة صحيحة

**التشفير**: جميع البيانات الحساسة مشفرة أثناء النقل والتخزين

**حماية من CSRF**: تطبيق حماية من هجمات Cross-Site Request Forgery

**تحديد المعدل**: حماية من الهجمات بتحديد عدد الطلبات المسموحة

---


## الواجهة الأمامية

### تقنيات React المستخدمة

**React 18 مع Hooks**: النظام يستخدم أحدث إصدار من React مع الاعتماد الكامل على Hooks بدلاً من Class Components. هذا يوفر كوداً أكثر نظافة وأداءً أفضل.

**Functional Components**: جميع المكونات مكتوبة كـ Functional Components مع استخدام Hooks لإدارة الحالة والتأثيرات الجانبية.

**Custom Hooks**: تم إنشاء Custom Hooks لإعادة استخدام المنطق المشترك مثل جلب البيانات والتحقق من صحة النماذج.

### بنية المشروع

```
src/
├── components/           # المكونات الرئيسية
│   ├── Dashboard.jsx    # لوحة المعلومات
│   ├── Products.jsx     # إدارة المنتجات
│   ├── Customers.jsx    # إدارة العملاء
│   ├── Suppliers.jsx    # إدارة الموردين
│   ├── Reports.jsx      # التقارير
│   ├── Sidebar.jsx      # الشريط الجانبي
│   └── ui/              # مكونات واجهة المستخدم
│       └── FormComponents.jsx
├── services/            # خدمات API
│   └── ApiService.js
├── utils/               # أدوات مساعدة
│   └── validation.js
├── styles/              # ملفات التنسيق
└── App.jsx             # المكون الرئيسي
```

### إدارة الحالة

**useState**: لإدارة الحالة المحلية في كل مكون

**useEffect**: لتحميل البيانات والتأثيرات الجانبية

**useCallback**: لتحسين الأداء بمنع إعادة إنشاء الدوال غير الضرورية

**useMemo**: لتحسين الأداء بحفظ نتائج العمليات المكلفة

### التصميم والتنسيق

**Tailwind CSS**: إطار عمل CSS utility-first يوفر مرونة كبيرة في التصميم مع حجم ملف صغير.

**دعم RTL**: تصميم كامل يدعم اتجاه النص من اليمين لليسار للغة العربية.

**التصميم المتجاوب**: الواجهة تتكيف مع جميع أحجام الشاشات من الهواتف المحمولة إلى الشاشات الكبيرة.

**نظام الألوان**: نظام ألوان متسق يستخدم متغيرات CSS لسهولة التخصيص.

### مكونات واجهة المستخدم

**FormInput**: مكون موحد لحقول الإدخال مع دعم التحقق من صحة البيانات
```jsx
<FormInput
  label="اسم المنتج"
  value={productName}
  onChange={setProductName}
  error={errors.productName}
  required
/>
```

**Button**: مكون أزرار موحد مع أنماط مختلفة
```jsx
<Button 
  variant="primary" 
  onClick={handleSave}
  loading={isLoading}
>
  حفظ
</Button>
```

**Modal**: مكون نوافذ منبثقة للحوارات والنماذج
```jsx
<Modal 
  isOpen={showModal} 
  onClose={closeModal}
  title="إضافة منتج جديد"
>
  {/* محتوى النافذة */}
</Modal>
```

**DataTable**: مكون جداول البيانات مع دعم البحث والفلترة والترتيب
```jsx
<DataTable
  data={products}
  columns={productColumns}
  searchable
  sortable
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

### التفاعل مع APIs

**ApiService**: خدمة موحدة للتعامل مع جميع طلبات API
```javascript
class ApiService {
  static async get(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      return await this.handleResponse(response);
    } catch (error) {
      throw new Error(`خطأ في جلب البيانات: ${error.message}`);
    }
  }

  static async post(endpoint, data) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      return await this.handleResponse(response);
    } catch (error) {
      throw new Error(`خطأ في إرسال البيانات: ${error.message}`);
    }
  }
}
```

**معالجة الأخطاء**: نظام شامل لمعالجة أخطاء API مع عرض رسائل مفيدة للمستخدم

**نظام Fallback**: عند فشل الاتصال بـ API، يتم عرض بيانات تجريبية للحفاظ على تجربة المستخدم

### التحقق من صحة البيانات

**مكتبة التحقق المخصصة**: نظام شامل للتحقق من صحة البيانات في الواجهة الأمامية
```javascript
const validationRules = {
  required: (value) => value && value.trim() !== '',
  email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
  phone: (value) => /^[0-9+\-\s()]+$/.test(value),
  positive: (value) => parseFloat(value) > 0,
  integer: (value) => Number.isInteger(parseFloat(value)),
};
```

**التحقق الفوري**: التحقق من صحة البيانات أثناء الكتابة مع عرض رسائل الخطأ فوراً

**التحقق قبل الإرسال**: تحقق شامل من جميع البيانات قبل إرسالها للخادم

### الرسوم البيانية والتصورات

**Recharts**: مكتبة رسوم بيانية تفاعلية مبنية على React وD3
```jsx
<ResponsiveContainer width="100%" height={300}>
  <PieChart>
    <Pie
      data={categoryData}
      cx="50%"
      cy="50%"
      outerRadius={80}
      fill="#8884d8"
      dataKey="value"
      label
    />
    <Tooltip />
    <Legend />
  </PieChart>
</ResponsiveContainer>
```

**أنواع الرسوم المدعومة**:
- رسوم دائرية لتوزيع الفئات
- رسوم بيانية خطية للاتجاهات الزمنية
- رسوم بيانية عمودية للمقارنات
- مؤشرات الأداء (KPIs) التفاعلية

### تحسين الأداء

**Code Splitting**: تقسيم الكود لتحميل أسرع
```jsx
const LazyComponent = React.lazy(() => import('./Component'));
```

**Memoization**: استخدام React.memo وuseMemo لتجنب إعادة الرسم غير الضرورية

**Virtual Scrolling**: للجداول الكبيرة لتحسين الأداء

**Image Optimization**: ضغط وتحسين الصور لتحميل أسرع

---

## الأمان والصلاحيات

### نظام المصادقة

**تشفير كلمات المرور**: استخدام bcrypt لتشفير كلمات المرور بشكل آمن
```python
from werkzeug.security import generate_password_hash, check_password_hash

# تشفير كلمة المرور
password_hash = generate_password_hash(password)

# التحقق من كلمة المرور
is_valid = check_password_hash(password_hash, password)
```

**إدارة الجلسات**: استخدام Flask Sessions مع تشفير آمن
```python
from flask import session
import secrets

# إنشاء مفتاح سري آمن
app.secret_key = secrets.token_hex(16)

# تسجيل دخول المستخدم
session['user_id'] = user.id
session['username'] = user.username
session['role'] = user.role
```

**انتهاء صلاحية الجلسات**: الجلسات تنتهي تلقائياً بعد فترة عدم نشاط محددة

### نظام الصلاحيات

**الأدوار المختلفة**:

**مدير النظام (Admin)**:
- جميع الصلاحيات
- إدارة المستخدمين
- إعدادات النظام
- النسخ الاحتياطي والاستعادة

**مدير المخزون (Manager)**:
- إدارة المنتجات والمخزون
- إدارة العملاء والموردين
- عرض جميع التقارير
- تصدير البيانات

**محاسب (Accountant)**:
- عرض البيانات والتقارير
- تصدير التقارير المالية
- عرض لوحة المعلومات

**مستخدم عادي (User)**:
- عرض المنتجات
- عرض التقارير الأساسية

**تطبيق الصلاحيات**:
```python
from functools import wraps
from flask import session, jsonify

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                return jsonify({'error': 'غير مصرح بالدخول'}), 401
            
            user_role = session.get('role')
            if not has_permission(user_role, permission):
                return jsonify({'error': 'ليس لديك صلاحية لهذه العملية'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# استخدام الصلاحيات
@app.route('/api/products', methods=['POST'])
@require_permission('INVENTORY_ADD')
def add_product():
    # منطق إضافة المنتج
    pass
```

### الحماية من الهجمات

**SQL Injection**: استخدام SQLAlchemy ORM يحمي تلقائياً من هجمات SQL Injection

**XSS (Cross-Site Scripting)**: تنظيف جميع المدخلات وتشفير المخرجات
```python
from markupsafe import escape

def sanitize_input(data):
    if isinstance(data, str):
        return escape(data)
    return data
```

**CSRF (Cross-Site Request Forgery)**: استخدام CSRF tokens للحماية من هجمات CSRF

**Rate Limiting**: تحديد عدد الطلبات المسموحة لمنع هجمات DDoS
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # منطق تسجيل الدخول
    pass
```

### تشفير البيانات

**تشفير أثناء النقل**: جميع الاتصالات تتم عبر HTTPS

**تشفير أثناء التخزين**: البيانات الحساسة مشفرة في قاعدة البيانات
```python
from cryptography.fernet import Fernet

# إنشاء مفتاح التشفير
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# تشفير البيانات
encrypted_data = cipher_suite.encrypt(data.encode())

# فك التشفير
decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
```

### مراجعة الأمان

**تسجيل العمليات**: جميع العمليات المهمة مسجلة للمراجعة
```python
import logging

# إعداد نظام التسجيل
logging.basicConfig(
    filename='security.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_security_event(event_type, user_id, details):
    logging.info(f"Security Event: {event_type} - User: {user_id} - Details: {details}")
```

**مراقبة الأنشطة المشبوهة**: النظام يراقب الأنشطة غير العادية ويسجلها

**تحديثات الأمان**: النظام يتضمن آلية لتطبيق تحديثات الأمان بسرعة

---

## التثبيت والنشر

### متطلبات النظام

**الحد الأدنى للمتطلبات**:
- نظام التشغيل: Windows 10, macOS 10.14, أو Linux (Ubuntu 18.04+)
- المعالج: Intel Core i3 أو AMD Ryzen 3
- الذاكرة: 4 جيجابايت RAM
- مساحة التخزين: 10 جيجابايت مساحة فارغة
- الشبكة: اتصال إنترنت للتحديثات

**المتطلبات الموصى بها**:
- المعالج: Intel Core i5 أو AMD Ryzen 5
- الذاكرة: 8 جيجابايت RAM أو أكثر
- مساحة التخزين: 50 جيجابايت مساحة فارغة
- الشبكة: اتصال إنترنت سريع

### تثبيت البيئة التطويرية

**تثبيت Python**:
```bash
# تحميل وتثبيت Python 3.11
# من الموقع الرسمي: https://python.org

# التحقق من التثبيت
python --version
pip --version
```

**تثبيت Node.js**:
```bash
# تحميل وتثبيت Node.js 18+
# من الموقع الرسمي: https://nodejs.org

# التحقق من التثبيت
node --version
npm --version
```

**إعداد المشروع**:
```bash
# استنساخ المشروع
git clone <repository-url>
cd inventory-management-system

# إعداد البيئة الافتراضية لـ Python
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate     # على Windows

# تثبيت متطلبات Python
pip install -r requirements.txt

# إعداد الواجهة الأمامية
cd inventory-frontend
npm install
```

### إعداد قاعدة البيانات

**SQLite (للتطوير)**:
```python
# في ملف config.py
DATABASE_URL = 'sqlite:///inventory.db'

# إنشاء الجداول
from app import db
db.create_all()
```

**PostgreSQL (للإنتاج)**:
```bash
# تثبيت PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# إنشاء قاعدة بيانات
sudo -u postgres createdb inventory_db

# إنشاء مستخدم
sudo -u postgres createuser --interactive
```

```python
# في ملف config.py
DATABASE_URL = 'postgresql://username:password@localhost/inventory_db'
```

### تشغيل النظام في بيئة التطوير

**تشغيل الواجهة الخلفية**:
```bash
cd src
python main.py
# الخادم سيعمل على http://localhost:5000
```

**تشغيل الواجهة الأمامية**:
```bash
cd inventory-frontend
npm run dev
# الخادم سيعمل على http://localhost:5173
```

### النشر في بيئة الإنتاج

**إعداد خادم Linux**:
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت المتطلبات
sudo apt install python3 python3-pip python3-venv nginx postgresql

# إنشاء مستخدم للتطبيق
sudo adduser inventory
sudo usermod -aG sudo inventory
```

**نشر الواجهة الخلفية**:
```bash
# نسخ الملفات
sudo cp -r /path/to/project /opt/inventory-system
sudo chown -R inventory:inventory /opt/inventory-system

# إعداد البيئة الافتراضية
cd /opt/inventory-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# إعداد خدمة systemd
sudo nano /etc/systemd/system/inventory.service
```

**ملف خدمة systemd**:
```ini
[Unit]
Description=Inventory Management System
After=network.target

[Service]
User=inventory
Group=inventory
WorkingDirectory=/opt/inventory-system/src
Environment=PATH=/opt/inventory-system/venv/bin
ExecStart=/opt/inventory-system/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**تفعيل الخدمة**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable inventory
sudo systemctl start inventory
sudo systemctl status inventory
```

**إعداد Nginx**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /opt/inventory-system/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

**بناء ونشر الواجهة الأمامية**:
```bash
cd inventory-frontend
npm run build
sudo cp -r dist/* /opt/inventory-system/frontend/dist/
```

### إعداد HTTPS

**استخدام Let's Encrypt**:
```bash
# تثبيت Certbot
sudo apt install certbot python3-certbot-nginx

# الحصول على شهادة SSL
sudo certbot --nginx -d your-domain.com

# تجديد تلقائي للشهادة
sudo crontab -e
# إضافة السطر التالي:
0 12 * * * /usr/bin/certbot renew --quiet
```

### النسخ الاحتياطي والاستعادة

**نسخ احتياطي لقاعدة البيانات**:
```bash
# PostgreSQL
pg_dump -U username -h localhost inventory_db > backup_$(date +%Y%m%d_%H%M%S).sql

# SQLite
cp inventory.db backup_$(date +%Y%m%d_%H%M%S).db
```

**استعادة قاعدة البيانات**:
```bash
# PostgreSQL
psql -U username -h localhost inventory_db < backup_file.sql

# SQLite
cp backup_file.db inventory.db
```

**نسخ احتياطي للملفات**:
```bash
# إنشاء أرشيف للنظام كاملاً
tar -czf inventory_backup_$(date +%Y%m%d_%H%M%S).tar.gz /opt/inventory-system
```

---

## الصيانة والمراقبة

### مراقبة الأداء

**مراقبة استخدام الموارد**:
```bash
# مراقبة استخدام المعالج والذاكرة
htop

# مراقبة مساحة القرص
df -h

# مراقبة حالة الخدمات
systemctl status inventory
systemctl status nginx
systemctl status postgresql
```

**مراقبة سجلات النظام**:
```bash
# سجلات التطبيق
tail -f /opt/inventory-system/logs/app.log

# سجلات Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# سجلات النظام
journalctl -u inventory -f
```

### الصيانة الدورية

**تنظيف قاعدة البيانات**:
```sql
-- حذف السجلات القديمة (أكثر من سنة)
DELETE FROM stock_movements 
WHERE created_at < DATE('now', '-1 year');

-- إعادة فهرسة الجداول
REINDEX;

-- تحليل الجداول لتحسين الأداء
ANALYZE;
```

**تنظيف الملفات المؤقتة**:
```bash
# حذف ملفات السجلات القديمة
find /opt/inventory-system/logs -name "*.log" -mtime +30 -delete

# حذف النسخ الاحتياطية القديمة
find /opt/backups -name "*.sql" -mtime +90 -delete
```

**تحديث النظام**:
```bash
# تحديث حزم النظام
sudo apt update && sudo apt upgrade -y

# تحديث حزم Python
source /opt/inventory-system/venv/bin/activate
pip list --outdated
pip install --upgrade package_name

# تحديث حزم Node.js
cd /opt/inventory-system/frontend
npm outdated
npm update
```

### النسخ الاحتياطي التلقائي

**سكريبت النسخ الاحتياطي**:
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# إنشاء مجلد النسخ الاحتياطية
mkdir -p $BACKUP_DIR

# نسخ احتياطي لقاعدة البيانات
pg_dump -U inventory_user -h localhost inventory_db > $BACKUP_DIR/db_backup_$DATE.sql

# نسخ احتياطي للملفات
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /opt/inventory-system

# حذف النسخ القديمة (أكثر من 30 يوم)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

**جدولة النسخ الاحتياطي**:
```bash
# إضافة مهمة cron للنسخ الاحتياطي اليومي
sudo crontab -e

# إضافة السطر التالي للنسخ الاحتياطي في الساعة 2:00 صباحاً يومياً
0 2 * * * /opt/inventory-system/scripts/backup.sh
```

### مراقبة الأمان

**مراقبة محاولات الدخول**:
```bash
# مراقبة محاولات تسجيل الدخول الفاشلة
grep "Failed login" /opt/inventory-system/logs/security.log

# مراقبة الأنشطة المشبوهة
grep "Suspicious" /opt/inventory-system/logs/security.log
```

**تحديثات الأمان**:
```bash
# تحديث النظام للحصول على تحديثات الأمان
sudo apt update && sudo apt upgrade -y

# فحص الثغرات الأمنية في حزم Python
pip install safety
safety check

# فحص الثغرات الأمنية في حزم Node.js
npm audit
npm audit fix
```

### استكشاف الأخطاء وإصلاحها

**مشاكل الأداء**:
```bash
# فحص استخدام الموارد
top
iotop
nethogs

# فحص استعلامات قاعدة البيانات البطيئة
# في PostgreSQL
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

**مشاكل الاتصال**:
```bash
# فحص حالة المنافذ
netstat -tlnp | grep :5000
netstat -tlnp | grep :80

# فحص حالة الخدمات
systemctl status inventory
systemctl status nginx
systemctl status postgresql
```

**استعادة النظام**:
```bash
# في حالة تعطل النظام
sudo systemctl restart inventory
sudo systemctl restart nginx

# في حالة تلف قاعدة البيانات
# استعادة من النسخة الاحتياطية
psql -U inventory_user -h localhost inventory_db < /opt/backups/latest_backup.sql
```

---

## الخلاصة التقنية

نظام إدارة المخزون هو حل تقني متكامل ومتطور يجمع بين أحدث التقنيات وأفضل الممارسات في تطوير تطبيقات الويب. النظام مصمم ليكون:

**قابل للتوسع**: معمارية مرنة تسمح بإضافة ميزات جديدة وتوسيع النظام حسب الحاجة

**آمن**: تطبيق شامل لمعايير الأمان مع حماية متعددة الطبقات

**سهل الصيانة**: كود منظم ومُوثق جيداً مع أدوات مراقبة وصيانة شاملة

**عالي الأداء**: تحسينات شاملة للأداء على جميع المستويات

**سهل الاستخدام**: واجهة مستخدم حديثة ومتجاوبة باللغة العربية

هذا التوثيق التقني يوفر دليلاً شاملاً للمطورين والمسؤولين التقنيين لفهم وإدارة وتطوير النظام بكفاءة.

---

**تاريخ آخر تحديث**: 16 يونيو 2025  
**إصدار التوثيق**: 1.0  
**إعداد**: Manus AI

---

