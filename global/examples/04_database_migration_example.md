# Database Migration Example

## Migration File Structure

\`\`\`
migrations/
├── 001_create_users_table.sql
├── 002_add_email_verification.sql
└── 003_create_posts_table.sql
\`\`\`

## Example Migration (PostgreSQL)

\`\`\`sql
-- 001_create_users_table.sql

-- UP
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- DOWN
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
\`\`\`

## Running Migrations

\`\`\`bash
# Apply all pending migrations
npm run migrate:up

# Rollback last migration
npm run migrate:down

# Check migration status
npm run migrate:status
\`\`\`
