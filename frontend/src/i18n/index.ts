/**
 * P2.64: Multi-language Support (i18n)
 * 
 * Internationalization system with Arabic/English support.
 */

import {
  createContext,
  useContext,
  useState,
  useCallback,
  ReactNode,
  useEffect,
} from 'react';

// =============================================================================
// Types
// =============================================================================

export type Language = 'en' | 'ar';
export type Direction = 'ltr' | 'rtl';

export interface TranslationKeys {
  // Common
  'common.save': string;
  'common.cancel': string;
  'common.delete': string;
  'common.edit': string;
  'common.add': string;
  'common.search': string;
  'common.filter': string;
  'common.export': string;
  'common.import': string;
  'common.refresh': string;
  'common.loading': string;
  'common.error': string;
  'common.success': string;
  'common.warning': string;
  'common.confirm': string;
  'common.yes': string;
  'common.no': string;
  'common.close': string;
  'common.back': string;
  'common.next': string;
  'common.previous': string;
  'common.submit': string;
  'common.reset': string;
  'common.clear': string;
  'common.all': string;
  'common.none': string;
  'common.select': string;
  'common.actions': string;
  'common.status': string;
  'common.date': string;
  'common.time': string;
  'common.name': string;
  'common.description': string;
  'common.total': string;
  'common.subtotal': string;
  'common.quantity': string;
  'common.price': string;
  'common.discount': string;
  'common.tax': string;
  
  // Navigation
  'nav.dashboard': string;
  'nav.products': string;
  'nav.inventory': string;
  'nav.invoices': string;
  'nav.customers': string;
  'nav.suppliers': string;
  'nav.reports': string;
  'nav.settings': string;
  'nav.users': string;
  'nav.logout': string;
  
  // Auth
  'auth.login': string;
  'auth.logout': string;
  'auth.username': string;
  'auth.password': string;
  'auth.email': string;
  'auth.forgotPassword': string;
  'auth.rememberMe': string;
  'auth.signIn': string;
  'auth.signUp': string;
  'auth.invalidCredentials': string;
  'auth.sessionExpired': string;
  
  // Products
  'products.title': string;
  'products.addProduct': string;
  'products.editProduct': string;
  'products.productName': string;
  'products.sku': string;
  'products.barcode': string;
  'products.category': string;
  'products.brand': string;
  'products.cost': string;
  'products.sellingPrice': string;
  'products.stock': string;
  'products.minStock': string;
  'products.lowStock': string;
  'products.outOfStock': string;
  
  // Invoices
  'invoices.title': string;
  'invoices.newInvoice': string;
  'invoices.invoiceNumber': string;
  'invoices.customer': string;
  'invoices.date': string;
  'invoices.dueDate': string;
  'invoices.items': string;
  'invoices.paid': string;
  'invoices.pending': string;
  'invoices.overdue': string;
  'invoices.cancelled': string;
  'invoices.print': string;
  'invoices.download': string;
  
  // Customers
  'customers.title': string;
  'customers.addCustomer': string;
  'customers.customerName': string;
  'customers.phone': string;
  'customers.address': string;
  'customers.balance': string;
  'customers.creditLimit': string;
  
  // Dashboard
  'dashboard.title': string;
  'dashboard.totalSales': string;
  'dashboard.totalPurchases': string;
  'dashboard.profit': string;
  'dashboard.lowStockItems': string;
  'dashboard.pendingInvoices': string;
  'dashboard.recentActivity': string;
  'dashboard.topProducts': string;
  'dashboard.topCustomers': string;
  
  // Settings
  'settings.title': string;
  'settings.general': string;
  'settings.appearance': string;
  'settings.language': string;
  'settings.currency': string;
  'settings.timezone': string;
  'settings.notifications': string;
  'settings.security': string;
  'settings.backup': string;
  
  // Messages
  'messages.saveSuccess': string;
  'messages.saveError': string;
  'messages.deleteSuccess': string;
  'messages.deleteError': string;
  'messages.deleteConfirm': string;
  'messages.noData': string;
  'messages.networkError': string;
  'messages.accessDenied': string;
  
