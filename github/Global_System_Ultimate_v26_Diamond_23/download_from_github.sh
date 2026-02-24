#!/bin/bash

# Global System - Download Script
# Version: v26.0.0 (Diamond 5)
# Description: Downloads the Global System repository to a new project location

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Global System Download Utility (v26.0.0) ===${NC}"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    echo "Please install it first: https://cli.github.com/"
    exit 1
fi

# Check authentication status
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: You are not logged in to GitHub.${NC}"
    echo "Please run 'gh auth login' first."
    exit 1
fi

# Get current username
USERNAME=$(gh api user -q .login)
REPO_NAME="global"
TARGET_DIR="Global_System_v26"

echo -e "${BLUE}Downloading repository '${USERNAME}/${REPO_NAME}'...${NC}"

# Clone repository
if [ -d "$TARGET_DIR" ]; then
    echo -e "${RED}Directory '$TARGET_DIR' already exists.${NC}"
    read -p "Do you want to overwrite it? (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        rm -rf "$TARGET_DIR"
    else
        echo "Aborted."
        exit 1
    fi
fi

gh repo clone "$USERNAME/$REPO_NAME" "$TARGET_DIR"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Download complete!${NC}"
    echo "Location: $(pwd)/$TARGET_DIR"
    echo "Version: v26.0.0 (Diamond 5)"
else
    echo -e "${RED}Download failed.${NC}"
    exit 1
fi
