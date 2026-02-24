# GUIDE-rag-qdrant-langchain-2026.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. 2026 RAG Landscape

**Key changes from 2024/2025:**
- LangChain 0.3+ with LCEL (LangChain Expression Language) is standard
- Qdrant dominates self-hosted production (Rust performance, Hybrid Search)
- ChromaDB relegated to prototyping only
- Hybrid Search (Dense + Sparse BM25) is default — not just dense vectors
- BGE-M3 is the go-to multilingual embedding model (Arabic + English)
- Local LLMs via Ollama are production-viable for RAG

## 2. Architecture

```
Document → Chunk → Embed (BGE-M3) → Store (Qdrant)
                                          │
Query → Embed → Hybrid Search ────────────┘
                    │
                    ▼
            Top-K Results + Query → LLM (Ollama) → Answer
```

## 3. Components

### 3.1 Embedding Model: BGE-M3
- **Model:** `BAAI/bge-m3`
- **Dimensions:** 768
- **Languages:** 100+ (including Arabic, English)
- **Supports:** Dense + Sparse + ColBERT (multi-vector)
- **Run on CPU:** Via FastEmbed (ONNX-based)

```python
from fastembed import TextEmbedding
model = TextEmbedding("BAAI/bge-m3")
embeddings = list(model.embed(["نقص النيتروجين في الطماطم"]))
```

### 3.2 Vector Database: Qdrant
- **Version:** 1.13+
- **Features:** Hybrid Search (Dense + Sparse BM25), metadata filtering
- **Docker:** `qdrant/qdrant:latest` on port 6333
- **Persistence:** Volume mount `/qdrant/storage`

### 3.3 LLM: Ollama (Local)
- **Models:** Qwen 2.5 (7B for Arabic), Phi-3 Mini (3.8B for CPU), Llama 3.1 (8B with GPU)
- **Docker:** `ollama/ollama:latest` on port 11434

## 4. Qdrant Collections (GAARA-AI)

```python
# scripts/init_qdrant_collections.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(url="http://qdrant:6333")

COLLECTIONS = {
    "gaara_agricultural": "Agricultural knowledge (crops, seasons, soil)",
    "gaara_products": "Seed catalog, varieties, specifications",
    "gaara_diseases": "Plant diseases database",
    "gaara_nutrients": "Nutrient deficiency information",
    "gaara_treatments": "Treatment protocols and fertilizers",
    "gaara_market": "Market intelligence, prices, competitors",
    "gaara_general": "General knowledge base",
}

for name, description in COLLECTIONS.items():
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
```

## 5. RAG Service Implementation

```python
# services/rag_service.py
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

class GAARARAGService:
    def __init__(self):
        # Embedding: BGE-M3 on CPU via ONNX
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={'device': 'cpu'}
        )
        # LLM: Ollama local
        self.llm = Ollama(
            base_url="http://ollama:11434",
            model="qwen2.5:7b",
            temperature=0.3
        )
        # Qdrant client
        self.qdrant = QdrantClient(url="http://qdrant:6333")
        # Text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120,
            separators=["\n\n", "\n", ".", "!", "?", "،", " "]  # Arabic-aware
        )

    def add_knowledge(self, text, category="general", metadata=None):
        """Chunk → Embed → Store in Qdrant"""
        collection = f"gaara_{category}"
        chunks = self.splitter.split_text(text)

        vector_store = QdrantVectorStore(
            client=self.qdrant,
            collection_name=collection,
            embedding=self.embeddings,
        )
        vector_store.add_texts(
            texts=chunks,
            metadatas=[{**(metadata or {}), "chunk_index": i} for i in range(len(chunks))]
        )
        return len(chunks)

    def search(self, query, category="general", top_k=5):
        """Semantic search in Qdrant"""
        collection = f"gaara_{category}"
        vector_store = QdrantVectorStore(
            client=self.qdrant,
            collection_name=collection,
            embedding=self.embeddings,
        )
        results = vector_store.similarity_search_with_score(query, k=top_k)
        return [{"text": doc.page_content, "score": score, "metadata": doc.metadata}
                for doc, score in results]

    def ask(self, question, category="general"):
        """Full RAG: Search → Retrieve → Augment → Generate"""
        collection = f"gaara_{category}"
        vector_store = QdrantVectorStore(
            client=self.qdrant,
            collection_name=collection,
            embedding=self.embeddings,
        )
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True,
            chain_type="stuff"  # Combine all docs into one prompt
        )
        result = qa_chain.invoke({"query": question})
        return {
            "answer": result["result"],
            "sources": [
                {"text": doc.page_content[:200], "metadata": doc.metadata}
                for doc in result.get("source_documents", [])
            ]
        }
```

## 6. Hybrid Search (Dense + Sparse BM25)

For best accuracy, combine semantic (dense) and keyword (sparse) search:

```python
from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse

# Hybrid: Dense BGE-M3 + Sparse BM25
sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

vector_store = QdrantVectorStore.from_documents(
    docs,
    embedding=dense_embeddings,
    sparse_embedding=sparse_embeddings,
    collection_name="gaara_agricultural",
    url="http://qdrant:6333",
    retrieval_mode=RetrievalMode.HYBRID,  # Both dense + sparse
)
```

## 7. Requirements

```
langchain>=0.3.0
langchain-community>=0.3.0
langchain-qdrant>=0.2.0
langchain-text-splitters>=0.3.0
qdrant-client>=1.13.0
fastembed>=0.4.0
sentence-transformers>=3.3.0
```

## 8. Migration from ChromaDB

If your project currently uses ChromaDB:

| ChromaDB | Qdrant Equivalent |
|----------|-------------------|
| `chromadb.Client()` | `QdrantClient(url="http://qdrant:6333")` |
| `collection.add()` | `vector_store.add_texts()` |
| `collection.query()` | `vector_store.similarity_search()` |
| In-memory | Docker service with volume persistence |
| No filtering | Advanced metadata filtering with conditions |
| No hybrid search | Dense + Sparse BM25 hybrid |
