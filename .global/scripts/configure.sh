#!/bin/bash
#
# configure.sh - تكوين مكونات Global Guidelines
# Configure Global Guidelines components
#
# Usage: ./configure.sh
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

CONFIG_FILE=".global/config.json"

print_header() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║       Global Guidelines Configuration                      ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

print_component() {
    local enabled=$1
    local name=$2
    local description=$3
    
    if [ "$enabled" = "true" ]; then
        echo -e "${GREEN}[✓]${NC} $name - $description"
    else
        echo -e "[ ] $name - $description"
    fi
}

# Initialize default configuration
init_config() {
    cat > "$CONFIG_FILE" << EOF
{
  "version": "1.0.0",
  "components": {
    "config": true,
    "tools": true,
    "templates": false,
    "examples": false,
    "scripts": true,
    "flows": true
  }
}
EOF
}

# Interactive configuration
configure_interactive() {
    print_header
    
    echo "Select components to integrate:"
    echo ""
    echo "1. config/definitions - Type definitions and constants"
    echo "2. tools/ - Development tools (analyze, detect, merge, update)"
    echo "3. templates/ - Project templates"
    echo "4. examples/ - Code examples"
    echo "5. scripts/ - Helper scripts"
    echo "6. flows/ - Workflow documentation"
    echo ""
    echo "Enter numbers separated by spaces (e.g., 1 2 5)"
    echo "Or press ENTER for default (1 2 5 6):"
    echo ""
    read -r selection
    
    # Default selection
    if [ -z "$selection" ]; then
        selection="1 2 5 6"
    fi
    
    # Reset all to false
    config_enabled=false
    tools_enabled=false
    templates_enabled=false
    examples_enabled=false
    scripts_enabled=false
    flows_enabled=false
    
    # Enable selected components
    for num in $selection; do
        case $num in
            1) config_enabled=true ;;
            2) tools_enabled=true ;;
            3) templates_enabled=true ;;
            4) examples_enabled=true ;;
            5) scripts_enabled=true ;;
            6) flows_enabled=true ;;
        esac
    done
    
    # Save configuration
    cat > "$CONFIG_FILE" << EOF
{
  "version": "1.0.0",
  "components": {
    "config": $config_enabled,
    "tools": $tools_enabled,
    "templates": $templates_enabled,
    "examples": $examples_enabled,
    "scripts": $scripts_enabled,
    "flows": $flows_enabled
  }
}
EOF
    
    # Show summary
    echo ""
    echo -e "${GREEN}Configuration saved!${NC}"
    echo ""
    echo "Selected components:"
    echo ""
    print_component "$config_enabled" "config/definitions" "Type definitions"
    print_component "$tools_enabled" "tools/" "Development tools"
    print_component "$templates_enabled" "templates/" "Project templates"
    print_component "$examples_enabled" "examples/" "Code examples"
    print_component "$scripts_enabled" "scripts/" "Helper scripts"
    print_component "$flows_enabled" "flows/" "Workflow docs"
    echo ""
    echo -e "${YELLOW}Next step:${NC} Run .global/scripts/apply.sh to apply configuration"
    echo ""
}

# Main
main() {
    if [ ! -d ".global" ]; then
        echo "Error: .global/ directory not found"
        echo "Please run integrate.sh first"
        exit 1
    fi
    
    configure_interactive
}

main "$@"

