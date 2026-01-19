# ==========================================
# Frontend Dockerfile - Gaara Scan AI v4.3.1
# Multi-stage build for production-ready frontend
# ==========================================

# ==========================================
# Stage 1: Builder - Build React app
# ==========================================
FROM node:20-alpine as builder

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=4.3.1
ARG VITE_API_URL=http://localhost:4001/api
ARG VITE_UPLOAD_URL=http://localhost:4001/uploads

# Set environment variables
ENV NODE_ENV=production \
    VITE_API_URL=${VITE_API_URL} \
    VITE_UPLOAD_URL=${VITE_UPLOAD_URL}

# Install build dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++

# Set working directory
WORKDIR /build

# Copy package files first for better caching
COPY package.json package-lock.json* ./

# Install dependencies with clean install
RUN npm ci --legacy-peer-deps && \
    npm cache clean --force

# Copy source code
COPY . .

# Build application with optimization
RUN npm run build && \
    ls -lh dist/

# ==========================================
# Stage 2: Production - Nginx server
# ==========================================
FROM nginx:1.25-alpine as production

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=4.3.1

# Set labels (OCI standard)
LABEL org.opencontainers.image.title="Gaara Scan AI Frontend" \
      org.opencontainers.image.description="Frontend for Gaara Scan AI System" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Gaara Group & Manus AI" \
      org.opencontainers.image.source="https://github.com/hamfarid/gaara-Scan-system"

# Install curl for healthcheck
RUN apk add --no-cache curl

# Remove default nginx config
RUN rm -rf /etc/nginx/conf.d/*

# Copy built files from builder
COPY --from=builder /build/dist /usr/share/nginx/html

# Create optimized nginx configuration
RUN cat > /etc/nginx/nginx.conf << 'EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/x-javascript
        application/xml
        application/xml+rss
        application/vnd.ms-fontobject
        application/x-font-ttf
        font/opentype
        image/svg+xml
        image/x-icon;

    include /etc/nginx/conf.d/*.conf;
}
EOF

# Create site configuration
RUN cat > /etc/nginx/conf.d/default.conf << 'EOF'
server {
    listen 4501;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # CORS headers (adjust as needed)
    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;

    # SPA routing - serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
        
        # Disable caching for index.html
        location = /index.html {
            add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
            expires off;
        }
    }

    # Cache static assets aggressively
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|webp|avif|woff|woff2|ttf|eot|otf)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # API proxy (optional - if backend is on different host)
    # location /api/ {
    #     proxy_pass http://backend:1005/api/;
    #     proxy_http_version 1.1;
    #     proxy_set_header Upgrade $http_upgrade;
    #     proxy_set_header Connection 'upgrade';
    #     proxy_set_header Host $host;
    #     proxy_cache_bypass $http_upgrade;
    #     proxy_set_header X-Real-IP $remote_addr;
    #     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #     proxy_set_header X-Forwarded-Proto $scheme;
    # }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF

# Use existing nginx user (already exists in nginx:alpine image)
# Adjust permissions for nginx user
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to nginx user (non-root)
USER nginx

# Expose port
EXPOSE 4501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:4501/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
