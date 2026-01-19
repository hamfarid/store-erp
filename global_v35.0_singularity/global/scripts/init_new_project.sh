#!/bin/bash

# Script to initialize a new project with the Global System structure
# Usage: ./init_new_project.sh <project_name>

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
  echo "Error: Project name is required."
  echo "Usage: ./init_new_project.sh <project_name>"
  exit 1
fi

TARGET_DIR="$(pwd)/$PROJECT_NAME"

if [ -d "$TARGET_DIR" ]; then
  echo "Error: Directory $TARGET_DIR already exists."
  exit 1
fi

echo "🚀 Initializing new project: $PROJECT_NAME"

# Create project directory
mkdir -p "$TARGET_DIR"

# Copy global structure (excluding scripts and git)
SOURCE_DIR="$(dirname "$0")/.."
rsync -av --exclude='.git' --exclude='scripts' "$SOURCE_DIR/" "$TARGET_DIR/global/"

# Create project root files
touch "$TARGET_DIR/project_memory.md"
touch "$TARGET_DIR/todo.md"
touch "$TARGET_DIR/plan.md"

# Initialize git
cd "$TARGET_DIR" || exit
git init

# Create basic .gitignore
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "global/" >> .gitignore # Optional: if you want to submodule it instead

echo "✅ Project initialized at $TARGET_DIR"
echo "📂 Structure:"
echo "  - global/ (The AI Brain)"
echo "  - project_memory.md"
echo "  - todo.md"
echo "  - plan.md"
