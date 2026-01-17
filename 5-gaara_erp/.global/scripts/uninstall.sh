#!/bin/bash
#
# uninstall.sh - إزالة Global Guidelines
# Uninstall Global Guidelines from project
#
# Usage: ./uninstall.sh [--full]
#

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

GLOBAL_DIR=".global"
FULL_UNINSTALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --full)
            FULL_UNINSTALL=true
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

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

remove_global_dir() {
    if [ -d "$GLOBAL_DIR" ]; then
        print_info "Removing $GLOBAL_DIR directory..."
        rm -rf "$GLOBAL_DIR"
        print_success "$GLOBAL_DIR removed"
    fi
}

remove_applied_files() {
    print_warning "This will remove files that were copied from Global Guidelines:"
    echo "  - config/definitions/"
    echo "  - tools/"
    echo ""
    echo -n "Are you sure? (y/N): "
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Remove config/definitions if it looks like it came from Global
        if [ -d "config/definitions" ]; then
            if grep -q "Global Guidelines" config/definitions/*.py 2>/dev/null; then
                print_info "Removing config/definitions..."
                rm -rf config/definitions
                print_success "config/definitions removed"
            fi
        fi
        
        # Remove tools if it looks like it came from Global
        if [ -d "tools" ]; then
            if grep -q "Global Guidelines" tools/*.py 2>/dev/null; then
                print_info "Removing tools..."
                rm -rf tools
                print_success "tools removed"
            fi
        fi
    fi
}

clean_gitignore() {
    if [ -f ".gitignore" ]; then
        print_info "Cleaning .gitignore..."
        
        # Remove .global/ entry
        sed -i.bak '/^\.global\/$/d' .gitignore
        sed -i.bak '/^# Global Guidelines/d' .gitignore
        rm -f .gitignore.bak
        
        print_success ".gitignore cleaned"
    fi
}

remove_shortcuts() {
    if [ -L "GUIDELINES.txt" ]; then
        print_info "Removing shortcuts..."
        rm -f GUIDELINES.txt
        print_success "Shortcuts removed"
    fi
}

# Main
main() {
    echo -e "${RED}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║         Global Guidelines Uninstall                       ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    
    if [ ! -d "$GLOBAL_DIR" ]; then
        print_warning "Global Guidelines not found (no $GLOBAL_DIR directory)"
        exit 0
    fi
    
    if [ "$FULL_UNINSTALL" = true ]; then
        echo -e "${YELLOW}Full uninstall mode${NC}"
        echo "This will remove:"
        echo "  - $GLOBAL_DIR directory"
        echo "  - Applied files (config, tools)"
        echo "  - .gitignore entries"
        echo "  - Shortcuts"
        echo ""
    else
        echo "This will remove:"
        echo "  - $GLOBAL_DIR directory"
        echo "  - .gitignore entries"
        echo "  - Shortcuts"
        echo ""
        echo "Applied files (config, tools) will NOT be removed"
        echo "Use --full flag for complete removal"
        echo ""
    fi
    
    echo -n "Continue? (y/N): "
    read -r response
    
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Uninstall cancelled"
        exit 0
    fi
    
    echo ""
    
    remove_global_dir
    clean_gitignore
    remove_shortcuts
    
    if [ "$FULL_UNINSTALL" = true ]; then
        remove_applied_files
    fi
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║  ✓ Global Guidelines uninstalled                          ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    if [ "$FULL_UNINSTALL" = false ]; then
        print_info "Applied files were kept. Remove manually if needed:"
        echo "  - config/definitions/"
        echo "  - tools/"
    fi
    
    echo ""
}

main "$@"

