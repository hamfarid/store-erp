# نظام التحقق من صحة النماذج - دليل شامل

## نظرة عامة

يوفر نظام التحقق من صحة النماذج (Form Validation System) مجموعة شاملة من المكونات والأدوات للتحقق من صحة البيانات المدخلة في النماذج مع دعم كامل للغة العربية والاتجاه من اليمين إلى اليسار (RTL).

## المميزات الرئيسية

- ✅ **تحقق في الوقت الفعلي** - التحقق من صحة البيانات أثناء الإدخال
- 📱 **دعم RTL كامل** - واجهة عربية احترافية
- 🎨 **حالات بصرية غنية** - تصاميم احترافية للأخطاء والنجاح
- ♿ **إمكانية الوصول** - متوافق مع معايير WCAG
- 🌙 **دعم الوضع الليلي** - تصاميم مخصصة للوضع الليلي
- 🧩 **مكونات قابلة لإعادة الاستخدام** - مكونات منفصلة وسهلة الاستخدام
- 🎯 **رسائل خطأ مخصصة** - رسائل خطأ واضحة وسهلة الفهم بالعربية

## المكونات المتاحة

### 1. FormField - حقل نصي

حقل إدخال نصي مع التحقق من الصحة والأيقونات البصرية.

```jsx
import { FormField } from '../components/FormValidation';
import { validationRules } from '../utils/validationRules';

<FormField
  label="البريد الإلكتروني"
  name="email"
  type="email"
  value={email}
  onChange={handleChange}
  onBlur={handleBlur}
  error={errors.email}
  touched={touched.email}
  placeholder="example@email.com"
  required
  validators={[
    validationRules.required,
    validationRules.email
  ]}
  hint="استخدم بريد إلكتروني صحيح"
/>
```

**الخصائص:**
- `label` - عنوان الحقل
- `name` - معرّف الحقل (يجب أن يكون فريداً)
- `type` - نوع الحقل (text, email, password, tel, url, date, etc.)
- `value` - القيمة الحالية للحقل
- `onChange` - دالة تُستدعى عند تغيير القيمة
- `onBlur` - دالة تُستدعى عند مغادرة الحقل
- `error` - رسالة الخطأ
- `touched` - هل تم لمس الحقل؟
- `disabled` - تعطيل الحقل
- `placeholder` - نص مساعد
- `required` - هل الحقل مطلوب؟
- `validators` - مصفوفة من دوال التحقق
- `hint` - تلميح للمستخدم
- `className` - فئة CSS مخصصة

### 2. FormSelect - حقل اختيار

حقل اختيار من قائمة مع التحقق من الصحة.

```jsx
<FormSelect
  label="الفئة"
  name="category"
  value={category}
  onChange={handleChange}
  onBlur={handleBlur}
  error={errors.category}
  touched={touched.category}
  options={[
    { value: '', label: 'اختر فئة' },
    { value: 'electronics', label: 'الإلكترونيات' },
    { value: 'clothing', label: 'الملابس' }
  ]}
  required
  validators={[validationRules.required]}
/>
```

### 3. FormTextarea - حقل نصي متعدد الأسطر

حقل نصي متعدد الأسطر مع عداد الأحرف.

```jsx
<FormTextarea
  label="الوصف"
  name="description"
  value={description}
  onChange={handleChange}
  onBlur={handleBlur}
  error={errors.description}
  touched={touched.description}
  placeholder="أدخل وصفاً تفصيلياً..."
  maxLength={500}
  rows={5}
  validators={[validationRules.minLength(10)]}
/>
```

### 4. FormCheckbox - مربع الاختيار

مربع اختيار واحد مع التحقق من الصحة.

```jsx
<FormCheckbox
  label="أوافق على الشروط والأحكام"
  name="acceptTerms"
  checked={acceptTerms}
  onChange={handleChange}
  error={errors.acceptTerms}
  touched={touched.acceptTerms}
  required
/>
```

### 5. FormRadio - أزرار الاختيار

مجموعة من أزرار الاختيار.

```jsx
<FormRadio
  label="نوع المستخدم"
  name="userType"
  value={userType}
  onChange={handleChange}
  options={[
    { value: 'customer', label: 'عميل' },
    { value: 'vendor', label: 'بائع' },
    { value: 'admin', label: 'مسؤول' }
  ]}
  required
/>
```

### 6. FormContainer - حاوية النموذج

حاوية لتجميع جميع حقول النموذج.

```jsx
<FormContainer onSubmit={handleSubmit}>
  {/* جميع حقول النموذج هنا */}
</FormContainer>
```

## قواعد التحقق

### قواعد التحقق المدمجة

```javascript
import { validationRules } from '../utils/validationRules';

// مطلوب
validationRules.required(value)

// بريد إلكتروني
validationRules.email(value)

// رقم جوال (صيغة سعودية)
validationRules.phone(value)

// كلمة مرور قوية
validationRules.password(value)

// رقم
validationRules.number(value)

// رقم موجب
validationRules.positiveNumber(value)

// رابط ويب
validationRules.url(value)

// تاريخ صحيح
validationRules.date(value)

// الحد الأدنى للطول
validationRules.minLength(10)(value)

// الحد الأقصى للطول
validationRules.maxLength(50)(value)

// القيمة الدنيا
validationRules.min(0)(value)

// القيمة العليا
validationRules.max(100)(value)

// نطاق القيم
validationRules.range(0, 100)(value)

// اسم مستخدم
validationRules.username(value)

// تطابق قيمتين
validationRules.match(passwordValue)(confirmPassword)

// تعبير نمطي مخصص
validationRules.pattern(/^\d{10}$/, 'يجب أن يكون الرقم 10 أرقام')(value)
```

## مثال شامل

