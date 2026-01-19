-- إعداد الإضافات المطلوبة لقاعدة البيانات
-- الملف: /home/ubuntu/clean_project/docker/postgres/setup_extensions.sql

\c gaara_scan_ai;

-- تفعيل الإضافات المطلوبة
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "hstore";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "unaccent";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- إضافة دعم البحث النصي العربي
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- إنشاء تكوين البحث النصي العربي
CREATE TEXT SEARCH CONFIGURATION arabic_config (COPY = simple);

-- إعداد قاموس البحث العربي
CREATE TEXT SEARCH DICTIONARY arabic_stem (
    TEMPLATE = simple,
    STOPWORDS = arabic
);

ALTER TEXT SEARCH CONFIGURATION arabic_config
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
    WITH arabic_stem;

-- إنشاء دوال مساعدة للبحث العربي
CREATE OR REPLACE FUNCTION normalize_arabic_text(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    -- تطبيع النص العربي
    RETURN regexp_replace(
        regexp_replace(
            regexp_replace(
                regexp_replace(input_text, '[أإآ]', 'ا', 'g'),
                '[ىي]', 'ي', 'g'
            ),
            '[ةه]', 'ه', 'g'
        ),
        '[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s]', '', 'g'
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- دالة البحث المتقدم
CREATE OR REPLACE FUNCTION advanced_search(
    search_term TEXT,
    table_name TEXT,
    columns TEXT[]
) RETURNS TABLE(id INTEGER, relevance REAL) AS $$
DECLARE
    query TEXT;
    col TEXT;
BEGIN
    query := 'SELECT id, ';
    
    -- بناء استعلام البحث
    FOR i IN 1..array_length(columns, 1) LOOP
        col := columns[i];
        IF i > 1 THEN
            query := query || ' + ';
        END IF;
        query := query || 'ts_rank(to_tsvector(''arabic_config'', ' || col || '), plainto_tsquery(''arabic_config'', $1))';
    END LOOP;
    
    query := query || ' as relevance FROM ' || table_name || ' WHERE ';
    
    FOR i IN 1..array_length(columns, 1) LOOP
        col := columns[i];
        IF i > 1 THEN
            query := query || ' OR ';
        END IF;
        query := query || 'to_tsvector(''arabic_config'', ' || col || ') @@ plainto_tsquery(''arabic_config'', $1)';
    END LOOP;
    
    query := query || ' ORDER BY relevance DESC';
    
    RETURN QUERY EXECUTE query USING search_term;
END;
$$ LANGUAGE plpgsql;

-- إنشاء دالة للنسخ الاحتياطي التلقائي
CREATE OR REPLACE FUNCTION create_backup_info(backup_name TEXT, backup_size BIGINT)
RETURNS VOID AS $$
BEGIN
    INSERT INTO backups.backup_history (backup_name, backup_size, created_at)
    VALUES (backup_name, backup_size, CURRENT_TIMESTAMP);
END;
$$ LANGUAGE plpgsql;

-- إنشاء جدول تاريخ النسخ الاحتياطية
CREATE TABLE IF NOT EXISTS backups.backup_history (
    id SERIAL PRIMARY KEY,
    backup_name VARCHAR(255) NOT NULL,
    backup_size BIGINT,
    backup_type VARCHAR(50) DEFAULT 'full',
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- إنشاء فهارس للأداء
CREATE INDEX IF NOT EXISTS idx_backup_history_created_at ON backups.backup_history(created_at);
CREATE INDEX IF NOT EXISTS idx_backup_history_status ON backups.backup_history(status);

