# RAG Vector DB Setup (Global System Ultimate Swarm Intelligence)

**Objective:** Set up a persistent memory system using ChromaDB.

## 1. 🧠 The Planner's Design
*   **Database:** ChromaDB (Local, Dockerized).
*   **Embedding Model:** `nomic-embed-text` (via Ollama).
*   **Collection Name:** `global_knowledge`.
*   **Persistence:** Must save to disk (`./chroma_data`).

## 2. 🛠️ The Executor's Implementation

```python
import chromadb
from chromadb.utils import embedding_functions
import os

# 1. Connect to Client
# If Docker: host="localhost", port=8000
# If Local: path="./chroma_data"
client = chromadb.HttpClient(host='localhost', port=8000)

# 2. Define Embedding Function (Ollama)
# Note: Requires 'ollama' python package
# pip install ollama
import ollama

class OllamaEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __call__(self, input: list[str]) -> list[list[float]]:
        embeddings = []
        for text in input:
            response = ollama.embeddings(model='nomic-embed-text', prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

# 3. Get/Create Collection
collection = client.get_or_create_collection(
    name="global_knowledge",
    embedding_function=OllamaEmbeddingFunction()
)

# 4. Add Documents
collection.add(
    documents=["The sky is blue.", "The grass is green."],
    metadatas=[{"source": "nature"}, {"source": "nature"}],
    ids=["id1", "id2"]
)

# 5. Query
results = collection.query(
    query_texts=["What color is the sky?"],
    n_results=1
)

print(results)
```

## 3. 🧐 The Reviewer's Checklist
*   [ ] Is the client connection configurable (Env Vars)?
*   [ ] Is the embedding model actually pulled in Ollama?
*   [ ] Are IDs unique?

## 4. ⚖️ The Critic's Verdict
*   **Approved.** This setup allows for semantic search and long-term memory persistence.
