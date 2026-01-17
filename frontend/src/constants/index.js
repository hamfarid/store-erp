/**
 * Application Constants
 * @file frontend/src/constants/index.js
 * 
 * ثوابت التطبيق
 */

// ============================================
// حالات المخزون
// ============================================
export const STOCK_STATUS = {
  IN_STOCK: 'in_stock',
  LOW_STOCK: 'low_stock',
  OUT_OF_STOCK: 'out_of_stock'
};

export const STOCK_STATUS_LABELS = {
  [STOCK_STATUS.IN_STOCK]: 'متوفر',
  [STOCK_STATUS.LOW_STOCK]: 'منخفض',
  [STOCK_STATUS.OUT_OF_STOCK]: 'نفذ'
};

// ============================================
// حالات الفواتير
// ============================================
export const INVOICE_STATUS = {
  DRAFT: 'draft',
  PENDING: 'pending',
  PAID: 'paid',
  PARTIAL: 'partial',
  OVERDUE: 'overdue',
  CANCELLED: 'cancelled',
  REFUNDED: 'refunded'
};

export const INVOICE_STATUS_LABELS = {
  [INVOICE_STATUS.DRAFT]: 'مسودة',
  [INVOICE_STATUS.PENDING]: 'قيد الانتظار',
  [INVOICE_STATUS.PAID]: 'مدفوعة',
  [INVOICE_STATUS.PARTIAL]: 'مدفوعة جزئياً',
  [INVOICE_STATUS.OVERDUE]: 'متأخرة',
  [INVOICE_STATUS.CANCELLED]: 'ملغاة',
  [INVOICE_STATUS.REFUNDED]: 'مستردة'
};

// ============================================
// أنواع المعاملات
// ============================================
export const TRANSACTION_TYPES = {
  SALE: 'sale',
  PURCHASE: 'purchase',
  RETURN: 'return',
  ADJUSTMENT: 'adjustment',
  TRANSFER: 'transfer',
  EXPENSE: 'expense',
  INCOME: 'income'
};

export const TRANSACTION_TYPE_LABELS = {
  [TRANSACTION_TYPES.SALE]: 'مبيعات',
  [TRANSACTION_TYPES.PURCHASE]: 'مشتريات',
  [TRANSACTION_TYPES.RETURN]: 'مرتجع',
  [TRANSACTION_TYPES.ADJUSTMENT]: 'تعديل',
  [TRANSACTION_TYPES.TRANSFER]: 'تحويل',
  [TRANSACTION_TYPES.EXPENSE]: 'مصروف',
  [TRANSACTION_TYPES.INCOME]: 'إيراد'
};

// ============================================
// طرق الدفع
// ============================================
export const PAYMENT_METHODS = {
  CASH: 'cash',
  CARD: 'card',
  BANK_TRANSFER: 'bank_transfer',
  CHECK: 'check',
  CREDIT: 'credit',
  MADA: 'mada',
  VISA: 'visa',
  MASTERCARD: 'mastercard',
  APPLE_PAY: 'apple_pay',
  STC_PAY: 'stc_pay'
};

export const PAYMENT_METHOD_LABELS = {
  [PAYMENT_METHODS.CASH]: 'نقداً',
  [PAYMENT_METHODS.CARD]: 'بطاقة',
  [PAYMENT_METHODS.BANK_TRANSFER]: 'تحويل بنكي',
  [PAYMENT_METHODS.CHECK]: 'شيك',
  [PAYMENT_METHODS.CREDIT]: 'آجل',
  [PAYMENT_METHODS.MADA]: 'مدى',
  [PAYMENT_METHODS.VISA]: 'فيزا',
  [PAYMENT_METHODS.MASTERCARD]: 'ماستركارد',
  [PAYMENT_METHODS.APPLE_PAY]: 'Apple Pay',
  [PAYMENT_METHODS.STC_PAY]: 'STC Pay'
};

// ============================================
// أنواع الوحدات
// ============================================
export const UNIT_TYPES = {
  PIECE: 'piece',
  KG: 'kg',
  GRAM: 'gram',
  LITER: 'liter',
  METER: 'meter',
  BOX: 'box',
  PACK: 'pack',
  CARTON: 'carton',
  DOZEN: 'dozen'
};

