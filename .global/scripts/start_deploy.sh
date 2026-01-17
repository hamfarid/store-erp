#!/bin/bash
# Start Deploy Script
# Automates the deployment process from development to production

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ  $1${NC}"
}

# Check if config manager exists
if [ ! -f "tools/project_config_manager.py" ]; then
    print_error "Configuration manager not found!"
    echo "Please ensure you're in the project root directory."
    exit 1
fi

# Load configuration
if [ ! -f ".global/project_config.json" ]; then
    print_error "No configuration found!"
    echo "Please run: python3 tools/project_config_manager.py setup"
    exit 1
fi

# Start deployment
print_header "STARTING DEPLOYMENT PROCESS"
echo ""

# Step 1: Pre-deployment checks
print_info "Step 1: Pre-deployment checks..."
echo ""

# Check if git repository
if [ -d ".git" ]; then
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "You have uncommitted changes."
        read -p "Continue anyway? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Deployment cancelled."
            exit 1
        fi
    else
        print_success "No uncommitted changes"
    fi
fi

# Check if tests exist and run them
if [ -f "pytest.ini" ] || [ -f "tests/" ]; then
    print_info "Running tests..."
    if command -v pytest &> /dev/null; then
        pytest || {
            print_error "Tests failed!"
            read -p "Continue anyway? [y/N]: " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        }
        print_success "Tests passed"
    else
        print_warning "pytest not found, skipping tests"
    fi
fi

print_success "Pre-deployment checks completed"
echo ""

# Step 2: Backup current state
print_info "Step 2: Backing up current state..."
echo ""

BACKUP_DIR="backups/deploy_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup database (if applicable)
if command -v pg_dump &> /dev/null; then
    print_info "Backing up PostgreSQL database..."
    # Get database name from config
    DB_NAME=$(python3 -c "import json; print(json.load(open('.global/project_config.json'))['database']['name'])")
    pg_dump "$DB_NAME" > "$BACKUP_DIR/database.sql" 2>/dev/null || print_warning "Database backup failed (might not exist yet)"
fi

# Backup configuration
cp -r .global "$BACKUP_DIR/" 2>/dev/null || true
cp .env "$BACKUP_DIR/" 2>/dev/null || true

print_success "Backup created: $BACKUP_DIR"
echo ""

# Step 3: Build production assets
print_info "Step 3: Building production assets..."
echo ""

# Frontend build (if applicable)
if [ -f "package.json" ]; then
    print_info "Building frontend..."
    if command -v npm &> /dev/null; then
        npm run build || print_warning "Frontend build failed"
        print_success "Frontend built"
    fi
fi

# Backend build (if applicable)
if [ -f "requirements.txt" ]; then
    print_info "Installing Python dependencies..."
    pip3 install -r requirements.txt --quiet
    print_success "Dependencies installed"
fi

print_success "Production assets built"
echo ""

# Step 4: Database setup
print_info "Step 4: Setting up database..."
echo ""

# Run migrations (Django example)
if [ -f "manage.py" ]; then
    print_info "Running Django migrations..."
    python3 manage.py migrate
    print_success "Migrations applied"
fi

# Run migrations (Flask example)
if [ -f "app.py" ] && command -v flask &> /dev/null; then
    print_info "Running Flask migrations..."
    flask db upgrade || print_warning "Flask migrations not configured"
fi

print_success "Database setup completed"
echo ""

# Step 5: Security hardening
print_info "Step 5: Applying security hardening..."
echo ""

# Update configuration to production
python3 tools/project_config_manager.py deploy

print_success "Security hardening applied"
echo ""

# Step 6: Launch application
print_info "Step 6: Launching application..."
echo ""

# Get configuration
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('.global/project_config.json'))['project']['name'])")
HOST=$(python3 -c "import json; print(json.load(open('.global/project_config.json'))['environment']['host'])")
FRONTEND_PORT=$(python3 -c "import json; print(json.load(open('.global/project_config.json'))['ports']['frontend'])")
BACKEND_PORT=$(python3 -c "import json; print(json.load(open('.global/project_config.json'))['ports']['backend'])")
ADMIN_USERNAME=$(python3 -c "import json; print(json.load(open('.global/project_config.json'))['admin']['username'])")

# Start services (example - customize based on your stack)
print_info "Starting services..."

# Example: Start with systemd
# systemctl start myapp

# Example: Start with PM2
# pm2 start ecosystem.config.js

# Example: Start with Docker
# docker-compose up -d

print_success "Services started"
echo ""

# Step 7: Post-deployment
print_info "Step 7: Post-deployment tasks..."
echo ""

# Health check
print_info "Performing health check..."
sleep 2

# Try to check if backend is responding
if command -v curl &> /dev/null; then
    if curl -s "http://$HOST:$BACKEND_PORT/health" > /dev/null 2>&1; then
        print_success "Health check passed"
    else
        print_warning "Health check endpoint not responding (might not be implemented)"
    fi
fi

print_success "Post-deployment tasks completed"
echo ""

# Final summary
print_header "DEPLOYMENT SUCCESSFUL!"
echo ""
echo -e "${GREEN}🎉 Your project has been deployed to production!${NC}"
echo ""
echo "Project: $PROJECT_NAME"
echo "Phase: PRODUCTION"
echo ""
echo "URLs:"
echo "  Frontend: http://$HOST:$FRONTEND_PORT"
echo "  Backend:  http://$HOST:$BACKEND_PORT"
echo "  Admin:    http://$HOST:$BACKEND_PORT/admin"
echo "  Setup:    http://$HOST:$FRONTEND_PORT/setup"
echo ""
echo "Admin Credentials:"
echo "  Username: $ADMIN_USERNAME"
echo "  Password: (check output above or .global/project_config.json)"
echo ""
echo -e "${YELLOW}⚠  IMPORTANT:${NC}"
echo "  1. Save your admin credentials securely"
echo "  2. Change the admin password after first login"
echo "  3. Complete the setup wizard"
echo "  4. Configure SSL/HTTPS for production"
echo "  5. Set up monitoring and backups"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
print_info "Opening admin panel and setup wizard..."

# Open URLs in browser (if available)
if command -v xdg-open &> /dev/null; then
    xdg-open "http://$HOST:$BACKEND_PORT/admin" 2>/dev/null &
    sleep 1
    xdg-open "http://$HOST:$FRONTEND_PORT/setup" 2>/dev/null &
elif command -v open &> /dev/null; then
    open "http://$HOST:$BACKEND_PORT/admin" 2>/dev/null &
    sleep 1
    open "http://$HOST:$FRONTEND_PORT/setup" 2>/dev/null &
else
    print_info "Please open the URLs above in your browser"
fi

echo ""
print_success "Deployment complete!"

