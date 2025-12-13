/**
 * P1.27: API Request/Response Validators
 * 
 * Runtime validation for API requests and responses using Zod schemas.
 * Ensures type safety at runtime and provides detailed error messages.
 */

import { z } from 'zod';

// =============================================================================
// Common Schemas
// =============================================================================

export const ApiErrorSchema = z.object({
  code: z.string(),
  message: z.string(),
  details: z.record(z.unknown()).optional(),
  request_id: z.string().optional(),
});

export const PaginationMetaSchema = z.object({
  page: z.number().int().positive(),
  per_page: z.number().int().positive(),
  total: z.number().int().nonnegative(),
  total_pages: z.number().int().nonnegative(),
});

export const ResponseMetaSchema = z.object({
  timestamp: z.string().datetime().optional(),
  request_id: z.string().optional(),
  pagination: PaginationMetaSchema.optional(),
});

export const ApiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    data: dataSchema.optional(),
    error: ApiErrorSchema.optional(),
    meta: ResponseMetaSchema.optional(),
  });

export const PaginatedResponseSchema = <T extends z.ZodTypeAny>(itemSchema: T) =>
  z.object({
    success: z.boolean(),
    data: z.array(itemSchema).optional(),
    error: ApiErrorSchema.optional(),
    meta: ResponseMetaSchema.extend({
      pagination: PaginationMetaSchema,
    }),
  });

// =============================================================================
// Auth Schemas
// =============================================================================

export const LoginRequestSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be at most 50 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password must be at most 128 characters'),
});

export const UserSchema = z.object({
  id: z.number().int().positive(),
  username: z.string(),
  email: z.string().email(),
  full_name: z.string().optional().nullable(),
  is_active: z.boolean(),
  role: z.string(),
  role_id: z.number().int().positive(),
  permissions: z.array(z.string()),
  created_at: z.string(),
  updated_at: z.string(),
});

export const LoginResponseSchema = z.object({
  access_token: z.string().min(1),
  refresh_token: z.string().min(1),
  user: UserSchema,
});

export const RoleSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  permissions: z.array(z.string()),
  created_at: z.string(),
  updated_at: z.string(),
});

export const ChangePasswordRequestSchema = z.object({
  old_password: z.string().min(8),
  new_password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number')
    .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character'),
  confirm_password: z.string(),
}).refine((data) => data.new_password === data.confirm_password, {
  message: 'Passwords do not match',
  path: ['confirm_password'],
});

// =============================================================================
// Product Schemas
// =============================================================================

export const ProductSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  sku: z.string(),
  barcode: z.string().optional().nullable(),
  description: z.string().optional().nullable(),
  price: z.number().nonnegative(),
  cost: z.number().nonnegative().optional().nullable(),
  quantity: z.number().int().nonnegative(),
  min_quantity: z.number().int().nonnegative().optional().nullable(),
  category_id: z.number().int().positive().optional().nullable(),
  category_name: z.string().optional().nullable(),
  brand_id: z.number().int().positive().optional().nullable(),
  brand_name: z.string().optional().nullable(),
  is_active: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const ProductCreateSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(200, 'Name must be at most 200 characters'),
  sku: z.string()
    .min(1, 'SKU is required')
    .max(50, 'SKU must be at most 50 characters')
    .regex(/^[A-Z0-9-]+$/i, 'SKU can only contain letters, numbers, and hyphens'),
  barcode: z.string().max(50).optional().nullable(),
  description: z.string().max(2000).optional().nullable(),
  price: z.number()
    .nonnegative('Price must be non-negative')
    .max(999999999, 'Price is too large'),
  cost: z.number().nonnegative().optional().nullable(),
  quantity: z.number().int().nonnegative().optional().default(0),
  min_quantity: z.number().int().nonnegative().optional().nullable(),
  category_id: z.number().int().positive().optional().nullable(),
  brand_id: z.number().int().positive().optional().nullable(),
});

export const ProductUpdateSchema = ProductCreateSchema.partial();

// =============================================================================
// Category Schemas
// =============================================================================

export const CategorySchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  description: z.string().optional().nullable(),
  parent_id: z.number().int().positive().optional().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const CategoryCreateSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name must be at most 100 characters'),
  description: z.string().max(500).optional().nullable(),
  parent_id: z.number().int().positive().optional().nullable(),
});

// =============================================================================
// Warehouse Schemas
// =============================================================================

