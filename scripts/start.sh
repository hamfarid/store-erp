#!/bin/bash

# 🏪 نظام إدارة المخزون الكامل - سكريبت التشغيل
# Complete Inventory Management System - Start Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if port is in use
check_port() {
    local port=$1
    if command -v lsof >/dev/null 2>&1; then
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
            return 0  # Port is in use
        fi
    elif command -v netstat >/dev/null 2>&1; then
        if netstat -an | grep ":$port " | grep LISTEN >/dev/null; then
            return 0  # Port is in use
        fi
    fi
    return 1  # Port is free
}

# Function to kill process on port
kill_port() {
    local port=$1
    print_status "إيقاف العملية على المنفذ $port..."
    print_status "Killing process on port $port..."
    
    if command -v lsof >/dev/null 2>&1; then
        local pid=$(lsof -ti:$port)
        if [ ! -z "$pid" ]; then
            kill -9 $pid 2>/dev/null || true
        fi
    elif command -v netstat >/dev/null 2>&1; then
        # For Windows/other systems
        if command -v taskkill >/dev/null 2>&1; then
            for pid in $(netstat -ano | grep ":$port " | awk '{print $5}'); do
                taskkill /PID $pid /F 2>/dev/null || true
            done
        fi
    fi
}

# Function to start backend
start_backend() {
    print_status "بدء تشغيل الخادم الخلفي..."
    print_status "Starting backend server..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_error "البيئة الافتراضية غير موجودة. يرجى تشغيل ./scripts/install.sh أولاً"
        print_error "Virtual environment not found. Please run ./scripts/install.sh first"
        exit 1
    fi
    
    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || {
        print_error "فشل في تفعيل البيئة الافتراضية"
        print_error "Failed to activate virtual environment"
        exit 1
    }
    
    # Check if main.py exists
    if [ ! -f "src/main.py" ]; then
        print_error "ملف src/main.py غير موجود"
        print_error "src/main.py not found"
        exit 1
    fi
    
    # Kill any existing process on port 8000
    if check_port 8000; then
        print_warning "المنفذ 8000 مستخدم، سيتم إيقاف العملية الموجودة"
        print_warning "Port 8000 is in use, killing existing process"
        kill_port 8000
        sleep 2
    fi
    
    # Start backend server
    print_status "تشغيل الخادم الخلفي على http://localhost:8000"
    print_status "Starting backend server on http://localhost:8000"
    
    # Start in background
    nohup python src/main.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if backend is running
    if check_port 8000; then
        print_success "الخادم الخلفي يعمل بنجاح (PID: $BACKEND_PID)"
        print_success "Backend server running successfully (PID: $BACKEND_PID)"
        echo $BACKEND_PID > ../logs/backend.pid
    else
        print_error "فشل في تشغيل الخادم الخلفي"
        print_error "Failed to start backend server"
        exit 1
    fi
    
    cd ..
}

# Function to start frontend
start_frontend() {
    print_status "بدء تشغيل الواجهة الأمامية..."
    print_status "Starting frontend server..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_error "مجلد node_modules غير موجود. يرجى تشغيل ./scripts/install.sh أولاً"
        print_error "node_modules directory not found. Please run ./scripts/install.sh first"
        exit 1
    fi
    
    # Kill any existing process on port 5173
    if check_port 5173; then
        print_warning "المنفذ 5173 مستخدم، سيتم إيقاف العملية الموجودة"
        print_warning "Port 5173 is in use, killing existing process"
        kill_port 5173
        sleep 2
    fi
    
    # Start frontend server
    print_status "تشغيل الواجهة الأمامية على http://localhost:5173"
    print_status "Starting frontend server on http://localhost:5173"
    
    # Start in background
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    # Wait a moment for server to start
    sleep 5
    
    # Check if frontend is running
    if check_port 5173; then
        print_success "الواجهة الأمامية تعمل بنجاح (PID: $FRONTEND_PID)"
        print_success "Frontend server running successfully (PID: $FRONTEND_PID)"
        echo $FRONTEND_PID > ../logs/frontend.pid
    else
        print_error "فشل في تشغيل الواجهة الأمامية"
        print_error "Failed to start frontend server"
        exit 1
    fi
    
    cd ..
}

# Function to stop servers
stop_servers() {
    print_status "إيقاف الخوادم..."
    print_status "Stopping servers..."
    
    # Stop backend
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill $BACKEND_PID
            print_success "تم إيقاف الخادم الخلفي"
            print_success "Backend server stopped"
        fi
        rm -f logs/backend.pid
    fi
    
    # Stop frontend
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            print_success "تم إيقاف الواجهة الأمامية"
            print_success "Frontend server stopped"
        fi
        rm -f logs/frontend.pid
    fi
    
    # Kill any remaining processes on ports
    kill_port 8000
    kill_port 5173
}

# Function to show status
show_status() {
    print_status "حالة الخوادم:"
    print_status "Server status:"
    
    if check_port 8000; then
        print_success "الخادم الخلفي يعمل على http://localhost:8000"
        print_success "Backend server running on http://localhost:8000"
    else
        print_error "الخادم الخلفي متوقف"
        print_error "Backend server stopped"
    fi
    
    if check_port 5173; then
        print_success "الواجهة الأمامية تعمل على http://localhost:5173"
        print_success "Frontend server running on http://localhost:5173"
    else
        print_error "الواجهة الأمامية متوقفة"
        print_error "Frontend server stopped"
    fi
}

# Main function
main() {
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "يرجى تشغيل هذا السكريبت من المجلد الجذر للمشروع"
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Create logs directory
    mkdir -p logs
    
    # Handle command line arguments
    case "${1:-start}" in
        "start")
            print_status "🏪 بدء تشغيل نظام إدارة المخزون الكامل..."
            print_status "🏪 Starting Complete Inventory Management System..."
            start_backend
            start_frontend
            echo ""
            print_success "🎉 النظام يعمل بنجاح!"
            print_success "🎉 System is running successfully!"
            echo ""
            print_status "الروابط:"
            print_status "URLs:"
            print_status "  الواجهة الأمامية / Frontend: http://localhost:5173"
            print_status "  الخادم الخلفي / Backend: http://localhost:8000"
            print_status "  API Documentation: http://localhost:8000/api"
            echo ""
            print_status "لإيقاف النظام: ./scripts/start.sh stop"
            print_status "To stop the system: ./scripts/start.sh stop"
            ;;
        "stop")
            stop_servers
            ;;
        "restart")
            stop_servers
            sleep 2
            start_backend
            start_frontend
            ;;
        "status")
            show_status
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status}"
            echo "الاستخدام: $0 {start|stop|restart|status}"
            exit 1
            ;;
    esac
}

# Handle Ctrl+C
trap 'print_status "تم إيقاف السكريبت"; print_status "Script interrupted"; exit 0' INT

# Run main function
main "$@"
