"""
Ingest Markdown files into Chroma collection for RAG.
Usage:
  python complete_inventory_system/backend/src/rag_ingest.py --rebuild
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable, List, Dict, Union, Sequence, Mapping, cast

import chromadb
from sentence_transformers import SentenceTransformer

# Paths
SRC_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SRC_DIR.parent
ROOT = BACKEND_DIR.parent

DOCS_DIRS = [
    ROOT / "docs",
    SRC_DIR / "models",
]
FILES = [
    ROOT / "FINAL_REPORT.md",  # if present at repo root
    SRC_DIR / "models" / "FINAL_REPORT.md",  # present in this repo
]

PERSIST_DIR = Path(
    os.environ.get("RAG_STORE_DIR", str(BACKEND_DIR / "instance" / "chroma"))
)
COLLECTION_NAME = os.environ.get("RAG_COLLECTION", "docs")
MODEL_NAME = os.environ.get("RAG_MODEL", "all-MiniLM-L6-v2")

MetadataValue = Union[str, int, float, bool, None]
MetadataDict = Dict[str, MetadataValue]


def iter_markdown_files() -> Iterable[Path]:
    """Yield unique Markdown/MDX files from configured sources."""
    seen = set()
    for p in FILES:
        if p.exists() and p.suffix.lower() in {".md", ".mdx"}:
            if p not in seen:
                seen.add(p)
                yield p
    for d in DOCS_DIRS:
        if d.exists():
            for p in d.rglob("*.md"):
                if p not in seen:
                    seen.add(p)
                    yield p
            for p in d.rglob("*.mdx"):
                if p not in seen:
                    seen.add(p)
                    yield p


def read_text(path: Path) -> str:
    """Read file text safely; return empty string on IO/decoding errors."""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        return ""


def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100,
) -> List[str]:
    """Naive word-based chunking with overlap."""
    words = text.split()
    chunks: List[str] = []
    i = 0
    n = len(words)
    while i < n:
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += max(1, chunk_size - overlap)
    return chunks


def main(rebuild: bool = False) -> None:
    """Ingest markdown into a Chroma collection."""
    # pylint: disable=too-many-locals
    PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(PERSIST_DIR))
    try:
        if rebuild:
            try:
                client.delete_collection(COLLECTION_NAME)
            except (ValueError, RuntimeError):
                # Collection may not exist yet
                pass
        col = client.get_or_create_collection(
            name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )
    except (ValueError, RuntimeError, TypeError):
        col = client.create_collection(
            name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )

    model = SentenceTransformer(MODEL_NAME)

    all_texts: List[str] = []
    all_ids: List[str] = []
    all_meta: List[MetadataDict] = []

    for path in iter_markdown_files():
        text = read_text(path)
        if not text.strip():
            continue
        chunks = chunk_text(text)
        for idx, ch in enumerate(chunks):
            meta_path = str(path.relative_to(ROOT)) if path.is_absolute() else str(path)
            id_base = meta_path.replace("\\", "/")
            all_texts.append(ch)
            all_ids.append(f"{id_base}:{idx}")
            all_meta.append({"path": id_base, "chunk": idx})

    if not all_texts:
        print("No markdown files found to ingest.")
        return

    embeddings = model.encode(
        all_texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )  # type: ignore

    # Upsert in batches to avoid large payloads
    batch_size = 256
    for i in range(0, len(all_texts), batch_size):
        j = i + batch_size
        metadata_batch = cast(Sequence[Mapping[str, MetadataValue]], all_meta[i:j])
        col.upsert(
            ids=all_ids[i:j],
            documents=all_texts[i:j],
            metadatas=metadata_batch,
            embeddings=embeddings[i:j],
        )
        print(f"Upserted {min(j, len(all_texts))}/{len(all_texts)}")

    print(
        f"Ingestion complete. Collection={COLLECTION_NAME}, "
        f"items={len(all_texts)} at {PERSIST_DIR}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rebuild", action="store_true", help="Drop and rebuild the collection"
    )
    args = parser.parse_args()
    main(rebuild=args.rebuild)
