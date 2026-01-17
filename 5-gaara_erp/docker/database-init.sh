#!/bin/bash
# =============================================================================
# Gaara ERP - Database Initialization Script
# =============================================================================
# Runs migrations and sets up initial data
# =============================================================================

set -euo pipefail

echo "=========================================="
echo "Gaara ERP - Database Initialization"
echo "=========================================="

# Wait for database to be ready
echo "Waiting for database..."
until PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${DB_HOST:-db}" -U "${POSTGRES_USER:-gaara_admin}" -d "${POSTGRES_DB:-gaara_erp}" -c '\q' 2>/dev/null; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "✓ Database is ready!"

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate --noinput
echo "✓ Migrations completed!"

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput || true
echo "✓ Static files collected!"

# Create superuser if requested
if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
    echo ""
    echo "Creating superuser..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
email = "${SUPERUSER_EMAIL:-admin@gaara-erp.com}"
password = "${SUPERUSER_PASSWORD:-admin123}"

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        first_name="Admin",
        last_name="User"
    )
    print(f"✓ Superuser created: {email}")
else:
    print(f"✓ Superuser already exists: {email}")
EOF
fi

# Load initial data if fixtures exist
if [ -d "fixtures" ] && [ "$(ls -A fixtures/*.json 2>/dev/null)" ]; then
    echo ""
    echo "Loading initial data fixtures..."
    for fixture in fixtures/*.json; do
        echo "Loading $fixture..."
        python manage.py loaddata "$fixture" || true
    done
    echo "✓ Fixtures loaded!"
fi

# Create default company/organization if needed
echo ""
echo "Setting up default organization..."
python manage.py shell << EOF || true
from core_modules.organization.models import Company
if not Company.objects.exists():
    Company.objects.create(
        name="Gaara ERP",
        code="GAARA",
        is_active=True
    )
    print("✓ Default company created")
else:
    print("✓ Company already exists")
EOF

echo ""
echo "=========================================="
echo "Database initialization completed!"
echo "=========================================="
