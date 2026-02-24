# Prompt 63: RAG Pipeline — LangChain + Qdrant + Ollama

> **Scope**: Retrieval-Augmented Generation for GAARA-AI Knowledge Base
> **When to Load**: Building or modifying the knowledge/RAG system

## Pipeline Architecture

```
User Question
    → BGE-M3 Embed Query (768 dims)
    → Qdrant Hybrid Search (Dense + Sparse BM25)
    → Retrieve Top-K Documents (k=5)
    → Augment Prompt with Context
    → Ollama LLM (Qwen2.5:7b) Generate Answer
    → Return Answer + Sources
```

## Qdrant Collections (7 Categories)
```python
COLLECTIONS = {
    'gaara_agricultural': 'Agricultural knowledge (crops, seasons, soil)',
    'gaara_products': 'Seed catalog, varieties, specifications',
    'gaara_diseases': 'Plant diseases database',
    'gaara_nutrients': 'Nutrient deficiency information',
    'gaara_treatments': 'Treatment protocols + fertilizers',
    'gaara_market': 'Market intelligence, prices, competitors',
    'gaara_general': 'General knowledge base',
}
# Vector size: 768 (BGE-M3)
# Distance: Cosine
```

## Key Components
- **Embeddings**: `BAAI/bge-m3` via HuggingFace (multilingual Arabic+English, 768 dims)
- **Text Splitter**: `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)`
- **Vector Store**: `QdrantVectorStore` via `langchain-qdrant`
- **LLM**: `Ollama(base_url="http://ollama:11434", model="qwen2.5:7b")`
- **Chain**: `RetrievalQA.from_chain_type` with `return_source_documents=True`

## Rules
- All text must be chunked before embedding (800 chars, 120 overlap)
- Category is mandatory for every knowledge item
- Hybrid Search (Dense + Sparse BM25) for best recall
- Source documents always returned with answers
- Arabic text: use BGE-M3 (not all-MiniLM which is English-only)
