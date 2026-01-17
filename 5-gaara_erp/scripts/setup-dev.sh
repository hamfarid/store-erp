#!/bin/bash
# =============================================================================
# Gaara ERP - Development Environment Setup
# =============================================================================
# Complete development environment initialization
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================="
echo "Gaara ERP - Development Setup"
echo "==========================================${NC}"

# Check prerequisites
echo ""
echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose installed${NC}"

# Check .env file
echo ""
echo "Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file not found${NC}"
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo -e "${YELLOW}⚠ Please edit .env file with your configuration${NC}"
    else
        echo -e "${RED}✗ .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Start services
echo ""
echo "Starting Docker services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for services
echo ""
echo "Waiting for services to be ready..."
sleep 10

# Run database initialization
echo ""
echo "Initializing database..."
if [ -f "docker/database-init.sh" ]; then
    docker-compose -f docker-compose.dev.yml exec -T backend bash /app/docker/database-init.sh || true
else
    docker-compose -f docker-compose.dev.yml exec -T backend python manage.py migrate --noinput
fi

# Seed database
echo ""
echo "Seeding database with initial data..."
if [ -f "scripts/seed-database.sh" ]; then
    docker-compose -f docker-compose.dev.yml exec -T backend bash /app/scripts/seed-database.sh || true
fi

# Create superuser
echo ""
echo "Creating superuser..."
read -p "Do you want to create a superuser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
fi

# Health check
echo ""
echo "Performing health check..."
if [ -f "scripts/check-health.sh" ]; then
    ./scripts/check-health.sh || echo -e "${YELLOW}⚠ Some services may not be ready yet${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}=========================================="
echo "Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "Access URLs:"
echo -e "  Frontend: ${GREEN}http://localhost:5173${NC}"
echo -e "  Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "  Admin:    ${GREEN}http://localhost:8000/admin${NC}"
echo -e "  API Docs: ${GREEN}http://localhost:8000/api/docs/${NC}"
echo ""
echo "Useful commands:"
echo "  View logs:    docker-compose -f docker-compose.dev.yml logs -f"
echo "  Stop services: docker-compose -f docker-compose.dev.yml down"
echo "  Restart:      docker-compose -f docker-compose.dev.yml restart"
echo ""
