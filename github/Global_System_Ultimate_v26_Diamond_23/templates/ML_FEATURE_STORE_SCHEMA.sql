-- ML Feature Store Schema Template (v2026.2)
-- Compatible with PostgreSQL / TimescaleDB

-- 1. Entities (e.g., Users, Products)
CREATE TABLE entities (
    entity_id UUID PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Feature Groups (Logical grouping of features)
CREATE TABLE feature_groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    owner VARCHAR(100)
);

-- 3. Feature Definitions (Metadata)
CREATE TABLE feature_definitions (
    feature_id SERIAL PRIMARY KEY,
    group_id INT REFERENCES feature_groups(group_id),
    feature_name VARCHAR(100) NOT NULL,
    data_type VARCHAR(50) NOT NULL, -- FLOAT, INT, VARCHAR, JSONB
    version INT DEFAULT 1,
    UNIQUE(group_id, feature_name, version)
);

-- 4. Feature Values (Time-series data)
-- Partitioned by time for efficiency
CREATE TABLE feature_values (
    entity_id UUID REFERENCES entities(entity_id),
    feature_id INT REFERENCES feature_definitions(feature_id),
    event_timestamp TIMESTAMP NOT NULL,
    value_float FLOAT,
    value_int INT,
    value_string TEXT,
    value_json JSONB,
    created_at TIMESTAMP DEFAULT NOW()
) PARTITION BY RANGE (event_timestamp);

-- Example Partition
CREATE TABLE feature_values_2026_q1 PARTITION OF feature_values
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

-- Indexes
CREATE INDEX idx_feature_lookup ON feature_values (entity_id, feature_id, event_timestamp DESC);
