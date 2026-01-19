# Database Migrations (v24.0)

## 1. The Supabase Standard
We exclusively use **Supabase Migrations** for all database changes.
**Why?**
- **Version Control:** Every change is a SQL file in `supabase/migrations`.
- **Safety:** No direct schema changes in production.
- **Consistency:** Local dev matches production exactly.

---

## 2. Workflow: The "Schema-First" Approach

### Step 1: Make Changes Locally
1.  Start local Supabase: `npx supabase start`
2.  Edit schema via Studio (`localhost:54323`) OR write SQL manually.
3.  **Generate Migration:**
    ```bash
    npx supabase db diff -f name_of_change
    ```
    *This creates `supabase/migrations/<timestamp>_name_of_change.sql`*

### Step 2: Review & Test
1.  Read the generated SQL file. Does it look right?
2.  Apply it locally (if not already applied): `npx supabase db reset` (Caution: wipes local data).

### Step 3: Push to Production
**CI/CD Pipeline (Recommended):**
*   GitHub Actions automatically runs `supabase db push` on merge to main.

**Manual Push (If permitted):**
```bash
npx supabase db push
```

---

## 3. Rules of Engagement
1.  **NEVER** edit the production database directly via the dashboard.
2.  **ALWAYS** use descriptive names for migrations (e.g., `add_users_table`, `update_profiles_rls`).
3.  **RLS is Mandatory:** Every table must have Row Level Security enabled.
    ```sql
    ALTER TABLE "public"."users" ENABLE ROW LEVEL SECURITY;
    ```

---

## 4. Troubleshooting
*   **Migration Conflict:** If local schema drifts from migration history, use `supabase db reset` to re-sync.
*   **Failed Push:** Check the logs. Did you try to alter a column that has data? You might need a manual script to migrate data first.