export const WarehouseSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  location: z.string().optional().nullable(),
  is_active: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const WarehouseCreateSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name must be at most 100 characters'),
  location: z.string().max(500).optional().nullable(),
  is_active: z.boolean().optional().default(true),
});

// =============================================================================
// Customer Schemas
// =============================================================================

export const CustomerSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  email: z.string().email().optional().nullable(),
  phone: z.string().optional().nullable(),
  address: z.string().optional().nullable(),
  tax_number: z.string().optional().nullable(),
  credit_limit: z.number().nonnegative().optional().nullable(),
  balance: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const CustomerCreateSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(200, 'Name must be at most 200 characters'),
  email: z.string().email('Invalid email format').optional().nullable(),
  phone: z.string()
    .regex(/^[\d+\-\s()]+$/, 'Invalid phone format')
    .optional()
    .nullable(),
  address: z.string().max(1000).optional().nullable(),
  tax_number: z.string().max(50).optional().nullable(),
  credit_limit: z.number().nonnegative().optional().nullable(),
});

// =============================================================================
// Supplier Schemas
// =============================================================================

export const SupplierSchema = z.object({
  id: z.number().int().positive(),
  name: z.string(),
  email: z.string().email().optional().nullable(),
  phone: z.string().optional().nullable(),
  contact_person: z.string().optional().nullable(),
  address: z.string().optional().nullable(),
  tax_number: z.string().optional().nullable(),
  balance: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const SupplierCreateSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(200, 'Name must be at most 200 characters'),
  email: z.string().email('Invalid email format').optional().nullable(),
  phone: z.string()
    .regex(/^[\d+\-\s()]+$/, 'Invalid phone format')
    .optional()
    .nullable(),
  contact_person: z.string().max(200).optional().nullable(),
  address: z.string().max(1000).optional().nullable(),
  tax_number: z.string().max(50).optional().nullable(),
});

// =============================================================================
// Invoice Schemas
// =============================================================================

export const InvoiceTypeSchema = z.enum(['sale', 'purchase', 'return']);
export const InvoiceStatusSchema = z.enum(['draft', 'pending', 'paid', 'cancelled']);

export const InvoiceItemSchema = z.object({
  id: z.number().int().positive(),
  product_id: z.number().int().positive(),
  product_name: z.string(),
  quantity: z.number().int().positive(),
  unit_price: z.number().nonnegative(),
  discount: z.number().nonnegative(),
  total: z.number().nonnegative(),
});

