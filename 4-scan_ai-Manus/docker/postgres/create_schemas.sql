-- Create additional schemas for Gaara Scan AI System
-- إنشاء المخططات الإضافية لنظام جعاره للمسح الذكي

\c gaara_scan_ai;

-- AI and Machine Learning schema
CREATE SCHEMA IF NOT EXISTS ai;
COMMENT ON SCHEMA ai IS 'AI models and predictions schema';

-- Diagnosis and analysis schema
CREATE SCHEMA IF NOT EXISTS diagnosis;
COMMENT ON SCHEMA diagnosis IS 'Plant disease diagnosis schema';

-- Monitoring schema
CREATE SCHEMA IF NOT EXISTS monitoring;
COMMENT ON SCHEMA monitoring IS 'System monitoring schema';

-- Grant permissions
GRANT ALL ON SCHEMA ai TO gaara_user;
GRANT ALL ON SCHEMA diagnosis TO gaara_user;
GRANT ALL ON SCHEMA monitoring TO gaara_user;

-- Create monitoring tables
CREATE TABLE IF NOT EXISTS monitoring.service_health (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'unknown',
    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_time_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monitoring.system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT,
    unit VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions on monitoring tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA monitoring TO gaara_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA monitoring TO gaara_user;
