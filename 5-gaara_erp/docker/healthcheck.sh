#!/bin/bash
# FILE: /home/ubuntu/gaara-erp-v12/docker/healthcheck.sh
# PURPOSE: Docker health check script لـ Gaara ERP v12
# OWNER: Manus AI | LAST-AUDITED: 2025-01-01
# OSF PRIORITY: Reliability (15%) - Critical Implementation

set -e

# Configuration
HEALTH_CHECK_URL="http://localhost:8000/health/"
TIMEOUT=10
MAX_RETRIES=3

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] [HEALTH-CHECK] $1" >&2
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] [HEALTH-CHECK] [SUCCESS]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] [HEALTH-CHECK] [ERROR]${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] [HEALTH-CHECK] [WARNING]${NC} $1" >&2
}

# Function to check HTTP endpoint
check_http_endpoint() {
    local url=$1
    local timeout=${2:-10}
    
    if command -v curl >/dev/null 2>&1; then
        # Use curl if available
        if curl -f -s --max-time "$timeout" "$url" >/dev/null 2>&1; then
            return 0
        else
            return 1
        fi
    elif command -v wget >/dev/null 2>&1; then
        # Use wget as fallback
        if wget -q --timeout="$timeout" --tries=1 -O /dev/null "$url" >/dev/null 2>&1; then
            return 0
        else
            return 1
        fi
    else
        # Use Python as last resort
        if python3 -c "
import urllib.request
import socket
socket.setdefaulttimeout($timeout)
try:
    urllib.request.urlopen('$url')
    exit(0)
except:
    exit(1)
" >/dev/null 2>&1; then
            return 0
        else
            return 1
        fi
    fi
}

# Function to check database connectivity
check_database() {
    log "Checking database connectivity..."
    
    if python manage.py check --database default >/dev/null 2>&1; then
        log_success "Database connection OK"
        return 0
    else
        log_error "Database connection failed"
        return 1
    fi
}

# Function to check Redis connectivity
check_redis() {
    log "Checking Redis connectivity..."
    
    if python -c "
import redis
import os
from urllib.parse import urlparse

try:
    redis_url = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')
    parsed = urlparse(redis_url)
    r = redis.Redis(
        host=parsed.hostname or 'localhost', 
        port=parsed.port or 6379, 
        db=int(parsed.path[1:]) if parsed.path else 0,
        socket_connect_timeout=5,
        socket_timeout=5
    )
    r.ping()
    print('Redis connection OK')
except Exception as e:
    print(f'Redis connection failed: {e}')
    exit(1)
" >/dev/null 2>&1; then
        log_success "Redis connection OK"
        return 0
    else
        log_warning "Redis connection failed (non-critical)"
        return 0  # Don't fail health check for Redis
    fi
}

# Function to check application health
check_application_health() {
    log "Checking application health..."
    
    # Check if Django is responding
    if check_http_endpoint "http://localhost:8000/admin/login/" "$TIMEOUT"; then
        log_success "Application responding OK"
        return 0
    else
        log_error "Application not responding"
        return 1
    fi
}

# Function to check system resources
check_system_resources() {
    log "Checking system resources..."
    
    # Check memory usage
    if command -v free >/dev/null 2>&1; then
        local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
        if [ "$mem_usage" -gt 90 ]; then
            log_warning "High memory usage: ${mem_usage}%"
        else
            log "Memory usage: ${mem_usage}%"
        fi
    fi
    
    # Check disk usage
    if command -v df >/dev/null 2>&1; then
        local disk_usage=$(df /app | tail -1 | awk '{print $5}' | sed 's/%//')
        if [ "$disk_usage" -gt 90 ]; then
            log_warning "High disk usage: ${disk_usage}%"
        else
            log "Disk usage: ${disk_usage}%"
        fi
    fi
    
    return 0
}

# Function to check security features
check_security_features() {
    log "Checking security features..."
    
    # Check if MFA is properly configured
    if python -c "
from security.mfa import MFAManager
from security.rate_limiting import RateLimitRule

try:
    # Check if security models are accessible
    rule_count = RateLimitRule.objects.count()
    print(f'Rate limiting rules: {rule_count}')
    
    # Check MFA configuration
    mfa_manager = MFAManager()
    print('MFA system initialized')
    
    print('Security features OK')
except Exception as e:
    print(f'Security check failed: {e}')
    exit(1)
" >/dev/null 2>&1; then
        log_success "Security features OK"
        return 0
    else
        log_warning "Security features check failed (non-critical)"
        return 0  # Don't fail health check for security features during startup
    fi
}

# Function to perform comprehensive health check
perform_health_check() {
    local checks_passed=0
    local total_checks=5
    
    log "Starting comprehensive health check..."
    
    # Database check (critical)
    if check_database; then
        checks_passed=$((checks_passed + 1))
    else
        log_error "Critical: Database check failed"
        return 1
    fi
    
    # Redis check (non-critical)
    if check_redis; then
        checks_passed=$((checks_passed + 1))
    fi
    
    # Application health check (critical)
    if check_application_health; then
        checks_passed=$((checks_passed + 1))
    else
        log_error "Critical: Application health check failed"
        return 1
    fi
    
    # System resources check (non-critical)
    if check_system_resources; then
        checks_passed=$((checks_passed + 1))
    fi
    
    # Security features check (non-critical)
    if check_security_features; then
        checks_passed=$((checks_passed + 1))
    fi
    
    log "Health check completed: $checks_passed/$total_checks checks passed"
    
    # Require at least 3 critical checks to pass
    if [ $checks_passed -ge 3 ]; then
        log_success "Health check PASSED"
        return 0
    else
        log_error "Health check FAILED"
        return 1
    fi
}

# Function to check if application is starting up
is_starting_up() {
    # Check if this is within the first 2 minutes of container startup
    if [ -f /tmp/container_start_time ]; then
        local start_time=$(cat /tmp/container_start_time)
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        if [ $elapsed -lt 120 ]; then  # 2 minutes
            return 0
        fi
    else
        # Create start time file
        date +%s > /tmp/container_start_time
        return 0
    fi
    
    return 1
}

# Main health check function
main() {
    local retry_count=0
    
    # During startup, be more lenient
    if is_starting_up; then
        log "Container is starting up, performing basic health check..."
        
        # Just check if the process is running
        if pgrep -f "gunicorn\|python.*manage.py" >/dev/null 2>&1; then
            log_success "Application process is running"
            exit 0
        else
            log_warning "Application process not found, but container is still starting up"
            exit 0  # Don't fail during startup
        fi
    fi
    
    # Perform full health check with retries
    while [ $retry_count -lt $MAX_RETRIES ]; do
        if perform_health_check; then
            exit 0
        fi
        
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $MAX_RETRIES ]; then
            log "Health check failed, retrying ($retry_count/$MAX_RETRIES)..."
            sleep 2
        fi
    done
    
    log_error "Health check failed after $MAX_RETRIES attempts"
    exit 1
}

# Handle signals
trap 'log "Health check interrupted"; exit 1' INT TERM

# Run main function
main "$@"
