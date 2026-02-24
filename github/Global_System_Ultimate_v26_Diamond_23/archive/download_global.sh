#!/bin/bash
# Global System Download Script (Global System Ultimate)
# Usage: ./download_global.sh <target_directory>

if [ -z "$1" ]; then
    echo "Usage: ./download_global.sh <target_directory>"
    exit 1
fi

TARGET_DIR=$1
REPO_URL="https://github.com/hamfarid/global.git"

echo "⬇️  Cloning Global System Global System Ultimate into $TARGET_DIR..."

if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  Directory $TARGET_DIR already exists."
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted."
        exit 1
    fi
    rm -rf "$TARGET_DIR"
fi

git clone "$REPO_URL" "$TARGET_DIR"

if [ $? -eq 0 ]; then
    echo "✅ Download complete."
    echo "👉 To start: cd $TARGET_DIR && python3 setup_project.py my_new_project"
else
    echo "❌ Download failed. Please check your internet connection or git credentials."
fi


# Injected by Global System Ultimate
python3 global/genesis.py
