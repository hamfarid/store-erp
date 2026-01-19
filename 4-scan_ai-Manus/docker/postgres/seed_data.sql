-- Seed Data for Gaara Scan AI System
-- بيانات أولية لنظام جعاره للمسح الذكي

-- Connect to main database
\c gaara_scan_ai;

-- Create plant diseases table if not exists
CREATE TABLE IF NOT EXISTS diseases (
    id SERIAL PRIMARY KEY,
    name_en VARCHAR(255) NOT NULL,
    name_ar VARCHAR(255),
    description TEXT,
    severity VARCHAR(50) DEFAULT 'medium',
    symptoms TEXT,
    treatment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create crops table if not exists
CREATE TABLE IF NOT EXISTS crops (
    id SERIAL PRIMARY KEY,
    name_en VARCHAR(255) NOT NULL,
    name_ar VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create diagnosis results table if not exists
CREATE TABLE IF NOT EXISTS diagnosis_results (
    id SERIAL PRIMARY KEY,
    image_path VARCHAR(500),
    crop_id INTEGER REFERENCES crops(id),
    disease_id INTEGER REFERENCES diseases(id),
    confidence FLOAT,
    user_id INTEGER REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create AI models table if not exists
CREATE TABLE IF NOT EXISTS ai_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model_type VARCHAR(100),
    version VARCHAR(50),
    accuracy FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    model_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default admin user (password: admin123)
INSERT INTO users (username, email, password_hash, is_superuser, is_staff, is_active, first_name, last_name)
VALUES ('admin', 'admin@gaarascan.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.5.Q.Z.q.Z.q.Z.', true, true, true, 'System', 'Admin')
ON CONFLICT (username) DO NOTHING;

-- Default plant diseases
INSERT INTO diseases (name_en, name_ar, description, severity)
VALUES 
    ('Powdery Mildew', 'البياض الدقيقي', 'Fungal disease causing white powdery coating on leaves', 'medium'),
    ('Leaf Rust', 'صدأ الأوراق', 'Fungal disease causing rust-colored spots on leaves', 'high'),
    ('Root Rot', 'تعفن الجذور', 'Disease affecting plant roots due to overwatering or fungi', 'high'),
    ('Bacterial Blight', 'اللفحة البكتيرية', 'Bacterial infection causing leaf spots and wilting', 'high'),
    ('Aphid Infestation', 'الإصابة بالمن', 'Pest infestation by small sap-sucking insects', 'low'),
    ('Leaf Spot', 'تبقع الأوراق', 'Fungal or bacterial disease causing spots on leaves', 'medium'),
    ('Downy Mildew', 'البياض الزغبي', 'Fungal disease causing yellow patches on leaves', 'medium'),
    ('Mosaic Virus', 'فيروس الموزاييك', 'Viral disease causing mottled leaf patterns', 'high'),
    ('Wilt Disease', 'مرض الذبول', 'Disease causing plant wilting due to vascular blockage', 'high'),
    ('Nutrient Deficiency', 'نقص العناصر الغذائية', 'Yellowing or discoloration due to lack of nutrients', 'low'),
    ('Healthy Plant', 'نبات سليم', 'No disease detected - plant is healthy', 'none'),
    ('Unknown', 'غير معروف', 'Disease not identified - requires further analysis', 'unknown')
ON CONFLICT DO NOTHING;

-- Default crop types
INSERT INTO crops (name_en, name_ar, category)
VALUES 
    ('Tomato', 'طماطم', 'vegetables'),
    ('Wheat', 'قمح', 'grains'),
    ('Corn', 'ذرة', 'grains'),
    ('Apple', 'تفاح', 'fruits'),
    ('Grape', 'عنب', 'fruits'),
    ('Potato', 'بطاطس', 'vegetables')
ON CONFLICT DO NOTHING;

-- Default AI models
INSERT INTO ai_models (name, model_type, version, accuracy, is_active)
VALUES 
    ('ResNet50', 'classification', '1.0.0', 0.92, true),
    ('YOLO v8', 'detection', '8.0.0', 0.95, true),
    ('PlantVision', 'segmentation', '1.2.0', 0.88, true)
ON CONFLICT DO NOTHING;

-- Grant permissions on new tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gaara_user;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_diseases_name ON diseases(name_en);
CREATE INDEX IF NOT EXISTS idx_crops_category ON crops(category);
CREATE INDEX IF NOT EXISTS idx_diagnosis_created ON diagnosis_results(created_at);
CREATE INDEX IF NOT EXISTS idx_ai_models_active ON ai_models(is_active);

-- Log initial setup
INSERT INTO activity_log (action, description)
VALUES ('SYSTEM_INIT', 'Database initialized with seed data');
