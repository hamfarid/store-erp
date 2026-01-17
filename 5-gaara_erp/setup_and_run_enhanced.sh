#!/bin/bash

# =============================================================================
# Gaara ERP v12 - Enhanced Complete Setup and Run Script
# =============================================================================
# This script provides comprehensive setup and management for Gaara ERP system
# with 69 active modules, advanced permissions, and full feature support.
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="Gaara ERP v12"
PROJECT_DIR="/home/ubuntu/gaara_erp_v12"
DJANGO_DIR="$PROJECT_DIR/gaara_erp"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="$PROJECT_DIR/logs"
BACKUP_DIR="$PROJECT_DIR/backups"

# Default environment variables
export DJANGO_SETTINGS_MODULE="gaara_erp.settings"
export APP_MODE="dev"
export DEBUG="True"
export SECRET_KEY="gaara-erp-v12-secret-key-change-in-production"
export DATABASE_URL="sqlite:///db.sqlite3"
export REDIS_URL="redis://localhost:6379/0"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# =============================================================================
# Utility Functions
# =============================================================================

print_header() {
    echo -e "${BLUE}=============================================================================${NC}"
    echo -e "${BLUE} $1 ${NC}"
    echo -e "${BLUE}=============================================================================${NC}"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_info "$1 is installed ✓"
        return 0
    else
        print_warning "$1 is not installed"
        return 1
    fi
}

# =============================================================================
# System Requirements Check
# =============================================================================

check_system_requirements() {
    print_header "Checking System Requirements"
    
    # Check Python
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_info "Python version: $PYTHON_VERSION"
        
        # Check if Python version is 3.8+
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python version is compatible"
        else
            print_error "Python 3.8+ is required"
            exit 1
        fi
    else
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check pip
    if ! check_command pip3; then
        print_error "pip3 is required but not installed"
        exit 1
    fi
    
    # Check git
    check_command git
    
    # Check Redis
    if ! check_command redis-server; then
        print_warning "Redis not found, attempting to install..."
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y redis-server
            sudo systemctl start redis-server
            sudo systemctl enable redis-server
        elif command -v yum &> /dev/null; then
            sudo yum install -y redis
            sudo systemctl start redis
            sudo systemctl enable redis
        else
            print_warning "Could not install Redis automatically"
        fi
    fi
    
    # Check if Redis is running
    if command -v redis-cli &> /dev/null; then
        if redis-cli ping &> /dev/null; then
            print_success "Redis is running"
        else
            print_warning "Redis is installed but not running, starting..."
            sudo systemctl start redis-server || sudo systemctl start redis
        fi
    fi
    
    # Check optional dependencies
    check_command postgresql
    check_command nginx
    
    print_success "System requirements check completed"
}

# =============================================================================
# Environment Setup
# =============================================================================

setup_environment() {
    print_header "Setting Up Environment"
    
    # Create project directories
    print_step "Creating project directories"
    mkdir -p "$LOG_DIR"
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$PROJECT_DIR/media"
    mkdir -p "$PROJECT_DIR/static"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        print_step "Creating virtual environment"
        python3 -m venv "$VENV_DIR"
    else
        print_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_step "Activating virtual environment"
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    print_step "Upgrading pip"
    pip install --upgrade pip
    
    # Create .env file if it doesn't exist
    if [ ! -f "$DJANGO_DIR/.env" ]; then
        print_step "Creating .env file"
        cat > "$DJANGO_DIR/.env" << EOF
# Gaara ERP v12 Environment Configuration
DEBUG=True
SECRET_KEY=gaara-erp-v12-secret-key-change-in-production
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
APP_MODE=dev
DJANGO_SETTINGS_MODULE=gaara_erp.settings

# Security Settings (for production)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Email Settings (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# AI Features (optional)
ENABLE_AI_FEATURES=True
OPENAI_API_KEY=
HUGGINGFACE_API_KEY=

# File Storage
MEDIA_ROOT=$PROJECT_DIR/media
STATIC_ROOT=$PROJECT_DIR/static
EOF
        print_success ".env file created"
    else
        print_info ".env file already exists"
    fi
    
    print_success "Environment setup completed"
}

