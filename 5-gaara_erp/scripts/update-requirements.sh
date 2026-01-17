#!/bin/bash
# =============================================================================
# Gaara ERP - Update Requirements Script
# =============================================================================
# Combines base, dev, prod, and test requirements
# =============================================================================

set -euo pipefail

echo "=========================================="
echo "Gaara ERP - Update Requirements"
echo "=========================================="

# Combine all requirements
echo ""
echo "Combining requirements files..."

# Start with base
cat gaara_erp/requirements-base.txt > gaara_erp/requirements.txt
echo "" >> gaara_erp/requirements.txt
echo "# Development dependencies (install with: pip install -r requirements-dev.txt)" >> gaara_erp/requirements.txt
echo "# Production dependencies (install with: pip install -r requirements-prod.txt)" >> gaara_erp/requirements.txt
echo "# Test dependencies (install with: pip install -r requirements-test.txt)" >> gaara_erp/requirements.txt

# Add production dependencies
if [ -f "gaara_erp/requirements-prod.txt" ]; then
    echo "" >> gaara_erp/requirements.txt
    echo "# Production dependencies" >> gaara_erp/requirements.txt
    cat gaara_erp/requirements-prod.txt >> gaara_erp/requirements.txt
fi

echo ""
echo "✓ Requirements file updated"
echo ""
echo "To install:"
echo "  Base:        pip install -r gaara_erp/requirements-base.txt"
echo "  Development: pip install -r gaara_erp/requirements-base.txt -r gaara_erp/requirements-dev.txt"
echo "  Production:  pip install -r gaara_erp/requirements-base.txt -r gaara_erp/requirements-prod.txt"
echo "  Testing:     pip install -r gaara_erp/requirements-base.txt -r gaara_erp/requirements-test.txt"
echo ""
