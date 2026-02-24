# Database Migration Workflow (v26.0.2 Diamond 32)

## Purpose
Safe, reversible database schema changes with zero-downtime deployment.

## Trigger
- New migration file created in `infrastructure/database/migrations/`
- Schema change required for feature development

## Steps

### 1. Create Migration
- Use Alembic: `alembic revision --autogenerate -m "description"`
- Review auto-generated migration for accuracy
- Add explicit `upgrade()` and `downgrade()` functions

### 2. Test Migration
- Run on local/dev database first
- Verify upgrade: `alembic upgrade head`
- Verify downgrade: `alembic downgrade -1`
- Run full test suite against migrated schema

### 3. Review
- PR must include migration file + model changes
- Reviewer checks: data loss risk, index impact, lock duration
- For large tables: confirm online DDL strategy (pt-online-schema-change)

### 4. Deploy
- Staging first: run migration, verify app compatibility
- Production: run during low-traffic window
- Monitor query performance for 30 minutes post-migration

### 5. Rollback Plan
- Keep previous Alembic revision hash documented in PR
- Rollback command: `alembic downgrade <previous_hash>`
- If data migration involved: verify backup exists before proceeding

## Related
- `prompts/22_database.md` — Database prompt
- `prompts/77_database_migrations.md` — Migration patterns
- `templates/ml/TEMPLATE-data-lineage.md` — Data lineage tracking
