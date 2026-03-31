#!/bin/bash
# ============================================================
# Store ERP v2.0.0 - Docker Deployment Script (Linux/Mac)
# ============================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENVIRONMENT="${1:-production}"

echo "============================================"
echo "  Store ERP v2.0.0 - Docker Deployment"
echo "============================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running"
    exit 1
fi

cd "$PROJECT_ROOT"

# Handle commands
case "$1" in
    down)
        echo "Stopping containers..."
        docker-compose -f docker-compose.yml down
        echo "Containers stopped!"
        exit 0
        ;;
    logs)
        echo "Showing logs..."
        docker-compose -f docker-compose.yml logs -f --tail=100
        exit 0
        ;;
    status)
        echo "Container Status:"
        docker-compose -f docker-compose.yml ps
        echo ""
        echo "Resource Usage:"
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
        exit 0
        ;;
    build)
        echo "Building Docker images..."
        docker-compose -f docker-compose.yml build --no-cache
        ;;
esac

echo "Environment: $ENVIRONMENT"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating from example..."
    if [ -f "backend/env.example.txt" ]; then
        cp backend/env.example.txt .env
        echo "Created .env file. Please update with your configuration."
    fi
fi

# Start containers
echo "Starting containers..."
docker-compose -f docker-compose.yml up -d

# Wait for services
echo ""
echo "Waiting for services to be ready..."
max_retries=30
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if docker-compose -f docker-compose.yml exec -T backend curl -s http://localhost:6001/api/health > /dev/null 2>&1; then
        break
    fi
    sleep 2
    echo -n "."
    ((retry_count++))
done

echo ""

if [ $retry_count -lt $max_retries ]; then
    echo ""
    echo "============================================"
    echo "  Deployment Complete!"
    echo "============================================"
    echo ""
    echo "Services running:"
    echo "  - Frontend:  http://localhost:6501"
    echo "  - Backend:   http://localhost:6001"
    echo "  - API Docs:  http://localhost:6001/api/docs"
    echo ""
    echo "Useful commands:"
    echo "  - View logs:    ./scripts/deploy-docker.sh logs"
    echo "  - Stop all:     ./scripts/deploy-docker.sh down"
    echo "  - Check status: ./scripts/deploy-docker.sh status"
else
    echo "Warning: Services may not be fully ready. Check logs with:"
    echo "  docker-compose logs -f"
fi

echo ""
docker-compose -f docker-compose.yml ps