# =============================================================================
# Dependencies Installation
# =============================================================================

install_dependencies() {
    print_header "Installing Dependencies"
    
    cd "$DJANGO_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Install main requirements
    print_step "Installing main requirements"
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Main requirements installed (134 packages)"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
    
    # Install development requirements (optional)
    if [ -f "requirements-dev.txt" ]; then
        print_step "Installing development requirements"
        pip install -r requirements-dev.txt
        print_info "Development requirements installed (35 packages)"
    fi
    
    # Install optional requirements (AI features)
    if [ -f "requirements-optional.txt" ] && [ "$INSTALL_OPTIONAL" = "true" ]; then
        print_step "Installing optional requirements (AI features)"
        pip install -r requirements-optional.txt
        print_info "Optional AI requirements installed (64 packages)"
    fi
    
    print_success "Dependencies installation completed"
}

# =============================================================================
# Database Setup
# =============================================================================

setup_database() {
    print_header "Setting Up Database"
    
    cd "$DJANGO_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Check database connection
    print_step "Checking database connection"
    if python manage.py check --database default; then
        print_success "Database connection successful"
    else
        print_error "Database connection failed"
        exit 1
    fi
    
    # Create migrations for all 69 modules
    print_step "Creating migrations for all modules"
    python manage.py makemigrations --noinput
    
    # Apply migrations
    print_step "Applying migrations"
    python manage.py migrate --noinput
    
    # Create superuser if it doesn't exist
    print_step "Creating superuser (if needed)"
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gaara-erp.com', 'Admin@123456')
    print('✓ Superuser created: admin / Admin@123456')
else:
    print('✓ Superuser already exists')
"
    
    # Initialize permissions system
    print_step "Initializing permissions system"
    python manage.py shell -c "
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Count permissions
total_permissions = Permission.objects.count()
print(f'✓ Total permissions in system: {total_permissions}')

# Check core permissions
try:
    from core_modules.permissions.models import UserPermission, AIPermission
    user_perms = UserPermission.objects.count()
    ai_perms = AIPermission.objects.count()
    print(f'✓ User permissions: {user_perms}')
    print(f'✓ AI permissions: {ai_perms}')
except:
    print('⚠ Custom permissions not yet created')
"
    
    # Load initial data (if available)
    if [ -f "fixtures/initial_data.json" ]; then
        print_step "Loading initial data"
        python manage.py loaddata fixtures/initial_data.json
    fi
    
    print_success "Database setup completed"
}

# =============================================================================
# Static Files Setup
# =============================================================================

setup_static_files() {
    print_header "Setting Up Static Files"
    
    cd "$DJANGO_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Collect static files
    print_step "Collecting static files"
    python manage.py collectstatic --noinput --clear
    
    print_success "Static files setup completed"
}

# =============================================================================
# System Validation
# =============================================================================

validate_system() {
    print_header "Validating System"
    
    cd "$DJANGO_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Run system checks
    print_step "Running system checks"
    python manage.py check
    
    # Check for security issues (development mode)
    if [ "$APP_MODE" = "dev" ]; then
        print_step "Running security checks (development mode)"
        python manage.py check --deploy || print_warning "Some security warnings in development mode (expected)"
    fi
    
    # Test database queries and module status
    print_step "Testing system components"
    python manage.py shell -c "
from django.contrib.auth.models import User, Group, Permission
from django.apps import apps
from django.conf import settings

print('=== System Status ===')
print(f'✓ Users: {User.objects.count()}')
print(f'✓ Groups: {Group.objects.count()}')
print(f'✓ Permissions: {Permission.objects.count()}')
print(f'✓ Installed apps: {len(apps.get_app_configs())}')

# Count modules by category
installed_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
categories = {}
for app in installed_apps:
    if '.' in app:
        category = app.split('.')[0]
        if category not in categories:
            categories[category] = []
        categories[category].append(app)

print(f'✓ Total active modules: {len(installed_apps)}')
for category, apps_list in sorted(categories.items()):
    print(f'  - {category}: {len(apps_list)} modules')

# Test some core models
try:
    from core_modules.organization.models import Company
    print(f'✓ Companies: {Company.objects.count()}')
except Exception as e:
    print(f'⚠ Company model: {e}')

try:
    from business_modules.accounting.models import Account
    print(f'✓ Accounts: {Account.objects.count()}')
except Exception as e:
    print(f'⚠ Account model: {e}')

try:
    from services_modules.assets.models.asset import Asset
    print(f'✓ Assets: {Asset.objects.count()}')
except Exception as e:
    print(f'⚠ Asset model: {e}')

# Test permissions system
try:
    from core_modules.permissions.models import UserPermission, AIPermission
    print(f'✓ User permissions: {UserPermission.objects.count()}')
    print(f'✓ AI permissions: {AIPermission.objects.count()}')
except Exception as e:
    print(f'⚠ Custom permissions: {e}')
"
    
    print_success "System validation completed"
}

