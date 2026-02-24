#!/bin/bash

################################################################################
# Store ERP - Stop Script
# Version: 2.0.0
# Description: Stop both backend and frontend servers
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

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

################################################################################
# Stop Servers
################################################################################

print_header "Stopping Store ERP Servers"

STOPPED=0

# Stop Backend
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        print_info "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        
        # Wait for process to stop
        for i in {1..10}; do
            if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            print_warning "Backend not responding, force killing..."
            kill -9 $BACKEND_PID
        fi
        
        print_success "Backend stopped"
        STOPPED=$((STOPPED + 1))
    else
        print_warning "Backend process not found (PID: $BACKEND_PID)"
    fi
    rm -f "$BACKEND_PID_FILE"
else
    print_info "Backend is not running"
fi

# Stop Frontend
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        print_info "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        
        # Wait for process to stop
        for i in {1..10}; do
            if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            print_warning "Frontend not responding, force killing..."
            kill -9 $FRONTEND_PID
        fi
        
        print_success "Frontend stopped"
        STOPPED=$((STOPPED + 1))
    else
        print_warning "Frontend process not found (PID: $FRONTEND_PID)"
    fi
    rm -f "$FRONTEND_PID_FILE"
else
    print_info "Frontend is not running"
fi

# Kill any remaining processes on ports
print_info "Checking for processes on ports..."

# Backend port (8000)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warning "Found process on port 8000, killing..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
fi

# Frontend port (5502)
if lsof -Pi :5502 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warning "Found process on port 5502, killing..."
    lsof -ti:5502 | xargs kill -9 2>/dev/null || true
fi

################################################################################
# Success
################################################################################

print_header "Store ERP Stopped"

if [ $STOPPED -gt 0 ]; then
    echo -e "${GREEN}✓ Stopped $STOPPED server(s)${NC}\n"
else
    echo -e "${YELLOW}⚠ No servers were running${NC}\n"
fi

echo "To start the servers again:"
echo "  ${BLUE}./start.sh${NC}"
echo ""
