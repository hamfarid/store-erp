#!/bin/bash
# Arabic Inventory Management System - Complete System Startup Script

echo "🚀 Starting Complete Arabic Inventory Management System..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Start backend in background
echo "🔧 Starting backend server..."
cd backend
pip3 install -r requirements.txt 2>/dev/null || echo "⚠️ Could not install Python dependencies"
export FLASK_APP=app.py
export FLASK_ENV=production
python3 app.py &
BACKEND_PID=$!
echo "✅ Backend started with PID: $BACKEND_PID"

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd ../frontend
npm install 2>/dev/null || echo "⚠️ Could not install Node.js dependencies"
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started with PID: $FRONTEND_PID"

echo ""
echo "🎉 Arabic Inventory Management System is now running!"
echo "📊 Backend API: http://localhost:5001"
echo "🌐 Frontend UI: http://localhost:3000"
echo ""
echo "To stop the system, press Ctrl+C or run:"
echo "kill $BACKEND_PID $FRONTEND_PID"

# Wait for user interrupt
trap "echo '🛑 Stopping system...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT
wait
