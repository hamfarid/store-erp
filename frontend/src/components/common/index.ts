/**
 * Common Components Index
 * 
 * Central export file for all common UI components.
 */

// =============================================================================
// Layout Components
// =============================================================================

export { default as Card, CardHeader, CardBody, CardFooter, ImageCard, HorizontalCard, FeatureCard, PricingCard } from './Card';

// =============================================================================
// Data Display
// =============================================================================

export { default as Badge, StatusBadge, CountBadge, BadgeGroup, PriorityBadge } from './Badge';
export { default as Avatar, AvatarGroup, AvatarWithName, EditableAvatar } from './Avatar';
export { default as StatCard, MiniStatCard, StatCardGrid, ComparisonStatCard, ProgressStatCard } from './StatCard';
export { default as DataTable } from './DataTable';

// =============================================================================
// Progress & Loading
// =============================================================================

export { default as Progress, ProgressBar, CircularProgress, StepsProgress, LoadingProgress, MultiProgress } from './Progress';
export { Skeleton, TextSkeleton, AvatarSkeleton, CardSkeleton, TableSkeleton, FormSkeleton, ListSkeleton, DashboardSkeleton } from './Skeleton';

// =============================================================================
// Forms & Inputs
// =============================================================================

export { default as Toggle, ToggleGroup, ToggleCard, CheckboxToggle } from './Toggle';
export { default as Dropdown, DropdownMenu, ContextMenu, SelectDropdown } from './Dropdown';

// =============================================================================
// Feedback
// =============================================================================

export { default as Alert, Banner, ToastAlert, AlertList } from './Alert';
export { default as Tooltip } from './Tooltip';
export { default as EmptyState, NoDataState, ErrorState, SearchEmptyState, PermissionDeniedState, MaintenanceState, ComingSoonState, SuccessState } from './EmptyState';

// =============================================================================
// Navigation
// =============================================================================

export { default as Breadcrumbs, BreadcrumbItem } from './Breadcrumbs';
export { default as Tabs, TabList, Tab, TabPanels, TabPanel, VerticalTabs } from './Tabs';

// =============================================================================
// Overlays
// =============================================================================

export { default as Modal, ConfirmModal, AlertModal, FormModal, FullScreenModal } from './Modal';

// =============================================================================
// Types
// =============================================================================

export type { 
  // Badge types
  BadgeProps,
  StatusBadgeProps,
  
  // Card types  
  CardProps,
  
  // Progress types
  ProgressBarProps,
  CircularProgressProps,
  
  // Toggle types
  ToggleProps,
  
  // Alert types
  AlertProps,
  
  // Modal types
  ModalProps,
} from './types';

