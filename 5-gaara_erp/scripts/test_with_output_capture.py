#!/usr/bin/env python
"""
Test script with explicit output capture to debug PowerShell output issues.
"""
import os
import sys
import subprocess
from pathlib import Path

# Set up environment
os.environ['APP_MODE'] = 'test'
os.environ['DJANGO_SETTINGS_MODULE'] = 'gaara_erp.settings'

# Change to project root
project_root = Path(__file__).parent.parent
os.chdir(project_root)

print(f"Working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Environment variables:")
print(f"  APP_MODE: {os.environ.get('APP_MODE')}")
print(f"  DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Test 1: Basic Django setup
print("\n=== Test 1: Basic Django setup ===")
try:
    result = subprocess.run([
        sys.executable, 'scripts/comprehensive_django_fix.py'
    ], capture_output=True, text=True, timeout=300)
    
    print(f"Return code: {result.returncode}")
    print(f"STDOUT length: {len(result.stdout)}")
    print(f"STDERR length: {len(result.stderr)}")
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        
except subprocess.TimeoutExpired:
    print("Process timed out")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Simple pytest run
print("\n=== Test 2: Simple pytest collection ===")
try:
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 
        'gaara_erp/agricultural_modules/research/tests',
        '--collect-only', '-q'
    ], capture_output=True, text=True, timeout=120, 
    env={**os.environ, 'TEST_EXTRA_APPS': 'agricultural_modules.research,agricultural_modules.nurseries'})
    
    print(f"Return code: {result.returncode}")
    print(f"STDOUT length: {len(result.stdout)}")
    print(f"STDERR length: {len(result.stderr)}")
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        
except subprocess.TimeoutExpired:
    print("Process timed out")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Direct Django command
print("\n=== Test 3: Django management command ===")
try:
    result = subprocess.run([
        sys.executable, 'gaara_erp/manage.py', 'check', '--verbosity=2'
    ], capture_output=True, text=True, timeout=120)
    
    print(f"Return code: {result.returncode}")
    print(f"STDOUT length: {len(result.stdout)}")
    print(f"STDERR length: {len(result.stderr)}")
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        
except subprocess.TimeoutExpired:
    print("Process timed out")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Output capture test complete ===")
