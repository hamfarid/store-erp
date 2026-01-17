#!/usr/bin/env python3
# FILE: scripts/verify_restorelog_model.py
# PURPOSE: Verify RestoreLog model has all required fields
# OWNER: Architecture Team
# LAST-AUDITED: 2025-11-18

import os
import sys
import django
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
sys.path.insert(0, str(PROJECT_ROOT))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings.dev')
django.setup()

from admin_modules.system_backups.models import RestoreLog

print("="*80)
print("RESTORELOG MODEL VERIFICATION")
print("="*80)
print()

# Get all fields
fields = [f.name for f in RestoreLog._meta.fields]

print("✅ RestoreLog model imported successfully")
print()
print(f"📊 Total Fields: {len(fields)}")
print()

# Required fields
required_fields = [
    'id',
    'name',
    'source_backup',
    'restore_type',
    'trigger_type',
    'status',
    'started_at',
    'completed_at',
    'duration_seconds',
    'message',
    'target_database',  # NEW FIELD
    'is_overwrite',
    'created_by',
    'created_at',
    'updated_at',
]

print("🔍 Field Verification:")
all_present = True
for field in required_fields:
    if field in fields:
        print(f"   ✅ {field}")
    else:
        print(f"   ❌ {field} - MISSING!")
        all_present = False

print()
print("="*80)
if all_present:
    print("✅ ALL REQUIRED FIELDS PRESENT")
else:
    print("❌ SOME FIELDS MISSING")
print("="*80)

