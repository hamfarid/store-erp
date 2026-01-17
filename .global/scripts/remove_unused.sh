#!/bin/bash
# File: scripts/remove_unused.sh
# Remove unused imports and code

echo "🧹 Removing unused code..."

# Check if autoflake is installed
if ! command -v autoflake &> /dev/null; then
    echo "Installing autoflake..."
    pip install autoflake
fi

# Remove unused imports and variables
autoflake --in-place \
  --remove-all-unused-imports \
  --remove-unused-variables \
  --remove-duplicate-keys \
  --recursive \
  --exclude=venv,.venv,migrations,node_modules,__pycache__ \
  .

echo "✅ Unused code removed"
