#!/bin/bash

################################################################################
# Store ERP - Start Script
# Version: 2.0.0
# Description: Start both backend and frontend servers
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# PID files
BACKEND_PID_FILE="$PROJECT_DIR/.backend.pid"
FRONTEND_PID_FILE="$PROJECT_DIR/.frontend.pid"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

wait_for_port() {
    local port=$1
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if check_port $port; then
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done
    return 1
}

################################################################################
# Check if already running
################################################################################

if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        print_warning "Backend is already running (PID: $BACKEND_PID)"
        read -p "Stop and restart? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Stopping backend..."
            kill $BACKEND_PID
            rm -f "$BACKEND_PID_FILE"
            sleep 2
        else
            print_info "Keeping backend running"
        fi
    else
        rm -f "$BACKEND_PID_FILE"
    fi
fi

if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_warning "Frontend is already running (PID: $FRONTEND_PID)"
        read -p "Stop and restart? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Stopping frontend..."
            kill $FRONTEND_PID
            rm -f "$FRONTEND_PID_FILE"
            sleep 2
        else
            print_info "Keeping frontend running"
        fi
    else
        rm -f "$FRONTEND_PID_FILE"
    fi
fi

################################################################################
# Start Backend
################################################################################

print_header "Starting Backend Server"

cd "$PROJECT_DIR/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found"
    print_info "Run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Flask app exists
if [ ! -f "src/app.py" ] && [ ! -f "app.py" ]; then
    print_error "Flask app not found"
    exit 1
fi

# Determine Flask app location
if [ -f "src/app.py" ]; then
    FLASK_APP="src/app.py"
else
    FLASK_APP="app.py"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start backend server
print_info "Starting Flask server..."

# Check if port is available
BACKEND_PORT=${PORT:-8000}
if check_port $BACKEND_PORT; then
    print_error "Port $BACKEND_PORT is already in use"
    print_info "Stop the process using this port or change PORT in backend/.env"
    exit 1
fi

# Start backend in background
nohup python $FLASK_APP > "$PROJECT_DIR/logs/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$BACKEND_PID_FILE"

# Wait for backend to start
print_info "Waiting for backend to start..."
if wait_for_port $BACKEND_PORT; then
    print_success "Backend started successfully (PID: $BACKEND_PID)"
    print_info "Backend URL: http://localhost:$BACKEND_PORT"
else
    print_error "Backend failed to start"
    print_info "Check logs: $PROJECT_DIR/logs/backend.log"
    exit 1
fi

################################################################################
# Start Frontend
################################################################################

print_header "Starting Frontend Server"

cd "$PROJECT_DIR/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_error "node_modules not found"
    print_info "Run ./setup.sh first"
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start frontend server
print_info "Starting Vite dev server..."

# Check if port is available
FRONTEND_PORT=5502
if check_port $FRONTEND_PORT; then
    print_error "Port $FRONTEND_PORT is already in use"
    print_info "Stop the process using this port"
    exit 1
fi

# Start frontend in background
nohup pnpm dev > "$PROJECT_DIR/logs/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$FRONTEND_PID_FILE"

# Wait for frontend to start
print_info "Waiting for frontend to start..."
if wait_for_port $FRONTEND_PORT; then
    print_success "Frontend started successfully (PID: $FRONTEND_PID)"
    print_info "Frontend URL: http://localhost:$FRONTEND_PORT"
else
    print_error "Frontend failed to start"
    print_info "Check logs: $PROJECT_DIR/logs/frontend.log"
    exit 1
fi

################################################################################
# Success
################################################################################

print_header "Store ERP Started Successfully!"

echo -e "${GREEN}✓ Both servers are running!${NC}\n"

echo "Access the application:"
echo "  ${BLUE}Frontend:${NC} http://localhost:$FRONTEND_PORT"
echo "  ${BLUE}Backend API:${NC} http://localhost:$BACKEND_PORT"
echo ""
echo "Default login:"
echo "  ${BLUE}Username:${NC} admin"
echo "  ${BLUE}Password:${NC} admin123"
echo ""
echo "Process IDs:"
echo "  ${BLUE}Backend:${NC} $BACKEND_PID"
echo "  ${BLUE}Frontend:${NC} $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  ${BLUE}Backend:${NC} $PROJECT_DIR/logs/backend.log"
echo "  ${BLUE}Frontend:${NC} $PROJECT_DIR/logs/frontend.log"
echo "  ${BLUE}Application:${NC} $PROJECT_DIR/logs/application/app.log"
echo ""
echo "Commands:"
echo "  ${BLUE}Stop servers:${NC} ./stop.sh"
echo "  ${BLUE}Restart servers:${NC} ./restart.sh"
echo "  ${BLUE}Check status:${NC} ./status.sh"
echo "  ${BLUE}View logs:${NC} tail -f logs/backend.log logs/frontend.log"
echo ""

print_success "Happy coding! 🚀"
