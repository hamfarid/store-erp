/**
 * Common Component Types
 * 
 * Type definitions for common UI components.
 */

import React from 'react';

// =============================================================================
// Badge Types
// =============================================================================

export type BadgeVariant = 'solid' | 'outline' | 'subtle';
export type BadgeColor = 'gray' | 'red' | 'orange' | 'yellow' | 'green' | 'teal' | 'blue' | 'indigo' | 'purple' | 'pink';
export type BadgeSize = 'sm' | 'md' | 'lg';

export interface BadgeProps {
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

export interface StatusBadgeProps {
  status: 'success' | 'warning' | 'error' | 'info' | 'pending' | 'inactive';
  label?: string;
  size?: BadgeSize;
  className?: string;
}

// =============================================================================
// Card Types
// =============================================================================

export interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  shadow?: 'none' | 'sm' | 'md' | 'lg';
  border?: boolean;
  hoverable?: boolean;
  clickable?: boolean;
  onClick?: () => void;
}

export interface CardHeaderProps {
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
  icon?: React.ReactNode;
  children?: React.ReactNode;
  className?: string;
}

// =============================================================================
// Avatar Types
// =============================================================================

export type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
export type AvatarStatus = 'online' | 'offline' | 'busy' | 'away';

export interface AvatarProps {
  src?: string;
  alt?: string;
  name?: string;
  size?: AvatarSize;
  status?: AvatarStatus;
  rounded?: boolean;
  border?: boolean;
  className?: string;
  onClick?: () => void;
}

// =============================================================================
// Progress Types
// =============================================================================

export type ProgressColor = 'blue' | 'green' | 'red' | 'yellow' | 'indigo' | 'purple' | 'pink';
export type ProgressSize = 'xs' | 'sm' | 'md' | 'lg';

export interface ProgressBarProps {
  value: number;
  max?: number;
  color?: ProgressColor;
  size?: ProgressSize;
  showLabel?: boolean;
  labelPosition?: 'inside' | 'outside' | 'top';
  animated?: boolean;
  striped?: boolean;
  className?: string;
}

export interface CircularProgressProps {
  value: number;
  max?: number;
  size?: number;
  strokeWidth?: number;
  color?: ProgressColor;
  showLabel?: boolean;
  className?: string;
}

// =============================================================================
// Toggle Types
// =============================================================================

export type ToggleSize = 'sm' | 'md' | 'lg';
export type ToggleColor = 'blue' | 'green' | 'indigo' | 'purple' | 'red';

export interface ToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
  size?: ToggleSize;
  color?: ToggleColor;
  label?: string;
  description?: string;
  labelPosition?: 'left' | 'right';
  className?: string;
  id?: string;
}

// =============================================================================
// Alert Types
// =============================================================================

export type AlertVariant = 'info' | 'success' | 'warning' | 'error';

export interface AlertProps {
  variant?: AlertVariant;
  title?: string;
  children: React.ReactNode;
  dismissible?: boolean;
  onDismiss?: () => void;
  icon?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}

// =============================================================================
// Modal Types
// =============================================================================

export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: ModalSize;
  showCloseButton?: boolean;
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  footer?: React.ReactNode;
  className?: string;
}

// =============================================================================
// StatCard Types
// =============================================================================

export type TrendDirection = 'up' | 'down' | 'neutral';
export type StatColor = 'blue' | 'green' | 'red' | 'yellow' | 'indigo' | 'purple' | 'gray';

export interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    direction: TrendDirection;
    label?: string;
  };
  color?: StatColor;
  loading?: boolean;
  className?: string;
  onClick?: () => void;
}

// =============================================================================
// Dropdown Types
// =============================================================================

export interface DropdownItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  danger?: boolean;
  divider?: boolean;
  onClick?: () => void;
}

export interface DropdownProps {
  trigger: React.ReactNode;
  items: DropdownItem[];
  align?: 'left' | 'right';
  className?: string;
}

// =============================================================================
// Tabs Types
// =============================================================================

export interface TabItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  badge?: string | number;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTab: string;
  onChange: (tabId: string) => void;
  variant?: 'underline' | 'pills' | 'enclosed';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  className?: string;
}

// =============================================================================
// Empty State Types
// =============================================================================

export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

// =============================================================================
// Breadcrumb Types
// =============================================================================

export interface BreadcrumbItemType {
  label: string;
  href?: string;
  icon?: React.ReactNode;
}

export interface BreadcrumbsProps {
  items: BreadcrumbItemType[];
  separator?: React.ReactNode;
  className?: string;
}

