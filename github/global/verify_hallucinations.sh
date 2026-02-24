#!/bin/bash

# Run Hallucination Verification Tool
# This script installs dependencies and runs the verification tool.

if [ -z "$1" ]; then
    echo "Usage: ./verify_hallucinations.sh <input_file> [threshold]"
    exit 1
fi

INPUT_FILE=$1
THRESHOLD=${2:-0.6}

echo "Running Hallucination Verification on '$INPUT_FILE' (Threshold: $THRESHOLD)..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r tools/hallucination_requirements.txt

# Run Tool
python3 tools/verify_hallucinations.py "$INPUT_FILE" --threshold "$THRESHOLD"
