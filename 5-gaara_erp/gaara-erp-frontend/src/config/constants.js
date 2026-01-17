/**
 * Application Constants
 * Centralized configuration and constants
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
}

// App Configuration
export const APP_CONFIG = {
  NAME: "Gaara ERP",
  VERSION: "1.0.0",
  DESCRIPTION: "نظام إدارة موارد المؤسسات الذكي",
  SUPPORT_EMAIL: "support@gaara-erp.com",
  SUPPORT_PHONE: "+966501234567",
}

// User Roles
export const ROLES = {
  ADMIN: "admin",
  MANAGER: "manager",
  ACCOUNTANT: "accountant",
  USER: "user",
}

export const ROLE_LABELS = {
  [ROLES.ADMIN]: "مدير",
  [ROLES.MANAGER]: "مدير فرع",
  [ROLES.ACCOUNTANT]: "محاسب",
  [ROLES.USER]: "مستخدم",
}

// User Status
export const USER_STATUS = {
  ACTIVE: "active",
  INACTIVE: "inactive",
  SUSPENDED: "suspended",
  PENDING: "pending",
}

export const USER_STATUS_LABELS = {
  [USER_STATUS.ACTIVE]: "نشط",
  [USER_STATUS.INACTIVE]: "معطل",
  [USER_STATUS.SUSPENDED]: "معلق",
  [USER_STATUS.PENDING]: "قيد الانتظار",
}

// Order Status
export const ORDER_STATUS = {
  PENDING: "pending",
  CONFIRMED: "confirmed",
  PROCESSING: "processing",
  SHIPPED: "shipped",
  DELIVERED: "delivered",
  CANCELLED: "cancelled",
  RETURNED: "returned",
}

export const ORDER_STATUS_LABELS = {
  [ORDER_STATUS.PENDING]: "قيد الانتظار",
  [ORDER_STATUS.CONFIRMED]: "مؤكد",
  [ORDER_STATUS.PROCESSING]: "قيد المعالجة",
  [ORDER_STATUS.SHIPPED]: "تم الشحن",
  [ORDER_STATUS.DELIVERED]: "تم التسليم",
  [ORDER_STATUS.CANCELLED]: "ملغي",
  [ORDER_STATUS.RETURNED]: "مرتجع",
}

// Invoice Status
export const INVOICE_STATUS = {
  DRAFT: "draft",
  SENT: "sent",
  PAID: "paid",
  OVERDUE: "overdue",
  CANCELLED: "cancelled",
}

export const INVOICE_STATUS_LABELS = {
  [INVOICE_STATUS.DRAFT]: "مسودة",
  [INVOICE_STATUS.SENT]: "مرسلة",
  [INVOICE_STATUS.PAID]: "مدفوعة",
  [INVOICE_STATUS.OVERDUE]: "متأخرة",
  [INVOICE_STATUS.CANCELLED]: "ملغاة",
}

// Product Status
export const PRODUCT_STATUS = {
  ACTIVE: "active",
  INACTIVE: "inactive",
  OUT_OF_STOCK: "out_of_stock",
  DISCONTINUED: "discontinued",
}

export const PRODUCT_STATUS_LABELS = {
  [PRODUCT_STATUS.ACTIVE]: "نشط",
  [PRODUCT_STATUS.INACTIVE]: "غير نشط",
  [PRODUCT_STATUS.OUT_OF_STOCK]: "نفد المخزون",
  [PRODUCT_STATUS.DISCONTINUED]: "متوقف",
}

// Stock Movement Types
export const MOVEMENT_TYPES = {
  IN: "in",
  OUT: "out",
  TRANSFER: "transfer",
  ADJUSTMENT: "adjustment",
  RETURN: "return",
}

export const MOVEMENT_TYPE_LABELS = {
  [MOVEMENT_TYPES.IN]: "وارد",
  [MOVEMENT_TYPES.OUT]: "صادر",
  [MOVEMENT_TYPES.TRANSFER]: "نقل",
  [MOVEMENT_TYPES.ADJUSTMENT]: "تعديل",
  [MOVEMENT_TYPES.RETURN]: "إرجاع",
}

// IoT Device Status
export const DEVICE_STATUS = {
  ONLINE: "online",
  OFFLINE: "offline",
  MAINTENANCE: "maintenance",
  ERROR: "error",
}

export const DEVICE_STATUS_LABELS = {
  [DEVICE_STATUS.ONLINE]: "متصل",
  [DEVICE_STATUS.OFFLINE]: "غير متصل",
  [DEVICE_STATUS.MAINTENANCE]: "صيانة",
  [DEVICE_STATUS.ERROR]: "خطأ",
}

// Alert Severity
export const ALERT_SEVERITY = {
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
  CRITICAL: "critical",
}

export const ALERT_SEVERITY_LABELS = {
  [ALERT_SEVERITY.LOW]: "منخفض",
  [ALERT_SEVERITY.MEDIUM]: "متوسط",
  [ALERT_SEVERITY.HIGH]: "عالي",
  [ALERT_SEVERITY.CRITICAL]: "حرج",
}

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  MAX_PAGE_SIZE: 100,
}

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: "dd/MM/yyyy",
  DISPLAY_WITH_TIME: "dd/MM/yyyy HH:mm",
  API: "yyyy-MM-dd",
  API_WITH_TIME: "yyyy-MM-dd'T'HH:mm:ss",
}

// Currency
export const CURRENCY = {
  SYMBOL: "ر.س",
  CODE: "SAR",
  DECIMAL_PLACES: 2,
}

// Validation Rules
export const VALIDATION = {
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_MAX_LENGTH: 128,
  PHONE_MIN_LENGTH: 10,
  PHONE_MAX_LENGTH: 15,
  NAME_MIN_LENGTH: 2,
  NAME_MAX_LENGTH: 50,
  EMAIL_MAX_LENGTH: 255,
  SKU_MIN_LENGTH: 3,
  SKU_MAX_LENGTH: 50,
}

// File Upload
export const FILE_UPLOAD = {
  MAX_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_IMAGE_TYPES: ["image/jpeg", "image/png", "image/webp", "image/gif"],
  ALLOWED_DOCUMENT_TYPES: [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ],
}

// Theme
export const THEME = {
  DEFAULT: "light",
  OPTIONS: ["light", "dark", "system"],
}

// Language
export const LANGUAGE = {
  DEFAULT: "ar",
  OPTIONS: ["ar", "en"],
  LABELS: {
    ar: "العربية",
    en: "English",
  },
}

// Routes (for navigation)
export const ROUTES = {
  HOME: "/dashboard",
  LOGIN: "/login",
  REGISTER: "/register",
  FORGOT_PASSWORD: "/forgot-password",
  PROFILE: "/profile",
  SETTINGS: "/settings",
  USERS: "/users",
  INVENTORY: "/inventory",
  SALES: "/sales",
  ACCOUNTING: "/accounting",
  IOT: "/iot",
  AI_ANALYTICS: "/ai-analytics",
}

// Permissions (for role-based access)
export const PERMISSIONS = {
  // Users
  USERS_READ: "users.read",
  USERS_WRITE: "users.write",
  USERS_DELETE: "users.delete",

  // Inventory
  INVENTORY_READ: "inventory.read",
  INVENTORY_WRITE: "inventory.write",
  INVENTORY_DELETE: "inventory.delete",

  // Sales
  SALES_READ: "sales.read",
  SALES_WRITE: "sales.write",
  SALES_DELETE: "sales.delete",

  // Accounting
  ACCOUNTING_READ: "accounting.read",
  ACCOUNTING_WRITE: "accounting.write",
  ACCOUNTING_DELETE: "accounting.delete",

  // Reports
  REPORTS_READ: "reports.read",
  REPORTS_EXPORT: "reports.export",

  // Settings
  SETTINGS_READ: "settings.read",
  SETTINGS_WRITE: "settings.write",
}

// Local Storage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: "access_token",
  REFRESH_TOKEN: "refresh_token",
  USER: "user",
  THEME: "theme",
  LANGUAGE: "language",
  SIDEBAR_STATE: "sidebar_state",
}

// Debounce Delays
export const DEBOUNCE_DELAYS = {
  SEARCH: 500,
  INPUT: 300,
  RESIZE: 250,
}

export default {
  API_CONFIG,
  APP_CONFIG,
  ROLES,
  ROLE_LABELS,
  USER_STATUS,
  USER_STATUS_LABELS,
  ORDER_STATUS,
  ORDER_STATUS_LABELS,
  INVOICE_STATUS,
  INVOICE_STATUS_LABELS,
  PRODUCT_STATUS,
  PRODUCT_STATUS_LABELS,
  MOVEMENT_TYPES,
  MOVEMENT_TYPE_LABELS,
  DEVICE_STATUS,
  DEVICE_STATUS_LABELS,
  ALERT_SEVERITY,
  ALERT_SEVERITY_LABELS,
  PAGINATION,
  DATE_FORMATS,
  CURRENCY,
  VALIDATION,
  FILE_UPLOAD,
  THEME,
  LANGUAGE,
  ROUTES,
  PERMISSIONS,
  STORAGE_KEYS,
  DEBOUNCE_DELAYS,
}
