# تصميم هيكل قواعد البيانات المتكاملة لنظام Gaara ERP

## 1. نظرة عامة على التكامل

### 1.1 الهدف من التكامل
الهدف الرئيسي هو إنشاء بنية قواعد بيانات متكاملة تسمح بالتفاعل السلس بين النظام الزراعي الحالي ونظام Gaara ERP الجديد، مع الحفاظ على استقلالية كل نظام وتجنب التكرار غير الضروري للبيانات.

### 1.2 استراتيجية التكامل
سنعتمد استراتيجية "التكامل الهجين" التي تجمع بين:
- **قواعد بيانات منفصلة**: لكل نظام قاعدة بيانات خاصة به
- **طبقة تكامل مركزية**: تدير التزامن والتحديثات بين النظامين
- **جداول مرجعية مشتركة**: للبيانات المشتركة بين النظامين

## 2. هيكل قواعد البيانات

### 2.1 قواعد البيانات الرئيسية
سيتكون النظام من أربع قواعد بيانات رئيسية:

1. **قاعدة بيانات النظام الزراعي (القائمة)**
   - تحتفظ بجميع بيانات النظام الزراعي الحالي
   - تضاف إليها جداول وحقول جديدة للتكامل مع نظام ERP

2. **قاعدة بيانات Gaara ERP الأساسية**
   - تحتوي على جميع بيانات نظام ERP الأساسية
   - تشمل وحدات: الحسابات، المخزون، الموارد البشرية، الشؤون الإدارية، إلخ

3. **قاعدة بيانات التكامل**
   - تحتوي على جداول التزامن والتحويل
   - تخزن سجلات العمليات والأخطاء
   - تدير قواعد التكامل والتحويل

4. **قاعدة بيانات التحليلات والذكاء الاصطناعي**
   - تجمع البيانات من النظامين لأغراض التحليل
   - تخزن نماذج التعلم الآلي ونتائج التحليل
   - تدعم لوحات المعلومات والتقارير المتقدمة

### 2.2 مخطط العلاقات بين قواعد البيانات

```
+---------------------------+        +---------------------------+
|                           |        |                           |
| قاعدة بيانات النظام الزراعي +<-------+ قاعدة بيانات التكامل       |
|                           |        |                           |
+-------------+-------------+        +-------------+-------------+
              ^                                    ^
              |                                    |
              |                                    |
              v                                    v
+-------------+-------------+        +-------------+-------------+
|                           |        |                           |
| قاعدة بيانات Gaara ERP     +<-------+ قاعدة بيانات التحليلات     |
|                           |        |                           |
+---------------------------+        +---------------------------+
```

## 3. آلية التكامل بين النظامين

### 3.1 طبقة التكامل المركزية
ستتكون طبقة التكامل من المكونات التالية:

1. **خدمة التزامن (Synchronization Service)**
   - تدير تزامن البيانات بين النظامين
   - تعمل وفق جدول زمني محدد أو عند الطلب
   - تدعم التزامن ثنائي الاتجاه أو أحادي الاتجاه حسب نوع البيانات

2. **واجهة برمجة التطبيقات للتكامل (Integration API)**
   - توفر نقاط نهاية RESTful للتفاعل بين النظامين
   - تدعم عمليات CRUD للبيانات المشتركة
   - تتضمن آليات المصادقة والتفويض

3. **محرك التحويل (Transformation Engine)**
   - يحول البيانات بين تنسيقات النظامين
   - يطبق قواعد العمل أثناء التحويل
   - يدعم التحويلات المعقدة والبسيطة

4. **نظام المراقبة والتسجيل (Monitoring & Logging)**
   - يراقب عمليات التكامل
   - يسجل الأخطاء والتحذيرات
   - يوفر لوحة تحكم لمراقبة حالة التكامل

### 3.2 استراتيجيات التزامن

سنستخدم استراتيجيات مختلفة للتزامن حسب نوع البيانات:

1. **التزامن الفوري (Real-time Sync)**
   - للبيانات الحرجة مثل المعاملات المالية
   - يستخدم آلية الأحداث (Event-driven)
   - يضمن الاتساق الفوري بين النظامين

2. **التزامن الدوري (Periodic Sync)**
   - للبيانات الأقل حساسية مثل التقارير
   - يعمل وفق جدول زمني محدد
   - يقلل الحمل على النظام

3. **التزامن عند الطلب (On-demand Sync)**
   - للبيانات التي تتطلب تدخل المستخدم
   - يتم تشغيله يدويًا أو عند حدوث أحداث معينة
   - يوفر مرونة في إدارة التزامن

