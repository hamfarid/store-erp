# Template: Qdrant Collection Setup (GAARA-AI)

> **Use For**: Creating new knowledge base collections

## Collection Definition
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType

client = QdrantClient(url="http://local-server:6333")

client.create_collection(
    collection_name="gaara_{category}",
    vectors_config=VectorParams(
        size=768,           # BGE-M3 dimensions
        distance=Distance.COSINE,
    ),
    # Enable Hybrid Search (Dense + Sparse)
    sparse_vectors_config={
        "bm25": SparseVectorParams()
    },
)
```

## Required Payload Fields
Every document stored MUST include:
```json
{
  "text": "The actual text chunk",
  "source_url": "https://...",
  "source_type": "web|pdf|docx|csv|manual",
  "collection": "gaara_{category}",
  "language": "ar|en",
  "category": "disease|nutrient|treatment|product|market|agriculture|general",
  "created_at": "2026-02-19T12:00:00Z",
  "chunk_hash": "sha256 of text chunk (for dedup)"
}
```

## 7 Standard Collections
| Collection | Category | Description |
|:-----------|:---------|:------------|
| gaara_agricultural | agriculture | Crops, seasons, soil, farming knowledge |
| gaara_products | product | Seed catalog, varieties, specifications |
| gaara_diseases | disease | Plant diseases database |
| gaara_nutrients | nutrient | Nutrient deficiency information |
| gaara_treatments | treatment | Treatment protocols, fertilizers, dosages |
| gaara_market | market | Market intelligence, prices, competitors |
| gaara_general | general | General knowledge base |

## Checklist
- [ ] Vector size: 768 (BGE-M3)
- [ ] Distance: Cosine
- [ ] Sparse vectors enabled (BM25 for Hybrid Search)
- [ ] All required payload fields present
- [ ] Duplicate check (source_url + chunk_hash) before insert
- [ ] Collection name follows pattern: gaara_{category}
