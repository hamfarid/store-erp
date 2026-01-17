# Error Handling Template

## Custom Error Classes

```javascript
// Base Error
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Specific Errors
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

## Global Error Handler

```javascript
const errorHandler = (err, req, res, next) => {
  const { statusCode = 500, message } = err;
  
  // Log error
  logger.error({
    message: err.message,
    stack: err.stack,
    statusCode,
    path: req.path,
    method: req.method
  });
  
  // Send response
  res.status(statusCode).json({
    status: 'error',
    statusCode,
    message: err.isOperational ? message : 'Something went wrong'
  });
};

module.exports = errorHandler;
```
