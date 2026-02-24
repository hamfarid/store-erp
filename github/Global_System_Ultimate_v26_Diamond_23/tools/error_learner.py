#!/usr/bin/env python3
"""
### 📊 Logical Chart
graph TD
    A[Error Detected] --> B{Check Attempt Count}
    B -->|1st Attempt| C[Log Error & Retry Standard]
    B -->|2nd Attempt| D[Consult lessons.md & Analyze]
    D --> E[Retry with New Strategy]
    B -->|3rd Attempt| F[STOP & Escalate]
    F --> G[Write to lessons.md]
    G --> H[Request Human Intervention]

### Workflow
1.  **Capture Error:** Receive error details and context.
2.  **Check History:** Determine how many times this specific error has occurred recently.
3.  **Escalate:**
    *   **Tier 1:** Simple retry.
    *   **Tier 2:** Deep analysis using RAG (Retrieval Augmented Generation) from `lessons.md`.
    *   **Tier 3:** Abort operation to prevent damage.
4.  **Learn:** Update `lessons.md` with the failure details for future reference.

### Imports
- os
- sys
- json
- datetime

### Exports
- handle_error(error_msg, context)
- log_lesson(error, solution)
"""

import os
import sys
import json
from datetime import datetime

# --- Configuration ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(ROOT_DIR, ".memory")
LESSONS_FILE = os.path.join(MEMORY_DIR, "lessons.md")
ERROR_DB = os.path.join(MEMORY_DIR, "error_history.json")

def load_history():
    if os.path.exists(ERROR_DB):
        try:
            with open(ERROR_DB, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_history(history):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(ERROR_DB, 'w') as f:
        json.dump(history, f, indent=2)

def log_lesson(error, solution, status="RESOLVED"):
    """Appends a learned lesson to the markdown journal."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
## [{timestamp}] {status}
**Error:** {error}
**Solution/Action:** {solution}
---
"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(LESSONS_FILE, "a") as f:
        f.write(entry)

def handle_error(error_msg, context=""):
    """Main entry point for error handling."""
    history = load_history()
    
    # Simple fingerprinting (could be more advanced)
    error_key = error_msg[:100] 
    
    if error_key not in history:
        history[error_key] = {"count": 0, "first_seen": str(datetime.now())}
    
    history[error_key]["count"] += 1
    count = history[error_key]["count"]
    save_history(history)
    
    print(f"🚨 Error Handler: '{error_key}...' (Attempt {count}/3)")
    
    if count == 1:
        print("🔄 Tier 1: Standard Retry. Please check syntax and imports.")
        return "RETRY"
    
    elif count == 2:
        print("🧠 Tier 2: Deep Analysis. Consulting lessons.md...")
        # Here we would ideally search lessons.md for similar errors
        # For now, we just advise the agent to read it.
        print(f"👉 ACTION REQUIRED: Read {LESSONS_FILE} for past solutions.")
        return "ANALYZE"
    
    else:
        print("🛑 Tier 3: CRITICAL STOP. Escalating to Human.")
        log_lesson(error_msg, "Escalated to human after 3 failed attempts.", status="FAILED")
        return "STOP"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(handle_error(sys.argv[1]))
    else:
        print("Usage: error_learner.py <error_message>")
