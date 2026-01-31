# Research: Gaara ERP v12 - Technical Decisions

**Plan Reference**: [plan.md](plan.md)  
**Date**: 2026-01-22  
**Status**: Phase 0 Complete

---

## R-01: Django Multi-Tenancy Best Practices

### Decision: PostgreSQL Schema-Based Isolation

**Rationale**:

- Full data isolation between tenants (constitutional requirement §2.2)
- Native PostgreSQL support for schema switching
- Simpler backup/restore per tenant
- Compliance with SOC2/ISO27001 data segregation requirements

**Alternatives Considered**:

| Approach | Pros | Cons | Rejected Because |
|----------|------|------|------------------|
| Shared Database, Shared Schema | Simple, cheap | No isolation, security risk | Violates Constitution §2.2 |
| Shared Database, Separate Schemas | Good isolation, moderate complexity | Connection pooling complexity | ✅ **Selected** |
| Separate Databases | Complete isolation | Expensive, complex migrations | Over-engineering for current scale |

**Implementation Pattern**:

```python
# Middleware approach
class TenantMiddleware:
    def __call__(self, request):
        tenant = self.resolve_tenant(request)
        connection.set_schema(tenant.schema_name)
        request.tenant = tenant
        return self.get_response(request)
    
    def resolve_tenant(self, request):
        # Priority: Subdomain > Custom Domain > Header
        subdomain = self.get_subdomain(request)
        if subdomain:
            return Tenant.objects.get(subdomain=subdomain)
        # ... fallback logic
```

**Dependencies**:

- `django-tenants` or custom implementation
- PostgreSQL 15.x with `search_path` support

---

## R-02: MFA Implementation Patterns

### Decision: Three-Method MFA with Graceful Degradation

**Rationale**:

- Constitutional mandate §2.3 requires SMS, TOTP, and Email OTP
- Graceful degradation ensures user access if one method fails
- Industry standard for enterprise security

**Implementation Strategy**:

| Method | Library/Service | Priority | Fallback |
|--------|-----------------|----------|----------|
| TOTP | `pyotp` | Primary | Yes |
| SMS OTP | Twilio/AWS SNS | Secondary | Yes |
| Email OTP | Django email | Tertiary | Final |

**Security Flow**:

```
1. User enters credentials → Validate
2. If valid → Check MFA enrollment
3. If enrolled → Present MFA options
4. User selects method → Generate OTP
5. User enters OTP → Validate
6. If valid → Issue JWT (1h access, 24h refresh)
```

**Key Requirements**:

- OTP validity: 5 minutes
- Rate limit: 3 attempts per 15 minutes
- Backup codes: 10 single-use codes at enrollment
- Device remembering: Optional 30-day trust

**Dependencies**:

- `pyotp==2.9.0` - TOTP generation/validation
- Twilio SDK or AWS SNS for SMS
- Django email backend

---

## R-03: PostgreSQL Schema Management

### Decision: Dynamic Schema Creation with Migration Tracking

**Rationale**:

- Each tenant needs isolated schema at registration
- Migrations must apply to all schemas
- Connection pooling must handle schema switching

**Schema Lifecycle**:

```
1. Tenant Registration → Create schema (CREATE SCHEMA tenant_xyz)
2. Apply base migrations → Run Django migrate on new schema
3. Active Use → Middleware sets search_path per request
4. Tenant Deletion → Archive schema, then drop after retention period
```

**Migration Strategy**:

```python
# Custom migration runner
def migrate_all_tenants():
    for tenant in Tenant.objects.all():
        with schema_context(tenant.schema_name):
            call_command('migrate', '--database=default')
```

**Connection Pooling**:

- Use `django-db-connection-pool` with per-schema pooling
- PgBouncer in transaction mode (compatible with schema switching)

**Shared vs Tenant Data**:

| Location | Data Type |
|----------|-----------|
| `public` schema | Tenants, Plans, Global Config |
| `tenant_*` schema | All business data (invoices, products, users, etc.) |

---

## R-04: HR Module Data Models

### Decision: Standard HR Schema with Saudi Labor Law Compliance

**Rationale**:

