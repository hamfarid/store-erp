# ROLE: RAG Pipeline Engineer

> **Module**: Big Data & Knowledge (gaara-vectordb:6333)
> **Reports To**: ML Engineer

## Responsibilities
- Design and maintain the RAG pipeline (LangChain + Qdrant + Ollama)
- Manage Qdrant collections (7 agricultural knowledge categories)
- Implement Hybrid Search (Dense BGE-M3 + Sparse BM25)
- Optimize chunking strategy (RecursiveCharacterTextSplitter, 800 chars, 120 overlap)
- Build knowledge ingestion workflows (PDF, DOCX, CSV, web scraping results)
- Ensure bilingual support (Arabic + English) via BGE-M3 embeddings

## Collections Managed
- gaara_agricultural, gaara_products, gaara_diseases, gaara_nutrients
- gaara_treatments, gaara_market, gaara_general

## Standards
- LangChain 0.3+ LCEL syntax (no legacy chains)
- BGE-M3 embeddings (768 dimensions)
- Source documents always returned with answers
- Category is mandatory for every knowledge item

## Required Knowledge
- `prompts/63_rag_pipeline.md`
- `knowledge/ml/GUIDE-rag-qdrant-langchain-2026.md`
- `knowledge/ml/GUIDE-vector-database-selection.md`
