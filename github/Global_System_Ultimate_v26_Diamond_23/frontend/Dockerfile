# Global System Ultimate - Frontend Dockerfile
# Verified Feb 2026: Node 22-alpine + Dynamic Ports

FROM node:22-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

# Smart Port Orchestration: Port is injected at runtime via $PORT
CMD ["sh", "-c", "npm run dev -- --host 0.0.0.0 --port ${PORT:-3000}"]
