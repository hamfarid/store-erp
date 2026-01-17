#!/bin/bash
# =============================================================================
# Gaara ERP - Complete Backup Script
# =============================================================================
# Backs up database, media files, and configuration
# =============================================================================

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="gaara_erp_backup_$TIMESTAMP"

echo "=========================================="
echo "Gaara ERP - Complete Backup"
echo "=========================================="

# Create backup directory
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

# Database backup
echo ""
echo "Backing up database..."
if [ -f "docker/database-backup.sh" ]; then
    ./docker/database-backup.sh
    # Move backup to backup directory
    mv backups/gaara_erp_backup_*.sql.gz "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true
else
    echo "Warning: Database backup script not found"
fi

# Media files backup
echo ""
echo "Backing up media files..."
if [ -d "gaara_erp/media" ]; then
    tar -czf "$BACKUP_DIR/$BACKUP_NAME/media.tar.gz" -C gaara_erp media/
    echo "✓ Media files backed up"
else
    echo "Warning: Media directory not found"
fi

# Configuration backup
echo ""
echo "Backing up configuration..."
if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/$BACKUP_NAME/.env.backup"
    echo "✓ Configuration backed up"
fi

# Docker volumes backup (if using Docker)
if command -v docker &> /dev/null; then
    echo ""
    echo "Backing up Docker volumes..."
    docker run --rm \
        -v gaara_erp_postgres_data:/data \
        -v "$(pwd)/$BACKUP_DIR/$BACKUP_NAME":/backup \
        alpine tar czf /backup/postgres_data.tar.gz -C /data . 2>/dev/null || echo "Warning: Could not backup postgres volume"
fi

# Create backup manifest
echo ""
echo "Creating backup manifest..."
cat > "$BACKUP_DIR/$BACKUP_NAME/manifest.txt" << EOF
Gaara ERP Backup Manifest
========================
Date: $(date)
Backup Name: $BACKUP_NAME
Version: 1.0.0

Contents:
- Database backup (if available)
- Media files
- Configuration files
- Docker volumes (if available)

To restore:
1. Extract media files: tar -xzf media.tar.gz
2. Restore database: ./docker/database-restore.sh <backup_file>
3. Restore configuration: cp .env.backup .env
EOF

# Compress entire backup
echo ""
echo "Compressing backup..."
cd "$BACKUP_DIR"
tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"
cd ..

echo ""
echo "=========================================="
echo "Backup completed: $BACKUP_DIR/${BACKUP_NAME}.tar.gz"
echo "=========================================="
du -h "$BACKUP_DIR/${BACKUP_NAME}.tar.gz"
