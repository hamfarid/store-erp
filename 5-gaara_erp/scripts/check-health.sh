#!/bin/bash
# =============================================================================
# Gaara ERP - Health Check Script
# =============================================================================
# Checks health of all services
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Gaara ERP - Health Check"
echo "=========================================="

HEALTHY=true

# Check backend
echo -n "Backend (http://localhost:8000/health/)... "
if curl -f -s http://localhost:8000/health/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Healthy${NC}"
else
    echo -e "${RED}✗ Unhealthy${NC}"
    HEALTHY=false
fi

# Check database
echo -n "Database (PostgreSQL)... "
if docker-compose ps db | grep -q "Up" 2>/dev/null || \
   PGPASSWORD="${POSTGRES_PASSWORD:-gaara_admin}" psql -h localhost -U "${POSTGRES_USER:-gaara_admin}" -d "${POSTGRES_DB:-gaara_erp}" -c '\q' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Healthy${NC}"
else
    echo -e "${RED}✗ Unhealthy${NC}"
    HEALTHY=false
fi

# Check Redis
echo -n "Redis... "
if docker-compose ps redis | grep -q "Up" 2>/dev/null || \
   redis-cli -h localhost ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Healthy${NC}"
else
    echo -e "${RED}✗ Unhealthy${NC}"
    HEALTHY=false
fi

# Check frontend
echo -n "Frontend (http://localhost:5173)... "
if curl -f -s http://localhost:5173 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Healthy${NC}"
else
    echo -e "${YELLOW}⚠ Not accessible (may be normal if not running)${NC}"
fi

# Check Celery
echo -n "Celery Worker... "
if docker-compose ps celery | grep -q "Up" 2>/dev/null; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${YELLOW}⚠ Not running${NC}"
fi

# Summary
echo ""
echo "=========================================="
if [ "$HEALTHY" = true ]; then
    echo -e "${GREEN}All critical services are healthy!${NC}"
    exit 0
else
    echo -e "${RED}Some services are unhealthy!${NC}"
    exit 1
fi
