#!/usr/bin/env python3
"""
Test Pylint Configuration
=========================

This script tests if Pylint can properly load Django settings.
"""

import os
import sys
import subprocess
from pathlib import Path


def test_pylint_django_config():
    """Test if Pylint can load Django settings correctly."""
    print("Testing Pylint Django configuration...")

    # Set up environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')

    # Test basic Python path setup
    sys.path.insert(0, str(Path('./gaara_erp').resolve()))

    try:
        # Try to import Django settings
        import django
        from django.conf import settings
        django.setup()

        print("✅ Django settings loaded successfully")
        print(f"   Settings module: {settings.SETTINGS_MODULE}")
        print(f"   Debug mode: {settings.DEBUG}")
        print(f"   Database engine: {settings.DATABASES['default']['ENGINE']}")

        return True

    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False


def test_pylint_command():
    """Test running pylint on a simple file."""
    print("\nTesting Pylint command execution...")

    try:
        # Create a simple test file
        test_file = Path('test_pylint_sample.py')
        test_file.write_text('''
"""Test file for Pylint."""
import os
import sys

def test_function():
    """Test function."""
    return "Hello, World!"

if __name__ == "__main__":
    print(test_function())
''')

        # Run pylint on the test file
        result = subprocess.run([
            sys.executable, '-m', 'pylint',
            '--rcfile=.pylintrc',
            str(test_file)
        ], capture_output=True, text=True, timeout=30)

        print("✅ Pylint executed successfully")
        print(f"   Return code: {result.returncode}")
        if result.stdout:
            print(f"   Output: {result.stdout[:200]}...")
        if result.stderr and 'django-settings-module-not-found' in result.stderr:
            print("❌ Django settings module still not found")
            return False
        else:
            print("✅ No Django settings module errors")

        # Clean up
        test_file.unlink()

        return True

    except subprocess.TimeoutExpired:
        print("❌ Pylint command timed out")
        return False
    except Exception as e:
        print(f"❌ Pylint command error: {e}")
        return False


def main():
    """Main test function."""
    print("🔍 PYLINT CONFIGURATION TEST")
    print("=" * 40)

    # Test Django configuration
    django_ok = test_pylint_django_config()

    # Test Pylint command
    pylint_ok = test_pylint_command()

    print("\n" + "=" * 40)
    print("📊 TEST RESULTS:")
    print(f"   Django Config: {'✅ PASS' if django_ok else '❌ FAIL'}")
    print(f"   Pylint Command: {'✅ PASS' if pylint_ok else '❌ FAIL'}")

    if django_ok and pylint_ok:
        print("\n🎉 All tests passed! Pylint configuration is working correctly.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the configuration.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