## 4. هيكل الجداول الرئيسية

### 4.1 جداول التكامل الرئيسية

#### 4.1.1 جدول تعيين الكيانات (Entity Mapping)
```sql
CREATE TABLE integration.entity_mapping (
    mapping_id SERIAL PRIMARY KEY,
    agri_entity_type VARCHAR(50) NOT NULL,
    agri_entity_id VARCHAR(50) NOT NULL,
    erp_entity_type VARCHAR(50) NOT NULL,
    erp_entity_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    UNIQUE (agri_entity_type, agri_entity_id, erp_entity_type)
);
```

#### 4.1.2 جدول سجل التزامن (Sync Log)
```sql
CREATE TABLE integration.sync_log (
    log_id SERIAL PRIMARY KEY,
    sync_type VARCHAR(50) NOT NULL,
    source_system VARCHAR(20) NOT NULL,
    target_system VARCHAR(20) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    message TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    user_id INTEGER,
    details JSONB
);
```

#### 4.1.3 جدول قواعد التحويل (Transformation Rules)
```sql
CREATE TABLE integration.transformation_rules (
    rule_id SERIAL PRIMARY KEY,
    source_entity VARCHAR(50) NOT NULL,
    target_entity VARCHAR(50) NOT NULL,
    source_field VARCHAR(50) NOT NULL,
    target_field VARCHAR(50) NOT NULL,
    transformation_type VARCHAR(50) NOT NULL,
    transformation_expression TEXT,
    priority INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);
```

### 4.2 التعديلات على النظام الزراعي الحالي

#### 4.2.1 إضافة حقول التكامل
سنضيف حقول التكامل التالية إلى الجداول الرئيسية في النظام الزراعي:

```sql
-- إضافة حقول التكامل إلى جدول المحاصيل
ALTER TABLE agricultural_system.crops
ADD COLUMN erp_product_id VARCHAR(50),
ADD COLUMN last_sync_at TIMESTAMP,
ADD COLUMN sync_status VARCHAR(20);

-- إضافة حقول التكامل إلى جدول الأمراض
ALTER TABLE agricultural_system.diseases
ADD COLUMN erp_service_id VARCHAR(50),
ADD COLUMN last_sync_at TIMESTAMP,
ADD COLUMN sync_status VARCHAR(20);

-- إضافة حقول التكامل إلى جدول المعالجات
ALTER TABLE agricultural_system.treatments
ADD COLUMN erp_inventory_id VARCHAR(50),
ADD COLUMN last_sync_at TIMESTAMP,
ADD COLUMN sync_status VARCHAR(20);
```

#### 4.2.2 إنشاء مشغلات (Triggers) للتزامن
سننشئ مشغلات في النظام الزراعي لإرسال إشعارات عند تغيير البيانات:

```sql
-- مثال على مشغل لجدول المحاصيل
CREATE OR REPLACE FUNCTION agricultural_system.notify_crop_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO integration.sync_queue (
        entity_type, entity_id, operation, source_system, created_at
    ) VALUES (
        'crop', NEW.id, 
        CASE WHEN TG_OP = 'DELETE' THEN 'DELETE' 
             WHEN TG_OP = 'UPDATE' THEN 'UPDATE' 
             ELSE 'INSERT' END,
        'agricultural_system', NOW()
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER crop_change_trigger
AFTER INSERT OR UPDATE OR DELETE ON agricultural_system.crops
FOR EACH ROW EXECUTE FUNCTION agricultural_system.notify_crop_change();
```

### 4.3 هيكل جداول نظام Gaara ERP الجديد

#### 4.3.1 جداول الحسابات والمالية
```sql
-- جدول الحسابات
CREATE TABLE erp.accounts (
    account_id SERIAL PRIMARY KEY,
    account_code VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    parent_account_id INTEGER REFERENCES erp.accounts(account_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    company_id INTEGER NOT NULL,
    currency_code CHAR(3) NOT NULL,
    opening_balance DECIMAL(18,2) DEFAULT 0,
    current_balance DECIMAL(18,2) DEFAULT 0,
    description TEXT,
    integration_id VARCHAR(50)
);

-- جدول القيود المحاسبية
CREATE TABLE erp.journal_entries (
    entry_id SERIAL PRIMARY KEY,
    entry_number VARCHAR(20) UNIQUE NOT NULL,
    entry_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    reference VARCHAR(100),
    source VARCHAR(50) NOT NULL,
    is_posted BOOLEAN DEFAULT FALSE,
    is_reversed BOOLEAN DEFAULT FALSE,
    reversal_of INTEGER REFERENCES erp.journal_entries(entry_id),
    company_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    notes TEXT,
    total_debit DECIMAL(18,2) DEFAULT 0,
    total_credit DECIMAL(18,2) DEFAULT 0,
    integration_id VARCHAR(50)
);
```

