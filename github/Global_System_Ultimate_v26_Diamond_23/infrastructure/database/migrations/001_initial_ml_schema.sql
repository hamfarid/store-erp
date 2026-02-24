-- Initial ML/AI Governance Schema
-- Version: 1.0.0
-- Date: 2026-02-16

CREATE TABLE IF NOT EXISTS feature_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner VARCHAR(100) NOT NULL,
    tags JSONB
);

CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES feature_groups(id),
    name VARCHAR(255) NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    description TEXT,
    is_categorical BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, name)
);

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL, -- 'classification', 'regression', 'llm'
    framework VARCHAR(50), -- 'pytorch', 'sklearn', 'tensorflow'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_versions (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES models(id),
    version VARCHAR(50) NOT NULL,
    s3_path VARCHAR(512) NOT NULL,
    metrics JSONB, -- {'accuracy': 0.95, 'f1': 0.94}
    parameters JSONB, -- {'lr': 0.001, 'batch_size': 32}
    status VARCHAR(50) DEFAULT 'staging', -- 'staging', 'production', 'archived'
    deployed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(model_id, version)
);

CREATE INDEX idx_features_name ON features(name);
CREATE INDEX idx_model_versions_status ON model_versions(status);
