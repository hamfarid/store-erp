# AI Agent Prompt: Configure Gaara ERP with Nginx Proxy

Create a Docker Compose configuration for this project with the following specifications:

## Network Configuration
- Network name: `Ai_project`
- Connect all containers to this existing external network

## Port Assignments
- Backend: 5001
- Frontend: 5501
- Database: 10502
- ML Service: 5101
- AI Service: 5601

## Container Names (REQUIRED)
- Backend: `gaara_erp-backend`
- Frontend: `gaara_erp-frontend`
- Database: `gaara_erp-database`
- ML Service: `gaara_erp-ml`
- AI Service: `gaara_erp-ai`

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
    container_name: gaara_erp-backend
    networks:
      - Ai_project
    expose:
      - "5001"
    environment:
      - PORT=5001
      
networks:
  Ai_project:
    external: true
```

## Testing
After setup, the services will be accessible through Nginx at:
- Backend: http://localhost:5001
- Frontend: http://localhost:5501
- ML: http://localhost:5101
- AI: http://localhost:5601
