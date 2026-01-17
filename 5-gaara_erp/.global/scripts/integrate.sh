#!/bin/bash
#
# integrate.sh - دمج Global Guidelines في مشروع قائم
# Integrate Global Guidelines into existing project
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash
#   OR
#   ./integrate.sh
#
# This script installs Global Guidelines in .global/ directory
# WITHOUT affecting your project's Git repository
#

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GLOBAL_DIR=".global"
REPO_URL="https://github.com/hamfarid/global"
BRANCH="main"
VERSION="3.7.0"

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║         Global Guidelines Integration Script              ║"
    echo "║                                                            ║"
    echo "║  Installs Global Guidelines without affecting your Git    ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if curl is installed
    if ! command -v curl &> /dev/null; then
        print_error "curl is not installed. Please install it first."
        exit 1
    fi
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        print_error "git is not installed. Please install it first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

check_existing_installation() {
    if [ -d "$GLOBAL_DIR" ]; then
        print_warning "Global Guidelines already installed in $GLOBAL_DIR"
        echo -n "Do you want to reinstall? (y/N): "
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled"
            exit 0
        fi
        print_info "Removing existing installation..."
        rm -rf "$GLOBAL_DIR"
    fi
}

create_directory() {
    print_info "Creating $GLOBAL_DIR directory..."
    mkdir -p "$GLOBAL_DIR"
    print_success "Directory created"
}

download_files() {
    print_info "Downloading Global Guidelines v$VERSION..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    
    # Clone repository
    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TEMP_DIR" > /dev/null 2>&1
    
    # Copy files to .global/
    cp -r "$TEMP_DIR"/* "$GLOBAL_DIR/"
    
    # Remove .git directory to avoid conflicts
    rm -rf "$GLOBAL_DIR/.git"
    
    # Clean up
    rm -rf "$TEMP_DIR"
    
    print_success "Files downloaded successfully"
}

update_gitignore() {
    print_info "Updating .gitignore..."
    
    if [ ! -f ".gitignore" ]; then
        touch .gitignore
    fi
    
    # Check if .global/ is already in .gitignore
    if grep -q "^\.global/$" .gitignore 2>/dev/null; then
        print_info ".global/ already in .gitignore"
    else
        echo "" >> .gitignore
        echo "# Global Guidelines (standalone installation)" >> .gitignore
        echo ".global/" >> .gitignore
        print_success ".gitignore updated"
    fi
}

create_shortcuts() {
    print_info "Creating shortcuts..."
    
    # Create symlinks for easy access
    if [ ! -f "GUIDELINES.txt" ]; then
        ln -s "$GLOBAL_DIR/GLOBAL_GUIDELINES_v3.7.txt" GUIDELINES.txt 2>/dev/null || true
    fi
    
    print_success "Shortcuts created"
}

make_scripts_executable() {
    print_info "Making scripts executable..."
    
    if [ -d "$GLOBAL_DIR/scripts" ]; then
        chmod +x "$GLOBAL_DIR/scripts"/*.sh 2>/dev/null || true
        print_success "Scripts are now executable"
    fi
}

print_next_steps() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║  ✓ Global Guidelines installed successfully!              ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo ""
    echo "  1. Configure components:"
    echo -e "     ${YELLOW}$GLOBAL_DIR/scripts/configure.sh${NC}"
    echo ""
    echo "  2. Apply to your project:"
    echo -e "     ${YELLOW}$GLOBAL_DIR/scripts/apply.sh${NC}"
    echo ""
    echo "  3. Read the guidelines:"
    echo -e "     ${YELLOW}cat $GLOBAL_DIR/GLOBAL_GUIDELINES_v3.7.txt${NC}"
    echo ""
    echo "  4. Explore the flows:"
    echo -e "     ${YELLOW}cat $GLOBAL_DIR/flows/INTEGRATION_FLOW.md${NC}"
    echo ""
    echo "  5. Use the tools:"
    echo -e "     ${YELLOW}python $GLOBAL_DIR/tools/analyze_dependencies.py .${NC}"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  - Integration Flow: $GLOBAL_DIR/flows/INTEGRATION_FLOW.md"
    echo "  - Development Flow: $GLOBAL_DIR/flows/DEVELOPMENT_FLOW.md"
    echo "  - Deployment Flow: $GLOBAL_DIR/flows/DEPLOYMENT_FLOW.md"
    echo ""
    echo -e "${GREEN}Happy coding! 🚀${NC}"
    echo ""
}

# Main execution
main() {
    print_header
    
    check_prerequisites
    check_existing_installation
    create_directory
    download_files
    update_gitignore
    create_shortcuts
    make_scripts_executable
    
    print_next_steps
}

# Run main function
main "$@"

