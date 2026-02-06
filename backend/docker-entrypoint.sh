#!/bin/sh
set -e

echo "=== Store Backend - Docker Entrypoint ==="
echo "Starting at $(date)"

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
max_retries=30
count=0
until python -c "
import psycopg2
import os
conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgresql://inventory_user:inventory_password@store_database:5432/inventory_db'))
conn.close()
print('PostgreSQL is ready')
" 2>/dev/null; do
    count=$((count + 1))
    if [ $count -ge $max_retries ]; then
        echo "ERROR: PostgreSQL not available after $max_retries attempts"
        exit 1
    fi
    echo "PostgreSQL not ready yet (attempt $count/$max_retries)..."
    sleep 2
done

echo "PostgreSQL is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis..."
count=0
until python -c "
import redis
import os
r = redis.from_url(os.environ.get('REDIS_URL', 'redis://store_redis:6379/0'))
r.ping()
print('Redis is ready')
" 2>/dev/null; do
    count=$((count + 1))
    if [ $count -ge $max_retries ]; then
        echo "WARNING: Redis not available, continuing without cache..."
        break
    fi
    echo "Redis not ready yet (attempt $count/$max_retries)..."
    sleep 2
done

# Create database tables via Flask app
echo "Initializing database tables..."
python -c "
from app import create_app
app = create_app()
with app.app_context():
    from src.database import db, create_tables, create_default_data
    db.create_all()
    try:
        create_default_data()
        print('Default data created successfully')
    except Exception as e:
        print(f'Default data creation skipped: {e}')
    print('Database tables initialized successfully')
" 2>&1 || echo "WARNING: Database init had issues, app will retry on startup"

# Create required directories
mkdir -p /app/logs /app/uploads /app/instance /app/backups 2>/dev/null || true

echo "=== Starting application ==="
exec "$@"
