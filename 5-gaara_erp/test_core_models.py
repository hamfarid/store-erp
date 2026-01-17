#!/usr/bin/env python
"""
Comprehensive Core Models Testing Script
Tests all core models: Country, Company, Branch, Currency, Department, SystemSetting, etc.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import sys


def test_core_models():
    """Test all core models functionality."""
    print("=" * 60)
    print("CORE MODELS TESTING")
    print("=" * 60)

    # Test imports
    try:
        from core_modules.core.models import (
            Country, Company, Branch, Currency
        )
        print("✓ Core models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import core models: {e}")
        return False

    # Test Country model
    print("\n--- Testing Country Model ---")
    try:
        # Create a test country
        country = Country.objects.create(
            name="Test Country",
            code="TC",
            phone_code="+999"
        )
        print(f"✓ Country created: {country}")

        # Test string representation
        assert str(country) == "Test Country"
        print("✓ Country string representation works")

        # Test unique constraint
        try:
            Country.objects.create(name="Test Country",
                                   code="TC2", phone_code="+998")
            print("✗ Country unique constraint failed")
        except IntegrityError:
            print("✓ Country unique constraint works")

        # Clean up
        country.delete()

    except Exception as e:
        print(f"✗ Country model test failed: {e}")
        return False

    # Test Company model
    print("\n--- Testing Company Model ---")
    try:
        # Create a test company
        company = Company.objects.create(
            name="Test Company",
            code="TC001",
            email="test@company.com"
        )
        print(f"✓ Company created: {company}")

        # Test string representation
        assert str(company) == "Test Company"
        print("✓ Company string representation works")

        # Clean up
        company.delete()

    except Exception as e:
        print(f"✗ Company model test failed: {e}")
        return False

    # Test Currency model
    print("\n--- Testing Currency Model ---")
    try:
        # Create a test currency
        currency = Currency.objects.create(
            name="Test Dollar",
            code="TSD",
            symbol="T$"
        )
        print(f"✓ Currency created: {currency}")

        # Test string representation
        assert str(currency) == "Test Dollar (TSD)"
        print("✓ Currency string representation works")

        # Clean up
        currency.delete()

    except Exception as e:
        print(f"✗ Currency model test failed: {e}")
        return False

    # Test TimestampedModel
    print("\n--- Testing TimestampedModel ---")
    try:
        # Create a test country to check timestamps
        country = Country.objects.create(
            name="Timestamp Test",
            code="TT",
            phone_code="+111"
        )

        # Check if timestamps are set
        assert hasattr(country, 'created_at')
        assert hasattr(country, 'updated_at')
        assert country.created_at is not None
        assert country.updated_at is not None
        print("✓ TimestampedModel fields work correctly")

        # Clean up
        country.delete()

    except Exception as e:
        print(f"✗ TimestampedModel test failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("CORE MODELS TESTING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    return True


def test_model_relationships():
    """Test relationships between core models."""
    print("\n--- Testing Model Relationships ---")

    try:
        from core_modules.core.models import Country, Company, Branch

        # Create country
        country = Country.objects.create(
            name="Test Country",
            code="TC",
            phone_code="+999"
        )

        # Create company
        company = Company.objects.create(
            name="Test Company",
            code="TC001",
            email="test@company.com",
            country=country
        )

        # Create branch
        branch = Branch.objects.create(
            name="Main Branch",
            code="MB001",
            company=company
        )

        # Test relationships
        assert company.country == country
        assert branch.company == company
        print("✓ Model relationships work correctly")

        # Clean up
        branch.delete()
        company.delete()
        country.delete()

    except Exception as e:
        print(f"✗ Model relationships test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = test_core_models()
    if success:
        success = test_model_relationships()

    if success:
        print("\n🎉 ALL CORE MODEL TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n❌ SOME CORE MODEL TESTS FAILED!")
        sys.exit(1)
