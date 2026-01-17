#!/bin/bash
# =============================================================================
# Gaara ERP - Cleanup Script
# =============================================================================
# Cleans up Docker containers, volumes, and build artifacts
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Gaara ERP - Cleanup"
echo "=========================================="

# Confirmation
read -p "This will remove containers, volumes, and build cache. Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Stop and remove containers
echo ""
echo "Stopping and removing containers..."
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
docker-compose down 2>/dev/null || true

# Remove volumes (optional)
read -p "Remove volumes? This will delete all data! (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing volumes..."
    docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true
    docker-compose down -v 2>/dev/null || true
    echo -e "${GREEN}✓ Volumes removed${NC}"
fi

# Remove build cache
read -p "Remove Docker build cache? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing build cache..."
    docker builder prune -f
    echo -e "${GREEN}✓ Build cache removed${NC}"
fi

# Remove unused images
read -p "Remove unused Docker images? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing unused images..."
    docker image prune -f
    echo -e "${GREEN}✓ Unused images removed${NC}"
fi

# Clean Python cache
echo ""
echo "Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
echo -e "${GREEN}✓ Python cache cleaned${NC}"

# Clean Node cache
if [ -d "gaara-erp-frontend" ]; then
    echo ""
    echo "Cleaning Node cache..."
    rm -rf gaara-erp-frontend/node_modules 2>/dev/null || true
    rm -rf gaara-erp-frontend/.vite 2>/dev/null || true
    rm -rf gaara-erp-frontend/dist 2>/dev/null || true
    echo -e "${GREEN}✓ Node cache cleaned${NC}"
fi

# Clean logs
echo ""
echo "Cleaning logs..."
rm -rf gaara_erp/logs/*.log 2>/dev/null || true
echo -e "${GREEN}✓ Logs cleaned${NC}"

echo ""
echo -e "${GREEN}=========================================="
echo "Cleanup completed!"
echo "==========================================${NC}"