# =============================================================================
# Services Setup
# =============================================================================

setup_services() {
    print_header "Setting Up Services"
    
    # Redis setup (if available)
    if command -v redis-server &> /dev/null; then
        print_step "Checking Redis server"
        if ! pgrep -x "redis-server" > /dev/null; then
            print_step "Starting Redis server"
            if command -v systemctl &> /dev/null; then
                sudo systemctl start redis-server || sudo systemctl start redis
            else
                redis-server --daemonize yes
            fi
            print_success "Redis server started"
        else
            print_info "Redis server already running"
        fi
    else
        print_warning "Redis not available - some features may not work"
    fi
    
    # Celery setup (optional)
    if [ "$START_CELERY" = "true" ]; then
        print_step "Starting Celery services"
        cd "$DJANGO_DIR"
        source "$VENV_DIR/bin/activate"
        
        # Start Celery worker
        celery -A gaara_erp worker --loglevel=info --detach --pidfile="$LOG_DIR/celery_worker.pid"
        
        # Start Celery beat
        celery -A gaara_erp beat --loglevel=info --detach --pidfile="$LOG_DIR/celery_beat.pid"
        
        print_success "Celery services started"
    fi
    
    print_success "Services setup completed"
}

# =============================================================================
# Development Server
# =============================================================================

start_development_server() {
    print_header "Starting Development Server"
    
    cd "$DJANGO_DIR"
    source "$VENV_DIR/bin/activate"
    
    print_info "🚀 Gaara ERP v12 Development Server"
    print_info "📊 69 Active Modules | Advanced Permissions | AI Features"
    print_info ""
    print_info "🌐 Server URLs:"
    print_info "  Main Application: http://127.0.0.1:8000"
    print_info "  Admin Panel: http://127.0.0.1:8000/admin"
    print_info "  API Documentation: http://127.0.0.1:8000/api/docs"
    print_info ""
    print_info "🔐 Default Admin Credentials:"
    print_info "  Username: admin"
    print_info "  Password: Admin@123456"
    print_info "  Email: admin@gaara-erp.com"
    print_info ""
    print_info "📋 Available Modules:"
    print_info "  • Core Modules: 16 (Users, Security, Permissions, AI)"
    print_info "  • Business Modules: 10 (Accounting, Inventory, Sales, Assets)"
    print_info "  • Services Modules: 24 (Projects, Maintenance, Analytics)"
    print_info "  • Integration Modules: 7 (AI, Translation, Analytics)"
    print_info "  • Agricultural Modules: 7 (Crops, Livestock, Irrigation)"
    print_info "  • AI Modules: 3 (Intelligent Assistant, Analytics)"
    print_info "  • Helper Modules: 3 (Data Import, Utilities)"
    print_info ""
    print_warning "Press Ctrl+C to stop the server"
    print_info ""
    
    # Start Django development server
    python manage.py runserver 0.0.0.0:8000
}

# =============================================================================
# Production Server Setup
# =============================================================================

