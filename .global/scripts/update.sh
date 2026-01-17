#!/bin/bash
#
# update.sh - تحديث Global Guidelines
# Update Global Guidelines to latest version
#
# Usage: ./update.sh [--version VERSION]
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

GLOBAL_DIR=".global"
REPO_URL="https://github.com/hamfarid/global"
BRANCH="main"
TARGET_VERSION=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --version)
            TARGET_VERSION="$2"
            shift 2
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

get_current_version() {
    if [ -f "$GLOBAL_DIR/VERSION" ]; then
        cat "$GLOBAL_DIR/VERSION"
    else
        echo "unknown"
    fi
}

update_global() {
    print_info "Updating Global Guidelines..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    
    # Clone repository
    if [ -n "$TARGET_VERSION" ]; then
        print_info "Downloading version $TARGET_VERSION..."
        git clone --depth 1 --branch "v$TARGET_VERSION" "$REPO_URL" "$TEMP_DIR" > /dev/null 2>&1
    else
        print_info "Downloading latest version..."
        git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TEMP_DIR" > /dev/null 2>&1
    fi
    
    # Backup config.json if exists
    if [ -f "$GLOBAL_DIR/config.json" ]; then
        cp "$GLOBAL_DIR/config.json" "$TEMP_DIR/config.json.backup"
    fi
    
    # Remove old .global (except config)
    rm -rf "$GLOBAL_DIR"
    
    # Copy new files
    cp -r "$TEMP_DIR" "$GLOBAL_DIR"
    
    # Remove .git directory
    rm -rf "$GLOBAL_DIR/.git"
    
    # Restore config if exists
    if [ -f "$GLOBAL_DIR/config.json.backup" ]; then
        mv "$GLOBAL_DIR/config.json.backup" "$GLOBAL_DIR/config.json"
    fi
    
    # Clean up
    rm -rf "$TEMP_DIR"
    
    print_success "Global Guidelines updated successfully"
}

show_changelog() {
    print_info "Recent changes:"
    echo ""
    
    if [ -f "$GLOBAL_DIR/CHANGELOG.md" ]; then
        head -n 30 "$GLOBAL_DIR/CHANGELOG.md"
    else
        echo "No changelog available"
    fi
}

# Main
main() {
    if [ ! -d "$GLOBAL_DIR" ]; then
        echo "Error: .global/ directory not found"
        echo "Please run integrate.sh first"
        exit 1
    fi
    
    current_version=$(get_current_version)
    
    echo -e "${BLUE}Current version: $current_version${NC}"
    echo ""
    
    if [ -n "$TARGET_VERSION" ]; then
        echo "Updating to version: $TARGET_VERSION"
    else
        echo "Updating to latest version"
    fi
    echo ""
    
    echo -n "Continue? (y/N): "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Update cancelled"
        exit 0
    fi
    
    update_global
    
    new_version=$(get_current_version)
    echo ""
    echo -e "${GREEN}Updated from $current_version to $new_version${NC}"
    echo ""
    
    show_changelog
    
    echo ""
    print_info "You may need to re-run: .global/scripts/apply.sh"
}

main "$@"

