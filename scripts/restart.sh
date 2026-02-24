#!/bin/bash

################################################################################
# Store ERP - Restart Script
# Version: 2.0.0
# Description: Restart both backend and frontend servers
################################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

################################################################################
# Restart
################################################################################

print_header "Restarting Store ERP"

# Stop servers
print_info "Stopping servers..."
"$PROJECT_DIR/stop.sh"

# Wait a moment
sleep 2

# Start servers
print_info "Starting servers..."
"$PROJECT_DIR/start.sh"

print_success "Restart complete!"
