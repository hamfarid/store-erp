#!/bin/bash
# =============================================================================
# P0.23: Software Bill of Materials (SBOM) Generation Script
# =============================================================================
# FILE: scripts/generate-sbom.sh
# PURPOSE: Generate SBOM for the Store Management System
# USAGE: ./scripts/generate-sbom.sh [format]
# FORMATS: cyclonedx (default), spdx
# =============================================================================

set -e

# Configuration
PROJECT_NAME="store-management-system"
VERSION="${VERSION:-$(git describe --tags --always 2>/dev/null || echo 'dev')}"
OUTPUT_DIR="./sbom"
FORMAT="${1:-cyclonedx}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== P0.23: SBOM Generation ===${NC}"
echo "Project: $PROJECT_NAME"
echo "Version: $VERSION"
echo "Format: $FORMAT"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check for required tools
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${YELLOW}Warning: $1 not found. Installing...${NC}"
        return 1
    fi
    return 0
}

# Generate Python SBOM using pip-audit or cyclonedx-py
generate_python_sbom() {
    echo -e "\n${GREEN}Generating Python SBOM...${NC}"
    
    if check_tool "cyclonedx-py"; then
        echo "Using cyclonedx-py..."
        if [ "$FORMAT" == "cyclonedx" ]; then
            cyclonedx-py requirements \
                -i backend/requirements.txt \
                -o "$OUTPUT_DIR/python-sbom.json" \
                --format json
        else
            cyclonedx-py requirements \
                -i backend/requirements.txt \
                -o "$OUTPUT_DIR/python-sbom.xml" \
                --format xml
        fi
    elif check_tool "pip-audit"; then
        echo "Using pip-audit..."
        pip-audit -r backend/requirements.txt \
            --format cyclonedx-json \
            -o "$OUTPUT_DIR/python-sbom.json" 2>/dev/null || true
    else
        echo -e "${YELLOW}Installing cyclonedx-bom...${NC}"
        pip install cyclonedx-bom
        cyclonedx-py requirements \
            -i backend/requirements.txt \
            -o "$OUTPUT_DIR/python-sbom.json" \
            --format json
    fi
    
    echo -e "${GREEN}✓ Python SBOM generated${NC}"
}

# Generate JavaScript SBOM if frontend exists
generate_js_sbom() {
    if [ -f "frontend/package.json" ]; then
        echo -e "\n${GREEN}Generating JavaScript SBOM...${NC}"
        
        if check_tool "cyclonedx-npm"; then
            cd frontend
            cyclonedx-npm --output-file "../$OUTPUT_DIR/js-sbom.json" --output-format json
            cd ..
        elif check_tool "npx"; then
            cd frontend
            npx @cyclonedx/cyclonedx-npm --output-file "../$OUTPUT_DIR/js-sbom.json"
            cd ..
        else
            echo -e "${YELLOW}Skipping JS SBOM - cyclonedx-npm not available${NC}"
            return 0
        fi
        
        echo -e "${GREEN}✓ JavaScript SBOM generated${NC}"
    fi
}

# Generate Docker SBOM using syft
generate_docker_sbom() {
    echo -e "\n${GREEN}Generating Docker SBOM...${NC}"
    
    if check_tool "syft"; then
        # Scan backend Dockerfile
        if [ -f "backend/Dockerfile" ]; then
            syft dir:backend \
                -o "$FORMAT-json=$OUTPUT_DIR/docker-backend-sbom.json" \
                --config .syft.yaml 2>/dev/null || \
            syft dir:backend \
                -o json="$OUTPUT_DIR/docker-backend-sbom.json"
        fi
        
        # Scan frontend if exists
        if [ -f "frontend/Dockerfile" ]; then
            syft dir:frontend \
                -o json="$OUTPUT_DIR/docker-frontend-sbom.json"
        fi
        
        echo -e "${GREEN}✓ Docker SBOM generated${NC}"
    else
        echo -e "${YELLOW}Skipping Docker SBOM - syft not installed${NC}"
        echo "Install with: curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s"
    fi
}

# Merge SBOMs into a single file
merge_sboms() {
    echo -e "\n${GREEN}Creating combined SBOM...${NC}"
    
    # Create a simple combined manifest
    cat > "$OUTPUT_DIR/sbom-manifest.json" << EOF
{
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "version": 1,
    "metadata": {
        "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
        "component": {
            "type": "application",
            "name": "$PROJECT_NAME",
            "version": "$VERSION"
        },
        "tools": [
            {"name": "sbom-generator", "version": "1.0.0"}
        ]
    },
    "components_files": [
        "python-sbom.json",
        "js-sbom.json",
        "docker-backend-sbom.json"
    ]
}
EOF
    
    echo -e "${GREEN}✓ SBOM manifest created${NC}"
}

# Verify SBOMs
verify_sboms() {
    echo -e "\n${GREEN}Verifying SBOMs...${NC}"
    
    if check_tool "jq"; then
        for file in "$OUTPUT_DIR"/*.json; do
            if [ -f "$file" ]; then
                if jq empty "$file" 2>/dev/null; then
                    echo -e "  ${GREEN}✓${NC} $(basename $file) - Valid JSON"
                else
                    echo -e "  ${RED}✗${NC} $(basename $file) - Invalid JSON"
                fi
            fi
        done
    else
        echo -e "${YELLOW}jq not installed - skipping validation${NC}"
    fi
}

# Main execution
main() {
    echo -e "\n${GREEN}Starting SBOM generation...${NC}\n"
    
    generate_python_sbom
    generate_js_sbom
    generate_docker_sbom
    merge_sboms
    verify_sboms
    
    echo -e "\n${GREEN}=== SBOM Generation Complete ===${NC}"
    echo "Output directory: $OUTPUT_DIR"
    echo ""
    ls -la "$OUTPUT_DIR"
}

main "$@"

