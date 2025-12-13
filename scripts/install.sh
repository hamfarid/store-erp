#!/bin/bash

# 🏪 نظام إدارة المخزون الكامل - سكريبت التثبيت
# Complete Inventory Management System - Installation Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        REQUIRED_VERSION="3.8"
        if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
            print_success "Python $PYTHON_VERSION found"
            return 0
        else
            print_error "Python $PYTHON_VERSION found, but Python $REQUIRED_VERSION or higher is required"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Function to check Node.js version
check_node_version() {
    if command_exists node; then
        NODE_VERSION=$(node -v | sed 's/v//')
        REQUIRED_VERSION="16.0.0"
        if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
            print_success "Node.js $NODE_VERSION found"
            return 0
        else
            print_error "Node.js $NODE_VERSION found, but Node.js $REQUIRED_VERSION or higher is required"
            return 1
        fi
    else
        print_error "Node.js not found"
        return 1
    fi
}

# Main installation function
main() {
    print_status "🏪 بدء تثبيت نظام إدارة المخزون الكامل..."
    print_status "Starting Complete Inventory Management System installation..."
    
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "يرجى تشغيل هذا السكريبت من المجلد الجذر للمشروع"
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Check system requirements
    print_status "فحص متطلبات النظام..."
    print_status "Checking system requirements..."
    
    if ! check_python_version; then
        print_error "يرجى تثبيت Python 3.8 أو أحدث"
        print_error "Please install Python 3.8 or newer"
        exit 1
    fi
    
    if ! check_node_version; then
        print_error "يرجى تثبيت Node.js 16 أو أحدث"
        print_error "Please install Node.js 16 or newer"
        exit 1
    fi
    
    if ! command_exists npm; then
        print_error "npm غير موجود. يرجى تثبيت Node.js مع npm"
        print_error "npm not found. Please install Node.js with npm"
        exit 1
    fi
    
    # Install backend dependencies
    print_status "تثبيت متطلبات الخادم الخلفي..."
    print_status "Installing backend dependencies..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "إنشاء بيئة افتراضية..."
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "تفعيل البيئة الافتراضية..."
    print_status "Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || {
        print_error "فشل في تفعيل البيئة الافتراضية"
        print_error "Failed to activate virtual environment"
        exit 1
    }
    
    # Upgrade pip
    print_status "تحديث pip..."
    print_status "Upgrading pip..."
    python -m pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        print_status "تثبيت متطلبات Python..."
        print_status "Installing Python requirements..."
        pip install -r requirements.txt
    else
        print_warning "ملف requirements.txt غير موجود، تثبيت المتطلبات الأساسية..."
        print_warning "requirements.txt not found, installing basic requirements..."
        pip install flask flask-cors flask-sqlalchemy sqlalchemy werkzeug bcrypt openpyxl pandas
    fi
    
    print_success "تم تثبيت متطلبات الخادم الخلفي بنجاح"
    print_success "Backend dependencies installed successfully"
    
    # Go back to project root
    cd ..
    
    # Install frontend dependencies
    print_status "تثبيت متطلبات الواجهة الأمامية..."
    print_status "Installing frontend dependencies..."
    
    cd frontend
    
    # Install npm dependencies
    print_status "تثبيت حزم npm..."
    print_status "Installing npm packages..."
    npm install
    
    print_success "تم تثبيت متطلبات الواجهة الأمامية بنجاح"
    print_success "Frontend dependencies installed successfully"
    
    # Go back to project root
    cd ..
    
    # Create necessary directories
    print_status "إنشاء المجلدات المطلوبة..."
    print_status "Creating necessary directories..."
    
    mkdir -p backend/instance
    mkdir -p backend/logs
    mkdir -p docs
    
    # Set permissions for scripts
    print_status "تعيين صلاحيات السكريبتات..."
    print_status "Setting script permissions..."
    
    chmod +x scripts/*.sh 2>/dev/null || true
    
    # Create .env files if they don't exist
    if [ ! -f "backend/.env" ]; then
        print_status "إنشاء ملف .env للخادم الخلفي..."
        print_status "Creating backend .env file..."
        cat > backend/.env << EOF
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///instance/inventory.db
EOF
    fi
    
    if [ ! -f "frontend/.env" ]; then
        print_status "إنشاء ملف .env للواجهة الأمامية..."
        print_status "Creating frontend .env file..."
        cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
EOF
    fi
    
    print_success "🎉 تم تثبيت النظام بنجاح!"
    print_success "🎉 System installed successfully!"
    
    echo ""
    print_status "للبدء في استخدام النظام:"
    print_status "To start using the system:"
    echo ""
    print_status "  ./scripts/start.sh"
    echo ""
    print_status "أو تشغيل الخوادم منفصلة:"
    print_status "Or run servers separately:"
    echo ""
    print_status "  # الخادم الخلفي / Backend:"
    print_status "  cd backend && source venv/bin/activate && python src/main.py"
    echo ""
    print_status "  # الواجهة الأمامية / Frontend:"
    print_status "  cd frontend && npm run dev"
    echo ""
}

# Run main function
main "$@"
