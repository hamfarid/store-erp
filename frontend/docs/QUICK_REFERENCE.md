# Form Validation System - Quick Reference Guide

> **Note:** This is a documentation file with code examples. For actual implementation patterns, see the examples in this guide.

## Table of Contents

1. [Imports](#imports)
2. [Component Examples](#component-examples)
3. [Form State Setup](#form-state-setup)
4. [Event Handlers](#event-handlers)
5. [Validation Rules](#validation-rules)
6. [Custom Validators](#custom-validators)
7. [CSS Classes](#css-classes)
8. [Performance Tips](#performance-tips)
9. [Error Messages](#error-messages)
10. [Pre-Submission Checklist](#pre-submission-checklist)

---

## Imports

```javascript
import React, { useState } from 'react';
import {
  FormField,
  FormSelect,
  FormTextarea,
  FormCheckbox,
  FormRadio,
  FormContainer
} from '@/components/FormValidation';
import { validationRules } from '@/utils/validationRules';
```

---

## Component Examples

### FormField

```jsx
<FormField
  label="البريد الإلكتروني"
  name="email"
  type="email"
  value={formData.email}
  onChange={handleChange}
  onBlur={handleBlur}
  error={errors.email}
  touched={touched.email}
  placeholder="example@email.com"
  required
  validators={[validationRules.required, validationRules.email]}
  hint="استخدم بريد إلكتروني صحيح"
/>
```

### FormSelect

```jsx
<FormSelect
  label="الفئة"
  name="category"
  value={formData.category}
  onChange={handleChange}
  error={errors.category}
  touched={touched.category}
  options={[
    { value: '', label: 'اختر فئة' },
    { value: 'cat1', label: 'الفئة الأولى' }
  ]}
  required
/>
```

### FormTextarea

```jsx
<FormTextarea
  label="الوصف"
  name="description"
  value={formData.description}
  onChange={handleChange}
  placeholder="أدخل الوصف..."
  maxLength={500}
  rows={5}
  validators={[validationRules.minLength(10)]}
/>
```

### FormCheckbox

```jsx
<FormCheckbox
  label="أوافق على الشروط"
  name="acceptTerms"
  checked={formData.acceptTerms}
  onChange={handleCheckboxChange}
  error={errors.acceptTerms}
  touched={touched.acceptTerms}
  required
/>
```

### FormRadio

```jsx
<FormRadio
  label="نوع المستخدم"
  name="userType"
  value={formData.userType}
  onChange={handleChange}
  options={[
    { value: 'customer', label: 'عميل' },
    { value: 'vendor', label: 'بائع' }
  ]}
  required
/>
```

---

## Form State Setup

```javascript
const [formData, setFormData] = useState({
  email: '',
  password: '',
  phone: '',
  category: '',
  description: '',
  acceptTerms: false
});

const [touched, setTouched] = useState({});
const [errors, setErrors] = useState({});
```

---

## Event Handlers

```javascript
const handleChange = (e) => {
  const { name, value } = e.target;
  setFormData(prev => ({ ...prev, [name]: value }));
  
  if (errors[name]) {
    setErrors(prev => ({ ...prev, [name]: '' }));
  }
};

const handleBlur = (e) => {
  const { name } = e.target;
  setTouched(prev => ({ ...prev, [name]: true }));
};

const handleCheckboxChange = (e) => {
  const { name, value } = e.target;
  setFormData(prev => ({ ...prev, [name]: value }));
};

const handleSubmit = async (e) => {
  e.preventDefault();
  
  // Mark all fields as touched
  const newTouched = {};
  Object.keys(formData).forEach(key => {
    newTouched[key] = true;
  });
  setTouched(newTouched);
  
  // Validate all fields
  const newErrors = {};
  
  if (Object.keys(newErrors).length === 0) {
    try {
      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        console.log('تم الإرسال بنجاح');
        setFormData({});
        setTouched({});
        setErrors({});
      }
    } catch (error) {
      console.error('خطأ:', error);
    }
  }
};
```

---

## Validation Rules

| Rule | Example | Description |
|------|---------|-------------|
| required | `validationRules.required(value)` | Field is required |
| email | `validationRules.email(value)` | Valid email format |
| phone | `validationRules.phone(value)` | Valid phone number |
| password | `validationRules.password(value)` | Strong password |
| number | `validationRules.number(value)` | Valid number |
| positiveNumber | `validationRules.positiveNumber(value)` | Positive number only |
| url | `validationRules.url(value)` | Valid URL |
| date | `validationRules.date(value)` | Valid date |
| minLength(n) | `validationRules.minLength(8)(value)` | Minimum length |
| maxLength(n) | `validationRules.maxLength(50)(value)` | Maximum length |
| min(n) | `validationRules.min(0)(value)` | Minimum value |
| max(n) | `validationRules.max(100)(value)` | Maximum value |
| range(min,max) | `validationRules.range(0,100)(value)` | Range validation |
| username | `validationRules.username(value)` | Valid username |
| match(val) | `validationRules.match(pwd)(cpwd)` | Match two values |
| pattern(regex, msg) | `validationRules.pattern(/.../, 'msg')` | Regex pattern |

---

## Custom Validators

```javascript
// Age validator
const validateAge = (age) => {
  const numAge = parseInt(age);
  if (isNaN(numAge) || numAge < 18) {
    return 'يجب أن تكون 18 سنة فأكثر';
  }
  return true;
};

// Password match validator
const validatePasswordMatch = (confirmPassword) => {
  if (confirmPassword !== formData.password) {
    return 'كلمات المرور غير متطابقة';
  }
  return true;
};

// Usage:
// validators={[validationRules.required, validateAge]}
```

---

## CSS Classes

```css
.form-container       /* Form container */
.form-group           /* Field group */
.form-label           /* Field label */
.form-field-wrapper   /* Field wrapper */
.form-input           /* Text input */
.form-input.input-valid    /* Valid input */
.form-input.input-invalid  /* Invalid input */
.form-input:disabled  /* Disabled input */
.form-select          /* Select field */
.form-textarea        /* Textarea field */
.form-checkbox        /* Checkbox field */
.form-radio           /* Radio field */
.form-error           /* Error message */
.form-error-icon      /* Error icon */
.form-success         /* Success message */
.form-success-icon    /* Success icon */
.form-warning         /* Warning message */
.form-hint            /* Hint text */
.required-indicator   /* Required indicator */
```

---

## Performance Tips

1. **Use useCallback for complex functions:**

```javascript
const handleChange = useCallback((e) => {
  // Handle change
}, [dependencies]);
```

2. **Separate touched and errors state:**
   - `touched`: Tracks which fields have been interacted with
   - `errors`: Tracks validation error messages

3. **Avoid unnecessary validation:**
   - Validate only when needed
   - Clear errors when field changes

4. **Use async validation for heavy checks:**
   - Check username availability
   - Check if email is registered

## Error Messages

### Required Field

> "هذا الحقل مطلوب"

### Invalid Email

> "يرجى إدخال بريد إلكتروني صحيح"

### Invalid Phone

> "يرجى إدخال رقم جوال صحيح"

### Weak Password

- "كلمة المرور يجب أن تكون 8 أحرف على الأقل"
- "يجب أن تحتوي على حرف كبير واحد على الأقل"
- "يجب أن تحتوي على حرف صغير واحد على الأقل"
- "يجب أن تحتوي على رقم واحد على الأقل"

### Min/Max Length

- Min: "يجب أن يكون الطول 10 أحرف على الأقل"
- Max: "يجب ألا يتجاوز الطول 50 أحرف"

---

## Pre-Submission Checklist

- [ ] All required fields are marked with `required={true}`
- [ ] All fields have initial values in formData
- [ ] All fields have setState/setErrors
- [ ] Event handlers are properly connected
- [ ] Validation works on blur and change
- [ ] Error messages are in Arabic and clear
- [ ] Visual icons are displayed correctly
- [ ] Button is disabled during submission
- [ ] Success/failure message is displayed
- [ ] Form returns to initial state after submission

---

**Last Updated:** November 10, 2025  
**Version:** 2.0 (Cleaned & Documentation Format)
