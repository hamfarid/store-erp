# 💾 Database Design Rules (Global System Ultimate)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel & CodeRabbit

## 1. The Philosophy
Data integrity is non-negotiable. Performance is a feature.

## 2. Core Principles
*   **Normalization:** 3NF is the default. Denormalize ONLY with documented justification.
*   **ACID:** Transactions are MANDATORY for multi-step operations.
*   **Indexing:** Foreign keys MUST be indexed.

## 3. Naming Conventions
*   **Tables:** Plural, snake_case (e.g., `users`, `order_items`).
*   **Columns:** snake_case (e.g., `created_at`, `is_active`).
*   **Primary Keys:** `id` (UUID or BigInt).
*   **Foreign Keys:** `singular_table_id` (e.g., `user_id`).

## 4. Performance (Sentinel Enforced)
*   **N+1 Problem:** FORBIDDEN. Use eager loading (JOINs).
*   **Select *:** FORBIDDEN. Select only required columns.
*   **Soft Deletes:** Use `deleted_at` timestamp instead of physical deletion.

## 5. Migrations
*   **Version Control:** All schema changes MUST be in migration files.
*   **Reversible:** All migrations MUST have a `down` method.
*   **Data Safety:** Migrations MUST NOT lose data without explicit warning.

## 6. Security
*   **Encryption:** Sensitive data (PII, Secrets) MUST be encrypted at rest.
*   **Least Privilege:** Application user MUST NOT have DDL privileges (DROP, ALTER) in production.
