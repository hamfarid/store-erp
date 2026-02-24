#!/bin/bash

# Global System Ultimate - Project Initialization Script
# Sets up a new project with the standard folder structure and governance files

VERSION="v26.0 Diamond 32 GAARA AI"
FRAMEWORK_DIR="global_system"

echo "🚀 Initializing New Project with Global System Ultimate ($VERSION)..."

# Check if framework is present
if [ ! -d "$FRAMEWORK_DIR" ]; then
    echo "❌ Framework directory '$FRAMEWORK_DIR' not found!"
    echo "📥 Please run download_global.sh first."
    exit 1
fi

# Create standard folder structure
echo "📂 Creating folder structure..."
mkdir -p .cursor/rules
mkdir -p .vscode
mkdir -p .claude
mkdir -p memory-bank
mkdir -p TASKS
mkdir -p docs
mkdir -p tests
mkdir -p scripts
mkdir -p tools

# Copy governance files
echo "📜 Copying governance files..."
cp "$FRAMEWORK_DIR/AGENTS.md" .
cp "$FRAMEWORK_DIR/BOOTSTRAP_v15.9.md" .
cp "$FRAMEWORK_DIR/CLAUDE.md" .
cp "$FRAMEWORK_DIR/VERSION" .

# Copy config files
echo "⚙️  Copying configuration..."
cp -r "$FRAMEWORK_DIR/.cursor/rules/" .cursor/rules/
cp -r "$FRAMEWORK_DIR/.vscode/" .vscode/
cp -r "$FRAMEWORK_DIR/.claude/" .claude/

# Initialize memory bank
echo "🧠 Initializing Memory Bank..."
cp -r "$FRAMEWORK_DIR/memory-bank/" .

# Create initial plan
echo "# Project Plan" > TASKS/PLAN.md
echo "Initialized with Global System Ultimate $VERSION" >> TASKS/PLAN.md

echo "✅ Project Initialized Successfully!"
echo "👉 Next Step: Read BOOTSTRAP_v15.9.md"
