#!/bin/bash
# =============================================================================
# Gaara ERP - Docker Entrypoint Script
# =============================================================================

set -euo pipefail

echo "Starting Gaara ERP backend..."

# Wait for database to be ready using Python (works as non-root appuser)
echo "Waiting for database..."
python -c "
import time, sys
while True:
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='${DB_HOST:-gaara_db}',
            port='${DB_PORT:-5432}',
            dbname='${DB_NAME:-gaara_erp}',
            user='${DB_USER:-gaara_admin}',
            password='${DB_PASSWORD:-${POSTGRES_PASSWORD:-}}',
            connect_timeout=5
        )
        conn.close()
        break
    except Exception as e:
        print(f'Database is unavailable ({e}) - sleeping')
        time.sleep(2)
" 2>/dev/null || {
    # Fallback: try with psql if available
    until PGPASSWORD="${DB_PASSWORD:-${POSTGRES_PASSWORD:-}}" psql -h "${DB_HOST:-gaara_db}" -U "${DB_USER:-gaara_admin}" -d "${DB_NAME:-gaara_erp}" -c '\q' 2>/dev/null; do
        echo "Database is unavailable - sleeping"
        sleep 2
    done
}
echo "Database is ready!"

# Run migrations if requested
if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput
    echo "Migrations completed!"
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true
echo "Static files collected!"

# Create superuser if requested (development only)
if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
    echo "Creating superuser..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="${SUPERUSER_EMAIL:-admin@gaara-erp.com}").exists():
    User.objects.create_superuser(
        email="${SUPERUSER_EMAIL:-admin@gaara-erp.com}",
        password="${SUPERUSER_PASSWORD:-admin123}",
        first_name="Admin",
        last_name="User"
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists!")
EOF
fi

# Execute the main command
exec "$@"
