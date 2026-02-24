#!/bin/bash
# Verify Package Integrity - Global System Ultimate v9

SOURCE_DIR="$(pwd)"
PACKAGE_DIR="$(pwd)/global_system_v9_package"

echo "🔍 Starting Integrity Check..."

# Count files (excluding .git and __pycache__)
SOURCE_COUNT=$(find "$SOURCE_DIR" -type f -not -path "*/.git/*" -not -path "*/__pycache__/*" | wc -l)
PACKAGE_COUNT=$(find "$PACKAGE_DIR" -type f | wc -l)

echo "📂 Source Files (Clean): $SOURCE_COUNT"
echo "📦 Package Files: $PACKAGE_COUNT"

if [ "$SOURCE_COUNT" -eq "$PACKAGE_COUNT" ]; then
    echo "✅ File Count Match: 100% Integrity"
else
    echo "❌ File Count Mismatch! Missing files detected."
    # List missing files
    diff -r "$SOURCE_DIR" "$PACKAGE_DIR" | grep "Only in $SOURCE_DIR"
fi

# Check size of .git folder (likely culprit for size drop)
GIT_SIZE=$(du -sh "$SOURCE_DIR/.git" | cut -f1)
echo "📉 Size of removed .git history: $GIT_SIZE"
