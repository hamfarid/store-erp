"""
Comprehensive Logging System for Store ERP

This module implements a structured logging system with JSON formatting,
multiple log levels, file rotation, and integration with the Memory System.

Based on GLOBAL_PROFESSIONAL_CORE_PROMPT.md principles:
- Meticulous Logging (30% of OSF Framework)
- Structured JSON format
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Automatic log rotation
- Integration with Memory System
"""

import logging
import logging.handlers
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import traceback


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    
    Converts log records to JSON format with consistent structure:
    {
        "timestamp": "2025-12-13T17:30:00.123456",
        "level": "INFO",
        "logger": "store_erp.auth",
        "message": "User logged in successfully",
        "module": "auth.py",
        "function": "login",
        "line": 123,
        "user_id": "user_123",
        "ip_address": "192.168.1.1",
        "extra": {...}
    }
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON string representation of log record
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_data["extra"] = record.extra_data
        
        return json.dumps(log_data, ensure_ascii=False)


class StoreERPLogger:
    """
    Main logger class for Store ERP.
    
    Provides structured logging with:
    - JSON formatting
    - Multiple log levels
    - File rotation (daily, size-based)
    - Console and file handlers
    - Integration with Memory System
    """
    
    def __init__(self, name: str = "store_erp"):
        """
        Initialize logger.
        
        Args:
            name: Logger name (default: "store_erp")
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Create logs directory if not exists
        self.logs_dir = Path(__file__).parent.parent.parent.parent / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.logs_dir / "application").mkdir(exist_ok=True)
        (self.logs_dir / "security").mkdir(exist_ok=True)
        (self.logs_dir / "performance").mkdir(exist_ok=True)
        (self.logs_dir / "errors").mkdir(exist_ok=True)
        
        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handlers()
    
    def _setup_console_handler(self):
        """Setup console handler with colored output."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Simple format for console (not JSON)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        self.logger.addHandler(console_handler)
    
    def _setup_file_handlers(self):
        """Setup file handlers with rotation."""
        
        # Application logs (all levels)
        app_handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.logs_dir / "application" / "app.log",
            when='midnight',
            interval=1,
            backupCount=30,  # Keep 30 days
            encoding='utf-8'
        )
        app_handler.setLevel(logging.DEBUG)
        app_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(app_handler)
        
        # Error logs (ERROR and CRITICAL only)
        error_handler = logging.handlers.RotatingFileHandler(
            filename=self.logs_dir / "errors" / "errors.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(error_handler)
        
        # Security logs
        security_handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.logs_dir / "security" / "security.log",
            when='midnight',
            interval=1,
            backupCount=90,  # Keep 90 days (compliance)
            encoding='utf-8'
        )
        security_handler.setLevel(logging.INFO)
        security_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(security_handler)
        
        # Performance logs
        perf_handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.logs_dir / "performance" / "performance.log",
            when='midnight',
            interval=1,
            backupCount=7,  # Keep 7 days
            encoding='utf-8'
        )
        perf_handler.setLevel(logging.INFO)
        perf_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(perf_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, message, **kwargs)
    
    def _log(self, level: int, message: str, **kwargs):
        """
        Internal logging method.
        
        Args:
            level: Log level
            message: Log message
            **kwargs: Extra data to include in log
        """
        extra = {'extra_data': kwargs} if kwargs else {}
        self.logger.log(level, message, extra=extra)
    
    def log_user_action(self, user_id: str, action: str, details: Dict[str, Any] = None):
        """
        Log user action.
        
        Args:
            user_id: User ID
            action: Action performed
            details: Additional details
        """
        self.info(
            f"User action: {action}",
            user_id=user_id,
            action=action,
            details=details or {}
        )
    
    def log_security_event(self, event_type: str, user_id: Optional[str] = None, 
                          ip_address: Optional[str] = None, details: Dict[str, Any] = None):
        """
        Log security event.
        
        Args:
            event_type: Type of security event
            user_id: User ID (if applicable)
            ip_address: IP address
            details: Additional details
        """
        self.warning(
            f"Security event: {event_type}",
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            details=details or {}
        )
    
    def log_api_request(self, method: str, endpoint: str, user_id: Optional[str] = None,
                       status_code: int = None, duration_ms: float = None):
        """
        Log API request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            user_id: User ID (if authenticated)
            status_code: Response status code
            duration_ms: Request duration in milliseconds
        """
        self.info(
            f"API request: {method} {endpoint}",
            method=method,
            endpoint=endpoint,
            user_id=user_id,
            status_code=status_code,
            duration_ms=duration_ms
        )
    
    def log_database_query(self, query_type: str, table: str, duration_ms: float = None):
        """
        Log database query.
        
        Args:
            query_type: Type of query (SELECT, INSERT, UPDATE, DELETE)
            table: Table name
            duration_ms: Query duration in milliseconds
        """
        self.debug(
            f"Database query: {query_type} on {table}",
            query_type=query_type,
            table=table,
            duration_ms=duration_ms
        )
    
    def log_performance(self, operation: str, duration_ms: float, details: Dict[str, Any] = None):
        """
        Log performance metric.
        
        Args:
            operation: Operation name
            duration_ms: Duration in milliseconds
            details: Additional details
        """
        self.info(
            f"Performance: {operation} took {duration_ms:.2f}ms",
            operation=operation,
            duration_ms=duration_ms,
            details=details or {}
        )
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any] = None):
        """
        Log error with full context.
        
        Args:
            error: Exception object
            context: Additional context
        """
        self.error(
            f"Error occurred: {str(error)}",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context or {},
            exc_info=True
        )


