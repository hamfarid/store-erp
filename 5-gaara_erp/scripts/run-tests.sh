#!/bin/bash
# =============================================================================
# Gaara ERP - Test Runner Script
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Gaara ERP - Test Suite"
echo "=========================================="

# Default test settings
TEST_MODULE="${1:-}"
COVERAGE="${COVERAGE:-false}"
VERBOSE="${VERBOSE:-2}"
PARALLEL="${PARALLEL:-false}"

# Check if running in Docker
if [ -f "/.dockerenv" ]; then
    echo "Running in Docker container"
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Run with coverage if requested
if [ "$COVERAGE" = "true" ]; then
    echo "Running tests with coverage..."
    $PYTHON_CMD -m pytest \
        --cov=gaara_erp \
        --cov-report=html \
        --cov-report=term \
        --cov-report=xml \
        -v \
        ${TEST_MODULE}

    echo ""
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
else
    # Run tests
    if [ -n "$TEST_MODULE" ]; then
        echo "Running tests for: $TEST_MODULE"
        $PYTHON_CMD -m pytest -v "$TEST_MODULE"
    else
        echo "Running all tests..."
        $PYTHON_CMD -m pytest -v
    fi
fi

echo ""
echo -e "${GREEN}✓ Tests completed!${NC}"
