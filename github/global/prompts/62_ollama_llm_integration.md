# Prompt 62: Ollama LLM Integration

> **Scope**: Local LLM service via Ollama for GAARA-AI
> **Container**: gaara-llm (port 11434)

## Service Design

Ollama runs as a Docker container providing local LLM inference. No API keys needed, fully private.

### Recommended Models
| Model | Size | Use Case | Arabic Support |
|:------|:-----|:---------|:--------------|
| Qwen2.5:7b | 4.7GB | Primary — chat, summarize, RAG | Excellent |
| Qwen2.5:1.5b | 1.1GB | CPU-only fallback | Good |
| Phi-3-mini | 2.3GB | Fast inference, code | Limited |
| Llama 3.1:8b | 4.7GB | General purpose | Moderate |
| nomic-embed-text | 274MB | Embeddings only | Good |

### API Usage
```python
import httpx

# Text Generation
response = await httpx.post("http://ollama:11434/api/generate", json={
    "model": "qwen2.5:7b",
    "prompt": "...",
    "temperature": 0.7,
    "stream": False
})

# Chat
response = await httpx.post("http://ollama:11434/api/chat", json={
    "model": "qwen2.5:7b",
    "messages": [{"role": "user", "content": "..."}],
    "stream": False
})

# Embeddings
response = await httpx.post("http://ollama:11434/api/embed", json={
    "model": "nomic-embed-text",
    "input": "text to embed"
})
```

### Rules
- Always use `stream: False` for Celery tasks (stream only for real-time chat)
- Set `OLLAMA_NUM_PARALLEL=2` and `OLLAMA_MAX_LOADED_MODELS=2` for CPU
- Health check: `GET http://ollama:11434/api/tags`
- GPU override: uncomment deploy.resources.reservations in docker-compose.gpu.yml
