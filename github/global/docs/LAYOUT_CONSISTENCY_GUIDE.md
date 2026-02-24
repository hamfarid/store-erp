# دليل التنسيق الموحد للصفحات
# Layout Consistency Guide

## نظرة عامة

تم إنشاء ملف `layout-consistency.css` لضمان تنسيق موحد عبر جميع صفحات التطبيق. هذا الملف يوفر أنماط CSS قياسية للعناصر المشتركة.

## الملفات المضافة

- `frontend/src/styles/layout-consistency.css` - ملف الأنماط الموحدة
- تم إضافته تلقائياً إلى `frontend/src/index.css`

## الاستخدام

### 1. حاوية الصفحة (Page Container)

```jsx
<div className="page-container">
  {/* محتوى الصفحة */}
</div>
```

**الميزات:**
- عرض كامل مع padding مناسب
- responsive تلقائياً
- max-width محدد للشاشات الكبيرة

### 2. رأس الصفحة (Page Header)

```jsx
<div className="page-header">
  <h1 className="page-title">عنوان الصفحة</h1>
  <div className="page-actions">
    <button>إجراء</button>
  </div>
</div>
```

**الميزات:**
- تخطيط مرن مع flexbox
- responsive تلقائياً
- دعم RTL

### 3. البطاقات (Cards)

```jsx
<div className="card-standard">
  <div className="card-header">
    <h2 className="card-title">عنوان البطاقة</h2>
  </div>
  <div className="card-content">
    {/* محتوى البطاقة */}
  </div>
</div>
```

**الميزات:**
- تصميم موحد
- دعم الوضع الداكن
- ظلال وحدود متناسقة

### 4. الجداول (Tables)

```jsx
<div className="table-wrapper">
  <table className="table-standard">
    <thead>
      <tr>
        <th>العمود 1</th>
        <th>العمود 2</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>بيانات 1</td>
        <td>بيانات 2</td>
      </tr>
    </tbody>
  </table>
</div>
```

**الميزات:**
- scroll أفقي تلقائي للجداول الكبيرة
- hover effects
- دعم RTL
- responsive

### 5. النماذج (Forms)

```jsx
<div className="form-container">
  <div className="form-grid form-grid-2">
    <div className="form-group">
      <label className="form-label">التسمية</label>
      <input className="form-input-standard" type="text" />
    </div>
  </div>
</div>
```

**الميزات:**
- تخطيط grid مرن
- دعم RTL
- focus states محسّنة

### 6. مجموعات الأزرار (Button Groups)

```jsx
<div className="button-group button-group-right">
  <button>زر 1</button>
  <button>زر 2</button>
</div>
```

**الخيارات:**
- `button-group-right` - محاذاة لليمين (RTL: يسار)
- `button-group-left` - محاذاة لليسار (RTL: يمين)
- `button-group-center` - محاذاة للوسط
- `button-group-space-between` - توزيع المسافات

### 7. شريط البحث والتصفية (Search & Filter Bar)

```jsx
<div className="search-filter-bar">
  <input className="search-input" placeholder="بحث..." />
  <select className="filter-select">
    <option>خيار</option>
  </select>
  <div className="action-buttons">
    <button>إجراء</button>
  </div>
</div>
```

**الميزات:**
- تخطيط مرن
- responsive تلقائياً
- دعم RTL

### 8. بطاقات الإحصائيات (Stats Cards)

```jsx
<div className="stats-grid">
  <div className="stats-card">
    <div className="stats-card-header">
      <span className="stats-card-title">العنوان</span>
    </div>
    <div className="stats-card-value">القيمة</div>
    <div className="stats-card-footer">
      {/* معلومات إضافية */}
    </div>
  </div>
</div>
```

**الميزات:**
- grid responsive تلقائياً
- hover effects
- دعم الوضع الداكن

### 9. الحالة الفارغة (Empty State)

```jsx
<div className="empty-state">
  <div className="empty-state-icon">
    <Icon />
  </div>
  <h3 className="empty-state-title">لا توجد بيانات</h3>
  <p className="empty-state-description">الوصف</p>
</div>
```

### 10. حالة التحميل (Loading State)

```jsx
<div className="loading-container">
  <div className="loading-spinner"></div>
  <p className="loading-text">جاري التحميل...</p>
</div>
```

## Grid Layouts

### Grid Container

```jsx
<div className="grid-container grid-3">
  {/* 3 أعمدة على الشاشات الكبيرة */}
</div>
```

**الخيارات:**
- `grid-1` - عمود واحد
- `grid-2` - عمودان
- `grid-3` - ثلاثة أعمدة
- `grid-4` - أربعة أعمدة

**Responsive:**
- تلقائياً يتحول إلى عمود واحد على الشاشات الصغيرة
- عمودان على الشاشات المتوسطة

## RTL Support

جميع الأنماط تدعم RTL تلقائياً:

```jsx
<div dir="rtl" className="page-container">
  {/* المحتوى */}
</div>
```

## Dark Mode Support

جميع الأنماط تدعم الوضع الداكن تلقائياً:

```jsx
<div className="dark">
  <div className="card-standard">
    {/* المحتوى */}
  </div>
</div>
```

## Best Practices

1. **استخدم الحاويات القياسية:**
   - استخدم `page-container` لكل صفحة
   - استخدم `card-standard` للبطاقات

2. **التخطيط المتسق:**
   - استخدم `page-header` لرأس الصفحة
   - استخدم `button-group` لمجموعات الأزرار

3. **الجداول:**
   - دائماً استخدم `table-wrapper` حول الجداول
   - استخدم `table-standard` للجداول

4. **Responsive:**
   - جميع الأنماط responsive تلقائياً
   - لا حاجة لإضافة media queries إضافية

5. **RTL:**
   - أضف `dir="rtl"` للعنصر الرئيسي
   - الأنماط ستعمل تلقائياً

## أمثلة كاملة

### صفحة منتجات

```jsx
<div className="page-container" dir="rtl">
  <div className="page-header">
    <h1 className="page-title">المنتجات</h1>
    <div className="page-actions">
      <button>إضافة منتج</button>
    </div>
  </div>
  
  <div className="search-filter-bar">
    <input className="search-input" placeholder="بحث..." />
    <select className="filter-select">
      <option>جميع الفئات</option>
    </select>
  </div>
  
  <div className="table-wrapper">
    <table className="table-standard">
      {/* جدول المنتجات */}
    </table>
  </div>
</div>
```

### صفحة إحصائيات

```jsx
<div className="page-container" dir="rtl">
  <div className="page-header">
    <h1 className="page-title">لوحة المعلومات</h1>
  </div>
  
  <div className="stats-grid">
    <div className="stats-card">
      <div className="stats-card-header">
        <span className="stats-card-title">إجمالي المبيعات</span>
      </div>
      <div className="stats-card-value">50,000 ج.م</div>
    </div>
    {/* بطاقات أخرى */}
  </div>
</div>
```

## التحديثات المستقبلية

- إضافة المزيد من الأنماط الموحدة
- تحسين الأداء
- إضافة المزيد من الأمثلة

## الدعم

للمساعدة أو الإبلاغ عن مشاكل، يرجى فتح issue في المستودع.

