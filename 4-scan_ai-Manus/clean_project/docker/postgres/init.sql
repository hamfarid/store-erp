-- ملف تهيئة قاعدة البيانات الأولية لنظام Gaara Scan AI
-- الملف: /home/ubuntu/clean_project/docker/postgres/init.sql

-- إنشاء قواعد البيانات المطلوبة
CREATE DATABASE gaara_scan_ai;
CREATE DATABASE grafana;
CREATE DATABASE gaara_memory;
CREATE DATABASE gaara_vector;
CREATE DATABASE gaara_analytics;

-- إنشاء المستخدمين والصلاحيات
CREATE USER gaara_user WITH ENCRYPTED PASSWORD 'gaara_secure_2024';
CREATE USER grafana_user WITH ENCRYPTED PASSWORD 'grafana_secure_2024';
CREATE USER memory_user WITH ENCRYPTED PASSWORD 'memory_secure_2024';
CREATE USER vector_user WITH ENCRYPTED PASSWORD 'vector_secure_2024';
CREATE USER analytics_user WITH ENCRYPTED PASSWORD 'analytics_secure_2024';

-- منح الصلاحيات للمستخدمين
GRANT ALL PRIVILEGES ON DATABASE gaara_scan_ai TO gaara_user;
GRANT ALL PRIVILEGES ON DATABASE grafana TO grafana_user;
GRANT ALL PRIVILEGES ON DATABASE gaara_memory TO memory_user;
GRANT ALL PRIVILEGES ON DATABASE gaara_vector TO vector_user;
GRANT ALL PRIVILEGES ON DATABASE gaara_analytics TO analytics_user;

-- إعداد صلاحيات إضافية
ALTER USER gaara_user CREATEDB;
ALTER USER gaara_user CREATEROLE;

-- إنشاء مخطط للنسخ الاحتياطية
\c gaara_scan_ai;
CREATE SCHEMA IF NOT EXISTS backups;
CREATE SCHEMA IF NOT EXISTS monitoring;
CREATE SCHEMA IF NOT EXISTS logs;

-- منح صلاحيات على المخططات
GRANT ALL ON SCHEMA backups TO gaara_user;
GRANT ALL ON SCHEMA monitoring TO gaara_user;
GRANT ALL ON SCHEMA logs TO gaara_user;

-- إنشاء جدول إعدادات النظام الأولية
CREATE TABLE IF NOT EXISTS system_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(255) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(50) DEFAULT 'string',
    is_required BOOLEAN DEFAULT FALSE,
    is_configured BOOLEAN DEFAULT FALSE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إدراج الإعدادات الأولية المطلوبة
INSERT INTO system_settings (setting_key, setting_value, setting_type, is_required, description) VALUES
('system_installed', 'false', 'boolean', TRUE, 'تحديد ما إذا كان النظام مثبت ومكون'),
('setup_completed', 'false', 'boolean', TRUE, 'تحديد ما إذا كان الإعداد الأولي مكتمل'),
('company_name', '', 'string', TRUE, 'اسم الشركة أو المؤسسة'),
('company_logo', '', 'string', FALSE, 'شعار الشركة'),
('company_address', '', 'text', FALSE, 'عنوان الشركة'),
('company_phone', '', 'string', FALSE, 'هاتف الشركة'),
('company_email', '', 'email', FALSE, 'بريد الشركة الإلكتروني'),
('tax_number', '', 'string', FALSE, 'الرقم الضريبي'),
('default_currency', 'USD', 'string', TRUE, 'العملة الافتراضية'),
('default_language', 'ar', 'string', TRUE, 'اللغة الافتراضية'),
('timezone', 'UTC', 'string', TRUE, 'المنطقة الزمنية'),
('admin_email', '', 'email', TRUE, 'بريد المدير الإلكتروني'),
('admin_password', '', 'password', TRUE, 'كلمة مرور المدير'),
('database_version', '1.0.0', 'string', FALSE, 'إصدار قاعدة البيانات'),
('last_backup', '', 'datetime', FALSE, 'تاريخ آخر نسخة احتياطية'),
('backup_enabled', 'true', 'boolean', FALSE, 'تفعيل النسخ الاحتياطي التلقائي'),
('ai_enabled', 'true', 'boolean', FALSE, 'تفعيل خدمات الذكاء الاصطناعي'),
('notifications_enabled', 'true', 'boolean', FALSE, 'تفعيل الإشعارات'),
('websocket_enabled', 'true', 'boolean', FALSE, 'تفعيل الاتصال الفوري');

-- إنشاء جدول المستخدمين الأولي
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    profile_picture VARCHAR(255),
    phone VARCHAR(20),
    department VARCHAR(100),
    position VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إنشاء فهارس للأداء
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_system_settings_key ON system_settings(setting_key);

-- إنشاء دالة لتحديث updated_at تلقائياً
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- إنشاء المشغلات للتحديث التلقائي
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_settings_updated_at BEFORE UPDATE ON system_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- إنشاء جدول سجل النشاط
CREATE TABLE IF NOT EXISTS activity_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    description TEXT,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activity_log_user_id ON activity_log(user_id);
CREATE INDEX idx_activity_log_action ON activity_log(action);
CREATE INDEX idx_activity_log_created_at ON activity_log(created_at);

-- إعداد الصلاحيات النهائية
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gaara_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO gaara_user;