# Global logger instance
logger = StoreERPLogger()


# Convenience functions
def debug(message: str, **kwargs):
    """Log debug message."""
    logger.debug(message, **kwargs)


def info(message: str, **kwargs):
    """Log info message."""
    logger.info(message, **kwargs)


def warning(message: str, **kwargs):
    """Log warning message."""
    logger.warning(message, **kwargs)


def error(message: str, **kwargs):
    """Log error message."""
    logger.error(message, **kwargs)


def critical(message: str, **kwargs):
    """Log critical message."""
    logger.critical(message, **kwargs)


def log_user_action(user_id: str, action: str, details: Dict[str, Any] = None):
    """Log user action."""
    logger.log_user_action(user_id, action, details)


def log_security_event(event_type: str, user_id: Optional[str] = None, 
                      ip_address: Optional[str] = None, details: Dict[str, Any] = None):
    """Log security event."""
    logger.log_security_event(event_type, user_id, ip_address, details)


def log_api_request(method: str, endpoint: str, user_id: Optional[str] = None,
                   status_code: int = None, duration_ms: float = None):
    """Log API request."""
    logger.log_api_request(method, endpoint, user_id, status_code, duration_ms)


def log_database_query(query_type: str, table: str, duration_ms: float = None):
    """Log database query."""
    logger.log_database_query(query_type, table, duration_ms)


def log_performance(operation: str, duration_ms: float, details: Dict[str, Any] = None):
    """Log performance metric."""
    logger.log_performance(operation, duration_ms, details)


def log_error_with_context(error: Exception, context: Dict[str, Any] = None):
    """Log error with full context."""
    logger.log_error_with_context(error, context)


# Example usage
if __name__ == "__main__":
    # Test logging
    info("Logger initialized successfully")
    debug("Debug message with extra data", user_id="test_user", action="test")
    warning("Warning message")
    error("Error message")
    
    # Test user action logging
    log_user_action("user_123", "login", {"ip": "192.168.1.1"})
    
    # Test security event logging
    log_security_event("failed_login", user_id="user_123", ip_address="192.168.1.1")
    
    # Test API request logging
    log_api_request("POST", "/api/auth/login", status_code=200, duration_ms=45.3)
    
    # Test performance logging
    log_performance("database_query", 123.45, {"query": "SELECT * FROM users"})
    
    # Test error logging
    try:
        raise ValueError("Test error")
    except Exception as e:
        log_error_with_context(e, {"operation": "test"})
    
    print("✅ Logging system test complete. Check logs/ directory.")
