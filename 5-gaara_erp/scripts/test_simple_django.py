#!/usr/bin/env python
"""Simple Django test to verify settings and basic functionality."""
import os
import sys
import django
from pathlib import Path

# Set up environment
os.environ['APP_MODE'] = 'test'
os.environ['DJANGO_SETTINGS_MODULE'] = 'gaara_erp.settings'
os.environ['TEST_EXTRA_APPS'] = 'agricultural_modules.research,agricultural_modules.nurseries'

# Change to gaara_erp directory
project_root = Path(__file__).parent.parent
gaara_erp_dir = project_root / "gaara_erp"
sys.path.insert(0, str(gaara_erp_dir))
os.chdir(gaara_erp_dir)

print(f"Working directory: {os.getcwd()}")
print(f"Python path includes: {gaara_erp_dir}")

try:
    # Setup Django
    django.setup()
    print("✓ Django setup successful")
    
    # Test basic imports
    from django.conf import settings
    print(f"✓ Settings loaded: {settings.SETTINGS_MODULE}")
    print(f"✓ Installed apps count: {len(settings.INSTALLED_APPS)}")
    
    # Test database connection
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='companies_company'")
        result = cursor.fetchone()
        if result:
            print("✓ companies_company table exists")
            cursor.execute("PRAGMA table_info(companies_company)")
            columns = [row[1] for row in cursor.fetchall()]
            if 'code' in columns:
                print("✓ companies_company.code column exists")
            else:
                print("✗ companies_company.code column missing")
                print(f"Available columns: {columns}")
        else:
            print("✗ companies_company table not found")
    
    # Test model imports
    try:
        from agricultural_modules.research.models import ResearchProject
        print("✓ ResearchProject model imported successfully")
    except Exception as e:
        print(f"✗ ResearchProject import failed: {e}")
    
    try:
        from agricultural_modules.nurseries.models import Nursery
        print("✓ Nursery model imported successfully")
    except Exception as e:
        print(f"✗ Nursery import failed: {e}")
    
    print("\n=== Django setup complete ===")
    
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
