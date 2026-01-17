# AI Agent Prompt: Configure Store Project with Nginx Proxy

Create a Docker Compose configuration for this project with the following specifications:

## Network Configuration
- Network name: `Ai_project`
- Connect all containers to this existing external network

## Port Assignments
- Backend: 6001
- Frontend: 6501
- Database: 12502
- ML Service: 6101
- AI Service: 6601

## Container Names (REQUIRED)
- Backend: `store-backend`
- Frontend: `store-frontend`
- Database: `store-database`
- ML Service: `store-ml`
- AI Service: `store-ai`

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
    container_name: store-backend
    networks:
      - Ai_project
    expose:
      - "6001"
    environment:
      - PORT=6001
      
networks:
  Ai_project:
    external: true
```

## Testing
After setup, the services will be accessible through Nginx at:
- Backend: http://localhost:6001
- Frontend: http://localhost:6501
- ML: http://localhost:6101
- AI: http://localhost:6601
