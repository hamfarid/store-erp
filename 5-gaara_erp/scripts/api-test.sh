#!/bin/bash
# =============================================================================
# Gaara ERP - API Testing Script
# =============================================================================
# Tests API endpoints using curl
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="${API_URL:-http://localhost:8000}"
API_BASE="${BASE_URL}/api"

echo "=========================================="
echo "Gaara ERP - API Testing"
echo "=========================================="
echo "Base URL: $BASE_URL"
echo ""

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=${3:-200}
    local data=${4:-""}
    local token=${5:-""}

    local url="${API_BASE}${endpoint}"
    local headers=()

    if [ -n "$token" ]; then
        headers+=("-H" "Authorization: Bearer $token")
    fi

    if [ -n "$data" ]; then
        headers+=("-H" "Content-Type: application/json")
        headers+=("-d" "$data")
    fi

    echo -n "Testing $method $endpoint... "

    local response
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "$url" "${headers[@]}")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$url" "${headers[@]}")
    elif [ "$method" = "PUT" ]; then
        response=$(curl -s -w "\n%{http_code}" -X PUT "$url" "${headers[@]}")
    elif [ "$method" = "DELETE" ]; then
        response=$(curl -s -w "\n%{http_code}" -X DELETE "$url" "${headers[@]}")
    fi

    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $http_code)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $http_code)"
        echo "Response: $body"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Health check
echo "1. Health Check"
test_endpoint "GET" "" 200 "" "" "/health/"

# Test authentication
echo ""
echo "2. Authentication"
test_endpoint "POST" "/auth/users/" 201 '{"email":"test@example.com","password":"testpass123","first_name":"Test","last_name":"User"}'

# Test login (if user exists)
echo ""
echo "3. Login"
LOGIN_RESPONSE=$(curl -s -X POST "${API_BASE}/auth/jwt/create/" \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"testpass123"}')

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access":"[^"]*' | cut -d'"' -f4 || echo "")

if [ -n "$ACCESS_TOKEN" ]; then
    echo -e "${GREEN}✓ Login successful${NC}"

    # Test authenticated endpoints
    echo ""
    echo "4. Authenticated Endpoints"
    test_endpoint "GET" "/users/" 200 "" "$ACCESS_TOKEN"
    test_endpoint "GET" "/dashboard/stats/" 200 "" "$ACCESS_TOKEN"
else
    echo -e "${YELLOW}⚠ Login failed, skipping authenticated tests${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
