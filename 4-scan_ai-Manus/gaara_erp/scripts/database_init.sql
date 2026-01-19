-- إنشاء قاعدة بيانات Gaara ERP الأساسية

-- المخطط الرئيسي للنظام
CREATE SCHEMA IF NOT EXISTS erp;
CREATE SCHEMA IF NOT EXISTS integration;
CREATE SCHEMA IF NOT EXISTS analytics;

-- جداول المستخدمين والصلاحيات
CREATE TABLE erp.users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    profile_image VARCHAR(255),
    phone VARCHAR(20),
    language_code CHAR(2) DEFAULT 'ar',
    timezone VARCHAR(50) DEFAULT 'Asia/Riyadh'
);

CREATE TABLE erp.roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);

CREATE TABLE erp.permissions (
    permission_id SERIAL PRIMARY KEY,
    permission_code VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    module VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE erp.role_permissions (
    role_id INTEGER REFERENCES erp.roles(role_id),
    permission_id INTEGER REFERENCES erp.permissions(permission_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE erp.user_roles (
    user_id INTEGER REFERENCES erp.users(user_id),
    role_id INTEGER REFERENCES erp.roles(role_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    PRIMARY KEY (user_id, role_id)
);

-- جداول الشركات والفروع
CREATE TABLE erp.companies (
    company_id SERIAL PRIMARY KEY,
    company_code VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    legal_name VARCHAR(100),
    tax_number VARCHAR(50),
    registration_number VARCHAR(50),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    logo_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    country_code CHAR(2),
    currency_code CHAR(3) DEFAULT 'SAR',
    fiscal_year_start DATE,
    notes TEXT
);

CREATE TABLE erp.branches (
    branch_id SERIAL PRIMARY KEY,
    branch_code VARCHAR(20) NOT NULL,
    branch_name VARCHAR(100) NOT NULL,
    company_id INTEGER REFERENCES erp.companies(company_id),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    manager_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    location_coordinates VARCHAR(50),
    UNIQUE (company_id, branch_code)
);

CREATE TABLE erp.user_branches (
    user_id INTEGER REFERENCES erp.users(user_id),
    branch_id INTEGER REFERENCES erp.branches(branch_id),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    PRIMARY KEY (user_id, branch_id)
);

-- جداول الإعدادات والتكوين
CREATE TABLE erp.settings (
    setting_id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(20) NOT NULL,
    is_system BOOLEAN DEFAULT FALSE,
    is_editable BOOLEAN DEFAULT TRUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);

CREATE TABLE erp.currencies (
    currency_code CHAR(3) PRIMARY KEY,
    currency_name VARCHAR(50) NOT NULL,
    symbol VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    decimal_places SMALLINT DEFAULT 2,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);

CREATE TABLE erp.exchange_rates (
    rate_id SERIAL PRIMARY KEY,
    from_currency CHAR(3) REFERENCES erp.currencies(currency_code),
    to_currency CHAR(3) REFERENCES erp.currencies(currency_code),
    rate DECIMAL(18,6) NOT NULL,
    effective_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    UNIQUE (from_currency, to_currency, effective_date)
);

CREATE TABLE erp.languages (
    language_code CHAR(2) PRIMARY KEY,
    language_name VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_rtl BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);

CREATE TABLE erp.translations (
    translation_id SERIAL PRIMARY KEY,
    language_code CHAR(2) REFERENCES erp.languages(language_code),
    translation_key VARCHAR(255) NOT NULL,
    translation_value TEXT NOT NULL,
    module VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    UNIQUE (language_code, translation_key)
);

-- جداول التكامل
CREATE TABLE integration.entity_mapping (
    mapping_id SERIAL PRIMARY KEY,
    agri_entity_type VARCHAR(50) NOT NULL,
    agri_entity_id VARCHAR(50) NOT NULL,
    erp_entity_type VARCHAR(50) NOT NULL,
    erp_entity_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    UNIQUE (agri_entity_type, agri_entity_id, erp_entity_type)
);

CREATE TABLE integration.sync_log (
    log_id SERIAL PRIMARY KEY,
    sync_type VARCHAR(50) NOT NULL,
    source_system VARCHAR(20) NOT NULL,
    target_system VARCHAR(20) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    message TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    user_id INTEGER,
    details JSONB
);

CREATE TABLE integration.sync_queue (
    queue_id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    source_system VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    priority SMALLINT DEFAULT 5,
    retry_count SMALLINT DEFAULT 0,
    max_retries SMALLINT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scheduled_at TIMESTAMP,
    processed_at TIMESTAMP,
    error_message TEXT
);

CREATE TABLE integration.transformation_rules (
    rule_id SERIAL PRIMARY KEY,
    source_entity VARCHAR(50) NOT NULL,
    target_entity VARCHAR(50) NOT NULL,
    source_field VARCHAR(50) NOT NULL,
    target_field VARCHAR(50) NOT NULL,
    transformation_type VARCHAR(50) NOT NULL,
    transformation_expression TEXT,
    priority INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);

-- جداول السجلات والتدقيق
CREATE TABLE erp.audit_log (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50),
    changes JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

-- إنشاء المستخدم الافتراضي والأدوار الأساسية
INSERT INTO erp.users (username, email, password_hash, first_name, last_name, is_admin)
VALUES ('admin', 'admin@gaaraerp.com', '$2a$12$1234567890123456789012uqZrZ9vl7JmUjzJl0xqXMQwKQrOcyJe', 'مدير', 'النظام', TRUE);

INSERT INTO erp.roles (role_name, description)
VALUES 
('مدير النظام', 'صلاحيات كاملة على النظام'),
('مدير', 'صلاحيات إدارية على النظام'),
('محاسب', 'صلاحيات على وحدة الحسابات'),
('مدير مخزون', 'صلاحيات على وحدة المخزون'),
('مدير مشاتل', 'صلاحيات على وحدة المشاتل والمزارع'),
('مدير موارد بشرية', 'صلاحيات على وحدة الموارد البشرية'),
('مستخدم', 'صلاحيات محدودة على النظام');

-- إضافة اللغات الأساسية
INSERT INTO erp.languages (language_code, language_name, is_rtl)
VALUES 
('ar', 'العربية', TRUE),
('en', 'English', FALSE),
('tr', 'Türkçe', FALSE),
('th', 'ไทย', FALSE);

-- إضافة العملات الأساسية
INSERT INTO erp.currencies (currency_code, currency_name, symbol, decimal_places)
VALUES 
('SAR', 'ريال سعودي', 'ر.س', 2),
('USD', 'دولار أمريكي', '$', 2),
('EUR', 'يورو', '€', 2),
('TRY', 'ليرة تركية', '₺', 2),
('AED', 'درهم إماراتي', 'د.إ', 2),
('OMR', 'ريال عماني', 'ر.ع', 3),
('THB', 'بات تايلندي', '฿', 2);
