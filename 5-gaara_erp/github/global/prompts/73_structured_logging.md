# STRUCTURED LOGGING PROMPT

**FILE**: github/global/prompts/73_structured_logging.md | **PURPOSE**: Structured JSON logging implementation | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

Structured logging is mandatory for all projects. All logs must be in JSON format for easy parsing and querying.

## Log Structure

```
logs/
├── debug.log       # Verbose debugging information
├── info.log        # General application flow
├── warn.log        # Potentially harmful situations
├── error.log       # Error events with stack traces
├── fatal.log       # Severe errors causing termination
└── background.log  # Background processes (cron, workers)
```

## Log Format (JSON)

All log entries MUST be in JSON format:

```json
{
  "timestamp": "2025-11-18T14:30:00.123Z",
  "level": "INFO",
  "message": "User logged in successfully",
  "details": {
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "ip": "192.168.1.1",
    "userAgent": "Mozilla/5.0...",
    "phase": "Execution",
    "action": "login"
  },
  "traceId": "abc-123-def-456",
  "service": "backend",
  "environment": "production"
}
```

## Log Levels

1. **DEBUG**: Detailed information for diagnosing problems
2. **INFO**: General informational messages
3. **WARN**: Warning messages for potentially harmful situations
4. **ERROR**: Error events that might still allow the application to continue
5. **FATAL**: Severe errors that will cause the application to terminate

## Implementation

### Python (Backend)

```python
# FILE: backend/utils/logger.py | PURPOSE: Structured logging utility | OWNER: Backend | LAST-AUDITED: 2025-11-18

import logging
import json
from datetime import datetime
from typing import Any, Dict
import traceback
import uuid

class StructuredLogger:
    """Structured JSON logger"""
    
    def __init__(self, service_name: str = "backend"):
        self.service_name = service_name
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        # Create loggers for each level
        self.loggers = {
            "debug": self._create_logger("debug", logging.DEBUG),
            "info": self._create_logger("info", logging.INFO),
            "warn": self._create_logger("warn", logging.WARNING),
            "error": self._create_logger("error", logging.ERROR),
            "fatal": self._create_logger("fatal", logging.CRITICAL),
        }
    
    def _create_logger(self, name: str, level: int) -> logging.Logger:
        """Create a logger for a specific level"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # File handler
        handler = logging.FileHandler(f"logs/{name}.log")
        handler.setLevel(level)
        
        # No formatter needed - we'll format manually
        logger.addHandler(handler)
        
        return logger
    
    def _format_log(
        self,
        level: str,
        message: str,
        details: Dict[str, Any] = None,
        trace_id: str = None,
        exception: Exception = None
    ) -> str:
        """Format log entry as JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.upper(),
            "message": message,
            "service": self.service_name,
            "environment": self.environment,
        }
        
        if details:
            log_entry["details"] = details
        
        if trace_id:
            log_entry["traceId"] = trace_id
        
        if exception:
            log_entry["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "stackTrace": traceback.format_exc()
            }
        
        return json.dumps(log_entry)
    
    def debug(self, message: str, details: Dict[str, Any] = None, trace_id: str = None):
        """Log debug message"""
        log_str = self._format_log("DEBUG", message, details, trace_id)
        self.loggers["debug"].debug(log_str)
    
    def info(self, message: str, details: Dict[str, Any] = None, trace_id: str = None):
        """Log info message"""
        log_str = self._format_log("INFO", message, details, trace_id)
        self.loggers["info"].info(log_str)
    
    def warn(self, message: str, details: Dict[str, Any] = None, trace_id: str = None):
        """Log warning message"""
        log_str = self._format_log("WARN", message, details, trace_id)
        self.loggers["warn"].warning(log_str)
    
    def error(
        self,
        message: str,
        details: Dict[str, Any] = None,
        trace_id: str = None,
        exception: Exception = None
    ):
        """Log error message"""
        log_str = self._format_log("ERROR", message, details, trace_id, exception)
        self.loggers["error"].error(log_str)
    
    def fatal(
        self,
        message: str,
        details: Dict[str, Any] = None,
        trace_id: str = None,
        exception: Exception = None
    ):
        """Log fatal message"""
        log_str = self._format_log("FATAL", message, details, trace_id, exception)
        self.loggers["fatal"].critical(log_str)

# Global logger instance
logger = StructuredLogger()
```

### Usage Example (Python)

