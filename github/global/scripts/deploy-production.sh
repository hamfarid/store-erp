#!/bin/bash

# ============================================
# Store ERP - Production Deployment Script
# ============================================
# This script deploys the Store ERP system to production
# Usage: ./scripts/deploy-production.sh [options]
# Options:
#   --build-only    Build images without deploying
#   --no-backup     Skip database backup
#   --force         Force deployment without confirmation

set -e  # Exit on error

# ==================== CONFIGURATION ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$PROJECT_ROOT/backups/deployment_$TIMESTAMP"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==================== FUNCTIONS ====================

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
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

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    # Check .env.production file
    if [ ! -f "$PROJECT_ROOT/.env.production" ]; then
        print_error ".env.production file not found"
        print_info "Copy .env.production.example to .env.production and fill in the values"
        exit 1
    fi
    print_success ".env.production file exists"
    
    echo ""
}

# Load environment variables
load_env() {
    print_header "Loading Environment Variables"
    
    if [ -f "$PROJECT_ROOT/.env.production" ]; then
        export $(cat "$PROJECT_ROOT/.env.production" | grep -v '^#' | xargs)
        print_success "Environment variables loaded"
    else
        print_error "Failed to load environment variables"
        exit 1
    fi
    
    echo ""
}

# Backup database
backup_database() {
    if [ "$SKIP_BACKUP" = true ]; then
        print_warning "Skipping database backup"
        return
    fi
    
    print_header "Backing Up Database"
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup PostgreSQL
    docker-compose -f docker-compose.production.yml exec -T postgres pg_dump \
        -U "${POSTGRES_USER:-store_user}" \
        -d "${POSTGRES_DB:-store_db}" \
        > "$BACKUP_DIR/database_backup.sql"
    
    if [ $? -eq 0 ]; then
        print_success "Database backup created: $BACKUP_DIR/database_backup.sql"
    else
        print_error "Database backup failed"
        exit 1
    fi
    
    # Compress backup
    gzip "$BACKUP_DIR/database_backup.sql"
    print_success "Backup compressed: $BACKUP_DIR/database_backup.sql.gz"
    
    echo ""
}

# Build Docker images
build_images() {
    print_header "Building Docker Images"
    
    cd "$PROJECT_ROOT"
    
    # Set build arguments
    export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    export VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    
    # Build images
    docker-compose -f docker-compose.production.yml build \
        --build-arg BUILD_DATE="$BUILD_DATE" \
        --build-arg VERSION="${VERSION:-1.0.0}" \
        --build-arg VCS_REF="$VCS_REF"
    
    if [ $? -eq 0 ]; then
        print_success "Docker images built successfully"
    else
        print_error "Docker image build failed"
        exit 1
    fi
    
    echo ""
}

# Run database migrations
run_migrations() {
    print_header "Running Database Migrations"
    
    docker-compose -f docker-compose.production.yml exec -T backend \
        flask db upgrade
    
    if [ $? -eq 0 ]; then
        print_success "Database migrations completed"
    else
        print_error "Database migrations failed"
        exit 1
    fi
    
    echo ""
}

# Deploy application
deploy_application() {
    print_header "Deploying Application"
    
    cd "$PROJECT_ROOT"
    
    # Stop existing containers
    print_info "Stopping existing containers..."
    docker-compose -f docker-compose.production.yml down
    
    # Start new containers
    print_info "Starting new containers..."
    docker-compose -f docker-compose.production.yml up -d
    
    if [ $? -eq 0 ]; then
        print_success "Application deployed successfully"
    else
        print_error "Application deployment failed"
        exit 1
    fi
    
    echo ""
}

# Health check
health_check() {
    print_header "Running Health Checks"
    
    # Wait for services to start
    print_info "Waiting for services to start (30 seconds)..."
    sleep 30
    
    # Check backend health
    print_info "Checking backend health..."
    BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${BACKEND_PORT:-5000}/health)
    
    if [ "$BACKEND_HEALTH" = "200" ]; then
        print_success "Backend is healthy"
    else
        print_error "Backend health check failed (HTTP $BACKEND_HEALTH)"
        exit 1
    fi
    
    # Check frontend health
    print_info "Checking frontend health..."
    FRONTEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${FRONTEND_PORT:-80}/)
    
    if [ "$FRONTEND_HEALTH" = "200" ]; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend health check failed (HTTP $FRONTEND_HEALTH)"
        exit 1
    fi
    
    # Check database connection
    print_info "Checking database connection..."
    docker-compose -f docker-compose.production.yml exec -T postgres \
        pg_isready -U "${POSTGRES_USER:-store_user}" -d "${POSTGRES_DB:-store_db}" > /dev/null
    
    if [ $? -eq 0 ]; then
        print_success "Database is healthy"
    else
        print_error "Database health check failed"
        exit 1
    fi
    
    echo ""
}

# Show deployment summary
show_summary() {
    print_header "Deployment Summary"
    
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo ""
    echo "Services:"
    docker-compose -f docker-compose.production.yml ps
    echo ""
    echo "Access URLs:"
    echo "  Frontend: http://localhost:${FRONTEND_PORT:-80}"
    echo "  Backend:  http://localhost:${BACKEND_PORT:-5000}"
    echo "  API Docs: http://localhost:${BACKEND_PORT:-5000}/api/docs"
    echo ""
    echo "Logs:"
    echo "  View logs: docker-compose -f docker-compose.production.yml logs -f"
    echo "  Backend:   docker-compose -f docker-compose.production.yml logs -f backend"
    echo "  Frontend:  docker-compose -f docker-compose.production.yml logs -f frontend"
    echo ""
    echo "Backup:"
    echo "  Location: $BACKUP_DIR"
    echo ""
}

# ==================== MAIN ====================

main() {
    # Parse arguments
    BUILD_ONLY=false
    SKIP_BACKUP=false
    FORCE=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --build-only)
                BUILD_ONLY=true
                shift
                ;;
            --no-backup)
                SKIP_BACKUP=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Usage: $0 [--build-only] [--no-backup] [--force]"
                exit 1
                ;;
        esac
    done
    
    # Confirmation
    if [ "$FORCE" != true ]; then
        print_warning "This will deploy the application to production"
        read -p "Are you sure you want to continue? (yes/no): " -r
        echo
        if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            print_info "Deployment cancelled"
            exit 0
        fi
    fi
    
    # Run deployment steps
    check_root
    check_prerequisites
    load_env
    
    if [ "$BUILD_ONLY" = true ]; then
        build_images
        print_success "Build completed successfully"
        exit 0
    fi
    
    backup_database
    build_images
    deploy_application
    run_migrations
    health_check
    show_summary
}

# Run main function
main "$@"

