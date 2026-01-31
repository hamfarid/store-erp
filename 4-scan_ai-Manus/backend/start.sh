#!/bin/bash
set -e

echo "🚀 Starting Gaara Scan AI Backend v4.3.1..."
echo "Environment: ${ENVIRONMENT:-production}"

# Function to wait for service
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=0

    echo "⏳ Waiting for ${service} at ${host}:${port}..."

    while [ $attempt -lt $max_attempts ]; do
        if nc -z ${host} ${port} 2>/dev/null; then
            echo "✅ ${service} is ready!"
            return 0
        fi
        attempt=$((attempt + 1))
        echo "Attempt ${attempt}/${max_attempts}: ${service} is unavailable - sleeping"
        sleep 2
    done

    echo "❌ ${service} failed to become available"
    return 1
}

# Wait for PostgreSQL
if [ -n "${DATABASE_HOST}" ] && [ -n "${DATABASE_PORT}" ]; then
    wait_for_service ${DATABASE_HOST} ${DATABASE_PORT} "PostgreSQL"
fi

# Wait for Redis
if [ -n "${REDIS_HOST}" ] && [ -n "${REDIS_PORT}" ]; then
    wait_for_service ${REDIS_HOST} ${REDIS_PORT} "Redis"
fi

# Run database migrations
if [ -f "alembic.ini" ] && [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    echo "🔄 Running database migrations..."
    # Handle multiple heads by upgrading all heads
    alembic heads | grep -q . && {
        echo "⚠️ Multiple migration heads detected, merging..."
        alembic merge heads -m "merge_heads" 2>/dev/null || true
    }
    alembic upgrade head || {
        echo "⚠️ Migration failed, trying to upgrade all heads..."
        alembic upgrade heads || {
            echo "⚠️ Migration failed, continuing without migrations..."
        }
    }
fi

# Start application with proper signal handling
echo "✅ Starting application on port ${APP_PORT}..."
exec uvicorn src.main:app \
    --host 0.0.0.0 \
    --port ${APP_PORT} \
    --workers ${WORKERS} \
    --log-level ${LOG_LEVEL} \
    --access-log \
    --use-colors
