#!/bin/bash
# =============================================================================
# Gaara ERP - Docker Health Check Script
# =============================================================================

set -euo pipefail

# Check if backend is responding
if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "Backend health check: OK"
    exit 0
else
    echo "Backend health check: FAILED"
    exit 1
fi
