#!/bin/bash

# Global System Ultimate - Download Script
# Downloads the latest version of the framework from GitHub

REPO_URL="https://github.com/hamfarid/global.git"
TARGET_DIR="global_system"

echo "🚀 Downloading Global System Ultimate..."

if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  Directory '$TARGET_DIR' already exists."
    read -p "Overwrite? (y/N) " confirm
    if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
        echo "❌ Aborted."
        exit 1
    fi
    rm -rf "$TARGET_DIR"
fi

echo "📦 Cloning repository..."
git clone --depth 1 "$REPO_URL" "$TARGET_DIR"

if [ $? -eq 0 ]; then
    echo "✅ Download complete!"
    echo "📂 Framework installed in: $TARGET_DIR"
    
    # Remove .git folder to detach from the source repo
    rm -rf "$TARGET_DIR/.git"
    
    echo "🔧 Initializing..."
    if [ -f "$TARGET_DIR/scripts/preflight_check.py" ]; then
        python3 "$TARGET_DIR/scripts/preflight_check.py"
    else
        echo "⚠️  Preflight check script not found."
    fi
    
    echo "🎉 Ready to use! Read $TARGET_DIR/BOOTSTRAP_v15.9.md to start."
else
    echo "❌ Download failed. Check your internet connection or repository permissions."
    exit 1
fi
