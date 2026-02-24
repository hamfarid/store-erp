# 🛡️ Error Handling Template (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel (Linter)

## 1. The Philosophy
Typed Errors > String Messages.

## 2. Custom Error Classes
You MUST extend `AppError` for all operational errors.

```javascript
// errors.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404);
  }
}

class ValidationError extends AppError {
  constructor(message = 'Validation failed') {
    super(message, 400);
  }
}

class AuthenticationError extends AppError {
  constructor(message = 'Authentication failed') {
    super(message, 401);
  }
}

module.exports = { AppError, NotFoundError, ValidationError, AuthenticationError };
```

## 3. Global Error Handler
You MUST catch all errors centrally.

```javascript
const errorHandler = (err, req, res, next) => {
  const { statusCode = 500, message } = err;
  
  // Sentinel Check: Mandatory Logging
  logger.error({
    message: err.message,
    stack: err.stack,
    statusCode,
    path: req.path,
    method: req.method
  });
  
  // Security: Hide implementation details in production
  res.status(statusCode).json({
    status: 'error',
    statusCode,
    message: err.isOperational ? message : 'Internal Server Error'
  });
};

module.exports = errorHandler;
```
