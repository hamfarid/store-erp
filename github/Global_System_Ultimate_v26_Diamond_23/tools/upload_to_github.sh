#!/bin/bash
# 🚀 Global System Ultimate - GitHub Upload Script
# Usage: ./upload_to_github.sh <repo_name> [private|public]

REPO_NAME=${1:-"global-system-ultimate"}
VISIBILITY=${2:-"private"}

# Read version dynamically
VERSION=$(cat ../VERSION 2>/dev/null || echo "Dynamic")

echo "🚀 Initializing GitHub Upload for '$REPO_NAME' (v$VERSION)..."

# 1. Initialize Git
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized."
fi

# 2. Create .gitignore if missing
if [ ! -f ".gitignore" ]; then
    echo "__pycache__/" > .gitignore
    echo "*.pyc" >> .gitignore
    echo ".env" >> .gitignore
    echo "venv/" >> .gitignore
    echo "node_modules/" >> .gitignore
    echo ".DS_Store" >> .gitignore
    echo "✅ .gitignore created."
fi

# 3. Add files
git add .
git commit -m "feat: Initial commit of Global System Ultimate v$VERSION"

# 4. Create Repo via GitHub CLI
echo "🌐 Creating repository on GitHub..."
gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --remote=origin --push

if [ $? -eq 0 ]; then
    echo "✅ Successfully uploaded to https://github.com/$(gh api user -q .login)/$REPO_NAME"
    echo "📋 Next Step: Run './tools/download_from_github.sh' in your new project folder."
else
    echo "❌ Error creating repository. Please check your GitHub CLI login ('gh auth login')."
fi