export const InvoiceSchema = z.object({
  id: z.number().int().positive(),
  invoice_number: z.string(),
  type: InvoiceTypeSchema,
  customer_id: z.number().int().positive().optional().nullable(),
  customer_name: z.string().optional().nullable(),
  supplier_id: z.number().int().positive().optional().nullable(),
  supplier_name: z.string().optional().nullable(),
  subtotal: z.number().nonnegative(),
  discount: z.number().nonnegative(),
  tax: z.number().nonnegative(),
  total: z.number().nonnegative(),
  paid_amount: z.number().nonnegative(),
  status: InvoiceStatusSchema,
  items: z.array(InvoiceItemSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const InvoiceItemCreateSchema = z.object({
  product_id: z.number().int().positive('Product is required'),
  quantity: z.number().int().positive('Quantity must be at least 1'),
  unit_price: z.number().nonnegative('Unit price must be non-negative'),
  discount: z.number().nonnegative().optional().default(0),
});

export const InvoiceCreateSchema = z.object({
  type: InvoiceTypeSchema,
  customer_id: z.number().int().positive().optional().nullable(),
  supplier_id: z.number().int().positive().optional().nullable(),
  discount: z.number().nonnegative().optional().default(0),
  tax: z.number().nonnegative().optional().default(0),
  items: z.array(InvoiceItemCreateSchema)
    .min(1, 'At least one item is required'),
}).refine(
  (data) => {
    if (data.type === 'sale') return data.customer_id != null;
    if (data.type === 'purchase') return data.supplier_id != null;
    return true;
  },
  {
    message: 'Customer is required for sales, Supplier is required for purchases',
    path: ['customer_id'],
  }
);

// =============================================================================
// Stock Movement Schemas
// =============================================================================

export const StockMovementTypeSchema = z.enum(['in', 'out', 'adjustment', 'transfer']);

export const StockMovementSchema = z.object({
  id: z.number().int().positive(),
  product_id: z.number().int().positive(),
  product_name: z.string(),
  warehouse_id: z.number().int().positive(),
  warehouse_name: z.string(),
  quantity: z.number().int(),
  type: StockMovementTypeSchema,
  reference_type: z.string().optional().nullable(),
  reference_id: z.number().int().positive().optional().nullable(),
  notes: z.string().optional().nullable(),
  created_by: z.number().int().positive(),
  created_at: z.string(),
});

export const StockMovementCreateSchema = z.object({
  product_id: z.number().int().positive('Product is required'),
  warehouse_id: z.number().int().positive('Warehouse is required'),
  quantity: z.number().int().nonzero('Quantity cannot be zero'),
  type: StockMovementTypeSchema,
  reference_type: z.string().optional().nullable(),
  reference_id: z.number().int().positive().optional().nullable(),
  notes: z.string().max(1000).optional().nullable(),
});

// =============================================================================
// Dashboard Schemas
// =============================================================================

export const DashboardStatsSchema = z.object({
  total_products: z.number().int().nonnegative(),
  total_customers: z.number().int().nonnegative(),
  total_suppliers: z.number().int().nonnegative(),
  low_stock_count: z.number().int().nonnegative(),
  today_sales: z.number().nonnegative(),
  today_purchases: z.number().nonnegative(),
  monthly_revenue: z.number().nonnegative(),
  monthly_profit: z.number(),
});

// =============================================================================
// RAG Schemas
// =============================================================================

export const RAGQueryRequestSchema = z.object({
  query: z.string()
    .min(1, 'Query is required')
    .max(1000, 'Query is too long'),
  top_k: z.number().int().positive().max(50).optional().default(5),
});

export const RAGResultSchema = z.object({
  text: z.string(),
  score: z.number(),
  meta: z.record(z.unknown()).optional(),
});

export const RAGQueryResponseSchema = z.object({
  results: z.array(RAGResultSchema),
});

// =============================================================================
// Query Parameter Schemas
// =============================================================================

export const ListParamsSchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  per_page: z.coerce.number().int().positive().max(100).optional().default(20),
  search: z.string().max(200).optional(),
  sort_by: z.string().optional(),
  sort_order: z.enum(['asc', 'desc']).optional().default('asc'),
});

export const ProductListParamsSchema = ListParamsSchema.extend({
  category_id: z.coerce.number().int().positive().optional(),
  brand_id: z.coerce.number().int().positive().optional(),
  is_active: z.coerce.boolean().optional(),
  low_stock: z.coerce.boolean().optional(),
});

// =============================================================================
// Validation Helper Functions
// =============================================================================

export type ValidationResult<T> = 
  | { success: true; data: T }
  | { success: false; errors: z.ZodError };

export function validate<T>(schema: z.ZodSchema<T>, data: unknown): ValidationResult<T> {
  const result = schema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data };
  }
  return { success: false, errors: result.error };
}

export function formatValidationErrors(error: z.ZodError): Record<string, string[]> {
  const errors: Record<string, string[]> = {};
  
  for (const issue of error.issues) {
    const path = issue.path.join('.') || 'root';
    if (!errors[path]) {
      errors[path] = [];
    }
    errors[path].push(issue.message);
  }
  
  return errors;
}

export function validateOrThrow<T>(schema: z.ZodSchema<T>, data: unknown): T {
  return schema.parse(data);
}

// =============================================================================
// Type Exports
// =============================================================================

export type LoginRequest = z.infer<typeof LoginRequestSchema>;
export type User = z.infer<typeof UserSchema>;
export type LoginResponse = z.infer<typeof LoginResponseSchema>;
export type Role = z.infer<typeof RoleSchema>;
export type Product = z.infer<typeof ProductSchema>;
export type ProductCreate = z.infer<typeof ProductCreateSchema>;
export type Category = z.infer<typeof CategorySchema>;
export type Warehouse = z.infer<typeof WarehouseSchema>;
export type Customer = z.infer<typeof CustomerSchema>;
export type CustomerCreate = z.infer<typeof CustomerCreateSchema>;
export type Supplier = z.infer<typeof SupplierSchema>;
export type SupplierCreate = z.infer<typeof SupplierCreateSchema>;
export type Invoice = z.infer<typeof InvoiceSchema>;
export type InvoiceCreate = z.infer<typeof InvoiceCreateSchema>;
export type StockMovement = z.infer<typeof StockMovementSchema>;
export type StockMovementCreate = z.infer<typeof StockMovementCreateSchema>;
export type DashboardStats = z.infer<typeof DashboardStatsSchema>;
export type RAGQueryRequest = z.infer<typeof RAGQueryRequestSchema>;

