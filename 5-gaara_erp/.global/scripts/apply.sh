#!/bin/bash
#
# apply.sh - تطبيق مكونات Global Guidelines على المشروع
# Apply Global Guidelines components to project
#
# Usage: ./apply.sh [--only component] [--backup]
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

CONFIG_FILE=".global/config.json"
BACKUP_DIR=".global_backup_$(date +%Y%m%d_%H%M%S)"

# Parse arguments
ONLY_COMPONENT=""
CREATE_BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --only)
            ONLY_COMPONENT="$2"
            shift 2
            ;;
        --backup)
            CREATE_BACKUP=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if component is enabled
is_enabled() {
    local component=$1
    
    if [ ! -f "$CONFIG_FILE" ]; then
        return 0  # If no config, apply all
    fi
    
    # Simple JSON parsing (requires jq or python)
    if command -v jq &> /dev/null; then
        enabled=$(jq -r ".components.$component" "$CONFIG_FILE")
        [ "$enabled" = "true" ]
    elif command -v python3 &> /dev/null; then
        enabled=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['components']['$component'])")
        [ "$enabled" = "True" ]
    else
        return 0  # If no parser, apply all
    fi
}

# Create backup
create_backup() {
    if [ "$CREATE_BACKUP" = true ]; then
        print_info "Creating backup in $BACKUP_DIR..."
        mkdir -p "$BACKUP_DIR"
        
        # Backup existing files that will be overwritten
        [ -d "config" ] && cp -r config "$BACKUP_DIR/" 2>/dev/null || true
        [ -d "tools" ] && cp -r tools "$BACKUP_DIR/" 2>/dev/null || true
        
        print_success "Backup created"
    fi
}

# Apply config/definitions
apply_config() {
    if [ -n "$ONLY_COMPONENT" ] && [ "$ONLY_COMPONENT" != "config" ]; then
        return
    fi
    
    if ! is_enabled "config"; then
        return
    fi
    
    print_info "Applying config/definitions..."
    
    # Create directories
    mkdir -p config/definitions
    
    # Copy files
    if [ -d ".global/templates/config" ]; then
        cp .global/templates/config/ports.py config/ 2>/dev/null || true
        cp .global/templates/config/definitions/*.py config/definitions/ 2>/dev/null || true
        
        # Create __init__.py if not exists
        if [ ! -f "config/__init__.py" ]; then
            touch config/__init__.py
        fi
        
        print_success "config/definitions applied"
    else
        print_warning "config templates not found in .global/"
    fi
}

# Apply tools
apply_tools() {
    if [ -n "$ONLY_COMPONENT" ] && [ "$ONLY_COMPONENT" != "tools" ]; then
        return
    fi
    
    if ! is_enabled "tools"; then
        return
    fi
    
    print_info "Applying tools..."
    
    # Create directory
    mkdir -p tools
    
    # Copy tools
    if [ -d ".global/tools" ]; then
        cp .global/tools/*.py tools/ 2>/dev/null || true
        
        # Create __init__.py if not exists
        if [ ! -f "tools/__init__.py" ]; then
            touch tools/__init__.py
        fi
        
        print_success "tools/ applied"
    else
        print_warning "tools not found in .global/"
    fi
}

# Apply templates
apply_templates() {
    if [ -n "$ONLY_COMPONENT" ] && [ "$ONLY_COMPONENT" != "templates" ]; then
        return
    fi
    
    if ! is_enabled "templates"; then
        return
    fi
    
    print_info "Templates are available in .global/templates/"
    print_info "Copy them manually as needed"
}

# Apply examples
apply_examples() {
    if [ -n "$ONLY_COMPONENT" ] && [ "$ONLY_COMPONENT" != "examples" ]; then
        return
    fi
    
    if ! is_enabled "examples"; then
        return
    fi
    
    print_info "Examples are available in .global/examples/"
    print_info "Copy them manually as needed"
}

# Apply scripts
apply_scripts() {
    if [ -n "$ONLY_COMPONENT" ] && [ "$ONLY_COMPONENT" != "scripts" ]; then
        return
    fi
    
    if ! is_enabled "scripts"; then
        return
    fi
    
    print_info "Scripts are available in .global/scripts/"
    print_success "Scripts ready to use"
}

# Apply flows
apply_flows() {
    if [ -n "$ONLY_COMPONENT" ] && [ "$ONLY_COMPONENT" != "flows" ]; then
        return
    fi
    
    if ! is_enabled "flows"; then
        return
    fi
    
    print_info "Flows are available in .global/flows/"
    print_success "Flows ready to read"
}

# Print summary
print_summary() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║  ✓ Components applied successfully!                       ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}What was applied:${NC}"
    echo ""
    
    is_enabled "config" && echo "  ✓ config/definitions - Type definitions copied"
    is_enabled "tools" && echo "  ✓ tools/ - Development tools copied"
    is_enabled "templates" && echo "  ✓ templates/ - Available in .global/templates/"
    is_enabled "examples" && echo "  ✓ examples/ - Available in .global/examples/"
    is_enabled "scripts" && echo "  ✓ scripts/ - Available in .global/scripts/"
    is_enabled "flows" && echo "  ✓ flows/ - Available in .global/flows/"
    
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo ""
    echo "  1. Review the applied files:"
    echo "     - config/definitions/"
    echo "     - tools/"
    echo ""
    echo "  2. Read the integration flow:"
    echo "     cat .global/flows/INTEGRATION_FLOW.md"
    echo ""
    echo "  3. Start using the tools:"
    echo "     python tools/analyze_dependencies.py ."
    echo ""
    
    if [ "$CREATE_BACKUP" = true ]; then
        echo "  Backup saved in: $BACKUP_DIR"
        echo ""
    fi
}

# Main
main() {
    if [ ! -d ".global" ]; then
        print_error ".global/ directory not found"
        echo "Please run integrate.sh first"
        exit 1
    fi
    
    echo -e "${BLUE}Applying Global Guidelines components...${NC}"
    echo ""
    
    create_backup
    apply_config
    apply_tools
    apply_templates
    apply_examples
    apply_scripts
    apply_flows
    
    print_summary
}

main "$@"

