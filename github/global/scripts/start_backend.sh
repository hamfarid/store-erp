#!/bin/bash
# Arabic Inventory Management System - Backend Startup Script

echo "🚀 Starting Arabic Inventory Management System Backend..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Navigate to backend directory
cd backend

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Start the Flask application
echo "✅ Starting Flask server on port 5001..."
python3 app.py

echo "🎉 Backend started successfully!"
