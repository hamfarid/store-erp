#!/bin/bash

# Script to initialize a new project with the Global System structure (Global System Ultimate Synchronized Intelligence Edition)
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

echo "🚀 Initializing new project: $PROJECT_NAME (Global System Ultimate Synchronized Intelligence Edition)"

# Create project directory
mkdir -p "$TARGET_DIR"

# Copy global structure (excluding scripts and git)
SOURCE_DIR="$(dirname "$0")/.."
rsync -av --exclude='.git' --exclude='scripts' "$SOURCE_DIR/" "$TARGET_DIR/global/"

# Create project root files
touch "$TARGET_DIR/project_memory.md"
touch "$TARGET_DIR/todo.md"
touch "$TARGET_DIR/plan.md"
touch "$TARGET_DIR/system_log.md"

# Initialize git
cd "$TARGET_DIR" || exit
git init

# Create basic .gitignore
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".venv/" >> .gitignore
echo ".memory/" >> .gitignore

# Create requirements.txt for the AI tools
echo "requests" > requirements.txt
echo "beautifulsoup4" >> requirements.txt
echo "playwright" >> requirements.txt
echo "pytest" >> requirements.txt
echo "flake8" >> requirements.txt

echo "✅ Project initialized at $TARGET_DIR"
echo "📂 Structure:"
echo "  - global/ (The AI Brain Global System Ultimate)"
echo "  - global/AI_CONTEXT_ROUTER.md (The Navigation System)"
echo "  - project_memory.md"
echo "  - todo.md"
echo "  - plan.md"
echo "  - system_log.md"
echo "  - requirements.txt (AI Tools Dependencies)"

echo "👉 Next Step: Run 'python3 global/tools/lifecycle.py $PROJECT_NAME \"Initialize Global System Ultimate\"'"


# Injected by Global System Ultimate
python3 global/genesis.py