```jsx
import React, { useState } from 'react';
import {
  FormField,
  FormSelect,
  FormCheckbox,
  FormContainer
} from '../components/FormValidation';
import { validationRules } from '../utils/validationRules';

function MyForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    category: '',
    acceptTerms: false
  });

  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Mark all as touched
    const newTouched = {};
    Object.keys(formData).forEach(key => {
      newTouched[key] = true;
    });
    setTouched(newTouched);

    // Validate
    const newErrors = {};
    
    const emailCheck = validationRules.required(formData.email);
    if (emailCheck !== true) {
      newErrors.email = emailCheck;
    } else {
      const emailFormat = validationRules.email(formData.email);
      if (emailFormat !== true) {
        newErrors.email = emailFormat;
      }
    }

    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      console.log('النموذج صحيح:', formData);
      // أرسل البيانات إلى الخادم
    }
  };

  return (
    <FormContainer onSubmit={handleSubmit}>
      <FormField
        label="البريد الإلكتروني"
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.email}
        touched={touched.email}
        required
        validators={[
          validationRules.required,
          validationRules.email
        ]}
      />

      <FormField
        label="كلمة المرور"
        name="password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        onBlur={handleBlur}
        error={errors.password}
        touched={touched.password}
        required
        validators={[
          validationRules.required,
          validationRules.password
        ]}
      />

      <FormSelect
        label="الفئة"
        name="category"
        value={formData.category}
        onChange={handleChange}
        error={errors.category}
        touched={touched.category}
        options={[
          { value: '', label: 'اختر فئة' },
          { value: 'a', label: 'فئة أ' }
        ]}
        required
      />

      <FormCheckbox
        label="أوافق على الشروط"
        name="acceptTerms"
        checked={formData.acceptTerms}
        onChange={handleChange}
        error={errors.acceptTerms}
        touched={touched.acceptTerms}
        required
      />

      <button type="submit">إرسال</button>
    </FormContainer>
  );
}

export default MyForm;
```

## رسائل الخطأ

جميع رسائل الخطأ مترجمة للعربية:

| المدقق | الرسالة |
|--------|---------|
| required | هذا الحقل مطلوب |
| email | يرجى إدخال بريد إلكتروني صحيح |
| phone | يرجى إدخال رقم جوال صحيح |
| password | كلمة المرور يجب أن تكون 8 أحرف على الأقل (وغيرها) |
| number | يجب إدخال رقم صحيح |
| positiveNumber | يجب إدخال رقم موجب |
| url | يرجى إدخال عنوان URL صحيح |
| date | يرجى إدخال تاريخ صحيح |
| minLength | يجب أن يكون الطول {min} أحرف على الأقل |
| maxLength | يجب ألا يتجاوز الطول {max} أحرف |
| min | يجب أن تكون القيمة {min} على الأقل |
| max | يجب ألا تتجاوز القيمة {max} |
| range | يجب أن تكون القيمة بين {min} و {max} |
| username | اسم المستخدم يجب أن يكون بين 3-20 حرف وأرقام وشرطة سفلية فقط |

## أنماط CSS

يتم تطبيق أنماط CSS تلقائياً على الحقول بناءً على الحالة:

- `.form-input` - نمط الحقل الافتراضي
- `.form-input.input-valid` - حقل صحيح (أخضر)
- `.form-input.input-invalid` - حقل غير صحيح (أحمر)
- `.form-input:disabled` - حقل معطل
- `.form-error` - رسالة خطأ
- `.form-success` - رسالة نجاح
- `.form-hint` - تلميح

## إمكانية الوصول

جميع المكونات متوافقة مع معايير WCAG:

- دعم قارئات الشاشة
- تسميات مرتبطة بشكل صحيح
- أدوار ARIA صحيحة
- رسائل الخطأ معلنة بشكل صحيح
- الملاحة باستخدام لوحة المفاتيح

## الاستخدام المتقدم

### إنشاء مدقق مخصص

```javascript
const customValidator = (value) => {
  // يجب أن تعيد true إذا كانت القيمة صحيحة
  // أو رسالة خطأ بالعربية إذا كانت غير صحيحة
  if (/* شرطك هنا */) {
    return true;
  }
  return 'رسالة الخطأ المخصصة';
};

// الاستخدام
validators={[customValidator]}
```

### التحقق الديناميكي

```javascript
const validateAge = (age) => {
  const numAge = parseInt(age);
  if (numAge < 18) return 'يجب أن تكون 18 سنة فأكثر';
  return true;
};

<FormField
  validators={[validationRules.required, validateAge]}
/>
```

### تطابق الحقول

```javascript
// التحقق من تطابق كلمات المرور
const confirmPasswordValidator = (value) => {
  if (value !== formData.password) {
    return 'كلمات المرور غير متطابقة';
  }
  return true;
};

<FormField
  label="تأكيد كلمة المرور"
  name="confirmPassword"
  type="password"
  validators={[
    validationRules.required,
    confirmPasswordValidator
  ]}
/>
```

## الأداء

- التحقق في الوقت الفعلي بدون تأخير
- استخدام `useCallback` لمنع إعادة العرض غير الضرورية
- دعم التحقق غير المتزامن (قريباً)

## الدعم والتوافقية

- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari
- ✅ الهواتف الذكية (iOS/Android)
- ✅ الأجهزة اللوحية

## الملفات المتعلقة

- `frontend/src/components/FormValidation.jsx` - مكونات النماذج
- `frontend/src/components/FormValidationExample.jsx` - مثال شامل
- `frontend/src/utils/validationRules.js` - قواعد التحقق
- `frontend/src/styles/FormValidation.css` - الأنماط

## المزيد من المساعدة

انظر `FormValidationExample.jsx` لمثال شامل يغطي جميع الحالات الممكنة.