export const UNIT_TYPE_LABELS = {
  [UNIT_TYPES.PIECE]: 'قطعة',
  [UNIT_TYPES.KG]: 'كيلوغرام',
  [UNIT_TYPES.GRAM]: 'غرام',
  [UNIT_TYPES.LITER]: 'لتر',
  [UNIT_TYPES.METER]: 'متر',
  [UNIT_TYPES.BOX]: 'صندوق',
  [UNIT_TYPES.PACK]: 'عبوة',
  [UNIT_TYPES.CARTON]: 'كرتون',
  [UNIT_TYPES.DOZEN]: 'درزن'
};

// ============================================
// أدوار المستخدمين
// ============================================
export const USER_ROLES = {
  SUPER_ADMIN: 'super_admin',
  ADMIN: 'admin',
  MANAGER: 'manager',
  ACCOUNTANT: 'accountant',
  CASHIER: 'cashier',
  INVENTORY: 'inventory',
  SALES: 'sales',
  VIEWER: 'viewer'
};

export const USER_ROLE_LABELS = {
  [USER_ROLES.SUPER_ADMIN]: 'مدير النظام',
  [USER_ROLES.ADMIN]: 'مدير',
  [USER_ROLES.MANAGER]: 'مشرف',
  [USER_ROLES.ACCOUNTANT]: 'محاسب',
  [USER_ROLES.CASHIER]: 'كاشير',
  [USER_ROLES.INVENTORY]: 'مسؤول مخزون',
  [USER_ROLES.SALES]: 'مبيعات',
  [USER_ROLES.VIEWER]: 'مشاهد'
};

// ============================================
// حالات الطلبات
// ============================================
export const ORDER_STATUS = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  PROCESSING: 'processing',
  SHIPPED: 'shipped',
  DELIVERED: 'delivered',
  CANCELLED: 'cancelled',
  RETURNED: 'returned'
};

export const ORDER_STATUS_LABELS = {
  [ORDER_STATUS.PENDING]: 'قيد الانتظار',
  [ORDER_STATUS.CONFIRMED]: 'مؤكد',
  [ORDER_STATUS.PROCESSING]: 'قيد التجهيز',
  [ORDER_STATUS.SHIPPED]: 'تم الشحن',
  [ORDER_STATUS.DELIVERED]: 'تم التسليم',
  [ORDER_STATUS.CANCELLED]: 'ملغي',
  [ORDER_STATUS.RETURNED]: 'مرتجع'
};

// ============================================
// فترات التقارير
// ============================================
export const REPORT_PERIODS = {
  TODAY: 'today',
  YESTERDAY: 'yesterday',
  THIS_WEEK: 'this_week',
  LAST_WEEK: 'last_week',
  THIS_MONTH: 'this_month',
  LAST_MONTH: 'last_month',
  THIS_QUARTER: 'this_quarter',
  LAST_QUARTER: 'last_quarter',
  THIS_YEAR: 'this_year',
  LAST_YEAR: 'last_year',
  CUSTOM: 'custom'
};

export const REPORT_PERIOD_LABELS = {
  [REPORT_PERIODS.TODAY]: 'اليوم',
  [REPORT_PERIODS.YESTERDAY]: 'أمس',
  [REPORT_PERIODS.THIS_WEEK]: 'هذا الأسبوع',
  [REPORT_PERIODS.LAST_WEEK]: 'الأسبوع الماضي',
  [REPORT_PERIODS.THIS_MONTH]: 'هذا الشهر',
  [REPORT_PERIODS.LAST_MONTH]: 'الشهر الماضي',
  [REPORT_PERIODS.THIS_QUARTER]: 'هذا الربع',
  [REPORT_PERIODS.LAST_QUARTER]: 'الربع الماضي',
  [REPORT_PERIODS.THIS_YEAR]: 'هذا العام',
  [REPORT_PERIODS.LAST_YEAR]: 'العام الماضي',
  [REPORT_PERIODS.CUSTOM]: 'فترة مخصصة'
};

// ============================================
// أنواع الضرائب
// ============================================
export const TAX_TYPES = {
  VAT: 'vat',
  EXEMPT: 'exempt',
  ZERO_RATED: 'zero_rated'
};

