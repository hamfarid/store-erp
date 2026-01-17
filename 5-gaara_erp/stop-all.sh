#!/bin/bash
# =============================================================================
# Store ERP - Stop All Services Script (Linux/macOS)
# =============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Store ERP - Stopping All Services${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Stop all compose files
docker-compose -f docker-compose.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.monitoring.yml down 2>/dev/null || true

echo -e "${GREEN}✓ All services stopped${NC}\n"

# Optional: Remove volumes
read -p "Remove all volumes? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose -f docker-compose.prod.yml down -v
    echo -e "${GREEN}✓ Volumes removed${NC}\n"
fi
