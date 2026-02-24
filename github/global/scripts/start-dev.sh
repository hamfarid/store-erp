#!/bin/bash
# =============================================================================
# Store ERP v2.0.0 - Development Start Script (Bash)
# =============================================================================
# Usage: ./scripts/start-dev.sh
# =============================================================================

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║           Store ERP v2.0.0 - Development Mode                     ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Get project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Python virtual environment
if [ ! -d "$PROJECT_ROOT/backend/venv" ]; then
    echo -e "${YELLOW}[!] Virtual environment not found. Creating...${NC}"
    cd "$PROJECT_ROOT/backend"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Check Node modules
if [ ! -d "$PROJECT_ROOT/frontend/node_modules" ]; then
    echo -e "${YELLOW}[!] Node modules not found. Installing...${NC}"
    cd "$PROJECT_ROOT/frontend"
    npm install
fi

echo ""
echo -e "${GREEN}[INFO] Starting services...${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    jobs -p | xargs -r kill 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${CYAN}[1/2] Starting Backend (Port 6001)...${NC}"
cd "$PROJECT_ROOT/backend"
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Wait for backend
sleep 3

# Start frontend
echo -e "${CYAN}[2/2] Starting Frontend (Port 6501)...${NC}"
cd "$PROJECT_ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo -e "  ${NC}Services Running:${NC}"
echo -e "  • Backend API:  ${YELLOW}http://localhost:6001${NC}"
echo -e "  • Frontend App: ${YELLOW}http://localhost:6501${NC}"
echo ""
echo -e "  ${NC}Default Login:${NC}"
echo -e "  • Username: ${YELLOW}admin${NC}"
echo -e "  • Password: ${YELLOW}admin123${NC}"
echo ""
echo -e "  ${NC}Press Ctrl+C to stop all services${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Wait for processes
wait
