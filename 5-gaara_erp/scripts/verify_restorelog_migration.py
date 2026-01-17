#!/usr/bin/env python3
# FILE: scripts/verify_restorelog_migration.py
# PURPOSE: Verify RestoreLog data migration integrity
# OWNER: Architecture Team
# LAST-AUDITED: 2025-11-18

"""
RestoreLog Migration Verification Script

This script verifies the integrity of the RestoreLog data migration
from database_management to system_backups.

Usage:
    python scripts/verify_restorelog_migration.py [--before|--after]
    
    --before: Run before migration (shows source data)
    --after: Run after migration (verifies migration)
"""

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

from django.db.models import Count, Q


def verify_before_migration():
    """Verify data before migration - show source data."""
    
    print("="*80)
    print("RESTORELOG MIGRATION - PRE-MIGRATION VERIFICATION")
    print("="*80)
    print()
    
    try:
        from admin_modules.database_management.models import RestoreLog as OldRestoreLog
        
        # Count records
        old_count = OldRestoreLog.objects.count()
        print(f"📊 database_management.RestoreLog: {old_count} records")
        
        if old_count > 0:
            # Show status breakdown
            print(f"\n📈 Status Breakdown:")
            status_counts = OldRestoreLog.objects.values('status').annotate(count=Count('id'))
            for item in status_counts:
                print(f"   - {item['status']}: {item['count']} records")
            
            # Show restore_method breakdown
            print(f"\n📈 Restore Method Breakdown:")
            method_counts = OldRestoreLog.objects.values('restore_method').annotate(count=Count('id'))
            for item in method_counts:
                print(f"   - {item['restore_method']}: {item['count']} records")
            
            # Show sample records
            print(f"\n📋 Sample Records (first 5):")
            for log in OldRestoreLog.objects.all()[:5]:
                print(f"   - {log.name} | {log.status} | {log.restore_method} | {log.target_database}")
        
    except Exception as e:
        print(f"❌ Error accessing database_management.RestoreLog: {e}")
    
    try:
        from admin_modules.system_backups.models import RestoreLog as NewRestoreLog
        
        new_count = NewRestoreLog.objects.count()
        print(f"\n📊 system_backups.RestoreLog: {new_count} records (before migration)")
        
    except Exception as e:
        print(f"❌ Error accessing system_backups.RestoreLog: {e}")
    
    print("\n" + "="*80)
    print("✅ Pre-migration verification complete")
    print("="*80)


def verify_after_migration():
    """Verify data after migration - check integrity."""
    
    print("="*80)
    print("RESTORELOG MIGRATION - POST-MIGRATION VERIFICATION")
    print("="*80)
    print()
    
    try:
        from admin_modules.database_management.models import RestoreLog as OldRestoreLog
        from admin_modules.system_backups.models import RestoreLog as NewRestoreLog
        
        # Count records
        old_count = OldRestoreLog.objects.count()
        new_count = NewRestoreLog.objects.count()
        
        print(f"📊 Source (database_management): {old_count} records")
        print(f"📊 Target (system_backups): {new_count} records")
        
        # Check if counts match
        if new_count >= old_count:
            print(f"✅ Record count OK (target has {new_count - old_count} additional records)")
        else:
            print(f"⚠️  WARNING: Target has fewer records ({old_count - new_count} missing)")
        
        # Verify field mapping
        print(f"\n🔍 Verifying Field Mapping:")
        
        errors = []
        verified = 0
        
        for old_log in OldRestoreLog.objects.all():
            # Find corresponding record in new system
            try:
                new_log = NewRestoreLog.objects.get(
                    name=old_log.name,
                    created_at=old_log.created_at
                )
                
                # Verify field mapping
                checks = [
                    (old_log.name == new_log.name, "name"),
                    (old_log.status == new_log.status, "status"),
                    (old_log.restore_method == new_log.trigger_type, "restore_method → trigger_type"),
                    (old_log.target_database == new_log.target_database, "target_database"),
                    (old_log.started_at == new_log.started_at, "started_at"),
                    (old_log.completed_at == new_log.completed_at, "completed_at"),
                    (old_log.duration_seconds == new_log.duration_seconds, "duration_seconds"),
                    (old_log.message == new_log.message, "message"),
                    (old_log.created_by == new_log.created_by, "created_by"),
                ]
                
                failed_checks = [field for passed, field in checks if not passed]
                
                if failed_checks:
                    errors.append(f"{old_log.name}: Failed checks: {', '.join(failed_checks)}")
                else:
                    verified += 1
                
            except NewRestoreLog.DoesNotExist:
                errors.append(f"{old_log.name}: Not found in target")
            except NewRestoreLog.MultipleObjectsReturned:
                errors.append(f"{old_log.name}: Multiple records found in target")
        
        print(f"   ✅ Verified: {verified} records")
        print(f"   ❌ Errors: {len(errors)} records")
        
        if errors:
            print(f"\n⚠️  ERRORS:")
            for error in errors[:10]:  # Show first 10 errors
                print(f"   - {error}")
            if len(errors) > 10:
                print(f"   ... and {len(errors) - 10} more errors")
        
        # Verify trigger_type mapping
        print(f"\n📈 Trigger Type Mapping Verification:")
        trigger_counts = NewRestoreLog.objects.values('trigger_type').annotate(count=Count('id'))
        for item in trigger_counts:
            print(f"   - {item['trigger_type']}: {item['count']} records")
        
        # Verify restore_type defaults
        print(f"\n📈 Restore Type Distribution:")
        restore_counts = NewRestoreLog.objects.values('restore_type').annotate(count=Count('id'))
        for item in restore_counts:
            print(f"   - {item['restore_type']}: {item['count']} records")
        
        # Final verdict
        print(f"\n{'='*80}")
        if len(errors) == 0 and new_count >= old_count:
            print("✅ MIGRATION SUCCESSFUL - All data verified")
        else:
            print(f"⚠️  MIGRATION COMPLETED WITH ISSUES - {len(errors)} errors found")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify RestoreLog migration')
    parser.add_argument('--before', action='store_true', help='Run before migration')
    parser.add_argument('--after', action='store_true', help='Run after migration')
    
    args = parser.parse_args()
    
    if args.before:
        verify_before_migration()
    elif args.after:
        verify_after_migration()
    else:
        print("Usage: python scripts/verify_restorelog_migration.py [--before|--after]")
        print()
        print("  --before: Run before migration (shows source data)")
        print("  --after: Run after migration (verifies migration)")

