#!/bin/bash

################################################################################
# Store ERP - Complete Setup Script
# Version: 2.0.0
# Description: Automated installation and setup for Store ERP
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

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

################################################################################
# Main Setup
################################################################################

print_header "Store ERP - Complete Setup"

echo "This script will:"
echo "  1. Check system requirements"
echo "  2. Install Python dependencies"
echo "  3. Install Node.js dependencies"
echo "  4. Setup database"
echo "  5. Create environment files"
echo "  6. Run initial tests"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Setup cancelled"
    exit 0
fi

################################################################################
# Step 1: Check System Requirements
################################################################################

print_header "Step 1: Checking System Requirements"

# Check Python
if check_command python3.11; then
    PYTHON_VERSION=$(python3.11 --version 2>&1 | awk '{print $2}')
    print_info "Python version: $PYTHON_VERSION"
else
    print_error "Python 3.11 is required but not installed"
    print_info "Install Python 3.11 first:"
    print_info "  Ubuntu: sudo apt install python3.11 python3.11-venv python3.11-dev"
    print_info "  macOS: brew install python@3.11"
    exit 1
fi

# Check pip
if ! check_command pip3; then
    print_error "pip3 is required but not installed"
    print_info "Install pip3: sudo apt install python3-pip"
    exit 1
fi

# Check Node.js
if check_command node; then
    NODE_VERSION=$(node --version)
    print_info "Node.js version: $NODE_VERSION"
    
    # Check if version is >= 18
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -lt 18 ]; then
        print_warning "Node.js version should be >= 18"
        print_info "Current version: $NODE_VERSION"
        print_info "Consider upgrading: https://nodejs.org/"
    fi
else
    print_error "Node.js is required but not installed"
    print_info "Install Node.js 18+:"
    print_info "  Ubuntu: curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs"
    print_info "  macOS: brew install node@22"
    exit 1
fi

# Check pnpm
if ! check_command pnpm; then
    print_warning "pnpm is not installed, installing..."
    npm install -g pnpm
    if check_command pnpm; then
        print_success "pnpm installed successfully"
    else
        print_error "Failed to install pnpm"
        exit 1
    fi
fi

# Check Git
if ! check_command git; then
    print_warning "Git is recommended but not required"
fi

print_success "All system requirements met!"

################################################################################
# Step 2: Setup Python Environment
################################################################################

print_header "Step 2: Setting up Python Environment"

cd "$PROJECT_DIR/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3.11 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies
print_info "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Install development dependencies
if [ -f "requirements-dev.txt" ]; then
    print_info "Installing development dependencies..."
    pip install -r requirements-dev.txt
    print_success "Development dependencies installed"
fi

print_success "Python environment setup complete!"

################################################################################
# Step 3: Setup Node.js Environment
################################################################################

print_header "Step 3: Setting up Node.js Environment"

cd "$PROJECT_DIR/frontend"

# Install Node.js dependencies
print_info "Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    pnpm install
    print_success "Node.js dependencies installed"
else
    print_error "package.json not found"
    exit 1
fi

print_success "Node.js environment setup complete!"

################################################################################
# Step 4: Setup Database
################################################################################

print_header "Step 4: Setting up Database"

cd "$PROJECT_DIR/backend"

# Activate virtual environment
source venv/bin/activate

# Check if database setup script exists
if [ -f "database_setup.py" ]; then
    print_info "Running database setup..."
    python database_setup.py
    print_success "Database setup complete"
elif [ -f "src/database_setup.py" ]; then
    print_info "Running database setup..."
    python src/database_setup.py
    print_success "Database setup complete"
else
    print_warning "Database setup script not found"
    print_info "You may need to run database migrations manually"
fi

# Run migrations if Flask-Migrate is used
if [ -d "migrations" ]; then
    print_info "Running database migrations..."
    if command -v flask &> /dev/null; then
        flask db upgrade
        print_success "Database migrations complete"
    else
        print_warning "Flask command not found, skipping migrations"
    fi
