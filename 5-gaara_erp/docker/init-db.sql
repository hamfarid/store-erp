-- =============================================================================
-- Gaara ERP - Database Initialization Script
-- =============================================================================
-- This script runs when the PostgreSQL container is first created
-- =============================================================================

-- Set timezone
SET timezone = 'Asia/Riyadh';

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- Set default encoding
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- Create custom types if needed
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'currency_code') THEN
        CREATE TYPE currency_code AS ENUM ('SAR', 'USD', 'EUR', 'GBP');
    END IF;
END$$;

-- Grant permissions (will be created by Django, but good to have)
-- Note: Actual tables will be created by Django migrations

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Gaara ERP database initialized successfully';
    RAISE NOTICE 'Timezone: Asia/Riyadh';
    RAISE NOTICE 'Encoding: UTF8';
END$$;
