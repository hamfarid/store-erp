# 🚦 Rate Limiting Template (Global System Ultimate)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel (Security Check)

## 1. The Philosophy
Protect the API. Deny Service to Abusers.

## 2. Express Implementation
You MUST implement rate limiting on ALL public routes.

```javascript
const rateLimit = require('express-rate-limit');

// General API limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    status: 'error',
    message: 'Too many requests, please try again later.'
  },
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
});

// Strict limiter for auth routes (Brute Force Protection)
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // Limit each IP to 5 failed login attempts per hour
  message: {
    status: 'error',
    message: 'Too many login attempts, please try again later.'
  },
  skipSuccessfulRequests: true, // Only count failures
});

// Apply to routes
app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);
```
