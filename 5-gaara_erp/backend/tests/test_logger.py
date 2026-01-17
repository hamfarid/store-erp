"""
Unit Tests for Logger Module

Tests the comprehensive logging system including:
- Logger initialization
- All log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- JSON formatting
- Specialized logging functions
- File creation and rotation
"""

import pytest
import logging
import json
import os
from pathlib import Path
from src.utils.logger import (
    StoreERPLogger,
    JSONFormatter,
    logger,
    debug,
    info,
    warning,
    error,
    critical,
    log_user_action,
    log_security_event,
    log_api_request,
    log_database_query,
    log_performance,
    log_error_with_context
)


class TestJSONFormatter:
    """Test JSONFormatter class."""
    
    def test_formatter_creates_valid_json(self):
        """Test that formatter creates valid JSON."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        output = formatter.format(record)
        data = json.loads(output)  # Should not raise exception
        
        assert "timestamp" in data
        assert "level" in data
        assert "logger" in data
        assert "message" in data
        assert data["message"] == "Test message"
    
    def test_formatter_includes_exception_info(self):
        """Test that formatter includes exception information."""
        formatter = JSONFormatter()
        
        try:
            raise ValueError("Test error")
        except ValueError:
            import sys
            exc_info = sys.exc_info()
        
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=exc_info
        )
        
        output = formatter.format(record)
        data = json.loads(output)
        
        assert "exception" in data
        assert data["exception"]["type"] == "ValueError"
        assert "Test error" in data["exception"]["message"]
        assert "traceback" in data["exception"]


class TestStoreERPLogger:
    """Test StoreERPLogger class."""
    
    def test_logger_initialization(self):
        """Test logger initialization."""
        test_logger = StoreERPLogger("test_logger")
        
        assert test_logger.name == "test_logger"
        assert test_logger.logger is not None
        assert test_logger.logger.level == logging.DEBUG
    
    def test_logger_creates_log_directories(self):
        """Test that logger creates necessary directories."""
        test_logger = StoreERPLogger("test_logger_2")
        
        assert test_logger.logs_dir.exists()
        assert (test_logger.logs_dir / "application").exists()
        assert (test_logger.logs_dir / "security").exists()
        assert (test_logger.logs_dir / "performance").exists()
        assert (test_logger.logs_dir / "errors").exists()
    
    def test_debug_logging(self):
        """Test debug level logging."""
        test_logger = StoreERPLogger("test_debug")
        test_logger.debug("Debug message", test_key="test_value")
        # No exception should be raised
    
    def test_info_logging(self):
        """Test info level logging."""
        test_logger = StoreERPLogger("test_info")
        test_logger.info("Info message", test_key="test_value")
        # No exception should be raised
    
    def test_warning_logging(self):
        """Test warning level logging."""
        test_logger = StoreERPLogger("test_warning")
        test_logger.warning("Warning message", test_key="test_value")
        # No exception should be raised
    
    def test_error_logging(self):
        """Test error level logging."""
        test_logger = StoreERPLogger("test_error")
        test_logger.error("Error message", test_key="test_value")
        # No exception should be raised
    
    def test_critical_logging(self):
        """Test critical level logging."""
        test_logger = StoreERPLogger("test_critical")
        test_logger.critical("Critical message", test_key="test_value")
        # No exception should be raised


class TestSpecializedLoggingFunctions:
    """Test specialized logging functions."""
    
    def test_log_user_action(self):
        """Test user action logging."""
        log_user_action(
            user_id="user_123",
            action="login",
            details={"ip": "192.168.1.1"}
        )
        # No exception should be raised
    
    def test_log_security_event(self):
        """Test security event logging."""
        log_security_event(
            event_type="failed_login",
            user_id="user_123",
            ip_address="192.168.1.1",
            details={"attempts": 3}
        )
        # No exception should be raised
    
    def test_log_api_request(self):
        """Test API request logging."""
        log_api_request(
            method="POST",
            endpoint="/api/auth/login",
            user_id="user_123",
            status_code=200,
            duration_ms=45.3
        )
        # No exception should be raised
    
    def test_log_database_query(self):
        """Test database query logging."""
        log_database_query(
            query_type="SELECT",
            table="users",
            duration_ms=12.5
        )
        # No exception should be raised
    
    def test_log_performance(self):
        """Test performance logging."""
        log_performance(
            operation="database_query",
            duration_ms=123.45,
            details={"query": "SELECT * FROM users"}
        )
        # No exception should be raised
    
    def test_log_error_with_context(self):
        """Test error logging with context."""
        try:
            raise ValueError("Test error")
        except Exception as e:
            log_error_with_context(
                error=e,
                context={"operation": "test"}
            )
        # No exception should be raised


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_debug_function(self):
        """Test debug convenience function."""
        debug("Debug message", key="value")
        # No exception should be raised
    
    def test_info_function(self):
        """Test info convenience function."""
        info("Info message", key="value")
        # No exception should be raised
    
    def test_warning_function(self):
        """Test warning convenience function."""
        warning("Warning message", key="value")
        # No exception should be raised
    
    def test_error_function(self):
        """Test error convenience function."""
        error("Error message", key="value")
        # No exception should be raised
    
    def test_critical_function(self):
        """Test critical convenience function."""
        critical("Critical message", key="value")
        # No exception should be raised


class TestLogFileCreation:
    """Test log file creation."""
    
    def test_application_log_exists(self):
        """Test that application log file is created."""
        test_logger = StoreERPLogger("test_app_log")
        test_logger.info("Test message")
        
        log_file = test_logger.logs_dir / "application" / "app.log"
        assert log_file.exists()
    
    def test_error_log_exists(self):
        """Test that error log file is created."""
        test_logger = StoreERPLogger("test_error_log")
        test_logger.error("Test error")
        
        log_file = test_logger.logs_dir / "errors" / "errors.log"
        assert log_file.exists()


@pytest.mark.integration
class TestLoggerIntegration:
    """Integration tests for logger."""
    
    def test_complete_logging_workflow(self):
        """Test complete logging workflow."""
        # Create logger
        test_logger = StoreERPLogger("integration_test")
        
        # Log at all levels
        test_logger.debug("Debug message")
        test_logger.info("Info message")
        test_logger.warning("Warning message")
        test_logger.error("Error message")
        test_logger.critical("Critical message")
        
        # Use specialized functions
        test_logger.log_user_action("user_123", "test_action")
        test_logger.log_security_event("test_event")
        test_logger.log_api_request("GET", "/api/test")
        test_logger.log_database_query("SELECT", "test_table")
        test_logger.log_performance("test_operation", 100.0)
        
        # Verify log files exist
        assert (test_logger.logs_dir / "application" / "app.log").exists()
        assert (test_logger.logs_dir / "errors" / "errors.log").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
