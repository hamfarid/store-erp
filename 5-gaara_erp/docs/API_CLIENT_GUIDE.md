# 📖 API Client Guide

**FILE**: docs/API_CLIENT_GUIDE.md  
**PURPOSE**: Complete guide for using the typed API client  
**OWNER**: Frontend Team  
**RELATED**: frontend/src/api/client.ts, frontend/src/hooks/useApi.ts  
**LAST-AUDITED**: 2025-10-27

---

## Overview

The Gaara Store API Client is a fully typed, production-ready client for interacting with the backend API. It provides:

- ✅ Full TypeScript type safety
- ✅ Automatic token management
- ✅ Retry logic with exponential backoff
- ✅ Error handling
- ✅ React hooks for easy integration

---

## Installation

The API client is already included in the frontend. No additional installation needed.

---

## Basic Usage

### Direct API Client

```typescript
import { apiClient } from '@/api';

// Login
const response = await apiClient.login({
  username: 'user@example.com',
  password: 'password123'
});

// Get products
const products = await apiClient.getProducts({ page: 1, per_page: 10 });

// Create product
const newProduct = await apiClient.createProduct({
  name: 'Product Name',
  sku: 'SKU123',
  price: 99.99,
  quantity: 100
});

// Logout
await apiClient.logout();
```

### React Hooks

```typescript
import { useLogin, useProducts } from '@/hooks';

function MyComponent() {
  const { login, loading, error } = useLogin();
  const { getProducts, data: products } = useProducts();

  const handleLogin = async () => {
    try {
      await login('user@example.com', 'password123');
      await getProducts(1, 10);
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <div>
      <button onClick={handleLogin} disabled={loading}>
        {loading ? 'Loading...' : 'Login'}
      </button>
      {error && <p>Error: {error.message}</p>}
      {products && <pre>{JSON.stringify(products, null, 2)}</pre>}
    </div>
  );
}
```

---

## API Methods

### Authentication

#### `login(credentials)`
```typescript
await apiClient.login({
  username: 'user@example.com',
  password: 'password123'
});
```

#### `logout()`
```typescript
await apiClient.logout();
```

#### `refreshAccessToken()`
```typescript
await apiClient.refreshAccessToken();
```

### Products

#### `getProducts(params?)`
```typescript
const products = await apiClient.getProducts({
  page: 1,
  per_page: 10
});
```

#### `getProduct(id)`
```typescript
const product = await apiClient.getProduct('product-id');
```

#### `createProduct(data)`
```typescript
const product = await apiClient.createProduct({
  name: 'Product Name',
  sku: 'SKU123',
  price: 99.99,
  quantity: 100
});
```

#### `updateProduct(id, data)`
```typescript
const product = await apiClient.updateProduct('product-id', {
  name: 'Updated Name',
  price: 149.99
});
```

#### `deleteProduct(id)`
```typescript
await apiClient.deleteProduct('product-id');
```

### Customers

#### `getCustomers(params?)`
```typescript
const customers = await apiClient.getCustomers({
  page: 1,
  per_page: 10
});
```

#### `getCustomer(id)`
```typescript
const customer = await apiClient.getCustomer('customer-id');
```

#### `createCustomer(data)`
```typescript
const customer = await apiClient.createCustomer({
  name: 'Customer Name',
  email: 'customer@example.com',
  phone: '+1234567890'
});
```

#### `updateCustomer(id, data)`
```typescript
const customer = await apiClient.updateCustomer('customer-id', {
  name: 'Updated Name'
});
```

#### `deleteCustomer(id)`
```typescript
await apiClient.deleteCustomer('customer-id');
```

### MFA

#### `setupMFA()`
```typescript
const setup = await apiClient.setupMFA();
```

#### `verifyMFA(code)`
```typescript
await apiClient.verifyMFA('123456');
```

#### `disableMFA()`
```typescript
await apiClient.disableMFA();
```

---

## Configuration

### Custom Base URL

```typescript
import { ApiClient } from '@/api';

const client = new ApiClient('https://api.example.com');
```

### Custom Timeout

```typescript
apiClient.setTimeout(60000); // 60 seconds
```

### Custom Retries

```typescript
apiClient.setRetries(5); // Retry up to 5 times
```

---

## Error Handling

```typescript
try {
  await apiClient.login({ username: 'user', password: 'pass' });
} catch (error) {
  if (error instanceof Error) {
    console.error('Error:', error.message);
  }
}
```

---

## React Hooks

### `useApi<T>()`
Generic hook for any API call

### `useLogin()`
Hook for login functionality

### `useLogout()`
Hook for logout functionality

### `useProducts()`
Hook for product operations

### `useCustomers()`
Hook for customer operations

### `useMFA()`
Hook for MFA operations

---

## Type Safety

All API methods are fully typed with TypeScript. The types are auto-generated from the OpenAPI specification.

```typescript
import type { components } from '@/api';

const product: components['schemas']['ProductResponse'] = await apiClient.getProduct('id');
```

---

## Testing

```typescript
import { describe, it, expect, vi } from 'vitest';
import { ApiClient } from '@/api';

describe('ApiClient', () => {
  it('should login successfully', async () => {
    const client = new ApiClient();
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          success: true,
          data: { access_token: 'token', refresh_token: 'refresh' }
        })
      } as Response)
    );

    const result = await client.login({ username: 'user', password: 'pass' });
    expect(result).toBeDefined();
  });
});
```

---

## Best Practices

1. ✅ Always use the singleton `apiClient` instance
2. ✅ Use React hooks in components for automatic loading/error states
3. ✅ Handle errors appropriately
4. ✅ Use TypeScript types for type safety
5. ✅ Set appropriate timeouts for long-running operations
6. ✅ Implement retry logic for critical operations

---

## Troubleshooting

### CORS Errors
Ensure the backend has CORS enabled for your frontend URL.

### 401 Unauthorized
Token may have expired. Call `refreshAccessToken()` or re-login.

### Network Timeouts
Increase timeout with `apiClient.setTimeout(ms)`.

### Retry Failures
Check network connectivity and backend availability.

---

**Status**: ✅ Complete  
**Last Updated**: 2025-10-27

