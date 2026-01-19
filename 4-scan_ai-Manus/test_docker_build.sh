#!/bin/bash
# ==========================================
# Test Docker Build Script
# Path: /home/ubuntu/gaara_scan_ai/test_docker_build.sh
# ==========================================

set -e

echo "=== اختبار بناء ملفات Docker ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_dockerfile() {
    local dockerfile=$1
    local context=$2
    local name=$3
    
    echo -e "${YELLOW}اختبار: ${name}${NC}"
    echo "  الملف: ${dockerfile}"
    echo "  السياق: ${context}"
    
    # Check if Dockerfile exists
    if [ ! -f "${dockerfile}" ]; then
        echo -e "  ${RED}✗ الملف غير موجود${NC}"
        return 1
    fi
    
    # Check basic syntax
    if grep -q "^FROM" "${dockerfile}"; then
        echo -e "  ${GREEN}✓ البنية الأساسية صحيحة${NC}"
    else
        echo -e "  ${RED}✗ البنية الأساسية غير صحيحة${NC}"
        return 1
    fi
    
    # Check for WORKDIR
    if grep -q "WORKDIR" "${dockerfile}"; then
        echo -e "  ${GREEN}✓ يحتوي على WORKDIR${NC}"
    else
        echo -e "  ${YELLOW}⚠ لا يحتوي على WORKDIR${NC}"
    fi
    
    # Check for EXPOSE
    if grep -q "EXPOSE" "${dockerfile}"; then
        echo -e "  ${GREEN}✓ يحتوي على EXPOSE${NC}"
    else
        echo -e "  ${YELLOW}⚠ لا يحتوي على EXPOSE${NC}"
    fi
    
    # Check for HEALTHCHECK
    if grep -q "HEALTHCHECK" "${dockerfile}"; then
        echo -e "  ${GREEN}✓ يحتوي على HEALTHCHECK${NC}"
    else
        echo -e "  ${YELLOW}⚠ لا يحتوي على HEALTHCHECK${NC}"
    fi
    
    echo ""
    return 0
}

# Test docker-compose.yml syntax
test_compose() {
    local compose_file=$1
    local name=$2
    
    echo -e "${YELLOW}اختبار: ${name}${NC}"
    echo "  الملف: ${compose_file}"
    
    if [ ! -f "${compose_file}" ]; then
        echo -e "  ${RED}✗ الملف غير موجود${NC}"
        return 1
    fi
    
    # Check YAML syntax with Python
    if python3 -c "import yaml; yaml.safe_load(open('${compose_file}'))" 2>/dev/null; then
        echo -e "  ${GREEN}✓ بنية YAML صحيحة${NC}"
    else
        echo -e "  ${RED}✗ بنية YAML غير صحيحة${NC}"
        return 1
    fi
    
    # Check for required fields
    if grep -q "services:" "${compose_file}"; then
        echo -e "  ${GREEN}✓ يحتوي على services${NC}"
    else
        echo -e "  ${RED}✗ لا يحتوي على services${NC}"
        return 1
    fi
    
    echo ""
    return 0
}

# Main tests
echo "=== اختبار ملفات Dockerfile ==="
echo ""

test_dockerfile "backend/Dockerfile" "backend" "Backend Dockerfile"
test_dockerfile "frontend/Dockerfile" "frontend" "Frontend Dockerfile"

echo "=== اختبار ملفات docker-compose.yml ==="
echo ""

test_compose "docker-compose.yml" "Main Docker Compose"
test_compose "docker/docker-compose.yml" "Docker Folder Compose"

echo "=== ملخص الاختبار ==="
echo -e "${GREEN}✓ اكتملت جميع الاختبارات${NC}"