export const TAX_RATES = {
  [TAX_TYPES.VAT]: 15,
  [TAX_TYPES.EXEMPT]: 0,
  [TAX_TYPES.ZERO_RATED]: 0
};

// ============================================
// حالات اللوط
// ============================================
export const LOT_STATUS = {
  ACTIVE: 'active',
  EXPIRED: 'expired',
  EXPIRING_SOON: 'expiring_soon',
  RESERVED: 'reserved',
  DEPLETED: 'depleted'
};

export const LOT_STATUS_LABELS = {
  [LOT_STATUS.ACTIVE]: 'نشط',
  [LOT_STATUS.EXPIRED]: 'منتهي',
  [LOT_STATUS.EXPIRING_SOON]: 'ينتهي قريباً',
  [LOT_STATUS.RESERVED]: 'محجوز',
  [LOT_STATUS.DEPLETED]: 'نفذ'
};

// ============================================
// إعدادات النظام
// ============================================
export const SYSTEM_SETTINGS = {
  DEFAULT_LANGUAGE: 'ar',
  DEFAULT_CURRENCY: 'EGP',
  DEFAULT_DATE_FORMAT: 'DD/MM/YYYY',
  DEFAULT_TIME_FORMAT: 'HH:mm',
  DEFAULT_PAGE_SIZE: 20,
  MAX_UPLOAD_SIZE: 10 * 1024 * 1024, // 10MB
  SESSION_TIMEOUT: 30 * 60 * 1000, // 30 minutes
  REFRESH_TOKEN_INTERVAL: 5 * 60 * 1000, // 5 minutes
};

// ============================================
// رسائل الخطأ
// ============================================
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'خطأ في الاتصال بالخادم',
  UNAUTHORIZED: 'غير مصرح لك بهذا الإجراء',
  NOT_FOUND: 'العنصر غير موجود',
  VALIDATION_ERROR: 'بيانات غير صحيحة',
  SERVER_ERROR: 'حدث خطأ في الخادم',
  SESSION_EXPIRED: 'انتهت صلاحية الجلسة',
  INSUFFICIENT_STOCK: 'الكمية المطلوبة غير متوفرة',
  DUPLICATE_ENTRY: 'هذا العنصر موجود مسبقاً',
  DELETE_RESTRICTED: 'لا يمكن حذف هذا العنصر'
};

// ============================================
// رسائل النجاح
// ============================================
export const SUCCESS_MESSAGES = {
  CREATED: 'تم الإنشاء بنجاح',
  UPDATED: 'تم التحديث بنجاح',
  DELETED: 'تم الحذف بنجاح',
  SAVED: 'تم الحفظ بنجاح',
  EXPORTED: 'تم التصدير بنجاح',
  IMPORTED: 'تم الاستيراد بنجاح',
  PRINTED: 'تمت الطباعة بنجاح',
  SENT: 'تم الإرسال بنجاح'
};

// ============================================
// مفاتيح التخزين المحلي
// ============================================
export const STORAGE_KEYS = {
  TOKEN: 'store_erp_token',
  REFRESH_TOKEN: 'store_erp_refresh_token',
  USER: 'store_erp_user',
  THEME: 'store_erp_theme',
  LANGUAGE: 'store_erp_language',
  SIDEBAR_STATE: 'store_erp_sidebar',
  TABLE_SETTINGS: 'store_erp_table_settings',
  CART: 'store_erp_cart'
};

// ============================================
// أحداث التتبع
// ============================================
export const AUDIT_EVENTS = {
  LOGIN: 'login',
  LOGOUT: 'logout',
  CREATE: 'create',
  UPDATE: 'update',
  DELETE: 'delete',
  EXPORT: 'export',
  IMPORT: 'import',
  PRINT: 'print',
  APPROVE: 'approve',
  REJECT: 'reject'
};

export default {
  STOCK_STATUS,
  INVOICE_STATUS,
  TRANSACTION_TYPES,
  PAYMENT_METHODS,
  UNIT_TYPES,
  USER_ROLES,
  ORDER_STATUS,
  REPORT_PERIODS,
  TAX_TYPES,
  LOT_STATUS,
  SYSTEM_SETTINGS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  STORAGE_KEYS,
  AUDIT_EVENTS
};
