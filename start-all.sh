#!/bin/bash
# =============================================================================
# Store ERP - Production Startup Script (Linux/macOS)
# =============================================================================
# This script starts all services including monitoring stack
# Usage: ./start-all.sh [OPTIONS]
# Options:
#   --no-monitoring    Skip monitoring stack (Prometheus, Grafana, Loki)
#   --dev              Start in development mode
#   --rebuild          Force rebuild of all containers
#   --help             Show this help message
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

START_MONITORING=true
DEV_MODE=false
REBUILD=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-monitoring)
            START_MONITORING=false
            shift
            ;;
        --dev)
            DEV_MODE=true
            shift
            ;;
        --rebuild)
            REBUILD=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --no-monitoring    Skip monitoring stack"
            echo "  --dev              Start in development mode"
            echo "  --rebuild          Force rebuild of all containers"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed ($(docker --version | cut -d ' ' -f3))"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    # Check .env file
    if [ ! -f .env ]; then
        print_warning ".env file not found, creating from .env.example"
        if [ -f .env.example ]; then
            cp .env.example .env
            print_info "Please edit .env file with your configuration"
            exit 1
        else
            print_error ".env.example not found"
            exit 1
        fi
    fi
    print_success ".env file found"
}

# Stop existing containers
stop_existing() {
    print_header "Stopping Existing Containers"
    
    # Stop main services
    docker-compose -f docker-compose.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    # Stop monitoring if running
    if [ "$START_MONITORING" = true ]; then
        docker-compose -f docker-compose.monitoring.yml down 2>/dev/null || true
    fi
    
    print_success "Stopped all existing containers"
}

# Start main services
start_main_services() {
    print_header "Starting Main Services"
    
    COMPOSE_FILE="docker-compose.prod.yml"
    if [ "$DEV_MODE" = true ]; then
        COMPOSE_FILE="docker-compose.yml"
        print_info "Using development configuration"
    fi
    
    BUILD_FLAG=""
    if [ "$REBUILD" = true ]; then
        BUILD_FLAG="--build"
        print_info "Forcing rebuild of containers"
    fi
    
    # Start services
    docker-compose -f "$COMPOSE_FILE" up -d $BUILD_FLAG
    
    print_success "Main services started"
}

# Start monitoring stack
start_monitoring() {
    if [ "$START_MONITORING" = false ]; then
        print_info "Skipping monitoring stack"
        return
    fi
    
    print_header "Starting Monitoring Stack"
    
    # Create monitoring directories if they don't exist
    mkdir -p monitoring
    
    # Start monitoring services
    docker-compose -f docker-compose.monitoring.yml up -d
    
    print_success "Monitoring stack started"
}

# Wait for services to be healthy
wait_for_services() {
    print_header "Waiting for Services to be Ready"
    
    MAX_WAIT=120
    ELAPSED=0
    
    while [ $ELAPSED -lt $MAX_WAIT ]; do
        if docker ps --filter "health=healthy" | grep -q "store_backend"; then
            print_success "Backend is healthy"
            break
        fi
        
        echo -n "."
        sleep 2
        ELAPSED=$((ELAPSED + 2))
    done
    
    if [ $ELAPSED -ge $MAX_WAIT ]; then
        print_warning "Services may not be fully ready. Check logs with: docker-compose logs"
    fi
}

# Display service URLs
display_urls() {
    print_header "Service URLs"
    
    echo -e "${GREEN}Main Services:${NC}"
    echo "  Frontend:    http://localhost:80"
    echo "  Backend API: http://localhost:5001/api"
    echo "  Health:      http://localhost:5001/health"
    
    if [ "$START_MONITORING" = true ]; then
        echo -e "\n${GREEN}Monitoring:${NC}"
        echo "  Grafana:     http://localhost:3000 (admin/admin123)"
        echo "  Prometheus:  http://localhost:9090"
        echo "  Loki:        http://localhost:3100"
    fi
    
    echo -e "\n${YELLOW}Useful Commands:${NC}"
    echo "  View logs:       docker-compose logs -f [service_name]"
    echo "  Stop all:        ./stop-all.sh"
    echo "  Restart:         docker-compose restart [service_name]"
    echo "  Shell access:    docker-compose exec [service_name] sh"
}

# Main execution
main() {
    print_header "Store ERP - Starting All Services"
    
    check_prerequisites
    stop_existing
    start_main_services
    start_monitoring
    wait_for_services
    display_urls
    
    print_success "All services started successfully!"
    echo -e "\n${BLUE}Tip: Use 'docker-compose logs -f' to view logs${NC}\n"
}

# Run main function
main
