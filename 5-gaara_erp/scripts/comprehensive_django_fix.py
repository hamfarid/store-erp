#!/usr/bin/env python
"""
Comprehensive Django setup and database fix script.
Addresses all the issues found in the Django setup output.
"""
import os
import sys
import django
import warnings
from pathlib import Path

# Set up environment
os.environ['APP_MODE'] = 'test'
os.environ['DJANGO_SETTINGS_MODULE'] = 'gaara_erp.settings'

# Change to gaara_erp directory
project_root = Path(__file__).parent.parent
gaara_erp_dir = project_root / "gaara_erp"
sys.path.insert(0, str(gaara_erp_dir))
os.chdir(gaara_erp_dir)

print(f"Working directory: {os.getcwd()}")

# Suppress warnings during setup
warnings.filterwarnings("ignore", category=RuntimeWarning, module="django.db.backends.utils")
warnings.filterwarnings("ignore", message="Model.*was already registered")

try:
    # Setup Django
    django.setup()
    print("✓ Django setup successful")
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    # Step 1: Create all missing tables
    print("\n=== Step 1: Running migrations ===")
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=1'])
    
    # Step 2: Check critical tables
    print("\n=== Step 2: Checking critical tables ===")
    critical_tables = [
        'core_systemsetting',
        'companies_company', 
        'core_country',
        'core_currency',
        'core_branch',
        'core_department'
    ]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        for table in critical_tables:
            if table in existing_tables:
                print(f"✓ {table} exists")
            else:
                print(f"✗ {table} missing")
        
        # Check companies_company specifically for code column
        if 'companies_company' in existing_tables:
            cursor.execute("PRAGMA table_info(companies_company)")
            columns = [row[1] for row in cursor.fetchall()]
            if 'code' in columns:
                print("✓ companies_company.code column exists")
            else:
                print("✗ companies_company.code column missing")
    
    # Step 3: Test model imports
    print("\n=== Step 3: Testing model imports ===")
    try:
        from core_modules.core.models import SystemSetting
        print("✓ SystemSetting imported successfully")
    except Exception as e:
        print(f"✗ SystemSetting import failed: {e}")
    
    try:
        from core_modules.companies.models import Company
        print("✓ Company imported successfully")
    except Exception as e:
        print(f"✗ Company import failed: {e}")
    
    try:
        from agricultural_modules.research.models import ResearchProject
        print("✓ ResearchProject imported successfully")
    except Exception as e:
        print(f"✗ ResearchProject import failed: {e}")
    
    # Step 4: Test basic database operations
    print("\n=== Step 4: Testing database operations ===")
    try:
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        print(f"✓ User model accessible, count: {user_count}")
    except Exception as e:
        print(f"✗ User model test failed: {e}")
    
    # Step 5: Create default SystemSetting if missing
    print("\n=== Step 5: Creating default settings ===")
    try:
        from core_modules.core.models import SystemSetting
        if not SystemSetting.objects.filter(key='default_setup').exists():
            SystemSetting.objects.create(
                key='default_setup',
                value='true',
                description='Default setup completed'
            )
            print("✓ Default SystemSetting created")
        else:
            print("✓ Default SystemSetting already exists")
    except Exception as e:
        print(f"✗ SystemSetting creation failed: {e}")
    
    print("\n=== Django setup and fix complete ===")
    
except Exception as e:
    print(f"✗ Critical error: {e}")
    import traceback
    traceback.print_exc()
