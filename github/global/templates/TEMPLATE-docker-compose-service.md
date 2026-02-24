# Template: Docker Compose Service Block

> **Use For**: Adding new services to GAARA-AI docker-compose.yml

## Service Block
```yaml
  gaara-{service}:
    build:
      context: ./services/{service}
      dockerfile: Dockerfile
    container_name: gaara-{service}
    restart: unless-stopped
    ports:
      - "{PORT}:{PORT}"
    environment:
      - SERVICE_NAME={service}
      - REDIS_URL=redis://:${REDIS_PASS}@redis:6379/0
      - DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASS}@postgres:5432/${DB_NAME}
      - OLLAMA_URL=http://gpu-pc:11434
      - QDRANT_URL=http://local-server:6333
    volumes:
      - ./models:/app/models:ro
      - ./logs/{service}:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{PORT}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
    networks:
      - gaara-network
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
```

## GPU Override (docker-compose.gpu.yml)
```yaml
  gaara-{service}:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - CUDA_VISIBLE_DEVICES=0
```
