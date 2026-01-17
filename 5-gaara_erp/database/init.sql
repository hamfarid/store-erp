-- Database Initialization Script for Inventory Management System
-- This script will be executed when the PostgreSQL container starts

-- Set client encoding
SET client_encoding = 'UTF8';

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;

-- Create schema if needed
CREATE SCHEMA IF NOT EXISTS public;

-- The actual tables will be created by the Flask application using SQLAlchemy
-- This file ensures the database is properly initialized

SELECT 'Database initialized successfully' AS status;
