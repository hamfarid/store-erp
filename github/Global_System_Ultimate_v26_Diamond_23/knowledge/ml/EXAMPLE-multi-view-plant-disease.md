# Multi-View Plant Disease Pipeline Example (v26.0)

> **Scope**: Complete Working Example of the Multi-View Pipeline
> **Compliance**: Global System Ultimate v26 Diamond 9

## 1. Pipeline Overview

```mermaid
graph LR
    A[Input Images] --> B[Preprocessing]
    B --> C[Quality Gate 1]
    C --> D[Binarization - 5 Views]
    D --> E[Quality Gate 2]
    E --> F[Multi-Crop - 10 Views]
    F --> G[Feature Extraction]
    G --> H[Embedding - DINOv2]
    H --> I[Quality Gate 3]
    I --> J[Classification]
    J --> K[GradCAM]
    K --> L[Quality Gate 4]
    L --> M[Similarity Search]
    M --> N[Report]
```

## 2. Environment Setup

```python
# Tool versions pinned per rules/ml/RULES-plant-disease-analysis.md Section 1
# PyTorch==2.1.0 torchvision==0.16.0 timm==0.9.10
# opencv-python==4.8.0 albumentations==1.3.1 chromadb==0.4.15
import torch
import torchvision.transforms as T
import timm
import cv2
import numpy as np
import chromadb
from PIL import Image
```

## 3. Step 1: Image Validation (Quality Gate 1)

```python
def validate_image(image_path: str) -> dict:
    """Validate image quality before pipeline processing."""
    img = cv2.imread(image_path)
    if img is None:
        return {"valid": False, "error": "ERR-IMG-001", "message": "Cannot read image"}
    
    h, w = img.shape[:2]
    if h < 960 or w < 1280:
        return {"valid": False, "error": "ERR-IMG-001", 
                "message": f"Resolution {w}x{h} below minimum 1280x960"}
    
    # Blur detection: Laplacian variance
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if laplacian_var < 100.0:
        return {"valid": False, "error": "ERR-IMG-002", 
                "message": f"Blur detected: variance={laplacian_var:.1f} < 100.0"}
    
    # Glare detection: V-channel analysis
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    glare_ratio = np.sum(hsv[:, :, 2] > 250) / hsv[:, :, 2].size
    if glare_ratio > 0.10:
        return {"valid": False, "error": "ERR-IMG-003", 
                "message": f"Glare detected: {glare_ratio:.1%} > 10%"}
        
    return {"valid": True, "resolution": f"{w}x{h}", 
            "blur_score": laplacian_var, "glare_ratio": glare_ratio}
```

## 4. Step 2: Binarization (5 Binary Views)

```python
def generate_binary_views(img_bgr: np.ndarray) -> dict:
    """Generate 5 binary views per rules/ml/RULES-image-binarization.md."""
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # View 1: Green Mask (healthy tissue) - H=35-85, S=40-255, V=40-255
    green_mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
    
    # View 2: Disease Mask (necrosis H=10-20 + chlorosis H=20-35)
    necrosis = cv2.inRange(hsv, (10, 50, 20), (20, 200, 150))
    chlorosis = cv2.inRange(hsv, (20, 40, 40), (35, 255, 255))
    disease_mask = cv2.bitwise_or(necrosis, chlorosis)
    
    # View 3: Edge Binary (Canny edge detection)
    edges = cv2.Canny(gray, 50, 150)
    
    # View 4: Texture Binary (adaptive threshold)
    texture = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
                                   
    # View 5: Saturation Binary (high saturation = vivid color regions)
    sat_binary = cv2.threshold(hsv[:, :, 1], 80, 255, cv2.THRESH_BINARY)[1]
    
    # Morphological cleanup (HARD LIMITS: max kernel 15x15, max 5 iterations)
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    views = {}
    for name, mask in [("green", green_mask), ("disease", disease_mask), 
                      ("edge", edges), ("texture", texture), ("saturation", sat_binary)]:
        cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open, iterations=1)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel_close, iterations=2)
        views[name] = cleaned
        
    return views

def validate_masks(views: dict) -> dict:
    """Quality Gate 2: Validate binary masks (fg 5-60%, contours 1-50)."""
    results = {}
    for name, mask in views.items():
        fg_ratio = np.sum(mask > 0) / mask.size
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv2.contourArea(c) >= 100] # min 100px²
        
        results[name] = {
            "fg_ratio": round(fg_ratio, 4),
            "contour_count": len(contours),
            "valid": 0.05 <= fg_ratio <= 0.60 and 1 <= len(contours) <= 50
        }
    return results
```

## 5. Step 3: Multi-Crop TTA (10 Views)

```python
def generate_tta_crops(img_pil: Image.Image, crop_size: int = 224) -> list:
    """Generate 10-crop TTA per rules/ml/RULES-multi-crop-augmentation.md."""
    img_resized = img_pil.resize((256, 256))
    w, h = img_resized.size
    
    positions = [
        (0, 0), # Top-Left
        (w - crop_size, 0), # Top-Right
        (0, h - crop_size), # Bottom-Left
        (w - crop_size, h - crop_size), # Bottom-Right
        ((w - crop_size) // 2, (h - crop_size) // 2), # Center
    ]
    
    crops = []
    for x, y in positions:
        crop = img_resized.crop((x, y, x + crop_size, y + crop_size))
        crops.append(crop)
        crops.append(crop.transpose(Image.FLIP_LEFT_RIGHT))
        
    assert len(crops) == 10, f"Expected 10 crops, got {len(crops)}"
    return crops

def preprocess_crops(crops: list) -> torch.Tensor:
    """Normalize crops for DINOv2 input."""
    transform = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return torch.stack([transform(crop) for crop in crops]) # [10, 3, 224, 224]
```

