# 🧠 RAG Architecture & Vector Database Strategy

> **Core Principle**: "Intelligence is not just processing; it is Retrieval + Synthesis."

## 1. The Singularity RAG Stack
When building RAG applications in the Global AI System, you MUST use the following stack:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Vector DB** | **ChromaDB** | Stores embeddings locally with persistence. |
| **LLM Runner** | **Ollama** | Runs local models (Llama 3, Mistral) for inference & embedding. |
| **Orchestrator** | **FastAPI** | Manages the API layer and async processing. |
| **Queue/Cache** | **Redis** | Caches frequent queries and manages ingestion queues. |

## 2. The "Level 12" Workflow

### A. Ingestion (The Knowledge Pipeline)
1.  **Extract**: Read text from PDF, MD, or Web (using `web_scraper.py`).
2.  **Chunk**: Split text into semantic chunks (overlap: 10-20%).
3.  **Embed**: Use `nomic-embed-text` via Ollama API.
4.  **Store**: Save to ChromaDB with rich metadata (`source`, `timestamp`, `author`).

### B. Retrieval (The Search)
1.  **Query Embedding**: Convert user question to vector.
2.  **Semantic Search**: Query ChromaDB for top-k (usually k=3 to 5) nearest neighbors.
3.  **Re-ranking (Optional)**: If high precision is needed, re-rank results using a cross-encoder.

### C. Generation (The Synthesis)
1.  **Context Assembly**: `Prompt = Context + Question`.
2.  **Inference**: Send to Ollama (`llama3`).
3.  **Citation**: The model MUST cite its sources based on the metadata provided.

## 3. Implementation Rules

### 🔴 FORBIDDEN
*   **DO NOT** use remote APIs (OpenAI, Pinecone) unless explicitly requested. We prioritize **Local Sovereignty**.
*   **DO NOT** hardcode model names. Use environment variables (`DEFAULT_LLM_MODEL`).
*   **DO NOT** re-ingest the same document twice. Use document hashes (MD5/SHA256) as IDs.

### 🟢 MUST DO
*   **MUST** use `global/tools/rag_engine.py` for all Chroma/Ollama interactions.
*   **MUST** handle "I don't know" scenarios gracefully.
*   **MUST** persist ChromaDB data to a Docker volume (`chroma_data`).

## 4. Code Pattern (FastAPI + RAG)

```python
# Standard RAG Endpoint Pattern
@app.post("/query")
def query_knowledge(request: QueryRequest):
    # 1. Retrieve
    results = engine.query(request.query)
    
    # 2. Augment
    context = "\n".join(results['documents'][0])
    
    # 3. Generate
    answer = engine.generate_response(request.query, context)
    
    return {"answer": answer, "sources": results['ids'][0]}
```
