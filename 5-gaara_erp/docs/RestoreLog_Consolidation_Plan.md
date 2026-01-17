# RestoreLog Consolidation Plan (P0 - CRITICAL)

**Date**: 2025-11-18  
**Priority**: P0 (Must Complete)  
**Similarity**: 80.0% (TRUE Duplicate)  
**Estimated Time**: 2 hours  
**Status**: PLANNING

---

## 📊 ANALYSIS SUMMARY

### Models to Consolidate:
1. **Source**: `database_management.RestoreLog` (will be deprecated)
2. **Target**: `system_backups.RestoreLog` (will be enhanced)

### Similarity Breakdown:
- **Fields**: 75.0% similar
- **Relationships**: 100.0% similar (both have source_backup ForeignKey)
- **Methods**: 100.0% similar (__str__, save)
- **Overall**: 80.0% similar

---

## 🔍 FIELD COMPARISON

### Common Fields (Both Models):
✅ `name` - CharField(255)  
✅ `source_backup` - ForeignKey(BackupLog)  
✅ `status` - CharField with STATUS_CHOICES  
✅ `started_at` - DateTimeField  
✅ `completed_at` - DateTimeField  
✅ `duration_seconds` - PositiveIntegerField  
✅ `message` - TextField  
✅ `created_by` - ForeignKey(User)  
✅ `created_at` - DateTimeField(auto_now_add)  
✅ `updated_at` - DateTimeField(auto_now)

### Unique to database_management.RestoreLog:
⚠️ `restore_method` - CharField (manual/automatic/recovery)  
⚠️ `target_database` - CharField(100)

### Unique to system_backups.RestoreLog:
⚠️ `restore_type` - CharField (database/files/full/custom)  
⚠️ `trigger_type` - CharField (manual/automatic/recovery)  
⚠️ `is_overwrite` - BooleanField

---

## 🎯 CONSOLIDATION STRATEGY

### Target Model: `system_backups.RestoreLog`

**Rationale**:
1. More comprehensive (has restore_type, trigger_type, is_overwrite)
2. Part of broader system_backups module
3. Better aligned with BackupLog in same module
4. More flexible for future enhancements

### Fields to Add to Target:
1. **`target_database`** (from database_management)
   - Type: CharField(100)
   - Purpose: Specify which database to restore to
   - Default: Can be derived from backup if not specified

2. **`restore_method`** (from database_management)
   - **DECISION**: Map to existing `trigger_type` field
   - Both serve same purpose (how restore was initiated)
   - No new field needed

### Field Mapping:
```
database_management.RestoreLog → system_backups.RestoreLog
-----------------------------------------------------------
name                    → name
source_backup           → source_backup
restore_method          → trigger_type (MAPPED)
status                  → status
target_database         → target_database (NEW FIELD)
started_at              → started_at
completed_at            → completed_at
duration_seconds        → duration_seconds
message                 → message
created_by              → created_by
created_at              → created_at
updated_at              → updated_at
```

---

## 📋 IMPLEMENTATION STEPS

### Step 1: Enhance Target Model (30 min)
- [  ] Add `target_database` field to system_backups.RestoreLog
- [  ] Update Meta indexes if needed
- [  ] Create migration file
- [  ] Test migration in development

### Step 2: Create Data Migration (30 min)
- [  ] Create data migration script
- [  ] Map restore_method → trigger_type
- [  ] Copy all records from database_management to system_backups
- [  ] Verify data integrity
- [  ] Test rollback procedure

### Step 3: Update All References (45 min)
- [  ] Find all imports of database_management.RestoreLog
- [  ] Update to system_backups.RestoreLog
- [  ] Update serializers
- [  ] Update views/viewsets
- [  ] Update admin.py
- [  ] Update tests

### Step 4: Testing (15 min)
- [  ] Run unit tests
- [  ] Run integration tests
- [  ] Verify Django check passes
- [  ] Test restore functionality
- [  ] Verify no broken imports

---

## 🔧 MIGRATION SCRIPT OUTLINE

```python
# Migration: Consolidate RestoreLog models

from django.db import migrations

def migrate_restore_logs(apps, schema_editor):
    """Migrate data from database_management to system_backups"""
    
    # Get models
    OldRestoreLog = apps.get_model('database_management', 'RestoreLog')
    NewRestoreLog = apps.get_model('system_backups', 'RestoreLog')
    
    # Migrate each record
    for old_log in OldRestoreLog.objects.all():
        NewRestoreLog.objects.create(
            name=old_log.name,
            source_backup=old_log.source_backup,
            trigger_type=old_log.restore_method,  # MAP
            restore_type='database',  # Default for DB restores
            status=old_log.status,
            target_database=old_log.target_database,  # NEW
            started_at=old_log.started_at,
            completed_at=old_log.completed_at,
            duration_seconds=old_log.duration_seconds,
            message=old_log.message,
            is_overwrite=False,  # Default
            created_by=old_log.created_by,
            created_at=old_log.created_at,
            updated_at=old_log.updated_at,
        )

class Migration(migrations.Migration):
    dependencies = [
        ('system_backups', '0001_add_target_database'),
        ('database_management', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(migrate_restore_logs),
    ]
```

---

## 📝 FILES TO UPDATE

### Models:
- [  ] `admin_modules/system_backups/models.py` - Add target_database field
- [  ] `admin_modules/database_management/models.py` - Mark as deprecated

### Serializers:
- [  ] `admin_modules/database_management/serializers.py` - Update import
- [  ] `admin_modules/reports/serializers.py` - Update import (if exists)

### Views:
- [  ] Find all views using database_management.RestoreLog
- [  ] Update imports

### Admin:
- [  ] `admin_modules/database_management/admin.py` - Update or remove
- [  ] `admin_modules/system_backups/admin.py` - Verify registration

### Tests:
- [  ] Update all test imports
- [  ] Add tests for target_database field

---

## ✅ ACCEPTANCE CRITERIA

- [  ] Target model has all necessary fields
- [  ] All data migrated successfully (0 data loss)
- [  ] All references updated
- [  ] All tests passing
- [  ] Django check: 0 errors
- [  ] Restore functionality works
- [  ] Documentation updated
- [  ] Old model marked as deprecated (not deleted yet)

---

## 🚨 RISKS & MITIGATION

### Risk 1: Data Loss
**Mitigation**: 
- Create full database backup before migration
- Test migration in development first
- Verify record count matches

### Risk 2: Broken References
**Mitigation**:
- Search entire codebase for imports
- Use IDE refactoring tools
- Run comprehensive tests

### Risk 3: Different BackupLog Models
**Issue**: database_management.RestoreLog references database_management.BackupLog  
**Mitigation**: 
- Keep ForeignKey flexible
- May need to migrate BackupLog references too
- Document this dependency

---

## 📅 TIMELINE

**Total**: 2 hours

- **10:30-11:00** (30 min): Enhance target model + create migration
- **11:00-11:30** (30 min): Create data migration script
- **11:30-12:15** (45 min): Update all references
- **12:15-12:30** (15 min): Testing & verification

---

**Status**: READY TO EXECUTE  
**Next**: Begin Step 1 - Enhance Target Model