  // Validation
  'validation.required': string;
  'validation.email': string;
  'validation.minLength': string;
  'validation.maxLength': string;
  'validation.min': string;
  'validation.max': string;
  'validation.pattern': string;
  
  [key: string]: string;
}

interface I18nContextType {
  language: Language;
  direction: Direction;
  setLanguage: (lang: Language) => void;
  t: (key: keyof TranslationKeys, params?: Record<string, string | number>) => string;
  formatNumber: (num: number, options?: Intl.NumberFormatOptions) => string;
  formatCurrency: (amount: number, currency?: string) => string;
  formatDate: (date: Date | string, options?: Intl.DateTimeFormatOptions) => string;
  formatTime: (date: Date | string) => string;
  formatRelativeTime: (date: Date | string) => string;
}

// =============================================================================
// Translations
// =============================================================================

const translations: Record<Language, TranslationKeys> = {
  en: {
    // Common
    'common.save': 'Save',
    'common.cancel': 'Cancel',
    'common.delete': 'Delete',
    'common.edit': 'Edit',
    'common.add': 'Add',
    'common.search': 'Search',
    'common.filter': 'Filter',
    'common.export': 'Export',
    'common.import': 'Import',
    'common.refresh': 'Refresh',
    'common.loading': 'Loading...',
    'common.error': 'Error',
    'common.success': 'Success',
    'common.warning': 'Warning',
    'common.confirm': 'Confirm',
    'common.yes': 'Yes',
    'common.no': 'No',
    'common.close': 'Close',
    'common.back': 'Back',
    'common.next': 'Next',
    'common.previous': 'Previous',
    'common.submit': 'Submit',
    'common.reset': 'Reset',
    'common.clear': 'Clear',
    'common.all': 'All',
    'common.none': 'None',
    'common.select': 'Select',
    'common.actions': 'Actions',
    'common.status': 'Status',
    'common.date': 'Date',
    'common.time': 'Time',
    'common.name': 'Name',
    'common.description': 'Description',
    'common.total': 'Total',
    'common.subtotal': 'Subtotal',
    'common.quantity': 'Quantity',
    'common.price': 'Price',
    'common.discount': 'Discount',
    'common.tax': 'Tax',
    
    // Navigation
    'nav.dashboard': 'Dashboard',
    'nav.products': 'Products',
    'nav.inventory': 'Inventory',
    'nav.invoices': 'Invoices',
    'nav.customers': 'Customers',
    'nav.suppliers': 'Suppliers',
    'nav.reports': 'Reports',
    'nav.settings': 'Settings',
    'nav.users': 'Users',
    'nav.logout': 'Logout',
    
    // Auth
    'auth.login': 'Login',
    'auth.logout': 'Logout',
    'auth.username': 'Username',
    'auth.password': 'Password',
    'auth.email': 'Email',
    'auth.forgotPassword': 'Forgot Password?',
    'auth.rememberMe': 'Remember me',
    'auth.signIn': 'Sign In',
    'auth.signUp': 'Sign Up',
    'auth.invalidCredentials': 'Invalid username or password',
    'auth.sessionExpired': 'Your session has expired. Please login again.',
    
    // Products
    'products.title': 'Products',
    'products.addProduct': 'Add Product',
    'products.editProduct': 'Edit Product',
    'products.productName': 'Product Name',
    'products.sku': 'SKU',
    'products.barcode': 'Barcode',
    'products.category': 'Category',
    'products.brand': 'Brand',
    'products.cost': 'Cost',
    'products.sellingPrice': 'Selling Price',
    'products.stock': 'Stock',
    'products.minStock': 'Min Stock',
    'products.lowStock': 'Low Stock',
    'products.outOfStock': 'Out of Stock',
    
    // Invoices
    'invoices.title': 'Invoices',
    'invoices.newInvoice': 'New Invoice',
    'invoices.invoiceNumber': 'Invoice #',
    'invoices.customer': 'Customer',
    'invoices.date': 'Date',
    'invoices.dueDate': 'Due Date',
    'invoices.items': 'Items',
    'invoices.paid': 'Paid',
    'invoices.pending': 'Pending',
    'invoices.overdue': 'Overdue',
    'invoices.cancelled': 'Cancelled',
    'invoices.print': 'Print',
    'invoices.download': 'Download',
    
    // Customers
    'customers.title': 'Customers',
    'customers.addCustomer': 'Add Customer',
    'customers.customerName': 'Customer Name',
    'customers.phone': 'Phone',
    'customers.address': 'Address',
    'customers.balance': 'Balance',
    'customers.creditLimit': 'Credit Limit',
    
    // Dashboard
    'dashboard.title': 'Dashboard',
    'dashboard.totalSales': 'Total Sales',
    'dashboard.totalPurchases': 'Total Purchases',
    'dashboard.profit': 'Profit',
    'dashboard.lowStockItems': 'Low Stock Items',
    'dashboard.pendingInvoices': 'Pending Invoices',
    'dashboard.recentActivity': 'Recent Activity',
    'dashboard.topProducts': 'Top Products',
    'dashboard.topCustomers': 'Top Customers',
    
    // Settings
    'settings.title': 'Settings',
    'settings.general': 'General',
    'settings.appearance': 'Appearance',
    'settings.language': 'Language',
    'settings.currency': 'Currency',
    'settings.timezone': 'Timezone',
    'settings.notifications': 'Notifications',
    'settings.security': 'Security',
    'settings.backup': 'Backup',
    
    // Messages
    'messages.saveSuccess': 'Saved successfully',
    'messages.saveError': 'Failed to save',
    'messages.deleteSuccess': 'Deleted successfully',
    'messages.deleteError': 'Failed to delete',
    'messages.deleteConfirm': 'Are you sure you want to delete this item?',
    'messages.noData': 'No data available',
    'messages.networkError': 'Network error. Please try again.',
    'messages.accessDenied': 'Access denied',
    
    // Validation
    'validation.required': 'This field is required',
    'validation.email': 'Please enter a valid email',
    'validation.minLength': 'Minimum {min} characters required',
    'validation.maxLength': 'Maximum {max} characters allowed',
    'validation.min': 'Minimum value is {min}',
    'validation.max': 'Maximum value is {max}',
    'validation.pattern': 'Invalid format',
  },
  
  ar: {
    // Common
    'common.save': 'حفظ',
    'common.cancel': 'إلغاء',
    'common.delete': 'حذف',
    'common.edit': 'تعديل',
    'common.add': 'إضافة',
    'common.search': 'بحث',
    'common.filter': 'تصفية',
    'common.export': 'تصدير',
    'common.import': 'استيراد',
    'common.refresh': 'تحديث',
    'common.loading': 'جاري التحميل...',
    'common.error': 'خطأ',
    'common.success': 'نجاح',
    'common.warning': 'تحذير',
    'common.confirm': 'تأكيد',
    'common.yes': 'نعم',
    'common.no': 'لا',
    'common.close': 'إغلاق',
    'common.back': 'رجوع',
    'common.next': 'التالي',
    'common.previous': 'السابق',
    'common.submit': 'إرسال',
    'common.reset': 'إعادة تعيين',
    'common.clear': 'مسح',
    'common.all': 'الكل',
    'common.none': 'لا شيء',
    'common.select': 'اختر',
    'common.actions': 'إجراءات',
    'common.status': 'الحالة',
    'common.date': 'التاريخ',
    'common.time': 'الوقت',
    'common.name': 'الاسم',
    'common.description': 'الوصف',
    'common.total': 'الإجمالي',
    'common.subtotal': 'المجموع الفرعي',
    'common.quantity': 'الكمية',
    'common.price': 'السعر',
    'common.discount': 'الخصم',
    'common.tax': 'الضريبة',
    
    // Navigation
    'nav.dashboard': 'لوحة التحكم',
    'nav.products': 'المنتجات',
    'nav.inventory': 'المخزون',
    'nav.invoices': 'الفواتير',
    'nav.customers': 'العملاء',
    'nav.suppliers': 'الموردون',
    'nav.reports': 'التقارير',
    'nav.settings': 'الإعدادات',
    'nav.users': 'المستخدمون',
    'nav.logout': 'تسجيل الخروج',
    
    // Auth
    'auth.login': 'تسجيل الدخول',
    'auth.logout': 'تسجيل الخروج',
    'auth.username': 'اسم المستخدم',
    'auth.password': 'كلمة المرور',
    'auth.email': 'البريد الإلكتروني',
    'auth.forgotPassword': 'نسيت كلمة المرور؟',
    'auth.rememberMe': 'تذكرني',
    'auth.signIn': 'دخول',
    'auth.signUp': 'تسجيل',
    'auth.invalidCredentials': 'اسم المستخدم أو كلمة المرور غير صحيحة',
    'auth.sessionExpired': 'انتهت صلاحية الجلسة. يرجى تسجيل الدخول مرة أخرى.',
    
    // Products
    'products.title': 'المنتجات',
    'products.addProduct': 'إضافة منتج',
    'products.editProduct': 'تعديل المنتج',
    'products.productName': 'اسم المنتج',
    'products.sku': 'رمز المنتج',
    'products.barcode': 'الباركود',
    'products.category': 'الفئة',
    'products.brand': 'العلامة التجارية',
    'products.cost': 'التكلفة',
    'products.sellingPrice': 'سعر البيع',
    'products.stock': 'المخزون',
    'products.minStock': 'الحد الأدنى',
    'products.lowStock': 'مخزون منخفض',
    'products.outOfStock': 'نفذ المخزون',
    
    // Invoices
    'invoices.title': 'الفواتير',
    'invoices.newInvoice': 'فاتورة جديدة',
    'invoices.invoiceNumber': 'رقم الفاتورة',
    'invoices.customer': 'العميل',
    'invoices.date': 'التاريخ',
    'invoices.dueDate': 'تاريخ الاستحقاق',
    'invoices.items': 'الأصناف',
    'invoices.paid': 'مدفوعة',
    'invoices.pending': 'معلقة',
    'invoices.overdue': 'متأخرة',
    'invoices.cancelled': 'ملغاة',
    'invoices.print': 'طباعة',
    'invoices.download': 'تحميل',
    
    // Customers
    'customers.title': 'العملاء',
    'customers.addCustomer': 'إضافة عميل',
    'customers.customerName': 'اسم العميل',
    'customers.phone': 'الهاتف',
    'customers.address': 'العنوان',
    'customers.balance': 'الرصيد',
    'customers.creditLimit': 'حد الائتمان',
    
    // Dashboard
    'dashboard.title': 'لوحة التحكم',
    'dashboard.totalSales': 'إجمالي المبيعات',
    'dashboard.totalPurchases': 'إجمالي المشتريات',
    'dashboard.profit': 'الربح',
    'dashboard.lowStockItems': 'أصناف مخزون منخفض',
    'dashboard.pendingInvoices': 'فواتير معلقة',
    'dashboard.recentActivity': 'النشاط الأخير',
    'dashboard.topProducts': 'أفضل المنتجات',
    'dashboard.topCustomers': 'أفضل العملاء',
    
    // Settings
    'settings.title': 'الإعدادات',
    'settings.general': 'عام',
    'settings.appearance': 'المظهر',
    'settings.language': 'اللغة',
    'settings.currency': 'العملة',
    'settings.timezone': 'المنطقة الزمنية',
    'settings.notifications': 'الإشعارات',
    'settings.security': 'الأمان',
    'settings.backup': 'النسخ الاحتياطي',
    
    // Messages
    'messages.saveSuccess': 'تم الحفظ بنجاح',
    'messages.saveError': 'فشل في الحفظ',
    'messages.deleteSuccess': 'تم الحذف بنجاح',
    'messages.deleteError': 'فشل في الحذف',
    'messages.deleteConfirm': 'هل أنت متأكد من حذف هذا العنصر؟',
    'messages.noData': 'لا توجد بيانات',
    'messages.networkError': 'خطأ في الشبكة. يرجى المحاولة مرة أخرى.',
    'messages.accessDenied': 'تم رفض الوصول',
    
    // Validation
    'validation.required': 'هذا الحقل مطلوب',
    'validation.email': 'يرجى إدخال بريد إلكتروني صحيح',
    'validation.minLength': 'الحد الأدنى {min} أحرف',
    'validation.maxLength': 'الحد الأقصى {max} أحرف',
    'validation.min': 'القيمة الأدنى هي {min}',
    'validation.max': 'القيمة الأقصى هي {max}',
    'validation.pattern': 'تنسيق غير صحيح',
  },
};

