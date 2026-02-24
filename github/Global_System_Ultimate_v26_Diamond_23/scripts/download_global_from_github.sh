#!/bin/bash
# Download Global System Ultimate from GitHub
# Usage: ./download_global_from_github.sh

REPO_URL="https://github.com/hamfarid/global.git"
TARGET_DIR="GitHub/global_system"

echo "🚀 Downloading Global System Ultimate..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Create directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Clone or Pull
if [ -d "$TARGET_DIR/.git" ]; then
    echo "🔄 Updating existing repository..."
    cd "$TARGET_DIR"
    git pull origin main
else
    echo "⬇️  Cloning repository..."
    git clone "$REPO_URL" "$TARGET_DIR"
fi

echo "✅ Download Complete."
echo "👉 Run: python3 $TARGET_DIR/scripts/activate_global.py"