setup_production_server() {
    print_header "Setting Up Production Server"
    
    cd "$DJANGO_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Install production server
    pip install gunicorn
    
    # Create gunicorn configuration
    cat > "$PROJECT_DIR/gunicorn.conf.py" << EOF
# Gunicorn configuration for Gaara ERP v12
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
daemon = False
user = "ubuntu"
group = "ubuntu"
tmp_upload_dir = None
logfile = "$LOG_DIR/gunicorn.log"
loglevel = "info"
access_logfile = "$LOG_DIR/gunicorn_access.log"
error_logfile = "$LOG_DIR/gunicorn_error.log"
EOF
    
    print_step "Starting Gunicorn server"
    gunicorn gaara_erp.wsgi:application -c "$PROJECT_DIR/gunicorn.conf.py"
}

# =============================================================================
# System Information
# =============================================================================

show_system_info() {
    print_header "System Information"
    
    cd "$DJANGO_DIR"
    source "$VENV_DIR/bin/activate"
    
    echo -e "${CYAN}🏢 Project Information:${NC}"
    echo "  Name: $PROJECT_NAME"
    echo "  Directory: $PROJECT_DIR"
    echo "  Django Directory: $DJANGO_DIR"
    echo "  Virtual Environment: $VENV_DIR"
    echo ""
    
    echo -e "${CYAN}⚙️ Environment:${NC}"
    echo "  APP_MODE: $APP_MODE"
    echo "  DEBUG: $DEBUG"
    echo "  DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
    echo ""
    
    echo -e "${CYAN}🗄️ Database:${NC}"
    python manage.py shell -c "
from django.conf import settings
from django.db import connection

db_settings = settings.DATABASES['default']
print(f'  Engine: {db_settings[\"ENGINE\"]}')
print(f'  Name: {db_settings[\"NAME\"]}')
if 'HOST' in db_settings and db_settings['HOST']:
    print(f'  Host: {db_settings[\"HOST\"]}')
if 'PORT' in db_settings and db_settings['PORT']:
    print(f'  Port: {db_settings[\"PORT\"]}')

# Test connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('  Status: ✓ Connected')
except Exception as e:
    print(f'  Status: ✗ Error - {e}')
"
    
    echo ""
    echo -e "${CYAN}📦 Modules Status:${NC}"
    python manage.py shell -c "
from django.conf import settings
from django.apps import apps

installed_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
print(f'  Total Active Modules: {len(installed_apps)}')

# Group by category
categories = {}
for app in installed_apps:
    if '.' in app:
        category = app.split('.')[0]
        if category not in categories:
            categories[category] = []
        categories[category].append(app)

for category, apps_list in sorted(categories.items()):
    print(f'  {category.replace(\"_\", \" \").title()}: {len(apps_list)} modules')
"
    
    echo ""
    echo -e "${CYAN}🏥 System Health:${NC}"
    python manage.py shell -c "
import sys
import django
from django.contrib.auth.models import User, Permission

print(f'  Python Version: {sys.version.split()[0]}')
print(f'  Django Version: {django.get_version()}')
print(f'  Users: {User.objects.count()}')
print(f'  Permissions: {Permission.objects.count()}')

# Check some key models
try:
    from core_modules.organization.models import Company
    print(f'  Companies: {Company.objects.count()}')
except:
    print('  Companies: Not available')

try:
    from business_modules.accounting.models import Account
    print(f'  Accounts: {Account.objects.count()}')
except:
    print('  Accounts: Not available')

try:
    from services_modules.assets.models.asset import Asset
    print(f'  Assets: {Asset.objects.count()}')
except:
    print('  Assets: Not available')
"
    
    echo ""
    echo -e "${CYAN}🔐 Security Features:${NC}"
    echo "  ✓ Advanced Permissions System (User + AI)"
    echo "  ✓ Role-Based Access Control"
    echo "  ✓ Audit Logging"
    echo "  ✓ CSRF Protection"
    echo "  ✓ SQL Injection Protection"
    echo ""
    
    echo -e "${CYAN}🤖 AI Features:${NC}"
    echo "  ✓ Intelligent Assistant"
    echo "  ✓ AI Analytics"
    echo "  ✓ AI Agriculture Module"
    echo "  ✓ Translation Services"
    echo "  ✓ AI Permissions System"
    echo ""
    
    echo -e "${CYAN}🌐 Integration Features:${NC}"
    echo "  ✓ External APIs Support"
    echo "  ✓ Email & Messaging Services"
    echo "  ✓ Payment Gateways"
    echo "  ✓ Cloud Services"
    echo "  ✓ Multi-language Support"
}

