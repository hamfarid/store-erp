#!/usr/bin/env python3
# FILE: scripts/find_duplicate_app_labels.py | PURPOSE: Find all duplicate app labels | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Find Duplicate App Labels

This script scans all Django apps in INSTALLED_APPS and identifies duplicate app labels.

Usage:
    python scripts/find_duplicate_app_labels.py
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
sys.path.insert(0, str(PROJECT_ROOT))

# Setup Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings.base')

# Import settings
from django.conf import settings

def find_duplicate_app_labels():
    """Find all duplicate app labels in INSTALLED_APPS."""
    
    print("="*80)
    print("SCANNING FOR DUPLICATE APP LABELS")
    print("="*80)
    print()
    
    # Get all installed apps
    installed_apps = settings.INSTALLED_APPS
    
    print(f"Total apps in INSTALLED_APPS: {len(installed_apps)}\n")
    
    # Track app labels
    app_labels = defaultdict(list)
    
    for app_path in installed_apps:
        # Extract app label (last part of the path)
        app_label = app_path.split('.')[-1]
        app_labels[app_label].append(app_path)
    
    # Find duplicates
    duplicates = {label: paths for label, paths in app_labels.items() if len(paths) > 1}
    
    if duplicates:
        print(f"❌ FOUND {len(duplicates)} DUPLICATE APP LABELS:\n")
        
        for label, paths in sorted(duplicates.items()):
            print(f"  {label} ({len(paths)} occurrences):")
            for path in paths:
                # Check if apps.py exists
                app_file = PROJECT_ROOT / path.replace('.', '/') / 'apps.py'
                has_apps = "✓" if app_file.exists() else "✗"
                print(f"    {has_apps} {path}")
            print()
        
        return list(duplicates.keys())
    else:
        print("✓ NO DUPLICATE APP LABELS FOUND\n")
        return []


def check_apps_py_files():
    """Check which apps have apps.py files."""
    
    print("="*80)
    print("CHECKING FOR MISSING apps.py FILES")
    print("="*80)
    print()
    
    installed_apps = settings.INSTALLED_APPS
    missing_apps_py = []
    
    for app_path in installed_apps:
        # Skip Django built-in apps
        if app_path.startswith('django.'):
            continue
        
        # Check if apps.py exists
        app_file = PROJECT_ROOT / app_path.replace('.', '/') / 'apps.py'
        
        if not app_file.exists():
            missing_apps_py.append(app_path)
            print(f"  ✗ {app_path}")
    
    if missing_apps_py:
        print(f"\n❌ {len(missing_apps_py)} apps missing apps.py\n")
    else:
        print("\n✓ All apps have apps.py files\n")
    
    return missing_apps_py


if __name__ == "__main__":
    try:
        duplicates = find_duplicate_app_labels()
        missing = check_apps_py_files()
        
        print("="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Duplicate app labels: {len(duplicates)}")
        print(f"Missing apps.py files: {len(missing)}")
        
        if duplicates or missing:
            print("\n⚠️  ACTION REQUIRED")
            sys.exit(1)
        else:
            print("\n✓ ALL CHECKS PASSED")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

