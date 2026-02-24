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
os, sys, json, subprocess, shutil, pathlib

### 📤 Exports
def get_changed_files(), def check_tool(), def analyze_file(), def generate_review_prompt(), def main()

### 💡 Example
```python
# Example usage for coderabbit_reviewer.py
# from coderabbit_reviewer import def get_changed_files()
```
"""

#!/usr/bin/env python3
"""
Module: coderabbit_reviewer.py

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
- os
    - sys
    - json
    - subprocess
    - shutil
    - pathlib.Path

### 📤 Exports
- Function: get_changed_files
    - Function: check_tool
    - Function: analyze_file
    - Function: generate_review_prompt
    - Function: main

### 💡 Examples
```python
    # Example usage
    from coderabbit_reviewer import get_changed_files
    result = get_changed_files()
    print(result)
    ```
"""


"""
CodeRabbit Reviewer (Synchronized Intelligence Edition Global System v26 Diamond 32)
Polyglot AI Code Reviewer supporting Python, JavaScript, and TypeScript.
Integrated with Speckit Global System v26 Diamond 32 and Sentinel.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

# --- Configuration ---
MAX_FILES_TO_REVIEW = 15
REVIEW_DEPTH = "deep"

def get_changed_files():
    """Retrieves a list of changed files from git."""
    try:
        # Check if inside a git repo
        subprocess.check_call(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Get changed files (staged + unstaged)
        result = subprocess.check_output(["git", "diff", "--name-only", "HEAD"], text=True)
        files = [f for f in result.splitlines() if f.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.json'))]
        return files[:MAX_FILES_TO_REVIEW]
    except subprocess.CalledProcessError:
        # Fallback: Scan current dir for recently modified files (last 1 hour)
        # This is a simple fallback for non-git environments
        return []

def check_tool(tool_name):
    """Checks if a CLI tool is available."""
    return shutil.which(tool_name) is not None

def analyze_file(file_path):
    """Performs static analysis based on file type."""
    issues = []
    file_path_obj = Path(file_path)
    
    if not file_path_obj.exists():
        return {"file": file_path, "error": "File not found"}

    # 1. Python Analysis (flake8)
    if file_path.endswith('.py'):
        if check_tool("flake8"):
            try:
                out = subprocess.check_output(["flake8", "--format=default", file_path], text=True, stderr=subprocess.STDOUT)
                for line in out.splitlines():
                    issues.append(f"[Flake8] {line}")
            except subprocess.CalledProcessError as e:
                for line in e.output.splitlines():
                    issues.append(f"[Flake8] {line}")
        else:
            issues.append("[System] flake8 not installed. Run `pip install flake8`.")

    # 2. JS/TS Analysis (ESLint) - Optimistic check
    elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
        if check_tool("eslint"):
            try:
                # Assuming eslint is configured in the project
                out = subprocess.check_output(["eslint", "--format=compact", file_path], text=True, stderr=subprocess.STDOUT)
                for line in out.splitlines():
                    issues.append(f"[ESLint] {line}")
            except subprocess.CalledProcessError as e:
                 for line in e.output.splitlines():
                    issues.append(f"[ESLint] {line}")
        else:
            issues.append("[System] eslint not found in PATH.")

    # 3. Read Content
    try:
        content = file_path_obj.read_text(encoding='utf-8')
    except Exception as e:
        return {"file": file_path, "error": f"Read error: {e}"}

    return {
        "file": file_path,
        "issues": issues,
        "content_snippet": content  # Return full content for LLM (it handles context window)
    }

def generate_review_prompt(analysis):
    """Generates a structured prompt for the LLM."""
    if "error" in analysis:
        return f"Error analyzing {analysis['file']}: {analysis['error']}"

    prompt = f"""
    **ROLE:** You are CodeRabbit (Global System v26 Diamond 32), a Senior Staff Engineer and AI Code Reviewer.
    
    **TASK:** Review the following file: `{analysis['file']}`
    
    **STATIC ANALYSIS REPORT:**
    {json.dumps(analysis['issues'], indent=2) if analysis['issues'] else "No static analysis issues found."}
    
    **CODE CONTENT:**
    ```
    {analysis['content_snippet']}
    ```
    
    **REVIEW GUIDELINES (Global System v26 Diamond 32):**
    1. **Correctness:** Identify logic errors, edge cases, and bugs.
    2. **Security:** Spot vulnerabilities (OWASP Top 10).
    3. **Performance:** Highlight inefficient algorithms or resource leaks.
    4. **Readability:** Suggest improvements for variable naming and structure.
    5. **Actionable:** Provide specific code snippets for every suggestion.
    
    **OUTPUT FORMAT:**
    - **Summary:** One sentence overview.
    - **Critical Issues:** (If any)
    - **Suggestions:** Bullet points with code blocks.
    """
    return prompt

def main():
    """
    Main implementation.
    """
    # Output strictly JSON for MCP integration
    output = {"status": "success", "reviews": []}
    
    try:
        files = get_changed_files()
        
        if not files:
            output["message"] = "No changed files detected to review."
            print(json.dumps(output, indent=2))
            return

        for file in files:
            analysis = analyze_file(file)
            prompt = generate_review_prompt(analysis)
            output["reviews"].append({
                "file": file,
                "static_issues_count": len(analysis.get("issues", [])),
                "llm_prompt": prompt
            })
            
    except Exception as e:
        output["status"] = "error"
        output["message"] = str(e)

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
