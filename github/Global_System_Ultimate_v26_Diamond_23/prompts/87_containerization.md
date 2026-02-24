# PROMPT 87: CONTAINERIZATION & ORCHESTRATION PROTOCOL

**Objective:** Ensure all containerized applications are secure, efficient, and conflict-free, with specialized support for AI, Data, and Full-Stack workloads.

---

## 🐳 CORE PRINCIPLES

1.  **Immutability:** Containers MUST be immutable. Configuration MUST be injected via environment variables.
2.  **Least Privilege:** Containers MUST NOT run as root. Use a specific `USER` instruction.
3.  **Port Discipline:** Exposed ports MUST be explicitly defined and checked for conflicts.
4.  **Health Checks:** Every container MUST have a `HEALTHCHECK` instruction.

---

## 🧠 SPECIALIZED CONTAINER SPECS (Mandatory)

### 1. Full-Stack Scraper Architecture (Web + Scraper + DB + Redis)
*   **Orchestration:** MUST use `docker-compose` to link all services.
*   **Service Roles:**
    *   `app`: The main web application/API.
    *   `scraper`: The worker container (often headless browser).
    *   `redis`: The message broker for job queues and caching.
    *   `postgres`: The persistent storage for scraped data.
*   **Networking:**
    *   `backend`: Private network for App <-> DB <-> Redis <-> Scraper communication.
    *   `frontend`: Public network for App <-> Internet (if needed).
*   **Scaling:** Scraper containers should be stateless to allow `docker compose up -d --scale scraper=5`.

### 2. AI Inference Containers (e.g., Ollama, vLLM, Triton)
*   **GPU Access:** MUST configure NVIDIA Runtime or equivalent.
    ```yaml
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    ```
*   **Model Caching:** MUST mount a host volume for model weights to avoid re-downloading.
    *   Example: `-v ./models:/root/.ollama`
*   **Resource Limits:** MUST set `shm_size` to at least `8gb` for large models.

### 3. Learning & Training Containers (e.g., Jupyter, PyTorch Training)
*   **Workspace Persistence:** MUST mount a local workspace volume.
*   **Interactive Access:** Expose ports `8888` (Jupyter) or `6006` (TensorBoard) ONLY if needed.
*   **Environment:** Inject `HUGGING_FACE_HUB_TOKEN` and `WANDB_API_KEY` via secrets.

### 4. Search & Knowledge Containers (e.g., Qdrant, Meilisearch, Elasticsearch)
*   **Data Persistence:** MUST use named volumes for vector stores.
*   **Memory Optimization:** Configure `mem_limit` to prevent OOM kills during indexing.
*   **Snapshots:** Configure automated snapshot volumes.

### 5. Auxiliary/Helper Containers (e.g., Redis, Postgres, RabbitMQ)
*   **Network Isolation:** MUST be on a backend-only network, not exposed to the host unless for debugging.
*   **Initialization:** Use `/docker-entrypoint-initdb.d` for seeding initial data.

---

## 🛡️ PRE-FLIGHT CHECKLIST (Mandatory)

Before starting any container, the AI MUST perform the following checks:

1.  **File Integrity:**
    *   Does `Dockerfile` exist?
    *   Does `docker-compose.yml` exist?
    *   Are `.dockerignore` files present?

2.  **Port Management (Interactive):**
    *   Scan `docker-compose.yml` for `ports` mapping.
    *   **INTERACTIVE STEP:** The AI MUST ask the user: *"Do you want to use the default ports or specify custom ports?"*
    *   Verify that the selected ports are available on the host system.

3.  **Resource Validation:**
    *   If AI container: Check if Host has GPU drivers installed (via `nvidia-smi`).
    *   If Search container: Check if Host has sufficient disk space for indices.
    *   If Scraper container: Check if Redis is configured and available.

---

## 📝 DOCKERFILE STANDARDS

```dockerfile
# ✅ GOOD (Production AI Service)
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

---

## 🔄 WORKFLOW INTEGRATION

1.  **Analyze:** Detect container type (Web vs AI vs Search vs Scraper).
2.  **Ask:** Query user for port/config preferences.
3.  **Provision:** Auto-add dependencies (e.g., Redis for Scrapers).
4.  **Validate:** Run `docker compose config` and resource checks.
5.  **Build:** Run `docker compose build`.
6.  **Run:** Run `docker compose up -d`.
7.  **Verify:** Check logs and health status.
