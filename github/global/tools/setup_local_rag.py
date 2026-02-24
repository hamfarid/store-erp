#!/usr/bin/env python3
"""
Local RAG & Vector DB Setup Script (ChromaDB)
---------------------------------------------
This script sets up a local RAG (Retrieval-Augmented Generation) system for the current project.
It uses ChromaDB in persistent mode, which stores data in a local directory (`.vector_db`)
and does NOT require a running server or port allocation, eliminating port conflicts.

Features:
1.  **Embedded Vector DB**: Uses ChromaDB in persistent mode (no ports needed).
2.  **Automatic Ingestion**: Scans the project for Markdown, Text, and Code files.
3.  **Smart Chunking**: Splits files into manageable chunks for better retrieval.
4.  **Query Interface**: Provides a simple CLI to query the local knowledge base.
5.  **Port Management (Optional)**: If an API server is needed, it dynamically finds an available port.

Usage:
    python3 tools/setup_local_rag.py [command]

Commands:
    init      Initialize the vector database and ingest files.
    query     Query the knowledge base.
    serve     Start a lightweight API server (auto-port selection).
    status    Check the status of the vector database.
"""

import os
import sys
import argparse
import glob
import json
import socket
from typing import List, Dict, Any

# Try to import chromadb, handle missing dependency
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("Error: 'chromadb' is not installed. Please run: pip install chromadb")
    sys.exit(1)

# Configuration
VECTOR_DB_DIR = os.path.join(os.getcwd(), ".vector_db")
COLLECTION_NAME = "project_knowledge"
ALLOWED_EXTENSIONS = {".md", ".txt", ".py", ".js", ".json", ".yaml", ".yml", ".sh"}
IGNORE_DIRS = {".git", ".vector_db", "__pycache__", "node_modules", ".venv", "venv"}

def get_files_to_ingest(root_dir: str) -> List[str]:
    """Recursively find all relevant files in the project."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out ignored directories
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext in ALLOWED_EXTENSIONS:
                files.append(os.path.join(dirpath, filename))
    return files

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def init_vector_db():
    """Initialize the vector database and ingest files."""
    print(f"Initializing Vector DB in: {VECTOR_DB_DIR}")
    
    # Initialize ChromaDB client in persistent mode
    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    
    # Get or create collection
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    
    # Find files
    files = get_files_to_ingest(os.getcwd())
    print(f"Found {len(files)} files to ingest.")
    
    count = 0
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content.strip():
                continue
                
            # Chunk content
            chunks = chunk_text(content)
            
            # Add to collection
            ids = [f"{file_path}_{i}" for i in range(len(chunks))]
            metadatas = [{"source": file_path, "chunk_index": i} for i in range(len(chunks))]
            
            collection.upsert(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            count += len(chunks)
            print(f"Ingested: {file_path} ({len(chunks)} chunks)")
            
        except Exception as e:
            print(f"Failed to ingest {file_path}: {e}")
            
    print(f"\nSuccess! Ingested {count} chunks from {len(files)} files.")

def query_vector_db(query_text: str, n_results: int = 5):
    """Query the vector database."""
    if not os.path.exists(VECTOR_DB_DIR):
        print("Error: Vector DB not initialized. Run 'init' first.")
        return

    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    print(f"\nResults for: '{query_text}'\n" + "-"*40)
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        print(f"[{i+1}] Source: {meta['source']}")
        print(f"Content: {doc[:200]}...\n")

def find_available_port(start_port: int = 8000, max_port: int = 9000) -> int:
    """Find an available port in the given range."""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    raise RuntimeError("No available ports found.")

def serve_api():
    """Start a lightweight API server for RAG."""
    try:
        from fastapi import FastAPI
        import uvicorn
    except ImportError:
        print("Error: 'fastapi' or 'uvicorn' not installed. Run: pip install fastapi uvicorn")
        return

    app = FastAPI()
    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    @app.get("/query")
    def api_query(q: str, n: int = 5):
        results = collection.query(query_texts=[q], n_results=n)
        return {"results": results}

    port = find_available_port()
    print(f"Starting RAG API Server on port {port}...")
    
    # Save port to a registry file for other tools to find
    registry_file = os.path.join(os.getcwd(), ".rag_server_info.json")
    with open(registry_file, "w") as f:
        json.dump({"port": port, "pid": os.getpid()}, f)
        
    uvicorn.run(app, host="0.0.0.0", port=port)

def main():
    parser = argparse.ArgumentParser(description="Local RAG & Vector DB Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    subparsers.add_parser("init", help="Initialize Vector DB and ingest files")
    
    query_parser = subparsers.add_parser("query", help="Query the knowledge base")
    query_parser.add_argument("text", type=str, help="Query text")
    
    subparsers.add_parser("serve", help="Start API server")
    subparsers.add_parser("status", help="Check status")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_vector_db()
    elif args.command == "query":
        query_vector_db(args.text)
    elif args.command == "serve":
        serve_api()
    elif args.command == "status":
        if os.path.exists(VECTOR_DB_DIR):
            print(f"Vector DB exists at: {VECTOR_DB_DIR}")
            client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
            try:
                collection = client.get_collection(name=COLLECTION_NAME)
                print(f"Collection '{COLLECTION_NAME}' contains {collection.count()} items.")
            except:
                print("Collection not found.")
        else:
            print("Vector DB not initialized.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
