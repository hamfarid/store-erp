#!/bin/bash
# Arabic Inventory Management System - Frontend Startup Script

echo "🚀 Starting Arabic Inventory Management System Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build the application
echo "🔨 Building the application..."
npm run build

# Start the development server (or serve the built files)
echo "✅ Starting development server..."
npm run dev

echo "🎉 Frontend started successfully!"
