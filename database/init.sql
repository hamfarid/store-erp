-- =============================================================================
-- Store ERP System - Database Initialization Script
-- Executed when the PostgreSQL container starts for the first time
-- =============================================================================

-- Set client encoding
SET client_encoding = 'UTF8';

-- Create required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Grant privileges to application user
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;

-- Ensure public schema exists and grant access
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL ON SCHEMA public TO inventory_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO inventory_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO inventory_user;

-- Set timezone
SET timezone = 'Africa/Cairo';

-- Tables are created by Flask SQLAlchemy via docker-entrypoint.sh
-- This init.sql ensures the database is properly configured with:
-- 1. UTF8 encoding
-- 2. UUID generation support (uuid-ossp)
-- 3. Full-text search support (pg_trgm)
-- 4. GIN index support (btree_gin)
-- 5. Proper user privileges

SELECT 'Database initialized successfully' AS status;
