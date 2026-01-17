#!/bin/bash
# File: scripts/fix_line_length.sh
# Fix line length to ≤120 characters

echo "📏 Fixing line length..."

# Install tools if needed
pip install -q autopep8 black isort

# Fix Python files
echo "Fixing with autopep8..."
autopep8 --in-place \
  --aggressive \
  --aggressive \
  --max-line-length=120 \
  --recursive \
  --exclude=venv,.venv,migrations,node_modules \
  .

echo "Fixing with black..."
black --line-length=120 --exclude='/(venv|\.venv|migrations|node_modules)/' .

echo "Fixing imports with isort..."
isort --profile=black --line-length=120 --skip=venv --skip=.venv --skip=migrations .

echo "✅ Line length fixed (≤120)"
