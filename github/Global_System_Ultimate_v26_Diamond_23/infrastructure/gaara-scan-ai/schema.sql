-- Image Catalog
CREATE TABLE image_catalog (
    id SERIAL PRIMARY KEY,
    image_url TEXT NOT NULL,
    source TEXT NOT NULL,
    label TEXT,
    quality_score FLOAT,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Training Metadata
CREATE TABLE training_metadata (
    id SERIAL PRIMARY KEY,
    model_version TEXT NOT NULL,
    accuracy FLOAT,
    loss FLOAT,
    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dataset_size INTEGER
);

-- Crawler Tracking
CREATE TABLE crawler_tracking (
    id SERIAL PRIMARY KEY,
    search_term TEXT NOT NULL,
    images_found INTEGER,
    last_run TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quality Gates
CREATE TABLE quality_gates (
    id SERIAL PRIMARY KEY,
    metric_name TEXT NOT NULL,
    threshold FLOAT NOT NULL,
    status TEXT DEFAULT 'active'
);
