"""
Minimal RAG service: ChromaDB + Sentence-Transformers
- Persistence under backend/instance/chroma
- Model configurable via RAG_MODEL env (default: all-MiniLM-L6-v2)
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Any

import chromadb
from chromadb.api.models.Collection import Collection
from sentence_transformers import SentenceTransformer

# Configuration
ROOT = Path(__file__).resolve().parents[2]  # .../complete_inventory_system
BACKEND_DIR = Path(__file__).resolve().parents[1]
INSTANCE_DIR = BACKEND_DIR / "instance"
PERSIST_DIR = Path(os.environ.get("RAG_STORE_DIR", str(INSTANCE_DIR / "chroma")))
COLLECTION_NAME = os.environ.get("RAG_COLLECTION", "docs")
MODEL_NAME = os.environ.get("RAG_MODEL", "all-MiniLM-L6-v2")
TOP_K_DEFAULT = int(os.environ.get("RAG_TOP_K", "5"))


@lru_cache(maxsize=1)
def _get_client() -> chromadb.Client:
    """Return a cached Chroma persistent client."""
    PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(PERSIST_DIR))


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    """Return a cached embedding model instance."""
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def _get_collection() -> Collection:
    """Return a cached collection; create if missing."""
    client = _get_client()
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception:  # pylint: disable=broad-exception-caught
        return client.create_collection(
            name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed texts to normalized vectors using the configured model."""
    model = _get_model()
    vecs = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )  # returns np.ndarray
    return vecs.tolist()


# P1.39: Import RAG caching
try:
    from rag_cache import cache_rag_query, get_rag_cache_stats

    RAG_CACHE_AVAILABLE = True
except ImportError:
    RAG_CACHE_AVAILABLE = False

    def cache_rag_query(ttl=None):
        def decorator(func):
            return func

        return decorator


@cache_rag_query(ttl=3600)  # P1.39: Cache RAG queries for 1 hour
def query(text: str, top_k: int | None = None) -> Dict[str, Any]:
    """
    Query similar docs and return a simple answer + sources payload.

    P1.39: Results are cached for improved performance.
    """
    top_k = top_k or TOP_K_DEFAULT
    if not text.strip():
        return {"success": False, "answer": "Empty query", "sources": []}

    col = _get_collection()
    q_emb = embed_texts([text])
    results = col.query(
        query_embeddings=q_emb,
        n_results=top_k,
        include=["metadatas", "documents", "distances"],
    )  # type: ignore

    docs = []
    for i in range(len(results.get("ids", [[]])[0])):
        docs.append(
            {
                "id": results["ids"][0][i],
                "distance": float(results.get("distances", [[None]])[0][i] or 0.0),
                "text": results.get("documents", [[""]])[0][i],
                "meta": results.get("metadatas", [[{}]])[0][i],
            }
        )

    # Simple deterministic synthesis (no external LLM)
    answer_lines = [f"Top {len(docs)} results for: {text}"]
    for j, d in enumerate(docs, 1):
        path = d.get("meta", {}).get("path", "?")
        answer_lines.append(f"{j}. {path}  (score={1.0 - d['distance']:.3f})")

    return {
        "success": True,
        "query": text,
        "answer": "\n".join(answer_lines),
        "sources": docs,
    }
