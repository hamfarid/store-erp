# 🧠 AI & RAG Operations Workflow (v30.0 — Feb 2026 Updated)

This document teaches the AI how to manage Vector Databases, Embeddings, and LLM interactions
using the **2026 production stack**: Qdrant + LangChain 0.3 + BGE-M3 + Ollama.

## 1. Standard RAG Module Structure (2026)

### 📥 Components
*   **Vector DB:** Qdrant (production) or ChromaDB (prototyping only)
*   **Embedding Model:** BGE-M3 (768 dims, Arabic+English, via FastEmbed/ONNX)
*   **LLM:** Ollama local (Qwen 2.5 7B for Arabic, Llama 3.1 8B for English)
*   **Framework:** LangChain 0.3+ with LCEL (LangChain Expression Language)
*   **Search Mode:** Hybrid (Dense semantic + Sparse BM25)

### 📤 Exports
*   **Ingest Function:** Chunk → Embed → Store in Qdrant
*   **Search Function:** Query → Embed → Hybrid Search → Return Top-K
*   **Ask Function (RAG):** Query → Search → Augment → LLM Generate → Answer

### 🔄 Operational Workflow
1.  **Ingestion:** Text → RecursiveCharacterTextSplitter(800, 120) → BGE-M3 embed → Qdrant upsert
2.  **Retrieval:** Query → BGE-M3 embed → Hybrid Search (Dense + Sparse BM25) → Top-5 chunks
3.  **Synthesis:** System prompt + Retrieved chunks + User query → Ollama LLM → Answer (Arabic/English)

## 2. Production RAG Engine (GAARA-AI)

```python
# services/rag_service.py
from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

class GAARARAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={'device': 'cpu'}
        )
        self.sparse = FastEmbedSparse(model_name="Qdrant/bm25")
        self.llm = Ollama(
            base_url="http://ollama:11434",
            model="qwen2.5:7b",
            temperature=0.3
        )
        self.qdrant = QdrantClient(url="http://qdrant:6333")
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=120,
            separators=["\n\n", "\n", ".", "!", "?", "،", " "]
        )

    # Collections: agricultural, products, diseases, nutrients, treatments, market, general
    COLLECTIONS = [
        "gaara_agricultural", "gaara_products", "gaara_diseases",
        "gaara_nutrients", "gaara_treatments", "gaara_market", "gaara_general"
    ]

    def add_knowledge(self, text, category="general", metadata=None):
        collection = f"gaara_{category}"
        chunks = self.splitter.split_text(text)
        store = QdrantVectorStore(
            client=self.qdrant, collection_name=collection,
            embedding=self.embeddings, sparse_embedding=self.sparse,
            retrieval_mode=RetrievalMode.HYBRID,
        )
        store.add_texts(chunks, metadatas=[{**(metadata or {})} for _ in chunks])
        return len(chunks)

    def search(self, query, category="general", top_k=5):
        collection = f"gaara_{category}"
        store = QdrantVectorStore(
            client=self.qdrant, collection_name=collection,
            embedding=self.embeddings, sparse_embedding=self.sparse,
            retrieval_mode=RetrievalMode.HYBRID,
        )
        return store.similarity_search_with_score(query, k=top_k)

    def ask(self, question, category="general"):
        collection = f"gaara_{category}"
        store = QdrantVectorStore(
            client=self.qdrant, collection_name=collection,
            embedding=self.embeddings, sparse_embedding=self.sparse,
            retrieval_mode=RetrievalMode.HYBRID,
        )
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=store.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
        )
        result = qa.invoke({"query": question})
        return {"answer": result["result"], "sources": result.get("source_documents", [])}
```

## 3. Qdrant Collection Initialization

```python
# scripts/init_qdrant_collections.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(url="http://qdrant:6333")

COLLECTIONS = {
    "gaara_agricultural": "Agricultural knowledge, crops, seasons, soil types",
    "gaara_products":     "Sakata seed catalog, varieties, specifications",
    "gaara_diseases":     "Plant diseases: symptoms, causes, 26 classes",
    "gaara_nutrients":    "Nutrient deficiency: N, P, K, Ca, Mg, Fe, Mn, Zn, B",
    "gaara_treatments":   "Treatment protocols, fertilizers, organic solutions",
    "gaara_market":       "Market intelligence, competitor prices, trends",
    "gaara_general":      "General knowledge, company docs, policies",
}

for name in COLLECTIONS:
    if not client.collection_exists(name):
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print(f"✅ Created: {name}")
```

## 4. Migration from ChromaDB

If upgrading from the old `tools/rag_engine.py` (ChromaDB-based):

| Old (ChromaDB) | New (Qdrant) |
|---|---|
| `chromadb.Client()` | `QdrantClient(url="http://qdrant:6333")` |
| `DefaultEmbeddingFunction()` | `HuggingFaceEmbeddings("BAAI/bge-m3")` |
| `collection.add(documents=...)` | `vector_store.add_texts(texts=...)` |
| `collection.query(query_texts=...)` | `vector_store.similarity_search(query=...)` |
| Dense search only | **Hybrid: Dense + Sparse BM25** |
| In-memory (lost on restart) | **Persistent volume** |
| No filtering | **Advanced metadata filtering** |

## 5. Requirements

```
langchain>=0.3.0
langchain-community>=0.3.0
langchain-qdrant>=0.2.0
langchain-text-splitters>=0.3.0
qdrant-client>=1.13.0
fastembed>=0.4.0
sentence-transformers>=3.3.0
```
