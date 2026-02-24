# 🗄️ Database Migration Example (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel (Migration Check)

## 1. The Philosophy
Data is sacred. Migrations MUST be reversible and transactional.

## 2. File Structure
```
migrations/
├── 001_create_users_table.sql
├── 002_add_email_verification.sql
└── 003_create_posts_table.sql
```

## 3. Example Migration (PostgreSQL)
You MUST include both `UP` and `DOWN` sections.

```sql
-- 001_create_users_table.sql

-- UP
BEGIN;
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
COMMIT;

-- DOWN
BEGIN;
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
COMMIT;
```

## 4. The "Transaction" Law
All migrations MUST be wrapped in `BEGIN; ... COMMIT;`. If a migration fails halfway, it must roll back completely.
