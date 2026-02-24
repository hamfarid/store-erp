#!/usr/bin/env python3
"""
Memory MCP Server (ChromaDB Backend)
------------------------------------
This script implements a Model Context Protocol (MCP) server for the project's memory.
It allows AI assistants (like Claude Desktop, Cursor) to interact with the local vector database
using a standardized protocol.

Features:
1.  **MCP Compliance**: Implements the MCP specification for tools and resources.
2.  **Vector DB Integration**: Connects to the local ChromaDB instance.
3.  **Tools**:
    *   `search_memory`: Search for relevant information in the project's knowledge base.
    *   `add_memory`: Add new information to the memory bank.
    *   `list_sources`: List all ingested files and their metadata.

Usage:
    python3 tools/memory_mcp_server.py
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any

# Try to import dependencies
try:
    import chromadb
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: Dependencies not installed. Run: pip install chromadb mcp")
    sys.exit(1)

# Configuration
VECTOR_DB_DIR = os.path.join(os.getcwd(), ".vector_db")
COLLECTION_NAME = "project_knowledge"

# Initialize MCP Server
mcp = FastMCP("Project Memory")

def get_collection():
    """Get the ChromaDB collection."""
    if not os.path.exists(VECTOR_DB_DIR):
        raise RuntimeError("Vector DB not initialized. Run 'python3 tools/setup_local_rag.py init' first.")
    
    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)

@mcp.tool()
def search_memory(query: str, n_results: int = 5) -> str:
    """Search the project's memory for relevant information."""
    try:
        collection = get_collection()
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        output = f"Results for: '{query}'\n" + "-"*40 + "\n"
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            output += f"[{i+1}] Source: {meta.get('source', 'Unknown')}\n"
            output += f"Content: {doc[:500]}...\n\n"
            
        return output
    except Exception as e:
        return f"Error searching memory: {str(e)}"

@mcp.tool()
def add_memory(content: str, source: str = "manual_entry") -> str:
    """Add a new memory entry manually."""
    try:
        collection = get_collection()
        
        # Simple chunking for manual entry
        chunks = [content]
        ids = [f"{source}_{os.urandom(4).hex()}"]
        metadatas = [{"source": source, "type": "manual"}]
        
        collection.upsert(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        return f"Successfully added memory from source: {source}"
    except Exception as e:
        return f"Error adding memory: {str(e)}"

@mcp.tool()
def list_sources() -> str:
    """List all unique sources in the memory bank."""
    try:
        collection = get_collection()
        # This is a bit inefficient in Chroma, but works for small datasets
        # For larger datasets, we should maintain a separate source registry
        result = collection.get(include=['metadatas'])
        sources = set()
        for meta in result['metadatas']:
            if meta and 'source' in meta:
                sources.add(meta['source'])
        
        return "Indexed Sources:\n" + "\n".join(sorted(list(sources)))
    except Exception as e:
        return f"Error listing sources: {str(e)}"

if __name__ == "__main__":
    mcp.run()
