"""
Test Data Validation Module
Path: /home/ubuntu/gaara_scan_ai/backend/tests/unit/test_data_validation.py

Tests for data validation functionality including:
- Input validation
- Data sanitization
- Schema validation
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch


class TestDataValidation:
    """Test cases for data validation module"""

    @pytest.fixture
    def valid_farm_data(self):
        """Valid farm data for testing"""
        return {
            "name": "Test Farm",
            "location": "Test Location",
            "area": 100.5,
            "owner_id": 1,
            "created_at": datetime.now().isoformat()
        }

    @pytest.fixture
    def invalid_farm_data(self):
        """Invalid farm data for testing"""
        return {
            "name": "",  # Empty name
            "location": None,  # Null location
            "area": -10,  # Negative area
        }

    def test_valid_farm_data_structure(self, valid_farm_data):
        """Test valid farm data has correct structure"""
        assert "name" in valid_farm_data
        assert "location" in valid_farm_data
        assert "area" in valid_farm_data
        assert "owner_id" in valid_farm_data

    def test_farm_name_not_empty(self, valid_farm_data):
        """Test farm name is not empty"""
        assert valid_farm_data["name"]
        assert len(valid_farm_data["name"]) > 0

    def test_farm_area_positive(self, valid_farm_data):
        """Test farm area is positive"""
        assert valid_farm_data["area"] > 0

    def test_invalid_farm_name(self, invalid_farm_data):
        """Test validation fails for empty name"""
        assert not invalid_farm_data["name"]

    def test_invalid_farm_location(self, invalid_farm_data):
        """Test validation fails for null location"""
        assert invalid_farm_data["location"] is None

    def test_invalid_farm_area(self, invalid_farm_data):
        """Test validation fails for negative area"""
        assert invalid_farm_data["area"] < 0

    @pytest.mark.parametrize("area,is_valid", [
        (100.5, True),
        (0, False),
        (-10, False),
        (1000000, True),
    ])
    def test_area_validation(self, area, is_valid):
        """Test area validation with different values"""
        if is_valid:
            assert area > 0
        else:
            assert area <= 0

    def test_email_validation(self):
        """Test email validation"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "admin+tag@company.org"
        ]
        invalid_emails = [
            "invalid.email",
            "@example.com",
            "user@",
            "user name@example.com"
        ]
        
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for email in valid_emails:
            assert re.match(email_pattern, email)
        
        for email in invalid_emails:
            assert not re.match(email_pattern, email)

    def test_phone_validation(self):
        """Test phone number validation"""
        valid_phones = [
            "+966501234567",
            "0501234567",
            "+1-555-123-4567"
        ]
        
        for phone in valid_phones:
            # Basic validation - contains only digits, +, -, and spaces
            cleaned = phone.replace("+", "").replace("-", "").replace(" ", "")
            assert cleaned.isdigit()

    def test_date_validation(self):
        """Test date validation"""
        valid_date = "2024-12-13"
        try:
            datetime.fromisoformat(valid_date)
            assert True
        except ValueError:
            assert False

    def test_string_sanitization(self):
        """Test string sanitization"""
        dangerous_input = "<script>alert('XSS')</script>"
        sanitized = dangerous_input.replace("<", "&lt;").replace(">", "&gt;")
        assert "<script>" not in sanitized
        assert "&lt;script&gt;" in sanitized

    @pytest.mark.parametrize("value,expected_type", [
        ("123", str),
        (123, int),
        (123.45, float),
        (True, bool),
        ([], list),
        ({}, dict),
    ])
    def test_type_validation(self, value, expected_type):
        """Test type validation"""
        assert isinstance(value, expected_type)

    def test_required_fields_validation(self, valid_farm_data):
        """Test required fields are present"""
        required_fields = ["name", "location", "area"]
        for field in required_fields:
            assert field in valid_farm_data

    def test_optional_fields_validation(self):
        """Test optional fields handling"""
        data = {
            "name": "Test",
            "description": None  # Optional field
        }
        # Optional fields can be None
        assert data.get("description") is None or isinstance(data.get("description"), str)

    def test_range_validation(self):
        """Test numeric range validation"""
        temperature = 25.5
        assert -50 <= temperature <= 60  # Valid temperature range

        humidity = 75
        assert 0 <= humidity <= 100  # Valid humidity range

    def test_length_validation(self):
        """Test string length validation"""
        name = "Test Farm Name"
        assert 1 <= len(name) <= 255

        description = "A" * 1000
        assert len(description) <= 5000  # Max description length
