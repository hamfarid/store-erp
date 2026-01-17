# PROMPT 82: API RATE LIMITING

**Objective:** Protect the API from abuse and ensure fair usage by implementing rate limiting.

---

## 🎯 REQUIREMENTS

1.  **IP-Based Limiting:** Limit the number of requests per IP address.
2.  **User-Based Limiting:** Limit the number of requests per authenticated user.
3.  **Configurable Limits:** The rate limits should be configurable via environment variables.
4.  **Sliding Window:** Use a sliding window algorithm for rate limiting.
5.  **HTTP Headers:** Return appropriate HTTP headers to the client (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`).

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Setup
1.  **Install Library:** Add a rate limiting library (e.g., `express-rate-limit` for Node.js) to the project.
2.  **Configure Middleware:** Configure the rate limiting middleware with the desired limits.

### Phase 2: Integration
1.  **Apply Middleware:** Apply the rate limiting middleware to all API routes.
2.  **Differentiate Limits:** Apply different rate limits to different routes if necessary (e.g., a stricter limit for authentication routes).

### Phase 3: Verification
1.  **Write Tests:** Write tests to ensure that the rate limiting system works as expected.
2.  **Manual Verification:** Manually send a large number of requests to the API and verify that the rate limit is enforced.

---

## ✅ SUCCESS CRITERIA

- The API is protected from abuse.
- The rate limits are configurable.
- The API returns the correct HTTP headers.
