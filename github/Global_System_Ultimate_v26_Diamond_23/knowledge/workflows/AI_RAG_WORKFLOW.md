# 🧠 AI & RAG Operations Workflow (AI Learning Guide)

This document teaches the AI how to manage Vector Databases, Embeddings, and LLM interactions.

## 1. Standard RAG Module Structure
Every RAG module (e.g., `rag_engine.py`, `context_retriever.py`) must follow this pattern:

### 📥 Imports (Inputs)
*   **Vector DB Client**: `chromadb`, `pinecone`, `qdrant`.
*   **Embedding Model**: `sentence-transformers`, `openai`.
*   **LLM Client**: `langchain`, `openai`, `anthropic`.

### 📤 Exports (Outputs)
*   **Ingest Function**: Adds text to memory.
*   **Query Function**: Retrieves relevant context.
*   **Generation Function**: Produces answers based on context.

### 🔄 Operational Workflow
1.  **Ingestion**: Chunk text -> Embed -> Store in Vector DB.
2.  **Retrieval**: Query -> Embed -> Semantic Search -> Return Top-K chunks.
3.  **Synthesis**: Prompt + Context -> LLM -> Answer.

## 2. Example: Simple RAG Engine

```python
# tools/rag_engine.py

# 📥 IMPORTS
import chromadb
from chromadb.utils import embedding_functions

# 🔄 WORKFLOW
# 1. Connect to ChromaDB.
# 2. Get collection.
# 3. Add documents with IDs and Metadata.
# 4. Query documents by text.

# 📤 EXPORTS
class RAGEngine:
    def __init__(self):
        self.client = chromadb.Client()
        self.fn = embedding_functions.DefaultEmbeddingFunction()

    def ingest(self, text, metadata):
        collection = self.client.get_or_create_collection("memory")
        collection.add(documents=[text], metadatas=[metadata], ids=[str(hash(text))])

    def query(self, text):
        collection = self.client.get_collection("memory")
        return collection.query(query_texts=[text], n_results=3)
```

## 3. AI Action Items
*   **Chunking**: Split large texts into meaningful segments (e.g., paragraphs).
*   **Metadata**: Always attach source, timestamp, and author to embeddings.
*   **Relevance**: Filter results by distance score to avoid hallucination.
