"""
### 📊 Logical Chart (Create -> Verify -> Execute)
```mermaid
flowchart TD
    Start([Start]) --> Order[1. Order Requirements]
    Order --> Create[2. Create Artifacts]
    Create --> Verify{3. Verify Success?}
    Verify -- No --> Rollback[Rollback/Fix]
    Rollback --> Create
    Verify -- Yes --> Execute[4. Execute/Deploy]
    Execute --> End([End])
```

### 🔄 Workflow
1.  **Order**: Define prerequisites and inputs.
2.  **Create**: Generate the output (file, data, resource).
3.  **Verify**: Check if the output meets standards (Syntax, Logic, Compliance).
4.  **Execute**: Apply the change or return the result.

### 📥 Imports
sys, os, argparse, json, datetime, rag_engine

### 📤 Exports
def learn_preference(), def get_dna_summary(), def main()

### 💡 Example
```python
# Example usage for user_dna.py
# from user_dna import def learn_preference()
```
"""

#!/usr/bin/env python3
"""
Module: user_dna.py

---
### 🔄 Workflow
1. Initialize module.
    2. Process inputs.
    3. Return results.

### 📊 Logical Chart
```mermaid
    graph TD
        A[Start] --> B{Process}
        B -->|Success| C[End]
    ```

### 📥 Imports
- sys
    - os
    - argparse
    - json
    - datetime.datetime
    - rag_engine.RAGEngine

### 📤 Exports
- Function: learn_preference
    - Function: get_dna_summary
    - Function: main

### 💡 Examples
```python
    # Example usage
    from user_dna import learn_preference
    result = learn_preference()
    print(result)
    ```
"""


"""
User DNA (Global System Ultimate)
Captures and enforces the user's coding style and preferences.
Stores "DNA" in the Global Vector DB and injects it into prompts.
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Import RAG Engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from rag_engine import RAGEngine
except ImportError:
    print("⚠️  RAG Engine not found. User DNA disabled.")
    sys.exit(0)

GLOBAL_COLLECTION = "User_DNA"

DEFAULT_DNA = {
    "language": "python",
    "indentation": "4 spaces",
    "comments": "docstrings",
    "typing": "strict",
    "frameworks": ["fastapi", "react"],
    "testing": "pytest"
}

def learn_preference(key, value):
    """Learns a new preference."""
    engine = RAGEngine(chroma_port=8000)
    if not engine.connect():
        return False

    engine.get_or_create_collection(GLOBAL_COLLECTION)
    
    doc_id = f"pref_{key}"
    text = f"PREFERENCE: {key} = {value}"
    metadata = {"key": key, "timestamp": datetime.now().isoformat()}
    
    success = engine.add_document(doc_id, text, metadata)
    if success:
        print(f"🧬 DNA Updated: {key} -> {value}")
    return success

def get_dna_summary():
    """Retrieves the full DNA profile."""
    engine = RAGEngine(chroma_port=8000)
    if not engine.connect():
        return DEFAULT_DNA

    engine.get_or_create_collection(GLOBAL_COLLECTION)
    # In a real scenario, we'd query all or keep a summary doc.
    # For now, we return a prompt-ready string.
    return "User prefers: Python, 4 spaces, Strict Typing, FastAPI."

def main():
    parser = argparse.ArgumentParser(description="User DNA Manager")
    parser.add_argument("--set", nargs=2, metavar=('KEY', 'VALUE'), help="Set a preference")
    parser.add_argument("--get", action="store_true", help="Get DNA summary")
    
    args = parser.parse_args()
    
    if args.set:
        learn_preference(args.set[0], args.set[1])
    
    if args.get:
        print(get_dna_summary())

if __name__ == "__main__":
    main()