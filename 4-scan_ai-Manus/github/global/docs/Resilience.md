# Resilience Patterns

## Purpose
This document details circuit breakers, retries, and fallbacks implemented in the system.

## Circuit Breaker

**Implementation:** `src/backend/utils/circuitBreaker.js`

**Configuration:**
- Failure threshold: 5 failures
- Timeout: 60 seconds
- Half-open retry: 30 seconds

**Usage:**
```javascript
const result = await circuitBreaker.execute(apiCall);
```

## Retry Logic

**Implementation:** `src/backend/utils/retry.js`

**Configuration:**
- Max retries: 3
- Backoff: Exponential (1s, 2s, 4s)
- Retryable errors: Network, timeout

**Usage:**
```javascript
const result = await retry(apiCall, { maxRetries: 3 });
```

## Fallbacks

**API Fallback:**
- Primary: External API
- Fallback: Cached data
- Last resort: Default values

**Database Fallback:**
- Primary: Primary database
- Fallback: Read replica
- Last resort: Error response


---

## Idempotency

**Implementation:** `src/backend/middleware/idempotency.js`

**Configuration:**
- **Header:** `Idempotency-Key`
- **Cache:** Redis
- **TTL:** 24 hours

**Usage:**
- This middleware is applied to all `POST`, `PUT`, `DELETE`, and `PATCH` routes.
- It automatically handles caching and response retrieval.

**Flow:**
1. Middleware checks for `Idempotency-Key` in the header.
2. If key exists in Redis, it returns the cached response.
3. If key does not exist, it proceeds to the controller.
4. After the controller returns a response, the middleware caches the response with the key.

**Frontend Implementation:**
- A utility function generates a UUIDv4 for each mutation.
- This key is added to the request header.

```javascript
// frontend/utils/api.js
import { v4 as uuidv4 } from 'uuid';

async function postWithIdempotency(url, data) {
  const idempotencyKey = uuidv4();
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Idempotency-Key': idempotencyKey,
    },
    body: JSON.stringify(data),
  });
  return response;
}
```