```python
from utils.logger import logger

# Info log
logger.info(
    "User logged in successfully",
    details={
        "userId": user.id,
        "email": user.email,
        "ip": request.client.host
    },
    trace_id=request.headers.get("X-Trace-ID")
)

# Error log
try:
    result = risky_operation()
except Exception as e:
    logger.error(
        "Failed to process payment",
        details={
            "userId": user.id,
            "amount": payment.amount
        },
        trace_id=trace_id,
        exception=e
    )
```

### TypeScript (Frontend)

```typescript
// FILE: frontend/src/utils/logger.ts | PURPOSE: Structured logging utility | OWNER: Frontend | LAST-AUDITED: 2025-11-18

type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR' | 'FATAL';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  details?: Record<string, any>;
  traceId?: string;
  service: string;
  environment: string;
  exception?: {
    type: string;
    message: string;
    stackTrace?: string;
  };
}

class StructuredLogger {
  private service: string = 'frontend';
  private environment: string = import.meta.env.MODE || 'development';

  private formatLog(
    level: LogLevel,
    message: string,
    details?: Record<string, any>,
    traceId?: string,
    exception?: Error
  ): LogEntry {
    const logEntry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      service: this.service,
      environment: this.environment,
    };

    if (details) {
      logEntry.details = details;
    }

    if (traceId) {
      logEntry.traceId = traceId;
    }

    if (exception) {
      logEntry.exception = {
        type: exception.name,
        message: exception.message,
        stackTrace: exception.stack,
      };
    }

    return logEntry;
  }

  private sendLog(logEntry: LogEntry) {
    // In production, send to backend logging endpoint
    if (this.environment === 'production') {
      fetch('/api/logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(logEntry),
      }).catch(() => {
        // Fallback to console if API fails
        console.error('Failed to send log to backend');
      });
    }

    // Always log to console in development
    if (this.environment === 'development') {
      const consoleMethod = logEntry.level === 'ERROR' || logEntry.level === 'FATAL' 
        ? console.error 
        : logEntry.level === 'WARN' 
        ? console.warn 
        : console.log;
      
      consoleMethod(JSON.stringify(logEntry, null, 2));
    }
  }

  debug(message: string, details?: Record<string, any>, traceId?: string) {
    const logEntry = this.formatLog('DEBUG', message, details, traceId);
    this.sendLog(logEntry);
  }

  info(message: string, details?: Record<string, any>, traceId?: string) {
    const logEntry = this.formatLog('INFO', message, details, traceId);
    this.sendLog(logEntry);
  }

  warn(message: string, details?: Record<string, any>, traceId?: string) {
    const logEntry = this.formatLog('WARN', message, details, traceId);
    this.sendLog(logEntry);
  }

  error(message: string, details?: Record<string, any>, traceId?: string, exception?: Error) {
    const logEntry = this.formatLog('ERROR', message, details, traceId, exception);
    this.sendLog(logEntry);
  }

  fatal(message: string, details?: Record<string, any>, traceId?: string, exception?: Error) {
    const logEntry = this.formatLog('FATAL', message, details, traceId, exception);
    this.sendLog(logEntry);
  }
}

export const logger = new StructuredLogger();
```

## Middleware Integration

### FastAPI (Python)

```python
from fastapi import Request
import uuid
from utils.logger import logger

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # Generate trace ID
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
    
    # Log request
    logger.info(
        f"{request.method} {request.url.path}",
        details={
            "method": request.method,
            "path": request.url.path,
            "ip": request.client.host,
            "userAgent": request.headers.get("user-agent")
        },
        trace_id=trace_id
    )
    
    # Process request
    response = await call_next(request)
    
    # Log response
    logger.info(
        f"Response {response.status_code}",
        details={
            "statusCode": response.status_code,
            "path": request.url.path
        },
        trace_id=trace_id
    )
    
    # Add trace ID to response headers
    response.headers["X-Trace-ID"] = trace_id
    
    return response
```

## Querying Logs

### Using jq (command-line JSON processor)

```bash
# Get all ERROR logs
cat logs/error.log | jq 'select(.level == "ERROR")'

# Get logs for specific user
cat logs/info.log | jq 'select(.details.userId == "123")'

# Get logs within time range
cat logs/info.log | jq 'select(.timestamp >= "2025-11-18T00:00:00Z" and .timestamp <= "2025-11-18T23:59:59Z")'

# Count logs by level
cat logs/*.log | jq -s 'group_by(.level) | map({level: .[0].level, count: length})'
```

---

**Completion Criteria**:
- [ ] Structured logger implemented
- [ ] All log levels configured
- [ ] Middleware integrated
- [ ] Logs directory created
- [ ] Log rotation configured (optional)
- [ ] Documentation updated

