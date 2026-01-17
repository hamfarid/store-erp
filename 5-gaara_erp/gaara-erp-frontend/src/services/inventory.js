import api from "./api"

/**
 * Inventory Service
 * Handles all inventory management API calls
 */

// Products
export const getProducts = async (params = {}) => {
  const { page = 1, limit = 10, search = "", category = "", warehouse = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(search && { search }),
    ...(category && { category }),
    ...(warehouse && { warehouse }),
  })

  return api.get(`/inventory/products?${queryParams}`)
}

export const getProductById = async (productId) => {
  return api.get(`/inventory/products/${productId}`)
}

export const createProduct = async (productData) => {
  return api.post("/inventory/products", productData)
}

export const updateProduct = async (productId, productData) => {
  return api.put(`/inventory/products/${productId}`, productData)
}

export const deleteProduct = async (productId) => {
  return api.delete(`/inventory/products/${productId}`)
}

export const bulkUpdateProducts = async (productIds, updates) => {
  return api.post("/inventory/products/bulk-update", { productIds, updates })
}

// Warehouses
export const getWarehouses = async (params = {}) => {
  return api.get("/inventory/warehouses", { params })
}

export const getWarehouseById = async (warehouseId) => {
  return api.get(`/inventory/warehouses/${warehouseId}`)
}

export const createWarehouse = async (warehouseData) => {
  return api.post("/inventory/warehouses", warehouseData)
}

export const updateWarehouse = async (warehouseId, warehouseData) => {
  return api.put(`/inventory/warehouses/${warehouseId}`, warehouseData)
}

export const deleteWarehouse = async (warehouseId) => {
  return api.delete(`/inventory/warehouses/${warehouseId}`)
}

// Stock Movements
export const getMovements = async (params = {}) => {
  const { page = 1, limit = 20, type = "", product = "", warehouse = "", dateFrom = "", dateTo = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(type && { type }),
    ...(product && { product }),
    ...(warehouse && { warehouse }),
    ...(dateFrom && { dateFrom }),
    ...(dateTo && { dateTo }),
  })

  return api.get(`/inventory/movements?${queryParams}`)
}

export const createMovement = async (movementData) => {
  return api.post("/inventory/movements", movementData)
}

export const getMovementById = async (movementId) => {
  return api.get(`/inventory/movements/${movementId}`)
}

// Stock Levels
export const getStockLevels = async (warehouseId, params = {}) => {
  return api.get(`/inventory/warehouses/${warehouseId}/stock`, { params })
}

export const updateStockLevel = async (warehouseId, productId, quantity) => {
  return api.patch(`/inventory/warehouses/${warehouseId}/stock/${productId}`, { quantity })
}

// Reports
export const getInventoryReport = async (params = {}) => {
  return api.get("/inventory/reports/summary", { params })
}

export const getLowStockAlerts = async (params = {}) => {
  return api.get("/inventory/reports/low-stock", { params })
}

export const getStockValuation = async (params = {}) => {
  return api.get("/inventory/reports/valuation", { params })
}

// Categories
export const getCategories = async () => {
  return api.get("/inventory/categories")
}

export const createCategory = async (categoryData) => {
  return api.post("/inventory/categories", categoryData)
}

// Mock data for development
export const mockProducts = [
  {
    id: 1,
    name: "بذور طماطم",
    sku: "PROD-001",
    category: "بذور",
    price: 25.50,
    cost: 15.00,
    stock: 500,
    minStock: 100,
    warehouse: "مخزن الرئيسي",
    unit: "كيلو",
    status: "active",
  },
  {
    id: 2,
    name: "سماد NPK",
    sku: "PROD-002",
    category: "أسمدة",
    price: 120.00,
    cost: 80.00,
    stock: 300,
    minStock: 50,
    warehouse: "مخزن الرئيسي",
    unit: "كيس",
    status: "active",
  },
]

export default {
  getProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
  bulkUpdateProducts,
  getWarehouses,
  getWarehouseById,
  createWarehouse,
  updateWarehouse,
  deleteWarehouse,
  getMovements,
  createMovement,
  getMovementById,
  getStockLevels,
  updateStockLevel,
  getInventoryReport,
  getLowStockAlerts,
  getStockValuation,
  getCategories,
  createCategory,
  mockProducts,
}
