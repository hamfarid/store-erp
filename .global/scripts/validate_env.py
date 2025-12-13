#!/usr/bin/env python3
"""
File: scripts/validate_env.py
Validate environment variables in .env file
"""

import os
import sys
from typing import Dict, List, Any

# Define required variables
REQUIRED_VARS = {
    'APP_ENV': {
        'required': True,
        'allowed_values': ['development', 'staging', 'production'],
        'description': 'Application environment'
    },
    'SECRET_KEY': {
        'required': True,
        'min_length': 32,
        'description': 'Application secret key'
    },
}


def validate_env() -> Dict[str, Any]:
    """Validate environment variables"""
    errors = []
    warnings = []

    # Check required variables
    for var, config in REQUIRED_VARS.items():
        value = os.getenv(var)

        if not value:
            if config['required']:
                errors.append(
                    f"❌ Missing required variable: {var} - {config['description']}")
            continue

        # Check allowed values
        if 'allowed_values' in config:
            if value not in config['allowed_values']:
                errors.append(
                    f"❌ Invalid value for {var}: '{value}'. "
                    f"Allowed: {', '.join(config['allowed_values'])}"
                )

        # Check minimum length
        if 'min_length' in config:
            if len(value) < config['min_length']:
                errors.append(
                    f"❌ {var} is too short. "
                    f"Minimum length: {config['min_length']}, got: {len(value)}")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
    }


def main():
    """Main validation function"""
    print("=" * 60)
    print("Environment Variables Validation")
    print("=" * 60)
    print()

    result = validate_env()

    # Print errors
    if result['errors']:
        print("ERRORS:")
        for error in result['errors']:
            print(f"  {error}")
        print()

    # Print warnings
    if result['warnings']:
        print("WARNINGS:")
        for warning in result['warnings']:
            print(f"  {warning}")
        print()

    # Summary
    if result['valid']:
        print("✅ All required environment variables are set correctly!")
        return 0
    else:
        print(f"❌ Validation failed with {len(result['errors'])} error(s)")
        return 1


if __name__ == '__main__':
    sys.exit(main())
