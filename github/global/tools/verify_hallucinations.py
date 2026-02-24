#!/usr/bin/env python3
"""
Hallucination Verification Tool (RAG-Based)
-------------------------------------------
This tool scans a text file and verifies each sentence against the project's memory (Vector DB).
It flags sentences that lack sufficient evidence in the knowledge base, helping to prevent hallucinations.

Features:
1.  **Sentence Segmentation**: Splits text into individual sentences for granular verification.
2.  **Semantic Search**: Uses RAG to find the most relevant evidence for each sentence.
3.  **Confidence Scoring**: Calculates a similarity score (0-1) to estimate factual accuracy.
4.  **Report Generation**: Produces a detailed report highlighting potential hallucinations.

Usage:
    python3 tools/verify_hallucinations.py <input_file> [--threshold 0.7]
"""

import os
import sys
import argparse
from typing import List, Dict, Tuple

# Try to import dependencies
try:
    import chromadb
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    print("Error: Dependencies not installed. Run: pip install chromadb sentence-transformers")
    sys.exit(1)

# Configuration
VECTOR_DB_DIR = os.path.join(os.getcwd(), ".vector_db")
COLLECTION_NAME = "project_knowledge"
DEFAULT_THRESHOLD = 0.6  # Minimum similarity score to consider "verified"

def get_collection():
    """Get the ChromaDB collection."""
    if not os.path.exists(VECTOR_DB_DIR):
        raise RuntimeError("Vector DB not initialized. Run 'python3 tools/setup_local_rag.py init' first.")
    
    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)

def split_into_sentences(text: str) -> List[str]:
    """Simple sentence splitter (can be improved with NLTK/Spacy)."""
    # Basic splitting by punctuation
    import re
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return [s.strip() for s in sentences if s.strip()]

def verify_text(input_file: str, threshold: float):
    """Verify the content of a text file against the knowledge base."""
    print(f"🔍 Verifying '{input_file}' against Project Memory...")
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        return

    collection = get_collection()
    sentences = split_into_sentences(content)
    
    print(f"📝 Found {len(sentences)} sentences. Checking evidence...\n")
    
    hallucinations = []
    verified_count = 0
    
    # Load model for local similarity check (optional but recommended for better scoring)
    # Here we rely on Chroma's distance, but for a real "Verification Tool", 
    # we might want to re-rank or use a cross-encoder. 
    # For simplicity/speed in this v1, we use Chroma's query results.
    
    for i, sentence in enumerate(sentences):
        # Skip very short sentences
        if len(sentence.split()) < 4:
            continue
            
        results = collection.query(
            query_texts=[sentence],
            n_results=1
        )
        
        # Chroma returns distance (lower is better) or similarity? 
        # Default is L2 distance. We need to interpret this carefully.
        # A distance > 1.0 usually means "not very similar".
        # Let's assume distance < 0.5 is a "good match".
        
        distance = results['distances'][0][0] if results['distances'] else 10.0
        evidence = results['documents'][0][0] if results['documents'] else "No evidence found."
        source = results['metadatas'][0][0].get('source', 'Unknown') if results['metadatas'] else "Unknown"
        
        # Invert distance to get a pseudo-confidence score (0-1)
        # This is a heuristic; actual implementation depends on the embedding model used.
        confidence = max(0, 1.0 - distance)
        
        if confidence < threshold:
            print(f"🚩 [Potential Hallucination] (Conf: {confidence:.2f})")
            print(f"   Sentence: \"{sentence}\"")
            print(f"   Best Evidence: \"{evidence[:100]}...\" (from {os.path.basename(source)})")
            print("-" * 40)
            hallucinations.append((sentence, confidence, evidence, source))
        else:
            verified_count += 1
            # print(f"✅ Verified: \"{sentence[:50]}...\"")

    print(f"\n📊 Verification Report:")
    print(f"   Total Sentences: {len(sentences)}")
    print(f"   Verified: {verified_count}")
    print(f"   Potential Hallucinations: {len(hallucinations)}")
    
    if hallucinations:
        print(f"\n⚠️  Found {len(hallucinations)} potential issues. Please review the flagged sentences.")
    else:
        print(f"\n✅ Excellent! No hallucinations detected based on current memory.")

def main():
    parser = argparse.ArgumentParser(description="Hallucination Verification Tool")
    parser.add_argument("input_file", help="Path to the text file to verify")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Confidence threshold (0.0 - 1.0)")
    
    args = parser.parse_args()
    
    verify_text(args.input_file, args.threshold)

if __name__ == "__main__":
    main()
