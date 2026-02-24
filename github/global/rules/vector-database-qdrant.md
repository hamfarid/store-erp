# Rule: Vector Database — Qdrant Standards

> **Applies To**: Knowledge Base, RAG Pipeline, Embeddings

## Collection Schema
All 7 GAARA-AI collections follow this configuration:
- Vector size: 768 (BGE-M3 embeddings)
- Distance metric: Cosine
- Hybrid Search: Dense vectors + Sparse BM25

## Collections
| Collection | Purpose | Sources |
|:-----------|:--------|:--------|
| gaara_agricultural | Crops, seasons, soil | Research papers, guides |
| gaara_products | Seed catalog, varieties | Product database |
| gaara_diseases | Plant diseases | PlantVillage, field data |
| gaara_nutrients | Nutrient deficiency | Mendeley, Roboflow |
| gaara_treatments | Treatment + fertilizer | Expert DB, research |
| gaara_market | Market intelligence | Scraped competitor data |
| gaara_general | General knowledge | Web learning sessions |

## Embedding Rules
1. ALWAYS use BGE-M3 embeddings (multilingual Arabic+English)
2. NEVER use all-MiniLM-L6-v2 or similar English-only models
3. Chunk text before embedding: 800 characters, 120 overlap
4. RecursiveCharacterTextSplitter for structured text
5. Store metadata with every vector: source, category, date, language

## Search Rules
1. Default to Hybrid Search (Dense + BM25) for best recall
2. Return top-K results (default k=5)
3. Always include source documents in response
4. Score threshold: filter results below 0.3 similarity

## Qdrant Version
- Qdrant 1.13+ required (Hybrid Search support)
- Client: `qdrant-client` Python package
