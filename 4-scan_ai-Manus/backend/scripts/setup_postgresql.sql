-- ============================================================================
-- GAARA AI - PostgreSQL Database Setup Script
-- ============================================================================
-- FILE: backend/scripts/setup_postgresql.sql
-- PURPOSE: Create database and user for Gaara AI
-- OWNER: DevOps Team
-- LAST-AUDITED: 2025-11-18
--
-- USAGE:
--   psql -U postgres -f setup_postgresql.sql
-- ============================================================================

-- Create database
CREATE DATABASE gaara_scan_ai
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    TEMPLATE = template0;

COMMENT ON DATABASE gaara_scan_ai IS 'Gaara AI - Smart Agriculture System Database';

-- Create user
CREATE USER gaara_user WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD 'GaaraSecure2024!@#';

COMMENT ON ROLE gaara_user IS 'Gaara AI application user';

-- Grant database privileges
GRANT ALL PRIVILEGES ON DATABASE gaara_scan_ai TO gaara_user;
GRANT CONNECT ON DATABASE gaara_scan_ai TO gaara_user;

-- Connect to the database
\c gaara_scan_ai

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO gaara_user;
GRANT CREATE ON SCHEMA public TO gaara_user;

-- Grant privileges on all existing tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO gaara_user;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gaara_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gaara_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO gaara_user;

-- Create extensions (if needed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For full-text search

-- Display success message
\echo '============================================================'
\echo 'PostgreSQL Database Setup Complete!'
\echo '============================================================'
\echo ''
\echo 'Database: gaara_scan_ai'
\echo 'User:     gaara_user'
\echo 'Password: GaaraSecure2024!@#'
\echo ''
\echo 'Next steps:'
\echo '1. Update backend/.env with database credentials'
\echo '2. Run: alembic upgrade head'
\echo '3. Run: python scripts/create_default_admin.py'
\echo ''
\echo '⚠️  IMPORTANT: Change the password in production!'
\echo '============================================================'

