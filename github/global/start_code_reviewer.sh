#!/bin/bash

# Start Code Reviewer MCP Server
# Usage: ./start_code_reviewer.sh

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Check if MCP SDK is installed
if ! python3 -c "import mcp" &> /dev/null; then
    echo "Installing MCP SDK..."
    pip3 install mcp fastmcp google-generativeai anthropic
fi

echo "Starting Code Reviewer MCP Server..."
echo "Connect your AI tool (Cursor/Claude) to this server."
echo "Use 'stdio' transport."

python3 tools/code_reviewer_mcp.py
