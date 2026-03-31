# =============================================================================
# Store ERP System - Frontend Dockerfile
# Multi-stage build: Node 20 build + Nginx serve
# =============================================================================

# ==================== BUILD STAGE ====================
FROM node:20-alpine AS builder

WORKDIR /app

# Accept build-time env vars for Vite
ARG VITE_API_URL=
ENV VITE_API_URL=$VITE_API_URL

# Install dependencies (need devDependencies for build)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# ==================== PRODUCTION STAGE ====================
FROM nginx:alpine AS production

LABEL maintainer="Store ERP Team" \
      description="Store ERP System - Frontend"

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Create log directory and set permissions
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
