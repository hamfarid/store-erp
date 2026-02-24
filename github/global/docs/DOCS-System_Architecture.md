# System Architecture

## Overview
The Global System v26.0 is built on a microservices architecture, utilizing a swarm of specialized AI agents.

### Components
- **Frontend:** React/Next.js
- **Backend:** Django/FastAPI
- **AI Core:** MCP (Model Context Protocol)
- **Database:** PostgreSQL/Redis

### Data Flow
1. User interacts with the Frontend.
2. Request is routed to the Backend via API Gateway.
3. Backend invokes AI Agents via MCP.
4. Agents process data and return results.
