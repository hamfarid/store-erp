/**
 * Tenant Selector Component - محدد المستأجر
 * Gaara ERP v12
 *
 * Dropdown component for selecting/switching between tenants.
 * Used in the application header/sidebar.
 *
 * @author Global v35.0 Singularity
 * @version 1.0.0
 * @created 2026-01-17
 */

import { useState } from 'react'
import { Building, ChevronDown, Check, Plus, Settings, Loader2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

import { useTenant } from '@/contexts/TenantContext'

/**
 * Get initials from tenant name
 */
const getInitials = (name) => {
  if (!name) return 'T'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .substring(0, 2)
    .toUpperCase()
}

/**
 * Status badge variant mapping
 */
const statusVariants = {
  active: 'default',
  trial: 'outline',
  suspended: 'destructive',
  expired: 'secondary',
}

/**
 * Tenant Selector Component
 *
 * @param {Object} props
 * @param {boolean} props.showLabel - Show tenant name label
 * @param {string} props.variant - Button variant
 * @param {string} props.size - Button size
 */
export function TenantSelector({
  showLabel = true,
  variant = 'outline',
  size = 'default'
}) {
  const navigate = useNavigate()
  const {
    currentTenant,
    tenants,
    isLoading,
    switchTenant,
    refreshTenants
  } = useTenant()

  const [isOpen, setIsOpen] = useState(false)

  /**
   * Handle tenant selection
   */
  const handleSelectTenant = async (tenant) => {
    if (tenant.id === currentTenant?.id) {
      setIsOpen(false)
      return
    }

    await switchTenant(tenant.id)
    setIsOpen(false)

    // Optionally navigate to dashboard after switch
    // navigate('/dashboard')
  }

  /**
   * Handle manage tenants click
   */
  const handleManageTenants = () => {
    setIsOpen(false)
    navigate('/admin/tenants')
  }

  // Show loading state
  if (isLoading && !currentTenant) {
    return (
      <Button variant={variant} size={size} disabled>
        <Loader2 className="w-4 h-4 animate-spin" />
        {showLabel && <span className="mr-2">جاري التحميل...</span>}
      </Button>
    )
  }

  // No tenants available
  if (!isLoading && tenants.length === 0) {
    return (
      <Button
        variant={variant}
        size={size}
        onClick={() => navigate('/admin/tenants')}
      >
        <Plus className="w-4 h-4" />
        {showLabel && <span className="mr-2">إنشاء مستأجر</span>}
      </Button>
    )
  }

  return (
    <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant={variant} size={size} className="min-w-[200px] justify-between">
          <div className="flex items-center gap-2">
            {currentTenant?.logo ? (
              <Avatar className="w-6 h-6">
                <AvatarImage src={currentTenant.logo} alt={currentTenant.name} />
                <AvatarFallback className="text-xs">
                  {getInitials(currentTenant.name)}
                </AvatarFallback>
              </Avatar>
            ) : (
              <Building className="w-4 h-4 text-muted-foreground" />
            )}
            {showLabel && (
              <span className="truncate max-w-[120px]">
                {currentTenant?.name_ar || currentTenant?.name || 'اختر مستأجر'}
              </span>
            )}
          </div>
          <ChevronDown className="w-4 h-4 mr-2 opacity-50" />
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-[280px]">
        <DropdownMenuLabel className="flex items-center justify-between">
          <span>المستأجرون</span>
          <Badge variant="secondary" className="text-xs">
            {tenants.length}
          </Badge>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />

        {/* Tenant list */}
        <div className="max-h-[300px] overflow-y-auto">
          {tenants.map((tenant) => (
            <DropdownMenuItem
              key={tenant.id}
              onClick={() => handleSelectTenant(tenant)}
              className="flex items-center gap-3 py-2 cursor-pointer"
            >
              {/* Tenant avatar/icon */}
              {tenant.logo ? (
                <Avatar className="w-8 h-8">
                  <AvatarImage src={tenant.logo} alt={tenant.name} />
                  <AvatarFallback>{getInitials(tenant.name)}</AvatarFallback>
                </Avatar>
              ) : (
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                  <Building className="w-4 h-4 text-primary" />
                </div>
              )}

              {/* Tenant info */}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">
                  {tenant.name_ar || tenant.name}
                </p>
                <p className="text-xs text-muted-foreground truncate">
                  {tenant.slug}
                </p>
              </div>

              {/* Status badge */}
              <Badge
                variant={statusVariants[tenant.status] || 'secondary'}
                className="text-xs"
              >
                {tenant.status === 'active' ? 'نشط' :
                 tenant.status === 'trial' ? 'تجريبي' :
                 tenant.status === 'suspended' ? 'موقوف' : tenant.status}
              </Badge>

              {/* Selected indicator */}
              {tenant.id === currentTenant?.id && (
                <Check className="w-4 h-4 text-primary" />
              )}
            </DropdownMenuItem>
          ))}
        </div>

        <DropdownMenuSeparator />

        {/* Actions */}
        <DropdownMenuItem onClick={handleManageTenants}>
          <Settings className="w-4 h-4 ml-2" />
          إدارة المستأجرين
        </DropdownMenuItem>

        <DropdownMenuItem onClick={() => { setIsOpen(false); refreshTenants(); }}>
          <Loader2 className="w-4 h-4 ml-2" />
          تحديث القائمة
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

/**
 * Compact version of tenant selector (icon only)
 */
export function TenantSelectorCompact() {
  return <TenantSelector showLabel={false} size="icon" />
}

export default TenantSelector
