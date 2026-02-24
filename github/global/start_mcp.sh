#!/bin/bash

# Start Memory MCP Server
# This script installs dependencies and starts the MCP server.

echo "Starting Memory MCP Server..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r tools/mcp_requirements.txt

# Start MCP Server
echo "Starting MCP Server..."
python3 tools/memory_mcp_server.py
