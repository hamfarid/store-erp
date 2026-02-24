#!/bin/bash
# Package Global System Ultimate v9 for GitHub Upload

# Define paths
SOURCE_DIR="$(pwd)"
OUTPUT_DIR="$(pwd)/global_system_v9_package"
ZIP_FILE="$(pwd)/global_system_v9.zip"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Copy all files to output directory
cp -r "$SOURCE_DIR"/* "$OUTPUT_DIR/"

# Remove unnecessary files (e.g., .git, __pycache__)
find "$OUTPUT_DIR" -name ".git" -type d -exec rm -rf {} +
find "$OUTPUT_DIR" -name "__pycache__" -type d -exec rm -rf {} +
find "$OUTPUT_DIR" -name "*.pyc" -type f -delete

# Create ZIP archive
cd "$OUTPUT_DIR"
zip -r "$ZIP_FILE" .

echo "✅ Global System Ultimate v9 packaged successfully!"
echo "📦 ZIP File: $ZIP_FILE"