fi

print_success "Database setup complete!"

################################################################################
# Step 5: Create Environment Files
################################################################################

print_header "Step 5: Creating Environment Files"

cd "$PROJECT_DIR"

# Backend .env
if [ ! -f "backend/.env" ]; then
    print_info "Creating backend .env file..."
    cat > backend/.env << 'EOF'
# Flask Configuration
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# Database
DATABASE_URL=sqlite:///store_erp.db

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:5502,http://localhost:3004

# Logging
LOG_LEVEL=INFO
LOG_DIR=../logs

# 2FA
TOTP_ISSUER=Store ERP

# Session
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
EOF
    print_success "Backend .env created"
    print_warning "Please update SECRET_KEY and JWT_SECRET_KEY in backend/.env"
else
    print_info "Backend .env already exists"
fi

# Frontend .env
if [ ! -f "frontend/.env" ]; then
    print_info "Creating frontend .env file..."
    cat > frontend/.env << 'EOF'
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# App Configuration
VITE_APP_NAME=Store ERP
VITE_APP_VERSION=2.0.0

# Features
VITE_ENABLE_2FA=true
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_RTL=true
EOF
    print_success "Frontend .env created"
else
    print_info "Frontend .env already exists"
fi

print_success "Environment files created!"

################################################################################
# Step 6: Create Required Directories
################################################################################

print_header "Step 6: Creating Required Directories"

cd "$PROJECT_DIR"

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs/application logs/security logs/performance logs/errors
    print_success "Logs directory created"
fi

# Create backups directory
if [ ! -d ".backups" ]; then
    mkdir -p .backups
    print_success "Backups directory created"
fi

# Create uploads directory
if [ ! -d "backend/uploads" ]; then
    mkdir -p backend/uploads
    print_success "Uploads directory created"
fi

print_success "Required directories created!"

################################################################################
# Step 7: Run Tests
################################################################################

print_header "Step 7: Running Tests"

cd "$PROJECT_DIR/backend"
source venv/bin/activate

if command -v pytest &> /dev/null; then
    print_info "Running Python tests..."
    if pytest --tb=short -v; then
        print_success "All Python tests passed!"
    else
        print_warning "Some Python tests failed"
        print_info "You can continue, but please review the test failures"
    fi
else
    print_warning "pytest not found, skipping tests"
fi

print_success "Tests complete!"

################################################################################
# Step 8: Build Frontend (Optional)
################################################################################

print_header "Step 8: Building Frontend (Optional)"

read -p "Do you want to build the frontend now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$PROJECT_DIR/frontend"
    print_info "Building frontend..."
    pnpm build
    print_success "Frontend built successfully!"
else
    print_info "Skipping frontend build"
fi

################################################################################
# Setup Complete
################################################################################

print_header "Setup Complete!"

echo -e "${GREEN}✓ Store ERP setup completed successfully!${NC}\n"

echo "Next steps:"
echo ""
echo "1. Update environment variables:"
echo "   - backend/.env (SECRET_KEY, JWT_SECRET_KEY)"
echo "   - frontend/.env (if needed)"
echo ""
echo "2. Start the application:"
echo "   ${BLUE}./start.sh${NC}"
echo ""
echo "3. Access the application:"
echo "   - Frontend: http://localhost:5502"
echo "   - Backend API: http://localhost:8000"
echo ""
echo "4. Default login credentials:"
echo "   - Username: admin"
echo "   - Password: admin123"
echo ""
echo "5. View logs:"
echo "   - Application: logs/application/app.log"
echo "   - Security: logs/security/security.log"
echo ""
echo "For more information, see:"
echo "   - README.md"
echo "   - docs/USER_GUIDE.md"
echo "   - docs/DEVELOPER_GUIDE.md"
echo ""

print_success "Happy coding! 🚀"
