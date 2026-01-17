/**
 * P1.25: Typed Frontend API Client
 * 
 * Auto-generated typed API client for the Store Management System.
 * Provides type-safe API calls with automatic error handling.
 */

// =============================================================================
// Types & Interfaces
// =============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta?: ResponseMeta;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  request_id?: string;
}

export interface ResponseMeta {
  timestamp: string;
  request_id: string;
  pagination?: PaginationMeta;
}

export interface PaginationMeta {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  meta: ResponseMeta & { pagination: PaginationMeta };
}

// Auth Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  role: string;
  role_id: number;
  permissions: string[];
  created_at: string;
  updated_at: string;
}

export interface Role {
  id: number;
  name: string;
  permissions: string[];
  created_at: string;
  updated_at: string;
}

// Product Types
export interface Product {
  id: number;
  name: string;
  sku: string;
  barcode?: string;
  description?: string;
  price: number;
  cost?: number;
  quantity: number;
  min_quantity?: number;
  category_id?: number;
  category_name?: string;
  brand_id?: number;
  brand_name?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductCreate {
  name: string;
  sku: string;
  barcode?: string;
  description?: string;
  price: number;
  cost?: number;
  quantity?: number;
  min_quantity?: number;
  category_id?: number;
  brand_id?: number;
}

export interface ProductUpdate extends Partial<ProductCreate> {}

// Category Types
export interface Category {
  id: number;
  name: string;
  description?: string;
  parent_id?: number;
  created_at: string;
  updated_at: string;
}

// Warehouse Types
export interface Warehouse {
  id: number;
  name: string;
  location?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Customer Types
export interface Customer {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  address?: string;
  tax_number?: string;
  credit_limit?: number;
  balance: number;
  created_at: string;
  updated_at: string;
}

export interface CustomerCreate {
  name: string;
  email?: string;
  phone?: string;
  address?: string;
  tax_number?: string;
  credit_limit?: number;
}

// Supplier Types
export interface Supplier {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  contact_person?: string;
  address?: string;
  tax_number?: string;
  balance: number;
  created_at: string;
  updated_at: string;
}

export interface SupplierCreate {
  name: string;
  email?: string;
  phone?: string;
  contact_person?: string;
  address?: string;
  tax_number?: string;
}

// Invoice Types
export interface Invoice {
  id: number;
  invoice_number: string;
  type: 'sale' | 'purchase' | 'return';
  customer_id?: number;
  customer_name?: string;
  supplier_id?: number;
  supplier_name?: string;
  subtotal: number;
  discount: number;
  tax: number;
  total: number;
  paid_amount: number;
  status: 'draft' | 'pending' | 'paid' | 'cancelled';
  items: InvoiceItem[];
  created_at: string;
  updated_at: string;
}

export interface InvoiceItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  discount: number;
  total: number;
}

export interface InvoiceCreate {
  type: 'sale' | 'purchase' | 'return';
  customer_id?: number;
  supplier_id?: number;
  discount?: number;
  tax?: number;
  items: InvoiceItemCreate[];
}

export interface InvoiceItemCreate {
  product_id: number;
  quantity: number;
  unit_price: number;
  discount?: number;
}

// Stock Movement Types
export interface StockMovement {
  id: number;
  product_id: number;
  product_name: string;
  warehouse_id: number;
  warehouse_name: string;
  quantity: number;
  type: 'in' | 'out' | 'adjustment' | 'transfer';
  reference_type?: string;
  reference_id?: number;
  notes?: string;
  created_by: number;
  created_at: string;
}

// Dashboard Types
export interface DashboardStats {
  total_products: number;
  total_customers: number;
  total_suppliers: number;
  low_stock_count: number;
  today_sales: number;
  today_purchases: number;
  monthly_revenue: number;
  monthly_profit: number;
}

// Query Parameters
export interface ListParams {
  page?: number;
  per_page?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface ProductListParams extends ListParams {
  category_id?: number;
  brand_id?: number;
  is_active?: boolean;
  low_stock?: boolean;
}

// =============================================================================
// API Client Class
// =============================================================================

export class ApiClient {
  private baseUrl: string;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
    this.loadTokens();
  }

