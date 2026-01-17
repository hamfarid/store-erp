#!/bin/bash
# =============================================================================
# Gaara ERP - Database Restore Script
# =============================================================================

set -euo pipefail

# Check if backup file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file.sql.gz>"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Configuration
DB_NAME="${POSTGRES_DB:-gaara_erp}"
DB_USER="${POSTGRES_USER:-gaara_admin}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

echo "WARNING: This will restore the database from backup."
echo "Database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"
read -p "Are you sure? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Restore cancelled."
    exit 1
fi

# Decompress if needed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "Decompressing backup..."
    gunzip -c "$BACKUP_FILE" > /tmp/restore.sql
    RESTORE_FILE="/tmp/restore.sql"
else
    RESTORE_FILE="$BACKUP_FILE"
fi

# Drop existing database and recreate
echo "Dropping existing database..."
PGPASSWORD="${POSTGRES_PASSWORD}" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d postgres \
    -c "DROP DATABASE IF EXISTS $DB_NAME;"

PGPASSWORD="${POSTGRES_PASSWORD}" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d postgres \
    -c "CREATE DATABASE $DB_NAME;"

# Restore database
echo "Restoring database..."
PGPASSWORD="${POSTGRES_PASSWORD}" pg_restore \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -v \
    "$RESTORE_FILE"

# Cleanup
if [[ "$BACKUP_FILE" == *.gz ]]; then
    rm -f "$RESTORE_FILE"
fi

echo "Database restored successfully!"
