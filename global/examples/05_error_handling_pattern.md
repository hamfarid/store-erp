# Error Handling Pattern

## Backend (Express Middleware)

\`\`\`javascript
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
  
  // Log error
  console.error({
    timestamp: new Date().toISOString(),
    method: req.method,
    url: req.url,
    error: message,
    stack: err.stack
  });
  
  // Don't leak error details in production
  if (process.env.NODE_ENV === 'production' && !err.isOperational) {
    message = 'Internal server error';
  }
  
  res.status(statusCode).json({
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
}

module.exports = { AppError, errorHandler };
\`\`\`

## Usage

\`\`\`javascript
const { AppError } = require('./errorHandler');

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
\`\`\`
