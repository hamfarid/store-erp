#!/bin/bash

###############################################################################
# Dependency Update Script for Store ERP
#
# This script updates all dependencies (Python and Node.js) and checks for
# security vulnerabilities.
#
# Author: Store ERP Team
# Version: 2.0
# Last Updated: 2025-12-13
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Store ERP - Dependency Update Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

###############################################################################
# Functions
###############################################################################

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed"
        return 1
    fi
    return 0
}

###############################################################################
# Pre-flight Checks
###############################################################################

log_info "Running pre-flight checks..."

# Check Python
if ! check_command python3.11; then
    log_error "Python 3.11 is required"
    exit 1
fi

# Check pip
if ! check_command pip3; then
    log_error "pip3 is required"
    exit 1
fi

# Check Node.js
if ! check_command node; then
    log_error "Node.js is required"
    exit 1
fi

# Check pnpm
if ! check_command pnpm; then
    log_warn "pnpm is not installed, installing..."
    npm install -g pnpm
fi

log_info "Pre-flight checks passed ✓"
echo ""

###############################################################################
# Backup Current Dependencies
###############################################################################

log_info "Creating backup of current dependencies..."

BACKUP_DIR="$PROJECT_ROOT/.backups/dependencies-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup Python requirements
if [ -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
    cp "$PROJECT_ROOT/backend/requirements.txt" "$BACKUP_DIR/requirements.txt.bak"
    log_info "Backed up requirements.txt"
fi

# Backup package.json
if [ -f "$PROJECT_ROOT/frontend/package.json" ]; then
    cp "$PROJECT_ROOT/frontend/package.json" "$BACKUP_DIR/package.json.bak"
    log_info "Backed up package.json"
fi

# Backup pnpm-lock.yaml
if [ -f "$PROJECT_ROOT/frontend/pnpm-lock.yaml" ]; then
    cp "$PROJECT_ROOT/frontend/pnpm-lock.yaml" "$BACKUP_DIR/pnpm-lock.yaml.bak"
    log_info "Backed up pnpm-lock.yaml"
fi

log_info "Backup created at: $BACKUP_DIR ✓"
echo ""

###############################################################################
# Update Python Dependencies
###############################################################################

log_info "Updating Python dependencies..."

cd "$PROJECT_ROOT/backend"

# Check for outdated packages
log_info "Checking for outdated Python packages..."
pip3 list --outdated || true

# Update pip
log_info "Updating pip..."
python3.11 -m pip install --upgrade pip

# Update setuptools and wheel
log_info "Updating setuptools and wheel..."
pip3 install --upgrade setuptools wheel

# Option 1: Update all packages (commented out for safety)
# pip3 install --upgrade -r requirements.txt

# Option 2: Update specific packages (safer)
log_info "Updating critical packages..."
pip3 install --upgrade flask flask-login flask-sqlalchemy flask-cors

# Security check with pip-audit (if available)
if command -v pip-audit &> /dev/null; then
    log_info "Running security audit with pip-audit..."
    pip-audit || log_warn "Security vulnerabilities found"
else
    log_warn "pip-audit not installed, skipping security check"
    log_info "Install with: pip3 install pip-audit"
fi

# Generate new requirements.txt
log_info "Generating new requirements.txt..."
pip3 freeze > requirements.txt.new
log_info "New requirements saved to requirements.txt.new"
log_warn "Review requirements.txt.new before replacing requirements.txt"

log_info "Python dependencies updated ✓"
echo ""

###############################################################################
# Update Node.js Dependencies
###############################################################################

log_info "Updating Node.js dependencies..."

cd "$PROJECT_ROOT/frontend"

# Check for outdated packages
log_info "Checking for outdated Node.js packages..."
pnpm outdated || true

# Update pnpm
log_info "Updating pnpm..."
pnpm add -g pnpm

# Update dependencies
log_info "Updating dependencies..."
pnpm update

# Update dev dependencies
log_info "Updating dev dependencies..."
pnpm update --dev

# Security audit
log_info "Running security audit..."
pnpm audit || log_warn "Security vulnerabilities found"

# Try to fix vulnerabilities
log_info "Attempting to fix vulnerabilities..."
pnpm audit --fix || log_warn "Some vulnerabilities could not be fixed automatically"

log_info "Node.js dependencies updated ✓"
echo ""

###############################################################################
# Check for Breaking Changes
###############################################################################

log_info "Checking for potential breaking changes..."

# Check React version
REACT_VERSION=$(pnpm list react --depth=0 2>/dev/null | grep react@ | awk '{print $2}' || echo "unknown")
log_info "React version: $REACT_VERSION"

# Check Vite version
VITE_VERSION=$(pnpm list vite --depth=0 2>/dev/null | grep vite@ | awk '{print $2}' || echo "unknown")
log_info "Vite version: $VITE_VERSION"

# Check Flask version
cd "$PROJECT_ROOT/backend"
FLASK_VERSION=$(pip3 show flask 2>/dev/null | grep Version | awk '{print $2}' || echo "unknown")
log_info "Flask version: $FLASK_VERSION"

echo ""

###############################################################################
# Test Installation
###############################################################################

log_info "Testing installation..."

# Test Python imports
cd "$PROJECT_ROOT/backend"
log_info "Testing Python imports..."
python3.11 -c "import flask; import sqlalchemy; print('✓ Python imports OK')" || log_error "Python import test failed"

# Test Node.js installation
cd "$PROJECT_ROOT/frontend"
log_info "Testing Node.js installation..."
pnpm list --depth=0 > /dev/null 2>&1 && log_info "✓ Node.js installation OK" || log_error "Node.js installation test failed"

echo ""

###############################################################################
# Summary
###############################################################################

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Update Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

log_info "Backup location: $BACKUP_DIR"
log_info "Python packages: Updated"
log_info "Node.js packages: Updated"
log_info "Security audits: Completed"

echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review requirements.txt.new and package.json changes"
echo "2. Test the application thoroughly"
echo "3. Run integration tests"
echo "4. Commit changes if everything works"
echo ""

log_warn "If you encounter issues, restore from backup:"
echo "  cp $BACKUP_DIR/requirements.txt.bak $PROJECT_ROOT/backend/requirements.txt"
echo "  cp $BACKUP_DIR/package.json.bak $PROJECT_ROOT/frontend/package.json"
echo "  cp $BACKUP_DIR/pnpm-lock.yaml.bak $PROJECT_ROOT/frontend/pnpm-lock.yaml"

echo ""
log_info "Update complete! ✓"