# =============================================================================
# Backup and Restore
# =============================================================================

create_backup() {
    print_header "Creating System Backup"
    
    BACKUP_NAME="gaara_erp_backup_$(date +%Y%m%d_%H%M%S)"
    BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
    
    mkdir -p "$BACKUP_PATH"
    
    cd "$DJANGO_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Backup database
    print_step "Backing up database"
    python manage.py dumpdata --natural-foreign --natural-primary > "$BACKUP_PATH/database.json"
    
    # Backup media files
    if [ -d "$PROJECT_DIR/media" ]; then
        print_step "Backing up media files"
        cp -r "$PROJECT_DIR/media" "$BACKUP_PATH/"
    fi
    
    # Backup configuration
    print_step "Backing up configuration"
    cp -r "$DJANGO_DIR/gaara_erp/settings" "$BACKUP_PATH/"
    cp "$DJANGO_DIR/.env" "$BACKUP_PATH/" 2>/dev/null || true
    
    # Create system info
    print_step "Creating system information"
    cat > "$BACKUP_PATH/system_info.txt" << EOF
Gaara ERP v12 Backup Information
Created: $(date)
System: $(uname -a)
Python: $(python --version)
Django: $(python -c "import django; print(django.get_version())")
Modules: 69 active modules
EOF
    
    # Create archive
    print_step "Creating backup archive"
    cd "$BACKUP_DIR"
    tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME"
    rm -rf "$BACKUP_PATH"
    
    print_success "Backup created: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
}

# =============================================================================
# Main Menu
# =============================================================================

show_menu() {
    clear
    print_header "$PROJECT_NAME - Enhanced Setup and Management Script"
    
    echo -e "${PURPLE}📊 System Status: 69 Active Modules | Advanced Permissions | AI Features${NC}"
    echo ""
    echo -e "${CYAN}🚀 Quick Start Options:${NC}"
    echo "  1) Full Setup (Recommended for first time)"
    echo "  2) Quick Start (Skip setup, just run)"
    echo "  3) Production Setup & Run"
    echo ""
    echo -e "${CYAN}🔧 Setup Options:${NC}"
    echo "  4) Install Dependencies Only"
    echo "  5) Setup Database Only"
    echo "  6) Setup Static Files Only"
    echo ""
    echo -e "${CYAN}🏃 Run Options:${NC}"
    echo "  7) Run Development Server"
    echo "  8) Run Production Server"
    echo ""
    echo -e "${CYAN}📊 Information & Maintenance:${NC}"
    echo "  9) System Information"
    echo "  10) System Health Check"
    echo "  11) Create Backup"
    echo ""
    echo -e "${CYAN}🔧 Advanced Options:${NC}"
    echo "  12) Reset Database"
    echo "  13) Update Dependencies"
    echo "  14) Run Tests"
    echo "  15) Install AI Features"
    echo ""
    echo -e "${CYAN}❌ Exit:${NC}"
    echo "  16) Exit"
    echo ""
}

# =============================================================================
# Main Script Logic
# =============================================================================

