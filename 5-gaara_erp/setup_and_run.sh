#!/bin/bash

# Gaara ERP v12 - Complete Setup and Run Script
# This script sets up and runs the complete Gaara ERP system

set -e  # Exit on any error

echo "🚀 Starting Gaara ERP v12 Complete Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/gaara_erp"

print_header "System Requirements Check"

# Check Python version
if ! command -v python3.11 &> /dev/null; then
    print_error "Python 3.11 is required but not installed"
    exit 1
fi
print_status "Python 3.11 found: $(python3.11 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is required but not installed"
    exit 1
fi
print_status "pip3 found: $(pip3 --version)"

# Check Redis
if ! command -v redis-server &> /dev/null; then
    print_warning "Redis not found, installing..."
    sudo apt update
    sudo apt install -y redis-server
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
fi
print_status "Redis server is available"

# Check if Redis is running
if ! redis-cli ping &> /dev/null; then
    print_warning "Redis is not running, starting..."
    sudo systemctl start redis-server
fi
print_status "Redis is running"

print_header "Environment Setup"

# Navigate to project directory
cd "$PROJECT_DIR"
print_status "Working directory: $(pwd)"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found! Please ensure the .env file is present."
    exit 1
fi
print_status ".env file found"

print_header "Python Dependencies Installation"

# Install main requirements
print_status "Installing main requirements..."
pip3 install -r requirements.txt

# Install development requirements (optional)
if [ -f "requirements-dev.txt" ]; then
    print_status "Installing development requirements..."
    pip3 install -r requirements-dev.txt
fi

# Install optional requirements (for AI features)
if [ -f "requirements-optional.txt" ]; then
    print_warning "Optional requirements available for AI features"
    read -p "Install optional AI requirements? (y/N): " install_optional
    if [[ $install_optional =~ ^[Yy]$ ]]; then
        print_status "Installing optional requirements..."
        pip3 install -r requirements-optional.txt
    fi
fi

print_header "Database Setup"

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    print_status "Database not found, will be created during migration"
fi

# Run migrations
print_status "Running database migrations..."
python3.11 manage.py migrate

# Check if admin user exists
print_status "Checking admin user..."
if python3.11 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Admin exists:', User.objects.filter(username='admin').exists())" | grep "Admin exists: False" > /dev/null; then
    print_status "Creating admin user..."
    python3.11 create_admin.py
else
    print_status "Admin user already exists"
fi

print_header "Static Files Collection"

# Collect static files
print_status "Collecting static files..."
python3.11 manage.py collectstatic --noinput

print_header "System Validation"

# Run system checks
print_status "Running system checks..."
python3.11 manage.py check

# Run integration tests
print_status "Running integration tests..."
python3.11 test_integration.py

print_header "Frontend Setup"

# Check if Node.js is available for frontend
if command -v node &> /dev/null && [ -d "main-frontend" ]; then
    print_status "Node.js found, setting up frontend..."
    cd main-frontend
    
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    print_status "Building frontend..."
    npm run build
    
    cd ..
else
    print_warning "Node.js not found or frontend directory missing, skipping frontend setup"
fi

print_header "Service Configuration"

# Create systemd service file (optional)
create_service() {
    cat > /tmp/gaara-erp.service << EOF
[Unit]
Description=Gaara ERP v12
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PATH
ExecStart=/usr/bin/python3.11 $PROJECT_DIR/manage.py runserver 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    print_status "Systemd service file created at /tmp/gaara-erp.service"
    print_status "To install: sudo cp /tmp/gaara-erp.service /etc/systemd/system/"
    print_status "To enable: sudo systemctl enable gaara-erp"
    print_status "To start: sudo systemctl start gaara-erp"
}

read -p "Create systemd service file? (y/N): " create_svc
if [[ $create_svc =~ ^[Yy]$ ]]; then
    create_service
fi

print_header "Startup Information"

print_status "Setup completed successfully!"
echo ""
echo -e "${BLUE}🎉 Gaara ERP v12 is ready to run!${NC}"
echo ""
echo -e "${GREEN}Admin Login Information:${NC}"
echo "  Username: admin"
echo "  Email: admin@gaara-erp.com"
echo "  Password: Admin@123456"
echo ""
echo -e "${GREEN}Access URLs:${NC}"
echo "  Main Application: http://localhost:8000/"
echo "  Admin Panel: http://localhost:8000/admin/"
echo "  API Documentation: http://localhost:8000/api/"
echo ""
echo -e "${GREEN}To start the server:${NC}"
echo "  cd $PROJECT_DIR"
echo "  python3.11 manage.py runserver 0.0.0.0:8000"
echo ""

# Ask if user wants to start the server now
read -p "Start the server now? (Y/n): " start_server
if [[ ! $start_server =~ ^[Nn]$ ]]; then
    print_header "Starting Gaara ERP Server"
    print_status "Server starting on http://localhost:8000/"
    print_status "Press Ctrl+C to stop the server"
    echo ""
    python3.11 manage.py runserver 0.0.0.0:8000
fi

print_status "Script completed!"
