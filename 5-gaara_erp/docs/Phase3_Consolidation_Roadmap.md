# PHASE 3 - MODEL CONSOLIDATION ROADMAP

**Created**: 2025-11-18  
**Based On**: Deep Duplicate Analysis Results  
**Total Models to Review**: 12 (1 TRUE + 11 POTENTIAL)

---

## 🎯 EXECUTIVE SUMMARY

**Analysis Results**:
- **TRUE Duplicates (≥80%)**: 1 model (MUST consolidate)
- **Potential Duplicates (50-80%)**: 11 models (REVIEW needed)
- **False Positives (<50%)**: 49 models (NO action needed)

**Estimated Time**: 3-4 days (24-32 hours)

---

## 📋 CONSOLIDATION PRIORITY MATRIX

### P0 - CRITICAL (Must Consolidate)

#### 1. RestoreLog (80.0% similarity) ⚠️
**Models**:
- `database_management.RestoreLog`
- `system_backups.RestoreLog`

**Differences**:
- database_management: `target_database`, `restore_method`
- system_backups: `trigger_type`, `restore_type`

**Action**: CONSOLIDATE into `system_backups.RestoreLog`  
**Estimated Time**: 2 hours  
**Risk**: Low  
**Dependencies**: None

**Migration Steps**:
1. Add missing fields to system_backups.RestoreLog
2. Create data migration script
3. Update all references to database_management.RestoreLog
4. Test restore functionality
5. Remove database_management.RestoreLog

---

### P1 - HIGH PRIORITY (70-80% similarity)

#### 2. AuditLog (79.1% similarity)
**Models**:
- `security.AuditLog`
- `custom_admin.AuditLog`

**Action**: REVIEW → Likely consolidate into security.AuditLog  
**Estimated Time**: 3 hours  
**Risk**: Medium (security-critical)

#### 3. HarvestQualityGrade (78.6% similarity)
**Models**:
- `agricultural_experiments.HarvestQualityGrade`
- `experiments.HarvestQualityGrade`

**Action**: REVIEW → May be intentional domain separation  
**Estimated Time**: 2 hours  
**Risk**: Low

#### 4. AgentRole (70.0% similarity)
**Models**:
- `ai_permissions.AgentRole`
- `ai_agents.AgentRole`

**Action**: REVIEW → Likely consolidate into ai_permissions.AgentRole  
**Estimated Time**: 2 hours  
**Risk**: Medium

---

### P2 - MEDIUM PRIORITY (60-70% similarity)

#### 5. ExperimentVariety (61.8% similarity)
**Models**:
- `agricultural_experiments.ExperimentVariety`
- `experiments.ExperimentVariety`

**Action**: REVIEW → Domain separation analysis needed  
**Estimated Time**: 2 hours

#### 6. BackupSchedule (60.5% similarity)
**Models**:
- `database_management.BackupSchedule`
- `system_backups.BackupSchedule`

**Action**: CONSOLIDATE into system_backups.BackupSchedule  
**Estimated Time**: 2 hours

#### 7. Department (59.2% similarity)
**Models**:
- `core.Department`
- `organization.Department`

**Action**: REVIEW → High-impact, needs careful analysis  
**Estimated Time**: 4 hours  
**Risk**: High (widely used)

---

### P3 - LOW PRIORITY (50-60% similarity)

#### 8. Harvest (55.0% similarity)
**Models**:
- `agricultural_experiments.Harvest`
- `experiments.Harvest`

**Action**: REVIEW → Domain separation likely correct  
**Estimated Time**: 2 hours

#### 9. AIRole (53.7% similarity)
**Models**:
- `permissions.AIRole`
- `ai_permissions.AIRole`

**Action**: REVIEW → Consolidate into ai_permissions.AIRole  
**Estimated Time**: 2 hours

#### 10. Message (52.7% similarity)
**Models**:
- `ai.Message`
- `intelligent_assistant.Message`

**Action**: REVIEW → Domain separation analysis needed  
**Estimated Time**: 2 hours

#### 11. BackupLog (51.4% similarity)
**Models**:
- `database_management.BackupLog`
- `system_backups.BackupLog`

**Action**: CONSOLIDATE into system_backups.BackupLog  
**Estimated Time**: 2 hours

#### 12. Country (50.0% similarity)
**Models**:
- `core.Country`
- `contacts.Country`

**Action**: REVIEW → Borderline, may keep separate  
**Estimated Time**: 2 hours

---

## 📅 EXECUTION TIMELINE

### Day 2 (8 hours)
**Morning (4 hours)**:
- [ ] Consolidate RestoreLog (P0) - 2 hours
- [ ] Review AuditLog (P1) - 2 hours

**Afternoon (4 hours)**:
- [ ] Review HarvestQualityGrade (P1) - 2 hours
- [ ] Review AgentRole (P1) - 2 hours

### Day 3 (8 hours)
**Morning (4 hours)**:
- [ ] Review ExperimentVariety (P2) - 2 hours
- [ ] Consolidate BackupSchedule (P2) - 2 hours

**Afternoon (4 hours)**:
- [ ] Review Department (P2) - 4 hours (high-impact)

### Day 4 (8 hours)
**Morning (4 hours)**:
- [ ] Review Harvest (P3) - 2 hours
- [ ] Review AIRole (P3) - 2 hours

**Afternoon (4 hours)**:
- [ ] Review Message (P3) - 2 hours
- [ ] Consolidate BackupLog (P3) - 2 hours

### Day 5 (4 hours)
**Morning (4 hours)**:
- [ ] Review Country (P3) - 2 hours
- [ ] Final testing and documentation - 2 hours

---

## 🔧 CONSOLIDATION PROCESS (Standard)

For each consolidation:

1. **Analysis** (30 min)
   - Compare field structures
   - Identify unique fields
   - Map relationships
   - Check usage patterns

2. **Planning** (30 min)
   - Choose target model
   - Design migration strategy
   - Identify breaking changes
   - Create rollback plan

3. **Implementation** (45 min)
   - Add missing fields to target
   - Create data migration
   - Update all references
   - Update tests

4. **Testing** (15 min)
   - Run unit tests
   - Run integration tests
   - Verify data integrity
   - Test rollback

---

## ✅ SUCCESS CRITERIA

- [ ] All P0 models consolidated
- [ ] All P1 models reviewed and decision documented
- [ ] All P2 models reviewed
- [ ] All migrations tested
- [ ] Zero data loss
- [ ] All tests passing
- [ ] Documentation updated

---

**Total Estimated Time**: 24-32 hours (3-4 days)  
**Start Date**: Day 2  
**Target Completion**: Day 5