#### 4.3.2 جداول المخزون
```sql
-- جدول المنتجات
CREATE TABLE erp.products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    category_id INTEGER NOT NULL,
    uom_id INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    company_id INTEGER NOT NULL,
    description TEXT,
    barcode VARCHAR(50),
    image_url VARCHAR(255),
    min_stock_level DECIMAL(18,2) DEFAULT 0,
    max_stock_level DECIMAL(18,2) DEFAULT 0,
    reorder_level DECIMAL(18,2) DEFAULT 0,
    cost_price DECIMAL(18,2) DEFAULT 0,
    selling_price DECIMAL(18,2) DEFAULT 0,
    tax_rate DECIMAL(5,2) DEFAULT 0,
    is_agricultural BOOLEAN DEFAULT FALSE,
    agricultural_id VARCHAR(50),
    integration_id VARCHAR(50)
);

-- جدول المستودعات
CREATE TABLE erp.warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    warehouse_code VARCHAR(20) UNIQUE NOT NULL,
    warehouse_name VARCHAR(100) NOT NULL,
    location_id INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    company_id INTEGER NOT NULL,
    address TEXT,
    manager_id INTEGER,
    contact_number VARCHAR(20),
    email VARCHAR(100),
    integration_id VARCHAR(50)
);
```

#### 4.3.3 جداول المشاتل والمزارع
```sql
-- جدول المشاتل
CREATE TABLE erp.nurseries (
    nursery_id SERIAL PRIMARY KEY,
    nursery_code VARCHAR(20) UNIQUE NOT NULL,
    nursery_name VARCHAR(100) NOT NULL,
    location_id INTEGER NOT NULL,
    area DECIMAL(10,2) NOT NULL,
    area_uom VARCHAR(10) DEFAULT 'sqm',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    company_id INTEGER NOT NULL,
    manager_id INTEGER,
    capacity INTEGER,
    description TEXT,
    agricultural_id VARCHAR(50),
    integration_id VARCHAR(50)
);

-- جدول المزارع
CREATE TABLE erp.farms (
    farm_id SERIAL PRIMARY KEY,
    farm_code VARCHAR(20) UNIQUE NOT NULL,
    farm_name VARCHAR(100) NOT NULL,
    location_id INTEGER NOT NULL,
    area DECIMAL(10,2) NOT NULL,
    area_uom VARCHAR(10) DEFAULT 'sqm',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    company_id INTEGER NOT NULL,
    manager_id INTEGER,
    soil_type VARCHAR(50),
    water_source VARCHAR(50),
    description TEXT,
    agricultural_id VARCHAR(50),
    integration_id VARCHAR(50)
);
```

## 5. استراتيجية التنفيذ والترحيل

### 5.1 مراحل التنفيذ

1. **المرحلة الأولى: إعداد البنية التحتية**
   - إنشاء قواعد البيانات الجديدة
   - تعديل قاعدة بيانات النظام الزراعي
   - إعداد بيئة التطوير والاختبار

2. **المرحلة الثانية: تطوير طبقة التكامل**
   - تطوير خدمة التزامن
   - تطوير واجهة برمجة التطبيقات للتكامل
   - تطوير محرك التحويل

3. **المرحلة الثالثة: ترحيل البيانات الأولي**
   - استخراج البيانات من النظام الزراعي
   - تحويل البيانات إلى تنسيق نظام ERP
   - تحميل البيانات في نظام ERP

4. **المرحلة الرابعة: اختبار التكامل**
   - اختبار التزامن ثنائي الاتجاه
   - اختبار سيناريوهات الأخطاء والاسترداد
   - اختبار الأداء والتحمل

5. **المرحلة الخامسة: النشر التدريجي**
   - نشر النظام في بيئة الإنتاج
   - مراقبة التكامل عن كثب
   - التحسين المستمر بناءً على التغذية الراجعة

### 5.2 استراتيجية الترحيل

سنعتمد استراتيجية "الترحيل التدريجي" التي تتضمن:

