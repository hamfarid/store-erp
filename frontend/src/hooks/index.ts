/**
 * FILE: frontend/src/hooks/index.ts
 * PURPOSE: Export all custom hooks
 * OWNER: Frontend Team
 * RELATED: frontend/src/hooks/useApi.ts
 * LAST-AUDITED: 2026-01-17
 */

// API Hooks
export {
  useApi,
  useLogin,
  useLogout,
  useProducts,
  useCustomers,
  useMFA,
} from './useApi';
export type { UseApiState } from './useApi';

// Debounce Hooks
export {
  useDebounce,
  useDebouncedCallback,
  useDebouncedSearch
} from './useDebounce';

// Storage Hooks
export {
  useLocalStorage,
  useSessionStorage
} from './useLocalStorage';

// Theme Hooks
export {
  useTheme,
  usePrefersReducedMotion,
  useMediaQuery,
  THEMES
} from './useTheme';

// Notification Hooks
export {
  useNotification,
  useBrowserNotification,
  NOTIFICATION_TYPES
} from './useNotification';

// Pagination Hooks
export {
  usePagination,
  useLocalPagination
} from './usePagination';

// Click Outside Hooks
export {
  useClickOutside,
  useClickOutsideMultiple,
  useDropdown
} from './useClickOutside';

// Permission Hooks
export {
  usePermission,
  usePermissions,
  useAllPermissions,
  usePermissionGate,
  useRoles
} from './usePermissions';

// Form Hook
export { useForm } from './useForm';

// Keyboard Shortcuts Hook
export { useKeyboardShortcuts } from './useKeyboardShortcuts';

// CSRF Hook
export { useCsrf } from './useCsrf';

// Connection Status Hook
export { useConnectionStatus } from './useConnectionStatus';

// Performance Hook
export { usePerformance } from './usePerformance';

// Observability Hook
export { useObservability } from './useObservability';

// Mobile Hook
export { useMobile } from './use-mobile';

