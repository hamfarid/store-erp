#!/bin/bash

################################################################################
# Store ERP - Status Script
# Version: 2.0.0
# Description: Check status of backend and frontend servers
################################################################################

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

get_process_info() {
    local pid=$1
    if ps -p $pid > /dev/null 2>&1; then
        ps -p $pid -o pid,ppid,%cpu,%mem,etime,cmd --no-headers
    else
        echo "Process not found"
    fi
}

################################################################################
# Check Status
################################################################################

print_header "Store ERP Status"

BACKEND_RUNNING=0
FRONTEND_RUNNING=0

# Check Backend
echo -e "${BLUE}Backend Server:${NC}"
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        print_success "Running (PID: $BACKEND_PID)"
        echo "  Process: $(get_process_info $BACKEND_PID)"
        
        if check_port 8000; then
            print_success "Port 8000: Listening"
            echo "  URL: http://localhost:8000"
        else
            print_error "Port 8000: Not listening"
        fi
        
        BACKEND_RUNNING=1
    else
        print_error "Not running (stale PID file)"
        rm -f "$BACKEND_PID_FILE"
    fi
else
    print_error "Not running"
fi
echo ""

# Check Frontend
echo -e "${BLUE}Frontend Server:${NC}"
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_success "Running (PID: $FRONTEND_PID)"
        echo "  Process: $(get_process_info $FRONTEND_PID)"
        
        if check_port 5502; then
            print_success "Port 5502: Listening"
            echo "  URL: http://localhost:5502"
        else
            print_error "Port 5502: Not listening"
        fi
        
        FRONTEND_RUNNING=1
    else
        print_error "Not running (stale PID file)"
        rm -f "$FRONTEND_PID_FILE"
    fi
else
    print_error "Not running"
fi
echo ""

# Check Database
echo -e "${BLUE}Database:${NC}"
if [ -f "$PROJECT_DIR/backend/store_erp.db" ]; then
    DB_SIZE=$(du -h "$PROJECT_DIR/backend/store_erp.db" | cut -f1)
    print_success "Database exists (Size: $DB_SIZE)"
    echo "  Location: $PROJECT_DIR/backend/store_erp.db"
else
    print_error "Database not found"
    print_info "Run ./setup.sh to create database"
fi
echo ""

# Check Logs
echo -e "${BLUE}Recent Logs:${NC}"
if [ -f "$PROJECT_DIR/logs/application/app.log" ]; then
    LOG_SIZE=$(du -h "$PROJECT_DIR/logs/application/app.log" | cut -f1)
    print_success "Application log exists (Size: $LOG_SIZE)"
    echo "  Last 5 lines:"
    tail -5 "$PROJECT_DIR/logs/application/app.log" | sed 's/^/    /'
else
    print_info "No application logs yet"
fi
echo ""

# Overall Status
print_header "Overall Status"

if [ $BACKEND_RUNNING -eq 1 ] && [ $FRONTEND_RUNNING -eq 1 ]; then
    echo -e "${GREEN}✓ All services are running${NC}"
    echo ""
    echo "Access the application:"
    echo "  ${BLUE}Frontend:${NC} http://localhost:5502"
    echo "  ${BLUE}Backend API:${NC} http://localhost:8000"
elif [ $BACKEND_RUNNING -eq 1 ] || [ $FRONTEND_RUNNING -eq 1 ]; then
    echo -e "${YELLOW}⚠ Some services are not running${NC}"
    echo ""
    echo "To start all services:"
    echo "  ${BLUE}./start.sh${NC}"
else
    echo -e "${RED}✗ No services are running${NC}"
    echo ""
    echo "To start all services:"
    echo "  ${BLUE}./start.sh${NC}"
fi
echo ""

# Commands
echo "Available commands:"
echo "  ${BLUE}./start.sh${NC}   - Start all servers"
echo "  ${BLUE}./stop.sh${NC}    - Stop all servers"
echo "  ${BLUE}./restart.sh${NC} - Restart all servers"
echo "  ${BLUE}./status.sh${NC}  - Check status (this command)"
echo ""