- Primary market is Saudi Arabia (SAR base currency per constitution)
- Must support GOSI (General Organization for Social Insurance) compliance
- Arabic-first with English support

**Core Entities**:

| Entity | Purpose | Key Fields |
|--------|---------|------------|
| Employee | Staff records | national_id, iqama_number, gosi_number, hire_date |
| Department | Org structure | name_ar, name_en, manager_id, parent_id |
| Attendance | Time tracking | employee_id, check_in, check_out, location |
| Leave | Absence management | type, start_date, end_date, status, approver_id |
| Payroll | Salary processing | base_salary, allowances, deductions, gosi_contribution |
| Contract | Employment terms | type (full-time/part-time/contract), start_date, end_date |

**Leave Types (Saudi Standard)**:

- Annual Leave (21-30 days based on tenure)
- Sick Leave (120 days per year)
- Hajj Leave (10-15 days, once per employment)
- Maternity Leave (70 days)
- Paternity Leave (3 days)
- Marriage Leave (5 days)
- Bereavement Leave (5 days)

**Payroll Calculations**:

- GOSI Employee Contribution: 9.75% (capped at 45,000 SAR)
- GOSI Employer Contribution: 11.75%
- Vacation pay calculation on termination

---

## R-05: Project Management Patterns

### Decision: Hierarchical Task Model with Dependency Tracking

**Rationale**:

- Constitution requires Projects module (PRJ-01 to PRJ-06)
- Must support Gantt chart visualization
- Resource allocation and time tracking needed

**Core Entities**:

| Entity | Purpose | Key Fields |
|--------|---------|------------|
| Project | Top-level container | name, status, start_date, end_date, budget, manager_id |
| Milestone | Key deliverables | project_id, name, due_date, status |
| Task | Work items | project_id, milestone_id, name, assignee_id, priority |
| TaskDependency | Sequencing | task_id, depends_on_task_id, type (FS/SS/FF/SF) |
| TimeLog | Time tracking | task_id, employee_id, hours, date, description |
| ResourceAllocation | Team assignment | project_id, employee_id, allocation_percentage |

**Dependency Types**:

- FS (Finish-to-Start): Default, B starts after A finishes
- SS (Start-to-Start): B starts when A starts
- FF (Finish-to-Finish): B finishes when A finishes
- SF (Start-to-Finish): B finishes when A starts

**Status Flow**:

```
Draft → Planned → In Progress → On Hold → Completed → Archived
                      ↓
                  Cancelled
```

---

## R-06: Django-Celery Integration

### Decision: Redis-Backed Celery with Beat Scheduler

**Rationale**:

- AI modules require async processing (plant diagnosis, forecasting)
- Background tasks for report generation, notifications
- Scheduled tasks for daily/weekly operations

**Task Categories**:

| Category | Examples | Priority |
|----------|----------|----------|
| AI Processing | Plant diagnosis, demand forecasting | High |
| Notifications | Email/SMS alerts, reminders | Medium |
| Reports | Daily summaries, financial reports | Medium |
| Maintenance | Cleanup, archival, backups | Low |

**Configuration**:

```python
# celery.py
app = Celery('gaara_erp')
app.config_from_object('django.conf:settings', namespace='CELERY')

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Riyadh'
```

**Tenant-Aware Tasks**:

```python
@app.task(bind=True)
def tenant_task(self, tenant_id, *args, **kwargs):
    with schema_context(Tenant.objects.get(id=tenant_id).schema_name):
        # Execute task in tenant context
        pass
```

---

## Summary of Decisions

| Research ID | Decision | Confidence |
|-------------|----------|------------|
| R-01 | PostgreSQL Schema-Based Multi-Tenancy | High ✅ |
| R-02 | Three-Method MFA (TOTP + SMS + Email) | High ✅ |
| R-03 | Dynamic Schema Creation with Shared Migrations | High ✅ |
| R-04 | Saudi Labor Law Compliant HR Schema | High ✅ |
| R-05 | Hierarchical Task Model with Dependencies | High ✅ |
| R-06 | Redis-Backed Celery with Tenant Awareness | High ✅ |

---

**Phase 0 Complete. Ready for Phase 1: Design & Contracts.**
