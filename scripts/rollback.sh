#!/bin/bash

# ============================================
# Store ERP - Rollback Script
# ============================================
# This script rolls back the Store ERP system to a previous backup
# Usage: ./scripts/rollback.sh [backup_directory]

set -e  # Exit on error

# ==================== CONFIGURATION ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUPS_DIR="$PROJECT_ROOT/backups"

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

# List available backups
list_backups() {
    print_header "Available Backups"
    
    if [ ! -d "$BACKUPS_DIR" ]; then
        print_error "No backups directory found"
        exit 1
    fi
    
    BACKUPS=($(ls -dt "$BACKUPS_DIR"/deployment_* 2>/dev/null))
    
    if [ ${#BACKUPS[@]} -eq 0 ]; then
        print_error "No backups found"
        exit 1
    fi
    
    echo "Available backups:"
    for i in "${!BACKUPS[@]}"; do
        BACKUP_NAME=$(basename "${BACKUPS[$i]}")
        BACKUP_DATE=$(echo "$BACKUP_NAME" | sed 's/deployment_//' | sed 's/_/ /')
        echo "  [$i] $BACKUP_NAME (Created: $BACKUP_DATE)"
    done
    echo ""
}

# Select backup
select_backup() {
    if [ -n "$1" ]; then
        BACKUP_DIR="$1"
        if [ ! -d "$BACKUP_DIR" ]; then
            print_error "Backup directory not found: $BACKUP_DIR"
            exit 1
        fi
    else
        list_backups
        read -p "Enter backup number to restore: " BACKUP_NUM
        
        if [ -z "$BACKUP_NUM" ] || [ "$BACKUP_NUM" -ge ${#BACKUPS[@]} ]; then
            print_error "Invalid backup number"
            exit 1
        fi
        
        BACKUP_DIR="${BACKUPS[$BACKUP_NUM]}"
    fi
    
    print_info "Selected backup: $BACKUP_DIR"
    echo ""
}

# Confirm rollback
confirm_rollback() {
    print_warning "⚠️  WARNING: This will rollback the database to a previous state"
    print_warning "⚠️  All data created after the backup will be lost"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " -r
    echo
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        print_info "Rollback cancelled"
        exit 0
    fi
}

# Create pre-rollback backup
create_pre_rollback_backup() {
    print_header "Creating Pre-Rollback Backup"
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    PRE_ROLLBACK_DIR="$BACKUPS_DIR/pre_rollback_$TIMESTAMP"
    mkdir -p "$PRE_ROLLBACK_DIR"
    
    # Backup current database
    docker-compose -f docker-compose.production.yml exec -T postgres pg_dump \
        -U "${POSTGRES_USER:-store_user}" \
        -d "${POSTGRES_DB:-store_db}" \
        > "$PRE_ROLLBACK_DIR/database_backup.sql"
    
    if [ $? -eq 0 ]; then
        gzip "$PRE_ROLLBACK_DIR/database_backup.sql"
        print_success "Pre-rollback backup created: $PRE_ROLLBACK_DIR"
    else
        print_error "Pre-rollback backup failed"
        exit 1
    fi
    
    echo ""
}

# Restore database
restore_database() {
    print_header "Restoring Database"
    
    # Find database backup file
    BACKUP_FILE=$(find "$BACKUP_DIR" -name "database_backup.sql.gz" -o -name "database_backup.sql" | head -n 1)
    
    if [ -z "$BACKUP_FILE" ]; then
        print_error "No database backup file found in $BACKUP_DIR"
        exit 1
    fi
    
    print_info "Restoring from: $BACKUP_FILE"
    
    # Decompress if needed
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        gunzip -c "$BACKUP_FILE" > /tmp/restore_backup.sql
        RESTORE_FILE="/tmp/restore_backup.sql"
    else
        RESTORE_FILE="$BACKUP_FILE"
    fi
    
    # Stop application
    print_info "Stopping application..."
    docker-compose -f docker-compose.production.yml stop backend frontend
    
    # Drop and recreate database
    print_info "Recreating database..."
    docker-compose -f docker-compose.production.yml exec -T postgres psql \
        -U "${POSTGRES_USER:-store_user}" \
        -c "DROP DATABASE IF EXISTS ${POSTGRES_DB:-store_db};"
    
    docker-compose -f docker-compose.production.yml exec -T postgres psql \
        -U "${POSTGRES_USER:-store_user}" \
        -c "CREATE DATABASE ${POSTGRES_DB:-store_db};"
    
    # Restore database
    print_info "Restoring database..."
    docker-compose -f docker-compose.production.yml exec -T postgres psql \
        -U "${POSTGRES_USER:-store_user}" \
        -d "${POSTGRES_DB:-store_db}" \
        < "$RESTORE_FILE"
    
    if [ $? -eq 0 ]; then
        print_success "Database restored successfully"
    else
        print_error "Database restore failed"
        exit 1
    fi
    
    # Cleanup
    if [ -f "/tmp/restore_backup.sql" ]; then
        rm /tmp/restore_backup.sql
    fi
    
    echo ""
}

# Restart application
restart_application() {
    print_header "Restarting Application"
    
    docker-compose -f docker-compose.production.yml up -d
    
    if [ $? -eq 0 ]; then
        print_success "Application restarted successfully"
    else
        print_error "Application restart failed"
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
    
    echo ""
}

# Show summary
show_summary() {
    print_header "Rollback Summary"
    
    echo -e "${GREEN}Rollback completed successfully!${NC}"
    echo ""
    echo "Restored from: $BACKUP_DIR"
    echo "Pre-rollback backup: $PRE_ROLLBACK_DIR"
    echo ""
    echo "Services:"
    docker-compose -f docker-compose.production.yml ps
    echo ""
}

# ==================== MAIN ====================

main() {
    cd "$PROJECT_ROOT"
    
    # Load environment variables
    if [ -f ".env.production" ]; then
        export $(cat .env.production | grep -v '^#' | xargs)
    fi
    
    select_backup "$1"
    confirm_rollback
    create_pre_rollback_backup
    restore_database
    restart_application
    health_check
    show_summary
}

# Run main function
main "$@"

