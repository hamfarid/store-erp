#!/bin/bash

# Script to upload the Global System to a new private GitHub repository
# Usage: ./upload_global_to_github.sh <repo_name>

REPO_NAME=$1

if [ -z "$REPO_NAME" ]; then
  echo "Error: Repository name is required."
  echo "Usage: ./upload_global_to_github.sh <repo_name>"
  exit 1
fi

echo "🚀 Preparing to upload Global System to GitHub repository: $REPO_NAME"

# Navigate to the global directory
cd "$(dirname "$0")/.." || exit

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
  git init
  echo "Initialized empty Git repository"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
  echo "node_modules/" > .gitignore
  echo ".env" >> .gitignore
  echo ".DS_Store" >> .gitignore
  echo "Created .gitignore"
fi

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Global System v28.0 (Singularity Edition)"

# Create private repository on GitHub
echo "Creating private repository on GitHub..."
gh repo create "$REPO_NAME" --private --source=. --remote=origin --push

if [ $? -eq 0 ]; then
  echo "✅ Successfully uploaded Global System to https://github.com/$(gh api user -q .login)/$REPO_NAME"
else
  echo "❌ Failed to create or push to repository. Please check your GitHub CLI authentication."
fi
