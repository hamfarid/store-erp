#!/bin/bash

# ============================================
# Store ERP - Health Check Script
# ============================================
# This script checks the health of all services
# Usage: ./scripts/health-check.sh [--verbose]

set -e  # Exit on error

# ==================== CONFIGURATION ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verbose mode
VERBOSE=false
if [ "$1" = "--verbose" ]; then
    VERBOSE=true
fi

# ==================== FUNCTIONS ====================

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
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

# Check Docker containers
check_containers() {
    print_header "Docker Containers Status"
    
    CONTAINERS=(
        "store_postgres_prod"
        "store_redis_prod"
        "store_backend_prod"
        "store_frontend_prod"
        "store_nginx_prod"
    )
    
    ALL_RUNNING=true
    
    for CONTAINER in "${CONTAINERS[@]}"; do
        STATUS=$(docker inspect -f '{{.State.Status}}' "$CONTAINER" 2>/dev/null || echo "not found")
        
        if [ "$STATUS" = "running" ]; then
            print_success "$CONTAINER is running"
            
            if [ "$VERBOSE" = true ]; then
                UPTIME=$(docker inspect -f '{{.State.StartedAt}}' "$CONTAINER")
                print_info "  Started: $UPTIME"
            fi
        else
            print_error "$CONTAINER is $STATUS"
            ALL_RUNNING=false
        fi
    done
    
    echo ""
    return $([ "$ALL_RUNNING" = true ] && echo 0 || echo 1)
}

# Check PostgreSQL
check_postgres() {
    print_header "PostgreSQL Health Check"
    
    # Check if container is running
    if ! docker ps | grep -q "store_postgres_prod"; then
        print_error "PostgreSQL container is not running"
        return 1
    fi
    
    # Check database connection
    if docker exec store_postgres_prod pg_isready -U "${POSTGRES_USER:-store_user}" -d "${POSTGRES_DB:-store_db}" > /dev/null 2>&1; then
        print_success "PostgreSQL is accepting connections"
    else
        print_error "PostgreSQL is not accepting connections"
        return 1
    fi
    
    # Check database size
    if [ "$VERBOSE" = true ]; then
        DB_SIZE=$(docker exec store_postgres_prod psql -U "${POSTGRES_USER:-store_user}" -d "${POSTGRES_DB:-store_db}" -t -c "SELECT pg_size_pretty(pg_database_size('${POSTGRES_DB:-store_db}'));" 2>/dev/null | xargs)
        print_info "Database size: $DB_SIZE"
        
        # Check active connections
        CONNECTIONS=$(docker exec store_postgres_prod psql -U "${POSTGRES_USER:-store_user}" -d "${POSTGRES_DB:-store_db}" -t -c "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null | xargs)
        print_info "Active connections: $CONNECTIONS"
    fi
    
    echo ""
    return 0
}

# Check Redis
check_redis() {
    print_header "Redis Health Check"
    
    # Check if container is running
    if ! docker ps | grep -q "store_redis_prod"; then
        print_error "Redis container is not running"
        return 1
    fi
    
    # Check Redis connection
    if docker exec store_redis_prod redis-cli ping > /dev/null 2>&1; then
        print_success "Redis is responding to PING"
    else
        print_error "Redis is not responding"
        return 1
    fi
    
    # Check memory usage
    if [ "$VERBOSE" = true ]; then
        MEMORY=$(docker exec store_redis_prod redis-cli INFO memory | grep "used_memory_human" | cut -d: -f2 | tr -d '\r')
        print_info "Memory usage: $MEMORY"
        
        # Check connected clients
        CLIENTS=$(docker exec store_redis_prod redis-cli INFO clients | grep "connected_clients" | cut -d: -f2 | tr -d '\r')
        print_info "Connected clients: $CLIENTS"
    fi
    
    echo ""
    return 0
}

# Check Backend API
check_backend() {
    print_header "Backend API Health Check"
    
    # Check if container is running
    if ! docker ps | grep -q "store_backend_prod"; then
        print_error "Backend container is not running"
        return 1
    fi
    
    # Check health endpoint
    BACKEND_PORT=${BACKEND_PORT:-5000}
    HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$BACKEND_PORT/health 2>/dev/null || echo "000")
    
    if [ "$HEALTH_RESPONSE" = "200" ]; then
        print_success "Backend health endpoint is responding (HTTP 200)"
    else
        print_error "Backend health endpoint failed (HTTP $HEALTH_RESPONSE)"
        return 1
    fi
    
    # Check API endpoint
    API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$BACKEND_PORT/api/health 2>/dev/null || echo "000")
    
    if [ "$API_RESPONSE" = "200" ]; then
        print_success "Backend API is responding (HTTP 200)"
    else
        print_warning "Backend API endpoint returned HTTP $API_RESPONSE"
    fi
    
    # Verbose checks
    if [ "$VERBOSE" = true ]; then
        # Check response time
        RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:$BACKEND_PORT/health 2>/dev/null || echo "0")
        print_info "Response time: ${RESPONSE_TIME}s"
        
        # Check container logs for errors
        ERROR_COUNT=$(docker logs store_backend_prod --since 1h 2>&1 | grep -i "error" | wc -l)
        if [ "$ERROR_COUNT" -gt 0 ]; then
            print_warning "Found $ERROR_COUNT errors in logs (last 1 hour)"
        else
            print_info "No errors in logs (last 1 hour)"
        fi
    fi
    
    echo ""
    return 0
}

