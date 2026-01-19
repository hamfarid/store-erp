#!/bin/bash

# Script to download the Global System from GitHub into the current project
# Usage: ./download_global_from_github.sh <repo_url>

REPO_URL=$1

if [ -z "$REPO_URL" ]; then
  echo "Error: Repository URL is required."
  echo "Usage: ./download_global_from_github.sh <repo_url>"
  exit 1
fi

echo "🚀 Downloading Global System from $REPO_URL"

# Check if global directory already exists
if [ -d "global" ]; then
  echo "⚠️  'global' directory already exists. Backing it up..."
  mv global "global_backup_$(date +%s)"
fi

# Clone the repository
git clone "$REPO_URL" global

# Remove .git folder from the cloned repo to avoid nested git issues
rm -rf global/.git

echo "✅ Global System installed in ./global/"
