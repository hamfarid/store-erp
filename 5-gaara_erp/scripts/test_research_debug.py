#!/usr/bin/env python
"""Debug script to run research tests with proper environment setup."""
import os
import sys
import subprocess
from pathlib import Path

# Set up environment
os.environ['APP_MODE'] = 'test'
os.environ['DJANGO_SETTINGS_MODULE'] = 'gaara_erp.settings'
os.environ['TEST_EXTRA_APPS'] = 'agricultural_modules.research,agricultural_modules.nurseries'

# Change to project root
project_root = Path(__file__).parent.parent
os.chdir(project_root)

print(f"Working directory: {os.getcwd()}")
print(f"APP_MODE: {os.environ.get('APP_MODE')}")
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"TEST_EXTRA_APPS: {os.environ.get('TEST_EXTRA_APPS')}")

# Run pytest
cmd = [
    sys.executable, '-m', 'pytest', 
    'gaara_erp/agricultural_modules/research/tests',
    '-v', '--tb=short', '--maxfail=1'
]

print(f"Running: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)

print("\n=== STDOUT ===")
print(result.stdout)
print("\n=== STDERR ===")
print(result.stderr)
print(f"\n=== RETURN CODE: {result.returncode} ===")
