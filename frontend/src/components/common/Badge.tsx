/**
 * P3.94: Badge Component
 * 
 * Versatile badge component for status indicators, counts, and labels.
 */

import React from 'react';

// =============================================================================
// Types
// =============================================================================

type BadgeVariant = 'solid' | 'outline' | 'subtle';
type BadgeColor = 'gray' | 'red' | 'orange' | 'yellow' | 'green' | 'teal' | 'blue' | 'indigo' | 'purple' | 'pink';
type BadgeSize = 'sm' | 'md' | 'lg';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  color?: BadgeColor;
  size?: BadgeSize;
  rounded?: boolean;
  dot?: boolean;
  removable?: boolean;
  onRemove?: () => void;
  className?: string;
}

// =============================================================================
// Color Styles
// =============================================================================

const colorStyles: Record<BadgeColor, Record<BadgeVariant, string>> = {
  gray: {
    solid: 'bg-gray-600 text-white',
    outline: 'border border-gray-600 text-gray-600',
    subtle: 'bg-gray-100 text-gray-700',
  },
  red: {
    solid: 'bg-red-600 text-white',
    outline: 'border border-red-600 text-red-600',
    subtle: 'bg-red-100 text-red-700',
  },
  orange: {
    solid: 'bg-orange-500 text-white',
    outline: 'border border-orange-500 text-orange-500',
    subtle: 'bg-orange-100 text-orange-700',
  },
  yellow: {
    solid: 'bg-yellow-500 text-white',
    outline: 'border border-yellow-500 text-yellow-600',
    subtle: 'bg-yellow-100 text-yellow-700',
  },
  green: {
    solid: 'bg-green-600 text-white',
    outline: 'border border-green-600 text-green-600',
    subtle: 'bg-green-100 text-green-700',
  },
  teal: {
    solid: 'bg-teal-600 text-white',
    outline: 'border border-teal-600 text-teal-600',
    subtle: 'bg-teal-100 text-teal-700',
  },
  blue: {
    solid: 'bg-blue-600 text-white',
    outline: 'border border-blue-600 text-blue-600',
    subtle: 'bg-blue-100 text-blue-700',
  },
  indigo: {
    solid: 'bg-indigo-600 text-white',
    outline: 'border border-indigo-600 text-indigo-600',
    subtle: 'bg-indigo-100 text-indigo-700',
  },
  purple: {
    solid: 'bg-purple-600 text-white',
    outline: 'border border-purple-600 text-purple-600',
    subtle: 'bg-purple-100 text-purple-700',
  },
  pink: {
    solid: 'bg-pink-600 text-white',
    outline: 'border border-pink-600 text-pink-600',
    subtle: 'bg-pink-100 text-pink-700',
  },
};

const dotColors: Record<BadgeColor, string> = {
  gray: 'bg-gray-500',
  red: 'bg-red-500',
  orange: 'bg-orange-500',
  yellow: 'bg-yellow-500',
  green: 'bg-green-500',
  teal: 'bg-teal-500',
  blue: 'bg-blue-500',
  indigo: 'bg-indigo-500',
  purple: 'bg-purple-500',
  pink: 'bg-pink-500',
};

// =============================================================================
// Badge Component
// =============================================================================

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'subtle',
  color = 'gray',
  size = 'md',
  rounded = false,
  dot = false,
  removable = false,
  onRemove,
  className = '',
}) => {
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-sm',
    lg: 'px-3 py-1 text-sm',
  };

  return (
    <span
      className={`
        inline-flex items-center gap-1.5
        font-medium
        ${sizeClasses[size]}
        ${rounded ? 'rounded-full' : 'rounded-md'}
        ${colorStyles[color][variant]}
        ${className}
      `}
    >
      {dot && (
        <span className={`w-1.5 h-1.5 rounded-full ${dotColors[color]}`} />
      )}
      {children}
      {removable && (
        <button
          type="button"
          onClick={onRemove}
          className="ml-1 -mr-0.5 h-4 w-4 rounded-full inline-flex items-center justify-center hover:bg-black/10"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </span>
  );
};

// =============================================================================
// Status Badge
// =============================================================================

type StatusType = 'success' | 'warning' | 'error' | 'info' | 'pending' | 'inactive';

interface StatusBadgeProps {
  status: StatusType;
  label?: string;
  size?: BadgeSize;
  className?: string;
}

const statusConfig: Record<StatusType, { color: BadgeColor; label: string; labelAr: string }> = {
  success: { color: 'green', label: 'Success', labelAr: 'ناجح' },
  warning: { color: 'yellow', label: 'Warning', labelAr: 'تحذير' },
  error: { color: 'red', label: 'Error', labelAr: 'خطأ' },
  info: { color: 'blue', label: 'Info', labelAr: 'معلومات' },
  pending: { color: 'orange', label: 'Pending', labelAr: 'معلق' },
  inactive: { color: 'gray', label: 'Inactive', labelAr: 'غير نشط' },
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  label,
  size = 'md',
  className = '',
}) => {
  const config = statusConfig[status];
  
  return (
    <Badge
      color={config.color}
      variant="subtle"
      size={size}
      dot
      className={className}
    >
      {label || config.labelAr}
    </Badge>
  );
};

// =============================================================================
// Count Badge
// =============================================================================

interface CountBadgeProps {
  count: number;
  max?: number;
  color?: BadgeColor;
  size?: BadgeSize;
  className?: string;
}

export const CountBadge: React.FC<CountBadgeProps> = ({
  count,
  max = 99,
  color = 'red',
  size = 'sm',
  className = '',
}) => {
  const displayCount = count > max ? `${max}+` : count;
  
  return (
    <Badge
      color={color}
      variant="solid"
      size={size}
      rounded
      className={`min-w-[20px] justify-center ${className}`}
    >
      {displayCount}
    </Badge>
  );
};

// =============================================================================
// Badge Group
// =============================================================================

interface BadgeGroupProps {
  children: React.ReactNode;
  className?: string;
}

export const BadgeGroup: React.FC<BadgeGroupProps> = ({
  children,
  className = '',
}) => {
  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {children}
    </div>
  );
};

// =============================================================================
// Priority Badge
// =============================================================================

type PriorityLevel = 'critical' | 'high' | 'medium' | 'low';

interface PriorityBadgeProps {
  priority: PriorityLevel;
  size?: BadgeSize;
  className?: string;
}

const priorityConfig: Record<PriorityLevel, { color: BadgeColor; label: string }> = {
  critical: { color: 'red', label: 'حرج' },
  high: { color: 'orange', label: 'عالي' },
  medium: { color: 'yellow', label: 'متوسط' },
  low: { color: 'green', label: 'منخفض' },
};

export const PriorityBadge: React.FC<PriorityBadgeProps> = ({
  priority,
  size = 'md',
  className = '',
}) => {
  const config = priorityConfig[priority];
  
  return (
    <Badge
      color={config.color}
      variant="subtle"
      size={size}
      className={className}
    >
      {config.label}
    </Badge>
  );
};

// =============================================================================
// Export
// =============================================================================

export default Badge;

