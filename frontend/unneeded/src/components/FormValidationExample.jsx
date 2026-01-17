import React, { useState } from 'react';
import {
  FormField,
  FormSelect,
  FormTextarea,
  FormCheckbox,
  FormRadio,
  FormContainer,
} from './FormValidation';
import { validationRules } from '../utils/validationRules';

/**
 * FormValidationExample Component
 * Demonstrates all form validation features and usage patterns
 */
const FormValidationExample = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    phone: '',
    username: '',
    category: '',
    description: '',
    acceptTerms: false,
    userType: 'customer',
  });

  const [touched, setTouched] = useState({});
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear error on change
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched((prev) => ({
      ...prev,
      [name]: true,
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Mark all fields as touched
    const newTouched = {};
    Object.keys(formData).forEach((key) => {
      newTouched[key] = true;
    });
    setTouched(newTouched);

    // Validate all fields
    const newErrors = {};

    // Email validation
    const emailValidation = validationRules.required(formData.email);
    if (emailValidation !== true) {
      newErrors.email = emailValidation;
    } else {
      const emailFormatValidation = validationRules.email(formData.email);
      if (emailFormatValidation !== true) {
        newErrors.email = emailFormatValidation;
      }
    }

    // Password validation
    const passwordValidation = validationRules.required(formData.password);
    if (passwordValidation !== true) {
      newErrors.password = passwordValidation;
    } else {
      const passwordStrengthValidation = validationRules.password(formData.password);
      if (passwordStrengthValidation !== true) {
        newErrors.password = passwordStrengthValidation;
      }
    }

    // Phone validation
    const phoneValidation = validationRules.phone(formData.phone);
    if (phoneValidation !== true) {
      newErrors.phone = phoneValidation;
    }

    // Username validation
    const usernameValidation = validationRules.required(formData.username);
    if (usernameValidation !== true) {
      newErrors.username = usernameValidation;
    } else {
      const usernameLengthValidation = validationRules.minLength(3)(formData.username);
      if (usernameLengthValidation !== true) {
        newErrors.username = usernameLengthValidation;
      }
    }

    // Category validation
    if (!formData.category) {
      newErrors.category = 'يرجى اختيار فئة';
    }

    // Description validation
    const descriptionValidation = validationRules.minLength(10)(formData.description);
    if (descriptionValidation !== true) {
      newErrors.description = descriptionValidation;
    }

    // Terms validation
    if (!formData.acceptTerms) {
      newErrors.acceptTerms = 'يجب قبول الشروط والأحكام';
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      console.log('Form submitted successfully:', formData);
      // Handle form submission
    }
  };

  const categoryOptions = [
    { value: '', label: 'اختر فئة' },
    { value: 'electronics', label: 'الإلكترونيات' },
    { value: 'clothing', label: 'الملابس' },
    { value: 'books', label: 'الكتب' },
    { value: 'furniture', label: 'الأثاث' },
    { value: 'other', label: 'أخرى' },
  ];

  const userTypeOptions = [
    { value: 'customer', label: 'عميل' },
    { value: 'vendor', label: 'بائع' },
    { value: 'admin', label: 'مسؤول' },
  ];

  return (
    <div className="form-example-container" style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h1>نموذج المثال - التحقق من الصحة</h1>

      <FormContainer onSubmit={handleSubmit}>
        {/* Email Field */}
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
          validators={[
            validationRules.required,
            validationRules.email,
          ]}
          hint="استخدم بريد إلكتروني صحيح"
        />

        {/* Username Field */}
        <FormField
          label="اسم المستخدم"
          name="username"
          type="text"
          value={formData.username}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.username}
          touched={touched.username}
          placeholder="username_123"
          required
          validators={[
            validationRules.required,
            validationRules.username,
          ]}
          hint="من 3-20 حرف أو أرقام"
        />

        {/* Phone Field */}
        <FormField
          label="رقم الجوال"
          name="phone"
          type="tel"
          value={formData.phone}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.phone}
          touched={touched.phone}
          placeholder="0501234567"
          validators={[validationRules.phone]}
          hint="صيغة سعودية: 05xxxxxxxx أو +96650xxxxxxxx"
        />

        {/* Password Field */}
        <FormField
          label="كلمة المرور"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.password}
          touched={touched.password}
          placeholder="••••••••"
          required
          validators={[
            validationRules.required,
            validationRules.password,
          ]}
          hint="8 أحرف، حروف كبيرة وصغيرة وأرقام"
        />

        {/* Category Select */}
        <FormSelect
          label="الفئة"
          name="category"
          value={formData.category}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.category}
          touched={touched.category}
          options={categoryOptions}
          required
          validators={[validationRules.required]}
        />

        {/* Description Textarea */}
        <FormTextarea
          label="الوصف"
          name="description"
          value={formData.description}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.description}
          touched={touched.description}
          placeholder="أدخل وصفاً تفصيلياً..."
          maxLength={500}
          rows={5}
          validators={[validationRules.minLength(10)]}
        />

        {/* User Type Radio */}
        <FormRadio
          label="نوع المستخدم"
          name="userType"
          value={formData.userType}
          onChange={handleChange}
          options={userTypeOptions}
          required
        />

        {/* Accept Terms Checkbox */}
        <FormCheckbox
          label="أوافق على الشروط والأحكام"
          name="acceptTerms"
          checked={formData.acceptTerms}
          onChange={handleCheckboxChange}
          error={errors.acceptTerms}
          touched={touched.acceptTerms}
          required
        />

        {/* Submit Button */}
        <button
          type="submit"
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: '#80AA45',
            color: '#ffffff',
            border: 'none',
            borderRadius: '6px',
            fontSize: '16px',
            fontWeight: '500',
            cursor: 'pointer',
            marginTop: '20px',
            transition: 'background-color 0.2s ease-in-out',
          }}
        >
          إرسال النموذج
        </button>
      </FormContainer>

      {/* Form Data Preview */}
      <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#f3f4f6', borderRadius: '6px' }}>
        <h3>معلومات النموذج الحالية:</h3>
        <pre style={{ direction: 'rtl', textAlign: 'left', fontSize: '12px' }}>
          {JSON.stringify(formData, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default FormValidationExample;
