# Supabase Integration Guidelines

## Overview
Supabase is our chosen Backend-as-a-Service (BaaS) provider, offering a suite of tools including Database, Auth, Realtime, and Storage.

## Core Components
1.  **PostgreSQL:** The core database.
2.  **Auth:** User authentication and management.
3.  **Realtime:** Listen to database changes.
4.  **Storage:** File storage (S3 compatible).
5.  **Edge Functions:** Server-side logic running on the edge.

## Best Practices
1.  **Row Level Security (RLS):**
    -   **MANDATORY:** All tables must have RLS enabled.
    -   **Policies:** Define granular policies for `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
    -   **Helper Functions:** Use `auth.uid()` to reference the current user.
2.  **Database Functions:**
    -   Use PL/pgSQL for complex transactional logic that needs to run atomically.
    -   Expose functions via RPC if needed by the client.
3.  **Types:**
    -   Generate TypeScript types from your database schema using the Supabase CLI: `supabase gen types typescript --project-id <id> > types/supabase.ts`.
4.  **Migrations:**
    -   Use `supabase migration new <name>` to create migrations.
    -   Review SQL files before applying.

## Workflow
-   **Local Dev:** `supabase start`
-   **Apply Migrations:** `supabase db reset` (local) or via CI/CD (remote).
-   **Edge Functions:** `supabase functions new <name>`
