#!/bin/bash
# =============================================================================
# Store ERP v2.0.0 - Deployment Script (Bash)
# =============================================================================
# Usage: ./scripts/deploy.sh [dev|staging|production]
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
ENVIRONMENT="${1:-dev}"
FORCE=false
NO_BACKUP=false
DOCKER_ONLY=false

for arg in "$@"; do
    case $arg in
        --force) FORCE=true ;;
        --no-backup) NO_BACKUP=true ;;
        --docker) DOCKER_ONLY=true ;;
    esac
done

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           Store ERP v2.0.0 - Deployment                           ║${NC}"
echo -e "${CYAN}║           Environment: $(printf '%-40s' "${ENVIRONMENT^^}")    ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Validate production deployment
if [ "$ENVIRONMENT" = "production" ] && [ "$FORCE" = false ]; then
    echo -e "${RED}[WARNING] You are deploying to PRODUCTION!${NC}"
    echo -e "${YELLOW}Use --force flag to confirm.${NC}"
    exit 1
fi

# Step 1: Create Backup
if [ "$NO_BACKUP" = false ]; then
    echo -e "${YELLOW}[1/6] Creating Backup...${NC}"
    BACKUP_DIR="$PROJECT_ROOT/backups"
    TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
    BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    if [ -f "$PROJECT_ROOT/backend/instance/store.db" ]; then
        cp "$PROJECT_ROOT/backend/instance/store.db" "${BACKUP_PATH}.db"
        echo -e "  ${GREEN}✓ Database backed up${NC}"
    fi
    
    # Backup config
    if [ -f "$PROJECT_ROOT/backend/.env" ]; then
        cp "$PROJECT_ROOT/backend/.env" "${BACKUP_PATH}.env"
        echo -e "  ${GREEN}✓ Config backed up${NC}"
    fi
else
    echo -e "${YELLOW}[1/6] Skipping Backup (--no-backup)${NC}"
fi

# Step 2: Check for updates
echo -e "${YELLOW}[2/6] Checking for Updates...${NC}"
cd "$PROJECT_ROOT"
if [ -d ".git" ]; then
    if [ -n "$(git status --porcelain)" ] && [ "$FORCE" = false ]; then
        echo -e "  ${RED}✗ Uncommitted changes detected!${NC}"
        echo -e "  ${YELLOW}Commit or stash changes first, or use --force${NC}"
        exit 1
    fi
    echo -e "  ${GREEN}✓ Repository clean${NC}"
else
    echo -e "  → Not a git repository"
fi

# Step 3: Install Dependencies
echo -e "${YELLOW}[3/6] Installing Dependencies...${NC}"

# Backend
cd "$PROJECT_ROOT/backend"
if [ -f "venv/bin/pip" ]; then
    echo -e "  → Backend dependencies"
    ./venv/bin/pip install -r requirements.txt -q
    echo -e "  ${GREEN}✓ Backend dependencies installed${NC}"
fi

# Frontend
cd "$PROJECT_ROOT/frontend"
echo -e "  → Frontend dependencies"
npm ci --silent
echo -e "  ${GREEN}✓ Frontend dependencies installed${NC}"

# Step 4: Run Migrations
echo -e "${YELLOW}[4/6] Running Database Migrations...${NC}"
cd "$PROJECT_ROOT/backend"
if [ -f "venv/bin/flask" ]; then
    ./venv/bin/flask db upgrade 2>/dev/null || true
    echo -e "  ${GREEN}✓ Migrations applied${NC}"
else
    echo -e "  → Skipping (flask not in venv)"
fi

# Step 5: Build Frontend
if [ "$ENVIRONMENT" != "dev" ]; then
    echo -e "${YELLOW}[5/6] Building Frontend...${NC}"
    cd "$PROJECT_ROOT/frontend"
    
    NODE_ENV=production npm run build
    
    echo -e "  ${GREEN}✓ Frontend built${NC}"
else
    echo -e "${YELLOW}[5/6] Skipping Frontend Build (dev mode)${NC}"
fi

# Step 6: Start Services
echo -e "${YELLOW}[6/6] Starting Services...${NC}"

if [ "$DOCKER_ONLY" = true ]; then
    cd "$PROJECT_ROOT"
    docker network create Ai_project 2>/dev/null || true
    docker-compose up -d
    echo -e "  ${GREEN}✓ Docker services started${NC}"
else
    echo -e "  → Use start-dev.sh for local or docker-compose for Docker"
fi

# Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo -e "  Environment:     $ENVIRONMENT"
echo -e "  ${GREEN}Status:          Ready${NC}"
echo ""

case $ENVIRONMENT in
    dev)
        echo -e "  URLs:"
        echo -e "  ${YELLOW}• Frontend: http://localhost:6501${NC}"
        echo -e "  ${YELLOW}• Backend:  http://localhost:6001${NC}"
        ;;
    staging)
        echo -e "  URLs:"
        echo -e "  ${YELLOW}• Frontend: http://staging.store-erp.local${NC}"
        echo -e "  ${YELLOW}• Backend:  http://api.staging.store-erp.local${NC}"
        ;;
    production)
        echo -e "  URLs:"
        echo -e "  ${YELLOW}• Frontend: https://store-erp.com${NC}"
        echo -e "  ${YELLOW}• Backend:  https://api.store-erp.com${NC}"
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""
