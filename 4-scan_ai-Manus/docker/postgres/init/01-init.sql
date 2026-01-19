-- ==========================================
-- Database Initialization Script
-- Gaara Scan AI v4.3
-- ==========================================

-- Create database if not exists (handled by POSTGRES_DB env var)
-- This script runs after database creation

-- ==========================================
-- Extensions
-- ==========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ==========================================
-- Create schemas
-- ==========================================
CREATE SCHEMA IF NOT EXISTS gaara;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS ai;

-- ==========================================
-- Set default privileges
-- ==========================================
ALTER DEFAULT PRIVILEGES IN SCHEMA gaara GRANT ALL ON TABLES TO gaara_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT ALL ON TABLES TO gaara_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ai GRANT ALL ON TABLES TO gaara_user;

-- ==========================================
-- Initial data (if needed)
-- ==========================================
-- This will be populated by Alembic migrations

-- ==========================================
-- Log completion
-- ==========================================
DO $$
BEGIN
    RAISE NOTICE '✅ Database initialization completed successfully';
END $$;

