/**
 * Services Index - فهرس الخدمات
 * Gaara ERP v12
 *
 * Central export for all API services.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 */

// Core API
export { default as api, createCrudService, apiHelpers } from './api'

// Tenant Service
export { default as tenantService } from './tenantService'

// Business Services
export { default as salesService } from './salesService'
export { default as inventoryService } from './inventoryService'
export { default as purchasingService } from './purchasingService'
export { default as customersService } from './customersService'

// Core Services
export { default as usersService } from './usersService'
export { default as rolesService } from './rolesService'
export { default as permissionsService } from './permissionsService'

// Utility Services
export { default as reportsService } from './reportsService'
