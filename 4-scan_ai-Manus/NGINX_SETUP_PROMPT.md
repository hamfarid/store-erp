# AI Agent Prompt: Configure Scan AI-Manus with Nginx Proxy

Create a Docker Compose configuration for this project with the following specifications:

## Network Configuration
- Network name: `Ai_project`
- Connect all containers to this existing external network

## Port Assignments
- Backend: 4001
- Frontend: 4501
- Database: 8502
- ML Service: 4101
- AI Service: 4601

## Container Names (REQUIRED)
- Backend: `scan_ai-Manus-backend`
- Frontend: `scan_ai-Manus-frontend`
- Database: `scan_ai-Manus-database`
- ML Service: `scan_ai-Manus-ml`
- AI Service: `scan_ai-Manus-ai`

## Requirements
1. Create `docker-compose.yml` file with all services
2. Each service must:
   - Use the exact container name specified above
   - Connect to the `Ai_project` network
   - Expose the assigned port internally
   - Do NOT publish ports to host (Nginx handles this)
3. Add health checks for each service
4. Include proper environment variables
5. Add volume mounts for data persistence

## Network Setup Command
```bash
docker network create Ai_project
```

## Example Service Configuration
```yaml
services:
  backend:
    container_name: scan_ai-Manus-backend
    networks:
      - Ai_project
    expose:
      - "4001"
    environment:
      - PORT=4001
      
networks:
  Ai_project:
    external: true
```

## Testing
After setup, the services will be accessible through Nginx at:
- Backend: http://localhost:4001
- Frontend: http://localhost:4501
- ML: http://localhost:4101
- AI: http://localhost:4601