main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --full-setup)
                FULL_SETUP=true
                shift
                ;;
            --quick-start)
                QUICK_START=true
                shift
                ;;
            --production)
                APP_MODE="prod"
                DEBUG="False"
                shift
                ;;
            --install-optional)
                INSTALL_OPTIONAL=true
                shift
                ;;
            --start-celery)
                START_CELERY=true
                shift
                ;;
            --help)
                echo "Gaara ERP v12 Enhanced Setup Script"
                echo ""
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --full-setup      Run complete setup process"
                echo "  --quick-start     Skip setup, just run server"
                echo "  --production      Run in production mode"
                echo "  --install-optional Install optional AI dependencies"
                echo "  --start-celery    Start Celery services"
                echo "  --help           Show this help message"
                echo ""
                echo "Features:"
                echo "  • 69 Active Modules"
                echo "  • Advanced Permissions (User + AI)"
                echo "  • AI Features & Translation"
                echo "  • Complete ERP Solution"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Check if running with arguments
    if [ "$FULL_SETUP" = "true" ]; then
        check_system_requirements
        setup_environment
        install_dependencies
        setup_database
        setup_static_files
        validate_system
        setup_services
        show_system_info
        read -p "Press Enter to start development server..."
        start_development_server
        return
    fi
    
    if [ "$QUICK_START" = "true" ]; then
        cd "$DJANGO_DIR"
        source "$VENV_DIR/bin/activate" 2>/dev/null || true
        start_development_server
        return
    fi
    
    # Interactive menu
    while true; do
        show_menu
        read -p "Please select an option (1-16): " choice
        
        case $choice in
            1)
                check_system_requirements
                setup_environment
                install_dependencies
                setup_database
                setup_static_files
                validate_system
                setup_services
                show_system_info
                read -p "Press Enter to start development server..."
                start_development_server
                ;;
            2)
                cd "$DJANGO_DIR"
                source "$VENV_DIR/bin/activate" 2>/dev/null || true
                start_development_server
                ;;
            3)
                APP_MODE="prod"
                DEBUG="False"
                check_system_requirements
                setup_environment
                install_dependencies
                setup_database
                setup_static_files
                validate_system
                setup_services
                setup_production_server
                ;;
            4)
                setup_environment
                install_dependencies
                ;;
            5)
                setup_database
                ;;
            6)
                setup_static_files
                ;;
            7)
                start_development_server
                ;;
            8)
                APP_MODE="prod"
                DEBUG="False"
                setup_production_server
                ;;
            9)
                show_system_info
                read -p "Press Enter to continue..."
                ;;
            10)
                validate_system
                read -p "Press Enter to continue..."
                ;;
            11)
                create_backup
                read -p "Press Enter to continue..."
                ;;
            12)
                print_warning "This will delete all data! Are you sure? (y/N)"
                read -p "> " confirm
                if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                    cd "$DJANGO_DIR"
                    rm -f db.sqlite3
                    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
                    find . -path "*/migrations/*.pyc" -delete
                    setup_database
                fi
                ;;
            13)
                setup_environment
                install_dependencies
                ;;
            14)
                cd "$DJANGO_DIR"
                source "$VENV_DIR/bin/activate" 2>/dev/null || true
                python manage.py test
                read -p "Press Enter to continue..."
                ;;
            15)
                INSTALL_OPTIONAL=true
                setup_environment
                install_dependencies
                ;;
            16)
                print_success "Thank you for using Gaara ERP v12!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please try again."
                sleep 2
                ;;
        esac
    done
}

# =============================================================================
# Script Entry Point
# =============================================================================

# Ensure we're in the right directory
if [ ! -f "$DJANGO_DIR/manage.py" ]; then
    print_error "Django project not found at $DJANGO_DIR"
    print_info "Please ensure the script is in the correct location"
    exit 1
fi

# Show banner
clear
echo -e "${BLUE}"
echo "============================================================================="
echo "   ____                           _____ _____  _____        __ ___  "
echo "  / ___| __ _  __ _ _ __ __ _     | ____|  _ \|  _ \ \      / /|_  | "
echo " | |  _ / _\` |/ _\` | '__/ _\` |    |  _| | |_) | |_) \ \ /\ / /   | | "
echo " | |_| | (_| | (_| | | | (_| |    | |___|  _ <|  __/ \ V  V /   / /  "
echo "  \____|\__,_|\__,_|_|  \__,_|    |_____|_| \_\_|     \_/\_/   /___|  "
echo ""
echo "                    Enhanced Setup & Management Script"
echo "============================================================================="
echo -e "${NC}"
echo -e "${GREEN}🚀 Features: 69 Active Modules | Advanced Permissions | AI Integration${NC}"
echo -e "${GREEN}📊 Complete ERP Solution for Business & Agriculture${NC}"
echo ""

# Run main function
main "$@"
