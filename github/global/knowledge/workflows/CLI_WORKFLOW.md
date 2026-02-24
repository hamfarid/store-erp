# 💻 CLI Tools & Scripts Workflow (AI Learning Guide)

This document teaches the AI how to build robust command-line utilities.

## 1. Standard Script Structure
Every CLI script (e.g., `manage.py`, `deploy.sh`) must follow this pattern:

### 📥 Imports (Inputs)
*   **Arg Parsing**: `argparse`, `click`, `typer`.
*   **System Ops**: `os`, `sys`, `subprocess`, `shutil`.
*   **Logging**: `logging`, `rich`.

### 📤 Exports (Outputs)
*   **Entry Point**: `main()` function or `if __name__ == "__main__":`.
*   **Exit Codes**: 0 (Success), Non-zero (Failure).
*   **Stdout/Stderr**: User feedback and error logs.

### 🔄 Operational Workflow
1.  **Parse Arguments**: Read flags and options from command line.
2.  **Validation**: Check inputs and environment (Pre-flight).
3.  **Execution**: Run the core logic.
4.  **Feedback**: Print progress and results.
5.  **Exit**: Return appropriate status code.

## 2. Example: File Renamer Tool

```python
# tools/renamer.py

# 📥 IMPORTS
import argparse
import os
import sys

# 🔄 WORKFLOW
# 1. Parse --target and --prefix args.
# 2. Walk through directory.
# 3. Rename files.
# 4. Print summary.

# 📤 EXPORTS
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--prefix", default="new_")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        print("❌ Target not found.")
        sys.exit(1)

    for f in os.listdir(args.target):
        old = os.path.join(args.target, f)
        new = os.path.join(args.target, args.prefix + f)
        os.rename(old, new)
        print(f"✅ Renamed: {f} -> {args.prefix + f}")

if __name__ == "__main__":
    main()
```

## 3. AI Action Items
*   **Help Message**: Always provide `-h/--help` documentation.
*   **Idempotency**: Scripts should be safe to run multiple times.
*   **Interactivity**: Use `input()` for dangerous operations (or `--force` flag).