// =============================================================================
// Context
// =============================================================================

const I18nContext = createContext<I18nContextType | null>(null);

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error('useI18n must be used within I18nProvider');
  }
  return context;
}

// Shorthand hook
export function useTranslation() {
  const { t, language, direction } = useI18n();
  return { t, language, direction };
}

// =============================================================================
// Provider
// =============================================================================

interface I18nProviderProps {
  children: ReactNode;
  defaultLanguage?: Language;
}

export function I18nProvider({ children, defaultLanguage = 'en' }: I18nProviderProps) {
  const [language, setLanguageState] = useState<Language>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('language') as Language;
      return saved || defaultLanguage;
    }
    return defaultLanguage;
  });

  const direction: Direction = language === 'ar' ? 'rtl' : 'ltr';

  // Update document direction
  useEffect(() => {
    document.documentElement.dir = direction;
    document.documentElement.lang = language;
    localStorage.setItem('language', language);
  }, [language, direction]);

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang);
  }, []);

  const t = useCallback(
    (key: keyof TranslationKeys, params?: Record<string, string | number>): string => {
      let text = translations[language][key] || key;
      
      if (params) {
        Object.entries(params).forEach(([k, v]) => {
          text = text.replace(new RegExp(`\\{${k}\\}`, 'g'), String(v));
        });
      }
      
      return text;
    },
    [language]
  );

  const formatNumber = useCallback(
    (num: number, options?: Intl.NumberFormatOptions) => {
      return new Intl.NumberFormat(language === 'ar' ? 'ar-SA' : 'en-US', options).format(num);
    },
    [language]
  );

  const formatCurrency = useCallback(
    (amount: number, currency = 'USD') => {
      return new Intl.NumberFormat(language === 'ar' ? 'ar-SA' : 'en-US', {
        style: 'currency',
        currency,
      }).format(amount);
    },
    [language]
  );

  const formatDate = useCallback(
    (date: Date | string, options?: Intl.DateTimeFormatOptions) => {
      const d = typeof date === 'string' ? new Date(date) : date;
      return new Intl.DateTimeFormat(
        language === 'ar' ? 'ar-SA' : 'en-US',
        options || { dateStyle: 'medium' }
      ).format(d);
    },
    [language]
  );

  const formatTime = useCallback(
    (date: Date | string) => {
      const d = typeof date === 'string' ? new Date(date) : date;
      return new Intl.DateTimeFormat(language === 'ar' ? 'ar-SA' : 'en-US', {
        timeStyle: 'short',
      }).format(d);
    },
    [language]
  );

  const formatRelativeTime = useCallback(
    (date: Date | string) => {
      const d = typeof date === 'string' ? new Date(date) : date;
      const now = new Date();
      const diff = now.getTime() - d.getTime();
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);

      const rtf = new Intl.RelativeTimeFormat(language === 'ar' ? 'ar' : 'en', {
        numeric: 'auto',
      });

      if (days > 0) return rtf.format(-days, 'day');
      if (hours > 0) return rtf.format(-hours, 'hour');
      if (minutes > 0) return rtf.format(-minutes, 'minute');
      return rtf.format(-seconds, 'second');
    },
    [language]
  );

  const value: I18nContextType = {
    language,
    direction,
    setLanguage,
    t,
    formatNumber,
    formatCurrency,
    formatDate,
    formatTime,
    formatRelativeTime,
  };

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

// =============================================================================
// Exports
// =============================================================================

export { translations };
export default I18nProvider;

