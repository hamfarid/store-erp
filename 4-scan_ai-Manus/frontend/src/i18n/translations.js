/**
 * Internationalization (i18n) Translations
 * =========================================
 * 
 * Complete Arabic and English translations for Gaara Scan AI.
 * Supports bilingual interface with RTL/LTR automatic switching.
 * 
 * Usage:
 *   import { useTranslation } from './i18n/translations';
 *   const { t, language } = useTranslation();
 *   <h1>{t('dashboard.title')}</h1>
 * 
 * @author Global System v35.0
 * @date 2026-01-17
 */

// ============================================
// Translation Data
// ============================================

export const translations = {
  // ----------------------------------------
  // Common / Shared
  // ----------------------------------------
  common: {
    appName: {
      ar: 'جارا سكان',
      en: 'Gaara Scan AI'
    },
    loading: {
      ar: 'جاري التحميل...',
      en: 'Loading...'
    },
    save: {
      ar: 'حفظ',
      en: 'Save'
    },
    cancel: {
      ar: 'إلغاء',
      en: 'Cancel'
    },
    delete: {
      ar: 'حذف',
      en: 'Delete'
    },
    edit: {
      ar: 'تعديل',
      en: 'Edit'
    },
    add: {
      ar: 'إضافة',
      en: 'Add'
    },
    search: {
      ar: 'بحث',
      en: 'Search'
    },
    filter: {
      ar: 'تصفية',
      en: 'Filter'
    },
    export: {
      ar: 'تصدير',
      en: 'Export'
    },
    import: {
      ar: 'استيراد',
      en: 'Import'
    },
    refresh: {
      ar: 'تحديث',
      en: 'Refresh'
    },
    close: {
      ar: 'إغلاق',
      en: 'Close'
    },
    confirm: {
      ar: 'تأكيد',
      en: 'Confirm'
    },
    yes: {
      ar: 'نعم',
      en: 'Yes'
    },
    no: {
      ar: 'لا',
      en: 'No'
    },
    back: {
      ar: 'رجوع',
      en: 'Back'
    },
    next: {
      ar: 'التالي',
      en: 'Next'
    },
    previous: {
      ar: 'السابق',
      en: 'Previous'
    },
    submit: {
      ar: 'إرسال',
      en: 'Submit'
    },
    reset: {
      ar: 'إعادة تعيين',
      en: 'Reset'
    },
    actions: {
      ar: 'إجراءات',
      en: 'Actions'
    },
    status: {
      ar: 'الحالة',
      en: 'Status'
    },
    date: {
      ar: 'التاريخ',
      en: 'Date'
    },
    time: {
      ar: 'الوقت',
      en: 'Time'
    },
    name: {
      ar: 'الاسم',
      en: 'Name'
    },
    description: {
      ar: 'الوصف',
      en: 'Description'
    },
    type: {
      ar: 'النوع',
      en: 'Type'
    },
    all: {
      ar: 'الكل',
      en: 'All'
    },
    none: {
      ar: 'لا شيء',
      en: 'None'
    },
    noData: {
      ar: 'لا توجد بيانات',
      en: 'No data available'
    },
    error: {
      ar: 'خطأ',
      en: 'Error'
    },
    success: {
      ar: 'نجاح',
      en: 'Success'
    },
    warning: {
      ar: 'تحذير',
      en: 'Warning'
    },
    info: {
      ar: 'معلومات',
      en: 'Info'
    }
  },

  // ----------------------------------------
  // Navigation
  // ----------------------------------------
  nav: {
    dashboard: {
      ar: 'لوحة التحكم',
      en: 'Dashboard'
    },
    diagnosis: {
      ar: 'التشخيص',
      en: 'Diagnosis'
    },
    diseases: {
      ar: 'الأمراض',
      en: 'Diseases'
    },
    farms: {
      ar: 'المزارع',
      en: 'Farms'
    },
    crops: {
      ar: 'المحاصيل',
      en: 'Crops'
    },
    equipment: {
      ar: 'المعدات',
      en: 'Equipment'
    },
    inventory: {
      ar: 'المخزون',
      en: 'Inventory'
    },
    workers: {
      ar: 'العمال',
      en: 'Workers'
    },
    reports: {
      ar: 'التقارير',
      en: 'Reports'
    },
    analytics: {
      ar: 'التحليلات',
      en: 'Analytics'
    },
    settings: {
      ar: 'الإعدادات',
      en: 'Settings'
    },
    profile: {
      ar: 'الملف الشخصي',
      en: 'Profile'
    },
    users: {
      ar: 'المستخدمون',
      en: 'Users'
    },
    mlDashboard: {
      ar: 'لوحة التعلم الآلي',
      en: 'ML Dashboard'
    },
    imageCrawler: {
      ar: 'جامع الصور',
      en: 'Image Crawler'
    }
  },

  // ----------------------------------------
  // Authentication
  // ----------------------------------------
  auth: {
    login: {
      ar: 'تسجيل الدخول',
      en: 'Login'
    },
    logout: {
      ar: 'تسجيل الخروج',
      en: 'Logout'
    },
    register: {
      ar: 'إنشاء حساب',
      en: 'Register'
    },
    forgotPassword: {
      ar: 'نسيت كلمة المرور؟',
      en: 'Forgot Password?'
    },
    resetPassword: {
      ar: 'إعادة تعيين كلمة المرور',
      en: 'Reset Password'
    },
    changePassword: {
      ar: 'تغيير كلمة المرور',
      en: 'Change Password'
    },
    email: {
      ar: 'البريد الإلكتروني',
      en: 'Email'
    },
    password: {
      ar: 'كلمة المرور',
      en: 'Password'
    },
    confirmPassword: {
      ar: 'تأكيد كلمة المرور',
      en: 'Confirm Password'
    },
    currentPassword: {
      ar: 'كلمة المرور الحالية',
      en: 'Current Password'
    },
    newPassword: {
      ar: 'كلمة المرور الجديدة',
      en: 'New Password'
    },
    rememberMe: {
      ar: 'تذكرني',
      en: 'Remember Me'
    },
    loginSuccess: {
      ar: 'تم تسجيل الدخول بنجاح',
      en: 'Login successful'
    },
    logoutSuccess: {
      ar: 'تم تسجيل الخروج بنجاح',
      en: 'Logged out successfully'
    },
    invalidCredentials: {
      ar: 'بيانات الاعتماد غير صحيحة',
      en: 'Invalid credentials'
    },
    accountLocked: {
      ar: 'الحساب مقفل مؤقتاً',
      en: 'Account temporarily locked'
    },
    mfaRequired: {
      ar: 'رمز التحقق الثنائي مطلوب',
      en: 'MFA token required'
    },
    mfaToken: {
      ar: 'رمز التحقق',
      en: 'Verification Code'
    },
    enableMfa: {
      ar: 'تفعيل التحقق الثنائي',
      en: 'Enable 2FA'
    },
    disableMfa: {
      ar: 'تعطيل التحقق الثنائي',
      en: 'Disable 2FA'
    }
  },

  // ----------------------------------------
  // Dashboard
  // ----------------------------------------
  dashboard: {
    title: {
      ar: 'لوحة التحكم',
      en: 'Dashboard'
    },
    welcome: {
      ar: 'مرحباً بك',
      en: 'Welcome'
    },
    totalDiagnoses: {
      ar: 'إجمالي التشخيصات',
      en: 'Total Diagnoses'
    },
    activeFarms: {
      ar: 'المزارع النشطة',
      en: 'Active Farms'
    },
    cropsMonitored: {
      ar: 'المحاصيل المراقبة',
      en: 'Crops Monitored'
    },
    diseasesDetected: {
      ar: 'الأمراض المكتشفة',
      en: 'Diseases Detected'
    },
    recentActivity: {
      ar: 'النشاط الأخير',
      en: 'Recent Activity'
    },
    quickActions: {
      ar: 'إجراءات سريعة',
      en: 'Quick Actions'
    },
    newDiagnosis: {
      ar: 'تشخيص جديد',
      en: 'New Diagnosis'
    },
    viewReports: {
      ar: 'عرض التقارير',
      en: 'View Reports'
    },
    systemHealth: {
      ar: 'صحة النظام',
      en: 'System Health'
    }
  },

  // ----------------------------------------
  // Diagnosis
  // ----------------------------------------
  diagnosis: {
    title: {
      ar: 'تشخيص أمراض النباتات',
      en: 'Plant Disease Diagnosis'
    },
    uploadImage: {
      ar: 'رفع صورة',
      en: 'Upload Image'
    },
    dragDrop: {
      ar: 'اسحب وأفلت الصورة هنا',
      en: 'Drag and drop image here'
    },
    or: {
      ar: 'أو',
      en: 'or'
    },
    browseFiles: {
      ar: 'تصفح الملفات',
      en: 'Browse Files'
    },
    analyzing: {
      ar: 'جاري التحليل...',
      en: 'Analyzing...'
    },
    results: {
      ar: 'نتائج التشخيص',
      en: 'Diagnosis Results'
    },
    disease: {
      ar: 'المرض',
      en: 'Disease'
    },
    confidence: {
      ar: 'نسبة الثقة',
      en: 'Confidence'
    },
    severity: {
      ar: 'شدة الإصابة',
      en: 'Severity'
    },
    recommendations: {
      ar: 'التوصيات',
      en: 'Recommendations'
    },
    treatment: {
      ar: 'العلاج',
      en: 'Treatment'
    },
    prevention: {
      ar: 'الوقاية',
      en: 'Prevention'
    },
    noDisease: {
      ar: 'لم يتم اكتشاف مرض',
      en: 'No disease detected'
    },
    healthyPlant: {
      ar: 'النبات سليم',
      en: 'Healthy plant'
    },
    history: {
      ar: 'سجل التشخيصات',
      en: 'Diagnosis History'
    }
  },

  // ----------------------------------------
  // Diseases Database
  // ----------------------------------------
  diseases: {
    title: {
      ar: 'قاعدة بيانات الأمراض',
      en: 'Diseases Database'
    },
    searchPlaceholder: {
      ar: 'ابحث عن مرض...',
      en: 'Search for a disease...'
    },
    symptoms: {
      ar: 'الأعراض',
      en: 'Symptoms'
    },
    causes: {
      ar: 'الأسباب',
      en: 'Causes'
    },
    affectedCrops: {
      ar: 'المحاصيل المتأثرة',
      en: 'Affected Crops'
    },
    images: {
      ar: 'الصور',
      en: 'Images'
    },
    addDisease: {
      ar: 'إضافة مرض',
      en: 'Add Disease'
    },
    editDisease: {
      ar: 'تعديل المرض',
      en: 'Edit Disease'
    },
    deleteDisease: {
      ar: 'حذف المرض',
      en: 'Delete Disease'
    },
    totalDiseases: {
      ar: 'إجمالي الأمراض',
      en: 'Total Diseases'
    }
  },

  // ----------------------------------------
  // Farms Management
  // ----------------------------------------
  farms: {
    title: {
      ar: 'إدارة المزارع',
      en: 'Farm Management'
    },
    addFarm: {
      ar: 'إضافة مزرعة',
      en: 'Add Farm'
    },
    editFarm: {
      ar: 'تعديل المزرعة',
      en: 'Edit Farm'
    },
    farmName: {
      ar: 'اسم المزرعة',
      en: 'Farm Name'
    },
    location: {
      ar: 'الموقع',
      en: 'Location'
    },
    area: {
      ar: 'المساحة',
      en: 'Area'
    },
    areaUnit: {
      ar: 'هكتار',
      en: 'hectares'
    },
    owner: {
      ar: 'المالك',
      en: 'Owner'
    },
    crops: {
      ar: 'المحاصيل',
      en: 'Crops'
    },
    workers: {
      ar: 'العمال',
      en: 'Workers'
    },
    noFarms: {
      ar: 'لا توجد مزارع مسجلة',
      en: 'No farms registered'
    }
  },

  // ----------------------------------------
  // Crops
  // ----------------------------------------
  crops: {
    title: {
      ar: 'إدارة المحاصيل',
      en: 'Crop Management'
    },
    addCrop: {
      ar: 'إضافة محصول',
      en: 'Add Crop'
    },
    cropName: {
      ar: 'اسم المحصول',
      en: 'Crop Name'
    },
    plantingDate: {
      ar: 'تاريخ الزراعة',
      en: 'Planting Date'
    },
    harvestDate: {
      ar: 'تاريخ الحصاد',
      en: 'Harvest Date'
    },
    stage: {
      ar: 'مرحلة النمو',
      en: 'Growth Stage'
    },
    health: {
      ar: 'صحة المحصول',
      en: 'Crop Health'
    },
    healthy: {
      ar: 'سليم',
      en: 'Healthy'
    },
    infected: {
      ar: 'مصاب',
      en: 'Infected'
    },
    treated: {
      ar: 'تحت العلاج',
      en: 'Under Treatment'
    }
  },

  // ----------------------------------------
  // ML / AI
  // ----------------------------------------
  ml: {
    title: {
      ar: 'الذكاء الاصطناعي',
      en: 'Machine Learning'
    },
    modelVersion: {
      ar: 'إصدار النموذج',
      en: 'Model Version'
    },
    accuracy: {
      ar: 'الدقة',
      en: 'Accuracy'
    },
    trainModel: {
      ar: 'تدريب النموذج',
      en: 'Train Model'
    },
    trainingProgress: {
      ar: 'تقدم التدريب',
      en: 'Training Progress'
    },
    dataCollection: {
      ar: 'جمع البيانات',
      en: 'Data Collection'
    },
    imagesCollected: {
      ar: 'الصور المجمعة',
      en: 'Images Collected'
    },
    sources: {
      ar: 'المصادر',
      en: 'Sources'
    },
    activeSources: {
      ar: 'المصادر النشطة',
      en: 'Active Sources'
    },
    lastTraining: {
      ar: 'آخر تدريب',
      en: 'Last Training'
    },
    startCrawler: {
      ar: 'بدء الجمع',
      en: 'Start Crawler'
    },
    stopCrawler: {
      ar: 'إيقاف الجمع',
      en: 'Stop Crawler'
    }
  },

  // ----------------------------------------
  // Settings
  // ----------------------------------------
  settings: {
    title: {
      ar: 'الإعدادات',
      en: 'Settings'
    },
    general: {
      ar: 'عام',
      en: 'General'
    },
    appearance: {
      ar: 'المظهر',
      en: 'Appearance'
    },
    language: {
      ar: 'اللغة',
      en: 'Language'
    },
    theme: {
      ar: 'السمة',
      en: 'Theme'
    },
    lightTheme: {
      ar: 'فاتح',
      en: 'Light'
    },
    darkTheme: {
      ar: 'داكن',
      en: 'Dark'
    },
    systemTheme: {
      ar: 'النظام',
      en: 'System'
    },
    notifications: {
      ar: 'الإشعارات',
      en: 'Notifications'
    },
    emailNotifications: {
      ar: 'إشعارات البريد',
      en: 'Email Notifications'
    },
    pushNotifications: {
      ar: 'الإشعارات الفورية',
      en: 'Push Notifications'
    },
    security: {
      ar: 'الأمان',
      en: 'Security'
    },
    privacy: {
      ar: 'الخصوصية',
      en: 'Privacy'
    },
    account: {
      ar: 'الحساب',
      en: 'Account'
    },
    deleteAccount: {
      ar: 'حذف الحساب',
      en: 'Delete Account'
    }
  },

  // ----------------------------------------
  // Error Messages
  // ----------------------------------------
  errors: {
    generic: {
      ar: 'حدث خطأ غير متوقع',
      en: 'An unexpected error occurred'
    },
    network: {
      ar: 'خطأ في الاتصال بالشبكة',
      en: 'Network connection error'
    },
    unauthorized: {
      ar: 'غير مصرح لك بهذا الإجراء',
      en: 'You are not authorized for this action'
    },
    notFound: {
      ar: 'الصفحة غير موجودة',
      en: 'Page not found'
    },
    serverError: {
      ar: 'خطأ في الخادم',
      en: 'Server error'
    },
    validation: {
      ar: 'خطأ في البيانات المدخلة',
      en: 'Validation error'
    },
    fileTooBig: {
      ar: 'حجم الملف كبير جداً',
      en: 'File size too large'
    },
    invalidFileType: {
      ar: 'نوع الملف غير مدعوم',
      en: 'Invalid file type'
    },
    sessionExpired: {
      ar: 'انتهت صلاحية الجلسة',
      en: 'Session expired'
    },
    rateLimited: {
      ar: 'طلبات كثيرة جداً، يرجى الانتظار',
      en: 'Too many requests, please wait'
    }
  },

  // ----------------------------------------
  // Success Messages
  // ----------------------------------------
  success: {
    saved: {
      ar: 'تم الحفظ بنجاح',
      en: 'Saved successfully'
    },
    deleted: {
      ar: 'تم الحذف بنجاح',
      en: 'Deleted successfully'
    },
    updated: {
      ar: 'تم التحديث بنجاح',
      en: 'Updated successfully'
    },
    created: {
      ar: 'تم الإنشاء بنجاح',
      en: 'Created successfully'
    },
    uploaded: {
      ar: 'تم الرفع بنجاح',
      en: 'Uploaded successfully'
    },
    emailSent: {
      ar: 'تم إرسال البريد بنجاح',
      en: 'Email sent successfully'
    },
    passwordChanged: {
      ar: 'تم تغيير كلمة المرور بنجاح',
      en: 'Password changed successfully'
    }
  },

  // ----------------------------------------
  // Confirmation Dialogs
  // ----------------------------------------
  confirm: {
    delete: {
      ar: 'هل أنت متأكد من الحذف؟',
      en: 'Are you sure you want to delete?'
    },
    logout: {
      ar: 'هل تريد تسجيل الخروج؟',
      en: 'Do you want to logout?'
    },
    discard: {
      ar: 'هل تريد تجاهل التغييرات؟',
      en: 'Discard changes?'
    },
    cannotUndo: {
      ar: 'لا يمكن التراجع عن هذا الإجراء',
      en: 'This action cannot be undone'
    }
  },

  // ----------------------------------------
  // Time & Date
  // ----------------------------------------
  time: {
    today: {
      ar: 'اليوم',
      en: 'Today'
    },
    yesterday: {
      ar: 'أمس',
      en: 'Yesterday'
    },
    tomorrow: {
      ar: 'غداً',
      en: 'Tomorrow'
    },
    thisWeek: {
      ar: 'هذا الأسبوع',
      en: 'This Week'
    },
    thisMonth: {
      ar: 'هذا الشهر',
      en: 'This Month'
    },
    thisYear: {
      ar: 'هذه السنة',
      en: 'This Year'
    },
    ago: {
      ar: 'منذ',
      en: 'ago'
    },
    minutes: {
      ar: 'دقائق',
      en: 'minutes'
    },
    hours: {
      ar: 'ساعات',
      en: 'hours'
    },
    days: {
      ar: 'أيام',
      en: 'days'
    }
  }
};