# Check Frontend
check_frontend() {
    print_header "Frontend Health Check"
    
    # Check if container is running
    if ! docker ps | grep -q "store_frontend_prod"; then
        print_error "Frontend container is not running"
        return 1
    fi
    
    # Check frontend endpoint
    FRONTEND_PORT=${FRONTEND_PORT:-80}
    FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$FRONTEND_PORT/ 2>/dev/null || echo "000")
    
    if [ "$FRONTEND_RESPONSE" = "200" ]; then
        print_success "Frontend is responding (HTTP 200)"
    else
        print_error "Frontend failed (HTTP $FRONTEND_RESPONSE)"
        return 1
    fi
    
    # Verbose checks
    if [ "$VERBOSE" = true ]; then
        # Check response time
        RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:$FRONTEND_PORT/ 2>/dev/null || echo "0")
        print_info "Response time: ${RESPONSE_TIME}s"
    fi
    
    echo ""
    return 0
}

# Check disk space
check_disk_space() {
    print_header "Disk Space Check"
    
    # Check available disk space
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$DISK_USAGE" -lt 80 ]; then
        print_success "Disk usage is healthy ($DISK_USAGE%)"
    elif [ "$DISK_USAGE" -lt 90 ]; then
        print_warning "Disk usage is high ($DISK_USAGE%)"
    else
        print_error "Disk usage is critical ($DISK_USAGE%)"
    fi
    
    # Check Docker volumes
    if [ "$VERBOSE" = true ]; then
        print_info "Docker volumes:"
        docker volume ls | grep store
    fi
    
    echo ""
}

# Check resource usage
check_resources() {
    print_header "Resource Usage Check"
    
    # Check CPU usage
    if command -v top &> /dev/null; then
        CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
        print_info "CPU usage: ${CPU_USAGE}%"
    fi
    
    # Check memory usage
    if command -v free &> /dev/null; then
        MEMORY_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
        print_info "Memory usage: ${MEMORY_USAGE}%"
    fi
    
    # Check Docker stats
    if [ "$VERBOSE" = true ]; then
        print_info "Docker container stats:"
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep store
    fi
    
    echo ""
}

# Generate summary
generate_summary() {
    print_header "Health Check Summary"
    
    if [ $TOTAL_FAILURES -eq 0 ]; then
        echo -e "${GREEN}✓ All health checks passed!${NC}"
    else
        echo -e "${RED}✗ $TOTAL_FAILURES health check(s) failed${NC}"
    fi
    
    echo ""
    echo "Timestamp: $(date)"
    echo ""
}

# ==================== MAIN ====================

main() {
    cd "$PROJECT_ROOT"
    
    # Load environment variables
    if [ -f ".env.production" ]; then
        export $(cat .env.production | grep -v '^#' | xargs)
    fi
    
    TOTAL_FAILURES=0
    
    # Run all health checks
    check_containers || ((TOTAL_FAILURES++))
    check_postgres || ((TOTAL_FAILURES++))
    check_redis || ((TOTAL_FAILURES++))
    check_backend || ((TOTAL_FAILURES++))
    check_frontend || ((TOTAL_FAILURES++))
    check_disk_space
    
    if [ "$VERBOSE" = true ]; then
        check_resources
    fi
    
    generate_summary
    
    # Exit with failure if any check failed
    exit $TOTAL_FAILURES
}

# Run main function
main "$@"

