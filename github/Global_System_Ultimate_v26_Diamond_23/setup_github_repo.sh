#!/bin/bash

# Global System - GitHub Repository Setup Script
# Version: v26.0.0 (Diamond 5)
# Description: Automates the creation and initialization of the 'global' private repository

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Global System GitHub Setup (v26.0.0) ===${NC}"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    echo "Please install it first: https://cli.github.com/"
    exit 1
fi

# Check authentication status
echo -e "${BLUE}Checking GitHub authentication...${NC}"
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: You are not logged in to GitHub.${NC}"
    echo "Please run 'gh auth login' first."
    exit 1
fi

REPO_NAME="global"
VISIBILITY="private"
DESCRIPTION="Global System for AI Development Governance - v26.0.0 Diamond 5"

echo -e "${BLUE}Creating repository '${REPO_NAME}' (${VISIBILITY})...${NC}"

# Check if repository exists
if gh repo view "$REPO_NAME" &> /dev/null; then
    echo -e "${GREEN}Repository '$REPO_NAME' already exists.${NC}"
else
    # Create repository and push code
    gh repo create "$REPO_NAME" --$VISIBILITY --description "$DESCRIPTION" --source=. --remote=origin --push
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Repository created and code pushed successfully!${NC}"
    else
        echo -e "${RED}Failed to create repository.${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}Verifying remote configuration...${NC}"
git remote -v

echo -e "${GREEN}=== Setup Complete ===${NC}"
echo "You can now use 'git push' to update the repository."
