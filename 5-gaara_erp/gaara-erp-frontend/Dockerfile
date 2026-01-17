# =============================================================================
# Gaara ERP Frontend - Multi-stage Dockerfile
# =============================================================================
# Production-ready React/Vite frontend
# =============================================================================

# =============================================================================
# Stage 1: Builder
# =============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml* package-lock.json* ./

# Install pnpm if not using npm
RUN npm install -g pnpm@latest || true

# Install dependencies
RUN if [ -f "pnpm-lock.yaml" ]; then \
      pnpm install --frozen-lockfile; \
    else \
      npm ci; \
    fi

# Copy source code
COPY . .

# Build arguments
ARG VITE_API_URL=http://localhost:8000/api
ENV VITE_API_URL=${VITE_API_URL}

# Build application
RUN if [ -f "pnpm-lock.yaml" ]; then \
      pnpm build; \
    else \
      npm run build; \
    fi

# =============================================================================
# Stage 2: Production
# =============================================================================
FROM nginx:1.25-alpine AS production

# Security labels
LABEL maintainer="Gaara ERP Team" \
      version="1.0" \
      description="Gaara ERP Frontend"

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create nginx cache directory
RUN mkdir -p /var/cache/nginx/client_temp && \
    chown -R nginx:nginx /var/cache/nginx && \
    chmod -R 755 /var/cache/nginx

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
