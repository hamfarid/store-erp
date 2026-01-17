#!/bin/bash
# =============================================================================
# Gaara ERP - Database Backup Script
# =============================================================================

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="${POSTGRES_DB:-gaara_erp}"
DB_USER="${POSTGRES_USER:-gaara_admin}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup filename
BACKUP_FILE="$BACKUP_DIR/gaara_erp_backup_$TIMESTAMP.sql"

echo "Starting database backup..."
echo "Database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"

# Perform backup
PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -F c \
    -f "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"
BACKUP_FILE="${BACKUP_FILE}.gz"

echo "Backup completed: $BACKUP_FILE"
echo "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "gaara_erp_backup_*.sql.gz" -mtime +7 -delete

echo "Old backups cleaned up (keeping last 7 days)"
