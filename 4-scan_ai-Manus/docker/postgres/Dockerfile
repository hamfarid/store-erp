# حاوية PostgreSQL المخصصة لنظام Gaara Scan AI

FROM postgres:15-alpine

# تثبيت الإضافات المطلوبة
RUN apk add --no-cache \
    postgresql-contrib \
    postgresql-dev \
    build-base \
    python3 \
    python3-dev \
    py3-pip

# تثبيت إضافات PostgreSQL المتقدمة
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && pip3 install --no-cache-dir psycopg2-binary \
    && apk del .build-deps

# نسخ ملفات التهيئة والإعداد
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql
COPY setup_extensions.sql /docker-entrypoint-initdb.d/02-setup_extensions.sql
COPY create_schemas.sql /docker-entrypoint-initdb.d/03-create_schemas.sql
COPY seed_data.sql /docker-entrypoint-initdb.d/04-seed_data.sql

# نسخ ملفات التكوين المخصصة
COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf

# إنشاء مجلدات البيانات والسجلات
RUN mkdir -p /var/lib/postgresql/data/gaara_logs \
    && mkdir -p /var/lib/postgresql/backups \
    && chown -R postgres:postgres /var/lib/postgresql

# إعداد متغيرات البيئة المخصصة
ENV POSTGRES_DB=gaara_scan_ai
ENV POSTGRES_USER=gaara_user
ENV POSTGRES_INITDB_ARGS="--encoding=UTF8 --locale=C --data-checksums"
ENV PGDATA=/var/lib/postgresql/data/pgdata

# إعداد الصلاحيات
USER postgres

# فحص صحة قاعدة البيانات
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# تعريض المنفذ
EXPOSE 5432

# أمر التشغيل مع التكوين المخصص
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

