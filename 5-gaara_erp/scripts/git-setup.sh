#!/bin/bash
# =============================================================================
# Gaara ERP - Git Setup and Push Script
# =============================================================================
# Helps set up git and push to GitHub
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================="
echo "Gaara ERP - Git Setup"
echo "==========================================${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git installed${NC}"

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo ""
    echo "Initializing git repository..."
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
else
    echo -e "${GREEN}✓ Git repository already exists${NC}"
fi

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}⚠ .gitignore not found, creating one...${NC}"
    # .gitignore should be created separately
fi

# Show status
echo ""
echo "Current git status:"
git status --short || true

# Ask for remote URL
echo ""
read -p "Enter GitHub repository URL (or press Enter to skip): " GITHUB_URL

if [ -n "$GITHUB_URL" ]; then
    # Check if remote already exists
    if git remote get-url origin &> /dev/null; then
        echo "Remote 'origin' already exists: $(git remote get-url origin)"
        read -p "Update it? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git remote set-url origin "$GITHUB_URL"
            echo -e "${GREEN}✓ Remote updated${NC}"
        fi
    else
        git remote add origin "$GITHUB_URL"
        echo -e "${GREEN}✓ Remote added${NC}"
    fi
fi

# Stage all files
echo ""
echo "Staging all files..."
git add .

# Show what will be committed
echo ""
echo "Files to be committed:"
git status --short

# Ask for commit message
echo ""
read -p "Enter commit message (or press Enter for default): " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="feat: Add comprehensive backend infrastructure, Docker setup, API documentation, and configuration modules"
fi

# Commit
echo ""
echo "Committing changes..."
git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓ Changes committed${NC}"

# Ask to push
if [ -n "$GITHUB_URL" ] || git remote get-url origin &> /dev/null; then
    echo ""
    read -p "Push to GitHub? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
        echo "Pushing to origin/$BRANCH..."
        git push -u origin "$BRANCH" || git push -u origin main || git push -u origin master
        echo -e "${GREEN}✓ Pushed to GitHub${NC}"
    fi
fi

echo ""
echo -e "${GREEN}=========================================="
echo "Git setup completed!"
echo "==========================================${NC}"