  // Token Management
  private loadTokens(): void {
    if (typeof window !== 'undefined') {
      this.accessToken = localStorage.getItem('access_token');
      this.refreshToken = localStorage.getItem('refresh_token');
    }
  }

  private saveTokens(access: string, refresh: string): void {
    this.accessToken = access;
    this.refreshToken = refresh;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
    }
  }

  private clearTokens(): void {
    this.accessToken = null;
    this.refreshToken = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  // HTTP Methods
  private async request<T>(
    method: string,
    endpoint: string,
    options: {
      body?: unknown;
      params?: Record<string, string | number | boolean | undefined>;
      requiresAuth?: boolean;
    } = {}
  ): Promise<ApiResponse<T>> {
    const { body, params, requiresAuth = true } = options;

    // Build URL with query params
    let url = `${this.baseUrl}${endpoint}`;
    if (params) {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, String(value));
        }
      });
      const queryString = searchParams.toString();
      if (queryString) {
        url += `?${queryString}`;
      }
    }

    // Build headers
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (requiresAuth && this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    // Get CSRF token if available
    const csrfToken = this.getCsrfToken();
    if (csrfToken && ['POST', 'PUT', 'DELETE', 'PATCH'].includes(method)) {
      headers['X-CSRF-Token'] = csrfToken;
    }

    try {
      const response = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
        credentials: 'include',
      });

      // Handle 401 - try refresh token
      if (response.status === 401 && this.refreshToken && requiresAuth) {
        const refreshed = await this.refreshAccessToken();
        if (refreshed) {
          headers['Authorization'] = `Bearer ${this.accessToken}`;
          const retryResponse = await fetch(url, {
            method,
            headers,
            body: body ? JSON.stringify(body) : undefined,
            credentials: 'include',
          });
          return await retryResponse.json();
        }
      }

      return await response.json();
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'NETWORK_ERROR',
          message: error instanceof Error ? error.message : 'Network error',
        },
      };
    }
  }

  private getCsrfToken(): string | null {
    if (typeof document !== 'undefined') {
      const meta = document.querySelector('meta[name="csrf-token"]');
      return meta?.getAttribute('content') || null;
    }
    return null;
  }

  private async refreshAccessToken(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.refreshToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.data) {
          this.saveTokens(data.data.access_token, data.data.refresh_token);
          return true;
        }
      }
    } catch {
      // Refresh failed
    }

    this.clearTokens();
    return false;
  }

  // ==========================================================================
  // Auth Endpoints
  // ==========================================================================

  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    const response = await this.request<LoginResponse>('POST', '/auth/login', {
      body: credentials,
      requiresAuth: false,
    });

    if (response.success && response.data) {
      this.saveTokens(response.data.access_token, response.data.refresh_token);
    }

    return response;
  }

  async logout(): Promise<ApiResponse<void>> {
    const response = await this.request<void>('POST', '/auth/logout');
    this.clearTokens();
    return response;
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    return this.request<User>('GET', '/auth/me');
  }

  async changePassword(oldPassword: string, newPassword: string): Promise<ApiResponse<void>> {
    return this.request<void>('POST', '/auth/change-password', {
      body: { old_password: oldPassword, new_password: newPassword },
    });
  }

  // ==========================================================================
  // User Endpoints
  // ==========================================================================

  async getUsers(params?: ListParams): Promise<PaginatedResponse<User>> {
    return this.request<User[]>('GET', '/users', { params }) as Promise<PaginatedResponse<User>>;
  }

  async getUser(id: number): Promise<ApiResponse<User>> {
    return this.request<User>('GET', `/users/${id}`);
  }

  async createUser(user: Omit<User, 'id' | 'created_at' | 'updated_at'> & { password: string }): Promise<ApiResponse<User>> {
    return this.request<User>('POST', '/users', { body: user });
  }

  async updateUser(id: number, user: Partial<User>): Promise<ApiResponse<User>> {
    return this.request<User>('PUT', `/users/${id}`, { body: user });
  }

  async deleteUser(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/users/${id}`);
  }

  // ==========================================================================
  // Role Endpoints
  // ==========================================================================

  async getRoles(): Promise<ApiResponse<Role[]>> {
    return this.request<Role[]>('GET', '/roles');
  }

  async getRole(id: number): Promise<ApiResponse<Role>> {
    return this.request<Role>('GET', `/roles/${id}`);
  }

  async createRole(role: Omit<Role, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<Role>> {
    return this.request<Role>('POST', '/roles', { body: role });
  }

  async updateRole(id: number, role: Partial<Role>): Promise<ApiResponse<Role>> {
    return this.request<Role>('PUT', `/roles/${id}`, { body: role });
  }

  async deleteRole(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/roles/${id}`);
  }

  // ==========================================================================
  // Product Endpoints
  // ==========================================================================

  async getProducts(params?: ProductListParams): Promise<PaginatedResponse<Product>> {
    return this.request<Product[]>('GET', '/products', { params }) as Promise<PaginatedResponse<Product>>;
  }

  async getProduct(id: number): Promise<ApiResponse<Product>> {
    return this.request<Product>('GET', `/products/${id}`);
  }

  async createProduct(product: ProductCreate): Promise<ApiResponse<Product>> {
    return this.request<Product>('POST', '/products', { body: product });
  }

  async updateProduct(id: number, product: ProductUpdate): Promise<ApiResponse<Product>> {
    return this.request<Product>('PUT', `/products/${id}`, { body: product });
  }

  async deleteProduct(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/products/${id}`);
  }

  async searchProducts(query: string): Promise<ApiResponse<Product[]>> {
    return this.request<Product[]>('GET', '/products/search', { params: { q: query } });
  }

  // ==========================================================================
  // Category Endpoints
  // ==========================================================================

  async getCategories(): Promise<ApiResponse<Category[]>> {
    return this.request<Category[]>('GET', '/categories');
  }

  async getCategory(id: number): Promise<ApiResponse<Category>> {
    return this.request<Category>('GET', `/categories/${id}`);
  }

  async createCategory(category: Omit<Category, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<Category>> {
    return this.request<Category>('POST', '/categories', { body: category });
  }

  async updateCategory(id: number, category: Partial<Category>): Promise<ApiResponse<Category>> {
    return this.request<Category>('PUT', `/categories/${id}`, { body: category });
  }

  async deleteCategory(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/categories/${id}`);
  }

  // ==========================================================================
  // Warehouse Endpoints
  // ==========================================================================

  async getWarehouses(): Promise<ApiResponse<Warehouse[]>> {
    return this.request<Warehouse[]>('GET', '/warehouses');
  }

  async getWarehouse(id: number): Promise<ApiResponse<Warehouse>> {
    return this.request<Warehouse>('GET', `/warehouses/${id}`);
  }

  async createWarehouse(warehouse: Omit<Warehouse, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<Warehouse>> {
    return this.request<Warehouse>('POST', '/warehouses', { body: warehouse });
  }

  async updateWarehouse(id: number, warehouse: Partial<Warehouse>): Promise<ApiResponse<Warehouse>> {
    return this.request<Warehouse>('PUT', `/warehouses/${id}`, { body: warehouse });
  }

  async deleteWarehouse(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/warehouses/${id}`);
  }

  // ==========================================================================
  // Customer Endpoints
  // ==========================================================================

  async getCustomers(params?: ListParams): Promise<PaginatedResponse<Customer>> {
    return this.request<Customer[]>('GET', '/customers', { params }) as Promise<PaginatedResponse<Customer>>;
  }

  async getCustomer(id: number): Promise<ApiResponse<Customer>> {
    return this.request<Customer>('GET', `/customers/${id}`);
  }

  async createCustomer(customer: CustomerCreate): Promise<ApiResponse<Customer>> {
    return this.request<Customer>('POST', '/customers', { body: customer });
  }

  async updateCustomer(id: number, customer: Partial<CustomerCreate>): Promise<ApiResponse<Customer>> {
    return this.request<Customer>('PUT', `/customers/${id}`, { body: customer });
  }

  async deleteCustomer(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/customers/${id}`);
  }

  // ==========================================================================
  // Supplier Endpoints
  // ==========================================================================

  async getSuppliers(params?: ListParams): Promise<PaginatedResponse<Supplier>> {
    return this.request<Supplier[]>('GET', '/suppliers', { params }) as Promise<PaginatedResponse<Supplier>>;
  }

  async getSupplier(id: number): Promise<ApiResponse<Supplier>> {
    return this.request<Supplier>('GET', `/suppliers/${id}`);
  }

  async createSupplier(supplier: SupplierCreate): Promise<ApiResponse<Supplier>> {
    return this.request<Supplier>('POST', '/suppliers', { body: supplier });
  }

  async updateSupplier(id: number, supplier: Partial<SupplierCreate>): Promise<ApiResponse<Supplier>> {
    return this.request<Supplier>('PUT', `/suppliers/${id}`, { body: supplier });
  }

  async deleteSupplier(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/suppliers/${id}`);
  }

  // ==========================================================================
  // Invoice Endpoints
  // ==========================================================================

  async getInvoices(params?: ListParams & { type?: string; status?: string }): Promise<PaginatedResponse<Invoice>> {
    return this.request<Invoice[]>('GET', '/invoices', { params }) as Promise<PaginatedResponse<Invoice>>;
  }

  async getInvoice(id: number): Promise<ApiResponse<Invoice>> {
    return this.request<Invoice>('GET', `/invoices/${id}`);
  }

  async createInvoice(invoice: InvoiceCreate): Promise<ApiResponse<Invoice>> {
    return this.request<Invoice>('POST', '/invoices', { body: invoice });
  }

  async updateInvoice(id: number, invoice: Partial<InvoiceCreate>): Promise<ApiResponse<Invoice>> {
    return this.request<Invoice>('PUT', `/invoices/${id}`, { body: invoice });
  }

  async deleteInvoice(id: number): Promise<ApiResponse<void>> {
    return this.request<void>('DELETE', `/invoices/${id}`);
  }

  async payInvoice(id: number, amount: number): Promise<ApiResponse<Invoice>> {
    return this.request<Invoice>('POST', `/invoices/${id}/pay`, { body: { amount } });
  }

  // ==========================================================================
  // Stock Movement Endpoints
  // ==========================================================================

  async getStockMovements(params?: ListParams & { product_id?: number; warehouse_id?: number }): Promise<PaginatedResponse<StockMovement>> {
    return this.request<StockMovement[]>('GET', '/stock-movements', { params }) as Promise<PaginatedResponse<StockMovement>>;
  }

  async createStockMovement(movement: Omit<StockMovement, 'id' | 'product_name' | 'warehouse_name' | 'created_by' | 'created_at'>): Promise<ApiResponse<StockMovement>> {
    return this.request<StockMovement>('POST', '/stock-movements', { body: movement });
  }

  // ==========================================================================
  // Dashboard Endpoints
  // ==========================================================================

  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    return this.request<DashboardStats>('GET', '/dashboard/stats');
  }

  async getLowStockProducts(limit?: number): Promise<ApiResponse<Product[]>> {
    return this.request<Product[]>('GET', '/dashboard/low-stock', { params: { limit } });
  }

  async getRecentInvoices(limit?: number): Promise<ApiResponse<Invoice[]>> {
    return this.request<Invoice[]>('GET', '/dashboard/recent-invoices', { params: { limit } });
  }

  // ==========================================================================
  // RAG Endpoints
  // ==========================================================================

  async queryRAG(query: string, topK?: number): Promise<ApiResponse<{ results: Array<{ text: string; score: number; meta?: Record<string, unknown> }> }>> {
    return this.request<{ results: Array<{ text: string; score: number; meta?: Record<string, unknown> }> }>('POST', '/rag/query', {
      body: { query, top_k: topK },
    });
  }
}

// =============================================================================
// Default Export
// =============================================================================

export const api = new ApiClient();
export default api;
