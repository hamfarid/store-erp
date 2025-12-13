/**
 * FILE: frontend/src/hooks/index.ts
 * PURPOSE: Export all custom hooks
 * OWNER: Frontend Team
 * RELATED: frontend/src/hooks/useApi.ts
 * LAST-AUDITED: 2025-10-27
 */

export {
  useApi,
  useLogin,
  useLogout,
  useProducts,
  useCustomers,
  useMFA,
} from './useApi';

export type { UseApiState } from './useApi';