1. **ترحيل البيانات الأساسية أولاً**
   - بيانات المنتجات والمحاصيل
   - بيانات المشاتل والمزارع
   - بيانات الموردين والعملاء

2. **ترحيل البيانات التاريخية لاحقًا**
   - المعاملات المالية
   - سجلات المخزون
   - سجلات الإنتاج

3. **التشغيل المتوازي للنظامين**
   - تشغيل النظامين جنبًا إلى جنب لفترة انتقالية
   - التحقق من صحة البيانات واتساقها
   - الانتقال التدريجي إلى النظام الجديد

## 6. اعتبارات الأمان والأداء

### 6.1 اعتبارات الأمان

1. **تشفير البيانات**
   - تشفير البيانات الحساسة في قاعدة البيانات
   - تشفير البيانات أثناء النقل بين النظامين
   - إدارة المفاتيح بشكل آمن

2. **التحكم في الوصول**
   - تطبيق مبدأ الامتيازات الأقل
   - التحقق من الهوية متعدد العوامل
   - تسجيل وتدقيق جميع عمليات الوصول

3. **حماية واجهة برمجة التطبيقات**
   - استخدام JWT للمصادقة
   - تطبيق حدود معدل الطلبات
   - التحقق من صحة جميع المدخلات

### 6.2 اعتبارات الأداء

1. **تحسين قاعدة البيانات**
   - إنشاء فهارس مناسبة
   - تقسيم الجداول الكبيرة
   - استخدام التخزين المؤقت للاستعلامات المتكررة

2. **تحسين عمليات التزامن**
   - جدولة عمليات التزامن في أوقات منخفضة الاستخدام
   - تنفيذ التزامن على دفعات
   - استخدام المعالجة المتوازية عند الإمكان

3. **مراقبة الأداء**
   - تتبع أوقات الاستجابة
   - مراقبة استخدام الموارد
   - تحديد وحل اختناقات الأداء

## 7. خطة الاختبار والتحقق

### 7.1 استراتيجية الاختبار

1. **اختبار الوحدات**
   - اختبار كل مكون من مكونات التكامل بشكل منفصل
   - التحقق من صحة عمليات التحويل
   - اختبار معالجة الحالات الاستثنائية

2. **اختبار التكامل**
   - اختبار التفاعل بين مكونات التكامل
   - التحقق من تدفق البيانات بين النظامين
   - اختبار سيناريوهات التزامن المختلفة

3. **اختبار النظام**
   - اختبار النظام بأكمله في بيئة مشابهة للإنتاج
   - التحقق من الأداء والاستقرار
   - اختبار استرداد النظام من الأخطاء

### 7.2 معايير التحقق

1. **اتساق البيانات**
   - التحقق من تطابق البيانات بين النظامين
   - التحقق من صحة التحويلات
   - التحقق من عدم فقدان البيانات

2. **الأداء**
   - قياس أوقات الاستجابة
   - قياس استهلاك الموارد
   - التحقق من قدرة النظام على التعامل مع الحمل المتوقع

3. **الموثوقية**
   - قياس معدل الأخطاء
   - قياس زمن الاسترداد من الأخطاء
   - التحقق من استمرارية العمل في حالة فشل أحد المكونات

## 8. الخلاصة والخطوات التالية

### 8.1 الخلاصة
تم تصميم هيكل قواعد البيانات المتكاملة لنظام Gaara ERP بطريقة تضمن التكامل السلس مع النظام الزراعي الحالي، مع الحفاظ على استقلالية كل نظام وتجنب التكرار غير الضروري للبيانات. يعتمد التصميم على استراتيجية "التكامل الهجين" التي تجمع بين قواعد بيانات منفصلة وطبقة تكامل مركزية وجداول مرجعية مشتركة.

### 8.2 الخطوات التالية

1. **إعداد بيئة التطوير**
   - إنشاء قواعد البيانات
   - إعداد أدوات التطوير
   - إعداد بيئة الاختبار

2. **تطوير النموذج الأولي لطبقة التكامل**
   - تطوير خدمة التزامن الأساسية
   - تطوير واجهة برمجة التطبيقات البسيطة
   - اختبار التكامل الأساسي

3. **تنفيذ التعديلات على النظام الزراعي**
   - إضافة حقول التكامل
   - إنشاء المشغلات
   - اختبار التعديلات

4. **البدء في تطوير نظام Gaara ERP**
   - تطوير البنية الأساسية
   - تطوير الوحدات الأساسية
   - تكامل الوحدات مع طبقة التكامل
