#!/usr/bin/env python
"""
Create the missing core_systemsetting table by running Django migrations.
"""
import os
import sys
import django
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

try:
    # Setup Django
    django.setup()
    print("✓ Django setup successful")
    
    from django.core.management import execute_from_command_line
    
    # Run migrations for core module
    print("Running migrations for core module...")
    execute_from_command_line(['manage.py', 'migrate', 'core', '--verbosity=2'])
    
    # Check if table was created
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_systemsetting'")
        result = cursor.fetchone()
        if result:
            print("✓ core_systemsetting table created successfully")
        else:
            print("✗ core_systemsetting table not found")
            # List all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"Available tables: {tables}")
    
    print("\n=== Migration complete ===")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
