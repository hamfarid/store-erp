# 🐳 Container Workflow

This guide explains the **Smart Port Orchestration** and **Dynamic Networking** architecture. It covers how to work with containers, link them, and troubleshoot networking issues in both Docker and Host-Only modes.

---

## 🧠 The Architecture

The system uses a **Dynamic Port Allocation** strategy based on user input. This ensures no port conflicts and allows multiple instances of the system to run on the same machine.

### 🔢 Port Logic
*   **Backend:** User Input (Default: `8000`)
*   **Frontend:** User Input (Default: `3000`)
*   **Redis:** Backend + Frontend (e.g., `11000`)
*   **Database:** Backend + 100 (e.g., `8100`)
*   **AI Service:** Backend + 200 (e.g., `8200`)
*   **ML Service:** Frontend + 100 (e.g., `3100`)

### 🌐 The Network (`global_neural_net`)
All containers are connected via a custom bridge network called `global_neural_net`. This allows them to communicate using **service names** instead of IP addresses.

| Service Name | Description | Internal Port | External Port |
|---|---|---|---|
| `global_nginx` | Reverse Proxy | `80` | `80` (Host) |
| `global_backend` | API Server | `8000` | Calculated |
| `global_frontend` | UI Server | `3000` | Calculated |
| `global_redis` | Cache/Queue | `6379` | Calculated |
| `global_ollama` | AI Model Runner | `11434` | Calculated |
| `global_chroma` | Vector DB | `8000` | `8000` |

---

## 🚀 Workflow: Starting the System

### 1. Run Genesis
The entry point is always `genesis.py`. It will ask for your base ports and generate the necessary configurations.

```bash
python3 genesis.py
```

### 2. Verify Nginx Config
Genesis automatically generates `nginx/nginx.conf`. Verify it maps to your calculated ports:

```nginx
upstream backend {
    server localhost:8000; # Should match your input
}
```

### 3. Start Containers
If you are in Docker mode, Genesis starts them automatically. To restart manually:

```bash
docker-compose -f infrastructure/docker-compose.shared.yml up -d
```

---

## 🔗 Linking Containers

To connect a new service (e.g., a new Microservice) to the network:

1.  **Add to Network:** Ensure your `docker-compose.yml` includes:
    ```yaml
    networks:
      - global_neural_net
    ```

2.  **Use Service Names:** Inside your code, refer to other services by name:
    *   Redis: `redis://global_redis:6379`
    *   Ollama: `http://global_ollama:11434`
    *   Backend: `http://global_backend:8000`

---

## 🛠️ Troubleshooting

### ❌ "Port Already in Use"
*   **Cause:** You chose a base port that conflicts with an existing service.
*   **Fix:** Run `genesis.py` again and choose a different Backend/Frontend port pair.

### ❌ "502 Bad Gateway" (Nginx)
*   **Cause:** The backend or frontend container is not running or not reachable.
*   **Fix:** Check logs: `docker logs global_backend`. Ensure they are on the `global_neural_net`.

### ❌ Host-Only Mode Issues
*   **Note:** In Host-Only mode, there is no Docker network. Services run on `localhost` at the calculated ports.
*   **Fix:** Ensure your `.env` files point to `localhost` instead of service names (e.g., `REDIS_HOST=localhost`).

---

## 🔄 Zero-Downtime Updates

### Docker Mode
The system uses **Rolling Updates**. To update a service:

```bash
docker-compose -f infrastructure/docker-compose.shared.yml up -d --no-deps --build <service_name>
```

### Host-Only Mode
Use the `speckit` process manager:

```bash
python3 tools/speckit.py manage --service backend --cmd "uvicorn main:app --port 8000"
```
