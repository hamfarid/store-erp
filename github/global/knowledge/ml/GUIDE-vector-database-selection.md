# Vector Database Selection Guide (v30.0 — Feb 2026 Updated)

## 1. Recommendation: Qdrant (Production Default)

As of Feb 2026, **Qdrant** is the recommended vector database for all GAARA-AI production workloads.

## 2. The Big Three: Qdrant vs ChromaDB vs Milvus

| Feature | **Qdrant** ⭐ | ChromaDB | Milvus |
| :--- | :--- | :--- | :--- |
| **Architecture** | Rust Service | Embedded (SQLite) | Distributed (Go) |
| **Setup** | Docker (1 container) | `pip install` | Kubernetes |
| **Scale** | 1M - 100M Vectors | < 1M | > 100M |
| **Speed** | **Very High (Rust)** | Medium | Very High |
| **Hybrid Search** | **✅ Dense + Sparse BM25** | ❌ Dense only | ✅ Dense + Sparse |
| **Metadata Filtering** | **Advanced (conditions)** | Basic | Advanced |
| **Persistence** | **Volume mount** | SQLite file | etcd + MinIO |
| **LangChain Integration** | **langchain-qdrant (official)** | langchain-chroma | langchain-milvus |
| **API** | REST + gRPC | Python only | REST + gRPC |
| **Best For** | **Production AI/RAG** | Prototyping, POC | Enterprise, Big Data |

## 3. When to Use What?

### 3.1 Use Qdrant If (DEFAULT):
*   You need production-grade vector search
*   You want Hybrid Search (Dense + Sparse BM25)
*   You need complex metadata filtering (e.g., "Tomato diseases in Egypt")
*   You run Docker already (single container, no Kubernetes needed)
*   You need Arabic + English multilingual support
*   **GAARA-AI: All 7 collections use Qdrant**

### 3.2 Use ChromaDB If:
*   You are building a quick POC/prototype (< 1 hour)
*   Dataset fits in memory (< 100K vectors)
*   You want zero infrastructure (pip install only)
*   **Note:** ChromaDB 0.5+ has Rust rewrite (4x faster) but still not production-grade

### 3.3 Use Milvus If:
*   Billions of vectors (enterprise scale)
*   Already running Kubernetes cluster
*   Need distributed storage across regions
*   **Not recommended for GAARA-AI** (overkill)

### 3.4 Use pgvector If:
*   Already heavy on PostgreSQL
*   Need ACID + vector search in same DB
*   Moderate scale (< 5M vectors)
*   Want to avoid another service
*   **Can complement Qdrant** for relational + vector queries

## 4. Qdrant for GAARA-AI

### 4.1 Collections
```python
GAARA_COLLECTIONS = {
    "gaara_agricultural":  "Agricultural knowledge, crops, seasons, soil",
    "gaara_products":      "Seed catalog, varieties, specifications",
    "gaara_diseases":      "Plant diseases: symptoms, causes, identification",
    "gaara_nutrients":     "Nutrient deficiency: N, P, K, Ca, Mg, Fe, Mn, Zn, B",
    "gaara_treatments":    "Treatment protocols, fertilizer recommendations",
    "gaara_market":        "Market intelligence, competitor prices",
    "gaara_general":       "General knowledge base, company docs",
}
```

### 4.2 Docker Setup
```yaml
qdrant:
  image: qdrant/qdrant:latest
  container_name: gaara-qdrant
  ports:
    - "6333:6333"    # REST API
    - "6334:6334"    # gRPC
  volumes:
    - qdrant_data:/qdrant/storage
  environment:
    - QDRANT__SERVICE__GRPC_PORT=6334
  restart: unless-stopped
```

### 4.3 Hybrid Search (Key Advantage)
```python
from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse

# Dense: BGE-M3 (semantic understanding)
# Sparse: BM25 (exact keyword matching)
sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

vector_store = QdrantVectorStore.from_documents(
    docs,
    embedding=dense_embeddings,      # BAAI/bge-m3 (768 dims)
    sparse_embedding=sparse_embeddings,
    collection_name="gaara_diseases",
    url="http://qdrant:6333",
    retrieval_mode=RetrievalMode.HYBRID,
)

# Query: combines semantic + keyword results
results = vector_store.similarity_search("نقص النيتروجين في الطماطم", k=5)
```

### 4.4 Metadata Filtering
```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Filter: only Egyptian crops, severity > 3
results = client.search(
    collection_name="gaara_diseases",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="country", match=MatchValue(value="Egypt")),
            FieldCondition(key="severity", range={"gt": 3}),
        ]
    ),
    limit=5,
)
```

## 5. Embedding Model: BGE-M3

| Model | Dims | Languages | Speed | Quality |
|-------|------|-----------|-------|---------|
| **BAAI/bge-m3** ⭐ | 768 | 100+ (Arabic ✅) | Medium | High |
| text-embedding-3-large | 3072 | Multi | API call | Very High |
| all-MiniLM-L6-v2 | 384 | English | Fast | Medium |
| multilingual-e5-large | 1024 | 100+ | Slow | High |

**BGE-M3 is the default** because:
- Supports Arabic + English natively
- 768 dimensions (good balance of quality vs storage)
- Runs locally on CPU via FastEmbed (ONNX)
- Supports Dense + Sparse + ColBERT (multi-vector retrieval)

## 6. Migration from ChromaDB → Qdrant

```python
# Step 1: Export from ChromaDB
import chromadb
old = chromadb.Client()
collection = old.get_collection("my_data")
data = collection.get(include=["documents", "metadatas", "embeddings"])

# Step 2: Import to Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

client = QdrantClient(url="http://qdrant:6333")
points = [
    PointStruct(
        id=i,
        vector=data["embeddings"][i],
        payload={"text": data["documents"][i], **(data["metadatas"][i] or {})}
    )
    for i in range(len(data["documents"]))
]
client.upsert(collection_name="gaara_general", points=points)
```