## 6. Step 4: Embedding Extraction

```python
def extract_embedding(batch: torch.Tensor) -> np.ndarray:
    """Extract DINOv2 768d embedding per rules/ml/RULES-embedding-storage.md."""
    model = timm.create_model("vit_base_patch14_dinov2", pretrained=True, num_classes=0)
    model.eval()
    
    with torch.no_grad():
        embeddings = model(batch).numpy() # [10, 768]
        
    # L2 normalize EACH crop embedding (MANDATORY)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms
    
    for i in range(len(embeddings)):
        assert abs(np.linalg.norm(embeddings[i]) - 1.0) < 1e-6
        
    # Average + re-normalize for final image embedding
    avg = embeddings.mean(axis=0)
    avg = avg / np.linalg.norm(avg)
    
    return avg # [768]
```

## 7. Step 5: Similarity Search (ChromaDB)

```python
def search_similar(embedding: np.ndarray, top_k: int = 5) -> list:
    """Query vector DB per rules/ml/RULES-embedding-storage.md."""
    client = chromadb.PersistentClient(path="./vector_db")
    collection = client.get_collection("plant_disease_embeddings")
    
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=top_k,
        include=["metadatas", "distances"]
    )
    
    matches = []
    for i in range(len(results["ids"][0])):
        cosine_sim = 1 - results["distances"][0][i] # ChromaDB returns L2 distance
        if cosine_sim >= 0.70: # Minimum similarity threshold
            matches.append({
                "id": results["ids"][0][i],
                "similarity": round(cosine_sim, 4),
                "disease": results["metadatas"][0][i].get("disease_label", "unknown"),
                "confidence": results["metadatas"][0][i].get("confidence", 0),
            })
            
    return matches

def store_embedding(embedding: np.ndarray, metadata: dict) -> str:
    """Store new embedding with full metadata."""
    client = chromadb.PersistentClient(path="./vector_db")
    collection = client.get_or_create_collection(
        "plant_disease_embeddings", 
        metadata={"hnsw:space": "cosine", "model_version": "dinov2_vit_b14"}
    )
    
    doc_id = metadata["image_id"]
    collection.add(
        ids=[doc_id],
        embeddings=[embedding.tolist()],
        metadatas=[{
            "image_id": metadata["image_id"],
            "plant_species": metadata["plant_species"],
            "disease_label": metadata["disease_label"],
            "view_type": metadata.get("view_type", "top"),
            "confidence": metadata.get("confidence", 0.0),
            "timestamp": metadata["timestamp"],
        }]
    )
    return doc_id
```

## 8. Full Pipeline Orchestration

```python
def run_pipeline(image_path: str, plant_species: str = "tomato") -> dict:
    """Complete multi-view plant disease diagnosis pipeline."""
    import time
    start = time.time()
    
    # Gate 1: Image validation
    validation = validate_image(image_path)
    if not validation["valid"]:
        return {"status": "rejected", "error": validation["error"], "message": validation["message"]}
        
    # Binarization
    img_bgr = cv2.imread(image_path)
    views = generate_binary_views(img_bgr)
    
    # Gate 2: Mask validation
    mask_results = validate_masks(views)
    valid_views = {k: v for k, v in mask_results.items() if v["valid"]}
    
    if len(valid_views) < 2:
        return {"status": "rejected", "error": "ERR-BIN-001", 
                "message": f"Only {len(valid_views)}/5 views passed quality gate"}
                
    # Multi-Crop TTA
    img_pil = Image.open(image_path).convert("RGB")
    crops = generate_tta_crops(img_pil)
    batch = preprocess_crops(crops)
    
    # Embedding
    embedding = extract_embedding(batch)
    
    # Similarity search
    similar = search_similar(embedding)
    
    elapsed = time.time() - start
    return {
        "status": "success",
        "valid_views": len(valid_views),
        "embedding_dim": len(embedding),
        "similar_images": similar,
        "processing_time_ms": round(elapsed * 1000, 1),
        "model_version": "dinov2_vit_b14",
        "pipeline_version": "v26.0",
    }
```

## 9. Cross-References

All code in this example follows governance rules defined in:
-   `rules/ml/RULES-plant-disease-analysis.md` for tool pinning and overall pipeline standards.
-   `rules/ml/RULES-image-binarization.md` for HSV thresholds and morphological limits.
-   `rules/ml/RULES-multi-crop-augmentation.md` for TTA crop strategy.
-   `rules/ml/RULES-embedding-storage.md` for L2 normalization and vector DB configuration.
-   `rules/ml/RULES-gradcam-heatmap.md` for explainability quality gates.
-   `errors/ml/ERROR-multi-view-pipeline-catalog.md` for error code definitions.
-   `workflows/ml/ML_MULTI_VIEW_WORKFLOW.md` for the full workflow orchestration.
