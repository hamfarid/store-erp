#!/bin/bash

# Global System - Project Structure Generator
# Version: v26.0.0 (Diamond 5)
# Description: Creates standard project folder hierarchy for new AI/ML projects

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=== Global System Project Structure Generator (v26.0.0) ===${NC}"

# Prompt for project name
read -p "Enter project name: " PROJECT_NAME

if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}Project name cannot be empty.${NC}"
    exit 1
fi

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

echo -e "${BLUE}Creating standard folder hierarchy...${NC}"

# Core Directories
mkdir -p docs/
mkdir -p src/
mkdir -p tests/
mkdir -p scripts/
mkdir -p config/
mkdir -p data/
mkdir -p models/
mkdir -p logs/
mkdir -p notebooks/

# Subdirectories
mkdir -p src/ml/
mkdir -p src/utils/
mkdir -p src/api/
mkdir -p src/frontend/

# Create placeholder files
touch README.md
touch .gitignore
touch requirements.txt
touch setup.py
touch .env.example

# Create initial documentation
echo "# $PROJECT_NAME" > README.md
echo "Project initialized using Global System v26.0.0 (Diamond 5)" >> README.md

# Create .gitignore
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo ".DS_Store" >> .gitignore

echo -e "${GREEN}Project structure created successfully!${NC}"
echo "Location: $(pwd)"
ls -F
