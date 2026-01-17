#!/bin/bash
# =============================================================================
# Gaara ERP - Quick Git Push Script
# =============================================================================
# Quick script to add, commit, and push changes
# =============================================================================

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Gaara ERP - Git Push"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Git repository not initialized. Run ./scripts/git-setup.sh first"
    exit 1
fi

# Get commit message from argument or prompt
COMMIT_MSG="${1:-}"

if [ -z "$COMMIT_MSG" ]; then
    echo ""
    echo "Recent changes:"
    git status --short | head -10
    echo ""
    read -p "Enter commit message: " COMMIT_MSG
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="chore: Update project files"
    fi
fi

# Stage all changes
echo ""
echo "Staging changes..."
git add .

# Commit
echo ""
echo "Committing..."
git commit -m "$COMMIT_MSG"

# Get current branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Push
echo ""
echo "Pushing to origin/$BRANCH..."
if git push origin "$BRANCH" 2>/dev/null || git push -u origin "$BRANCH" 2>/dev/null; then
    echo -e "${GREEN}✓ Successfully pushed to GitHub${NC}"
else
    echo -e "${YELLOW}⚠ Push failed. Check your remote configuration.${NC}"
    echo "Run: git remote -v to check remotes"
    echo "Run: ./scripts/git-setup.sh to configure remote"
fi

echo ""
echo "=========================================="
