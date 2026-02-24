# Embedding Storage Rules (v26.0)

> **Scope**: Vector Database Management
> **Compliance**: Multi-View Plant Disease Detection
> **Version**: 26.0.0

## 1. Vector Database Selection

| Scale | Recommended DB | Version | Why? |
| :--- | :--- | :--- | :--- |
| **< 500K Vectors** | **ChromaDB** | 1.5.0 | Embedded, Python-native, No setup. Dev/prototyping. |
| **500K - 5M** | **Qdrant** | 1.16.x | Rust-based, Fast, Filtered HNSW. Production. |
| **> 5M** | **Milvus** | 2.6.10 | Distributed, Scalable, IVF_RABITQ. Enterprise. |

## 2. Embedding Configuration

### 2.1 Dimensionality
*   **DINOv2 ViT-B/14**: 768 dimensions (**PRIMARY** model).
*   **ResNet50**: 2048 dimensions.
*   **ViT-B/16**: 768 dimensions.
*   **CLIP**: 512 dimensions.
*   **Rule**: Must match model output exactly. Mismatch = `ERR-EMB-001`.

### 2.2 Distance Metric
*   **Cosine Similarity**: Default for L2-normalized vectors (0-1 range).
*   **Euclidean (L2)**: Use for unnormalized vectors.
*   **Dot Product**: Use for recommendation systems.

### 2.3 Normalization (MANDATORY)
*   **Rule**: L2-normalize ALL embeddings before storage.
*   **Verify**: `assert abs(np.linalg.norm(embedding) - 1.0) < 1e-6`

## 3. Similarity Thresholds (Plant Disease Domain)

| Comparison | Threshold | Interpretation |
| :--- | :--- | :--- |
| **Same-disease match** | cosine > 0.85 | High confidence same disease |
| **Probable match** | 0.70 < cosine ≤ 0.85 | Needs human review |
| **Different disease** | cosine < 0.70 | Distinct disease classes |
| **Drift alert** | centroid shift > 0.05 | Distribution change detected |

## 4. Indexing Strategy

### 4.1 HNSW (Hierarchical Navigable Small World)
*   **M (Max Links)**: 16-64 (Higher = Better Recall, Slower Indexing).
*   **ef_construction**: 100-500 (Higher = Better Quality).
*   **ef_search**: 50-200 (Runtime parameter).

### 4.2 Metadata Schema
Every vector MUST store:
*   `image_id`: UUID.
*   `plant_species`: String (e.g., “Tomato”).
*   `disease_label`: String (e.g., “Early Blight”).
*   `view_angle`: String (“Top”, “Side”, “Bottom”).
*   `view_type`: String (“original”, “binary”, “gradcam”, “crop”).
*   `confidence`: Float (model prediction confidence).
*   `timestamp`: ISO8601.

## 5. Drift Detection (Embedding Space)

### 5.1 Centroid Monitoring
*   **Method**: Monitor centroid shift of disease classes over time.
*   **Metric**: Cosine distance between monthly centroids.
*   **Threshold**: Shift > 0.05 triggers alert.
*   **Window**: 30-day rolling window, calculated weekly.

### 5.2 Drift-Adapter Pattern
When drift is detected:
1.  Alert fires (centroid shift > 0.05).
2.  Collect new samples from drifted distribution.
3.  Fine-tune embedding model on new + old samples (replay buffer).
4.  Validate: new centroid distances maintain class separation (inter-class > 0.70).
5.  Re-index affected vectors with updated embeddings.
6.  Log drift event with before/after centroid positions.

## 6. Storage & Processing Budget
*   **Per image**: 5-12 MB raw, 768 × float32 = 3KB embedding.
*   **Batch insertion**: ≤1000 vectors per batch for ChromaDB, ≤10000 for Qdrant.
*   **Query latency target**: <50ms for top-10 nearest neighbors.
*   **Embedding generation**: 30ms (GPU), 300ms (CPU) per image.

## 7. Code Example (ChromaDB)
```python
import chromadb
import numpy as np

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(
    name="plant_diseases",
    metadata={"hnsw:space": "cosine"}
)

# L2-normalize before storage (MANDATORY)
embedding = model.encode(image)
embedding = embedding / np.linalg.norm(embedding)

collection.add(
    embeddings=[embedding.tolist()],
    metadatas=[{
        "species": "Tomato",
        "disease": "Early Blight",
        "view_type": "original",
        "confidence": 0.94,
    }],
    ids=["img_001"]
)

# Similarity search with threshold
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=10,
)

# Filter: only return results with distance < 0.15 (cosine > 0.85)
```

## 8. Cross-References
*   **Master Rules**: `rules/ml/RULES-plant-disease-analysis.md`
*   **Drift Errors**: `errors/ml/ERROR-drift-detection-catalog.md`
*   **Error Catalog**: `errors/ml/ERROR-multi-view-pipeline-catalog.md` → `ERR-EMB-001`
