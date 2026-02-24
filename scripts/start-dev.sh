#!/bin/bash
# =============================================================================
# Store ERP - Development Mode Startup Script
# =============================================================================
# Starts backend and frontend in development mode with hot reload
# =============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Store ERP - Development Mode${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate || source .venv/Scripts/activate

# Install/upgrade dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r backend/requirements.txt --upgrade

# Check if argon2-cffi is installed
if ! python -c "import argon2" 2>/dev/null; then
    echo -e "${YELLOW}Installing argon2-cffi...${NC}"
    pip install argon2-cffi==23.1.0
fi

echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Kill any existing Python processes
pkill -f "flask run" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true

# Start backend
echo -e "${BLUE}Starting backend on http://127.0.0.1:5002${NC}"
cd backend
export FLASK_APP=app:create_app
export FLASK_ENV=development
export FLASK_DEBUG=1

python -m flask run --host=0.0.0.0 --port=5002 --debug &
BACKEND_PID=$!

cd ..

echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}\n"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Development Server Running${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${GREEN}Services:${NC}"
echo "  Backend:  http://127.0.0.1:5002"
echo "  API Docs: http://127.0.0.1:5002/api"
echo "  Health:   http://127.0.0.1:5002/health"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}\n"

# Wait for backend process
wait $BACKEND_PID
