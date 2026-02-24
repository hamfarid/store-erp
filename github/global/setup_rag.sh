#!/bin/bash

# Setup Local RAG System
# This script installs dependencies and initializes the local vector database.

echo "Setting up Local RAG System..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r tools/rag_requirements.txt

# Initialize Vector DB
echo "Initializing Vector DB..."
python3 tools/setup_local_rag.py init

echo "RAG System Setup Complete!"
echo "To query the knowledge base, run: python3 tools/setup_local_rag.py query 'your query'"
echo "To start the API server, run: python3 tools/setup_local_rag.py serve"
