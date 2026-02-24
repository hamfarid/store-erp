# 🛡️ Error Handling Pattern (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel (Linter)

## 1. The Philosophy
Errors are expected. Crashing is forbidden.

## 2. The Protocol (Operational vs Programmer)
*   **Operational Errors:** Expected (e.g., "User not found"). Handle gracefully.
*   **Programmer Errors:** Bugs (e.g., "Undefined variable"). Fix immediately.

## 3. Backend Implementation (Express)
You MUST use a centralized error handler.

```javascript
// errorHandler.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

function errorHandler(err, req, res, next) {
  let { statusCode = 500, message } = err;
  
  // Sentinel Check: Log everything
  console.error({
    timestamp: new Date().toISOString(),
    method: req.method,
    url: req.url,
    error: message,
    stack: err.stack
  });
  
  // Security: Don't leak stack traces in production
  if (process.env.NODE_ENV === 'production' && !err.isOperational) {
    message = 'Internal server error';
  }
  
  res.status(statusCode).json({
    status: 'error',
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
}

module.exports = { AppError, errorHandler };
```

## 4. Usage
```javascript
// You MUST use try/catch or async wrapper
async function getUser(req, res, next) {
  try {
    const user = await db.findUserById(req.params.id);
    if (!user) {
      throw new AppError('User not found', 404);
    }
    res.json(user);
  } catch (error) {
    next(error);
  }
}
```
