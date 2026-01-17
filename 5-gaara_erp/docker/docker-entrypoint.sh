#!/bin/bash
# =============================================================================
# Gaara ERP - Docker Entrypoint Script
# =============================================================================

set -euo pipefail

echo "Starting Gaara ERP backend..."

# Wait for database to be ready
echo "Waiting for database..."
until PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${DB_HOST:-db}" -U "${POSTGRES_USER:-gaara_admin}" -d "${POSTGRES_DB:-gaara_erp}" -c '\q' 2>/dev/null; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is ready!"

# Run database initialization if script exists
if [ -f "/app/docker/database-init.sh" ]; then
    echo "Running database initialization..."
    bash /app/docker/database-init.sh
fi

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
