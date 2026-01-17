/**
 * Application TypeScript Definitions
 * @file frontend/src/types/index.d.ts
 * 
 * تعريفات TypeScript للتطبيق
 */

// ============================================
// User Types
// ============================================
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  phone?: string;
  role: UserRole;
  permissions: string[];
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

export type UserRole = 
  | 'super_admin'
  | 'admin'
  | 'manager'
  | 'accountant'
  | 'cashier'
  | 'inventory'
  | 'sales'
  | 'viewer';

// ============================================
// Product Types
// ============================================
export interface Product {
  id: number;
  sku: string;
  barcode?: string;
  name: string;
  name_en?: string;
  description?: string;
  category_id: number;
  category?: Category;
  unit_id: number;
  unit?: Unit;
  cost_price: number;
  selling_price: number;
  min_stock: number;
  max_stock?: number;
  current_stock: number;
  tax_type: TaxType;
  is_active: boolean;
  has_lots: boolean;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  name_en?: string;
  parent_id?: number;
  description?: string;
  is_active: boolean;
}

export interface Unit {
  id: number;
  name: string;
  name_en?: string;
  symbol: string;
  is_base: boolean;
}

export type TaxType = 'vat' | 'exempt' | 'zero_rated';

// ============================================
// Lot Types
// ============================================
export interface Lot {
  id: number;
  lot_number: string;
  product_id: number;
  product?: Product;
  warehouse_id: number;
  warehouse?: Warehouse;
  quantity: number;
  cost_price: number;
  expiry_date?: string;
  production_date?: string;
  supplier_id?: number;
  purchase_invoice_id?: number;
  status: LotStatus;
  created_at: string;
}

export type LotStatus = 
  | 'active'
  | 'expired'
  | 'expiring_soon'
  | 'reserved'
  | 'depleted';

// ============================================
// Warehouse Types
// ============================================
export interface Warehouse {
  id: number;
  code: string;
  name: string;
  address?: string;
  manager_id?: number;
  is_active: boolean;
  is_default: boolean;
}

// ============================================
// Invoice Types
// ============================================
export interface Invoice {
  id: number;
  invoice_number: string;
  invoice_type: InvoiceType;
  customer_id?: number;
  customer?: Customer;
  supplier_id?: number;
  supplier?: Supplier;
  warehouse_id: number;
  warehouse?: Warehouse;
  subtotal: number;
  discount_amount: number;
  discount_percentage: number;
  tax_amount: number;
  total_amount: number;
  paid_amount: number;
  due_amount: number;
  status: InvoiceStatus;
  payment_method: PaymentMethod;
  notes?: string;
  items: InvoiceItem[];
  created_at: string;
  due_date?: string;
}

export interface InvoiceItem {
  id: number;
  product_id: number;
  product?: Product;
  lot_id?: number;
  lot?: Lot;
  quantity: number;
  unit_price: number;
  discount: number;
  tax_amount: number;
  total: number;
}

export type InvoiceType = 'sale' | 'purchase' | 'sale_return' | 'purchase_return';

export type InvoiceStatus = 
  | 'draft'
  | 'pending'
  | 'paid'
  | 'partial'
  | 'overdue'
  | 'cancelled'
  | 'refunded';

export type PaymentMethod = 
  | 'cash'
  | 'card'
  | 'bank_transfer'
  | 'check'
  | 'credit'
  | 'mada'
  | 'visa'
  | 'mastercard'
  | 'apple_pay'
  | 'stc_pay';

// ============================================
// Customer/Supplier Types
// ============================================
export interface Customer {
  id: number;
  code: string;
  name: string;
  phone?: string;
  email?: string;
  address?: string;
  tax_number?: string;
  credit_limit: number;
  balance: number;
  is_active: boolean;
}

export interface Supplier {
  id: number;
  code: string;
  name: string;
  phone?: string;
  email?: string;
  address?: string;
  tax_number?: string;
  balance: number;
  is_active: boolean;
}

// ============================================
// Report Types
// ============================================
export interface ReportFilter {
  startDate?: string;
  endDate?: string;
  warehouseId?: number;
  categoryId?: number;
  customerId?: number;
  supplierId?: number;
  productId?: number;
  status?: string;
}

export interface SalesReport {
  period: string;
  total_sales: number;
  total_returns: number;
  net_sales: number;
  cost_of_goods: number;
  gross_profit: number;
  profit_margin: number;
  items_sold: number;
  transactions_count: number;
}

export interface InventoryReport {
  product_id: number;
  product_name: string;
  category_name: string;
  current_stock: number;
  min_stock: number;
  stock_value: number;
  status: string;
}

// ============================================
// API Response Types
// ============================================
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// ============================================
// Form Types
// ============================================
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'number' | 'email' | 'password' | 'select' | 'textarea' | 'date' | 'checkbox';
  required?: boolean;
  placeholder?: string;
  options?: { value: string | number; label: string }[];
  validation?: {
    min?: number;
    max?: number;
    minLength?: number;
    maxLength?: number;
    pattern?: string;
  };
}

// ============================================
// Notification Types
// ============================================
export interface Notification {
  id: number;
  type: NotificationType;
  title: string;
  message: string;
  read: boolean;
  created_at: string;
  link?: string;
}

export type NotificationType = 
  | 'info'
  | 'success'
  | 'warning'
  | 'error'
  | 'low_stock'
  | 'expiry'
  | 'payment_due';

// ============================================
// Settings Types
// ============================================
export interface SystemSettings {
  company_name: string;
  company_name_en?: string;
  logo_url?: string;
  address?: string;
  phone?: string;
  email?: string;
  tax_number?: string;
  commercial_register?: string;
  currency: string;
  timezone: string;
  date_format: string;
  fiscal_year_start: string;
  default_tax_rate: number;
  low_stock_threshold: number;
  expiry_warning_days: number;
}

// ============================================
// Dashboard Types
// ============================================
export interface DashboardStats {
  sales_today: number;
  sales_this_month: number;
  total_customers: number;
  total_products: number;
  low_stock_items: number;
  expiring_lots: number;
  pending_payments: number;
  top_products: TopProduct[];
  recent_sales: Invoice[];
}

export interface TopProduct {
  product_id: number;
  product_name: string;
  quantity_sold: number;
  revenue: number;
}
