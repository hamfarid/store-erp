/**
 * Tenant Context - سياق المستأجر
 * Gaara ERP v12
 *
 * Provides tenant state management across the application.
 * Handles current tenant selection and tenant switching.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 * @created 2026-01-17
 */

import { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react'
import { toast } from 'sonner'
import tenantService from '@/services/tenantService'

/**
 * Tenant Context default values
 */
const TenantContext = createContext({
  // Current tenant
  currentTenant: null,
  setCurrentTenant: () => {},

  // All tenants user has access to
  tenants: [],

  // Loading states
  isLoading: false,
  isInitialized: false,

  // Actions
  refreshTenants: () => {},
  switchTenant: () => {},
  clearTenant: () => {},

  // Helpers
  hasTenantAccess: () => false,
  getCurrentTenantId: () => null,
})

/**
 * Tenant Provider Component
 * مزود سياق المستأجر
 *
 * Wraps the application to provide tenant context.
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 */
export function TenantProvider({ children }) {
  // State
  const [currentTenant, setCurrentTenantState] = useState(null)
  const [tenants, setTenants] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isInitialized, setIsInitialized] = useState(false)

  /**
   * Load tenants from API
   */
  const refreshTenants = useCallback(async () => {
    try {
      setIsLoading(true)
      const response = await tenantService.getTenants()

      if (response.success && response.data) {
        setTenants(response.data)

        // If no current tenant, try to restore from storage
        const storedTenantId = localStorage.getItem('current_tenant_id')
        if (!currentTenant && storedTenantId) {
          const stored = response.data.find(t => t.id === storedTenantId)
          if (stored) {
            setCurrentTenantState(stored)
            tenantService.setCurrentTenant(stored.id)
          }
        }

        // If still no tenant and user has tenants, select first one
        if (!currentTenant && !storedTenantId && response.data.length > 0) {
          const firstTenant = response.data[0]
          setCurrentTenantState(firstTenant)
          tenantService.setCurrentTenant(firstTenant.id)
          localStorage.setItem('current_tenant_id', firstTenant.id)
        }
      }
    } catch (error) {
      console.error('Error loading tenants:', error)
      // Don't show error toast on initial load
      if (isInitialized) {
        toast.error('فشل في تحميل المستأجرين')
      }
    } finally {
      setIsLoading(false)
      setIsInitialized(true)
    }
  }, [currentTenant, isInitialized])

  /**
   * Set current tenant and persist
   */
  const setCurrentTenant = useCallback((tenant) => {
    setCurrentTenantState(tenant)

    if (tenant) {
      // Set in service for API headers
      tenantService.setCurrentTenant(tenant.id)
      // Persist to localStorage
      localStorage.setItem('current_tenant_id', tenant.id)
      localStorage.setItem('current_tenant_slug', tenant.slug)
    } else {
      tenantService.clearCurrentTenant()
      localStorage.removeItem('current_tenant_id')
      localStorage.removeItem('current_tenant_slug')
    }
  }, [])

  /**
   * Switch to a different tenant
   */
  const switchTenant = useCallback(async (tenantId) => {
    const tenant = tenants.find(t => t.id === tenantId)

    if (!tenant) {
      toast.error('المستأجر غير موجود')
      return false
    }

    setCurrentTenant(tenant)
    toast.success(`تم التبديل إلى: ${tenant.name_ar || tenant.name}`)

    // Optionally reload page to refresh all data
    // window.location.reload()

    return true
  }, [tenants, setCurrentTenant])

  /**
   * Clear current tenant
   */
  const clearTenant = useCallback(() => {
    setCurrentTenant(null)
  }, [setCurrentTenant])

  /**
   * Check if user has access to a specific tenant
   */
  const hasTenantAccess = useCallback((tenantId) => {
    return tenants.some(t => t.id === tenantId)
  }, [tenants])

  /**
   * Get current tenant ID
   */
  const getCurrentTenantId = useCallback(() => {
    return currentTenant?.id || localStorage.getItem('current_tenant_id')
  }, [currentTenant])

  // Load tenants on mount
  useEffect(() => {
    refreshTenants()
  }, []) // Only on mount, not including refreshTenants

  // Restore tenant from storage on mount
  useEffect(() => {
    const storedTenantId = localStorage.getItem('current_tenant_id')
    if (storedTenantId && !currentTenant) {
      tenantService.setCurrentTenant(storedTenantId)
    }
  }, [currentTenant])

  // Memoize context value
  const contextValue = useMemo(() => ({
    currentTenant,
    setCurrentTenant,
    tenants,
    isLoading,
    isInitialized,
    refreshTenants,
    switchTenant,
    clearTenant,
    hasTenantAccess,
    getCurrentTenantId,
  }), [
    currentTenant,
    setCurrentTenant,
    tenants,
    isLoading,
    isInitialized,
    refreshTenants,
    switchTenant,
    clearTenant,
    hasTenantAccess,
    getCurrentTenantId,
  ])

  return (
    <TenantContext.Provider value={contextValue}>
      {children}
    </TenantContext.Provider>
  )
}

/**
 * Hook to use tenant context
 * خطاف لاستخدام سياق المستأجر
 *
 * @returns {Object} Tenant context value
 *
 * @example
 * const { currentTenant, switchTenant } = useTenant()
 */
export function useTenant() {
  const context = useContext(TenantContext)

  if (!context) {
    throw new Error('useTenant must be used within a TenantProvider')
  }

  return context
}

/**
 * Hook to get current tenant ID only
 * @returns {string|null} Current tenant ID
 */
export function useCurrentTenantId() {
  const { getCurrentTenantId } = useTenant()
  return getCurrentTenantId()
}

/**
 * Hook to check if tenant is selected
 * @returns {boolean} True if tenant is selected
 */
export function useHasTenant() {
  const { currentTenant } = useTenant()
  return currentTenant !== null
}

export default TenantContext
