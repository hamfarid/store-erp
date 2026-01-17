#!/bin/bash
# =============================================================================
# Gaara ERP - Deployment Script
# =============================================================================
# Production deployment automation
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Gaara ERP - Production Deployment"
echo "=========================================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Load environment variables
set -a
source .env
set +a

# Backup database before deployment
echo ""
echo "Creating database backup..."
if [ -f "docker/database-backup.sh" ]; then
    ./docker/database-backup.sh || echo -e "${YELLOW}Warning: Backup failed, continuing...${NC}"
else
    echo -e "${YELLOW}Warning: Backup script not found, skipping backup${NC}"
fi

# Pull latest code
echo ""
echo "Pulling latest code..."
git pull origin main || git pull origin master

# Build Docker images
echo ""
echo "Building Docker images..."
docker-compose build --no-cache

# Stop existing containers
echo ""
echo "Stopping existing containers..."
docker-compose down

# Start new containers
echo ""
echo "Starting containers..."
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Run migrations
echo ""
echo "Running database migrations..."
docker-compose exec -T backend python manage.py migrate --noinput

# Collect static files
echo ""
echo "Collecting static files..."
docker-compose exec -T backend python manage.py collectstatic --noinput

# Restart services
echo ""
echo "Restarting services..."
docker-compose restart

# Health check
echo ""
echo "Performing health check..."
sleep 5
if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
    exit 1
fi

# Show running containers
echo ""
echo "Running containers:"
docker-compose ps

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment completed successfully!"
echo "==========================================${NC}"
