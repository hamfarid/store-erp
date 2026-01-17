/**
 * FILE: frontend/src/api/index.ts
 * PURPOSE: Export all API client and types
 * OWNER: Frontend Team
 * RELATED: frontend/src/api/client.ts, frontend/src/api/types.ts
 * LAST-AUDITED: 2025-10-27
 */

// Export API client
export { ApiClient, apiClient, default } from './client';
export type { ApiError, RequestOptions } from './client';

// Export types
export type { paths, components } from './types';