// ============================================
// Translation Hook
// ============================================

import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for accessing translations
 * 
 * @returns {Object} Translation utilities
 */
export const useTranslation = () => {
  const [language, setLanguage] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('language') || 'ar';
    }
    return 'ar';
  });

  useEffect(() => {
    const handleStorage = (e) => {
      if (e.key === 'language') {
        setLanguage(e.newValue || 'ar');
      }
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  /**
   * Get translation by key path
   * @param {string} key - Dot-separated key path (e.g., 'nav.dashboard')
   * @param {Object} params - Interpolation parameters
   * @returns {string} Translated string
   */
  const t = useCallback((key, params = {}) => {
    const keys = key.split('.');
    let value = translations;

    for (const k of keys) {
      if (value && value[k]) {
        value = value[k];
      } else {
        console.warn(`Translation key not found: ${key}`);
        return key;
      }
    }

    // Get language-specific translation
    let result = value[language] || value['en'] || key;

    // Handle interpolation
    if (params && typeof result === 'string') {
      Object.entries(params).forEach(([param, val]) => {
        result = result.replace(new RegExp(`{{${param}}}`, 'g'), val);
      });
    }

    return result;
  }, [language]);

  /**
   * Change current language
   * @param {string} lang - Language code ('ar' or 'en')
   */
  const changeLanguage = useCallback((lang) => {
    setLanguage(lang);
    localStorage.setItem('language', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);
  }, []);

  return {
    t,
    language,
    changeLanguage,
    isRTL: language === 'ar',
    isArabic: language === 'ar',
    isEnglish: language === 'en'
  };
};

// ============================================
// Simple translate function (non-hook)
// ============================================

/**
 * Simple translation function for use outside React components
 * @param {string} key - Translation key
 * @param {string} lang - Language code (optional, defaults to localStorage)
 * @returns {string} Translated string
 */
export const translate = (key, lang = null) => {
  const language = lang || (typeof window !== 'undefined' ? localStorage.getItem('language') : 'ar') || 'ar';
  const keys = key.split('.');
  let value = translations;

  for (const k of keys) {
    if (value && value[k]) {
      value = value[k];
    } else {
      return key;
    }
  }

  return value[language] || value['en'] || key;
};

export default translations;
