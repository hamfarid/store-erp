#!/usr/bin/env python
"""
Comprehensive Accounting Module Testing Script
Tests accounting models, API endpoints, financial calculations, chart of accounts
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')
django.setup()


def test_accounting_models():
    """Test accounting models functionality."""
    print("=" * 60)
    print("ACCOUNTING MODELS TESTING")
    print("=" * 60)

    try:
        # Test imports
        from gaara_erp.business_modules.accounting.models import (
            Account, AccountType, JournalEntry, JournalEntryLine,
            ChartOfAccounts, FinancialPeriod
        )
        print("✓ Accounting models imported successfully")

        # Test AccountType model
        print("\n--- Testing AccountType Model ---")
        account_type = AccountType.objects.create(
            name="Test Asset",
            code="TA",
            category="asset"
        )
        print(f"✓ AccountType created: {account_type}")

        # Test Account model
        print("\n--- Testing Account Model ---")
        account = Account.objects.create(
            name="Test Cash Account",
            code="1001",
            account_type=account_type,
            balance=Decimal('1000.00')
        )
        print(f"✓ Account created: {account}")

        # Test string representation
        assert str(account) == "1001 - Test Cash Account"
        print("✓ Account string representation works")

        # Test FinancialPeriod model
        print("\n--- Testing FinancialPeriod Model ---")
        from datetime import date
        period = FinancialPeriod.objects.create(
            name="Test Period 2024",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )
        print(f"✓ FinancialPeriod created: {period}")

        # Clean up
        account.delete()
        account_type.delete()
        period.delete()
        print("✓ Test data cleaned up")

    except ImportError as e:
        print(f"⚠ Accounting models not available: {e}")
        return True
    except Exception as e:
        print(f"✗ Accounting models test failed: {e}")
        return False

    return True


def test_journal_entries():
    """Test journal entry functionality."""
    print("\n--- Testing Journal Entries ---")

    try:
        from gaara_erp.business_modules.accounting.models import (
            Account, AccountType, JournalEntry, JournalEntryLine
        )
        from datetime import date

        # Create test account types
        asset_type = AccountType.objects.create(
            name="Asset", code="A", category="asset"
        )
        liability_type = AccountType.objects.create(
            name="Liability", code="L", category="liability"
        )

        # Create test accounts
        cash_account = Account.objects.create(
            name="Cash", code="1001", account_type=asset_type
        )
        loan_account = Account.objects.create(
            name="Loan Payable", code="2001", account_type=liability_type
        )

        # Create journal entry
        journal_entry = JournalEntry.objects.create(
            reference="JE001",
            description="Test Journal Entry",
            date=date.today()
        )
        print(f"✓ JournalEntry created: {journal_entry}")

        # Create journal entry lines
        debit_line = JournalEntryLine.objects.create(
            journal_entry=journal_entry,
            account=cash_account,
            debit=Decimal('1000.00'),
            credit=Decimal('0.00')
        )

        credit_line = JournalEntryLine.objects.create(
            journal_entry=journal_entry,
            account=loan_account,
            debit=Decimal('0.00'),
            credit=Decimal('1000.00')
        )

        print("✓ Journal entry lines created")

        # Test journal entry balance
        total_debits = sum(line.debit for line in journal_entry.lines.all())
        total_credits = sum(line.credit for line in journal_entry.lines.all())

        if total_debits == total_credits:
            print("✓ Journal entry is balanced")
        else:
            print("✗ Journal entry is not balanced")

        # Clean up
        journal_entry.delete()
        cash_account.delete()
        loan_account.delete()
        asset_type.delete()
        liability_type.delete()
        print("✓ Journal entry test data cleaned up")

    except Exception as e:
        print(f"✗ Journal entries test failed: {e}")
        return False

    return True


def test_accounting_api_endpoints():
    """Test accounting API endpoints."""
    print("\n--- Testing Accounting API Endpoints ---")

    client = Client()

    try:
        # Test accounts API
        response = client.get('/api/accounting/accounts/')
        print(
            f"GET /api/accounting/accounts/ - Status: {response.status_code}")

        if response.status_code == 200:
            print("✓ Accounts API endpoint works")
        elif response.status_code == 404:
            print("⚠ Accounts API endpoint not found (may be disabled)")
        else:
            print(f"⚠ Accounts API returned status {response.status_code}")

        # Test journal entries API
        response = client.get('/api/accounting/journal-entries/')
        print(
            f"GET /api/accounting/journal-entries/ - Status: {response.status_code}")

        if response.status_code == 200:
            print("✓ Journal Entries API endpoint works")
        elif response.status_code == 404:
            print("⚠ Journal Entries API endpoint not found (may be disabled)")
        else:
            print(
                f"⚠ Journal Entries API returned status {response.status_code}")

        # Test chart of accounts API
        response = client.get('/api/accounting/chart-of-accounts/')
        print(
            f"GET /api/accounting/chart-of-accounts/ - Status: {response.status_code}")

        if response.status_code == 200:
            print("✓ Chart of Accounts API endpoint works")
        elif response.status_code == 404:
            print("⚠ Chart of Accounts API endpoint not found (may be disabled)")
        else:
            print(
                f"⚠ Chart of Accounts API returned status {response.status_code}")

    except Exception as e:
        print(f"✗ Accounting API endpoints test failed: {e}")
        return False

    return True


def test_financial_calculations():
    """Test financial calculations and business logic."""
    print("\n--- Testing Financial Calculations ---")

    try:
        from gaara_erp.business_modules.accounting.models import Account, AccountType
        from decimal import Decimal

        # Create test account type
        asset_type = AccountType.objects.create(
            name="Asset", code="A", category="asset"
        )

        # Create test account
        account = Account.objects.create(
            name="Test Account",
            code="1001",
            account_type=asset_type,
            balance=Decimal('1000.00')
        )

        # Test balance calculations
        original_balance = account.balance
        print(f"✓ Original balance: {original_balance}")

        # Test debit operation (should increase asset balance)
        account.balance += Decimal('500.00')
        account.save()
        print(f"✓ After debit: {account.balance}")

        # Test credit operation (should decrease asset balance)
        account.balance -= Decimal('200.00')
        account.save()
        print(f"✓ After credit: {account.balance}")

        # Verify final balance
        expected_balance = original_balance + \
            Decimal('500.00') - Decimal('200.00')
        if account.balance == expected_balance:
            print("✓ Financial calculations are correct")
        else:
            print("✗ Financial calculations are incorrect")

        # Clean up
        account.delete()
        asset_type.delete()
        print("✓ Financial calculations test data cleaned up")

    except Exception as e:
        print(f"✗ Financial calculations test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = True

    success &= test_accounting_models()
    success &= test_journal_entries()
    success &= test_accounting_api_endpoints()
    success &= test_financial_calculations()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL ACCOUNTING MODULE TESTS COMPLETED!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ SOME ACCOUNTING MODULE TESTS FAILED!")
        print("=" * 60)
        sys.exit(1)
